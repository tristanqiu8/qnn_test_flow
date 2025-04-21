# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [unreleased]

### Added

- 支持`Mac Intel`平台

## [1.8.0] - 2025-03-13

### Added

- C API添加`qnn_signed_pd`选项，用于启用签名进程域
- C API添加`dInferGetTensor()`接口，用于通过名字获取输入输出tensor

## [1.7.0] - 2025-03-07

### Changed

- IOS平台使用dylib方式集成，使能`CoreML`、`TFLite`、`MNN`框架

### Added

- `CoreML`添加`high_performance`配置

### Fixed

- 修复了`CoreML`的`stride`处理错误
- 修复了`CoreML`模型解密前没有清理残留临时文件夹的问题
- 修复了`MacOS`/`iOS`Objective-C生命周期问题


## [1.6.0] - 2025-03-05

### Added

- 添加`dInfer_type.h`头文件，统一C/C++类型定义，并提供类型字符串转换API
- `osal/filesystem`模块添加`GetCurrentDir()`API
- `osal/env`模块机型识别API适配`QCOM_LE`平台

### Changed

- 升级`ANDROID`/`QCOM_LE`编译`QNN`版本为`2.31`，支持`SM8625（8gen3）`
- 升级`dInferNetRun`测试工具，支持多任务并发配置，支持框架：`QNN`/`TRT`/`MNN`/`TFLite`

### Fixed

- 修复了`DINFER_LOG_WARNING`的拼写错误
- 修复了`qnn_load_from_cache`解析逻辑的错误

### Deprecated

- 未来可能移除的标记API、类型、成员已标记为`DINFER_DEPRECATED`，编译时如果使用到会进行警告，请用户尽快迁移到新名称

## [1.5.1] - 2025-02-11

### Added

- 支持Jetson平台dInferNetRun工具

### Fixed

- 修复了[MACLEARN-17065](https://jira-rd.djicorp.com/browse/MACLEARN-17065): TRT重复创建Context导致推理耗时异常

## [1.5.0] - 2025-02-05

### Added

- 支持Windows平台TRT框架
- 支持Windows平台dInferNetRun工具
- 编译系统V2支持Linux平台，并支持TRT动态加载
- 添加dInfer/osal/cuda.h模块，用于识别CUDA环境
- dInfer/utils.h模块添加版本查询接口

### Changed

- dInfer/osal/env.h模块中的GetEnv接口支持获取环境变量长度

### Bugs

- [MACLEARN-17065](https://jira-rd.djicorp.com/browse/MACLEARN-17065): TRT重复创建Context导致推理耗时异常

## [1.4.0] - 2025-01-16

### Added

- 支持Jetson平台TRT框架

### Bugs

- [MACLEARN-17065](https://jira-rd.djicorp.com/browse/MACLEARN-17065): TRT重复创建Context导致推理耗时异常

## [1.3.0] - 2025-01-08

### Added

- 支持Windows平台MNN框架，可用后端：CPU/CUDA/OpenCL
- 升级QNN版本为2.29，适用于ANDROID/QCOM_LE系统，支持高通 8 Gen 4
- 添加用户指南文档，位于`${dInferSDK}/${PLATFORM}/doc/User_Guide`
- 开放系统抽象层OSAL（Operation System Abstraction Layer）接口供用户使用，位于`${dInferSDK}/${PLATFORM}/include/dInfer/osal`
- 开放工具函数供用户使用，位于`${dInferSDK}/${PLATFORM}/include/dInfer/utils.h`

### Changed

- QNN2.29以上版本，请使用**QNN高阶API V2**，详情参考用户指南

## [1.2.8] - 2024-12-30

### Fixed

- 修复了模型解密的错误：在拷贝加密模型到临时路径前，会首先清空并删除残留的临时文件，以防万一

## [1.2.7] - 2024-11-14

### Added

- 增加QNN功耗配置接口，用户可精确控制模型运行和空闲时的功耗配置

## [1.2.6] - 2024-09-18

### Added

- 支持ARMv7a平台MNN推理

## [1.2.5] - 2024-09-05

### Changed

- 优化Objective-C的错误日志输出

## [1.2.4] - 2024-09-05

### Deprecated

- dInferLayout已被弃用，不建议前后处理依据该信息解释Tensor
    - 前后处理应该依据模型转换时确定的layout解释Tensor
    - 推理框架API层面只关注dims、data_type、stride等信息用于内存管理，且推理框架也无法从模型中获取layout信息
    - layout取决于模型如何训练、导出、转换，且因任务的不同而不同，不可穷举

### Changed

- CoreML不再处理`input_layout`选项，仅根据模型内部dim、data_type信息分配内存
- MAC_ARM64启用`USING_NEON`编译选项

### Fixed

- 修复 IOS_HG308编译未启用TFLite问题
- 修复 CoreML 加密模型解析失败问题

## [1.2.3] - 2024-08-21

### Added

- 添加对MAC_ARM64平台的支持

### Changed

- 模型解密使用NEON/多线程加速

## [1.2.2] - 2024-08-12

### Added

- iOS平台支持编译动态库
- iOS平台动态库支持MNN框架

## [1.2.1] - 2024-07-18

### Changed

- 优化 TensorRT 序列化模型加载速度
    - NOTE: 通过dInfer接口获取的输入输出tensor顺序将不再与ONNX保持一致，强烈建议用户使用 GetTensor() 接口通过 name 索引

## [1.2.0] - 2024-07-05

### Added

- 增加QNN功耗配置接口，用户可精确控制功耗配置

### Changed

- C API中的 dInferModelInfo_C 结构体增加预留字段，结构体大小增加

## [1.1.2] - 2024-06-28

### Fixed

- 修复 QNN device 对象导致的内存泄漏

## [1.1.1]

### Added 

- 增加 DINFER_NCS Layout
- QNN HTP 增加 PERFORMANCEv2, BALANCEDv2, POWER_SAVERv2 功耗配置

### Fixed

- 修复 CoreML tensor length 成员未更新等问题
- 修复 QNN app 对象导致的内存泄漏

### Enhanced

- 优化 CoreML 

## [1.1.0]

### Added

- 添加 `GetTensor()` API
- 添加`qnn_shared_buffer`选项以支持共享内存

### Fixed

- 修复 MNN tensor data.type 未更新问题
