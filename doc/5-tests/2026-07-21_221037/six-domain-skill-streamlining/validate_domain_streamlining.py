from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

import yaml


class ValidationFailure(Exception):
    """用于聚合当前阶段的确定性校验错误。"""


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def resolve_inside(root: Path, raw: str, label: str, errors: list[str]) -> Path | None:
    candidate = (root / raw).resolve()
    try:
        candidate.relative_to(root.resolve())
    except ValueError:
        fail(errors, f"{label} 越出仓库根目录：{raw}")
        return None
    return candidate


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_yaml(path: Path, label: str, errors: list[str]) -> dict[str, Any] | None:
    try:
        value = yaml.safe_load(path.read_text(encoding="utf-8"))
    except Exception as exc:  # 验证器必须把输入错误转换为可复核失败。
        fail(errors, f"{label} 无法按 UTF-8 YAML 读取：{exc}")
        return None
    if not isinstance(value, dict):
        fail(errors, f"{label} 根节点必须是对象")
        return None
    return value


def load_json(path: Path, label: str, errors: list[str]) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:  # 验证器必须把输入错误转换为可复核失败。
        fail(errors, f"{label} 无法按 UTF-8 JSON 读取：{exc}")
        return None


def validate_manifest(manifest: dict[str, Any], errors: list[str], phase: str) -> list[dict[str, Any]]:
    if manifest.get("schema_version") != 1:
        fail(errors, "manifest schema_version 必须为 1")
    if manifest.get("manifest_id") != "MANIFEST-SS-20260721":
        fail(errors, "manifest_id 不符合冻结标识")
    scope = manifest.get("scope")
    if not isinstance(scope, dict):
        fail(errors, "manifest 缺少 scope")
    elif scope.get("skill_count") != 36 or scope.get("retire_candidate_count") != 11:
        fail(errors, "scope 数量必须为 36 个 Skill、11 个退役候选")
    candidates = manifest.get("candidates")
    if not isinstance(candidates, list) or len(candidates) != 36:
        fail(errors, "candidates 必须包含 36 条")
        return []
    seen_source: set[str] = set()
    seen_id: set[str] = set()
    retired = 0
    allowed_actions = {"merge_retire", "reference_refactor", "canonical_owner", "retain_specialized"}
    for item in candidates:
        if not isinstance(item, dict):
            fail(errors, "candidate 存在非对象条目")
            continue
        cid = item.get("candidate_id")
        source = item.get("source_skill")
        target = item.get("target_owner")
        action = item.get("action")
        if not isinstance(cid, str) or not cid or cid in seen_id:
            fail(errors, f"candidate_id 缺失或重复：{cid}")
        else:
            seen_id.add(cid)
        if not isinstance(source, str) or not source or source in seen_source:
            fail(errors, f"source_skill 缺失或重复：{source}")
        else:
            seen_source.add(source)
        if not isinstance(target, str) or not target:
            fail(errors, f"{cid} 缺少 target_owner")
        if action not in allowed_actions:
            fail(errors, f"{cid} action 非法：{action}")
        if not isinstance(item.get("protected_semantics"), list) or not item["protected_semantics"]:
            fail(errors, f"{cid} 缺少 protected_semantics")
        contract = item.get("trigger_contract")
        if not isinstance(contract, dict) or not contract.get("preserve_description"):
            fail(errors, f"{cid} 缺少 trigger_contract.preserve_description=true")
        rollback = item.get("rollback_locator")
        if not isinstance(rollback, dict) or not rollback.get("baseline_commit") or not rollback.get("source_root"):
            fail(errors, f"{cid} 缺少 rollback_locator")
        if action == "merge_retire":
            retired += 1
            completed_retirement = item.get("delete_authorized") is True
            if phase in {"baseline", "trigger", "pre-delete", "all"} and not completed_retirement and item.get("delete_authorized") is not False:
                fail(errors, f"{cid} {phase} 阶段 delete_authorized 必须为 false")
            if phase == "post-delete" and item.get("delete_authorized") not in {False, True}:
                fail(errors, f"{cid} post-delete 阶段 delete_authorized 必须为布尔值")
    if retired != 11:
        fail(errors, f"实际 merge_retire 数量为 {retired}，必须为 11")
    if len(seen_source) != 36:
        fail(errors, f"实际唯一 source_skill 数量为 {len(seen_source)}，必须为 36")
    return candidates


def validate_asset_inventory(root: Path, manifest: dict[str, Any], errors: list[str], phase: str) -> None:
    raw = manifest.get("asset_inventory")
    if not isinstance(raw, str):
        fail(errors, "manifest 缺少 asset_inventory")
        return
    index_path = resolve_inside(root, "doc/5-tests/2026-07-21_221037/six-domain-skill-streamlining/" + raw, "asset_inventory", errors)
    if index_path is None or not index_path.is_file():
        fail(errors, f"asset_inventory 文件不存在：{raw}")
        return
    data = load_json(index_path, "asset_inventory", errors)
    if not isinstance(data, dict) or len(data) != 36:
        fail(errors, "asset_inventory 必须覆盖 36 个 Skill")
        return
    for skill, record in data.items():
        if not isinstance(record, dict) or record.get("root") != skill:
            fail(errors, f"asset_inventory.{skill} root 不一致")
            continue
        files = record.get("files")
        if not isinstance(files, list) or not files:
            fail(errors, f"asset_inventory.{skill}.files 为空")
            continue
        # 旧周期已完成删除的 source 只保留冻结回滚记录；后续 baseline/trigger/pre-delete/post-delete
        # 都不得把历史哈希误当作当前磁盘资产重新读取。
        if record.get("retired") is True:
            continue
        actual_total = 0
        for item in files:
            if not isinstance(item, dict) or not item.get("path"):
                fail(errors, f"asset_inventory.{skill} 存在非法文件条目")
                continue
            path = resolve_inside(root, str(item["path"]), f"asset_inventory.{skill}.path", errors)
            if path is None or not path.is_file():
                fail(errors, f"资产不存在：{item.get('path')}")
                continue
            actual_total += path.stat().st_size
            if item.get("bytes") != path.stat().st_size:
                fail(errors, f"资产字节数漂移：{item['path']}")
            if item.get("sha256") != sha256(path):
                fail(errors, f"资产 SHA-256 漂移：{item['path']}")
        if record.get("file_count") != len(files):
            fail(errors, f"asset_inventory.{skill}.file_count 与 files 数量不一致")
        if record.get("package_bytes") != actual_total:
            fail(errors, f"asset_inventory.{skill}.package_bytes 与磁盘不一致")


def validate_consumer_index(root: Path, manifest: dict[str, Any], errors: list[str]) -> None:
    raw = manifest.get("active_consumer_index")
    if not isinstance(raw, str):
        fail(errors, "manifest 缺少 active_consumer_index")
        return
    index_path = resolve_inside(root, "doc/5-tests/2026-07-21_221037/six-domain-skill-streamlining/" + raw, "active_consumer_index", errors)
    if index_path is None or not index_path.is_file():
        fail(errors, f"active_consumer_index 文件不存在：{raw}")
        return
    data = load_json(index_path, "active_consumer_index", errors)
    if not isinstance(data, dict) or len(data) != 36:
        fail(errors, "active_consumer_index 必须覆盖 36 个 Skill")
        return
    for skill, files in data.items():
        if not isinstance(files, list) or not files:
            fail(errors, f"active_consumer_index.{skill} 为空")
            continue
        for raw_path in files:
            path = resolve_inside(root, str(raw_path), f"active_consumer_index.{skill}", errors)
            if path is None or not path.is_file():
                fail(errors, f"消费者文件不存在：{raw_path}")


def validate_candidates_exist(root: Path, candidates: list[dict[str, Any]], errors: list[str], phase: str, only_source: str | None = None) -> None:
    for item in candidates:
        source = str(item.get("source_skill", ""))
        if only_source and source != only_source:
            continue
        target = str(item.get("target_owner", ""))
        source_path = root / source
        target_path = root / target
        if item.get("action") == "merge_retire":
            # 已完成的旧周期删除候选保留 manifest 记录，但不再要求 source 回到磁盘；
            # 当前候选仍保持 delete_authorized=false，因此仍会在 pre-delete 阶段要求 source 存在。
            completed_retirement = item.get("delete_authorized") is True
            if phase in {"baseline", "pre-delete"} and not completed_retirement and not (source_path / "SKILL.md").is_file():
                fail(errors, f"{phase} 阶段 source 不存在：{source}")
            if phase == "post-delete" and not completed_retirement and source_path.exists():
                fail(errors, f"post-delete 阶段旧目录仍存在：{source}")
            if phase == "post-delete" and completed_retirement and source_path.exists():
                fail(errors, f"post-delete 阶段已授权删除的旧目录仍存在：{source}")
        if not (target_path / "SKILL.md").is_file():
            fail(errors, f"target owner 不存在：{target}")


def validate_trigger_cases(root: Path, manifest: dict[str, Any], candidates: list[dict[str, Any]], errors: list[str], phase: str, only_source: str | None = None) -> None:
    raw = manifest.get("trigger_cases")
    if not isinstance(raw, str):
        fail(errors, "manifest 缺少 trigger_cases")
        return
    path = resolve_inside(root, "doc/5-tests/2026-07-21_221037/six-domain-skill-streamlining/" + raw, "trigger_cases", errors)
    if path is None or not path.is_file():
        fail(errors, f"trigger_cases 文件不存在：{raw}")
        return
    data = load_yaml(path, "trigger_cases", errors)
    if not isinstance(data, dict) or data.get("schema_version") != 1:
        fail(errors, "trigger_cases schema_version 必须为 1")
        return
    cases = data.get("cases")
    if not isinstance(cases, list) or len(cases) != 72:
        fail(errors, "trigger_cases 必须包含每个 Skill 一条正例和一条负例，共 72 条")
        return
    candidate_sources = {str(x.get("source_skill")) for x in candidates}
    for case in cases:
        if not isinstance(case, dict):
            fail(errors, "trigger case 存在非对象条目")
            continue
        if only_source and str(case.get("source_skill")) != only_source:
            continue
        for key in ("id", "domain", "source_skill", "target_owner", "prompt", "phase", "expected"):
            if not case.get(key):
                fail(errors, f"trigger case 缺少字段 {key}：{case.get('id')}")
        if case.get("source_skill") not in candidate_sources:
            fail(errors, f"trigger case source 不在 manifest：{case.get('source_skill')}")
        if phase in {"pre-delete", "post-delete"}:
            target_path = root / str(case.get("target_owner")) / "SKILL.md"
            if not target_path.is_file():
                fail(errors, f"trigger case target 不存在：{case.get('target_owner')}")
            if phase == "pre-delete" and case.get("target_route") and case.get("target_route") != "canonical-owner":
                target_text = target_path.read_text(encoding="utf-8")
                route = str(case["target_route"])
                # 路由标记在对应迁移任务完成后才成为强制承接证据。
                if f"{route}" not in target_text and str(case.get("source_skill")) in {x.get("source_skill") for x in candidates if x.get("action") == "merge_retire"}:
                    fail(errors, f"pre-delete 目标 owner 尚未承接 route marker：{case.get('source_skill')} -> {route}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="验证六域 Skill 精简的 manifest、资产基线、消费者和触发契约")
    parser.add_argument("--repo-root", required=True)
    parser.add_argument("--manifest", required=True)
    parser.add_argument("--phase", choices=["baseline", "trigger", "pre-delete", "post-delete", "all"], required=True)
    parser.add_argument("--only-source", help="仅验证一个 candidate source，供增量迁移的 scoped pre-delete/post-delete 使用")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = Path(args.repo_root).resolve()
    errors: list[str] = []
    if not root.is_dir():
        errors.append(f"repo-root 不存在：{root}")
        return report(args.phase, errors)
    manifest_path = resolve_inside(root, args.manifest, "manifest", errors)
    if manifest_path is None or not manifest_path.is_file():
        errors.append(f"manifest 不存在：{args.manifest}")
        return report(args.phase, errors)
    manifest = load_yaml(manifest_path, "manifest", errors)
    if manifest is None:
        return report(args.phase, errors)
    candidates = validate_manifest(manifest, errors, args.phase)
    if args.phase in {"baseline", "all"}:
        validate_asset_inventory(root, manifest, errors, args.phase)
        validate_consumer_index(root, manifest, errors)
        validate_candidates_exist(root, candidates, errors, "baseline", args.only_source)
    if args.phase in {"trigger", "pre-delete", "post-delete", "all"}:
        validate_trigger_cases(root, manifest, candidates, errors, "pre-delete" if args.phase == "all" else args.phase, args.only_source)
        validate_candidates_exist(root, candidates, errors, args.phase, args.only_source)
    return report(args.phase, errors)


def report(phase: str, errors: list[str]) -> int:
    result = {"schema_version": 1, "phase": phase, "valid": not errors, "errors": errors, "error_count": len(errors)}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
