#!/usr/bin/env python3
"""long-run-loop-rules: loop_controller.py

主控制器状态管理脚本。管理状态文件的生命周期，支持 start/record-iteration/status/stop 命令。

用法:
    python loop_controller.py start --task-sha256 <hash> --goal-objective <text> --completion-marker <marker> [--max-iterations 50]
    python loop_controller.py record-iteration --task-sha256 <hash> --thread-id <id> --summary <text> [--cost 0.0]
    python loop_controller.py status --task-sha256 <hash>
    python loop_controller.py stop --task-sha256 <hash> --status <done|blocked|limited>

状态文件路径: $CODEX_HOME/state/long-run-loop/<task-sha256>.json
"""

import argparse
import json
import os
import sys
import hashlib
from datetime import datetime, timezone, timedelta

BEIJING_TZ = timezone(timedelta(hours=8))

DEFAULT_CONFIG = {
    "max_iterations": 50,
    "checkpoint_interval": 10,
    "dead_loop_window": 5,
    "dead_loop_similarity_threshold": 0.95,
    "cost_alert_thresholds": [10, 50, 100],
    "rate_limit_per_hour": 100,
    "max_runtime_minutes": 480,
    "worker_timeout_minutes": 30,
}


def _get_state_dir():
    """获取状态文件目录。"""
    codex_home = os.environ.get("CODEX_HOME")
    if codex_home:
        d = os.path.join(codex_home, "state", "long-run-loop")
    else:
        # fallback: 当前用户 home 目录
        d = os.path.join(os.path.expanduser("~"), ".codex", "state", "long-run-loop")
    os.makedirs(d, exist_ok=True)
    return d


def _get_state_path(task_sha256):
    return os.path.join(_get_state_dir(), f"{task_sha256}.json")


def _now_iso():
    return datetime.now(BEIJING_TZ).isoformat()


def _make_default_state(task_sha256, goal_objective, completion_marker, config_override=None):
    config = dict(DEFAULT_CONFIG)
    if config_override:
        config.update(config_override)
    return {
        "version": 1,
        "task_sha256": task_sha256,
        "goal_objective": goal_objective,
        "completion_marker": completion_marker,
        "config": config,
        "current_iteration": 0,
        "worker_thread_ids": [],
        "worker_summaries": [],
        "total_cost_estimate": 0.0,
        "dead_loop_count": 0,
        "started_at": _now_iso(),
        "last_updated": _now_iso(),
        "status": "active",
    }


def _read_state(task_sha256):
    path = _get_state_path(task_sha256)
    if not os.path.exists(path):
        print(json.dumps({"error": "state file not found", "path": path}))
        sys.exit(1)
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def _write_state(state):
    path = _get_state_path(state["task_sha256"])
    state["last_updated"] = _now_iso()
    with open(path, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)


def cmd_start(args):
    # 只在参数显式传入时才覆盖默认值，避免把未传参数覆盖成 None
    config_override = {}
    if args.max_iterations is not None:
        config_override["max_iterations"] = args.max_iterations
    if args.checkpoint_interval is not None:
        config_override["checkpoint_interval"] = args.checkpoint_interval
    if args.max_runtime_minutes is not None:
        config_override["max_runtime_minutes"] = args.max_runtime_minutes

    state = _make_default_state(
        task_sha256=args.task_sha256,
        goal_objective=args.goal_objective,
        completion_marker=args.completion_marker,
        config_override=config_override or None,
    )
    _write_state(state)
    print(json.dumps({"status": "created", "task_sha256": args.task_sha256, "path": _get_state_path(args.task_sha256)}))


def cmd_record_iteration(args):
    state = _read_state(args.task_sha256)
    if state["status"] != "active":
        print(json.dumps({"error": f"state is not active: {state['status']}", "status": state["status"]}))
        sys.exit(1)

    state["current_iteration"] += 1
    if args.thread_id:
        state["worker_thread_ids"].append(args.thread_id)
    if args.summary:
        state["worker_summaries"].append(args.summary)
    if args.cost is not None:
        state["total_cost_estimate"] += args.cost

    _write_state(state)
    print(json.dumps({
        "status": "recorded",
        "current_iteration": state["current_iteration"],
        "total_cost_estimate": state["total_cost_estimate"],
    }))


def cmd_status(args):
    state = _read_state(args.task_sha256)
    print(json.dumps(state, ensure_ascii=False, indent=2))


def cmd_stop(args):
    state = _read_state(args.task_sha256)
    if args.status not in ("done", "blocked", "limited"):
        print(json.dumps({"error": f"invalid status: {args.status}, expected done/blocked/limited"}))
        sys.exit(1)
    state["status"] = args.status
    if args.reason:
        state["stop_reason"] = args.reason
    _write_state(state)
    print(json.dumps({"status": "stopped", "final_status": args.status, "reason": args.reason or ""}))


def main():
    parser = argparse.ArgumentParser(description="long-run-loop-rules: loop controller")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # start
    p_start = subparsers.add_parser("start", help="create a new loop state file")
    p_start.add_argument("--task-sha256", required=True, help="unique task identifier (sha256)")
    p_start.add_argument("--goal-objective", required=True, help="Goal objective text")
    p_start.add_argument("--completion-marker", required=True, help="completion marker string")
    p_start.add_argument("--max-iterations", type=int, default=None, help="max iterations (default: 50)")
    p_start.add_argument("--checkpoint-interval", type=int, default=None, help="checkpoint interval (default: 10)")
    p_start.add_argument("--max-runtime-minutes", type=int, default=None, help="max runtime in minutes (default: 480)")

    # record-iteration
    p_record = subparsers.add_parser("record-iteration", help="record a worker iteration")
    p_record.add_argument("--task-sha256", required=True)
    p_record.add_argument("--thread-id", default=None, help="worker thread ID")
    p_record.add_argument("--summary", default=None, help="worker iteration summary")
    p_record.add_argument("--cost", type=float, default=None, help="estimated cost for this iteration")

    # status
    p_status = subparsers.add_parser("status", help="show current loop state")
    p_status.add_argument("--task-sha256", required=True)

    # stop
    p_stop = subparsers.add_parser("stop", help="stop the loop")
    p_stop.add_argument("--task-sha256", required=True)
    p_stop.add_argument("--status", required=True, choices=["done", "blocked", "limited"])
    p_stop.add_argument("--reason", default=None, help="stop reason")

    args = parser.parse_args()

    if args.command == "start":
        cmd_start(args)
    elif args.command == "record-iteration":
        cmd_record_iteration(args)
    elif args.command == "status":
        cmd_status(args)
    elif args.command == "stop":
        cmd_stop(args)


if __name__ == "__main__":
    main()
