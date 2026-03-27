# 前端 JavaScript / TypeScript 通用安全规则

## 适用范围

适用于现代浏览器环境下的原生 JavaScript / TypeScript 前端代码。

## 默认工作方式

- DOM、URL、消息通道、浏览器存储、第三方脚本都视为高风险面
- 前端只负责展示和交互，不能承担最终授权边界
- 写新代码时优先避免危险 API，而不是事后再补丁式修复

## 生产安全基线

- 有条件时启用 CSP
- 第三方脚本最小化并可追踪
- 跨窗口消息必须校验来源
- 客户端不存放长期敏感凭证

## 核心规则

### JS-XSS-001：不要把不可信 HTML 注入 DOM

- 避免直接使用 `innerHTML`、`outerHTML`、`insertAdjacentHTML`
- 必须渲染富文本时，先经过可信的白名单清洗
- 默认优先使用 `textContent` 或安全模板能力

### JS-XSS-002：不要使用 `document.write`

- `document.write` 既容易造成 XSS，也容易破坏文档结构
- 新代码中默认禁止使用

### JS-XSS-003：禁止字符串转代码执行

- 不要使用 `eval`、`new Function`
- 不要把字符串传给 `setTimeout`、`setInterval`
- 动态代码执行应视为高危危险点

### JS-XSS-004：不要用字符串设置事件处理器

- 不要 `setAttribute("onclick", "...")`
- 统一使用函数绑定事件

### JS-URL-001：导航和跳转 URL 必须校验

- `window.location`、`location.replace`、动态跳转都要校验来源
- 默认只允许相对路径或白名单域名
- `javascript:`、`data:` 等协议默认禁止

### JS-URL-002：插入到 `href`、`src` 的 URL 必须清洗

- 图片、链接、iframe、脚本、媒体 URL 都要校验协议和域名
- 不可信 URL 不能直接进 DOM 属性

### JS-CSP-001：高风险页面应使用 CSP

- 如果页面需要展示富文本、引入第三方脚本或交互复杂，优先配 CSP
- 不要为了图方便大量依赖内联脚本和 `unsafe-eval`

### JS-TT-001：支持时优先使用 Trusted Types

- 如果项目本身有 CSP/Trusted Types 基础，可继续强化 DOM XSS 防护
- 不要无节制绕过 Trusted Types 限制

### JS-MSG-001：`postMessage` 必须校验来源

- 接收消息时校验 `origin`
- 发送消息时设置明确 `targetOrigin`
- 消息内容本身也要视为不可信

### JS-STORAGE-001：浏览器存储不是密钥保险箱

- `localStorage`、`sessionStorage`、IndexedDB 都可能被 XSS 读取
- 不要把长期访问令牌、私钥、敏感密钥放进 Web Storage

### JS-SUPPLY-001：第三方脚本是供应链风险

- 能少引就少引
- 引入前说明来源、用途和替换成本
- 标签管理器、统计脚本、聊天脚本都要视为高风险依赖

### JS-SRI-001：第三方静态资源优先启用 SRI

- 使用 CDN 脚本或样式时，优先使用 SRI 或改为自托管

### JS-DOMC-001：避免 DOM Clobbering

- 不要依赖 `window.xxx` 或 `document.xxx` 这种易被 DOM 命名污染的访问方式
- 查询元素统一使用显式选择器和局部作用域

## 审计重点

- 是否存在 `innerHTML`、`eval`、`document.write`
- 是否存在动态 URL 注入、未校验跳转、危险协议
- 是否存在 `postMessage("*")` 或不校验消息来源
- 是否把敏感令牌存进 Web Storage
- 是否引入过多第三方脚本且来源不可控
