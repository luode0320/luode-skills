# Flask Web 安全规则

## 适用范围

适用于 Flask 应用及其模板、Session、上传、路由和部署配置。

## 生产安全基线

- 生产环境不能使用 Flask 开发服务器
- 生产环境必须关闭 Debug
- `SECRET_KEY` 强随机且保密
- Session Cookie 安全属性明确
- 反向代理信任、Host 校验、请求大小限制都要显式配置

## 核心规则

### FLASK-DEPLOY-001：生产环境禁止开发服务器和 Debug

- 不要用 `flask run` 或开发服务器跑生产
- 不要对外暴露调试页面和堆栈

### FLASK-CONFIG-001：密钥和敏感配置必须外置

- `SECRET_KEY`、数据库密码、第三方凭证通过环境变量或密钥系统注入
- 不能写死在代码里

### FLASK-SESS-001：Session Cookie 必须安全配置

- 生产 HTTPS 环境下启用 `Secure`
- 启用 `HttpOnly`
- `SameSite` 策略明确

### FLASK-CSRF-001：Cookie 认证写操作必须防 CSRF

- 表单提交和 Cookie 会话写接口都要考虑 CSRF
- 不要为了方便整体关闭 CSRF

### FLASK-XSS-001：模板默认保持安全渲染

- Jinja 模板默认保持自动转义
- 不要把不可信内容直接当 HTML 输出
- 不要执行来自外部的模板字符串

### FLASK-HEADERS-001：安全响应头要显式配置

- Frame、防 MIME 嗅探、Referrer-Policy、CSP 等要统一管理

### FLASK-LIMITS-001：请求和上传大小必须限制

- 上传接口要限制大小、数量和类型
- 表单和 JSON 解析都不能无上限

### FLASK-HOST-001：Host 和代理信任必须正确

- Host 校验要启用
- 反向代理信任不能过宽

### FLASK-FILE-001：文件服务必须防路径穿越

- 用户输入不能直接作为文件路径
- 上传目录不能直接变成活动内容站点

### FLASK-UPLOAD-001：上传要校验并安全存储

- 服务端生成文件名
- 校验类型和大小
- 风险格式按附件下载处理

### FLASK-INJECT-001：数据库访问必须参数化

- 不要拼 SQL
- 动态字段和排序字段走白名单

### FLASK-INJECT-002：避免命令注入

- 不把用户输入拼进 shell 命令

### FLASK-SSRF-001：外部请求必须防 SSRF

- 用户可控 URL 要限制协议和目标域
- 屏蔽本机和内网地址

### FLASK-REDIRECT-001：重定向必须校验目标

- 回跳和通用重定向仅允许相对路径或白名单域名

### FLASK-CORS-001：CORS 必须显式和最小化

- 不能用全开放带凭证跨域

## 审计重点

- 是否仍然在生产环境使用 Debug 或开发服务器
- 是否把密钥写死在配置文件里
- 是否存在模板 XSS、SQL 拼接、任意文件路径、危险外部请求
- Session、CORS、代理信任、Host 校验是否配置过宽
