# 环境依赖吸收指引（env dependency absorption）

> 吸收经验的常见盲区：只吸收"规则正文"，丢弃规则依赖的**环境配置**（环境变量 / 宿主配置 / hook / 依赖 / 路径）。
> 结果是本机验证有效，换一台电脑后静默失效——用户反复踩"另一台电脑上就没有这些配置"的坑。
> 本指引把「环境依赖」提升为吸收的一等公民：**吸收时同步识别、登记、附加自检能力**。

## 1. 环境依赖五类（识别清单）

| 类型 | 典型示例 | 失效症状（换机器后） |
|---|---|---|
| **环境变量** | `CODEBUDDY_*`、`API_KEY`、`PATH` 追加 | 功能静默退化或报错，无任何提示 |
| **宿主配置** | `~/.workbuddy/settings.json`、`{workspace}/.workbuddy/` | 开关/钩子不生效，行为退回默认 |
| **hook / 插件 / MCP** | `~/.workbuddy/hooks/*.py`、MCP server 配置 | 配置指向不存在的脚本，钩子静默失效 |
| **依赖安装** | pip/npm 包、系统库、CLI 工具 | `ImportError` / `command not found` |
| **路径引用** | 绝对路径、知识库根、junction 挂载 | 文件/目录找不到 |

**判定信号**：吸收的原子条目中若出现"设置环境变量 / 修改配置 / 安装依赖 / 部署脚本 / 使用某工具 / 引用某路径"，即隐含环境依赖，必须走第 2 步。

> **与「agent 通用性」的区分（2026-08-30 补）**：环境依赖（本节，第 8 条）关注配置离开**机器**失效；「agent 通用性」（设计内核第 9 条）关注机制离开**特定 agent**（Codex / Claude / ZCode / WorkBuddy）失效。逐条判定时两者都要显式登记：环境依赖登记在裁决表「环境依赖」列，agent 绑定登记在「agent 通用性」列（`通用` 或 `例外: <绑定对象> + 理由`）。凡条目依赖某 agent 专属路径 / 配置 / hook / 命令 / 声明（如 `~/.claude/`、`~/.codex/`、codex/claude 专属 MCP、`agent_created` 限定），即使本机可运行，也属于 agent 绑定，须按「agent 通用性判定」处理（通用落点或登记例外）。

## 2. 吸收时必做：环境依赖登记

1. **逐条判定**：裁决表的每条来源原子条目，额外判定是否隐含环境依赖（用第 1 节五类清单对照）。
2. **登记列**：裁决表新增「环境依赖」列，取值：
   - `N/A`——纯规则/方法论条目，无环境依赖（+ 一句话理由）；
   - 依赖项清单——`类型: 名称 = 目标值`，如 `env: CODEBUDDY_MAX_RETRIES = 15`、`hook: summary-check.py`、`pip: requests`。
3. **落点**：环境依赖定义写入目标 skill 的 manifest（如本 skill 的 `references/workbuddy-env-manifest.md`），或并入主清单；**同一依赖项全仓库只允许一个权威定义**，其余 skill 引用，不重复定义（纳入同域扫描检查项）。
4. **来源记录**：`source-notes.md` 追加一行，注明"环境依赖 X 项已登记至 <manifest 路径>"。

## 3. 环境类 skill 的自检附加能力（强制）

环境依赖 ≥ 1 项的 skill 落盘时，**必须**附带自检方式，二选一：

- **简单场景（1-3 项依赖）**：SKILL.md 内加「环境自检」小节，给出三行命令——检测 / 配置 / 验证。示例：
  ```bash
  # 检测：<命令>（缺失时输出缺什么）
  # 配置：<命令>（幂等，重复执行不产生副作用）
  # 验证：<命令>（确认生效）
  ```
- **复杂场景（≥3 项或涉及宿主配置/hook 部署）**：提供 `scripts/env-bootstrap-check.py` 或等效脚本，支持 `--check`（只读检测）/ `--dry-run`（预览修复）/ `--fix`（自动补齐），并登记到本 skill 的 manifest。
- **WorkBuddy 平台级配置**：统一走 `skill-absorption-rules/scripts/env-bootstrap-check.py`（覆盖 manifest 全部 8 项），单个 skill 不重复造轮子。

## 4. 换机器恢复流程（用户场景）

```bash
# 1) 新机器 clone 仓库（含本 skill 的 manifest + assets + scripts）
git clone <luode-skills-repo>

# 2) 自动补齐 WorkBuddy 平台级配置（settings / 环境变量 / hook 脚本）
python3 skill-absorption-rules/scripts/env-bootstrap-check.py --fix

# 3) 逐 skill 运行独立自检（若有 manifest 之外的依赖）
# 4) 验证 hook 真实生效：跑一个真实任务，检查 ~/.workbuddy/hooks/*.log 有今日调用记录
```

## 5. 与既有流程的衔接

- **裁决表**：新增「环境依赖」列（`N/A + 理由` 或依赖项清单）。
- **同域扫描**：把"环境依赖重复登记"纳入检查——同一依赖项在两个 skill 重复定义时，收敛为单一权威（manifest）+ 引用。
- **收口说明**：追加「环境依赖登记 X 项 / 自检能力 Y 项」。
- **棘轮验证**：环境类吸收的效果验证场景必须包含"换机器/干净环境模拟"（如用临时 `--home-dir` 跑一遍自检脚本），只在本机验证不算闭环。
- **本指引自身的 manifest**：WorkBuddy 平台级配置权威清单见 `references/workbuddy-env-manifest.md`，hook 资产见 `assets/hooks/`。
