#ifndef DINFER_OSAL_TIME_H_
#define DINFER_OSAL_TIME_H_

#include "dInfer/osal/common.h"
#include "dInfer/osal/log.h"
#include <cstdint>

#define DINFER_TIME_BEGIN(name) \
    double name ## t1 = dInfer::GetTimestampMS(); \

#define DINFER_TIME_END(name) \
    double name ## t2 = dInfer::GetTimestampMS(); \
    double name ## t1t2 = name ## t2 - name ## t1; \
    LOGI("DINFER_TIME: %s = %f ms\n", #name, name ## t1t2);

namespace dInfer {

/**
 * @brief Sleep for a given number of milliseconds
 * 
 * @param ms The number of milliseconds to sleep
 */
DINFER_API void SleepMS(uint32_t ms);

/**
 * @brief Get the Time in microseconds
 * 
 * @return double time in microseconds
 */
DINFER_API double GetTimestampUS();

/**
 * @brief Get the Time in milliseconds
 * 
 * @return double time in milliseconds
 */
DINFER_API double GetTimestampMS();

} // namespace dInfer

#endif // DINFER_OSAL_TIME_H_
