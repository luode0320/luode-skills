# 第 1 轮：静态覆盖对照

## 测试目标

验证旧 `code-comment-rules` 的原规则、references 和相邻边界是否都能在新 skill 集合中找到明确落点，不出现遗漏或弱化。

## 执行方式

1. 对照 [2026-04-03_code-comment-rules拆分预案.md](C:/Users/Administrator/.codex/skills/ment/2026-04-03_code-comment-rules拆分预案.md) 第 7 节映射表逐条检查原规则落点。
2. 校验新 skill 目录结构与 `agents/openai.yaml`、`references/` 是否齐全。
3. 运行结构校验：
   - `python -X utf8 .system\skill-creator\scripts\quick_validate.py C:\Users\Administrator\.codex\skills\comment-placement-granularity-rules`
   - `python -X utf8 .system\skill-creator\scripts\quick_validate.py C:\Users\Administrator\.codex\skills\comment-completion-gate-rules`
   - `python -X utf8 .system\skill-creator\scripts\quick_validate.py C:\Users\Administrator\.codex\skills\chinese-comment-rules`
   - `python -X utf8 .system\skill-creator\scripts\quick_validate.py C:\Users\Administrator\.codex\skills\skill-hit-check-rules`
   - `python -X utf8 .system\skill-creator\scripts\quick_validate.py C:\Users\Administrator\.codex\skills\skill-compliance-gate-rules`

## 覆盖结论

- `R-CC-001` 至 `R-CC-004` 已由 `comment-placement-granularity-rules` 主承接。
- `R-CC-005` 至 `R-CC-011`、`R-CC-013` 已由 `comment-completion-gate-rules` 主承接。
- `R-CC-012` 由 `chinese-comment-rules` 主承接。
- `R-CC-014` 由 `comment-placement-granularity-rules`、`comment-completion-gate-rules`、`chinese-comment-rules` 组合承接。
- `R-CC-015` 已拆分为 placement / granularity / gate 侧 references 读取规则。

## 实际结果

- 新 skill 目录、`SKILL.md`、`agents/openai.yaml` 与 `references/` 均已落地。
- 上述 5 个相关 skill 结构校验全部通过，未发现 skill 目录结构损坏或前言字段缺失。
- 静态映射层面未发现旧规则无落点的情况。

## 结论

通过
