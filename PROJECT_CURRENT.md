# 项目当前状态

## 更新时间

- 2026-08-02

## 当前任务

- 来源对象：用户已确认的独立 `session-handoff-rules` skill。
- 当前目标：提取当前会话压缩信息，生成脱敏交接包，并在同一保存项目的 `local` 环境创建新 Codex 任务继续；默认只提示人工归档旧任务。
- 当前状态：skill 本体、触发词、Codex App 路由、交接包契约、标准库校验脚本、契约测试、项目记忆和字典均已落盘；风格回归通过；同项目 local 新任务已取得真实任务标识，新任务启动契约核验已完成。

## 范围与边界

- 范围：`session-handoff-rules`、交接包 JSON 契约、脱敏 / 大小校验、`list_projects -> create_thread -> wait_threads` 路由、根 `test/` 契约测试、项目记忆和 skill 字典。
- 非范围：再次创建新任务、自动调用 `set_thread_archived`、旧任务归档、业务项目代码、数据库、外部服务和 Git 历史写入。
- 保护边界：工作树保留用户和其它会话的既有未提交改动；不执行 reset、checkout、commit 或 push。

## 已完成

- 新增 `session-handoff-rules/SKILL.md`，覆盖九个触发词、事实抽取、脱敏、local 项目创建、等待和人工归档边界。
- 新增 `references/handoff-packet-contract.md`、`references/codex-thread-routing.md` 与 `scripts/validate_handoff_packet.py`。
- 新增 `test/session-handoff-rules/validate_handoff_packet_test.py`，覆盖有效包、`next_steps` 缺失、敏感字段和大小限制。
- `编码skill.md`、`PROJECT_MEMORY.md`、`字典.md` 和 `skill-dictionary/data.js` 已同步；字典将新 skill 归入记忆域。
- 已完成本地验证：quick validation 通过，交接包定向测试 `4/4` 通过，根 `test/` 全量 Python 入口 `191/191` 通过，`git diff --check` 通过。

## 门禁说明

- 本轮 `Obsidian:不适用`；任务只维护仓库内 skill、测试和字典，不读取或写入 vault。所有实现与验证仅使用本地仓库、Windows Python、临时目录和本地 Git 只读检查。

## 验证与交接

- `PROJECT_CURRENT.md` 为 UTF-8 并保留所有会话的 registry 投影；当前新任务投影 `REQ-SH-START-20260802-001` 已完成、失活并同步收口。
- 最后执行点：交接包已通过标准库校验，当前代码、项目文档和工作树边界已核对；`quick_validate`、定向契约测试 `4/4` 和根测试 `191/191` 已复验通过；本轮未再次创建任务、未调用归档工具、未执行 Git 历史写入。

<!-- BEGIN TASK PLAN PROJECTION -->
```json
{
  "version": 4,
  "registry_schema": "task_plan_projection_registry",
  "registry_updated_at": "2026-08-02T09:51:50.898982Z",
  "projections": [
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
      "projection_id": "SESSION/642f6c0ae9fc393c4cbff38f2b6317b945894cadd4888be5015994cf1f4fd8bc",
      "session_id": "019f9dd1-31f3-7401-8575-eadf6b3ec55f",
      "projection_origin": "persisted",
      "synthesis_mode": "none",
      "state": "inactive",
      "plan_key": "REQ-PSR-V2-001/CYCLE-14",
      "source_document": "doc/2-需求/2026-07-28_014412_代码位置目录规则V2.md",
      "plan_fingerprint": "800d03cf7113c96d0020b18ce87bb222afe6209f499bf210ab845f6e3c633cbb",
      "updated_at": "2026-07-31T15:40:21.210576Z",
      "steps": [
        {
          "id": "TASK-14-01",
          "step": "[TASK-14-01] 删除后端 data 目录规则和 Catalog 条目",
          "status": "completed"
        },
        {
          "id": "TASK-14-02",
          "step": "[TASK-14-02] 完成严格检查、测试与文档收口",
          "status": "completed"
        }
      ]
    },
    {
      "projection_id": "SESSION/1dabf0c126d0a2cf9fc2896e6312dd759f9cdeee01ebc9631c9dbb9e86096df5",
      "session_id": "019fb8f8-2434-7f30-ab1f-6928ccc5b93a",
      "projection_origin": "persisted",
      "synthesis_mode": "none",
      "state": "inactive",
      "plan_key": "TEST-LAYOUT-20260801",
      "source_document": "user-confirmed-plan:root-test-layout-20260801",
      "plan_fingerprint": "1964bbdc5c2793c8437a14ae3552b6c5c2b84f7911763b0574b99890a6bb1201",
      "updated_at": "2026-08-01T12:25:00Z",
      "steps": [
        {
          "id": "TASK-TEST-LAYOUT-01",
          "step": "冻结根 test 目录需求、实施文档和测试证据契约",
          "status": "completed"
        },
        {
          "id": "TASK-TEST-LAYOUT-02",
          "step": "更新测试资产规则并建立位置与命名校验",
          "status": "completed"
        },
        {
          "id": "TASK-TEST-LAYOUT-03",
          "step": "迁移七组活动 tests 到根 test 目录",
          "status": "completed"
        },
        {
          "id": "TASK-TEST-LAYOUT-04",
          "step": "同步活动消费者、目录树、字典和项目四件套",
          "status": "completed"
        },
        {
          "id": "TASK-TEST-LAYOUT-05",
          "step": "执行全链路真实测试并完成 6-review 收口",
          "status": "completed"
        }
      ]
    },
    {
      "projection_id": "SESSION/c75f9770bc950c84196f26c76402d99a13989852dc296ef7954ff10b20d9eb52",
      "session_id": "019fbe92-f266-7eb2-a426-2b4df1b29bae",
      "projection_origin": "synthesized",
      "synthesis_mode": "fallback",
      "state": "inactive",
      "plan_key": "SYNTH-FALLBACK/20260802T040348Z",
      "source_document": "",
      "plan_fingerprint": "c3ac163c8326bb6195931dc7e75d8ae18bf006125040d6015ba17f67deb2cadb",
      "updated_at": "2026-08-02T04:07:19.771974Z",
      "steps": [
        {
          "id": "RECOVERY-01",
          "step": "[RECOVERY-01] 核对当前任务目标与范围",
          "status": "completed"
        },
        {
          "id": "RECOVERY-02",
          "step": "[RECOVERY-02] 确认中断点与未完成工作",
          "status": "completed"
        },
        {
          "id": "RECOVERY-03",
          "step": "[RECOVERY-03] 继续当前任务执行",
          "status": "completed"
        }
      ]
    },
    {
      "projection_id": "SESSION/af95daef0fde26ea931aa19b9451721e9ccdcbc5e3ff08cfb18c8d374403e914",
      "session_id": "019fc0a5-45cb-7902-b1dc-d9e9f98d7284",
      "projection_origin": "persisted",
      "synthesis_mode": "none",
      "state": "inactive",
      "plan_key": "REQ-SH-START-20260802-001",
      "source_document": "session-handoff-rules/SKILL.md",
      "plan_fingerprint": "06daabdb153e19ec7966882dcdcb964d84ed626a1200f5b627d8651c83950743",
      "updated_at": "2026-08-02T04:21:17.828959Z",
      "steps": [
        {
          "id": "TASK-SH-START-01",
          "step": "[TASK-SH-START-01] 校验交接包并核对项目当前状态",
          "status": "completed"
        },
        {
          "id": "TASK-SH-START-02",
          "step": "[TASK-SH-START-02] 核验当前会话投影、中断点和未提交改动边界",
          "status": "completed"
        },
        {
          "id": "TASK-SH-START-03",
          "step": "[TASK-SH-START-03] 执行仍必要的后续步骤并更新验证证据",
          "status": "completed"
        }
      ]
    },
    {
      "projection_id": "SESSION/66543947614ef037fef0038b76ce599e4bf523e7023a0ed0102892074ad2c309",
      "session_id": "019fc0b2-6e7b-7cc3-889c-1c45b5d6ad57",
      "projection_origin": "persisted",
      "synthesis_mode": "none",
      "state": "active",
      "plan_key": "REQ-CUR-20260802-001/CYCLE-CUR-01",
      "source_document": "doc/3-实施/2026-08-02_123351_PROJECT_CURRENT任务记录保留与过期清理_实施周期01_七天保留与自动清理.md",
      "plan_fingerprint": "ff5724d2a374b7e931ab96f4a9eab93a0d44c350021b5228777a6a57a9600d67",
      "updated_at": "2026-08-02T05:02:00Z",
      "steps": [
        {
          "id": "TASK-CUR-01",
          "step": "[TASK-CUR-01] 落盘需求变更与实施契约",
          "status": "completed"
        },
        {
          "id": "TASK-CUR-02",
          "step": "[TASK-CUR-02] 实现 registry 自动清理并补齐行为测试",
          "status": "in_progress"
        },
        {
          "id": "TASK-CUR-03",
          "step": "[TASK-CUR-03] 同步两个 Owner Skill 的行为规则",
          "status": "pending"
        },
        {
          "id": "TASK-CUR-04",
          "step": "[TASK-CUR-04] 同步 bootstrap 模板与生成规则",
          "status": "pending"
        },
        {
          "id": "TASK-CUR-05",
          "step": "[TASK-CUR-05] 迁移项目记忆并清理真实旧投影",
          "status": "pending"
        },
        {
          "id": "TASK-CUR-06",
          "step": "[TASK-CUR-06] 刷新字典、全量测试与最终风格收口",
          "status": "pending"
        }
      ]
    },
    {
      "projection_id": "SESSION/25c4de2884dde3fc1ae8e23c37876448d2016cbab5fed677ab2ff3019cfca232",
      "session_id": "019fc15c-b869-7933-84b6-c40268b0ce3f",
      "projection_origin": "synthesized",
      "synthesis_mode": "fallback",
      "state": "active",
      "plan_key": "SYNTH-FALLBACK/20260802T092611Z",
      "source_document": "",
      "plan_fingerprint": "c3ac163c8326bb6195931dc7e75d8ae18bf006125040d6015ba17f67deb2cadb",
      "updated_at": "2026-08-02T09:51:32.192Z",
      "steps": [
        {
          "id": "RECOVERY-01",
          "step": "[RECOVERY-01] 核对当前任务目标与范围",
          "status": "completed"
        },
        {
          "id": "RECOVERY-02",
          "step": "[RECOVERY-02] 确认中断点与未完成工作",
          "status": "completed"
        },
        {
          "id": "RECOVERY-03",
          "step": "[RECOVERY-03] 继续当前任务执行",
          "status": "in_progress"
        }
      ]
    }
  ]
}
```
<!-- END TASK PLAN PROJECTION -->
