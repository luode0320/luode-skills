# EVD-SS-03-02-TEST：活跃消费者迁移与旧入口负向验证

结论：PASS；影响：当前 Skill、项目规则、README、接口测试集成和主规划中的测试资产引用已统一指向 `test-strategy-rules` 的 `test-asset-governance` 路由；范围：active-consumers、当前规则文件、正负触发、历史排除；非范围：历史审查/验证归档；完成标准：索引路径存在，活跃文件无四个旧入口 token，正例 route alias 可定位，负例不携带 required token。

## 执行环境

- 仓库根目录：`F:\luode-skills`。
- 环境：local 文件系统、Python UTF-8、PowerShell 7。
- 外部连接：`N/A + 原因 + 证据`：本周期只处理本地 Skill 资产、索引、字典和文档，不连接业务数据库、缓存、消息队列、HTTP/RPC 或非 local 环境。

## 真实测试

```powershell
@'
# 当前消费者索引路径存在，排除 doc/ 历史归档后不允许残留 retired token
'@ | python -
python -B doc/5-tests/2026-07-21_221037/six-domain-skill-streamlining/validate_domain_streamlining.py --repo-root F:\luode-skills --manifest doc/5-tests/2026-07-21_221037/six-domain-skill-streamlining/mapping/domain-streamlining-manifest.yaml --phase baseline
python -B doc/5-tests/2026-07-21_221037/six-domain-skill-streamlining/validate_cycle03_routes.py --repo-root F:\luode-skills --manifest doc/5-tests/2026-07-21_221037/six-domain-skill-streamlining/mapping/domain-streamlining-manifest.yaml --phase post-delete
```

结果：消费者扫描返回 `valid=true`、`consumer_index_missing=[]`、`retired_token_live_hits=[]`；baseline 和 route validator 均退出码 `0`。

## 失败预期与边界

- 将旧 token 写回当前 README、规则或 agent 文件时，消费者扫描必须非零退出。
- `doc/` 历史归档不作为当前 live consumer，不能通过改写历史记录伪造迁移。
- 缺少 canonical route 或负例携带 required token 时 route validator 必须非零退出。

## 清理与回滚

不写业务数据；回滚只恢复当前消费者文件和 `active-consumers.json`，不改历史归档。
