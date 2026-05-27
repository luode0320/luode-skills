---
name: skill-hit-check-rules
description: 【强制总控】每轮用户新消息（含新会话第一条）都必须先做命中检查并在首条中间进度输出。凡涉及 Git 协作动作（含显式关键词与隐式语义，如“提交git/帮我提交/commit一下/推送代码/看下状态”），必须联动命中 git-collaboration-rules；命中后必须同步输出可核验执行证据，缺失证据视为命中失败。
---

# Skill 命中检查规则（最小闭环版）

## -1.4 极简硬闸门（新增，强制）
- 每轮首条中间进度第一行必须输出：
  - `HIT-CHECK:<PASS/BLOCK>; GIT-RULE:<PASS/NA/BLOCK>`
- 若本轮存在 Git 意图，`GIT-RULE` 不得为 `NA`。
- 未输出该行即判定 `BLOCK`，除盘点命令外禁止执行任何领域命令。

## -1. 触发确认（强制）
- 每轮用户新消息都必须命中本 skill，且必须先执行命中检查，再执行任何领域动作。
- 若用户消息包含任一 Git 意图（关键词或语义），必须同时命中 `git-collaboration-rules`。
- 若应命中未命中，判定 `BLOCK`，禁止继续执行对应领域命令。

## -1.0 新会话首轮保障（强制）
- 新会话第一条用户消息与普通轮次同等处理，不得因“缺少历史上下文”跳过本 skill。
- 无论是否已加载其他 skill，首条中间进度必须先输出“Skill 命中检查”，之后才能执行任何命令。
- 若首轮直接执行了领域命令（如 `git status`、`npm`、`go test`）而未先输出命中检查，判定为流程违规。

## -1.1 Git 意图识别（强制）
以下任一命中即视为 Git 意图，不要求用户必须出现单词 `git`：
- 显式关键词：`git`、`commit`、`push`、`pull`、`rebase`、`merge`、`cherry-pick`、`stash`、`status`、`diff`、`log`
- 中文动作词：`提交`、`推送`、`拉取`、`合并`、`变基`、`暂存`、`提交代码`、`提代码`
- 高频口语表达：`提交git`、`帮我提交`、`commit一下`、`给我推上去`、`看下git状态`、`看下改动`
- 语义等价表达：请求“把当前改动入库/提交到分支/同步到远端/查看当前提交记录”

未命中上述字面词但语义上等价时，仍必须判定为 Git 意图并联动命中 `git-collaboration-rules`。

## -1.2 Git 判定优先级（强制）
- 若同一消息同时命中多个领域，Git 判定优先级高于普通开发任务，必须先联动命中 `git-collaboration-rules`。
- 只要用户意图中包含“提交/推送/查看改动或状态/同步分支”等 Git 协作动作，不得以“需求过短”或“口语化表达”降级为普通对话。

## 0. 首条消息格式（强制）
每轮第一条中间进度必须以以下模板开头：
- `templates/hit-check-template.md`
- 最小必填三行（可在模板基础上扩展，但不得缺失）：
  - `HIT-CHECK:<PASS/BLOCK>; GIT-RULE:<PASS/NA/BLOCK>`
  - `SKILLS:<skill1,skill2,...>`
  - `GIT-LINK:<YES/NO>`

## 1. 最小流程
1. 判定命中 skill（基于用户本轮请求）
2. 先输出“Skill 命中检查”
3. 再进入主任务执行
4. 若判定存在 Git 意图，必须在同一首条中间进度显式写出“联动命中 git-collaboration-rules”

## 1.1 首条闸门（强制阻断）
若本轮命中任一 skill，但首条中间进度未按模板输出“Skill 命中检查”，则不得执行对应领域命令。
特别地：命中 `git-collaboration-rules` 时，未输出首条命中检查与三要素证据前，禁止执行任何 `git` 命令（`status` 与 `diff --cached --stat` 盘点命令除外）。

若本轮存在 Git 意图但首条未声明联动命中 `git-collaboration-rules`，同样视为未命中，禁止执行 Git 命令。

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
4. 若 gate 脚本缺失，证据清单中对应项必须标注 `FALLBACK` 且补齐等价检查结果；否则判定未完成。

## 3. 通过标准
- 首条中间进度与最终回复都含“Skill 命中检查”
- Git 场景下证据最小集完整
- 无“只命中未执行”
- 最终回复必须包含固定校验行：
  - `HIT-CHECK:PASS`
  - Git 场景追加：`GIT-RULE:PASS`

## 4. 执行文件
- `templates/hit-check-template.md`
- （Git 场景）`../git-collaboration-rules/templates/evidence-template.md`
