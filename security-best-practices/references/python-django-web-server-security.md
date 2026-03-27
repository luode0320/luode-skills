# Django Web 安全规则

## 适用范围

适用于 Django 应用及其模板、认证、Session、Admin、ORM 和中间件体系。

## 生产安全基线

- `DEBUG=False`
- `SECRET_KEY` 强随机、保密、可轮换
- `ALLOWED_HOSTS` 明确配置
- 启用安全相关中间件和 Cookie 策略
- 管理后台、调试页面、内部接口不能裸露在公网

## 核心规则

### DJANGO-DEBUG-001：生产环境必须关闭 Debug

- 不要向客户端暴露堆栈、配置和内部路径

### DJANGO-CONFIG-001：密钥和敏感配置必须外置

- `SECRET_KEY`、数据库密码、第三方凭证通过环境变量或密钥管理注入
- 不要提交到仓库，不要写入日志

### DJANGO-HOST-001：Host 校验必须启用

- `ALLOWED_HOSTS` 不能留空或过宽
- 反向代理场景下要明确 Host 与协议转发策略

### DJANGO-CSRF-001：Cookie 认证写操作必须使用 CSRF 防护

- Django 自带 CSRF 机制，不要随意关闭
- 如果某接口免除了 CSRF，要写清楚原因和替代保护

### DJANGO-AUTH-001：认证与授权必须一致且可复用

- 保护逻辑尽量集中，不要在视图里到处散落权限判断
- 对象级访问要校验所有权和租户边界

### DJANGO-SESS-001：Session 和 Cookie 必须安全配置

- 生产 HTTPS 环境下启用 `Secure`
- 会话 Cookie 启用 `HttpOnly`
- `SameSite` 策略明确

### DJANGO-XSS-001：模板保持自动转义

- 不要滥用 `safe`
- 富文本渲染需要清洗
- 不可信模板片段不能动态执行

### DJANGO-ORM-001：数据库访问默认走 ORM 或参数化 SQL

- 不要用字符串拼 SQL
- 原生 SQL 仅在必要时使用，并确保参数化

### DJANGO-RESP-001：响应字段不能过度暴露

- API、序列化器、模板上下文都要最小化字段
- 不要返回密码哈希、内部状态、权限细节等敏感字段

### DJANGO-FILE-001：文件上传和静态文件服务要隔离

- 上传内容不能直接作为活动内容内联暴露
- 文件路径不要直接来自用户输入

### DJANGO-REDIRECT-001：登录回跳和通用跳转必须校验

- `next` 等回跳参数只能允许安全路径或白名单域名

### DJANGO-ADMIN-001：管理后台必须受保护

- Admin 入口要受认证保护，必要时加网络层限制
- 不要把管理界面暴露给所有互联网流量

## 审计重点

- 是否开启了 `DEBUG`
- 是否滥用 `csrf_exempt`
- 是否存在 `safe`、富文本、原生 SQL、任意回跳
- 是否把敏感字段通过序列化器或模板暴露出去
- Admin、内部接口、上传目录是否暴露过宽
