# Obsidian bridge 操作规则

Windows 和 WSL 均只调用公开 bridge；bridge 再调用官方 Windows Obsidian CLI。依据官方帮助文档，CLI 需要 Obsidian 1.12.7+ installer、设置中的 Command line interface，并依赖 Obsidian 应用运行。WSL 的 PATH 没有原生 `obsidian` 不构成阻断；只有 bridge doctor 无法恢复应用或无法锁定固定 vault 才阻断。

参考来源：https://obsidian.md/help/cli

## 必需前置

执行任何 vault 读写前，先完成 bridge doctor：

1. 运行 `python obsidian-knowledge-flow/scripts/obsidian_cli_bridge.py doctor --json`。
2. 断言响应的 `ok=true`、`vault_root=D:\obsidian_data`、非空 `vault_selector` 与 `verified=true`。
3. bridge 在 Windows 直接使用适配器，在 WSL 自动使用 Windows interop；调用方不得自行选择 shell、CLI 路径或 selector。
4. 应用不可达时，bridge 只隐藏启动一次、最长等待 15 秒并有限重试；不得杀死用户已有 Obsidian 进程，也不得无限重试。
5. 所有笔记 path 必须是 vault 相对路径、以 `知识库/` 开头，且不得包含 `..`、盘符、UNC 或 Windows 非法字符。

任何一项失败都视为 bridge 硬依赖不满足。不要回退到 `rg`、`Get-Content`、`Set-Content`、Python 或 Node 直接读写 vault Markdown 文件。

## Vault 定位

- 唯一 vault root 是 `D:\obsidian_data`；`知识库/` 只是 vault 内路径前缀，不是 vault selector。
- bridge adapter 通过官方注册列表查询动态唯一解析 selector；该查询只在 adapter 内部执行，调用方不传 vault 名称、不依赖 cwd，也不读取 listing 作为文件系统 fallback。
- 若固定根未注册、出现零个或多个匹配项，bridge 返回稳定 vault 错误并停止；不得改用嵌套 `D:\obsidian_data\知识库` 作为 vault root。

## 常用命令模板

以下命令由 bridge 统一处理 UTF-8、Windows/WSL transport、超时、应用恢复、selector 与读回验证。写入正文通过 UTF-8 文件传递；超过约 1800 字符时 adapter 自动分块并读回验证。

```bash
python obsidian-knowledge-flow/scripts/obsidian_cli_bridge.py doctor --json
python obsidian-knowledge-flow/scripts/obsidian_cli_bridge.py search --query "关键词" --limit 10 --json
python obsidian-knowledge-flow/scripts/obsidian_cli_bridge.py search-context --query "关键词" --limit 10 --json
python obsidian-knowledge-flow/scripts/obsidian_cli_bridge.py read --path "知识库/20-Knowledge/topic/note.md" --json
python obsidian-knowledge-flow/scripts/obsidian_cli_bridge.py create --path "知识库/10-Sessions/2026/07/session-title.md" --content-file "<UTF-8正文文件>" --json
python obsidian-knowledge-flow/scripts/obsidian_cli_bridge.py append --path "知识库/20-Knowledge/topic/note.md" --content-file "<UTF-8正文文件>" --json
python obsidian-knowledge-flow/scripts/obsidian_cli_bridge.py open --path "知识库/20-Knowledge/topic/note.md" --json
```

### 项目身份解析

`project-context` 是白名单内唯一不触达官方 CLI 的操作：它只把项目路径规范化成稳定的项目身份，用于笔记 frontmatter 的项目字段，不读写 vault。

```bash
python obsidian-knowledge-flow/scripts/obsidian_cli_bridge.py project-context --project-path "D:\luode\luode-skills" --json
```

### 迭代治理只读组

以下五个命令用于冲突巡检与处置前取证，全部只读。实测均接受 `path=`，与 `read`/`open` 只认 `file=` 的历史差异无关。

```bash
python obsidian-knowledge-flow/scripts/obsidian_cli_bridge.py property-read --path "知识库/20-Knowledge/topic/note.md" --name status --json
python obsidian-knowledge-flow/scripts/obsidian_cli_bridge.py properties --path "知识库/20-Knowledge/topic/note.md" --json
python obsidian-knowledge-flow/scripts/obsidian_cli_bridge.py backlinks --path "知识库/20-Knowledge/topic/note.md" --json
python obsidian-knowledge-flow/scripts/obsidian_cli_bridge.py files --folder "知识库/20-Knowledge" --json
python obsidian-knowledge-flow/scripts/obsidian_cli_bridge.py orphans --json
```

- `properties` 返回整篇 frontmatter 的 JSON，是读取 `status`、`title`、`superseded_by` 等字段的首选通道；逐个 `property-read` 在字段缺失时会返回 `Error: Property "<名>" not found.`，属于合法业务结果而非失败。
- `backlinks` 返回引用计数，是三档处置的前置取证；`files` 可省略 `--folder` 表示全库枚举；`orphans` 不接受任何路径参数。
- 枚举命令返回的中文路径可直接回传给其他命令：bridge 已把 stdout 固定为 UTF-8，不再依赖系统 locale。

### 迭代治理写操作组

以下三个命令用于分级处置，每个都带回读验证。

```bash
python obsidian-knowledge-flow/scripts/obsidian_cli_bridge.py property-set --path "知识库/20-Knowledge/topic/note.md" --name status --value superseded --json
python obsidian-knowledge-flow/scripts/obsidian_cli_bridge.py property-set --path "知识库/20-Knowledge/topic/note.md" --name superseded_by --value "[[新笔记标题]]" --type list --json
python obsidian-knowledge-flow/scripts/obsidian_cli_bridge.py move --path "知识库/20-Knowledge/topic/note.md" --to "知识库/90-Archive/note.md" --json
python obsidian-knowledge-flow/scripts/obsidian_cli_bridge.py delete --path "知识库/20-Knowledge/topic/note.md" --json
```

三类写操作的 readback 判据：

| 操作 | readback 判据 | 不符时的错误码 |
| --- | --- | --- |
| `property-set` | 回读该属性并与写入值逐字比对，必须相等 | `READBACK_MISMATCH` |
| `move` | 新路径必须可读，旧路径必须不可读 | `READBACK_MISMATCH` |
| `delete` | 原路径必须不可读 | `READBACK_MISMATCH` |

存在性探测必须使用严格模式：`properties` 对不存在的文件以退出码零返回 `Error:` 载荷，只有严格模式才会把它判为不可读。

写操作硬边界：

- `delete` 一律进回收站，bridge 不接受也不透传 `permanent`；已实测删除后文件可在 Windows 回收站中找到。
- `move` 的目标目录必须已存在；目标目录缺失时 CLI 以退出码零返回 `ENOENT` 载荷，原文件保持无损。
- `move` 的 `--to` 既可以是完整目标路径，也可以只给目录，后者保留原文件名。
- 执行案例笔记受追加式契约保护：`知识库/20-Knowledge/execution-failure-cases/` 下的路径禁止 `move` 与 `delete`，也不得作为 `move` 目标，bridge 直接返回 `EXECUTION_CASE_IMMUTABLE`。
- `property-set` 只改目标属性，实测其余 frontmatter 字段、顺序与中文值全部保留。

### Windows/WSL 调用模板

- Windows Agent：在 Windows shell 中直接运行上面的 `python ... bridge.py` 命令；bridge 选择 Windows direct transport。
- WSL Agent：在 WSL shell 中运行同一 bridge 入口；bridge 通过 `powershell.exe` 或可用的 `pwsh.exe` 调用 Windows adapter，返回 `transport=wsl-powershell-interop`。调用方不直接寻找 Linux `obsidian`。
- 需要从 Windows shell 复核 WSL 入口时，使用 `wsl.exe -d Ubuntu-24.04 -- python3 /mnt/d/luode/luode-skills/obsidian-knowledge-flow/scripts/obsidian_cli_bridge.py doctor --json`；该路径只指向仓库测试资产，不是 vault 访问路径。

应用恢复只允许一轮：初次命令失败且错误属于应用不可达时，adapter 隐藏启动一次，最多轮询 15 秒，然后只重试原操作一次。响应中的 `attempts` 不得超过 3；参数、路径、interop、PowerShell、selector、timeout 或 readback 错误不触发无变化重试。

生产入口只允许上述 allowlist；不得向 bridge 透传任意 Obsidian 子命令。

## 读写约束

- 创建或更新笔记前必须先 bridge `search` 或 `search-context` 检索现有笔记；读取证据必须来自 bridge `read`。
- `create`、`append` 的响应必须 `verified=true`；没有 readback 证据的写入不得宣称成功。
- 全量批处理可从受控 source root 读取 Markdown；target vault 的 create、append、read 与 INDEX 更新仍只走 bridge。
- bridge 临时 request/response 文件必须在 finally 清理，正文、token、凭据和临时文件内容不得写日志。

## 阻断文案要点

bridge 阻断时，说明必须包含：

- 失败的前置项：interop、PowerShell、CLI、应用、vault、路径、超时或读回失败。
- 目标 vault 根目录。
- 用户可执行的恢复动作：安装/升级 Obsidian 1.12.7+ installer，在设置中启用 Command line interface，把 `D:\obsidian_data` 打开/注册，重新运行 bridge doctor。

阻断时不要写入任何笔记，也不要把直接文件读写结果当成 vault 事实。

## 验证映射

| bridge 能力 | 自动化或实机证据 |
| --- | --- |
| doctor、固定 root、唯一 selector | TEST-OBS-001/011 |
| WSL interop 与参数 UTF-8 | TEST-OBS-003/007 |
| create/append/readback 与路径安全 | TEST-OBS-004/008/013 |
| 自动启动、10KB 中文和超时边界 | TEST-OBS-006/010 |
| distill、INDEX 与脱敏 | TEST-OBS-014/015 |
| references bridge-only 规则与禁止词扫描 | TEST-OBS-016 |
| 迭代治理只读组与中文路径可回传 | TEST-OBS-017 |
| 写属性、移动、删除与三类 readback | TEST-OBS-018 |
| 执行案例目录禁止 move/delete | TEST-OBS-019 |
