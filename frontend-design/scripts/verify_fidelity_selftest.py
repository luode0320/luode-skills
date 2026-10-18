#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""还原度守卫的反向自证：注入漂移后，守卫必须以**明确原因**失败，全部还原后必须重新 PASS。

[用法] python verify_fidelity_selftest.py
[返回] 退出码 0=七类断言全部符合预期；1=存在"该红不红"或"还原后仍红"的守卫失效。
最近修改时间：2026-10-15 04:42:00；改动原因：首版自测将基线备份写在脚本内、崩溃时未还原，
且只看退出码不看原因串，导致一份预先损坏的基线被误判成"篡改已拦截"。本版加前置对账、
仓库外备份与 finally 还原。
"""

import json
import subprocess
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
GUARD = REPO / "frontend-design" / "scripts" / "verify_fidelity.py"
LIB = REPO / "frontend-design" / "component-library"
BASELINE = REPO / "frontend-design" / "references" / "component-library-baseline.json"
VICTIM = LIB / "src" / "components" / "ui" / "Segmented.vue"

EXPECTED_FILES = 139
EXPECTED_PROVENANCE = "upstream-git-blob"

failures = []


def run_guard(args):
    """跑守卫并返回 (退出码, 合并后的输出文本)。

    [参数] args: 传给守卫的参数列表
    [返回] (returncode, stdout+stderr)
    """
    p = subprocess.run([sys.executable, str(GUARD), *args], capture_output=True)
    text = (p.stdout or b"").decode("utf-8", "replace") + (p.stderr or b"").decode("utf-8", "replace")
    return p.returncode, text


def require(name, cond, detail=""):
    """记录一条断言并在失败时保留原因。

    [参数] name: 断言名；cond: 是否为真；detail: 失败诊断
    [返回] None
    """
    print(f"{'OK  ' if cond else 'BAD '} {name} {detail}".rstrip())
    if not cond:
        failures.append(name)


def main():
    """按"前置对账 → 四类注入 → 全量还原"顺序自证守卫有效性。

    [参数] None
    [返回] 退出码 int
    """
    if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    baseline_bytes = BASELINE.read_bytes()
    victim_bytes = VICTIM.read_bytes()
    sandbox = Path(tempfile.gettempdir()) / "pearl-fidelity-selftest-backup"
    sandbox.mkdir(parents=True, exist_ok=True)
    (sandbox / "baseline.json").write_bytes(baseline_bytes)
    (sandbox / "Segmented.vue").write_bytes(victim_bytes)

    try:
        payload = json.loads(baseline_bytes.decode("utf-8"))
        require("baseline_provenance", payload.get("derived_from") == EXPECTED_PROVENANCE,
                f"derived_from={payload.get('derived_from')!r}")
        require("baseline_file_count", len(payload.get("files", {})) == EXPECTED_FILES,
                f"files={len(payload.get('files', {}))}")

        # 前置对账：未篡改的基线必须先放行，否则后面的"拒绝"毫无意义
        rc, out = run_guard(["--offline"])
        require("pristine_baseline_accepted", rc == 0 and "FIDELITY: PASS" in out, f"rc={rc}")

        # 1. 基线指纹防篡改：改掉一个哈希后离线模式必须点明指纹问题
        tampered = json.loads(baseline_bytes.decode("utf-8"))
        first_key = sorted(tampered["files"])[0]
        tampered["files"][first_key] = "0" * 64
        BASELINE.write_text(json.dumps(tampered, ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8")
        rc, out = run_guard(["--offline"])
        require("tampered_baseline_rejected", rc == 1 and "BASELINE_TAMPERED" in out,
                f"rc={rc} first={out.strip().splitlines()[:1]}")

        # 2. 溯源标签造假：指纹重算也过不了，因为来源标记不再等于上游 blob
        forged = json.loads(baseline_bytes.decode("utf-8"))
        forged["derived_from"] = "local-files"
        body = {k: v for k, v in forged.items() if k != "manifest_sha256"}
        forged["manifest_sha256"] = __import__("hashlib").sha256(
            json.dumps(body, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
        ).hexdigest()
        BASELINE.write_text(json.dumps(forged, ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8")
        rc, out = run_guard(["--offline"])
        require("self_derived_baseline_rejected", rc == 1 and "BASELINE_UNTRUSTED" in out,
                f"rc={rc} first={out.strip().splitlines()[:1]}")
    finally:
        BASELINE.write_bytes(baseline_bytes)
        VICTIM.write_bytes(victim_bytes)

    # 3. 基线还原后必须重新放行（防止把"恢复"当成功、实际留下坏盘）
    rc, out = run_guard(["--offline"])
    require("baseline_restored_pass", rc == 0 and "FIDELITY: PASS" in out, f"rc={rc}")

    try:
        # 4. 本地内容漂移
        VICTIM.write_bytes(victim_bytes + b"\n<!-- drift probe -->\n")
        rc, out = run_guard(["--offline"])
        hit = [l for l in out.splitlines() if l.startswith("DRIFTED")]
        require("local_drift_detected", rc == 1 and bool(hit), f"rc={rc} hit={hit[:1]}")
    finally:
        VICTIM.write_bytes(victim_bytes)

    try:
        # 5. 本地文件缺失
        stash = LIB / "src" / "components" / "ui" / ".Segmented.vue.selftest"
        VICTIM.rename(stash)
        try:
            rc, out = run_guard(["--offline"])
            hit = [l for l in out.splitlines() if l.startswith("MISSING")]
            require("local_missing_detected", rc == 1 and bool(hit), f"rc={rc} hit={hit[:1]}")
        finally:
            stash.rename(VICTIM)
    finally:
        if not VICTIM.exists() and victim_bytes:
            VICTIM.write_bytes(victim_bytes)

    try:
        # 6. 行尾污染（LF→CRLF）：这正是当初报 PASS 的那类缺陷
        VICTIM.write_bytes(victim_bytes.replace(b"\n", b"\r\n"))
        rc, out = run_guard(["--offline"])
        hit = [l for l in out.splitlines() if l.startswith("DRIFTED")]
        require("crlf_drift_detected", rc == 1 and bool(hit), f"rc={rc} hit={hit[:1]}")
    finally:
        VICTIM.write_bytes(victim_bytes)

    # 7. 全量还原后，离线与联网都必须重新 PASS
    rc_off, out_off = run_guard(["--offline"])
    rc_on, out_on = run_guard([])
    require("restore_offline_pass", rc_off == 0 and "FIDELITY: PASS" in out_off, f"rc={rc_off}")
    require("restore_online_pass", rc_on == 0 and "FIDELITY: PASS" in out_on, f"rc={rc_on}")

    ok = not failures
    print("GUARD_SELFTEST: " + ("PASS" if ok else f"FAIL {failures}"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
