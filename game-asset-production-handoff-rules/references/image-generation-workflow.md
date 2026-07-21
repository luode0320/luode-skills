# Image Generation Workflow

本参考整理自 `Image Generation Skill` 的设计思路，目的是让 `game-asset-production-handoff-rules` 在开始实现前先完成图像设计层的收口。

源 skill:

- https://raw.githubusercontent.com/openai/codex/main/codex-rs/skills/src/assets/samples/imagegen/SKILL.md

## 设计阶段默认路径

在产出 2D 游戏资产前，先把需求转成图像设计 spec，再进入实现。

默认先判断：

1. 这是 `generate` 还是 `edit`
2. 输出是单资产还是多资产变体
3. 是否需要透明背景、参考图、局部编辑或合成
4. 资产是否会被当前项目直接消费

## 统一设计输入

设计 brief 默认至少包含：

- use case
- asset type
- primary request
- input images
- scene / backdrop
- subject
- style / medium
- composition / framing
- lighting / mood
- color palette
- materials / textures
- text
- constraints
- avoid

## 交付原则

- 先把图像设计想清楚，再做实现。
- 设计结果不是最终成品时，要明确标注为设计输入。
- 如果用户要多个资产或多个变体，先拆成多个明确目标，再做实现。
- 透明背景、切图、变体和局部编辑，全部先在设计层定清楚，再交给实现层收口。

## 和本 skill 的关系

- `Image Generation Skill` 负责设计阶段的图像方案和 prompt 收口。
- `game-asset-production-handoff-rules` 负责把设计好的方案实现成可交付的 2D 原创资产。
- 设计阶段不替代后处理、切图、命名、导出和 Godot 接入。
