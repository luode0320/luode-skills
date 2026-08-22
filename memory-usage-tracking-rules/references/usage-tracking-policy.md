# 计数回写策略（usage-tracking-policy）

## 目标

定义"什么动作算使用、谁在何时 +1、如何防虚报"的完整口径，保证使用次数可量化、可审计、可区分。

## 1. "使用"的定义（谁 +1）

**只有"实际引用"才 +1**，即条目的内容**真实影响了本轮的决策、输出、代码、命名、配置取值或流程走向**。典型场景：

- 决策时引用了 `PROJECT_MEMORY.md` 的稳定决策条目（如"环境白名单 {local, apifox}"）并据此行事。
- 编码时复用了 `PROJECT_STYLE.md` 的风格样例（如"方法返回空值"写法）。
- 历史追问/状态不足时**窄读** `PROJECT_HISTORY.md` 的某条事件并据此继续任务。
- 被其他 skill 的规则正文显式引用（如 `references/` 交叉引用指向某条记忆）。

**不 +1** 的场景：

- 会话启动按规则读取记忆文件全文（`父目录规则 -> PROJECT_CURRENT.md -> PROJECT_MEMORY.md`）。
- 只读取但未影响任何决策/输出（读了但没用上）。
- 机器索引区/计数锚点区本身的读写维护动作。

## 2. 台账收集（会话内内存态）

- 会话内维护内存台账：`usage_log: [{file, anchor, reason}]`。
- 按 `(file, anchor)` 去重：**同一会话内同一条目只 +1**，避免多轮引用重复累计。
- 台账不即时写盘；只有任务收口时一次性回写。
- `reason` 用一句话记录引用场景（如"apifox 环境白名单决策依据"），用于审计与防虚报。

## 3. 回写时机（收口闸门）

- 本 skill 已在 `skill-hit-check-rules/references/deferred-gate-registry.md` 注册为**收口前**延迟 gate。
- 非 Plan Mode 实质任务轮：首条 `闸门预告` 登记，收口前执行回写。
- 收口流程：
  1. 检查内存台账是否为空 → 为空则本 gate 无动作，直接 PASS。
  2. 台账非空 → 跑 `scripts/usage_ledger_validate.py` 校验（见下）。
  3. 校验 `ok=true` → AI 编辑三文件计数锚点完成回写（+1、刷新 `last_used_at`、必要时 `usage_days + 1`）。
  4. 校验 `ok=false` → 阻断回写，修正台账中的非法 claim 后再回写。
  5. 回写后跑 `scripts/scan_absorption_candidates.py` 检查是否产生吸收候选（见 `absorption-trigger.md`）。

### `usage_days` 维护规则

- `usage_days` 记录"引用分布在多少个不同日期"，是"跨 ≥ 2 个日期"阈值的直接判据。
- 回写时：若 `last_used_at` 与当天日期不同（或为 null），则 `usage_days + 1` 且 `last_used_at = 当天`；若相同，则只 `usage_count + 1`，`usage_days` 不变。
- 不保存历史日期数组（控体积），`usage_days` 为增量维护的去重天数。

## 4. 防虚报（前置校验）

- `usage_ledger_validate.py` 逐条校验 claim：
  - 锚点存在性：`(file, anchor)` 必须能在对应文件的计数锚点区定位（MEMORY 用 `entity_id`，STYLE/HISTORY 用 `title`）。
  - 可定位性：锚点 key 必须能回指到人类阅读区的真实条目/事件。
  - 会话内去重：重复 claim 只保留一条。
- 输出 `{ok, valid_claims, invalid_claims}`；`ok=false` 时**禁止回写**。
- 校验不通过的原因（如锚点缺失）本身就是信号：要么该条目尚未建锚点（收口时补建），要么 claim 是编造的（丢弃并记录）。

## 5. 机器/人类区同步

- 计数**只写机器区/计数锚点区**，人类阅读区不展示计数（控制启动必读体积）。
- 吸收发生后（`absorbed_to` 非空），人类区条目状态标记为 `已沉淀`，并保留一行指针：`已沉淀为 skill: project-<slug>-<topic>-rules`。
- 状态为 `deprecated` / `stale` / `retired` / `conflicted` 的条目**不参与计数**（生命周期状态优先于计数）。

## 6. 与 `更新时间` 的关系

| 字段 | 语义 |
|---|---|
| `更新时间` | 内容修订时间：条目内容被改写时刷新 |
| `last_used_at` | 最近实际引用时间：条目被引用时刷新 |

两者独立维护，互不联动。

## 7. 防膨胀

- 每个实体仅增 4 个标量字段（约 80 字节）；122 条规模约 10KB，可控。
- 计数锚点区只承载计数，不承载全文、证据或历史。
- HISTORY 锚点随事件裁剪而删除，计数块体积有上限。
