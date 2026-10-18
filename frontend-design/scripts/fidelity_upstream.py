#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""还原度守卫的上游参照物侧：取上游冻结 commit 的对象库字节、算清单，并管理离线基线读写。

[判据] 参照物只能是上游 git 对象库的原始 blob 字节：
    临时克隆会继承本机 core.autocrlf=true，工作树文件被展成 CRLF，
    直接读工作树会把参照物算错（本地 LF 反而全部判为漂移），因此统一走 cat-file。
    基线只能由联网模式生成并带清单指纹，离线模式拒绝非上游派生或指纹失配的基线，避免自证循环。

[边界] 本文件不扫描本地组件库，也不做漂移裁决；那两件事留在 verify_fidelity.py。
最近修改时间：2026-10-17 07:04:00；改动原因：登记 src/main.ts 的一行覆盖层引入缝隙，
使外壳留白缺陷可在不改冻结样式一个字节的口径下修复。
"""

import hashlib
import json
import subprocess
from pathlib import Path

COMMIT = "577079e9a347555fadddd3865fc0bbcdb00d9fb4"
UPSTREAM = "https://github.com/wbr664393425-lgtm/scaffold-master"
SUBTREE = "scaffold-vue"

ROOT = Path(__file__).resolve().parent.parent
LIB = ROOT / "component-library"
BASELINE = ROOT / "references" / "component-library-baseline.json"

# 基线溯源标签：只有由上游对象库派生的清单才被离线模式信任。
PROVENANCE = "upstream-git-blob"

# 本地受管例外：允许与上游内容漂移的配置层文件（不属于 src 视觉/行为还原面）。
# vite.config.ts 挂载本地 mock 插件；package-lock.json 由本机 npm 重写。
LOCAL_MANAGED = {"vite.config.ts", "package-lock.json"}

# 上游仓库根、按同路径收录进组件库的文件（设计契约与许可证）。
ROOT_TRACKED = {"DESIGN.md", "LICENSE"}

# 登记缝隙：上游把「sys_menu.component → 页面组件」的登记表写死在 auth.ts 里，
# 本地新增后台页面必须在此展开一次，否则页面无法被路由装配。
# 不按「整文件豁免」处理——那会让行为文件后续的真实改动静默不可见。
# 做法是声明出允许加入的精确行，校验时先把这些行剥掉，再要求剩余内容与上游逐字节相等。
SANCTIONED_SEAMS = {
    "src/composables/auth.ts": [
        "import { LOCAL_VIEWS } from '@/data/view-registry'",
        "  ...LOCAL_VIEWS,",
    ],
    # 上游冻结样式把外壳画成「深色描边 + 大外阴影」，但只给 8px 舞台留白，
    # 本地把后台整体改成组件库后外壳全程可见，阴影被裁成方形暗块。
    # 修复只能以「追加一行 import」的声明形式进入冻结入口，缝隙之外仍须逐字节等于上游。
    "src/main.ts": [
        "import './styles/overrides.css'",
    ],
}


def sh_bytes(args, cwd=None):
    """执行命令并以原始字节返回 stdout，避免文本模式把 CRLF 归一成 LF。

    [参数] args: 命令列表；cwd: 工作目录
    [返回] (returncode, stdout 字节, stderr 字节)
    最近修改时间：2026-10-16 20:05:00；改动原因：随守卫拆分迁移，判定口径不变。
    """
    # 1. 以捕获模式执行，退出码与两路输出全部按字节返回。
    p = subprocess.run(args, cwd=cwd, capture_output=True)
    return p.returncode, p.stdout, p.stderr


def ensure_clone(dest):
    """把上游仓库准备到 dest 并检出冻结 commit。

    [参数] dest: 本地克隆目录
    [返回] None；失败时抛 RuntimeError
    最近修改时间：2026-10-16 20:05:00；改动原因：随守卫拆分迁移，判定口径不变。
    """
    # 1. 缺对象库时先静默克隆上游仓库。
    if not (dest / ".git").exists():
        rc, _, err = sh_bytes(["git", "clone", "--quiet", UPSTREAM, str(dest)])
        if rc != 0:
            raise RuntimeError(f"clone 失败：{err[:200]!r}")
    # 2. 强制检出冻结 commit，排除本机分支漂移。
    rc, _, err = sh_bytes(["git", "-C", str(dest), "checkout", "--quiet", "--force", COMMIT])
    if rc != 0:
        raise RuntimeError(f"checkout {COMMIT[:12]} 失败：{err[:200]!r}")
    # 3. 回读 HEAD 自证检出的就是冻结提交。
    rc, head, _ = sh_bytes(["git", "-C", str(dest), "rev-parse", "HEAD"])
    if head.decode().strip() != COMMIT:
        raise RuntimeError(f"HEAD 与冻结 commit 不一致：{head.decode().strip()}")


def blob_sha(dest, gitpath):
    """取上游对象库里的原始 blob 字节并算 sha256。

    [参数] dest: 上游克隆目录；gitpath: 仓库内路径（如 scaffold-vue/src/main.ts）
    [返回] sha256 十六进制字符串
    最近修改时间：2026-10-16 20:25:00；改动原因：随守卫拆分迁移，判定口径不变。
    """
    # 1. 从对象库按 `commit:path` 取原始字节，绕开本机行尾转换配置。
    rc, blob, err = sh_bytes(["git", "-C", str(dest), "cat-file", "blob", f"{COMMIT}:{gitpath}"])
    if rc != 0:
        raise RuntimeError(f"上游 blob 读取失败：{gitpath} {err[:160]!r}")
    # 2. 对原始字节算哈希作为参照值。
    return hashlib.sha256(blob).hexdigest()


def upstream_hashes(dest):
    """枚举应纳入还原面的上游文件，逐文件从对象库算 sha256。

    [参数] dest: 上游克隆目录
    [返回] {相对组件库根的路径: sha256}
    最近修改时间：2026-10-16 20:05:00；改动原因：随守卫拆分迁移，判定口径不变。
    """
    # 1. 列出 subtree 内全部受管文件路径。
    rc, out, err = sh_bytes(["git", "-C", str(dest), "ls-tree", "-r", "--name-only", COMMIT, SUBTREE])
    if rc != 0:
        raise RuntimeError(f"ls-tree 失败：{err[:200]!r}")
    paths = [l for l in out.decode("utf-8").splitlines() if l.strip()]
    if not paths:
        raise RuntimeError("上游 subtree 为空，疑似上游路径或 commit 变更")
    # 2. 去掉 subtree 前缀得到组件库内相对路径，逐文件算哈希。
    mapping = {}
    for line in paths:
        rel = line[len(SUBTREE) + 1:]
        mapping[rel] = blob_sha(dest, line)
    # 3. 追加仓库根随行文件（设计契约与许可证）。
    for rel in sorted(ROOT_TRACKED):
        mapping[rel] = blob_sha(dest, rel)
    return mapping


def canonical(payload):
    """把清单序列化为稳定字节，用于计算清单自身指纹。

    [参数] payload: 可 JSON 化的 dict
    [返回] 排序后的紧凑 UTF-8 字节
    最近修改时间：2026-10-16 20:05:00；改动原因：随守卫拆分迁移，判定口径不变。
    """
    return json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def write_baseline(files):
    """把上游来源的清单落盘，并记录清单指纹防篡改。

    [参数] files: {路径: sha256}
    [返回] None
    最近修改时间：2026-10-16 20:05:00；改动原因：随守卫拆分迁移，判定口径不变。
    """
    # 1. 组装带溯源信息的清单载荷。
    payload = {
        "upstream_commit": COMMIT,
        "upstream_repo": UPSTREAM,
        "subtree": SUBTREE,
        "derived_from": PROVENANCE,
        "local_managed": sorted(LOCAL_MANAGED),
        "root_tracked": sorted(ROOT_TRACKED),
        "files": files,
    }
    # 2. 用去掉指纹字段自身的稳定字节算清单指纹。
    probe = {k: v for k, v in payload.items() if k != "manifest_sha256"}
    payload["manifest_sha256"] = hashlib.sha256(canonical(probe)).hexdigest()
    # 3. 显式按 UTF-8 字节落盘。
    BASELINE.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    BASELINE.write_bytes(text.encode("utf-8"))
    print(f"BASELINE_WRITTEN: {len(files)} files @ upstream {COMMIT[:12]}")


def read_baseline():
    """读取离线基线并校验其自身指纹，拒绝来路不明的基线。

    [参数] None
    [返回] dict 基线；不可用时返回 None 并打印原因
    最近修改时间：2026-10-16 20:05:00；改动原因：随守卫拆分迁移，判定口径不变。
    """
    # 1. 基线缺失时拒绝用本地文件自建，避免自证循环。
    if not BASELINE.exists():
        print("BASELINE_MISSING: 基线不存在；禁止用本地文件自建（会形成自证循环），请先联网运行本脚本")
        return None
    payload = json.loads(BASELINE.read_text(encoding="utf-8"))
    probe = {k: v for k, v in payload.items() if k != "manifest_sha256"}
    # 2. 溯源标签不符即判为不可信。
    if payload.get("derived_from") != PROVENANCE:
        print("BASELINE_UNTRUSTED: 基线未标记为上游派生，请联网重建")
        return None
    # 3. 清单指纹失配即判为被篡改。
    if payload.get("manifest_sha256") != hashlib.sha256(canonical(probe)).hexdigest():
        print("BASELINE_TAMPERED: 基线清单指纹不一致，请联网重建")
        return None
    return payload
