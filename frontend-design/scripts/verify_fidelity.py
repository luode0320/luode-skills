#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""还原度守卫：把 component-library 与**上游真实字节**逐文件比对。

[用法]
    python verify_fidelity.py                 # 默认：联网取上游冻结 commit 逐字节对账（权威模式）
    python verify_fidelity.py --offline       # 离线：与基线清单比对（基线只能由联网模式生成）
    python verify_fidelity.py --write-baseline # 联网取上游并刷新基线清单
[返回] 退出码 0=还原度一致；1=存在缺失、内容漂移或基线不可信。
最近修改时间：2026-10-16 19:40:00；改动原因：上游参照物侧（常量、克隆、清单读写）拆到 fidelity_upstream.py，
本文件只保留本地扫描与三向对账裁决，回到 200 行基准内。
"""

import hashlib
import sys
import tempfile
from pathlib import Path

from fidelity_upstream import (
    COMMIT,
    LIB,
    LOCAL_MANAGED,
    SANCTIONED_SEAMS,
    ensure_clone,
    read_baseline,
    upstream_hashes,
    write_baseline,
)

SKIP_PARTS = {"node_modules", ".npm-cache", ".vite", "dist"}


def strip_seam(data, lines):
    """从文件字节里剥掉声明过的缝隙行（含其行尾），每种行尾只剥一次。

    [参数] data: 文件原始字节；lines: 允许加入的行文本列表。
    [返回] 剥离后的字节。
    最近修改时间：2026-10-16 20:05:00；改动原因：随守卫拆分迁移，判定口径不变。
    """
    # 1. 逐条声明行尝试剥离，优先匹配 CRLF 再匹配 LF。
    for line in lines:
        for sep in (b"\r\n", b"\n"):
            pat = line.encode("utf-8") + sep
            # 2. 每种行尾只剥一次，避免重复删除造成字节错位。
            if pat in data:
                data = data.replace(pat, b"", 1)
                break
    return data


def scan_local():
    """扫描本地组件库（排除构建与缓存产物），逐文件算 sha256。

    声明过缝隙的文件按「剥掉缝隙行之后」的字节算哈希，
    这样参照物仍是上游原始内容，缝隙之外的任何改动都会被判为漂移。

    [参数] None
    [返回] {相对路径: sha256}
    最近修改时间：2026-10-16 20:05:00；改动原因：随守卫拆分迁移，判定口径不变。
    """
    # 1. 组件库目录不存在时返回空清单，由入口判为失败。
    manifest = {}
    if not LIB.exists():
        return manifest
    for item in sorted(LIB.rglob("*")):
        # 2. 跳过目录与构建缓存产物，只保留还原面文件。
        if not item.is_file():
            continue
        if SKIP_PARTS.intersection(item.parts):
            continue
        # 3. 声明过缝隙的文件先剥缝隙行，再按剩余字节算哈希。
        rel = item.relative_to(LIB).as_posix()
        data = item.read_bytes()
        seam = SANCTIONED_SEAMS.get(rel)
        if seam:
            data = strip_seam(data, seam)
        manifest[rel] = hashlib.sha256(data).hexdigest()
    return manifest


def judge(reference, local):
    """以参照清单为准做三向对账并输出结论。

    [参数] reference: {路径: sha256}（上游或基线）；local: {路径: sha256}
    [返回] 退出码 int
    最近修改时间：2026-10-16 20:05:00；改动原因：随守卫拆分迁移，判定口径不变。
    """
    # 1. 先算四类差集：缺失、未声明漂移、受管覆盖、本地新增。
    missing = sorted(set(reference) - set(local))
    drifted = sorted(r for r in set(reference) & set(local) if local[r] != reference[r] and r not in LOCAL_MANAGED)
    overridden = sorted(r for r in set(reference) & set(local) if local[r] != reference[r] and r in LOCAL_MANAGED)
    extra = sorted(set(local) - set(reference))
    # 2. 逐条打印缺失与漂移，再据此判失败。
    for rel in missing:
        print(f"MISSING: {rel}")
    for rel in drifted:
        print(f"DRIFTED: {rel}")
    if missing or drifted:
        print(f"FIDELITY: FAIL (missing={len(missing)}, drifted={len(drifted)})")
        return 1
    # 3. 通过态下分别打印声明缝隙、受管覆盖与本地新增，保证漂移只以声明形式可见。
    print(f"FIDELITY: PASS ({len(local)} local / {len(reference)} upstream-tracked; upstream {COMMIT[:12]})")
    for rel in sorted(SANCTIONED_SEAMS):
        if rel in local and rel in reference:
            print(f"SEAM: {rel} (+{len(SANCTIONED_SEAMS[rel])} 行声明式登记缝隙，剥离后与上游逐字节相等)")
    for rel in overridden:
        print(f"OVERRIDE: {rel} (local-managed, declared)")
    for rel in extra:
        print(f"LOCAL_ONLY: {rel}")
    return 0


def main(argv):
    """入口：选择联网权威模式、离线模式或刷新基线。

    [参数] argv: 命令行参数列表
    [返回] 退出码 int
    最近修改时间：2026-10-16 20:05:00；改动原因：随守卫拆分迁移，判定口径不变。
    """
    # 1. 解析模式开关并扫描本地清单，目录缺失或为空直接失败。
    offline = "--offline" in argv
    refresh = "--write-baseline" in argv
    local = scan_local()
    if not local:
        print("FIDELITY: FAIL (组件库目录不存在或为空)")
        return 1
    # 2. 离线模式只信任上游派生且指纹相符的基线。
    if offline:
        baseline = read_baseline()
        if baseline is None:
            return 1
        print(f"MODE: offline (baseline @ upstream {baseline.get('upstream_commit', '')[:12]})")
        return judge(baseline["files"], local)
    # 3. 联网模式取上游对象库字节，不可用时提示改用离线模式。
    dest = Path(tempfile.gettempdir()) / "pearl-upstream-fidelity"
    try:
        ensure_clone(dest)
        files = upstream_hashes(dest)
    except RuntimeError as exc:
        print(f"UPSTREAM_UNAVAILABLE: {exc}")
        print("HINT: 联网不可用时改用 --offline，但离线只信任上游派生的基线")
        return 1
    # 4. 按需刷新基线后做对账裁决。
    print(f"MODE: online (upstream {len(files)} tracked files)")
    if refresh:
        write_baseline(files)
    return judge(files, local)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
