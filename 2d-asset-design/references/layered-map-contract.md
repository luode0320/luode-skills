# 分层地图合同

适用于俯视 RPG、探索地图、神殿/村庄/地牢图，以及角色与场景道具需要分层互动的 2D 地图。

## 层级

1. `base`
2. `props`
3. `actors`
4. `foreground`
5. `collision`
6. `zones`
7. `preview`

## Base 图规则

底图只允许放稳定地表信息：

- 地面材质
- 道路
- 水体
- 地表图案
- 低矮地形边界

不要把这些烘焙进 base：

- 建筑
- 树
- 门
- 栏杆
- 灯
- 箱子
- NPC
- 怪物
- UI

## 推荐流程

1. 先做 ground-only base
2. 再做 dressed reference
3. 最终运行时用 base + props + collision + zones

`dressed reference` 只是规划图，不是最终运行时唯一地图。
