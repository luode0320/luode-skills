# 路径映射规则

## 基本映射

- `C:\Users\name\project` -> `/mnt/c/Users/name/project`
- `D:\work\repo` -> `/mnt/d/work/repo`
- `F:\code\app` -> `/mnt/f/code/app`

## 转换步骤

1. 读取 Windows 绝对路径。
2. 取出盘符并转小写。
3. 去掉 `:`。
4. 将剩余 `\` 替换为 `/`。
5. 拼成 `/mnt/<drive-letter>/<rest-of-path>`。

## 注意事项

- 如果路径中包含空格，进入 `bash -lc` 时要整体放进单引号。
- 如果路径位于 `\\wsl$\<distro>\...`，不要再按 `/mnt/<drive>` 转换，应直接使用对应 Linux 原生路径。
- 如果仓库是 Windows 路径，但命令依赖 Linux 侧相对路径、符号链接、可执行位或大小写敏感行为，仍应在 WSL 中执行。
