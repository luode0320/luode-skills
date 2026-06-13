---
name: 2d-asset-design
description: 用于设计、生成和后处理原创 2D 游戏素材。当用户想要新建、重做、补齐、替换、迭代或统一 2D 游戏素材时自动使用；当角色、怪物、Boss、地图、瓦片、场景道具、UI、图标、特效、投射物、掉落物、Sprite Sheet、逐帧动画、Godot 可导入贴图或分层 2D 资源在需求实现过程中成为阻塞项时也自动使用。也用于把 Kenney、OpenGameArt、Quaternius、KayKit、Godot Demo 等免费素材站资源当作参考板进行风格提炼，再重新设计和生成原创素材，而不是直接复用下载素材作为最终游戏资产。
---

# 2D 素材设计

## 作用

这个 skill 只负责 2D 游戏素材。
它覆盖三段完整链路：

1. 设计：明确素材的玩法职责、视觉方向、风格边界与可读性目标。
2. 生成：按角色、怪物、地图、道具、UI、特效等资产类型产出新的原创 2D 素材方案。
3. 后处理：把原始素材整理成可继续接入 Godot 的透明 PNG、切帧序列、Sprite Sheet、GIF 预览和元数据。

## 自动触发范围

出现以下任一意图时，自动使用本 skill：

- 用户明确要求“做素材”“设计素材”“生成素材”“换美术”“补 2D 资源”“重做角色/怪物/UI/地图素材”。
- 当前任务推进到某一步，发现缺少角色、怪物、子弹、道具、图标、地图、瓦片、场景道具、特效、HUD 等 2D 素材。
- 需要把免费素材站资源当成参考，再重新设计项目自己的原创素材。
- 需要把 2D 素材整理为 Godot 可导入的透明图、分帧图、Sprite Sheet、可预览动画。
- 需要统一 2D 资产风格，避免不同来源素材混用导致画面割裂。

以下情况不要用本 skill：

- 3D 模型、3D 场景、骨骼动画、音效、配乐、文案、纯代码逻辑。
- 用户只是在问“这个素材授权是否可用”，但还没有进入素材设计或生产阶段。

## 核心原则

### 1. 免费素材只做参考，不直接入库

Kenney、OpenGameArt、Quaternius、KayKit、Godot Demo 等来源默认只允许做参考板、比例参考、层次参考、风格拆解与制作约束参考。
不要把下载素材直接作为最终游戏资产，也不要只做轻微换色、裁切、描边后冒充原创成品。

需要参考规则时，读取 [references/reference-only-policy.md](references/reference-only-policy.md)。

### 2. 先满足玩法可读性，再追求装饰细节

任何素材先回答这几个问题：

- 玩家需要在多远距离识别它。
- 它在战斗里承担什么玩法职责。
- 它要和哪些同类对象拉开差异。
- 它是否需要动画、方向、层级、碰撞边界或交互提示。

如果细节会破坏识别速度，优先删细节。

### 3. 只构建项目原创 2D 素材

目标不是“找到能用的现成包”，而是“借鉴参考后，为当前项目构建新的原创 2D 视觉资产”。

### 4. 面向 Godot 交付

默认考虑：

- 透明背景
- 合理的画布尺寸
- 明确的角色脚底或中心锚点
- Sprite Sheet 行列组织
- 可切分的动画帧
- 可拆层的地图/道具资源
- Godot 导入后的继续编辑空间

## 执行流程

### 第 1 步：识别资产任务

先把请求收敛成明确资产类别：

- 角色
- 怪物
- Boss
- 投射物
- 命中特效
- 掉落物 / 拾取物
- UI / HUD / 图标
- 地图背景
- 瓦片 / Tile
- 场景道具 / Prop Pack
- 动画 Sprite Sheet

如果用户一次要很多资产，优先拆成一个主资产族先做，不要在一个回合里把全部资产混成一锅。

当一句话可能对应多种素材生产方案时，读取 [references/asset-modes.md](references/asset-modes.md)。

### 第 2 步：先写素材 brief

在生成素材前，先输出简短素材 brief，至少包含：

- 资产类型
- 玩法用途
- 观看视角：俯视 / 侧视 / 3/4
- 风格方向
- 轮廓语言
- 配色方向
- 材质提示
- 动画需求
- 交付格式

示例：

```text
资产：近战精英怪
用途：让玩家一眼识别为高威胁近战压迫单位
视角：俯视
风格：非像素、清晰卡通、商业手游/独立动作游戏质感
轮廓：宽肩、短腿、前臂武器明显、重心低
配色：苔绿色主体，骨白色护甲，橙色危险点缀
动画：idle、run、wind-up、attack、hit、death
交付：透明背景 Sprite Sheet，供 Godot 4 导入
```

### 第 3 步：处理外部参考

当请求里提到某个外部素材包或截图时：

1. 提炼可复用信息：轮廓、色块、层次、材质、节奏、构图密度、镜头角度。
2. 丢弃直接复用风险高的部分：独特造型、完整构图、原包专属排列、可直接辨认的角色或道具设计。
3. 重新组合成当前项目自己的风格 brief。

不要输出“就直接用这个包”作为结论。

### 第 4 步：生成原始素材

优先使用当前可用的图像生成能力产出新的原创素材。
如果环境里没有图像生成能力，不要假装已经生成完成，而是输出：

- 可执行的生成 brief
- 建议的构图 / 帧数 / 行列结构
- 后处理参数
- 接入 Godot 所需交付格式

手写生成提示词时，读取 [references/prompt-rules.md](references/prompt-rules.md)。
提示词由 agent 主动编写，不要依赖脚本自动拼 prompt。

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

### 投射物、命中特效、法术效果

- 优先保证单帧清晰与循环节奏。
- 通常使用 `center` 对齐。
- 允许比角色更高对比，但不要脱离项目主色系太远。

### 地图、瓦片、场景道具

- 先区分“背景底图”“可交互道具”“碰撞对象”“纯装饰对象”。
- 可编辑地图优先拆层，不要把所有内容烘焙成一张不可拆背景。
- 方形 prop pack 只适合紧凑小物件；大树、门、桥、平台、长墙、地形块不要硬塞进均匀小格子。
- 如果目标是地图或关卡，先判断是 `tile_mode`、`scene_mode`、`side_scroll_mode`、`grid_mode`、`room_chunk_mode` 还是 `baked_scene_mode`。
- 只要目标是可玩地图，就不要只交付一张平面背景图。

地图相关约束分别读取：

- [references/map-strategies.md](references/map-strategies.md)
- [references/layered-map-contract.md](references/layered-map-contract.md)
- [references/prop-pack-contract.md](references/prop-pack-contract.md)

### UI、图标、掉落物

- 优先强调识别速度。
- 小尺寸下先看大色块和轮廓，不要先堆细节。

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
- prop pack 只适合一组同风格、同尺度、静态、紧凑的小道具；宽长结构、大体量对象、精确碰撞对象默认单独生成或改走 strip / tile / scene object 路线。
- 对所有原始生成图，默认要求纯色背景、固定格数、无文字、无 UI、无标签、无格线、无边框。

## 输出模式

每次执行本 skill，优先按这个结构组织结果：

1. 资产目标
2. 参考提炼
3. 原创 brief
4. 生成方案
5. 后处理方案
6. Godot 交付物

## 资源

- 资产模式判定： [references/asset-modes.md](references/asset-modes.md)
- 提示词规则： [references/prompt-rules.md](references/prompt-rules.md)
- 参考与原创边界规则： [references/reference-only-policy.md](references/reference-only-policy.md)
- 地图模式选择： [references/map-strategies.md](references/map-strategies.md)
- 分层地图合同： [references/layered-map-contract.md](references/layered-map-contract.md)
- prop pack 合同： [references/prop-pack-contract.md](references/prop-pack-contract.md)
- 后处理流程说明： [references/postprocess-workflow.md](references/postprocess-workflow.md)
- 后处理脚本： [scripts/postprocess_sprite_sheet.py](scripts/postprocess_sprite_sheet.py)
- 布局参考图脚本： [scripts/make_layout_guide.py](scripts/make_layout_guide.py)
- 分层预览合成脚本： [scripts/compose_layered_preview.py](scripts/compose_layered_preview.py)
