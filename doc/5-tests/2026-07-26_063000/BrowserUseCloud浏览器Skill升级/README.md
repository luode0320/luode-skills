---
schema_version: 1
doc_id: "TESTDOC-BU-001"
doc_type: "test"
source_ids:
  - "REQ-BU-20260726-001"
  - "CYCLE-BU-02"
  - "CYCLE-BU-03"
  - "CYCLE-BU-04"
  - "TASK-BU-04"
  - "TASK-BU-06"
  - "TASK-BU-09"
status: "accepted"
version: "v1.0"
current_slice: "TEST-BU-PREFLIGHT/ROUTE/SESSION/CONFIG"
updated_at: "2026-07-26 14:45:00"
reader_level: "business_general"
writing_style: "plain_chinese"
appendix_policy: "preserve_existing_or_one_terminal_appendix"
review_acceptance_gates:
  - stage: "functional_validation"
    applicability: "applicable"
    reason: "预检、账单失败关闭、硬费用上限和 session 清理均可用本机 mock 真实执行。"
    basis: "AC-BU-003..009、14 个标准库单元测试。"
    required_by_source: true
    required_now: true
    completed_validation:
      - "Browser Use Cloud 预检单元测试 14/14"
      - "Cloud 正负 trigger fixture 8/8"
      - "7 个相关 Skill quick_validate"
    substitute_validation: []
    manual_follow_up: "N/A。原因：本轮禁止调用真实 Cloud；证据：BOUND-BU-006。"
    pass_standard: "全部 local mock、路由和结构门禁通过，且没有真实 Cloud 请求。"
  - stage: "review"
    applicability: "applicable"
    reason: "本轮新增收费前安全 Owner、预检脚本和多 Skill 路由。"
    basis: "REVIEW-BU-001、REVIEW-BU-002。"
    required_by_source: true
    required_now: true
    completed_validation:
      - "实现审查无 P0/P1"
      - "当前改动总审查无 P0/P1"
    substitute_validation: []
    manual_follow_up: "N/A"
    pass_standard: "无泄密、无无确认收费入口、无竞争 Owner。"
  - stage: "browser_integration"
    applicability: "not_applicable"
    reason: "本轮只升级规则、预检和路由，不创建真实 Browser Use Cloud session。"
    basis: "用户冻结的最大推进边界明确禁止真实 Cloud 和额度消费。"
    required_by_source: false
    required_now: false
    completed_validation: []
    substitute_validation: []
    manual_follow_up: "N/A"
    pass_standard: "N/A"
  - stage: "third_party"
    applicability: "not_applicable"
    reason: "单元测试只访问 loopback mock，trigger 与 Skill 校验只读本地文件。"
    basis: "测试命令和 fixture 均不含真实账户、key、Cookie 或 Cloud endpoint 调用。"
    required_by_source: false
    required_now: false
    completed_validation: []
    substitute_validation: []
    manual_follow_up: "N/A"
    pass_standard: "N/A"
---

# Browser Use Cloud 浏览器 Skill 升级测试

结论：Browser Use Cloud 升级的本地行为与路由回归已通过；影响：缺 key、认证失败、账单异常、零余额、无硬费用上限和 session 未停止都不能进入“可确认”状态；范围：Cloud 预检、逐动作 schema、session 清理、正负路由和 Skill 结构；非范围：真实 Cloud、真实 key、真实代理和验证码效果；变化：新增 14 个 local mock 用例和 8 个 trigger fixture；完成标准：全部自动测试退出码为 0、无真实外联、输出不含哨兵凭据和身份字段；术语说明：哨兵凭据是只存在于测试进程中的假值，用于验证输出脱敏；验证状态：自动测试通过。图片资产决策：N/A；原因：本轮不交付视觉资产；证据：测试对象全部是脚本状态、路由文本和结构校验。

## 文档信息

| 项目 | 内容 |
|---|---|
| 来源对象 | `REQ-BU-20260726-001` |
| 测试轮次 | `2026-07-26_063000` |
| 自动测试 | 预检 14/14、trigger 8/8、Skill 校验 7/7 |
| 网络边界 | 只访问 `127.0.0.1` 随机端口 mock；不访问真实 Cloud |
| 图片资产决策 | N/A；原因：无视觉交付；证据：测试对象均为脚本状态、路由文本和结构校验 |

## 测试资产

- 预检测试：`browser-use-cloud-rules/tests/test_browser_use_cloud_preflight.py`。
- 被测脚本：`browser-use-cloud-rules/scripts/browser_use_cloud_preflight.py`。
- 路由 fixture：`doc/5-tests/2026-07-17_155229/skill-split-validation/cases/browser-use-cloud/trigger_cases.json`。
- trigger 验证器：`doc/5-tests/2026-07-17_155229/skill-split-validation/validate_skill_split.py`。
- 本 README 只保存测试结论；真实测试资产保持在冻结计划指定的 Skill 与既有 trigger 验证器目录，不复制第二份 fixture。

## 执行环境与命令

环境为 Windows 本地工作区和 Python 3；单元测试使用标准库 `ThreadingHTTPServer` 创建 loopback mock，测试结束后关闭端口和线程。没有读取真实 `BROWSER_USE_API_KEY`，没有创建 Cloud session。

```powershell
py.exe -3 -X utf8 -B -m unittest discover `
  -s browser-use-cloud-rules/tests `
  -p "test_*.py"

py.exe -3 -X utf8 -B doc/5-tests/2026-07-17_155229/skill-split-validation/validate_skill_split.py `
  --mode trigger `
  --root . `
  --cases doc/5-tests/2026-07-17_155229/skill-split-validation/cases/browser-use-cloud
```

## 覆盖与结果

| 测试组 | 覆盖 | 结果 |
|---|---|---|
| `TEST-BU-PREFLIGHT-001..010` | 缺 key、401/403、损坏账单、零余额、超时、硬上限、免费层和脱敏 | 14/14 PASS |
| `TEST-BU-CONFIRM-001..004` | `run_session` 与 `send_task` 独立 action/schema，禁止复用授权 | PASS |
| `TEST-BU-SESSION-001..003` | 活跃状态停止整个 session；仅 `stopped` 回读合法费用 | PASS |
| `TEST-BU-ROUTE-001..008` | 3 个 Cloud 正例与 5 个既有浏览器路由负例 | 8/8 PASS |
| `TEST-BU-CONFIG-001` | Cloud Skill、Agent 配置与相邻 Owner 结构 | 7/7 PASS |
| `TEST-BU-NET-001` | 测试仅 loopback，无真实收费 session | PASS |

## 关键断言

- 缺 key 固定提醒用户在本机配置并重启 Codex，且明确禁止在聊天中粘贴 key。
- 401、403、账户不存在、响应损坏、字段缺失和超时全部失败关闭。
- 只有当前动作 `inputSchema.properties.maxCostUsd` 为可写数值字段时才允许进入确认；输出 schema、描述、别名和只读字段均不能误放行。
- 免费层不等于永久免费，仍需费用预检与当次确认。
- `send_task` 不复用 `run_session` 的 schema 或授权结论。
- 活跃 session 固定生成 `stop_session(strategy="session")` 清理指令；仅最终 `stopped` 且费用合法时允许报告实际成本。
- 结果、异常和测试输出不含哨兵 key、姓名、项目 ID 或订阅 ID。
- Cloud 正例唯一命中 `browser-use-cloud-rules`；普通浏览、真实 Chrome、DevTools 和本地 browser session 保持既有 Owner。

## 完成标准

单元测试、trigger 回归、七个相关 Skill 校验全部退出码为 0；测试服务器全部回收；没有 `__pycache__`、真实 key、真实 Cloud 请求或收费 session；测试结论可回指验收标准、实施周期、审查和最终验收。

## 验收结论

本地功能与回归验证通过。真实 Browser Use Cloud 运行属于明确非范围，因此不以真实账户、代理地域、验证码完成率或费用账单作为本轮正式放行条件。

## 验证结论

`functional-validation-rules:PASS`、`test-regression-rules:PASS`、`test-program-rules:PASS`。测试不污染生产代码，不连接 test、staging 或 production 配置，也不创建真实 Cloud session。

## 追踪附录

`REQ-BU-20260726-001 -> AC-BU-001..012 -> CYCLE-BU-02/03/04 -> TASK-BU-04/06/09 -> TEST-BU-* -> TESTDOC-BU-001 -> REVIEW-BU-001/002 -> ACCEPT-BU-FINAL-001`。
