# 项目当前状态

## 目标与范围

- 目标：收敛浏览器工具路由，明确 Chrome Plugin、Chrome DevTools MCP 与 `agent-browser` 的职责边界。
- 范围：浏览器路由源头、认证 URL、功能验证、测试策略、团队路由、项目入口文档、项目记忆与 skill 字典。
- 非范围：删除 `agent-browser` skill、修改用户 MCP 配置、安装工具、访问真实网页或 Git 提交/推送。

## 当前状态

- 状态：已完成，提交已完成，未推送远端。
- 当前执行点：浏览器工具路由改造、残留硬绑定审计、字典刷新和 skill 校验已收口。
- 更新时间：2026-07-12

## 已完成

- 已将用户真实 Chrome profile、登录态、标签页和扩展统一路由到 Chrome Plugin。
- 已将常规 DOM、控制台、Network、Performance 与页面验证路由到 Chrome DevTools MCP（能力满足时）。
- 已保留 `agent-browser`，仅用于隔离 profile/session、HAR/route、视觉 diff、录制/trace、代理、多引擎及明确要求的高级自动化。
- 已移除前后端联调必须使用 `agent-browser` 的硬绑定，保留 local、授权、服务可达、真实用户路径、证据和进程收口要求。
- 已同步 `agent-browser`、`authenticated-url-routing-rules`、`mcp-installation-rules`、功能验证、测试策略、团队路由及入口文档。
- 已刷新 `skill-dictionary/data.js` 与 `字典.md`。

## 待办

- 无。

## 阻断

- 无。

## 验证

- `quick_validate.py`：5 个受影响 skill 通过（`agent-browser`、`authenticated-url-routing-rules`、`mcp-installation-rules`、`functional-validation-rules`、`test-strategy-rules`）。
- 字典生成器：`implemented_total=83`、`planned_missing=0`。
- `git diff --check`：通过；关键改动文件保持 UTF-8 内容。
- 残留硬绑定搜索：未发现“联调必须使用 `agent-browser`”或旧线性优先级文案。
- 路由场景静态核对：真实 profile -> Chrome Plugin；常规调试 -> Chrome DevTools MCP；隔离/高级能力 -> `agent-browser`；无可用等价工具 -> 阻断。

## 下一执行点

- 本轮任务已完成；提交已完成，未推送远端，当前工作树应保持清洁。
