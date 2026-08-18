---
name: gdrive-junction-mount
description: >-
  Windows 下把本地目录通过 NTFS junction 挂载到谷歌云盘同步目录的完整流程。
  当用户要在 Windows 上把某个目录（博客、知识库、记忆、项目数据等）移动到
  D:\谷歌云盘\ 下，或把原路径改成挂载到云盘、把已挂载的目录重新挂载到另一个
  云盘目录、更新挂载目标时触发。核心思路：真实数据迁到云盘目录，原路径建
  junction 指向它，谷歌云盘客户端自动同步，无需写同步脚本。也覆盖回滚、
  完整性校验、中文路径坑（cmd mklink 中文乱码、PowerShell 原生支持）和
  占用排查。当用户提到"挂载到谷歌云盘""目录放到云盘同步""用 junction 挂
  载""云盘目录挂载""把 X 挂到云盘"时使用。
---

# 谷歌云盘目录挂载（NTFS Junction）

## 目的与适用范围

在 Windows 上，让某本地目录的真实数据落在 `D:\谷歌云盘\` 下（由谷歌云盘客户端自动同步到云端 / 其他电脑），同时保持原路径可用。做法是**真实数据迁入云盘目录，原路径建 junction 指向它**。

- 适用于：博客、知识库、项目数据、zcode 记忆（`C:\Users\luode\.zcode\cli\memories`）等任意目录。
- 前提：目标盘（D / F 等）为 NTFS 文件系统（junction 仅 NTFS 支持）；谷歌云盘客户端 `GoogleDriveFS.exe` 已运行。
- 不需要管理员权限：NTFS junction（目录联接）是用户级能力，普通用户即可创建。
- 关键事实：zcode 记忆路径 `C:\Users\luode\.zcode\cli\memories` 在应用里**硬编码**、无法通过配置改路径，所以 junction 是唯一干净的挂载方式。skills 目录（`C:\Users\luode\.zcode\skills`）此前也已用 junction 挂载到 `F:\luode-skills`。

## 核心概念与方向（为什么）

- **junction 是本地文件系统层面的重定向**，不是网络 / 云盘同步工具。它只让"通过原路径的读写"落到目标目录，**不会**把更新实时推送到另一个物理盘。
- 正确的挂载方向只有一种：**真实数据放云盘同步目录，原路径作为入口指向它**（`原路径 → 云盘目录`）。反向（云盘入口指向本地真实数据）会让谷歌云盘客户端同步一个空的链接，换机即断。
- 不要在 junction 之间做**链式**挂载（A→B→C）：中间层一旦消失整条链断且极难排查。数据在哪个盘的云盘同步目录，就一级指向它。
- 云盘客户端是**单向备份语义**（本地→云端）;若要多台电脑双向编辑同一份数据，junction 指向云端同步目录仍是最优解（各机指同一份），但换机需要在新机重建 junction。

## 前置检查（每轮必做）

1. 盘符文件系统确认：`cmd /c "wmic logicaldisk where deviceid='<盘>:' get filesystem"`，必须为 `NTFS`。
2. 目标云盘目录是否存在：`ls "D:/谷歌云盘/<dir>"`。
   - 已存在 → 先核对内容是否就是要挂载的数据（可能是上次挂载残留或旧副本）。
   - 不存在 → 用 PowerShell 创建。
3. 源目录身份确认：`powershell -NoProfile -Command "Get-Item '<源路径>' | Select Name,LinkType,Target | Format-List"`。
   - `LinkType` 为空 = 真实目录；`LinkType=Junction` = 已是链接（先看清指向，避免链式或反向）。
4. 确认无进程占用源目录：关闭打开它的 VS Code / 终端 / 资源管理器窗口，确认无 dev server / 编辑器进程占用（否则改名会报"访问被拒绝"）。

## 首次挂载流程

> **顺序铁律：先让数据在云盘就位（第 1、2 步），再切换原路径（第 3 步）。** 反过来"先改名 → 再建链"，一旦 Target 不存在就会卡在中间状态：源已改名成 `.bak`、junction 又没建成。`New-Item` 的 `-Target` 必须**已存在**（不会自动创建），所以顺序只能是：建目录/拷数据 → 校验 → 改名 → 建链。

目标：把真实目录 `X:\src` 迁到 `D:\谷歌云盘\dst`，`X:\src` 变成 junction 指向它。

### 第 0 步：确认方向与现状

确认 `D:\谷歌云盘\dst` 尚不存在或为空，`X:\src` 是真实目录（LinkType 为空）。若 `D:\谷歌云盘\dst` 已存在且是 junction，先删除该链接（`cmd /c rmdir "D:\谷歌云盘\dst"`，只删链接不动数据）；若已存在真实数据，核对它是否是想要的数据，避免覆盖。

### 第 1 步：复制数据到云盘（完整性保留）

> 不要用 `cp -r` 或 PowerShell `Copy-Item -Recurse` 复制大型目录：`Copy-Item` 在目标有同名文件占位时会报"无法将容器复制到现有叶项"。用 robocopy，保留 ACL / 时间戳 / 隐藏文件，多线程加速：

```bash
cmd //c "robocopy <X:\src> <D:\谷歌云盘\dst> /E /COPY:DAT /DCOPY:DAT /R:2 /W:1 /MT:16 /NFL /NDL /NJH /NP"
```

- 退出码 0–7 均为成功（0=无变化，1=有复制，…）。
- 若报错 `错误 123 访问源目录 <当前目录>"<源>"`，是 Git Bash 给 `cmd //c` 传中文/带引号路径时注入了当前目录前缀的转义问题，改用 PowerShell 传参或把路径写成不含引号的直连形式。

### 第 2 步：完整性校验（迁移前必做，缺一不可）

```bash
# 文件数与总字节（du 对稀疏文件统计口径可能不同，以文件数 + robocopy 校验为准）
echo "源文件数: $(find "<X:\src>" -type f | wc -l)"
echo "目标文件数: $(find "<D:\谷歌云盘\dst>" -type f | wc -l)"

# robocopy 校验模式（/L 只列出差异；/XD 排除 .git 时 git 仓库需单独核对 .git）
cmd //c "robocopy <X:\src> <D:\谷歌云盘\dst> /L /E /COPY:DAT /R:0 /W:0 /NFL /NDL /NJH /NP"
# 应看到：复制 0 / 不匹配 0 / 失败 0

# 若含 git 仓库，核对 .git 一致（对象数、字节）
# 源 git 仓库完整性：git -C <src> fsck --no-progress（dangling 对象是正常的）
```

文件数一致 + robocopy 显示 0 差异 = 迁移安全。

### 第 3 步：切换原路径为 junction

> **必须使用 PowerShell，不要用 `cmd mklink`**：`cmd mklink` 遇到中文路径（如"谷歌云盘"）会报"文件名、目录名或卷标语法不正确"（编码转义问题）；PowerShell 原生支持中文路径。

```powershell
# 1) 源目录改名保留现场（若上一步失败"访问被拒绝"，是有进程占用，先排查关闭）
Rename-Item "<X:\src>" "<X:\src>.bak"

# 2) 建 junction：原路径 -> 云盘目录
New-Item -ItemType Junction -Path "<X:\src>" -Target "<D:\谷歌云盘\dst>"
# 若报"无法删除目录 X:\src，因为该目录不为空"：说明 Rename-Item 未生效（目录仍真实存在），
# 检查上一步是否被占用拦截，确认后再执行。

# 3) 验证
Get-Item "<X:\src>" | Select Name, LinkType, Target
# 应看到 LinkType=Junction, Target=<D:\谷歌云盘\dst>
```

### 第 4 步：验证通过 junction 读写

```bash
# 读取穿透
ls "<X:\src>/" && find "<X:\src>" -type f | wc -l   # 文件数与云盘一致

# 写入穿透（在云盘侧应能看到新增）
Set-Content "<X:\src>\_mount_test.txt" "ok"
ls "<D:\谷歌云盘\dst>/_mount_test.txt"              # 应存在
Remove-Item "<D:\谷歌云盘\dst>/_mount_test.txt"
```

## 更新挂载（重新指向另一个云盘目录）

目标：把已挂载的 `X:\src`（当前 junction → `D:\谷歌云盘\old`）改挂到 `D:\谷歌云盘\new`。

```powershell
# 1) 确认旧数据已安全（如需保留则先复制到 new，或确认 new 已有完整数据）
# 2) 删除旧 junction（只删链接，不删云盘数据）
cmd /c rmdir "<X:\src>"
# 3) 建新 junction 指向新目录
New-Item -ItemType Junction -Path "<X:\src>" -Target "<D:\谷歌云盘\new>"
# 4) 验证 + 写入穿透测试（同上）
Get-Item "<X:\src>" | Select Name, LinkType, Target
```

> 更新时若旧目录里已有数据需要迁到新目录，先在云盘内用 robocopy 从 `old` 复制到 `new`，再执行上面的重挂。`.bak` 现场只在首次迁移时保留；重挂不改名。

## 回滚（恢复为真实目录）

```powershell
cmd /c rmdir "<X:\src>"                      # 删 junction 链接（不删云盘数据）
Rename-Item "<X:\src>.bak" "<X:\src>"        # 恢复原真实目录（若保留过 .bak）
```

- junction 删除只移除链接本身，**云盘里的数据不删**，回滚不会丢数据。
- 若没保留 `.bak`，把云盘目录 `Move-Item` 回原路径即可：`Move-Item "<D:\谷歌云盘\dst>" "<X:\src>"`。

## 已落地实例（本机参考）

- `C:\Users\luode\.zcode\cli\memories`（junction）→ `D:\谷歌云盘\zcode-memories`：zcode 工作区记忆，按项目分区 `projects/<项目名>-<hash>/memory/*.md`。
- `C:\Users\luode\.zcode\skills`（junction）→ `F:\luode-skills`：用户级 skill 库（git 仓库）。
- 云盘根 `D:\谷歌云盘\` 下现有：`知识库/`（知识沉淀）、`zcode-memories/`（记忆）、`blog/` 等。

## 常见坑速查

| 症状 | 原因 | 处理 |
| --- | --- | --- |
| `cmd mklink` 报"文件名、目录名或卷标语法不正确" | 中文路径在 Git Bash→cmd 编码转义损坏 | 改用 PowerShell `New-Item -ItemType Junction` |
| `cmd //c robocopy` 报"错误 123 访问源目录 当前目录\"源\"" | 引号路径被注入当前目录前缀 | 去掉多余引号 / 用 PowerShell 传参 |
| `Copy-Item -Recurse` 报"无法将容器复制到现有叶项" | 目标存在同名文件占位 | 清空目标残留，改用 robocopy |
| 改名源目录报"访问被拒绝" | 有进程（编辑器 / dev server / 云盘）占用 | 关占用进程后重试 |
| junction 建后 `find` 报文件数 0 | Git Bash `find` 不穿透 junction 符号链接（`ls`/`cat` 正常） | 用 `ls` / PowerShell 验证，`find` 的 0 是误报 |
| 删除 junction 后残留文件级占位（Link count=2） | junction 删除后的占位 | 若与源一致可安全删除后重建 |
| `New-Item -ItemType Junction` 报 `Could not find item <目标>` | **Target 目录不存在**（junction 不会自动创建目标） | 先 `New-Item -ItemType Directory` 建目录，或先把数据 robocopy 到云盘再建链 |
| 改名成功但建链失败 → 源没了、目标也没有（中间状态） | 流程顺序错误：数据没先在云盘就位就切换了 | 数据没丢，在 `.bak` 里：先建云盘目录 + robocopy，校验后再建 junction，确认后删 `.bak`；带数据源自适应的脚本可直接续跑 |

## 边界与不负责事项

- junction 是本地重定向，不提供跨机实时双向同步；多机共享需各机装谷歌云盘客户端并各自建 junction 指向本地同步目录。
- 本 skill 只做挂载与回滚，不做云端数据托管 / 备份策略设计；`D:\谷歌云盘\` 的同步节奏由谷歌云盘客户端决定。
- 挂载目标必须是云盘客户端真正同步的目录（`D:\谷歌云盘\` 下），指向其它盘符目录的 junction 不会被同步。
