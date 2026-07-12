# 周期 03 实施规划与执行卡验证

## 验证目的

验证 `CYCLE-03` 的三个最小任务能被一般模型按固定字段执行，并证明输出 gate 会拒绝缺文件/符号、缺真实测试、模糊动作、P0/P1 未决、预计超过 5 个文件、孤立 EVD 和 Mermaid 图无前置说明的样例。

## 资产位置

- 实施周期文档：`doc/3-实施/2026-07-12_033322_需求与实施文档极致完备化_实施周期03_执行卡与输出门禁.md`
- ASCII 测试脚本：`doc/5-tests/2026-07-12_042731/implementation_planning_cycle03/test_cycle03_contract.py`
- 本说明目录只保存本 README；可执行脚本放在同级 ASCII 镜像目录。

## local 执行命令

在仓库根目录运行：

```powershell
python -X utf8 doc/5-tests/2026-07-12_042731/implementation_planning_cycle03/test_cycle03_contract.py
python -X utf8 doc/5-tests/2026-07-12_042731/implementation_planning_cycle03/test_cycle03_contract.py -k decision
python -X utf8 doc/5-tests/2026-07-12_042731/implementation_planning_cycle03/test_cycle03_contract.py -k low_reasoning
python -X utf8 doc/5-tests/2026-07-12_042731/implementation_planning_cycle03/test_cycle03_contract.py -k negative
python -X utf8 artifact-delivery-gate-rules/scripts/validate_engineering_docs.py --profile implementation_cycle --doc "doc/3-实施/2026-07-12_033322_需求与实施文档极致完备化_实施周期03_执行卡与输出门禁.md" --root .
git diff --check
```

这些命令只读取 local 仓库和本地 Python，不连接数据库、缓存、消息队列、HTTP/RPC、test 或 production 环境。构建、lint 或人工阅读不能替代脚本断言。

## 样本与断言

| 样本 | 预期 |
| --- | --- |
| 周期03完整文档 | 通过身份、任务字段、两张 Mermaid 图和追踪检查 |
| 决策日志 `DEC-03-001` 正例 | 有 `SRC`、选项、理由、影响、回滚和 EVD，测试通过 |
| 缺文件/符号或缺真实测试入口 | 报告缺失字段并失败 |
| 模糊动作、P0/P1 未决 | 失败，不猜测默认值 |
| 预计触达 6 个文件 | 失败，超过单任务五文件边界 |
| 缺 REVIEW EVD | 失败，拒绝孤立任务追踪 |
| Mermaid 删除图形目的 | 失败，拒绝无前置说明的图 |

## 失败预期、清理与回滚

每个负例都在内存中构造，不写入业务代码、数据库或外部服务；测试失败时保留终端输出作为 `EVD-T03-03-TEST-01` 的失败证据。修复只允许触碰当前任务写集，先回读 UTF-8 和 `git diff`，再重跑当前任务；不得用 Git 历史写入清理。

## 证据记录

- `EVD-T03-01-TEST-01`：决策日志正/反样例。
- `EVD-T03-02-TEST-01`：低推理任务契约和 `unresolved_decisions` P0/P1=0 断言。
- `EVD-T03-03-TEST-01`：六类任务负例和 Mermaid 前置说明负例。
- `EVD-C03-CLOSE-TEST-01`：实施周期 profile、UTF-8、链接和 Mermaid 前置语法检查。
- Mermaid CLI 当前不可用；本验证只执行无浏览器语法前置检查，不能作为真实渲染解析证据。
