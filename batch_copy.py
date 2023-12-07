import os
import shutil


def run_copy(in_dir, dump_dir):
    if not os.path.exists(dump_dir):
        os.makedirs(dump_dir)
        
    for root, _, filenames in os.walk(in_dir):
        for filename in filenames:
            # if filename.endswith("int8_input.raw"):
            #     # model_name = root.split("/")[2]
            #     model_name = filename.split(".")[0][:-11]
            #     case_dir = os.path.join(dump_dir, model_name)
            #     if not os.path.exists(case_dir):
            #         os.makedirs(case_dir)
            #     src_path = os.path.join(root, filename)
            #     des_path = os.path.join(case_dir, filename)
            #     shutil.copy(src_path, des_path)
            #     filename = "ctx_" + model_name + ".serial.bin"
            #     src_path = os.path.join(root, filename)
            #     des_path = os.path.join(case_dir, filename)
            #     shutil.copy(src_path, des_path)
            
            if filename.endswith(".onnx"):
                # model_name = root.split("/")[2]
                model_name = filename.split(".")[0]
                case_dir = os.path.join(dump_dir, model_name)
                if not os.path.exists(case_dir):
                    os.makedirs(case_dir)
                src_path = os.path.join(root, filename)
                des_path = os.path.join(case_dir, filename)
                shutil.copy(src_path, des_path)

            
if __name__ == "__main__":
    in_dir = "./benchmark_build/constructed_case"
    # dump_dir = "./light_bm_build_stage2"
    dump_dir = "./benchmark/03_Constructed_ONNX"
    run_copy(in_dir, dump_dir)