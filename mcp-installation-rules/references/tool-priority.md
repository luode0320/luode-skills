# 工具优先级与条件路由

本文件是浏览器工具选择的唯一矩阵来源。工具名称、用户 profile 边界、能力后备和不可用处理均按本文件执行；其他 skill 不得再定义固定的线性优先级。

## 浏览器工具边界

| 工具 | 能力定位 | 适用条件 | 不适用 / 不可用处理 |
| --- | --- | --- | --- |
| `Chrome Plugin` | 连接用户当前 Chrome，复用真实标签、登录态、Cookie、扩展和 profile | 任务依赖用户已经打开的页面、已有认证状态、浏览器扩展或真实 profile | 连接失败时要求修复 Chrome 连接；不得改用独立 profile 工具绕过用户认证边界 |
| `Chrome DevTools MCP` | 独立浏览器调试与验证：DOM、样式、控制台、Network、Performance、Coverage、运行时状态 | 不依赖用户真实 profile 的本地页面调试、页面行为验证、网络或性能诊断 | 未安装或未接通时，只有在任务不依赖 DevTools 专属能力且不需要真实 profile 时，才按下方条件后备；否则阻断 |
| `browser-session-automation-rules` | 隔离 profile / 具名 session 的核心浏览器自动化：打开、快照、交互、认证、等待、截图、批量执行 | 任务需要隔离 profile、具名 session、认证登录、表单交互、数据提取，或独立 profile 的基础自动化在 Chrome DevTools MCP 不可用时 | CLI / 能力不可用时明确阻断；不得用于替代需要 Chrome Plugin 的真实 profile / 登录态 |
| `browser-advanced-testing-rules` | 浏览器高级验证与观测：HAR / 网络记录、视觉 diff、trace / profiling、代理、多 session 观测面板 | 任务明确需要网络 HAR、视觉 / 页面 diff、性能 profiling、录制 trace、代理配置或多 session dashboard 观测 | CLI / 能力不可用时明确阻断；不得用于替代需要 Chrome Plugin 的真实 profile / 登录态 |

## 浏览器路由矩阵

按任务条件选择，不按工具名做无条件替换：

| 任务信号 | 首选工具 | 条件后备 / 处理 |
| --- | --- | --- |
| 已有标签、登录态、Cookie、扩展、用户真实 profile | `Chrome Plugin` | Chrome Plugin 不可用时阻断并要求修复连接 |
| 独立 profile 的 DOM、样式、控制台、页面行为验证 | `Chrome DevTools MCP` | 不依赖 DevTools 专属能力时可使用 `browser-session-automation-rules`；否则阻断 |
| 独立 profile 的 Network、Performance、Coverage 或运行时调试 | `Chrome DevTools MCP` | 无等价能力时阻断，不以基础自动化结果冒充 DevTools 验证 |
| 隔离 profile、具名 session、认证登录、表单交互、批量执行 | `browser-session-automation-rules` | 不可用时阻断，不自动切换到 Chrome Plugin |
| HAR / route、视觉 diff、录制 / trace、代理、多引擎、多 session 观测面板 | `browser-advanced-testing-rules` | 不可用时阻断，不自动切换到 Chrome Plugin |
| 不依赖真实 profile 的基础打开、点击、填写或一次性截图 | `Chrome DevTools MCP`（可用时） | Chrome DevTools MCP 不可用时可条件后备 `browser-session-automation-rules`；仍需满足 local 与安全约束 |

名称约定：

- `Chrome DevTools MCP` 是本仓库统一使用的官方工具名。
- 用户提到“谷歌浏览器 MCP”“Google Chrome MCP”“Chrome MCP”“Chrome DevTools for agents”时，默认都映射到 `Chrome DevTools MCP`，不要在规则里并列成多个不同工具。
- `Chrome Plugin` 是用户真实 Chrome profile 的连接能力，不等同于 `Chrome DevTools MCP`；前者的登录态和浏览器状态不能由后者、`browser-session-automation-rules` 或 `browser-advanced-testing-rules` 自动推断、复制或绕过。

## 通用约束

- 浏览器联调必须完成真实的 local 验证并保留工具与结果证据；“选择工具”不能代替验证本身。
- 路由判断本身不触发 MCP 安装或修改用户 Chrome profile；也不得为绕过连接失败而切换到不等价工具。
- 当所需能力不存在、工具未接通且没有满足安全边界的等价后备时，明确记录阻断，不虚构验证结果。

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
