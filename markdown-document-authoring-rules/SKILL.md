---
name: markdown-document-authoring-rules
description: 当任务需要创建、修改、审查或交付 Markdown 需求、Bug、计划、架构、测试、交付或工作报告时触发；负责统一正文层级、结论顺序、留白、密度、表格、Mermaid、图片决策、技术附录和视觉验收，领域 skill 继续负责业务语义、验收条件、测试策略和交付状态。
---

# 通用 Markdown 文档写作与呈现规则

## 职责

- 本 skill 是 Markdown 工程文档的唯一公共呈现 Owner。
- 负责读者定位、结论优先、标题层级、段落密度、列表、表格、引用、代码块、Mermaid、图片决策、正文与附录分层和视觉验收。
- 负责把 PPTX 中可迁移的内容表达原则适配为 Markdown 规则。
- 领域 skill 继续负责需求、Bug、计划、架构、测试和交付语义；本 skill 不接管领域字段、业务状态、接口契约、测试断言或发布判断。
- visualization-standard 继续负责 Mermaid 图形类型和图前说明；artifact-storage-rules 继续负责路径、命名、图片根目录和 UTF-8；artifact-delivery-gate-rules 继续负责文档门禁。

## 自动触发

- 创建新的 Markdown 需求、Bug、实施计划、实施周期、任务卡、架构、项目设计、测试、6-review、交付总结或工作报告时。
- 修改上述文档的标题、正文结构、表格、列表、代码块、Mermaid、图片引用或附录时。
- 审查 Markdown 文档的可读性、视觉密度、图形选择、表格宽度、链接、路径、编码或目录归位时。
- 从 PPTX 或其他可视化文档吸收内容组织和视觉表达原则时。
- 多个领域 skill 同时产出 Markdown，需要统一呈现规则时。

## 不触发或不接管

- 不替代 requirement-intake-rules 的需求主文档 Owner。
- 不替代 bug-intake-rules 及 Bug 专项 skill 的现象、复现、根因、修复和验证 Owner。
- 不替代 implementation-planning-rules 的周期、任务、AC、真实测试和停止条件 Owner。
- 不替代 architecture-doc-rules、project-design-doc-rules、test-strategy-rules、delivery-summary-rules 的领域语义。
- 不修改历史 Markdown，不批量迁移旧文档，不改变 PPTX 生成行为。
- 不引入外部渲染器、数值图表库、图片生成器或业务运行时依赖。

## 默认工作流

1. 读取当前领域 skill，冻结文档目标、读者、范围、非范围、完成标准和验证状态。
2. 读取本 skill 的 references，确认正文、附录、表格、Mermaid 和图片的呈现方式。
3. 先写 H1 后的唯一白话开场，依次说明结论、影响、范围、非范围、变化、完成标准、术语说明和验证状态。
4. 选择表达形式：结论用短段落，稳定字段用表格，流程和责任顺序用 Mermaid，原始命令和日志放执行附录，稳定 ID 和证据放追踪附录。
5. 检查标题层级、段落长度、列表深度、表格列数、代码块、链接、引用和 Mermaid 可读性。
6. 按 visualization-standard 的图前目的、关联 ID 和图后异常边界要求补齐图形说明。
7. 按 artifact-storage-rules 处理文件路径、命名、图片根目录、相对引用和 UTF-8。
8. 先运行真实的文档或 skill 验证，再执行测试后的 6-review；不得把人工阅读或静态检查写成真实测试。
9. 发现领域语义、路径 Owner 或图形 Owner 冲突时停止并回到对应 Owner，不自行创建第二套规则。

## Markdown 呈现基线

- 文档标题使用一个 H1；正文按业务阅读顺序组织 H2/H3，不用标题代替段落内容。
- H1 后只保留一段白话开场；技术命令、日志、SQL、接口报文、稳定 ID 和追踪矩阵进入文末连续附录。
- 每个段落只表达一个结论；需要并列比较时优先使用表格；需要顺序关系时优先使用 Mermaid。
- 表格列数以读者能横向比较为准；字段含义、单位、来源、完成标准和证据必须明确。
- 列表用于同层级项目；避免把长段落拆成没有逻辑关系的列表。
- 代码块保留命令、配置、JSON、YAML、Mermaid 和原始输出；代码块前写其用途或输入来源。
- 链接文本说明目标，不使用没有含义的“点击这里”；本地路径遵循 artifact-storage-rules。
- 正文面向业务读者，技术细节放执行附录；追踪附录位于文档末尾，不能在附录后继续添加业务正文。

## 图形与表格路由

| 内容 | 首选表达 | 约束 |
| --- | --- | --- |
| 结论和影响 | 短段落 | 先结论，后解释和证据 |
| 角色、字段、状态、规则对比 | Markdown 表格 | 表头说明单位、来源和判定方式 |
| 顺序、依赖、周期、任务 | Mermaid flowchart | 图前写目的和关联 ID，图后写异常边界 |
| 多角色调用和跨 Owner 路由 | Mermaid sequenceDiagram | 参与者名称和正文术语一致 |
| 状态变化和阻断 | Mermaid stateDiagram-v2 | 明确进入、通过、阻断和停止状态 |
| 数据关系 | Mermaid erDiagram | 只表达结构关系，不代替字段契约 |
| UI、截图、真实产物和外观对比 | Markdown 图片 | 使用 doc/data/images 相对路径、非空 alt 和 IMG-* |
| Mermaid 能表达的流程或结构 | Mermaid | 不使用图片替代 |

## PPTX 原则适配

- 迁移内容决定表达方式、结论优先、层次清晰、留白、对齐、语义对比、图表自解释、装饰克制和最终视觉验收。
- 适配为 Markdown 的标题层级、段落密度、表格比较、Mermaid 图形、代码块和渲染后检查。
- 不迁移幻灯片尺寸、字号、英寸、页面比例、固定页面布局、每页必须有视觉元素、OOXML 和 PowerPoint API。
- 不把固定色板、固定比例和演示文稿封面规则写成 Markdown 强制约束。

## 图片资产决策

- 图片资产决策必须写成“需要”或“N/A + 原因 + 证据”。
- 流程、时序、状态、依赖、数据关系和风险分支必须保留 Mermaid，图片不能替代这些图形。
- UI、截图、真实产物、外观基线和 Mermaid 无法表达的视觉信息可以使用图片。
- 图片统一落到 doc/data/images，正文使用从当前文档位置计算的相对路径，alt 必须包含 IMG-*。
- 本期纯规则、计划和 skill 文档在没有真实视觉产物时使用 N/A，并写清原因和证据。
- 禁止使用占位图、程序绘图、绝对路径、外部热链、Base64、HTML img 和越界路径。

## 领域 Owner 路由契约

1. 领域 skill 先冻结业务语义和完成条件。
2. 本 skill 只处理 Markdown 呈现、图形选择、附录分层和视觉验收。
3. visualization-standard 决定 Mermaid 图形类别和图前说明。
4. artifact-storage-rules 决定文档路径、文件命名、图片路径和编码。
5. artifact-delivery-gate-rules 决定 profile、ID、图形、链接、图片和交付门禁。
6. 发生冲突时按“领域语义 → 公共呈现 → Mermaid 标准 → 存储规则 → 交付门禁”顺序裁决；不可裁决时停止。

## 通过条件

- 文档具有唯一 H1、白话开场、清晰层级、正文与附录边界。
- 图形、表格和正文术语一致，Mermaid 图前有目的和关联 ID。
- 图片决策明确；使用图片时路径、alt、IMG-*、资产清单和签名完整。
- 领域 skill 的业务字段、验收条件、测试入口和停止条件未被删除。
- 新建或修改的文档和 skill 通过对应 validator、quick validation、真实 Mermaid 解析和测试后 6-review。

## 失败和阻断条件

- 出现第二个 Markdown 呈现 Owner。
- 把 PPTX 的物理版式、字号、英寸或 OOXML 混入 Markdown 规则。
- 用图片替代 Mermaid 流程、时序、状态或依赖图。
- 领域语义、测试断言、权限、兼容或回滚边界被改写。
- Mermaid、文档 profile、quick validation、字典、skill 合规或 6-review 失败。
- 发现历史文档批量迁移、外部项目写入、生产访问或超范围文件变化。

## References

- PPTX 可迁移原则：references/pptx-absorbed-principles.md
- Markdown 视觉清单：references/markdown-visual-checklist.md
- Owner 路由契约：references/route-contract.md
- Mermaid 图形标准：../implementation-planning-rules/references/visualization-standard.md
- 文档路径与图片规则：../artifact-storage-rules/references/path-map.yaml
- 白话正文与附录契约：../artifact-delivery-gate-rules/references/plain-language-document-contract.md
- 文档交付门禁：../artifact-delivery-gate-rules/SKILL.md
