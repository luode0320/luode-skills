# Godot MCP 编辑器操作方法论（吸收自 godot-mcp 插件）

> 归属 owner：`godot-project-bootstrap-rules`。本文件是 Godot 项目就绪后"通过 MCP 操作编辑器"的方法论补充，不产生独立自动触发入口。吸收来源：`codebuddy-plugins-official/godot-mcp`（anengyuki/Godot-mcp，MIT，市场缓存只读路径 `plugins/marketplaces/codebuddy-plugins-official/plugins/godot-mcp/`）。吸收原则：只吸收方法论（三场景分流、目录契约、声明式场景构建、部署/调试流程），**不复制插件本体代码**（MCP server / addons GDScript 属于安装资产，由 `mcp-installation-rules` 与项目配置补齐，本文件只定义如何使用）。

## 适用场景

- Godot 项目已就绪（`godot-project-bootstrap-rules` 完成自举）、MCP 已注册，用户开始用自然语言做游戏/改场景/写脚本。
- 用户说"做一个 X 游戏 / 加个玩法 / 改个节点 / 场景怎么调 / 报错了 / 部署 MCP"。
- 编辑器操作前先确认：MCP 已注册、`${WORKSPACE}/godot-editor/` 存在、9080 端口监听中；未就绪先走部署流程（见下文"部署 5 步"）。

## 一、三场景分流（首次激活必做）

每次激活先做**环境探测**（4 个标志位，一次性收集，不反问用户）：

| 标志 | 判定 |
|------|------|
| `hasActiveGame` | `${WORKSPACE}/active-game.json` 是否存在 |
| `hasProject` | active 游戏目录（或 fallback 子目录）下是否有 `project.godot` |
| `hasEditor` | `${WORKSPACE}/godot-editor/` 下是否有 `Godot_v*.exe` |
| `editorListening` | 9080 端口是否监听（Godot 插件是否启用） |

按优先级分流（禁止反问"你是新建还是修改"）：

1. `hasProject == false` → **场景 1 = make_game**：先部署环境（godot-editor + MCP 注册），再创建项目。
2. `hasProject == true` 且用户说"再来一个/新游戏/再做一个/换一个游戏" → **场景 2 = new_game**：仅新建另一个游戏（复用编辑器，不重部署）。
3. 其他（加/改/删/优化 + 节点/场景/脚本/UI/角色/敌人/关卡/菜单） → **场景 3 = modify_game**：修改当前游戏内容。

## 二、工作区目录契约（强制）

```
${WORKSPACE}/
├── godot-editor/          ← 编辑器二进制（由部署流程下载，不嵌套在 game 里）
├── active-game.json       ← 全局唯一"当前操作游戏目录"标记（新建/切换时写入）
├── game1/  game2/  ...    ← 每个游戏是 ${WORKSPACE} 的一级子目录，平铺
```

- `active-game.json` 字段：`gameDir`（绝对路径）、`projectName`、`template`、`createdAt`、`pluginVersion`。
- 严禁：项目嵌套在 `godot-editor/` 内、工作区根写除 `<projectName>/` 与 `active-game.json` 之外的资产、跨 game 目录读写。
- 没有 `active-game.json` 时禁止手写 `project.godot`；先走 make_game 创建。

## 三、场景修改：build_godot_scene 声明式调用（场景 3 唯一允许）

- 把用户需求**一次性**翻译成完整的声明式 root 树，**调用一次** `build_godot_scene`；禁止多次原子调用、禁止手写 `.tscn`。

```
build_godot_scene({
  scenePath: "res://scenes/<场景名>.tscn",
  root: {
    name: "<根节点名>",
    type: "<Godot 节点类型>",       // Node2D / CharacterBody2D / Control / Camera2D
    properties: { ... },            // Vector2 用 [x,y]；Color 用 [r,g,b,a] (0-1)；rotation 用弧度
    script: { path: "res://scripts/<x>.gd", content: "<完整 GDScript>" },
    children: [ ... ]               // 递归，每个子节点同构
  },
  saveAfter: true, openInEditor: true
})
```

- 返回的 report **原样展示**给用户，不复述、不总结。
- 独立 GDScript（autoload / 工具脚本，不挂节点）：直接用 Write/Edit 写 `${gameDir}/scripts/...`。
- 策划案/表格/Markdown：写 `${gameDir}/docs/`、`${gameDir}/data/`；图片/模型/音频：拷贝到 `${gameDir}/assets/...`（编辑器自动 reimport）。

## 四、Godot 4 路径与类型约定

| 类型 | 格式 | 示例 |
|------|------|------|
| 资源路径 | `res://...` | `res://scenes/main.tscn` |
| 节点类型 | Godot 4 类名 | `Node2D` / `CharacterBody2D` / `Control` / `Camera2D` |
| 脚本扩展名 | `.gd` | `res://scripts/player.gd` |
| 场景扩展名 | `.tscn`（文本格式） | `res://scenes/main.tscn` |
| Vector2 / Vector3 | 数组 | `[100, 200]` / `[1, 2, 3]` |
| Color | RGBA 数组 0–1 | `[1, 0.5, 0.5, 1]` |
| 旋转单位 | 弧度（radians） | `1.5708` |

## 五、部署 5 步（场景 1 或 MCP 连不上时）

按顺序执行，每步真实跑命令并贴回输出：

1. **Node.js >= 18 检查**：`node --version`；未装或 <18 → 让用户安装 18 LTS+，不继续。
2. **构建 MCP Server**：`server/dist/index.js` 不存在则 `npm install + npm run build`。
3. **`.mcp.json` 注册校验**：确认 godot-mcp 配置已写入 MCP 配置；未注册按 `mcp-installation-rules` 补齐。
4. **下载 godot-editor** 到 `${WORKSPACE}/godot-editor/`。
5. **9080 端口探测**：未监听通常是正常的（还没有项目被编辑器打开），创建项目后引导用户用编辑器打开并启用插件。

## 六、Debug 三工具（用户报告报错/崩溃/编译失败时）

- 只允许调用三个 MCP 单元查询工具：`get_debug_errors` / `get_script_errors` / `get_editor_output`。
- `script_path` 始终用 `res://` 形式（指向 `active-game.json` 的 `gameDir`），不写绝对路径、不跨 game 读写。
- 错误扫描、行号定位、上下文提取由 MCP 单元工具完成；本文件只负责调用 + 美化展示 + 引导。
- 修复后让用户重新触发开发流程，不做"自动 run → 自动 debug"循环（本 MCP 无 run_project）。

## 七、严禁行为

- 不调用 `build_godot_scene` + 三个 debug 工具之外的任何 MCP 工具（旧 `godot_deploy` / `godot_dev_router` / `operate_node` / `operate_scene` / `operate_script` / `run_project` 等已移除）。
- 不做多次原子调用改场景；必须一次 `build_godot_scene` 传完整树。
- 不反问用户"你是新建还是修改"；按三场景优先级直接判定。
- 不把 godot-editor 或 game 目录放到 `${WORKSPACE}` 之外或嵌套位置。
- 不在没有 `active-game.json` 时手写 `project.godot`。
- 不做"自动 run_project → 自动再 debug"循环。
- 不改 `${WORKSPACE}/godot-editor/`（那是部署流程的领地）。

## 与本地规则的边界

- 插件安装、MCP 注册来源分析：`mcp-installation-rules`；本文件只定义注册后的操作方式。
- 项目自举（规则文件、图像配置模板）：`godot-project-bootstrap-rules` 主文件；本文件是"就绪后如何操作"的补充。
- 素材生产（2D 游戏素材）：`game-asset-design-gate-rules` / `game-asset-production-handoff-rules` / `character-sprite-animation-production`；本文件不替代图像与动画生产流程。
- 编辑器二进制下载位置、MCP server 构建：由部署流程与项目配置决定，本文件只引用不复制命令细节。
