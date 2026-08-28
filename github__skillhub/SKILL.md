---
name: github
description: "通过 GitHub CLI（gh）完整操作 GitHub：认证配置（gh auth）、PR 与 CI 排查、发布 Release、触发 GitHub Actions 工作流、仓库管理（create/delete/fork）、Issue 管理、gh api 高级查询、JSON 结构化输出。适用于命令行管理 GitHub 仓库生命周期、发布版本、操作工作流、排查 CI 失败场景。触发词：github、gh 命令、github cli、发布 release、打 tag、触发 workflow、github actions、管理仓库、创建仓库、fork、gh auth、gh release、issue、pr、ci 失败、github 命令行。"
license: MIT
metadata:
  displayName: "GitHub 命令行操作"
  version: "1.1.0"
  author: "Clawhub Developer"
---

# GitHub 命令行操作（gh）

通过 `gh` CLI 完成 GitHub 全生命周期操作：认证、PR/CI、Release、Actions、仓库管理。**查询/排查类场景与 `github-cli` 分工**：本 skill 覆盖完整操作（含写操作），`github-cli` 专精 PR/CI 查询排查（详见「适用边界」）。

## 使用流程

1. **认证**：`gh auth status` 确认已登录；未登录执行 `gh auth login`。
2. **定操作**：按「场景速查表」定位（查询类 → 可转 `github-cli` 详版）。
3. **执行**：带 `--repo owner/repo`（git 目录外必带）；写操作（release/delete/run）前向用户确认。
4. **验证**：写操作后核对返回 URL / `gh <obj> list` 确认生效。

## 场景速查表

| 目标 | 核心命令 | 验证点 |
|---|---|---|
| 登录/认证 | `gh auth login` / `gh auth status` | status 显示已登录账户 |
| PR 检查 / CI 排查 | `gh pr checks` / `gh run view --log-failed` | 检查项 pass/fail 状态 |
| 发布 Release | `gh release create v1.0.0 --title "..." --notes "..."` | release URL 返回；`gh release list` 可见 |
| 触发 Actions | `gh workflow run <name> --ref <branch>` | `gh run list` 出现新 run |
| 管理仓库 | `gh repo create/fork/delete` | repo 列表/网页确认 |
| Issue 管理 | `gh issue create/list/close` | issue URL 返回 |
| 高级查询 | `gh api ... --jq` | 输出字段符合预期 |

## 认证与配置

```bash
gh auth login                # 浏览器或 token 登录
gh auth status               # 查看登录状态
gh auth switch               # 多账户切换
```

**注意**：CI 环境/脚本场景可用 `GH_TOKEN` 环境变量（token 只读用途最小化授权）。

## 发布 Release

```bash
# 创建 release（tag 不存在会自动创建）
gh release create v1.0.0 --title "v1.0.0" --notes "变更摘要" --target main
# 附带资产文件
gh release upload v1.0.0 dist/app.zip
# 查看/删除（删除需确认）
gh release list
gh release delete v1.0.0 --yes   # 危险操作，先确认
```

**验证**：`gh release list` 显示新版本；资产上传后 `gh release view v1.0.0` 列出附件。

## 触发 GitHub Actions

```bash
# 列出可用 workflow
gh workflow list
# 手动触发（支持 workflow_dispatch）
gh workflow run deploy.yml --ref main
# 查看运行状态
gh run list --limit 5
gh run watch <run-id>        # 实时跟踪
```

**验证**：`gh run list` 出现对应 run 且结论符合预期；失败时 `gh run view <run-id> --log-failed` 定位。

## 仓库管理

```bash
gh repo create my-repo --public --clone      # 创建并克隆
gh repo fork owner/repo --clone              # fork 并克隆
gh repo view owner/repo                      # 查看详情
gh repo delete owner/repo --yes              # 危险操作，先确认
```

**验证**：创建后 `gh repo view` 正常；删除前必须二次确认。

## PR/CI 查询与排查（简版）

```bash
gh pr checks 55 --repo owner/repo
gh run view <run-id> --repo owner/repo --log-failed
gh issue list --repo owner/repo --state open --json number,title --jq '.[] | "\(.number): \(.title)"'
```

详细排查流程 → 转 `github-cli`（skill_2053082027691548672）。

## 适用边界

**何时用**：命令行全量管理 GitHub（认证、release、Actions、仓库、Issue、PR/CI）。

**何时不用**：
- 仅 PR/CI 查询排查（纯读场景）→ 转 `github-cli`（更精简的查询工作流）；
- 本地 git 提交/分支/推送 → 转 `git__skillhub`；提交/推送/回退的安全规则 → 转 `git-collaboration-rules`；
- 未安装 `gh` 或未认证 → 先 `gh auth login`；
- 写操作（release create/delete、repo delete、workflow run）未获用户确认 → 不做。

## 验收清单

- [ ] `gh auth status` 已认证；git 目录外命令带 `--repo`
- [ ] 写操作（release/repo 删除、workflow 触发）已获用户显式确认
- [ ] release 创建后已 `gh release list` 验证；资产已确认上传
- [ ] workflow 触发后 `gh run list` 可见新 run，失败已用 `--log-failed` 定位
- [ ] 查询输出用 `--json`/`--jq` 结构化，未解析人类可读文本
- [ ] 无越权写操作（未授权不 create/delete）

## 快速参考

| 命令 | 用途 |
|---|---|
| `gh auth login/status` | 认证 |
| `gh release create/upload/list` | 发布管理 |
| `gh workflow run/list` | Actions 触发与查看 |
| `gh repo create/fork/delete` | 仓库管理 |
| `gh issue create/list/close` | Issue 管理 |
| `gh pr checks` / `gh run view` | PR/CI 状态 |
| `gh api <endpoint> --jq` | 高级查询 |
