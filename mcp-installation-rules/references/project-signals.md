# 项目标记识别

## 前端项目常见标记

满足任一条即可视为“命中前端项目标记”，再结合仓库上下文判断是否为真实主项目：

- 存在 `package.json`、`pnpm-lock.yaml`、`yarn.lock`、`bun.lockb`
- 存在 `vite.config.*`、`next.config.*`、`nuxt.config.*`
- 存在 `src/`、`public/`、`pages/`、`app/` 等典型前端目录
- 存在 `.tsx`、`.jsx`、`.vue`、`.svelte`、`.html` 为主的页面或组件代码
- 需求明确要求“打开页面”“调试浏览器”“验证前端交互”“看网络请求”“抓性能数据”

## Godot 项目常见标记

满足任一条即可视为“命中 Godot 项目标记”，再结合仓库上下文判断是否为真实主项目：

- 存在 `project.godot`
- 存在 `.tscn`、`.scn`、`.tres`、`.res`、`.gd` 等 Godot 资源或脚本文件
- 存在 `addons/` 且内容明显为 Godot 插件
- 存在 `icon.svg`、`export_presets.cfg` 等 Godot 项目常见文件
- 需求明确要求“控制 Godot 编辑器”“创建场景”“操作节点”“运行 Godot 项目”“读取编辑器状态”

## 混合项目判定

- 若仓库同时包含前端与 Godot 标记，不冲突，默认两个 MCP 都需要准备。
- 若只有网页管理后台或游戏官网前端，不会削弱 Godot 标记；两者仍应分别接管各自工具面。
- 若仓库只是包含文档示例或少量静态文件，不能直接判定为真实前端项目。
