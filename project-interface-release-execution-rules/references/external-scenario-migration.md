# 外部场景兼容迁移与隔离工具环境

> 归属 owner：`project-interface-release-execution-rules`。本文件定义一个 schema 版本的兼容窗口和工具运行时边界。

## 兼容窗口

- 旧 CLI 命令、旧接口列表式结果读取和旧场景资产保留一个 schema 版本，并输出明确弃用提示。
- 旧接口结果即使历史状态为 PASS，迁移后也只能成为 PENDING，不能自动晋级 verified 或进入场景门禁。
- 迁移必须写入新文件，不覆盖输入；输入输出都必须位于项目根内。
- 下一主版本可以删除兼容包装，但删除前必须有迁移命令、回归证据和发布说明。

## 隔离工具环境

- 工具解释器要求 Python 3.11+，依赖安装在工具缓存或独立虚拟环境，不修改被测项目依赖。
- 锁定依赖由 `scripts/requirements.in` 和 `scripts/requirements.lock` 管理。
- doctor 只读检查解释器、锁定版本、可导入性和 HTTP/SSE/WebSocket/Socket.IO runtime，不发起网络连接。
- 缺包、版本漂移或 runtime 不可用时返回 BLOCKED/PENDING，禁止使用被测项目环境凑依赖。

## external 命令语义

- `external-generate` 只生成 candidate，成功仍返回退出码 4。
- `external-validate` 校验 schema、来源、local 前置条件和动作白名单，合法目录返回 0。
- `external-verify` 额外要求全部场景为 verified，且 loader 能重算绑定正向运行、故障识别、cleanup、verification run 及项目根内 artifact 路径/SHA-256 的 `external-verify/1.0` 晋级证明；candidate、仅手写五项布尔值或缺结构化运行摘要均返回 4/契约错误。
- `external-run` 默认进入 scenario 轨道；`release-run` 和旧 `run` 仍默认 legacy，仅显式参数可改变迁移期轨道。
- `external-migrate` 对旧结果生成独立新文件并保留 deprecated 标识。
- `external-doctor` 与 `release-run` 共享同一工具环境门禁。

## 停止条件

- 非 local 资产、项目根外路径、敏感值持久化、旧结果自动提升、工具依赖写入被测项目或迁移覆盖源文件时立即停止。
- 兼容测试、历史报告读取或 strict validator 失败时不得宣布最终验收通过。
