---
name: test-doc-rules
description: 当新增或修改测试 README、验证说明、测试报告、覆盖说明、测试执行记录时触发。负责统一测试文档的最小结构、记录字段、主文档入口和归档方式；必须以 `artifact-storage-rules` 与 `test-location-rules` 为基准，使用中央约定的测试任务主说明 `README.md` 作为中文主说明入口，并把额外文档放到同一时间戳根目录下的 ASCII 真实代码路径镜像目录中；同时强制禁止为了测试目的污染生产代码（新增测试专用方法、测试专用数据、测试专用结构体字段等）。不要用它代替 test-location-rules、test-program-rules、functional-validation-rules 或 test-regression-rules。
---

# 测试文档规则

只在“测试说明文档应该怎么写、怎么组织、怎么留痕”这个问题上使用这个 skill。
如果当前争议是测试程序怎么写，请转交 `test-program-rules`；如果是功能到底算不算通过，请转交 `functional-validation-rules`；如果是旧能力有没有被带坏，请转交 `test-regression-rules`。

**重要：本 skill 必须服从 `test-location-rules`。中文说明目录只允许存放 `README.md`；如果需要详细说明、案例表、补充报告、截图说明或执行清单，这些文档必须放到同一时间戳根目录下的 ASCII 真实代码路径镜像目录中。**

## 测试隔离红线（强制）

- 严禁为了测试目的改动生产代码语义，包括但不限于新增测试专用方法、测试专用数据、测试专用结构体字段。
- 测试文档中若出现“为测试方便新增生产字段/方法”的做法，必须标记为违规并阻断，不得作为可接受方案沉淀。
- 测试说明只记录测试资产与结论，不为生产代码污染行为背书。

## Skill 作用与适用场景

- 作为测试资源管理链的第四道规则，统一测试文档入口、章节和归档方式。
- 约束测试 README、验证说明、测试报告、覆盖说明和执行记录的最小结构。
- 保证接手人可以先从中文 README 快速理解测试，再按 README 指向找到真实测试代码与证据。
- 防止把测试文档继续散落到 `testing/`、`analysis/`、仓库根目录或中文说明目录之外的随意位置。
- 防止中文说明目录被堆满额外 markdown、截图和报告，重新退化成杂物目录。

## 自动触发信号

- 新增或修改测试 `README.md`、验证说明、测试报告、覆盖说明、测试执行记录。
- 需要给当前测试任务补写执行方法、依赖条件、覆盖范围和验证结论。
- 发现测试已经执行，但没有留下结构化说明和结论。
- 发现有人准备把测试文档写到 `testing/`、`analysis/`、仓库根目录、业务代码目录或中文说明目录之外的任意位置。
- 发现中文说明目录中开始出现多个 `.md`、截图或附件，违反“仅 README”基线。

## 进入后先做什么

1. 先确认测试目录已经遵循 `test-location-rules`，即存在独立的中央约定时间戳根目录。
2. 确认中央约定的测试任务主说明 `README.md` 作为当前任务唯一的中文主说明入口。
3. 区分当前文档属于主 README、详细验证说明、覆盖补充、执行记录还是报告摘要。
4. 如果需要额外 markdown、图片说明或附件，先确定它们对应的真实代码路径镜像目录，再放入 ASCII 路径中。
5. 确认 README 是否已经能说明测试目标、运行入口、依赖条件、覆盖范围和最终结论。

## 默认执行流程

1. 默认先确认遵循 `test-location-rules`：所有测试文档都属于中央约定的测试时间戳根目录。
2. 再读 `../artifact-storage-rules/references/path-map.yaml`、`../artifact-storage-rules/references/naming-templates.md` 与 `../artifact-storage-rules/references/update-policy.md`，确认测试时间戳根目录、中文主说明 `README.md`、ASCII 镜像路径和同一轮测试是否继续复用同一根目录。
3. 默认先读 `references/doc-minimums.md`，确认 README 和补充文档的最小字段。
4. 如果当前文档与测试程序、功能结论或回归结论职责混淆，再读 `references/doc-boundaries.md`。
5. 如果需要判断当前文档是否达标，再读 `references/doc-examples.md` 对照正反例。
6. 输出缺失章节、补充建议、应放入 README 的内容，以及应转移到 ASCII 镜像路径的详细文档。
7. 测试文档未稳定前，不进入正式交付总结或发布留痕阶段。

## 权责边界与不负责事项

- 只负责测试文档结构、字段和归档方式，不负责决定测试资产落点，那属于 `test-location-rules`。
- 只负责把结论记录清楚，不负责判定功能是否通过，那属于 `functional-validation-rules`。
- 只负责把回归范围和结论留痕清楚，不负责决定回归是否充分，那属于 `test-regression-rules`。
- 不负责测试程序实现、断言设计、mock 组织和脚本拆分，那属于 `test-program-rules`。
- 如果文档写不清，是因为测试资产、需求边界或执行事实本身不清，应回流相应上游 skill。

## 需要暂停并确认的条件

- 中文说明目录之外没有找到明确的 ASCII 真实代码路径镜像目录，导致详细文档无处安放。
- 当前 README 既想承载中文总览，又想堆放大量原始日志、截图和明细，结构已经失控。
- 为了补齐文档，需要先补录大量缺失的执行事实、环境信息或测试结果。
- 当前文档准备脱离中央约定的测试时间戳根目录单独放到 `testing/`、`analysis/` 或其他目录。

## 执行通过 / 驳回标准

- 通过：中央约定的测试任务主说明 `README.md` 已经清楚说明测试对象、执行方式、依赖条件、真实资产入口、覆盖范围和最终结论；如有额外文档，也已落在同一时间戳根目录下的 ASCII 镜像路径中，并被 README 正确引用。
- 驳回：README 只剩口头式结论，缺少运行入口和结果依据；补充文档继续散落到 `testing/`、`analysis/`、仓库根目录、业务目录或中文说明目录中，无法支持复现、交接和追溯；或文档把“新增测试专用方法/数据/结构体字段”作为可接受做法记录到生产代码方案中。

## 执行结果归档要求

- 主文档固定归档到 `artifact-storage-rules` 约定的测试任务主说明 `README.md`。
- 主 README 至少包含测试目的、测试对象、执行方式、依赖数据与环境、覆盖范围、真实资产路径和验证结论。
- 额外 markdown、截图说明、执行明细、案例表和附录文档，统一归档到中央约定的测试时间戳根目录下的 ASCII 真实代码路径镜像目录中。
- 测试任务主说明位置、目录命名模板和同一轮测试的复用策略统一遵循 `../artifact-storage-rules/references/path-map.yaml`、`../artifact-storage-rules/references/naming-templates.md` 与 `../artifact-storage-rules/references/update-policy.md`。
- 主 README 必须显式写出这些详细文档或证据文件所在的 ASCII 路径，避免只留一堆孤立附件。
- 如果同一需求拆成多轮独立验证，应分别维护各自时间戳根目录的 README，而不是在一个 README 中持续堆叠历史轮次。

## references 读取规则

- 默认先读 `references/doc-minimums.md`。
- 在定位测试时间戳根目录、中文主说明 `README.md`、ASCII 镜像路径或判断是否继续沿用同一轮测试根目录时，先读 `../artifact-storage-rules/references/path-map.yaml`、`../artifact-storage-rules/references/naming-templates.md` 与 `../artifact-storage-rules/references/update-policy.md`。
- 只有在职责边界混淆时，再读 `references/doc-boundaries.md`。
- 只有在需要正反例或模板参考时，再读 `references/doc-examples.md`。
