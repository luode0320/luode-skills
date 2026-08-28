# 知识库的 WSL 侧访问口径

[file-operations.md](file-operations.md) 给的是 Windows 宿主口径（PowerShell + `D:\` 绝对路径）。当
agent 本身跑在 WSL 内时，那套命令不可用，但**知识库仍然完全可读可写**——同一个 Google Drive
目录经 drvfs 挂载后可用 POSIX 工具直读，不需要 PowerShell、不需要任何 bridge 命令。

本文件只补 WSL 侧的访问方式，路径安全规则、笔记 schema、三态判定、引用台账等约定与 Windows
侧完全一致，不在此重复。

## 一、双宿主根目录映射

| 宿主 | 知识库根目录 | 读写工具 |
| --- | --- | --- |
| Windows | `D:\谷歌云盘\知识库\` | PowerShell（`Get-Content` / `Set-Content` / `Add-Content`） |
| WSL | `/mnt/d/谷歌云盘/知识库` | POSIX（`cat` / `rg` / `find` / heredoc 重定向） |

两者是**同一份文件**，不是两份副本；任一侧写入后由 Google Drive 客户端负责多端同步。

笔记路径参数的口径不随宿主变化：始终是相对知识库根的裸相对路径（如
`20-Knowledge/项目/note.md`），禁止加 `知识库/` 前缀，禁止把 `/mnt/d/...` 或 `D:\...` 绝对路径
当作笔记路径参数写进 frontmatter、wikilink 或引用台账。绝对路径只出现在 shell 命令里。

## 二、挂载探测（5 步，仅在首次或报错时执行）

固定映射已知，正常轮次直接用 `/mnt/d/谷歌云盘/知识库`，不做探测。只有该路径读不到时才按下列顺序定位：

1. **确认盘符已挂载**：`ls -d /mnt/d` 与 `mount | grep -i drvfs`。WSL2 现版本 drvfs 以 `9p` 类型
   出现（`D:\ on /mnt/d type 9p (...aname=drvfs;path=D:\...)`），不要因为 `type` 不是字面
   `drvfs` 就判定未挂载。
2. **确认根目录存在**：`[ -d "/mnt/d/谷歌云盘/知识库" ] && echo ok`。中文路径必须加引号。
3. **确认可读可写**：`ls -1 "$KB"` 有输出、`[ -w "$KB" ]` 为真。只做权限位判断，不落盘探测文件。
4. **确认编码**：`file -i "$KB/INDEX.md"` 应为 `charset=utf-8`。若为 `unknown-8bit` 或
   `iso-8859-1`，说明该笔记曾被 GBK/ANSI 写入，先转回 UTF-8 再改动。

同一盘符可能同时挂载在多个挂载点（如 `/mnt/d` 与 `~/d/<user>`、`~/.codex/skills` 这类
9p 挂载）。它们指向同一份文件，但**只用 `/mnt/d` 这一个规范形态**参与知识库路径拼接，避免
同一笔记在证据里出现两种绝对路径。

5. **确认起点不是符号链接**：`ls -ld <dir>`。skill 库与知识库所在的家目录入口可能整个是指向
   Windows 盘的符号链接（本机实测 `~/.claude/skills -> /mnt/d/谷歌云盘/luode-skills`）。
   `find <符号链接>` 默认不进入目标目录，**静默返回零结果且退出码 0**——会被误读成"库里没有
   这条笔记"。起点加尾斜杠、改用 `find -L`，或先 `readlink -f` 解出真实路径。
   完整机理与其余 6 个静默失败陷阱见 `wsl-windows-bridge__skillhub` 的
   `references/wsl-windows-comm-pitfalls.md`。

## 三、POSIX 工具对照（与 file-operations.md 的 PowerShell 表一一对应）

以下命令统一假设 `KB="/mnt/d/谷歌云盘/知识库"`。

| 动作 | WSL 命令 |
| --- | --- |
| 全文检索 | `rg "关键词" "$KB" --glob "*.md" -l` |
| 检索 wikilink 引用 | `rg '\[\[笔记名\]\]' "$KB" --glob "*.md" -l` |
| 按名定位 | `find "$KB" -type f -name "*.md" \| grep -iE "关键词"` |
| 读取 | `cat "$KB/20-Knowledge/topic/note.md"` |
| 窄读 | `sed -n '1,40p' "$KB/.../note.md"` |
| 写入（新建或覆盖） | `cat > "$KB/.../new-note.md" <<'MD'` … `MD` |
| 追加 | `cat >> "$KB/.../note.md" <<'MD'` … `MD` |
| 移动 | `mv "$KB/20-Knowledge/topic/old.md" "$KB/90-Archive/old.md"` |
| 删除 | `rm "$KB/20-Knowledge/topic/trash.md"` |
| 建目录 | `mkdir -p "$KB/20-Knowledge/topic"` |

硬约束：

- **中文路径全程加引号**。`$KB` 含中文，任何未加引号的展开都会被 shell 分词成
  `/mnt/d/谷歌云盘/知识库` 之外的无效片段。
- **写入必须用 quoted heredoc**（`<<'MD'`）。未加引号的 heredoc 会把笔记正文里的 `$`、反引号、
  `\` 当作 shell 语法展开，静默破坏 frontmatter 与代码块。
- 不使用裸 `>` / `>>` 写中文而不确认编码；WSL 默认 locale 为 UTF-8 时 heredoc 直接产出 UTF-8，
  但仍须按下节回读校验。

## 四、写后回读验证（WSL 侧等价流程）

Windows 侧靠 `$before -ne $after` 比对；WSL 侧用指纹与编码双校验：

```bash
NOTE="$KB/20-Knowledge/topic/note.md"
cat > "$NOTE" <<'MD'
...笔记正文...
MD
file -i "$NOTE"          # 必须为 charset=utf-8
md5sum "$NOTE"; wc -c "$NOTE"
sed -n '1,20p' "$NOTE"   # 回读确认中文未乱码、frontmatter 完整
```

回读不一致、编码非 UTF-8 或中文乱码时重试一次，仍失败则判 `阻断`，不得登记引用台账的沉淀条目。

## 五、机器索引脚本在 WSL 下的可用性

`scripts/audit_vault_knowledge.py` 的 `KB_ROOT` 按「环境变量 `KNOWLEDGE_VAULT_ROOT` -> 各宿主候选
按实测存在命中」解析，`knowledge_index.py` 复用同一常量，因此两个脚本在 Windows 与 WSL 下都可直接运行：

```bash
cd ~/.claude/skills
python3 knowledge-flow/scripts/knowledge_index.py query --keyword "<词>"
python3 knowledge-flow/scripts/knowledge_index.py check
python3 knowledge-flow/scripts/audit_vault_knowledge.py --json
```

WSL 下调用要点：

- 用 `python3`，不是 `python`（多数 WSL 发行版无 `python` 别名）。
- 脚本路径是相对 skill 根的 `knowledge-flow/scripts/...`，先 `cd ~/.claude/skills`，或直接给绝对路径。
  注意 `~/.claude/skills` 本身可能是符号链接：`cd` 与 `cat` 对它透明，但 `find` 需要尾斜杠或 `-L`。
- 知识库位于非默认位置时用 `KNOWLEDGE_VAULT_ROOT=/path/to/vault python3 ...` 覆盖，不要改脚本常量。

「第一跳固定用机器索引」这条检索规则在 WSL 下同样成立，不因宿主不同退化为 `rg` 优先。

## 六、失败回退表（实测证据 2026-08-27）

| 症状 | 根因 | 处理 |
| --- | --- | --- |
| 脚本输出 `{"ok": false, "code": "KB_ROOT_NOT_FOUND"}`，退出码 4 | `KB_ROOT` 解析未命中当前宿主形态 | 先按第二节确认挂载与根目录；确认存在仍失败时用 `KNOWLEDGE_VAULT_ROOT` 显式覆盖 |
| 命令报路径不存在，但 `ls` 手动敲能进去 | 中文路径未加引号被 shell 分词 | 全程 `"$KB/..."` 加引号重试 |
| 笔记写入后 frontmatter 缺字段或正文被截断 | heredoc 未加引号，`$`/反引号被展开 | 改用 `<<'MD'` 重写该笔记，并回读校验 |
| 脚本"看起来成功"但产物是错的 | 用了 `cmd \| head` 后取 `$?`，拿到的是管道末端命令退出码 | 改 `out=$(cmd 2>&1); rc=$?` 先取码再截断输出 |
| `check` 退出码 5 | 存量笔记 frontmatter 不合规，与本轮写入无关 | 只对本轮新写或改写的笔记当轮修到合规，历史存量不当轮裁决 |
| `find` 在库内搜不到明明存在的笔记 | 查找起点是符号链接，find 默认 `-P` 不进入目标目录 | 起点加尾斜杠、改用 `find -L`，或 `readlink -f` 解出真实路径 |
| 写出的笔记被静默截断，shell 报一串 `command not found` | heredoc 定界符与笔记正文里的某一行同名，heredoc 提前结束 | 外层定界符换成正文绝不会出现的长串；写入后核对 `wc -l` 与 `tail -5` |
| `/mnt/d` 不存在 | 当前不是 WSL，或该盘符未挂载 | 若在 Windows 宿主，改用 [file-operations.md](file-operations.md) 的 PowerShell 口径 |

## 七、边界

- 本文件只解决「WSL 内如何访问同一个知识库」，不改变知识库四态判定、目录落点、笔记 schema、
  三态判定与引用台账口径。
- WSL 侧访问不需要 `wsl-windows-bridge__skillhub` 的 `win-ps` / `win-copy`：drvfs 直读即可，
  引入 bridge 只会增加失败面。只有需要调用 Windows 侧程序（而非读写文件）时才用 bridge。
- 需要在 WSL 与 Windows 路径形态间转换时用 `wslpath`（见 `wsl-path-converter__skillhub`），
  但笔记路径参数仍只用裸相对路径，不写入任何绝对路径形态。
