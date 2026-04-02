---
name: go-test-compile-path-rules
description: 当 Go 项目中的测试路径会进入编译链路、出现源码目录 `*_test.go`、中文可编译路径，或存在白盒同包测试诉求时触发。负责统一 Go 测试可编译路径必须保持 ASCII、源码目录禁放 `*_test.go`、白盒诉求改用 seam 方案，并把测试资产收回中央测试根目录；不要用它代替测试任务根目录创建、散落测试资产迁移、测试命名规则或测试程序实现规则。
---

# Go 测试编译路径规则

只在“Go 测试路径会影响编译和扫描链路”这个问题上使用本 skill。
它负责拦住源码目录 `*_test.go`、中文可编译路径和白盒同包落地这几类最容易把测试规则打穿的场景。

## Skill 作用与适用场景

- 处理 Go 源码目录出现 `*_test.go` 的禁放问题。
- 处理中文目录进入 Go 可编译测试路径的问题。
- 处理白盒同包测试诉求，并把它收口到 seam 方案。
- 在 Go 场景下判断测试资产应如何保持 ASCII 可编译路径。

## 自动触发信号

- 准备在 Go 源码目录创建或修改 `*_test.go`。
- 发现 `go test ./...` 会扫描到中文测试包路径。
- 需要访问未导出符号，准备走同包白盒测试。
- 发现测试目录虽然在 `test/` 下，但镜像路径仍包含中文或不可编译路径。

## 强制规则

- Go 源码目录绝对不允许出现 `*_test.go`。
- 会被 Go 编译链路扫描的测试目录路径必须保持 ASCII。
- 白盒同包诉求不是例外通道；统一处理方式是先改 seam，再把测试资产放回 `test/<时间戳>/` 的 ASCII 镜像路径。
- 若某个测试文件既违规落在源码目录，又属于散落资产，同时触发 `test-scattered-asset-location-rules` 处理迁移。

## 默认执行流程

1. 先读 `references/go-compile-path.md`，判断当前问题属于源码目录禁放、中文编译路径还是白盒同包诉求。
2. 如果当前测试任务目录尚未建立，先转交 `test-task-root-layout-rules`。
3. 若当前文件散落在非测试目录，同时转交 `test-scattered-asset-location-rules`。
4. 根据引用文档选择对应整改动作：改 seam、迁移到 `test/<时间戳>/` ASCII 镜像路径、清理中文可编译路径。
5. 复核 `go test ./...` 不再因路径问题失真后，再进入后续测试程序实现阶段。

## 权责边界与不负责事项

- 只负责 Go 测试编译路径和禁放规则，不负责测试任务根布局。
- 不负责一般性的散落资产迁移，那属于 `test-scattered-asset-location-rules`。
- 不负责测试程序实现细节、断言写法或测试说明组织。

## 通过 / 驳回标准

- 通过：源码目录不存在 `*_test.go`，Go 可编译测试路径保持 ASCII，白盒诉求已改为 seam 方案，相关测试资产已回到中央测试根目录的正确镜像路径下。
- 驳回：仍试图在源码目录保留 `*_test.go`、仍允许中文进入 Go 可编译路径，或把白盒同包落地当成长期特例。

## references 读取规则

- 默认先读 `references/go-compile-path.md`。
- 需要确定目标时间戳根目录时，再读 `../artifact-storage-rules/references/path-map.yaml` 与 `../artifact-storage-rules/references/update-policy.md`。
