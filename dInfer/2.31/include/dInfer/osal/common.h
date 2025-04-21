#ifndef DINFER_OSAL_COMMON_H_
#define DINFER_OSAL_COMMON_H_

#ifdef _WIN64

#ifdef EXPORT_DINFER_API
#define DINFER_API __declspec(dllexport)
#else
#define DINFER_API __declspec(dllimport)
#endif  // EXPORT_DINFER_API

#else
#define DINFER_API
#endif  // _WIN64

// Items that are marked as deprecated will be removed in a future release.
#if __cplusplus >= 201402L
#define DINFER_DEPRECATED(msg) [[deprecated(msg)]]
#if __GNUC__ < 6
#define DINFER_DEPRECATED_ENUM(msg)
#else
#define DINFER_DEPRECATED_ENUM(msg) DINFER_DEPRECATED(msg)
#endif
#ifdef _MSC_VER
#define DINFER_DEPRECATED_API(msg) __declspec(dllexport)
#else
#define DINFER_DEPRECATED_API(msg) [[deprecated(msg)]] __attribute__((visibility("default")))
#endif
#else // __cplusplus < 201402L
#ifdef _MSC_VER
#define DINFER_DEPRECATED(msg)
#define DINFER_DEPRECATED_ENUM(msg)
#define DINFER_DEPRECATED_API(msg) __declspec(dllexport)
#else
#define DINFER_DEPRECATED(msg) __attribute__((deprecated(msg)))
#define DINFER_DEPRECATED_ENUM(msg) DINFER_DEPRECATED(msg)
#define DINFER_DEPRECATED_API(msg) __attribute__((deprecated(msg), visibility("default")))
#endif
#endif

#endif // DINFER_OSAL_COMMON_H_
