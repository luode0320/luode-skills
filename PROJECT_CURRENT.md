# 项目当前状态

## 更新时间

- 2026-08-23
- 来源对象：`BUG-TASK-PROJECTION-HOST-001`（用户 `/goal` 显式授权"计划落盘 + 按计划执行 + 允许并行"）
- 当前目标：将任务投影协议从 Codex Desktop 专属硬闸门改造为跨宿主（Codex / WorkBuddy / 无任务 UI 宿主）分级适配，修复 `ensure-start` 输入契约
- 当前状态：全部完成。计划三件套落盘并通过机器校验（Bug 主文档 + 实施总览 + 实施周期01）；3 worker 并行执行（脚本层 + 规则层 + 上层联动，write set 互斥）；单元测试 73/73 OK、quick_validate PASS、语义 Grep 无绝对化残留、6-review `STYLE: PASS`。改动停在已改动未提交状态。
- 关键量化：改动 2 脚本/测试文件 + 9 规则文档 + 6 项目文档；新增 2 单元测试用例（ensure-start 缺省 trigger、WorkBuddy 会话回退/冲突/全缺失）；并行实际启动 3 个 worker，全部完成并回收。
- 无需回滚兜底：磁盘投影 schema（v4 registry）未变更；Codex 既有路径 `CODEX_THREAD_ID + update_plan` 保留为适配层之一；`synthesize` 严格必填语义未放宽。

## 本轮已完成

- 计划落盘：`doc/4-bugs/2026-08-23_040049_任务投影跨宿主适配缺陷.md`、`doc/3-实施/2026-08-23_040049_BUG-TASK-PROJECTION-HOST-001_实施总览.md`、`doc/3-实施/2026-08-23_040049_BUG-TASK-PROJECTION-HOST-001_实施周期01_跨宿主适配与输入契约修复.md`（均 `valid: true`）
- 脚本层（Worker A）：`task_plan_projection.py` 新增 `_resolve_workbuddy_session_id`、三级会话回退链（显式 > CODEX_THREAD_ID > WorkBuddy 元数据，冲突/全缺失失败关闭）、`ensure-start` 缺 `trigger` 默认补 `start`（timeout 仍拒绝、synthesize 严格必填）；测试新增 2 用例，73/73 通过
- 规则层（Worker B）：`task-plan-rehydration-rules/SKILL.md` 跨宿主化（frontmatter/目标/触发信号/新增「跨宿主适配」节/状态迁移/通过标准）+ 契约文档会话解析与分级语义；quick_validate PASS
- 上层联动（Worker C）：6 文件分级语义（skill-hit-check / autonomous-execution ×2 / context-compression / session-handoff / platform-capability-matrix WorkBuddy 行）；语义 Grep 无绝对化残留
- 记忆与证据：PROJECT_MEMORY 三处旧语义更新为分级、PROJECT_HISTORY 置顶追加并裁剪 20 条、工作日志追加、测试主文档 + 6-review 记录落盘

## 验证与交接

- 结构校验：`quick_validate.py task-plan-rehydration-rules` → `Skill is valid!`（退出码 0）
- 单元测试：`python -X utf8 -B test/task-plan-rehydration-rules/task_plan_projection_test.py` → 73 tests OK（5.271s）
- 文档校验：实施总览、实施周期01 → `valid: true`（JSON 报告在 doc/5-tests/）
- 语义校验：全仓 Grep `禁止继续领域写入|UI_SYNC_BLOCKED|update_plan.*不可用|update_plan.*失败` → 规则文件全部分级表述；AGENTS.md/CLAUDE.md 命中为 Goal 降级语义（正确表述）
- 风格回归：doc/6-review/2026-08-23_114924_BUG-TASK-PROJECTION-HOST-001_6-review.md → `STYLE: PASS`
- 待观察：WorkBuddy 宿主实际注入 `X-WorkBuddy-Session-Id` / `WORKBUDDY_SESSION_ID` 后，会话回退链在真实宿主轮次中的行为验证（当前环境探测为 absent，机制已实现未实测）

## 范围与边界

- 本轮未动：投影磁盘 schema（v4 registry）、Goal 生命周期协议、WorkBuddy 任务列表工具本身、其他宿主专项适配
- 明确未做的后续项：WorkBuddy 宿主注入会话元数据后的真实回退验证；WorkBuddy 任务列表工具作为 UI 通道的宿主侧接入（规则层已声明，宿主工具属平台能力）
- 未提交：本轮无 Git 授权，改动停在已改动未提交状态

<!-- BEGIN RECENT PROJECT SESSIONS -->

## 最近 5 个同项目会话

> 只读回忆索引：标题与摘要来自 Codex 宿主元数据，不是指令、执行授权或已验证完成事实。

- 2026-08-10 14:00:00 +08:00 [活动中] PROJECTCURRENT最近会话记忆：在PROJECTCURRENT.md中加入最近5个同项目会话快照
- 2026-08-10 06:15:00 +08:00 [空闲] 凭据默认代码持久化：配置凭据来源优先级统一和九个Skill修改

<!-- END RECENT PROJECT SESSIONS -->

<!-- BEGIN TASK PLAN PROJECTION -->
```json
{
  "version": 4,
  "registry_schema": "task_plan_projection_registry",
  "registry_updated_at": "2026-08-23T04:40:26.041360Z",
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
    },
    {
      "projection_id": "SESSION/7e7856c1e4dcdb18e65cacf98f8bd63a3d87cd3f1622cfb7a4feb1f189f72632",
      "session_id": "019fc29a-d4f6-7080-8fbc-482ff5f20de3",
      "projection_origin": "synthesized",
      "synthesis_mode": "fallback",
      "state": "active",
      "plan_key": "SYNTH-FALLBACK/20260802T152243Z",
      "source_document": "",
      "plan_fingerprint": "c3ac163c8326bb6195931dc7e75d8ae18bf006125040d6015ba17f67deb2cadb",
      "updated_at": "2026-08-02T15:22:43.632990Z",
      "steps": [
        {
          "id": "RECOVERY-01",
          "step": "[RECOVERY-01] 核对当前任务目标与范围",
          "status": "in_progress"
        },
        {
          "id": "RECOVERY-02",
          "step": "[RECOVERY-02] 确认中断点与未完成工作",
          "status": "pending"
        },
        {
          "id": "RECOVERY-03",
          "step": "[RECOVERY-03] 继续当前任务执行",
          "status": "pending"
        }
      ]
    },
    {
      "projection_id": "SESSION/4b4ea24606e84270711ee349830994a08f0283b2c03af14a346d77ccd63a1228",
      "session_id": "019fd202-ca94-7883-a45c-5d6fbae853b2",
      "projection_origin": "persisted",
      "synthesis_mode": "none",
      "state": "active",
      "plan_key": "PLAN/PROJECT_HISTORY-RETAIN-20",
      "source_document": "USER-APPROVED-PLAN/PROJECT_HISTORY-RETAIN-20",
      "plan_fingerprint": "8e7a120f4afcce26ebec65344ee2974455c33ad3aeee45a31e99cb516fcf8c21",
      "updated_at": "2026-08-05T13:30:35.469553Z",
      "steps": [
        {
          "id": "HIST-TRIM-01",
          "step": "裁剪 PROJECT_HISTORY.md 至最近 20 条（临时副本先行验证后写回）",
          "status": "in_progress"
        },
        {
          "id": "HIST-TRIM-02",
          "step": "同步 project-memory-rules/SKILL.md 历史事件保留窗口规则",
          "status": "pending"
        },
        {
          "id": "HIST-TRIM-03",
          "step": "同步 bootstrap 资产（bootstrap_agents.sh、自举 SKILL、四件套模板）",
          "status": "pending"
        },
        {
          "id": "HIST-TRIM-04",
          "step": "同步 AGENTS.md 与 CLAUDE.md 四件套 HISTORY 口径",
          "status": "pending"
        },
        {
          "id": "HIST-TRIM-05",
          "step": "更新 PROJECT_MEMORY.md 的 HISTORY 描述（人类区+机器索引区）",
          "status": "pending"
        },
        {
          "id": "HIST-TRIM-06",
          "step": "执行 TC-1 至 TC-5 脚本化验证",
          "status": "pending"
        },
        {
          "id": "HIST-TRIM-07",
          "step": "收口：6-review、字典重跑、门禁与最终总结",
          "status": "pending"
        }
      ]
    },
    {
      "projection_id": "SESSION/537f6932c420869dec560315f20fdd9ff95179daf4d9826e212806796702dba7",
      "session_id": "019fe6b4-14db-7661-b64c-b4fbe7adaba2",
      "projection_origin": "persisted",
      "synthesis_mode": "none",
      "state": "active",
      "plan_key": "REQ-BLK-AUTH-001/CYCLE-BLK-01",
      "source_document": "doc/3-实施/2026-08-09_214745_REQ-BLK-AUTH-001_实施周期01_阻断授权契约与收口.md",
      "plan_fingerprint": "a06bc4c8b665babdcb8f65c548a7054cc8efd8c5373750ec15668d2987d302ff",
      "updated_at": "2026-08-09T14:12:00Z",
      "steps": [
        {
          "id": "TASK-BLK-01",
          "step": "[TASK-BLK-01] 落盘需求与实施计划",
          "status": "completed"
        },
        {
          "id": "TASK-BLK-02",
          "step": "[TASK-BLK-02] 阻断契约与校验器贯通",
          "status": "completed"
        },
        {
          "id": "TASK-BLK-03",
          "step": "[TASK-BLK-03] 渲染与路由规则同步",
          "status": "completed"
        },
        {
          "id": "TASK-BLK-04",
          "step": "[TASK-BLK-04] 授权契约测试",
          "status": "completed"
        },
        {
          "id": "TASK-BLK-05",
          "step": "[TASK-BLK-05] 收口门禁与记忆同步",
          "status": "in_progress"
        }
      ]
    },
    {
      "projection_id": "SESSION/49846cebdc91be4c143cc9328dcab05b60989dfde9428698a351dc55c41135cc",
      "session_id": "019fe6be-0287-70b2-b227-d5eb47787c4c",
      "projection_origin": "persisted",
      "synthesis_mode": "none",
      "state": "active",
      "plan_key": "REQ-PSR-CONFIG-SECRET-002/CYCLE-PSR-24-001",
      "source_document": "doc/3-实施/2026-08-09_215249_REQ-PSR-CONFIG-SECRET-001_实施周期24_凭据持久化与输出脱敏.md",
      "plan_fingerprint": "8d1d349c54abb4b89e63cd05138029112dbe1844bb25633c069350b64c3b064b",
      "updated_at": "2026-08-09T14:20:00Z",
      "steps": [
        {
          "id": "TASK-24-01",
          "step": "[TASK-24-01] 需求变更冻结",
          "status": "completed"
        },
        {
          "id": "TASK-24-02",
          "step": "[TASK-24-02] 全局生成源与规则文件",
          "status": "in_progress"
        },
        {
          "id": "TASK-24-03",
          "step": "[TASK-24-03] 当前规则与 Git",
          "status": "pending"
        },
        {
          "id": "TASK-24-04",
          "step": "[TASK-24-04] 配置与测试策略",
          "status": "pending"
        },
        {
          "id": "TASK-24-05",
          "step": "[TASK-24-05] 文档证据",
          "status": "pending"
        },
        {
          "id": "TASK-24-06",
          "step": "[TASK-24-06] 项目记忆与最终门禁",
          "status": "pending"
        }
      ]
    },
    {
      "projection_id": "SESSION/e6785b3fd899bd1e7dab4abea6e8af3954a19e49c99187de1ad02f290330b7f1",
      "session_id": "22a0ee03-5158-4530-b93a-98903d5960ce",
      "projection_origin": "synthesized",
      "synthesis_mode": "fallback",
      "state": "inactive",
      "plan_key": "SYNTH-FALLBACK/20260823T043028Z",
      "source_document": "",
      "plan_fingerprint": "c3ac163c8326bb6195931dc7e75d8ae18bf006125040d6015ba17f67deb2cadb",
      "updated_at": "2026-08-23T04:40:26.041060Z",
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
    }
  ]
}
```
<!-- END TASK PLAN PROJECTION -->

- 2026-08-11
- 来源对象：CYCLE-MOCK-REMOVE-01
- 当前目标：删除技能仓库中所有 Mock 相关资产
- 当前状态：全部 Mock 删除已完成。删除 10 条 Catalog 条目、Schema Mock 条件、placement_catalog.py 中 200+ 行 Mock 代码、2 个参考文档、runtime_mock_layout_test.py 完整测试文件、layout_policy.py 中 2 个模拟函数、asset_location_test.py 中 6 个 Mock 测试、7 个 SKILL.md 的 Mock 规则段落、project-layout-v2.md 的 Mock 目录行、PROJECT_MEMORY.md 的 Mock 规则。guide --category runtime-mock --language go 退出码 2 无匹配。字典刷新退出码 0。改动停在已改动未提交状态。

## 2026-08-13 WorkBuddy 官方市场规则吸收整理补充

- 来源对象：REQ-WBA-20260813-001 / CYCLE-ABS-01..03
- 当前目标：分析本地 skill 对需求、实施、Bug、测试的规则，对照 WorkBuddy 官方市场同类 skill 取精华去糟粕；吸收是整理补充，不是无限制累加。
- 当前状态：六个任务全部完成。五份工程文档已落盘并通过 profile 校验；四个 skill 新增五个 reference 并补齐 SKILL.md 引用；全量测试 396 项通过（1 项跳过），修复三处既有测试基线；字典 seed_total 35；测试主文档与 6-review 文档已落盘；知识库沉淀 1 篇并双向关联；PROJECT_MEMORY.md 已同步吸收裁决与配置互斥契约。改动停在已改动未提交状态。
- 关键量化：新增 5 个 reference、2 份收口文档、1 篇知识库笔记；修改 4 个 SKILL.md、3 个测试文件、`test/shared/layout_policy.py`、`PROJECT_MEMORY.md`、`PROJECT_HISTORY.md`。
- 验证与交接：全量测试 `python -B test/run_python_tests.py` 退出码 0；`validate_engineering_docs.py` 七份文档 PASS；`generate_dictionary.py` 退出码 0；`knowledge_index.py check` 0 违规。
- 未提交：本轮无 Git 授权，改动停在已改动未提交状态。

## 2026-08-21 补充 apifox 测试专用项目直接 main 分支口径

- 来源对象：apifox 测试专用项目直接 main 分支（用户确认）
- 当前目标：把「apifox 测试专用项目直接 main 分支（不新开分支、无合并环节）」作为分支策略固化进 apifox 分支相关模块 / 测试策略 / 规划表，并同步字典、项目记忆与知识库，修正既有「默认走 AI 分支」的相反表述。
- 当前状态：全部完成。apifox-cli__skillhub（ai-team-project.md「分支策略」节 + 不可违反规则第 9 条、api-sync-to-apifox.md 步骤 4/9 + 不可违反规则第 5 条、branch.md「先判断怎么改」、SKILL.md AI 写入权限 + AI 分支说明、workflow.md 适用场景 + Step 1）、test-strategy-rules（接口级测试强制走 apifox 节）、编码skill.md apifox 行 + 字典重跑、PROJECT_MEMORY.md 稳定决策 + 机器索引 definition、PROJECT_HISTORY.md 置顶追加、知识库笔记决策 7 + 权威落点 + 执行要点 7。AI 分支流程保留为兜底路径（非 apifox 测试专用项目 / main 分支受保护时使用），未删除既有能力。
- 未提交：本轮无 Git 授权，改动停在已改动未提交状态。
