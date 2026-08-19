---
name: 2d-game-dev
slug: 2d-game-dev
version: 1.0.0
displayName: 2D 游戏开发（Godot 4）
summary: 用 Godot 4 从零到可玩的 2D 游戏完整工作流：脚手架、场景架构、平台跳跃/俯视角控制器、TileMap、UI、资产接入、无头验证与导出。
description: >-
  用 Godot 4 + GDScript 开发 2D 游戏的端到端工作流。触发场景："做一个 2D 游戏"、
  "写个平台跳跃/横版/俯视角/弹幕/roguelike 游戏"、"用 Godot 做游戏"、"加个角色控制器/
  相机/血条/关卡/敌人"、"游戏跑不起来帮我查"、"导出到网页/桌面"、"make a 2D game"、
  "platformer / top-down shooter in Godot"。覆盖项目脚手架、场景树架构规范、常用玩法
  模板（CharacterBody2D 控制器、TileMap 关卡、Area2D 拾取与伤害、敌人 AI）、UI/HUD、
  像素画导入设置、免费素材源、命令行无头验证与截图验收、导出发布。只做 2D；3D 游戏用
  3d-game-dev skill。
---

# 2D 游戏开发（Godot 4 + GDScript）

从零把一个 2D 游戏做到可玩、可验证、可发布。引擎固定用 **Godot 4.x + GDScript**：
免费开源、单二进制、命令行友好（agent 可以无头跑起来自测），2D 支持是引擎一等公民。

核心原则：**每加一个系统就跑一次游戏验证**，不要盲写一大堆脚本最后一起调。
Godot 的报错在启动时就会暴露，无头运行 + 截图就能闭环验收，见第 8 节。

## 1. 环境准备

```bash
godot --version   # 需要 4.x；没有则安装：
# macOS:  brew install godot
# Windows: winget install GodotEngine.GodotEngine
# Linux:  下载官方二进制 https://godotengine.org/download
```

## 2. 项目脚手架

不需要打开编辑器,直接写文件即可。最小 `project.godot`：

```ini
[application]
config/name="MyGame"
run/main_scene="res://scenes/main.tscn"
config/features=PackedStringArray("4.4")

[rendering]
textures/canvas_textures/default_texture_filter=0   ; 像素画必须关滤波,高清美术删掉这行

[display]
window/size/viewport_width=640
window/size/viewport_height=360
window/stretch/mode="canvas_items"                  ; 低分辨率整数缩放,像素画标配
```

目录约定：

```
scenes/    每个实体一个 .tscn（player.tscn, enemy.tscn, level_1.tscn, hud.tscn）
scripts/   与场景同名的 .gd
assets/    sprites/ tiles/ audio/ fonts/
autoload/  全局单例（game_state.gd 等）
```

`.tscn` 是文本格式,可以直接手写/由 agent 生成,不必依赖编辑器。写完用
`godot --headless --path . --import` 让引擎导入资源,再运行验证。

## 3. 架构规范（避免后期重构的最少规则）

- **一个实体一个场景**：player、每种敌人、子弹、道具、HUD 各自独立 `.tscn`,用
  `preload().instantiate()` 动态生成。
- **信号向上、调用向下**：子节点用 `signal` 通知父级（`died`、`coin_collected`）,
  父级直接调用子节点方法。兄弟节点之间不互相引用。
- **全局状态用 autoload**：分数、关卡进度、设置放 `autoload/game_state.gd`,在
  `project.godot` 的 `[autoload]` 段注册 `GameState="*res://autoload/game_state.gd"`。
- **物理逻辑写在 `_physics_process(delta)`**,渲染/输入相关写 `_process`。所有位移乘
  `delta`（`velocity` 本身是速度,`move_and_slide()` 内部已处理,不要再乘）。
- **碰撞分层**：在项目设置里命名 physics layers（player / enemy / world / pickup /
  player_hurtbox …）。`collision_layer` 是"我是谁",`collision_mask` 是"我碰谁",
  绝大多数碰撞 bug 都是这两个搞反。

## 4. 玩法模板

### 平台跳跃控制器（CharacterBody2D）

```gdscript
extends CharacterBody2D
const SPEED := 130.0
const JUMP_VELOCITY := -300.0

func _physics_process(delta: float) -> void:
    if not is_on_floor():
        velocity += get_gravity() * delta
    if Input.is_action_just_pressed("jump") and is_on_floor():
        velocity.y = JUMP_VELOCITY
    var dir := Input.get_axis("move_left", "move_right")
    velocity.x = dir * SPEED
    move_and_slide()
```

手感增强按需加：coyote time（离地后 0.1s 内仍可跳）、jump buffer（落地前 0.1s 的
跳跃输入生效）、松开跳跃键提前减速上升（可变跳高）。这三条是"手感好"的主要来源。

### 俯视角控制器

```gdscript
func _physics_process(_delta: float) -> void:
    velocity = Input.get_vector("move_left", "move_right", "move_up", "move_down") * SPEED
    move_and_slide()
```

输入动作在 `project.godot` 的 `[input]` 段定义（WASD + 方向键都绑上）。

### 相机

Player 下挂 `Camera2D`：`position_smoothing_enabled = true`,用
`limit_left/right/top/bottom` 卡住关卡边界防止露出黑边。

### 关卡（TileMapLayer）

Godot 4.3+ 用 `TileMapLayer`（旧 `TileMap` 已废弃）。TileSet 里给砖块图集开
physics layer 画碰撞形状,地形自动接缝用 terrain。关卡即一个场景：
`level_1.tscn = TileMapLayer + 出生点 Marker2D + 敌人/道具实例`。

### 拾取与伤害（Area2D）

```gdscript
# coin.tscn: Area2D + Sprite2D + CollisionShape2D
extends Area2D
func _ready() -> void:
    body_entered.connect(func(body):
        if body.is_in_group("player"):
            GameState.coins += 1
            queue_free())
```

伤害同理：敌人挂 hitbox（Area2D）,玩家挂 hurtbox,层/掩码只对彼此开放。
受击后给玩家短暂无敌帧（Timer + 闪烁）。

### 敌人 AI

从简单到够用：来回巡逻（`RayCast2D` 探测悬崖/墙壁掉头）→ 视野内追击
（到玩家的向量归一化 × 速度）→ 状态机（一个 `enum State` + `match`,不必上框架）。

## 5. UI / HUD 与游戏流程

- HUD 用 `CanvasLayer` 场景,内部 Control 节点 + 锚点布局;监听 `GameState` 的信号
  刷新血条（`TextureProgressBar`）和分数（`Label`）。
- 流程 = 场景切换：`get_tree().change_scene_to_file("res://scenes/level_1.tscn")`。
  主菜单 → 关卡 → 结算,各是一个场景。
- 暂停：`get_tree().paused = true`;暂停菜单所在 CanvasLayer 的 `process_mode`
  设为 `PROCESS_MODE_WHEN_PAUSED`。
- 音频：BGM 一个常驻 `AudioStreamPlayer`（可放 autoload）,音效各实体自带;
  总线音量走 `AudioServer.set_bus_volume_db`。

## 6. 美术与音频

- **像素画导入**：全局默认滤波已在第 2 节关掉;个别高清图在 Import 面板单独改回。
- **免费素材（可直接商用）**：Kenney.nl（CC0,量大管饱,风格统一）、itch.io 免费区、
  OpenGameArt。先用 Kenney 把玩法跑通,再换定制美术。
- **AI 生成**：若装有 `game-asset` skill,可用 AI 生成角色/图块/UI 并抠图、切
  sprite sheet、配 BGM 和音效;没有就用上面的免费源。
- **Sprite 动画**：`AnimatedSprite2D` + SpriteFrames 从 sprite sheet 切帧;
  按朝向 `flip_h`,按状态 `play("run"/"idle"/"jump")`。

## 7. 手感与打磨清单

出玩法原型后按优先级打磨：屏幕震动（Camera2D 偏移噪声）、受击闪白与顿帧、
粒子（`GPUParticles2D`：落地灰尘、拾取闪光）、音效反馈每个交互都要有、
死亡/重生流程、`Tween` 做 UI 弹入弹出。这些便宜且对体验提升巨大。

## 8. 验证闭环（agent 自测,别让用户当测试员）

```bash
# 1. 资源导入 + 解析错误检查（改完场景/脚本后必跑）
godot --headless --path . --import 2>&1 | grep -iE "error|SCRIPT ERROR" || echo IMPORT_OK

# 2. 无头试运行 N 帧,抓启动期运行时报错（node not found、null 引用等）
godot --headless --path . --quit-after 120 2>&1 | grep -iE "error" || echo RUN_OK

# 3. 视觉验收：正常窗口跑几秒 + 自动截图（无头模式不渲染,截图必须带窗口）
godot --path . --quit-after 180   # 配合下面的截图 autoload
```

截图 autoload（临时加,验收完移除）：

```gdscript
extends Node
func _ready() -> void:
    for i in 3:
        await get_tree().create_timer(1.0).timeout
        get_viewport().get_texture().get_image().save_png("res://.shots/shot_%d.png" % i)
```

跑完读取 `.shots/*.png` 检查画面：角色是否在场、图块是否错位、UI 是否遮挡。
**每完成一个系统就走一遍 1→2,里程碑节点走 3。**

## 9. 导出发布

首次导出先装模板：`godot --headless --install-export-templates`（或编辑器里下载）。
写 `export_presets.cfg` 后：

```bash
godot --headless --path . --export-release "Web" build/web/index.html
godot --headless --path . --export-release "macOS" build/mac/MyGame.zip
```

Web 是最好分享的目标（itch.io 直接托管）;像素小游戏包体通常 < 50MB,无需担心。

## 10. 常见坑

- 位移不乘 `delta` → 帧率相关的移速;但 `velocity` 交给 `move_and_slide()` 时不要
  自己再乘。
- 碰撞层/掩码配反 → 用项目设置里的命名层排查,别用裸数字。
- 像素画发糊 → 忘了关 texture filter;缩放出现细缝 → stretch mode 不是
  `canvas_items` 或相机坐标非整数（开 2D 项目设置的 snap）。
- `@onready var x = $Path/To/Node` 路径改名后悄悄变 null → 用 `%UniqueName`
  （场景内唯一名）引用,重构不断。
- 俯视角遮挡关系错 → 开 Y-sort（TileMapLayer 与实体父节点都要开）。
- 单向平台：TileSet 物理层勾 one-way;下跳用临时忽略碰撞层实现。
