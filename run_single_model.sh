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
#model and data:
adb push $MODEL_LIB/. /data/local/tmp/model/.
adb shell chmod  777 /data/local/tmp/model/qnn-sample-app
adb shell chmod  777 /data/local/tmp/model/qnn-net-run


adb shell ADSP_LIBRARY_PATH=/data/local/tmp/model \
          LD_LIBRARY_PATH=/data/local/tmp/model \
          /data/local/tmp/model/qnn-sample-app \
          --backend libQnnHtp.so --model  lib${MODEL_NAME}.so \
          --input_list /data/local/tmp/model/${MODEL_NAME}_input_list.txt \
          --output_dir /data/local/tmp/model/output > log_${MODEL_NAME}.txt

