# 微业务架构规则与相邻 Skill 边界

本 Skill 只拥有业务域隔离、版本目录语义、脚手架、确定性导入检查和 CodeGraph 审查证据编排；它不拥有目录位置、JSON 响应结构或通用代码分层。

| Skill | 关系 | 边界 |
|---|---|---|
| `package-structure-rules` | 强联动、唯一目录 Owner | 决定 `<source-root>/<domain>/` 目录树与版本目录 `<v?>` 位置（router/<v?>/、controller/<v?>/、entity/<v?>/、service/<v?>/）、其他域内目录、Catalog 与 CLI。微业务 Skill 只能引用，不复制。 |
| `codegraph-analysis-rules` | 审查证据 Owner | 提供跨文件导入节点、调用链和影响面检索；本 Skill 将其用于跨域导入审查。 |
| `code-quality-rules` | 结构边界 | 不额外创建 interface、注册或依赖注入层；版本目录边界是用户冻结的跨域隔离边界。 |
| `artifact-storage-rules` | 文档路径 Owner | 决定需求、测试、审查和验收资产的路径。 |
| `architecture-doc-rules` | 可选联动 | 可将业务域与版本目录关系摘要回写项目架构文档。 |
| `project-rule-file-bootstrap-rules` | 初始化衔接 | 先保证规则文件与项目记忆存在；本 Skill 仅幂等写微业务标记。 |

## 明确不再拥有的规则

- 不创建、不维护或不允许根 `contract/` 作为跨业务通信层。
- 不定义目录内部文件名、语言扩展名；这些由 `package-structure-rules` 统一定义。
- 不把版本目录隔离扩展为 HTTP、gRPC、消息队列或真实微服务部署。
