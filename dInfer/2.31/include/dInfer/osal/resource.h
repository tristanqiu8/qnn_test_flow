#ifndef DINFER_OSAL_RESOURCE_H_
#define DINFER_OSAL_RESOURCE_H_

#include "dInfer/osal/common.h"

#include <cstdint>
#include <vector>

namespace dInfer {

/**
 * @brief Get the memory usage of the current process
 * 
 * @param vm_usage Virtual memory usage in kB
 * @param resident_set Physical memory usage in kB
 */
DINFER_API void MemUsage(double& vm_usage, double& resident_set);

/**
 * @brief Get the peak virtual memory usage of the current process
 * 
 * @return Peak virtual memory usage in kB
 */
DINFER_API long GetPeakMemoryUsage();

/**
 * @brief Get the peak physical memory usage of the current process
 * 
 * @return Peak physical memory usage in kB
 */
DINFER_API long GetPeakPhysicalMemoryUsage();

/**
 * @brief Get the CPU time used by the current process (user and kernel mode)
 * 
 * @return CPU time in ms
 */
DINFER_API double GetCpuTime();

/**
 * @brief Start sampling the CPU load of the current process at the specified interval
 * 
 * @param interval_ms Sampling interval in milliseconds
 */
DINFER_API void StartSamplingCpuLoading(uint64_t interval_ms);

/**
 * @brief Stop sampling the CPU load and return the sampling results
 * 
 * @return A reference to a vector containing the CPU load samples
 */
DINFER_API const std::vector<float>& StopSamplingCpuLoading();

} // namespace dInfer

#endif // DINFER_OSAL_RESOURCE_H_
