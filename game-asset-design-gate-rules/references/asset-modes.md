# 资产模式

当一句用户请求可能落到多种资产生产方案时，先用这份模式表收敛。

## 资产类型

- `player`：可操控主角
- `npc`：场景功能型角色
- `creature`：怪物、野兽、精灵、Boss、召唤物
- `character`：非主角的人形单位
- `spell`：法术或技能序列
- `projectile`：火球、箭矢、子弹、飞刃等飞行物
- `impact`：命中、接触、爆炸爆发
- `prop`：物件、道具、祭坛、武器、拾取物
- `summon`：召唤入场素材
- `fx`：通用视觉特效

## 动作类型

- `single`
- `idle`
- `cast`
- `attack`
- `shoot`
- `jump`
- `hurt`
- `combat`
- `walk`
- `run`
- `hover`
- `charge`
- `projectile`
- `impact`
- `explode`
- `death`

## 打包预设

- `single_asset`：单图或单 sheet
- `unit_bundle`：默认 `idle + combat`
- `spell_bundle`：默认 `cast + projectile + impact`
- `combat_bundle`：默认 `idle + attack + hurt`
- `line_bundle`：一组形态线
- `hero_action_bundle`：一个动作一个 sheet
- `engine_atlas`：最终交付引擎的组合 atlas

## 常见网格

- `1x4`：投射物、简单循环特效
- `2x2`：短 idle、短攻击、短受击、简单 walk/run
- `2x3`：施法、死亡、较丰富动作
- `3x3`：大型待机、Boss aura、展示型循环
- `4x4`：四方向行走或较长单一连续动作

## 决策提示

- “做主角四方向行走” -> `player`
- “做侧视主角 idle/run/shoot/jump” -> `hero_action_bundle`
- “做火球术” -> `spell_bundle`
- “做命中爆炸” -> `impact`
- “做一组森林小道具” -> `prop`

## 默认后处理倾向

- 站地角色：`anchor=bottom`
- 浮空特效 / 投射物：`anchor=center`
- 高价值本体动作：优先保主体最大组件
