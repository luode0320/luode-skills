---
name: agent-browser
description: 面向 AI 代理的浏览器自动化 CLI。当用户需要与网站交互时使用，包括打开页面、填写表单、点击按钮、截图、提取数据、测试 Web 应用，或执行任何浏览器自动化任务。典型触发语句包括“打开一个网站”“填写表单”“点击按钮”“截个图”“抓取页面数据”“测试这个 Web 应用”“登录某个网站”“自动化浏览器操作”，以及任何需要通过程序控制浏览器完成的任务。
allowed-tools: Bash(npx agent-browser:*), Bash(agent-browser:*)
---

# 使用 agent-browser 进行浏览器自动化

这个 CLI 通过 CDP 直接使用 Chrome/Chromium。可通过 `npm i -g agent-browser`、`brew install agent-browser` 或 `cargo install agent-browser` 安装。执行 `agent-browser install` 下载 Chrome，执行 `agent-browser upgrade` 更新到最新版本。

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

1. **先判定页面状态，再做交互**
   - `open` 后立刻执行：`get title` + `get text body`
   - 按状态分流：
     - 命中业务页：继续自动化
     - 命中登录页：进入登录分支（优先复用已有 session/state）
     - 命中 WAF/风控页：进入风控兜底分支

2. **变更启动参数前必须清会话**
   - 需要切换 `--args` / `--user-agent` / profile 时，先执行 `close --all`
   - 否则容易复用旧 daemon 参数，导致“参数看起来生效但实际未生效”

3. **页面跳转后必须重抓 ref**
   - click 提交、导航、弹层切换、异步刷新后，旧 `@eN` 视为失效
   - 固定动作：`wait --load networkidle` -> `snapshot -i`

4. **高风险站点强制留证据**
   - 每个关键阶段至少保存：`url`、`title`、`snapshot`、`screenshot`
   - 失败时必须带证据回传，不要只返回“执行失败”

5. **会话复用优先级**
   - `--session-name`（长期复用） > `--state`（文件恢复） > `--auto-connect`（临时兜底）

6. **重试必须有限次并可解释**
   - 建议最多 2-3 次重试
   - 每次重试都要说明：触发原因、调整动作、结果

7. **测试截图只临时保留，收口前必须清理**
   - 过程截图允许保留用于定位问题与中间汇报
   - 测试完成后默认删除临时截图，避免在仓库与测试目录遗留垃圾截图
   - 只有用户明确要求“保留截图作为交付物”时才允许保留，并应集中放到约定目录

完整经验与命令模板见：
- [references/browser-operation-lessons.md](references/browser-operation-lessons.md)
- [references/tapd-workflow-automation.md](references/tapd-workflow-automation.md)

## 命令链式执行

多个命令可以在一次 shell 调用里用 `&&` 串起来。浏览器会通过后台守护进程保持会话，所以链式执行是安全的，而且通常比拆成多次调用更高效。

```bash
# 一次调用里完成 open + wait + snapshot
agent-browser open https://example.com && agent-browser wait --load networkidle && agent-browser snapshot -i

# 串联多个交互步骤
agent-browser fill @e1 "user@example.com" && agent-browser fill @e2 "password123" && agent-browser click @e3

# 打开页面并截图
agent-browser open https://example.com && agent-browser wait --load networkidle && agent-browser screenshot page.png
```

**什么时候适合链式执行：** 当你不需要读取中间命令输出再决定下一步时，用 `&&` 最合适，例如 open + wait + screenshot。若需要先解析输出，再决定后续动作，就应拆开执行，例如先 snapshot 拿到 refs，再根据 refs 交互。

## 处理认证

当自动化的网站需要登录时，根据场景选择合适方案：

**方案 1：导入用户当前浏览器的登录态（一次性任务最快）**

```bash
# 连接用户当前正在运行的 Chrome（用户已经登录）
agent-browser --auto-connect state save ./auth.json
# 使用保存的登录态
agent-browser --state ./auth.json open https://app.example.com/dashboard
```

State 文件里会明文保存会话 token，请加入 `.gitignore`，并在不再需要时删除。如需静态加密，可设置 `AGENT_BROWSER_ENCRYPTION_KEY`。

**方案 2：持久化 profile（适合重复性任务）**

```bash
# 首次运行：手动登录或自动化登录
agent-browser --profile ~/.myapp open https://app.example.com/login
# ... 填账号密码并提交 ...

# 后续运行：默认已登录
agent-browser --profile ~/.myapp open https://app.example.com/dashboard
```

**方案 3：使用 session name（自动保存 / 恢复 cookies + localStorage）**

```bash
agent-browser --session-name myapp open https://app.example.com/login
# ... 登录流程 ...
agent-browser close  # 状态会自动保存

# 下次执行时自动恢复
agent-browser --session-name myapp open https://app.example.com/dashboard
```

**方案 4：使用认证金库（凭据加密保存，通过名称登录）**

```bash
echo "$PASSWORD" | agent-browser auth save myapp --url https://app.example.com/login --username user --password-stdin
agent-browser auth login myapp
```

`auth login` 会先执行导航并等待登录表单相关 selector 出现后再填写 / 点击，因此在延迟加载的 SPA 登录页中更稳定。

**方案 5：手动保存 / 加载 state 文件**

```bash
# 登录后保存：
agent-browser state save ./auth.json
# 未来会话中恢复：
agent-browser state load ./auth.json
agent-browser open https://app.example.com/dashboard
```

关于 OAuth、2FA、cookie 认证和 token 刷新模式，请看 [references/authentication.md](references/authentication.md)。

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

# 网络
agent-browser network requests                 # 查看已跟踪请求
agent-browser network requests --type xhr,fetch  # 按资源类型过滤
agent-browser network requests --method POST   # 按 HTTP 方法过滤
agent-browser network requests --status 2xx    # 按状态码过滤（200, 2xx, 400-499）
agent-browser network request <requestId>      # 查看完整请求 / 响应详情
agent-browser network route "**/api/*" --abort  # 拦截并中止匹配请求
agent-browser network har start                # 开始 HAR 录制
agent-browser network har stop ./capture.har   # 停止并保存 HAR 文件

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

# 实时预览 / 流式输出
agent-browser stream enable           # 启动运行时 WebSocket 流服务，自动选端口
agent-browser stream enable --port 9223  # 指定端口
agent-browser stream status           # 查看当前状态、端口、连接和 screencast
agent-browser stream disable          # 停止流服务并移除 .stream 元数据文件

# 剪贴板
agent-browser clipboard read                      # 读取剪贴板文本
agent-browser clipboard write "Hello, World!"     # 写入剪贴板
agent-browser clipboard copy                      # 复制当前选中内容
agent-browser clipboard paste                     # 粘贴剪贴板内容

# 对话框（alert / confirm / prompt）
agent-browser dialog accept              # 接受对话框
agent-browser dialog accept "my input"   # 接受 prompt 并输入文本
agent-browser dialog dismiss             # 取消 / 关闭对话框
agent-browser dialog status              # 查看当前是否有对话框弹出

# Diff（比较页面状态）
agent-browser diff snapshot                          # 比较当前快照与上一次快照
agent-browser diff snapshot --baseline before.txt    # 与保存的文本基线比较
agent-browser diff screenshot --baseline before.png  # 做像素级视觉 diff
agent-browser diff url <url1> <url2>                 # 对比两个页面
agent-browser diff url <url1> <url2> --wait-until networkidle  # 自定义等待策略
agent-browser diff url <url1> <url2> --selector "#main"  # 仅比较某个元素范围
```

## Streaming

每个 session 都会自动启动一个 WebSocket 流服务，并绑定到系统分配的端口。用 `agent-browser stream status` 查看当前端口和连接状态。用 `stream disable` 关闭流服务；如需重新启用，可执行 `stream enable --port <port>`。

## Batch 批量执行

可以把多个命令以 JSON 字符串数组的形式通过管道传给 `batch`，从而在一次调用里执行。这能避免多次启动进程的额外开销，适合已知的多步流程。

```bash
echo '[
  ["open", "https://example.com"],
  ["snapshot", "-i"],
  ["click", "@e1"],
  ["screenshot", "result.png"]
]' | agent-browser batch --json

# 遇到第一个错误就停止
agent-browser batch --bail < commands.json
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
# 只保存一次凭据（通过 AGENT_BROWSER_ENCRYPTION_KEY 静态加密）
# 推荐通过 stdin 传密码，避免进入 shell 历史
echo "pass" | agent-browser auth save github --url https://github.com/login --username user --password-stdin

# 使用已保存配置登录（LLM 不会看到密码）
agent-browser auth login github

# 查看 / 列出 / 删除配置
agent-browser auth list
agent-browser auth show github
agent-browser auth delete github
```

`auth login` 会等待用户名 / 密码 / 提交按钮的 selector 出现后再执行交互，超时时间受默认 action timeout 控制。

### 使用 State 持久化认证

```bash
# 先登录一次并保存状态
agent-browser open https://app.example.com/login
agent-browser snapshot -i
agent-browser fill @e1 "$USERNAME"
agent-browser fill @e2 "$PASSWORD"
agent-browser click @e3
agent-browser wait --url "**/dashboard"
agent-browser state save auth.json

# 后续会话中复用
agent-browser state load auth.json
agent-browser open https://app.example.com/dashboard
```

### Session 持久化

```bash
# 浏览器重启后自动保存 / 恢复 cookies 和 localStorage
agent-browser --session-name myapp open https://app.example.com/login
# ... 登录流程 ...
agent-browser close  # 状态自动保存到 ~/.agent-browser/sessions/

# 下次会自动加载
agent-browser --session-name myapp open https://app.example.com/dashboard

# 对静态保存的数据加密
export AGENT_BROWSER_ENCRYPTION_KEY=$(openssl rand -hex 32)
agent-browser --session-name secure open https://app.example.com

# 管理已保存状态
agent-browser state list
agent-browser state show myapp-default.json
agent-browser state clear myapp
agent-browser state clean --older-than 7
```

### 处理 Iframe

Iframe 内容会自动内联到 snapshot 结果中。iframe 里的 refs 会自带 frame 上下文，因此可以直接交互。

```bash
agent-browser open https://example.com/checkout
agent-browser snapshot -i
# @e1 [heading] "Checkout"
# @e2 [Iframe] "payment-frame"
#   @e3 [input] "Card number"
#   @e4 [input] "Expiry"
#   @e5 [button] "Pay"

# 直接交互，不需要切 frame
agent-browser fill @e3 "4111111111111111"
agent-browser fill @e4 "12/28"
agent-browser click @e5

# 如果想把快照范围限制到某个 iframe：
agent-browser frame @e2
agent-browser snapshot -i         # 只看 iframe 内容
agent-browser frame main          # 返回主 frame
```

### 数据提取

```bash
agent-browser open https://example.com/products
agent-browser snapshot -i
agent-browser get text @e5           # 获取指定元素文本
agent-browser get text body > page.txt  # 获取整页文本

# JSON 输出，便于解析
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
# 自动发现开启了 remote debugging 的 Chrome
agent-browser --auto-connect open https://example.com
agent-browser --auto-connect snapshot

# 或显式指定 CDP 端口
agent-browser --cdp 9222 snapshot
```

Auto-connect 会通过 `DevToolsActivePort`、常见调试端口（9222、9229）自动发现 Chrome；若 HTTP 方式的 CDP 发现失败，则回退到直接 WebSocket 连接。

### 配色方案（暗黑模式）

```bash
# 用 flag 持久启用暗黑模式（影响当前页和后续新标签）
agent-browser --color-scheme dark open https://example.com

# 或通过环境变量
AGENT_BROWSER_COLOR_SCHEME=dark agent-browser open https://example.com

# 或在当前 session 中设置（对后续命令持续生效）
agent-browser set media dark
```

### 视口与响应式测试

```bash
# 设置自定义视口（默认 1280x720）
agent-browser set viewport 1920 1080
agent-browser screenshot desktop.png

# 测移动端宽度布局
agent-browser set viewport 375 812
agent-browser screenshot mobile.png

# Retina / HiDPI：CSS 布局不变，但按 2x 像素密度渲染
# 截图逻辑尺寸不变，但内容渲染更清晰
agent-browser set viewport 1920 1080 2
agent-browser screenshot retina.png

# 设备模拟（一次设置视口 + UA）
agent-browser set device "iPhone 14"
agent-browser screenshot device.png
```

第三个参数 `scale` 用于设置 `window.devicePixelRatio`，不会改变 CSS 布局尺寸。适合测试 retina 渲染或输出更高清的截图。

### 可视化浏览器（调试）

```bash
agent-browser --headed open https://example.com
agent-browser highlight @e1          # 高亮元素
agent-browser inspect                # 打开当前页面的 Chrome DevTools
agent-browser record start demo.webm # 录制会话
agent-browser profiler start         # 启动 Chrome DevTools profiling
agent-browser profiler stop trace.json # 停止并保存 profile（路径可选）
```

可通过环境变量 `AGENT_BROWSER_HEADED=1` 启用 headed 模式。浏览器扩展在 headed 和 headless 模式下都可使用。

### 本地文件（PDF、HTML）

```bash
# 用 file:// 打开本地文件
agent-browser --allow-file-access open file:///path/to/document.pdf
agent-browser --allow-file-access open file:///path/to/page.html
agent-browser screenshot output.png
```

### iOS 模拟器（Mobile Safari）

```bash
# 列出可用 iOS 模拟器
agent-browser device list

# 在指定设备上启动 Safari
agent-browser -p ios --device "iPhone 16 Pro" open https://example.com

# 工作流与桌面一致：snapshot、交互、再 snapshot
agent-browser -p ios snapshot -i
agent-browser -p ios tap @e1          # tap（click 的别名）
agent-browser -p ios fill @e2 "text"
agent-browser -p ios swipe up         # iOS 专用手势

# 截图
agent-browser -p ios screenshot mobile.png

# 关闭会话（同时关闭模拟器）
agent-browser -p ios close
```

**要求：** macOS + Xcode + Appium（`npm install -g appium && appium driver install xcuitest`）

**真机：** 如果设备已预配置，也支持物理 iOS 设备。使用 `--device "<UDID>"`，其中 UDID 来自 `xcrun xctrace list devices`。

## 安全

所有安全特性都是可选开启的。默认情况下，agent-browser 不会限制导航、动作或输出。

### Content Boundaries（推荐给 AI 代理）

启用 `--content-boundaries` 后，页面来源的输出会被边界标记包裹，帮助 LLM 区分工具输出与不可信页面内容：

```bash
export AGENT_BROWSER_CONTENT_BOUNDARIES=1
agent-browser snapshot
# 输出：
# --- AGENT_BROWSER_PAGE_CONTENT nonce=<hex> origin=https://example.com ---
# [accessibility tree]
# --- END_AGENT_BROWSER_PAGE_CONTENT nonce=<hex> ---
```

### 域名白名单

将导航限制在可信域名内。通配符如 `*.example.com` 也会匹配裸域名 `example.com`。对非允许域名发起的子资源请求、WebSocket 和 EventSource 连接也会被阻止。记得把页面依赖的 CDN 域名一并加入：

```bash
export AGENT_BROWSER_ALLOWED_DOMAINS="example.com,*.example.com"
agent-browser open https://example.com        # 允许
agent-browser open https://malicious.com       # 阻止
```

### 动作策略

使用策略文件限制破坏性动作：

```bash
export AGENT_BROWSER_ACTION_POLICY=./policy.json
```

示例 `policy.json`：

```json
{ "default": "deny", "allow": ["navigate", "snapshot", "click", "scroll", "wait", "get"] }
```

认证金库相关操作（如 `auth login`）不会受 action policy 限制，但仍受域名白名单限制。

### 输出上限

防止超大页面把上下文灌满：

```bash
export AGENT_BROWSER_MAX_OUTPUT=50000
```

## Diff（验证变化）

执行动作后可以用 `diff snapshot` 验证页面是否按预期发生变化。它会比较当前 accessibility tree 与当前 session 中上一次快照之间的差异。

```bash
# 典型流程：snapshot -> action -> diff
agent-browser snapshot -i          # 先拍一份基线快照
agent-browser click @e2            # 执行动作
agent-browser diff snapshot        # 看差异（自动与上一份快照比较）
```

用于视觉回归测试或监控时：

```bash
# 先保存一张基线截图，再在后续比较
agent-browser screenshot baseline.png
# ... 一段时间后或发生变更后 ...
agent-browser diff screenshot --baseline baseline.png

# 比较 staging 与 production
agent-browser diff url https://staging.example.com https://prod.example.com --screenshot
```

`diff snapshot` 用 `+` 表示新增、`-` 表示删除，格式类似 git diff。`diff screenshot` 会输出一张差异图，把变化的像素高亮成红色，并给出不匹配百分比。

## 超时与慢页面

默认超时时间是 25 秒，可通过环境变量 `AGENT_BROWSER_DEFAULT_TIMEOUT`（毫秒）覆盖。对慢网站或大页面，应优先使用显式等待，而不是完全依赖默认超时：

```bash
# 等待网络活动稳定（最适合慢页面）
agent-browser wait --load networkidle

# 等待指定元素出现
agent-browser wait "#content"
agent-browser wait @e1

# 等待特定 URL 模式（适合跳转后）
agent-browser wait --url "**/dashboard"

# 等待某个 JS 条件成立
agent-browser wait --fn "document.readyState === 'complete'"

# 万不得已时再固定等待（毫秒）
agent-browser wait 5000
```

对持续较慢的网站，建议在 `open` 后加 `wait --load networkidle`，确保页面真正加载完成后再做 snapshot。若是某个具体元素慢，可以直接等待该元素：`wait <selector>` 或 `wait @ref`。

## JavaScript 对话框（alert / confirm / prompt）

当页面弹出 JavaScript 对话框（`alert()`、`confirm()`、`prompt()`）时，所有其它浏览器命令（snapshot、screenshot、click 等）都会被阻塞，直到对话框被处理。如果命令无故超时，优先检查是否有未关闭的对话框：

```bash
# 查看是否有对话框阻塞
agent-browser dialog status

# 接受对话框（关闭 alert / 点击 OK）
agent-browser dialog accept

# 接受 prompt 并输入内容
agent-browser dialog accept "my input"

# 取消 / 关闭对话框
agent-browser dialog dismiss
```

当对话框仍然处于打开状态时，所有命令响应中都会带一个 `warning` 字段，说明对话框类型和内容。在 `--json` 模式下，该字段会以 `"warning"` 键出现。

## Session 管理与清理

当多个代理或多个自动化流程并行运行时，一定要使用具名 session，避免互相干扰：

```bash
# 每个代理使用独立 session
agent-browser --session agent1 open site-a.com
agent-browser --session agent2 open site-b.com

# 查看当前活动 session
agent-browser session list
```

完成后务必关闭浏览器 session，避免后台进程泄漏：

```bash
agent-browser close                    # 关闭默认 session
agent-browser --session agent1 close   # 关闭指定 session
agent-browser close --all              # 关闭所有活动 session
```

如果之前某个 session 没有正确关闭，守护进程可能还在。可执行 `agent-browser close` 清理，或用 `agent-browser close --all` 一次关闭全部。

## 测试截图清理（强制）

截图可以在执行过程中用于排障与汇报，但默认视为临时产物。
当测试完成并进入收口阶段时，必须执行截图清理，避免遗留垃圾文件。

默认规则：

- 允许过程截图：用于中间定位、异常证据、阶段性汇报。
- 强制收口清理：测试完成后删除临时截图。
- 保留例外：只有用户明确要求保留截图时，才保留并集中归档。

推荐做法：

```bash
# 示例：清理项目内临时截图目录
Remove-Item -LiteralPath .\\screenshots\\* -Force -ErrorAction SilentlyContinue

# 示例：清理 /tmp 下本次测试截图（按前缀）
Remove-Item -LiteralPath /tmp/ab-test-*.png -Force -ErrorAction SilentlyContinue
```

补充：若截图属于失败用例证据且用户要求保留，需在最终总结中说明“保留原因 + 保存位置”。

若想在空闲一段时间后自动关闭守护进程（适合 CI 或一次性环境）：

```bash
AGENT_BROWSER_IDLE_TIMEOUT_MS=60000 agent-browser open example.com
```

## Ref 生命周期（重要）

当页面发生变化后，refs（`@e1`、`@e2` 等）会失效。以下场景后必须重新抓取快照：

- 点击会触发导航的链接或按钮
- 提交表单
- 动态内容加载（下拉框、弹窗等）

```bash
agent-browser click @e5              # 导航到新页面
agent-browser snapshot -i            # 必须重新抓快照
agent-browser click @e1              # 使用新的 refs
```

## 带标注的截图（Vision 模式）

使用 `--annotate` 可输出一张带编号标记的截图，编号会映射到交互元素 refs。每个标号 `[N]` 对应 ref `@eN`。同时，这个过程也会缓存 refs，因此可以不额外 snapshot 就直接交互。

```bash
agent-browser screenshot --annotate
# 输出中会给出图片路径和图例：
#   [1] @e1 button "Submit"
#   [2] @e2 link "Home"
#   [3] @e3 textbox "Email"
agent-browser click @e2              # 直接使用标注截图里的 ref
```

以下场景尤其适合使用带标注截图：

- 页面里有无文字的图标按钮或纯视觉元素
- 需要同时验证视觉布局和样式
- 页面含有 canvas 或图表元素（文本快照看不到）
- 需要基于空间位置做判断

## 语义定位器（Refs 的替代方案）

当 refs 不可用或不稳定时，可改用语义定位器：

```bash
agent-browser find text "Sign In" click
agent-browser find label "Email" fill "user@test.com"
agent-browser find role button click --name "Submit"
agent-browser find placeholder "Search" type "query"
agent-browser find testid "submit-btn" click
```

## JavaScript 求值（eval）

使用 `eval` 可以在浏览器上下文中执行 JavaScript。**复杂表达式很容易被 shell 转义破坏**，因此复杂场景应优先使用 `--stdin` 或 `-b`。

```bash
# 简单表达式可直接写
agent-browser eval 'document.title'
agent-browser eval 'document.querySelectorAll("img").length'

# 复杂 JS：推荐使用 --stdin + heredoc
agent-browser eval --stdin <<'EVALEOF'
JSON.stringify(
  Array.from(document.querySelectorAll("img"))
    .filter(i => !i.alt)
    .map(i => ({ src: i.src.split("/").pop(), width: i.width }))
)
EVALEOF

# 另一种方式：base64 编码，彻底绕开 shell 转义
agent-browser eval -b "$(echo -n 'Array.from(document.querySelectorAll("a")).map(a => a.href)' | base64)"
```

**为什么很重要：** shell 在处理命令时，内部双引号、`!`（history expansion）、反引号、`$()` 都可能在 JS 到达 agent-browser 前就把内容改坏。`--stdin` 和 `-b` 可以绕开这些问题。

**经验规则：**

- 单行、无嵌套引号：普通 `eval 'expression'` 基本足够
- 有嵌套引号、箭头函数、模板字符串或多行代码：用 `eval --stdin <<'EVALEOF'`
- 程序自动生成脚本：用 `eval -b`

## 配置文件

可以在项目根目录创建 `agent-browser.json` 保存持久配置：

```json
{
  "headed": true,
  "proxy": "http://localhost:8080",
  "profile": "./browser-data"
}
```

优先级从低到高依次为：`~/.agent-browser/config.json` < `./agent-browser.json` < 环境变量 < CLI flags。可通过 `--config <path>` 或环境变量 `AGENT_BROWSER_CONFIG` 指定自定义配置文件（如果文件不存在或无效，会直接报错退出）。所有 CLI 选项都映射为 camelCase key（例如 `--executable-path` 对应 `"executablePath"`）。布尔 flag 支持显式写 `true` / `false`（例如 `--headed false` 可覆盖配置）。用户级配置和项目级配置里的 extensions 会合并，而不是互相覆盖。

## 深入文档

| Reference                                                            | 适用场景 |
| -------------------------------------------------------------------- | --------------------------------------------------------- |
| [references/commands.md](references/commands.md)                     | 完整命令参考及全部选项 |
| [references/browser-operation-lessons.md](references/browser-operation-lessons.md) | 浏览器自动化实战经验、失败分流与稳定执行清单 |
| [references/snapshot-refs.md](references/snapshot-refs.md)           | Ref 生命周期、失效规则与排障 |
| [references/session-management.md](references/session-management.md) | 并行 session、状态持久化、并发抓取 |
| [references/screenshot-cleanup.md](references/screenshot-cleanup.md) | 测试截图生命周期、清理时机与保留例外 |
| [references/authentication.md](references/authentication.md)         | 登录流程、OAuth、2FA、状态复用 |
| [references/tapd-workflow-automation.md](references/tapd-workflow-automation.md) | TAPD 场景自动化流程、暂停点复盘与无交互收敛 |
| [references/video-recording.md](references/video-recording.md)       | 调试和留档时的视频录制 |
| [references/profiling.md](references/profiling.md)                   | Chrome DevTools profiling 与性能分析 |
| [references/proxy-support.md](references/proxy-support.md)           | 代理配置、地域测试、代理轮换 |

## 浏览器引擎选择

通过 `--engine` 指定本地浏览器引擎，默认是 `chrome`。

```bash
# 使用 Lightpanda（高性能无头浏览器，需要单独安装）
agent-browser --engine lightpanda open example.com

# 通过环境变量指定
export AGENT_BROWSER_ENGINE=lightpanda
agent-browser open example.com

# 指定自定义二进制路径
agent-browser --engine lightpanda --executable-path /path/to/lightpanda open example.com
```

支持的引擎：
- `chrome`（默认）-- 通过 CDP 驱动 Chrome/Chromium
- `lightpanda` -- 通过 CDP 驱动 Lightpanda 无头浏览器（内存更小、速度更快）

Lightpanda 不支持 `--extension`、`--profile`、`--state` 或 `--allow-file-access`。安装方式见 https://lightpanda.io/docs/open-source/installation 。

## 观测面板（Observability Dashboard）

这个 dashboard 是独立的后台服务，用于展示所有 session 的实时浏览器视口、命令活动和 console 输出。

```bash
# 只需安装一次 dashboard
agent-browser dashboard install

# 启动 dashboard 服务（后台运行，默认端口 4848）
agent-browser dashboard start

# 所有 session 都会自动显示在 dashboard 中
agent-browser open example.com

# 停止 dashboard
agent-browser dashboard stop
```

Dashboard 与浏览器 session 相互独立，默认运行在 4848 端口（可通过 `--port` 调整）。所有 session 都会自动向 dashboard 推流。

## 可直接使用的模板

| Template                                                                 | 说明 |
| ------------------------------------------------------------------------ | ----------------------------------- |
| [templates/form-automation.sh](templates/form-automation.sh)             | 带校验的表单填写流程 |
| [templates/authenticated-session.sh](templates/authenticated-session.sh) | 登录一次，后续复用状态 |
| [templates/capture-workflow.sh](templates/capture-workflow.sh)           | 带截图的内容抓取流程 |
| [templates/tapd-weekly-report.sh](templates/tapd-weekly-report.sh)       | TAPD 我的工作周维度进度统计（含 WAF/登录兜底） |

```bash
./templates/form-automation.sh https://example.com/form
./templates/authenticated-session.sh https://app.example.com/login
./templates/capture-workflow.sh https://example.com ./output
./templates/tapd-weekly-report.sh 2026-04-03 ./output
```
## 项目联调强制规则（新增）

### 触发规则补充（强制）

- 当项目同时存在前端与后端（例如同仓库含 `frontend` 与 `backend`、`web` 与 `api`、或等价目录）且任务进入“测试/验证/联调”阶段时，必须触发并使用 `agent-browser` 做浏览器联调测试。
- 该规则优先级高于“仅命令行验证”或“仅静态代码判断”；除非用户明确禁止浏览器联调，否则不得跳过。
- 若系统需要登录授权（会话、账号密码、验证码、token、cookie、state）而当前上下文缺失有效授权信息，必须先向用户获取登录账户或 token，再继续联调。
- 若准备开始前后端联调，允许主动关闭用户已启动的前端与后端进程，并按当前任务重新启动前后端服务后再调试。

### 执行要求补充（强制）

1. 联调前先确认服务可访问（前端页面可打开、后端接口可达）。
2. 使用 `agent-browser` 完成至少一次真实用户路径的页面交互验证（打开页面、关键操作、结果确认）。
3. 联调开场应先执行进程基线收口：关闭当前已运行的前端与后端进程，再按本轮调试目标重新启动前后端服务。
4. 需要授权的场景必须先完成授权注入或登录流程；若遇到注册受限（如验证码、短信、人机验证）无法自行获取可用会话，必须暂停并向用户索取可用账户、token 或其他可登录方式。
5. 最终结论必须基于联调证据（至少包含 URL/页面状态与关键结果），不能仅基于代码推断给出“已验证通过”。
6. 测试完成、前后端浏览器联调完成后，必须关闭本轮为联调启动的前端与后端进程，禁止遗留后台运行进程。
7. 进程收口必须可核验：至少记录一次“关闭动作 + 关闭后状态检查”结论（例如端口不再监听或对应进程已退出）。
