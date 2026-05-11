# 测试截图清理规则

## 目标

允许测试过程截图用于排障，但禁止测试结束后遗留无主截图文件。

## 生命周期规则

1. 生成阶段（允许）
- 测试执行中可截图，用于中间诊断与汇报。

2. 收口阶段（必须清理）
- 当测试完成并进入最终收口时，默认删除临时截图。
- 不允许把临时截图长期留在仓库或测试目录中。

3. 例外保留（需明确）
- 仅当用户明确要求保留时，才允许保留截图。
- 保留时必须记录“保留原因 + 保存位置 + 关联任务”。

## 清理时机

- 单次测试结束后立即清理。
- 批量测试任务在总收口前统一清理一次。
- session 关闭前再次检查截图目录是否已清空（或仅剩用户要求保留的文件）。

## 命名与目录建议

- 临时截图使用任务前缀，例如 `ab-test-<step>.png`。
- 临时截图放到可统一删除的目录，例如 `./screenshots/tmp/` 或 `/tmp/`。
- 需要保留的截图单独放到 `./screenshots/archive/`（或团队约定目录）。

## PowerShell 清理示例

```powershell
# 删除临时目录中的全部截图
Remove-Item -LiteralPath .\screenshots\tmp\* -Force -ErrorAction SilentlyContinue

# 删除 /tmp 下当前任务前缀截图
Remove-Item -LiteralPath /tmp/ab-test-*.png -Force -ErrorAction SilentlyContinue
```

## 通过标准

- 通过：测试结束后，临时截图已清理；若有保留截图，已说明保留原因与路径。
- 驳回：测试已结束但仍残留未说明用途的临时截图文件。
