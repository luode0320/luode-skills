# AI 团队项目定位 — project / settings

> 本模块覆盖「AI 团队对应项目」的 projectId 解析、默认项目登记与 AI 分支工作流结合。已从 SKILL.md 继承：登录与项目、写入标准流程、AI 权限规则、AI 分支说明、必须询问用户。
>
> 背景：本仓库约定接口级测试与接口新增/更新统一落在 Apifox 组织下名为「AI」的团队对应项目中。本模块负责把「团队名 + 项目名」解析为 CLI 可用的 `--project <projectId>`。

## 何时加载

- 首次接入 apifox，需要确定「AI 团队对应项目」是哪一个
- 多项目环境，需要确认当前命令作用于哪个项目
- 接口新增/更新同步 apifox 前，需要确认目标项目（配合 `modules/api-sync-to-apifox.md`）
- 接口测试执行前，需要确认被测用例落在哪个项目

## 解析 projectId 的标准流程（强制）

1. **确认登录**：`apifox whoami`；未登录先 `apifox login --with-token <TOKEN>`（token 由用户提供，凭证存 `~/.apifox/config.toml`，不要打印到日志或聊天摘要）。
2. **列出可访问项目**：`apifox project list`。
3. **按团队名「AI」过滤**：
   - 若输出含团队/团队 ID 字段，定位团队名为「AI」的项目；
   - 若输出不含团队字段，按项目名与用户确认哪个是「AI 团队」对应项目；
   - 多个候选项目时，必须询问用户，不要自行猜测。
4. **记录 projectId**：确认后把 projectId 登记到项目根 `.apifox/settings.json` 的 `projectId` 字段（写入本地配置文件前先询问用户），后续命令可省略 `--project`；多项目场景仍建议显式 `--project <projectId>`。
5. **验证**：`apifox endpoint list --project <projectId> --limit 1` 或 `apifox project list` 复核 projectId 有效。

## 默认项目登记（.apifox/settings.json）

- 项目未指定时，CLI 先查 `.apifox/settings.json` 中是否有默认 `projectId`
- 写入 `settings.json` 属于本地配置写入，执行前必须先询问用户
- 一个工作区可以有多个项目，`settings.json` 只记录默认项目；切换项目用显式 `--project`

## AI 分支工作流与接口同步结合（强制）

接口新增/更新到 apifox 时，默认走 AI 分支隔离，避免直接污染主分支：

```text
确认源分支和目标项目（--project <projectId>）
  → 创建 AI 分支（命名：ai/年月日-from-来源分支名-接口同步）
  → pick-to 导入源分支已有接口（新建接口不需要）
  → 在 AI 分支上 import / endpoint create / update / test-case 落地
    （所有命令带 --branch <aiBranchName>）
  → 运行验证（test-case run --environment <localhost环境>）
  → merge-request preview 让用户确认
  → 用户确认后 create merge-request 或 merge
```

- 主分支受保护时（isProtected）优先 `merge-request`，不要直接 `merge`
- AI 分支 24 小时内与来源分支无差异将自动归档；修改源分支已有资源前必须先 `pick-to`
- 直接编辑主分支需 Apifox 客户端 2.8.32+「项目设置 - 功能设置 - AI 功能设置 - 外部 AI 编辑权限」开启；未开启时选 AI 分支流程

## 不可违反规则

1. 未确认项目身份前不执行任何写操作
2. 写入 `.apifox/settings.json` 前必须询问用户
3. 目标主分支受保护时优先 merge-request，不直接 merge
4. 不要在 AI 分支里修改源分支已有资源而不先 pick-to
5. 不要在分支任务中省略 `--branch`
6. 团队名/项目名不明确时，先问用户，不要猜测
