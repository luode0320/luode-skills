"""ASCII-only local fake used only by the adapter contract tests."""

from __future__ import annotations

import os
import sys
import time
from pathlib import Path


MODE = os.environ.get("FAKE_OBSIDIAN_MODE", "")
STATE_PATH = Path(os.environ["FAKE_OBSIDIAN_STATE"])
READY_PATH = os.environ.get("FAKE_OBSIDIAN_READY", "")
VAULTS = os.environ.get("FAKE_OBSIDIAN_VAULTS", "")
READ_BYTES = int(os.environ.get("FAKE_OBSIDIAN_READ_BYTES", "0"))
DEBUG_PATH = os.environ.get("FAKE_OBSIDIAN_DEBUG", "")


def main(arguments: list[str]) -> int:
    """Emulate the narrow CLI contract without opening a real vault.

    [参数] arguments: argv received by the fake CLI.
    [返回] Process exit code for the requested contract scenario.
    Last modified: 2026-07-13 18:38:00. Mirror append's implicit leading newline for long-body readback.
    """
    # 1. Capture argv before mode-specific behavior so contract tests can detect PowerShell argument splitting.
    if DEBUG_PATH:
        with Path(DEBUG_PATH).open("a", encoding="utf-8") as debug_file:
            debug_file.write(repr(arguments) + "\n")
    if not arguments:
        if READY_PATH:
            Path(READY_PATH).write_text("ready", encoding="utf-8")
        return 0
    if MODE == "timeout":
        time.sleep(3)
    if MODE == "cli_failed":
        print("fake cli failure", file=sys.stderr)
        return 9
    if arguments[0] == "version":
        if MODE == "semantic_error":
            sys.stdout.write("Error: fake version failure")
            return 0
        if MODE == "app_unavailable" and (not READY_PATH or not Path(READY_PATH).exists()):
            print("The CLI is unable to find Obsidian", file=sys.stderr)
            return 1
        sys.stdout.write("fake-1.0")
        return 0
    if arguments[:2] == ["vaults", "verbose"]:
        if MODE == "vaults_semantic_error":
            sys.stdout.write("Error: fake vault listing failure")
            return 0
        entries = VAULTS or r"main|D:\obsidian_data"
        for entry in entries.split(";"):
            selector, root = entry.split("|", 1)
            sys.stdout.write(selector + "\t" + root + "\n")
        return 0
    commands = {"search", "search:context", "read", "create", "append", "open"}
    command_index = next((index for index, value in enumerate(arguments) if value in commands), -1)
    if command_index < 0:
        print("unknown command", file=sys.stderr)
        return 2
    command = arguments[command_index]
    content = next((value[8:] for value in arguments[command_index + 1 :] if value.startswith("content=")), "")
    if MODE == "write_semantic_error" and command in {"create", "append"}:
        sys.stdout.write("Error: fake write failure")
        return 0
    if command == "create":
        STATE_PATH.write_text(content, encoding="utf-8")
        return 0
    if command == "append":
        # 1. 官方 append 会在追加正文前补一个换行，fake 必须保持同一契约。
        with STATE_PATH.open("a", encoding="utf-8") as state_file:
            state_file.write("\n" + content)
        return 0
    if command == "read":
        if MODE == "readback_mismatch":
            sys.stdout.write("different")
        elif MODE == "error_like_content":
            sys.stdout.write("Error: saved user content")
        elif READ_BYTES:
            sys.stdout.write("x" * READ_BYTES)
        elif STATE_PATH.exists():
            sys.stdout.write(STATE_PATH.read_text(encoding="utf-8"))
        return 0
    if command in {"search", "search:context"}:
        expected_query = os.environ.get("FAKE_OBSIDIAN_EXPECT_QUERY")
        expected_limit = os.environ.get("FAKE_OBSIDIAN_EXPECT_LIMIT")
        if expected_query and expected_limit:
            expected_arguments = {f"query={expected_query}", f"limit={expected_limit}"}
            actual_arguments = set(arguments[command_index + 1 :])
            if not expected_arguments.issubset(actual_arguments):
                print("query or limit was split", file=sys.stderr)
                return 2
        sys.stdout.write("fake search result")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
