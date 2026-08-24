# 来源记录（source-notes）

> 归属 owner：`code-quality-rules`。登记本 skill 历次调整的来源与落点，与 `workbuddy-absorption-map.md` 配套。

## 2026-08-23：内部更新——删除纪律

- **调整类型**：内部更新通道。
- **调整诉求**：删除代码/功能必须彻底（remove 语义），禁止 xxxv2 备份版本，禁止记忆残留"禁止使用"描述。
- **触发场景**：用户在主会话提出 agent 把"删除"执行成"废弃"，留下 xxxv2 备份和记忆警示。
- **落点**：
  - 主定义：`code-quality-rules/references/code-removal-discipline.md`（新建）
  - 入口引用：`code-quality-rules/SKILL.md` 最小改动主线核心约束 + references 读取规则
  - 联动补充：`project-memory-rules/SKILL.md` 写入规则
- **裁决依据**：见 `../code-quality-rules/workbuddy-absorption-map.md` 2026-08-23 段落。
- **未落盘内容**：无。
- **外部源**：无（内部更新通道）。

## 2026-08-23：外部吸收——cd-debug（调试排错特工）

- **调整类型**：外部吸收通道。
- **外部源**：skillhub 市场 `cd-debug__skillhub`（调试排错特工 v1.0.0，作者 smart）。
- **调整诉求**：吸收「定位报错根因，给最小改动的修复方案」中的最小改动部分规则。
- **裁决结论**：7 条原子精华中 5 条保留本地（本地已更强）、2 条拒绝（触发体系冲突 + 商业形态）、0 条合并 → 无落盘改动；最小改动规则权威仍在 `minimal-change-general.md` / `minimal-change-boundaries.md` / `minimal-change-examples.md`，入口协调见 `bug-fix-proposal-rules`「与最小改动的协调」。
- **落点**：无（裁决登记于 `workbuddy-absorption-map.md` 2026-08-23 段落）。
- **未落盘内容**：全部未落盘——外部源无超出本地的规则细节。
- **外部源删除**：已删除用户级 + 工作区两份安装源（md5 一致）。