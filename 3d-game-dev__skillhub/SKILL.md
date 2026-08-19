---
name: 3d-game-dev
slug: 3d-game-dev
version: 1.0.0
displayName: 3D 游戏开发（Godot 4）
summary: 用 Godot 4 从零到可玩的 3D 游戏完整工作流：第一/第三人称控制器、glTF 资产管线、关卡拼搭、灯光氛围、导航 AI、性能与导出。
description: >-
  用 Godot 4 + GDScript 开发 3D 游戏的端到端工作流。触发场景："做一个 3D 游戏"、
  "第一人称/第三人称/FPS/TPS/3D 平台跳跃"、"用 Godot 做 3D"、"加个 3D 角色控制器/
  相机/敌人寻路/关卡"、"导入 glb 模型不显示"、"3D 场景太暗/太卡"、"make a 3D game"、
  "first-person controller in Godot"。覆盖项目脚手架、CharacterBody3D 控制器与相机
  （鼠标视角、SpringArm3D）、glTF 导入与免费 CC0 资产源（KayKit/Poly Haven）、
  StandardMaterial3D 材质贴图、WorldEnvironment 灯光氛围、NavigationAgent3D 敌人
  寻路、动画播放、HUD、无头验证与截图验收、性能优化、导出。只做 3D；2D 游戏用
  2d-game-dev skill。
---

# 3D 游戏开发（Godot 4 + GDScript）

从零把一个 3D 游戏做到可玩、可验证、可发布。引擎固定 **Godot 4.x + GDScript**，
资产格式固定 **glTF（.glb）**。约定 **1 unit = 1 米**，所有模型按真实尺度摆放。

核心原则：**先灰盒后美术**——用 CSGBox3D/基本几何把玩法和手感调对，再替换成正式
模型；**每加一个系统就跑一遍验证**（见第 9 节）。

## 1. 环境与脚手架

```bash
godot --version   # 需要 4.x；macOS: brew install godot
```

`project.godot` 最小配置（渲染器决定平台与画质上限）：

```ini
[application]
config/name="My3DGame"
run/main_scene="res://scenes/main.tscn"
config/features=PackedStringArray("4.4")

[rendering]
renderer/rendering_method="forward_plus"   ; 桌面端；导出网页/手机改 "mobile" 或 "gl_compatibility"
```

目录约定：

```
scenes/    main.tscn player.tscn enemy.tscn level_1.tscn hud.tscn
scripts/   同名 .gd
assets/    models/ materials/ textures/ hdris/ audio/
autoload/  game_state.gd
```

`main.tscn` 起步三件套：`WorldEnvironment` + `DirectionalLight3D`（开 shadow）+
一块地板（CSGBox3D 或 MeshInstance3D+StaticBody3D）。没有灯和环境的 3D 场景是
纯黑的——"画面全黑"九成是这里。

## 2. 角色控制器（CharacterBody3D）

### 第一人称

节点：`CharacterBody3D > CollisionShape3D(Capsule) + Node3D(Head) > Camera3D`

```gdscript
extends CharacterBody3D
const SPEED := 5.0
const JUMP_VELOCITY := 4.5
const MOUSE_SENS := 0.002
@onready var head: Node3D = $Head

func _ready() -> void:
    Input.mouse_mode = Input.MOUSE_MODE_CAPTURED

func _unhandled_input(event: InputEvent) -> void:
    if event is InputEventMouseMotion:
        rotate_y(-event.relative.x * MOUSE_SENS)
        head.rotate_x(-event.relative.y * MOUSE_SENS)
        head.rotation.x = clampf(head.rotation.x, -PI/2, PI/2)

func _physics_process(delta: float) -> void:
    if not is_on_floor():
        velocity += get_gravity() * delta
    if Input.is_action_just_pressed("jump") and is_on_floor():
        velocity.y = JUMP_VELOCITY
    var input := Input.get_vector("move_left", "move_right", "move_forward", "move_back")
    var dir := (transform.basis * Vector3(input.x, 0, input.y)).normalized()
    velocity.x = dir.x * SPEED
    velocity.z = dir.z * SPEED
    move_and_slide()
```

按 Esc 释放鼠标：`Input.mouse_mode = Input.MOUSE_MODE_VISIBLE`。

### 第三人称

相机换成 `SpringArm3D > Camera3D`（spring_length 3~5，SpringArm 自动防穿墙），
水平旋转加在 SpringArm 的 yaw 上；移动方向按相机朝向换算，角色模型用
`look_at` 或对 `rotation.y` 做 `lerp_angle` 平滑转身。

## 3. 资产管线（glTF）

- **免费 CC0 源**：KayKit（低多边形套件+带骨骼动画角色，Godot AssetLib 可搜）、
  Quaternius、Poly Haven（写实道具/PBR 材质/HDRI，无角色）、Poly Pizza。
  先拿套件把关卡拼出来，风格统一且零成本。
- **`.glb` 优先于 `.gltf`**：Godot 4 下部分 `.gltf` 会*静默*导入失败
  （`load()` 返回 null 且无报错）。下载的资产包好文件常嵌很深，
  `find <dir> -iname '*.glb'` 先定位。
- **导入**：`.glb` 拖进 `res://` 自动导入；代码里
  `preload("res://assets/models/x.glb").instantiate()` 直接实例化。
- **碰撞**：导入的模型自带的只有网格。静态景物在 Import 面板给 mesh 开
  "Generate Physics"，或代码 `$Mesh.create_trimesh_collision()`（仅静态；
  动态刚体用 convex）。
- **带动画的角色**：glb 内含 `AnimationPlayer`，
  `$Model/AnimationPlayer.play("Run")`；先 `get_animation_list()` 打印确认动画名。
  状态多了再上 `AnimationTree`（locomotion 混合、one-shot 攻击），两三个状态
  直接 play 切换即可。
- **AI 生成贴图/HUD**：若装有 `game-asset-gen` skill 可生成无缝贴图与图标；
  `game-asset-3d` skill 可自动搜索下载上述 CC0 源。没有则手动下载。

## 4. 关卡搭建

- **灰盒**：CSGBox3D 快速拼布局（记得勾 Use Collision），手感对了再替换模型。
- **套件拼搭（kit-bash）**：KayKit 类套件逐件实例化摆放；同一件重复几十次以上
  改用 `MultiMeshInstance3D`（一次 draw call）。
- **规则网格关卡**（地牢/体素风）：`GridMap` + MeshLibrary（把套件场景转成
  MeshLibrary 后像 3D TileMap 一样刷）。
- 出生点、触发器用 `Marker3D` / `Area3D`（拾取、伤害区、关卡切换门，写法同 2D，
  只是节点带 3D 后缀）。物理层命名规范同样适用：layer=我是谁，mask=我碰谁。

## 5. 材质与贴图（StandardMaterial3D）

- 贴图三件套：albedo + normal（Godot 用 **OpenGL 约定 nor_gl**）+
  roughness/AO/metallic（Poly Haven 的 `arm` 是三合一打包图，
  勾 "ORM" 材质类型或分通道指定）。
- 平铺：`uv1_scale` 控制重复次数；没有 UV 的程序化几何体勾 `uv1_triplanar`。
- 天空：`WorldEnvironment > Environment > Sky`。快速出效果用
  `ProceduralSkyMaterial`；要真实感用 Poly Haven HDRI + `PanoramaSkyMaterial`，
  并把 ambient light source 设为 Sky，让环境光来自天空。

## 6. 灯光与氛围（画面质感的 80%）

- `DirectionalLight3D` 当太阳：开 shadow，角度斜 30~45°；室内补
  `OmniLight3D`/`SpotLight3D`（阴影灯越少越好，每盏阴影灯都有开销）。
- `Environment` 上依次调：Tonemap 设 **Filmic/ACES**（默认 Linear 是"塑料感"
  主因）、开 Glow（自发光材质会泛光）、加 Volumetric Fog 或普通 Fog 拉出景深
  层次、SSAO 增强角落接触感（Forward+ 专属）。
- 调完灯光对比截图前后——这一步性价比极高，别跳过。

## 7. 敌人 AI 与寻路

关卡根挂 `NavigationRegion3D`，把静态地面/障碍放进去后 Bake（编辑器按钮或
`bake_navigation_mesh()`）。敌人：

```gdscript
# CharacterBody3D + NavigationAgent3D
@onready var agent: NavigationAgent3D = $NavigationAgent3D

func _physics_process(delta: float) -> void:
    agent.target_position = player.global_position       # 加 Timer 每 0.2s 更新更省
    if not agent.is_navigation_finished():
        var next := agent.get_next_path_position()
        var dir := (next - global_position).normalized()
        velocity.x = dir.x * SPEED
        velocity.z = dir.z * SPEED
    if not is_on_floor():
        velocity += get_gravity() * delta
    move_and_slide()
```

行为分层：巡逻（导航到路径点）→ 发现（到玩家距离 + 视线 RayCast3D）→ 追击 →
攻击（Area3D hitbox），一个 `enum` 状态机足够。

## 8. HUD 与游戏流程

3D 场景之上叠 `CanvasLayer`：准星（居中 TextureRect）、血条
（TextureProgressBar）、拾取提示。流程同 2D：
`get_tree().change_scene_to_file()` 切主菜单/关卡/结算；暂停时记得把
`Input.mouse_mode` 还原成 VISIBLE。

## 9. 验证闭环（agent 自测）

```bash
# 1. 导入 + 解析检查（改完必跑；新增 glb 后尤其要跑，看有无导入失败）
godot --headless --path . --import 2>&1 | grep -iE "error|SCRIPT ERROR" || echo IMPORT_OK

# 2. 无头跑 120 帧抓运行时报错
godot --headless --path . --quit-after 120 2>&1 | grep -iE "error" || echo RUN_OK

# 3. 视觉验收：带窗口跑几秒 + 自动截图（无头不渲染）
godot --path . --quit-after 240
```

截图 autoload 与 2D 相同（`get_viewport().get_texture().get_image().save_png(...)`，
定时存 3 张）。3D 重点检查：画面是否全黑（灯/环境）、模型是否显示（.gltf 静默
失败、scale 过大过小）、材质是否发紫（贴图丢失）、角色是否穿地（碰撞没生成）。

## 10. 性能

按收益排序：阴影灯数量与 shadow 分辨率 > 重复物件改 MultiMeshInstance3D >
`Camera3D.far` 别默认 4000 米 > 大关卡加 `OccluderInstance3D`（遮挡剔除）>
网格 LOD（导入时自动生成，确认没关）。目标平台弱（网页/手机）就直接换
Mobile / Compatibility 渲染器，比逐项抠更有效。

## 11. 导出

```bash
godot --headless --install-export-templates   # 首次
godot --headless --path . --export-release "macOS" build/mac/MyGame.zip
godot --headless --path . --export-release "Windows Desktop" build/win/MyGame.exe
# 网页导出需 gl_compatibility 渲染器；3D 网页包体大，桌面端是 3D 的主发布目标
```

## 12. 常见坑

- 画面全黑/死白 → 没灯、没 Environment，或 HDRI 曝光没调（Environment 里调
  background energy / tonemap exposure）。
- `.gltf` 静默导入失败 → 换 `.glb`，或换资产；`load()` 返回 null 必查此项。
- 模型尺度错 → 别在 Godot 里手动缩放刚体（物理会出鬼畜），在导入设置里改
  scale 或用正确尺度的资产。
- 鼠标视角上下颠倒/过快 → `relative` 符号与灵敏度；忘了 clamp pitch 会翻筋斗。
- 敌人穿墙 → 导航网格没重 Bake（改了关卡要重烘焙），或 agent radius 与
  碰撞体不匹配。
- 影子全糊 → DirectionalLight3D 的 shadow max distance 太大，拉小到玩家
  视距（如 50m）立刻清晰。
