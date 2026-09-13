# 测试资产清理证据

## 基本信息

- **清理时间**: {datetime}
- **清理触发条件**: {收口清理 / Skill 退役清理 / 定期清理 / 存量清理}
- **清理范围**: {test/ 下具体路径}
- **清理方式**: {自动清理 / 用户确认后清理}
- **确认人**: {用户确认记录}

## 清理清单

| 路径 | 类别 | 文件数 | 大小 | 清理动作 | 结果 |
|------|------|--------|------|---------|------|
| {path} | {category} | {count} | {size} | {deleted/moved/skipped} | {ok/fail} |
| ... | ... | ... | ... | ... | ... |

## 统计

- **总计清理**: {N} 个目录/文件，{size} 空间释放
- **__pycache__ 清理**: {N} 个目录，{size} 自动清理
- **遗留资产清理**: {N} 个目录，{size} 用户确认后清理
- **临时数据清理**: {N} 个文件，{size} 用户确认后清理

## 排除项

- {path} — 理由：{reason}
- ...

## 异常记录

- {path} — 异常：{error description}
- ...

## 后续操作

- [ ] 检查清理后测试运行是否正常（`python -X utf8 -B -m unittest discover -s test -p "*_test.py" -v`）
- [ ] 如有遗留资产未清理，记录到 `PROJECT_HISTORY.md` 待办
- [ ] 引用检查结果：{有引用依赖 / 无引用依赖 / 引用状态未知}

---

*清理脚本: `test-strategy-rules/scripts/scan_stale_test_assets.py`*
*缓存清理: `test-strategy-rules/scripts/cleanup_pycache.py`*