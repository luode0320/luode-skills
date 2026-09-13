---
name: git-line-ending-hygiene
description: 当工作树出现大批"改了但看不出改了啥"的文件、git status 动辄几百上千条变更、跨平台（Windows/WSL/Linux）协作后 review 被迫淹没在噪音里时触发。识别纯行尾符（CRLF/LF）污染，用 .gitattributes 固化行尾符，并处理存量已污染文件的归一。核心反直觉点：正确时机下新增 `.gitattributes` 会让存量假 diff **自动消失**，无需 `git add --renormalize`；但若索引中本已存 CRLF，则相反会暴露大量真实 diff。另含从「白名单式」迁移到「全覆盖式」时保留 linguist 等独立配置的要点。
agent_created: true
---

# Git 行尾符治理

## 一、先确认「确实是纯行尾符差异」

不要凭感觉判断。用**忽略空白**比对，若差异归零，即为纯行尾符污染：

```bash
# 症状：动辄上千条变更
git status --short | wc -l

# 诊断 1：总量是否对称（行尾符污染的特征是增删行数完全相等）
git diff --shortstat
# 典型输出：1398 files changed, 466386 insertions(+), 466386 deletions(-)

# 诊断 2：忽略空白后是否归零（决定性判据）
git diff --ignore-all-space --shortstat
# 输出为空 → 确认是纯行尾符差异，无任何业务改动

# 诊断 3：确认方向（HEAD 是 LF 还是 CRLF）
git show HEAD:<某个文件> | head -3 | cat -A   # 行尾显示 $ = LF
git diff <某个文件> | cat -A | grep -m3 XXX   # 行尾显示 ^M$ = CRLF
```

**为什么这个判断重要**：纯行尾符污染会让真实改动被淹没，使 code review 与提交范围判定失效。必须先把它与业务改动分开——用**精确文件暂存**（`git add <具体文件>`），绝不在此时使用 `git add -A` / `git add .`。

## 二、根治：在仓库根新增 `.gitattributes`

```
* text=auto eol=lf
```

- `text=auto`：git 自动识别文本文件并做换行规范化；二进制文件被自动检测排除，不受影响。
- `eol=lf`：checkout 到工作树时统一写出 LF。

写入时**确保该文件自身是 LF**（`newline="\n"`），否则第一个受害者就是它自己。

### 「eol 会隐含 text 属性」的疑虑（已实测否定）

git 文档 `eol` 一节写有 "It enables end-of-line conversion without any content checks, effectively setting the text attribute"，容易让人担心 `* text=auto eol=lf` 里的 `eol=lf` 会**覆盖 `auto` 的二进制检测**，把 PNG/JPG 当文本处理从而损坏文件。

**实测结论：不会。** `text=auto` 的自动检测在两者同时出现时仍然生效，二进制文件被正确跳过：

```bash
# 验证一个二进制文件的属性与索引状态
git check-attr text eol -- assets/logo.png
git ls-files --eol -- assets/logo.png
# 期望：i/-text w/-text（git 仍识别为二进制，不做行尾转换）
```

可放心使用该写法。若要额外保险，对已知二进制类型显式标注（与 `*` 规则叠加时，更具体的模式优先，不冲突）：

```
*.png binary
*.jpg binary
```

## 三、关键反直觉点（决定要不要跑 renormalize）

多数资料会告诉你"加完 .gitattributes 还要 `git add --renormalize .`"。**这取决于索引里现在存的是什么**：

| 索引中内容 | 加 `eol=lf` 后的现象 | 需要 renormalize 吗 |
|---|---|---|
| **LF**（HEAD 原本就是 LF，只是工作树被改了） | 比较时把工作树 CRLF 规范化成 LF，与索引一致 → **假 diff 自动消失** | **不需要** |
| **CRLF**（历史上就以 CRLF 入库过） | 规范化后与索引不一致 → 暴露出大量真实 diff | 需要，且这确实是必须提交的归一 |

所以正确顺序是：**先加 .gitattributes，再观察 `git status` 数量**。

```bash
# 加完立即验证效果
git status --short | wc -l          # 应为 0（或只剩真实改动）

# 确认规则真的生效在这批文件上
git check-attr text eol -- <某个既有文件>
# 期望：text: auto / eol: lf
```

若数量降为 0 → 无需 renormalize，直接提交 `.gitattributes` 即可。
若暴露出大量 diff → 说明索引里存的是 CRLF，此时 `git add --renormalize .` 并**单独提交**这次归一（commit 信息里说清是行尾符归一，便于 review 跳过）。

## 三之二、从「白名单式」迁移到「全覆盖式」

若仓库已有 `.gitattributes`，但用的是 `* text=auto` 加**逐类型白名单**（`*.go text eol=lf`、`*.json text eol=lf` …），则未列入白名单的文本类型（`.txt`/`.sql`/`.lua`/`Dockerfile`/`.env.example`/`LICENSE` 等）只走 `text=auto`，checkout 时不强制 LF —— 同一仓库内存在两套行尾符行为。

迁移步骤：

1. **先查索引有无 CRLF**（决定性前提）：
   ```bash
   git ls-files --eol | awk '{print $1}' | sort | uniq -c
   # 关注 i/crlf 的数量
   ```
2. 把 `* text=auto` 改为 `* text=auto eol=lf`，删除已被 `*` 覆盖的逐类型行。
3. **保留与行尾符无关的独立配置** —— 最容易误删的是 GitHub Linguist 配置：
   ```
   web/**/*.tsx -linguist-detectable
   electron/** linguist-vendored
   web/src/routeTree.gen.ts linguist-generated
   ```
   删掉会改变 GitHub 语言统计，但与行尾符毫无关系。二进制 `binary` 标注同理，保留作防御。
4. 改完立即 `git status` 验证是否有额外 diff 冒出。

**判据**：`i/crlf = 0` 时迁移安全（零额外 diff）；若 `i/crlf > 0`，收紧规则会让这批文件暴露为待归一改动，需单独提交。

## 四、写入方式（跨平台/WSL 注意事项）

从 Windows 侧工具直接写 WSL 挂载盘会失败（`EPERM`），且 shell 内嵌引号易被多层剥掉。稳妥做法：写脚本文件再执行，并用 Python 强制 LF 写入。

```python
with io.open(path, "w", encoding="utf-8", newline="\n") as f:
    f.write(content)   # newline="\n" 是关键，避免被转成 CRLF
```

## 五、收尾清单

- [ ] `--ignore-all-space` 比对确认差异性质
- [ ] 用精确文件暂存，保护污染文件不被误提交
- [ ] `.gitattributes` 自身为 LF
- [ ] 验证规则对既有文件生效（`git check-attr`）
- [ ] 改动前查 `git ls-files --eol`，确认 `i/crlf` 数量
- [ ] 观察 `git status` 数量，判断是否需要 renormalize
- [ ] 迁移时保留 linguist / binary 等独立配置
- [ ] 提交时只含 `.gitattributes`（若需 renormalize 则单独一笔）
- [ ] 查其他仓库是否已有 `.gitattributes`，避免重复或写法冲突

## 六、预防

行尾符污染的源头通常是 Windows 侧工具（编辑器默认 CRLF、脚本重写文件、解压/同步工具）。固化 `.gitattributes` 后，**已跟踪文件在 checkout 时会被强制为 LF**，源头即使再改写，也会在下次 git 比较/提交时被规范化，假 diff 不再堆积。

若污染仍反复出现，应排查具体是哪个工具在写文件，而不是反复手工清理。
