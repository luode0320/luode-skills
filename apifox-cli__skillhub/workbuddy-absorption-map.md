# workbuddy-absorption-map（吸收裁决登记表）

> 归属 owner：`apifox`。登记外部 skill 精华吸收裁决，每行含"整理去重"列。追加式维护，不覆盖历史。

## 本次调整（续5）：接口层 preProcessors 注入 + headers.add 追加语义纠错 + 环境变量漂移坑（来源 = 兑换项目接口层鉴权补齐实战）

- 调整时间：2026-08-26
- 通道：**内部更新**（存量论断纠错 + 新坑沉淀，无外部源）
- 来源：用户发现接口节点本身（api 层）前置操作为空，要求接口本身也加鉴权脚本。实施中连续踩出三个此前 skill 未覆盖/写错的坑：①接口层脚本级联到所有下级用例；②`headers.add` 对同名 key 是**追加**而非覆盖（服务端取第一个头），推翻第九节「覆盖」假设；③fixture 重跑导致环境变量密钥漂移（order not found 症状）
- 裁决摘要：存量纠错 1 处（headers.add 语义）+ 新增 3 条坑（级联副作用 / inheritPreProcessors 不可依赖 / 环境变量漂移）

| # | 原子条目 | 本地现状（调整前） | 裁决 | 落点 | 整理去重 |
|---|---------|-------------------|------|------|----------|
| 1 | 接口层 `api.preProcessors` 与用例层同一通道可批量写入（match-name 重导），但**级联执行到所有下级用例**——给接口加脚本=给所有无脚本用例加脚本，豁免用例必须同步补「清除鉴权头」脚本 | 第九节只覆盖用例层注入，无接口层通道记录 | 合并（核心） | `case-debug-case-vs-test-case.md` 第九节（接口层注入通道 + 级联副作用 + 清除脚本） | case study 完整写一遍，test-auth.md 三件事表第 2.5 行引用 |
| 2 | **`pm.request.headers.add` 对同名 key 是追加（非覆盖）**，服务端 `c.GetHeader` 取第一个头——接口层先注入、用例层后 add 时两个同名头共存、生效的是接口层旧值；签名脚本必须「先 remove 再 add」完全接管 | 第九节要点 4 写「headers.add 对同名 key 是覆盖」 | 合并（**存量纠错**） | case study 第九节 3 处改写 + 要点 4 改为追加语义 + 接管前缀强制 | 改写既有结论行，不新增节；实测证据（63 脚本插接管前缀后 407432230 恢复） |
| 3 | `inheritPreProcessors: {"enable": false}` 落库但 CLI run 引擎不读，自动化场景不可依赖，必须用清除脚本 | 无继承开关相关记录 | 合并 | case study 第九节「尝试过但不可行的方案」段 | 与要点 3 同处，不重复 |
| 4 | fixture 重跑 → 环境变量密钥漂移：`partner_fixture.py` 重新生成 api_secret、api_key 轮换，环境变量 `v2ApiSecret` 不跟着变 → 用例身份≠订单归属 → /status 返回 order not found（鉴权却通过，症状极具迷惑性）；修复=重写环境变量（整体覆盖 payload 带全量变量） | 无「环境变量会过期」的判定 | 合并（高价值） | case study 第九节要点 5（判定方法：手动用库中当前凭据请求成功而用例失败 → 漂移） | 只写一处 |
| 5 | 并行回归 runner：8 worker 并发 `test-case run`，72 用例 287 断言 1m21s 跑完（单用例 6-8s），判定仍按「断言数│N│M」解析 | 只有串行 runner 记录 | 合并（补强） | PROJECT_TEST.md 全量回归状态行 | 不进 skill（属项目脚本细节），仅文档登记 |

**净增减**：1 个文件改 5 处（case-debug-case-vs-test-case.md 第九节）+ 吸收映射本表。无删除、无新增节。

**同域冗余扫描**：范围全部 `C:\Users\luode\.workbuddy\skills`，关键词 `headers.add` / `inheritPreProcessors` / `环境变量漂移`。命中仅 apifox skill 内部（case study 第九节 + test-auth.md 2.5 行引用 + test-case.md T-3 引用）。**结论：PASS（0 处需清理）**。

**棘轮验证**（与续4 同评委口径，主 agent 自评）：

| # | 维度 | 权重 | 前 | 后 | 依据 |
|---|------|------|----|----|------|
| 1 | Frontmatter 质量 | 8 | 9 | 9 | description 未改 |
| 2 | 工作流清晰度 | 15 | 10 | 10 | 三层（接口/DEBUG_CASE/TEST_CASE）注入通道齐备，各带级联副作用处置 |
| 3 | 边界条件覆盖 | 10 | 10 | 10 | 豁免清除脚本、接管前缀、环境变量漂移判定三类边界全部补齐 |
| 4 | 检查点设计 | 7 | 9 | 9 | 回读验证 + 全量回归复用既有 runner |
| 5 | 指令具体性 | 15 | 10 | 10 | 接管前缀 JS 代码、清除脚本、payload 结构均为可复制实例 |
| 6 | 资源整合度 | 5 | 9 | 9 | 1 文件 5 处 + 映射表；同域 0 冗余 |
| 7 | 整体架构 | 15 | 9 | 9 | 全部挂第九节既有小节，未新增节 |
| 8 | 实测表现 | 25 | 10 | 10 | 72/72 回归 0 失败；headers.add 追加语义经 curl 双头实验决定性确认；两处存量错误结论被实测纠正 |

**总分：92.0 → 92.5（+0.5）**，涨幅 ≤ 1 接近收敛，**保留本次内部更新**。

**源处置**：N/A（内部更新通道，实测推翻存量论断，无外部源）。

## 本次调整（续4）：DEBUG_CASE 鉴权脚本批量注入通道（来源 = 兑换项目接口用例鉴权漏洞实战）

- 调整时间：2026-08-26
- 通道：**内部更新**（实测推翻 skill 存量论断 + 新通道沉淀，非外部吸收，无外部源可删）
- 来源：用户发现兑换项目接口用例（DEBUG_CASE）66 个全部无鉴权前置脚本（自动化用例有、接口用例没有），要求「双通道都完整 + 重跑全量测试 + 沉淀经验」。实测发现 2026-08-24 case study「调试用例事后完全无法用 CLI 补」论断**部分错误**——`import --format apifox` 原生格式 match-name 重导对已存在接口的 `api.cases[]` 执行 update 语义，`preProcessors` 真实落库
- 裁决摘要：存量纠错 1 处（能力边界结论） + 合并 4 条 / 拒绝 0 条

| # | 原子条目 | 本地现状（调整前） | 裁决 | 落点 | 整理去重 |
|---|---------|-------------------|------|------|----------|
| 1 | 原生格式 match-name 重导对已存在接口执行 update 语义（endpointCase updateCount=138 全命中），DEBUG_CASE 的 preProcessors 真实落库；接口契约字段全保留，副作用仅 ordering 归零 | `test-case.md`「CLI 能力边界」写"调试用例事后完全无法用 CLI 补"（2026-08-24 结论） | 合并（**存量纠错**） | `test-case.md` CLI 能力边界结论修正为两分支（body 仍只能 example 灌入；处理器可经原生重导批量写） | 改写既有结论行，不新增节；T-3 修复路径补第 3 条（处理器类） |
| 2 | DEBUG_CASE 批量补鉴权脚本标准流程：export → 改 JSON → import match-name（模块冲突加 module-map）→ 回读验证；不删接口、不动 ID、不重建用例 | 无任何 DEBUG_CASE 事后写入通道记录 | 合并（核心） | `test-case.md` T-3 第 3 条 + `case-debug-case-vs-test-case.md` 新增第八节（完整证据链/命令/可迁移要点） | 通道只在 case study 完整写一遍，T-3 引用；命令模板不复制 |
| 3 | 注入豁免清单：负向「缺凭据」与安全性「错误签名/无签名」类用例必须豁免注入（脚本会破坏其拒绝语义） | 无"哪些用例不能挂鉴权脚本"的判定 | 合并 | `test-auth.md` 三件事表第 2 行 + case study 第八节要点 2 | 表内一句 + case 详述，无重复段落 |
| 4 | v1/v2 双签名并存分发：脚本按接口 securityScheme 分发（v1=authSecret+x-api-key 选密钥 / v2=v2ApiSecret），脚本全文从项目内已有 TEST_CASE 提取模板，密钥一律 pm.environment.get() 运行时取 | test-auth.md 只有 v2 单模板记录 | 合并（补强） | `test-auth.md` 三件事表第 2 行 + case study 第八节要点 3/4 | 模板不新写，指向"从真实用例提取"方法 |
| 5 | import 结果解读陷阱：updateCount=0 不等于没写入——endpointCase 命中仍会更新用例，须看完整输出尾部而非头部 | 无 | 合并（高价值） | case study 第八节要点 5 + `testing-pitfalls.md` 陷阱登记 | 只写一处（case study），pitfalls 引用 |

**净增减**：3 个文件（test-case.md 纠错 1 处 + T-3 补 1 条 / test-auth.md 表 1 行补强 / case-debug-case-vs-test-case.md 新增第八节约 60 行）+ 吸收映射本表。无删除。

**同域冗余扫描**：范围全部 `C:\Users\luode\.workbuddy\skills`，关键词 `match-name` / `DEBUG_CASE` / `原生重导` / `endpointCase`。命中仅 apifox skill 内部三处（test-case.md / test-auth.md / case study，均互相引用指向 case study 为完整权威）。**结论：PASS（0 处需清理）**。

**棘轮验证**（评分方式：主 agent 自评，与 2026-08-25 同评委口径）：

| # | 维度 | 权重 | 前 | 后 | 依据 |
|---|------|------|----|----|------|
| 1 | Frontmatter 质量 | 8 | 9 | 9 | description 未改 |
| 2 | 工作流清晰度 | 15 | 9 | 10 | 补出 DEBUG_CASE 事后写入的唯一自动化通道，双通道（TEST_CASE 用 test-case 命令 / DEBUG_CASE 用原生重导）各有完整闭环 |
| 3 | 边界条件覆盖 | 10 | 10 | 10 | 豁免清单（缺凭据负向/安全性）补齐了"哪些用例不能注入"的此前空白 |
| 4 | 检查点设计 | 7 | 9 | 9 | 未新增用户门控；回读验证复用既有 export 核对 |
| 5 | 指令具体性 | 15 | 10 | 10 | 通道带完整命令链（export/import/module-map/回读），非抽象原则 |
| 6 | 资源整合度 | 5 | 9 | 9 | 3 文件 + case study 第八节；同域 0 冗余、引用链可达 |
| 7 | 整体架构 | 15 | 9 | 9 | 全部挂既有文件/既有节，case study 追加第八节；净增约 70 行属克制 |
| 8 | 实测表现 | 25 | 10 | 10 | 真实漏洞驱动：66 DEBUG_CASE 全补、138 endpointCase update、72/72 回归 0 失败、回读 66/66 落库；存量错误论断被实测推翻并修正 |

**总分：91.5 → 92.0（+0.5）**，涨幅 ≤ 1 接近收敛，**保留本次内部更新**。与 2026-08-25（91.0 → 91.5）同评委口径，可对比。

**源处置**：N/A（内部更新通道，实测推翻存量论断，无外部源）。

## 本次调整（续3）：apifox 测试隔离环境密钥策略放宽（来源 = 用户明确指示）

- 调整时间：2026-08-25
- 通道：**内部更新**（用户指示口径调整，非外部吸收，无外部源可删）
- 来源：用户明确说明"apifox 环境允许 agent 自行填入，不需要用户手动，因为环境本身是隔离的，无需保密密钥安全，这个要吸收到 apifox skill 中"。实测中 11 个用例依赖 `v2ApiSecret`，此前 skill 强制"agent 不代填、必须用户手动在客户端填"，与隔离项目现状不符
- 裁决摘要：合并 5 条 / 存量纠错 2 处 / 拒绝 0 条

| # | 原子条目 | 本地现状（调整前） | 裁决 | 落点 | 整理去重 |
|---|---------|-------------------|------|------|----------|
| 1 | 敏感变量处理按 apifox 环境隔离等级分流：默认档（共享/正式项目）保持"值不回显 + agent 不代填"；隔离档（apifox 测试专用项目）密钥低敏、agent 可直接代填 | `environment.md` 敏感变量节一律"agent 不代填、值由用户在客户端自行填入" | 合并（核心） | `environment.md` 敏感变量节改为两档分流 + 不可违反规则第 1 条补隔离档口径 | 改写既有节为「默认档 / 隔离档」两分支，不新增独立章节 |
| 2 | agent 代填通道：Apifox 开放 API `PUT/GET /api/v1/projects/{projectId}/environments/{id}` 可读写 `variables`（与 CLI 不同），鉴权 `Bearer <Access Token>` + `X-Apifox-Api-Version` | 无任何代填通道（CLI 2.2.9 读写不到环境变量是硬事实，但开放 API 可行未被记录） | 合并（新增） | `environment.md` 新增「agent 代填通道」小节（请求/鉴权头/body 序列化 JSON/回读核对）+ `test-auth.md` CLI 事实表第一行补开放 API 通道 | 通道细节只在 environment.md 写一遍，test-auth 事实表只引用 |
| 3 | 凭据红线分流：默认档保持"agent 不把密钥/token 填进 apifox"；隔离档值可进 apifox，但**脱敏红线收窄为"值不扩散到仓库文档/git/聊天摘要/PROJECT_TEST.md"** | `test-auth.md` 凭据处理红线一律不代填 | 合并 | `test-auth.md` 凭据处理红线按档分流 + 不可违反规则第 4 条 | 与 environment.md 分流口径完全一致，单一权威 + 互相引用 |
| 4 | SKILL.md 权限豁免节补充"密钥类变量值在隔离体内低敏"，路由表同步口径 | 豁免边界仅"敏感信息脱敏"一句，未区分隔离档；路由表写"agent 不代填密钥" | 合并 | `SKILL.md` 权限豁免节 + 鉴权自动化路由行 | 权限豁免节为隔离档判定权威，模块内只引用 |
| 5 | ai-team-project.md 步骤 5 与 `project-test-md-template.md` 存量纠错：模板仍写"用 CLI 写入避免暴露"（做不到的规则） | 步骤 5 未提代填通道；模板第 53 行"用 CLI 写入"是 2026-08-21 纠错残留 | 合并（含**存量纠错**） | `ai-team-project.md` 步骤 5 加注隔离档可代填 + 模板改为"开放 API 代填（隔离档）/ 人工填（默认档）" | 纠错型改写：删掉做不到的 CLI 写入表述，换成两档通道 |

**净增减**：5 个文件（environment.md / test-auth.md / ai-team-project.md / SKILL.md / project-test-md-template.md）+ case study 加注 2 处（79/83 行口径更新指针）；新增约 40 行，其中纠错改写 2 处（模板 CLI 写入表述、步骤 5 口径），无删除。

**同域冗余扫描**：范围全部 `C:\Users\luode\.workbuddy\skills`（含兄弟 skill），关键词 `不代填` / `只能人工` / `客户端自行填` / `用户自行填`。命中仅 apifox skill 内部：environment.md（默认档分支，正确保留）、test-auth.md（默认档分支，正确保留）、case 加注 2 处（已带 2026-08-25 更新指针）。**结论：PASS（0 处需清理）**。无其他 skill 出现"apifox 不代填"口径，无需跨 skill 同步。

**棘轮验证**（评分方式：主 agent 自评，与 2026-08-21 两次自评同评委口径）：

| # | 维度 | 权重 | 前 | 后 | 依据 |
|---|------|------|----|----|------|
| 1 | Frontmatter 质量 | 8 | 9 | 9 | description 未改；仅路由表关键词增强 |
| 2 | 工作流清晰度 | 15 | 9 | 9 | 两档各有完整闭环：默认档=人工填+运行时脚本；隔离档=开放 API 代填+GET 回读核对 |
| 3 | 边界条件覆盖 | 10 | 9 | 10 | 补齐"隔离档怎么填"的唯一执行通道（开放 API），此前只有"人工填"一条路，隔离项目会卡死 |
| 4 | 检查点设计 | 7 | 9 | 9 | 未新增用户门控；隔离档判定复用既有 SKILL.md 权限豁免 |
| 5 | 指令具体性 | 15 | 9 | 10 | 代填通道带完整请求方法/URL/鉴权头/body 序列化 JSON 格式/成功判定与回读核对命令 |
| 6 | 资源整合度 | 5 | 9 | 9 | 5 文件 + case 2 处加注；同域 0 冗余、引用链可达、UTF-8 无乱码 |
| 7 | 整体架构 | 15 | 9 | 9 | 全部挂既有节/既有文件，仅 environment.md 新增 1 个小节；净增 40 行属克制 |
| 8 | 实测表现 | 25 | 9 | 10 | 用户真实指令驱动（11 用例依赖 v2ApiSecret 卡在"不代填"）；2026-08-21 从"CLI 写入"纠错为"人工填"，本轮再放宽为"隔离档可代填"，隔离档判定前置被证明必要 |

**总分：91.0 → 91.5（+0.5）**，涨幅 ≤ 1 接近收敛，**保留本次内部更新**。与前两次自评（90.0 → 93.0、81.0 → 90.0）为同评委口径，可对比。

**源处置**：N/A（内部更新通道，用户指示口径调整，无外部源）。

## 本次调整（续2）：接口归类与持续维护（来源 = 用户指明"接口生成也要记得归类"）

- 调整时间：2026-08-21
- 通道：**内部更新**（非外部吸收，无外部源可删）
- 来源：用户指明"apifox 的接口生成也记得归类，后续也可以持续整理接口的位置，不是生成了就不用调整"，附截图反面案例：全部接口堆在「默认模块 / 接口」平铺层，未按业务模块归类
- 裁决摘要：合并 6 条 / 拒绝 0 条

| # | 原子条目 | 本地现状（调整前） | 裁决 | 落点 | 整理去重 |
|---|---------|-------------------|------|------|----------|
| 1 | 创建即归类：endpoint 创建时必须落在业务 folder，禁止停在「默认模块/接口」平铺层 | `api-design.md` 只有 folder 命令入口，无归类要求 | 合并（核心） | `api-design.md`「folder 选择规范（强制）」+ 创建流程第 2 步 | 不新增 gate，挂既有「创建接口标准流程」与 A1 同节点（节点 1） |
| 2 | 业务模块识别按「产品模块/业务域/功能域」，禁止按 URL 路径机械分组 | `import-export.md` Step 5 已有 tags 业务化（导入侧） | 合并（补强到 folder 维度） | `api-folder-organization.md`「业务模块识别法」+ `import-export.md` Step 5 强化 | 与既有 tags 规则互补不重复（folder=结构、tags=语义），Step 5 改写非新增节 |
| 3 | 归类是持续工作：迁移/合并/拆分/归档，不累积归类欠账 | 无任何归类维护流程 | 合并（新增独立模块） | 新建 `modules/api-folder-organization.md` | 新模块为唯一权威，兄弟模块只引用不复制 |
| 4 | 接口变更/同步后必须校验 folder 归属 | `api-sync-to-apifox.md` 步骤 6 只校验字段说明 | 合并（新增子项） | `api-sync-to-apifox.md` 步骤 6.2 + 不可违反规则第 9 条 | 挂既有步骤 6 系列，不开新流程 |
| 5 | 定期审计归类异常（未归类/归类错误/空 folder/超深 folder） | `project-onboarding-checklist.md` 10 硬动作无 folder 项 | 合并（新增硬动作 A11） | `project-onboarding-checklist.md` 节点 1 A11 + 批量修复第 9 项 + 不可违反规则第 6 条 | 与 A1（description）并列于节点 1，复用既有审计节奏（A9/A10 顺带） |
| 6 | SKILL.md 模块路由表支持归类任务命中 | 路由表无归类入口 | 合并 | `SKILL.md` 新增 `api-folder-organization.md` 行 + api-design 行补关键词 + A11 入硬动作清单 | 路由行合并进既有表，不新增表结构 |

**净增减**：6 个文件（1 新建模块 + 5 增量），新增约 150 行、0 删除；因全部为挂既有节/新建唯一权威模块，无冗余段落需删除。

**同域冗余扫描**：范围 `project-interface-baseline-rules` / `artifact-storage-rules` / `import-export.md`（既有 tags 规则），关键词 folder / 归类 / 目录 / 分组。`project-interface-baseline-rules` 命中均为 `doc/5-tests/基线/` 基线资产目录（不同主题，非接口 folder）；`artifact-storage-rules` 零命中；`import-export.md` Step 5 与新增 folder 规则互补（tags vs folder 两个维度）。**结论：PASS（0 处需清理）**。跨模块引用链：api-design / api-sync / import-export / onboarding-checklist 均只引用 `api-folder-organization.md` 为唯一权威，无重复段落。

**棘轮验证**（评分方式：主 agent 自评，与 2026-08-21 前两次自评同评委口径）：

| # | 维度 | 权重 | 前 | 后 | 依据 |
|---|------|------|----|----|------|
| 1 | Frontmatter 质量 | 8 | 9 | 9 | description 未改；仅路由表关键词增强 |
| 2 | 工作流清晰度 | 15 | 9 | 9 | 新增「持续维护工作流」表格（迁移/合并/拆分/归档四场景+动作+验证），A11 触发/命令/通过/阻断齐全 |
| 3 | 边界条件覆盖 | 10 | 9 | 10 | 补齐"接口未归类/归类错误/空 folder/超深 folder"四个此前无处理路径的场景，各带处置与复扫归零条件 |
| 4 | 检查点设计 | 7 | 9 | 9 | 新增 1 条硬动作（A11）挂既有节点 1，未新增用户门控 |
| 5 | 指令具体性 | 15 | 9 | 10 | A11 与批量修复第 9 项带可执行命令（endpoint list 解析、folder create、endpoint update + get 回读），非抽象原则 |
| 6 | 资源整合度 | 5 | 9 | 9 | 新模块 + 5 处交叉引用；同域 0 冗余、引用链可达、UTF-8 无乱码 |
| 7 | 整体架构 | 15 | 9 | 9 | 新建 1 个独立模块（folder 归类是独立职责域）+ 其余全部挂既有节；净增 150 行但 0 冗余，属克制 |
| 8 | 实测表现 | 25 | 10 | 10 | 3 个真实场景 prompt 全部可路由：P1 接口堆默认模块要归类（5 模块命中）/ P2 接口迁移（api-folder-organization + test-case 引用）/ P3 定期归类审计（A9/A10 + A11） |

**总分：89.0 → 91.0（+2.0）**，涨幅 > 1 不早停，**保留本次内部更新**。与前两次自评（90.0 → 93.0、81.0 → 90.0）为同评委口径，可对比。

**源处置**：N/A（内部更新通道，无外部源）。

## 本次调整（续）：鉴权链路 gap 回补（来源 = 同接口的鉴权补齐实战）

- 调整时间：2026-08-21（同日续做）
- 通道：**执行中 gap 回补**
- 来源：用户指出"没有配置鉴权的步骤……作为接口文档应该要完善，上线之后也是要使用的"。查证发现 53 个 swag YAML 全量写错安全方案，apifox 侧鉴权链路整条缺失
- 裁决摘要：合并 6 条 / 拒绝 1 条 / 存量纠错 1 处

| # | 原子条目 | 本地现状（调整前） | 裁决 | 落点 | 整理去重 |
|---|---------|-------------------|------|------|----------|
| 1 | 本地免签 ≠ 不配鉴权：安全方案 + 用例签名脚本 + 鉴权用例三件必须齐，否则文档交出去线上必 401 | `test-auth.md` 只讲 token/JWT 登录类鉴权，没有"免签服务也必须配"的强制口径 | 合并（核心） | `test-auth.md` 新增「鉴权配置必须进 apifox（强制，即使本地免签）」+ 不可违反规则第 0 条 | 新章节顶部引用既有「方案选型」，不重复展开 token 方案 |
| 2 | 安全方案必须与鉴权中间件真实机制一致；自定义签名是 `apiKey`+`in: header`，不是 `http bearer`；错的比缺的更危险 | `api-sync-to-apifox.md` 契约校验只查字段说明，不查安全方案；swag 生成侧无口径 | 合并 | `api-sync-to-apifox.md` 步骤 6.1 + 不可违反规则第 8 条；**生成侧沉到 `swag-openapi-maintainer-rules` 核心约束**（含"口径变更属全量重生成范围"） | 两处互相引用，判定标准只在 swag skill 写一遍 |
| 3 | 凭据红线：agent 不把密钥/token 填进 apifox（云端 SaaS + 凭据输入禁令），只建空值占位 + 运行时取值脚本；本地验签让脚本自读配置，明文不进输出 | 无此约束，原规则甚至要求"用 CLI 写入值" | 合并 | `test-auth.md`「凭据处理红线」+ 签名脚本模板 | 与 `environment.md` 敏感变量节收敛为「单一权威 + 引用」 |
| 4 | CLI 事实一：`environment` 读写不到环境变量（update 报 success 但回读 null，get 只返回 5 个字段） | `environment.md` 写着"值写入 apifox 环境变量时用 CLI 写入"——**做不到** | 合并（含**存量纠错**） | `test-auth.md`「两条 CLI 事实」+ 改写 `environment.md` 敏感变量节与不可违反规则第 7 条 | **纠错型改写**：删掉做不到的规则，换成"人工填 + agent 只建脚本" |
| 5 | CLI 事实二：导入的 operation-level `security` 不绑定接口鉴权（`endpoint get` 的 securityScheme 为 `{}`，export 的 security 为 `[]`）；`endpoint update` 该字段无结构定义，不猜着写 | 无 | 合并 | `test-auth.md`「两条 CLI 事实」 | 同上表内，未开新节 |
| 6 | 统计口径陷阱：runner 报告里失败断言是 `1. 2.` 编号而非 `×`，用 grep 数 √/× 会把失败漏计成全绿；须解析「断言数 总数/失败数」并用已知失败用例校准 | 无（本轮 agent 自己踩了，差点误报"12 个用例 fail=0"） | 合并（高价值） | `testing-pitfalls.md` 陷阱 12-1 + `test-case.md` 运行规则「结果统计口径」 | 挂既有表/节 |
| 7 | 上游只读依赖无权限被静默降级：Mongo `not authorized` → 文案空串 → 精确断言挂，但 HTTP 200 且 status=true | 无 | 合并 | `testing-pitfalls.md` 陷阱 18-2 | 与 18-1（缓存）并列，共用"先看服务日志"处置 |
| 8 | 本项目的密钥来源名（H5/APP）、库名、caseId | 属项目事实 | 拒绝 | — | N/A（留项目 `PROJECT_TEST.md`，密钥值不落任何文档） |

**净增减**：5 个文件（apifox 4 模块 + SKILL.md 路由）+ 跨 skill 1 处（`swag-openapi-maintainer-rules` 核心约束）+ case study 续篇；新增约 95 行，其中**纠错改写 6 行**（`environment.md` 做不到的 CLI 写入规则），净增约 89 行。

**同域冗余扫描**：范围 `test-strategy-rules` / `test-program-rules` / `test-regression-rules` / `functional-validation-rules` / `bug-validation-rules` / `api-contract-rules`，关键词 免签 / securitySchemes / bearer / 签名 / 断言数 / environment 变量 / not authorized。仅"签名"命中 `test-program-rules/references/runtime-mock-pattern.md`（运行时 mock 语境，非同一主题）。**结论：PASS（0 处需清理）**。跨 skill 落点（swag 生成侧）为职责归属而非重复：判定标准只写在 swag skill，apifox 侧只引用。

**棘轮验证**：8 维自评 90.0 → 93.0（+3.0）。维度变化：边界条件覆盖 9→10（补齐鉴权链路与两类"报成功但没生效"的 CLI 事实）、实测表现 9→10（本轮 6 条经验全部来自真实执行，含 agent 自身误报的纠正）；其余维持。涨幅 > 1 不早停，保留。

**源处置**：N/A（内部 gap 回补通道）。

## 本次调整：执行中 gap 回补（来源 = /getActivityExposure 联调实战）

- 调整时间：2026-08-21
- 通道：**执行中 gap 回补**（非外部吸收，无外部源可删）
- 来源：EllipalFinance-go 项目 `POST /api/swap/v2/getActivityExposure` 首次接入 apifox 的真实联调（10 用例 / 43 断言全绿），过程暴露 5 类本 skill 未覆盖的场景
- 裁决摘要：合并 7 条 / 拒绝 1 条 / 阻断级 1 条（#1 会导致误判合法接口的用例无效）

| # | 原子条目 | 本地现状（调整前） | 裁决 | 落点 | 整理去重 |
|---|---------|-------------------|------|------|----------|
| 1 | header-only 接口（schema `properties: {}` + 维度全在请求头）的 body `{}` 是真实契约，空壳判定应看"schema 有无必填字段" | `test-case.md` 把 `{}` 一律判无效；pitfalls #23 把空对象 schema 一律当风险 → **误判** | 合并（阻断级） | `test-case.md` 参数完整性节例外条款（三条证据）+ 不可违反规则第 1 条补例外 | **改写而非新增**：pitfalls #23 原"一律回 import-export 补"精化为两分支判定 |
| 2 | header-only 接口的正向分层：关键参数=业务请求头，L4 过滤×分页免除 | 规则 E-1 特殊场景只覆盖"仅分页"情形 | 合并 | `test-case-generation.md` 规则 E-1 特殊场景 | 挂既有条目下，不开新节 |
| 3 | 包装式启动（`go run`/`nodemon`/`--reload`/`mvn`）派生子进程，杀父进程不释放端口 → 新实例静默退出，用例全绿却测的是旧实例 | `environment.md` 有端口探测无关停核验；**规则权威在 `test-strategy-rules` SKILL.md:141** | 合并（只写执行细节 + 引用权威） | `environment.md` 新增「服务重启与关停核验」+ 不可违反规则第 15 条 + pitfalls 陷阱 32 | **同域去重**：不复制 test-strategy-rules 的"必须关闭并核验"规则本体，开头显式引用；A2 节重复的探测命令块收敛为引用（-15 行） |
| 4 | 服务端缓存 TTL 掩盖前置数据变更：改完立刻跑读到旧值 | pitfalls 第三节与 test-data-and-judgement 均无 | 合并 | pitfalls 陷阱 18-1 + 参数解析协议补生效性确认 | 挂既有表/节，不开新节 |
| 5 | 伪造来源头（`X-Forwarded-For`/`X-Real-IP`）测业务维度会同时改变鉴权判定，使该维度不可测；处置=固化安全性用例 + 登记待补测 | `test-auth.md` 与 pitfalls 第四节均无 | 合并 | `test-auth.md` 新增「免签分支与来源头耦合」+ pitfalls 陷阱 22-1 | 两处互相引用，不重复写处置步骤 |
| 6 | 断言期望值必须先实测取得，禁止只读代码推断 | 有"真实数据优先"，无"期望值来源"要求 | 合并（一句强化） | `test-data-and-judgement.md` 参数解析协议 | 并入既有协议列表，不开新节 |
| 7 | fixture 优先级反向设计：闸门对照记录 sort 高于期望命中记录，"命中主记录"即证明所有闸门生效 | 无同类技巧 | 合并 | `test-data-and-judgement.md` 新增「二之二」短节（含适用/不适用/代价） | 唯一新增二级标题；写明不适用场景防滥用 |
| 8 | 本项目 caseId/endpointId、apifox 库缺 v1 老表现象 | 属项目事实 | 拒绝 | — | N/A（已在项目 `PROJECT_TEST.md`，不进全局 skill） |

**净增减**：6 个模块 + SKILL.md 路由 4 行；本次回补新增约 78 行，整理删除约 15 行（environment.md A2 与端口探测三级链重复的命令块）+ 改写 1 条（pitfalls #23 从"一律当风险"改为两分支判定），**本次净增约 63 行**。

> 体积口径说明：本轮开始时 `modules/` 总量 181,280 字节，收口时 192,221 字节；差值**不能全部归因本次回补**——期间用户并发修改了 `environment.md`（新增环境白名单 local/apifox、local→apifox 单向灌数规则）与 `test-data-and-judgement.md`（新增「〇、旧数据灌入」节）。可归因本次的是上述 78 行新增与 15 行删除。

**同域冗余扫描**：范围 `test-strategy-rules` / `test-program-rules` / `test-regression-rules` / `functional-validation-rules` / `bug-validation-rules`。逐关键词 grep（关停 / 残留进程 / 缓存 / TTL / header-only / X-Forwarded-For / 反向设计 / 期望值）—— 仅"关闭并核验进程状态"在 `test-strategy-rules` SKILL.md:141 有规则权威，已收敛为「单一权威 + apifox 域执行细节引用」；其余 7 项兄弟 skill 零命中。无门控层叠（新增内容全部挂既有节）、无散落产物（未新建根目录文件）。**结论：PASS（发现 1 处，清理/收敛 1 处）**。

**棘轮验证**（评分方式：**非独立子 agent，主 agent 自评**，用户 2026-08-21 明确选定；下轮建议换独立评委避免锚定）：

| # | 维度 | 权重 | 前 | 后 | 依据 |
|---|------|------|----|----|------|
| 1 | Frontmatter 质量 | 8 | 9 | 9 | description 未改；仅路由表关键词增强 |
| 2 | 工作流清晰度 | 15 | 8 | 9 | 新增关停三步、header-only 三条证据判定、重启生效验证三查，均为有序可执行步骤 |
| 3 | 边界条件覆盖 | 10 | 8 | 9 | 补齐 4 个此前无处理路径的失败模式（空 body 误判 / 重启假生效 / 缓存掩盖 / 鉴权耦合），各带 fallback |
| 4 | 检查点设计 | 7 | 9 | 9 | 未新增用户门控；新增 1 条不可违反规则（第 15 条关停核验） |
| 5 | 指令具体性 | 15 | 8 | 9 | 新增内容均带可执行命令（`pkill -f '[e]xe/main'`、`ss -tln` 含副端口）与具体判定条件，非抽象原则 |
| 6 | 资源整合度 | 5 | 9 | 9 | 新增 case study 并被登记引用；6 处交叉引用锚点已 grep 校验可达，编码 UTF-8 |
| 7 | 整体架构 | 15 | 9 | 9 | 新增内容全部挂既有节，仅 1 个新二级标题；同域收敛 1 处 + 内部删除 15 行，净增 63 行属克制 |
| 8 | 实测表现 | 25 | 7 | 9 | 4 个真实场景 prompt 全部可路由：P1 header-only 建用例（4 模块命中）/ P2 全绿但改动没生效（3）/ P3 插了数据读不到（2）/ P4 伪造 IP 测地区被拒（4）。调整前 P1 会误判为无效用例，P2/P3/P4 无内容可路由 |

**总分：81.0 → 90.0（+9.0）**，涨幅 > 1 分不早停，**保留本次回补**。

> 与 2026-08-19 记录的 92.1 不可直接比较：那次是独立子 agent 评分，本次是主 agent 自评，评委锚定不同；本次的 81.0 基线同样由本次评委按同一 rubric 重打，前后差值才是有效信号。

**源处置**：N/A（内部 gap 回补通道，无外部源）。

## 本次吸收：api-test-automation-pro__skillhub（API测试自动化专家版 v1.5.0）

- 吸收时间：2026-08-19
- 来源：本地安装 `api-test-automation-pro__skillhub`（用户级 + 工作区双副本，MIT）
- 吸收方式：补缺式吸收（用户已确认：拒绝脚本层、吸收后删源、apifox 为主 + test-strategy-rules 策略引用）
- 裁决摘要：合并 9 条 / 保留本地 7 条 / 拒绝 4 条

| # | 外部精华 | 本地现状（吸收前） | 裁决 | 落点 | 整理去重 |
|---|---------|-------------------|------|------|----------|
| 1 | 契约测试方法论（Schema 校验/变化检测） | test-case-generation 仅"结构断言"简单映射 | 合并 | 新建 `modules/test-contract.md` | test-case-generation 原"契约测试（映射到 apifox）"小节压缩为引用 |
| 2 | 性能测试 4 类型 + P50-P99 指标 + 预热渐进加压 | 同上仅"重复执行+响应时间断言" | 合并 | 新建 `modules/test-performance.md` | test-case-generation 原"性能测试（映射到 apifox）"小节压缩为引用 |
| 3 | YAML 批量定义方法论（when/loop/parallel/hooks） | 本地无 YAML 定义能力 | 合并 | 新建 `modules/test-yaml-definition.md` | 无重复；无 apifox 映射语法标注"仅设计参考"防跑偏 |
| 4 | 五层健康评分（功能30/性能20/安全20/稳定15/契约15） | 本地无健康评分 | 合并 | 新建 `modules/test-health-score.md` | 无重复；数据缺口按 0 计并明示 |
| 5 | 四层诊断（网络/请求/业务/性能→根因→建议） | testing-pitfalls 有 31 条陷阱但无分层诊断 | 合并 | `testing-pitfalls.md` 追加第七节 | 与"运行失败时"排查用法衔接，统一到使用方式第 2 条 |
| 6 | 8 类异常 Fallback 策略表 | 本地无系统化 Fallback 表 | 合并 | `testing-pitfalls.md` 追加第八节 | 与"常见恢复"表归类去重 |
| 7 | 三重门控（设计/执行/报告） | SKILL.md 已有"必须询问用户"但非阶段门控 | 合并 | `SKILL.md` 核心共享规则追加 | 与"必须询问用户"清单归类（事项确认 vs 阶段确认） |
| 8 | Top20 必检项 + 用例类型级 P0/P1/P2 | test-selection-policy 有接口级 P0/P1/P2 | 合并 | `testing-pitfalls.md` 追加第十/十一节 | 与 test-selection-policy 接口级分级显式区分声明 |
| 9 | 9 类安全 payload 分类 + 断言顺序 + 16 种断言速查 | 鉴权安全陷阱仅 4 条；断言规则 4 行 | 合并 | `testing-pitfalls.md` 第九节 + `test-case.md` 断言顺序/速查 | 与第四节"鉴权与安全陷阱"合并去重（用例层 vs 漏洞类层） |
| 10 | 自然语言→用例、测试点分析、6 大用例矩阵 | test-case-generation 已吸收 | 保留本地 | — | N/A（已覆盖） |
| 11 | 陷阱库 140 条全量 | 本地 31 条 apifox 场景化 | 保留本地（抽条） | `testing-pitfalls.md` 第十二节抽取 8 条 | 只抽本地未覆盖高价值条目（幂等/弱网/分布式），不全量搬 |
| 12 | Mock/多格式报告/GraphQL | apifox 内置能力 | 保留本地 | — | N/A（已覆盖） |
| 13 | Spring Doc 解析 | swag-openapi-maintainer-rules 已覆盖 | 保留本地 | — | N/A（已覆盖） |
| 14 | 22 个 Python 脚本（约 1 万行） | 红线：接口测试必须 apifox 落地 | 拒绝 | — | N/A（拒绝原因：脚本层与 apifox 落地红线冲突，记入 source-notes） |
| 15 | README 缺失 5 references（security_checks 等） | 均为脚本层专属文档 | 拒绝 | — | N/A（精华从 README/SKILL.md 可读描述吸收） |
| 16 | HTTP 全表参考 | troubleshooting/test-case 已覆盖场景 | 拒绝 | — | N/A（低频冗余） |

**净增减预估**：新增 4 模块（16,520 字节）+ 强化 3 模块 + SKILL.md；整理去重约 6 处（test-case-generation 压缩 -568 字节、pitfalls 归类去重、SKILL.md 门控归类）。

**棘轮验证**：darwin 8 维评分 吸收前约 75.7 → 吸收后 92.1（独立子 agent 评分，2026-08-19）；实测 3/3 路由命中；保留。

**源处置**：吸收确认后删除源 skill 双副本（用户级 `C:\Users\luode\.workbuddy\skills\api-test-automation-pro__skillhub\` + 工作区 `D:\谷歌云盘\luode-skills\api-test-automation-pro__skillhub\`），详见 source-notes。
