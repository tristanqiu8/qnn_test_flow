import os, shutil
import argparse as ap
import json
import numpy as np
import onnxruntime as ort
from onnxruntime.datasets import get_example


def init():
    os.system("source /home/tristan/.bashrc")

def run(args):
    if not os.path.exists(args.out_dir):
        os.mkdir(args.out_dir)
    else:
        shutil.rmtree(args.out_dir)
        os.mkdir(args.out_dir)
    
    if args.fxp == "i8" or "i16":
        default_conf_path = './conf/vtcm_config_i8.json'
    elif args.fxp == "fp16":
        default_conf_path = './conf/vtcm_config_fp.json'
    else:
        assert False, "fxp type not supported"

    with open(default_conf_path, 'r') as load_f:
        json_cfg_dict =json.load(load_f)
    load_f.close()

    for root, dirnames, filenames in os.walk(args.in_dir):
        for filename in filenames:
            model_found = False
                
            if filename.endswith("onnx"):
                model_name = filename.split(".")[0]
                model_path = os.path.abspath(os.path.join(root, filename))
                model_dir = os.path.abspath(os.path.join(args.out_dir, model_name))
                encoding_name = model_name + ".encodings"
                encoding_path = os.path.abspath(os.path.join(root, encoding_name))
                if not os.path.exists(model_dir):
                    os.mkdir(model_dir)
                onnx_path = os.path.abspath(os.path.join(model_dir, model_name + ".onnx"))
                os.system("cp " + model_path + " " + onnx_path)
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
                    input_shape[0] = args.batch
                print("new input shape", input_shape)
                x = np.random.random(input_shape)
                x = x.astype(np.float32)
                raw_input_path = os.path.abspath(os.path.join(model_dir, model_name + "_input.raw"))
                x.tofile(raw_input_path)
                input_list_path = os.path.join(model_dir, model_name + "_input_list.txt")
                pc_input_list_path = os.path.join(model_dir, model_name + "_pc_input_list.txt")
                f = open(input_list_path, 'w')
                f.write("/data/local/tmp/model/" + model_name + "_input.raw")
                f.close()
                f = open(pc_input_list_path, 'w')
                f.write(raw_input_path)
                f.close()

                # step 3: model compilation
                # stage 1: converter/nn compile
                cpp_fname = model_name + ".cpp"
                bin_fname = model_name + ".bin"
                cpp_path = os.path.abspath(os.path.join(model_dir, cpp_fname))
                # os.system("source $QNN_SDK_ROOT/target/x86_64-linux-clang/bin/envsetup.sh")
                if encoding_found:
                    os.system("qnn-onnx-converter --input_network " + onnx_path + " --output_path " 
                                + cpp_path + " --input_list " + pc_input_list_path +
                                " --quantization_overrides " + encoding_path + " --arch_checker")
                else:
                    if args.fxp == "i8" or args.fxp == "i16":
                        cmd = (
                            f"qnn-onnx-converter --input_network {onnx_path} --input_list {pc_input_list_path} --output_path {cpp_path} --act_bitwidth {args.fxp[1:]}"
                            f" --weights_bitwidth 8 --bias_bitwidth 32 --input_dim {input_name} {input_shape[0]},{input_shape[1]},{input_shape[2]},{input_shape[3]}"
                        )
                    elif args.fxp == "fp16":
                        cmd = (
                            f"qnn-onnx-converter --input_network {onnx_path} --input_list {pc_input_list_path} --output_path {cpp_path} --float_bitwidth 16"
                            f" --input_dim {input_name} {input_shape[0]},{input_shape[1]},{input_shape[2]},{input_shape[3]}"
                        )
                    print(f"onnx conversion cmd is: {cmd}")
                    os.system(cmd)
                # stage 2: clang and generate .so
                model_bin_path  = os.path.abspath(os.path.join(model_dir, bin_fname))
                # import pdb; pdb.set_trace()
                os.system("qnn-model-lib-generator -c " + cpp_path + " -b " +  model_bin_path + " -o " + model_dir)
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
                cmd = (
                    f"qnn-context-binary-generator --model {so_path} --backend libQnnHtp.so --binary_file {binary_fname} "
                    f"--output_dir {model_dir} --config_file htp_extension.json"
                )
                print("qnn-context-binary-generator cmd is: ", cmd)
                os.system(cmd)
                os.chdir(cur_dir)

                # step 4: push to the pdb
                # os.environ['MODEL_LIB'] = lib_dir
                # os.environ['MODEL_DIR'] = model_dir
                # os.environ['MODEL_NAME'] = model_name
                # os.environ['QNN_APP'] = args.app
                # os.system("bash run_single_adb.sh")
                # # parse the detailed result
                # log_path = os.path.abspath(os.path.join(model_dir, "output_detailed/qnn-profiling-data_0.log"))
                # parse_txt_path = os.path.abspath(os.path.join(model_dir, "qnn-profiling.txt"))
                # parse_csv_path = os.path.abspath(os.path.join(model_dir, "qnn-profiling.csv"))
                # os.system("./lib/x86_64-linux-clang/qnn-profile-viewer --input_log=" + log_path +
                #             " --output=" + parse_csv_path +
                #             " --reader=$QNN_SDK_ROOT/lib/x86_64-linux-clang/libQnnHtpProfilingReader.so > " + parse_txt_path)


def main():
    parser = ap.ArgumentParser()
    parser.add_argument("--in_dir", help='target test case dir (ONNX)', default="./depthwise")
    parser.add_argument("--out_dir", help='target dump directory', default="./test_dump")
    parser.add_argument("--app", help="test run app", default="qnn-net-run")
    parser.add_argument("--format", help="build format: .so or seriealized .bin", default="bin")
    parser.add_argument("--sram", help="sram size, unit MB, up to 8", type=int, default=0)
    parser.add_argument("--fxp", help="fxp type: i8, i16, or fp16", default="i8")
    parser.add_argument("--batch", help="change batch size", type=int, default=2)
    parser.add_argument("--pm", help="power mode", default="burst")
    args = parser.parse_args()
    run(args)


if __name__=="__main__":
    main()
