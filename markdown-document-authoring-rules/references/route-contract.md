# Markdown Owner 路由契约

## Owner 清单

| Owner | 负责内容 | 不负责内容 |
| --- | --- | --- |
| markdown-document-authoring-rules | Markdown 正文、层级、留白、密度、表格、Mermaid、图片决策和视觉验收 | 领域业务语义、业务状态、接口、测试断言和发布判断 |
| requirement-intake-rules | 需求主文档、需求字段、来源和需求语义 | 公共 Markdown 排版规则 |
| bug-intake-rules 及 Bug 专项 skill | 现象、复现、根因、修复提案和验证 | 公共 Markdown 排版规则 |
| implementation-planning-rules | 计划、周期、任务、AC、真实测试和停止边界 | 公共 Markdown 排版规则的重复定义 |
| visualization-standard | Mermaid 图类型、图前目的和关联 ID | 完整 Markdown 文章结构 |
| artifact-storage-rules | 文档路径、命名、图片根目录、相对路径和编码 | 文档内容和业务语义 |
| artifact-delivery-gate-rules | 文档 profile、ID、图形、链接、图片和交付门禁 | 领域业务决策和文章内容 |

## 路由顺序

1. 领域 skill 先确定业务语义、读者、范围、完成标准和验证。
2. markdown-document-authoring-rules 决定正文、附录、表格和图形呈现。
3. visualization-standard 决定 Mermaid 类型和图前说明。
4. artifact-storage-rules 决定路径、命名、图片和编码。
5. artifact-delivery-gate-rules 执行 profile 和交付校验。
6. 真实测试通过后执行 6-review。

## 冲突处理

- 业务语义冲突回到领域 Owner。
- Mermaid 图形类型冲突回到 visualization-standard。
- 路径、命名和图片冲突回到 artifact-storage-rules。
- 交付字段和 profile 冲突回到 artifact-delivery-gate-rules。
- 公共呈现规则冲突由本 skill 统一裁决。
- 无法裁决时状态为 blocked，不得通过复制规则建立第二 Owner。

## 消费者接入要求

- 消费者 skill 只增加公共 skill 路由和职责边界。
- 消费者 skill 保留原有业务字段、验收条件、测试入口和停止条件。
- 消费者 skill 不复制公共 skill 的完整视觉规则。
- 任何路由接入都必须通过自身 quick validation。

## 图片与 Mermaid 边界

图片资产决策：N/A + 原因：本契约只描述 Owner 和路由；证据：visualization-standard.md 与 artifact-storage-rules/references/path-map.yaml。
流程、时序、状态和依赖关系必须使用 Mermaid；图片只补充 UI、截图、真实产物或外观信息。
