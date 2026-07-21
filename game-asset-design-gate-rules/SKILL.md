---
name: game-asset-design-gate-rules
description: 2D 游戏素材的设计确认闸门。当用户想要新建、重做、补齐、替换、迭代或统一 2D 游戏素材，需要先做参考候选筛选、判定质量阶梯、锁定项目视觉基线、写素材 brief、形成 image spec 或走设计预览确认时自动使用。设计尚未确认前不进入真实生成、后处理或 Godot 交付；已确认设计的生产、动画、地图、后处理和 Godot 交接请转交 `game-asset-production-handoff-rules`。正式素材任务默认先联动共享根目录设计 skill `agent-sprite-forge-design`：先检索参考候选，再出设计图给用户确认。
---

# 2D 游戏素材设计确认闸门

## 作用

这个 skill 只负责 2D 游戏素材链路里的"设计"这一段：明确素材的玩法职责、视觉方向、风格边界与可读性目标，并在真实生成前完成参考筛选、质量阶梯判定、项目视觉基线锁定、素材 brief 和设计预览确认。生成、后处理和 Godot 交付由 `game-asset-production-handoff-rules` 负责，两者是同源拆分，设计闸门必须先通过，生产交接才能开始。

在进入实现前，默认先用共享根目录 skill `agent-sprite-forge-design` 做美术设计收口：先检索外部参考候选给用户，再基于用户选定截图配合 `Image Generation Skill` 产出设计图预览；只有用户确认设计方向后，才把结果交给 `game-asset-production-handoff-rules` 进入正式生产。

## 自动触发范围

出现以下任一意图时，自动使用本 skill：

- 用户明确要求"做素材""设计素材""生成素材""换美术""补 2D 资源""重做角色/怪物/UI/地图素材"。
- 当前任务推进到某一步，发现缺少角色、怪物、子弹、道具、图标、地图、瓦片、场景道具、特效、HUD 等 2D 素材，需要先确定设计方向。
- 需要把第三方素材站、商店页、作品页或用户提供截图当成参考，再重新设计项目自己的原创素材。
- 需要先去素材网站检索候选、给用户看截图、再根据用户选中的参考做原创设计。
- 需要判定当前资产该走哪个质量阶梯（Tier 0~3），或需要锁定/核对项目视觉基线。
- 需要把设计方向写成素材 brief 或 image spec，交给生产组实现。

以下情况不要用本 skill：

- 3D 模型、3D 场景、骨骼动画、音效、配乐、文案、纯代码逻辑。
- 用户只是在问"这个素材授权是否可用"，但还没有进入素材设计或生产阶段。
- 设计已经确认，只需要真实生成、切帧、后处理或 Godot 交付：见 `game-asset-production-handoff-rules`。

## 核心原则

### 1. 先设计，再实现

设计阶段默认先走共享根目录 `agent-sprite-forge-design`，并结合 `Image Generation Skill` 的图像设计工作流：

- 先检索外部参考候选并给用户看
- 先让用户选定要推进的参考截图或参考方向
- 先把资产目标写成清晰的 image spec
- 先明确 sprite / map / layered map / FX / engine handoff 属于哪条设计链路
- 再判断是 `generate` 还是 `edit`（真实生成参数由 `game-asset-production-handoff-rules` 的 [references/image-generation-workflow.md](../game-asset-production-handoff-rules/references/image-generation-workflow.md) 负责）
- 再明确是否需要透明背景、变体、合成或局部修改
- 先给用户看设计图预览并等待确认
- 再把已确认的设计结果交给 `game-asset-production-handoff-rules` 进行实现和后处理

如果用户继续通过对话调整设计，默认继续留在设计阶段，不得抢跑进入最终生产。

还必须读取 [references/design-preview-confirmation-gate.md](references/design-preview-confirmation-gate.md)。

### 2. 第三方素材默认只做参考，不直接入库

Kenney、OpenGameArt、Quaternius、KayKit、Godot Demo、itch.io、CraftPix、Fab、ArtStation Marketplace、Gumroad 等来源默认都只允许做参考板、比例参考、层次参考、风格拆解与制作约束参考。
不要把第三方素材直接作为最终游戏资产，也不要只做轻微换色、裁切、描边后冒充原创成品。

如果当前阶段只是做参考检索与方向筛选，不要因为素材站点付费、需要登录、需要购买或只能看商店页，就把它从候选池排除；这类限制只在"需要实际下载或直接接入第三方素材"时再考虑。

需要参考规则时，读取 [references/reference-only-policy.md](references/reference-only-policy.md)。

### 3. 先满足玩法可读性，再追求装饰细节

任何素材先回答这几个问题：

- 玩家需要在多远距离识别它。
- 它在战斗里承担什么玩法职责。
- 它要和哪些同类对象拉开差异。
- 它是否需要动画、方向、层级、碰撞边界或交互提示。

如果细节会破坏识别速度，优先删细节。

但"删细节"不等于"删结构"。对于树、建筑、掩体、场景机关、门、桥、路障、遗迹、残骸、雕像等场景物件，默认必须保留足以让单体物件成立的结构信息、材质层次、接地感和体块关系，不能把"更扁平、更少颜色"误做成"轻装饰符号"。

### 4. 只构建项目原创 2D 素材

目标不是"找到能用的现成包"，而是"借鉴参考后，为当前项目构建新的原创 2D 视觉资产"。

### 5. 商业级场景物件优先于轻装饰交付

除非用户明确要求"临时 demo 占位""只做极简符号""只做噪点/小装饰 pack"，否则：

- 默认不要走"轻装饰、小装饰符号、噪点"路线。
- 默认不要把树、建筑、掩体、场景机关、门、桥、残骸、雕像、祭坛、地标、可交互场景物件做成随手点缀。
- 默认把场景物件当成独立 hero prop 设计，再决定是否需要补充少量 micro props。

本项目默认拒绝"只是为了填空而存在的小装饰包"。轻装饰、噪点、符号化草簇只能作为明确说明的 demo 资产，不能作为正式生产方案。

### 6. 商业级审稿闸门优先于"结构齐全"

"有轮廓、有体积、有结构、有阴影"只是最低级 hero prop 门槛，不等于商业级完成度。
当用户要求高质量、正式资产、接近成品游戏观感，或已经指出"距离参考差很多"时，必须进入商业级审稿闸门。

需要审稿细则时，读取 [references/art-direction-quality-gate.md](references/art-direction-quality-gate.md)。

默认结论规则：

- 只达到"能看出是什么"的结果，判为 `Tier 1: low hero prop`，不得当正式最终资产交付。
- 只有同时具备好看的外轮廓、线稿节奏、姿态/生长势、负形、材质层级、局部焦点、接地影和地图融合度，才允许进入正式候选。
- 程序几何图形、简单椭圆堆叠、规则多边形拼接、重复 stamp、均匀描边、没有手绘线条节奏的结果，只能作为构图草稿或 demo，默认不能作为正式 hero prop。
- 对树木、怪物、建筑、地标、Boss、主角等高价值资产，必须先做参考差距拆解，再生成或制作原创资产。

### 7. 项目风格一致性是强制前置条件

任何正式素材都必须像来自同一个游戏，而不是像多个素材包拼在一起。
质量高但风格不一致，仍然判定为失败结果。

需要风格一致性规则时，读取 [references/project-style-consistency-contract.md](references/project-style-consistency-contract.md)。

默认强规则：

- 设计新素材前，必须先锁定项目视觉基线，包括镜头角度、描边逻辑、色相范围、明度/饱和度、材质语言、发光方式、阴影方向、细节密度、UI/战斗可读性优先级。
- 新素材必须继承项目主视觉 DNA，只允许在玩法职责需要时做受控差异。
- 不允许因为单个素材"更好看"就引入完全不同画风、不同描边、不同渲染方式、不同光照方向或不同材质语言。
- 如果参考图风格强于项目现有风格，必须先提炼可融入项目的部分，再重设计；不能把参考风格整包搬进项目导致风格割裂。
- 交付前必须做风格一致性自审；不通过时优先回炉，而不是继续堆细节。

## 设计确认流程

### 第 0 步：先走设计确认闭环

正式 2D 素材任务默认必须先命中共享根目录 `agent-sprite-forge-design`，再交给生产组进入生产部分。

默认顺序：

1. 检索外部参考候选
2. 向用户展示候选素材截图、链接或候选清单
3. 由用户选定要推进的参考截图，或补充新的参考截图
4. 锁定项目视觉基线
5. 形成 image spec / 素材 brief
6. 生成设计图预览
7. 向用户展示设计图并等待确认
8. 如果用户不满意，继续通过对话迭代设计图
9. 只有用户明确确认满意后，才把设计结果交给 `game-asset-production-handoff-rules` 进入正式生产、后处理和 Godot 交付

没有用户确认时，不得把设计预览当最终素材交付。
没有用户选定参考前，不得直接跳过候选筛选阶段假定风格。

如果任务进入角色、怪物、Boss 的动作生产、direction set 或 sprite sheet 生产，设计确认通过后转交生产组的 [references/character-animation-production-gate.md](../game-asset-production-handoff-rules/references/character-animation-production-gate.md)，并联动共享根目录 `character-sprite-animation-production`。

### 第 1 步：识别资产任务

先把请求收敛成明确资产类别：角色、怪物、Boss、投射物、命中特效、掉落物/拾取物、UI/HUD/图标、地图背景、瓦片/Tile、场景道具/Hero Prop、小型道具/Prop Pack（仅在明确满足例外条件时）、动画 Sprite Sheet。

如果用户一次要很多资产，优先拆成一个主资产族先做，不要在一个回合里把全部资产混成一锅。

当一句话可能对应多种素材生产方案时，读取 [references/asset-modes.md](references/asset-modes.md)。

如果请求涉及树木、建筑、掩体、场景机关、门、桥、地标、建筑残骸、祭坛、雕像、车辆残骸、大型植被、可交互地图物件或任何"用户会盯着看并判断质感"的场景对象，默认直接判定为 `Hero Prop`，而不是 `Prop Pack`。

### 第 1.2 步：先做参考候选筛选

在写正式 brief 前，先做外部参考候选筛选，最少整理出：候选来源网站、候选链接或页面、候选截图或可描述的预览图、每个候选的风格标签、每个候选适合借鉴的点、每个候选与项目当前方向的风险点。

如果用户已经直接给了参考截图，可以跳过网站检索，但仍然要做参考拆解。
若当前只能访问网站页面、商店页、作品页、宣传图或付费预览图，也可以纳入候选；只要当前任务不是"直接下载接入"，就不要把这类来源排除。

### 第 1.5 步：判定质量阶梯

生成前必须先判定当前资产应该达到哪个质量阶梯：

- `Tier 0: Blockout`：只验证尺寸、位置和碰撞，不允许当正式美术。
- `Tier 1: Low Hero Prop`：有基本结构和体积，但造型、线稿和材质仍像低级草稿；只能作为迭代中间态。
- `Tier 2: Production Candidate`：具备明确造型语言、手绘线条节奏、材质分层和可用接地感，可以进入项目候选。
- `Tier 3: Shippable`：缩小后仍好看，单体成立，放进地图也融合，能承受用户对照商业游戏截图审视。

除非用户明确说"占位/demo/临时"，本项目正式素材默认目标至少是 `Tier 2`，重要角色、怪物、树木、建筑、Boss、地图主视觉默认目标是 `Tier 3`。

### 第 1.6 步：锁定项目视觉基线

写素材 brief 前，必须先建立或读取当前项目的视觉基线。

优先来源：项目已有正式素材（角色、怪物、地图、UI、特效、图标）、项目素材记录文档（例如 `game/assets/README.md`）、项目设计文档或 AGENTS.md 中的美术方向、用户本轮明确指定的风格方向。

视觉基线至少包含：镜头与透视、轮廓与描边、色彩、材质、光照与阴影、细节密度、玩法可读性。

如果已有素材风格本身还不稳定，先输出"临时项目风格基线"，并在本轮所有素材里保持一致；不得每个素材各自找一个新画风。
需要把设计结果交给实现层时，必须先形成 image spec，再交给生产组进入生成提示词或实现步骤。

### 第 2 步：先写素材 brief

在交给生产组生成素材前，先输出简短素材 brief，并准备设计图预览。至少包含：资产类型、玩法用途、观看视角、风格方向、项目视觉基线继承点、允许的受控差异、轮廓语言、配色方向、材质提示、体积与结构要求、接地感/阴影策略、线稿与边缘质量要求、局部焦点和视觉重心、质量阶梯目标、动画需求、交付格式。

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

如果是场景物件，还必须补：是否属于 `Hero Prop`、单体是否需要独立成立、是否需要明显的接地阴影、是否需要材质分层、是否允许只作为背景噪点（默认不允许）、参考差距拆解、回炉条件、风格一致性风险、image spec 交接字段（资产类型、用途、主要诉求、项目视觉基线、参考来源、参考差距、允许差异、风格约束、构图、材质、光照、质量阶梯、输出格式、通过条件、禁止项）。

设计工作流参考：[references/image-spec-contract.md](references/image-spec-contract.md)、[references/design-preview-confirmation-gate.md](references/design-preview-confirmation-gate.md)；真实生成的 brief-to-generation 映射规范见生产组 [references/image-generation-workflow.md](../game-asset-production-handoff-rules/references/image-generation-workflow.md)。

### 第 3 步：处理外部参考

当请求里提到某个外部素材包或截图时：

1. 提炼可复用信息：轮廓、色块、层次、材质、节奏、构图密度、镜头角度。
2. 丢弃直接复用风险高的部分：独特造型、完整构图、原包专属排列、可直接辨认的角色或道具设计。
3. 重新组合成当前项目自己的风格 brief。

如果用户还没有指定参考图，先由 agent 提供候选参考，不要默认把检索责任推回给用户。

参考图只能用于提升项目风格内的质量，不允许让项目突然变成另一个游戏。提炼参考时必须分成两类：可吸收（轮廓节奏、线稿层次、材质组织、焦点细节、阴影/发光方法）；不直接吸收（原作独特造型、世界观符号、专属配色比例、可识别角色或物件身份、与项目现有视觉基线冲突的渲染方式）。

当存在参考图时，必须额外做"差距拆解"，至少比较外轮廓、线条节奏、姿态/生长势、负形、材质层次、局部焦点。

不要输出"就直接用这个包"作为结论。

## UI、图标、掉落物

- 优先强调识别速度。
- 小尺寸下先看大色块和轮廓，不要先堆细节。

## 设计输出模式

每次执行本 skill，优先按这个结构组织结果：

1. 资产目标
2. 参考提炼
3. 原创 brief
4. 设计预览方案
5. 用户确认状态

用户确认满意后，把以上 5 项交给 `game-asset-production-handoff-rules`，由对方接续"生成方案 / 后处理方案 / Godot 交付物"。

## 资源

- 资产模式判定： [references/asset-modes.md](references/asset-modes.md)
- 提示词规则： [references/prompt-rules.md](references/prompt-rules.md)
- 商业级审稿闸门： [references/art-direction-quality-gate.md](references/art-direction-quality-gate.md)
- 项目风格一致性合同： [references/project-style-consistency-contract.md](references/project-style-consistency-contract.md)
- 图像设计交接合同： [references/image-spec-contract.md](references/image-spec-contract.md)
- 设计预览确认闸门： [references/design-preview-confirmation-gate.md](references/design-preview-confirmation-gate.md)
- 参考与原创边界规则： [references/reference-only-policy.md](references/reference-only-policy.md)
