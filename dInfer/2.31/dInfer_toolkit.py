import os
import argparse
from datetime import datetime
import time
import subprocess

ADB = 'adb'
DINFER_SDK_PATH = os.path.dirname(os.path.abspath(__file__))
RESULT_PATH = os.path.join(DINFER_SDK_PATH, 'result', datetime.now().strftime('%Y%m%d_%H%M%S'))
PLATFORM = os.path.basename(DINFER_SDK_PATH)
DEV_TMP_PATH = '/data/local/tmp/dInfer/'
DEV_SD_PATH = '/sdcard/gtest/dInfer/'
SYSMON_BIN = 'sysMonApp'
if PLATFORM in ["QCOM_LE", "JETSON"]:
    DEV_TMP_PATH = '/blackbox/nn_test/'
    DEV_SD_PATH = '/blackbox/nn_test/'
    SYSMON_BIN = 'sysMonAppLE'

def get_git_root_path():
    """
    获取当前仓库的git根目录
    """
    try:
        git_root = subprocess.check_output(['git', 'rev-parse', '--show-toplevel'], encoding='utf-8').strip()
        print("Git root directory is:", git_root)
        return git_root
    except subprocess.CalledProcessError:
        print("Error: Not a git repository (or any of the parent directories)")
        return None
    
def cmd_runner(cmd_list, assert_result = True):
    for cmd in cmd_list:
        print(cmd)
        result = os.system(cmd)
        if assert_result:
            assert result == 0, f'命令执行错误: {cmd}'

def push_data(data_path=None):
    if data_path is None:
        data_path = f'{DINFER_SDK_PATH}/data'

    cmd_list = []
    cmd_list.append(f'{ADB} shell "rm -rf {DEV_SD_PATH}/data && mkdir -p {DEV_SD_PATH}/data"')

    if os.path.isdir(data_path):
        cmd_list.append(f'{ADB} push {data_path}/. {DEV_SD_PATH}/data')
    else:
        print(f"{data_path} not found, skip push")

    cmd_runner(cmd_list)

def push_lib():
    cmd_list = []
    cmd_list.append(f'{ADB} shell "rm -rf {DEV_TMP_PATH}/lib && mkdir -p {DEV_TMP_PATH}/lib"')

    libs_dir = f"{DINFER_SDK_PATH}/libs"
    if os.path.isdir(libs_dir):
        cmd_list.append(f'{ADB} push {libs_dir}/. {DEV_TMP_PATH}/lib')
    else:
        print(f"{libs_dir} not found, skip push")
        
    lib_dir = f"{DINFER_SDK_PATH}/lib"
    if os.path.isdir(lib_dir):
        cmd_list.append(f'{ADB} push {lib_dir}/. {DEV_TMP_PATH}/lib')
    else:
        print(f"{lib_dir} not found, skip push")

    dsp_dir = f"{DINFER_SDK_PATH}/dsp"
    if os.path.isdir(dsp_dir):
        cmd_list.append(f'{ADB} push {dsp_dir}/. {DEV_TMP_PATH}/lib')
    else:
        print(f"{dsp_dir} not found. skip push")

    cmd_runner(cmd_list)

def push_test():
    cmd_list = []
    cmd_list.append(f'{ADB} shell "rm -rf {DEV_TMP_PATH}/test && mkdir -p {DEV_TMP_PATH}/test"')

    test_dir = f"{DINFER_SDK_PATH}/test"
    if os.path.isdir(test_dir):
        cmd_list.append(f'{ADB} push {test_dir}/. {DEV_TMP_PATH}/test')
        cmd_list.append(f'{ADB} shell "chmod +x {DEV_TMP_PATH}/test/*"')
    else:
        print(f"{test_dir} not found. skip push")

    cmd_runner(cmd_list)
    
def push_bin():
    cmd_list = []
    cmd_list.append(f'{ADB} shell "rm -rf {DEV_TMP_PATH}/bin && mkdir -p {DEV_TMP_PATH}/bin"')
    
    bin_dir = f"{DINFER_SDK_PATH}/bin"
    if os.path.isdir(bin_dir):
        cmd_list.append(f'{ADB} push {bin_dir}/. {DEV_TMP_PATH}/bin')
        cmd_list.append(f'{ADB} shell "chmod +x {DEV_TMP_PATH}/bin/*"')
    else:
        print(f"{bin_dir} not found. skip")

    cmd_runner(cmd_list)
    
def push_model(model_path=None):
    if model_path is None:
        model_path = f'{DINFER_SDK_PATH}/model'
    cmd_list = []
    cmd_list.append(f'{ADB} shell "rm -rf {DEV_SD_PATH}/model && mkdir -p {DEV_SD_PATH}/model"')
    if os.path.isdir(model_path):
        cmd_list.append(f'{ADB} push {model_path}/. {DEV_SD_PATH}/model')
    else:
        print(f"{model_path} not found. skip")

    cmd_runner(cmd_list)

def push_sysmon():
    cmd_list = []
    sysmon_bin_path = f"{DINFER_SDK_PATH}/tool/sysmon/{SYSMON_BIN}"
    if os.path.isfile(sysmon_bin_path):
        cmd_list.append(f'{ADB} push {sysmon_bin_path} {DEV_TMP_PATH}')
        cmd_list.append(f'{ADB} shell "chmod +x {DEV_TMP_PATH}/{SYSMON_BIN}"')
    else:
        print(f"{sysmon_bin_path} not found. skip")

    cmd_runner(cmd_list)

def clear_result(sysmon_profiler=False):
    cmd_list = []
    cmd_list.append(f'{ADB} shell "rm -rf {DEV_SD_PATH}/result"')
    cmd_list.append(f'{ADB} shell "mkdir -p {DEV_SD_PATH}/result"')
    if sysmon_profiler:
        cmd_list.append(f'{ADB} shell "rm -rf /sdcard/sysmon_cdsp.bin"')
    cmd_runner(cmd_list)

def wait_for_disconnect():
    print("INFO: Waiting for adb device to disconnect")
    while True:
        result = subprocess.run([ADB, 'devices'], capture_output=True, text=True)
        if 'device' not in result.stdout.split('\n', 1)[1]:
            print("Device disconnected.")
            break
        print("Device still connected. Waiting...")
        time.sleep(1)

def run_gtest(cmd, nohup=False, sysmon_profiler=False, sysmon_profiler_duration_s=10):

    binary_name = cmd[0]
    args = cmd[1:]

    if sysmon_profiler:
        cmd = f'{ADB} shell "nohup {DEV_TMP_PATH}/{SYSMON_BIN} profiler --q6 cdsp --duration {sysmon_profiler_duration_s} > {DEV_SD_PATH}/result/sysmon.log 2>&1 &"'
        cmd_runner([cmd], False)

    if nohup:
        cmd = f'{ADB} shell "export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:{DEV_TMP_PATH}/lib ADSP_LIBRARY_PATH={DEV_TMP_PATH}/lib && \
            cd {DEV_TMP_PATH} && \
            nohup bin/{binary_name} ' + ' '.join(args) + f' > {DEV_SD_PATH}/result/{binary_name}.log 2>&1 &"'
        cmd_runner([cmd], False)
        wait_for_disconnect();
    else:
        cmd = f'{ADB} shell "export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:{DEV_TMP_PATH}/lib ADSP_LIBRARY_PATH={DEV_TMP_PATH}/lib && \
            cd {DEV_TMP_PATH} && \
            bin/{binary_name} ' + ' '.join(args) + '"'
        cmd_runner([cmd], False)
    
def pull_result(sysmon_profiler=False):

    if not os.path.exists(RESULT_PATH):
        os.makedirs(RESULT_PATH)
    cmd_list = []
    cmd_list.append(f'{ADB} wait-for-device pull {DEV_SD_PATH}/result/. {RESULT_PATH}')
    cmd_runner(cmd_list)

    if sysmon_profiler:
        cmd_list = []
        cmd_list.append(f'{ADB} pull /sdcard/sysmon_cdsp.bin {RESULT_PATH}')
        cmd_runner(cmd_list)
        # parser
        import platform
        if platform.system() == 'Windows':
            PARSER_PATH=f"{DINFER_SDK_PATH}/tool/sysmon/parser_win_v2/HTML_Parser/sysmon_parser.exe"
        elif platform.system() == 'Linux':
            PARSER_PATH=f"{DINFER_SDK_PATH}/tool/sysmon/parser_linux_v2/HTML_Parser/sysmon_parser"
        else:
            print("ERROR: 未知操作系统，无法选择sysmon parser!")
        os.makedirs(f'{RESULT_PATH}/sysmon')
        cmd = f'{PARSER_PATH} {RESULT_PATH}/sysmon_cdsp.bin --outdir {RESULT_PATH}/sysmon'
        cmd_runner([cmd], False)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='dInfer Toolkit')
    parser.add_argument('--adb', default='adb', help='adb command')
    parser.add_argument('--sdk_path', default=DINFER_SDK_PATH, help='set sdk folder of specific platform in dInfer_out, eg: dInfer/dInfer_out/ANDROID')
    parser.add_argument('--dev_tmp_path', default=DEV_TMP_PATH, help='set tmp folder to save test,lib on device')
    parser.add_argument('--dev_sdcard_path', default=DEV_SD_PATH, help='set sdcard folder to save model,testdata,config on device')
    parser.add_argument('--result_path', default=RESULT_PATH, help='set local result folder to save result data and log')
    parser.add_argument('--push_data', action='store_true', help='push test data to device')
    parser.add_argument('--push_sdk', action='store_true', help='push total sdk(dsp,lib,model,test) to device')
    parser.add_argument('--push_lib', action='store_true', help='push only lib and dsp to device')
    parser.add_argument('--push_test', action='store_true', help='DEPRECATED, please use --push_bin')
    parser.add_argument('--push_model', action='store_true', help='push only model to device')
    parser.add_argument('--pull_result', action='store_true', help='only pull result directory from device')
    parser.add_argument('--args', action='store_true', help='DEPRECATED, please use --run')
    parser.add_argument('--nohup', action='store_true', help='run gtest in background')
    parser.add_argument('--sysmon_profiler', action='store_true', help='use sysmonApp profiler')
    parser.add_argument('--profiler_s', default=10, type=int, help='sysmon profiler duration seconds')
    parser.add_argument('--push_bin', action='store_true', help='push only bin to device')
    parser.add_argument('--run', nargs=argparse.REMAINDER, help='run bin on device, eg: "--run dInferTest --gtest_list_tests", or "--run dInferNetRun"')
    parser.add_argument('--data_path', default=None, help='set local data folder to save test data')
    parser.add_argument('--model_path', default=None, help='set local model folder to save model')

    try:
        args = parser.parse_args()
    except argparse.ArgumentError as e:
        parser.print_help()
        raise e
    
    ADB = args.adb
    DINFER_SDK_PATH = args.sdk_path
    DEV_TMP_PATH = args.dev_tmp_path
    DEV_SD_PATH = args.dev_sdcard_path
    RESULT_PATH = args.result_path

    if PLATFORM == "QCOM_LE":
        # 需要root权限
        cmd_list = []
        cmd_list.append(f"{ADB} root")
        cmd_list.append(f"{ADB} shell mount -o rw,remount /")
        cmd_runner(cmd_list)

    if args.args:
        print("--args参数已弃用，请使用--run参数！")
        exit(-1)

    if args.push_test:
        print("test目录已弃用，请使用bin目录！使用--push_bin推送！")
        exit(-1)

    if args.pull_result:
        print("only pull result!")
        pull_result()
        exit(0)
    
    if args.push_data:
        push_data(args.data_path)

    if args.push_sdk or args.push_lib:
        push_lib()

    if args.push_sdk or args.push_model:
        push_model(args.model_path)

    if args.push_sdk or args.push_bin:
        push_bin()

    if args.sysmon_profiler:
        push_sysmon()

    if args.run is None or len(args.run) == 0:
        print('please use --run to run binary on device')
        parser.print_usage()
    else:
        clear_result(args.sysmon_profiler)
        run_gtest(args.run, args.nohup, args.sysmon_profiler, args.profiler_s)
        pull_result(args.sysmon_profiler)