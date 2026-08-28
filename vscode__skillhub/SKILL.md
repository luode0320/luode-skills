---
name: "vscode"
description: "VS Code 常见故障诊断与配置修复：格式化/保存不生效、调试器无法启动、launch.json 配置、扩展崩溃失效、终端 shell 不对、环境变量缺失、远程开发（SSH/DevContainer/WSL）连接失败、智能提示不工作、设置冲突、工作区信任。适用于 VS Code 行为异常排查与配置场景。触发词：vscode、vs code、vscode 报错、格式化不生效、format on save、prettier 冲突、debugger、launch.json、断点无效、扩展崩溃、插件不生效、终端 shell、环境变量找不到、remote ssh、devcontainer、wsl 扩展、智能提示不工作、intellisense、settings.json、工作区信任。"
license: MIT
metadata:
  displayName: "VS Code 故障诊断与配置"
  version: "1.1.0"
  author: "Clawhub Developer"
---

# VS Code 故障诊断与配置

面向 VS Code 日常故障的**症状驱动诊断手册**：先按症状定位到对应流程，再按「排查 → 修复 → 验证」三步闭环。原版速查知识点已重组为 8 个诊断流程，每个流程自带验证检查点，避免"改了设置但不确定是否生效"。

## 使用流程

1. **定位症状类别**：在下方「症状速查表」找到当前现象对应的章节号。
2. **按流程排查**：进入对应章节，按「排查 → 修复 → 验证」顺序执行，**每步验证通过才进入下一步**。
3. **验证修复**：执行各章节末尾的验证命令/操作，确认现象消失。
4. **收尾**：重启 VS Code（`Cmd/Ctrl+Shift+P` → `Developer: Reload Window`）后复测一次，确认无回归。

## 症状速查表

| 现象 | 章节 | 最常见根因 |
|---|---|---|
| 保存后没有自动格式化 / 格式化成别家风格 | [§1 格式化冲突](#1-格式化与保存不生效) | `defaultFormatter` 未显式指定 |
| 按 F5 无反应 / 报错 / 断点不命中 | [§2 调试器无法启动](#2-调试器无法启动) | `launch.json` 缺失或 `program` 路径错 |
| 扩展装了一堆后 VS Code 崩溃 | [§3 扩展崩溃与失效](#3-扩展崩溃与失效) | 扩展间冲突 |
| 新终端打开是错的 shell / 环境变量缺失 | [§4 终端 shell 与环境变量](#4-终端-shell-与环境变量) | `defaultProfile` 未设置 |
| 远程连不上 / WSL 里扩展不生效 | [§5 远程开发连接问题](#5-远程开发连接问题) | SSH Host 不匹配 / 扩展未装到远端 |
| 代码没提示 / 报"无法加载模块" | [§6 智能提示与语言服务](#6-智能提示与语言服务) | TS Server 卡死 |
| 改了 settings.json 没效果 | [§7 设置不生效](#7-设置不生效) | 设置优先级被覆盖 |
| 功能被禁用 / 打开项目提示受限 | [§8 工作区信任](#8-工作区信任) | Restricted Mode |

---

## 1. 格式化与保存不生效

**排查**
1. 确认是否多个格式化器并存：`Cmd/Ctrl+Shift+P` → `Format Document` 右键菜单看"Format Document With…"列出几家。
2. 检查 `editor.formatOnSave` 是否被 workspace 设置覆盖（见 §7 优先级）。
3. 检查是否同时装 Prettier 与 ESLint 且都配置了格式化。

**修复**
- 同语言只留一个格式化器：在 settings.json 显式声明
  ```json
  "[javascript]": { "editor.defaultFormatter": "esbenp.prettier-vscode" },
  "editor.formatOnSave": true
  ```
- ESLint 项目若 Prettier 与其冲突，禁用其一：`"prettier.enable": false`。
- `.editorconfig` 会覆盖部分编辑器设置——若改设置无效，检查项目根 `.editorconfig`。

**验证**：修改代码 → 保存 → 确认格式按预期变化；`Format Document` 右键菜单确认当前默认格式化器已唯一。

## 2. 调试器无法启动

**排查**
1. 没有 `launch.json`：`Cmd/Ctrl+Shift+P` → `Debug: Open launch.json`，或运行视图点"create a launch.json file"。
2. 检查 `"program"` 路径：必须用绝对工作区变量 `"${workspaceFolder}/src/index.js"`，不要用相对 `launch.json` 所在目录的路径。
3. Node 项目踩进 node_modules：配置 `"skipFiles": ["${workspaceFolder}/node_modules/**"]`。
4. 多进程/前后端同调：确认是否配置了 `"compounds"`。

**修复**
```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "type": "node",
      "request": "launch",
      "name": "Launch Program",
      "program": "${workspaceFolder}/src/index.js",
      "cwd": "${workspaceFolder}",
      "skipFiles": ["${workspaceFolder}/node_modules/**"]
    }
  ]
}
```
- `"cwd"` 相对**工作区根**，不是 launch.json 所在目录。

**验证**：F5 启动后第一行可执行代码处断点命中；Step Over 不会进入 node_modules。

## 3. 扩展崩溃与失效

**排查**
1. 崩溃发生在装某个扩展之后 → 优先怀疑新装扩展。
2. 查看 `Output` 面板（下拉选 `Extension Host`）找崩溃堆栈。
3. 检查键位/功能冲突：`Cmd/Ctrl+K Cmd/Ctrl+S` 看按键绑定是否有重复来源。

**修复**
- 停用最近安装的扩展 → 逐个启用定位冲突源：`扩展面板` → 右键 `Disable`。
- 报 "Cannot find module"：**完整退出 VS Code 重开**（不是 Reload Window），再不行重装该扩展。
- 扩展设置不生效：检查是否有 workspace 级设置覆盖（§7）。

**验证**：启用扩展后操作其核心功能一次（如格式化/跳转）；`Developer: Reload Window` 后扩展仍正常加载。

## 4. 终端 shell 与环境变量

**排查**
1. 新终端打开后 shell 不对 → 检查 `terminal.integrated.defaultProfile.windows/linux/osx`。
2. 终端里找不到刚安装的命令 → 环境变量问题：VS Code 终端继承**启动方式**的环境，不重新读 `.bashrc`。
3. Shell 集成行为异常（提示符错乱）→ 检查 `terminal.integrated.shellIntegration.enabled`。

**修复**
```json
"terminal.integrated.defaultProfile.windows": "Git Bash",
"terminal.integrated.defaultProfile.linux": "bash"
```
- 安装新工具后终端不识别：**重启 VS Code**（不是只开新终端）。
- Shell 集成异常时降级：`"terminal.integrated.shellIntegration.enabled": false`。

**验证**：新开终端显示预期 shell；`echo $PATH` / `where <cmd>` 能命中刚安装的工具。

## 5. 远程开发连接问题

**排查**
1. SSH 连不上：确认 `~/.ssh/config` 的 `Host` 名与连接目标一致；自定义配置路径时检查 `"remote.SSH.configFile"`。
2. 容器不识别：确认仓库根有 `.devcontainer/devcontainer.json`（不会自动根据 Dockerfile 生成）。
3. WSL 里扩展不生效：WSL 远端扩展**独立安装**，本机装的不自动同步。

**修复**
- SSH：在 `~/.ssh/config` 里把 `Host` 写成 VS Code 连接时输入的名字，或设置
  `"remote.SSH.configFile": "/path/to/custom_config"`。
- 容器：确保 `devcontainer.json` 存在且 `docker` 守护进程运行，然后 `Remote-Containers: Reopen in Container`。
- WSL：远端 `扩展面板` → 确认扩展标有 `WSL` 标签（本地/远程双装）。

**验证**：`Remote-SSH: Connect to Host` 成功登录；`Ports` 面板能看到自动转发的端口；WSL 远端扩展列表非空。

## 6. 智能提示与语言服务

**排查**
1. IntelliSense 无反应：`Output` 面板下拉选对应语言服务，看是否报错/未启动。
2. TypeScript 项目报"无法加载模块"或提示陈旧：TS Server 状态卡死。

**修复**
- 重启语言服务：`Cmd/Ctrl+Shift+P` → `TypeScript: Restart TS Server`。
- 语言服务彻底损坏：`Developer: Reload Window`，仍不行则删除工作区 `.vscode` 外的缓存（`%APPDATA%/Code/Cache` 等，先备份）。

**验证**：输入 `.` 出现补全列表；ts 报错消失且与 `tsc` 输出一致。

## 7. 设置不生效

**排查**——先确认设置优先级：
1. 用户级 → 工作区级（`.vscode/settings.json`）→ 文件夹级（多根工作区）→ 后声明覆盖先声明。
2. 检查当前生效值：`Cmd/Ctrl+Shift+P` → `Preferences: Open Settings (UI)` → 看该项是否显示"Workspace"来源（表示被覆盖）。
3. 部分设置仅用户级生效（如 `terminal.integrated.shell*` 系列）。

**修复**
- 被覆盖则把改动写进**工作区级** `.vscode/settings.json`（改错层级是"改了没用"最常见原因）。
- 多根工作区：各文件夹有各自设置，需逐文件夹改或用根 `.code-workspace` 的 `settings` 段。
- 保存失败：检查 settings.json 文件权限（只读会静默丢弃改动）。

**验证**：在 Settings UI 搜索该项，来源列显示预期层级；重开窗口后行为仍符合预期。

## 8. 工作区信任

**排查**
1. 状态栏显示 "Restricted Mode"：功能被裁剪（调试、任务、部分扩展禁用）。
2. 打开未知来源文件夹首次弹信任提示时选了"否"或忽略。

**修复**
- 当前文件夹：状态栏 `Restricted Mode` → `Manage Workspace Trust` → `Trust`。
- 多根工作区可只信任部分文件夹（`Workspace Trust` 面板逐项勾选）。

**验证**：状态栏不再显示 Restricted Mode；调试按钮恢复可用。

---

## 适用边界

**何时用**：VS Code 出现上述 8 类症状、需要按步骤排查；配置调试/格式化/远程开发环境。

**何时不用**：
- 需要深入代码级调试方案 → 转 `vscode-fullstack-debug`（全栈调试专精）；
- WSL 专属环境/路径问题 → 转 `wsl-windows-bridge__skillhub`、`wsl-chrome-cdp__skillhub`；
- 前端框架本身的构建/配置问题 → 转 `vue__skillhub`、`frontend-component-rules`；
- 终端脚本语义问题（非 VS Code 配置）→ 转 `bash__skillhub`、`shell__skillhub`。

## 验收清单

- [ ] 已按「症状速查表」定位到正确章节
- [ ] 每步修改后执行了该章节的**验证**操作
- [ ] 修改的是正确层级的 settings.json（用户/工作区/文件夹）
- [ ] 涉及扩展/终端环境的改动，已 `Developer: Reload Window` 或完整重启复测
- [ ] 修复后无回归：相关功能（格式化/调试/提示）至少各触发一次

## 快速参考（速查）

| 主题 | 关键点 |
|---|---|
| 设置优先级 | User → Workspace → Folder，后者覆盖前者；`.code-workspace` 管多根 |
| 格式化 | 每语言显式 `editor.defaultFormatter`；Prettier/ESLint 二选一 |
| 调试 | `launch.json` 必须存在；`program` 用 `${workspaceFolder}`；`skipFiles` 跳 node_modules |
| 扩展 | 崩溃逐个启停定位；"Cannot find module" 需完整重启 |
| 终端 | `defaultProfile.*` 指定 shell；新装工具需重启 VS Code |
| 远程 | SSH Host 名必须匹配；容器需 `devcontainer.json`；WSL 扩展远程独立装 |
| 信任 | Restricted Mode 下调试/任务/扩展被禁用，需 Trust |
| 语言服务 | `TypeScript: Restart TS Server` 解决提示陈旧 |
