# 报告落盘规则（仅本地）

## 报告文件

- 目录：`<project_path>/doc/审查/`。
- 文件名：`YYYY-MM-DD_<审查中文主题>.md`（遵循 `artifact-storage-rules` 中央模板；同主题复用或覆盖）。
- 编码：UTF-8。

## 内容结构

```md
# 提交级代码审核结果

**时间**: <date>
**分支**: <current_branch>
**项目**: <project_path>
**Commits**: <commit_list>

---

<review_result>
```

## 输出建议

- 发现问题：`发现问题。结果已保存到 <project_path>/doc/审查/<report_file>`
- 未发现问题：`Review 完成，未发现阻断项。结果已保存到 <project_path>/doc/审查/<report_file>`

## 明确不做

- 不上报企业微信。
- 不再写入项目根目录固定文件名。
