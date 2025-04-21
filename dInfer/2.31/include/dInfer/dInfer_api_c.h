/*
 * Description
 *   dInfer C api
 *   <table>
 *   \Author         Date        Change Description
 *   ----------     ----------  -------------------
 *   Yone.li        2023.10     C API V1.
 *   Lucas.lv       2025.03     Add alias for API update preparation
 *   </table>
 */

#ifndef __DINFER_API_C_H__
#define __DINFER_API_C_H__

#include "dInfer/dInfer_type.h"
#include "dInfer/osal/common.h"

#ifdef __cplusplus
extern "C" {
#endif

#include <stdint.h>
#include <stdarg.h>

typedef struct { 
    char* runtime;
    union {
        bool model_encrypt;     // NOTE: if model is encrypted.
        bool model_encrypt_C DINFER_DEPRECATED("please use model_encrypt instead");
    };
    union {
        char*  model_path;      // NOTE: input model path.
        char*  model_path_C DINFER_DEPRECATED("please use model_path instead");
    };

    // NOTE: QNN optional attrs
    union {
        char* optional_attrs_ic;    //qnn_input_config
        char* optional_attrs_ic_C DINFER_DEPRECATED("please use optional_attrs_ic instead");
    };
    union {
        char* optional_attrs_oc;    //qnn_output_config
        char* optional_attrs_oc_C DINFER_DEPRECATED("please use optional_attrs_oc instead");
    };
    union {
        char* optional_attrs_pl;    //qnn_power_level
        char* optional_attrs_pl_C DINFER_DEPRECATED("please use optional_attrs_pl instead");
    };
    union {
        bool  optional_attrs_ql;    //qnn_load_from_cache
        bool  optional_attrs_ql_C DINFER_DEPRECATED("please use optional_attrs_ql instead");
    };
    bool  optional_attrs_shared_buffer; // set to use qnn htp shared buffer, host_addr = ion_addr, device_addr = fd

    // NOTE: MNN optional attrs
    union {
        int32_t optional_attrs_forwardtype;
        int32_t optional_attrs_forwardtype_C DINFER_DEPRECATED("please use optional_attrs_forwardtype instead");
    };
    union {
        int32_t optional_attrs_numberthread;
        int32_t optional_attrs_numberthread_C DINFER_DEPRECATED("please use optional_attrs_numberthread instead");
    };
    union {
        int32_t optional_attrs_precision;
        int32_t optional_attrs_precision_C DINFER_DEPRECATED("please use optional_attrs_precision instead");
    };
    union {
        int32_t optional_attrs_power;
        int32_t optional_attrs_power_C DINFER_DEPRECATED("please use optional_attrs_power instead");
    };
    union {
        int32_t optional_attrs_memorymode;
        int32_t optional_attrs_memorymode_C DINFER_DEPRECATED("please use optional_attrs_memorymode instead");
    };
    
    void* optional_attrs_htp_power_cfg; // set to use custom qnn htp power cfg, ref dInferHtpPowerConfig in dInfer_adv_qnn.h
    void* optional_attrs_htp_power_run_cfg; // set to use custom qnn htp power cfg for run, ref dInferHtpPowerConfig in dInfer_adv_qnn.h
    void* optional_attrs_htp_power_idle_cfg; // set to use custom qnn htp power cfg for idle, ref dInferHtpPowerConfig in dInfer_adv_qnn.h

    uint8_t qnn_signed_pd; // set non-zero to use Signed Process Domain

    uint8_t reserved[47];

} dInferModelInfo_t;
typedef dInferModelInfo_t dInferModelInfo_C DINFER_DEPRECATED("please use dInferModelInfo_t instead");  

typedef struct { 
    union {
        dInferTensor_t** input_tensor;
        dInferTensor_t** input_tensor_C_ DINFER_DEPRECATED("please use input_tensor instead");
    };
    union {
        dInferTensor_t** output_tensor;
        dInferTensor_t** output_tensor_C_ DINFER_DEPRECATED("please use output_tensor instead");
    };
    union {
        int input_num;
        int input_num_C DINFER_DEPRECATED("please use input_num instead");
    };
    union {
        int output_num;
        int output_num_C DINFER_DEPRECATED("please use output_num instead");
    };
} dInferTensorInfo_t;
typedef dInferTensorInfo_t dInferTensorInfo_C DINFER_DEPRECATED("please use dInferTensorInfo_t instead");

/**
 * @brief Create dInferInferface object.
 *
 * @param dInfer_model_info  Data and dInferEngine information of model for dInfer.
 * @return dInferInterface object pointer.
 */
DINFER_API void* dInferInterfaceCreate_C(dInferModelInfo_t *dInfer_model_info, dInferTensorInfo_t* dInfer_tensor_info);

/**
 * @brief Get tensor by name
 * 
 * @param dInfer_tensor_info dInferTensorInfo_t object
 * @param name tensor name
 * @return matched tensor pointor, nullptr if not found
 */
DINFER_API dInferTensor_t* dInferGetTensor(dInferTensorInfo_t* dInfer_tensor_info, const char* name);

/**
* @brief Run model inference
* @return Return DINFER_OK if success
*/
DINFER_API dInferStatus_t dInferInterfaceProcess_C(void* dInferInterface_ptr);

/**
* @brief Run model inference
* @return Return DINFER_OK if success
* @remark dInferInterfaceProcessSync_C on functions dInferInterfaceProcess_C, it supports input and output 
* external addresses to be passed in and modified.
*/
DINFER_API dInferStatus_t dInferInterfaceProcessSync_C(void* dInferInterface_ptr, dInferTensorInfo_t* dInfer_tensor_info);

/**
 * @brief Destroy dInferInferface object.
 *
 * @param dInfer_interface  Object created by dInferInterfaceCreate().
 * @return Return DINFER_OK if success
 */
DINFER_API dInferStatus_t dInferInterfaceDestroy_C(void* dInferInterface_ptr, dInferTensorInfo_t* dInfer_tensor_info);

/**
 * @brief Init save log_path and log_level.
 *
 * @param log_path Path to save log. If log_path is nullptr, only set log_level.
 *                  If log_path is "logcat", output to logcat(Android Only)
 * @param log_level The max-printed log level.
 * @return Return DINFER_OK if success
 */
DINFER_API dInferStatus_t dInferInitLog_C(dInferLogLevel_t log_level, const char *log_path);

/**
 * @brief Register logger callback and set log level.
 * 
 * @param log_level The max-printed log level.
 * @param cb        logger function callback pointer.
 * @return Return DINFER_OK if success
 */
DINFER_API dInferStatus_t dInferRegisterLog_C(const dInferLogLevel_t log_level, dInferLogCallback_t cb);

/**
 * @brief DeInit log path and register, log will output to stdout and set level to DINFER_LOG_DEBUG
 * 
 * @return Return DINFER_OK if success
 */
DINFER_API dInferStatus_t dInferDeInitLog_C();

/**
 * @brief Get the Version Major Number
 * 
 * @return int32_t version major
 */
DINFER_API int dInferGetVersionMajor();

/**
 * @brief Get the Version Minor Number
 * 
 * @return int32_t version minor
 */
DINFER_API int dInferGetVersionMinor();

/**
 * @brief Get the Version Patch Number
 * 
 * @return int32_t version patch
 */
DINFER_API int dInferGetVersionPatch();

/**
 * @brief Get the Version
 * 
 * @return const char* full version string, eg. 1.4.0
 */
DINFER_API const char *dInferGetVersion();

/**
 * @brief Get the Build Config String
 * 
 * @return const char* build config string
 */
DINFER_API const char *dInferGetBuildConfig();

#ifdef __cplusplus
}
#endif

#endif //__DINFER_API_C_H__
