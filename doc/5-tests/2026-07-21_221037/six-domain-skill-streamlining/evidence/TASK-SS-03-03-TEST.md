# EVD-SS-03-03-TEST：测试资产旧 source 删除与 post-delete 验证

结论：PASS；范围：四个测试资产 Skill 的 pre-delete、物理删除、manifest/asset retired、字典刷新和 post-delete；非范围：planning/project-interface 两个保留 owner 的 source 删除；完成标准：旧目录不存在、owner route 完整、冻结回滚记录存在、post-delete 全部通过。

## 执行环境

- 仓库根目录：`F:\luode-skills`。
- 环境：local 文件系统、Python UTF-8、PowerShell 7。
- 外部连接：`N/A + 原因 + 证据`：本周期只处理本地 Skill 资产、索引、字典和文档，不连接业务数据库、缓存、消息队列、HTTP/RPC 或非 local 环境。

## 删除前测试

以下六个候选均曾逐候选执行 `run_domain_trigger_cases.ps1 -Phase pre-delete -OnlySource <source>`，退出码均为 `0`：`implementation-planning-rules`、`project-interface-release-execution-rules`、`test-doc-rules`、`test-naming-rules`、`test-scattered-asset-location-rules`、`test-task-root-layout-rules`。四个待删除 source 在删除前均通过。

## 物理删除与删除后测试

```powershell
python -B skill-dictionary/generate_dictionary.py
python -B doc/5-tests/2026-07-21_221037/six-domain-skill-streamlining/validate_cycle03_routes.py --repo-root F:\luode-skills --manifest doc/5-tests/2026-07-21_221037/six-domain-skill-streamlining/mapping/domain-streamlining-manifest.yaml --phase post-delete
python -B doc/5-tests/2026-07-21_221037/six-domain-skill-streamlining/validate_domain_streamlining.py --repo-root F:\luode-skills --manifest doc/5-tests/2026-07-21_221037/six-domain-skill-streamlining/mapping/domain-streamlining-manifest.yaml --phase baseline
```

结果：四个旧目录均不存在；字典返回 `implemented_total=81`、`planned_missing=0`、`seed_total=33`；route validator、baseline 均 `valid=true`、退出码 `0`；四个旧 asset record 标记 `retired: true`。

## 清理与回滚

- 清理：只清理本任务 Python 缓存，不写业务环境。
- 回滚：按各 candidate `rollback_locator` 恢复 source root、owner route、消费者、manifest、asset inventory 和字典。
- 停止：任何旧 token、断链、hash 漂移、route 缺失或 post-delete 失败时停止。
