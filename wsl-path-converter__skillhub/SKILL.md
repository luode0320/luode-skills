---
name: wsl-path-converter
description: 当需要在 WSL 与 Windows 之间转换路径格式时使用（如把 C:\xxx 转成 /mnt/c/xxx 或反向）。触发词：路径转换 / wslpath / path convert / 转换路径 / WSL路径。使用 WSL 内置 wslpath 三模式（-u/-w/-m）提供可执行命令、4 步工作流与实测失败回退表。
license: MIT
metadata:
  author: OpenClaw Assistant
  version: "1.1.0"
  displayName: WSL 路径转换
---

# WSL 路径转换（wsl-path-converter）

## 一、定位与适用边界

本 skill 解决 WSL 与 Windows 之间的路径格式互转。核心事实源是 **WSL 内置 `wslpath` 命令**——不需要任何脚本或第三方工具。

适用场景：
- 把 Windows 路径（`D:\app\scripts`）转成 WSL 可访问路径（`/mnt/d/app/scripts`）
- 把 WSL 路径（`/mnt/c/...`）转成 Windows 工具可识别的路径（`C:\...` 或 `C:/...`）
- 在 shell 命令、脚本参数、配置文件间传递路径前做格式归一

不适用：批量多路径转换或需要与 `win-copy` 等命令联动时，应改用 `wsl-windows-bridge__skillhub` 的 `win-path` 脚本封装（见「五、交叉引用」）。

## 二、核心命令：wslpath 三模式

| 模式 | 命令 | 方向 | 示例 | 实测输出 |
|---|---|---|---|---|
| Unix | `wslpath -u '<WIN路径>'` | Windows → WSL | `wslpath -u 'D:\app\scripts'` | `/mnt/d/app/scripts` |
| Windows | `wslpath -w '<WSL路径>'` | WSL → Windows | `wslpath -w /mnt/d/app/scripts` | `D:\app\scripts` |
| Mixed | `wslpath -m '<WSL路径>'` | WSL → Windows（正斜杠分隔） | `wslpath -m /mnt/d/app/scripts` | `D:/app/scripts` |

注意事项：
- 路径含空格时必须加引号（实测 `/mnt/c/Program Files/App` → `C:\Program Files\App` 正常）。
- 相对路径会自动基于当前工作目录解析（实测在 `/mnt/d` 下 `wslpath -w .` → `D:\`）。

## 三、工作流（4 步）

1. **识别路径方向**：判断输入是 Windows 格式（盘符 `X:\` 或 UNC `\\` 开头）还是 WSL 格式（`/mnt/` 或 `/` 开头）。不确定时同时执行 `-u` 与 `-w` 看哪个输出合理，禁止猜测。
2. **选择模式**：Windows → WSL 用 `-u`；WSL → Windows 用 `-w`（反斜杠分隔）或 `-m`（正斜杠分隔，适合 JSON/URL/脚本参数）。
3. **执行命令**：`wslpath -u '<路径>'`（或 `-w`/`-m`），含空格路径务必加引号。
4. **验证输出**：核对转换结果是否仍指向原位置——WSL 路径应可 `ls`/`test -e` 通过，Windows 路径应 `test -f` 或在资源管理器中可达；失败则查下表。

## 四、失败回退表（实测证据 2026-08-25）

| 症状 | 根因 | 处理 |
|---|---|---|
| 无效盘符（如 `Z:\no\such\dir`） | 该盘符不存在或未挂载 | 输出 `wslpath: <路径>` 且 exit 1——**原样保留输入**，不要编造转换结果；提示用户确认盘符 |
| UNC 路径（`\\server\share\dir`） | wslpath 对 UNC 处理不可靠：两次实测输出不同（一次丢失前导 `\\` 输出 `server/share/dir`，一次错误挂载到 `/mnt/d/` 下） | 不依赖 wslpath 转换 UNC；需要时手工保留前缀并只转盘符部分 |
| 路径含空格转换结果异常 | 未加引号导致 shell 分词 | 全程对路径参数加引号重试 |
| 相对路径输出不符合预期 | 基于当前 cwd 解析 | 先 `cd` 到目标目录或用绝对路径 |
| `wslpath: command not found` | 极旧 WSL 发行版无此工具 | 检查 `wsl --update` 或改用 `win-path`（bridge 脚本封装） |

## 五、交叉引用（引用不复制）

- **`wsl-windows-bridge__skillhub` 的 `win-path`**：需要批量多路径转换、与 `win-copy`/`win-open` 联动的脚本化场景时指回；`win-path` 是 `wslpath` 的薄封装（`-w` 默认 / `-u` 反向 / 失败回退原样），本 skill 只负责内置 `wslpath` 的决策。
- **`wsl-powershell__skillhub` 的 `psctl.sh`**：该脚本内部 `process_wsl_paths()` 含反方向（WSL → Windows）sed 转换；在 PowerShell 调用链中处理路径时指回，不重复实现。

## 六、安全与边界

- 只做路径格式转换，**不访问、不修改、不删除任何文件**——转换后的路径是否可用由调用方自行验证。
- 不修改用户 shell 配置、不写入任何全局状态；`wslpath` 为只读命令，无副作用。
- 本 skill 只给命令与决策，不自动执行转换后的文件操作。
