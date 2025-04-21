/*
 * Description
 *   dInfer advanced api for QNN
 *   <table>
 *   \Author         Date        Change Description
 *   ----------     ----------  -------------------
 *   Lucas.Lv       2024.06     Initialize.
 *   </table>
 */
#ifndef __DINFER_ADV_QNN_H__
#define __DINFER_ADV_QNN_H__

#include "dInfer/osal/common.h"
#include "dInfer/dInfer_type.h"
#include <stdint.h>

#ifdef __cplusplus
extern "C" {
#endif

/**
 * @brief Allows client to start (non-zero value) or stop (zero value)
 * participating in DCVS
 *
 */
typedef uint32_t dInferHtpPerfInfrastructure_DcvsEnable_t;

/**
 * @brief Allows client to set up the sleep latency in microseconds
 *
 */
typedef uint32_t dInferHtpPerfInfrastructure_SleepLatency_t;


/**
 * @brief Allows client to disable sleep or low power modes.
 * Pass a non-zero value to disable sleep in HTP
 *
 */
typedef uint32_t dInferHtpPerfInfrastructure_SleepDisable_t;

/**
 * @brief Allows client to set up the RPC control latency in microseconds
 *
 */
typedef uint32_t dInferHtpPerfInfrastructure_RpcControlLatency_t;

/**
 * @brief Allows client to set up the RPC polling time in microseconds
 */
typedef uint32_t dInferHtpPerfInfrastructure_RpcPollingTime_t;

/**
 * @brief These are the different voltage corners that can
 * be requested by the client to influence the voting scheme
 * for DCVS
 *
 */
typedef enum {
  /// Maps to HAP_DCVS_VCORNER_DISABLE.
  /// Disable setting up voltage corner
  DINFER_DCVS_VOLTAGE_CORNER_DISABLE = 0x10,
  /// Maps to HAP_DCVS_VCORNER_SVS2.
  /// Set voltage corner to minimum value supported on platform
  DINFER_DCVS_VOLTAGE_VCORNER_MIN_VOLTAGE_CORNER = 0x20,
  /// Maps to HAP_DCVS_VCORNER_SVS2.
  /// Set voltage corner to SVS2 value for the platform
  DINFER_DCVS_VOLTAGE_VCORNER_SVS2 = 0x30,
  /// Maps to HAP_DCVS_VCORNER_SVS.
  /// Set voltage corner to SVS value for the platform
  DINFER_DCVS_VOLTAGE_VCORNER_SVS = 0x40,
  /// Maps to HAP_DCVS_VCORNER_SVS_PLUS.
  /// Set voltage corner to SVS_PLUS value for the platform
  DINFER_DCVS_VOLTAGE_VCORNER_SVS_PLUS = 0x50,
  /// Maps to HAP_DCVS_VCORNER_NOM.
  /// Set voltage corner to NOMINAL value for the platform
  DINFER_DCVS_VOLTAGE_VCORNER_NOM = 0x60,
  /// Maps to HAP_DCVS_VCORNER_NOM_PLUS.
  /// Set voltage corner to NOMINAL_PLUS value for the platform
  DINFER_DCVS_VOLTAGE_VCORNER_NOM_PLUS = 0x70,
  /// Maps to HAP_DCVS_VCORNER_TURBO.
  /// Set voltage corner to TURBO value for the platform
  DINFER_DCVS_VOLTAGE_VCORNER_TURBO = 0x80,
  /// Maps to HAP_DCVS_VCORNER_TURBO_PLUS.
  /// Set voltage corner to TURBO_PLUS value for the platform
  DINFER_DCVS_VOLTAGE_VCORNER_TURBO_PLUS = 0x90,
  /// Maps to HAP_DCVS_VCORNER_TURBO_L2.
  /// Set voltage corner to TURBO_L2 value for the platform
  DINFER_DCVS_VOLTAGE_VCORNER_TURBO_L2 = 0x92,
  /// Maps to HAP_DCVS_VCORNER_TURBO_L3.
  /// Set voltage corner to TURBO_L3 value for the platform
  DINFER_DCVS_VOLTAGE_VCORNER_TURBO_L3 = 0x93,
  /// Maps to HAP_DCVS_VCORNER_MAX.
  /// Set voltage corner to maximum value supported on the platform
  DINFER_DCVS_VOLTAGE_VCORNER_MAX_VOLTAGE_CORNER = 0xA0,
  /// UNKNOWN value that must not be used by client
  DINFER_DCVS_VOLTAGE_VCORNER_UNKNOWN = 0x7fffffff
} dInferHtpPerfInfrastructure_VoltageCorner_t;

/**
 * @brief This enum defines all the possible power mode
 *        that a client can set to influence DCVS mode
 */
typedef enum {
  /// Maps to HAP_DCVS_V2_ADJUST_UP_DOWN.
  /// Allows for DCVS to adjust up and down
  DINFER_HTP_PERF_INFRASTRUCTURE_POWERMODE_ADJUST_UP_DOWN = 0x1,
  /// Maps to HAP_DCVS_V2_ADJUST_ONLY_UP.
  /// Allows for DCVS to adjust up only
  DINFER_HTP_PERF_INFRASTRUCTURE_POWERMODE_ADJUST_ONLY_UP = 0x2,
  /// Maps to HAP_DCVS_V2_POWER_SAVER_MODE.
  /// Higher thresholds for power efficiency
  DINFER_HTP_PERF_INFRASTRUCTURE_POWERMODE_POWER_SAVER_MODE = 0x4,
  /// Maps to HAP_DCVS_V2_POWER_SAVER_AGGRESSIVE_MODE.
  /// Higher thresholds for power efficiency with faster ramp down
  DINFER_HTP_PERF_INFRASTRUCTURE_POWERMODE_POWER_SAVER_AGGRESSIVE_MODE = 0x8,
  /// Maps to HAP_DCVS_V2_PERFORMANCE_MODE.
  /// Lower thresholds for maximum performance
  DINFER_HTP_PERF_INFRASTRUCTURE_POWERMODE_PERFORMANCE_MODE = 0x10,
  /// Maps to HAP_DCVS_V2_DUTY_CYCLE_MODE.
  /// The below value applies only for HVX clients:
  ///  - For streaming class clients:
  ///   - detects periodicity based on HVX usage
  ///   - lowers clocks in the no HVX activity region of each period.
  ///  - For compute class clients:
  ///   - Lowers clocks on no HVX activity detects and brings clocks up on detecting HVX activity
  ///   again.
  ///   - Latency involved in bringing up the clock will be at max 1 to 2 ms.
  DINFER_HTP_PERF_INFRASTRUCTURE_POWERMODE_DUTY_CYCLE_MODE = 0x20,
  /// UNKNOWN value that must not be used by client
  DINFER_HTP_PERF_INFRASTRUCTURE_POWERMODE_UNKNOWN = 0x7fffffff
} dInferHtpPerfInfrastructure_PowerMode_t;

typedef struct dInferHtpPowerConfig {
  dInferHtpPerfInfrastructure_DcvsEnable_t dcvsEnable;
  dInferHtpPerfInfrastructure_PowerMode_t powerMode;
  dInferHtpPerfInfrastructure_SleepLatency_t sleepLatency;
  dInferHtpPerfInfrastructure_SleepDisable_t sleepDisable;
  dInferHtpPerfInfrastructure_VoltageCorner_t busVoltageCornerMin;
  dInferHtpPerfInfrastructure_VoltageCorner_t busVoltageCornerTarget;
  dInferHtpPerfInfrastructure_VoltageCorner_t busVoltageCornerMax;
  dInferHtpPerfInfrastructure_VoltageCorner_t coreVoltageCornerMin;
  dInferHtpPerfInfrastructure_VoltageCorner_t coreVoltageCornerTarget;
  dInferHtpPerfInfrastructure_VoltageCorner_t coreVoltageCornerMax;
  dInferHtpPerfInfrastructure_RpcControlLatency_t rpcControlLatency;
  dInferHtpPerfInfrastructure_RpcPollingTime_t rpcPollingTime;
} dInferHtpPowerConfig_t;

/**
 * @brief Convert dInferHtpPerfInfrastructure_PowerMode_t to string
 * 
 * @param power_mode 
 * @return const char* power mode string
 * @throws std::invalid_argument if power_mode is not in dInferHtpPerfInfrastructure_PowerMode_t
 */
DINFER_API const char *StrPowerMode(dInferHtpPerfInfrastructure_PowerMode_t power_mode);

/**
 * @brief Convert string to dInferHtpPerfInfrastructure_PowerMode_t
 * 
 * @param str power mode string
 * @return dInferHtpPerfInfrastructure_PowerMode_t
 * @throws std::invalid_argument if str is not in {"ADJUST_UP_DOWN", "ADJUST_ONLY_UP", "POWER_SAVER_MODE", "POWER_SAVER_AGGRESSIVE_MODE", "PERFORMANCE_MODE", "DUTY_CYCLE_MODE"}
 */
DINFER_API dInferHtpPerfInfrastructure_PowerMode_t ToPowerMode(const char *str);

/**
 * @brief Convert dInferHtpPerfInfrastructure_VoltageCorner_t to string
 * 
 * @param voltage_corner 
 * @return const char* voltage corner string
 * @throws std::invalid_argument if voltage_corner is not in dInferHtpPerfInfrastructure_VoltageCorner_t
 */
DINFER_API const char *StrVoltageCorner(dInferHtpPerfInfrastructure_VoltageCorner_t voltage_corner);

/**
 * @brief Convert string to dInferHtpPerfInfrastructure_VoltageCorner_t
 * 
 * @param str voltage corner string
 * @return dInferHtpPerfInfrastructure_VoltageCorner_t
 * @throws std::invalid_argument if str is not in {"DISABLE", "SVS2", "SVS", "SVS_PLUS", "NOM", "NOM_PLUS", "TURBO", "TURBO_PLUS", "TURBO_L2", "TURBO_L3", "MAX"}
 */
DINFER_API dInferHtpPerfInfrastructure_VoltageCorner_t ToVoltageCorner(const char *str);

// special defines for Pure C API
#define DINFER_QNN_INPUT_CONFIG_NOT_SET   0
#define DINFER_QNN_OUTPUT_CONFIG_NOT_SET  0

// DINFER_MAX_LOG_TYPE means use the same level as dInferInitLog()
#define DINFER_QNN_DEFAULT_LOG_LEVEL      DINFER_LOG_DEFAULT


typedef struct dInferQnnOption{
    const char* lib_cache_path; // must be set while load from library
    bool  load_from_cache;      // set to load from cache(serialized.bin) rather than library
    bool  shared_buffer;        // set to use qnn htp shared buffer, host_addr = ion_addr, device_addr = fd
    bool  signed_pd;            // set to use signed pd
    dInferLogLevel_t log_level; // set log level
    dInferHtpPowerConfig_t* power_cfg;      // set to use custom qnn htp power cfg
    dInferHtpPowerConfig_t* power_run_cfg;  // set to use custom qnn htp power cfg for run
    dInferHtpPowerConfig_t* power_idle_cfg; // set to use custom qnn htp power cfg for idle
    int input_config;           // Reserved for v1 API
    int output_config;          // Reserved for v1 API
    const char *power_level;    // Reserved for v1 API
    uint64_t reserved[8];
} dInferQnnOption_t;

#define QNN_OPTION_INIT { \
    NULL, \
    false, \
    false, \
    false, \
    DINFER_MAX_LOG_TYPE, \
    NULL, \
    NULL, \
    NULL, \
    DINFER_QNN_INPUT_CONFIG_NOT_SET, \
    DINFER_QNN_OUTPUT_CONFIG_NOT_SET, \
    NULL, \
}

#ifdef __cplusplus
}
#endif

#endif // __DINFER_ADV_QNN_H__