#ifndef DINFER_OSAL_FILESYSTEM_H_
#define DINFER_OSAL_FILESYSTEM_H_

#include <cstdint>
#include <string>
#include <vector>

#include "dInfer/osal/common.h"

namespace dInfer {

/**
 * @brief Read a binary file
 * @param filename Name of the file
 * @param buffer Buffer to store the read data
 * @param buffer_size Size of the buffer
 * @return Returns 0 on success, -1 on failure
 */
DINFER_API int32_t ReadBinaryFile(const char *filename, void **buffer, size_t *buffer_size = nullptr);

/**
 * @brief Write to a binary file
 * @param buffer Buffer containing data to write
 * @param buffer_size Size of the buffer
 * @param filename Name of the file
 * @return Returns 0 on success, -1 on failure
 */
DINFER_API int32_t WriteBinaryFile(const void *buffer, size_t buffer_size, const char *filename);

/**
 * @brief Create a folder
 * @param file_path Path of the folder
 * @return Returns 0 on success, -1 on failure
 */
DINFER_API int32_t CreateFolder(const char *file_path);

/**
 * @brief Remove a binary file
 * @param filename Name of the file
 * @return Returns 0 on success, -1 on failure
 */
DINFER_API int32_t RemoveBinaryFile(const char *filename);

/**
 * @brief Get file paths with specified suffixes in a folder and append to filelist
 * @param path Path of the folder
 * @param filelist Vector to store file paths
 * @param suffixs Vector of file suffixes
 * @return Number of files
 */
DINFER_API int GetSuffixFiles(const std::string& path, std::vector<std::string> &filelist, std::vector<std::string> suffixs);

/**
 * @brief Check if the path (file or directory) is accessible
 * 
 * @param path The path to check
 * @return true If the path is accessible
 * @return false If the path is not accessible
 */
DINFER_API bool Access(std::string path);

/**
 * @brief Check if it is a file
 * @param filename Name of the file
 * @return Returns true if it is a file, otherwise false
 */
DINFER_API bool IsFile(std::string filename);

/**
 * @brief Get all filenames in a folder and append to filelist
 * @param path Path of the folder
 * @param filenames Vector to store filenames
 */
DINFER_API void GetFileNames(std::string path, std::vector<std::string>& filenames);

/**
 * @brief Get the file extension
 * @param filename Name of the file
 * @return File extension
 */
DINFER_API std::string GetExtensionName(const std::string &filename);

/**
 * @brief Calculate the SHA1 of a file
 * @param filename Name of the file
 * @param sha1sum SHA1 of the file
 * @return Returns 0 on success, -1 on failure
 */
DINFER_API int CalculateFileSHA1(const char *filename, std::string &sha1sum);

/**
 * @brief Calculate the SHA1 of a buffer
 * 
 * @param buffer 
 * @param size 
 * @param sha1sum 
 * @return Returns 0 on success, -1 on failure
 */
DINFER_API int CalculateBufferSHA1(const void *buffer, size_t size, std::string &sha1sum);

/**
 * @brief Get the current working directory
 * @return Current working directory, "." if failed
 */
DINFER_API std::string GetCurrentDir();

} // namespace dInfer

#endif // DINFER_OSAL_FILESYSTEM_H_
