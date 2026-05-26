Skill 命中检查：
- 命中 skill：
`<skill-a>`: <命中原因>
`<skill-b>`: <命中原因>

# 若命中 git-collaboration-rules，必须追加：
Skill 执行证据：
- 已读取 skill 文件：`git-collaboration-rules/SKILL.md`
- 当前盘点命令：`git status --short`、`git diff --cached --stat`
- 下一步命令：`scripts/pre_commit_gate.sh "<title>"`
