#!/bin/bash
#==============================================================================
#
#  Copyright (c) 2020-2022 Qualcomm Technologies, Inc.
#  All Rights Reserved.
#  Confidential and Proprietary - Qualcomm Technologies, Inc.
#
#==============================================================================

# This script sets up the various environment variables needed to run various sdk binaries and scripts
OPTIND=1

_usage()
{
cat << EOF
Usage: $(basename ${BASH_SOURCE[${#BASH_SOURCE[@]} - 1]}) [-h] [-c CAFFE_DIRECTORY] [-f CAFFE2_DIRECTORY] [-t TENSORFLOW_DIRECTORY]

Script sets up environment variables needed for running sdk binaries and scripts, where only one of the
Caffe, Onnx, or Tensorflow directories have to be specified.

optional arguments:
 -c CAFFE_DIRECTORY            Specifies Caffe directory
 -o ONNX_DIRECTORY             Specifies ONNX directory
 -t TENSORFLOW_DIRECTORY       Specifies TensorFlow directory

EOF
}


# flag indicating if any ML framework was setup
ANY_ML_FW_SETUP_DONE=0

function _setup_qnn()
{
  # get directory of the bash script
  local SOURCEDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
  local QNN_SDK_TOOLS=$(readlink -f ${SOURCEDIR}/..)
  export PYTHONPATH="${QNN_SDK_TOOLS}/python/":${PYTHONPATH}
  export QNN_SDK_ROOT="$( cd "${QNN_SDK_TOOLS}/../.." && pwd )"
  export PATH=${QNN_SDK_TOOLS}/bin:${PATH}
  if [ "x${LD_LIBRARY_PATH}" = "x" ]; then
    export LD_LIBRARY_PATH=${QNN_SDK_TOOLS}/lib
  else
    export LD_LIBRARY_PATH=${QNN_SDK_TOOLS}/lib:${LD_LIBRARY_PATH}
  fi
  if ls ${QNN_SDK_ROOT}/target/x86_64-linux-clang/bin/hexagon-* > /dev/null 2>&1; then
    export HEXAGON_TOOLS_DIR=${QNN_SDK_ROOT}/target/x86_64-linux-clang/bin
  fi
}

function _setup_caffe()
{
  if ! _is_valid_directory $1; then
    return 1
  fi

  # common setup
  _setup_qnn

  local CAFFEDIR=$1

  # current tested SHA for caffe
  local VERIFY_CAFFE_SHA="18b09e807a6e146750d84e89a961ba8e678830b4"

  # setup an environment variable called $CAFFE_HOME
  export CAFFE_HOME=${CAFFEDIR}
  echo "[INFO] Setting CAFFE_HOME="${CAFFEDIR}

  # update PATH
  export PATH=${CAFFEDIR}/build/install/bin:${PATH}
  export PATH=${CAFFEDIR}/distribute/bin:${PATH}

  # update LD_LIBRARY_PATH
  export LD_LIBRARY_PATH=${CAFFEDIR}/build/install/lib:${LD_LIBRARY_PATH}
  export LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:${CAFFEDIR}/distribute/caffe/distribute/lib
  export LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:${CAFFEDIR}/distribute/lib

  # update PYTHONPATH
  export PYTHONPATH=${CAFFEDIR}/distribute/caffe/distribute/python:${PYTHONPATH}
  export PYTHONPATH=${CAFFEDIR}/dependencies/python:${PYTHONPATH}
  export PYTHONPATH=${CAFFEDIR}/build/install/python:${PYTHONPATH}
  export PYTHONPATH=${CAFFEDIR}/distribute/python:${PYTHONPATH}

  # check Caffe SHA
  pushd ${CAFFEDIR} > /dev/null
  local CURRENT_CAFFE_SHA=$(git rev-parse HEAD)
  if [ "${VERIFY_CAFFE_SHA}" != "${CURRENT_CAFFE_SHA}" ]; then
    echo "[WARNING] Expected CAFFE HEAD rev "${VERIFY_CAFFE_SHA}" but found "${CURRENT_CAFFE_SHA}" instead. This SHA is not tested."
  fi
  popd > /dev/null

  # set flag that ML framework was setup
  ANY_ML_FW_SETUP_DONE=1

  return 0
}

function _setup_onnx()
{
  if ! _is_valid_directory $1; then
    return 1
  fi

  # common setup
  _setup_qnn

  local ONNXDIR=$1

  # setup an environment variable called $ONNX_HOME
  export ONNX_HOME=${ONNXDIR}
  export PYTHONPATH=${ONNX_HOME}:${PYTHONPATH}
  export PYTHONPATH=$ONNX_HOME/distribute:${PYTHONPATH}
  export PYTHONPATH=$ONNX_HOME/dependencies/python:$PYTHONPATH
  echo "[INFO] Setting ONNX_HOME="${ONNXDIR}

  # set flag that ML framework was setup
  ANY_ML_FW_SETUP_DONE=1

  return 0
}

function _setup_tensorflow()
{
  if ! _is_valid_directory $1; then
    return 1
  fi

  # common setup
  _setup_qnn

  local TENSORFLOWDIR=$1

  # setup an environment variable called $TENSORFLOW_HOME
  export TENSORFLOW_HOME=${TENSORFLOWDIR}
  export PYTHONPATH=${TENSORFLOW_HOME}:${PYTHONPATH}
  export PYTHONPATH=$TENSORFLOW_HOME/distribute:${PYTHONPATH}
  export PYTHONPATH=$TENSORFLOW_HOME/dependencies/python:$PYTHONPATH
  echo "[INFO] Setting TENSORFLOW_HOME="${TENSORFLOWDIR}

  # set flag that ML framework was setup
  ANY_ML_FW_SETUP_DONE=1

  return 0
}

function _check_ndk()
{
  # check NDK in path
  local ndkDir=$(which ndk-build)

  if [[ ! -d "${ANDROID_NDK_ROOT}" ]]; then
    if [ ! -s "${ndkDir}" ]; then
      echo "[WARNING] Can't find ANDROID_NDK_ROOT or ndk-build."
    else
      ANDROID_NDK_ROOT=$(dirname ${ndkDir})
      echo "[INFO] Found ndk-build at "${ndkDir}
    fi
  else
    echo "[INFO] Found ANDROID_NDK_ROOT at "${ANDROID_NDK_ROOT}
    if [ ! -s "${ndkDir}" ]; then
      # Add ANDROID_NDK_ROOT to PATH
      export PATH=$ANDROID_NDK_ROOT:$PATH
    fi
  fi
}

function _check_linux_oe_aarch64_gcc93()
{
  if [[ ! -d "${QNN_AARCH64_LINUX_OE_GCC_93}" ]]; then
    echo "[WARNING] Can't find QNN_AARCH64_LINUX_OE_GCC_93"
  else
    echo "[INFO] Found QNN_AARCH64_LINUX_OE_GCC_93 at "${QNN_AARCH64_LINUX_OE_GCC_93}
  fi
}

function _check_linux_oe_aarch64_gcc82()
{
  if [[ ! -d "${QNN_AARCH64_LINUX_OE_GCC_82}" ]]; then
    echo "[WARNING] Can't find QNN_AARCH64_LINUX_OE_GCC_82"
  else
    echo "[INFO] Found QNN_AARCH64_LINUX_OE_GCC_82 at "${QNN_AARCH64_LINUX_OE_GCC_82}
  fi
}

function _check_ubuntu_aarch64_gcc75()
{
  # check aarch64-linux-gnu-g++ in path
  local aarch64LinuxGnuDir=$(which aarch64-linux-gnu-g++)

  if [[ ! -d "${QNN_AARCH64_UBUNTU_GCC_75}" ]]; then
    if [ ! -s "${aarch64LinuxGnuDir}" ]; then
      echo "[WARNING] Can't find QNN_AARCH64_UBUNTU_GCC_75 or aarch64-linux-gnu-g++."
    else
      QNN_AARCH64_UBUNTU_GCC_75=$(dirname ${aarch64LinuxGnuDir})
      echo "[INFO] Found aarch64-linux-gnu-g++ at "${aarch64LinuxGnuDir}
    fi
  else
    echo "[INFO] Found QNN_AARCH64_UBUNTU_GCC_75 at "${QNN_AARCH64_UBUNTU_GCC_75}
    if [ ! -s "${aarch64LinuxGnuDir}" ]; then
      # Add QNN_AARCH64_UBUNTU_GCC_75 to PATH
      export PATH=$QNN_AARCH64_UBUNTU_GCC_75/root/bin:$PATH
    fi
  fi
}

function _is_valid_directory()
{
  if [[ ! -z $1 ]]; then
    if [[ ! -d $1 ]]; then
      echo "[ERROR] Invalid directory "$1" specified. Please rerun the srcipt with a valid directory path."
      return 1
    else
      return 0
    fi
  else
    return 1
  fi
}

function _cleanup()
{
  unset -f _usage
  unset -f _setup_qnn
  unset -f _setup_caffe
  unset -f _setup_tensorflow
  unset -f _check_ndk
  unset -f _check_ubuntu_aarch64_gcc75
  unset -f _check_linux_oe_aarch64_gcc93
  unset -f _check_linux_oe_aarch64_gcc82
  unset -f _is_valid_directory
  unset -f _cleanup
}

# script can only handle one framework per execution
if [[ "$#" -gt 2 ]]; then
  echo "[ERROR] Invalid number of arguments. See -h for help."
  return 1
fi

# parse arguments
while getopts "h?c:o:t:" opt; do
  case ${opt} in
    h  ) _usage; return 0 ;;
    c  ) _setup_caffe ${OPTARG} || return 1 ;;
    o  ) _setup_onnx ${OPTARG} || return 1 ;;
    t  ) _setup_tensorflow ${OPTARG} || return 1 ;;
    \? ) echo "See -h for help."; return 1 ;;
  esac
done

if [ ${ANY_ML_FW_SETUP_DONE} = 0 ]; then
  echo "[WARNING] No source ML framework has been setup. See -h for help."
  # do common setup since not done via ML framework setup
  _setup_qnn
fi

# check for NDK
_check_ndk

# check for aarch64 ubuntu gcc7.5
_check_ubuntu_aarch64_gcc75

# check for aarch64 Linux OE gcc9.3
_check_linux_oe_aarch64_gcc93

# check for aarch64 Linux OE gcc8.2
_check_linux_oe_aarch64_gcc82

# cleanup
_cleanup

echo "[INFO] QNN SDK environment set. QNN_SDK_ROOT: ${QNN_SDK_ROOT}"

