#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""按上游冻结 commit 把 component-library 恢复为逐字节一致内容，并以真实二进制读取取证。

[用法] python redrop_to_upstream.py [--dry-run]
[返回] 退出码 0=全部一致（或已恢复一致）；1=仍有真实内容差异。证据写入 references/redrop-report.json。
最近修改时间：2026-10-15；改动原因：独立对账发现本地全部文件被写成 CRLF，字节级还原不成立，需按上游原字节重落盘。
"""
import json
import subprocess
import sys
import tempfile
from pathlib import Path

COMMIT = "577079e9a347555fadddd3865fc0bbcdb00d9fb4"
REPO = Path(__file__).resolve().parent.parent
LIB = REPO / "component-library"
UP = "https://github.com/wbr664393425-lgtm/scaffold-master"
PREFIX = "scaffold-vue/"
# 本地受管例外：允许与上游漂移的配置层文件（不属于 src 视觉/行为还原面）。
OVERRIDES = {"vite.config.ts", "package-lock.json"}
# 本地自述文档：不冒充上游文件，改用独立文件名，避免覆盖上游 README。
LOCAL_GUIDE = "LOCAL-GUIDE.md"
REPORT = REPO / "references" / "redrop-report.json"


def sh_bytes(args, cwd=None):
    """执行命令并以原始字节返回 stdout，避免任何换行改写。

    [参数] args: 命令列表；cwd: 工作目录
    [返回] (returncode, stdout bytes, stderr bytes)
    """
    p = subprocess.run(args, cwd=cwd, capture_output=True)
    return p.returncode, p.stdout, p.stderr


def ensure_clone(dest):
    """把上游仓库克隆到固定临时目录，已存在则复用。

    [参数] dest: 克隆目标目录
    [返回] (ok, 说明文本)
    """
    if not (dest / ".git").exists():
        rc, _, err = sh_bytes(["git", "clone", "--quiet", UP, str(dest)])
        if rc != 0:
            return False, "CLONE_FAIL " + err.decode("utf-8", "replace")[:200]
    rc, out, _ = sh_bytes(["git", "-C", str(dest), "cat-file", "-t", COMMIT])
    if rc != 0 or out.strip() != b"commit":
        return False, "COMMIT_NOT_FOUND"
    return True, "CLONE_OK"


def upstream_tree(dest):
    """列出上游 commit 下 scaffold-vue 子树的全部文件路径。

    [参数] dest: 克隆目录
    [返回] [相对 scaffold-vue 的路径]
    """
    rc, out, _ = sh_bytes(["git", "-C", str(dest), "ls-tree", "-r", "--name-only", COMMIT, PREFIX[:-1]])
    if rc != 0:
        return []
    names = out.decode("utf-8").splitlines()
    return [n[len(PREFIX):] for n in names if n.startswith(PREFIX)]


def upstream_blob(dest, rel):
    """读取上游 commit 中某文件的原始字节。

    [参数] dest: 克隆目录；rel: 相对 scaffold-vue 的路径
    [返回] bytes；读取失败返回 None
    """
    rc, out, _ = sh_bytes(["git", "-C", str(dest), "cat-file", "blob", f"{COMMIT}:{PREFIX}{rel}"])
    return out if rc == 0 else None


def classify(up_bytes, local_bytes):
    """按字节比对结果分类差异类型。

    [参数] up_bytes: 上游字节；local_bytes: 本地字节（None 表示缺失）
    [返回] "identical" | "eol" | "content" | "missing"
    """
    if local_bytes is None:
        return "missing"
    if local_bytes == up_bytes:
        return "identical"
    if local_bytes.replace(b"\r\n", b"\n") == up_bytes.replace(b"\r\n", b"\n"):
        return "eol"
    return "content"


def main():
    dry = "--dry-run" in sys.argv[1:]
    dest = Path(tempfile.gettempdir()) / "pearl-upstream-facts"
    ok, note = ensure_clone(dest)
    if not ok:
        print(note)
        print("REDROP: BLOCKED")
        return 1
    files = upstream_tree(dest)
    if not files:
        print("REDROP: BLOCKED (empty upstream tree)")
        return 1

    stats = {"identical": 0, "eol": 0, "content": 0, "missing": 0, "restored": 0}
    content_drift, restored, skipped_override, guide_saved = [], [], [], []
    guide_target = LIB / LOCAL_GUIDE

    for rel in files:
        up_bytes = upstream_blob(dest, rel)
        if up_bytes is None:
            content_drift.append(f"CATFILE_FAIL {rel}")
            continue
        local_path = LIB / rel
        local_bytes = local_path.read_bytes() if local_path.exists() else None
        if rel in OVERRIDES:
            skipped_override.append(rel)
            continue
        state = classify(up_bytes, local_bytes)
        stats[state] += 1
        if state == "identical":
            continue
        if state == "content":
            content_drift.append(f"{rel} up={len(up_bytes)}B local={len(local_bytes) if local_bytes else 0}B")
            # README 是本地自述文档被覆盖的场景：先把本地内容保全到独立文件名，再恢复上游原文。
            if rel == "README.md" and local_bytes and not guide_target.exists():
                if not dry:
                    guide_target.write_bytes(local_bytes)
                guide_saved.append(LOCAL_GUIDE)
        if not dry:
            local_path.parent.mkdir(parents=True, exist_ok=True)
            local_path.write_bytes(up_bytes)
            restored.append(rel)
            stats["restored"] += 1

    report = {
        "upstream_commit": COMMIT,
        "upstream_file_count": len(files),
        "stats": stats,
        "skipped_overrides": sorted(skipped_override),
        "content_drift_not_restored": sorted(content_drift),
        "restored_count": len(restored),
        "local_guide_preserved": sorted(guide_saved),
        "dry_run": dry,
    }
    if not dry:
        REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    # 复核：重落盘后再逐字节比对一次，确保磁盘事实与上游一致。
    verify = {"identical": 0, "eol": 0, "content": 0, "missing": 0}
    bad = []
    for rel in files:
        if rel in OVERRIDES:
            continue
        up_bytes = upstream_blob(dest, rel)
        local_path = LIB / rel
        local_bytes = local_path.read_bytes() if local_path.exists() else None
        state = classify(up_bytes, local_bytes)
        verify[state] += 1
        if state != "identical":
            bad.append(f"{state} {rel}")

    print(f"UPSTREAM_COUNT={len(files)}")
    print(f"BEFORE={json.dumps(stats, ensure_ascii=False)}")
    print(f"VERIFY={json.dumps(verify, ensure_ascii=False)}")
    for line in bad[:20]:
        print(f"  RESIDUAL {line}")
    for line in content_drift[:20]:
        print(f"  DRIFT {line}")
    print(f"REPORT={REPORT}")
    print("REDROP: PASS" if not bad else "REDROP: FAIL")
    return 0 if not bad else 1


if __name__ == "__main__":
    sys.exit(main())
