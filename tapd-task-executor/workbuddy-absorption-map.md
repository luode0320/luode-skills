# 吸收裁决表

> 本文件记录 tapd-task-executor 的内部调整与执行中 gap 回补。

| 日期 | 来源 | 条目 | 本地现状 | 裁决 | 落点 | 整理去重（含同域清理） | 环境依赖 | agent 通用性 |
|---|---|---|---|---|---|---|---|---|
| 2026-10-12 | 内部调整（用户会话） | 根据个人每日可用开发时间、日历占用与 TAPD 同迭代任务负载，估算 Story 子 Task 的预计开始 / 截止日期；显式处理未排期任务的不确定性，更新目标后 CLI 回读 | 子 Task 规则已有工时估算与创建后字段回读，但无个人日容量排期流程 | 合并 | references/story-bug-task-workflow.md §一.4 | 追加在子 Task 创建规则之后；扫描 tapd-task-executor、tapd-cli、tapd-openapi，未发现同域重复，0 处清理 | N/A + 理由：纯规则文本，复用已连接的日历与 TAPD CLI，不新增环境配置 | 通用 |
| 2026-11-23 | 内部调整（用户会话） | TAPD 流程强制命令行，绝对禁止浏览器；CLI 不支持的工作流查询不转网页或直接 API | 原规则允许 CLI 不足时回退直接 API，再回退浏览器；任务执行器另有直接脚本补位 | 合并 | SKILL.md §3 与 references/story-bug-task-workflow.md §零、cli-field-pitfalls.md、qa-assignment-rules.md | 删除直接 API 补位与浏览器回退句；工作流读取改为 CLI 当前状态 + 字段候选 + 逐跳回读，遗留能力缺口如实报告 | 无新增配置，复用现有 CLI 凭据预检 | 通用 |
