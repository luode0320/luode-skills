# URL 认证路由执行失败案例库

本文件保存已脱敏、可复用的 URL 认证、真实 Chrome 接管、权限页和正文读取失败案例，归属 `authenticated-url-routing-rules`。详细页面内容、cookie、token、HAR 和私有路径不得写入。

## 统一维护规则

- 状态使用 `candidate`、`active`、`stale`、`superseded`、`rejected`；只有同输入同成功标准验证通过且来源可回溯的案例才能 `active`。
- 执行前由 `execution-failure-learning-rules` 按环境、浏览器通道、页面状态和错误特征预检；不匹配时不得套用。
- 新案例先写 candidate；根因、复验、脱敏、去重和当前轮维护授权齐全后才能晋级 active。

## URL-AUTH-001

- 状态：`active`
- 类型：浏览器策略阻断
- 适用通道：Chrome Plugin / 用户真实 profile
- 错误特征：已连接并认领标签页，但正文读取被浏览器安全策略拒绝
- 根因：页面内容读取策略阻止正文访问，不等同于登录失败
- 解决方案：只报告路由验证成功和正文读取被阻断；保留当前 Chrome 授权链路，不切换 raw CDP、截图 OCR、下载或搜索绕过
- 验证：确认 URL、标题和标签页状态可读，正文未被声称为已分析
- 禁止动作：索取密码、验证码、cookie、token 或绕过鉴权
- 来源：`authenticated-url-routing-rules/SKILL.md` 实测回灌清单
- 最后验证：2026-07-12

## URL-AUTH-002

- 状态：`active`
- 类型：登录/权限状态
- 适用通道：Chrome Plugin
- 错误特征：页面停留在登录页、权限页、验证码或人机验证
- 根因：用户真实 Chrome 会话未完成授权
- 解决方案：停在真实 Chrome 授权分支，用户完成动作后重新 `openTabs()` / `claimTab()`
- 验证：重新认领后确认页面状态不再是授权阻断页
- 禁止动作：用公开搜索、第三方转载、无登录态抓取替代真实页面
- 来源：`authenticated-url-routing-rules/SKILL.md` 异常处理规则
- 最后验证：2026-07-12
