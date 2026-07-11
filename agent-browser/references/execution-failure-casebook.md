# Agent Browser 执行失败案例库

本文件保存 `agent-browser` 的可复用失败恢复经验；截图、HAR、认证状态、私有 URL 和业务数据只作为临时证据，不得写入案例正文。

## 统一维护规则

- 状态使用 `candidate`、`active`、`stale`、`superseded`、`rejected`。
- 执行前按 session、snapshot 生命周期、命令阶段和 shell 环境预检 active 案例；失败后先查库，再有限重试。
- 新案例必须同输入、同页面成功标准复验；无法脱敏或无法确定根因时拒绝写入。

## BROWSER-001

- 状态：`active`
- 类型：引用生命周期
- 错误特征：snapshot 生成后 DOM 变化导致 ref 无效或点击目标不存在
- 根因：snapshot ref 只在当前页面状态有效，导航或重渲染后旧 ref 失效
- 解决方案：重新 snapshot，重新定位目标，再执行交互；不得重复使用旧 ref
- 验证：目标动作在新 snapshot 上完成且 URL/页面状态符合原成功标准
- 来源：`agent-browser/references/snapshot-refs.md`、`browser-operation-lessons.md`
- 最后验证：2026-07-12

## BROWSER-002

- 状态：`active`
- 类型：命令解析
- 错误特征：`eval` 遇到嵌套引号、箭头函数、模板字符串或多行代码后脚本被 shell 改写
- 根因：shell 在命令到达浏览器运行时前处理了引号、反引号或 `$()`
- 解决方案：多行或嵌套脚本改用 `eval --stdin`；程序生成脚本使用 `eval -b`
- 验证：脚本完整到达浏览器运行时并得到可解析输出
- 来源：`agent-browser/SKILL.md` 实战经验优先流程
- 最后验证：2026-07-12

## BROWSER-003

- 状态：`active`
- 类型：会话恢复
- 错误特征：临时 auto-connect 无法恢复登录态或并行 session 状态
- 根因：未使用可持久化 session 或 state 文件
- 解决方案：优先 `--session-name`，其次 `--state`，最后才使用 `--auto-connect`
- 验证：重新打开目标页面后会话状态和页面成功标准保持一致
- 来源：`agent-browser/SKILL.md` 会话复用优先级
- 最后验证：2026-07-12
