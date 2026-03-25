# Next.js 安全规则

## 适用范围

适用于使用 Next.js 构建的全栈 Web 应用，包括 App Router、Route Handlers、Server Components、Server Actions 和中间件。

## 默认工作方式

- 先区分服务端代码和客户端代码
- 先判断数据在服务端边界、浏览器边界还是接口边界流动
- 任何进入客户端 bundle 的内容，都视为默认可见

## 生产安全基线

- 只把真正可公开的配置放进客户端环境变量
- 认证、授权和敏感数据查询优先放在服务端
- 响应头、缓存策略、重定向和图片来源都要显式配置
- 对外开放的 Route Handlers 必须做输入校验和权限控制

## 核心规则

### NEXT-CONFIG-001：客户端环境变量都是公开的

- 任何带 `NEXT_PUBLIC_` 的配置都视为公开信息
- API Key、签名密钥、数据库凭证不能进入客户端 bundle

### NEXT-AUTH-001：认证和授权必须放在服务端

- Middleware、Route Handlers、Server Actions、服务端组件读取敏感数据时都要校验身份
- 不能仅依赖前端路由守卫做权限控制

### NEXT-ACTION-001：Server Actions 必须校验输入和权限

- Server Action 不是天然安全
- 调用前要校验参数、身份和对象级权限
- 修改型操作要考虑幂等和重复提交

### NEXT-API-001：Route Handlers 必须显式校验输入

- `searchParams`、Body、Header、Cookie 都不能直接信任
- 结构化校验优先于零散 `if`

### NEXT-RESP-001：服务端返回值必须控制字段暴露

- 不要把完整数据库对象直接返回给客户端
- 对用户、订单、权限、账单类数据使用明确的输出模型

### NEXT-XSS-001：富文本和 HTML 渲染必须防 XSS

- React 默认转义并不覆盖 `dangerouslySetInnerHTML`
- Markdown、富文本、CMS 内容必须清洗后渲染

### NEXT-URL-001：重定向和导航目标必须校验

- `redirect()`、`NextResponse.redirect()` 的目标不能直接来自用户输入
- 默认仅允许相对路径或白名单域名

### NEXT-CACHE-001：缓存和重验证策略必须明确

- 页面、请求、Server Component 的缓存行为要能解释清楚
- 含用户态、权限态、动态敏感数据的内容不能被错误缓存

### NEXT-HEADERS-001：安全响应头要在应用或边缘层明确设置

- 是否启用 CSP、Frame 防护、Referrer-Policy 等要统一管理
- 不能依赖“可能上游已经有”

### NEXT-IMAGE-001：远程图片和资源来源要白名单

- 外部图片域、资源域和下载域都要最小化
- 不可信资源 URL 不直接拼进页面

### NEXT-SSRF-001：服务端外部请求必须防 SSRF

- 用户可控 URL 不能直接交给 `fetch`
- 对目标域、协议、超时和重定向都要限制

### NEXT-CSRF-001：Cookie 认证写操作必须防 CSRF

- 如果浏览器自动带 Cookie，修改型请求要考虑 CSRF
- 只用 Header Token 的接口通常不受 CSRF 影响

### NEXT-FILE-001：上传、下载和文件访问必须隔离

- 用户输入不能直接映射为服务端文件路径
- 用户上传内容默认按不可信内容处理

## 审计重点

- 是否把敏感环境变量暴露到客户端
- 是否仅靠前端判断权限
- 是否存在未校验的 Server Actions、Route Handlers
- 是否存在错误缓存用户态数据
- 是否存在危险重定向、富文本渲染和外部请求
