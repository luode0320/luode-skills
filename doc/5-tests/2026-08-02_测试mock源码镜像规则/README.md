---
schema_version: 1
doc_id: "TEST-TEST-MOCK-MIRROR-001"
doc_type: test
source_ids: ["REQ-TEST-LAYOUT-20260801", "TASK-TEST-MOCK-MIRROR-01"]
status: accepted
version: "v1.0"
current_slice: "TASK-TEST-MOCK-MIRROR-01"
updated_at: "2026-08-02 23:33:30"
reader_level: business_general
writing_style: plain_chinese
appendix_policy: preserve_existing_or_one_terminal_appendix
---

# 测试 mock、stub、fake 源码镜像规则真实测试

结论：测试程序与源码关联的 mock、stub、fake、fixture、helper 均按被测源码相对路径落在根 `test/`；影响：模拟程序可与对应测试一起发现，`doc/5-tests/` 只保存说明和非可执行证据；范围：路径策略、正向源码镜像、错误路径拒绝和历史可执行资产只读保护；非范围：真实业务项目迁移、业务逻辑、外部服务和 Git 历史；变化：新增三类模拟程序的源码镜像校验与文档目录负向断言；术语说明：源码镜像是把模拟程序放在与被测源码相同的相对目录下；验证状态：治理专项 `13/13`、根 Python 测试 `216/216`、相关 Skill 校验和风格回归已通过；完成标准：治理专项与根 Python 测试通过，相关 Skill 校验、文档 profile 和差异检查通过。

## 文档信息

| 字段 | 内容 |
| --- | --- |
| 关联任务 | `TASK-TEST-MOCK-MIRROR-01` |
| 测试环境 | local 工作树、Windows Python、临时目录 |
| 可执行代码根 | `test/` |
| 证据根 | 当前目录，仅保存 README 和非可执行证据 |

## 测试矩阵

| TEST | 入口 | 样本/断言 | 失败预期 | 清理 |
| --- | --- | --- | --- | --- |
| `TEST-TEST-MOCK-MIRROR-001-A` | `test/test-asset-governance/asset_location_test.py` | mock/stub/fake 在 `test/` 且与源码相对路径镜像 | 任一源码关联模拟程序越界即失败 | `TemporaryDirectory` 自动清理 |
| `TEST-TEST-MOCK-MIRROR-001-B` | 同上 | `doc/5-tests/` 仅允许 README、日志、报告、截图等非可执行证据 | 在证据目录放置模拟程序即失败 | 不写历史资产 |

## 真实测试命令

```powershell
python -X utf8 -B -m unittest discover -s test/test-asset-governance -p "*_test.py" -v
python -X utf8 -B test/run_python_tests.py
python -X utf8 -B artifact-delivery-gate-rules/scripts/validate_engineering_docs.py --profile test --doc doc/5-tests/2026-08-02_测试mock源码镜像规则/README.md --root F:\luode-skills --strict
git diff --check
```

## 当前实测结果

| 项目 | 状态 | 证据 |
| --- | --- | --- |
| 治理专项 | `13/13` 通过 | `test/test-asset-governance/asset_location_test.py` |
| 根 Python 测试 | `216/216` 通过 | `test/run_python_tests.py` |
| 六个相关 Skill | 全部通过 | 各 Skill `quick_validate.py` |
| 历史 `doc/5-tests` 可执行资产 | 指纹校验通过 | `validate_legacy_manifest` 无错误 |

## 完成标准

- 治理专项和根 Python 测试全部通过，且 mock/stub/fake 正向镜像与错误路径拒绝断言均执行。
- 测试文档 profile、6-review 风格回归、Skill 校验和 `git diff --check` 均通过；失败时保持 `in_progress`，不得宣称规则收口。

## 测试边界

- 只读取本地规则仓库和临时目录，不连接数据库、缓存、消息队列、HTTP/RPC 上游或任何非 local 环境。
- 不在当前目录新增可执行测试、mock、stub、fake、fixture 或 helper；这些资产统一留在根 `test/` 并按源码路径镜像。
- 图片资产决策：N/A + 原因：本轮仅验证文本规则和路径契约 + 证据：测试矩阵与命令均为文本/路径断言。

## 追踪附录

`TASK-TEST-MOCK-MIRROR-01` -> `test/shared/layout_policy.py` / `test/test-asset-governance/asset_location_test.py` -> `TEST-TEST-MOCK-MIRROR-001-A..B` -> `13/13`、`216/216` -> `STYLE: PASS`。
