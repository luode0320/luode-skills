# 来源记录（source-notes）

> 本文件登记 `frontend-design` 历次外部吸收的来源与落点。

## 2026-09-06 · Apple 流体交互设计（apple-design）集成

- **外部来源**：WorkBuddy 市场 skill `apple-design`（个人开发者，v1.0.0），本地安装源 `~/.workbuddy/skills/apple-design/`。
- **描述**：Apple 流体界面设计指南，基于 WWDC 流体交互设计，涵盖弹簧动画、手势驱动、毛玻璃、无障碍适配等。
- **吸收通道**：外部吸收。
- **裁决摘要**：合并 9 条精华（流体交互思想/弹簧参数表/速度移交/动量投射/毛玻璃配方/光学排版/无障碍降级/八大原则/交互校验清单），拒绝 3 条（代码生成脚本/工具声明/被动触发模式）。
- **同域扫描**：范围 = frontend-design（吸收目标）、frontend-ui-visual-rules（同域规则层）、frontend-component-rules（同域组件层）。发现 0 处重复段落（弹簧参数/毛玻璃配方/交互校验均为本地缺失能力，同域无命中）。0 处门控层叠。0 处散落产物。**PASS**。
- **落点**：新增 `references/apple-fluid-design.md`；修改 `SKILL.md`（版本 1.2.0 → 1.3.0，动效节追加弹簧物理、背景节追加毛玻璃、边界条件追加无障碍降级、第 4 步自查追加交互校验、职责边界引用）。
- **来源可回指**：本地安装源已删除；市场元数据见 `_skillhub_meta.json`（slug: `apple-design`, version: 1.0.0）。

## 2026-09-06 · Design（skillhub）设计偏好学习机制集成

- **外部来源**：skillhub `design` v1.0.0（ownerId `kn73vp5rarc3b14rc7wjcw8f8580t5d1`），本地安装源 `~/.workbuddy/skills/design__skillhub/`。
- **描述**：Auto-learns your visual preferences. Adapts to UI, graphics, video, and any creative work.
- **吸收通道**：外部吸收。
- **裁决摘要**：合并 7 条精华（偏好学习机制/四分类体系/判定标准/检测维度/反馈模式/媒介区分/主观性处理），拒绝 1 条（偏好模板形态 → 形态不迁移）。保留本地 1 条（维护规则）。
- **同域收敛**：发现 `frontend-ui-visual-rules/references/visual-preference-learning.md` 已于 2026-08-22 从同一源吸收，存在同域交叉冗余。收敛为「单一权威（visual-preference-learning.md）+ 引用（frontend-design 引用指针）」：删除新建的 `design-preference-learning.md`，增强权威文件补充工作流集成内容，frontend-design SKILL.md 引用权威。
- **落点**：`frontend-design/SKILL.md`（第 1 步工作流增加偏好查询环节 + 职责边界引用）。
- **来源可回指**：本地安装源已删除；skillhub 元数据见 `~/.workbuddy/skills/design__skillhub/_skillhub_meta.json`（已删除，元数据归档至本次吸收记录）。