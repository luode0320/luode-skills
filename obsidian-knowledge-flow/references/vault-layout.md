# Vault 布局

所有操作都使用一个固定的 Obsidian vault 根目录。根目录按 `OBSIDIAN_KB_ROOT`、`OBSIDIAN_VAULT_ROOT`、`.obsidian-kb-root`、系统默认路径的顺序解析。

## 默认根目录

- Windows：`D:\obsidian_data`
- WSL/Linux：`/usr/local/src/obsidian_data`

默认路径不存在时，允许先创建这个目录；创建目录只完成本地根目录 bootstrap，不代表 Obsidian 已经注册该 vault。创建后必须继续通过 Obsidian CLI 校验该目录能作为目标 vault 操作；若 CLI 不能识别、不能切换或不能在该目录下执行命令，必须阻断并提示用户在 Obsidian 中打开/注册一次该 vault。

禁止在当前仓库下自动创建备用 vault。禁止因为默认目录创建失败就静默回退到当前工作区、用户 home、临时目录或其他路径。

## 根目录校验

1. 解析到根目录后，先规范化为绝对路径。
2. 如果根目录来自环境变量或 `.obsidian-kb-root`，必须确认路径存在且是目录；不存在时阻断，不自动替用户创建自定义路径。
3. 如果根目录来自系统默认路径，目录不存在时才允许自动创建。
4. 任何笔记相对路径都必须在该根目录内解析；包含 `..`、符号链接逃逸或绝对路径写出根目录时阻断。
5. 使用 CLI 前，优先在该根目录作为当前工作目录执行命令；如果 CLI 选择了别的 active vault，阻断。

## 目录树

```text
<vault-root>/
├── 00-Inbox/        # 不确定捕获和未分类片段
├── 10-Sessions/     # 会话笔记，按时间分区
├── 20-Knowledge/    # 长期知识笔记
├── 30-MOCs/         # 内容地图和主题枢纽
├── 40-Entities/     # 人、项目、仓库、工具、术语、产品
├── 50-Sources/      # 外部网页、视频、仓库、论文、数据集
├── 90-Archive/      # 保留历史的退役笔记
├── Attachments/     # 二进制文件与媒体
├── Templates/       # 可选 Obsidian 模板
└── INDEX.md         # 轻量全局导航和检索提示
```

## 落点规则

- `00-Inbox/`: 仅在分类不确定，或用户要求原始捕获时使用。
- `10-Sessions/YYYY/MM/`: 每个有价值的会话片段保存为一篇会话笔记。
- `20-Knowledge/<topic>/`: 保存长期概念、决策、流程和可复用模式。`20-Knowledge` 下最多保留两级主题目录。
- `30-MOCs/`: 保存高价值主题地图。只有能连接多个相关笔记或提升检索效率时才创建 MOC。
- `40-Entities/<type>/`: 保存反复出现的实体。推荐类型：`people`、`projects`、`repos`、`tools`、`terms`、`orgs`、`products`。
- `50-Sources/<type>/`: 保存来源摘要。推荐类型：`web`、`video`、`repo`、`paper`、`dataset`。
- `90-Archive/`: 只有笔记需要从当前检索中退出时，才移动到这里。

## 文件名规则

- 优先使用稳定、可读的 Markdown 文件名。
- 标题使用用户主要语言；产品、仓库、人名等固定名称保持原样。
- 删除 Windows 不安全字符：`< > : " / \ | ? *`。
- 只有会话笔记和时间顺序重要的来源笔记才添加时间戳。
- 除非用户明确要求，否则 vault 根目录下不要超过三级目录。

## 索引规则

- `INDEX.md` 保持简短，只链接主要 MOC、活跃项目和检索入口。
- 不要把 `INDEX.md` 变成完整目录。详细检索交给 Obsidian CLI、frontmatter、标签、别名、backlinks 和 MOC。
- 新建 MOC、项目笔记或重要知识笔记时，如果能提升导航效率，就在 `INDEX.md` 中添加一个链接。
