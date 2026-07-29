---
schema_version: 1
doc_id: "TEST-MBA-CRONTASK-001"
doc_type: "test"
source_ids: ["REQ-PSR-UTILS-TIMEUTIL-001"]
status: "accepted"
version: "v1.0"
current_slice: "scaffold crontask 改名回归"
updated_at: "2026-07-29 16:20:54"
template_version: 1
reader_level: business_general
writing_style: plain_chinese
appendix_policy: preserve_existing_or_one_terminal_appendix
review_acceptance_gates:
  - stage: functional_validation
    applicability: applicable
    reason: micro_business.py 的 scaffold 子命令此前完全没有测试覆盖，本次改名（corntask→crontask）必须有真实测试证明脚手架行为已同步。
    basis: AC-MBA-SCAFFOLD-001、AC-MBA-SCAFFOLD-002。
    required_by_source: true
    required_now: true
    completed_validation: ["TEST-MBA-CRONTASK-001"]
    substitute_validation: []
    manual_follow_up: "N/A；原因：本地单元测试已直接调用 CLI 并断言真实创建的目录结构；证据：2 项 unittest 结果。"
    pass_standard: 2 项测试全部通过。
  - stage: browser_integration
    applicability: not_applicable
    reason: 本测试没有浏览器页面或前端联调入口。
    basis: N/A。
    required_by_source: false
    required_now: false
    completed_validation: []
    substitute_validation: []
    manual_follow_up: N/A
    pass_standard: N/A
  - stage: third_party
    applicability: not_applicable
    reason: 本测试只使用本地 Python 和临时目录，不连接任何外部服务。
    basis: N/A。
    required_by_source: false
    required_now: false
    completed_validation: []
    substitute_validation: []
    manual_follow_up: N/A
    pass_standard: N/A
---

# 微业务脚手架 crontask 改名验证

结论：`micro-business-architecture-rules/scripts/micro_business.py` 的 `scaffold` 子命令此前把拼写错误的 `corntask` 写死为默认子目录之一，且完全没有自动化测试覆盖；本次改名为 `crontask` 后，新增的 2 项本地单元测试证明脚手架现在创建的是 `crontask/` 而不是历史拼写 `corntask/`，且二次执行保持幂等。影响：下游新建业务包时得到正确拼写的目录名，不再需要人工重命名。范围：`scaffold` 子命令的目录创建行为与幂等性。非范围：`check` 子命令的跨域隔离校验（未受本次改名影响，不在本测试覆盖范围）、真实业务项目里已存在的历史 `corntask/` 目录迁移。变化：新增本测试目录，`DEFAULT_SUBDIRS` 常量由 `corntask` 改为 `crontask`。完成标准：2 项 `unittest` 全部通过。术语说明：`scaffold` 是脚手架子命令，用于新建业务包骨架；幂等指重复执行不报错、不重复创建。验证状态：本地 Python 测试已执行通过。图片资产决策：N/A，原因：目录和 CLI 行为没有视觉验收对象。证据：所有结果由退出码和文件系统断言判断。

## 文档信息

| 项目 | 内容 |
|---|---|
| 测试任务 | `TEST-MBA-CRONTASK-001`。 |
| 真实测试资产 | `micro-business-architecture-rules/test_scaffold_crontask.py`。 |
| 执行环境 | 本机 Windows Python 3（标准库，无第三方依赖）、临时 fixture、`D:\luode\luode-skills` 规则仓库。 |
| 外部连接 | N/A；原因：测试不读取外部配置且不发起网络连接；证据：测试仅调用本地 CLI。 |

## 测试范围与样本

| 分类 | 样本 | 预期结果 |
|---|---|---|
| 正向创建 | `scaffold orders --root <tmp> --business-dir internal/business`。 | 业务包下存在 `crontask/`，不存在历史拼写 `corntask/`。 |
| 幂等性 | 同一业务包连续执行两次 `scaffold`。 | 两次均返回退出码 0，`crontask/` 只存在一份，不报错。 |

## 测试命令与断言

```bash
python -m unittest discover -s "doc/5-tests/2026-07-29_162054_微业务脚手架crontask改名验证/micro-business-architecture-rules" -p "test_*.py" -v
```

| 断言 ID | 断言 | 失败预期 | 实际结果 |
|---|---|---|---|
| `AC-MBA-SCAFFOLD-001` | `scaffold` 创建的业务包下存在 `crontask/`，不存在 `corntask/`。 | 目录名断言失败。 | 通过。 |
| `AC-MBA-SCAFFOLD-002` | 二次执行 `scaffold` 幂等，不报错、不重复创建。 | 第二次调用返回非 0 退出码。 | 通过。 |

## 验证结论

本轮执行 2 项 `unittest`，结果为 `OK`。`scaffold orders` 命令在临时目录下创建的业务包骨架包含 `crontask/`（历史拼写 `corntask/` 不再出现）；二次执行同一命令返回退出码 0 且不重复创建，证明改名后的幂等行为未受影响。

## 完成标准

1. 所有 2 项本地单元测试返回成功。
2. `scaffold` 创建的业务包目录树中包含 `crontask/`，不包含 `corntask/`。
