# 调整来源记录

## 2026-08-28 内部调整：本轮 TAPD 任务闭环实操经验固化

**通道**：内部更新 + 执行中 gap 回补
**来源**：完成 TAPD 需求 `1162459836001001627`（地区需要增加到兑换流水）的真实执行过程，宿主项目 `ellipal_admin`
**诉求**：把「怎么找任务 / 怎么定性 / 怎么填评论 / 怎么改状态」的实操经验固化进本 skill，避免下次重踩

### 裁决表

| # | 条目 | 本地现状 | 裁决 | 落点 |
|---|---|---|---|---|
| 1 | 我名下的活在 story/bug，`task` 实体为空 | 第 3 步写 `task list`，方向错 | 修正 | SKILL.md §3 |
| 2 | story 按人筛选须用 `developer`，`current_owner` 静默失效 | 未提 | 合并 | cli-field-pitfalls §1 |
| 3 | `status="<>closed"` 排除已关闭；状态含自定义 `status_1~5` | 未提 | 合并 | cli-field-pitfalls §3 |
| 4 | 模糊查询 `name="~kw"` 不生效，须拉全量本地过滤 | 未提 | 合并 | cli-field-pitfalls §4 |
| 5 | 评论正文不能 shell 内联，会被 `---`/`\|` 静默截断 | 未提 | 合并 | cli-field-pitfalls §5 + SKILL.md §6 |
| 6 | 非交互 shell 不加载 `.bashrc` 导致环境变量缺失 | 仅泛指按 env-bootstrap 核对 | 合并 | cli-field-pitfalls §6 |
| 7 | 只有标题的老单先回仓库查现状，可能早已实现 | 判定表缺此类 | 合并（核心） | task-analysis-criteria §1/§3 + SKILL.md §5 |
| 8 | 需求终态 `story update ... status=resolved`，须核对返回体 | 只有 `progressing` | 修正 | SKILL.md §6 + cli-field-pitfalls §8 |
| 9 | 验证中发现顺带缺陷要问用户处置 | 未提 | 合并 | SKILL.md §6 + task-analysis-criteria §3 |
| 10 | 改动无对应单时先全量扫描证明，再问用户 | 未提 | 合并 | SKILL.md §7（新增） |
| 11 | `entry-type=stories`、Markdown 自动转 HTML | `tapd-cli` / `tapd-addcomment` 已写 | 保留本地 | — |
| 12 | 归项目过滤 | 第 4 步已有，本轮验证有效 | 保留本地 | — |
| 13 | 兜底清单排序 | §四已有 | 保留本地 | — |

净增减：新增 8 条 / 修正 2 处错误写法 / 保留 3 条不重复吸收。

### 同域冗余扫描

**范围**：`tapd-cli`、`tapd-openapi`、`tapd-env-bootstrap`、`tapd-addcomment`、`tapd-task-executor`

**发现 2 处、清理 2 处，PASS**：

1. **与权威冲突**：初稿在 cli-field-pitfalls §6 断言「WSL 内没有环境变量，不要去 WSL 补」，与 `tapd-env-bootstrap`（唯一权威）记载的「WSL 侧有真源 `~/.tapd/env.sh` + `.bashrc` 注入」矛盾。真实原因是非交互 `bash -lc` 不读 `.bashrc`。已改写为只记录现象与判断方向，配置事实收敛回 `tapd-env-bootstrap` 引用，不重复定义。
2. **重复造轮**：初稿用 Python subprocess 解决评论传参，而 `tapd-addcomment/scripts/add_comment.py` 原生支持 `--description -` 从 stdin 读取，文档明确标注「适合长文本 / 含特殊字符」。已收敛为「首选 addcomment stdin，tapd-cli 路径才用读文件传参」，格式细节引用 `tapd-addcomment` 不复述。

未发现门控层叠与散落产物。引用链可达、无断链、全部 UTF-8。

### 体积变化

| 文件 | 前 | 后 |
|---|---|---|
| SKILL.md | 5089 | 7809 |
| references/task-analysis-criteria.md | ~1100 | 3266 |
| references/cli-field-pitfalls.md | 新建 | 4950 |

净增约 9800 字节。本轮属实操经验首次固化，增量即新知识，无与兄弟 skill 重复的内容（同域扫描已清理 2 处）；CLI 陷阱集中收进 references 而非堆进 SKILL.md，主文件仍控制在 8KB 内。

### 未做

未跑 8 维评分棘轮验证——本 skill 无吸收前评分基线，按自动吸收例外通道同口径，改用结构校验（引用链 / 编码 / 体积 / 同域扫描）替代。

---

## 2026-08-28 内部调整（第二批）：交付链接与工时登记

**通道**：执行中 gap 回补 + 用户明确诉求
**来源**：本会话执行 TAPD 需求 1130399328001001399 过程中暴露的两个 gap

### 裁决表

| # | 条目 | 触发方式 | 裁决 | 落点 |
|---|---|---|---|---|
| 1 | 交付时必须给可点链接 + 所在项目 + 迭代归属 | 用户「我找不到你创建的缺陷」——只给裸 id 导致找不到，且它在非主项目、`iteration_id=0` 不进看板 | 合并 | SKILL.md §6 第 6 点 |
| 2 | `tapd-addcomment` 脚本不可用，评论统一走 tapd-cli 文件传参 | 实测 `add_comment.py:344` 字典缺逗号直接 `SyntaxError`，推翻第一批写的「首选 stdin」 | **修正** | cli-field-pitfalls §5 + SKILL.md §6 第 3 点 |
| 3 | 收口必须登记工时 | 用户明确要求 | 合并 | SKILL.md §6 第 5 点 + cli-field-pitfalls §8 |

### 工时规则的实测依据

规则口径不是自拟，全部来自实查团队既有记录与命令行为：

- **单位与粒度**：查 30399328 现有 timesheet，取值为 0.5 / 1 / 1.5 / 2 / 3，确认单位是小时、0.5 为最小粒度，无分钟或人天写法
- **`entity_type` 单数**：`timesheet add --help` 明确 `entity_type(story/task/bug)`，与评论的 `entry-type=stories` 复数不同
- **必须先查再写**：命令帮助声明「同一 entity_type+entity_id+spentdate+owner 只能有一条记录」；且实测发现**关单可能自动生成占位记录**——1001399（30399328）关单瞬间自动产生 `timespent=0` 记录（created 与关单 modified 同为 17:37:19），而 1001627（62459836）关单后查为 0 条，证明这是**项目级配置差异**，不能假设任一情况，故规则写成「查到则 update、没查到则 add」
- **list 参数约束**：只传 `entity_id` 不传 `entity_type` 会 422 `param entity_type is required`

### 同域冗余扫描

**范围**：`tapd-cli`、`tapd-openapi`、`tapd-env-bootstrap`、`tapd-addcomment`、`tapd-task-executor`

**发现 0 处，PASS**：`tapd-cli/SKILL.md` 的功能覆盖表里只有 `timesheet | add / list / update / count` 一行罗列，无参数语义与使用约束定义，本次新增的粒度、先查后写、占位记录等内容在同域内无第二处承载，不构成重复。链接格式在本 skill §3 已有一处，§6 第 6 点是引用而非重复定义。

### 用户明确的边界

前面已完成的 1001627 与 1001399 **不补工时**，规则自后续任务起生效。
