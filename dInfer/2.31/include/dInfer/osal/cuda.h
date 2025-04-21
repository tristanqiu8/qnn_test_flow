#ifndef DINFER_OSAL_CUDA_H_
#define DINFER_OSAL_CUDA_H_

#include "dInfer/osal/common.h"

namespace dInfer {

/**
 * @brief Get the Cuda Runtime Version
 * 
 * @return int runtime version, 0 means failed
 * Returns the version number of the current CUDA Runtime instance. 
 * The version is returned as (1000 &times; major + 10 &times; minor). 
 * For example, CUDA 9.2 would be represented by 9020.
 */
DINFER_API int cudaGetRuntimeVersion();

/**
 * @brief Get the Cuda Driver Version
 * 
 * @return int driver version, 0 means failed
 * Returns the latest version of CUDA supported by the driver. 
 * The version is returned as (1000 &times; major + 10 &times; minor).
 * For example, CUDA 9.2 would be represented by 9020.
 */
DINFER_API int cudaGetDriverVersion();

/**
 * @brief Get the Cuda Device Count
 * 
 * @return int device count, 0 means failed
 * Returns the number of devices with compute capability
 * greater or equal to 2.0
 */
DINFER_API int cudaGetDeviceCount();

/**
 * @brief Get the Cuda Device
 * 
 * @return int device index, -1 means failed
 * Returns the current device for the calling host thread.
 */
DINFER_API int cudaGetDevice();

/**
 * @brief Get the Cuda SM Version
 * 
 * @param deviceIndex current device index can get by cudaGetDevice()
 * @return int sm version, 0 means failed
 */
DINFER_API int cudaGetSMVersion(int deviceIndex);

} // namespace dInfer

#endif // DINFER_OSAL_CUDA_H_