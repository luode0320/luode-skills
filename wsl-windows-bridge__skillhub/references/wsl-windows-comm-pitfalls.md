# WSL ↔ Windows 通信陷阱清单

agent 跑在 WSL 内、目标文件在 Windows 盘时，最常见的失败**都不报错**——它们返回空结果或
`False`，看起来像"文件不存在""目录是空的""知识库没有这条笔记"。本清单只收录实测复现过的
静默失败，按隐蔽程度排序。

配套：免桥直读的决策表见 SKILL.md「前置判定」节；知识库专属口径见 `knowledge-flow` 的
`references/wsl-access.md`；路径格式互转见 `wsl-path-converter__skillhub`。

## 实测拓扑示例（2026-08-27）

WSL 家目录下的工具目录可能整个是指向 Windows 盘的符号链接，本机实测：

```
~/.claude/skills  ->  /mnt/d/谷歌云盘/luode-skills     # skill 库本体在 Windows 盘
~/.codex/skills   ->  D:\ 的 9p 挂载
知识库             ->  /mnt/d/谷歌云盘/知识库
```

含义：对这些目录的读写实际落在 Windows NTFS 上、经 Google Drive 同步，同时受 9p 语义与下列
所有陷阱约束。动手前先 `ls -ld <dir>` 看清它是真目录还是符号链接。

## 陷阱 1：find 起点是符号链接时静默返回零结果

**症状**：`ls` 能列出文件、`test -f` 确认存在，但 `find <dir> -name "<文件名>"` 什么都不返回，
且退出码 0、无任何错误输出。

**根因**：`find` 默认 `-P` 模式不解引用符号链接。当**查找起点本身**是符号链接时，find 把它当
一个类型为 `l` 的节点处理完就结束，从不进入目标目录。

**实测证据**：

```
$ ls -ld ~/.claude/skills
lrwxrwxrwx ... /home/luode/.claude/skills -> /mnt/d/谷歌云盘/luode-skills

$ find ~/.claude/skills -maxdepth 0 -printf '%y %p\n'
l /home/luode/.claude/skills          # find 眼里它是 symlink，不是目录

$ find ~/.claude/skills -maxdepth 1 -name "字典.md"
                                      # 零结果，退出码 0，无报错
```

**三种修法**（任选，实测均有效）：

```
find ~/.claude/skills/ -maxdepth 1 -name "字典.md"      # 1. 起点加尾斜杠
find -L ~/.claude/skills -maxdepth 1 -name "字典.md"    # 2. -L 跟随符号链接
find "$(readlink -f ~/.claude/skills)" -name "字典.md"  # 3. 先解出真实路径
```

**不要误判方向**：本轮曾把零结果归因为「9p 挂载处理不了中文文件名」。对照实验推翻了它——
ext4 与 9p 上新建的 `字典.md`，`find -name` 都能正常找到，文件名字节是规范 UTF-8
（`od -c` 为 `345 255 227 345 205 270`）。唯一变量是符号链接。**零结果先查起点类型，
不要先怀疑编码。**

## 陷阱 2：Windows 风格路径在 WSL 下被当成相对路径

**症状**：代码里写着 `D:/xxx` 或 `D:\xxx`，在 WSL 下 `exists()` 恒为假，不抛异常；
更麻烦的是结果**随当前工作目录变化**，同一段代码在不同 cwd 下表现不同。

**根因**：POSIX 语义里 `D:` 只是个普通目录名，不是盘符。整个路径被当作相对路径解析。

**实测证据**：

```
>>> from pathlib import Path
>>> p = Path("D:/谷歌云盘/知识库")
>>> p.is_absolute()
False                                    # 关键：不是绝对路径
>>> p.exists()
False                                    # 静默为假，无异常
>>> p.resolve()
PosixPath('<当前cwd>/D:/谷歌云盘/知识库')   # 被拼到 cwd 后面
```

shell 侧同样静默：`[ -e "D:/谷歌云盘/知识库" ]` 直接为假，不报错。

**修法**：

```
wslpath -u 'D:\谷歌云盘\知识库'        # -> /mnt/d/谷歌云盘/知识库
```

跨宿主复用的脚本不要硬编码单一形态，按「环境变量覆盖 -> 各宿主候选按实测存在命中」解析。
本轮 `knowledge-flow` 的 `KB_ROOT` 就是硬编码 `D:/谷歌云盘/知识库` 导致 WSL 下第一跳
机器索引固定失效（返回 `KB_ROOT_NOT_FOUND`、退出码 4），已按此模式修复。

## 陷阱 3：drvfs 在 mount 里以 9p 类型出现

**症状**：按 `type drvfs` 过滤 `mount` 输出得到空结果，误判盘符未挂载。

**实测证据**：

```
D:\ on /mnt/d type 9p (rw,noatime,aname=drvfs;path=D:\;uid=1000;gid=1000;...)
```

`type` 是 `9p`，`drvfs` 只出现在 `aname=` 选项里。

**修法**：用 `mount | grep -i drvfs`（匹配选项串）或 `findmnt -T <path>`，不要按 `type` 字面过滤。
`df -T <path>` 同样显示 `9p`。

## 陷阱 4：同一盘符挂载在多个挂载点

**症状**：同一个文件在证据、日志、报告里出现两种以上绝对路径，看起来像两个不同文件。

**实测证据**：`D:\` 同时挂在 `/mnt/d`、`~/d/<user>`、`~/.codex/skills`。它们指向同一份文件。

**修法**：统一只用 `/mnt/<drive>` 这一个规范形态参与路径拼接。需要确认某路径的真实落点时用
`findmnt -T <path>` 或 `readlink -f <path>`。

## 陷阱 5：中文路径分词与 heredoc 变量展开

**症状**：手敲 `ls` 能进的目录，脚本里报路径不存在；写出的文件 frontmatter 缺字段或正文被截断。

**根因**：两个独立问题——路径未加引号被 shell 按空格分词；heredoc 未加引号使正文里的
`$`、反引号、反斜杠被当 shell 语法展开。

**修法**：变量赋值与每次展开都加引号；写文件用 quoted heredoc（定界符加单引号），正文原样写入。
写后回读校验编码与指纹：`file -i`（应为 `charset=utf-8`）、`md5sum`、`wc -c`、`sed -n '1,20p'`。

## 陷阱 6：heredoc 定界符与正文内容冲突

**症状**：写出的文件在中途被截断，且 shell 把文件后半段当命令执行，报出一串
`command not found`——错误信息里全是本该写进文件的中文句子。

**根因**：正文里出现了与外层 heredoc 定界符**同名的独立一行**，shell 在那一行提前结束 heredoc，
剩余内容退化为命令。写"如何使用 heredoc"这类文档时极易踩到：文档正文里的示例
`cat > f <<'MD'` … `MD`，那个收尾的 `MD` 就会杀掉外层的 `<<'MD'`。

**实测证据**：本轮写本文件时外层用 `<<'MD'`，正文陷阱 5 的示例里也有一行 `MD`，
文件在 127 行处被截断，随后 shell 报
`/bin/bash: line 311: 之后: command not found` 等一连串错误。

**修法**：

- 外层定界符取一个正文绝不会出现的长串，如 `<<'PITFALLS_DOC_EOF_20260827'`
- 或改用 Python/文件写入 API 落盘，绕开 shell heredoc 语义
- 写入后**必须核对行数与末尾内容**（`wc -l` + `tail -5`），截断是静默的，只看退出码发现不了

## 陷阱 7：管道遮蔽退出码

**症状**：明明失败的命令被判成成功，或反之。

**根因**：`cmd | head` 之后 `$?` 是 `head` 的退出码，不是 `cmd` 的。

**实测证据**：本轮把正确返回 4 的脚本误判为「exit 0 假成功」，多绕一轮才发现是测量方式错误。

**修法**：先取码再截断输出（`out=$(cmd 2>&1); rc=$?`），或 `set -o pipefail`，或查
`${PIPESTATUS[0]}`。

## 排查顺序

WSL 侧读不到 Windows 盘上的东西时，按此顺序查，**不要先怀疑编码或权限**：

1. 起点是不是符号链接？`ls -ld <dir>` — 是则按陷阱 1 处理
2. 路径是不是 Windows 形态？看 `is_absolute()` 或用 `wslpath -u` 转 — 是则按陷阱 2 处理
3. 盘符挂上了吗？`findmnt -T <path>` — 注意 type 是 `9p`（陷阱 3）
4. 路径引号加了吗？（陷阱 5）
5. 退出码是不是被管道遮蔽了？（陷阱 7）

只有以上全部排除后，才考虑真正的权限、编码或 Windows 侧文件锁问题。上桥
（`win-ps` / `win-copy`）是最后手段，不是第一反应。
