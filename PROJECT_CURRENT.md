# 项目当前状态

## 当前任务

- 目标：升级 `obsidian-knowledge-flow`，将执行期间的非预期失败、异常、编码/JSON/命令问题转为可检索的脱敏正反例和持续状态事件。
- 范围：Obsidian 执行案例契约、`execution-failure-learning-rules` 的动态持久化边界、bridge-only 写入、离线契约测试和字典同步。
- 非范围：新建独立 skill、静态 casebook 动态追加、直接文件系统写 vault、Git 推送或历史改写。
- 状态：本地实现与离线验证完成；真实 vault 沉淀因未注册阻断。

## 已完成

- 执行案例唯一落点为 `知识库/20-Knowledge/execution-failure-cases/<owner>/<case>.md`，静态 casebook 仅作种子与回归基线。
- 案例契约保留失败特征、反例、正例、验证证据和追加式状态事件；只有 `active` 且 scope、工具主版本、输入指纹精确匹配时才自动复用。
- 受控 UTF-8 渲染器执行 local-only、脱敏、去重键、状态枚举和 `superseded` 终态校验。
- 离线执行案例契约测试 10 项通过，Python 编译、`git diff --check` 和 skill 字典生成通过。

## 阻断

- Obsidian 沉淀阻断：bridge doctor 返回 `VAULT_NOT_REGISTERED`，固定 vault `D:\obsidian_data` 未注册；未使用文件系统写入替代，未声称案例已持久化。

## 验证

- `python -m unittest discover -s doc/5-tests/2026-07-14_015624/obsidian-knowledge-flow -p "test_*.py" -v`：9 项通过。
- `python -m py_compile obsidian-knowledge-flow/scripts/render_execution_case.py`：通过。
- `git diff --check`：通过。
- `python skill-dictionary/generate_dictionary.py`：84 个已实现 skill，0 个缺失计划项。
- `python obsidian-knowledge-flow/scripts/obsidian_cli_bridge.py doctor --json`：阻断，`VAULT_NOT_REGISTERED`。

## 交接点

- 本地升级已收口。恢复真实沉淀时，从 bridge doctor 重新进入，再按 `search/read/create-or-append/readback` 顺序写入脱敏案例；不得直接写 vault 文件或静态 casebook。
