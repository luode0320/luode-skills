# 来源记录 — test-strategy-rules

## 2026-08-30 外部吸收：`comprehensive-test-case-writer`（全面测试用例编写器）

- **来源类型**：外部 skill（skillhub 市场安装源）。
- **安装位置**：用户级 `C:\Users\luode\.workbuddy\skills\functional-use-cases__skillhub\`；工作区副本 `D:\谷歌云盘\luode-skills\functional-use-cases__skillhub\`。
- **源体量**：SKILL.md 8,501 字节 + `evals/evals.json`（无 references、无脚本）。
- **源处置**：吸收确认后删除双副本（用户级 + 工作区），已删除。

### 落点

| 外部精华 | 落点文件 | 说明 |
|---------|---------|------|
| 8 大质量维度 | `references/test-case-design-methods.md` §1 | 测试域维度定义单一权威 |
| 黑盒五法（等价类/边界值/决策表/状态转换/场景法） | 同文件 §2 | 仅方法定义，接口级落地归 apifox |
| 按任务类型裁剪维度 | 同文件 §3 | 防"全测一遍" |
| 用例质量四性 | 同文件 §4 | 与 apifox Step 5 分工，不层叠 |
| 游戏测试专项 | 同文件 §5 | 条件化加载，去具体游戏名 |
| 维度落地边界（apifox 可落地 vs 转出） | `apifox-cli__skillhub/modules/test-case-from-requirement.md` Step 3.5 | 防非 HTTP 维度伪造接口用例 |
| 下游引用 | `functional-validation-rules/SKILL.md` references 读取规则 | 单一权威收敛 |
| 主入口触发词 | 本 skill `SKILL.md` description + 「用例设计方法（单一权威）」小节 | — |

### 拒绝项及理由

- **7 字段用例模板 + P0-P3 优先级**：本地 apifox 已有 12 字段模板 + 风险导向 P0-P2，更强；引入会形成两套模板、两套优先级。
- **工作流程 7 步 / SMART 原则 / 资源书单**：与本地既有执行流程重复，书单为低频信息。

### 环境依赖

来源条目**不含**环境依赖（无环境变量、宿主配置、hook、依赖安装、路径引用），故本次不登记环境依赖项，也不附加自检能力。
