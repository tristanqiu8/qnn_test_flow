/*
 * Description
 *   Dynamic Loading module
 *   <table>
 *   \Author         Date        Change Description
 *   ----------     ----------  -------------------
 *   Lucas.lv       2024.12     Reference from QNN 2.29.0.241129 SampleApp
 *   </table>
 */

#ifndef DINFER_OSAL_DL_H_
#define DINFER_OSAL_DL_H_

#include "dInfer/osal/common.h"
#include "dInfer/osal/log.h"

#include <string>

namespace dInfer {

// we only support subset of POSIX of dlopen/dlsym/dladdr/dlerror/dlclose
// except the following flags for dlopen, others should be done only
// when we really need them
// DL_NOW is MUST
// DL_LOCAL is enabled if not specified
enum {
  DL_NOW    = 0x0001,
  DL_LOCAL  = 0x0002,
  DL_GLOBAL = 0x0004,
  DL_LAZY   = 0x0008,
  DL_NODELETE = 0x0010,
};

// specify this address to distingiush from NULL pointer
#define DL_DEFAULT (void *)(0x4)

//---------------------------------------------------------------------------
/// @brief
///   Loads the dynamic shared object
/// @param filename
///   If contains path separators, treat it as relative or absolute pathname
///   or search it for the rule of dynamic linker
/// @param flags
///   - DL_NOW: resolve undefined symbols before return. MUST be specified.
///   - DL_LOCAL: optional, but the default specified. Symbols defined in this
///     shared object are not made available to resolve references in subsequently
///     loaded shared objects
///   - DL_GLOBAL: optional, resolve symbol globally
///   - DL_LAZY: optional, load the library lazily
///   - DL_NODELETE: optional, do not unload the library when dlclose is called
/// @return
///   On success, a non-NULL handle for the loaded library.
///   On error, NULL
//---------------------------------------------------------------------------
DINFER_API void *dlOpen(const char *filename, int flags);

//---------------------------------------------------------------------------
/// @brief
///   Obtain address of a symbol in a shared object or executable
/// @param handle
///   A handle of a dynamic loaded shared object returned by dlopen
/// @param symbol
///   A null-terminated symbol name
/// @return
///   On success, return the address associated with symbol
///   On error, NULL
//---------------------------------------------------------------------------
DINFER_API void *dlSym(void *handle, const char *symbol);

//---------------------------------------------------------------------------
/// @brief
///   Translate the address of a symbol to the path of the belonging shared object
/// @param addr
///   Address of symbol in a shared object
/// @param path
///   Full name of shared object that contains address, usually it is an absolute path
/// @return
///   On success, return a non-zero value
///   On error, return 0
//---------------------------------------------------------------------------
DINFER_API int dlAddrToLibName(void *addr, std::string &name);

//---------------------------------------------------------------------------
/// @brief
///   Decrements the reference count on the dynamically loaded shared object
///   referred to by handle. If the reference count drops to 0, then the
///   object is unloaded.
/// @return
///   On success, 0; on error, a nonzero value
//---------------------------------------------------------------------------
DINFER_API int dlClose(void *handle);

//---------------------------------------------------------------------------
/// @brief
///   Obtain error diagnostic for functions in the dl-family APIs.
/// @return
///   Returns a human-readable, null-terminated string describing the most
///   recent error that occurred from a call to one of the functions in the
///   dl-family APIs.
///   On Windows, returns an empty string if no error occurred.
///   On POSIX, returns NULL if no error occurred.
//---------------------------------------------------------------------------
DINFER_API char *dlError(void);

template <class T>
inline T resolveSymbol(void* libHandle, const char* sym) {
  T ptr = (T)dlSym(libHandle, sym);
  if (ptr == nullptr) {
    LOGI("Unable to access symbol [%s]. dlError(): %s\n",
              sym,
              dlError());
  }
  return ptr;
}

}

#endif // DINFER_OSAL_DL_H_