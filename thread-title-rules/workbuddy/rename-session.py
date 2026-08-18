#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
thread-title-rules —— WorkBuddy 宿主会话标题写入脚本。

把当前 WorkBuddy 会话的标题写入原生会话表（~/.workbuddy/workbuddy.db 的 sessions 表）。
与 mcp/bootstrap.mjs 同一设计风格：幂等、带备份、稳定 JSON 输出、--check 只读模式。

安全边界（严格遵守）：
- 绝不打印 CODEBUDDY_MCP_CONFIG 环境变量全文（含 Bearer token），只提取会话 ID。
- 只 UPDATE sessions 表指定行的 title（或 custom_title）单字段；不删行、不碰其他表。
- 写入前做整库备份（sqlite backup API，WAL 安全），备份文件不与既有文件重名。
- 提供 --expect-old 原子保护：调用方先读到的旧标题若已变化则拒绝写入。

用法：
  python rename-session.py --check
  python rename-session.py --title "新标题"
  python rename-session.py --title "新标题" --session-id <uuid> [--field custom_title]
  python rename-session.py --title "新标题" --expect-old "旧标题"

最近修改时间：2026-08-19（吸收 auto-rename-session-label 后新增的 WorkBuddy 适配）。
"""

import argparse
import json
import os
import re
import sqlite3
import sys
import uuid
from datetime import datetime

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

SESSION_ID_RE = re.compile(r"[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}")


def emit(payload, exit_code=0):
    """输出稳定 JSON 并以指定退出码结束。"""
    print(json.dumps(payload, ensure_ascii=False))
    sys.exit(exit_code)


def resolve_config_dir(env=None):
    """解析 WorkBuddy 配置目录：WORKBUDDY_CONFIG_DIR > CODEBUDDY_CONFIG_DIR > ~/.workbuddy。"""
    env = env or os.environ
    for key in ("WORKBUDDY_CONFIG_DIR", "CODEBUDDY_CONFIG_DIR"):
        value = env.get(key)
        if value and str(value).strip():
            return os.path.abspath(str(value).strip())
    return os.path.join(os.path.expanduser("~"), ".workbuddy")


def resolve_db_path(config_dir):
    """sessions 元数据所在的 SQLite 文件。"""
    return os.path.join(config_dir, "workbuddy.db")


def extract_session_id(env=None):
    """
    从可信宿主元数据提取当前会话 ID，绝不回显整个环境变量（内含 Bearer token）。
    顺序：CODEBUDDY_MCP_CONFIG 的 X-WorkBuddy-Session-Id 请求头 > 正则兜底 > 失败。
    """
    env = env or os.environ
    raw = env.get("CODEBUDDY_MCP_CONFIG")
    if not raw:
        return None
    # 1) 优先按 JSON 解析取 headers.X-WorkBuddy-Session-Id
    try:
        cfg = json.loads(raw)
        for server in cfg.get("mcpServers", {}).values():
            headers = server.get("headers") if isinstance(server, dict) else None
            if isinstance(headers, dict) and headers.get("X-WorkBuddy-Session-Id"):
                sid = str(headers["X-WorkBuddy-Session-Id"]).strip()
                if SESSION_ID_RE.fullmatch(sid):
                    return sid
    except Exception:
        pass
    # 2) 正则兜底（JSON 结构变化时）
    m = SESSION_ID_RE.search(raw)
    return m.group(0) if m else None


def validate_title(title):
    """标题校验：去除首尾空白后须为 1-40 个 Unicode 字符（8-24 字规则由 Skill 负责）。"""
    title = (title or "").strip()
    if not title:
        return None, "title_empty"
    length = len(title)
    if length > 40:
        return None, "title_too_long"
    return title, None


def backup_db(db_path):
    """用 sqlite backup API 做整库备份（WAL 安全），返回备份路径；同名备份已存在则失败。
    时间戳精度到毫秒，避免同一秒内重复运行时报 backup_exists（幂等承诺：重复写入安全）。"""
    stamp = datetime.now().strftime("%Y%m%d%H%M%S%f")[:-3]
    backup_path = f"{db_path}.bak-{stamp}"
    if os.path.exists(backup_path):
        return None, "backup_exists"
    src = sqlite3.connect(db_path)
    try:
        dst = sqlite3.connect(backup_path)
        try:
            src.backup(dst)
        finally:
            dst.close()
    finally:
        src.close()
    return backup_path, None


def do_check(db_path, session_id, env=None):
    """只读探测：宿主、会话 ID、标题现状。绝不写入。"""
    payload = {
        "ok": True,
        "mode": "check",
        "host": "workbuddy",
        "sessionId": session_id,
        "dbPath": db_path,
        "dbExists": os.path.exists(db_path),
        "title": None,
        "customTitle": None,
        "writable": False,
    }
    if not session_id:
        payload["ok"] = False
        payload["error"] = "session_id_unavailable"
        return payload
    if not os.path.exists(db_path):
        payload["ok"] = False
        payload["error"] = "db_not_found"
        return payload
    try:
        con = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
        try:
            row = con.execute(
                "SELECT title, custom_title FROM sessions WHERE id = ? AND deleted_at IS NULL", (session_id,)
            ).fetchone()
            if row:
                payload["title"] = row[0]
                payload["customTitle"] = row[1]
            else:
                payload["ok"] = False
                payload["error"] = "session_not_found"
        finally:
            con.close()
    except Exception as exc:  # noqa: BLE001 —— 探测失败也要给出可读 JSON
        payload["ok"] = False
        payload["error"] = f"probe_failed: {exc}"
    payload["writable"] = os.access(db_path, os.W_OK)
    return payload


def do_rename(db_path, session_id, title, field, expect_old):
    """写入标题：备份 → 原子保护 → UPDATE → 回读校验。"""
    if field not in ("title", "custom_title"):
        return {"ok": False, "error": "invalid_field"}

    if not os.path.exists(db_path):
        return {"ok": False, "error": "db_not_found", "sessionId": session_id}

    con = sqlite3.connect(db_path)
    try:
        # 0) 读取写入前旧值（同时确认会话存在）
        row = con.execute(
            "SELECT title, custom_title FROM sessions WHERE id = ? AND deleted_at IS NULL", (session_id,)
        ).fetchone()
        if not row:
            return {"ok": False, "error": "session_not_found", "sessionId": session_id}
        old_value = row[0] if field == "title" else row[1]

        # 1) 原子保护：调用方基于旧值决策，期间标题若被他人修改则拒绝覆盖
        if expect_old is not None and old_value != expect_old:
            return {
                "ok": False,
                "error": "title_changed_since_read",
                "reason": "写入前重查发现标题已被修改，拒绝覆盖（并发保护）",
                "sessionId": session_id,
                "field": field,
                "currentTitle": old_value,
                "expectedOld": expect_old,
            }

        # 2) 整库备份（WAL 安全），写入前完成
        backup_path, backup_err = backup_db(db_path)
        if backup_err:
            return {"ok": False, "error": backup_err, "sessionId": session_id}

        # 3) UPDATE 单行单字段
        cur = con.execute(
            f"UPDATE sessions SET {field} = ?, updated_at = ? WHERE id = ? AND deleted_at IS NULL",
            (title, int(datetime.now().timestamp() * 1000), session_id),
        )
        if cur.rowcount != 1:
            return {"ok": False, "error": "session_not_found", "sessionId": session_id, "backupPath": backup_path}
        con.commit()

        # 4) 回读校验：证明真实落库
        after = con.execute(
            f"SELECT {field} FROM sessions WHERE id = ?", (session_id,)
        ).fetchone()
        verified = bool(after and after[0] == title)
        return {
            "ok": verified,
            "mode": "rename",
            "sessionId": session_id,
            "field": field,
            "oldTitle": old_value,
            "newTitle": title,
            "backupPath": backup_path,
            "verified": verified,
        }
    finally:
        con.close()


def main(argv=None):
    parser = argparse.ArgumentParser(description="WorkBuddy 宿主会话标题写入脚本（幂等、带备份、只读 --check）")
    parser.add_argument("--check", action="store_true", help="只读探测，不写入不备份")
    parser.add_argument("--title", help="新标题（执行模式必填）")
    parser.add_argument("--session-id", help="显式会话 ID；缺省从 CODEBUDDY_MCP_CONFIG 提取")
    parser.add_argument("--db", help="显式 workbuddy.db 路径；缺省 $WORKBUDDY_CONFIG_DIR/workbuddy.db")
    parser.add_argument("--field", choices=["title", "custom_title"], default="custom_title",
                        help="写入字段：custom_title=用户改名槽（默认，主进程不覆盖）；title=主进程独占的自动摘要槽，仅诊断用、不应主动写")
    parser.add_argument("--expect-old", help="原子保护：当前值与此不一致时拒绝写入")
    args = parser.parse_args(argv)

    config_dir = resolve_config_dir()
    db_path = os.path.abspath(args.db) if args.db else resolve_db_path(config_dir)

    # 会话 ID：显式参数优先，否则从可信宿主元数据提取（绝不回显 env 全文）
    session_id = None
    if args.session_id and SESSION_ID_RE.fullmatch(str(args.session_id).strip()):
        session_id = str(args.session_id).strip()
    else:
        session_id = extract_session_id()
    if session_id:
        session_id = session_id.lower()

    if args.check:
        payload = do_check(db_path, session_id)
        emit(payload, 0 if payload["ok"] else 1)

    # 执行模式：标题必填
    title, title_err = validate_title(args.title)
    if title_err:
        emit({"ok": False, "error": title_err, "hint": "标题去除首尾空白后须为 1-40 个 Unicode 字符"}, 1)
    if not session_id:
        emit({"ok": False, "error": "session_id_unavailable",
              "hint": "请用 --session-id 显式传入，或确认 CODEBUDDY_MCP_CONFIG 已携带 X-WorkBuddy-Session-Id"}, 1)

    payload = do_rename(db_path, session_id, title, args.field, args.expect_old)
    emit(payload, 0 if payload.get("ok") else 1)


if __name__ == "__main__":
    main()
