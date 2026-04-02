# 测试命名边界

## 用途

用于区分"命名问题"与"落点问题、实现问题、需求问题"。

**重要：本规则必须以 `test-task-root-layout-rules` 为基础；所有关于测试资源放置位置的问题都属于 `test-task-root-layout-rules` 职责范围；若测试资产已经散落到错误目录，还要同步转交 `test-scattered-asset-location-rules`。**

## 这些问题属于命名域

- 测试任务中文说明目录应该叫什么。
- 测试文件、测试脚本、测试数据目录应该如何表达业务目标。
- 同类测试资产命名风格不一致，需要统一。
- 在确定时间戳根目录、中文说明目录和真实代码路径镜像目录时，确保三者各自承担正确命名职责。

## 这些问题不属于命名域

- 测试资源应该放在项目级测试目录还是模块内目录，那属于 `test-task-root-layout-rules`。
- 是否应该创建 `test/` 根目录，那属于 `test-task-root-layout-rules`。
- 时间戳根目录是否应该使用 `yyyy-MM-DD_HHmmss` 格式，那属于 `test-task-root-layout-rules`。
- 中文说明目录与真实代码路径镜像目录如何拆分，那属于 `test-task-root-layout-rules`。
- 测试程序如何拆函数、怎么写断言、怎么组织脚手架，那属于 `test-program-rules`。
- 测试文档怎么写章节、怎么记录结果，那属于 `test-doc-rules`。
- 功能是否满足需求、回归范围够不够，那属于功能验证和回归验证 skill。

## 必须遵循测试任务根布局与 Go 编译路径约定

在进入命名域之前，必须先确认以下约定已经满足：
1. 所有测试资产统一放在 `test/` 根目录下。
2. 时间戳根目录命名使用 `yyyy-MM-DD_HHmmss` 格式。
3. 中文说明目录单独使用本次测试任务中文主题命名（动态命名），并包含 `README.md`。
4. 真实测试路径按真实代码路径镜像组织，并保持 ASCII。
5. 同一需求的多个测试分别创建独立目录。

如果以上约定未满足，应先转交 `test-task-root-layout-rules` 处理；若测试资产已散落在错误目录，再同步转交 `test-scattered-asset-location-rules`。

## 需要回流的场景

- 名称无法确定，是因为需求边界不清或场景目标不清。
- 一个测试资产承载多个目标，本质上应先拆任务或拆目录。
- 名称变更将牵涉脚本入口、配置项或外部调用方，需要先确认影响面。
- 测试资产不在 `test/` 根目录下，需要先转交 `test-scattered-asset-location-rules`，并在必要时由 `test-task-root-layout-rules` 补齐目标根布局。
