# 认证 URL 路由 skill 验证

## 测试目的

验证 `authenticated-url-routing-rules` 是否能覆盖用户提供 URL 时优先复用真实 Chrome 登录态的场景，并把执行中确认的异常处理方式沉淀回 skill。

## 测试对象

- `authenticated-url-routing-rules/SKILL.md`
- `authenticated-url-routing-rules/agents/openai.yaml`
- `skill-dictionary/data.js`
- `字典.md`
- `PROJECT_MEMORY.md`

## 真实测试资产入口

- 详细执行证据: `doc/5-tests/2026-07-02_114217/authenticated-url-routing-rules/evidence.md`

## 执行前置条件

- 当前环境可访问 Chrome Plugin 的 `chrome:control-chrome` 能力。
- 用户真实 Chrome 中已登录并打开目标微信文档链接。
- 本轮只执行只读验证，不提交表单、不修改网页内容、不导出敏感数据。

## 运行方式

- 结构校验: `python .system\skill-creator\scripts\quick_validate.py authenticated-url-routing-rules`
- 字典刷新: `python skill-dictionary\generate_dictionary.py`
- Chrome 只读验证: 通过 `chrome:control-chrome` 初始化、读取 `browser.documentation()`、命名 session、`openTabs()` 查找目标标签页、`claimTab()` 认领、读取 `tab.url()` 与 `tab.title()`，再尝试一次 `domSnapshot()` 检查正文可读性。

## 依赖数据与环境

- 执行环境: Windows PowerShell，设置 `PYTHONUTF8=1`。
- 浏览器环境: 用户真实 Chrome profile。
- 页面环境: 用户已登录的微信文档标签页。

## 覆盖范围

- 已覆盖 Chrome Plugin 优先路由。
- 已覆盖已打开标签页认领而非重复打开。
- 已覆盖 URL / 标题最低可访问性证据读取。
- 已覆盖正文读取被浏览器安全策略拒绝时的停手与 handoff 分支。
- 已覆盖 skill 结构校验与字典生成。

## 验证结论

- 通过: `authenticated-url-routing-rules` 结构校验通过。
- 通过: skill 字典生成成功，`implemented_total=80`、`planned_missing=0`、`seed_total=23`。
- 通过: Chrome Plugin 成功认领用户真实 Chrome 中的微信文档标签页，并读取到当前 URL 与页面标题。
- 通过: 正文读取被浏览器安全策略拒绝后，按 skill 规则停止绕过尝试，并将标签页保留为 `handoff`。
- 警告: 该微信文档正文未被 agent 读取，因此不能输出完整正文摘要或需求分析结论。

## 未覆盖项

- 未覆盖登录页 / 验证码 / 权限开通后的二次恢复流程，本轮页面已处于用户登录态。
- 未覆盖 `agent-browser --auto-connect` 回退链路，因为 Chrome Plugin 可用且已命中首选路径。
