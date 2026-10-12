# Desktop 重启后步骤清单恢复案例

## 来源与问题

- 来源：用户先要求当前会话原生步骤清单必须显示，随后澄清显示故障不得暂停领域任务，并在重启 Codex Desktop 后要求继续。
- 问题：配置已启用 `update_plan`，但重启前活动会话仍未注册该工具；恢复时 Goal 状态仍标记为 `blocked`，容易把纯 UI 故障误当成领域任务阻断。

## 原子裁决

| 条目 | 裁决 | 理由与落点 |
| --- | --- | --- |
| 原生清单实际可见是用户明确要求的验收条件 | 合并 | 保留为待验证 UI 验收；配置、磁盘 projection 或文件面板都不能冒充显示证据。 |
| UI 同步失败必须暂停领域任务 | 拒绝 | 用户明确裁决显示问题不影响任务；沿用 `UI_SYNC_BLOCKED` 降级继续。 |
| Desktop 重启后复查工具注册与当前会话投影 | 合并 | 工具已注册且投影校验通过时立即同步；仅因 UI 失败留下的 Goal `blocked` 状态不阻断用户明确继续。 |

## 同域整理

- 唯一 Owner：`task-plan-rehydration-rules/SKILL.md` 的原生清单验收规则。
- 同域扫描：`skill-hit-check-rules`、`autonomous-execution-rules`、`context-compression-rules`、`agent-runtime-recovery-rules` 及同一 Skill 内的保存和 Goal 流程。
- 清理：重启分支并入既有降级规则；Owner 内 4 处重复 UI 失败处置改为引用唯一 `UI_SYNC_BLOCKED` 规则。其他 Skill 仅保留其路由所需摘要。
- 环境依赖：无新增；沿用已有用户级 Codex 配置和运行时 `update_plan` 工具。`C:\Users\luode\.codex\skills` 已核实为当前正式 Skill 仓库的目录联接。
- 文件体积：以本轮改动前的 14,256 字符为基线，最终 SKILL.md 为 14,457 字符，净增 201 字符；新增验收和恢复信息同时收敛了重复处置描述。

## 验证与评分

- 实际场景：当前线程经历了“必须显示”“显示失败不得暂停”“重启后继续”三条真实用户指令；重启后本回合重新注册 `update_plan`，当前会话 projection 校验通过，随后 `update_plan` 调用成功。没有直接屏幕截图，不能把工具回执称为独立视觉证据。
- 结构校验：`python -X utf8 -B .system/skill-creator/scripts/quick_validate.py task-plan-rehydration-rules` 通过。
- 独立评分：新评委按同一评分表将 HEAD 基线评为 73.8/100，当前版本为 78.5/100，增加 4.7 分。此前另一评委使用不同分值尺度得出 81.30/82.15，未与新评委分数混算；整改后整体架构维度从 8 提高到 9。实测维度未由评委另行执行 prompt 套件，按 5 分中性分，不当作效果验证结论。
- 字典：description 与 `##` 级标题未变化，按仓库规则无需刷新字典。

## 第二阶段：细粒度步骤默认显示（2026-10-12）

- **来源**：用户偏好任务步骤越细越好且数量不设小上限；Goal、普通会话和 Plan Mode 都默认展示，长清单由用户滚动查看。
- **合并项**：新增默认粒度契约与所有模式路由；正式计划步骤优先；Goal 默认清单扩展至至少 10 个阶段，并可按任务工作项继续拆细；无来源恢复 fallback 扩展至 8 项；脚本移除固定 20 项校验并保留 51,200 字节总限。
- **整理去重**：把唯一细节放在 `task-plan-rehydration-rules`；`skill-hit-check-rules`、`context-compression-rules`、`autonomous-execution-rules` 和平台模板只保留路由；Plan Mode 不再等同“不展示”。保留 `UI_SYNC_BLOCKED` 非阻断策略和投影状态安全规则。
- **验证范围**：新增 21 步投影接受用例；Goal 默认十步、状态迁移和 fallback 数量按常量断言；验证脚本测试、Skill quick validation、工程文档 profile、UTF-8 与引用链。UI 无截图时不宣称原生悬浮层实显。
- **旧规则对照**：无独立的 8 维可比基线（上一轮分数评价的是前一阶段）；因此以 `git show HEAD` 的未修改版本作为本轮 8D 基线，并由独立评分确认变化。
- **兼容补强**：旧三步 Goal 清单读取时映射到新默认清单；Goal 允许连续编号的脱敏任务专属步骤超过十项。验证新增旧 registry 迁移、22 步 Goal 接受和错序编号拒绝用例。
