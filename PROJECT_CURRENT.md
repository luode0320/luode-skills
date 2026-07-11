# 项目当前状态

## 目标与范围

- 目标：完善 Windows / PowerShell / WSL 执行规则的失败恢复与经验持续回写闭环。
- 范围：`windows-wsl-execution-rules` 主 skill、失败恢复案例库、skill 默认提示、字典索引和项目状态记录。
- 非范围：业务代码、外部数据库、远程 MCP、Obsidian vault 写入、Git 提交或推送。

## 当前状态

- 状态：已完成。
- 当前执行点：Windows / WSL 失败恢复规则、案例库、字典和验证已收口。
- 更新时间：2026-07-12

## 已完成

- 已确认 `F:\AGENTS.md` 是当前项目父目录公共规则入口。
- 已确认 `PROJECT_CURRENT.md` 与 `PROJECT_HISTORY.md` 缺失，需要由自举流程创建。
- 已确认 Obsidian CLI 可用，固定 vault 为 `D:\obsidian_data`。
- 已确定采用“项目本地四件套 + Obsidian 选择性知识流”方案。
- 已同步 Obsidian、项目记忆和自举 skill，明确本地 Markdown 与 vault CLI 链路分层。
- 已同步 `AGENTS.md`、`CLAUDE.md`、`PROJECT_MEMORY.md`、`PROJECT_STYLE.md` 及缺失的 current/history 文件。
- 已刷新 skill 字典并通过三个受影响 skill 的 frontmatter 校验。
- 已通过临时仓库 bootstrap 行为测试和固定 vault 的 Obsidian CLI 检索/追加/读回验证。
- 已为 `windows-wsl-execution-rules` 增加失败恢复最小闭环、跨环境恢复路由、去重/脱敏/验证门禁和自动回写入口。
- 已新增失败恢复案例库，并记录本轮已验证的 PowerShell UTF-8 读取乱码与 `Get-FileHash` 哈希对象误用案例。
- 已同步 `agents/openai.yaml` 默认提示，要求恢复成功后回写可复用案例。

## 待办

- 无。

## 阻断

- 无。

## 验证

- `quick_validate.py`：三个受影响 skill 通过。
- bootstrap 临时仓库：缺失创建、幂等复跑、history 保留和 current 超限阻断通过。
- 字典生成器：`implemented_total=83`、`planned_missing=0`。
- `git diff --check`：通过；关键文件 UTF-8 回读通过。
- 目标文件与生成索引：显式 UTF-8 回读、内容存在性、字节数和 SHA-256 校验通过。
- Obsidian CLI：版本 1.12.7，固定 vault 注册、目标笔记检索、读取、追加和读回通过。

## 下一执行点

- 本轮任务已完成；提交已完成，未推送远端，仓库应保持清洁。
