#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ralph-stop.py — WorkBuddy 版 Ralph Loop Stop hook（外部控制循环）

机制与 Claude Code 官方 ralph-loop 插件同构：
  1. 读取 stdin 的 hook payload JSON（session_id / transcript_path / cwd 等，字段可能部分缺失）
  2. 定位项目状态文件 <cwd>/.workbuddy/loop-state.md
     - 不存在 / 非 active / 会话不匹配 / 状态损坏 -> 放行（不影响正常会话）
  3. 读取 transcript 最后一条 assistant 输出，检测完成标记 <promise>XXX</promise>
     - 精确匹配 completion_promise -> 放行 + 清理状态文件
     - 未匹配 -> iteration +1 写回状态文件，stderr 注入"继续执行原任务"，exit code 2
       （WorkBuddy 将 exit code 2 的 stderr 注入下一条消息，强制 agent 继续 -> 循环）
  4. 达到 max_iterations -> 放行 + 清理状态文件

状态文件格式（YAML frontmatter + prompt 正文，与 Claude Code 版 ralph-loop.local.md 兼容）：
  ---
  active: true
  iteration: 1
  session_id: <session-id>
  max_iterations: 50
  completion_promise: "DONE"
  started_at: "2026-08-22T..."
  ---
  <prompt 正文，每次迭代原样喂回>

依赖：Python 3（无第三方库）。Windows 下由 WorkBuddy hook 经 Git Bash 以 python3 调用。
"""

import json
import os
import re
import sys
import datetime

STATE_FILE_REL = os.path.join(".workbuddy", "loop-state.md")
LOG_PATH = os.path.join(os.path.expanduser("~"), ".workbuddy", "hooks", "ralph-stop.log")
LOG_MAX_BYTES = 200 * 1024


def debug_log(msg):
    """追加一行调试日志（用于端到端验证 hook 是否被平台调用）。"""
    try:
        if os.path.isfile(LOG_PATH) and os.path.getsize(LOG_PATH) > LOG_MAX_BYTES:
            os.remove(LOG_PATH)
        with open(LOG_PATH, "a", encoding="utf-8") as f:
            f.write("%s %s\n" % (datetime.datetime.now().isoformat(timespec="seconds"), msg))
    except Exception:
        pass


def parse_frontmatter(text):
    """解析 YAML frontmatter（--- 包裹的头部）+ 正文。返回 (frontmatter dict, body str)。"""
    lines = text.split("\n")
    if not lines or lines[0].strip() != "---":
        return {}, text
    end = None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            end = i
            break
    if end is None:
        return {}, text
    fm = {}
    for line in lines[1:end]:
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if ":" in line:
            k, v = line.split(":", 1)
            fm[k.strip()] = v.strip().strip('"').strip("'")
    body = "\n".join(lines[end + 1:]).strip()
    return fm, body


def load_state(cwd):
    """读取状态文件，返回 (frontmatter, body) 或 (None, None)。"""
    path = os.path.join(cwd, STATE_FILE_REL)
    if not os.path.isfile(path):
        return None, None
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            text = f.read()
    except Exception:
        return None, None
    fm, body = parse_frontmatter(text)
    return fm, body


def clear_state(cwd):
    """删除状态文件（放行时清理）。"""
    path = os.path.join(cwd, STATE_FILE_REL)
    try:
        if os.path.isfile(path):
            os.remove(path)
    except Exception:
        pass


def bump_iteration(cwd, iteration):
    """迭代 +1 写回状态文件。"""
    path = os.path.join(cwd, STATE_FILE_REL)
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            text = f.read()
        new_text = re.sub(r"^iteration:.*$", "iteration: %d" % iteration,
                          text, count=1, flags=re.MULTILINE)
        with open(path, "w", encoding="utf-8") as f:
            f.write(new_text)
    except Exception:
        pass


def extract_promise(text, promise):
    """在文本中查找 <promise>XXX</promise>，返回是否精确匹配。"""
    if not promise or not text:
        return False
    # 取所有 promise 标签内容，空白归一后精确比较
    for m in re.finditer(r"<promise>(.*?)</promise>", text, re.DOTALL):
        val = re.sub(r"\s+", " ", m.group(1)).strip()
        if val == promise:
            return True
    return False


def read_last_assistant_text(transcript_path):
    """从 transcript 提取最后一条 assistant 文本。兼容 JSONL 与 '## assistant' 文本格式。"""
    if not transcript_path or not os.path.isfile(transcript_path):
        return ""
    try:
        with open(transcript_path, "r", encoding="utf-8", errors="replace") as f:
            content = f.read()
    except Exception:
        return ""
    if not content.strip():
        return ""
    # 尝试 JSONL：逐行解析，收集 role=assistant 的 text 块
    jsonl_texts = []
    jsonl_ok = False
    for line in content.split("\n"):
        line = line.strip()
        if not line:
            continue
        try:
            obj = json.loads(line)
        except Exception:
            jsonl_ok = False
            break
        jsonl_ok = True
        try:
            msg = obj.get("message") or obj
            role = msg.get("role") or obj.get("role")
            if role == "assistant":
                c = msg.get("content")
                if isinstance(c, list):
                    for block in c:
                        if isinstance(block, dict) and block.get("type") == "text":
                            jsonl_texts.append(block.get("text", ""))
                elif isinstance(c, str):
                    jsonl_texts.append(c)
        except Exception:
            continue
    if jsonl_ok and jsonl_texts:
        return jsonl_texts[-1]
    # 文本格式：取最后一个 "## assistant" 块
    if "## assistant" in content:
        return content.split("## assistant")[-1]
    return content[-8000:]


def main():
    try:
        payload = json.loads(sys.stdin.read() or "{}")
    except Exception:
        payload = {}
    hook_session = payload.get("session_id") or ""
    transcript_path = payload.get("transcript_path") or ""
    cwd = payload.get("cwd") or os.getcwd()
    debug_log("HOOK invoked | cwd=%s | has_session=%s | has_transcript=%s"
              % (cwd, bool(hook_session), bool(transcript_path)))

    fm, body = load_state(cwd)
    # 无状态文件或非 active -> 放行
    if fm is None or not fm.get("active") in ("true", "True", True):
        debug_log("DECISION allow | reason=no_active_state")
        print(json.dumps({"continue": True}))
        return 0

    # 会话隔离：状态文件属于其它会话时放行
    state_session = fm.get("session_id", "")
    if state_session and hook_session and state_session != hook_session:
        debug_log("DECISION allow | reason=session_mismatch state=%s hook=%s" % (state_session, hook_session))
        print(json.dumps({"continue": True}))
        return 0

    # 字段校验：损坏则清理并放行
    def is_int(v):
        try:
            int(v)
            return True
        except Exception:
            return False

    iteration = fm.get("iteration", "1")
    max_iterations = fm.get("max_iterations", "0")
    completion_promise = fm.get("completion_promise", "") or ""
    if not is_int(iteration) or not is_int(max_iterations) or not body:
        sys.stderr.write(
            "⚠️  Ralph loop: 状态文件损坏或缺失 prompt，循环停止（已清理）。"
            " 重新用 loop 启动指令创建新的循环。"
        )
        clear_state(cwd)
        debug_log("DECISION allow | reason=corrupt_state")
        print(json.dumps({"continue": True}))
        return 0

    iteration = int(iteration)
    max_iterations = int(max_iterations)

    # 迭代上限 -> 放行 + 清理
    if max_iterations > 0 and iteration >= max_iterations:
        sys.stderr.write("🛑 Ralph loop: 达到最大迭代次数 (%d)，循环停止。" % max_iterations)
        clear_state(cwd)
        debug_log("DECISION allow | reason=max_iterations reached=%d" % max_iterations)
        print(json.dumps({"continue": True}))
        return 0

    # 提取最后 assistant 文本，检测完成标记
    last_text = read_last_assistant_text(transcript_path)
    if completion_promise and extract_promise(last_text, completion_promise):
        sys.stderr.write("✅ Ralph loop: 检测到完成标记 <promise>%s</promise>，循环完成。" % completion_promise)
        clear_state(cwd)
        debug_log("DECISION allow | reason=promise_found")
        print(json.dumps({"continue": True}))
        return 0

    # 未完成 -> 迭代 +1，exit 2 + stderr 喂回原任务
    bump_iteration(cwd, iteration + 1)
    if completion_promise:
        msg = ("🔄 Ralph 迭代 %d | 任务未完成，请继续执行原任务，直到真正完成。"
               " 完成标准：输出 <promise>%s</promise>（仅当任务确实完成时输出，不得谎报）。"
               "\n\n原任务：\n%s") % (iteration + 1, completion_promise, body)
    else:
        msg = ("🔄 Ralph 迭代 %d | 任务未完成，请继续执行原任务。"
               " 未设置完成标记，循环将持续直到达到迭代上限或手动取消。"
               "\n\n原任务：\n%s") % (iteration + 1, body)
    sys.stderr.write(msg)
    debug_log("DECISION block | iteration=%d promise=%s" % (iteration + 1, completion_promise))
    return 2


if __name__ == "__main__":
    try:
        sys.exit(main())
    except SystemExit:
        raise
    except Exception as e:
        # 任何异常都放行，绝不阻塞正常会话
        print(json.dumps({"continue": True}))
        sys.exit(0)
