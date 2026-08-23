# WorkBuddy 环境配置权威清单（env manifest）

> **用途**：跨机器恢复 WorkBuddy 平台级环境配置（`settings.json` / 环境变量 / hook 脚本）。
> 换电脑后这些配置不会随仓库自动迁移，必须由本清单 + `scripts/env-bootstrap-check.py` 检测缺失并自动补齐。
> **数据源**：2026-08-23 本机（luode@Windows）实测验证的事实，非推测；官方文档与 `ACC_PRODUCT_CONFIG_V3` 环境变量交叉确认。
> **权威边界**：本文件是 WorkBuddy 平台级配置的**单一权威**；其他 skill 需要引用环境配置时一律指回本文件，不重复定义。

## 配置项总览

| # | 配置项 | 类型 | 缺失影响 | 目标值 |
|---|---|---|---|---|
| 1 | `autoCompactEnabled` | settings.json | 上下文自动压缩开关失效（退回默认） | `true` |
| 2 | `hooks.Stop` 含 summary-check.py 条目 | settings.json | 收口前任务状态检查失去平台强制兜底 | 追加条目 |
| 3 | `CODEBUDDY_CODE_MAX_TURNS` | 环境变量 | 单回合工具调用上限退回默认 500 | `1000` |
| 4 | `CODEBUDDY_MAX_RETRIES` | 环境变量 | 失败重试次数退回默认，429/超时更易中断 | `15` |
| 7 | `~/.workbuddy/hooks/summary-check.py` | hook 脚本 | Stop hook 配置指向不存在的文件，平台兜底失效 | 文件存在 |
| 8 | `~/.workbuddy/hooks/ralph-stop.py` | hook 脚本 | ralph 外部循环能力丢失（`ralph-loop` 状态机） | 文件存在 |
| 9 | `~/.browser-use/.env` | 路径引用（junction） | Browser Use Cloud 凭据读取失败（REST 通道与 MCP 均受影响） | junction → `D:\谷歌云盘\browser-use`，`.env` 含 `BROWSER_USE_API_KEY` |

## 各配置项细则

### 1. settings.json → `autoCompactEnabled`

- **路径**：`~/.workbuddy/settings.json`（用户级；项目级在 `{workspace}/.workbuddy/settings.json`，不在此清单范围）
- **目标值**：`true`
- **检测**：解析 JSON 后 `data.get('autoCompactEnabled') is True`
- **配置**：**merge 写入**——加载原 JSON，仅设置该 key，其他 key（`hooks`/`claw`/`sandbox` 等）原样保留；不整体覆盖
- **验证**：重读 JSON，确认 key 存在且为 `true`
- **来源**：2026-08-23 实测生效；官方 settings 文档存在 `autoCompactEnabled` 配置项

### 2. settings.json → `hooks.Stop` 追加 summary-check 条目

- **路径**：同上
- **目标**：`hooks.Stop` 数组内存在 command 含 `summary-check.py` 的条目
- **条目形态**（与现有 ralph-stop 条目同构）：
  ```json
  {"hooks": [{"type": "command", "command": "python3 \"C:/Users/<user>/.workbuddy/hooks/summary-check.py\" # summary-check-pmw002"}]}
  ```
- **检测**：遍历 `hooks.Stop`，任一 `hooks[0].command` 含 `summary-check.py`
- **配置**：仅追加缺失条目，**不删除/不覆盖 ralph-stop.py 或其他已有条目**；command 中的路径用实际 home 目录
- **验证**：重读 JSON，数组长度 +1 且含目标条目
- **来源**：2026-08-23 实测：Stop hook 每日被真实调用（ralph-stop 当日 188 次），exit code 2 打回通道验证可用

### 3-4. 环境变量（×2）

> ⚠️ **2026-08-23 已移除 `CODEBUDDY_AUTOCOMPACT_PCT_OVERRIDE=60` 与 `CODEBUDDY_PRE_MESSAGE_COMPACT_PCT=10`。**
> 这两个变量把紧急压缩阈值压到 60%、消息前压缩阈值压到 10%，导致频繁提前压缩 + 连续 5 次
> 触发 `consecutiveMaxTokenCompactCount` 上限后 abort（"频繁乱压缩 / 会话突然结束" 事故根因）。
> 压缩阈值应回归平台默认（紧急 90% / 默认 pre-message），**禁止再写入这两个变量**。

- **持久化方式（Windows）**：`setx <NAME> <VALUE>`（写入 `HKCU\Environment`，**重启新建进程后生效**）
- **检测（Windows）**：`reg query "HKCU\Environment" /v <NAME>` 解析 `REG_SZ` 值
- **检测（非 Windows）**：`os.environ.get(<NAME>)`（无持久化则提示写入 shell profile）
- **配置（非 Windows）**：写入 `~/.bashrc` / `~/.zshrc` 导出语句（脚本给出建议命令，不自动改 shell 配置）
- **验证**：Windows 重查注册表；新进程 `echo %NAME%`

| 变量 | 目标值 | 设计意图 |
|---|---|---|
| `CODEBUDDY_CODE_MAX_TURNS` | `1000` | 单回合工具调用上限放宽（默认 500），长任务少被步数截断 |
| `CODEBUDDY_MAX_RETRIES` | `15` | 失败重试拉满（上限 15），网络/瞬时错误自动恢复 |

### 7-8. hook 脚本文件

- **源资产**：`skill-absorption-rules/assets/hooks/summary-check.py`、`ralph-stop.py`
- **目标**：`~/.workbuddy/hooks/<name>.py`
- **检测**：`os.path.isfile(目标)`；存在时对比 md5 判断是否过期
- **配置**：`shutil.copy2` 复制；目标已存在且内容不同 → 先备份 `.bak-<时间戳>` 再覆盖（防止覆盖用户本地改动）
- **验证**：`py_compile` 通过 + md5 与资产一致
- **依赖**：Python 3 标准库，无第三方依赖；Windows 下由 WorkBuddy hook 经 Git Bash 以 `python3` 调用

### 9. `~/.browser-use/.env`（Browser Use Cloud 凭据）

- **路径**：`C:\Users\luode\.browser-use` 为 junction，指向 `D:\谷歌云盘\browser-use`（Google Drive 同步目录，跨机器恢复天然可用）
- **目标值**：junction 存在且指向上述目录；`~/.browser-use/.env` 存在且含非空 `BROWSER_USE_API_KEY=xxx` 行
- **检测**：`test -d ~/.browser-use` 且 `grep -qE '^BROWSER_USE_API_KEY=.+' ~/.browser-use/.env`；或运行 `browser-use-cloud-rules/scripts/browser-use.sh --check`
- **配置**：`mkdir -p ~/.browser-use && cp browser-use-cloud-rules/scripts/.env.example ~/.browser-use/.env`（幂等），再编辑填入真实 key；Windows 建议 `icacls` 限制本用户读写
- **验证**：`bash browser-use-cloud-rules/scripts/browser-use.sh --check` 全部 `[ok]`；`--balance` 返回余额 JSON（不消费额度）
- **权威定义**：`browser-use-cloud-rules/SKILL.md`（凭据策略唯一 Owner）；本条目只登记路径依赖事实
- **来源**：2026-08-23 吸收 browser-use-api/browser-use-guide 时登记；junction 已由用户创建（指向 Google Drive 同步目录）

## 检测/补齐速查

```bash
# 检测（只读，exit 0=完备 / 1=有缺失）
python3 "skill-absorption-rules/scripts/env-bootstrap-check.py"

# 预览修复计划（不落盘）
python3 "skill-absorption-rules/scripts/env-bootstrap-check.py" --dry-run

# 自动补齐缺失项（settings merge 写入 / setx 环境变量 / 复制 hook 脚本）
python3 "skill-absorption-rules/scripts/env-bootstrap-check.py" --fix
```

## 变更记录

- 2026-08-23 初版：登记「任务未完成回合提前结束」修复（Layer 0 平台配置 + Layer 2 hook）的全部配置事实；hook 资产入库 `assets/hooks/`。
- 2026-08-23：登记第 9 项 `~/.browser-use/.env`（Browser Use Cloud 凭据路径依赖，junction → Google Drive 同步目录）；吸收 browser-use-api/browser-use-guide 时随环境依赖登记写入。
- 2026-08-23：移除 `CODEBUDDY_AUTOCOMPACT_PCT_OVERRIDE` 与 `CODEBUDDY_PRE_MESSAGE_COMPACT_PCT` 两项（频繁乱压缩事故根因，压缩阈值回归平台默认 90% / 默认 pre-message）。
