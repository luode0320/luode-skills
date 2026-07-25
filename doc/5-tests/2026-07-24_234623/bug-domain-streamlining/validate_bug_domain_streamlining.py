#!/usr/bin/env python3
"""只验证本轮 Bug 风险入口合并资产；历史周期的旧引用明确不在扫描范围。"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


REQUIRED_TARGETS = (
    "bug-fix-proposal-rules/references/regression-risk.md",
    "bug-fix-proposal-rules/references/regression-risk/risk-dimensions.md",
    "bug-fix-proposal-rules/references/regression-risk/risk-examples.md",
    "bug-fix-proposal-rules/references/regression-risk/risk-ranking-and-scope.md",
)
REQUIRED_ROUTE_TOKENS = (
    "## 条件路由：regression-risk",
    "公共方法",
    "共享模块",
    "兼容",
    "异常语义",
)
REQUIRED_INTAKE_ROUTE_TOKENS = {
    "bug-intake-rules/references/discovery-and-gap.md": (
        "仅在 intake 完成现象标准化后",
        "只使用 local 配置",
        "只读侦察",
        "runtime-diagnostics",
        "test-regression-rules",
        "bug-validation-rules",
    ),
    "bug-intake-rules/references/runtime-diagnostics.md": (
        "静态证据不足",
        "只使用 local 配置",
        "临时资产必须可清理",
        "bug-root-cause-rules",
        "test-regression-rules",
        "bug-validation-rules",
    ),
}


def digest(path: Path) -> str:
    """[参数] path：待计算哈希的本地文件路径；[返回] 文件 SHA-256 摘要；最近修改时间：2026-07-25。"""
    return hashlib.sha256(path.read_bytes()).hexdigest()


def fail(errors: list[str], message: str) -> None:
    """[参数] errors：错误列表，message：待追加的错误说明；[返回] 无；最近修改时间：2026-07-25。"""
    errors.append(message)


def main() -> int:
    """[参数] 无；[返回] 本地专项验证退出码；最近修改时间：2026-07-25。"""
    parser = argparse.ArgumentParser()
    # 1. 解析输入、读取冻结清单，并按阶段核对保留资产与已删除入口。
    parser.add_argument("--repo-root", type=Path, required=True)
    parser.add_argument(
        "--phase",
        choices=("baseline", "intake-contract", "pre-delete", "post-delete"),
        required=True,
    )
    args = parser.parse_args()
    root = args.repo_root.resolve()
    here = Path(__file__).resolve().parent
    inventory = json.loads((here / "inventory.json").read_text(encoding="utf-8"))
    errors: list[str] = []
    source_dir = root / inventory["retire_directory"]

    if args.phase in ("baseline", "pre-delete"):
        if not source_dir.is_dir():
            fail(errors, "旧风险目录缺失")
        for asset in inventory["source_assets"]:
            path = root / asset["path"]
            if not path.is_file():
                fail(errors, f"源资产缺失: {asset['path']}")
            elif args.phase == "baseline" and digest(path) != asset["sha256"]:
                fail(errors, f"源资产哈希不匹配: {asset['path']}")

    if args.phase in ("pre-delete", "post-delete"):
        for path_text in REQUIRED_TARGETS:
            if not (root / path_text).is_file():
                fail(errors, f"目标资产缺失: {path_text}")
        target = root / "bug-fix-proposal-rules/SKILL.md"
        text = target.read_text(encoding="utf-8") if target.is_file() else ""
        for token in REQUIRED_ROUTE_TOKENS:
            if token not in text:
                fail(errors, f"目标路由缺少语义: {token}")
        for consumer in inventory["active_consumers"]:
            path = root / consumer
            if path.is_file() and "bug-regression-risk-rules" in path.read_text(encoding="utf-8"):
                fail(errors, f"活跃消费者残留旧入口: {consumer}")

    if args.phase == "post-delete" and source_dir.exists():
        fail(errors, "post-delete 时旧风险目录仍存在")

    fixtures = json.loads((here / "trigger-fixtures.json").read_text(encoding="utf-8"))
    if len(fixtures.get("fixtures", [])) != 5:
        fail(errors, "触发 fixture 数量不是 5")
    for route_path, tokens in REQUIRED_INTAKE_ROUTE_TOKENS.items():
        path = root / route_path
        text = path.read_text(encoding="utf-8") if path.is_file() else ""
        for token in tokens:
            if token not in text:
                fail(errors, f"intake 路由缺少语义: {route_path}: {token}")
    if errors:
        print("FAIL")
        print("\n".join(f"- {item}" for item in errors))
        return 1
    print(f"PASS phase={args.phase} assets={len(inventory['source_assets'])} fixtures=5")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
