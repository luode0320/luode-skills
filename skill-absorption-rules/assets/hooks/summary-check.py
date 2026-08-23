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
  4. 投影 registry 异常（有托管痕迹但解析失败/损坏）-> 显式中断点打回（防止中断被伪装成完成）
  5. 平台中断痕迹检测（registry 正常但 transcript 尾部含平台 abort 完整原话）-> 显式中断点打回
  6. 打回次数上限（状态文件计数 + 时间窗）防死循环
  7. 无 PROJECT_CURRENT.md / 无 session / 完全无投影痕迹 -> 放行（不影响正常会话）

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

# 平台中断痕迹信号：宿主 abort 的完整原话，agent 正常回复极少完整复述，
# 以最小化「讨论压缩/中断话题」时被误伤的概率。
INTERRUPT_SIGNALS = (
    "Aborting session for context compaction",
    "stopping compact loop",
)


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
    """读取并解析 v4 投影 registry；无托管区或解析失败返回 None。"""
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


def has_projection_trace(project_current_path):
    """判断 PROJECT_CURRENT.md 是否残留投影托管痕迹（marker 存在）。

    用于区分「本就没有投影的正常会话」与「投影丢失/损坏」：
    前者放行，后者应输出显式中断点打回，防止中断被伪装成完成。
    """
    if not os.path.isfile(project_current_path):
        return False
    try:
        data = open(project_current_path, encoding="utf-8").read()
    except Exception:
        return False
    return "BEGIN TASK PLAN PROJECTION" in data or "END TASK PLAN PROJECTION" in data


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
    """读取 transcript 尾部（用于豁免/中断判断），超限只读最近 max_bytes。"""
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


def detect_interrupt_signal(transcript):
    """检测 transcript 尾部的平台中断痕迹，命中返回信号字符串，否则 None。

    仅匹配宿主 abort 的完整原话，避免误伤 agent 在正常回复中讨论压缩问题的场景。
    """
    if not transcript:
        return None
    tail = transcript[-16000:]
    for sig in INTERRUPT_SIGNALS:
        if sig in tail:
            return sig
    return None


def _maybe_reject(session_id, cwd, remaining_text, reason):
    """统一打回逻辑：状态文件计数防死循环 + stderr 注入 + exit code。

    返回 2 表示打回（阻止收口），0 表示放行（stop_hook_active / 打回超限）。
    """
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

    state["session_id"] = session_id
    state["reject_count"] = state.get("reject_count", 0) + 1
    state["last_reject"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
    try:
        os.makedirs(os.path.dirname(state_path), exist_ok=True)
        with open(state_path, "w", encoding="utf-8") as f:
            json.dump(state, f, ensure_ascii=False, indent=2)
    except Exception:
        pass

    msg = (
        "[SUMMARY-GATE-PMW-002] %s。"
        "请继续执行剩余步骤；若因真实阻断或平台硬限制（上下文/token 上限、单回合步数上限、超时、额度、"
        "非交互模式进程退出）无法继续，必须输出显式中断点（已完成清单 + 剩余任务清单 + 下一动作 + "
        "重入入口/投影 ID），禁止输出“已完成”式总结。打回次数：%d/%d。"
        % (remaining_text, state["reject_count"], MAX_REJECTIONS)
    )
    debug_log("DECISION reject | reason=%s | count=%d/%d | remaining=%s" % (
        reason, state["reject_count"], MAX_REJECTIONS, remaining_text))
    sys.stderr.write(msg + "\n")
    return 2


def main():
    payload = load_payload()
    cwd = payload.get("cwd") or os.getcwd()
    session_id = resolve_session_id(payload)
    debug_log("HOOK invoked | cwd=%s | has_session=%s | has_transcript=%s" % (
        cwd, str(bool(session_id)), str(bool(payload.get("transcript_path")))))

    if not session_id:
        debug_log("DECISION allow | reason=no_session")
        return 0

    project_current = os.path.join(cwd, "PROJECT_CURRENT.md")
    registry = load_registry(project_current)
    transcript = read_transcript_tail(payload.get("transcript_path"))

    # 1. registry 无法解析：有托管痕迹=损坏（打回），无痕迹=正常无投影（放行）
    if registry is None:
        if has_projection_trace(project_current):
            exemption = has_exemption(transcript)
            if exemption:
                debug_log("DECISION allow | reason=exemption:%s" % exemption)
                return 0
            return _maybe_reject(
                session_id, cwd,
                "检测到 PROJECT_CURRENT.md 存在任务投影托管痕迹，但投影 registry 解析失败或为空"
                "（疑似中断/压缩后投影未正确落盘）",
                "registry_corrupt_or_empty",
            )
        debug_log("DECISION allow | reason=no_registry")
        return 0

    incomplete = find_incomplete_steps(registry, session_id)

    # 2. 无未完成 step：检查平台中断痕迹（防止投影误标 completed 后中断被伪装成完成）
    if not incomplete:
        interrupt = detect_interrupt_signal(transcript)
        if interrupt:
            exemption = has_exemption(transcript)
            if exemption:
                debug_log("DECISION allow | reason=exemption:%s" % exemption)
                return 0
            return _maybe_reject(
                session_id, cwd,
                "检测到平台中断痕迹（%s），但投影未记录未完成步骤，疑似中断被误标为完成" % interrupt,
                "interrupt_signal:" + interrupt,
            )
        debug_log("DECISION allow | reason=no_incomplete_steps")
        return 0

    # 3. 有未完成 step：豁免检查后打回
    exemption = has_exemption(transcript)
    if exemption:
        debug_log("DECISION allow | reason=exemption:%s" % exemption)
        return 0
    return _maybe_reject(
        session_id, cwd,
        "检测到当前会话仍有未完成任务（%s）" % "、".join(incomplete),
        "incomplete_steps",
    )


if __name__ == "__main__":
    sys.exit(main())
