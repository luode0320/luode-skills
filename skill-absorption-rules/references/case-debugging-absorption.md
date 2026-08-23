# Case Study：调试（debugging-skillhub）吸收

> 归属 owner：`skill-absorption-rules`。记录 2026-08-22 对 awesome-ai-agent-skills「调试」skill 的完整吸收过程与验证证据。

## 背景

- 上轮（同日晚间）刚完成 `diagnose`（mattpocock/skills）吸收：反馈回路 / 假设排序 / 唯一前缀标签 / 正确接缝 / 复盘五块方法论已落盘 Bug 域五件套。
- 本轮的「调试」skill 与 diagnose 高度同域，吸收策略调整为「**补缺优先**」：先对照已吸收精华，重叠部分一律判保留本地，只补本地真实缺失的领域知识。

## 裁决摘要

- 拆解 20 条原子规则：**合并 10 / 保留本地 9 / 拒绝 1**。
- 保留本地 9 条集中在「工作流骨架」（复现/修复/验证）与 diagnose 已覆盖的方法论（一次一变量/战略日志/先复现/回归测试），理由均为本地更强或全覆盖。
- 合并 10 条集中在「领域知识」：根因类别清单、堆栈阅读纪律、二分隔离战术、先查最近变更、Heisenbug、环境匹配复现、三类边界场景、跨语言工具表。
- 拒绝 1 条：教学示例代码（精华已提取为根因类别条目）。

## 落盘清单

| 文件 | 动作 | 体积 |
|------|------|------|
| `bug-root-cause-rules/references/root-cause-catalog.md` | 新建 | +2549 B |
| `bug-root-cause-rules/references/static-analysis-path.md` | 补 3 节 | +992 B |
| `bug-intake-rules/references/.../runtime-observation-methods.md` | 补 2 节 | +985 B |
| `bug-reproduction-rules/references/stability-checks.md` | 补 1 节 | +479 B |
| `bug-root-cause-rules/SKILL.md` | 同步引用 2 处 | — |
| `bug-reproduction-rules/SKILL.md` | 同步引用 2 处 + 编号整理 | — |

净增 **+5005 bytes**，全部引用式接入。

## 验证证据

- **结构校验**：bug-root-cause / bug-reproduction / bug-intake 三个 skill `quick_validate.py` 全部 PASS。
- **UTF-8**：4 个落盘文件全部通过。
- **同域扫描**：范围 = Bug 域 5 + 测试域 3（8 skill）；发现 0 处重复段落、0 处门控层叠、0 处散落产物；清理 1 处格式（bug-reproduction SKILL.md 编号重复）；**PASS**。
- **互补性确认**：
  - root-cause-catalog（候选池）→ hypothesis-ranking（排序纪律）→ root-cause-evidence（证据复核）三级互补，引用链单向可达。
  - stability-checks 环境匹配（复现判定阶段）vs feedback-loop 索要环境（回路构建失败阶段），阶段不同。
  - static-analysis-path 禁用一半系统（静态排除战术）vs feedback-loop 二分 harness（自动化回路工具），语义不同。

## 与 diagnose 吸收的关系

两次吸收形成完整闭环：

| 来源 | 贡献 | 落点 |
|------|------|------|
| diagnose | 方法论骨架（回路/假设/接缝/复盘） | feedback-loop / hypothesis-ranking / correct-seam / post-mortem / 日志标签 |
| 调试 | 领域知识（根因类别/定位战术/边界场景/工具表） | root-cause-catalog / static-analysis-path / observation-methods / stability-checks |

重叠部分零重复吸收（一次一变量、战略日志、先复现、回归测试均判保留本地，指向已吸收 reference 或本地更强规则）。

## 源清理

`debugging-skillhub__skillhub` 为 git 未跟踪安装源，删除后 junction 双路径自动失效（与 diagnose 同模式）。
