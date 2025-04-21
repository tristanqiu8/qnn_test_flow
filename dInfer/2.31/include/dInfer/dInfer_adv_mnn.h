/*
 * Description
 *   dInfer advanced api for MNN
 *   <table>
 *   \Author         Date        Change Description
 *   ----------     ----------  -------------------
 *   Lucas.Lv       2024.12     Initialize.
 *   </table>
 */
#ifndef __DINFER_API_MNN_H__
#define __DINFER_API_MNN_H__

#include <stddef.h>
#include <string>
#include <vector>

#ifndef MNNForwardType_h
typedef enum {
    MNN_FORWARD_CPU = 0,

    /*
     Firtly find the first available backends not equal to CPU
     If no other backends, use cpu
     */
    MNN_FORWARD_AUTO = 4,

    /*Hand write metal*/
    MNN_FORWARD_METAL = 1,

    /*NVIDIA GPU API*/
    MNN_FORWARD_CUDA = 2,

    /*Android / Common Device GPU API*/
    MNN_FORWARD_OPENCL = 3,
    MNN_FORWARD_OPENGL = 6,
    MNN_FORWARD_VULKAN = 7,

    /*Android 8.1's NNAPI or CoreML for ios*/
    MNN_FORWARD_NN = 5,

    /*User can use API from Backend.hpp to add or search Backend*/
    MNN_FORWARD_USER_0 = 8,
    MNN_FORWARD_USER_1 = 9,
    MNN_FORWARD_USER_2 = 10,
    MNN_FORWARD_USER_3 = 11,

    MNN_FORWARD_ALL,

    /* Apply arm extension instruction set to accelerate some Ops, this forward type
       is only used in MNN internal, and will be active automatically when user set forward type
       to be MNN_FORWARD_CPU and extension instruction set is valid on hardware.
    */
    MNN_FORWARD_CPU_EXTENSION

} MNNForwardType;

typedef enum {
    // choose one tuning mode Only
    MNN_GPU_TUNING_NONE    = 1 << 0,/* Forbidden tuning, performance not good */
    MNN_GPU_TUNING_HEAVY  = 1 << 1,/* heavily tuning, usually not suggested */
    MNN_GPU_TUNING_WIDE   = 1 << 2,/* widely tuning, performance good. Default */
    MNN_GPU_TUNING_NORMAL = 1 << 3,/* normal tuning, performance may be ok */
    MNN_GPU_TUNING_FAST   = 1 << 4,/* fast tuning, performance may not good */

    // choose one opencl memory mode Only
    /* User can try OpenCL_MEMORY_BUFFER and OpenCL_MEMORY_IMAGE both,
     then choose the better one according to performance*/
    MNN_GPU_MEMORY_BUFFER = 1 << 6,/* User assign mode */
    MNN_GPU_MEMORY_IMAGE  = 1 << 7,/* User assign mode */
    // choose one opencl memory mode Only, this mode Only support for Qualcomm gpu
    /* User can try MNN_GPU_RECORD_OP and MNN_GPU_RECORD_KERNEL both,
     then choose the better one according to performance*/
    MNN_GPU_RECORD_OP  = 1 << 8,/* the kernels in one op execution record into one recording */
    MNN_GPU_RECORD_BATCH  = 1 << 9,/* 10 kernels record into one recording */
} MNNGpuMode;

namespace MNN {
struct BackendConfig {
    enum MemoryMode { Memory_Normal = 0, Memory_High, Memory_Low };

    MemoryMode memory = Memory_Normal;

    enum PowerMode { Power_Normal = 0, Power_High, Power_Low };

    PowerMode power = Power_Normal;

    enum PrecisionMode { Precision_Normal = 0, Precision_High, Precision_Low, Precision_Low_BF16 };

    PrecisionMode precision = Precision_Normal;

    /** user defined context */
    union {
        void* sharedContext = nullptr;
        size_t flags; // Valid for CPU Backend
    };
};

}; // namespace MNN
#endif // MNNForwardType_h

#ifndef MNN_Interpreter_hpp
namespace MNN {

/** session schedule config */
struct ScheduleConfig {
    /** which tensor should be kept */
    std::vector<std::string> saveTensors;
    /** forward type */
    MNNForwardType type = MNN_FORWARD_CPU;
    /** CPU:number of threads in parallel , Or GPU: mode setting*/
    union {
        int numThread = 4;
        int mode;
    };

    /** subpath to run */
    struct Path {
        std::vector<std::string> inputs;
        std::vector<std::string> outputs;

        enum Mode {
            /**
             * Op Mode
             * - inputs means the source op, can NOT be empty.
             * - outputs means the sink op, can be empty.
             * The path will start from source op, then flow when encounter the sink op.
             * The sink op will not be compute in this path.
             */
            Op = 0,

            /**
             * Tensor Mode
             * - inputs means the inputs tensors, can NOT be empty.
             * - outputs means the outputs tensors, can NOT be empty.
             * It will find the pipeline that compute outputs from inputs.
             */
            Tensor = 1
        };

        /** running mode */
        Mode mode = Op;
    };
    Path path;

    /** backup backend used to create execution when desinated backend do NOT support any op */
    MNNForwardType backupType = MNN_FORWARD_CPU;

    /** extra backend config */
    BackendConfig* backendConfig = nullptr;
};

}; // namespace MNN
#endif // MNN_Interpreter_hpp

#endif // __DINFER_API_MNN_H__