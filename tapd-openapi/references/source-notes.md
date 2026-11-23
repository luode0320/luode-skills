# TAPD OpenAPI 调整来源

## 2026-10-13：Bug 版本默认每次查询所属项目当前迭代

- 内部调整来源：用户在完成 NEXCHANGE(DEFI) 报价修复及 TAPD 补录后明确要求：“默认使用当前迭代，不是固定的，每次都需要重新查询该 Bug 所属项目的当前迭代。”
- 当次证据：项目接口存在两个同时标为当前的迭代，不能只取开启状态或最高版本；最终依据 Bug 修复小版本说明选定当次目标，并回读 `iteration_id` 与 `version_report`。该历史选择不是后续任务的固定默认值。
- 落点：主 SKILL 的关键规则 12、[版本规则](bug-version-and-current-iteration.md)、现有 [修复补录入口](completed-fix-and-timesheet.md)。保留该入口已存在的身份、工时和写入失败处理内容，不另复制。
- 同域边界：`tapd-cli` 负责客户端调用；`tapd-task-executor` 负责任务执行；Bug 默认版本策略只归 `tapd-openapi`。`mine` 的便捷当前迭代查询不替代写入裁决。
- 环境依赖：无新增环境配置，继续复用 `tapd-env-bootstrap` 的已有鉴权预检和 TAPD GET 接口；不保存凭据。agent 通用性：通用 HTTP/API、Markdown 规则，不绑定单一宿主。
- 验证与独立评分见 [吸收案例](case-current-bug-version.md)。

## 2026-10-13 已完成修复补录与工时登记

- 来源：本会话 EllipalFinance-go 空主币表修复后的 TAPD 补录，用户要求新增 Bug 并填 1 小时工时，随后授权吸收经验到 TAPD skill。
- 实证：[Bug 1130399328001004055](https://www.tapd.cn/tapd_fe/30399328/bug/detail/1130399328001004055)。创建及 GET 回读确认 reporter/current_owner 为罗德、status=resolved、resolution=fixed，描述含 c58fa653 和 32b3143c；timesheet 1130399328001008070 为 2026-10-13、timespent=1，匹配记录只有一条。
- 边界：代码级回归通过、运行服务未重启且 HTTP 接口未验收。此姓名和项目仅为案例，不是默认值。
- 内部调整：openapi 专用补录流程及状态/工时回读；CLI 只补 Windows/WSL UTF-8 临时脚本调用。身份、凭据和 API 字段仍引用原 Owner，修正 Bug 索引 5 个失效路径，补录与受委派执行分流。
- 语义澄清：本次实例曾同时填 effort=1 和实际 1 小时；后续仅要求已完成修复工时时只填 timespent，明确要求预估时再写 effort，不照抄双填。
- 裁决与验证：[吸收裁决表](../workbuddy-absorption-map.md)、[案例与校验](case-tapd-openapi-absorption.md)。

## 2026-10-19 TAPD 操作统一 CLI 优先（已被 2026-11-23 决定取代）

- 来源：用户指出 TAPD 任务误走浏览器并要求修正规则，使 CLI 成为默认通道，只有 CLI 无法处理时再回退。
- 裁决与落点：当时以 CLI → 直接 OpenAPI → 浏览器作为回退顺序；该顺序已被 2026-11-23 用户要求取代，只保留历史来源意义，不再作为现行路由规则。
- 现行规则以本文件下一条 2026-11-23 记录为准：TAPD 强制使用 `tapd-cli`，绝对禁止浏览器。

## 2026-11-23 TAPD 强制 CLI、绝对禁止浏览器

- 来源：用户明确要求再次优化 TAPD skill 规则，“绝对不要使用浏览器，必须强制使用 cli”。
- 本地现状：五个 TAPD skill 与 `authenticated-url-routing-rules` 仍保留 CLI → 直接 API → 浏览器三级回退；`browser-session-automation-rules` 还保留 TAPD 页面周报脚本与自动化流程参考。
- 裁决与落点：以 `tapd-openapi/SKILL.md` 为 TAPD 通道权威，统一改成命令行唯一入口；同步更新 `tapd-cli`、`tapd-addcomment`、`tapd-task-executor`、`authenticated-url-routing-rules`。删除 `browser-session-automation-rules` 的 TAPD 自动化参考与 TAPD 周报模板，从浏览器 skill 中移除 TAPD 入口。
- 能力边界：`tapd-cli` 没有工作流转换规则查询子命令。规则改为先读当前状态与字段候选，再逐跳更新并回读，不把缺失能力转成浏览器或直接 API 回退；该缺口如实交给用户，不伪造已查询。
- 整理去重：五个 TAPD skill 的通用“浏览器仅用于页面专属操作”句收敛为同一口径“TAPD 不开放浏览器”；删除任务执行器中的 `tapd_client_stdlib.py mine` 直接 API 补位，改用 `tapd-cli` 分页拉取后本地筛选。
- 环境依赖与通用性：无新增环境配置，复用 `tapd-env-bootstrap` 的既有 CLI 凭据预检；不绑定单一 agent。
- 验证：结构校验、字典刷新与残留扫描见本轮收口记录；未对真实 TAPD 实体执行写操作，仅使用 CLI 帮助命令核验能力边界。
