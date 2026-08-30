# 吸收裁决表 — test-strategy-rules

## 2026-08-30 吸收 `comprehensive-test-case-writer`（全面测试用例编写器）

- **来源**：skillhub 安装源，用户级 `C:\Users\luode\.workbuddy\skills\functional-use-cases__skillhub\`（SKILL.md 8,501 字节 + evals/evals.json；无 references），工作区同名副本 `D:\谷歌云盘\luode-skills\functional-use-cases__skillhub\`。
- **通道**：外部吸收通道（本地安装源模式）。
- **环境依赖**：N/A（源为纯方法论，无 CLI / 环境变量 / hook / 依赖安装 / 路径引用）。
- **用户确认**：落点 `test-strategy-rules` 为权威；游戏测试专项吸收为条件化小节；apifox 侧只补维度边界表。

| # | 外部条目 | 本地现状（吸收前） | 裁决 | 落点 | 整理去重 |
|---|---------|-------------------|------|------|----------|
| 1 | 需求文档 / 现有用例双输入驱动 | apifox `test-case-from-requirement.md` 已覆盖且更强（五维预检 + RTM 双向追溯） | 保留本地 | — | N/A（本地更强，未重复落） |
| 2 | 8 大测试维度（功能/性能/安全/易用性/界面/兼容性/异常/游戏） | 测试域 5 个 skill **零维度定义**；`strategy-dimensions.md` 只有策略维度、无质量维度 | 合并 | `references/test-case-design-methods.md` 第一节 | 未改 `strategy-dimensions.md`（策略维度 ≠ 质量维度，避免概念层叠） |
| 3 | 5 种黑盒方法（等价类/边界值/决策表/状态转换/场景法） | apifox 有（接口级）；**测试域无权威**，非接口场景无方法可依 | 合并 | 同文件第二节（方法定义 + 适用信号 + 用例下限） | 方法定义声明接口级落地归 apifox，避免两套方法表 |
| 4 | 用例模板 7 字段 + P0-P3 四级优先级 | apifox 12 字段模板 + 风险导向 P0-P2，本地更强 | 拒绝 | — | N/A（拒绝原因：引入会形成两套模板与两套优先级） |
| 5 | 质量检查点（正确性/完整性/可执行性/一致性） | apifox Step 5 有 11 项覆盖验证；测试域无 | 合并 | 同文件第四节（四性） | 加一句分工声明：接口级以 apifox Step 5 为准，四性只做非接口场景与跨维度总判，防门控层叠 |
| 6 | 维度覆盖裁剪（不是每轮铺满 8 维） | 本地无，易导致"全测一遍" | 合并 | 同文件第三节（按任务类型最小维度集） | 与 `priority-model.md` 明确分工：优先级取舍归 priority-model，维度裁剪归本文件 |
| 7 | 游戏测试专项（玩法/数值平衡/技能道具/联机/付费/本地化/更新/兼容矩阵） | 本地无 | 合并（条件化） | 同文件第五节，命中游戏项目时加载 | 去掉原神/星铁等具体游戏名与米哈游语境，只保留通用方法；显式声明游戏服务端 HTTP 接口仍走 apifox 通道 |
| 8 | 评审优化现有用例闭环 | apifox 规则 D「补全前先评估覆盖缺口」已含 | 保留本地 | — | N/A（已覆盖） |
| 9 | 工作流程 7 步 / 最佳实践 SMART / 资源书单 | 本地执行流程已覆盖；书单为低频 | 拒绝 | — | N/A（拒绝原因：低频且与既有流程重复） |

**净增减预估**：新增 reference 1 个（约 7.5 KB）+ SKILL.md 新增 1 小节（约 600 字节）+ description 补触发词（约 130 字节）；整理去重 3 处（见下）。无环境依赖条目，故不附加自检能力。

**同域冗余扫描（2026-08-30 执行）**

- 扫描范围：`test-strategy-rules`、`test-program-rules`、`test-regression-rules`、`functional-validation-rules`、`bug-validation-rules`、`apifox-cli__skillhub`。
- ① 重复段落：新增关键词（质量维度 / 黑盒五法 / 状态转换 / 决策表 / 等价类 / 四性 / 用例设计方法）在 4 个兄弟 skill 中**零命中**，无逐字重复；apifox 侧维度边界表与 test-strategy-rules 维度表措辞与列定义不同（前者讲"可落地 / 落地方式 / 转出去向"，后者讲"要回答的问题 / 典型判据 / 执行通道"），并互引单一权威，属域专属补充而非重复。
- ② 门控 / 概念层叠：四性检查与 apifox Step 5 覆盖验证存在层叠风险 → 在 reference 第四节补分工声明收敛；权威声明由"4 个 skill 直接引用"改为"统一以本节为准"（原表述引用链不可达）。
- ③ 散落产物：新建 reference 已被 `test-strategy-rules/SKILL.md` 与 `functional-validation-rules/SKILL.md` 引用，无孤立文件。
- ④ 引用链：全部可达（已逐条核对路径存在），UTF-8 无乱码。
- 扫描结论：**发现 2 处、清理 2 处、PASS**（层叠风险 1 处 + 引用链不可达声明 1 处，均在本闭环内收敛）。

**顺手整理（吸收即整理）**

1. `test-strategy-rules/SKILL.md` 末尾孤行 `- 基于风险的测试结论分层：references/risk-based-test-conclusion.md` 错挂在「四、与其他测试类型的关系」小节下 → 移入「references 读取规则」并补全句式（语义零丢失）。
2. `functional-validation-rules/SKILL.md` reads 规则第 89 行"测试主文档、测试主文档"重复词 → 去重。
3. 权威声明表述修正，避免空引用。

**棘轮验证**：吸收前测试域在"用例设计方法"维度为空白（无可引用的方法定义、无维度清单、无质量判定），吸收后新增单一权威 reference + 3 处下游引用 + apifox 边界表，覆盖从 0 → 有；体积净增约 8.2 KB（其中 SKILL.md 主体仅 +730 字节，其余在按需加载的 reference），符合"净增最小化"。保留。

**源处置**：吸收确认后删除源 skill 双副本（用户级 + 工作区），详见 `references/source-notes.md`。
