# package-structure-rules 吸收裁决表（workbuddy-absorption-map）

> 归属 owner：`skill-absorption-rules`。每行必须可回指来源与落点，含「整理去重」列。

## 2026-08-26 内部更新：版本化目录导入别名对齐（v1/v2 语义别名反例）

来源：ellipal_finance 代码实测（用户报告）。`service/v1/list` 被以 `swapList` 语义别名导入，v2 用 `v2list`，不对称导致缓存清理只调 v1、v2 停留在旧过滤结果直到 600 秒 TTL 兜底且不报错。

| 来源 | 调整条目 | 本地现状 | 裁决 | 落点 / 理由 | 整理去重 |
| --- | --- | --- | --- | --- | --- |
| 内部调整（代码实测 gap） | 版本化目录内任意包的导入别名必须与版本目录名对齐（`v1<后缀>` / `v2<后缀>`） | SKILL.md 第 6 条仅约定 `v?router`/`v?controller`/`v?entity`/`v?service` 四类，未覆盖任意子包，未禁止语义别名 | 合并 | `SKILL.md` 核心边界第 6 条（动作前必读位置，拦截力最强） | 与既有 `v?router` 别名表述合并为同一句，不新增平行条目 |
| 内部调整（代码实测 gap） | 禁止业务语义别名导入版本化包（如 `swapList` 导入 v1 list），并给出正反例与漏调后果 | 完全缺失 | 合并 | `references/lookup-and-reference-contract.md` 新增「版本化目录导入别名对齐（强制）」小节 | 细则放 reference，SKILL.md 只放强制摘要，避免重复展开 |

**净增/净减**：SKILL.md +1 句（约 160 字节）、lookup-and-reference-contract.md +1 小节（约 380 字节）；无删除。
**同域冗余扫描**：范围 {package-structure-rules, naming-rules, code-style-consistency-rules, entity-file-naming}；发现 0 处逐字重复（naming-rules 只约束通用驼峰命名，未覆盖版本目录别名；本规则归属 package-structure-rules 的引用契约）；清理 0 处；PASS。
**棘轮评分**：内部更新通道按最小回补执行（非外部吸收，不适用 8 维评分基线对比；改动为规则补齐）。
**源删除**：无（内部更新通道）。

## 2026-08-27 内部更新：新增根级 cachetask/ 缓存重建任务目录

来源：用户会话提出——`crontask/` 是定时任务目录，但还存在"类定时任务"（缓存更新：缓存 60s 到期后先返回旧数据、再异步更新新缓存，Stale-While-Revalidate 模式），希望有专属目录 `cachetask/` 承载并加入目录树。

| 来源 | 调整条目 | 本地现状 | 裁决 | 落点 / 理由 | 整理去重 |
| --- | --- | --- | --- | --- | --- |
| 用户需求 | 新增后端根级 `cachetask/` 目录：缓存过期驱动的异步重建任务入口（SWR：TTL 到期先返旧数据再异步重建） | 根级任务入口仅有 `crontask/`（时间驱动）与 `async/`（消息驱动），无缓存过期驱动落点；`utils/cache/` 只做 Redis/Mongo 缓存读写技术适配 | 合并 | `project-layout-v2.md` 后端目录树 + 正文说明；`SKILL.md` 核心边界第 2 条根级唯一位置 + description；`structure-general.md`/`node-python-module-layout.md`/`java-layer-layout.md` 根级目录列表；`placement_catalog.py` `ADOPTION_V2_SOURCE_ROOTS["backend"]` 集合 | 与 `crontask/`、`async/` 合并为"三类根级任务入口"表述，不新建平行条目 |
| 一致性延伸 | 工作汇报按目录归类时识别 `cachetask/` | `generate_git_report.py` `MODULE_LABELS` 仅有 `crontask` | 合并 | `work-report-summary-rules/scripts/generate_git_report.py` 补 `"cachetask": "缓存任务"` | 与既有 `crontask` 映射同表同格式 |
| 既有基线漂移（顺手修复） | `standard_environments` 断言过期 | catalog 已含 `apifox`（2026-08-21 引入），测试仍断言 `["local","test","prod"]` | 合并 | `configuration_layout_test.py` 断言同步为含 `apifox` | 与 apifox 环境扩展既有事实对齐 |

**净增/净减**：project-layout-v2.md +1 目录条目 +1 段正文说明；SKILL.md description +2 字 + 核心边界第 2 条 +1 目录；3 个 language reference 各 +1 目录名；placement_catalog.py +1 集合元素；generate_git_report.py +1 映射；configuration_layout_test.py 断言 +1 环境；字典 data.js/字典.md 随 description 重跑。
**同域冗余扫描**：范围 {package-structure-rules, work-report-summary-rules, architecture-doc-rules}；发现 0 处逐字重复（`cachetask/` 与 `crontask/`、`async/`、`utils/cache/` 职责边界已在目录树正文显式区分）；清理 0 处；PASS。
**棘轮评分**：内部更新通道按最小回补执行（非外部吸收，不适用 8 维评分基线对比；改动为规则补齐）。
**源删除**：无（内部更新通道）。
