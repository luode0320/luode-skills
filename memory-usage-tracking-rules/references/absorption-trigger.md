# 吸收触发与自动吸收（absorption-trigger）

## 目标

定义"高频记忆条目 → 项目本地 skill"的量化触发阈值与自动吸收执行序列，让 `skill-absorption-rules` / `project-local-skills-rules` 的"场景高频、稳定、长期独立"判据从定性变为定量。

## 1. 触发阈值（必须全部满足）

```
usage_count ≥ 3
AND usage_days ≥ 2
AND absorbed_to 为空
AND 条目生命周期状态为 active（非 deprecated/stale/retired/conflicted）
```

- **3 次**过滤偶然引用；**`usage_days ≥ 2`**（引用分布在 ≥ 2 个不同日期）排除单日凑数；与 `project-local-skills-rules` 既有"5+ tool call"沉淀门槛同量级。
- `absorbed_to` 非空即冻结：已吸收条目不重复进候选，除非对应 skill 被删除回退。
- HISTORY 计数仅作**弱信号**：同一主题在 HISTORY 反复出现（`usage_days ≥ 2` 且次数 ≥ 3）可作候选辅助证据，但不能单独触发吸收（吸收候选以 MEMORY/STYLE 为主）。

## 2. 执行序列（收口时自动执行）

| 步骤 | 动作 | 执行者 |
|---|---|---|
| 1 | 跑 `scripts/scan_absorption_candidates.py` 出候选清单（只读，含 usage_count / dates / absorbed_to / suggested_skill_name / dedup_hint） | 脚本自动 |
| 2 | 查重：`ls <项目根>/skills/ \| grep '^project-'`（luode-skills 仓库用 `ls . \| grep '^project-'`）+ 与通用 skill 对照；已覆盖则**更新不新建** | AI 按 `project-local-skills-rules/references/dedup-and-update.md` |
| 3 | 用 `.system/skill-creator/scripts/init_skill.py` 生成 `project-<slug>-<topic>-rules/` 骨架，按 `project-local-skills-rules/references/project-skill-template.md` 填充（含踩坑经验与可直接复制的命令） | 脚本自动 + AI 填充 |
| 4 | 回写原条目标记 `absorbed_to` + 人类区状态"已沉淀"+ 指针行 | AI 按规则 |
| 5 | `quick_validate.py` 校验 + 同域冗余扫描（复用 `skill-absorption-rules` SKILL.md 第 5 步四项检查：重复段落 / 门控层叠 / 散落产物 / 引用链） | 脚本自动 |
| 6 | 登记 `workbuddy-absorption-map.md` / `references/source-notes.md` / `.workbuddy/memory/当日日志` | AI 按规则 |
| 7 | 收口总结列出改动文件清单（diff 锚点）；**不自动 git commit** | 规则强制 |

单轮候选多个时：按 `usage_count` 降序逐个处理，每完成一个 skill 再处理下一个；同一主题的多个条目**合并**为一个 skill（吸收即整理），不重复建 skill。

## 3. 与"人在回路 / 棘轮"的调和

用户已确认"达阈值自动吸收"，不设人工确认闸门。为保持既有 `skill-absorption-rules` 的质量底线，用以下机制替代人工确认：

- **git 可回滚**：吸收写盘后可随时 `git diff` 审计、`git checkout` 回退；收口总结强制列改动文件清单作 diff 锚点。
- **机器可验证的三条件 PASS/FAIL**（替代人工确认）：
  1. `quick_validate.py` PASS；
  2. 同域冗余扫描 PASS（发现可清理冗余未清理 = FAIL）；
  3. `absorbed_to` 指针可达（回写位置正确、skill 目录真实存在）。
  任一 FAIL → **自动回滚本次吸收**（`git checkout` 恢复相关文件），并在收口总结说明回滚原因。
- **事后审计点**：当日日志追加"自动吸收记录"（候选、diff 摘要、校验结论），用户事后可审可回滚。

## 4. 命名与落点

- 落点：`project-<项目slug>-<topic>-rules/` 统一写入**项目根目录 `skills/`**（如 `D:\某项目\skills\project-<slug>-<topic>-rules\`）；luode-skills 仓库特例直接落仓库根（仓库根即 skill 资产库，88 个 skill 平级在根下）。命中由项目级 `AGENTS.md` / `CLAUDE.md` 显式声明引用 `skills/` 目录，AI 按声明扫描命中；不依赖任何工具专属路径（如 `~/.workbuddy/skills/`）。
- 项目 slug 用项目目录名（如 `luode-skills`）；topic 用条目主题短语（如 `memory-usage-tracking`）。
- 通用规则（跨项目通用、不限于本项目的经验）**不得**沉淀为 `project-*` skill，应转交 `skill-absorption-rules` 走通用 skill 更新通道。

## 5. 防重复吸收 / 防膨胀

- 阈值够硬（≥3 次且跨 ≥2 日期），避免偶然引用触发。
- 吸收后 `absorbed_to` 非空即冻结计数，后续引用走 skill。
- 查重硬约束：已覆盖场景只更新不新建。
- 每次吸收复用"吸收即整理"：同主题合并、冗余段落收敛为「单一权威 + 引用」，只增不减视为不合格。
