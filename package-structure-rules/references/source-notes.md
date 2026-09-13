# package-structure-rules 来源记录

## 2026-09-11

- 内部调整：`package-structure-rules`，调整诉求「补齐结构体『按类型与作用分层』缺口——角色谱系、各角色落点、按语言生态的差异与注释颗粒度」。
- 触发来源：用户会话——AI 辅助开发瓶颈已从逻辑正确性转向代码质量，其九维清单中「结构体按类型与作用分层的定义位置及注释」此前无承接；`entity-file-naming.md` 只讲 `entity/<v?>/` 内文件粒度（`req`/`resp` 前缀），不含角色分层。
- 口径：用户裁决「按语言生态」（Go 用导出性表达外传边界、Java `class`/`record` + 既有 PO/DTO/VO、TS `interface`/`type`、Python `dataclass`/Pydantic）。
- 落点：`references/struct-role-layering.md`（新建，4652B）、`SKILL.md` 唯一事实源第 18 行。
- 裁决依据：见 `../workbuddy-absorption-map.md` 2026-09-11 段落。
- 顺手修复：`references/directory-usage-routing.md` 第 19 行原将 `utils/decimal/` 行与 `utils/cache/redis/` 行挤在同一行（缺换行），Markdown 表格破损，已拆回两行；本项由 Item 4（公共工具索引契约）基线侦察时发现。

## 2026-08-27

- 内部调整：`package-structure-rules`，调整诉求「新增根级 `cachetask/` 目录，专门承载缓存过期驱动的异步重建任务（Stale-While-Revalidate：TTL 到期先返回旧数据，再异步更新新缓存）」。
- 触发来源：用户会话——`crontask/` 是定时任务目录，但存在"类定时任务"（如缓存 60s 到期先返旧数据再异步重建），希望有专属目录；知识库《配置表驱动缓存五件套》印证现有 `crontask/` 承担的是周期主动刷新（30 分钟 cron），与 SWR 模式触发机制不同。
- 落点：`project-layout-v2.md`（目录树条目 + 三类任务入口正文说明）、`SKILL.md`（description + 核心边界第 2 条）、`structure-general.md`/`node-python-module-layout.md`/`java-layer-layout.md`（根级目录列表）、`placement_catalog.py`（`ADOPTION_V2_SOURCE_ROOTS["backend"]` 集合）、`work-report-summary-rules/scripts/generate_git_report.py`（目录分类映射）。
- 顺手修复：`configuration_layout_test.py` `standard_environments` 断言同步 apifox（2026-08-21 引入的标准环境扩展，测试基线未同步的既有漂移）。

## 2026-08-26

- 内部调整：`package-structure-rules`，调整诉求「版本化目录导入别名必须与版本目录名对齐，禁止业务语义别名（v1/v2 不对称导致缓存漏清）」。
- 触发来源：ellipal_finance 代码实测，`swapList "ellipal_finance/internal/service/v1/list"` + `v2list` 不对称；`swapList.ClearSwapListCache()` 只清 v1，v2 主币列表停留旧结果直到 600 秒 TTL 兜底且不报错。
- 落点：SKILL.md 核心边界第 6 条 + `references/lookup-and-reference-contract.md`「版本化目录导入别名对齐（强制）」。
