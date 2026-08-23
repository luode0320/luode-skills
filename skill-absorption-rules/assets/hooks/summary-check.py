#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
summary-check.py — WorkBuddy Stop hook：收口前任务状态检查（SUMMARY-GATE-PMW-002 平台强制兜底）

机制（与 ralph-stop.py 同构，职责独立）：
  1. 读取 stdin 的 Stop hook payload JSON（session_id / transcript_path / cwd 等，字段可能部分缺失）
  2. 定位 <cwd>/PROJECT_CURRENT.md 的 v4 投影 registry
  3. 按 session_id 匹配 active/blocked projection；存在未完成 step 时：
     - 命中豁免（Plan Mode / 用户明确结束 / 已输出阻断收口 / stop_hook_active / 打回超限）-> 放行 exit 0
     - 未命中豁免 -> stderr 注入剩余任务清单 + exit code 2（WorkBuddy 将 exit code 2 的 stderr
       注入下一条消息，强制 agent 继续 -> 平台兜底）
  4. 打回次数上限（状态文件计数 + 时间窗）防死循环
  5. 无 PROJECT_CURRENT.md / 无 session / 解析失败 / 无未完成 step -> 放行（不影响正常会话）

依赖：Python 3（无第三方库）。Windows 下由 WorkBuddy hook 经 Git Bash 以 python3 调用。
"""

import json
import os
import re
import sys
import datetime

STATE_FILE_REL = os.path.join(".workbuddy", "summary-check-state.json")
LOG_PATH = os.path.join(os.path.expanduser("~"), ".workbuddy", "hooks", "summary-check.log")
LOG_MAX_BYTES = 200 * 1024
MAX_REJECTIONS = 3
REJECT_WINDOW_SECONDS = 600


def debug_log(msg):
    """追加一行调试日志（用于端到端验证 hook 是否被平台调用）。"""
    try:
        if os.path.isfile(LOG_PATH) and os.path.getsize(LOG_PATH) > LOG_MAX_BYTES:
            os.remove(LOG_PATH)
        with open(LOG_PATH, "a", encoding="utf-8") as f:
            f.write("%s %s\n" % (datetime.datetime.now().isoformat(timespec="seconds"), msg))
    except Exception:
        pass


def load_payload():
    raw = sys.stdin.read() if not sys.stdin.isatty() else ""
    if not raw.strip():
        return {}
    try:
        return json.loads(raw)
    except Exception:
        return {}


def resolve_session_id(payload):
    sid = payload.get("session_id")
    if sid:
        return str(sid)
    sid = os.environ.get("WORKBUDDY_SESSION_ID")
    if sid:
        return sid
    mcp = os.environ.get("CODEBUDDY_MCP_CONFIG")
    if mcp:
        try:
            cfg = json.loads(mcp)
            for server in cfg.get("mcpServers", {}).values():
                headers = server.get("headers") or {}
                if headers.get("X-WorkBuddy-Session-Id"):
                    return str(headers["X-WorkBuddy-Session-Id"])
        except Exception:
            pass
    return None


def load_registry(project_current_path):
    if not os.path.isfile(project_current_path):
        return None
    try:
        data = open(project_current_path, encoding="utf-8").read()
    except Exception:
        return None
    m = re.search(r"BEGIN TASK PLAN PROJECTION.*?```json\n(.*?)\n```", data, re.S)
    if not m:
        return None
    try:
        return json.loads(m.group(1))
    except Exception:
        return None


def find_incomplete_steps(registry, session_id):
    """返回当前 session 的 active/blocked projection 中未完成 step 的 id/文案列表。"""
    if not registry or not isinstance(registry, dict):
        return []
    for proj in registry.get("projections", []):
        if proj.get("session_id") != session_id:
            continue
        if proj.get("state") not in ("active", "blocked"):
            continue
        incomplete = [s for s in proj.get("steps", []) if s.get("status") in ("pending", "in_progress")]
        if incomplete:
            return [s.get("id") or s.get("step", "?") for s in incomplete]
    return []


def read_transcript_tail(transcript_path, max_bytes=65536):
    """读取 transcript 尾部（用于豁免判断），超限只读最近 max_bytes。"""
    if not transcript_path or not os.path.isfile(transcript_path):
        return ""
    try:
        size = os.path.getsize(transcript_path)
        with open(transcript_path, "rb") as f:
            if size > max_bytes:
                f.seek(size - max_bytes)
            data = f.read()
        return data.decode("utf-8", errors="replace")
    except Exception:
        return ""


def has_exemption(transcript):
    """豁免判断：Plan Mode / 用户明确结束 / 已输出阻断收口。命中返回原因字符串，否则 None。"""
    if "<proposed_plan>" in transcript or "Plan Mode" in transcript:
        return "plan_mode"
    end_signals = ("结束", "停止", "到此为止", "不要继续", "不要下一步建议", "不要扩散", "终止", "停手")
    tail = transcript[-4000:]
    for sig in end_signals:
        if sig in tail:
            return "user_end:" + sig
    tail8 = transcript[-8000:]
    if "任务阻断收口" in tail8 or "BLK-" in tail8:
        return "blocked_closure"
    return None


def main():
    payload = load_payload()
    cwd = payload.get("cwd") or os.getcwd()
    session_id = resolve_session_id(payload)
    debug_log("HOOK invoked | cwd=%s | has_session=%s | has_transcript=%s" % (
        cwd, str(bool(session_id)), str(bool(payload.get("transcript_path")))))

    project_current = os.path.join(cwd, "PROJECT_CURRENT.md")
    registry = load_registry(project_current)

    if registry is None:
        debug_log("DECISION allow | reason=no_registry")
        return 0
    if not session_id:
        debug_log("DECISION allow | reason=no_session")
        return 0

    incomplete = find_incomplete_steps(registry, session_id)
    if not incomplete:
        debug_log("DECISION allow | reason=no_incomplete_steps")
        return 0

    transcript = read_transcript_tail(payload.get("transcript_path"))
    exemption = has_exemption(transcript)
    if exemption:
        debug_log("DECISION allow | reason=exemption:%s" % exemption)
        return 0

    # 状态文件：stop_hook_active 放行 + 打回计数防死循环
    state_path = os.path.join(cwd, STATE_FILE_REL)
    state = {"session_id": session_id, "reject_count": 0, "last_reject": None}
    try:
        if os.path.isfile(state_path):
            with open(state_path, encoding="utf-8") as f:
                state = json.load(f)
        if state.get("stop_hook_active"):
            debug_log("DECISION allow | reason=stop_hook_active")
            return 0
        if state.get("last_reject"):
            last = datetime.datetime.fromisoformat(state["last_reject"])
            now = datetime.datetime.now(datetime.timezone.utc)
            if (now - last).total_seconds() > REJECT_WINDOW_SECONDS:
                state["reject_count"] = 0
        if state.get("reject_count", 0) >= MAX_REJECTIONS:
            debug_log("DECISION allow | reason=max_rejections_reached")
            return 0
    except Exception:
        pass

    # 打回：更新状态文件 + stderr 注入剩余任务清单 + exit code 2
    state["session_id"] = session_id
    state["reject_count"] = state.get("reject_count", 0) + 1
    state["last_reject"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
    try:
        os.makedirs(os.path.dirname(state_path), exist_ok=True)
        with open(state_path, "w", encoding="utf-8") as f:
            json.dump(state, f, ensure_ascii=False, indent=2)
    except Exception:
        pass

    remaining = "、".join(incomplete)
    msg = (
        "[SUMMARY-GATE-PMW-002] 检测到当前会话仍有未完成任务（%s）。"
        "请继续执行剩余步骤；若因真实阻断或平台硬限制（上下文/token 上限、单回合步数上限、超时、额度、"
        "非交互模式进程退出）无法继续，必须输出显式中断点（已完成清单 + 剩余任务清单 + 下一动作 + "
        "重入入口/投影 ID），禁止输出“已完成”式总结。打回次数：%d/%d。"
        % (remaining, state["reject_count"], MAX_REJECTIONS)
    )
    debug_log("DECISION reject | count=%d/%d | remaining=%s" % (
        state["reject_count"], MAX_REJECTIONS, remaining))
    sys.stderr.write(msg + "\n")
    return 2


if __name__ == "__main__":
    sys.exit(main())
