# Pre/Post Gate 与回退

现有脚本始终归 `git-collaboration-rules` 所有，不迁移、不复制。

### 查找优先级

1. 本 Skill 的 `scripts/pre_commit_gate.sh`、`scripts/post_commit_gate.sh`。
2. 仓库根目录的 `scripts/pre_commit_gate.sh`、`scripts/post_commit_gate.sh`。
3. 两处均不存在或不可执行时，执行完整等价回退并在证据中标注“回退”。

不得仅因仓库根目录缺少脚本判定阻断；本 Skill 自带脚本可用时直接使用。

### Pre gate

优先运行 `scripts/pre_commit_gate.sh "<title>"`。脚本或等价回退至少检查：

- 标题匹配 `<type>: [中文简要说明] 标题说明`。
- README 改动日志末行剥除时间戳后等于标题。
- 六类流程产物域不混提。
- staged 不同时包含实现/运行配置与流程产物或测试文件。
- 本次新增或修改的 Go 测试不位于 `doc/5-tests/` 外；未纳入本次提交的历史文件不阻断。
- staged 不命中 `internal/service/[^/]+.go`。
- `git diff --cached --check` 通过。

机械 gate 不替代 staged 基础代码核查与基础验收。

### Post gate

提交后优先运行 `scripts/post_commit_gate.sh`。脚本缺失时至少检查 `git log -1 --pretty=%B` 不包含字面量 `\n`。失败时修正当前提交并重新验证，不得忽略失败继续下一次提交。

### 回退完整性

缺少任一等价检查、未标注回退或结果不满足成功标准，均视为门禁未完成，不得宣称提交闭环通过。
