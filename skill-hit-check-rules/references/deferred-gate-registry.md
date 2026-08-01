# 延迟触发 gate 注册表

本表是「延迟触发类 skill（B 类）」的单一真相源，供三处共用：首条 `闸门预告` 字段登记、中段/收口双复检、`skill-execution-compliance-gate-rules` 末端审计。

「延迟触发」指触发点晚于每轮开头的首条命中检查——在**中段改码 / 收口前 / 测试前 / 失败时 / 提交前**才该触发。这类 gate 若不在首条预声明，就只能靠 agent「到点自觉」，存在结构性漏触发风险。首条命中检查必须按本表 + 当前任务类型，把本轮预计将适用的 gate 登记进 `闸门预告` 字段；`闸门预告` 是预测，中段按真实改动对账修正，收口按其逐项复核声明与执行是否一致。Plan Mode 下 `闸门预告:不适用(Plan Mode)`。

## 触发检查点定义

- `收口前`：准备输出本轮最终回复 / 结束输出阶段。
- `中段改码`：本轮首次发生代码新增或修改之后。
- `测试前`：功能代码完成、准备进入测试或验证。
- `失败时`：非预期工具 / 命令 / API / 环境失败发生当下（无法首条预测，只登记「若失败则触发」）。
- `提交前`：`git commit` 之前（由 `git-collaboration-rules` 自身承载，本表只登记）。

## 注册表

| gate skill | 触发检查点 | 任务类型前提（predicate） | 强制/条件 | 兑现说明 |
|---|---|---|---|---|
| `reasoning-summary-structure-rules` | 收口前 | 非 Plan Mode 的实质任务轮 | 强制 | 按其固定总结结构输出；恒为 `闸门预告` 成员 |
| `comment-completion-gate-rules` | 中段改码 + 收口前 | 本轮有任意代码新增/修改 | 强制 | 改动位点注释补齐闸门，缺项不得收口 |
| `comment-placement-granularity-rules` | 中段改码 | 本轮有任意代码新增/修改 | 强制 | 与上一条联动，判定注释落点与颗粒度 |
| `code-style-consistency-rules`（`6-review`） | 测试后 | 真实测试完成、准备风格回归 | 强制 | 唯一活动风格回归入口，只输出 STYLE |
| `skill-execution-compliance-gate-rules` | 收口前 | 本轮命中多 skill / 有工具执行 / 改 skill 资产 | 强制 | 末端合规 PASS/FAIL |
| `execution-failure-learning-rules` | 失败时 | 非预期工具/命令/API/环境失败 | 条件 | 失败才触发，首条登记「若失败则触发」 |
| `code-change-finalization-gate-rules` | 收口前 | 本轮有代码/测试改动且准备最终收口 | 强制 | 复核测试与 6-review 结果 |
| `artifact-delivery-gate-rules` | 收口前 | 本轮产生或应产生持久化研发文档 | 条件 | 文档落盘闸门 |
| `test-regression-rules` | 测试前 | Bug 修复 / 公共模块 / 接口兼容性变化后 | 条件 | 回归风险验证 |
| `functional-validation-rules` | 测试前 | 新功能或改动后功能待验证 | 条件 | 功能验证 |
| `bug-validation-rules` | 改动后 | Bug 修复后验证是否真修好、有无副作用 | 条件 | 修复验证 |
| `code-context-resync-rules` | 中段改码 | 继续修改已有代码且疑似文件内容漂移 | 条件 | 改前重读文件防脏写 |
| `autonomous-execution-rules` | 中段推进 | 多步任务尚未闭环且有必需下一步 | 条件 | 自动继续边界 |

## 维护约定

- 本表只登记 B 类延迟 gate；A 类首条即声明 skill（`parallel-task-dispatch-rules`/`git-collaboration-rules`/`obsidian-knowledge-flow`/`task-plan-rehydration-rules`）与 C 类领域 skill 不入表。
- 新增或调整 gate 触发时机时只改本表，`hit-checklist.md` 各「场景补充」引用本表、不复制清单，避免双维护。
