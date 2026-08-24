# 吸收裁决表（api-contract-rules）

> 归属 owner：`skill-absorption-rules`。记录本 skill 历次外部吸收 / 内部调整的裁决与整理去重，保证可追溯。追加行时保持「整理去重」列必填（无整理写 `N/A + 理由`）。

## 2026-08-23：吸收 api-design__skillhub（REST API 设计模式）

- **来源**：`api-design__skillhub`（本地安装源，origin: ECC，`_skillhub_meta.json` 可回指），SKILL.md 约 520 行。
- **来源通道**：外部吸收。
- **环境依赖**：`N/A`（纯规则正文吸收，无环境变量 / 宿主配置 / hook / 依赖安装 / 路径引用）。
- **已删除源**：吸收确认后已删除 `api-design__skillhub/` 目录（含 SKILL.md、_meta.json、_icon.png、_skillhub_meta.json）。

### 裁决明细

| 外部精华 | 本地现状 | 裁决 | 落点 | 整理去重 |
|---|---|---|---|---|
| 资源复数、小写、kebab-case 命名 | 本地复数一致，多词资源命名未规定 | 合并 | `references/path-and-method-semantics.md`「路径原则」补 kebab-case 规则与子资源层级表达 | `N/A`（目标段原 5 行，增补 2 行，无重复可清） |
| 子资源 `/users/:id/orders`、path 参数 | 本地强制 POST + 路径动词、禁 path 参数 | 拒绝 | — | 机制形态与本地红线冲突 |
| HTTP 方法语义表（幂等/安全） | 本地强制 POST，禁 GET/PUT/PATCH/DELETE | 拒绝 | — | 本地红线冲突，不引入多方法语义 |
| 状态码语义（409/422/429/503；201/204 不引入） | 本地仅 200/400/401/403/404/500 | 合并 | `references/response-variants.md`「HTTP 状态码语义补充」 | 201/204 与本地统一 200 + 四字段冲突，落盘时适配排除 |
| 不要"200 包一切"、不要 500 当校验错 | 本地错误响应四字段 + 400 参数错误 | 保留本地 | — | 本地更强（四字段强制） |
| 响应 data wrapper / error{code,message,details} | 本地四字段 + `data.fieldErrors` | 保留本地 | — | 本地更强且字段级错误已有等价物 |
| 分页 meta + links（self/next/last） | 本地 offset 分页 `pagination{page,pageSize,total,totalPages,hasNext}` | 保留本地（links 拒绝） | — | links 与 POST 风格不匹配；`hasNext` 本地已有 |
| cursor 分页 + offset/cursor 选择矩阵 | 本地仅 offset，无 cursor 概念 | 合并 | `references/response-variants.md`「分页变体：cursor」+ 选择矩阵 | 删除本文件与 `response-shape-baseline.md` 逐字重复的 offset 分页段（约 30 行），收敛为「单一权威 + 引用」 |
| 过滤/排序/搜索（query 参数、稀疏字段） | 本地禁 query 参数；筛选条件放 body 但无表达规范 | 拒绝 | — | query 形态冲突；本地无对应需求，避免为吸收而吸收 |
| 认证授权（Bearer/API key/资源级/角色） | 本地明确"鉴权不混入参数模型设计" | 拒绝 | — | 职责边界冲突 |
| 限流（X-RateLimit-* 头、429 + Retry-After、限流层级） | 本地无任何限流规则 | 合并 | `references/response-variants.md`「限流响应」 | `N/A`（纯新增章节，无重复可清） |
| 版本化（URL v1 前缀、弃用时间线、Sunset、410、破坏/非破坏变更清单） | 本地仅一句"版本字段确有需要才引入" | 合并 | `references/response-variants.md`「兼容字段与版本化策略」 | 保留原兼容字段两句，扩展为版本化策略，无重复 |
| 实现样例（TS/Python/Go） | 本地已有 Go+Gin 正反例 | 拒绝 | — | 框架不匹配、本地更强 |
| 设计 Checklist | 本地已有"执行通过/驳回标准" | 保留本地 | — | 本地已覆盖核心项 |

### 净增减与评分

- **体积变化**：`path-and-method-semantics.md` +2 行；`response-variants.md` 新增约 75 行、删除约 30 行重复段 → 净增约 45 行，伴明确去重动作。
- **同域冗余扫描**：扫描范围 `api-contract-rules` / `error-handling-rules` / `swag-openapi-maintainer-rules`；发现重复段落 1 处（本 skill 内部两 reference 的 offset 分页段）、清理 1 处；门控/概念层叠 0、散落产物 0、引用链 PASS → **PASS**。
- **棘轮评分**：见当次收口说明（结构评分 + 效果验证结论）。
