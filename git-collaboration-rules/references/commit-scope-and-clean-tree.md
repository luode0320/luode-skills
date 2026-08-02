# 提交域与工作树清空

本文件定义提交拆分和“提交git”场景的完成目标。

### 提交域隔离

- 同一任务的流程文档统一归入 `docs` 提交域，包含 `doc/2-需求/`、`doc/3-实施/`、`doc/4-bugs/`、`doc/5-tests/`、`doc/6-review/`、`doc/7-验收/` 以及项目状态同步文件。
- 项目状态同步文件至少包括 `PROJECT_CURRENT.md`、`PROJECT_MEMORY.md`、`PROJECT_HISTORY.md`、`PROJECT_STYLE.md`、`编码skill.md`、`字典.md`、`skill-dictionary/data.js`；它们默认跟随同一任务的 `docs` 提交，不再额外拆 `chore`。
- 可执行测试文件至少包括根 `test/**`、`*_test.*`、`*.spec.*`、`*.test.*`，归入 `test` 提交，不与代码实现或 `docs` 提交混提；`doc/5-tests/**` 只保存测试说明、日志、报告、截图和非可执行证据，归入 `docs` 提交。
- 代码实现和运行配置作为实现域，不与 `docs` 域或 `test` 域混提。
- 每次暂存前先冻结当前 commit 的文件清单；发现 `docs`、`test`、实现域跨域时拆分，不为追求一次提交强行混提。

### 清空目标

用户当前轮明确要求“提交git”时，目标是清空 staged、unstaged 和 untracked 改动。允许按业务域创建多个 commit，逐次执行盘点、核查、pre gate、commit 和 post gate，直到 `git status --short` 为空。

若存在未获放行的用户改动、门禁失败、冲突或其它明确阻断，停止循环并报告剩余文件与原因；不得把“部分提交成功”描述为工作树已清空。

### README 与标题

- 每个 commit 标题使用 `<type>: [中文简要说明] 标题说明`。
- 根目录 `README.md` 在改动日志最后一条后追加 `<yyyy-MM-dd HH:mm:ss> <提交标题>`，时间戳使用当前北京时间。
- README 日志属于当前 commit 的门禁输入，必须与该次标题匹配。
