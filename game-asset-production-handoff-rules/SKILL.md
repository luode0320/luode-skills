---
name: game-asset-production-handoff-rules
description: 2D 游戏素材的生产交接。当设计预览已经过用户确认，需要真实调用图像生成能力产出原始素材、生产角色/怪物/Boss 动作与 Sprite Sheet、生产地图/瓦片/场景道具/prop pack、执行去背切帧对齐等确定性后处理、或整理 Godot 可导入交付物时自动使用。设计尚未确认前不要使用本 skill；参考筛选、质量阶梯判定、项目视觉基线锁定、素材 brief 与预览确认请先转交 `game-asset-design-gate-rules`。生产角色/怪物/Boss 动作、direction set 或 sprite sheet 时，默认联动共享根目录 `character-sprite-animation-production`。
---

# 2D 游戏素材生产交接

## 作用

这个 skill 只负责设计已确认之后的 2D 游戏素材生产链路。
它覆盖两段完整链路：

1. 生成：按角色、怪物、地图、道具、UI、特效等资产类型，真实调用图像生成能力产出新的原创 2D 素材。
2. 后处理：把原始素材整理成可继续接入 Godot 的透明 PNG、切帧序列、Sprite Sheet、GIF 预览和元数据。

它的默认质量目标不是"先交付一个能用的占位图"，而是"按商业游戏成品标准生产可直接进入正式美术链路的原创 2D 资产"。

进入本 skill 前，默认已经通过 `game-asset-design-gate-rules` 完成参考筛选、质量阶梯判定、项目视觉基线锁定、素材 brief 撰写和用户预览确认。若生产对象包含角色、怪物或 Boss 动作，本 skill 再自动联动共享根目录 `character-sprite-animation-production` 负责动作生产与 QA。

## 自动触发范围

出现以下任一意图时，自动使用本 skill：

- 设计预览已经用户确认，需要真实生成最终生产素材。
- 需要生产角色、怪物、Boss、投射物、命中特效、地图、瓦片、场景道具、prop pack 的最终原始图。
- 需要对已生成的原始素材执行去背、切帧、对齐、拼表、导出 GIF 预览或 QA 元数据等后处理。
- 需要把 2D 素材整理为 Godot 可导入的透明图、分帧图、Sprite Sheet、可预览动画、分层地图或合成预览图。

以下情况不要用本 skill：

- 设计方向尚未经用户确认（应先使用 `game-asset-design-gate-rules`）。
- 3D 模型、3D 场景、骨骼动画、音效、配乐、文案、纯代码逻辑。

## 核心原则

### 1. 面向 Godot 交付

默认考虑：

- 透明背景
- 合理的画布尺寸
- 明确的角色脚底或中心锚点
- Sprite Sheet 行列组织
- 可切分的动画帧
- 可拆层的地图/道具资源
- Godot 导入后的继续编辑空间

### 2. 真实生成优先于程序绘制拼接

程序绘制、Pillow、SVG 几何拼接可以用于布局草图、碰撞草图、分层验证、风格探索和临时 blockout，但对 `Tier 2` / `Tier 3` 正式素材，默认不得只靠简单几何脚本直接交付最终资产；对所有生图相关正式交付，也不得把程序绘制、Pillow、SVG、脚本拼接、自动布局结果、后处理合成图当作原始生图结果，这些方式只能作为草图、验证图或后处理辅助图。如果只能使用程序绘制，也必须模拟手绘质量：非均匀轮廓、非对称结构、局部断线、压重线、复杂负形、材质遮挡、局部焦点和二次细节；做不到则必须声明为草稿。

## 生产执行流程

### 第 4 步：生成原始素材

先区分"设计预览图"和"最终生产素材"：

- 设计预览图：用于给用户确认方向（由 `game-asset-design-gate-rules` 负责）
- 最终生产素材：用于后处理、导出和 Godot 接入（本 skill 负责）

默认必须先经过设计预览图确认，再进入最终生产。

优先使用当前可用的图像生成能力产出新的原创素材。
只要任务语义属于生图、改图、参考图出新图、原始素材图、动作关键帧或 sprite 方向图，就必须自动联动 `imagegen` 产出原始图，不得等待用户额外明确说"使用 imagegen"。
如果环境里没有图像生成能力，不要假装已经生成完成，而是输出：

- 可执行的生成 brief
- 建议的构图 / 帧数 / 行列结构
- 后处理参数
- 接入 Godot 所需交付格式

手写生成提示词时，读取 [references/prompt-rules.md](../game-asset-design-gate-rules/references/prompt-rules.md)（`game-asset-design-gate-rules` 维护）。
提示词由 agent 主动编写，不要依赖脚本自动拼 prompt。

如果是大型场景物件或高价值场景物件，生成方案必须显式满足以下质量门槛：

- 明确轮廓，缩小后仍能一眼认出是什么物件
- 有成立的体积关系，而不是平面符号拼贴
- 有主要结构层：例如树冠、枝干、树根、屋顶、墙体、支撑、包边、挂件
- 有接地阴影或落地压重关系
- 有材质分层，而不是整块纯色
- 如风格允许，可有少量发光点缀，但不能喧宾夺主
- 单体物件即使脱离地图，也应像一个完整资产，而不是地图噪点

完成初稿后，必须做质量阶梯自审和风格一致性自审（判定标准见 `game-asset-design-gate-rules`）。未达到目标质量阶梯或风格不一致时，默认回炉一次，不要直接交付。

### 第 5 步：执行后处理

当已经拿到原始图之后，使用本 skill 的脚本做确定性整理，而不是手工反复操作。

读取 [references/postprocess-workflow.md](references/postprocess-workflow.md)。

默认使用：

- [scripts/postprocess_sprite_sheet.py](scripts/postprocess_sprite_sheet.py)
- [scripts/make_layout_guide.py](scripts/make_layout_guide.py)
- [scripts/compose_layered_preview.py](scripts/compose_layered_preview.py)

它负责：

- 洋红背景去除
- 分格切帧
- 主体组件筛选
- 帧内容裁切
- 按中心或脚底对齐
- 导出透明帧
- 重新拼成对齐后的透明 Sprite Sheet
- 导出 GIF 预览
- 导出 QA 元数据 JSON
- 把 prop pack 按网格切成单独 PNG

`make_layout_guide.py` 用于：

- 生成只提供行列和安全边距的布局参考图
- 控制 prop pack、固定格数 sheet、tileset-like atlas 的几何布局
- 只提供布局信息，不提供创意方向

`compose_layered_preview.py` 用于：

- 把底图与独立 prop 做成 QA 合成预览图
- 在不污染运行时结构的前提下，快速验证 props 位置、遮挡、层次和整体观感
- 辅助分层地图工作流，而不是替代真正的运行时分层结构

### 第 6 步：交付 Godot 可用结果

交付时至少说明：

- 原始素材是什么
- 后处理输出目录是什么
- 透明帧数量
- 最终 sheet 的尺寸和行列
- 是否已导出 GIF 预览
- 是否存在需要回炉的 QA 风险

## 资产类型约束

### 角色、怪物、Boss

- 优先保证轮廓分组稳定。
- 动画帧之间角色体量不要漂移太大。
- 需要固定脚底锚点时，优先用 `bottom` 对齐。
- 不要把大范围脱离本体的攻击弧光、爆炸、远距离子弹直接塞进角色本体 sheet，优先拆成独立 FX。
- 如果进入 idle / walk / run / attack / cast / hit / death / 4向 / 8向 / sprite sheet 生产，默认联动共享根目录 `character-sprite-animation-production`，并读取 [references/character-animation-production-gate.md](references/character-animation-production-gate.md)。

### 投射物、命中特效、法术效果

- 优先保证单帧清晰与循环节奏。
- 通常使用 `center` 对齐。
- 允许比角色更高对比，但不要脱离项目主色系太远。

### 地图、瓦片、场景道具

- 先区分"背景底图""可交互道具""碰撞对象""纯装饰对象"。
- 可编辑地图优先拆层，不要把所有内容烘焙成一张不可拆背景。
- 默认先问：这个物件是不是玩家会一眼看到、会评价质感、会把它当成正式场景资产的一部分。如果答案是"会"，直接按 `Hero Prop` 处理。
- 方形 prop pack 只适合明确的小型配角道具；默认不是地图场景物件的首选交付形态。
- 除非用户特别要求，否则大树、建筑、掩体、门、桥、平台、长墙、祭坛、路障、残骸、雕像、地形块、关键交互物件一律禁止按小装饰 `Prop Pack` 路线生产。
- 这类资产默认必须按独立 `Hero Prop` 设计：有体积、材质、结构、接地感，单体成立，可单独验收。
- "更扁平、更少颜色"只允许降低配色复杂度，不允许削弱资产成立所需的结构信息。
- 如果目标是地图或关卡，先判断是 `tile_mode`、`scene_mode`、`side_scroll_mode`、`grid_mode`、`room_chunk_mode` 还是 `baked_scene_mode`。
- 只要目标是可玩地图，就不要只交付一张平面背景图。

场景物件的正式质量标准默认至少包括：

- 明确轮廓
- 有树冠体积或主体体块
- 有枝干结构、梁柱结构或支撑关系
- 有接地阴影
- 有材质分层
- 可有发光点缀
- 单体物件本身成立
- 有好看的外轮廓和负形，而不是规则几何轮廓
- 有手绘线稿节奏：粗细变化、关键压重、适当断线和局部轮廓强调
- 有姿态或生长势：树枝、残骸、建筑结构不能完全对称、均匀或僵硬
- 有 1-3 个局部焦点细节，例如发光晶体、挂件、破损边、苔藓、符文、绑带或机械核心
- 有地图融合度：颜色、明度、阴影方向和画面噪点不能像贴纸

如果结果只是轻装饰符号、噪点、草簇暗示、几何图形拼接、没有主体结构的平面涂抹，默认判定为失败结果，必须回炉。

地图相关约束分别读取：

- [references/map-strategies.md](references/map-strategies.md)
- [references/layered-map-contract.md](references/layered-map-contract.md)
- [references/prop-pack-contract.md](references/prop-pack-contract.md)

## 默认交付规范

- 图片格式：PNG
- 需要透明时：RGBA 透明背景
- 动画预览：GIF
- 帧数据：独立 PNG 帧目录
- 质检信息：JSON

如果用户没指定，角色/怪物的短动作默认优先做 4 帧或 6 帧，小而稳；不要一上来做超长复杂动画。

## 额外强约束

- 角色、怪物、Boss、本体动作默认不要用原始单行 `1xN` sheet，优先使用 `2x2`、`2x3`、`3x3`、`4x4` 这类更稳的多行网格。
- 主角或高价值单位的本体动作默认与大范围 FX 分离；刀光、枪焰、长拖尾、投射物、爆炸冲击默认独立生成。
- 如果本体动作为了塞进固定格子导致体量明显缩小，视为失败结果，应该拆 FX 或重做。
- 除非用户特别要求，否则默认禁止把正式场景生产任务降级为"轻装饰、小装饰符号、噪点包"。
- prop pack 只适合一组同风格、同尺度、静态、紧凑的小道具；宽长结构、大体量对象、精确碰撞对象、关键视觉对象默认单独生成或改走 strip / tile / scene object / hero prop 路线。
- 树木、建筑、掩体、门、桥、祭坛、雕像、残骸、建筑边缘件、大型植被默认按独立 hero prop 设计，不能因为"地图更扁平"就退化成几笔符号。
- 正式场景物件默认必须满足"商业级场景物件质量"，而不是"先有个能摆进去的交付"。
- 对所有原始生成图，默认要求纯色背景、固定格数、无文字、无 UI、无标签、无格线、无边框。

## 生产输出模式

每次执行本 skill，优先按这个结构组织结果：

1. 生成方案
2. 后处理方案
3. Godot 交付物

## 资源

- 图像设计工作流（真实调用规范）： [references/image-generation-workflow.md](references/image-generation-workflow.md)
- 资产模式判定： [references/asset-modes.md](references/asset-modes.md)
- 角色动画生产闸门： [references/character-animation-production-gate.md](references/character-animation-production-gate.md)
- 地图模式选择： [references/map-strategies.md](references/map-strategies.md)
- 分层地图合同： [references/layered-map-contract.md](references/layered-map-contract.md)
- prop pack 合同： [references/prop-pack-contract.md](references/prop-pack-contract.md)
- 后处理流程说明： [references/postprocess-workflow.md](references/postprocess-workflow.md)
- 后处理脚本： [scripts/postprocess_sprite_sheet.py](scripts/postprocess_sprite_sheet.py)
- 布局参考图脚本： [scripts/make_layout_guide.py](scripts/make_layout_guide.py)
- 分层预览合成脚本： [scripts/compose_layered_preview.py](scripts/compose_layered_preview.py)
