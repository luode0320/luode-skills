# jQuery 前端安全规则

## 适用范围

适用于使用 jQuery 操作 DOM、发起请求和处理页面交互的传统前端项目。

## 默认工作方式

- jQuery 项目最常见问题不是“没有安全能力”，而是太容易把字符串直接塞进 DOM、请求或 URL
- 优先避免危险 API，而不是依赖人工记忆

## 核心规则

### JQ-XSS-001：谨慎使用 `.html()`

- 不可信内容默认不要进入 `.html()`
- 渲染纯文本时使用 `.text()`
- 必须展示富文本时，先做清洗

### JQ-XSS-002：避免字符串事件和危险属性注入

- 不要动态设置 `onclick`、`onerror` 等事件属性
- 动态设置 `href`、`src` 时要校验协议和域名

### JQ-XSS-003：不要把模板字符串直接拼成 DOM

- 尤其不要把用户输入拼接进 HTML 字符串再 append 到页面
- 复杂组件优先用模板或组件化手段生成

### JQ-AJAX-001：AJAX 请求要明确处理认证和 CSRF

- Cookie 认证的写操作要带 CSRF Token
- 不要把令牌明文写在 URL 查询参数里

### JQ-JSONP-001：默认禁用 JSONP

- JSONP 天然扩大脚本注入面
- 除非项目历史包袱无法移除，否则不再新增 JSONP 依赖

### JQ-URL-001：跳转和外链必须校验

- `location.href`、`window.open`、动态链接地址都要走白名单
- 不允许 `javascript:`、`data:` 这类危险协议

### JQ-STORAGE-001：不要把敏感凭证存浏览器可读存储

- `localStorage` 和 `sessionStorage` 容易被 XSS 读取
- 访问令牌、刷新令牌、敏感密钥默认不放这里

## 审计重点

- 是否大量使用 `.html()`、字符串拼接 DOM、`append("<div>...")`
- 是否仍在使用 JSONP
- 是否把 CSRF、Token、敏感参数直接拼到 URL
- 是否使用了危险事件属性和不可信链接
