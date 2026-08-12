# 知识库文件操作规则

本 skill 使用标准文件工具读写 `D:\谷歌云盘\知识库\` 下的所有笔记，不依赖任何 CLI 桥接层。

## 路径安全规则

- 所有笔记路径必须是相对知识库根 `D:\谷歌云盘\知识库\` 的裸相对路径
- 禁止再加 `知识库/` 前缀：根目录本身已经是 `知识库`，前缀叠加会生成嵌套目录 `D:\谷歌云盘\知识库\知识库\`
- 禁止包含 `..`、盘符（如 `C:`）、UNC 路径（如 `\\server\share`）或 Windows 非法字符（`< > : " / \ | ? *`）
- 路径必须指向 `D:\谷歌云盘\知识库\` 内的文件

正确与错误写法对照：

| 写法 | 判定 | 实际落点 |
| --- | --- | --- |
| `20-Knowledge/topic/note.md` | 正确 | `D:\谷歌云盘\知识库\20-Knowledge\topic\note.md` |
| `知识库/20-Knowledge/topic/note.md` | 错误 | `D:\谷歌云盘\知识库\知识库\20-Knowledge\topic\note.md`（嵌套） |
| `D:\谷歌云盘\知识库\20-Knowledge\note.md` | 错误 | 带盘符的绝对路径不作为笔记路径参数 |

笔记正文内的 wikilink 同样使用裸相对路径，例如 `[[20-Knowledge/codex-rules/仓库总规则]]`。

## 常用文件操作

### 检索
```powershell
# 全文搜索
Select-String -Path "D:\谷歌云盘\知识库\**\*.md" -Pattern "关键词" -SimpleMatch

# 或使用 rg（更快）
rg "关键词" "D:\谷歌云盘\知识库\" --glob "*.md" -l

# 搜索 wikilink 引用
rg "\[\[笔记名\]\]" "D:\谷歌云盘\知识库\" --glob "*.md" -l
```

### 读取
```powershell
Get-Content -Raw -Encoding UTF8 "D:\谷歌云盘\知识库\20-Knowledge\topic\note.md"
```

### 写入（新建或覆盖）
```powershell
Set-Content -Encoding UTF8 -Path "D:\谷歌云盘\知识库\20-Knowledge\topic\new-note.md" -Value $markdownContent
```

### 追加
```powershell
Add-Content -Encoding UTF8 -Path "D:\谷歌云盘\知识库\20-Knowledge\topic\note.md" -Value $appendix
```

### 移动
```powershell
Move-Item -LiteralPath "D:\谷歌云盘\知识库\20-Knowledge\topic\old.md" -Destination "D:\谷歌云盘\知识库\90-Archive\old.md"
```

### 删除
```powershell
Remove-Item -LiteralPath "D:\谷歌云盘\知识库\20-Knowledge\topic\trash.md"
```

## 写后回读验证

每次写入后必须回读内容并比对一致性：

```powershell
$before = $markdownContent
# 写入...
Set-Content -Encoding UTF8 -Path $path -Value $before
# 回读
$after = Get-Content -Raw -Encoding UTF8 $path
if ($after -ne $before) { throw "READBACK_MISMATCH" }
```

## 执行案例保护

`20-Knowledge/execution-failure-cases/` 下的路径禁止移动和删除，仅允许追加。写入前必须验证目标路径不在该目录下。

## 写入失败处理

- 目录不存在时先创建目标目录：`New-Item -ItemType Directory -Force -Path $dir`
- 写入后回读不一致时重试一次；失败则报告 `阻断`
- 路径安全规则不满足时直接报告 `阻断`，不执行任何文件操作
