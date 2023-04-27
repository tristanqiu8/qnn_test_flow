import os, shutil
import argparse as ap
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
    for root, dirnames, filenames in os.walk(args.in_dir):
        for filename in filenames:
            if filename.endswith("prototxt"):
                proto_path = os.path.abspath(os.path.join(root, filename))
                expect_param_path = proto_path.split(".")[0] + ".caffemodel"
                # out_onnx_path = proto_path.split(".")[0] + ".onnx"
                assert os.path.exists(expect_param_path)
                model_name = filename.split(".")[0]
                # print("Running model: " + model_name)
                
                # step 1: convert caffe to onnx
                model_dir = os.path.abspath(os.path.join(args.out_dir, model_name))
                if not os.path.exists(model_dir):
                    os.mkdir(model_dir)
                onnx_tmp_path = os.path.abspath(os.path.join(model_dir, model_name + "_tmp.onnx"))
                onnx_path = os.path.abspath(os.path.join(model_dir, model_name + ".onnx"))
                os.system("python" + " -m caffe2onnx.convert"
                           + " --prototxt " + proto_path + " --caffemodel " + expect_param_path
                           + " --onnx " + onnx_tmp_path)
                os.system("python remove_initializer_from_input.py --input " + onnx_tmp_path + " --output " + onnx_path)
                os.remove(onnx_tmp_path)
                
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
                os.system("bash $QNN_SDK_ROOT/target/x86_64-linux-clang/bin/envsetup.sh")
                os.system("qnn-onnx-converter --input_network " + onnx_path + " --output_path " 
                          + cpp_path + " --input_list " + pc_input_list_path)
                # stage 2: clang and generate .so
                model_bin_path  = os.path.abspath(os.path.join(model_dir, bin_fname))
                # import pdb; pdb.set_trace()
                # cmd = "qnn-model-lib-generator -c " + cpp_path + " -b " +  model_bin_path + " -o" + model_dir
                os.system("qnn-model-lib-generator -c " + cpp_path +
                          " -b " +  model_bin_path + " -o" + model_dir)
                # stage 3: serialized
                model_lib_fname = "lib" + model_name + ".so"
                binary_fname = "ctx_" + model_name
                lib_dir = os.path.join(model_dir, "x86_64-linux-clang")
                so_path = os.path.abspath(os.path.join(lib_dir, model_lib_fname))
                os.system("qnn-context-binary-generator -backend $QNN_SDK_ROOT/target/x86_64-linux-clang/lib/libQnnHtp.so --model "
                          + so_path + " --binary_file " + binary_fname + " --log_level verbose --output_dir " +
                          model_dir)
                # import pdb; pdb.set_trace()
                
                # step 4: push to the pdb
                # os.environ['MODEL_LIB'] = lib_dir
                os.environ['MODEL_DIR'] = model_dir
                os.environ['MODEL_NAME'] = model_name
                # lib_dir = os.path.join(model_dir, "aarch64-android")
                # model_lib_path = os.path.join(lib_dir, model_lib_fname)
                # assert os.path.exists(model_lib_path)
                # import pdb; pdb.set_trace()
                os.system("bash run_perf.sh")
                # import pdb; pdb.set_trace()


def main():
    parser = ap.ArgumentParser()
    parser.add_argument("--in_dir", help='target test case dir (Caffe)', required=True)
    parser.add_argument("--out_dir", help='target dump directory', default="./test_dump")
    parser.add_argument("--mode", help="test run mode", default="normal")
    args = parser.parse_args()
    init()
    test(args)


if __name__=="__main__":
    main()