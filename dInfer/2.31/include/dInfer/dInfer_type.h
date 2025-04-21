/*
 * Description
 *   dInfer Types
 *   <table>
 *   \Author         Date        Change Description
 *   ----------     ----------  ---------------------------------------------
 *   Lucas.lv       2025.03      Extracted from C/C++ API V1
 *   </table>
 */
#ifndef __DINFER_TYPE_H__
#define __DINFER_TYPE_H__

#include "dInfer/osal/common.h"

#pragma pack(push)
#pragma pack(4)

#define MAX_RANK (6)

#ifdef __cplusplus
extern "C" {
#endif //__cplusplus

#include <stdint.h>
#include <stdarg.h>

typedef enum dInferStatus {
    DINFER_ERROR = -1,
    DINFER_OK    = 0,

    DINFER_ERROR_C DINFER_DEPRECATED_ENUM("please use DINFER_ERROR instead") = DINFER_ERROR,
    DINFER_OK_C    DINFER_DEPRECATED_ENUM("please use DINFER_OK instead") = DINFER_OK,
} dInferStatus_t;

typedef enum dInferLogLevel {
    DINFER_LOG_DEBUG = 0,
    DINFER_LOG_INFO,
    DINFER_LOG_WARNING,
    DINFER_LOG_ERROR,
    DINFER_MAX_LOG_TYPE,
    DINFER_LOG_DEFAULT = DINFER_LOG_INFO,
    DINFER_LOG_WARNIING = DINFER_LOG_WARNING,
    
    DINFER_LOG_DEBUG_C DINFER_DEPRECATED_ENUM("please use DINFER_LOG_DEBUG instead") = DINFER_LOG_DEBUG,
    DINFER_LOG_INFO_C    DINFER_DEPRECATED_ENUM("please use DINFER_LOG_INFO instead") = DINFER_LOG_INFO,
    DINFER_LOG_WARNIING_C DINFER_DEPRECATED_ENUM("please use DINFER_LOG_WARNING instead") = DINFER_LOG_WARNING,
    DINFER_LOG_WARNING_C DINFER_DEPRECATED_ENUM("please use DINFER_LOG_WARNING instead") = DINFER_LOG_WARNING,
    DINFER_LOG_ERROR_C DINFER_DEPRECATED_ENUM("please use DINFER_LOG_ERROR instead") = DINFER_LOG_ERROR,
    DINFER_MAX_LOG_TYPE_C DINFER_DEPRECATED_ENUM("please use DINFER_MAX_LOG_TYPE instead") = DINFER_MAX_LOG_TYPE,
    DINFER_LOG_DEFAULT_C DINFER_DEPRECATED_ENUM("please use DINFER_LOG_DEFAULT instead") = DINFER_LOG_DEFAULT,
} dInferLogLevel_t;

typedef enum dInferDevice {
    DINFER_NONE = 0x01 << 0,
    DINFER_CPU  = 0x01 << 1,
    DINFER_DSP  = 0x01 << 2,
    DINFER_NPU  = 0x01 << 3,
    DINFER_GPU  = 0x01 << 4,
    DINFER_HTP  = 0x01 << 5,    //NOTE: for Qualcomm (NPU + DSP)
    DINFER_HTA  = 0x01 << 6,    //NOTE: for Qualcomm (NPU)
} dInferDevice_t;

typedef enum dInferDataType {
    DINFER_U0 = -1, DINFER_U1 = 0, DINFER_I4,
    DINFER_U4, DINFER_I8, DINFER_U8,
    DINFER_U16, DINFER_I16, DINFER_U32,
    DINFER_I32, DINFER_F8, DINFER_F16,
    DINFER_FB16, DINFER_F32, DINFER_F64,

    DINFER_U0_C DINFER_DEPRECATED_ENUM("please use DINFER_U0 instead") = DINFER_U0,
    DINFER_U1_C DINFER_DEPRECATED_ENUM("please use DINFER_U1 instead") = DINFER_U1,
    DINFER_I4_C DINFER_DEPRECATED_ENUM("please use DINFER_I4 instead") = DINFER_I4,
    DINFER_U4_C DINFER_DEPRECATED_ENUM("please use DINFER_U4 instead") = DINFER_U4,
    DINFER_I8_C DINFER_DEPRECATED_ENUM("please use DINFER_I8 instead") = DINFER_I8,
    DINFER_U8_C DINFER_DEPRECATED_ENUM("please use DINFER_U8 instead") = DINFER_U8,
    DINFER_U16_C DINFER_DEPRECATED_ENUM("please use DINFER_U16 instead") = DINFER_U16,
    DINFER_I16_C DINFER_DEPRECATED_ENUM("please use DINFER_I16 instead") = DINFER_I16,
    DINFER_U32_C DINFER_DEPRECATED_ENUM("please use DINFER_U32 instead") = DINFER_U32,
    DINFER_I32_C DINFER_DEPRECATED_ENUM("please use DINFER_I32 instead") = DINFER_I32,
    DINFER_F8_C  DINFER_DEPRECATED_ENUM("please use DINFER_F8 instead") = DINFER_F8,
    DINFER_F16_C DINFER_DEPRECATED_ENUM("please use DINFER_F16 instead") = DINFER_F16,
    DINFER_FB16_C DINFER_DEPRECATED_ENUM("please use DINFER_FB16 instead") = DINFER_FB16,
    DINFER_F32_C DINFER_DEPRECATED_ENUM("please use DINFER_F32 instead") = DINFER_F32,
    DINFER_F64_C DINFER_DEPRECATED_ENUM("please use DINFER_F64 instead") = DINFER_F64,
} dInferDataType_t;


typedef enum dInferMemType {
    DINFER_MEM_NONE = 0,
    DINFER_MEM_HOST_BUF, //NOTE: cpu buffer, like cpu system heap/stack
    DINFER_MEM_SHARED_BUF, //NOTE: the Buffer, cpu and device(like gpu/npu/dsp) can access it.
    DINFER_MEM_DEVICE_BUF,  //NOTE: device buffer, only device can access it.
    DINFER_MEM_DEVICE_IMAGE1D, //NOTE: GPU Image 1D buffer
    DINFER_MEM_DEVICE_IMAGE2D, //NOTE: GPU Image 2D buffer
    DINFER_MEM_DEVICE_IMAGE3D, //NOTE: GPU Image 3D buffer

    DINFER_MEM_NONE_C DINFER_DEPRECATED_ENUM("please use DINFER_MEM_NONE instead") = DINFER_MEM_NONE,
    DINFER_MEM_HOST_BUF_C DINFER_DEPRECATED_ENUM("please use DINFER_MEM_HOST_BUF instead") = DINFER_MEM_HOST_BUF,
    DINFER_MEM_SHARED_BUF_C DINFER_DEPRECATED_ENUM("please use DINFER_MEM_SHARED_BUF instead") = DINFER_MEM_SHARED_BUF,
    DINFER_MEM_DEVICE_BUF_C DINFER_DEPRECATED_ENUM("please use DINFER_MEM_DEVICE_BUF instead") = DINFER_MEM_DEVICE_BUF,
    DINFER_MEM_DEVICE_IMAGE1D_C DINFER_DEPRECATED_ENUM("please use DINFER_MEM_DEVICE_IMAGE1D instead") = DINFER_MEM_DEVICE_IMAGE1D,
    DINFER_MEM_DEVICE_IMAGE2D_C DINFER_DEPRECATED_ENUM("please use DINFER_MEM_DEVICE_IMAGE2D instead") = DINFER_MEM_DEVICE_IMAGE2D,
    DINFER_MEM_DEVICE_IMAGE3D_C DINFER_DEPRECATED_ENUM("please use DINFER_MEM_DEVICE_IMAGE3D instead") = DINFER_MEM_DEVICE_IMAGE3D,
} dInferMemType_t;

typedef enum dInferLayout {
    DINFER_N = 0, DINFER_NC, DINFER_NCHW,
    DINFER_NHWC, DINFER_NCHWCx, DINFER_NCHWC8,
    DINFER_NCHWC16, DINFER_NSC,

    DINFER_N_C DINFER_DEPRECATED_ENUM("please use DINFER_N instead") = DINFER_N,
    DINFER_NC_C DINFER_DEPRECATED_ENUM("please use DINFER_NC instead") = DINFER_NC,
    DINFER_NCHW_C DINFER_DEPRECATED_ENUM("please use DINFER_NCHW instead") = DINFER_NCHW,
    DINFER_NHWC_C DINFER_DEPRECATED_ENUM("please use DINFER_NHWC instead") = DINFER_NHWC,
    DINFER_NCHWCx_C DINFER_DEPRECATED_ENUM("please use DINFER_NCHWCx instead") = DINFER_NCHWCx,
    DINFER_NCHWC8_C DINFER_DEPRECATED_ENUM("please use DINFER_NCHWC8 instead") = DINFER_NCHWC8,
    DINFER_NCHWC16_C DINFER_DEPRECATED_ENUM("please use DINFER_NCHWC16 instead") = DINFER_NCHWC16,
    DINFER_NSC_C DINFER_DEPRECATED_ENUM("please use DINFER_NSC instead") = DINFER_NSC,
} dInferLayout_t;

typedef enum dInferEngine {
    DINFER_TFLITE     = 0x01 << 0,
    DINFER_QNN        = 0x01 << 1,
    DINFER_COREML     = 0x01 << 2,
    DINFER_DBIT       = 0x01 << 3,
    DINFER_MNN        = 0x01 << 4,
    DINFER_PADDLELITE = 0x01 << 5,
    DINFER_TRT        = 0x01 << 6,  //NOTE: for NVIDIA GPU, Requirements:
                                    //  - GPU Compute Capability: 6.x~9.0(6.x is DEPRECATED, not recommended), see https://developer.nvidia.com/cuda-gpus and https://docs.nvidia.com/deeplearning/tensorrt/archives/tensorrt-861/support-matrix/index.html
                                    //  - NVIDIA Driver >= 450.80.02(Linux)/r452.39(Windows), see https://docs.nvidia.com/deploy/cuda-compatibility/index.html#minor-version-compatibility
    DINFER_TORCHLIB   = 0x01 << 7,
    DINFER_ACL        = 0x01 << 8,
} dInferEngine_t;

typedef dInferStatus_t dInferStatus_C DINFER_DEPRECATED("please use dInferStatus_t instead");
typedef dInferLogLevel_t dInferLogLevel_C DINFER_DEPRECATED("please use dInferLogLevel_t instead");
typedef dInferDataType_t dInferDataType_C DINFER_DEPRECATED("please use dInferDataType_t instead");
typedef dInferMemType_t dInferMemType_C DINFER_DEPRECATED("please use dInferMemType_t instead");
typedef dInferLayout_t dInferLayout_C DINFER_DEPRECATED("please use dInferLayout_t instead");

typedef struct dInferMem {
    
    union {
        uint64_t host_addr;     //NOTE: host_addr = 0 if cpu can not access the mem
        uint64_t host_addr_C DINFER_DEPRECATED("please use host_addr instead");
    };

    union {
        uint64_t device_addr;   //NOTE: device_addr != 0 if the device can access the mem.default = 0
        uint64_t device_addr_C DINFER_DEPRECATED("please use device_addr instead");
    };

    union {
        dInferMemType_t type;
        dInferMemType_t type_C DINFER_DEPRECATED("please use type instead");
    };

    union {
        int32_t  size;
        int32_t  size_C DINFER_DEPRECATED("please use size instead");
    };
} dInferMem_t;

typedef struct dInferQuant {
    union {
        int32_t   number;       //NOTE: number eq output tensor channel if using per-chennel Quantization
        int32_t   number_C DINFER_DEPRECATED("please use number instead");
    };

    union {
        dInferMem_t scale;      //NOTE: scale element type is float
        dInferMem_t scale_C DINFER_DEPRECATED("please use scale instead");
    };

    union {
        dInferMem_t zeropoint;  //NOTE: zeropoint element type is int32
        dInferMem_t zeropoint_C DINFER_DEPRECATED("please use zeropoint instead");
    };
} dInferQuant_t;

typedef struct dInferTensor {  // NOTE: please check layout and data_type before using.
    union {
        uint32_t id;
        uint32_t id_C DINFER_DEPRECATED("please use id instead");
    };

    union {
        int32_t  rank;
        int32_t  rank_C DINFER_DEPRECATED("please use rank instead");
    };

    union {
        int32_t  dim[MAX_RANK];
        DINFER_DEPRECATED("please use dim instead") int32_t  dim_C[MAX_RANK];
    };

    union {
        int32_t  offset[MAX_RANK];      // NOTE: unit data_type
        DINFER_DEPRECATED("please use offset instead") int32_t  offset_C[MAX_RANK];
    };

    union {
        int32_t  length[MAX_RANK];      // NOTE: unit data_type
        DINFER_DEPRECATED("please use length instead") int32_t  length_C[MAX_RANK];
    };
    
    union {
        dInferLayout_t   layout;  // DEPRECATED: layout字段已被弃用，不建议前后处理依据该信息解释Tensor
                                  //  前后处理应该依据模型转换时确定的layout解释Tensor
                                  //  推理框架API层面只关注dims、data_type、stride等信息用于内存管理，且推理框架也无法从模型中获取layout信息
                                  //  layout取决于模型如何训练、导出、转换，且因任务的不同而不同，不可穷举
        dInferLayout_t   layout_C DINFER_DEPRECATED("please use layout instead");
    };

    union {
        dInferDataType_t data_type;
        dInferDataType_t data_type_C DINFER_DEPRECATED("please use data_type instead");
    };

    union {
        dInferMem_t      data;
        dInferMem_t      data_C DINFER_DEPRECATED("please use data instead");
    };

    union {
        dInferQuant_t   *quant;
        dInferQuant_t   *quant_C DINFER_DEPRECATED("please use quant instead");
    };

    union {
        const char* name;
        const char* name_C DINFER_DEPRECATED("please use name instead");
    };
} dInferTensor_t;

typedef dInferMem_t dInferMem_C DINFER_DEPRECATED("please use dInferMem_t instead");
typedef dInferQuant_t dInferQuant_C DINFER_DEPRECATED("please use dInferQuant_t instead");
typedef dInferTensor_t dInferTensor_C DINFER_DEPRECATED("please use dInferTensor_t instead");

typedef int (*dInferLogCallback_t)(int log_level, const char *func_name, int line_num, const char *fmt, ...);
typedef dInferLogCallback_t dInferLogCallback_C DINFER_DEPRECATED("please use dInferLogCallback_t instead");

/**
 * @brief Convert dInferStatus to string
 * 
 * @param status dInfer status
 * @return const char* status string
 * @throws std::invalid_argument if status is not in dInferStatus
 */
DINFER_API const char *StrStatus(dInferStatus_t status);

/**
 * @brief Convert string to dInferStatus
 * 
 * @param str status string
 * @return dInferStatus
 * @throws std::invalid_argument if str is not in {"DINFER_OK", "DINFER_ERROR", "OK", "ERROR"}
 */
DINFER_API dInferStatus_t ToStatus(const char* str);

/**
 * @brief Convert dInferLogLevel to string
 * 
 * @param log_level dInfer log level
 * @return const char* log level string
 * @throws std::invalid_argument if log_level is not in dInferLogLevel
 */
DINFER_API const char *StrLogLevel(dInferLogLevel_t log_level);

/**
 * @brief Convert string to dInferLogLevel
 * 
 * @param str log level string
 * @return dInferLogLevel
 * @throws std::invalid_argument if str is not in {"DINFER_LOG_DEBUG", "DEBUG", "DINFER_LOG_INFO", "INFO", "DINFER_LOG_WARNIING", "WARNING", "DINFER_LOG_ERROR", "ERROR", "DINFER_MAX_LOG_TYPE"}
 */
DINFER_API dInferLogLevel_t ToLogLevel(const char* str);

/**
 * @brief Convert dInferDevice to string
 * 
 * @param device dInfer device
 * @return const char* device string
 * @throws std::invalid_argument if device is not in dInferDevice
 */
DINFER_API const char *StrDevice(dInferDevice_t device);

/**
 * @brief Convert string to dInferDevice
 * 
 * @param str device string
 * @return dInferDevice
 * @throws std::invalid_argument if str is not in {"DINFER_NONE", "NONE", "DINFER_CPU", "CPU", "DINFER_GPU", "GPU", "DINFER_NPU", "NPU", "DINFER_DSP", "DSP", "DINFER_MAX_DEVICE"}
 */
DINFER_API dInferDevice_t ToDevice(const char* str);

/**
 * @brief Convert dInferDataType to string
 * 
 * @param data_type dInfer data type
 * @return const char* data type string
 * @throws std::invalid_argument if data_type is not in dInferDataType
 */
DINFER_API const char *StrDataType(dInferDataType_t data_type);

/**
 * @brief Convert string to dInferDataType
 * 
 * @param str data type string
 * @return dInferDataType
 * @throws std::invalid_argument if str is not in {"DINFER_U16", "U16", "DINFER_I16", "I16", "DINFER_U32", "U32", "DINFER_I32", "I32", "DINFER_F8", "F8", "DINFER_F16", "F16", "DINFER_FB16", "FB16", "DINFER_F32", "F32", "DINFER_F64", "F64"}
 */
DINFER_API dInferDataType_t ToDataType(const char* str);

/**
 * @brief Convert dInferMemType to string
 * 
 * @param mem_type dInfer memory type
 * @return const char* memory type string
 * @throws std::invalid_argument if mem_type is not in dInferMemType
 */
DINFER_API const char *StrMemType(dInferMemType_t mem_type);

/**
 * @brief Convert string to dInferMemType
 * 
 * @param str memory type string
 * @return dInferMemType
 * @throws std::invalid_argument if str is not in {"DINFER_MEM_NONE", "NONE", "DINFER_MEM_HOST_BUF", "HOST_BUF", "DINFER_MEM_SHARED_BUF", "SHARED_BUF", "DINFER_MEM_DEVICE_BUF", "DEVICE_BUF", "DINFER_MEM_DEVICE_IMAGE1D", "DEVICE_IMAGE1D", "DINFER_MEM_DEVICE_IMAGE2D", "DEVICE_IMAGE2D", "DINFER_MEM_DEVICE_IMAGE3D", "DEVICE_IMAGE3D"}
 */
DINFER_API dInferMemType_t ToMemType(const char* str);

/**
 * @brief Convert dInferLayout to string
 * 
 * @param layout dInfer layout
 * @return const char* layout string
 * @throws std::invalid_argument if layout is not in dInferLayout
 */
DINFER_API const char *StrLayout(dInferLayout_t layout);

/**
 * @brief Convert string to dInferLayout
 * 
 * @param str layout string
 * @return dInferLayout
 * @throws std::invalid_argument if str is not in {"DINFER_N", "N", "DINFER_NC", "NC", "DINFER_NCHW", "NCHW", "DINFER_NHWC", "NHWC", "DINFER_NCHWCx", "NCHWCx", "DINFER_NCHWC8", "NCHWC8", "DINFER_NCHWC16", "NCHWC16", "DINFER_NSC", "NSC"}
 */
DINFER_API dInferLayout_t ToLayout(const char* str);

/**
 * @brief Convert dInferEngine to string
 * 
 * @param engine dInfer engine
 * @return const char* engine string
 * @throws std::invalid_argument if engine is not in dInferEngine
 */
DINFER_API const char *StrEngine(dInferEngine_t engine);

/**
 * @brief Convert string to dInferEngine
 * 
 * @param str engine string
 * @return dInferEngine
 * @throws std::invalid_argument if str is not in {"DINFER_TFLITE", "TFLITE", "DINFER_QNN", "QNN", "DINFER_COREML", "COREML", "DINFER_DBIT", "DBIT", "DINFER_MNN", "MNN", "DINFER_PADDLELITE", "PADDLELITE", "DINFER_TRT", "TRT", "DINFER_TORCHLIB", "TORCHLIB", "DINFER_ACL", "ACL"}
 */
DINFER_API dInferEngine_t ToEngine(const char* str);

/**
 * @brief Get the dInfer data type size in bits
 * 
 * @param data_type dInfer data type
 * @return int32_t bits
 */
DINFER_API int32_t GetTypeSizeBit(dInferDataType_t data_type);

/**
 * @brief Get the tensor data size in bytes
 * 
 * @param tensor dInfer tensor
 * @return int32_t bytes
 */
DINFER_API int32_t GetTensorDataSize(const dInferTensor_t *tensor);

/**
 * @brief Get the tensor element count
 * 
 * @param tensor dInfer tensor
 * @return int32_t element count
 */
DINFER_API int32_t GetTensorCount(const dInferTensor_t *tensor);

/**
 * @brief Print the tensor information to dInfer log info
 * 
 * @param tag tag string
 * @param tensor dInfer tensor
 */
DINFER_API void PrintTensor(const char *tag, const dInferTensor_t *tensor);

#ifdef __cplusplus
};
#endif //__cplusplus

#pragma pack(pop)

#endif // __DINFER_TYPE_H__