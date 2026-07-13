# Obsidian 执行失败持续学习验证

## 结论

本轮测试资产验证执行失败持续学习案例的正例、反例、脱敏、追加式状态事件、scope 精确检索、失败状态排除，以及 Obsidian bridge 失败时不写静态 casebook、不使用文件系统 fallback 的边界。

测试只使用 Python 标准库、内存 FakeBridge 和临时目录；不启动 Obsidian，不连接真实 vault，不读取或修改 `D:\\obsidian_data`。

## 测试落点与命名

- 中文主说明：`doc/5-tests/2026-07-14_015624/Obsidian执行失败持续学习验证/README.md`
- ASCII 真实测试：`doc/5-tests/2026-07-14_015624/obsidian-knowledge-flow/test_execution_learning_contract.py`
- 时间戳：`2026-07-14_015624`，由当前运行时生成。
- 真实动态案例目标：`知识库/20-Knowledge/execution-failure-cases/<owner-skill>/<case-id>.md`。
- 静态 owner casebook 仅作为种子和回归基线，测试不会写入任何 skill reference 文件。

## 覆盖矩阵

| 编号 | 场景 | 关键断言 |
| --- | --- | --- |
| `TEST-OBS-LEARN-01` | skill/reference 契约 | 存在失败特征、反例、正例、验证证据、状态事件和 bridge-only 规则 |
| `TEST-OBS-LEARN-02` | 正反例与脱敏 | secret 不进入正文；同一案例 create 后 append 状态事件并 readback 为 `active` |
| `TEST-OBS-LEARN-03` | scope 检索 | 只返回 scope 精确匹配且最终状态为 `active` 的案例 |
| `TEST-OBS-LEARN-04` | 路径与 UTF-8 JSON | 固定知识库前缀、路径越界拒绝、中文正文保持 UTF-8 |
| `TEST-OBS-LEARN-05` | doctor 失败 | 静态 casebook 不变；不调用 create；不得声称 candidate 已持久化 |
| `TEST-OBS-LEARN-06` | vault 失败状态 | `VAULT_NOT_REGISTERED` 与 `verified=false` 原样保留 |

## 执行命令

```powershell
python -m unittest discover -s doc/5-tests/2026-07-14_015624/obsidian-knowledge-flow -p "test_*.py" -v
```

通过标准：全部测试通过；失败样例必须稳定失败并保留结构化错误码；测试过程不得产生真实 vault 写入或静态 casebook 改动。

## 清理、回滚与停止条件

- 测试使用的临时目录由 `TemporaryDirectory` 或操作系统临时目录管理，不保留用户数据。
- 本轮仅新增本时间戳测试目录；回滚时删除该目录即可，不涉及生产代码、skill 主文件或 Obsidian vault。
- 若案例规范路径、状态事件或 bridge allowlist 契约发生冲突，停止测试并回到唯一 owner 与固定路径裁决，不以修改测试断言掩盖契约冲突。

## 证据

测试脚本在当前实现完成后执行，并将命令输出与通过数量补充到本 README；静态检查不替代以上行为测试。
