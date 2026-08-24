# Case：skill-merger 吸收（2026-08-23）

> 本次吸收的完整裁决表见 `workbuddy-absorption-map.md`（2026-08-23 skill-merger 条目）；来源记录见 `source-notes.md`。本 case 记录**可迁移的判断经验**，供后续吸收「同类 skill（多技能关系处理类）」对照。

## 场景

用户要求把外部 skill **mimo-skill-merger（技能合并器）**吸收进本地 `skill-absorption-rules`（吸收规则自身）。外部源 v1.3.0、74 行 SKILL.md + 24 行 details.md，MIT-0，17 条原子规则。

## 关键裁决经验（可迁移）

1. **「吸收类 skill 吸收到自己」时的落点判断**：skill-merger 的三策略（吸收/融合/编排）处理的是**自有技能间**的关系；本地 skill-absorption-rules 的「内部更新通道」触发信号已含"把这两个 skill 合并"但无执行细则 → 落点为补 `references/merge-strategies.md`，不新建目录（符合红线「优先补现有 skill 的 reference」）。
2. **外部策略与本地红线的冲突处理（融合型）**：skill-merger 的融合型产出"新技能 C"——与本地红线「不新增同类 skill 目录」直接冲突。处理：**保留策略精华、改写落点**（融合产物落现有主 skill 的 reference），在 reference 头部显式标注本地红线适配。不是整条拒绝，也不是原样照搬。
3. **形态不匹配的典型拒绝项**：版本管理（新技能 v1.0.0）与命名规则（主功能词+后缀）——本地合并产物是 reference/正文补丁、无新技能实体，这两条无载体 → 拒绝，理由写"形态不匹配"。
4. **与本地「读原文」纪律冲突的拒绝项**：skill-merger 反合理化④"只读 description + 前 3 步即可判断"——本地红线「能查证就不要凭记忆」要求读 SKILL.md + references 原文 → 拒绝（本地更强）。注意区分：快速扫描只可用于**预判策略**，不可用于**内容裁决**。
5. **术语防层叠**：外部「吸收型（技能间子集吸收）」与本地「外部吸收通道（外部精华→本地）」语义不同——在 reference 内显式区分，避免后续混用。

## 净增体积与整理去重

- 外部源 3KB（SKILL.md 3004B + details.md 734B）→ 合并 8 项精华 → 新 reference `merge-strategies.md` 3889B。
- SKILL.md 正文仅净增 3 行（三通道表格 1 行 + references 读取规则 1 行），细则全部下沉 reference，符合「单一可编辑资产 + 吸收即整理」。
- 同域扫描（absorption / audit / split-preserve / hit-check）0 冗余 PASS：三策略为本地缺失能力，与 audit 只读、split 反向拆分语义可区分。
- 体系净增约 +1.4KB 等价（新内容 4.4KB − 删源 3KB）。

## 棘轮验证

独立子 agent 8 维评分：基线 75.8 → 新分 86.8（+11.0）PASS，6 维提升、2 维持平；`quick_validate.py` 结构校验 PASS；实测 3 场景（合并两 skill / 差异大拒绝合并 / 吸收 skillhub 源）全部可被新规则直接指导。

## 复盘教训

- 吸收「关系处理类 skill」时，外部策略名与本地通道名可能同词异义（吸收型），必须做术语显式区分，否则后续裁决会混用。
- 外部"兜底/反合理化"类规则（防半途而废）对本地有真实补强价值——本地强调"必须做"但缺少"防止找借口不做"的对抗机制，这类精华值得优先吸收。
