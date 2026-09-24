# Codex 工具通道异常排查与修复指南

> 记录 Codex Desktop / CLI 中出现「工具通道整体不可用 / 命令执行全部立刻中止 (aborted) / 0 秒退出」等严重故障的根因诊断与根治方案。

---

## 一、典型现象

在 Codex Desktop 会话中（尤其是运行 `/goal` 或调用命令执行时），模型频繁输出以下特征信息：
- 模型多次执行探针，均立刻返回「已中止（aborted）」，耗时 0 秒、零输出。
- 模型在思考过程（reasoning）或最终回复中提示：
  > “工具通道仍未恢复：本轮脚本探针与目标状态写入均返回「已中止」，无输出……故障不在整个应用，而是被卡在「执行命令 / 运行脚本」这一条通道上……需要你侧重启才能恢复。”
- 用户重启客户端或新开线程后，故障依旧百分之百稳定复现。

---

## 二、快速定位（SQLite 日志排查法）

不要盲目重启应用或猜测仓库文件锁，直接查询 Codex 本地内核运行时日志数据库：

```bash
python -c "
import sqlite3
conn = sqlite3.connect(r'C:\Users\luode\.codex\logs_2.sqlite')
cursor = conn.cursor()
rows = cursor.execute('''
    SELECT id, datetime(ts, 'unixepoch', 'localtime'), level, target, feedback_log_body 
    FROM logs 
    WHERE level = 'ERROR' OR feedback_log_body LIKE '%abort%' OR feedback_log_body LIKE '%tool exec%'
    ORDER BY id DESC LIMIT 20;
''').fetchall()
for r in rows:
    print(f'[{r[1]}] [{r[2]}] [{r[3]}] {r[4][:200]}')
"
```

### 关键特征判据

| 日志特征 | 根因分类 | 对应方案 |
| :--- | :--- | :--- |
| `[codex_core::tools::router] dispatch_tool_call_with_terminal_outcome: error=Fatal error: tool exec invoked with incompatible payload` | **模型工具模式配置错误**（第三方中转模型被配置为 `tool_mode = "code_mode_only"`） | 方案 A：修正 catalog 中的第三方模型为标准 `function_call` 模式 |
| `in-flight tool future failed during drain: Fatal error: tool exec invoked with incompatible payload` | 同上 | 同上 |
| `Failed to spawn node_repl / No such file or directory` 或找不到特定 hash 路径 | **版本更新路径漂移**（`config.toml` 中硬编码了旧版本哈希目录） | 方案 B：更新 `config.toml` 中的运行时哈希路径 |
| 找不到 `plugins/cache/openai-bundled/browser/...` | **插件目录名不匹配**（实际目录名为 `chrome`） | 方案 C：在 Windows 侧建立 Junction 软链接 |

---

## 三、根本原因深度解析

### 1. Code Mode 与标准 Function Calling 协议冲突（核心根因）
- **OpenAI 官方 Code Mode**：原生 GPT-5.6 / GPT-6 模型支持 Responses API 的 Code Mode。在此模式下，Codex 会将所有工具折叠为一个内部工具 `exec`，模型通过 `custom_tool_call` 格式输出原始 JavaScript 代码文本（raw source text）。
- **第三方中转模型**：DeepSeek、GLM、Kimi、Gemini、Qwen 等通过 OpenAI-compatible API 调用。它们在处理工具调用时，一律输出标准的 OpenAI `function_call` 格式（参数封装在 `arguments: "{\"input\": \"...\"}"` 中）。
- **致命冲突**：当我们在 `model-catalog.json` 中给第三方模型配置了 `"tool_mode": "code_mode_only"` 与 `"use_responses_lite": true` 时，Codex 桌面版强制开启 Code Mode 并注册了 `code_mode::execute_handler`。该 handler 强校验 payload 类型，收到 `function_call` 后判定类型不兼容，立即触发 `Fatal error: tool exec invoked with incompatible payload` 并掐断执行，直接返回 `aborted`。

### 2. 客户端自动更新导致的路径失效
Codex 客户端静默升级后，`AppData/Local/OpenAI/Codex/` 下的哈希目录会发生变化（如从 `ad3b5049246cde44` 变为 `df473e5367fa2b42`，CLI 目录从 `994e8469124a0d31` 变为 `247581e40ee272fb`）。如果 `config.toml` 中残留了旧哈希路径，就会引发相关组件拉起失败。

---

## 四、彻底根治步骤

### 方案 A：修正模型目录配置（针对第三方模型）

第三方模型必须设置为标准工具调用模式，严禁设置 `code_mode_only`：

1. 打开生成脚本 `scripts/generate_catalog.py`，确保第三方模型配置段包含：
   ```python
   if not is_gpt:
       m.pop("model_messages", None)
       m["base_instructions"] = NEUTRAL_INSTRUCTIONS
       # 关键配置：允许标准 OpenAI function_call 工具（exec_command, apply_patch 等）
       m["tool_mode"] = None
       m["use_responses_lite"] = False
       m["multi_agent_version"] = None
       m["include_skills_usage_instructions"] = True
       m["include_apps_usage_instructions"] = True
       m["include_plugin_usage_instructions"] = True
       m["node_repl_disabled"] = False
       m["node_repl_auto_review_required"] = False
   ```
2. 执行脚本重新生成并同步：
   ```bash
   python ~/.workbuddy/skills/codex-custom-models/scripts/generate_catalog.py
   ```
3. 检查生成的 `~/.codex/model-catalog.json`，确保第三方模型的 `"tool_mode": null` 且 `"use_responses_lite": false`。

### 方案 B：校准 `config.toml` 路径（针对更新漂移）

1. 查看当前系统中最新运行时哈希：
   ```bash
   ls -d /c/Users/luode/AppData/Local/OpenAI/Codex/runtimes/cua_node/*/
   ls -d /c/Users/luode/AppData/Local/OpenAI/Codex/bin/*/
   ```
2. 检查 `~/.codex/config.toml` 中的 `notify` 与 `CODEX_CLI_PATH`，将旧哈希替换为最新目录。

### 方案 C：补齐插件目录 Junction

若存在插件查找 `browser` 目录的情况，在 PowerShell 中执行建立 Junction：
```powershell
New-Item -ItemType Junction -Path "C:\Users\luode\.codex\plugins\cache\openai-bundled\browser" -Target "C:\Users\luode\.codex\plugins\cache\openai-bundled\chrome" -Force
```

---

## 五、验证标准

运行一次涉及命令行执行的测试（如 `deepseek-v4.1-flash` 执行 `git status`）：

```bash
/c/Users/luode/AppData/Local/OpenAI/Codex/bin/<latest_hash>/codex.exe exec --skip-git-repo-check --dangerously-bypass-approvals-and-sandbox -m deepseek-v4.1-flash 'Check git status in current directory'
```

- **验证合格判据**：
  1. CLI 或 App 正确发出 `function_call` 调用 `exec_command`；
  2. 命令正常执行并返回实际终端输出及退出码；
  3. 全程无 `Fatal error: tool exec invoked with incompatible payload` 报错；
  4. 日志数据库中无新产生的 `aborted` 错误记录。
