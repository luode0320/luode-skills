---
name: browser-session-automation-rules
description: 面向 AI 代理的核心浏览器自动化：打开页面、抓取快照、点击/填写/选择等交互、处理认证登录、隔离 profile、具名并行 session、批量执行、截图与截图清理。当任务需要隔离 profile、具名并行 session、可脚本化 batch、常规页面交互与登录，或用户明确要求使用 agent-browser 时触发；普通用户 Chrome profile 和一般页面调试优先按浏览器路由选择 Chrome Plugin 或 Chrome DevTools MCP，不因前后端联调自动强制本 skill。若需要网络 HAR、视觉/页面 diff、性能 profiling、录制 trace、代理或多 session 观测面板，转交 `browser-advanced-testing-rules`。
allowed-tools: Bash(npx agent-browser:*), Bash(agent-browser:*)
---

# 使用 agent-browser 进行核心浏览器自动化

这个 CLI 通过 CDP 直接使用 Chrome/Chromium。可通过 `npm i -g agent-browser`、`brew install agent-browser` 或 `cargo install agent-browser` 安装。执行 `agent-browser install` 下载 Chrome，执行 `agent-browser upgrade` 更新到最新版本。

本 skill 与 `browser-advanced-testing-rules` 是同源拆分：本 skill 负责“打开页面、抓取快照、执行交互、认证登录、session 管理”这条核心自动化链路；网络 HAR、视觉/页面 diff、性能 profiling、录制 trace、代理配置和多 session 观测面板由对方负责。域名白名单、动作策略、输出上限、配置文件优先级、`--engine` 引擎选择和项目联调路由规则两组同等适用，各自维护一份。

## 核心工作流

每一次浏览器自动化都遵循下面这个模式：

1. **打开页面**：`agent-browser open <url>`
2. **抓取快照**：`agent-browser snapshot -i`（拿到元素引用，如 `@e1`、`@e2`）
3. **执行交互**：使用这些引用进行点击、填写、选择
4. **重新抓快照**：导航后或 DOM 变化后，重新获取新的引用

```bash
agent-browser open https://example.com/form
agent-browser snapshot -i
# 输出：@e1 [input type="email"], @e2 [input type="password"], @e3 [button] "Submit"

agent-browser fill @e1 "user@example.com"
agent-browser fill @e2 "password123"
agent-browser click @e3
agent-browser wait --load networkidle
agent-browser snapshot -i  # 检查结果
```

## 实战经验优先流程（新增）

以下规则来自真实浏览器自动化执行复盘，默认优先于“理想流程”：

执行前命中浏览器、session、snapshot 或 shell 高风险调用时，先触发 `execution-failure-learning-rules` 的 `prevent` 并查阅 [references/execution-failure-casebook.md](references/execution-failure-casebook.md)；执行失败后走 `recover`，修复并按同一成功标准复验后再写 candidate。

1. **先判定页面状态，再做交互**
   - `open` 后立刻执行：`get title` + `get text body`
   - 按状态分流：命中业务页继续自动化；命中登录页进入登录分支（优先复用已有 session/state）；命中 WAF/风控页进入风控兜底分支
2. **变更启动参数前必须清会话**
   - 需要切换 `--args` / `--user-agent` / profile 时，先执行 `close --all`，否则容易复用旧 daemon 参数
3. **页面跳转后必须重抓 ref**
   - click 提交、导航、弹层切换、异步刷新后，旧 `@eN` 视为失效；固定动作：`wait --load networkidle` -> `snapshot -i`
4. **高风险站点强制留证据**
   - 每个关键阶段至少保存：`url`、`title`、`snapshot`、`screenshot`；失败时必须带证据回传
5. **会话复用优先级**：`--session-name`（长期复用） > `--state`（文件恢复） > `--auto-connect`（临时兜底）
6. **重试必须有限次并可解释**：建议最多 2-3 次，每次说明触发原因、调整动作、结果
7. **测试截图只临时保留，收口前必须清理**：过程截图允许保留用于定位问题，测试完成后默认删除，只有用户明确要求保留时才集中归档

完整经验与命令模板见：
- [references/browser-operation-lessons.md](references/browser-operation-lessons.md)
- [references/tapd-workflow-automation.md](references/tapd-workflow-automation.md)

## 命令链式执行

多个命令可以在一次 shell 调用里用 `&&` 串起来。浏览器会通过后台守护进程保持会话，所以链式执行是安全的，而且通常比拆成多次调用更高效。

```bash
agent-browser open https://example.com && agent-browser wait --load networkidle && agent-browser snapshot -i
agent-browser fill @e1 "user@example.com" && agent-browser fill @e2 "password123" && agent-browser click @e3
agent-browser open https://example.com && agent-browser wait --load networkidle && agent-browser screenshot page.png
```

**什么时候适合链式执行：** 不需要读取中间命令输出再决定下一步时用 `&&`；需要先解析输出再决定后续动作时应拆开执行。

## 处理认证

当自动化网站需要登录时，按场景选择方案（可运行示例见下方"常见模式"对应小节；OAuth、2FA、cookie 认证、token 刷新细节见 [references/authentication.md](references/authentication.md)）：

- **一次性任务，导入当前浏览器登录态最快**：`agent-browser --auto-connect state save ./auth.json`，再用 `--state ./auth.json` 打开目标页。State 文件明文保存 token，需加入 `.gitignore` 且用完删除；如需加密设置 `AGENT_BROWSER_ENCRYPTION_KEY`。
- **重复性任务，用持久化 profile**：`agent-browser --profile ~/.myapp open <url>`，同一 profile 目录自动复用登录态。
- **需要自动保存 / 恢复 cookies + localStorage**：用 `--session-name`，示例见下方"Session 持久化"。
- **凭据加密保存、按名称登录**：用 `auth save` / `auth login`，示例见下方"使用 Auth Vault 进行认证"；`auth login` 会先导航并等待登录表单相关 selector 出现再填写/点击，延迟加载的 SPA 登录页更稳定。
- **手动控制 state 文件保存 / 加载时机**：示例见下方"使用 State 持久化认证"。

## 常用命令

```bash
# 导航
agent-browser open <url>              # 打开页面（别名：goto, navigate）
agent-browser close                   # 关闭浏览器
agent-browser close --all             # 关闭所有活动会话

# 快照
agent-browser snapshot -i             # 抓取可交互元素及 refs（推荐）
agent-browser snapshot -s "#selector" # 将快照范围限制到某个 CSS selector

# 交互（使用 snapshot 产生的 @refs）
agent-browser click @e1               # 点击元素
agent-browser click @e1 --new-tab     # 点击并在新标签打开
agent-browser fill @e2 "text"         # 清空后输入文本
agent-browser type @e2 "text"         # 不清空，直接输入
agent-browser select @e1 "option"     # 选择下拉项
agent-browser check @e1               # 勾选复选框
agent-browser press Enter             # 按键
agent-browser keyboard type "text"    # 在当前焦点位置输入（无 selector）
agent-browser keyboard inserttext "text"  # 不触发按键事件，直接插入文本
agent-browser scroll down 500         # 页面滚动
agent-browser scroll down 500 --selector "div.content"  # 在指定容器内滚动

# 获取信息
agent-browser get text @e1            # 获取元素文本
agent-browser get url                 # 获取当前 URL
agent-browser get title               # 获取页面标题
agent-browser get cdp-url             # 获取 CDP WebSocket URL

# 等待
agent-browser wait @e1                # 等待元素出现
agent-browser wait --load networkidle # 等待网络空闲
agent-browser wait --url "**/page"    # 等待 URL 命中模式
agent-browser wait 2000               # 固定等待毫秒数
agent-browser wait --text "Welcome"    # 等待文本出现（子串匹配）
agent-browser wait --fn "!document.body.innerText.includes('Loading...')"  # 等待文本消失
agent-browser wait "#spinner" --state hidden  # 等待元素消失

# 下载
agent-browser download @e1 ./file.pdf          # 点击元素并触发下载
agent-browser wait --download ./output.zip     # 等待任意下载完成
agent-browser --download-path ./downloads open <url>  # 设置默认下载目录

# 视口与设备模拟
agent-browser set viewport 1920 1080          # 设置视口尺寸（默认：1280x720）
agent-browser set viewport 1920 1080 2        # 2x retina（CSS 大小不变，截图更清晰）
agent-browser set device "iPhone 14"          # 模拟设备（视口 + UA）

# 捕获
agent-browser screenshot              # 截图到临时目录
agent-browser screenshot --full       # 全页截图
agent-browser screenshot --annotate   # 带编号标注的截图
agent-browser screenshot --screenshot-dir ./shots  # 保存到指定目录
agent-browser screenshot --screenshot-format jpeg --screenshot-quality 80
agent-browser pdf output.pdf          # 输出为 PDF

# 实时预览 / 流式输出（详见下方 Streaming 小节）
agent-browser stream enable --port 9223  # 启动 WebSocket 流服务，可指定端口

# 剪贴板
agent-browser clipboard read                      # 读取剪贴板文本
agent-browser clipboard write "Hello, World!"     # 写入剪贴板（还支持 copy/paste 子命令）

# 对话框（alert / confirm / prompt，完整说明见下方"JavaScript 对话框"）
agent-browser dialog accept              # 接受对话框
```

网络 HAR 记录（`network requests/route/har`）和视觉/页面 diff（`diff snapshot/screenshot/url`）属于高级验证能力，见 `browser-advanced-testing-rules`。

## Streaming

每个 session 自动启动一个 WebSocket 流服务，绑定到系统分配的端口；用 `stream status` 查看端口和连接状态，`stream disable` 关闭。跨 session 的实时观测面板（dashboard）由 `browser-advanced-testing-rules` 负责。

## Batch 批量执行

可以把多个命令以 JSON 字符串数组的形式通过管道传给 `batch`，从而在一次调用里执行。

```bash
echo '[
  ["open", "https://example.com"],
  ["snapshot", "-i"],
  ["click", "@e1"],
  ["screenshot", "result.png"]
]' | agent-browser batch --json

agent-browser batch --bail < commands.json  # 遇到第一个错误就停止
```

当命令序列已知，且不依赖中间输出时，优先用 `batch`。若需要根据中间结果决定下一步，应使用拆开的命令或 `&&` 串联。

## 常见模式

### 表单提交
```bash
agent-browser open https://example.com/signup
agent-browser snapshot -i
agent-browser fill @e1 "Jane Doe"
agent-browser fill @e2 "jane@example.com"
agent-browser select @e3 "California"
agent-browser check @e4
agent-browser click @e5
agent-browser wait --load networkidle
```

### 使用 Auth Vault 进行认证（推荐）
```bash
echo "pass" | agent-browser auth save github --url https://github.com/login --username user --password-stdin
agent-browser auth login github
agent-browser auth list
agent-browser auth show github
agent-browser auth delete github
```

### 使用 State 持久化认证
```bash
agent-browser open https://app.example.com/login
agent-browser snapshot -i
agent-browser fill @e1 "$USERNAME"
agent-browser fill @e2 "$PASSWORD"
agent-browser click @e3
agent-browser wait --url "**/dashboard"
agent-browser state save auth.json
agent-browser state load auth.json
agent-browser open https://app.example.com/dashboard
```

### Session 持久化
```bash
agent-browser --session-name myapp open https://app.example.com/login
agent-browser close  # 状态自动保存到 ~/.agent-browser/sessions/
agent-browser --session-name myapp open https://app.example.com/dashboard
export AGENT_BROWSER_ENCRYPTION_KEY=$(openssl rand -hex 32)
agent-browser state list
agent-browser state show myapp-default.json
agent-browser state clear myapp
agent-browser state clean --older-than 7
```

### 处理 Iframe
Iframe 内容会自动内联到 snapshot 结果中，iframe 里的 refs 会自带 frame 上下文，可以直接交互。
```bash
agent-browser open https://example.com/checkout
agent-browser snapshot -i
agent-browser fill @e3 "4111111111111111"
agent-browser fill @e4 "12/28"
agent-browser click @e5
agent-browser frame @e2   # 若要把快照范围限制到某个 iframe
agent-browser snapshot -i
agent-browser frame main  # 返回主 frame
```

### 数据提取
```bash
agent-browser open https://example.com/products
agent-browser snapshot -i
agent-browser get text @e5
agent-browser get text body > page.txt
agent-browser snapshot -i --json
agent-browser get text @e1 --json
```

### 并行 Session
```bash
agent-browser --session site1 open https://site-a.com
agent-browser --session site2 open https://site-b.com
agent-browser --session site1 snapshot -i
agent-browser --session site2 snapshot -i
agent-browser session list
```

### 连接到已运行的 Chrome
```bash
agent-browser --auto-connect open https://example.com
agent-browser --cdp 9222 snapshot
```
`--auto-connect` 通过 `DevToolsActivePort`、常见调试端口（9222、9229）自动发现 Chrome，HTTP 发现失败时回退到直接 WebSocket 连接。

### 配色方案（暗黑模式）
```bash
agent-browser --color-scheme dark open https://example.com
agent-browser set media dark
```

### 视口与响应式测试
按不同尺寸依次 `set viewport <w> <h>` 或 `set device "<name>"` 后截图对比：桌面 `1920 1080`、移动 `375 812`、`2` 倍视网膜（devicePixelRatio 不改 CSS 布局）、具名设备如 `"iPhone 14"`。

### 可视化浏览器（调试）
```bash
agent-browser --headed open https://example.com
agent-browser highlight @e1          # 高亮元素
agent-browser inspect                # 打开当前页面的 Chrome DevTools
```
可通过环境变量 `AGENT_BROWSER_HEADED=1` 启用 headed 模式。录制视频（`record start`）和性能 profiling（`profiler start/stop`）属于高级验证能力，见 `browser-advanced-testing-rules`。

### 本地文件（PDF、HTML）
```bash
agent-browser --allow-file-access open file:///path/to/document.pdf
agent-browser --allow-file-access open file:///path/to/page.html
agent-browser screenshot output.png
```

### iOS 模拟器（Mobile Safari）
在常规命令前加 `-p ios --device "iPhone 16 Pro"`（或已连接真机的 `--device "<UDID>"`，UDID 来自 `xcrun xctrace list devices`），其余 `open`/`snapshot`/`tap`/`fill`/`swipe`/`screenshot`/`close` 用法与常规命令一致。**要求：** macOS + Xcode + Appium（`npm install -g appium && appium driver install xcuitest`）。

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

## 超时与慢页面
默认超时时间是 25 秒，可通过环境变量 `AGENT_BROWSER_DEFAULT_TIMEOUT`（毫秒）覆盖。对慢网站或大页面，应优先使用上方"等待"小节里的显式等待（`--load networkidle`、`--url`、`--fn` 等），固定毫秒等待仅作万不得已的兜底。

## JavaScript 对话框（alert / confirm / prompt）
当页面弹出对话框时，其它浏览器命令都会被阻塞，直到对话框被处理：
```bash
agent-browser dialog status
agent-browser dialog accept
agent-browser dialog accept "my input"
agent-browser dialog dismiss
```
当对话框仍处于打开状态时，所有命令响应中都会带一个 `warning` 字段。

## Session 管理与清理
命名 session 的用法见上方"并行 Session"；单独关闭用 `agent-browser --session <name> close`，遗留守护进程或收尾清理统一用 `agent-browser close --all` 一次关闭全部。

## 测试截图清理（强制）
- 允许过程截图：用于中间定位、异常证据、阶段性汇报。
- 强制收口清理：测试完成后删除临时截图。
- 保留例外：只有用户明确要求“保留截图作为交付物”时才允许保留，并集中放到约定目录。

```bash
Remove-Item -LiteralPath .\screenshots\* -Force -ErrorAction SilentlyContinue
Remove-Item -LiteralPath /tmp/ab-test-*.png -Force -ErrorAction SilentlyContinue
```
若截图属于失败用例证据且用户要求保留，需在最终总结中说明“保留原因 + 保存位置”。若想在空闲一段时间后自动关闭守护进程：`AGENT_BROWSER_IDLE_TIMEOUT_MS=60000 agent-browser open example.com`。

## Ref 生命周期（重要）
当页面发生变化后，refs（`@e1`、`@e2` 等）会失效，以下场景后必须重新抓取快照：点击会触发导航的链接或按钮、提交表单、动态内容加载（下拉框、弹窗等）。
```bash
agent-browser click @e5              # 导航到新页面
agent-browser snapshot -i            # 必须重新抓快照
agent-browser click @e1              # 使用新的 refs
```

## 带标注的截图（Vision 模式）
使用 `--annotate` 可输出一张带编号标记的截图，编号映射到交互元素 refs，同时缓存 refs，可直接交互。
```bash
agent-browser screenshot --annotate
agent-browser click @e2
```
适合：无文字图标按钮、需要同时验证视觉布局和样式、canvas/图表元素、需要基于空间位置判断。

## 语义定位器（Refs 的替代方案）
```bash
agent-browser find text "Sign In" click
agent-browser find label "Email" fill "user@test.com"
agent-browser find role button click --name "Submit"
agent-browser find placeholder "Search" type "query"
agent-browser find testid "submit-btn" click
```

## JavaScript 求值（eval）
使用 `eval` 可以在浏览器上下文中执行 JavaScript。**复杂表达式很容易被 shell 转义破坏**，应优先使用 `--stdin` 或 `-b`。
```bash
agent-browser eval 'document.title'
agent-browser eval --stdin <<'EVALEOF'
JSON.stringify(Array.from(document.querySelectorAll("img")).map(i => i.src))
EVALEOF
agent-browser eval -b "$(echo -n 'Array.from(document.querySelectorAll("a")).map(a => a.href)' | base64)"
```
**经验规则：** 单行无嵌套引号用 `eval 'expression'`；有嵌套引号/箭头函数/模板字符串/多行代码用 `eval --stdin <<'EVALEOF'`；程序自动生成脚本用 `eval -b`。

## 配置文件
可以在项目根目录创建 `agent-browser.json` 保存持久配置。优先级从低到高：`~/.agent-browser/config.json` < `./agent-browser.json` < 环境变量 < CLI flags。可通过 `--config <path>` 或环境变量 `AGENT_BROWSER_CONFIG` 指定自定义配置文件。所有 CLI 选项都映射为 camelCase key。用户级配置和项目级配置里的 extensions 会合并，而不是互相覆盖。

## 深入文档

| Reference | 适用场景 |
| --- | --- |
| [references/commands.md](references/commands.md) | 完整命令参考及全部选项（含网络/HAR/diff，供高级验证组交叉引用） |
| [references/browser-operation-lessons.md](references/browser-operation-lessons.md) | 浏览器自动化实战经验、失败分流与稳定执行清单 |
| [references/snapshot-refs.md](references/snapshot-refs.md) | Ref 生命周期、失效规则与排障 |
| [references/session-management.md](references/session-management.md) | 并行 session、状态持久化、并发抓取 |
| [references/screenshot-cleanup.md](references/screenshot-cleanup.md) | 测试截图生命周期、清理时机与保留例外 |
| [references/authentication.md](references/authentication.md) | 登录流程、OAuth、2FA、状态复用 |
| [references/tapd-workflow-automation.md](references/tapd-workflow-automation.md) | TAPD 场景自动化流程、暂停点复盘与无交互收敛 |
| [references/execution-failure-casebook.md](references/execution-failure-casebook.md) | 浏览器/session/snapshot 执行失败案例与恢复标准 |

## 浏览器引擎选择
通过 `--engine` 指定本地浏览器引擎，默认是 `chrome`。
```bash
agent-browser --engine lightpanda open example.com
export AGENT_BROWSER_ENGINE=lightpanda
agent-browser --engine lightpanda --executable-path /path/to/lightpanda open example.com
```
支持 `chrome`（默认）和 `lightpanda`（无头浏览器，内存更小速度更快，不支持 `--extension`/`--profile`/`--state`/`--allow-file-access`）。

## 可直接使用的模板

| Template | 说明 |
| --- | --- |
| [templates/form-automation.sh](templates/form-automation.sh) | 带校验的表单填写流程 |
| [templates/authenticated-session.sh](templates/authenticated-session.sh) | 登录一次，后续复用状态 |
| [templates/capture-workflow.sh](templates/capture-workflow.sh) | 带截图的内容抓取流程 |
| [templates/tapd-weekly-report.sh](templates/tapd-weekly-report.sh) | TAPD 我的工作周维度进度统计（含 WAF/登录兜底） |

```bash
./templates/form-automation.sh https://example.com/form
./templates/authenticated-session.sh https://app.example.com/login
./templates/capture-workflow.sh https://example.com ./output
./templates/tapd-weekly-report.sh 2026-04-03 ./output
```

## 项目联调规则

### 触发规则补充（强制）
- 当项目同时存在前端与后端且任务进入“测试/验证/联调”阶段时，必须完成真实 local 浏览器联调；具体工具按 `mcp-installation-rules` 的统一路由选择。
- 用户已有 Chrome 标签页、登录态、Cookie 或扩展时使用 Chrome Plugin；常规 DOM/控制台调试且 Chrome DevTools MCP 已接通时使用 Chrome DevTools MCP；只有隔离 profile、并发 session、批量执行或其他核心自动化场景才使用本 skill；HAR/route、视觉 diff、录制/trace、代理或其他引擎场景见 `browser-advanced-testing-rules`。
- 所选浏览器通道不可用且没有满足安全边界的替代通道时，记录本地联调阻断，不强行切换工具。
- 若系统需要登录授权而当前上下文缺失有效授权信息，必须先向用户获取登录账户或 token，再继续联调。
- 若准备开始前后端联调，允许主动关闭用户已启动的前端与后端进程，并按当前任务重新启动前后端服务后再调试。
- 项目联调场景下，浏览器打开的前端 URL、后端 API、代理、鉴权回调和依赖服务必须来自 local 本地环境；不得把 `test` / `prod` / `staging` 域名或远端服务当作联调目标。

### 执行要求补充（强制）
1. 联调前先确认服务可访问（前端页面可打开、后端接口可达）。
2. 使用路由选定的浏览器工具完成至少一次真实用户路径的页面交互验证。
3. 联调开场应先执行进程基线收口：关闭当前已运行的前端与后端进程，再按本轮调试目标重新启动前后端服务。
4. 需要授权的场景必须先完成授权注入或登录流程；若遇到注册受限无法自行获取可用会话，必须暂停并向用户索取可用账户、token 或其他可登录方式。
5. 最终结论必须基于联调证据，不能仅基于代码推断给出“已验证通过”。
6. 测试完成、前后端浏览器联调完成后，必须关闭本轮为联调启动的前端与后端进程，禁止遗留后台运行进程。
7. 进程收口必须可核验：至少记录一次“关闭动作 + 关闭后状态检查”结论。
8. 若 local 前端、后端、API 代理或鉴权依赖无法启动，必须记录为本地联调阻断；不得改用 test / prod / staging 页面、接口或账号继续验证。