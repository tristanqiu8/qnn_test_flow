import os, shutil
import argparse as ap
import numpy as np
import onnxruntime as ort
from onnxruntime.datasets import get_example


def init():  # step 0: initialize a qnn sdk environment
    # QNN_SDK_ROOT is preset in ~/.bashrc
    os.system("bash $QNN_SDK_ROOT/init.sh")
    # os.system("source $QNN_SDK_ROOT/target/x86_64-linux-clang/bin/envsetup.sh")


def test(args):
    if not os.path.exists(args.out_dir):
        os.mkdir(args.out_dir)
    else:
        shutil.rmtree(args.out_dir)
        os.mkdir(args.out_dir)
    for root, dirnames, filenames in os.walk(args.in_dir):
        for filename in filenames:
            if filename.endswith("prototxt"):
                proto_path = os.path.join(root, filename)
                expect_param_path = proto_path.split(".")[0] + ".caffemodel"
                # out_onnx_path = proto_path.split(".")[0] + ".onnx"
                assert os.path.exists(expect_param_path)
                model_name = filename.split(".")[0]
                # print("Running model: " + model_name)
                
                # step 1: convert caffe to onnx
                model_dir = os.path.join(args.out_dir, model_name)
                if not os.path.exists(model_dir):
                    os.mkdir(model_dir)
                onnx_tmp_path = os.path.abspath(os.path.join(model_dir, model_name + "_tmp.onnx"))
                onnx_path = os.path.abspath(os.path.join(model_dir, model_name + ".onnx"))
                os.system("/home/titan/anaconda3/envs/qnn2/bin/python" + " -m caffe2onnx.convert"
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
                os.system("qnn-onnx-converter --input_network " + onnx_path + " --output_path " 
                          + cpp_path + " --input_list " + pc_input_list_path)
                # stage 2: clang and generate .so
                os.system("source $QNN_SDK_ROOT/target/x86_64-linux-clang/bin/envsetup.sh")
                model_bin_path  = os.path.abspath(os.path.join(model_dir, bin_fname))
                os.system("qnn-model-lib-generator -c " + cpp_path +
                          " -b " +  model_bin_path + " -o" + model_dir)

                # step 5: push to the pdb
                model_lib_fname = "lib" + model_name + ".so"
                lib_dir = os.path.join(model_dir, "aarch64-android")
                model_lib_path = os.path.join(lib_dir, model_lib_fname)
                assert os.path.exists(model_lib_path)
                # os.environ['QNN_TARGET_ARCH'] = "aarch64-android"
                os.environ['MODEL_LIB'] = lib_dir
                os.environ['MODEL_DIR'] = model_dir
                os.environ['MODEL_NAME'] = model_name
                # os.environ['QAUNT_MODEL_NAME'] = model_lib_fname
                # import pdb; pdb.set_trace()
                os.system("bash run_single_model.sh")


def main():
    parser = ap.ArgumentParser()
    parser.add_argument("--in_dir", help='target test case dir (caffe)', required=True)
    parser.add_argument("--out_dir", help='target dump directory', default="./test_dump")
    parser.add_argument("--mode", help="test run mode", default="normal")
    args = parser.parse_args()
    init()
    test(args)


if __name__=="__main__":
    main()