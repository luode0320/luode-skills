# TASK-REQ-01-02 真实测试

结论：PASS；影响：新增五阶段验证器与 fixtures 已由当前磁盘状态和本地验证入口证明；范围：本任务冻结 write set；非范围：其他任务和 Git 历史；变化：执行专项 phase 或 Quick Validate；完成标准：退出码 0、valid=true、无活跃旧消费者；术语说明：scoped 表示只核验本任务 Owner 和引用边界；验证状态：已通过。

## 输入与命令

- 基线提交：`76ee419d59396d919fea04ed55ea373ddeb8cb26`。
- 入口：`python -B doc/5-tests/2026-07-22_231500/requirement-domain-streamlining/validate_requirement_domain_streamlining.py --repo-root F:\luode-skills --manifest doc/5-tests/2026-07-22_231500/requirement-domain-streamlining/mapping/requirement-domain-manifest.yaml --phase baseline`。
- 相关修改 Skill 同时执行 `quick_validate.py`，全部退出码为 0。

## 样本、断言与失败预期

| 项目 | 内容 |
| --- | --- |
| 正向断言 | Owner、route、reference、consumer 或字典状态符合 manifest |
| 负向断言 | 旧活跃入口、双 Owner、缺失路径、单行 Markdown 或 planned_missing 不得出现 |
| 失败预期 | 任一断言失败即退出码 1，并保持候选 HOLD |
| 清理 | 无临时业务数据；只保留工程证据 |
| 回滚 | 使用 baseline commit、冻结 SHA 和候选路径恢复本任务 |

## 证据

- `doc/5-tests/2026-07-22_231500/requirement-domain-streamlining/evidence/trigger-result.json`。
- 14 条自然语言 prompt 已真实经过确定性 `route_prompt()`；实际 owner/route、负向排除、重复 ID、Skill 名称自证、NFKC/空白规范化和无关文本不误入均通过。
- baseline 已校验 Git blob 与 LF/CRLF 工作树指纹、13 个消费者精确集合、9 个既有总控保护契约精确集合和 6 个候选的 `worktree_hash`。
- reference 已校验四个 Owner 的唯一 `agents/openai.yaml`、Owner 名称、22 个冻结 reference 资产、递归可达性、无 scripts，以及 splitting/change 全资产树禁止实施 Owner 标题。
- N/A：本任务不连接外部服务，不产生图片或数据库数据。
