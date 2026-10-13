# Skill 规则调整记录

| 来源 | 原子规则 | 本地现状 | 裁决 | agent 通用性 | 环境依赖 | 落点 | 整理去重 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 内部更新（PROJECT_CURRENT 多会话写入保护） | 同项目多个会话更新 PROJECT_CURRENT 时，普通正文写入必须与投影和最近会话摘要写入共用锁并持锁重读最新文件。 | 最近会话快照规则已要求共用 `.PROJECT_CURRENT.md.lock`，普通当前状态规则仅要求保留 registry 字节，未定义锁与并发合并。 | 补充共享锁、持锁重读、仅更新自有正文区域、两个托管区逐字节不变，以及锁失败/超限/原子写失败时原文件不变。 | 适用于所有使用本 Skill 维护项目当前状态的 agent。 | N/A：复用现有锁路径，不新增依赖。 | `SKILL.md` 的普通状态写入约束；依据见 `references/source-notes.md` 和 `task-plan-rehydration-rules` 持久化契约。 | 锁路径与投影身份只由任务投影 Owner 定义；本 Skill 只限定普通正文的并发写入，不复制 registry schema。 |
| 用户规则更新（PROJECT_CURRENT 投影容量超限自恢复） | 投影因全文超过 51,200 字节被拒绝时，主动压缩普通历史正文并重试；若安全压缩后仍不够，领域任务继续。 | 原规则要求 `PROJECT_CURRENT.md` 超限“阻断并压缩”，托管区保护要求完整保留，但未定义历史压缩、有限重试和执行降级。 | 通过共享锁重读最新文件，只合并/压缩最旧已完成历史，保留投影 registry、隔离项、最近会话快照和活动状态；最多两轮后仍超限则原文件不变、投影未持久化、任务继续。 | 所有维护项目当前状态的 agent；投影 Owner 负责超限路由，本 Skill 负责正文压缩。 | N/A：沿用 `.PROJECT_CURRENT.md.lock` 和既有原子写入。 | `SKILL.md` 的 `PROJECT_CURRENT 超限压缩` 及 `references/source-notes.md`；投影 Owner 契约作触发方。 | 不修改快照脚本和 registry schema，不删除唯一历史事实；细节只由本 Skill 持有。 |
