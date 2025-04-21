#ifndef DINFER_OSAL_ENV_H_
#define DINFER_OSAL_ENV_H_

#include "dInfer/osal/common.h"
#include <stddef.h>

namespace dInfer {

/**
 * @brief Set an environment variable.
 * 
 * @param name The name of the environment variable to set.
 * @param value The value to set the environment variable to.
 * @param overwrite If non-zero, overwrite the existing value.
 * @return int 0 on success, or -1 on error.
 */
DINFER_API int SetEnv(const char *name, const char *value, int overwrite);

/**
 * @brief Get the value of an environment variable.
 * 
 * @param name The name of the environment variable to get.
 * @param value A buffer to store the value of the environment variable. or NULL to get the size only.
 * @param value_size The size of the buffer.
 * @return int 0 on success, <0 on error, >0 on value_size not enough.
 *         return -1 if the variable is not set.
 *         return the actual size of the environment variable (without \0) if value_size is not enough,
 *         and the value is undefined.
 */
DINFER_API int GetEnv(const char *name, char *value, size_t value_size);

/**
 * @brief Get the Soc Id
 *        Only support Qualcomm platform now.
 * 
 * @return int Soc Id on Qualcommm platform
 *         always return 0 on other platform 
 */
DINFER_API int GetSocId();

/**
 * @brief Get the Phone Model
 *        Only support Android platform now.
 * 
 * @return const char* Phone Model
 */
DINFER_API const char* GetPhoneModel();

/**
 * @brief Get the Soc Name
 *        Only support Android platform now.
 * 
 * @return const char* Soc Name
 */
DINFER_API const char* GetSocName();

/**
 * @brief Get the CPU Infomation
 *        Only support Android platform now.
 * 
 * @return const char* CPU Infomation
 */
DINFER_API const char* GetCPUInfo();

} // namespace dInfer

#endif // DINFER_OSAL_ENV_H_
