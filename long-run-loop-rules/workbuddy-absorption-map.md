# 吸收裁决表（workbuddy-absorption-map）

> 本文件登记 long-run-loop-rules 历次吸收的裁决记录，来源可回指。格式：日期 | 来源 | 条目摘要 | 裁决 | 落点 | 整理去重（含同域清理位置）。

## 2026-09-24 内部调整：Goal 模式免确认推进与临时产物清理

- **来源**：用户指令（2026-09-24，内部更新通道，无外部原文）
- **裁决数**：内部诉求拆解 4 条原子条目 → 全部合并（无拒绝、无保留现状）
  - A1「Goal 模式 = 计划已完成，直接实现」→ 合并
  - A2「执行分歧按 agent 推荐方案推进，不要求用户确认」→ 合并
  - A3「分歧无法判定时自行分析得出最推荐方向并默认执行」→ 合并（补最安全兜底口径）
  - A4「临时生成的文件和脚本执行后删除，不污染项目目录」→ 合并（落为引用既有 Owner，不新建规则）
- **落点（单一 skill：long-run-loop-rules 为 Goal 模式 Owner）**：
  - 新增 `SKILL.md`「Goal 模式免确认推进（分歧按推荐方案执行）」章节（计划视为已完成 / 分歧自行裁决 / 推荐方向判定顺序 / 最安全兜底 / 红线 / 临时产物清理 / 边界与退出）+ description 补口径
  - 新增 `references/safety-mechanisms.md`「Goal 模式免确认推进」章节（只写与安全熔断的衔接，规则本体引用 SKILL.md，避免双权威）
  - 联动 `autonomous-execution-rules`（SKILL.md description + 必须暂停节点补例外；`continuation-and-pause.md` 新小节 + 暂停项收缩）
  - 联动仓库级 `AGENTS.md` / `CLAUDE.md`（新增同主题章节，双文件同哈希）
- **主要裁决理由**：
  - 合并 A1-A3：Goal 模式语义在本地已由 `long-run-loop-rules`（Goal 生命周期）与 `autonomous-execution-rules`（执行许可/暂停边界）共同承载，本次是给「Goal 激活态」补免确认推进语义，属既有 Owner 内部更新，不新增 skill 目录。
  - 合并 A4 但不新定义：临时产物清理已有唯一 Owner `runtime-process-cleanup-rules`（零豁免原则 + 三层清理对象 + 收口回读），本 skill 只写引用，避免与既有清理规则形成双权威。
  - 保留既有红线未放开：提交授权、`local` 连接、凭据、跨项目写入、安全熔断均保持原 Owner 口径。
- **整理去重（同域扫描结论）**：
  - 扫描范围：long-run-loop-rules（自身）+ autonomous-execution-rules + runtime-process-cleanup-rules + git-collaboration-rules + skill-hit-check-rules（延迟 gate 注册表）+ AGENTS.md/CLAUDE.md
  - 发现并收敛 1 处本次引入的重复风险：免确认推进口径同时在 `SKILL.md` 与 `safety-mechanisms.md` 展开 → 收敛为单一权威（SKILL.md 详述，safety-mechanisms.md 只留与安全熔断的衔接并引用）
  - 发现并修正 1 处本次引入的编号漂移：新章节插入后 `safety-mechanisms.md` 中「独立验证」交叉引用编号与章节号不一致 → 还原为「6. 独立验证」
  - 发现并修正 1 处本次引入的结构错位：新章节一度被放入「智能检测」子节 → 移出为独立顶层章节，保持原编号语义
  - 与 `runtime-process-cleanup-rules` / `git-collaboration-rules` 无重复无层叠（引用式衔接，职责层级不同）
  - 结论：PASS
- **环境依赖**：N/A（规则纯文本，无环境变量/宿主配置/hook/依赖/路径引用）
- **自检能力**：N/A（无环境依赖项）
- **净增体积**：待收口统计
- **删除源**：N/A（内部更新通道，无外部安装源）
- **评分**：内部更新通道无吸收前基线，按 `skill-absorption-rules` 用 `quick_validate.py` 结构校验替代棘轮；校验结果见收口说明

## 2026-08-23 吸收：loop-engineering（skillhub）

- **来源**：`loop-engineering`（skillhub 市场安装源，本地目录 `~/.workbuddy/skills/loop-engineering__skillhub/`，SKILL.md + references/{patterns,config-examples,anti-patterns,integration}.md 全部读原文）
- **裁决数**：外部拆解 18 条原子条目 → 合并 7 组 / 保留本地 6 组 / 拒绝 5 组
- **落点（单一 skill：long-run-loop-rules）**：
  - 新增 `references/loop-patterns-library.md`（8 模式压缩 + 选择指南 + 组合建议 + 与本 skill 主路径对接）
  - 修改 `references/safety-mechanisms.md`（补 3 节：4 反馈信号处理 / 5 最小可行循环 / 6 独立验证；安全边界汇总 +3 遵守 +2 禁止）
  - 修改 `references/completion-marker-pattern.md`（补「独立验证（控制器职责，强制）」节）
  - 修改 `references/loop-config-schema.md`（补「Automation 触发参数心智」节）
  - 修改 `SKILL.md`（补范式定位导语 / /loop 定时循环映射 / 循环模式选择 3 节 + 维护注意事项 +1 条）
- **主要裁决理由**：
  - 合并 A1 范式演进 / A2 /loop vs /goal / B1-B8 模式库 / B9-B10 选择指南 / C1 Automation 心智 / D3 反馈信号 / D5 最小可行循环 / D6 反馈信号污染 / E2 可观测部分
  - 保留本地 A3 组件表 / A4 设计原则 / D1 无终止 / D2 单 agent 过大 / D4 状态丢失（本地 safety-mechanisms 已覆盖且更具体）
  - 拒绝 C2-C5 平台无关伪代码（本地有具体脚本实现，避免体积膨胀）/ E1 OpenClaw 集成（平台不匹配，WorkBuddy/Codex 环境）
- **整理去重（同域扫描结论）**：
  - 扫描范围：long-run-loop-rules（自身）+ autonomous-execution-rules + execution-failure-learning-rules + parallel-task-dispatch-rules + goal/loop（skillhub 教育源）
  - 发现并收敛 1 处**本次引入的交叉重复**：独立验证手段列举在 safety-mechanisms.md「6. 独立验证」与 completion-marker-pattern.md「独立验证」逐字重复 → 收敛为单一权威（completion-marker-pattern.md 详述手段，safety-mechanisms.md 改为引用）
  - 发现并修正 2 处**存量不一致**：SKILL.md 配置表缺 `max_runtime_minutes`/`worker_timeout_minutes` 两参数（已补全）；loop-config-schema.md 示例 `--max-runtime` 与 schema 名不一致（已改为 `--max-runtime-minutes`）
  - 与 autonomous-execution-rules / execution-failure-learning-rules 无重复无层叠（职责层级不同）
  - 结论：PASS
- **环境依赖**：N/A（规则纯文本，无环境变量/宿主配置/hook/依赖/路径引用）
- **自检能力**：N/A（无环境依赖项）
- **净增体积**：吸收前目录 ~20.4KB → 吸收后 ~34.0KB（净增 ~5.5KB，其中模式库 6.2KB 为外部 15KB 原文压缩版）
- **删除源**：已删除本地安装源 `~/.workbuddy/skills/loop-engineering__skillhub/`
- **评分**：见 8 维棘轮验证记录（基线 vs 吸收后）

## 2026-08-23 吸收：dw-goal-breakdown（skillhub，目标拆解）

- **来源**：`dw-goal-breakdown`（skillhub 市场安装源，工作区目录 `D:\谷歌云盘\luode-skills\dw-goal-breakdown__skillhub/`，SKILL.md 读原文；v1.0.0，作者 Dream，MIT）
- **裁决数**：外部拆解 5 条原子条目 → 合并 4 / 拒绝 1（拒绝项：源文件排版缺陷——逐字换行乱码、`示例: None` 占位）
- **落点（单一 skill：long-run-loop-rules）**：
  - 新增 `references/goal-breakdown-before-loop.md`（倒推法三步：澄清目标与 deadline → 拆 3 层动作 → 标首个最小可行步；输出与 goal objective 衔接；边界：工程计划转 implementation-planning-rules、业务切片转 requirement-splitting-rules）
  - 修改 `SKILL.md`（触发后行为补"目标模糊先拆解前置"；语义触发示例补"拆解目标 / 怎么实现 / 大目标太小步 / OKR"限定词）
- **主要裁决理由**：
  - 合并 A1 适用场景三件套（可衡量结果/月→周→日/今日第一步）/ A2 倒推法流程 / A3 首个最小可行步（10 分钟可启动）/ A4 转行示例
  - 拒绝 A5 排版缺陷（本地 skill 规范禁止乱码与空占位）
- **整理去重（同域扫描结论）**：
  - 扫描范围：long-run-loop-rules（自身）+ implementation-planning-rules + requirement-splitting-rules + requirement-intake-rules + goal（skillhub 教育源）+ autonomous-execution-rules
  - 发现并收敛 1 处本次引入的交叉重复：goal-breakdown-before-loop.md（方法本体）与 implementation-planning-rules/references/goal-breakdown-seed.md（入口三问）步骤高度重复 → 收敛为单一权威（before-loop 详述方法），seed 改为引用式（`../../long-run-loop-rules/references/goal-breakdown-before-loop.md`）只承接工程域使用时机
  - 关键词扫描（倒推法/最小可行步/周→日/10 分钟可启动/拆解目标/大目标太小步）：除本次两处新落盘文件外 0 命中；无门控层叠（SKILL.md 新增触发词已限定"目标模糊需先拆解再执行时"，与 implementation-planning-rules 的"计划型问题"语义分域）
  - 结论：PASS
- **环境依赖**：N/A（规则纯文本，无环境变量/宿主配置/hook/依赖/路径引用）
- **自检能力**：N/A（无环境依赖项）
- **净增体积**：吸收前目录 ~34.0KB → 吸收后 ~36.1KB（净增 ~2.1KB：before-loop.md 1.8KB + SKILL.md 两处小节 0.3KB）
- **删除源**：已删除工作区安装源 `dw-goal-breakdown__skillhub/`
- **评分**：8 维棘轮验证 long-run-loop-rules 基线 81.0 → 吸收后 86.5（+5.5，主要提升：边界条件覆盖模糊目标 fallback、指令具体性给出 3 层/10 分钟参数）；新分严格高于基线，保留。评分方式：第三方视角（间隔一轮重新打分）。
