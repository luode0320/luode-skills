#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
env-bootstrap-check.py — WorkBuddy 环境配置自检与自动补齐（跨机器恢复）

背景：luode-skills 仓库的 skill 依赖本机 WorkBuddy 平台级配置（settings.json /
环境变量 / hook 脚本）。换电脑或环境重建后这些配置不会自动迁移，本脚本依据
references/workbuddy-env-manifest.md 的权威定义，从仓库 assets 自动检测并补齐。

用法：
  python3 env-bootstrap-check.py             # 只检测，输出报告（exit 0=完备 / 1=有缺失）
  python3 env-bootstrap-check.py --dry-run   # 检测 + 预览将执行的修复（不落盘）
  python3 env-bootstrap-check.py --fix       # 检测 + 自动补齐缺失项
  python3 env-bootstrap-check.py --home-dir <DIR>   # 覆盖 home 目录（测试/模拟新机器）
  python3 env-bootstrap-check.py --repo-root <DIR>  # 覆盖仓库根（默认脚本上溯两级）

检测项（6 项，权威定义见 references/workbuddy-env-manifest.md）：
  1. settings.json  autoCompactEnabled == true
  2. settings.json  hooks.Stop 含 summary-check.py 条目
  3. 环境变量 CODEBUDDY_CODE_MAX_TURNS == 1000
  4. 环境变量 CODEBUDDY_MAX_RETRIES == 15
  5. hook 脚本 ~/.workbuddy/hooks/summary-check.py 存在且与资产一致
  6. hook 脚本 ~/.workbuddy/hooks/ralph-stop.py 存在且与资产一致

安全边界：
  - settings.json 用 merge 写入（只改目标 key，保留其余配置，修改前备份 .bak-<ts>）
  - hooks.Stop 只追加缺失条目，不删除/覆盖已有条目
  - hook 脚本覆盖前备份旧版 .bak-<ts>（防止覆盖用户本地改动）
  - 非 Windows 平台的环境变量不自动改 shell 配置，--fix 时打印建议命令
依赖：Python 3 标准库，无第三方依赖。
"""

import argparse
import datetime
import hashlib
import json
import os
import shutil
import subprocess
import sys

# ---------------------------------------------------------------------------
# 常量（与 references/workbuddy-env-manifest.md 保持一致）
# ---------------------------------------------------------------------------

SETTINGS_REL = os.path.join(".workbuddy", "settings.json")   # 相对 home 目录（真实位置 ~/.workbuddy/settings.json）
HOOKS_DIR_REL = os.path.join(".workbuddy", "hooks")
# 注意：已移除 CODEBUDDY_AUTOCOMPACT_PCT_OVERRIDE / CODEBUDDY_PRE_MESSAGE_COMPACT_PCT。
# 这两个变量会把压缩阈值压到 60%/10%，导致频繁提前压缩 + 连续 abort（2026-08-23
# "频繁乱压缩 / 会话突然结束" 事故根因），禁止再写入，压缩阈值回归平台默认。
ENV_VARS = {
    "CODEBUDDY_CODE_MAX_TURNS": "1000",
    "CODEBUDDY_MAX_RETRIES": "15",
}
HOOK_ASSETS = ["summary-check.py", "ralph-stop.py"]
SUMMARY_HOOK_TAG = "summary-check-pmw002"

# ---------------------------------------------------------------------------
# 工具函数
# ---------------------------------------------------------------------------


def log(msg):
    print(msg)


def md5(path):
    try:
        h = hashlib.md5()
        with open(path, "rb") as f:
            for chunk in iter(lambda: f.read(65536), b""):
                h.update(chunk)
        return h.hexdigest()
    except Exception:
        return None


def backup(path):
    """复制一份 .bak-<时间戳> 备份；文件不存在则不备份。"""
    if not os.path.isfile(path):
        return None
    ts = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    bak = path + ".bak-" + ts
    try:
        shutil.copy2(path, bak)
        return bak
    except Exception:
        return None


def load_json(path):
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None


def save_json(path, data):
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return True
    except Exception:
        return False


# ---------------------------------------------------------------------------
# 检测器（每项返回 (status, detail)；status: ok / missing / mismatch）
# ---------------------------------------------------------------------------


def check_settings_autocompact(home_dir):
    path = os.path.join(home_dir, SETTINGS_REL)
    data = load_json(path)
    if data is None:
        return ("missing", "settings.json 不存在或无法解析")
    if data.get("autoCompactEnabled") is True:
        return ("ok", "autoCompactEnabled=true")
    return ("mismatch", "autoCompactEnabled=%r（目标 true）" % data.get("autoCompactEnabled"))


def check_settings_stop_hook(home_dir):
    path = os.path.join(home_dir, SETTINGS_REL)
    data = load_json(path)
    if data is None:
        return ("missing", "settings.json 不存在或无法解析")
    stop = (data.get("hooks") or {}).get("Stop") or []
    for entry in stop:
        cmds = (entry.get("hooks") or [])
        for c in cmds:
            if SUMMARY_HOOK_TAG in c.get("command", "") or "summary-check.py" in c.get("command", ""):
                return ("ok", "hooks.Stop 含 summary-check 条目")
    return ("missing", "hooks.Stop 缺 summary-check 条目（现有 %d 条）" % len(stop))


def _win_reg_get(name):
    """Windows 下读取 HKCU\\Environment 注册表值；不存在返回 None。"""
    try:
        out = subprocess.check_output(
            ["reg", "query", r"HKCU\Environment", "/v", name],
            stderr=subprocess.DEVNULL, text=True, timeout=10,
        )
        for line in out.splitlines():
            if name in line and "REG_SZ" in line:
                parts = line.split()
                if parts:
                    return parts[-1]
        return None
    except Exception:
        return None


def check_env_var(name, target):
    if sys.platform.startswith("win"):
        cur = _win_reg_get(name)
        if cur is None:
            return ("missing", "%s 未设置（注册表无此值）" % name)
        if cur == target:
            return ("ok", "%s=%s" % (name, cur))
        return ("mismatch", "%s=%s（目标 %s）" % (name, cur, target))
    # 非 Windows：读当前进程环境（无法判断持久化，仅提示）
    cur = os.environ.get(name)
    if cur == target:
        return ("ok", "%s=%s" % (name, cur))
    return ("missing", "%s=%r（目标 %s，未持久化需写 shell profile）" % (name, cur, target))


def check_hook_file(home_dir, name):
    target = os.path.join(home_dir, HOOKS_DIR_REL, name)
    asset = os.path.join(ASSETS_HOOKS_DIR, name)
    if not os.path.isfile(target):
        return ("missing", "%s 不存在（资产在 assets/hooks/）" % name)
    if not os.path.isfile(asset):
        return ("ok", "%s 存在但仓库无资产副本（不比对）" % name)
    if md5(target) == md5(asset):
        return ("ok", "%s 存在且与资产一致" % name)
    return ("mismatch", "%s 与资产内容不同（可能本地改过）" % name)


# ---------------------------------------------------------------------------
# 修复器（每项返回 (ok, detail)）
# ---------------------------------------------------------------------------


def fix_settings_autocompact(home_dir):
    path = os.path.join(home_dir, SETTINGS_REL)
    data = load_json(path)
    if data is None:
        data = {}
    if data.get("autoCompactEnabled") is True:
        return (True, "已是 true")
    backup(path)
    data["autoCompactEnabled"] = True
    if save_json(path, data):
        return (True, "已写入 autoCompactEnabled=true（merge，其余 key 保留）")
    return (False, "写入失败")


def fix_settings_stop_hook(home_dir):
    path = os.path.join(home_dir, SETTINGS_REL)
    data = load_json(path)
    if data is None:
        data = {}
    hooks = data.setdefault("hooks", {})
    stop = hooks.setdefault("Stop", [])
    for entry in stop:
        for c in (entry.get("hooks") or []):
            if "summary-check.py" in c.get("command", ""):
                return (True, "已存在，无需追加")
    backup(path)
    hook_path = os.path.join(home_dir, HOOKS_DIR_REL, "summary-check.py").replace("\\", "/")
    stop.append({"hooks": [{"type": "command",
                            "command": 'python3 "%s" # %s' % (hook_path, SUMMARY_HOOK_TAG)}]})
    if save_json(path, data):
        return (True, "已追加 hooks.Stop 条目（现有条目保留）")
    return (False, "写入失败")


def fix_env_var(name, value):
    if sys.platform.startswith("win"):
        try:
            subprocess.run(["setx", name, value], check=True,
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=30)
            return (True, "setx %s %s（重启新建进程后生效）" % (name, value))
        except Exception:
            return (False, "setx 失败")
    return (False, "非 Windows：请手动写入 shell profile：export %s=%s" % (name, value))


def fix_hook_file(home_dir, name):
    target = os.path.join(home_dir, HOOKS_DIR_REL, name)
    asset = os.path.join(ASSETS_HOOKS_DIR, name)
    if not os.path.isfile(asset):
        return (False, "仓库无资产 %s，无法补齐" % name)
    os.makedirs(os.path.dirname(target), exist_ok=True)
    if os.path.isfile(target) and md5(target) == md5(asset):
        return (True, "已存在且一致")
    backup(target)
    try:
        shutil.copy2(asset, target)
        return (True, "已复制 %s（旧版已备份）" % name)
    except Exception:
        return (False, "复制失败")


# ---------------------------------------------------------------------------
# 主流程
# ---------------------------------------------------------------------------

CHECKS = [
    ("settings.autoCompactEnabled", check_settings_autocompact, fix_settings_autocompact),
    ("settings.hooks.Stop.summary-check", check_settings_stop_hook, fix_settings_stop_hook),
    ("env.CODEBUDDY_CODE_MAX_TURNS",
     lambda h: check_env_var("CODEBUDDY_CODE_MAX_TURNS", ENV_VARS["CODEBUDDY_CODE_MAX_TURNS"]),
     lambda h: fix_env_var("CODEBUDDY_CODE_MAX_TURNS", ENV_VARS["CODEBUDDY_CODE_MAX_TURNS"])),
    ("env.CODEBUDDY_MAX_RETRIES",
     lambda h: check_env_var("CODEBUDDY_MAX_RETRIES", ENV_VARS["CODEBUDDY_MAX_RETRIES"]),
     lambda h: fix_env_var("CODEBUDDY_MAX_RETRIES", ENV_VARS["CODEBUDDY_MAX_RETRIES"])),
    ("hook.summary-check.py", lambda h: check_hook_file(h, "summary-check.py"),
     lambda h: fix_hook_file(h, "summary-check.py")),
    ("hook.ralph-stop.py", lambda h: check_hook_file(h, "ralph-stop.py"),
     lambda h: fix_hook_file(h, "ralph-stop.py")),
]


def main():
    global ASSETS_HOOKS_DIR
    parser = argparse.ArgumentParser(description="WorkBuddy 环境配置自检与自动补齐")
    parser.add_argument("--check", action="store_true", help="只检测（默认）")
    parser.add_argument("--dry-run", action="store_true", help="检测 + 预览修复计划，不落盘")
    parser.add_argument("--fix", action="store_true", help="检测 + 自动补齐")
    parser.add_argument("--home-dir", default=os.path.expanduser("~"), help="home 目录（默认 ~）")
    parser.add_argument("--repo-root", default=None, help="luode-skills 仓库根（默认脚本上溯两级）")
    args = parser.parse_args()

    if args.repo_root:
        repo_root = os.path.abspath(args.repo_root)
    else:
        repo_root = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
    ASSETS_HOOKS_DIR = os.path.join(repo_root, "skill-absorption-rules", "assets", "hooks")

    home_dir = os.path.abspath(args.home_dir)
    mode = "fix" if args.fix else ("dry-run" if args.dry_run else "check")

    log("=" * 60)
    log("WorkBuddy 环境配置自检 | 模式=%s" % mode)
    log("home_dir   = %s" % home_dir)
    log("repo_root  = %s" % repo_root)
    log("assets     = %s" % ASSETS_HOOKS_DIR)
    log("=" * 60)

    results = []
    for name, checker, fixer in CHECKS:
        status, detail = checker(home_dir)
        results.append((name, status, detail))
        mark = {"ok": "PASS", "missing": "MISS", "mismatch": "DIFF"}.get(status, "?")
        log("  [%s] %-36s %s" % (mark, name, detail))

    has_issue = any(s != "ok" for _, s, _ in results)
    log("-" * 60)

    if not has_issue:
        log("全部 %d 项配置完备，无需处理。exit=0" % len(CHECKS))
        return 0

    if mode == "check":
        log("存在 %d 项缺失/不一致。可运行 --dry-run 预览修复，或 --fix 自动补齐。" %
            sum(1 for _, s, _ in results if s != "ok"))
        return 1

    # dry-run / fix：逐项执行修复器
    fixed = 0
    failed = 0
    for name, status, detail in results:
        if status == "ok":
            continue
        fixer_fn = dict((n, f) for n, _, f in CHECKS)[name]
        if mode == "dry-run":
            log("  [计划] %-36s -> %s" % (name, detail))
            continue
        ok, msg = fixer_fn(home_dir)
        if ok:
            fixed += 1
            log("  [修复] %-36s %s" % (name, msg))
        else:
            failed += 1
            log("  [失败] %-36s %s" % (name, msg))

    if mode == "dry-run":
        log("以上为将执行的修复计划（未落盘）。确认后运行 --fix。exit=2")
        return 2

    # fix 完成后复检
    log("-" * 60)
    log("复检：")
    remaining = 0
    for name, checker, _ in CHECKS:
        status, detail = checker(home_dir)
        if status != "ok":
            remaining += 1
            log("  [%s] %-36s %s" % ({"ok": "PASS", "missing": "MISS", "mismatch": "DIFF"}[status], name, detail))
    if remaining == 0:
        log("复检全部通过。环境配置已恢复完备。exit=0")
        return 0
    log("仍有 %d 项未恢复（多为环境变量需重启或非 Windows 手动配置）。exit=1" % remaining)
    return 1


if __name__ == "__main__":
    sys.exit(main())
