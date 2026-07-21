# AGENTS.md / CLAUDE.md 受管章节索引

本文件只列出受管章节的标题、来源变量和一句话用途，不复制正文；正文的唯一权威来源是 `../../scripts/bootstrap_agents.sh` 内对应的 heredoc 变量（由 `sync_agents_file` 按下表顺序调用 `sync_section` 写入规则文件）。需要查看某一章节的确切文字时，直接打开脚本对应变量，不在本仓库另存第二份正文，避免与本次拆分要消除的重复副本问题重演。

| 序号 | 受管章节标题 | 脚本变量 |
|---:|---|---|
| 1 | 适用范围 | `BODY_SCOPE` |
| 2 | 注意 | `BODY_NOTICE` |
| 3 | Skill 强制自动触发规则（最高优先级） | `BODY_SKILL_AUTO` |
| 4 | 严禁脑补工具调用与结果（最高优先级，强制） | `BODY_NO_HALLUCINATE` |
| 5 | 严禁自动提交 Git（最高优先级，强制） | `BODY_NO_AUTO_COMMIT` |
| 6 | Skill 命中强制规则 | `BODY_SKILL_HIT` |
| 7 | 代码生成风格入口规则 | `BODY_CODE_GENERATION_STYLE` |
| 8 | Karpathy 风格硬闸门 | `BODY_KARPATHY_HARD_GATES` |
| 9 | 会话动态重命名规则 | `BODY_THREAD_TITLE` |
| 10 | 注释任务强制流程 | `BODY_COMMENT_TASK` |
| 11 | 上下文压缩续做规则 | `BODY_CONTEXT_COMPRESS` |
| 12 | 文件编码与写入规则 | `BODY_CHINESE_ENC` |
| 13 | 变更最小化 | `BODY_MIN_CHANGE` |
| 14 | 本地连接调试测试红线（最高优先级，强制） | `BODY_LOCAL_ONLY_CONNECTION` |
| 15 | 依赖与工具复用优先规则 | `BODY_REUSE_FIRST` |
| 16 | 最小实现优先级阶梯 | `BODY_MINIMAL_LADDER` |
| 17 | 输出格式规则 | `BODY_OUTPUT_FORMAT` |
| 18 | Windows / WSL 执行规则 | `BODY_WINDOWS_WSL` |
| 19 | CodeGraph 强制准备规则 | `BODY_CODEGRAPH` |
| 20 | 代码库探索规则 | `BODY_CODE_EXPLORE` |
| 21 | 插件检测安装规则 | `BODY_PLUGIN` |
| 22 | 图像生成强制规则 | `BODY_IMAGEGEN` |
| 23 | Godot 项目工具配置（仅 Godot 项目） | `GODOT_TOOLING_SECTION` |
| 24 | 图像生成配置（仅 Godot 项目） | `GODOT_IMAGEGEN_SECTION` |

另有两份非受管章节但同属规则文件组的静态内容：`GITATTRIBUTES_CONTENT`（两种换行符变体）、`EDITORCONFIG_CONTENT`（两种换行符变体），只在 `.gitattributes` / `.editorconfig` 缺失时首次写入，不走 `sync_section` 增量同步。
