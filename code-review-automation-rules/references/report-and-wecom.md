# 报告落盘规则（仅本地）

## 报告文件

- 目录：`<project_path>`（被审核项目根目录）。
- 文件名：`code_review_result.md`（固定名，同名覆盖）。
- 编码：UTF-8。

## 内容结构

```md
# Code Review 结果

**时间**: <date>
**分支**: <current_branch>
**项目**: <project_path>
**Commits**: <commit_list>

---

<review_result>
```

## 输出建议

- 发现问题：`发现问题。结果已保存到 <project_path>/code_review_result.md`
- 未发现问题：`Review完成，未发现问题。结果已保存到 <project_path>/code_review_result.md`

## 明确不做

- 不上报企业微信。
- 不生成时间戳新文件。
