# Case Study：diagnose 吸收（2026-08-22）

> 本文记录 `mattpocock/skills` 的 `diagnose`（v1.0.0）吸收全过程，作为后续调试域吸收的对照样例。

## 来源与形态

- 来源：marketplace 安装源，homepage `https://github.com/mattpocock/skills`。
- 形态：外部吸收通道（本地安装源吸收模式：读原文 → 裁决 → 落盘 → 删源）。
- 外部 SKILL.md 125 行，六阶段闭环：反馈回路 → 复现 → 假设 → 插桩 → 修复+回归 → 清理+复盘。

## 核心价值判断

diagnose 的灵魂是 **Phase 1「反馈回路优先」**：调试第一优先是构建快速、确定性、agent 可运行的 pass/fail 信号，回路在手则二分/假设/插桩机械推进，回路缺失则看代码无效。本地 Bug 域五件套覆盖生命周期管理，但缺这块元方法论，以及假设排序纪律、正确接缝概念、修复后复盘。

## 裁决结果

- 合并 15 条（5 个落点：feedback-loop / hypothesis-ranking / debug-log 标签 / correct-seam / post-mortem）
- 保留本地 2 条（探针映射一次一变量、debugger 优先于日志——本地 runtime-observation-methods 已更强）
- 拒绝 0 条

## 落盘改动

| 文件 | 动作 | 内容 |
|---|---|---|
| `bug-reproduction-rules/references/feedback-loop.md` | 新建 | 反馈回路优先原则 + 10 种构建方式 + 迭代三问 + 非确定性复现率 + 无法构建回路处理 + 复现三确认 + 性能回归测量 |
| `bug-reproduction-rules/SKILL.md` | 修改 | 默认执行流程第 2 步 + references 读取规则 |
| `bug-root-cause-rules/references/hypothesis-ranking.md` | 新建 | 3-5 排序假设 + 可证伪预测格式 + 给用户看不阻塞 |
| `bug-root-cause-rules/SKILL.md` | 修改 | 默认执行流程第 3 步 + references 读取规则 |
| `bug-intake-rules/references/runtime-diagnostics-bug-debug-log-rules-debug-log-placement.md` | 修改 | 补「唯一前缀标签 [DEBUG-xxxx] + 一次 grep 清理」 |
| `test-regression-rules/references/correct-seam.md` | 新建 | 正确接缝定义 + 无接缝即发现 + 修复前失败测试流程 + 修复收尾清单 |
| `test-regression-rules/SKILL.md` | 修改 | 默认执行流程第 2 步 + references 读取规则 |
| `bug-validation-rules/references/post-mortem.md` | 新建 | 修复后复盘「什么能阻止这个 Bug」+ 架构建议修复后给 |
| `bug-validation-rules/SKILL.md` | 修改 | 默认执行流程第 7 步 + references 读取规则 |

## 净增体积与整理去重

- 净增：+9292 bytes（4 个新 reference + 1 处小补丁），全部引用式接入。
- 整理去重：N/A（本地五件套引用式结构无同义重复；本次为四块真实缺失的方法论增量，无存量冗余可清）。
- 同域扫描：范围 = Bug 域 5 + 测试域 3 skill；发现 0 冗余（feedback-loop 与 reproduction-template 方法层/格式层互补，post-mortem 与 validation-checklist 阶段前后互补）；清理 0；**PASS**。

## 棘轮验证

- `quick_validate.py` 5/5 skill PASS。
- 4 个新文件 UTF-8 无乱码（3919/1337/2345/1691 bytes）。
- 引用链可达：5 处 SKILL.md 引用 + post-mortem 跨 skill 引用 correct-seam 均可达。

## 关键教训

1. **跨 skill 分散吸收时，每次编辑都先确认文件未被外部修改**：Google Drive 同步目录下 Edit 工具会因文件被 linter/同步进程 touch 而报 "File has been modified since read"，重读后重试即可，非数据损坏。
2. **方法论类吸收的落点要按生命周期阶段归位**：反馈回路→复现域、假设→根因域、插桩→诊断域、接缝→回归域、复盘→验证域，而不是集中塞进一个 skill，保证后续按阶段触发精准。
3. **"保留本地"不等于"不吸收"**：探针一次一变量、debugger 优先两条本地已有更强版本，裁决保留并记录理由，避免为吸收而吸收。
