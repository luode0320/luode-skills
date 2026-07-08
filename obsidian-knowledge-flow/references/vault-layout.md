# Vault 布局

本 skill 只使用一个固定的 Obsidian vault 根目录：`D:\obsidian_data`。
真正的知识工作区固定在该 vault 下的 `知识库/` 目录，后续所有 Obsidian 检索、捕获和沉淀都以 `D:\obsidian_data\知识库\` 为主落点。
不要再通过 `OBSIDIAN_KB_ROOT`、`OBSIDIAN_VAULT_ROOT`、`.obsidian-kb-root` 或其它候选路径重新推导 vault。

## 固定根目录

- Windows：`D:\obsidian_data`
- 该根目录一旦确认，不再重新探测其他路径。
- 如果 `D:\obsidian_data` 不存在，允许创建；创建后必须继续通过 Obsidian CLI 校验该目录能作为目标 vault 操作。
- 如果 CLI 不能识别、不能切换或不能在该固定 vault 下执行命令，必须阻断并提示用户在 Obsidian 中打开/注册一次该 vault。
- `知识库/` 是固定知识目录；如果缺失，只能在 `D:\obsidian_data` 内补齐，不能改用其他根目录。

## 目录树

```text
D:\obsidian_data/
└── 知识库/
    ├── 00-Inbox/
    ├── 10-Sessions/
    ├── 20-Knowledge/
    ├── 30-MOCs/
    ├── 40-Entities/
    ├── 50-Sources/
    ├── 90-Archive/
    ├── Attachments/
    ├── Templates/
    └── INDEX.md
```

## 落点规则

- `知识库/00-Inbox/`: 仅在分类不确定，或用户要求原始捕获时使用。
- `知识库/10-Sessions/YYYY/MM/`: 每个有价值的会话片段保存为一篇会话笔记。
- `知识库/20-Knowledge/<topic>/`: 保存长期概念、决策、流程和可复用模式。`20-Knowledge` 下最多保留两级主题目录。
- `知识库/30-MOCs/`: 保存高价值主题地图。只有能连接多个相关笔记或提升检索效率时才创建 MOC。
- `知识库/40-Entities/<type>/`: 保存反复出现的实体。推荐类型：`people`、`projects`、`repos`、`tools`、`terms`、`orgs`、`products`。
- `知识库/50-Sources/<type>/`: 保存来源摘要。推荐类型：`web`、`video`、`repo`、`paper`、`dataset`。
- `知识库/90-Archive/`: 只有笔记需要从当前检索中退出时，才移动到这里。

## 文件名规则

- 优先使用稳定、可读的 Markdown 文件名。
- 标题使用用户主要语言；产品、仓库、人名等固定名称保持原样。
- 删除 Windows 不安全字符：`< > : " / \ | ? *`。
- 只有会话笔记和时间顺序重要的来源笔记才添加时间戳。
- 除非用户明确要求，否则 `知识库/` 根目录下不要超过三级目录。

## 索引规则

- `知识库/INDEX.md` 保持简短，只链接主要 MOC、活跃项目和检索入口。
- 不要把 `知识库/INDEX.md` 变成完整目录。详细检索交给 Obsidian CLI、frontmatter、标签、别名、backlinks 和 MOC。
- 新建 MOC、项目笔记或重要知识笔记时，如果能提升导航效率，就在 `知识库/INDEX.md` 中添加一个链接。
