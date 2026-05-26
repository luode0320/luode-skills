---
name: skill-hit-check-rules
description: 每轮用户新消息都必须先做命中检查并在首条中间进度输出。命中 git-collaboration-rules 时，必须同步输出可核验执行证据，缺失证据视为命中失败。
---

# Skill 命中检查规则（最小闭环版）

## 0. 首条消息格式（强制）
每轮第一条中间进度必须以以下模板开头：
- `templates/hit-check-template.md`

## 1. 最小流程
1. 判定命中 skill（基于用户本轮请求）
2. 先输出“Skill 命中检查”
3. 再进入主任务执行

## 2. Git 特殊闸门（强制）
若命中 `git-collaboration-rules`，则：
1. 首条中间进度必须追加“Skill 执行证据”三要素：
- 已读取 skill 文件路径
- 当前 git 盘点命令
- 下一步命令
2. 最终回复必须附“Skill 执行证据清单”最小集：
- `git status --short`
- `git diff --cached --stat`
- `scripts/pre_commit_gate.sh "<title>"`
- `git commit ...`
- `scripts/post_commit_gate.sh`
- `git log -1 --pretty=%B`
- `git log -1 --pretty=%s`
3. 缺任一项，判定为未完成，不得给“已完成”。

## 3. 通过标准
- 首条中间进度与最终回复都含“Skill 命中检查”
- Git 场景下证据最小集完整
- 无“只命中未执行”

## 4. 执行文件
- `templates/hit-check-template.md`
- （Git 场景）`../git-collaboration-rules/templates/evidence-template.md`
