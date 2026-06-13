# 地图模式选择

当任务涉及 2D 地图、关卡、tilemap、场景道具或分层地图时，先选地图模式。

## 模式

- `tile_mode`
- `scene_mode`
- `side_scroll_mode`
- `grid_mode`
- `room_chunk_mode`
- `baked_scene_mode`

## 默认路由

- 俯视 RPG / 类宝可梦 / 怪物养成探索 -> `tile_mode`
- 塔防 / 幸存者竞技场 / 俯视场景型战斗 -> `scene_mode`
- 横版动作 / 平台跳跃 / 银河城 / 跑酷 -> `side_scroll_mode`
- 战棋 / 自动化 / 棋盘规则场景 -> `grid_mode`
- 模块化房间 / 肉鸽房间 -> `room_chunk_mode`
- 标题图 / 固定展示背景 -> `baked_scene_mode`

## 强规则

只要用户说的是可玩地图、关卡、场景，默认不要只交一张平面图。
至少要能拆出：

- 背景或底图
- props 或可交互对象
- 碰撞信息
- 区域 / 出口 / 关键点元数据
