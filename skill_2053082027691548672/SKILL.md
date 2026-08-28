---
name: github-cli
description: "使用 GitHub CLI（gh）操作 GitHub：PR 检查与状态查询（gh pr checks）、CI 运行查看与失败日志（gh run list/view --log-failed）、Issue 管理、gh api 高级查询、JSON 结构化输出（--json/--jq）。适用于通过命令行管理 GitHub 仓库任务、排查 CI 失败、批量操作 Issue/PR 场景。触发词：github cli、gh 命令、gh pr、gh run、gh api、查看CI、workflow 失败、PR 检查、issue 列表、github 命令行、check CI、ci 状态。"
license: MIT
metadata:
  displayName: "GitHub CLI（gh）操作"
  version: "1.1.0"
  author: "Clawhub Developer"
---

# GitHub CLI（gh）操作

通过 `gh` CLI 完成 GitHub 日常运维：PR 检查、CI 排查、Issue 管理、API 高级查询。前置条件：`gh` 已安装且已认证（`gh auth status` 应显示已登录）。

## 使用流程

1. **确认前置**：`gh auth status` 已认证；不在 git 目录内操作时，所有命令必须带 `--repo owner/repo`。
2. **定位场景**：按「场景速查表」找到对应工作流。
3. **执行命令**：按工作流中的命令执行（替换 `owner/repo`、`55`、`<run-id>` 等占位符）。
4. **验证结果**：核对每个工作流末尾的验证点（输出字段是否符合预期）。

## 场景速查表

| 目标 | 工作流 | 核心命令 |
|---|---|---|
| PR 是否通过 CI | [§1 PR 检查](#1-pr-检查) | `gh pr checks` |
| CI 失败原因 | [§2 CI 故障排查](#2-ci-故障排查) | `gh run view --log-failed` |
| 批量管理 Issue/PR | [§3 Issue 与 PR 管理](#3-issue-与-pr-管理) | `gh issue/pr list --json` |
| 子命令覆盖不到的查询 | [§4 gh api 高级查询](#4-gh-api-高级查询) | `gh api ... --jq` |
| 结构化输出给脚本 | [§5 JSON 输出](#5-json-输出) | `--json/--jq` |

---

## 1. PR 检查

**目标**：确认 PR 的 CI 状态与合并条件。

```bash
# 检查 PR 55 的所有检查项（需在 git 目录，或加 --repo）
gh pr checks 55 --repo owner/repo
# 查看 PR 详情（分支、合入状态、reviewer）
gh pr view 55 --repo owner/repo
# 查看 PR 上所有评论/评审
gh pr view 55 --repo owner/repo --comments
```

**验证**：输出包含每个 check 的 `pass`/`fail`/`pending` 状态；若有 `fail` 项，转入 §2。

## 2. CI 故障排查

**目标**：定位失败的 workflow run 与具体失败步骤。

```bash
# 列出最近 10 次运行（含结论 success/failure）
gh run list --repo owner/repo --limit 10
# 查看指定 run 的结构与各 step 状态
gh run view <run-id> --repo owner/repo
# 只看失败步骤的日志（省去滚动长日志）
gh run view <run-id> --repo owner/repo --log-failed
# 只看指定 job 的日志
gh run view <run-id> --repo owner/repo --job <job-id>
```

**验证**：`--log-failed` 输出的错误行能定位到失败命令与报错信息；修复后重跑：`gh run rerun <run-id>`。

## 3. Issue 与 PR 管理

**目标**：批量列出、筛选、创建 Issue/PR。

```bash
# 列出 open 的 issue（结构化）
gh issue list --repo owner/repo --state open --limit 20
# 筛选：指派给某人 / 带某 label
gh issue list --repo owner/repo --assignee @me --label "bug"
# 创建 issue
gh issue create --repo owner/repo --title "标题" --body "描述" --label bug
# 创建 PR（本地分支已 push 后）
gh pr create --repo owner/repo --title "标题" --body "描述" --base main --head feature-x
```

**验证**：列表命令输出行数与网页端一致；创建命令返回新 issue/PR 的 URL 即成功。

## 4. gh api 高级查询

**目标**：子命令没有的能力，用 `gh api` 直连 REST API。

```bash
# 取 PR 指定字段
gh api repos/owner/repo/pulls/55 --jq '.title, .state, .user.login'
# 列分支保护规则
gh api repos/owner/repo/branches/main/protection --jq '.required_status_checks.contexts'
# 分页取全部结果（默认单页 30 条）
gh api --paginate "repos/owner/repo/issues?state=all" --jq '.[] | .number'
```

**验证**：`--jq` 表达式输出期望字段；分页场景用 `--paginate` 确认结果集完整（数量与网页一致）。

## 5. JSON 输出

**目标**：把结果交给脚本/工具消费，避免解析人类可读文本。

```bash
# 关键：所有结构化子命令都支持 --json，字段用逗号列出
gh issue list --repo owner/repo --json number,title,labels \
  --jq '.[] | "\(.number): \(.title)"'
# 输出原始 JSON（不写 --jq 时）
gh pr list --repo owner/repo --json number,title,mergeable
```

**验证**：`--jq` 过滤后输出格式稳定；无匹配时为空输出而非报错（区分「查询无结果」与「命令失败」用 `$?`）。

---

## 适用边界

**何时用**：命令行管理 GitHub（PR/CI/Issue/API 查询）、CI 失败定位、批量操作、脚本化 GitHub 数据获取。

**何时不用**：
- 本地 git 提交/分支操作 → 转 `git__skillhub`、`git-collaboration-rules`（提交/推送/回退规则）；
- GitHub 发布/资产上传等发布流水线 → 转 `github__skillhub`（同域补充）；
- 未安装或未认证 `gh`（`gh auth login` 后重试）；
- 需要 Web 交互（创建 release 草稿、编辑 wiki）→ 直接用 GitHub 网页。

## 验收清单

- [ ] `gh auth status` 通过；git 目录外已带 `--repo owner/repo`
- [ ] 查询类命令输出符合预期字段（用 `--json` 而非解析文本）
- [ ] CI 排查按「run list → view → log-failed」三级定位完成
- [ ] 创建/修改类命令（issue/pr create）返回了对应 URL
- [ ] 未在无授权情况下执行写操作（gh 写命令需用户明确要求）

## 快速参考

| 命令 | 用途 | 常用参数 |
|---|---|---|
| `gh pr checks <n>` | PR 检查项状态 | `--repo` |
| `gh pr view <n>` | PR 详情 | `--comments` |
| `gh run list` | 最近 workflow 运行 | `--limit` |
| `gh run view <id>` | 运行详情 | `--log-failed` / `--job` |
| `gh issue list` | Issue 列表 | `--state` / `--assignee` / `--label` |
| `gh api <endpoint>` | REST API 直连 | `--jq` / `--paginate` |
| `gh auth status` | 认证检查 | — |
