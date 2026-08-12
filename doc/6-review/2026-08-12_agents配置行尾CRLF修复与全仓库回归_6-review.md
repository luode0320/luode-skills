---
schema_version: 1
doc_id: "STYLE-AGENTS-EOL-LF-001"
doc_type: "style_regression"
source_ids: ["TASK-EOL-LF-01", "TASK-EOL-LF-02"]
status: accepted
version: "v1.0"
current_slice: "8 份 agents 配置行尾还原 + 全仓库行尾与控制字符常驻回归"
updated_at: "2026-08-12"
template_version: "style-regression-v1"
reader_level: business_general
writing_style: plain_chinese
appendix_policy: preserve_existing_or_one_terminal_appendix
---

# agents 配置行尾 CRLF 修复与全仓库回归 6-review 风格回归

结论：本次风格回归为通过，过程中发现并已在本轮修正一处注释格式偏差。影响：确认 8 份配置文件只被还原了行尾、内容语义一字未动，新增的检查程序在命名、位置、注释和编码上都跟随了仓库既有写法，可以交给用户决定是否提交。范围：8 份技能智能体配置文件的行尾还原，以及一个新增的检查程序。非范围：业务正确性判断、发布放行、`doc/` 历史归档目录下的文件，以及仓库中原本就存在的 4 个测试失败。变化：8 份配置从 CRLF 行尾还原为 LF；新增 4 条常驻检查，把原本只覆盖单个技能目录的行尾与控制字符检查扩大到全仓库。完成标准：8 份文件的 CRLF 计数归零、全部能被 YAML 解析器解析为映射、无异常控制字符，新增检查程序在注入故障时确会报错、清理后恢复通过，且不影响仓库既有测试的通过情况。术语说明：CRLF 与 LF 是两种行尾写法，仓库规定这批文件只能用 LF，用错会让脚本在 Linux 环境下执行失败；控制字符指不可打印的低位字符，混入配置会让解析直接报错。验证状态：已通过。

## 文档信息

| 项 | 内容 |
| --- | --- |
| 来源对象 | 用户直接指派的行尾违规修复任务 |
| 实施总览 | N/A + 原因：单点修复任务，未走实施总览 + 证据：本轮无 `doc/3-实施/` 新增文档 |
| 覆盖周期 | N/A + 原因：无周期拆分 + 证据：同上 |
| 关联最小任务 | `TASK-EOL-LF-01` 行尾还原、`TASK-EOL-LF-02` 常驻回归扩面 |
| 关联真实测试 | `TEST-EOL-LF-001` 至 `TEST-EOL-LF-004` |
| 执行时点 | 真实测试完成之后，本轮仅执行一次 |
| 风格结论 | 通过，无 P0；1 个 P1 已在本轮修正 |

## 图片资产决策

图片资产决策：N/A + 原因：本次回归只检查文本文件的格式、注释、命名与位置，不涉及界面或截图 + 证据：`doc/data/images/` 下无本任务图片引用。

## 检查范围

| 文件 | 改动性质 |
| --- | --- |
| `.system/imagegen/agents/openai.yaml` | 仅行尾还原 |
| `.system/plugin-creator/agents/openai.yaml` | 仅行尾还原 |
| `.system/review-agent/agents/openai.yaml` | 仅行尾还原 |
| `.system/skill-creator/agents/openai.yaml` | 仅行尾还原 |
| `.system/skill-installer/agents/openai.yaml` | 仅行尾还原 |
| `authenticated-url-routing-rules/agents/openai.yaml` | 仅行尾还原 |
| `code-snippet-location-rules/agents/openai.yaml` | 仅行尾还原 |
| `windows-encoding-rules/agents/openai.yaml` | 仅行尾还原 |
| `test/shared/asset_eol_health_test.py` | 新增检查程序 |

## 范围外说明

以下内容明确不在本次判断范围：业务正确性、需求覆盖度、发布放行结论、最终验收结论，以及历史归档目录与本轮未改动的文件。仓库中原本就存在的 4 个测试失败与本轮无关，已用移除本轮新增文件后复跑的方式确认，本次不修复也不作结论。

## 真实测试前置证据

| 测试 | 结果 |
| --- | --- |
| `TEST-EOL-LF-001` LF 强制文件无 CRLF | PASS，扫描全仓库 `.sh` / `.bash` / `.yaml` / `.yml` |
| `TEST-EOL-LF-002` 扫描范围非空 | PASS，防止排除规则写错后检查静默通过 |
| `TEST-EOL-LF-003` agents 配置可解析 | PASS，全部解析为映射 |
| `TEST-EOL-LF-004` agents 配置无控制字符 | PASS，扫描结果为空 |
| `EVIDENCE-EOL-LF-001` 故障注入负向验证 | 注入含 CRLF 的探针文件后检查确会报错并准确指名，清理后恢复通过 |
| `EVIDENCE-EOL-LF-002` 内容未变反证 | 6 份纳入版本管理的文件比对输出为空，证明只改行尾 |
| `EVIDENCE-EOL-LF-003` 既有失败无关性 | 移除本轮新增文件后复跑，4 个失败文件的失败数与移除前完全一致 |

## 检查清单

| 检查项 | 结论 | 依据 |
| --- | --- | --- |
| 编码与尾随空白 | 通过 | 新增文件为 UTF-8、无字节序标记，尾随空白零行，结尾保留换行 |
| 行尾策略 | 通过 | 8 份配置的 CRLF 计数全部归零，孤立回车计数为零 |
| 控制字符 | 通过 | 8 份配置扫描结果为空，未复现历史上的响铃字符问题 |
| 内容语义未变 | 通过 | 版本管理侧比对输出为空，改动完全落在行尾 |
| 函数注释三段式 | 通过（补齐后） | 首查时注释头未跟随同目录写法，7 处已统一 |
| 步骤编号注释 | 通过（补齐后） | 按同目录习惯给唯一的多步骤方法补编号，单步骤方法保持不加 |
| 测试文件命名 | 通过 | 沿用仓库统一的 `_test.py` 结尾，未使用被策略禁止的前缀写法 |
| 测试资产归位 | 通过 | 落在专用于跨领域检查的共享测试目录，属落点策略的特例目录 |
| 公共实现复用 | 通过 | 同目录既有落点策略程序职责不同，无可复用能力，也未反向依赖 |
| 依赖引入 | 通过 | 只依赖标准库与仓库已在用的 YAML 解析库，未引入新依赖 |
| 改动范围最小化 | 通过 | 未批量格式化、未重排无关代码、未改动其它技能资产 |
| 临时文件残留 | 通过 | 一次性修复脚本写在仓库外临时目录并已删除，故障探针已确认清理 |
| 局部风格跳变 | 通过 | 未引入外部模板式写法或个人偏好风格 |

## 问题与修复

| 优先级 | 位置 | 问题 | 处理 |
| --- | --- | --- | --- |
| P1 | 新增检查程序的 7 处函数注释头 | 沿用了另一个目录下同主题程序的写法（半角冒号、不写改动原因），与同目录既有程序不一致 | 按"同目录优先"改为全角冒号并显式写出改动原因，复跑测试仍通过 |
| P2 | 新增检查程序的多步骤方法 | 缺少同目录习惯的步骤编号注释 | 给唯一的多步骤方法补上编号，单步骤方法维持不加，与同目录既有做法一致 |

## 范围外发现

`doc/5-tests/` 下仍有 3 份 CRLF 的 yaml（`2026-07-17_155229/skill-split-validation/mapping/candidate-matrix.yaml`、`release-test-plan-example.yaml`、`基线/interface-inventory-example.yaml`）。该目录是只读历史归档，且其中测试证据的字节内容已被指纹基线锁定，改写会破坏基线，因此新增检查程序把 `doc` 列入排除目录，本轮不做处理，留给用户决定是否单独立项。

## 6-review 结论

`STYLE: PASS`

1 个 P1 与 1 个 P2 均已在本轮修正并复跑通过，无遗留项；本轮改动跟随仓库既有写法，未引入局部风格跳变、临时文件残留或路径漂移。

## 执行附录

### 检测与验证命令

```bash
python -X utf8 test/shared/asset_eol_health_test.py
```

### 关键证据

- 行尾还原：8 份文件 `read_bytes().count(b"\x0d\x0a")` 由 6/6/6/5/5/3/4/4 全部归零，残留孤立 `\x0d` 计数为 0。
- 内容未变：6 份已跟踪文件 `git diff --numstat` 输出为空；`.system/imagegen/` 与 `.system/review-agent/` 被 `.gitignore` 忽略、不进版本库，故无对应比对输出。
- 可解析性：8 份文件 `yaml.safe_load` 全部返回 `dict`，顶层键为 `interface`（`review-agent` 另含 `policy`）。
- 控制字符：8 份文件按 `ord(ch) < 32 and ch not in "\n\t"` 扫描结果为空，未复现历史上的 `\x07`（BEL）问题。
- 负向验证：注入 `test/shared/__crlf_probe.yaml`（含 2 处 CRLF）后测试 `FAILED (failures=1)` 并准确报出该文件，清理后恢复 `OK`，排除空跑假绿。
- 既有失败无关性：移除本轮新增测试后复跑 4 个失败文件，失败数为 1+1 / 8 / 5 / 2，与移除前完全一致。
- 落点合规依据：`test/shared/layout_policy.py` 的 `SPECIAL_TEST_DIRECTORIES` 把 `shared` 列为特例目录，不要求镜像被测源码目录。
