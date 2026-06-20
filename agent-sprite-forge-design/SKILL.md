---
name: agent-sprite-forge-design
description: 用于在正式生产 2D 游戏素材前完成美术设计收口。吸收 0x0funky/agent-sprite-forge 的 Codex-first 资产设计思路：先检索外部参考候选并让用户选定截图，再判断资产类型、镜头、构图、sheet/layout、分层地图策略和引擎交付方式，最后用图像生成产出设计图预览。适用于角色、怪物、Boss、地图、场景物件、投射物、FX、掉落物、图标等 2D 游戏资产的“先看参考候选、再做设计预览、确认后生产”流程。当用户需要先看方案图、先确认美术方向、先迭代设计稿再落地素材时必须使用。
---

# Agent Sprite Forge Design

## 作用

这个 skill 只负责 2D 游戏素材的设计阶段，不直接负责最终量产交付。

它吸收 `0x0funky/agent-sprite-forge` 的核心强项：

1. 先由 agent 检索外部参考候选，并把候选截图或链接交给用户筛选。
2. 先由 agent 判断资产类型、动作、布局、分层和引擎交付方式。
3. 先产出用于审美确认的设计图，而不是直接把第一版生成结果当最终资产。
4. 让图像生成负责 raw visual exploration，让后处理脚本只负责确定性整理。
5. 把 sprite、map、FX、layered map、engine handoff 当成一条完整 pipeline，而不是单张图任务。

补充强规则：

- 只要当前任务需要设计预览图、方向图、风格图、参考图出新图或任何原始位图探索结果，就必须自动联动 `imagegen`；不得要求用户额外明确说“使用 imagegen”。
- 设计阶段允许脚本做整理、对齐、版式参考和后处理辅助，但不得用脚本绘图、拼图或程序合成结果冒充 imagegen 已生成的设计图。

## 强制流程

任何正式 2D 游戏素材任务，默认必须按以下顺序执行：

1. 先检索外部参考候选，并向用户展示候选素材的截图、链接或风格清单。
2. 由用户从候选中选定要推进的参考截图，或追加新的参考截图。
3. 再锁定项目视觉基线。
4. 再写 image spec / 资产 brief。
5. 再生成“设计预览图 / 方向图 / 风格图”给用户看。
6. 等用户明确确认“方向可以 / 设计满意 / 开始做最终素材”后，才允许进入生产和后处理。
7. 如果用户继续提出修改意见，默认继续迭代设计图，不得抢跑去做最终素材。

没有用户确认，不得把设计图直接升级成最终资产。
没有用户选定参考方向前，也不得跳过候选筛选直接进入正式设计。

## 设计阶段最小交付

设计阶段至少要向用户展示以下内容中的一种或多种：

- 角色 / 怪物 / Boss 的单体设计图
- 场景物件 hero prop 设计图
- 地图底图方向图
- 分层地图 props 方向图
- projectile / impact / spell bundle 设计图
- 图标 / 掉落物方向图

默认不要只给文字 brief 就进入生产。
只要环境允许，就应优先给用户看图再确认。

如果用户还没有给参考截图，默认先由 agent 去检索候选并整理给用户，不要直接假定风格已经锁定。

## 设计判断

先判断属于哪类资产：

- `generate2dsprite` 型：角色、怪物、Boss、投射物、FX、图标、道具、掉落物、固定 frame sprite sheet
- `generate2dmap` 型：地图底图、分层地图、prop pack、透明 props、Godot 可编辑地图交付

设计时必须先确定：

- asset type
- gameplay use case
- camera / framing
- silhouette language
- color system
- material language
- lighting / contact shadow logic
- sheet / layout strategy
- map layering strategy
- engine handoff expectation

## 设计图确认闸门

当用户没有明确说“开始做最终素材”前：

- 设计图默认视为 `preview-only`
- 允许继续对话迭代
- 允许重写 brief、镜头、比例、材质、轮廓、配色
- 不允许把 preview 直接后处理成正式生产资产

只有用户明确确认后，才允许切到生产阶段。

当用户还没有明确选定候选参考截图前：

- 当前阶段默认视为 `reference-selection`
- 允许继续补候选网站、补截图、换参考方向
- 不允许把“我猜用户可能喜欢这个风格”直接当成已确认参考

## 质量红线

设计图阶段也要提前拦截以下失败信号：

- 图形拼接感强
- 像图标或贴纸
- 单体结构不成立
- 与项目已有风格不一致
- 像另一个素材包或另一个游戏
- 没有明确外轮廓和视觉重心
- 地图 props 像小装饰而不是 hero prop
- 参考方向其实还没被用户确认

这些情况出现时，默认继续回炉设计图，而不是进入生产。

## 和 2d-asset-design 的关系

- `agent-sprite-forge-design` 负责设计阶段和用户确认闭环。
- `2d-asset-design` 负责在确认后继续生产、后处理和 Godot 交付。
- `2d-asset-design` 命中正式素材任务时，应先命中本 skill。

## 参考来源

本 skill 吸收自 `0x0funky/agent-sprite-forge` 的公开 GitHub 工作流说明，包括：

- Codex-first asset planning
- sprite / FX / map 分流
- layered raster map pipeline
- Godot / Unity engine handoff 思路
- deterministic post-processing only after raw visual generation

参考仓库：

- https://github.com/0x0funky/agent-sprite-forge
