# TASK-REQ-03-01 真实测试

结论：PASS；影响：修复 intake 自动触发口径 已由当前磁盘状态和本地验证入口证明；范围：本任务冻结 write set；非范围：其他任务和 Git 历史；变化：执行专项 phase 或 Quick Validate；完成标准：退出码 0、valid=true、无活跃旧消费者；术语说明：scoped 表示只核验本任务 Owner 和引用边界；验证状态：已通过。

## 输入与命令

- 基线提交：`76ee419d59396d919fea04ed55ea373ddeb8cb26`。
- 入口：`python -B doc/5-tests/2026-07-22_231500/requirement-domain-streamlining/validate_requirement_domain_streamlining.py --repo-root F:\luode-skills --manifest doc/5-tests/2026-07-22_231500/requirement-domain-streamlining/mapping/requirement-domain-manifest.yaml --phase trigger`。
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
- N/A：本任务不连接外部服务，不产生图片或数据库数据。
