## 代码图谱 MCP（CodeGraph + codebase-memory-mcp）

适用于任何需要长期理解和维护的代码仓库（不限前端 / Godot）。这是一组配合使用的代码图谱 MCP：

| 工具 | 仓库 | 定位 |
|------|------|------|
| CodeGraph | `colbymchenry/codegraph` | **默认入口**：日常理解代码、查调用链、分析改动影响 |
| codebase-memory-mcp | `DeusData/codebase-memory-mcp` | **架构分析补充**：项目架构关系、跨模块依赖、函数调用频率、Route/Service/Controller 关系、ADR 记录 |

**配合规则：**

- CodeGraph 作默认入口，codebase-memory-mcp 作高级图分析工具；不要用 memory-mcp 替代日常的 CodeGraph 探索。
- 仅在架构层任务（架构梳理、跨模块依赖、调用频率统计、ADR）才补充使用 codebase-memory-mcp。
- 两个工具的结果与当前代码不一致时，以当前代码为准，并重新同步对应索引。

**安装与配置：**

- CodeGraph 的强制安装与 `codegraph init` 初始化由 `project-rule-file-bootstrap-rules` 的 CodeGraph 准备规则负责。
- codebase-memory-mcp 按官方仓库 `https://github.com/DeusData/codebase-memory-mcp` 的当前说明安装并建立索引；**不要沿用第三方博客转述里的旧命名、旧参数或旧安装路径**，一切以官方仓库 README 为准。
- 两者均为 stdio 类 MCP，需要时把对应 server 配置补齐到项目级 MCP / Codex 配置（与本 skill 其他 MCP 的配置补齐策略一致）。
- 安装或建立索引失败时，回退到 CodeGraph，再回退到本地搜索与文件读取，不阻塞主任务。
