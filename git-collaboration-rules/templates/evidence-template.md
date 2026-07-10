Skill 执行证据：
- 已读取 skill 文件：`git-collaboration-rules/SKILL.md`
- 当前盘点命令：`git status --short`、`git diff --cached --stat`
- 当前 staged 基础代码核查：`<已执行/未执行 + 覆盖范围 + 结论摘要；不依赖审查文档>`
- 下一步命令：`scripts/pre_commit_gate.sh \"<title>\"`
- 脚本可用性：`pre=<已找到/缺失>`、`post=<已找到/缺失>`

Skill 执行证据清单：
- `git status --short`：<结果摘要>
- `git diff --cached --stat`：<结果摘要>
- `git diff --cached --check`：<通过/阻断 + 摘要>
- 当前 staged 基础代码核查：
  - 格式：<通过/不适用 + 范围或项目格式化检查结果>
  - 注释：<通过/不适用 + 摘要>
  - 安全性：<通过/不适用 + 摘要>
  - 并发安全性：<通过/不适用 + 摘要>
  - 系统崩溃风险：<通过/不适用 + 摘要>
  - 边界条件：<通过/不适用 + 摘要>
  - 阻断项：<无 / P0/P1 或明确风险>
- `scripts/pre_commit_gate.sh "<title>"`：<通过/阻断 或 回退 + 摘要>
- `git commit ...`：<commit id + 标题>
- `scripts/post_commit_gate.sh`：<通过/阻断 或 回退 + 摘要>
- `git log -1 --pretty=%B`：<结果摘要>
- `git log -1 --pretty=%s`：<结果摘要>

固定校验行（强制）：
- `命中检查:通过`
- `Git规则:通过`
