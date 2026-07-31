# 项目当前状态

## 更新时间

- 2026-07-31

## 当前任务

- 来源对象：代码位置目录规则 V2 的 `utils`/源码根 `util`、微业务 JSON RPC、旧项目渐进采纳、`utils/ip/`、根治理文件和后端数据存储目录升级。
- 当前目标：完成 `package-structure-rules` 中 V2 新项目规则、旧项目 `adoption`、数据存储连接、模型分类、独立字段 SQL 与公开 CLI 查询的唯一位置、只读检查、测试、审查和验收闭环。
- 当前状态：`TASK-05-01` 至 `TASK-13-03` 已完成。CYCLE-13 已通过 48 项本地行为测试、Python 编译、公开 `database-*` 查询、文档校验、审查与最终验收；Java 模型映射已收敛到 `database/model/{db,redis,mongo}/`；本会话任务投影已失活收口。

## 范围与边界

- 范围：`package-structure-rules`、`micro-business-architecture-rules`、必要相邻工具规则、V2 研发产物、Skill 字典和当前任务状态。
- 非范围：业务项目迁移、自动移动、删除或重命名旧文件、真实数据库迁移、网络 RPC、外部服务、前端 `src/util/`、业务域私有 `util/` 和 Git 历史写入。
- 保护边界：工作树保留用户和其它会话的既有未提交改动；不执行 reset、checkout、commit 或 push。

## 已完成

- 根 `utils/` 只承载可独立复制的工具包和 SDK，禁止直接文件与项目包依赖；源码根 `util/` 只承载直接落盘的项目高关联工具函数，禁止子目录。
- Catalog、CLI、四语言路径映射、strict/legacy 检查、完整目录树、公共工具示例和 Skill 字典已同步。
- 每个微业务域按需提供扁平 `rpc/`；跨域只导入目标域精确 `rpc/`，请求和响应均为 JSON 字符串，统一采用 `Response{code,status,message,data}` 语义。
- Catalog、CLI、微业务隔离脚本、CodeGraph fixture、目录树和引用契约已同步；本地行为回归 21/21 通过，`py_compile`、关键 query 与完整树渲染通过。
- 旧项目使用 `doc/1-架构/3-目录规则收敛清单.yaml` 进行人工登记：已采纳 V2 目录可原地扩展，遗留源码仅可维护已登记快照，新业务和独立逻辑必须进入 Catalog 唯一 V2 路径。
- `utils/ip/` 已固定为 IP 提取、规范化、公私网判断与国家/地区归属查询的独立工具包；不承载代理信任、风控、业务黑白名单或业务地域策略。
- 三类项目根固定保存 `AGENTS.md`、`CLAUDE.md`、`PROJECT_CURRENT.md`、`PROJECT_MEMORY.md`、`PROJECT_HISTORY.md`；`PROJECT_STYLE.md` 仅在真实存在长期风格时创建。Catalog 把它们建模为文件节点，`init` 仅创建位置且不改写正文，strict 在两个规则文件同时存在时拒绝正文不一致。
- `check --policy adoption --adoption-manifest ...` 已实现只读检查；无效、越界、重复或禁止路径清单稳定失败，检查不改写项目或清单。
- `database/connection/` 已覆盖关系型数据库、Redis、Mongo 等数据存储连接；`database/model/` 只允许 `db/`、`redis/`、`mongo/`；独立字段 SQL 只进入 `database/sql/field/{create,update,delete}/` 且每个叶子目录只放 `.sql` 文件。
- 公开 `database-connection`、`database-sql`、`database-migration` 查询名称已与 Catalog 内部字段兼容；未连接数据库、缓存、消息队列、第三方 API 或非 local 环境。

## 门禁说明

- WSL `python3` 缺少 `yaml`，不能作为本轮文档校验入口；Windows Python 3.14 已提供 PyYAML，48 项本地 `unittest`、Python 编译、三条公开 `database-*` 查询和 `git diff --check` 均通过；文档与 Skill 校验将在最终状态更新前复跑。

## 验证与交接

- `PROJECT_CURRENT.md` 为 UTF-8 且保留所有会话的 registry 投影；当前会话 CYCLE-13 在最终门禁通过后使用 `task_plan_projection.py deactivate` 失活，且不影响其它会话投影。
- 后续目录位置查询与旧项目渐进检查以 `package-structure-rules/scripts/placement_catalog.py` 和 `placement-catalog.yaml` 为唯一入口。

<!-- BEGIN TASK PLAN PROJECTION -->
```json
{
  "version": 4,
  "registry_schema": "task_plan_projection_registry",
  "registry_updated_at": "2026-07-31T14:39:51.741619Z",
  "projections": [
    {
      "projection_id": "SESSION/53bbdc7515365d913192a90ec514e04314175256f1b1987074ac04697dda7366",
      "session_id": "019f9819-51c9-7380-8ff2-8b77ff9e7966",
      "projection_origin": "persisted",
      "synthesis_mode": "none",
      "state": "active",
      "plan_key": "REQ-RT-20260712-001/CYCLE-RT-13..18",
      "source_document": "doc/3-实施/2026-07-12_190609_通用上线测试引擎_修订版全量实施计划.md",
      "plan_fingerprint": "115c7cfa1e9da5a7d5c68fde68d664219cf2349f3dc387d9c8c474fedeaf507c",
      "updated_at": "2026-07-25T06:50:26Z",
      "steps": [
        {
          "id": "C13-01",
          "step": "[C13-01] 加载 external-scenario/1.0 并跑通 HTTP JSON 读场景",
          "status": "completed"
        },
        {
          "id": "C13-02",
          "step": "[C13-02] 实现候选生成、验证与生命周期迁移",
          "status": "completed"
        },
        {
          "id": "C14-01",
          "step": "[C14-01] 实现 form/multipart 上传读回与清理",
          "status": "completed"
        },
        {
          "id": "C14-02",
          "step": "[C14-02] 实现下载头与内容摘要验证",
          "status": "completed"
        },
        {
          "id": "C14-03",
          "step": "[C14-03] 实现 SSE 关联、断流与重连场景",
          "status": "completed"
        },
        {
          "id": "C15-01",
          "step": "[C15-01] 实现原生 WebSocket 场景",
          "status": "completed"
        },
        {
          "id": "C15-02",
          "step": "[C15-02] 实现 Socket.IO namespace/event/ack 场景",
          "status": "completed"
        },
        {
          "id": "C15-03",
          "step": "[C15-03] 实现 HTTP 到实时事件再到 HTTP 读回",
          "status": "completed"
        },
        {
          "id": "C16-01",
          "step": "[C16-01] 实现外部结果优先与受控只读探针",
          "status": "completed"
        },
        {
          "id": "C16-02",
          "step": "[C16-02] 实现清理、临时命名空间与污染阻断",
          "status": "completed"
        },
        {
          "id": "C16-03",
          "step": "[C16-03] 实现跨协议确定性 oracle",
          "status": "completed"
        },
        {
          "id": "C17-01",
          "step": "[C17-01] 拆分接口结果与场景结果报告",
          "status": "completed"
        },
        {
          "id": "C17-02",
          "step": "[C17-02] 实现 shadow 双轨对账",
          "status": "completed"
        },
        {
          "id": "C17-03",
          "step": "[C17-03] 实现场景硬门禁切换",
          "status": "completed"
        },
        {
          "id": "C18-01",
          "step": "[C18-01] 实现旧资产与 CLI 兼容迁移",
          "status": "completed"
        },
        {
          "id": "C18-02",
          "step": "[C18-02] 实现隔离工具环境与 doctor",
          "status": "completed"
        },
        {
          "id": "C18-03",
          "step": "[C18-03] 完成字典、回归、审查与最终验收",
          "status": "in_progress"
        }
      ]
    },
    {
      "projection_id": "SESSION/e3fee3201c0f1a9b557248ded3b4691524dd6d9775d8ec03515471ee4143db9c",
      "session_id": "019f9816-ff13-7072-8560-1e7662073134",
      "projection_origin": "persisted",
      "synthesis_mode": "none",
      "state": "active",
      "plan_key": "REQ-RTP-001/CYCLE-RTP-05",
      "source_document": "doc/3-实施/2026-07-25_163230_CodexDesktop任务悬浮窗断点恢复_实施周期05_超时自动升级.md",
      "plan_fingerprint": "8e5add7fbb20ad22002f1aab94b6f63f447e75b4c8497ffd2ac9d257df259d17",
      "updated_at": "2026-07-25T08:53:12Z",
      "steps": [
        {
          "id": "TASK-RTP-10",
          "step": "[TASK-RTP-10] 冻结超时升级需求与验收",
          "status": "completed"
        },
        {
          "id": "TASK-RTP-11",
          "step": "[TASK-RTP-11] 补齐悬浮窗超时触发规则",
          "status": "completed"
        },
        {
          "id": "TASK-RTP-12",
          "step": "[TASK-RTP-12] 实现并测试 ensure-timeout CLI",
          "status": "completed"
        },
        {
          "id": "TASK-RTP-13",
          "step": "[TASK-RTP-13] 完成字典回归审查与验收",
          "status": "in_progress"
        }
      ]
    },
    {
      "projection_id": "SESSION/c2bcdd2ae69ca02ea8bb2c5245216040be065b9bed627279ea8e46cc319828d1",
      "session_id": "019f9550-ec83-7fe1-a9c2-e76721253920",
      "projection_origin": "persisted",
      "synthesis_mode": "none",
      "state": "inactive",
      "plan_key": "REQ-RT-20260712-001/CYCLE-RT-13..18",
      "source_document": "doc/3-实施/2026-07-12_190609_通用上线测试引擎_修订版全量实施计划.md",
      "plan_fingerprint": "115c7cfa1e9da5a7d5c68fde68d664219cf2349f3dc387d9c8c474fedeaf507c",
      "updated_at": "2026-07-25T16:00:12.390563Z",
      "steps": [
        {
          "id": "C13-01",
          "step": "[C13-01] 加载 external-scenario/1.0 并跑通 HTTP JSON 读场景",
          "status": "completed"
        },
        {
          "id": "C13-02",
          "step": "[C13-02] 实现候选生成、验证与生命周期迁移",
          "status": "completed"
        },
        {
          "id": "C14-01",
          "step": "[C14-01] 实现 form/multipart 上传读回与清理",
          "status": "completed"
        },
        {
          "id": "C14-02",
          "step": "[C14-02] 实现下载头与内容摘要验证",
          "status": "completed"
        },
        {
          "id": "C14-03",
          "step": "[C14-03] 实现 SSE 关联、断流与重连场景",
          "status": "completed"
        },
        {
          "id": "C15-01",
          "step": "[C15-01] 实现原生 WebSocket 场景",
          "status": "completed"
        },
        {
          "id": "C15-02",
          "step": "[C15-02] 实现 Socket.IO namespace/event/ack 场景",
          "status": "completed"
        },
        {
          "id": "C15-03",
          "step": "[C15-03] 实现 HTTP 到实时事件再到 HTTP 读回",
          "status": "completed"
        },
        {
          "id": "C16-01",
          "step": "[C16-01] 实现外部结果优先与受控只读探针",
          "status": "completed"
        },
        {
          "id": "C16-02",
          "step": "[C16-02] 实现清理、临时命名空间与污染阻断",
          "status": "completed"
        },
        {
          "id": "C16-03",
          "step": "[C16-03] 实现跨协议确定性 oracle",
          "status": "completed"
        },
        {
          "id": "C17-01",
          "step": "[C17-01] 拆分接口结果与场景结果报告",
          "status": "completed"
        },
        {
          "id": "C17-02",
          "step": "[C17-02] 实现 shadow 双轨对账",
          "status": "completed"
        },
        {
          "id": "C17-03",
          "step": "[C17-03] 实现场景硬门禁切换",
          "status": "completed"
        },
        {
          "id": "C18-01",
          "step": "[C18-01] 实现旧资产与 CLI 兼容迁移",
          "status": "completed"
        },
        {
          "id": "C18-02",
          "step": "[C18-02] 实现隔离工具环境与 doctor",
          "status": "completed"
        },
        {
          "id": "C18-03",
          "step": "[C18-03] 完成字典、回归、审查与最终验收",
          "status": "completed"
        }
      ]
    },
    {
      "projection_id": "SESSION/e0641079a9b3807614bb7bea657755435440b1b8a87869e3e169419fef60eb93",
      "session_id": "019f98be-5f55-7c40-9dcb-0d31788ff83c",
      "projection_origin": "synthesized",
      "synthesis_mode": "exact",
      "state": "inactive",
      "plan_key": "CYCLEDOC-RTP-05",
      "source_document": "doc/3-实施/2026-07-25_163230_CodexDesktop任务悬浮窗断点恢复_实施周期05_超时自动升级.md",
      "plan_fingerprint": "78fe389ec6fcf8820370aaee55972c5702eb014a1f1277bc848630786471950f",
      "updated_at": "2026-07-25T10:44:00.535000Z",
      "steps": [
        {
          "id": "TASK-RTP-10",
          "step": "[TASK-RTP-10] 冻结超时需求、验收、总览和周期追踪",
          "status": "completed"
        },
        {
          "id": "TASK-RTP-11",
          "step": "[TASK-RTP-11] 让唯一 Owner 与相邻执行路由表达一致的超时规则",
          "status": "completed"
        },
        {
          "id": "TASK-RTP-12",
          "step": "[TASK-RTP-12] 实现可验证且无 schema 漂移的 `ensure-timeout` CLI",
          "status": "completed"
        },
        {
          "id": "TASK-RTP-13",
          "step": "[TASK-RTP-13] 补齐测试、生成资产、项目状态和合规证据",
          "status": "completed"
        }
      ]
    },
    {
      "projection_id": "SESSION/3973c62658af29715b77501632a92f3b40cba5d0771b4b64bb71c98ceb451c21",
      "session_id": "019f98d4-9fd6-73c2-ad35-acf08ad74ac1",
      "projection_origin": "synthesized",
      "synthesis_mode": "exact",
      "state": "inactive",
      "plan_key": "CYCLEDOC-RTP-06",
      "source_document": "doc/3-实施/2026-07-25_203000_CodexDesktop任务悬浮窗断点恢复_实施周期06_Goal自动升级.md",
      "plan_fingerprint": "73134d0acf46d2ec23f4a9f874465450559529584a17f518ed4ef77f38f252f9",
      "updated_at": "2026-07-25T13:57:52.005254Z",
      "steps": [
        {
          "id": "TASK-RTP-14",
          "step": "[TASK-RTP-14] 冻结需求变更和验收",
          "status": "completed"
        },
        {
          "id": "TASK-RTP-15",
          "step": "[TASK-RTP-15] 冻结 Cycle 06 执行契约",
          "status": "completed"
        },
        {
          "id": "TASK-RTP-16",
          "step": "[TASK-RTP-16] 新增无写入 `probe-timeout`",
          "status": "completed"
        },
        {
          "id": "TASK-RTP-17",
          "step": "[TASK-RTP-17] 冻结 Goal 编排和失败降级",
          "status": "completed"
        },
        {
          "id": "TASK-RTP-18",
          "step": "[TASK-RTP-18] 同步连续执行与 standing authorization",
          "status": "completed"
        },
        {
          "id": "TASK-RTP-19",
          "step": "[TASK-RTP-19] 同步全局规则和项目记忆",
          "status": "completed"
        },
        {
          "id": "TASK-RTP-20",
          "step": "[TASK-RTP-20] 完成字典与自动回归",
          "status": "completed"
        },
        {
          "id": "TASK-RTP-21",
          "step": "[TASK-RTP-21] 完成真实 Desktop 审查验收",
          "status": "completed"
        }
      ]
    },
    {
      "projection_id": "SESSION/2ac02581582ba844cadf597eeea6bf0056e817767fe90edffde4a54da2617807",
      "session_id": "019f9a5c-65d7-7312-a3d2-5bd5533dbe1a",
      "projection_origin": "synthesized",
      "synthesis_mode": "exact",
      "state": "active",
      "plan_key": "IMP-PMW-001",
      "source_document": "doc/3-实施/2026-07-26_040639_BUG-PLAN-WAIT-20260726-001_实施总览.md",
      "plan_fingerprint": "803519e47bb6c839a34fa8fbd83fe9dab4f58939090177a4293c777d100e428a",
      "updated_at": "2026-07-25T21:10:00Z",
      "steps": [
        {
          "id": "TASK-PMW-01",
          "step": "[TASK-PMW-01] `TASK-PMW-01`",
          "status": "completed"
        },
        {
          "id": "TASK-PMW-02",
          "step": "[TASK-PMW-02] `TASK-PMW-02`",
          "status": "completed"
        },
        {
          "id": "TASK-PMW-03",
          "step": "[TASK-PMW-03] `TASK-PMW-03`",
          "status": "completed"
        },
        {
          "id": "TASK-PMW-04",
          "step": "[TASK-PMW-04] `TASK-PMW-04`",
          "status": "in_progress"
        }
      ]
    },
    {
      "projection_id": "SESSION/7931d74771fbbf6f11294b901bd9909bf47008569a75f10070efbb8186297805",
      "session_id": "019f9cf5-ee26-75c0-a639-55a73500c7df",
      "projection_origin": "synthesized",
      "synthesis_mode": "exact",
      "state": "active",
      "plan_key": "CYCLE-RTP-07",
      "source_document": "doc/3-实施/2026-07-26_150000_CodexDesktop任务悬浮窗断点恢复_实施周期07_首次持久化即悬浮窗同步.md",
      "plan_fingerprint": "b19faa6359fd7434e012cedaa2cb3e9ae7373b74b8e540e4149f65ece8c4733f",
      "updated_at": "2026-07-26T15:00:00Z",
      "steps": [
        {
          "id": "TASK-RTP-22",
          "step": "[TASK-RTP-22] session 与 ensure-start",
          "status": "completed"
        },
        {
          "id": "TASK-RTP-23",
          "step": "[TASK-RTP-23] 投影回归",
          "status": "completed"
        },
        {
          "id": "TASK-RTP-24",
          "step": "[TASK-RTP-24] Owner UI 闸门",
          "status": "completed"
        },
        {
          "id": "TASK-RTP-25",
          "step": "[TASK-RTP-25] 恢复与状态路由",
          "status": "completed"
        },
        {
          "id": "TASK-RTP-26",
          "step": "[TASK-RTP-26] 自治与上下文路由",
          "status": "completed"
        },
        {
          "id": "TASK-RTP-27",
          "step": "[TASK-RTP-27] 文档与 profile",
          "status": "completed"
        },
        {
          "id": "TASK-RTP-28",
          "step": "[TASK-RTP-28] 字典、审查与真实验收",
          "status": "in_progress"
        }
      ]
    },
    {
      "projection_id": "SESSION/71df5f38455c3a5ee4c8ff567163229e45ab77d8eb0f40c258f8fcb2cdf9f5df",
      "session_id": "019f9a43-800a-73b0-80bb-2a79bf2abd67",
      "projection_origin": "synthesized",
      "synthesis_mode": "exact",
      "state": "inactive",
      "plan_key": "PLAN-SUMMARY-DETAIL-001",
      "source_document": "doc/3-实施/2026-07-26_073000_reasoning-summary-structure-rules_结果与结论详细度_实施总览.md",
      "plan_fingerprint": "f9311cab0a07ace29835d15029ec024e9318472089444a4878792abba65661fe",
      "updated_at": "2026-07-26T08:25:07.435729Z",
      "steps": [
        {
          "id": "TASK-SUMMARY-DETAIL-01",
          "step": "[TASK-SUMMARY-DETAIL-01] `CYCLE-SUMMARY-DETAIL-01`",
          "status": "completed"
        },
        {
          "id": "TASK-SUMMARY-DETAIL-02",
          "step": "[TASK-SUMMARY-DETAIL-02] `CYCLE-SUMMARY-DETAIL-02`",
          "status": "completed"
        },
        {
          "id": "TASK-SUMMARY-DETAIL-03",
          "step": "[TASK-SUMMARY-DETAIL-03] `CYCLE-SUMMARY-DETAIL-03`",
          "status": "completed"
        }
      ]
    },
    {
      "projection_id": "SESSION/fd59b49ba40d507de38be62f910b6551b82a8d84a2bd733dc080c52dd1d32c06",
      "session_id": "019f9d75-5d5c-7a30-a262-71d2c7806880",
      "projection_origin": "persisted",
      "synthesis_mode": "none",
      "state": "active",
      "plan_key": "IMPLEMENTATION-PLAN-OUTPUT-001",
      "source_document": "doc/3-实施/2026-07-26_BUG-PLAN-OUTPUT-20260726-001_实施总览.md",
      "plan_fingerprint": "6ff907ed2ca8398cf86b7b28800dc5af1111dd2878aaa1a6e26518116b29051a",
      "updated_at": "2026-07-26T09:25:00Z",
      "steps": [
        {
          "id": "TASK-PLAN-01",
          "step": "[TASK-PLAN-01] 建立脱敏会话夹具与失败基线",
          "status": "completed"
        },
        {
          "id": "TASK-PLAN-02",
          "step": "[TASK-PLAN-02] 增加总结 Skill 的 Plan Mode 负向退出",
          "status": "completed"
        },
        {
          "id": "TASK-PLAN-03",
          "step": "[TASK-PLAN-03] 让计划 Skill 接管唯一计划出口",
          "status": "completed"
        },
        {
          "id": "TASK-PLAN-04",
          "step": "[TASK-PLAN-04] 冻结等待闸门与压缩恢复",
          "status": "completed"
        },
        {
          "id": "TASK-PLAN-05",
          "step": "[TASK-PLAN-05] 同步命中总控与 Plan Mode 排除路由",
          "status": "completed"
        },
        {
          "id": "TASK-PLAN-06",
          "step": "[TASK-PLAN-06] 同步 AGENTS、CLAUDE 与 bootstrap 生成源",
          "status": "completed"
        },
        {
          "id": "TASK-PLAN-07",
          "step": "[TASK-PLAN-07] 补齐 Bug、需求、实施与验收文档链",
          "status": "completed"
        },
        {
          "id": "TASK-PLAN-08",
          "step": "[TASK-PLAN-08] 生成 Skill 字典并同步项目记忆",
          "status": "completed"
        },
        {
          "id": "TASK-PLAN-09",
          "step": "[TASK-PLAN-09] 执行专项回归与合规校验",
          "status": "completed"
        },
        {
          "id": "TASK-PLAN-10",
          "step": "[TASK-PLAN-10] 完成实现审查与当前改动审查",
          "status": "completed"
        },
        {
          "id": "TASK-PLAN-11",
          "step": "[TASK-PLAN-11] 验证真实新 Plan 会话的用户可见出口",
          "status": "in_progress"
        }
      ]
    },
    {
      "projection_id": "SESSION/444df4cee5780ee03eb74622ed45767f35e97e556c364555013921aa2c879530",
      "session_id": "019f9dd1-31f3-7401-8575-eadf6b3ec55f",
      "projection_origin": "persisted",
      "synthesis_mode": "none",
      "state": "inactive",
      "plan_key": "REQ-PSR-V2-001/CYCLE-13",
      "source_document": "doc/3-实施/2026-07-31_000000_代码位置目录规则V2_实施周期13_数据存储目录扩展.md",
      "plan_fingerprint": "2e39812fa45e7561fe5cec51f834f5d50e7cb3366dc44053df3c954ca1bfd891",
      "updated_at": "2026-07-31T14:39:51.741343Z",
      "steps": [
        {
          "id": "TASK-13-01",
          "step": "[TASK-13-01] 固化数据存储目录、Catalog 与唯一查询",
          "status": "completed"
        },
        {
          "id": "TASK-13-02",
          "step": "[TASK-13-02] 实现 strict SQL 检查并完成真实行为测试",
          "status": "completed"
        },
        {
          "id": "TASK-13-03",
          "step": "[TASK-13-03] 完成文档、审查、验收与合规收口",
          "status": "completed"
        }
      ]
    }
  ]
}
```
<!-- END TASK PLAN PROJECTION -->
