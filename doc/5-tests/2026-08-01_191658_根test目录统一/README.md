---
schema_version: 1
doc_id: "TEST-TEST-LAYOUT-20260801"
doc_type: test
source_ids: ["REQ-TEST-LAYOUT-20260801", "CYCLE-TEST-LAYOUT-01"]
status: accepted
version: "v1.1"
current_slice: "TASK-TEST-LAYOUT-05"
updated_at: "2026-08-01 20:30:00"
reader_level: business_general
writing_style: plain_chinese
appendix_policy: preserve_existing_or_one_terminal_appendix
---

# 根 test 目录统一真实测试

结论：本目录只记录根测试目录治理的测试说明和证据，不存放可执行测试代码；影响：代码和证据分别有唯一入口；范围：文档校验、位置校验、七组活动测试和全量入口；非范围：外部服务、数据库和历史包批量迁移；变化：后续可执行文件进入根 `test/`；完成标准：计划中的每个 `TEST` 实际运行通过并关联 `STYLE`；术语说明：真实测试是实际运行测试程序并检查断言，不是格式检查；验证状态：全量 Python `187/187`、测试资产治理 `9/9`、七类严格文档 profile、字典生成和差异检查均已通过。

## 文档信息

| 字段 | 内容 |
| --- | --- |
| 关联需求 | `REQ-TEST-LAYOUT-20260801` |
| 关联周期 | `CYCLE-TEST-LAYOUT-01..03` |
| 测试环境 | local 工作树、Windows Python、临时目录和临时 Go 模块 |
| 可执行代码根 | `test/` |
| 证据根 | 当前目录的 `evidence/` 与 `artifacts/` |

## 测试矩阵

| TEST | 入口 | 完成条件 | 样本/断言 | 失败预期 | 清理 |
| --- | --- | --- | --- | --- | --- |
| `TEST-TEST-LAYOUT-01` | 严格文档 profile | `AC-TEST-LAYOUT-001` | 本轮需求、总览、周期和 README 合法 | 任一 profile 非零 | 无外部状态 |
| `TEST-TEST-LAYOUT-02` | `test/test-asset-governance` | `AC-TEST-LAYOUT-002..004` | 正确镜像通过；错误目录、错误命名、源码 Go 测试和历史篡改失败 | 断言失败 | 临时目录自动清理 |
| `TEST-TEST-LAYOUT-03` | 七个根测试目录 | `AC-TEST-LAYOUT-005` | 每组迁移后断言等价通过 | 任一组非零 | `-B` 不生成字节码 |
| `TEST-TEST-LAYOUT-04` | `test/run_python_tests.py` | 全量活动入口 | 递归发现根 `test/`，不扫描 `doc/5-tests/` | 历史目录被扫描即失败 | 临时目录自动清理 |
| `TEST-TEST-LAYOUT-05` | 字典、路径扫描、差异检查 | 规则和索引一致 | 活动旧路径为零、无格式错误 | 任一命令非零 | 无外部状态 |

## 完成标准

- 每个 `AC-TEST-LAYOUT-*` 都由对应 `TEST-TEST-LAYOUT-*` 的实际断言覆盖。
- 仅在真实测试通过后编写 `doc/6-review/` 的 `STYLE: PASS` 或 `STYLE: FIX_REQUIRED`。
- N/A + 原因 + 证据：本任务不连接数据库、缓存、消息队列、HTTP/RPC 上游或外部服务；证据为全部命令只读本地工作树或临时目录。

## 真实测试命令

```powershell
python -X utf8 -B artifact-delivery-gate-rules/scripts/validate_engineering_docs.py --profile requirement --doc doc/2-需求/2026-08-01_191658_根test目录统一.md --root F:\luode-skills --strict
python -X utf8 -B artifact-delivery-gate-rules/scripts/validate_engineering_docs.py --profile implementation_overview --doc doc/3-实施/2026-08-01_191658_根test目录统一_实施总览.md --root F:\luode-skills --strict
python -X utf8 -B artifact-delivery-gate-rules/scripts/validate_engineering_docs.py --profile implementation_cycle --doc doc/3-实施/2026-08-01_191658_根test目录统一_实施周期01_测试资产契约.md --root F:\luode-skills --strict
python -X utf8 -B artifact-delivery-gate-rules/scripts/validate_engineering_docs.py --profile implementation_cycle --doc doc/3-实施/2026-08-01_191658_根test目录统一_实施周期02_活动测试迁移.md --root F:\luode-skills --strict
python -X utf8 -B artifact-delivery-gate-rules/scripts/validate_engineering_docs.py --profile implementation_cycle --doc doc/3-实施/2026-08-01_191658_根test目录统一_实施周期03_消费者同步与全链路回归.md --root F:\luode-skills --strict
python -X utf8 -B artifact-delivery-gate-rules/scripts/validate_engineering_docs.py --profile test --doc doc/5-tests/2026-08-01_191658_根test目录统一/README.md --root F:\luode-skills --strict
python -X utf8 -B artifact-delivery-gate-rules/scripts/validate_engineering_docs.py --profile style_regression --doc doc/6-review/2026-08-01_191658_根test目录统一_6-review.md --root F:\luode-skills --strict
python -X utf8 -B -m unittest discover -s test/test-asset-governance -p "*_test.py" -v
python -X utf8 -B test/run_python_tests.py
python -X utf8 -B skill-dictionary/generate_dictionary.py
git diff --check
git diff --cached --check
```

## 测试边界

- `doc/5-tests/` 的既有可执行文件只由历史指纹清单读取；本轮不移动、不改写。
- 所有运行使用 local 工作树与临时目录；任何非 local 配置或外部服务均不在测试范围内。
- `6-review` 不验证业务正确性、需求覆盖或发布放行，只验证本轮改动的写法、位置、格式和可读性。
- 图片资产决策：N/A + 原因：无界面或视觉产物需要验证 + 证据：测试对象是路径、脚本和文本资产。

## 本轮实测结果

| TEST | 状态 | 证据 |
| --- | --- | --- |
| `TEST-TEST-LAYOUT-01` | requirement、implementation_overview、implementation_cycle、test 四个 profile 均通过 | `EVD-TASK-TEST-LAYOUT-01-TEST-01` |
| `TEST-TEST-LAYOUT-02` | 治理测试 `9/9` 通过，覆盖镜像、命名、历史指纹和临时 Go 黑盒编译 | `EVD-TASK-TEST-LAYOUT-02-TEST-01` |
| `TEST-TEST-LAYOUT-03` | 七组迁移测试均从根 `test/` 运行通过 | `EVD-TASK-TEST-LAYOUT-03-TEST-01` |
| `TEST-TEST-LAYOUT-04` | 统一 Python 发现入口只扫描根 `test/`，全量 `187/187` 通过 | `EVD-TASK-TEST-LAYOUT-04-TEST-01` |
| `TEST-TEST-LAYOUT-05` | 字典生成、活动路径扫描、七个严格 profile、旧 Go 阻断表达扫描与差异检查通过 | `EVD-TASK-TEST-LAYOUT-05-TEST-01` |

实现证据：`EVD-TASK-TEST-LAYOUT-01-IMPL-01`、`EVD-TASK-TEST-LAYOUT-02-IMPL-01`、`EVD-TASK-TEST-LAYOUT-03-IMPL-01`、`EVD-TASK-TEST-LAYOUT-04-IMPL-01`、`EVD-TASK-TEST-LAYOUT-05-IMPL-01`。

## 执行附录

每次执行后将脱敏日志和报告写入本目录 `evidence/` 或 `artifacts/`；禁止在本目录新增 `.py`、`.go`、`.ps1`、`.js` 或可执行 fixture。

## 追踪附录

| AC | TASK | TEST | 预期证据 |
| --- | --- | --- | --- |
| `AC-TEST-LAYOUT-001` | `TASK-TEST-LAYOUT-01` | `TEST-TEST-LAYOUT-01` | `EVD-TASK-TEST-LAYOUT-01-TEST-01` |
| `AC-TEST-LAYOUT-002..004` | `TASK-TEST-LAYOUT-02` | `TEST-TEST-LAYOUT-02` | `EVD-TASK-TEST-LAYOUT-02-TEST-01` |
| `AC-TEST-LAYOUT-005` | `TASK-TEST-LAYOUT-03` | `TEST-TEST-LAYOUT-03` | `EVD-TASK-TEST-LAYOUT-03-TEST-01` |
| `AC-TEST-LAYOUT-001..005` | `TASK-TEST-LAYOUT-04..05` | `TEST-TEST-LAYOUT-04..05` | `EVD-TASK-TEST-LAYOUT-04..05-TEST-01` |
