# 吸收裁决表（workbuddy-absorption-map）

> 本文件登记 `frontend-ui-visual-rules` 历次外部吸收的裁决与落地记录，保证可回指、可审计。

## 2026-08-22 · Design v1.0.0（skillhub）→ 视觉偏好学习机制

- **来源**：skillhub `design` v1.0.0（ownerId `kn73vp5rarc3b14rc7wjcw8f8580t5d1`），本地安装路径 `~/.workbuddy/skills/design__skillhub/`（含 SKILL.md + criteria.md + dimensions.md + _icon.png + meta）。
- **来源形态**：纯 Markdown 偏好记忆模板（33 行 SKILL.md + 2 个 reference）。安全检查：P2（无脚本、无外联执行逻辑）。
- **核心机制**：视觉偏好自学习——从用户选择/反馈/反应中检测模式 → 2+ 一致偏好确认 → 四分类（总体审美/按介质/品牌项目/明确拒绝）紧凑沉淀 → 跨介质（UI/图形/视频/印刷）复用。

### 三态裁决

| 外部精华 | 本地现状 | 裁决 | 落点 | 整理去重 |
| --- | --- | --- | --- | --- |
| 偏好自动学习机制（检测模式 → 2+ 一致确认 → 紧凑记录） | 本地视觉类 skill（frontend-ui-visual-rules 规则型 / frontend-design 生成型 / web-design-guidelines 在线审查型）均无偏好记忆能力 | 合并 | references/visual-preference-learning.md | N/A（目标文件无同义段落；aesthetic-direction-rules.md 为"定方向方法论"，与"记忆偏好"互补） |
| 四分类记忆结构（Aesthetic/By Medium/Brands/Never） | 本地无偏好容器 | 合并（中文适配） | 同上 | 同上 |
| 何时添加判定（1 次明确表态立即记；2+ 模式确认；客户需求/一次性实验/品牌规范不记） | 本地无 | 合并 | 同上 | 同上 |
| 检测维度（风格/颜色/字体/布局/UI/图形/视频/反馈模式） | 本地无偏好维度清单 | 合并（压缩中文化） | 同上 | 同上 |
| 写入格式（超紧凑关键词、tends toward 倾向表述、记录例外、品味进化更新） | 本地无 | 合并 | 同上 | 同上 |
| 跨介质通用（UI/图形/视频/印刷） | 本地视觉 skill 只覆盖前端 | 合并（保留跨介质语义，沉淀位置落用户级文件） | 同上 | 同上 |
| 外部模板形态（33 行模板 + Empty sections 占位） | 本地为规则文档体系 | 拒绝（不复制外部形态） | — | — |
| 英文原文 | — | 拒绝（统一译中文） | — | — |

### 同域冗余扫描结论（2026-08-22）

- **扫描范围**：frontend-ui-visual-rules（主落点）、frontend-design、web-design-guidelines、imagegen、design__skillhub（源）、agent-sprite-forge-design、game-asset-design-gate-rules、character-sprite-animation-production。
- **发现 0 处**：frontend-design「记住」为页面记忆点理念、imagegen「tasteful」为英文形容词，均非偏好机制；无重复段落、无门控层叠、无散落产物（新 reference 被 SKILL.md 两处引用）。
- **结论：PASS**。

### 棘轮评分（2026-08-22）

- 评分方式：独立子代理（agent-88eed7fa）按 darwin 8 维评分；基线由主代理按同标准评估。
- 基线（吸收前，10 references 无偏好机制）：**69.3 分**。
- 吸收后：**87.5 分**（Frontmatter 8 / 工作流 9 / 边界 8 / 检查点 8 / 指令 9 / 资源 9 / 架构 9 / 实测 9）。
- 涨幅 **+18.2**，棘轮通过；3 场景实测（极简偏好沉淀 / 2+ 一致确认深色高对比 / 品牌规范不记）全部通过。
- 吸收后小修：流程步骤 2 条件与 references 读取规则对齐（"已有偏好或本轮收到反馈"）。

### 体积账（防臃肿证据）

- 目标净增：+3,488B（visual-preference-learning.md）+ SKILL.md 净 +2 行（+11/−9）≈ **+3.8KB**。
- 删源：−7,499B（design__skillhub 全目录）。
- **体系级净减 ≈ 3.7KB**。

### 源清理

- 2026-08-22 吸收确认后删除 `design__skillhub`（用户级 junction + 工作区副本，git 未跟踪 `??`，删除无残留）。
