# 工具优先级与回退

## 浏览器相关

当项目命中前端标记，并且任务涉及以下任一场景时，优先使用 `Chrome DevTools MCP`：

- 打开真实页面并交互
- 调试 DOM、样式、控制台错误
- 查看 Network、Performance、Coverage 等 DevTools 能力
- 验证前端页面行为、抓取运行时状态

优先级固定为：

1. `Chrome DevTools MCP`
2. `agent-browser`
3. 其他本地浏览器兜底方式

回退条件：

- 当前环境未安装或未接通 Chrome DevTools MCP
- 任务只需要最基础的浏览器自动化，且暂时无法安装 MCP
- 需要的只是一次性截图或简单表单操作，可临时回退 `agent-browser`

## Godot 编辑器相关

当项目命中 Godot 标记，并且任务涉及以下任一场景时，优先使用 `Godot AI MCP`：

- 创建或编辑场景
- 操作节点、资源、脚本挂载
- 运行项目并读取编辑器或运行态反馈
- 从编辑器抓取当前状态、错误或可视化上下文

优先级固定为：

1. `Godot AI MCP`
2. 其他 Godot 本地兜底方式

回退条件：

- 当前环境未安装或未接通 Godot AI MCP
- 任务只需要静态阅读项目文件，不需要控制编辑器
- 当前只是做代码级修改，尚未进入编辑器联动阶段
