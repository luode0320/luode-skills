# 已下载中文安全种子选择规则

## 用途

用于把已下载并中文化的 `security-best-practices` seeds 作为本 skill 的框架细则来源。

## 使用方式

- 先用本 skill 的通用基线判断问题类型。
- 再根据当前语言和框架，打开对应中文 seed 文件补充实现细节。
- 同时存在前后端时，前后端 seed 都要读，不只读一侧。

## 已下载 seed 路径

- Go 后端通用：
  - `E:/luode-skills/downloaded-seeds/security-best-practices/references/golang-general-backend-security.md`
- Express 后端：
  - `E:/luode-skills/downloaded-seeds/security-best-practices/references/javascript-express-web-server-security.md`
- Next.js 全栈 / 服务端：
  - `E:/luode-skills/downloaded-seeds/security-best-practices/references/javascript-typescript-nextjs-web-server-security.md`
- React 前端：
  - `E:/luode-skills/downloaded-seeds/security-best-practices/references/javascript-typescript-react-web-frontend-security.md`
- Vue 前端：
  - `E:/luode-skills/downloaded-seeds/security-best-practices/references/javascript-typescript-vue-web-frontend-security.md`
- 通用前端：
  - `E:/luode-skills/downloaded-seeds/security-best-practices/references/javascript-general-web-frontend-security.md`
- Django 后端：
  - `E:/luode-skills/downloaded-seeds/security-best-practices/references/python-django-web-server-security.md`
- FastAPI 后端：
  - `E:/luode-skills/downloaded-seeds/security-best-practices/references/python-fastapi-web-server-security.md`
- Flask 后端：
  - `E:/luode-skills/downloaded-seeds/security-best-practices/references/python-flask-web-server-security.md`

## 选择提示

- 服务端认证、授权、输入校验、上传下载、外部请求优先读后端 seed。
- 浏览器 Cookie、Token、前端权限展示、富文本、跳转和 Web Storage 优先读前端 seed。
- 全栈项目如果存在 Next.js Route Handlers、Server Actions、客户端页面，要同时读服务端和客户端相关细则。
- 如果代码里看不出某项安全能力是否由网关、代理或平台兜底，要标记为“代码中不可见，需运行时确认”。
