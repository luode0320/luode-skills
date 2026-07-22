# EVD-SS-01-TEST：基线验证证据

结论：`TASK-SS-01-01` 的 manifest、资产索引、消费者索引和路径边界验证通过；影响：后续周期获得可复核迁移前基线；范围：Python 验证器、PowerShell wrapper、正向 baseline 和两个预期负向样本；非范围：不证明任何 Skill 已迁移或删除；变化：冻结 36 个目标 Skill、11 个退役候选和 72 条触发样本；完成标准：正向命令退出码为 0，负向命令按预期返回非零；术语说明：baseline 是迁移前事实；验证状态：PASS。

## 执行环境

- 仓库根目录：`F:\luode-skills`
- 环境：local 文件系统、Python UTF-8、PowerShell 7
- 外部连接：N/A + 原因 + 证据：本任务只读取本地仓库文件，不连接业务服务。

## 正向命令与结果

```powershell
$env:PYTHONUTF8='1'
python -X utf8 -m py_compile "doc/5-tests/2026-07-21_221037/six-domain-skill-streamlining/validate_domain_streamlining.py"
python -X utf8 "doc/5-tests/2026-07-21_221037/six-domain-skill-streamlining/validate_domain_streamlining.py" --repo-root "F:\luode-skills" --manifest "doc/5-tests/2026-07-21_221037/six-domain-skill-streamlining/mapping/domain-streamlining-manifest.yaml" --phase baseline
pwsh -NoProfile -File "doc/5-tests/2026-07-21_221037/six-domain-skill-streamlining/run_domain_trigger_cases.ps1" -RepoRoot "F:\luode-skills" -CasesRoot "doc/5-tests/2026-07-21_221037/six-domain-skill-streamlining" -Phase baseline
```

实际结果：

```json
{"schema_version":1,"phase":"baseline","valid":true,"errors":[],"error_count":0}
```

- Python 编译：退出码 `0`。
- 直接验证器：退出码 `0`。
- PowerShell wrapper：退出码 `0`。
- 测试 README 文档 profile：`valid=true`、`status=PASS`、`errors=[]`。

## 预期负向命令与结果

```powershell
python -X utf8 "doc/5-tests/2026-07-21_221037/six-domain-skill-streamlining/validate_domain_streamlining.py" --repo-root "F:\luode-skills" --manifest "C:\Windows\win.ini" --phase baseline
```

结果：退出码 `1`，报告仓库越界和 manifest 不存在；未读取仓库外文件。

```powershell
python -X utf8 "doc/5-tests/2026-07-21_221037/six-domain-skill-streamlining/validate_domain_streamlining.py" --repo-root "F:\luode-skills" --manifest "doc/5-tests/2026-07-21_221037/six-domain-skill-streamlining/mapping/domain-streamlining-manifest.yaml" --phase invalid
```

结果：退出码 `2`，argparse 拒绝非法阶段。

## 清理与回滚

- 清理：删除 `__pycache__` 和临时 stdout 文件；保留 manifest、索引、fixture、脚本和本证据。
- 回滚：只删除本任务新增测试资产，不触碰任何 Skill 目录、字典或 `.codex/config.toml`。
