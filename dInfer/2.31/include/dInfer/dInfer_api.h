/*
 * Description
 *   dInfer api
 *   <table>
 *   \Author         Date        Change Description
 *   ----------     ----------  -------------------
 *   Citeace.Chen   2022.09     Initialize.
 *   </table>
 */

#ifndef __DINFER_API_H__
#define __DINFER_API_H__

#include "dInfer/dInfer_type.h"
#include "dInfer/osal/common.h"
#include <iostream>
#include <vector>
#include <map>

#ifdef __cplusplus
extern "C" {
#endif //__cplusplus

#include <stdint.h>
#include <stdarg.h>

#pragma pack(push)
#pragma pack(4)

struct dInferModelInfo {
    dInferDevice device  = dInferDevice::DINFER_CPU;    // NOTE: inference backends.
    dInferEngine runtime = dInferEngine::DINFER_TFLITE;    // NOTE: inference framework.
    bool model_encrypt   = true; // NOTE: if model is encrypted.
    std::string  model_path;  // NOTE: input model path.

    std::map<std::string, void *> optional_attrs;  // NOTE: infer attributes，eg, tflite_cpu_thread, tflite_gpu_accuracy
};

struct dInferProfile {
    float init_ms;      // NOTE: model init time in ms
    float infer_ms;     // NOTE: model average inference time usage in ms
    float stability;    // NOTE: reflect the stability of frame rate, 100% means the expected frame rate is achieved every time
    const std::vector<double> *timelist;    // NOTE: only be used while enabled profiling&timelist optinal attributes
};

class DINFER_API dInferInterface {
public:
    virtual ~dInferInterface() {};

    /**
     * @brief Run model inference
     * @return Return DINFER_OK if success
     */
    virtual dInferStatus Process() = 0;

    /**
     * @brief Get performance statistics from initialization to current
     * @note only avaliable with optional attribute "profiling"
     *
     * @return dInferProfile
     */
    virtual dInferProfile GetProfile() = 0;

    /**
     * @brief Get tensor by name
     * @return nullptr if not found
     */
    virtual dInferTensor* GetTensor(const char* name) = 0;

    /**
     * @brief Use input_tensor_ after dInferInterfaceCreate(),
     *        please check if the tensor_size is zero first.
     */
    std::vector<dInferTensor *> input_tensor_;
    /**
     * @brief Use output_tensor_ after Process(),
     *        please check if the tensor_size is zero first.
     */
    std::vector<dInferTensor *> output_tensor_;
};

/**
 * @brief Create dInferInferface object.
 *
 * @param dInfer_model_info  Data and dInferEngine information of model for dInfer.
 * @return dInferInterface object pointer.
 */
DINFER_API dInferInterface* dInferInterfaceCreate(dInferModelInfo *dInfer_model_info);
/**
 * @brief Destroy dInferInferface object.
 *
 * @param dInfer_interface  Object created by dInferInterfaceCreate().
 * @return Return DINFER_OK if success
 */
DINFER_API dInferStatus dInferInterfaceDestroy(dInferInterface *dInfer_interface);

/**
 * @brief Init save log_path and log_level.
 *
 * @param log_path Path to save log. If log_path is nullptr, only set log_level.
 *                  If log_path is "logcat", output to logcat(Android Only)
 * @param log_level The max-printed log level.
 * @return Return DINFER_OK if success
 */
DINFER_API dInferStatus dInferInitLog(const dInferLogLevel log_level = dInferLogLevel::DINFER_LOG_INFO,
                           const char *log_path = nullptr);

/**
 * @brief Register logger callback and set log level.
 *
 * @param log_level The max-printed log level.
 * @param cb        logger function callback pointer.
 * @return Return DINFER_OK if success
 */
DINFER_API dInferStatus dInferRegisterLog(const dInferLogLevel log_level = dInferLogLevel::DINFER_LOG_INFO,
                           dInferLogCallback_t cb = nullptr);

/**
 * @brief DeInit log path and register, log will output to stdout and set level to DINFER_LOG_DEBUG
 *
 * @return Return DINFER_OK if success
 */
DINFER_API dInferStatus dInferDeInitLog();

#pragma pack(pop)

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
};
#endif //__cplusplus

#endif //__DINFER_API_H__
