# React 前端安全规则

## 适用范围

适用于 React 18/19 及 TypeScript/JavaScript 客户端应用。

## 默认工作方式

- React 的“默认转义”很有帮助，但只覆盖一部分风险
- 凡是绕开 React 正常渲染路径的地方，都要额外警惕
- 前端只负责展示和交互，不负责最终授权

## 生产安全基线

- 客户端 bundle 不包含秘密
- 富文本、Markdown、外链、文件预览都要显式治理
- 第三方脚本最小化
- 跨域、跨窗口消息、认证状态流转都要可解释

## 核心规则

### REACT-CONFIG-001：客户端环境变量都是公开信息

- 不要把私钥、数据库凭证、服务端 API Key 放进前端环境变量
- 构建时进入客户端 bundle 的内容，默认都会被用户看到

### REACT-XSS-001：谨慎使用 `dangerouslySetInnerHTML`

- 不可信内容不能直接放进 `dangerouslySetInnerHTML`
- Markdown、富文本、CMS 内容必须先清洗

### REACT-XSS-002：不要绕开 React 默认转义

- 默认用 JSX 表达文本
- 不要为了图方便改成字符串拼 HTML

### REACT-DOM-001：避免危险 DOM Sink

- 不要在 React 代码里回退到 `innerHTML`、`outerHTML`、字符串事件处理器
- 若必须操作原生 DOM，要明确说明原因和风险边界

### REACT-URL-001：`href`、`src`、跳转地址必须校验

- 外链、下载链、跳转链路都要限制协议和域名
- `javascript:`、`data:` 默认禁止

### REACT-MARKUP-001：Markdown 和富文本渲染必须安全配置

- 只允许必要标签和属性
- 关闭危险 HTML 扩展能力
- 图片、链接、iframe 等节点要做额外白名单控制

### REACT-CSP-001：高风险页面应配 CSP

- 展示用户内容、接第三方脚本、接广告或可配置页面时优先使用 CSP
- 不要依赖大量内联脚本

### REACT-3P-001：第三方脚本必须最小化和可追踪

- 标签管理器、埋点、客服、实验平台都要视为高风险依赖
- 引入前说明来源、权限和替代成本

### REACT-AUTH-001：令牌和会话处理要考虑 XSS 风险

- 不要把高敏感 Token 长期放在 Web Storage
- 如果使用 Cookie 会话，要明确 CSRF 策略

### REACT-CSRF-001：Cookie 认证写操作必须考虑 CSRF

- 浏览器自动带 Cookie 时，修改类请求要有 CSRF 防护
- 只用 Header Token 的请求通常不需要额外 CSRF 机制

### REACT-AUTHZ-001：不要依赖前端做最终授权

- 前端隐藏按钮不等于后端授权
- 所有关键权限判断都必须在服务端再做一次

### REACT-NET-001：外发请求不能造成数据泄漏

- 不要把用户可控 URL 直接当作请求目标
- 不要把敏感 Header 自动带到未知域名

### REACT-REDIRECT-001：跳转必须防开放重定向

- 回跳地址只允许相对路径或白名单域名

### REACT-SW-001：Service Worker 属于高权限能力

- 只有确实需要时才引入
- 缓存更新、回滚和资源作用域都要明确

### REACT-POSTMSG-001：`postMessage` 必须校验来源

- 收消息要校验 `origin`
- 发消息要指定 `targetOrigin`

### REACT-FILE-001：上传与预览不能引入活动内容风险

- 上传文件要限制类型和大小
- 预览 HTML、SVG、富媒体时要格外谨慎

## 审计重点

- 是否使用了 `dangerouslySetInnerHTML`
- 是否把敏感配置打进客户端 bundle
- 是否把 Token 长期放在 `localStorage`
- 是否存在不受控第三方脚本、危险外链、开放重定向
- 是否只在前端做权限判断
