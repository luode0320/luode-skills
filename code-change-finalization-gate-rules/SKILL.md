---
name: code-change-finalization-gate-rules
description: 收口闸门，最终回复前按本轮改动类型执行检查。本轮存在代码或测试新增 / 修改时检查：OCR 代码审查、注释链（消费 `comment-rules` 结论）、根 `test/` 测试代码镜像与命名、生产代码测试污染扫描（`scan_test_pollution.py`，FAIL 且未登记豁免为阻断）、测试后的 `6-review` 风格回归、真实运行验证、测试资产清理、`internal/router` 提交前风格、用户手改保护。本轮无代码改动但命中多个 skill 时，只检查已命中 skill 当前阶段的必需动作是否真实完成、工具失败是否已走 `execution-failure-learning-rules`、运行时状态是否真实收口。存在计划内未完成必需项或阻断级缺口时禁止给出「已完成 / 已验证可用」。不产出打卡字段，最终总结由 `reasoning-summary-structure-rules` 渲染。
---

# 代码变更最终收口闸门

在最终回复前确认本轮该做的检查已经真实执行，而不是再跑一遍业务。

## 检查清单（按本轮改动类型取用）

代码或测试有改动时逐项执行：

1. **OCR 代码审查**：读 `references/ocr-review/review-workflow.md`，按 `rule-path-map.md` 匹配文件类型并加载 `rule_docs/` 规则做行级审查。Critical 未修复即阻断；High/Medium 在最终回复提示。
2. **注释链**：消费 `comment-rules` 补齐闸门分区的结论与证据，含位置颗粒度分区的适用性判断。字段、编号、清单细则不在本入口重复定义。本轮有 Python 改动时执行 `python comment-rules/scripts/check_function_header.py --root . --diff-only`，`HEADER: FAIL` 与注释结论冲突时以脚本实测为准。
3. **测试落点**：新增测试文件是否全部落在根 `test/` 的镜像路径且命名一致（Python `*_test.py`、Go ASCII 外部黑盒包）；测试证据与结论写入 `doc/5-tests/` 主文档，不放进 `test/`。细则由 `test-program-rules` 与 `test-strategy-rules` 的 test-asset-governance 定义。
4. **生产代码测试污染**：本轮改动生产代码时执行 `python test-strategy-rules/scripts/scan_test_pollution.py --root . --diff-only`。FAIL 且未在 `.test-pollution-allowlist` 登记豁免即阻断；判据见 `test-strategy-rules/references/production-test-pollution.md`。
5. **真实运行验证**：核心接口、页面、导出、查询、提交或任务入口是否真实跑过。只有静态证据时必须显式降级为「仅静态验证」并给出人工验证交接，不得宣称功能可用。改动触达接口可见行为时，按 `test-strategy-rules` 的接口证据要求核验，本地脚本结果不能顶替。
6. **6-review 风格回归**：真实测试完成后执行 `code-style-consistency-rules` 的 `6-review`，消费 `STYLE` 结论；不执行或结果为需要修复即阻断。
7. **测试资产清理**：本轮产生临时测试数据时按 test-asset-lifecycle 清理，`__pycache__` 一并清理；未产生则写 `N/A + 无临时数据产生`。
8. **`internal/router` 风格**：改动包含 `internal/router` 时检查——无 `.GET(`/`.PUT(`/`.PATCH(`/`.DELETE(`、无 `:id` / `{id}` 路径参数、无 `registerPostRoutes` 或 route 列表驱动注册、路由 path 未经本地常量引用（允许全局根前缀常量）。任一不满足先回改。
9. **用户手改保护**：与旧上下文冲突时先重读当前文件再改，确认最终 diff 未回退用户内容。

本轮无代码改动、但命中多个 skill 时：

1. 对本轮实际命中的 skill（不臆造未命中项）核对当前阶段必需动作是否真实完成：已执行 / 可执行但未执行 / 当前阶段不适用三类。
2. 出现非预期工具、命令、API、模型、浏览器或安装器失败时，核验 `execution-failure-learning-rules` 的分类、恢复与同输入复验证据。
3. 存在 goal/plan/task 等显式状态机制时，确认收口动作已真实执行，只写完成文案不算结束运行时状态。
4. 本轮改动触及契约面（签名 / 形态 / 路径 / 配置键 / 枚举 / 输出格式）时，扫描该契约的消费方并核对；本轮产生的临时脚本、临时文件和后台任务必须清理并回读确认。

## 阻断判定

阻断级：Critical 未修复；测试资产适用但专职 Owner 未执行或缺证据；污染扫描未跑、FAIL 未豁免或豁免理由不成立；测试文件未按镜像与命名规则落位；`comment-rules` 缺结论或结果需修复；未跑 `6-review` 或结果需修复；核心运行路径无真实验证且未降级交接；只有 build / lint / 静态搜索却宣称功能可用；用户手改被回退；临时数据未清理。

非阻断级：缺口不影响当前结论正确性，且不属于当前阶段必需项。作为事实交给最终总结 owner 决定是否展示。

## 边界

- 只做收口检查，不代替业务实现、功能测试或需求验收。
- 不复制注释字段、测试目录清单、污染判据等各 Owner 的细则。
- 不拥有最终输出模板、后续内容或阻断渲染权。
- 当前阶段不适用项不得误报为未执行缺口。

## references

- OCR 审查工作流：`references/ocr-review/review-workflow.md`；路径映射：`references/ocr-review/rule-path-map.md`；语言规则：`references/ocr-review/rule_docs/{语言}.md`。规则源自 <https://github.com/alibaba/open-code-review> 的翻译版吸收。
- 最终条件区块统一读 `../reasoning-summary-structure-rules/references/conditional-sections-rules.md`。
