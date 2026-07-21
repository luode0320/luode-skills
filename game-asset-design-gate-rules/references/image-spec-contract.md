# 图像设计交接合同

本合同用于把 `Image Generation Skill` 的设计结果，稳定转成 `game-asset-production-handoff-rules` 能直接实现的图像设计规格。

它不是最终美术成品说明，而是设计层与实现层之间的交接单。

## 适用场景

- 需要先设计，再实现 2D 游戏资产。
- 需要把参考图、项目风格、质量阶梯和输出约束收口成明确输入。
- 需要让同一批资产共享同一个设计基线，而不是各自临场发挥。

## 必填字段

每个 image spec 默认至少包含以下字段：

- `asset_type`：资产类型
- `use_case`：玩法用途或展示用途
- `primary_request`：本轮主要诉求
- `project_visual_baseline`：项目视觉基线摘要
- `reference_sources`：参考来源与参考价值
- `reference_gap`：与目标参考相比的主要差距
- `allowed_differences`：允许的受控差异
- `style_constraints`：风格约束
- `composition`：构图、视角、镜头与重心
- `materials`：材质和表面语言
- `lighting`：光照、阴影和发光规则
- `quality_tier`：`Tier 0` / `Tier 1` / `Tier 2` / `Tier 3`
- `output_format`：最终交付格式
- `pass_criteria`：通过条件
- `avoid`：必须避免的内容

## 设计层规则

- 先写 image spec，再写生成提示词。
- 如果 image spec 里没有项目视觉基线，就先补齐，不要直接生成。
- 如果 image spec 里没有参考差距，就不能说自己已经“对标参考”。
- 如果 image spec 里没有通过条件，就不能把设计结果当作收口结果。
- 如果目标是 `Tier 2` 或 `Tier 3`，spec 里必须显式说明高完成度要求，而不是只写“高质量”。

## 交接层规则

- `Image Generation Skill` 输出的是设计输入和图像方案。
- `game-asset-production-handoff-rules` 接的是这些输入，并继续完成实现、切图、后处理和 Godot 交付。
- 设计输出未达到通过条件时，默认回炉，不进入实现层。
- 设计阶段的参考图只负责提供方向，不允许直接沿用原包身份。

## 推荐模板

```text
资产类型：
用途：
主要诉求：
项目视觉基线：
参考来源：
参考差距：
允许差异：
构图/视角：
材质/光照：
质量阶梯：
输出格式：
通过条件：
禁止项：
```
