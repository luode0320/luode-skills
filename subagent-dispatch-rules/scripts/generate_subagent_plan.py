#!/usr/bin/env python3
"""生成子 agent 启动计划。"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Any


DEFAULT_EXECUTION_SKILL = "subagent-dispatch-rules"
DEFAULT_TASK_NAME = "并行子任务"
MAX_TASK_NAME_LENGTH = 10
TRAILING_NOISE_WORDS = (
    "并测试",
    "测试",
    "脚本",
    "规则",
    "文档",
    "说明",
    "方案",
)


def configure_utf8_streams() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="根据线程拆分信息生成子 agent 启动计划。")
    parser.add_argument("--input", required=True, help="输入 JSON 路径。")
    parser.add_argument("--output", help="输出 JSON 路径；省略时打印到标准输出。")
    return parser.parse_args()


def load_input(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(f"输入文件不存在：{path}")

    raw = path.read_text(encoding="utf-8")
    data = json.loads(raw)
    if not isinstance(data, dict):
        raise ValueError("输入 JSON 根节点必须是对象。")
    return data


def compact_text(value: str) -> str:
    return " ".join(value.split()).strip()


def sanitize_task_name(task_summary: str) -> str:
    cleaned = compact_text(task_summary)
    trimmed = True
    while trimmed:
        trimmed = False
        for noise_word in TRAILING_NOISE_WORDS:
            if cleaned.endswith(noise_word) and len(cleaned) > len(noise_word) + 1:
                cleaned = cleaned[: -len(noise_word)]
                trimmed = True
                break

    chinese_chunks = re.findall(r"[\u4e00-\u9fff]+", cleaned)
    if chinese_chunks:
        preferred_text = "".join(chinese_chunks).strip()
        if preferred_text:
            return preferred_text[:MAX_TASK_NAME_LENGTH]

    fallback_chars = [char for char in cleaned if char.isalnum()]
    if fallback_chars:
        return "".join(fallback_chars)[:MAX_TASK_NAME_LENGTH] or DEFAULT_TASK_NAME

    return DEFAULT_TASK_NAME


def normalize_string_list(raw_value: Any, field_name: str) -> list[str]:
    if raw_value is None:
        return []
    if not isinstance(raw_value, list):
        raise ValueError(f"{field_name} 必须是字符串数组。")

    result: list[str] = []
    for item in raw_value:
        text = compact_text(str(item))
        if text:
            result.append(text)
    return result


def normalize_thread(thread_data: Any, task_name: str, shared_constraints: list[str]) -> dict[str, Any]:
    if not isinstance(thread_data, dict):
        raise ValueError("threads 中的每一项都必须是对象。")

    thread_id = compact_text(str(thread_data.get("thread", "")))
    if not thread_id:
        raise ValueError("threads[*].thread 不能为空。")

    goal = compact_text(str(thread_data.get("goal", "")))
    if not goal:
        raise ValueError(f"线程 {thread_id} 缺少 goal。")

    expected_output = compact_text(str(thread_data.get("expected_output", "")))
    if not expected_output:
        raise ValueError(f"线程 {thread_id} 缺少 expected_output。")

    write_scope = normalize_string_list(thread_data.get("write_scope"), f"线程 {thread_id} 的 write_scope")
    read_scope = normalize_string_list(thread_data.get("read_scope"), f"线程 {thread_id} 的 read_scope")
    extra_constraints = normalize_string_list(
        thread_data.get("extra_constraints"),
        f"线程 {thread_id} 的 extra_constraints",
    )

    raw_agent_type = compact_text(str(thread_data.get("agent_type", ""))).lower()
    if raw_agent_type:
        agent_type = raw_agent_type
    elif write_scope:
        agent_type = "worker"
    else:
        agent_type = "explorer"

    if agent_type not in {"worker", "explorer", "default"}:
        raise ValueError(f"线程 {thread_id} 的 agent_type 不支持：{agent_type}")

    launch_name = f"{task_name}-{thread_id}"
    message = build_agent_message(
        launch_name=launch_name,
        goal=goal,
        agent_type=agent_type,
        write_scope=write_scope,
        read_scope=read_scope,
        expected_output=expected_output,
        shared_constraints=shared_constraints,
        extra_constraints=extra_constraints,
    )

    return {
        "thread": thread_id,
        "agent_name": launch_name,
        "logical_agent_name": launch_name,
        "agent_type": agent_type,
        "goal": goal,
        "expected_output": expected_output,
        "write_scope": write_scope,
        "read_scope": read_scope,
        "shared_constraints": shared_constraints,
        "extra_constraints": extra_constraints,
        "message": message,
    }


def build_agent_message(
    launch_name: str,
    goal: str,
    agent_type: str,
    write_scope: list[str],
    read_scope: list[str],
    expected_output: str,
    shared_constraints: list[str],
    extra_constraints: list[str],
) -> str:
    lines = [
        f"逻辑子任务名：{launch_name}",
        "命名说明：",
        "- 该名称用于主 agent 跟踪，不等于平台显示昵称。",
        "任务目标：",
        f"- {goal}",
    ]

    if agent_type == "worker":
        lines.extend(
            [
                "写集边界：",
                f"- 仅允许修改：{', '.join(write_scope) if write_scope else '未指定，请保持只读'}",
                "- 你不是独自在代码库里，不要回退他人改动。",
            ]
        )
    elif read_scope:
        lines.extend(
            [
                "读取范围：",
                f"- {', '.join(read_scope)}",
            ]
        )

    if read_scope and agent_type == "worker":
        lines.extend(
            [
                "补充读取范围：",
                f"- {', '.join(read_scope)}",
            ]
        )

    all_constraints = shared_constraints + extra_constraints
    if all_constraints:
        lines.append("约束：")
        for constraint in all_constraints:
            lines.append(f"- {constraint}")

    lines.extend(
        [
            "输出要求：",
            f"- {expected_output}",
            "- 最终回复请列出你实际改动或核查的文件路径。",
        ]
    )
    return "\n".join(lines)


def build_plan(data: dict[str, Any]) -> dict[str, Any]:
    task_summary = compact_text(str(data.get("task_summary", "")))
    if not task_summary:
        raise ValueError("task_summary 不能为空。")

    raw_threads = data.get("threads")
    if not isinstance(raw_threads, list) or not raw_threads:
        raise ValueError("threads 必须是非空数组。")

    execution_skill = compact_text(str(data.get("execution_skill", DEFAULT_EXECUTION_SKILL))) or DEFAULT_EXECUTION_SKILL
    shared_constraints = normalize_string_list(data.get("shared_constraints"), "shared_constraints")
    task_name = sanitize_task_name(task_summary)

    threads = [normalize_thread(item, task_name, shared_constraints) for item in raw_threads]

    return {
        "task_name": task_name,
        "task_summary": task_summary,
        "execution_skill": execution_skill,
        "planned_thread_count": len(threads),
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "threads": threads,
    }


def write_output(plan: dict[str, Any], output_path: Path | None) -> None:
    text = json.dumps(plan, ensure_ascii=False, indent=2) + "\n"
    if output_path is None:
        sys.stdout.write(text)
        return

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(text, encoding="utf-8")


def main() -> int:
    configure_utf8_streams()
    args = parse_args()

    input_path = Path(args.input).expanduser().resolve()
    output_path = Path(args.output).expanduser().resolve() if args.output else None

    try:
        data = load_input(input_path)
        plan = build_plan(data)
        write_output(plan, output_path)
    except Exception as exc:  # noqa: BLE001
        print(f"生成子 agent 启动计划失败：{exc}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
