import os, shutil, sys, io
import argparse as ap
import json
import numpy as np
import onnxruntime as ort
from onnxruntime.datasets import get_example
import subprocess

soc_mapping = {"v73": 43, "v75": 57, "v79": 69}
qnn_test_dir_v73 = "/data/local/tmp/qnn_test_234/"
qnn_test_dir_v79 = "/data/local/tmp/qnn_test_234/"

def init():
    os.system("source /home/tristan/.bashrc")

def sys_call(cmd):
    result = subprocess.run(
                        cmd,
                        capture_output=True,  # 捕获标准输出和标准错误
                        shell=True,           # 使用 shell 执行命令
                        check=True,           # 如果命令返回非零退出码，则抛出异常
                        # timeout=200, 
                        text=True             # 将输出作为字符串返回
                    )
    if result.stdout:
        print("STDOUT:", result.stdout)
    if result.stderr:
        print("STDERR:", result.stderr)

def run(args):
    if not os.path.exists(args.out_dir):
        os.mkdir(args.out_dir)

    if args.arch == "v73":
        qnn_test_dir = qnn_test_dir_v73
    elif args.arch == "v79":
        qnn_test_dir = qnn_test_dir_v79
    else:
        assert False, "arch not supported"

    if args.fxp == "i8" or args.fxp == "i16":
        default_conf_path = './conf/vtcm_config_i8.json'
    elif args.fxp == "fp16":
        default_conf_path = './conf/vtcm_config_fp.json'
    else:
        assert False, "fxp type not supported"

    with open(default_conf_path, 'r') as load_f:
        json_cfg_dict =json.load(load_f)
    load_f.close()
    json_cfg_dict['devices'][0]['dsp_arch'] = args.arch
    json_cfg_dict['devices'][0]['soc_id'] = soc_mapping[args.arch]

    for root, dirnames, filenames in os.walk(args.in_dir):
        for filename in filenames:
            model_found = False
                
            if filename.endswith("onnx"):
                import onnx_tool
                model_name = filename.split(".")[0]
                model_path = os.path.abspath(os.path.join(root, filename))
                model_dir = os.path.abspath(os.path.join(args.out_dir, f"{model_name}_{args.pm}_{args.fxp}_B{args.batch}_{args.arch}_{args.app}"))
                encoding_name = model_name + ".encodings"
                encoding_path = os.path.abspath(os.path.join(root, encoding_name))
                if not os.path.exists(model_dir):
                    os.mkdir(model_dir)
                else:  # whether remove evethings in the out_dir
                    shutil.rmtree(model_dir)
                    os.mkdir(model_dir)
                onnx_path = os.path.abspath(os.path.join(model_dir, model_name + ".onnx"))
                sys_call("cp " + model_path + " " + onnx_path)
                stat_file = os.path.abspath(os.path.join(model_dir, model_name + "_macs.txt"))
                # 捕获 stdout
                old_stdout = sys.stdout
                sys.stdout = captured_output = io.StringIO()

                # 执行 profiling
                stats = onnx_tool.model_profile(model_path)

                # 恢复 stdout
                sys.stdout = old_stdout

                # 将捕获的输出写入文件
                with open(stat_file, "w") as f:
                    f.write(captured_output.getvalue())

                model_found = True
                if os.path.exists(encoding_path):
                    encoding_found = True
                else:
                    encoding_found = False
                
            if model_found:
                # step 2: prepare input.raw and its file txt
                example = get_example(onnx_path)
                sess = ort.InferenceSession(example, providers=ort.get_available_providers())
                assert(len(sess.get_inputs()) == 1)  # handles only one input case as for now
                # input_name = sess.get_inputs()[0].name
                # print("input name", input_name)
                input_shape = sess.get_inputs()[0].shape
                input_name = sess.get_inputs()[0].name
                print("onnx input shape", input_shape)
                if args.batch != 1:
                    input_shape[0] = args.batch * input_shape[0]
                print("new input shape", input_shape)

                if args.fxp == "i8":
                    x = np.random.randint(-128, 127, size=input_shape).astype(np.int8)
                elif args.fxp == "i16":
                    x = np.random.randint(-32768, 32767, size=input_shape).astype(np.int16)
                elif args.fxp == "fp16":
                    x = np.random.randn(input_shape[0], input_shape[1], input_shape[2],input_shape[3]).astype(np.float16)
                input_file = f"{input_shape[0]}x{input_shape[1]}x{input_shape[2]}x{input_shape[3]}_{args.fxp}.raw"
                raw_input_path = os.path.abspath(os.path.join(model_dir, input_file))
                x.tofile(raw_input_path)
                input_list_path = os.path.join(model_dir, model_name + "_input_list.txt")
                pc_input_list_path = os.path.join(model_dir, model_name + "_pc_input_list.txt")
                f = open(input_list_path, 'w')
                f.write(qnn_test_dir + input_file)
                f.close()
                f = open(pc_input_list_path, 'w')
                f.write(raw_input_path)
                f.close()

                # step 3: model compilation
                # stage 1: converter/nn compile
                cpp_fname = model_name + ".cpp"
                bin_fname = model_name + ".bin"
                cpp_path = os.path.abspath(os.path.join(model_dir, cpp_fname))
                if encoding_found:
                    if args.fxp == "i8" or args.fxp == "i16":
                        cmd = (
                                f"qnn-onnx-converter --input_network {onnx_path} --input_list {pc_input_list_path} --output_path {cpp_path} "
                                f"--quantization_overrides {encoding_path} --input_dim {input_name} {input_shape[0]},{input_shape[1]},{input_shape[2]},{input_shape[3]}"
                        )
                    else:
                        print("fp16 not supported for encoding")
                        exit(-1)
                else:
                    if args.fxp == "i8" or args.fxp == "i16":
                        cmd = (
                            f"qnn-onnx-converter --input_network {onnx_path} --input_list {pc_input_list_path} --output_path {cpp_path} --act_bitwidth {args.fxp[1:]}"
                            f" --weights_bitwidth 8 --bias_bitwidth 32 --input_dim {input_name} {input_shape[0]},{input_shape[1]},{input_shape[2]},{input_shape[3]}"
                        )
                    elif args.fxp == "fp16":
                        cmd = (
                            f"qnn-onnx-converter --input_network {onnx_path} --output_path {cpp_path} --float_bitwidth 16"
                            f" --input_dim {input_name} {input_shape[0]},{input_shape[1]},{input_shape[2]},{input_shape[3]}"
                        )
                print(f"onnx conversion cmd is: {cmd}")
                sys_call(cmd)
                # stage 2: clang and generate .so
                model_bin_path  = os.path.abspath(os.path.join(model_dir, bin_fname))
                cmd = "qnn-model-lib-generator -c " + cpp_path + " -b " +  model_bin_path + " -o " + model_dir
                print("qnn-model-lib-generator cmd is: ", cmd)
                os.system(cmd)
                # stage 3: serialized
                model_lib_fname = "lib" + model_name + ".so"
                binary_fname = "lib_" + model_name
                lib_dir = os.path.join(model_dir, "x86_64-linux-clang")
                so_path = os.path.abspath(os.path.join(lib_dir, model_lib_fname))

                # with open("./conf/PerfSetting_sample.conf", 'r') as load_f:
                #     perf_conf_dict = json.load(load_f)
                # load_f.close()
                json_cfg_dict['graphs'][0]['graph_names'] = [model_name]
                if args.sram:
                    json_cfg_dict['graphs'][0]['vtcm_mb'] = args.sram
                json_cfg_dict["devices"][0]["cores"][0]["perf_profile"] = args.pm
                VTCM_Conf_fpath = os.path.abspath(os.path.join(model_dir, "vtcm_config.json"))
                with open(VTCM_Conf_fpath, 'w') as dump_f:
                    json.dump(json_cfg_dict, dump_f, indent=4, ensure_ascii=False)
                os.system("cp ./conf/htp_extension.json " + model_dir)
                cur_dir = os.getcwd()
                os.chdir(model_dir)
                if args.app == "profiler":
                    cmd = (
                        f"qnn-context-binary-generator --model {so_path} --backend libQnnHtp.so --binary_file {binary_fname} "
                        f"--profiling_level detailed --profiling_option optrace "
                        f"--output_dir {model_dir} --config_file htp_extension.json"
                    )
                else:
                    cmd = (
                        f"qnn-context-binary-generator --model {so_path} --backend libQnnHtp.so --binary_file {binary_fname} "
                        f"--output_dir {model_dir} --config_file htp_extension.json"
                    )
                print("qnn-context-binary-generator cmd is: ", cmd)
                sys_call(cmd)
                # os.chdir(cur_dir)

                # step 4: execute the model
                if args.app == "qnn-net-run":
                    print("qnn-net-run test mode...")
                    print("prepare the case")
                    cmd = f"adb push {binary_fname}.bin {qnn_test_dir}."
                    subprocess.run([cmd], capture_output=True, shell=True, check=True, text=True)
                    cmd = f"adb push {input_file} {qnn_test_dir}."
                    subprocess.run([cmd], capture_output=True, shell=True, check=True, text=True)
                    cmd = f"adb push {input_list_path} {qnn_test_dir}."
                    subprocess.run([cmd], capture_output=True, shell=True, check=True, text=True)
                    cmd = f"adb push htp_extension.json {qnn_test_dir}."
                    subprocess.run([cmd], capture_output=True, shell=True, check=True, text=True)
                    cmd = f"adb push vtcm_config.json {qnn_test_dir}."
                    subprocess.run([cmd], capture_output=True, shell=True, check=True, text=True)
                    print("run qnn-net-run")
                    # 构造完整的命令字符串
                    command = (
                        f"adb shell '"
                        f"cd {qnn_test_dir} && "
                        f"export LD_LIBRARY_PATH=./ && "
                        f"export ADSP_LIBRARY_PATH=./ && "
                        f"rm -rf {model_name}_dump && "
                        f"./qnn-net-run --retrieve_context {binary_fname}.bin --backend libQnnHtp.so --input_list {model_name}_input_list.txt "
                        f"--use_native_input_files --use_native_output_files --output_dir {model_name}_dump "
                        f"--log_level error --config_file htp_extension.json --profiling_level basic "
                        f"--perf_profile {args.pm} --shared_buffer --duration {args.runtime} --keep_num_outputs=2"
                        "'"
                    )

                    # 执行命令
                    sys_call(command)
                    print("collecting result...")
                    # 第一步：运行 qnn-profile-viewer 并将输出重定向到文件
                    command1 = (
                        f"adb shell '"
                        f"cd {qnn_test_dir} && "
                        f"export LD_LIBRARY_PATH=./ && "
                        f"export ADSP_LIBRARY_PATH=./ && "
                        f"rm -rf {model_name}_profiling.txt && "
                        f"./qnn-profile-viewer --input_log {model_name}_dump/qnn-profiling-data.log > {model_name}_profiling.txt"
                        "'"
                    )
                    sys_call(command1)
                    # 第二步：从设备拉取生成的 profiling 文件
                    command2 = f"adb pull {qnn_test_dir}/{model_name}_profiling.txt {model_dir}/."
                    sys_call(command2)
                
                elif args.app == "sim":
                    print("qnn-net-run simulator...")
                    command = (
                        f"qnn-net-run --model ./x86_64-linux-clang/{model_lib_fname} --backend $QNN_SDK_ROOT/lib/x86_64-linux-clang/libQnnHtp.so "
                        f"--input_list {model_name}_pc_input_list.txt "
                        f"--use_native_input_files --output_dir ./sim_dump "
                        f"--log_level error --config_file htp_extension.json --profiling_level basic "
                        f"--perf_profile {args.pm} --shared_buffer --duration {args.runtime} --keep_num_outputs=2"
                    )
                    import pdb; pdb.set_trace()
                    # [ ERROR ] Unable to load backend. dlerror(): libcdsprpc.so: cannot open shared object file: No such file or directory
                    sys_call(command)
                    print("parsing result...")
                    command1 = (
                        f"qnn-profile-viewer --input_log sim_dump/qnn-profiling-data.log > qnn_profiling.txt"
                    )
                    print("qnn-profile-viewer cmd is: ", command1)
                    sys_call(command1)
                    print("qnn-net-run simulator done")
                elif args.app == "dInfer":
                    print("run dInfer")
                else:
                    print("run profiler!")
                    print("qnn-net-run test mode...")
                    print("prepare the case")
                    cmd = f"adb push {binary_fname}.bin {qnn_test_dir}."
                    subprocess.run([cmd], capture_output=True, shell=True, check=True, text=True)
                    cmd = f"adb push {input_file} {qnn_test_dir}."
                    subprocess.run([cmd], capture_output=True, shell=True, check=True, text=True)
                    cmd = f"adb push {input_list_path} {qnn_test_dir}."
                    subprocess.run([cmd], capture_output=True, shell=True, check=True, text=True)
                    cmd = f"adb push htp_extension.json {qnn_test_dir}."
                    subprocess.run([cmd], capture_output=True, shell=True, check=True, text=True)
                    cmd = f"adb push vtcm_config.json {qnn_test_dir}."
                    subprocess.run([cmd], capture_output=True, shell=True, check=True, text=True)
                    print("run qnn-net-run")
                    # 构造完整的命令字符串
                    command = (
                        f"adb shell '"
                        f"cd {qnn_test_dir} && "
                        f"export LD_LIBRARY_PATH=./ && "
                        f"export ADSP_LIBRARY_PATH=./ && "
                        f"rm -rf {model_name}_dump && "
                        f"./qnn-net-run --retrieve_context {binary_fname}.bin --backend libQnnHtp.so --input_list {model_name}_input_list.txt "
                        f"--use_native_input_files --use_native_output_files --output_dir {model_name}_dump --log_level info "
                        f"--config_file htp_extension.json --profiling_level detailed --profiling_option optrace "
                        f"--perf_profile {args.pm} --shared_buffer --duration {args.runtime} --keep_num_outputs=2"
                        "'"
                    )

                    # 执行命令
                    sys_call(command)
                    print("collecting result...")
                    command1 = f"adb pull {qnn_test_dir}/{model_name}_dump/qnn-profiling-data_0.log {model_dir}/."
                    sys_call(command1)
                    command2 = (
                               f"qnn-profile-viewer --config ../../conf/config.json "
                               f"--reader $QNN_SDK_ROOT/lib/x86_64-linux-clang/libQnnHtpOptraceProfilingReader.so "
                               f"--input_log qnn-profiling-data_0.log "
                               f"--schematic ./*_schematic.bin --output ./chrometrace.json"
                               )
                    print("qnn-profile-viewer cmd is: ", command2)
                    sys_call(command2)
                os.chdir(cur_dir)


def main():
    parser = ap.ArgumentParser()
    parser.add_argument("--in_dir", help='target test case dir (ONNX)', default="./yf_naf_block")
    parser.add_argument("--out_dir", help='target dump directory', default="./test_dump")
    parser.add_argument("--app", help="app selection: qnn-net-run, dInfer, sim, or profiler", default="qnn-net-run")
    parser.add_argument("--format", help="build format: .so or seriealized .bin", default="bin")
    parser.add_argument("--sram", help="sram size, unit MB, up to 8", type=int, default=0)
    parser.add_argument("--fxp", help="fxp type: i8, i16, or fp16", default="i8")
    parser.add_argument("--batch", help="change batch size", type=int, default=1)
    parser.add_argument("--runtime", help="# seconds to run", type=int, default=30)
    parser.add_argument("--arch", help="htp arch: v73-8Gen2, v75-8Gen3, v79-8Gen4", default='v79')
    parser.add_argument("--pm", help="power mode", default="burst")
    args = parser.parse_args()
    init()
    run(args)


if __name__=="__main__":
    main()
