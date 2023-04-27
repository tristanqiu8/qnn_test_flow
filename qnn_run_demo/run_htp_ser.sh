export QNN_TARGET_ARCH=aarch64-android
export MODEL_LIB=model
export QAUNT_MODEL_NAME=libhg307_480x480_img_pet_quant_2M.serialized.bin

adb shell "rm -rf /data/local/tmp/model"
adb shell "mkdir /data/local/tmp/model"

#dsp_lib
adb push lib/hexagon-v73/lib/unsigned/libQnnHtpV73Skel.so /data/local/tmp/model
adb push lib/hexagon-v69/lib/unsigned/libQnnHtpV69Skel.so /data/local/tmp/model
adb push lib/hexagon-v68/lib/unsigned/libQnnHtpV68Skel.so /data/local/tmp/model
#dsp and cpu lib
adb push lib/$QNN_TARGET_ARCH/. /data/local/tmp/model/.

#model and data:
adb push $MODEL_LIB/. /data/local/tmp/model/.
adb shell chmod  777 /data/local/tmp/model/qnn-sample-app
adb shell chmod  777 /data/local/tmp/model/qnn-net-run

adb shell  ADSP_LIBRARY_PATH=/data/local/tmp/model \
           LD_LIBRARY_PATH=/data/local/tmp/model  \
           /data/local/tmp/model/qnn-sample-app --backend /data/local/tmp/model/libQnnHtp.so \
           --retrieve_context /data/local/tmp/model/$QAUNT_MODEL_NAME \
           --input_list /data/local/tmp/model/input.txt \
           --output_dir   /data/local/tmp/model/output \
           --system_library /data/local/tmp/model/libQnnSystem.so > ${QAUNT_MODEL_NAME}_log.txt
adb shell  ADSP_LIBRARY_PATH=/data/local/tmp/model \
           LD_LIBRARY_PATH=/data/local/tmp/model  \
           /data/local/tmp/model/qnn-net-run --backend /data/local/tmp/model/libQnnHtp.so \
           --retrieve_context /data/local/tmp/model/$QAUNT_MODEL_NAME \
            --input_list /data/local/tmp/model/input.txt \
            --output_dir   /data/local/tmp/model/output  --profiling_level detailed --log_level
adb pull /data/local/tmp/model/output/. res/$QAUNT_MODEL_NAME.so/.

