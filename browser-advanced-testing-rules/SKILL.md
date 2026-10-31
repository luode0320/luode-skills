---
name: browser-advanced-testing-rules
description: 面向 AI 代理的本地浏览器高级验证与观测：网络 HAR 记录/路由拦截、视觉与页面 diff、性能 profiling、会话录制 trace、代理配置、非 Chrome 引擎、跨 session 观测面板（dashboard）。当任务需要本地网络 HAR、视觉/页面 diff、性能 profiling、录制 trace、调试代理或多 session 观测面板时触发。普通打开页面、快照交互、认证登录、隔离 profile、批量执行请转交 `browser-session-automation-rules`；普通用户 Chrome profile 和一般页面调试优先按浏览器路由选择 Chrome Plugin 或 Chrome DevTools MCP；云端自主长链、托管并发、地域出口、托管代理、隐身或合规验证码等 Browser Use Cloud 专属需求转交 `browser-use-cloud-rules`。
allowed-tools: Bash(npx agent-browser:*), Bash(agent-browser:*)
---

# 使用 agent-browser 进行浏览器高级验证与观测

本 skill 与 `browser-session-automation-rules` 是同源拆分：核心工作流（打开页面、快照、交互、认证、session 管理、批量执行、截图清理）由对方负责；本 skill 只负责网络 HAR 记录、视觉/页面 diff、性能 profiling、录制 trace、代理配置、非 Chrome 引擎和多 session 观测面板。域名白名单、动作策略、输出上限、配置文件优先级、`--engine` 引擎选择和项目联调路由规则两组同等适用，各自维护一份。

本 skill 只管理本地高级验证，不接 Browser Use Cloud。需要 Cloud 托管环境或地域出口时转交 `browser-use-cloud-rules`；本地代理能力不能被描述成 Cloud 托管代理，Cloud 缺 key、账单或费用确认时也不得回退本 skill 绕过收费闸门。

执行前命中浏览器、session 或高风险调用时，先触发 `execution-failure-learning-rules` 的 `prevent` 并查阅 [references/execution-failure-casebook.md](references/execution-failure-casebook.md)；执行失败后走 `recover`，修复并按同一成功标准复验后再写 candidate。

## 网络 HAR 记录与路由拦截

```bash
agent-browser network requests                 # 查看已跟踪请求
agent-browser network requests --type xhr,fetch  # 按资源类型过滤
agent-browser network requests --method POST   # 按 HTTP 方法过滤
agent-browser network requests --status 2xx    # 按状态码过滤（200, 2xx, 400-499）
agent-browser network request <requestId>      # 查看完整请求 / 响应详情
agent-browser network route "**/api/*" --abort  # 拦截并中止匹配请求
agent-browser network har start                # 开始 HAR 录制
agent-browser network har stop ./capture.har   # 停止并保存 HAR 文件
```
完整命令参考（含全部过滤选项）见 `browser-session-automation-rules` 的 [references/commands.md](../browser-session-automation-rules/references/commands.md) 的 `Network` 小节。

## Diff（验证变化）

执行动作后可以用 `diff snapshot` 验证页面是否按预期发生变化。它会比较当前 accessibility tree 与当前 session 中上一次快照之间的差异。

```bash
# 典型流程：snapshot -> action -> diff
agent-browser snapshot -i          # 先拍一份基线快照
agent-browser click @e2            # 执行动作
agent-browser diff snapshot        # 看差异（自动与上一份快照比较）

# 视觉回归/监控：先保存基线截图，再在后续比较
agent-browser screenshot baseline.png
agent-browser diff screenshot --baseline baseline.png

# 比较两个 local 页面状态
agent-browser diff url http://localhost:3000 http://localhost:3001 --screenshot
```
`diff snapshot` 用 `+` 表示新增、`-` 表示删除，格式类似 git diff。`diff screenshot` 会输出一张差异图，把变化的像素高亮成红色，并给出不匹配百分比。

## 录制与性能 Profiling

```bash
agent-browser record start demo.webm   # 录制会话视频
agent-browser record stop              # 停止录制
agent-browser profiler start           # 启动 Chrome DevTools profiling
agent-browser profiler stop trace.json # 停止并保存 profile（路径可选）
```
`--headed`、`highlight`、`inspect`（打开可视浏览器、高亮元素、打开 DevTools）属于核心调试能力，见 `browser-session-automation-rules` 的"可视化浏览器（调试）"小节。视频录制细节见 [references/video-recording.md](references/video-recording.md)，性能分析细节见 [references/profiling.md](references/profiling.md)。

## 代理配置

可在 `agent-browser.json` 或 CLI flag 中设置代理：
```json
{ "proxy": "http://localhost:8080" }
```
地域测试、代理轮换和认证代理的完整配置见 [references/proxy-support.md](references/proxy-support.md)。

## 观测面板（Observability Dashboard）

这个 dashboard 是独立的后台服务，用于展示所有 session 的实时浏览器视口、命令活动和 console 输出。

```bash
agent-browser dashboard install   # 只需安装一次
agent-browser dashboard start     # 启动 dashboard 服务（后台运行，默认端口 4848）
agent-browser open example.com    # 所有 session 都会自动显示在 dashboard 中
agent-browser dashboard stop      # 停止 dashboard
```
Dashboard 与浏览器 session 相互独立，默认运行在 4848 端口（可通过 `--port` 调整）。所有 session 都会自动向 dashboard 推流。

## 安全
所有安全特性都是可选开启的。默认情况下，agent-browser 不会限制导航、动作或输出。

### Content Boundaries（推荐给 AI 代理）
```bash
export AGENT_BROWSER_CONTENT_BOUNDARIES=1
agent-browser snapshot
```

### 域名白名单
```bash
export AGENT_BROWSER_ALLOWED_DOMAINS="example.com,*.example.com"
agent-browser open https://example.com        # 允许
agent-browser open https://malicious.com       # 阻止
```

### 动作策略
```bash
export AGENT_BROWSER_ACTION_POLICY=./policy.json
```
认证金库相关操作（如 `auth login`）不会受 action policy 限制，但仍受域名白名单限制。

### 输出上限
```bash
export AGENT_BROWSER_MAX_OUTPUT=50000
```

## 配置文件
可以在项目根目录创建 `agent-browser.json` 保存持久配置。优先级从低到高：`~/.agent-browser/config.json` < `./agent-browser.json` < 环境变量 < CLI flags。可通过 `--config <path>` 或环境变量 `AGENT_BROWSER_CONFIG` 指定自定义配置文件。所有 CLI 选项都映射为 camelCase key。用户级配置和项目级配置里的 extensions 会合并，而不是互相覆盖。

## 浏览器引擎选择
通过 `--engine` 指定本地浏览器引擎，默认是 `chrome`。
```bash
agent-browser --engine lightpanda open example.com
export AGENT_BROWSER_ENGINE=lightpanda
agent-browser --engine lightpanda --executable-path /path/to/lightpanda open example.com
```
支持 `chrome`（默认）和 `lightpanda`（无头浏览器，内存更小速度更快，不支持 `--extension`/`--profile`/`--state`/`--allow-file-access`）。

## 深入文档

| Reference | 适用场景 |
| --- | --- |
| [references/video-recording.md](references/video-recording.md) | 调试和留档时的视频录制 |
| [references/profiling.md](references/profiling.md) | Chrome DevTools profiling 与性能分析 |
| [references/proxy-support.md](references/proxy-support.md) | 代理配置、地域测试、代理轮换 |
| [references/execution-failure-casebook.md](references/execution-failure-casebook.md) | 浏览器/session/snapshot 执行失败案例与恢复标准 |
| `browser-session-automation-rules` 的 [references/commands.md](../browser-session-automation-rules/references/commands.md) | 完整命令参考（含 Network、Diff 等本组用到的全部选项） |

## 项目联调规则

本 skill 不拥有本地联调流程。联调何时触发、进程基线收口、local 环境边界、授权注入、进程收口与证据要求，全部由 `test-strategy-rules` 的《页面/UI 级测试执行通道（强制）》与《测试进程生命周期（强制）》定义，本 skill 只消费该结论，不重复定义，也不得据此另立一套流程。

### 本 skill 在此流程中的位置（强制）

- 工具选择按 `mcp-installation-rules` 的统一路由；只有本轮需要 HAR/route 记录、视觉 diff、性能 profiling、录制 trace、调试代理、非 Chrome 引擎或多 session 观测面板时，才由本 skill 接管执行。
- 其余浏览器操作场景交给 `browser-session-automation-rules`；云端长链交给 `browser-use-cloud-rules`。
- 高级观测产物（HAR、trace、diff 报告、profile）必须与本轮测试证据一并落盘，并在结论中标注其覆盖的页面与操作路径；不得只给观测文件而不给判定。
- 通道不可用时按 `test-strategy-rules` 的阻断口径记录，不自行发明替代流程。
