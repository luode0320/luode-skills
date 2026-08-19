# source-notes（吸收来源记录）

> 归属 owner：`apifox`。记录本 skill 各模块的能力来源，可回指来源仓库/版本。

## 2026-08-19：API测试自动化专家版 v1.5.0（api-test-automation-pro__skillhub）

- **来源**：本地安装 skillhub 包（`api-test-automation-pro__skillhub`，v1.5.0，MIT，category=backend-testing），安装时用户级 + 工作区双副本。
- **来源能力**：REST/GraphQL 功能测试、Spring Doc/OpenAPI 解析、YAML 测试定义、性能测试、契约测试、测试点分析、180 陷阱知识库（Python 工具库形态，约 1 万行脚本 + 18 references）。
- **吸收落点**（详见 `workbuddy-absorption-map.md`）：
  - `modules/test-contract.md` ← contract_guide.md（契约方法论）
  - `modules/test-performance.md` ← performance_guide.md（性能方法论）
  - `modules/test-yaml-definition.md` ← yaml_test_guide.md（YAML 定义方法论）
  - `modules/test-health-score.md` ← health_report.md（五层健康评分）
  - `modules/testing-pitfalls.md` 七~十二节 ← SKILL.md（四层诊断/8 类 Fallback）+ security_checker 分类 + test_pitfalls_checklist.md（Top20/优先级表/高价值陷阱）
  - `modules/test-case.md` 断言顺序/速查 ← SKILL.md 约束 + Assertions 分类
  - `SKILL.md` 路由表 + 三重门控 ← SKILL.md 检查点（Inversion 门控）
  - `test-strategy-rules/SKILL.md` + `references/strategy-dimensions.md` ← 策略级引用与可选维度
- **已删除的源**：吸收确认后删除源 skill 双副本（用户级 + 工作区），内容已全部吸收或登记。
- **整体拒绝的记录**：
  - 22 个 Python 脚本（约 1 万行）：脚本实现层与本地红线"接口级测试必须 apifox 落地、禁本地 shell/curl 代替"冲突，整体拒绝，仅吸收方法论与检查清单。
  - README 提及但实际缺失的 5 个 references（smart_parser_guide.md / diagnostic_guide.md / template_loader_guide.md / memory_system.md / security_checks.md）：均为脚本层专属文档且未落地，拒绝；其分类精华从 README/SKILL.md 可读描述吸收。
  - HTTP 全表参考：低频冗余，本地 troubleshooting/test-case 已覆盖场景。
- **历史吸收（早于本次）**：`modules/testing-pitfalls.md` 原 31 条陷阱与 `modules/test-case-generation.md` 三类用例方法论亦标注吸收自 API 测试类 skill（含本源的 180 陷阱库），本次为补缺式二次吸收。
