# 项目当前状态

## 当前任务

- 目标：按 `SRC-SKILL-STREAMLINE-20260721-001` 完成需求、实施、测试、Bug、审查、验收六域 Skill 的结构精简，保持自动触发与用户习惯，完成候选映射、迁移、真实删除、测试、审查和验收。
- 范围：36 个目标域 Skill；11 个退役入口；活跃引用、references、agents/scripts/templates 的物理归属、字典、工程文档和项目记忆。
- 非范围：不以模型能力代替规则；不回写历史归档；不改 `.codex/config.toml`；当前轮未获 Git 历史写入授权。
- 状态：已完成 `CYCLE-SS-01` 至 `CYCLE-SS-06`。六域结构精简、自动触发保持、真实删除、字典、任务级证据、审查与最终验收均已完成。

## 已完成

- 11 个 `merge_retire` source 均已真实删除；`requirement-gap-rules` 的遗漏已在 CYCLE-SS-06 纠正，受保护 gap-routing 细则迁入 `requirement-intake-rules`。
- 25 个保留或 reference_refactor owner 均保持原自动触发语义；审查/验收域四个 owner 采用 owner 内共享证据 reference，提交级审查保持独立专责。
- 全量 `baseline`、`trigger` 与 `post-delete` 验证通过；字典为 `implemented_total=75`、`planned_missing=0`、`seed_total=33`。
- CYCLE-SS-05 与 CYCLE-SS-06 的任务级 TEST/REVIEW/ACCEPT、周期审查、周期验收和工程文档 profile 均已落盘并通过。

## 待完成

- 无。

## 阻断

- `BLK-SS-001`：Obsidian bridge 返回 `VAULT_NOT_REGISTERED`，仅阻断 vault 沉淀；不影响本仓库 local 任务完成结论。
- `.codex/config.toml` 是无关未提交改动，持续排除。

## 验证

- `validate_domain_streamlining.py --phase baseline`：PASS。
- `validate_domain_streamlining.py --phase trigger`：PASS。
- `validate_domain_streamlining.py --phase post-delete`：PASS。
- `skill-dictionary/generate_dictionary.py`：PASS，`planned_missing=0`。

## 下一执行点

- 原始六域精简目标已完成；除非用户提出新目标，不继续扩展或自动新增整理工作。
