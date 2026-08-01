"""验证研发流程收敛后的活动路由、目录和文档 profile。"""

from __future__ import annotations

import json
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
RETIRED_SKILLS = (
    "acceptance-criteria-rules",
    "final-acceptance-rules",
    "implementation-review-rules",
    "project-change-review-rules",
    "code-review-automation-rules",
)
SKIP_DIRECTORIES = {".git", ".tmp", "doc", "downloaded-seeds", ".system"}
SKIP_FILES = {"PROJECT_HISTORY.md"}


# [参数] 无
# [返回] 生成活动文本文件及其仓库相对路径。
# 最近修改时间：2026-08-01 修正扫描根目录后排除非活动归档和临时索引。
def iter_active_files():
    # 1. 仅向活动规则和脚本提供可扫描的 UTF-8 文本候选。
    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        relative = path.relative_to(ROOT).as_posix()
        parts = set(path.relative_to(ROOT).parts)
        if parts & SKIP_DIRECTORIES or relative in SKIP_FILES:
            continue
        if path.suffix.lower() not in {".md", ".yaml", ".yml", ".py", ".sh", ".ps1", ".json"}:
            continue
        yield path, relative


# [参数] 无
# [返回] 返回退役 Skill 名称或编码问题的活动引用。
# 最近修改时间：2026-08-01 将编码异常转为可诊断的扫描失败结果。
def find_active_references() -> list[dict[str, str]]:
    findings: list[dict[str, str]] = []
    # 1. 逐文件识别退役入口，避免解码异常掩盖真实路径。
    for path, relative in iter_active_files():
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            findings.append({"path": relative, "retired_skill": "non_utf8_text"})
            continue
        for retired in RETIRED_SKILLS:
            if retired in text:
                findings.append({"path": relative, "retired_skill": retired})
    return findings


# [参数] fixture：包含待验证退役 Skill 名称的临时 fixture 文件。
# [返回] 退役名称不存在活动 `SKILL.md` 时返回 True。
# 最近修改时间：2026-08-01 明确负向触发 fixture 的拒绝判定。
def retired_trigger_is_rejected(fixture: Path) -> bool:
    # 1. fixture 只能命中已物理删除的退役 Skill。
    requested = fixture.read_text(encoding="utf-8")
    return all(
        not (ROOT / retired / "SKILL.md").exists()
        for retired in RETIRED_SKILLS
        if retired in requested
    )


# [参数] 无
# [返回] 全部流程收敛断言通过时返回 0，否则返回 1。
# 最近修改时间：2026-08-01 02:28:06；所有流程收敛断言必须共同决定退出状态。
def main() -> int:
    checks: dict[str, object] = {}

    # 1. 验证退役目录已删除，同时保留历史归档目录。
    missing_retired = [name for name in RETIRED_SKILLS if (ROOT / name).exists()]
    checks["retired_skill_directories_absent"] = not missing_retired
    checks["retired_skill_directories"] = {"missing": missing_retired}
    checks["legacy_archives_preserved"] = all(
        (ROOT / directory).is_dir() for directory in ("doc/6-审查", "doc/7-验收")
    )

    # 2. 验证活动文件不再保留退役路由。
    active_references = find_active_references()
    checks["active_reference_scan_zero"] = not active_references
    checks["active_references"] = active_references

    # 3. 验证唯一的 6-review 入口和负向触发行为。
    style_skill = (ROOT / "code-style-consistency-rules/SKILL.md").read_text(encoding="utf-8")
    style_contract = (ROOT / "code-style-consistency-rules/references/style-regression-contract.md").read_text(encoding="utf-8")
    profile = (ROOT / "artifact-delivery-gate-rules/references/document-quality-profiles.yaml").read_text(encoding="utf-8")
    checks["six_review_route"] = all(
        marker in style_skill or marker in style_contract or marker in profile
        for marker in ("6-review", "STYLE: PASS", "style_regression")
    )

    with tempfile.TemporaryDirectory(prefix="flow-streamlining-") as temporary:
        fixture = Path(temporary) / "retired.md"
        fixture.write_text("name: implementation-review-rules\n", encoding="utf-8")
        checks["retired_trigger_fixture_fails"] = retired_trigger_is_rejected(fixture)

    checks["style_regression_document_present"] = (
        ROOT / "doc/6-review/2026-08-01_000000_流程收敛_6-review.md"
    ).is_file()

    # 4. 将所有流程收敛的必需布尔断言统一收敛为稳定的 JSON 结果。
    required_checks = (
        "retired_skill_directories_absent",
        "legacy_archives_preserved",
        "active_reference_scan_zero",
        "six_review_route",
        "retired_trigger_fixture_fails",
        "style_regression_document_present",
    )
    failures = [name for name in required_checks if checks[name] is not True]
    result = {"ok": not failures, "failures": failures, "checks": checks}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
