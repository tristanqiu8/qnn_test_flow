export QNN_TARGET_ARCH=aarch64-android

adb shell "rm -rf /data/local/tmp/model"
adb shell "mkdir /data/local/tmp/model"

#dsp_lib
adb push lib/hexagon-v73/lib/unsigned/libQnnHtpV73Skel.so /data/local/tmp/model
adb push lib/hexagon-v69/lib/unsigned/libQnnHtpV69Skel.so /data/local/tmp/model
adb push lib/hexagon-v68/lib/unsigned/libQnnHtpV68Skel.so /data/local/tmp/model
#dsp and cpu lib
adb push lib/$QNN_TARGET_ARCH/. /data/local/tmp/model/.
adb push ${MODEL_DIR}/${MODEL_NAME}_input.raw /data/local/tmp/model/.
adb push ${MODEL_DIR}/${MODEL_NAME}_input_list.txt /data/local/tmp/model/.
adb push ${MODEL_DIR}/ctx_${MODEL_NAME}.bin /data/local/tmp/model/.
adb push ${MODEL_DIR}/${QNN_TARGET_ARCH}/lib${MODEL_NAME}.so /data/local/tmp/model/.
adb push ${MODEL_DIR}/PerfSetting.conf /data/local/tmp/model/.
adb push ${MODEL_DIR}/HtpConfigFile_local.json /data/local/tmp/model/.
#model and data:
# adb push $MODEL_LIB/. /data/local/tmp/model/.
adb shell chmod 777 /data/local/tmp/model/${QNN_APP}
adb shell chmod 777 /data/local/tmp/model/qnn-net-run
adb shell chmod 777 /data/local/tmp/model/qnn-profile-viewer


adb shell ADSP_LIBRARY_PATH=/data/local/tmp/model \
          LD_LIBRARY_PATH=/data/local/tmp/model \
          /data/local/tmp/model/${QNN_APP} \
          --backend /data/local/tmp/model/libQnnHtp.so \
          --retrieve_context  /data/local/tmp/model/ctx_${MODEL_NAME}.bin \
          --input_list /data/local/tmp/model/${MODEL_NAME}_input_list.txt \
          --system_library /data/local/tmp/model/libQnnSystem.so \
          --output_dir /data/local/tmp/model/output_so > ${MODEL_DIR}/log_bin_${MODEL_NAME}.txt

adb shell ADSP_LIBRARY_PATH=/data/local/tmp/model \
          LD_LIBRARY_PATH=/data/local/tmp/model \
          /data/local/tmp/model/${QNN_APP} \
          --backend /data/local/tmp/model/libQnnHtp.so \
          --model  /data/local/tmp/model/lib${MODEL_NAME}.so \
          --input_list /data/local/tmp/model/${MODEL_NAME}_input_list.txt \
          --output_dir /data/local/tmp/model/output_bin > ${MODEL_DIR}/log_so_${MODEL_NAME}.txt

adb shell ADSP_LIBRARY_PATH=/data/local/tmp/model \
        LD_LIBRARY_PATH=/data/local/tmp/model \
        /data/local/tmp/model/qnn-net-run \
        --backend /data/local/tmp/model/libQnnHtp.so \
        --model /data/local/tmp/model/lib${MODEL_NAME}.so \
        --input_list /data/local/tmp/model/${MODEL_NAME}_input_list.txt \
        --profiling_level=backend \
        --log_level verbose \
        --perf_profile burst \
        --config_file /data/local/tmp/model/HtpConfigFile_local.json \
        --output_dir /data/local/tmp/model/output_detailed
    
adb pull /data/local/tmp/model/output_detailed/ ${MODEL_DIR}/.