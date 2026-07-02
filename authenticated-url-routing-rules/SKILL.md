---
name: authenticated-url-routing-rules
description: 当用户提供任意 URL、链接或网页地址，并要求打开、读取、分析、总结、截图、提取内容、排查页面、查看文档、理解网页、检查资料、访问在线文档或处理已在浏览器登录过的页面时触发。默认优先使用 Chrome Plugin 的 `chrome:control-chrome` 接管用户已登录的真实 Chrome profile，以复用登录态、扩展、权限和已打开标签页；禁止优先使用 `web`、隔离浏览器、无登录态 Playwright 或普通抓取导致权限丢失。若 Chrome Plugin 不可用，再回退到 `agent-browser` 的 auto-connect、state、profile 或 session；若仍遇到登录页、权限页、验证码或人机验证，要求用户在真实 Chrome 中完成授权后继续，不得通过搜索引擎或第三方页面绕过权限。
---

# 认证 URL 路由规则

## 目标

当用户给出 URL 时，先选对浏览器通道，再分析页面内容。

本 skill 只负责 URL 访问通道决策：默认让 agent 复用用户真实 Chrome 登录态，避免内部文档、企业系统、微信文档、飞书、语雀、Notion、Confluence、TAPD、GitHub 私有页面等链接因隔离浏览器或 `web` 抓取而丢失权限。

## 默认路由

1. 只要用户消息中包含 URL 或明显的网页链接，就先触发本 skill。
2. 优先加载并执行 `chrome:control-chrome`，通过 Chrome Plugin 接管用户已登录的真实 Chrome profile。
3. 若用户说明“我已经在浏览器打开 / 已登录 / 默认浏览器能看 / 你看这个链接”，仍按第 2 步执行，不再询问是否需要复用登录态。
4. Chrome Plugin 可用时，不优先使用 `web`、隔离 Playwright、无登录态浏览器或普通 HTTP 抓取。
5. 如果用户明确说“这是公开网页，用 web 搜索 / 网页抓取即可”，才允许优先走 `web`。

## 回退顺序

只有当前一步不可用或被明确阻断时，才进入下一步：

1. `chrome:control-chrome`
2. `agent-browser --auto-connect`
3. `agent-browser` 的 state / profile / session
4. 请求用户在真实 Chrome 中完成登录、授权、验证码或权限开通后继续

不得把登录页、权限页、验证码页或 403 / 无权限页面替换成搜索结果、公开缓存、第三方转载或其他站点来绕过鉴权。

## 执行要求

- 先判断页面状态，再分析内容：至少确认当前 URL、页面标题和正文/截图/可访问状态。
- 若页面已打开在用户 Chrome 标签页中，优先复用或切到该标签页；若没有打开，再在真实 Chrome 中打开 URL。
- 对文档类、后台类、管理类链接默认只读；任何写入、删除、提交、分享权限调整、表单提交、导出敏感数据等动作必须另行获得用户明确授权。
- 页面跳转、弹窗、登录回调或异步刷新后，必须重新读取页面状态。
- 遇到权限问题时，报告看到的页面状态和阻断点，不要臆造页面内容。

## Chrome Plugin 确认步骤

使用 `chrome:control-chrome` 时，按以下顺序执行：

1. 先按 `chrome:control-chrome` 的要求完成 Chrome runtime 初始化，并完整读取 `browser.documentation()`。
2. 立即调用 `browser.nameSession("🔎 <任务名>")`，便于用户和后续 agent 识别本次浏览器接管任务。
3. 调用 `browser.user.openTabs()` 检查用户真实 Chrome 中是否已有目标 URL 标签页。
4. 若存在匹配标签页，使用 `browser.user.claimTab(tabInfo)` 认领该标签页，不要重新 `goto` 同一 URL，避免刷新丢失用户页面状态。
5. 若不存在匹配标签页，才用 `browser.tabs.new()` 新建标签页并 `tab.goto(url)`。
6. 打开或认领后，先读取 `tab.url()` 与 `tab.title()` 作为最低可访问性证据。
7. 只有浏览器策略允许时，才继续读取 DOM、截图或可见文本；若策略拒绝，进入“异常处理”。
8. 浏览器任务结束前必须调用 `browser.tabs.finalize({ keep })`。如果页面需要用户继续查看或后续继续处理，将目标标签页以 `status: "handoff"` 保留；否则按 Chrome 文档默认清理。

## 实测回灌清单

本 skill 必须持续吸收真实执行中已经确认有效的步骤和异常处理办法。只要某个 URL 访问问题已经通过本 skill、`chrome:control-chrome` 或授权浏览器链路解决，并且该问题未来可能重复出现，就要优先回写到本 skill，而不是只留在聊天记录里。

### 已确认可用步骤

- 用户已经在默认 Chrome 打开并登录目标页面时，优先用 `openTabs()` 查找现有标签页，再用 `claimTab(tabInfo)` 认领；认领成功后不要重新打开同一 URL。
- 认领或打开页面后，先读取 `tab.url()` 与 `tab.title()`。这两项是最低可访问性证据，能区分“Chrome 登录态已复用但正文不可读”和“页面根本没打开 / 没权限”。
- 对微信文档这类富文档页面，标题可读不等于正文可读；必须继续确认正文、DOM、截图或可见文本是否被工具允许读取。
- 页面需要用户继续查看、补授权或手动复制允许分享的内容时，收口前将标签页保留为 `handoff`，不要关闭用户正在使用的真实标签页。

### 已确认异常处理

- 如果 Chrome Plugin 已成功连接并认领用户标签页，但正文读取被浏览器安全策略拒绝，结论写成“路由验证成功、内容读取被策略阻断”，不得写成“文档已分析完成”。
- 该安全策略拒绝不是普通登录失败；不得通过 raw CDP、截图 OCR、复制页面、下载、搜索引擎、第三方转载、另一个浏览器或无登录态抓取绕过。
- 如果只能读取 URL / 标题，最终只报告这些已验证信息和阻断事实；未读到正文时不得补写正文摘要、需求结论或页面细节。
- 如果是登录页、权限页、验证码或人机验证，停在真实 Chrome 授权分支，请用户在 Chrome 中完成动作后再重新 `openTabs()` / `claimTab()`，不要索取密码、验证码、cookie、token 或 localStorage。

### 回写要求

- 新增的异常处理必须写成“触发条件 -> 允许动作 -> 禁止动作 -> 收口证据”，避免只写抽象提醒。
- 如果新经验会改变 `description`、触发条件或 `##` 标题，收口前必须重新生成 skill 字典。
- 如果新经验来自具体页面，skill 正文只沉淀通用模式；不要把敏感页面正文、内部标题、截图、cookie、token、HAR 或导出文件写入仓库。

## 异常处理

### Chrome Plugin 不可用

- 先按 `chrome:control-chrome` 的故障文档排查连接、扩展、浏览器发现或选择问题。
- 若仍不可用，说明 Chrome Plugin 不可用原因，再进入 `agent-browser --auto-connect`。
- 不得在未说明 Chrome Plugin 失败原因时直接改用隔离浏览器或 `web`。

### 已登录标签页可打开但正文读取被安全策略拒绝

- 该场景说明 Chrome 登录态复用成功，但浏览器安全策略禁止 agent 读取该页面内容。
- 必须停止进一步正文读取尝试，不得用 raw CDP、浏览器内部命令、另一个浏览器、截图 OCR、下载、复制页面内容、搜索引擎或第三方转载绕过策略。
- 可以报告已经确认的安全证据，例如 URL、页面标题、是否认领了已打开标签页，以及策略拒绝的事实。
- 将目标标签页以 `handoff` 保留，让用户可在真实 Chrome 中继续查看或手动复制允许分享的内容。

### 登录页、权限页、验证码或人机验证

- 报告当前页面状态和阻断点。
- 请求用户在真实 Chrome 中完成登录、授权、验证码或权限开通。
- 用户完成后，再重新通过 `openTabs()` 认领或复用原标签页继续。
- 不保存或索取用户密码、验证码、cookie、token 或 localStorage。

### 页面标题可读但正文为空

- 先判断是否为富文本编辑器、canvas、iframe、懒加载、权限遮罩或安全策略限制。
- 可按 Chrome 文档允许的方式尝试一次截图或 DOM 快照；若仍无内容，报告“仅确认标题/URL，正文未被工具可读”。
- 不把标题可读误写成正文已分析完成。

## 安全边界

- 不要求用户粘贴 cookie、token、localStorage、sessionStorage 或账号密码。
- 不把认证 state、profile、截图、HAR、导出文件等敏感临时产物提交到仓库。
- 如果必须临时保存 state 文件，必须说明其敏感性，放入忽略路径或任务后删除。
- 不在未确认范围的情况下跨域跳转到无关站点。
- 不用登录态执行破坏性操作。

## 通过标准

- 对任意 URL 任务，已优先尝试 `chrome:control-chrome`。
- 若未使用 Chrome Plugin，已说明不可用原因并按回退顺序尝试下一通道。
- 若页面需要用户授权，已停在真实授权阻断处并说明用户需要完成的动作。
- 最终分析结论来自真实浏览器页面状态、文本、截图或等价工具输出，不来自猜测。
- 若浏览器安全策略拒绝正文读取，已明确标记为“路由验证成功、内容读取被策略阻断”，未伪装成完整内容分析通过。

## 维护注意事项

- 在 Windows PowerShell 下维护本 skill 或生成 `agents/openai.yaml` 时，先设置 UTF-8 运行环境，例如 `$env:PYTHONUTF8='1'`，避免 Python 按 GBK 读取中文 frontmatter 失败。
- 通过命令行传递包含 `$authenticated-url-routing-rules` 的 `default_prompt` 时，必须防止 PowerShell 把 `$authenticated` 当变量展开；生成后要读取 `agents/openai.yaml` 核对默认提示是否保留完整 skill 名。
- 执行过程中遇到并确认解决的 URL 认证、真实 Chrome 接管、登录态复用、权限页、正文读取策略或 handoff 问题，必须按“实测回灌清单”回写本 skill。
- 修改本 skill 的 `description`、新增或修改 `##` 标题后，必须运行 `python skill-dictionary/generate_dictionary.py` 刷新 `skill-dictionary/data.js` 与 `字典.md`。
- 修改后必须运行 `python .system/skill-creator/scripts/quick_validate.py authenticated-url-routing-rules` 做结构校验。

## 常见触发示例

- `分析这个 URL`
- `打开这个微信文档看看`
- `总结这个飞书链接`
- `这个页面我浏览器已经登录了，你看一下`
- `读一下这个 Notion / Confluence / TAPD 页面`
- `这个链接 agent 打开有权限问题，帮我用已登录浏览器看`
