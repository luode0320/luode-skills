# 路径映射规则

代码留在 Windows 目录，执行 Go 命令时换算为 WSL 自动挂载路径 `/mnt/<drive>/...`。WSL 启动时自动挂载 Windows 盘符，**无需 bind mount 或手动挂载**。

## 映射表

| Windows 路径 | WSL 路径（执行时使用） |
|-------------|----------------------|
| `D:\luode\<project>` | `/mnt/d/luode/<project>` |
| `D:\luode\ellipal_admin` | `/mnt/d/luode/ellipal_admin` |
| `C:\Users\luode\Documents\...\w-m` | `/mnt/c/Users/luode/Documents/.../w-m` |

## 换算步骤

1. 取出盘符并转小写（`D` → `d`）
2. 去掉 `:`
3. 将 `\` 替换为 `/`
4. 前缀 `/mnt/`

示例：`D:\luode\project` → `/mnt/d/luode/project`

## 注意事项

- 不要把 Windows 路径（`D:\...`）直接传给 WSL 内部命令；`wsl.exe --cd` 后必须是 `/mnt/<drive>/...` 格式。
- 如果路径中包含空格，整体放进引号。
- 如果路径位于 `\\wsl$\<distro>\...`（代码本身在 WSL 内部），直接使用对应 Linux 原生路径，不走 `/mnt` 换算。
- `/mnt/<drive>` 由 WSL 启动时自动挂载，通常无需任何手动操作。
