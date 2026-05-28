命中检查:<通过/阻断>; Git规则:<通过/不适用/阻断>
命中技能:<skill1,skill2,...>
Git联动:<是/否>
前置自检:就绪

Skill 命中检查：
- 命中 skill：
`<skill-a>`: <命中原因>
`<skill-b>`: <命中原因>
- 闸门状态：`<通过/阻断>`

# 若命中 git-collaboration-rules，必须追加：
Skill 执行证据：
- 已读取 skill 文件：`git-collaboration-rules/SKILL.md`
- 当前盘点命令：`git status --short`、`git diff --cached --stat`
- 下一步命令：`scripts/pre_commit_gate.sh "<title>"`
- 脚本可用性：`pre=<已找到/缺失>`、`post=<已找到/缺失>`

# 若发生违规顺序（先执行命令后命中检查），必须追加：
自恢复:需要重启
