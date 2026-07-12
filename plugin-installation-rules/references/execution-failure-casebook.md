# AI 插件安装执行失败案例库

本文件保存插件安装、启用、验证和回退的脱敏经验，归属 `plugin-installation-rules`；官方仓库是安装命令唯一来源。

## 统一维护规则

- 状态使用 `candidate`、`active`、`stale`、`superseded`、`rejected`。
- 按插件、AI 平台、官方版本和验证入口匹配 active；第三方旧命令不得作为解决方案。
- 安装失败时先回退常规流程；candidate 必须包含官方来源和复验结果。

## PLUGIN-001

- 状态：`active`
- 类型：平台安装入口
- 错误特征：把第三方文章中的旧命令当作当前插件安装命令，导致命令不存在或安装错误
- 根因：第三方转述与官方仓库当前安装方式不一致
- 解决方案：回到官方仓库 README，按当前 AI 平台选择官方安装入口；确认安装后再验证
- 验证：插件在当前 AI 环境可见并能完成最小能力检查
- 禁止动作：臆造命令、沿用旧参数、把未验证安装写成成功
- 来源：`plugin-installation-rules/SKILL.md` 官方来源约束
- 最后验证：2026-07-12

## PLUGIN-002

- 状态：`active`
- 类型：交互式安装阻断
- 错误特征：安装需要用户执行斜杠命令，Agent 无法直接触发
- 根因：当前平台安装入口是交互式用户动作
- 解决方案：明确提示用户执行官方命令，等待确认后再做可用性验证；期间回退常规流程
- 验证：用户确认安装后，按官方方式检查插件已启用
- 来源：`plugin-installation-rules/SKILL.md` 必装插件流程
- 最后验证：2026-07-12

## PLUGIN-003

- 状态：`active`
- 类型：provisioning/runtime owner 分流
- 错误特征：插件已启用并在任务执行期间失活、崩溃、超时或无响应
- 根因：运行期插件或宿主生命周期故障，不是安装、启用或首次可用性问题
- 解决方案：保留插件标识、AI 平台、版本和最小脱敏失败证据，转交 `agent-runtime-recovery-rules` 的 `plugin_runtime_unhealthy`；由 adapter 能力协商决定 reload/restart/resume。不得猜测 CLI、进程名或 UI 操作
- 验证：运行期 owner 以原成功标准完成健康探针和恢复后验证；无 adapter 能力时明确 `manual_handoff`/`blocked`
- 禁止动作：将运行期失活写入本安装 casebook 的恢复方案；把重新安装插件宣称为通用 runtime recovery
- 来源：`execution-failure-learning-rules/references/classification-and-routing.md` provisioning/runtime 分流
- 最后验证：2026-07-12
