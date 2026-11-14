#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""与上游 jailbreaks 仓库同步提示词语料。

判定链：
    1. git ls-remote 取上游 HEAD，与 data/sources.json 的 locked_sha 比对
    2. 无差异 -> 直接报告 UP_TO_DATE，不落盘、不克隆
    3. 有差异 -> --check 只列差异清单；--apply 才真正拉取并落盘
    4. 落盘后逐文件哈希比对，输出 新增 / 修改 / 删除 / 未变 四类
    5. 收口：重建索引、更新 sources.json、删除临时克隆目录

用法：
    python sync_upstream.py --check      # 只探测，不改动任何文件
    python sync_upstream.py --apply      # 拉取并落盘 + 重建索引
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import stat
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
PROMPTS_DIR = SKILL_DIR / "prompts"
SOURCES_FILE = SKILL_DIR / "data" / "sources.json"
REPO_URL = "https://github.com/togg53192-cmd/jailbreaks"
PROMPT_SUFFIXES = {".md", ".txt"}
SKIP_NAMES = {"README.md"}


def now_iso() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def write_json_atomic(path: Path, payload: dict) -> None:
    """先写临时文件再原子替换，避免并发读拿到残缺 JSON。"""
    temp_path = path.with_suffix(path.suffix + ".tmp")
    temp_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    os.replace(temp_path, path)


def run(cmd: list[str], cwd: Path | None = None) -> str:
    """执行外部命令，失败时抛出带原始输出的异常。"""
    try:
        result = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=180,
                                encoding="utf-8", errors="replace")
    except FileNotFoundError as exc:
        raise SystemExit(f"命令不可用：{cmd[0]}（请先确认 git 已安装）") from exc
    except subprocess.TimeoutExpired as exc:
        raise SystemExit(f"命令超时（180s）：{' '.join(cmd)}") from exc
    if result.returncode != 0:
        raise SystemExit(f"命令失败（{result.returncode}）：{' '.join(cmd)}\n{result.stderr.strip()}")
    return result.stdout.strip()


def remote_head() -> str:
    """取上游默认分支的最新 commit sha。"""
    output = run(["git", "ls-remote", REPO_URL, "HEAD"])
    if not output:
        raise SystemExit(f"无法从上游取到 HEAD：{REPO_URL}（检查网络或仓库可见性）")
    return output.split()[0]


def load_sources() -> dict:
    if not SOURCES_FILE.exists():
        return {}
    return json.loads(SOURCES_FILE.read_text(encoding="utf-8"))


def hash_file(path: Path) -> str:
    """按规范化后的内容取哈希：行尾统一为 LF。

    语料是文本资产，行尾差异属于传输噪声，不是内容变更。
    Windows 侧 git 的 autocrlf 会把克隆结果转成 CRLF，而 Linux 侧保持 LF；
    若不规范化，同一次同步在两侧会得出相反的差异清单，导致快照被反复重写。
    """
    return hashlib.sha256(path.read_bytes().replace(b"\r\n", b"\n")).hexdigest()


def local_snapshot() -> dict[str, str]:
    """本地 prompts/ 的文件名到哈希映射。"""
    if not PROMPTS_DIR.exists():
        return {}
    return {p.name: hash_file(p) for p in sorted(PROMPTS_DIR.iterdir()) if p.is_file()}


def collect_upstream(target: Path) -> dict[str, Path]:
    """上游文件映射到本地平铺命名。

    规则：子目录文件按「逐级目录名用 - 连接」加前缀，使上游目录调整时命名稳定。
    例：0x8D jailbreaks/BigPickle-opencode.md -> 0x8D-jailbreaks-BigPickle-opencode.md
    """
    mapping: dict[str, Path] = {}
    for path in sorted(target.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in PROMPT_SUFFIXES:
            continue
        if ".git" in path.parts or path.name in SKIP_NAMES:
            continue
        relative = path.relative_to(target)
        prefix = [part.replace(" ", "-") for part in relative.parts[:-1]]
        mapping["-".join(prefix + [path.name])] = path
    return mapping


def diff_sets(local: dict[str, str], remote: dict[str, Path]) -> dict[str, list[str]]:
    added = sorted(set(remote) - set(local))
    removed = sorted(set(local) - set(remote))
    changed = sorted(name for name in set(local) & set(remote) if hash_file(remote[name]) != local[name])
    unchanged = sorted(set(local) & set(remote) - set(changed))
    return {"added": added, "removed": removed, "changed": changed, "unchanged": unchanged}


def handle_remove_error(func, path, exc_info) -> None:
    """删除失败时先去掉只读位再重试。

    Windows 上 git 克隆出的 .git 内部对象默认带只读属性，
    shutil.rmtree 会静默失败并留下空壳目录，这一层是必需的。
    """
    try:
        os.chmod(path, stat.S_IWRITE | stat.S_IREAD)
        func(path)
    except OSError:
        pass


def remove_temp(temp_dir: Path) -> bool:
    """删除临时目录并回读确认，返回是否已彻底清除。"""
    for _ in range(2):
        if not temp_dir.exists():
            break
        shutil.rmtree(temp_dir, onerror=handle_remove_error)
    return not temp_dir.exists()


def report(diff: dict[str, list[str]], applied: bool) -> None:
    print(f"ADDED={len(diff['added'])} CHANGED={len(diff['changed'])} "
          f"REMOVED={len(diff['removed'])} UNCHANGED={len(diff['unchanged'])}")
    for name in diff["added"]:
        print("  + " + name)
    for name in diff["changed"]:
        print("  ~ " + name)
    for name in diff["removed"]:
        print("  - " + name + "（上游已删除，本地快照默认保留，需人工裁决）")
    print("APPLIED" if applied else "DRY_RUN（未改动任何文件，加 --apply 落盘）")


def apply_sync(remote: dict[str, Path], diff: dict[str, list[str]], sha: str) -> None:
    PROMPTS_DIR.mkdir(parents=True, exist_ok=True)
    for name in diff["added"] + diff["changed"]:
        # 统一以 LF 落盘：与上游一致，跨平台哈希才稳定
        content = remote[name].read_bytes().replace(b"\r\n", b"\n")
        (PROMPTS_DIR / name).write_bytes(content)
    snapshot = local_snapshot()
    payload = {
        "upstream": {
            "repo": REPO_URL,
            "locked_sha": sha,
            "locked_at": now_iso(),
            "last_checked_at": now_iso(),
            "file_count": len(snapshot),
            "total_bytes": sum((PROMPTS_DIR / n).stat().st_size for n in snapshot),
        },
        "last_sync": {
            "added": diff["added"],
            "changed": diff["changed"],
            "removed": diff["removed"],
        },
        "files": snapshot,
    }
    write_json_atomic(SOURCES_FILE, payload)
    print(f"SOURCES_WRITTEN={SOURCES_FILE}")
    run([sys.executable, str(SKILL_DIR / "scripts" / "build_index.py")])


def main() -> int:
    parser = argparse.ArgumentParser(description="同步上游 jailbreaks 提示词语料")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--check", action="store_true", help="只探测上游是否有更新")
    group.add_argument("--apply", action="store_true", help="拉取上游并落盘")
    args = parser.parse_args()

    sources = load_sources()
    locked = sources.get("upstream", {}).get("locked_sha", "")
    head = remote_head()
    print(f"UPSTREAM_HEAD={head}")
    print(f"LOCAL_LOCKED={locked or '（尚无锁定版本）'}")

    if locked and head == locked and args.check:
        print("UP_TO_DATE（上游无更新）")
        return 0

    temp_dir = Path(tempfile.mkdtemp(prefix="pojia-sync-"))
    clone_dir = temp_dir / "jailbreaks"
    try:
        run(["git", "clone", "--depth", "1", "--quiet", REPO_URL, str(clone_dir)])
        remote = collect_upstream(clone_dir)
        diff = diff_sets(local_snapshot(), remote)
        report(diff, applied=args.apply)
        has_change = any(diff[key] for key in ("added", "changed", "removed"))
        if args.apply and has_change:
            apply_sync(remote, diff, head)
            print("SYNC: PASS")
        elif args.apply:
            # 零变更时不重写 sources.json、不重建索引：
            # 否则每次 --apply 都会刷新时间戳，让「文件真的变了没」失去判据。
            print("NO_CHANGE（跳过落盘与索引重建，保持文件指纹稳定）")
        elif not has_change:
            print("UP_TO_DATE（上游内容与本地快照一致）")
    finally:
        # 临时克隆目录用完即删，并回读确认（runtime-process-cleanup-rules）
        print(f"TEMP_CLEANED={remove_temp(temp_dir)}")
    return 0


if __name__ == "__main__":
    # stdout 与 stderr 都要锁 UTF-8：SystemExit / argparse 的报错走 stderr，
    # 只改 stdout 会让中文错误在 GBK 控制台（chcp 936）上变成乱码。
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
    raise SystemExit(main())
