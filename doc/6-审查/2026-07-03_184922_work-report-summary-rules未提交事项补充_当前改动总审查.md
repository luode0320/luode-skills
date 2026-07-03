# work-report-summary-rules 未提交事项补充当前改动总审查

## 审查结论

- 审查结论: 通过
- 审查范围: `work-report-summary-rules/SKILL.md`、`work-report-summary-rules/agents/openai.yaml`、`work-report-summary-rules/references/projects.json`、`work-report-summary-rules/references/report-format.md`、`work-report-summary-rules/references/uncommitted-worktree.md`、`work-report-summary-rules/scripts/generate_git_report.py`、`README.md`、`skill-dictionary/data.js`、`字典.md`
- 是否允许提交: 是
- 阻断问题: 无

## 审查摘要

### 1. 规则口径一致性

- `work-report-summary-rules` 已从“只统计已提交 Git 记录”升级为“已提交事项 + 工作区未提交进行中事项”双来源模型。
- Skill 正文、`report-format.md`、`projects.json`、`openai.yaml` 已同步到同一口径：
  - 未提交事项必须来自真实 Git 工作区证据。
  - 未提交事项必须显式标注为 `进行中`。
  - 无提交但有未提交改动的项目仍应进入项目明细。

### 2. 脚本实现检查

- `generate_git_report.py` 已新增工作区扫描、低价值未提交改动过滤、路径数量限制和 `进行中:` 摘要生成逻辑。
- 额外修复了 Windows 下真实编码问题：
  - 配置文件按 `utf-8-sig` 读取，兼容 BOM。
  - `git log`、`git status`、`git config` 子进程显式改为 UTF-8 解码，并关闭 `core.quotepath` 转义，避免中文路径和中文提交被系统默认 `gbk` 解码打断。

### 3. 验证结果

1. `python -m py_compile work-report-summary-rules/scripts/generate_git_report.py` 通过。
2. 使用当前仓库构造临时 `projects.json` 跑周报样例通过，输出中已出现：
   - 常规已提交事项
   - `进行中: 工作区仍有未提交改动...`
3. 已刷新 `skill-dictionary/data.js` 与 `字典.md`，新 reference `uncommitted-worktree.md` 已纳入字典产物。

## 风险与边界

- 未提交事项当前仍是“工作区改动摘要”口径，不会强猜业务任务名；这是刻意保守设计，避免把 AI 推断写成事实。
- 当前工作区还存在用户其他未提交改动（如 `artifact-storage-rules`、`implementation-planning-rules`、`requirement-change-rules`），本审查未覆盖其业务正确性，仅确认本轮 `work-report-summary-rules` 改动未与其冲突。
