Skill 执行证据：
- 已读取 skill 文件：`git-collaboration-rules/SKILL.md`
- 当前盘点命令：`git status --short`、`git diff --cached --stat`
- 下一步命令：`scripts/pre_commit_gate.sh \"<title>\"`
- 脚本可用性：`pre=<已找到/缺失>`、`post=<已找到/缺失>`

Skill 执行证据清单：
- `git status --short`：<结果摘要>
- `git diff --cached --stat`：<结果摘要>
- `scripts/pre_commit_gate.sh "<title>"`：<通过/阻断 或 回退 + 摘要>
- `git commit ...`：<commit id + 标题>
- `scripts/post_commit_gate.sh`：<通过/阻断 或 回退 + 摘要>
- `git log -1 --pretty=%B`：<结果摘要>
- `git log -1 --pretty=%s`：<结果摘要>

固定校验行（强制）：
- `命中检查:通过`
- `Git规则:通过`
