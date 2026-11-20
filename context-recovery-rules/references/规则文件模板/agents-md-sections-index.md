# AGENTS.md / CLAUDE.md 受管章节索引

本文件只列出受管章节的标题与来源变量，不复制正文；正文的唯一权威来源是 `../../scripts/bootstrap_agents.sh` 内对应的 heredoc 变量（由 `sync_agents_file` 按下表顺序调用 `sync_section` 写入规则文件）。需要查看某一章节的确切文字时直接打开脚本对应变量，不在本仓库另存第二份正文。

| 序号 | 受管章节标题 | 脚本变量 |
|---:|---|---|
| 1 | 语言 | `BODY_LANGUAGE` |
| 2 | 适用范围 | `BODY_SCOPE` |
| 3 | 注意 | `BODY_NOTICE` |
| 4 | Skill 强制自动触发规则（最高优先级） | `BODY_SKILL_AUTO` |
| 5 | 严禁脑补工具调用与结果（最高优先级，强制） | `BODY_NO_HALLUCINATE` |
| 6 | 严禁自动提交 Git（最高优先级，强制） | `BODY_NO_AUTO_COMMIT` + `BODY_NO_AUTO_COMMIT_PROJECT_EXTRA`（仅归属仓库） |
| 7 | 跨项目写入红线（最高优先级，强制） | `BODY_NO_CROSS_PROJECT_WRITE` |
| 8 | Skill 命中强制规则 | `BODY_SKILL_HIT` |
| 9 | 代码生成风格入口规则 | `BODY_CODE_GENERATION_STYLE` |
| 10 | Karpathy 风格硬闸门 | `BODY_KARPATHY_HARD_GATES` |
| 11 | 注释任务强制流程 | `BODY_COMMENT_TASK` |
| 12 | 上下文压缩续做规则 | `BODY_CONTEXT_COMPRESS` |
| 13 | 文件编码与写入规则 | `BODY_CHINESE_ENC` |
| 14 | 变更最小化 | `BODY_MIN_CHANGE` |
| 15 | 本地连接调试测试红线（最高优先级，强制） | `BODY_LOCAL_ONLY_CONNECTION` |
| 16 | 测试不得污染生产代码红线（最高优先级，强制） | `BODY_TEST_POLLUTION` |
| 17 | 最小实现优先级阶梯 | `BODY_MINIMAL_LADDER` |
| 18 | 输出格式规则 | `BODY_OUTPUT_FORMAT` |
| 19 | Windows / WSL 执行规则 | `BODY_WINDOWS_WSL` |
| 20 | CodeGraph 与代码检索 | `BODY_CODEGRAPH` |
| 21 | 插件检测安装规则 | `BODY_PLUGIN` |
| 22 | 图像生成强制规则 | `BODY_IMAGEGEN` |
| 23 | Godot 项目工具配置（仅 Godot 项目） | `GODOT_TOOLING_SECTION` |
| 24 | 图像生成配置（仅 Godot 项目） | `GODOT_IMAGEGEN_SECTION` |

非受管但同属规则文件组的静态内容：`GITATTRIBUTES_CONTENT`（两种换行符变体）、`EDITORCONFIG_CONTENT`（两种换行符变体），只在 `.gitattributes` / `.editorconfig` 缺失时首次写入，不走 `sync_section` 增量同步。

子目录规则文件可声明跳过受管章节同步：在文件中单独写一行 `<!-- bootstrap-agents:skip-managed-sections -->`（脚本变量 `SKIP_MANAGED_SECTIONS_MARKER`，由 `has_skip_marker` 判定，允许首尾空白与 CRLF 行尾）。含该标记的子目录 `AGENTS.md` / `CLAUDE.md` 不写入上表任何章节，脚本逐文件打印跳过原因；标记按文件生效，根目录规则文件忽略该标记，始终按上表同步。
