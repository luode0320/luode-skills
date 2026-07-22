# EVD-SS-02-02-TEST：需求域活跃消费者迁移测试

结论：PASS；影响：需求域 live consumer 已从已退役入口迁移到 `requirement-intake-rules` 的 `initial-discovery` 路由；范围：active-consumers 索引、live 规则文件、模板注册、项目记忆、项目风格、README、编码规则、Bug 对称路由和团队路由；非范围：`.tmp` 历史盘点、PROJECT_MEMORY 变更记录、历史归档、旧目录删除；变化：旧入口不再作为 live consumer 的触发引用；完成标准：9 个 live consumer 均存在、无旧入口文字、canonical route 可定位，负向残留样本按预期失败；验证状态：PASS。

## 执行环境

- 仓库根目录：`F:\luode-skills`
- 环境：local 文件系统、Python UTF-8、PowerShell 7。
- 外部连接：`N/A + 原因 + 证据`：只读检查本地规则与文档，不连接业务服务。

## 正向真实测试

```powershell
python -B "doc/5-tests/2026-07-21_221037/six-domain-skill-streamlining/validate_requirement_consumers.py" --repo-root "F:\luode-skills" --index "F:\luode-skills/doc/5-tests/2026-07-21_221037/six-domain-skill-streamlining/inventory/active-consumers.json"
```

实际结果：

```json
{"task":"TASK-SS-02-02","valid":true,"consumer_count":9,"errors":[]}
```

- 正向退出码：`0`。
- 断言：索引中的 9 个 live consumer 全部存在；不包含旧入口字面量；除 PROJECT_MEMORY/PROJECT_STYLE 的历史/来源型例外外，均包含 `initial-discovery` canonical route；索引集合与冻结 write set 一致。

## 预期负向测试

```powershell
python -B "doc/5-tests/2026-07-21_221037/six-domain-skill-streamlining/validate_requirement_consumers.py" --repo-root "F:\luode-skills" --index "F:\luode-skills/doc/5-tests/2026-07-21_221037/six-domain-skill-streamlining/inventory/.tmp-consumers-negative.json"
```

样本先在 local 测试根目录临时加入 `requirement-discovery-rules/SKILL.md`，结果退出码：`1`；断言命中“活跃 consumer 残留旧入口”和 write set 不一致；随后已删除临时样本。

## 历史保护断言

- `PROJECT_MEMORY.md` 的 `## 变更记录` 及其之前历史事件未重写；测试只校验稳定规则区，避免把历史事实伪装成当前路由。
- 未修改 `doc/` 历史归档、`.tmp/skill-governance/` 盘点快照或 Git 历史。

## 清理与回滚

- 清理：删除 `.tmp-consumers-negative.json`；不写 local 业务数据。
- 回滚：恢复 9 个 live consumer、`active-consumers.json` 和项目记忆/风格/README 改动；不删除 source，不触碰 `.codex/config.toml`。