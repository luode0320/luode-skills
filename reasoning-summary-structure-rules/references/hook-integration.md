# WorkBuddy Hook 增强触发（reasoning-summary-structure-rules）

本文件记录如何用 WorkBuddy 的 hook 功能提高 `reasoning-summary-structure-rules` 的触发准确率——把「模型自觉套总结结构」升级为「平台强制校验」，并把「后台异步任务」的收口信号做成可校验的固定结构。

## 为什么 hook 能提高触发准确率

本 skill 的触发机制是「文本信号 + 闸门预声明」：`skill-hit-check-rules` 在每轮首条把本 skill 预声明为收口 Owner，模型在最终回复前按模板输出。这个机制的薄弱点是「收口前必须自觉想起并套用模板」——如果模型在最终回复时跳过总结容器，规则无法拦截。

WorkBuddy hooks 提供两个强触发点：

| hook 事件 | 触发时机 | 能力 | 对触发准确率的提升 |
|---|---|---|---|
| `UserPromptSubmit` | 用户提交消息时 | 向本轮 prompt 注入 `additionalContext`（软提醒） | 每轮一开始就提醒模型“最终收口必须按总结结构输出”，降低漏触发概率 |
| `Stop` | Agent 完成响应、准备停止时 | 以 **exit code 2** 退出时，stderr 会注入到下一条消息，强制 Agent 继续执行（硬校验） | 最终回复若缺总结容器/异步任务小节，打回要求重写，杜绝“没有总结就收口” |

组合效果：`UserPromptSubmit` 负责“提前提醒”，`Stop` 负责“事后拦截”，二者把触发从“自觉”变成“提醒 + 强制”。

## 配置位置

hook 配置在 WorkBuddy 的设置文件 `hooks` 字段：

| 作用域 | 路径 |
|---|---|
| 用户级（所有项目生效） | `~/.workbuddy/settings.json` |
| 项目级（仅当前项目生效，覆盖用户级） | `<项目根>/.workbuddy/settings.json`（CodeBuddy CLI 为 `<项目根>/.codebuddy/settings.json`） |

> 实测说明：WorkBuddy 桌面版用户级配置路径为 `~/.workbuddy/settings.json`；CodeBuddy CLI / IDE 文档样例同时提到 `.codebuddy/settings.json`。配置前先确认本机 WorkBuddy 版本实际生效路径（可在设置页或文档确认），两处都配则项目级优先。

## 配置示例

```json
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "python3 \"$CODEBUDDY_PROJECT_DIR/.workbuddy/hooks/summary-reminder.py\"",
            "timeout": 10
          }
        ]
      }
    ],
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "python3 \"$CODEBUDDY_PROJECT_DIR/.workbuddy/hooks/summary-check.py\"",
            "timeout": 15
          }
        ]
      }
    ]
  }
}
```

> Windows 注意：WorkBuddy hook 的 `command` 通过 Git Bash 执行（不经过 cmd/PowerShell），脚本路径用 `$CODEBUDDY_PROJECT_DIR` 或绝对路径均可；Python 脚本务必用 `python3` 显式调用，不要直接执行 `.py`。

## UserPromptSubmit 软提醒脚本示例

作用：每轮用户提交时注入一句话提醒，让模型在收口前记住本 skill 的结构要求。

```python
#!/usr/bin/env python3
"""summary-reminder.py - UserPromptSubmit 软提醒注入"""
import json, sys

def main():
    data = json.load(sys.stdin)
    prompt = data.get("prompt", "")
    # 简单判断：常规任务（非纯闲聊）就注入提醒
    if len(prompt.strip()) < 2:
        print(json.dumps({"continue": True}))
        return
    reminder = (
        "【收口提醒】本轮最终回复前必须命中 reasoning-summary-structure-rules："
        "以 --- 分隔线 + `# 📋 本轮总结` 容器开场，按固定顺序输出必填小节；"
        "若启动了后台异步任务（run_in_background / CI 等待 / 长任务），必须在「结果与结论」之后输出 "
        "`## 🔄 后台异步任务` 小节，写明任务标识、轮询节奏、结果回流渠道与用户等待语义，"
        "并把「同步已完成 + 异步在跑」明确分流出收口信号。"
    )
    out = {
        "continue": True,
        "hookSpecificOutput": {
            "hookEventName": "UserPromptSubmit",
            "additionalContext": reminder
        }
    }
    print(json.dumps(out, ensure_ascii=False))

if __name__ == "__main__":
    main()
```

## Stop 硬校验脚本示例

作用：Agent 准备停止时检查会话记录（transcript）最后一条 assistant 消息是否已输出总结容器；未输出则 exit code 2，stderr 注入下一条消息强制 Agent 补总结。

```python
#!/usr/bin/env python3
"""summary-check.py - Stop 硬校验：缺总结容器或异步任务小节则打回"""
import json, os, re, sys

SUMMARY_MARK = "# 📋 本轮总结"
ASYNC_MARK = "## 🔄 后台异步任务"

def main():
    data = json.load(sys.stdin)
    transcript = data.get("transcript_path", "")
    cwd = data.get("cwd", "")

    # 拿不到 transcript 时放行（避免误伤无法校验的环境）
    if not transcript or not os.path.isfile(transcript):
        print(json.dumps({"continue": True}))
        return

    try:
        with open(transcript, "r", encoding="utf-8", errors="replace") as f:
            content = f.read()
    except Exception:
        print(json.dumps({"continue": True}))
        return

    # 简单启发式：取最后一次 assistant 输出块（含总结容器或 Plan Mode 输出）
    last_assistant = content.split("## assistant")[-1] if "## assistant" in content else content[-8000:]

    has_summary = SUMMARY_MARK in last_assistant
    has_plan = "<proposed_plan>" in last_assistant  # Plan Mode 下不强制总结

    if has_plan:
        print(json.dumps({"continue": True}))
        return

    if not has_summary:
        # exit code 2：stderr 注入下一条消息，要求 Agent 补总结
        sys.stderr.write(
            "【总结闸门】上一条回复未命中 reasoning-summary-structure-rules 的总结容器 "
            f"（缺少 `{SUMMARY_MARK}`）。请按该 skill 模板重新输出最终总结：以 --- 分隔线 + 总结容器开场，"
            "按固定顺序输出必填小节；若启动了后台异步任务，同时补 `## 🔄 后台异步任务` 小节"
            "（任务标识、轮询节奏、结果回流渠道、用户等待语义）。"
        )
        sys.exit(2)

    # 有总结容器但疑似有后台异步任务却缺异步小节：也打回一次（仅在能可靠识别时启用）
    # 说明：transcript 中若出现 "run_in_background" / "后台" 等信号且无 ASYNC_MARK 时提示补写；
    # 为防死循环，此分支只在缺少小节时提示一次，不做无限打回。
    if ASYNC_MARK not in last_assistant and ("run_in_background" in last_assistant or "轮询" in last_assistant):
        sys.stderr.write(
            "【异步分流提醒】检测到本轮涉及后台异步任务（run_in_background / 轮询），"
            "但总结缺少 `## 🔄 后台异步任务` 小节。请补写该小节：任务标识、轮询节奏、"
            "结果回流渠道（系统通知 / 下一会话 / 用户指令）、用户等待语义，"
            "并明确「同步已完成 + 异步在跑」的收口信号。"
        )
        sys.exit(2)

    print(json.dumps({"continue": True}))

if __name__ == "__main__":
    main()
```

### 防死循环说明

- `Stop` 的 exit code 2 会把 stderr 注入下一条消息，Agent 会继续执行。若校验条件永远不满足，可能反复打回。
- 本脚本只在「缺少总结容器」或「有异步信号但缺异步小节」两种明确缺口时打回；Agent 补写后即可通过，不会无限循环。
- 如需更强防死循环，可在 `Stop` payload 的 `stop_hook_active` 字段为 true（表示已处于 stop hook 反馈循环）时直接放行一次，避免重复打回。

## 实测注意事项（重要）

- WorkBuddy 官方文档列了 7 类事件（SessionStart / SessionEnd / PreToolUse / PostToolUse / UserPromptSubmit / Stop / PreCompact），但「文档列了」不等于「桌面版真的触发」——配置后必须用真实任务实测确认 `Stop` 的 exit code 2 反馈确实生效。
- `Stop` payload 含 `session_id`、`transcript_path`、`stop_hook_active`、`background_tasks` 等字段（部分版本）；`transcript_path` 指向会话记录文件，校验脚本依赖它的可读性与格式，先手工查看一次 transcript 再定解析逻辑。
- hook 脚本超时默认 60s（可配 `timeout`）；长时间阻塞会拖慢收口，建议校验脚本控制在秒级完成。
- `UserPromptSubmit` 的 `additionalContext` 是注入到本轮上下文的提醒文本，不是可执行校验；真正强制靠 `Stop` 的 exit code 2。

## 与「🔄 后台异步任务」小节的关系

- 该小节是本 skill 新增的条件小节：本轮启动了后台异步任务时必选，位于「结果与结论」之后、「后续内容」之前。
- `Stop` 校验脚本把「任务标识 + 结果回流渠道 + 用户等待语义」视为异步收口信号，缺小节判定为未收口。
- 该小节不等同于“任务未完成”、不是 `blocked/manual_handoff`、不触发「后续内容」；它只是把「同步已完成 + 异步在跑」两个状态显式分流，让用户一眼看出“本轮结束了，后台还有异步任务，结果会通过系统通知回流”。
