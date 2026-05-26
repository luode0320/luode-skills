---
name: git-collaboration-rules
description: 当出现 git/commit/提交/push/pull/status/diff/log 等协作动作时触发。默认执行“最小可执行闭环”：短清单 + 阻断脚本 + 统一证据模板。用户明确请求“提交git”时，目标是清空当前全部未提交改动（staged、unstaged、untracked），允许按业务拆分多次提交，但必须循环到 `git status --short` 为空（除阻断项外）。
---

# Git 协作规则（最小闭环版）

## -1. 触发确认（强制）
当用户请求包含 `git/commit/提交/push/pull/status/diff/log` 任一关键词时，必须命中本 skill；未命中不得执行 git 命令。

## 0. 首条中间进度（强制）
必须先输出并填写模板：
- `templates/evidence-template.md` 中的 **Skill 执行证据** 区块。

## 1. 执行短清单（强制按顺序）
1. 盘点：`git status --short`、`git diff --cached --stat`
2. 业务拆分：能拆分就拆分为多次提交
3. 写 README 日志：根目录 `README.md` 增加 `yyyy-MM-DD HH:mm:ss <提交标题>`
4. 设定标题：`<type>: [中文简要说明] 标题说明`
5. 提交前闸门：优先执行 `scripts/pre_commit_gate.sh "<title>"`，失败即阻断
6. 执行提交：`git commit`（正文必须真实换行，禁止字面量 `\\n`）
7. 提交后闸门：优先执行 `scripts/post_commit_gate.sh`，失败即 `git commit --amend` 修正
8. 若用户请求“提交git”：重复 1-7，直到 `git status --short` 为空

## 1.1 脚本缺失回退（强制）
若仓库不存在 `scripts/pre_commit_gate.sh` 或 `scripts/post_commit_gate.sh`，必须执行等价回退检查，且在最终证据中标注 `FALLBACK`：

- pre 回退检查：
  - 标题匹配 `<type>: [中文简要说明] 标题说明`
  - `README.md` 包含本次提交标题
  - Go 项目不存在 `test/` 外 `*_test.go`
  - staged 不命中 `internal/service/[^/]+.go`
- post 回退检查：
  - `git log -1 --pretty=%B` 不包含字面量 `\\n`

缺任一回退检查视为未完成，不得给“已完成”。

## 2. 阻断条件（脚本化/回退等价）
以下任一命中必须停止提交并回报 BLOCK：
- 标题不匹配 `<type>: [中文简要说明] 标题说明`
- `README.md` 未包含本次提交标题日志
- Go 项目存在 `test/` 外 `*_test.go`
- staged 命中 `internal/service/[^/]+.go`
- 最新 commit 正文含字面量 `\\n`

## 3. 统一证据输出（强制）
最终回复必须贴出并填写：
- `templates/evidence-template.md` 中的 **Skill 执行证据清单** 区块。

## 4. 通过标准
- 闸门脚本存在时均为 PASS；若脚本缺失，回退检查全部 PASS 且证据标注 `FALLBACK`
- 提交标题与正文格式合规
- 用户请求“提交git”时工作区清空（`git status --short` 为空）
- 证据模板已完整填写

## 5. 执行文件
- `scripts/pre_commit_gate.sh`
- `scripts/post_commit_gate.sh`
- `templates/evidence-template.md`
