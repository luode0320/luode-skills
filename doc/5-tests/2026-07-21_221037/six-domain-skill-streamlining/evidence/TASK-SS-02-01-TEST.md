# EVD-SS-02-01-TEST：需求域 initial-discovery 路由迁移测试

结论：PASS；影响：原独立 discovery 入口的自动触发契约、主动侦察规则和资源已由 `requirement-intake-rules` 的 `initial-discovery` 条件路由承接；范围：主入口、route references、manifest、触发 fixtures 和目标 owner 定向验证；非范围：活跃消费者全面迁移、旧目录删除、gap 路由和最终字典收口；变化：新增一个唯一主入口下的 discovery 条件路由；完成标准：目标 owner、route marker、保护语义、迁移 references 和正/负 fixtures 均通过；术语说明：条件路由是主 Skill 内按触发条件进入的职责分支，不是竞争入口；验证状态：PASS。

## 执行环境

- 仓库根目录：`F:\luode-skills`
- 环境：local 文件系统、Python UTF-8、PowerShell 7。
- 外部连接：`N/A + 原因 + 证据`：本任务只读取和校验本地规则资产，不连接数据库、缓存、消息队列、HTTP/RPC 或外部业务服务。

## 正向真实测试

```powershell
python -B "doc/5-tests/2026-07-21_221037/six-domain-skill-streamlining/validate_requirement_route_migration.py" --repo-root "F:\luode-skills" --fixtures "F:\luode-skills\doc/5-tests/2026-07-21_221037/six-domain-skill-streamlining/fixtures/trigger-cases.yaml"
python -B "doc/5-tests/2026-07-21_221037/six-domain-skill-streamlining/validate_domain_streamlining.py" --repo-root "F:\luode-skills" --manifest "F:\luode-skills\doc/5-tests/2026-07-21_221037/six-domain-skill-streamlining/mapping/domain-streamlining-manifest.yaml" --phase baseline
python -B "doc/5-tests/2026-07-21_221037/six-domain-skill-streamlining/validate_domain_streamlining.py" --repo-root "F:\luode-skills" --manifest "F:\luode-skills\doc/5-tests/2026-07-21_221037/six-domain-skill-streamlining/mapping/domain-streamlining-manifest.yaml" --phase trigger
```

实际结果：

```json
{"task":"TASK-SS-02-01","valid":true,"errors":[]}
{"schema_version":1,"phase":"baseline","valid":true,"errors":[],"error_count":0}
{"schema_version":1,"phase":"trigger","valid":true,"errors":[],"error_count":0}
```

- 目标 owner 定向测试退出码：`0`。
- manifest baseline 退出码：`0`。
- manifest trigger 退出码：`0`。
- 正例断言：`requirement-intake-rules` 与 `initial-discovery` 均存在，主入口包含 route marker 和 discovery 保护语义。
- 负例断言：负例不携带目标 route token，不被测试脚本误当作正例承接。
- 删除前保护断言：旧 source `requirement-discovery-rules/SKILL.md` 仍存在，作为冻结基线，未发生提前删除。

## 预期阻断验证

完整 manifest 的 `pre-delete` 阶段当前按预期未放行，因为其他未迁移候选尚未承接 route marker；该结果属于周期级前置条件未满足，不是本任务的失败证据。当前任务使用定向 owner 测试和 `trigger` 阶段完成自身闭环，完整 `pre-delete` 留给 `TASK-SS-02-03`。

## 清理与回滚

- 清理：本次测试使用 `python -B`，不生成 Python 字节码；不写 local 业务数据。
- 回滚：删除本任务新增的 `initial-discovery-*` references、定向验证脚本和 owner route 变更，恢复 `domain-asset-inventory.json`、manifest 与字典生成物到本任务前状态；不删除冻结 source，不触碰 `.codex/config.toml`。