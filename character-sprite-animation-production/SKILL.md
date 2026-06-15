---
name: character-sprite-animation-production
description: 用于在 2D 游戏角色、怪物、Boss 或类角色单位需要动作生产时，负责角色动画的生产、分方向拆分、fixed-cell sheet 布局、动作 QA 与预览验证。吸收 character-animation-creator-skill 的核心思路：先锁定角色 identity，再做 base pose，再按动作和方向逐项扩展，并在生成后做 contact sheet、方向一致性、体量漂移和动画可读性审查。适用于 idle、walk、run、attack、cast、hit、death、4向/8向、fixed-cell sprite sheet 等角色动画任务。
---

# Character Sprite Animation Production

## 作用

这个 skill 只负责 2D 角色动画生产，不负责项目整体美术方向设计。

它吸收 `character-animation-creator-skill` 的核心强项：

1. 先锁定角色 identity，再做动作。
2. 先做 base pose / canonical frame，再扩展成整套动作。
3. 按动作、方向、尺寸逐项生产，而不是一次性混生成。
4. 把 animation QA 当成正式交付的一部分，而不是生成完就结束。

## 自动触发

当满足以下任一条件时自动使用：

- 用户要求角色、怪物、Boss 做动画。
- 用户要求 idle / walk / run / attack / hit / death / cast / dash 等动作。
- 需要把单体角色设计扩展成 sprite sheet。
- 需要做 4向 / 8向角色动画。
- 需要检查角色动作体量是否漂移、方向是否统一、帧间是否稳定。

## 核心流程

### 1. 先锁 identity

动作生产前，必须先确认：

- 角色身份
- 武器或肢体主结构
- 头身比例
- 轮廓重心
- 主配色和焦点色
- 镜头角度

如果角色设计本身还未确认，先回到设计阶段，不得直接做动画。

### 2. 先做 base pose

先建立一个 canonical base pose：

- neutral idle
- 清楚的脚底锚点
- 清楚的武器朝向
- 适合作为所有方向和动作扩展的基础

没有 base pose，不得直接生成整套动作。

### 3. 按动作和方向拆分

默认拆分维度：

- action：idle / walk / run / attack / cast / hit / death
- direction：front / back / left / right 或 8向
- size tier：如果有多尺寸输出需求，再单独处理

不要把所有动作和所有方向糊成一个 prompt 一次做完。

### 4. 先 preview 再 final

先给出 contact sheet、方向预览或关键动作预览。
如果用户或主 skill 还在确认阶段，这些结果默认视为 preview，不直接进入最终生产。

### 5. 动画 QA

生成后必须检查：

- 角色 identity across frames 是否稳定
- 头、躯干、武器、脚底锚点是否漂移过大
- 动作节奏是否可读
- 左右方向是否真的成对，而不是乱画
- 本体体量是否因攻击帧或大 FX 被挤小
- 是否应该把大范围 FX 分离成独立层

## 固定格子规则

默认适合 fixed-cell sprite sheet：

- 主体完整落在格内
- 四周保留安全边距
- 脚底锚点一致
- 不为了塞进格子而把角色缩得过小

如果大武器、刀光、枪焰、长拖尾破坏本体稳定性，默认拆分 FX，不把它们硬塞进角色本体格子。

## 默认交付

至少说明：

- action set
- direction set
- sheet rows x cols
- cell size
- anchor strategy
- preview / gif / contact sheet 是否已导出
- 是否存在需回炉动作

## 与 2d-asset-design 的关系

- `agent-sprite-forge-design` 负责设计阶段和用户确认
- `2d-asset-design` 负责正式素材生产总流程
- `character-sprite-animation-production` 只负责角色动画生产与 QA

如果任务只是静态单体设计图，不触发本 skill。
如果任务进入角色动作或 sprite sheet 生产，`2d-asset-design` 应自动联动本 skill。

## 参考来源

本 skill 吸收自 `character-animation-creator-skill` 的公开工作流思路，包括：

- character identity lock
- canonical base sprite
- per-action / per-direction generation
- fixed-cell animation production
- contact sheet / preview / QA workflow

参考仓库：

- <PRIVATE_URL>
