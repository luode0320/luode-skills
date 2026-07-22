from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

import yaml

# CYCLE-SS-05 只允许四个 owner 下沉重复证据细则；自动化审查入口保持专责。
REFERENCE_REFACTOR_SOURCES = {
    "implementation-review-rules",
    "project-change-review-rules",
    "acceptance-criteria-rules",
    "final-acceptance-rules",
}
RETAIN_SPECIALIZED_SOURCE = "code-review-automation-rules"
SOURCES = REFERENCE_REFACTOR_SOURCES | {RETAIN_SPECIALIZED_SOURCE}
REQUIRED_PRESERVED = {"自动触发别名", "用户习惯", "授权与停止边界", "输出与证据归档", "审查或验收边界"}
REQUIRED_PROTECTED_TERMS = ("自动触发", "用户习惯", "授权", "安全", "停止", "输出", "证据归档")


def parse_args() -> argparse.Namespace:
    """[参数]：无，读取命令行；[返回]：验证参数；最近修改时间：2026-07-21。"""
    # 1. 阶段受限，避免把 baseline 当作已完成 route 迁移。
    parser = argparse.ArgumentParser(description="验证周期05审查与验收域资产和条件路由")
    parser.add_argument("--repo-root", required=True)
    parser.add_argument("--manifest", required=True)
    parser.add_argument("--migration-map", required=True)
    parser.add_argument("--fixtures", default="doc/5-tests/2026-07-21_221037/six-domain-skill-streamlining/fixtures/trigger-cases.yaml")
    parser.add_argument("--phase", choices=["baseline", "route"], required=True)
    return parser.parse_args()


def sha256_text(value: str) -> str:
    """[参数]：value 为 UTF-8 文本；[返回]：SHA-256 十六进制摘要；最近修改时间：2026-07-21。"""
    # 1. 仅对冻结 description 的文本值取摘要，避免格式差异掩盖自动触发漂移。
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def read_yaml(path: Path, label: str, errors: list[str]) -> dict[str, Any] | list[Any] | None:
    """[参数]：path 为 YAML 路径，label 为错误标签；[返回]：YAML 对象或 None；最近修改时间：2026-07-21。"""
    # 1. 显式按 UTF-8 读取，避免 Windows 默认编码掩盖规则文件损坏。
    try:
        return yaml.safe_load(path.read_text(encoding="utf-8"))
    except Exception as exc:  # 验证器必须将读取失败转为可复核错误。
        errors.append(f"{label} 无法按 UTF-8 YAML 读取：{exc}")
        return None


def read_skill_description(path: Path, errors: list[str]) -> str | None:
    """[参数]：path 为 SKILL.md；[返回]：front matter description；最近修改时间：2026-07-21。"""
    # 1. 保持前置 YAML 最小解析，description 的原文本必须可逐字校验。
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError as exc:
        errors.append(f"SKILL.md 不是 UTF-8：{path.as_posix()}：{exc}")
        return None
    if not text.startswith("---\n"):
        errors.append(f"SKILL.md 缺少 front matter：{path.as_posix()}")
        return None
    parts = text.split("---\n", 2)
    if len(parts) < 3:
        errors.append(f"SKILL.md front matter 未闭合：{path.as_posix()}")
        return None
    for line in parts[1].splitlines():
        if line.startswith("description: "):
            return line.partition(": ")[2]
    errors.append(f"SKILL.md 缺少 description：{path.as_posix()}")
    return None


def load_candidates(manifest: dict[str, Any], route_map: dict[str, Any], errors: list[str]) -> tuple[dict[str, dict[str, Any]], dict[str, dict[str, Any]]]:
    """[参数]：manifest 与迁移映射；[返回]：source 索引；最近修改时间：2026-07-21。"""
    # 1. 两份机器事实必须覆盖同一组五个 owner，避免只改文档而脱离冻结候选。
    candidates = {item["source_skill"]: item for item in manifest.get("candidates", []) if item.get("source_skill") in SOURCES}
    mappings = {item["source_skill"]: item for item in route_map.get("owner_routes", []) if item.get("source_skill") in SOURCES}
    if set(candidates) != SOURCES or set(mappings) != SOURCES:
        errors.append("CYCLE-SS-05 candidate 或 migration map 集合不完整")
    return candidates, mappings


def validate_fixtures(root: Path, fixtures_raw: dict[str, Any] | list[Any] | None, candidates: dict[str, dict[str, Any]], errors: list[str]) -> None:
    """[参数]：fixture 数据与候选；[返回]：无；最近修改时间：2026-07-21。"""
    # 1. 正负 fixture 都要存在，自动触发不能只验证正向命中。
    if isinstance(fixtures_raw, dict):
        fixtures_raw = fixtures_raw.get("cases")
    if not isinstance(fixtures_raw, list):
        errors.append("trigger fixtures.cases 必须是列表")
        return
    fixtures = {item.get("id"): item for item in fixtures_raw if isinstance(item, dict) and isinstance(item.get("id"), str)}
    for source, candidate in sorted(candidates.items()):
        contract = candidate.get("trigger_contract")
        if not isinstance(contract, dict):
            errors.append(f"trigger_contract 缺失：{source}")
            continue
        for fixture_id in [*contract.get("positive_fixture_ids", []), *contract.get("negative_fixture_ids", [])]:
            fixture = fixtures.get(fixture_id)
            if not isinstance(fixture, dict):
                errors.append(f"trigger fixture 缺失：{source}/{fixture_id}")
                continue
            if fixture.get("source_skill") != source or fixture.get("target_owner") != candidate.get("target_owner"):
                errors.append(f"trigger fixture owner 漂移：{source}/{fixture_id}")
            if fixture.get("target_route") != candidate.get("target_route"):
                errors.append(f"trigger fixture route 漂移：{source}/{fixture_id}")
            if fixture_id.endswith("-NEG") and fixture.get("required_target_tokens"):
                errors.append(f"negative fixture 不得要求 target token：{source}/{fixture_id}")


def validate_owner(root: Path, source: str, candidate: dict[str, Any], mapping: dict[str, Any], phase: str, errors: list[str]) -> None:
    """[参数]：owner 的候选、映射和验证阶段；[返回]：无；最近修改时间：2026-07-21。"""
    # 1. 冻结资产全部存在；reference_refactor 不得伪装成删除 owner。
    owner = root / str(candidate.get("target_owner", ""))
    skill_path = owner / "SKILL.md"
    if not skill_path.is_file():
        errors.append(f"owner 缺失: {source}")
        return
    for asset in mapping.get("source_assets", []):
        if not isinstance(asset, str) or not (root / asset).is_file():
            errors.append(f"冻结 source asset 缺失: {asset}")
    preserved = set(mapping.get("preserved", []))
    missing_preserved = REQUIRED_PRESERVED - preserved
    if missing_preserved:
        errors.append(f"保护语义声明缺失：{source}/{sorted(missing_preserved)}")
    description = read_skill_description(skill_path, errors)
    expected_hash = mapping.get("baseline_description_sha256")
    if not isinstance(expected_hash, str) or len(expected_hash) != 64:
        errors.append(f"baseline description hash 缺失：{source}")
    elif description is not None and sha256_text(description) != expected_hash:
        errors.append(f"description 或自动触发契约漂移：{source}")
    skill_text = skill_path.read_text(encoding="utf-8")
    aliases = candidate.get("trigger_contract", {}).get("trigger_aliases", [])
    for alias in aliases:
        if alias not in skill_text:
            errors.append(f"SKILL 入口缺少 trigger alias：{source}/{alias}")
    action = candidate.get("action")
    if source in REFERENCE_REFACTOR_SOURCES:
        if action != "reference_refactor":
            errors.append(f"{source} action 必须为 reference_refactor")
        route = candidate.get("target_route")
        reference_path = owner / "references" / f"{route}.md"
        if phase == "route":
            if not reference_path.is_file():
                errors.append(f"route reference 缺失：{source}/{route}")
                return
            ref_text = reference_path.read_text(encoding="utf-8")
            if "# " not in ref_text or "## 保护语义" not in ref_text or "## 原 owner 细则" not in ref_text:
                errors.append(f"route reference 结构不完整：{source}")
            for term in REQUIRED_PROTECTED_TERMS:
                if term not in ref_text:
                    errors.append(f"route reference 缺少保护语义：{source}/{term}")
            if "references/shared-evidence-and-specialized-contracts.md" not in skill_text:
                errors.append(f"SKILL 未显式路由到 shared evidence reference：{source}")
            if "共享证据和专属契约" not in skill_text:
                errors.append(f"SKILL 未保留条件路由摘要：{source}")
    elif source == RETAIN_SPECIALIZED_SOURCE:
        if action != "retain_specialized":
            errors.append("code-review-automation-rules 不得被合并或删除")
        if (owner / "references" / "shared-evidence-and-specialized-contracts.md").exists():
            errors.append("code-review-automation-rules 不得被共享证据 reference 吞并")
        if "specialized-lifecycle" not in skill_text:
            errors.append("code-review-automation-rules 缺少 retained-specialized 条件路由标记")


def main() -> int:
    """[参数]：命令行提供仓库、清单、映射和阶段；[返回]：0/1；最近修改时间：2026-07-21。"""
    # 1. 先读取冻结机器事实，再检查实现后的 owner 与 trigger/保护语义。
    args = parse_args()
    root = Path(args.repo_root).resolve()
    errors: list[str] = []
    if not root.is_dir():
        errors.append(f"repo-root 不存在：{root}")
    manifest_path = (root / args.manifest).resolve()
    map_path = (root / args.migration_map).resolve()
    fixture_path = (root / args.fixtures).resolve()
    for path, label in ((manifest_path, "manifest"), (map_path, "migration map"), (fixture_path, "trigger fixtures")):
        if not path.is_file():
            errors.append(f"{label} 不存在：{path}")
    if errors:
        print(json.dumps({"schema_version": 1, "phase": args.phase, "candidate_count": 0, "valid": False, "errors": errors}, ensure_ascii=False, indent=2))
        return 1
    manifest = read_yaml(manifest_path, "manifest", errors)
    route_map = read_yaml(map_path, "migration map", errors)
    fixtures = read_yaml(fixture_path, "trigger fixtures", errors)
    if not isinstance(manifest, dict) or not isinstance(route_map, dict):
        print(json.dumps({"schema_version": 1, "phase": args.phase, "candidate_count": 0, "valid": False, "errors": errors}, ensure_ascii=False, indent=2))
        return 1
    candidates, mappings = load_candidates(manifest, route_map, errors)
    validate_fixtures(root, fixtures, candidates, errors)
    for source in sorted(SOURCES):
        candidate = candidates.get(source)
        mapping = mappings.get(source)
        if candidate is not None and mapping is not None:
            validate_owner(root, source, candidate, mapping, args.phase, errors)
    report = {"schema_version": 1, "phase": args.phase, "candidate_count": len(candidates), "valid": not errors, "errors": errors}
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
