# Express Web 服务安全规则

## 适用范围

适用于使用 Express 4.x / 5.x、Node.js LTS 构建的服务端 Web 应用和 API。

## 默认工作方式

- 所有输入都视为不可信，包括 `req.params`、`req.query`、`req.body`、Header、Cookie、上传文件和外部系统返回值
- 写新代码时默认采用安全实现
- 改已有代码时，顺手识别接近代码中的明显高风险问题

## 生产安全基线

- 使用 `helmet` 或同等能力设置基础安全响应头
- 关闭 `x-powered-by`
- 正确配置反向代理信任关系
- 请求体大小和 multipart 解析大小必须受控
- Cookie、Session、CORS 必须显式配置
- 生产环境错误响应不能泄漏堆栈和内部细节

## 核心规则

### EXPRESS-INPUT-001：所有输入都要校验和归一化

- 查询参数、路径参数、Header、Body 都要先校验再使用
- 对枚举、排序字段、过滤字段使用白名单
- 不要直接把 `req.query` 和 `req.body` 原样传给数据库或模板

### EXPRESS-HEADERS-001：基础安全响应头必须明确配置

- 优先使用 `helmet`
- 是否启用 CSP、Frame 防护、Referrer-Policy 等要有明确策略
- 不要假设上游一定会帮你补这些 Header

### EXPRESS-FINGERPRINT-001：减少框架指纹暴露

- 关闭 `x-powered-by`
- 404、500 等错误响应不要暴露框架和版本细节
- 调试信息只进内部日志，不直接给客户端

### EXPRESS-COOKIE-001：生产 Cookie 必须带安全属性

- HTTPS 生产环境下使用 `Secure`
- 会话 Cookie 使用 `HttpOnly`
- `SameSite` 默认优先 `Lax`
- Cookie 作用域最小化，不随意放大 Path 和 Domain

### EXPRESS-SESS-001：Session 存储必须可用于生产

- 不要用开发态内存 Session 存储跑生产
- Session 名称不要使用默认值
- Session 生命周期、刷新策略和固定攻击防护要明确

### EXPRESS-CSRF-001：Cookie 认证写操作必须防 CSRF

- Cookie 自动带凭证时，写操作必须加 CSRF 防护
- 不要通过 GET 触发状态变更
- 如果只走 `Authorization` Header，一般不需要额外 CSRF 机制

### EXPRESS-CORS-001：CORS 必须显式且最小授权

- `allow_credentials` 与通配 Origin 不能同时宽松配置
- 不要对整个互联网开放带凭证跨域
- 允许的 Header、Method、Origin 都要精确约束

### EXPRESS-PROXY-001：`trust proxy` 必须谨慎配置

- 只有在明确受信代理存在时才开启
- 错误的代理信任会影响真实 IP、协议判断和安全控制

### EXPRESS-BODY-001：请求体解析必须有限制

- JSON、表单、上传大小要分别限制
- 避免无上限 body 造成内存和 CPU 压力

### EXPRESS-QUERY-001：防止参数污染和类型混乱

- 同名参数、多值参数、数组参数都要明确处理
- 不要默认接受重复 query 参数

### EXPRESS-XSS-001：HTML 输出必须防 XSS

- 模板渲染保持自动转义
- 不要把用户输入直接拼接进 HTML
- 不要渲染不可信模板字符串

### EXPRESS-FILE-001：文件服务必须防路径穿越

- `sendFile`、`download`、静态文件路径都不能直接使用用户输入
- 上传目录不要直接作为活动内容根目录暴露

### EXPRESS-UPLOAD-001：上传必须校验并安全存储

- 校验大小、类型、数量
- 服务端生成文件名
- HTML、SVG、JS 等风险格式不要直接内联访问

### EXPRESS-INJECT-001：防 SQL / NoSQL 注入

- SQL 一律参数化
- Mongo 风格查询要防操作符注入
- 不要把未经处理的对象直接塞进数据库查询

### EXPRESS-CMD-001：禁止把用户输入拼接到命令行

- 能用库解决就不用 shell
- 禁止 `child_process.exec` 拼接不可信输入
- `spawn` / `execFile` 也要做白名单校验

### EXPRESS-SSRF-001：外部请求必须防 SSRF

- 用户可控 URL 只能访问白名单
- 阻止本机、内网和云元数据地址
- 请求超时和重定向策略必须显式

### EXPRESS-ERROR-001：错误处理不能泄漏敏感信息

- 客户端错误响应只返回必要信息
- 堆栈、SQL、内部路径、配置值只写内部日志
- 日志中也不要记录完整凭证

### EXPRESS-AUTH-001：认证和授权接口要有限流和防爆破

- 登录、验证码、找回密码、令牌签发接口要有限流
- 错误信息不要帮助攻击者枚举账户

### EXPRESS-DEPS-001：依赖版本和中间件补丁要及时

- Node、Express、身份认证、中间件、文件处理和解析组件都要视为安全敏感依赖

## 审计重点

- 是否存在 `helmet` 缺失、`x-powered-by` 未关闭、错误回包过多
- 是否存在 `sendFile/download` 路径直接来自用户输入
- 是否存在 SQL/NoSQL 查询拼接、危险命令执行、任意跳转
- 是否存在 `trust proxy`、CORS、Session、Cookie 配置过宽
- 是否存在登录接口未限流、上传无约束、body 无上限
