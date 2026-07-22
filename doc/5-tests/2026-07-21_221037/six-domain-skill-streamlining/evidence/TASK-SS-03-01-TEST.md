# EVD-SS-03-01-TEST：实施与测试域 owner 路由拆分

结论：PASS；影响：`implementation-planning-rules` 与 `project-interface-release-execution-rules` 的大段执行契约已拆入 owner references，自动触发仍由原 owner description 和 route marker 承接；范围：两个 owner 的 route、reference、agent prompt、资产 hash、正负触发；非范围：四个测试旧 source 的物理删除和全局其他 Bug 候选；变化：入口文件从执行细则全文改为主入口加条件路由，规则正文没有删除；完成标准：owner、route、reference、trigger alias、rollback 和 baseline 均通过；验证状态：PASS。

## 执行环境

- 仓库根目录：`F:\luode-skills`。
- 环境：local 文件系统、Python UTF-8、PowerShell 7。
- 外部连接：`N/A + 原因 + 证据`：本周期只处理本地 Skill 资产、索引、字典和文档，不连接业务数据库、缓存、消息队列、HTTP/RPC 或非 local 环境。

## 真实测试

```powershell
$env:PYTHONUTF8='1'
python -B doc/5-tests/2026-07-21_221037/six-domain-skill-streamlining/validate_domain_streamlining.py --repo-root F:\luode-skills --manifest doc/5-tests/2026-07-21_221037/six-domain-skill-streamlining/mapping/domain-streamlining-manifest.yaml --phase baseline
python -B doc/5-tests/2026-07-21_221037/six-domain-skill-streamlining/validate_cycle03_routes.py --repo-root F:\luode-skills --manifest doc/5-tests/2026-07-21_221037/six-domain-skill-streamlining/mapping/domain-streamlining-manifest.yaml --phase post-delete
```

结果：两条命令退出码均为 `0`；baseline `valid=true`、`errors=[]`；route validator `candidate_count=6`、`positive_negative_cases_checked=6`、`valid=true`。

## 结构断言

- planning 入口 `12,735` 字节，详细契约落在 `references/plan-mode-and-cycle-contracts.md`。
- project interface 入口 `5,232` 字节，详细契约落在 `references/shared-evidence-and-specialized-contracts.md`。
- owner 文件仍保留原 description、local 红线、授权/停止边界和 agent prompt。
- 失败预期：缺 route marker、缺 trigger alias、缺 target owner、资产 hash 漂移或 rollback 字段时非零退出。

## 清理与回滚

- 清理：使用 `python -B`，不写业务数据。
- 回滚：按 `cycle03-route-migration-map.yaml` 和 manifest 的 baseline commit 恢复 owner SKILL、references、agents、consumer index 和字典生成物。
- 停止：任一保护语义无法在 owner 或 route reference 定位时停止，不进入后续删除。
