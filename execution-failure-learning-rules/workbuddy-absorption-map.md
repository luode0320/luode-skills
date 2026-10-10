# workbuddy-absorption-map

本文件登记 `execution-failure-learning-rules` 的吸收/调整裁决历史（外部吸收 + 内部更新 + 执行中 gap 回补）。

## 2026-10-08 执行中 gap 回补：owner 取 frontmatter name 与历史 owner 承接

| 来源 | 条目 | 本地现状 | 裁决 | 落点 | 整理去重 | 环境依赖 | agent 通用性 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 用户 2026-10-08 指令；知识库 `20-Knowledge/execution-failure-cases/` 目录现状 | owner 一律取 frontmatter `name`，不取仓库目录名；`owner_skill`、`case_key` 首段与知识库 `<owner>/` 目录名同值；两者不一致时按 `^name:` 反查 | 路由表只写 owner 名，没说明与目录名的对应；`wsl-windows-bridge`（目录 `wsl-windows-bridge__skillhub`）、`powershell`（目录 `powershell__skillhub`）名与目录不同，去后缀推导会误判 `py__skillhub`（`name` 是 `python`） | 合并 | `references/classification-and-routing.md`「唯一 owner 规则」第 6 条 | N/A：新增通则，无同义旧条可并 | N/A：纯规则口径 | 通用 |
| 同上 | 路由表注明「原 X 已删除」的 X 是历史 owner：旧案例原地保留、只追加，同行写明拆分承接的按内容归对应 owner；去重与检索同时查承接 owner 和历史 owner 目录，比对历史目录时 `owner_skill` 段视同承接 owner、枚举外的旧 `category` 不比对；命中只更新出现次数、验证时间、来源并追加状态事件，这是模板「不能修改其他 skill 的案例正文」的唯一例外；新案例只写承接 owner | 知识库 `windows-wsl-execution-rules/` 下 2 篇旧案例，`owner_skill` 与 `case_key` 首段都是 `windows-wsl-execution-rules`、`category` 都是枚举外的 `command`，按新 owner 或完整去重键都查不到；路由表第 29 行已写「原 `windows-wsl-execution-rules` 已删除」 | 合并 | 同上第 7 条；具体映射复用第 29 行既有文字 | 复用既有注明，不另建映射表 | N/A | 通用 |
| 独立评分问题清单（2026-10-08） | `case-template.md` 的 `owner_skill`、`note_path` 字段看不到第 6 条，照模板写入的 agent 可能取目录名 | 模板只写「唯一 owner skill」，未说取值来源 | 合并 | `references/case-template.md` 第 5 行补一句指向第 6 条 | 只加指针，取值规则仍只在第 6 条（单一权威） | N/A | 通用 |
| 存量整理 | 第 3 行「具体案例由 owner skill 的 casebook 保存」，与 SKILL.md、`lifecycle-and-gates.md`（知识库是动态案例唯一事实来源）冲突 | 过时口径 | 合并（改写） | 同文件第 3 行：案例写入知识库，casebook 只作种子与回归基线 | 消除 1 处跨文件口径冲突 | N/A | 通用 |

- 环境依赖登记：0 项（纯规则口径，不涉及环境变量、配置、hook、依赖或路径引用）。
- 同域冗余扫描：范围 = 本 skill 的 SKILL.md、`lifecycle-and-gates.md`、`case-template.md`，`knowledge-flow` 的 `references/execution-case-notes.md`，知识库 7 个 owner 目录。owner 命名口径无重复段落（`execution-case-notes.md` 第 10 行「owner 为负责该案例的 skill 名」与第 6 条一致）；知识库逐篇核对 `owner_skill` 与 `case_key` 首段，与目录名不一致 0 处；仓库内把 `__skillhub` 目录名当 owner 的写法 0 处（去掉该限定的对照检索命中 13 处）。无门控层叠，无散落产物，引用链可达。**PASS**。
- 范围外遗留（另开任务）：第 4、5 条仍写 casebook 旧口径，与 `lifecycle-and-gates.md` 第 65 行冲突；第 47 行 Git Bash 路径疑似误写成对反斜杠；`case-template.md` 的 `id` 格式写 `<owner>-...`，知识库实际是 `YYYYMMDD-HHMMSS-exec-case-<slug>`；`knowledge-flow/references/execution-case-notes.md` 的状态事件格式、candidate 含义和写入工具三处与本 skill 口径不一致。
- 独立评分（只读子代理，未参与修改；改前按 HEAD，改后按工作树）：8 维改前 → 改后依次为 8→8、9→9、8→9、8→8、8→9、8→8、8→9、4→8，加权总分 71.5 → 85.5（+14.0）；只看维度 1–7 也从 61.5 升到 65.5（+4.0），棘轮通过，保留。评分者的改前分比本轮基线 75.5 低 4.0，因为它对照了第 3 行与 SKILL.md、生命周期文件的口径冲突，并用 E 场景核对了知识库实际数据；沿用基线时提升 10.0，结论不变。维度 8 为场景推演暂定分（E1–E3 改前通过 1/3、改后 3/3）。评分针对下一条修正之前的版本，修正后未再独立复评。
- 评分问题处置：与本 skill 相关的 4 项全部修正。第 7 条补了跨目录命中判据：`owner_skill` 段视同承接 owner，枚举外的旧 `category` 不比对。补了拆分承接：同行写明的按案例内容归对应 owner。写明追加状态事件是模板「不能修改其他 skill 的案例正文」的唯一例外。模板加了指向第 6 条的指针。
- 结构校验：`quick_validate.py execution-failure-learning-rules` 输出 `Skill is valid!`，EXIT=0，评分问题修正后重跑结果相同；description 与 `##` 标题未改，未重跑字典。
- 净增体积：`references/classification-and-routing.md` 7,405 → 8,855 字节（+1,450）；`references/case-template.md` 4,971 → 5,223（+252）；本登记文件新建。
- 来源记录：执行中 gap 回补，诉求「核对 owner 名与目录名的对应关系，以及已删除旧 owner 留在知识库的 2 篇案例是否要在路由表写明」（用户 2026-10-08 指令）。不新建 `references/source-notes.md`：字典脚本扫描 `references/` 文件列表，新增文件会改变字典输出，而 `skill-dictionary/data.js`、`字典.md` 正被其他会话修改，重跑会碰到他人改动，故来源记录并入本文件。
