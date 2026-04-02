---
name: test-task-root-layout-rules
description: 当为当前需求、当前 Bug 或当前验证任务新增测试任务目录，或需要决定 `test/` 根目录下的当天时间戳根目录、中文说明目录和 ASCII 真实代码路径镜像布局时触发。负责统一测试任务根目录创建、当天时间戳校验、中文 README 说明目录和真实测试资产镜像布局；不要用它代替散落测试资产迁移、Go 编译路径冲突处理、测试命名规则或测试程序实现规则。
---

# 测试任务根布局规则

只在“当前测试任务的根目录和布局该怎么建”这个问题上使用本 skill。
它负责把测试任务先放到正确的根目录和时间戳根目录下，再把中文说明目录和 ASCII 资产镜像目录布置完整。

## Skill 作用与适用场景

- 决定新的测试任务应该放到 `test/` 根目录下的哪个当天时间戳目录。
- 统一中文说明目录、`README.md` 和真实测试资产镜像目录的并列布局。
- 统一“时间戳根目录只放时间戳、不混中文”的根布局规则。
- 统一“真实测试资产按真实代码路径镜像、且保持 ASCII”的落点规则。
- 在进入测试命名、测试程序编写或测试文档组织前，先把目录骨架定准。

## 自动触发信号

- 新增测试任务目录或准备写入新的测试资产。
- 需要决定是否创建新的当天时间戳根目录。
- 需要为当前测试任务创建中文说明目录和 `README.md`。
- 需要把真实测试资产映射到 ASCII 真实代码路径镜像目录。
- 同一需求存在多轮独立验证，需要判断是否拆成多个时间戳根目录。

## 强制规则

- 统一使用 `test/` 作为测试根目录，不得改用 `tests/`、`qa/`、`verify/` 等名称。
- 默认新测试任务必须创建当天时间戳根目录，命名格式为 `yyyy-MM-DD_HHmmss`。
- 若检测到目标目录日期早于运行时当天日期，必须暂停并询问用户是否明确复用旧目录。
- 未获明确许可前，禁止把新文件写入历史时间戳目录；读取历史目录仅可作为参考。
- 每个时间戳根目录都必须同时包含一个中文说明目录和一个或多个 ASCII 真实代码路径镜像目录。
- 中文说明目录默认只存放 `README.md`，不承载真实测试代码、脚本、mock、fixture、日志或报告产物。
- 真实测试资产必须按真实代码路径镜像组织；若无法精确映射到单一源码文件，至少映射到最接近的源码模块路径。
- 同一需求的多个独立测试验证，默认拆成多个时间戳根目录，而不是强行混在一个目录里。

## 默认执行流程

1. 先读 `../artifact-storage-rules/references/path-map.yaml`、`../artifact-storage-rules/references/naming-templates.md` 与 `../artifact-storage-rules/references/update-policy.md`，确认中央约定的测试根目录与复用策略。
2. 再读 `references/task-root-layout.md`，确认时间戳根目录、中文说明目录和 ASCII 镜像目录的布局规则。
3. 判断当前任务应新建当天时间戳根目录，还是在用户明确允许时复用旧目录。
4. 先创建时间戳根目录，再创建中文说明目录和 `README.md`。
5. 最后为真实测试资产准备 ASCII 镜像目录，等待后续 `test-program-rules` 或 `test-doc-rules` 继续落盘。

## 权责边界与不负责事项

- 只负责测试任务根目录和布局，不负责散落资产迁移。
- 不负责 Go 编译路径冲突、源码目录 `*_test.go` 禁放和 seam 方案，那属于 `go-test-compile-path-rules`。
- 不负责测试名称本身，那属于 `test-naming-rules`。
- 不负责测试程序写法，那属于 `test-program-rules`。
- 不负责测试说明内容结构，那属于 `test-doc-rules`。

## 通过 / 驳回标准

- 通过：当前测试任务已放在 `test/` 根目录下的当天时间戳根目录中，中文说明目录和 `README.md` 已就位，真实测试资产镜像目录保持 ASCII，且没有把新文件误写到未经允许的历史目录。
- 驳回：根目录名称不合规、时间戳目录不是当天且未获明确复用许可、中文说明目录缺失、`README.md` 缺失，或真实测试资产没有准备 ASCII 镜像目录。

## references 读取规则

- 默认先读 `references/task-root-layout.md`。
- 需要确认中央约定路径时，再读 `../artifact-storage-rules/references/path-map.yaml`、`../artifact-storage-rules/references/naming-templates.md` 与 `../artifact-storage-rules/references/update-policy.md`。
