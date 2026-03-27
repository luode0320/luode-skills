# FastAPI Web 安全规则

## 适用范围

适用于 FastAPI、Starlette、Pydantic、Uvicorn 相关服务。

## 默认工作方式

- 新代码默认采用安全写法
- 修改代码时，顺带关注高影响风险
- 结论要基于路由、依赖、配置和运行方式给出，不靠猜测

## 生产安全基线

- 生产环境禁止 `reload` 和调试模式
- OpenAPI / Docs 在生产环境默认关闭或受保护
- 认证通过依赖统一挂载
- 请求模型和响应模型都要显式声明
- 上传、下载、外部请求、WebSocket 都按高风险入口处理

## 核心规则

### FASTAPI-DEPLOY-001：生产环境不能使用开发态运行模式

- 不要在生产环境使用 `--reload`
- 不要把调试异常页暴露给用户

### FASTAPI-OPENAPI-001：文档页和 OpenAPI 默认关闭或受保护

- `/docs`、`/redoc`、`/openapi.json` 默认不公开暴露

### FASTAPI-AUTH-001：认证应通过依赖统一执行

- 不要在每个路由函数里手写零散认证逻辑
- 受保护路由优先挂在 Router 边界统一控制

### FASTAPI-AUTH-002：认证信息不要放在 URL 里

- Token、API Key、重置链接密钥不要放 query 参数
- Header 优先于 URL 参数

### FASTAPI-AUTH-003：密码必须强哈希存储

- 密码使用 bcrypt 或 argon2id
- 禁止明文或快速哈希直接存储密码

### FASTAPI-AUTH-004：JWT 校验必须严格

- 校验签名、算法、有效期和关键 claims
- JWT 载荷不能存放敏感秘密

### FASTAPI-AUTHZ-001：对象级和字段级权限必须明确

- 用户可控 ID 的资源访问必须做所有权或租户校验
- 返回模型要避免过度暴露

### FASTAPI-SESS-001：Cookie 会话必须安全配置

- 生产 HTTPS 环境下设置 `Secure`
- 会话 Cookie 设置 `HttpOnly`
- `SameSite` 策略要明确

### FASTAPI-CSRF-001：Cookie 认证写操作必须防 CSRF

- 仅在浏览器会自动带 Cookie 时适用

### FASTAPI-VALID-001：请求解析必须结构化

- 优先使用 Pydantic 模型
- 写接口拒绝额外字段，防止批量赋值漏洞

### FASTAPI-RESP-001：响应模型必须控制字段暴露

- 不要直接返回 ORM 对象或内部字典
- 用户、账单、权限、认证数据都要定义公开模型

### FASTAPI-XSS-001：HTML 输出和模板必须防 XSS

- 不可信内容不能直接进入 HTML
- 富文本先清洗，模板保持安全默认值

### FASTAPI-CORS-001：CORS 必须显式且最小授权

- 不要把 `allow_credentials=True` 和宽泛 Origin 同时放开

### FASTAPI-LIMITS-001：请求与上传大小必须限制

- Body、multipart、文件数量和大小都要受控

### FASTAPI-FILES-001：文件访问必须防路径穿越

- `FileResponse`、静态文件目录不能直接使用用户路径

### FASTAPI-UPLOAD-001：上传文件必须校验并安全暴露

- 校验类型、大小、数量
- 用户文件默认视为不可信内容

### FASTAPI-INJECT-001：数据库访问必须防注入

- SQL 一律参数化
- 动态字段采用白名单

### FASTAPI-INJECT-002：禁止命令注入

- 不要把用户输入拼到 `subprocess` 或 shell

### FASTAPI-SSRF-001：外部请求必须限制目标

- 用户可控 URL 不能直接请求
- 限制协议、域名、IP、超时和重定向

### FASTAPI-WS-001：WebSocket 也必须鉴权和限流

- 非公开频道要在握手阶段鉴权
- 对来源、连接数和消息频率做控制

## 审计重点

- 是否存在 `debug=True`、`--reload`、开放 docs
- 是否存在缺少依赖认证的路由
- 是否存在 Pydantic 缺失、响应过度暴露、任意文件访问
- 是否存在危险外部请求、SQL 拼接、命令执行和未鉴权 WebSocket
