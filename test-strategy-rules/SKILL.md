---
name: test-strategy-rules
description: 当需要确定测试策略、优先级、覆盖范围和待补测风险，或需要判定「这轮该怎么测」时触发。负责测试域的三条执行通道与两侧治理：代码级/接口级/页面前端级测试如何选、接口测试必须走 apifox 并落地用例、页面测试必须真实浏览器点击、生产代码测试污染判定与硬阻断扫描、测试进程与测试数据的生命周期收口、测试代码与证据的双根落点。当本轮新增或修改测试主文档、测试命名、测试资产落点，或发现测试脚本/fixture/mock 散落时，进入 `test-asset-governance` 条件路由；当出现测试数据清理、测试资产过期或遗留资产处置时，进入 `test-asset-lifecycle` 条件路由。不要用它代替具体测试程序编写、功能验证执行或回归结论判定。
---

# 测试策略规则

只在需要先回答「这次应该怎么测」时使用。已经明确在做功能验证、联调或回归时转交对应执行 skill；只涉及目录、命名、程序或文档落点时转交 `test-asset-governance` 条件路由。

## 测试代码与证据双根

- 活动测试代码、mock、stub、fake、fixture、helper 和数据构造只在根 `test/`；源码关联资产按被测源码目录镜像，跨源码复用才进 `test/shared/`。Python 测试为 `*_test.py`，模拟程序用 `_mock` / `_stub` / `_fake` 后缀。
- `doc/5-tests/` 只保留扁平测试主文档，日志、报告、截图和非可执行证据内联进正文，不新增测试程序或 mock。
- Go 测试只在根 `test/` 的 ASCII 外部黑盒包中，源码目录不允许 `*_test.go`。

## 测试域四条红线（单一权威在 references）

| 名称 | 权威文件 | 一句话 |
|---|---|---|
| 测试隔离红线 | `references/test-isolation-redline.md` | 禁止为测试改动生产代码，按引用面判据判定 |
| 测试进程生命周期 | `references/test-process-lifecycle.md` | 测试收口必关进程，关闭动作要有复查证据 |
| 本地环境配置发现与连接 | `references/local-environment-connection.md` | 判定本地环境看配置归属，不看物理地址 |
| 生产代码测试污染扫描 | `references/production-test-pollution.md` | 五类污染模式与治理四步；扫描脚本硬阻断 |

其他 skill 引用上述名称时以对应 reference 为准，本文件不复制正文。

### 污染扫描（硬阻断）

本轮存在生产代码新增或修改时，收口前必须执行并消费结论：

```bash
python test-strategy-rules/scripts/scan_test_pollution.py --root . --diff-only
```

`POLLUTION: PASS` 放行；`POLLUTION: FAIL` 阻断收口，须先迁移到 `test/` 或在项目根 `.test-pollution-allowlist` 登记豁免并写明理由；`SUSPECT` / `ORPHAN` 为提示级交 `6-review` 判断。

## 测试执行通道（单一权威在 references）

| 通道 | 权威文件 | 适用对象 |
|---|---|---|
| 代码级 | 本地 `test/` 的 `go test` / pytest | 函数、模块、纯逻辑 |
| 接口级 | `references/api-test-channel.md` | 有 method + path、经 HTTP 调用的接口 |
| 页面前端级 | `references/ui-test-channel.md` | 页面、组件、路由、用户交互路径 |

- 接口级统一在 apifox「AI 团队」项目真实运行并落地用例，environment 只允许 `local`；本地脚本覆盖不构成豁免。
- 页面前端级必须用真实浏览器完成至少一条用户路径的点击与交互，断言结果并留证；接口全绿不能替代前端点击。
- 同一轮可能同时含三层：按对象分类各层执行，证据分列，任一层不得顶替另一层。
- 三层之外的条件化补充：`references/integration-test-rules.md`（项目联调）、`references/doc-stage-test-requirement.md`（写需求/实施/Bug 文档时预埋测试要求）、`references/test-sample-distribution.md`（读写接口的样本分布要求，禁伪造数据当通过）。

上述通道文件内的红线与例外口径不再在本文件重复。

## 策略产出流程

1. 确认任务类型、改动范围与主要风险来源。
2. 按上表判定本轮适用哪几层通道，读对应 reference。
3. 用 `references/strategy-dimensions.md` 梳理维度，需要排序时读 `references/priority-model.md`，需要模板时读 `references/strategy-template.md`。
4. 输出策略摘要：任务类型、风险来源、测试类型与优先级、待补测说明；策略摘要写进 `artifact-storage-rules` 约定的测试主文档，不新开策略 md。
5. 分流到 `functional-validation-rules`、`test-regression-rules`、`test-program-rules` 或浏览器执行通道。
6. 收口前确认摘要已真实落盘；进入最终回复前联动 `artifact-delivery-gate-rules` 核对。

## 权责边界

- 只负责测试大盘策略与测试域红线，不代替具体执行验证或回归结论。
- 不把「修改生产代码以便更好测试」纳入任何策略选项。
- 不在需求或修复目标未收敛时硬做测试策略；策略试图覆盖全量却无匹配资源时驳回。
- 不为同一轮测试额外创建策略文档，策略摘要固定落在测试主文档。

## 条件路由：test-asset-governance

命中测试文档、测试命名、测试任务根布局或测试资产散落任一信号时进入本路由；先读 `references/test-asset-governance.md`，再按「中央测试根目录 → 当天时间戳测试主文档 → 中文测试主文档 → ASCII 真实代码镜像 → 资产归档与 gate」顺序执行。

## 条件路由：test-asset-lifecycle

命中测试数据清理、测试资产过期、`__pycache__` 堆积、临时测试资产清理或遗留资产处置任一信号时进入本路由；先读 `references/test-asset-lifecycle.md`，再按「六类资产分类 → 触发条件判定 → 清理策略 → 清理执行 → 证据归档」顺序执行。

## references 读取规则

- 默认读 `references/strategy-dimensions.md`；资产治理读 `references/test-asset-governance.md`；资产生命周期读 `references/test-asset-lifecycle.md`。
- 需要用例设计方法、覆盖维度、黑盒五法与用例质量四性时读 `references/test-case-design-methods.md`；接口级字段模板与 RTM 以 `apifox-cli__skillhub/modules/test-case-from-requirement.md` 为准。
- 需要风险分层结论时读 `references/risk-based-test-conclusion.md`。
- 决定测试主文档与多轮拆分方式时读 `../artifact-storage-rules/references/path-map.yaml` 与 `../artifact-storage-rules/references/update-policy.md`。
- 创建或修改测试策略主文档时读 `../artifact-delivery-gate-rules/references/plain-language-document-contract.md`；涉及浏览器联调或第三方验证时读 `../artifact-delivery-gate-rules/references/review-acceptance-gate-contract.md`。
- Markdown 呈现统一读 `../markdown-document-authoring-rules/SKILL.md`，本 skill 不复制呈现规则。
