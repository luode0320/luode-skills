# 来源记录

## 2026-10-13 PROJECT_CURRENT 多会话写入保护

- 来源：内部规则调整；任务投影多会话审计发现，普通当前状态的整文件写入必须与 projection 和最近会话摘要写入共用文件锁。
- 裁决：补充普通正文写入的共享 `.PROJECT_CURRENT.md.lock`、持锁重读、只改自有正文区、原样保留两个托管区、写入失败不覆盖原文要求。
- 依据：`task-plan-rehydration-rules/references/task-plan-projection-contract.md` 的共享文件读改写契约；`project-memory-rules/scripts/sync_recent_project_sessions.py` 的 `acquire_lock` 与持锁重读实现。
- 整理去重：具体锁路径和投影身份仍由任务投影 Owner 契约定义；本 Skill 仅引用并限定普通正文写入责任。

## 2026-10-13 PROJECT_CURRENT 投影容量超限自恢复

- 来源：用户明确要求任务投影因 `PROJECT_CURRENT.md` 超过 51,200 UTF-8 字节时，不得阻断任务，应主动清理并压缩历史信息。
- 裁决：投影 Owner 因容量上限拒绝写入后，调用本 Skill 在共享锁内重读最新全文，只压缩普通正文中最旧的已完成历史；精确保留 v5 registry（含 `quarantined_projections`）、最近会话快照及所有活动/未验证/授权状态。压缩后重新计算并由 Owner 重试，最多两轮；若无法安全释放空间则保留原文件、标记 projection 未持久化并继续领域任务。
- 风险边界：不得把 registry 结构错误、身份冲突、UTF-8/标记损坏、锁失败等误判为容量问题；不得改写托管区或静默截断。普通投影不能落盘时，宿主 UI 可独立同步但需如实报告持久化状态。
- 依据：`task-plan-rehydration-rules/SKILL.md` 的容量失败路由及 `references/task-plan-projection-contract.md` 的候选全文字节校验；本 Skill 保持正文压缩职责。
- 验证：两个受影响 Skill 的 `quick_validate.py` 均通过；独立只读审阅完成超限可压缩、无安全空间/锁失败、非容量错误三种规则场景走查，覆盖判断正确但不代表脚本运行测试通过。投影回归套件运行 84 项，7 项失败、3 项错误，包含针对 v4 的旧断言与临时锁超时；知识索引修复失效 SSH 备份笔记引用后复查 310 篇笔记、803 条链接、死链 0、结构违规 0；UTF-8/LF/无尾随空白检查通过。`git diff --check` 退出码 0；`git status --short` 无法读取缺失 tree 对象，工作区完整状态不能确认。`PROJECT_CURRENT.md` 未由本次规则修改写入。
