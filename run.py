import os, shutil
import argparse as ap
import json
import numpy as np
import onnxruntime as ort
from onnxruntime.datasets import get_example


def init():  # step 0: initialize a qnn sdk environment
    # QNN_SDK_ROOT is preset in ~/.bashrc
    os.system("source $QNN_SDK_ROOT/init.sh")


def test(args):
    if not os.path.exists(args.out_dir):
        os.mkdir(args.out_dir)
    else:
        shutil.rmtree(args.out_dir)
        os.mkdir(args.out_dir)
    
    with open('./conf/HtpConfigFile.json', 'r') as load_f:
        default_cfg_dict =json.load(load_f)
    load_f.close()

    for root, dirnames, filenames in os.walk(args.in_dir):
        for filename in filenames:
            model_found = False
            if filename.endswith("prototxt"):
                encoding_found = False
                proto_path = os.path.abspath(os.path.join(root, filename))
                expect_param_path = proto_path.split(".")[0] + ".caffemodel"
                # out_onnx_path = proto_path.split(".")[0] + ".onnx"
                if not os.path.exists(expect_param_path):
                    print(expect_param_path + " is not found! Current test skip")
                    continue
                model_name = filename.split(".")[0]
                # print("Running model: " + model_name)
                
                # step 1: convert caffe to onnx
                model_dir = os.path.abspath(os.path.join(args.out_dir, model_name))
                if not os.path.exists(model_dir):
                    os.mkdir(model_dir)
                onnx_tmp_path = os.path.abspath(os.path.join(model_dir, model_name + "_tmp.onnx"))
                onnx_path = os.path.abspath(os.path.join(model_dir, model_name + ".onnx"))
                ret = os.system("python" + " -m caffe2onnx.convert"
                           + " --prototxt " + proto_path + " --caffemodel " + expect_param_path
                           + " --onnx " + onnx_tmp_path)
                if ret:
                    print("caffe2onnx for case " + model_name + " failed! Skip the test")
                    continue
                ret = os.system("python remove_initializer_from_input.py --input " + onnx_tmp_path + " --output " + onnx_path)
                if ret:
                    print("remove_initializer_from_input for case " + model_name + " failed! Skip the test")
                    continue
                os.remove(onnx_tmp_path)
                model_found = True
                
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
                # print("input shape", input_shape)
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
                os.system("source $QNN_SDK_ROOT/target/x86_64-linux-clang/bin/envsetup.sh")
                if encoding_found:
                    os.system("qnn-onnx-converter --input_network " + onnx_path + " --output_path " 
                                + cpp_path + " --input_list " + pc_input_list_path +
                                " --quantization_overrides " + encoding_path + " --arch_checker")
                else:
                    os.system("qnn-onnx-converter --input_network " + onnx_path + " --output_path " 
                                + cpp_path + " --input_list " + pc_input_list_path + " --arch_checker")
                # stage 2: clang and generate .so
                model_bin_path  = os.path.abspath(os.path.join(model_dir, bin_fname))
                # import pdb; pdb.set_trace()
                os.system("qnn-model-lib-generator -c " + cpp_path + " -b " +  model_bin_path + " -o " + model_dir)
                # stage 3: serialized
                model_lib_fname = "lib" + model_name + ".so"
                binary_fname = "ctx_" + model_name
                lib_dir = os.path.join(model_dir, "x86_64-linux-clang")
                so_path = os.path.abspath(os.path.join(lib_dir, model_lib_fname))
                # os.system("cp ./conf/HtpConfigFile.json " + model_dir)

                with open("./conf/PerfSetting_sample.conf", 'r') as load_f:
                    perf_conf_dict = json.load(load_f)
                load_f.close()
                perf_conf_dict['graphs']['graph_names'] = [model_name]
                perf_conf_dict['graphs']['vtcm_mb'] = args.sram
                PerfSetting_Conf_fpath = os.path.abspath(os.path.join(model_dir, "PerfSetting.conf"))
                with open(PerfSetting_Conf_fpath, 'w') as dump_f:
                    json.dump(perf_conf_dict, dump_f, indent=4, ensure_ascii=False)
                dump_f.close()
                cfg_dict = default_cfg_dict
                cfg_dict['backend_extensions']['config_file_path'] = PerfSetting_Conf_fpath
                HtpConfigFile_path = os.path.abspath(os.path.join(model_dir, "HtpConfigFile.json"))
                with open(HtpConfigFile_path, 'w') as dump_f:
                    json.dump(cfg_dict, dump_f, indent=4, ensure_ascii=False)
                dump_f.close()
                cfg_dict['backend_extensions']['config_file_path'] = "/data/local/tmp/model/PerfSetting.conf"
                HtpConfigFile_local_path = os.path.abspath(os.path.join(model_dir, "HtpConfigFile_local.json"))
                with open(HtpConfigFile_local_path, 'w') as dump_f:
                    json.dump(cfg_dict, dump_f, indent=4, ensure_ascii=False)
                dump_f.close()
                if args.sram:
                    os.system("qnn-context-binary-generator -backend $QNN_SDK_ROOT/target/x86_64-linux-clang/lib/libQnnHtp.so --model "
                            + so_path + " --binary_file " + binary_fname + " --log_level verbose --output_dir " +
                            model_dir + " --config_file " + HtpConfigFile_path)
                else:
                    os.system("qnn-context-binary-generator -backend $QNN_SDK_ROOT/target/x86_64-linux-clang/lib/libQnnHtp.so --model "
                            + so_path + " --binary_file " + binary_fname + " --log_level verbose --output_dir " +
                            model_dir)
                
                # step 4: push to the pdb
                # os.environ['MODEL_LIB'] = lib_dir
                os.environ['MODEL_DIR'] = model_dir
                os.environ['MODEL_NAME'] = model_name
                os.environ['QNN_APP'] = args.app
                os.system("bash run_single_adb.sh")
                # parse the detailed result
                log_path = os.path.abspath(os.path.join(model_dir, "output_detailed/qnn-profiling-data_0.log"))
                parse_txt_path = os.path.abspath(os.path.join(model_dir, "qnn-profiling.txt"))
                parse_csv_path = os.path.abspath(os.path.join(model_dir, "qnn-profiling.csv"))
                os.system("./lib/x86_64-linux/bin/qnn-profile-viewer --input_log=" + log_path +
                            " --output=" + parse_csv_path +
                            " --reader=./lib/x86_64-linux/lib/libQnnHtpProfilingReader.so > " + parse_txt_path)
                # import pdb; pdb.set_trace()


def main():
    parser = ap.ArgumentParser()
    parser.add_argument("--in_dir", help='target test case dir (Caffe)', required=True)
    parser.add_argument("--out_dir", help='target dump directory', default="./test_dump")
    parser.add_argument("--app", help="test run app", default="qnn-max100-app")
    parser.add_argument("--format", help="build format: .so or seriealized .bin", default="bin")
    parser.add_argument("--sram", help="sram size, unit MB, up to 8", type=int, default=0)
    args = parser.parse_args()
    init()
    test(args)


if __name__=="__main__":
    main()
