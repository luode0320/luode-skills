#!/usr/bin/env python3
"""需求域 Skill 精简专项验证器：真实扫描、映射、触发与收口验证。"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
import unicodedata
from pathlib import Path
from urllib.parse import unquote

import yaml


OLD_ROUTES = ("requirement-gap-rules", "requirement-discovery-rules")
CORE_SKILLS = (
    "requirement-intake-rules",
    "requirement-boundary-rules",
    "requirement-splitting-rules",
    "requirement-change-rules",
)
EXPECTED_ACTIVE_CONSUMERS = {
    "requirement-boundary-rules/SKILL.md",
    "requirement-change-rules/SKILL.md",
    "acceptance-criteria-rules/references/acceptance-boundaries.md",
    "acceptance-criteria-rules/references/shared-evidence-and-specialized-contracts.md",
    "artifact-storage-rules/references/root-directories.md",
    "artifact-storage-rules/references/update-policy.md",
    "parallel-task-dispatch-rules/references/existing-skill-mapping.md",
    "team-development-rules/references/conflict-examples.md",
    "team-development-rules/references/routing-rules.md",
    "test-strategy-rules/references/test-asset-governance.md",
    "README.md",
    "PROJECT_MEMORY.md",
    "PROJECT_STYLE.md",
}
EXPECTED_PROTECTED_CONTRACT_FILES = {
    "autonomous-execution-rules/SKILL.md",
    "context-compression-rules/SKILL.md",
    "git-collaboration-rules/SKILL.md",
    "implementation-review-rules/SKILL.md",
    "project-change-review-rules/SKILL.md",
    "project-rule-file-bootstrap-rules/SKILL.md",
    "reasoning-summary-structure-rules/SKILL.md",
    "recent-context-bootstrap-rules/SKILL.md",
    "skill-hit-check-rules/SKILL.md",
}
EXPECTED_REFERENCE_ASSETS = {
    "requirement-intake-rules": {
        "extreme-completeness-standard.md",
        "gap-routing.md",
        "initial-discovery-checklist.md",
        "initial-discovery-evidence-and-memory.md",
        "initial-discovery-output-template.md",
        "initial-discovery-route.md",
        "intake-boundaries-and-examples.md",
        "intake-checklist.md",
        "missing-info-checklist.md",
        "pause-triggers.md",
        "requirement-domain-shared-contract.md",
        "requirement-gap-examples.md",
        "requirement-structure-template.md",
    },
    "requirement-boundary-rules": {
        "acceptance-routing-examples.md",
        "boundary-checklist.md",
        "history-vs-change.md",
    },
    "requirement-splitting-rules": {
        "splitting-dimensions.md",
        "splitting-examples.md",
        "splitting-sequence.md",
    },
    "requirement-change-rules": {
        "change-classification.md",
        "change-decision-examples.md",
        "impact-recheck.md",
    },
}
EXPECTED_CASES = {
    "TRG-01": ("requirement-intake-rules", "initial-discovery"),
    "TRG-02": ("requirement-intake-rules", "intake"),
    "TRG-03": ("requirement-intake-rules", "gap-routing"),
    "TRG-04": ("requirement-boundary-rules", "boundary"),
    "TRG-05": ("requirement-splitting-rules", "splitting"),
    "TRG-06": ("requirement-change-rules", "change"),
    "TRG-07": ("bug-intake-rules", "bug"),
    "TRG-08": ("acceptance-criteria-rules", "acceptance"),
    "TRG-09": ("functional-validation-rules", "functional-validation"),
    "TRG-10": ("final-acceptance-rules", "final-acceptance"),
    "TRG-11": ("history-recall-rules", "history"),
    "TRG-12": ("implementation-planning-rules", "planning"),
    "TRG-13": ("stop", "no-new-action"),
    "TRG-14": ("requirement-intake-rules", "intake"),
}
LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
INLINE_PATH_RE = re.compile(r"`([^`\n]+\.(?:md|yaml|yml|json|py))`")
BANNED_IMPLEMENTATION_HEADINGS = (
    "## 实施总览",
    "## 实施周期",
    "## 文件/符号落点",
    "## 真实测试命令",
)


def read_utf8(path: Path) -> str:
    raw = path.read_bytes()
    if raw.startswith(b"\xef\xbb\xbf"):
        raise ValueError(f"UTF-8 BOM is not allowed: {path}")
    return raw.decode("utf-8")


def git_output(repo: Path, *args: str) -> bytes:
    return subprocess.check_output(["git", *args], cwd=repo)


def git_show(repo: Path, revision: str, path: str) -> bytes:
    return git_output(repo, "show", f"{revision}:{path}")


def sha256_hex(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest().upper()


def newline_hashes(raw: bytes) -> dict[str, str]:
    """返回 Git blob 在 LF 与 CRLF 工作树中的合法原始字节指纹。"""
    lf = raw.replace(b"\r\n", b"\n")
    crlf = lf.replace(b"\n", b"\r\n")
    return {"git": sha256_hex(raw), "lf": sha256_hex(lf), "crlf": sha256_hex(crlf)}


def load_yaml(path: Path) -> dict:
    payload = yaml.safe_load(read_utf8(path))
    if not isinstance(payload, dict):
        raise ValueError(f"YAML root must be mapping: {path}")
    return payload


def load_json(path: Path) -> dict:
    payload = json.loads(read_utf8(path))
    if not isinstance(payload, dict):
        raise ValueError(f"JSON root must be object: {path}")
    return payload


def active_files(repo: Path):
    for path in repo.rglob("*"):
        if not path.is_file():
            continue
        rel = path.relative_to(repo).as_posix()
        if rel.startswith((".git/", "doc/", ".tmp/")) or rel == "PROJECT_HISTORY.md":
            continue
        yield path, rel


def active_old_refs(repo: Path) -> list[dict]:
    found: list[dict] = []
    for path, rel in active_files(repo):
        try:
            text = read_utf8(path)
        except (UnicodeDecodeError, OSError, ValueError):
            continue
        for number, line in enumerate(text.splitlines(), 1):
            if any(old in line for old in OLD_ROUTES):
                found.append({"file": rel, "line": number, "text": line.strip()})
    return found


def dictionary_summary(repo: Path) -> dict:
    text = read_utf8(repo / "skill-dictionary/data.js").strip()
    prefix = "window.SKILL_DICTIONARY = "
    if not text.startswith(prefix) or not text.endswith(";"):
        raise ValueError("skill-dictionary/data.js wrapper is invalid")
    payload = json.loads(text[len(prefix) : -1])
    return payload.get("summary", {})


def validate_manifest(repo: Path, manifest: dict) -> tuple[list[str], dict]:
    errors: list[str] = []
    required_keys = (
        "baseline_commit",
        "expected_skill_total",
        "expected_planned_missing",
        "required_files",
        "retired_paths",
        "active_consumers",
        "protected_existing_uncommitted",
        "protected_existing_contracts",
        "candidates",
        "fixtures",
        "protected_semantics_file",
        "baseline_inventory",
    )
    for key in required_keys:
        if manifest.get(key) in (None, "", []):
            errors.append(f"manifest missing field: {key}")
    candidate_fields = (
        "id",
        "source",
        "target",
        "action",
        "trigger_contract",
        "write_set",
        "rollback_locator",
        "baseline_hash",
        "worktree_hash",
    )
    for item in manifest.get("candidates", []):
        for field in candidate_fields:
            if item.get(field) in (None, "", []):
                errors.append(f"candidate {item.get('id')} missing field: {field}")
    active_consumers = set(manifest.get("active_consumers", []))
    if active_consumers != EXPECTED_ACTIVE_CONSUMERS:
        errors.append(
            "active consumer contract drift: "
            f"missing={sorted(EXPECTED_ACTIVE_CONSUMERS - active_consumers)}, "
            f"extra={sorted(active_consumers - EXPECTED_ACTIVE_CONSUMERS)}"
        )
    contract_files = {str(item.get("file", "")) for item in manifest.get("protected_existing_contracts", [])}
    if contract_files != EXPECTED_PROTECTED_CONTRACT_FILES:
        errors.append(
            "protected existing contract set drift: "
            f"missing={sorted(EXPECTED_PROTECTED_CONTRACT_FILES - contract_files)}, "
            f"extra={sorted(contract_files - EXPECTED_PROTECTED_CONTRACT_FILES)}"
        )
    protected_uncommitted = set(manifest.get("protected_existing_uncommitted", []))
    if protected_uncommitted != EXPECTED_PROTECTED_CONTRACT_FILES:
        errors.append(
            "protected uncommitted set drift: "
            f"missing={sorted(EXPECTED_PROTECTED_CONTRACT_FILES - protected_uncommitted)}, "
            f"extra={sorted(protected_uncommitted - EXPECTED_PROTECTED_CONTRACT_FILES)}"
        )
    for rel in manifest.get("required_files", []):
        if not (repo / rel).exists():
            errors.append(f"missing required file: {rel}")
    for rel in manifest.get("retired_paths", []):
        if (repo / rel).exists():
            errors.append(f"retired path still exists: {rel}")
    return errors, {"candidate_count": len(manifest.get("candidates", []))}


def phase_baseline(repo: Path, manifest: dict) -> tuple[list[str], dict]:
    errors, data = validate_manifest(repo, manifest)
    revision = str(manifest.get("baseline_commit", ""))
    head = git_output(repo, "rev-parse", "HEAD").decode().strip()
    if head != revision:
        errors.append(f"HEAD drifted from frozen baseline: {head}")

    inventory_path = repo / str(manifest.get("baseline_inventory", ""))
    try:
        inventory = load_json(inventory_path)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        errors.append(f"baseline inventory invalid: {exc}")
        inventory = {"files": {}}
    inventory_files = inventory.get("files", {})
    inventory_results = []
    for rel, expected_record in inventory_files.items():
        if not isinstance(expected_record, dict):
            errors.append(f"baseline inventory record must be object: {rel}")
            continue
        expected_git = str(expected_record.get("git_sha256", "")).upper()
        expected_worktree = str(expected_record.get("worktree_sha256", "")).upper()
        if not expected_git or not expected_worktree:
            errors.append(f"baseline inventory hashes missing: {rel}")
            continue
        try:
            hashes = newline_hashes(git_show(repo, revision, rel))
        except subprocess.CalledProcessError:
            errors.append(f"baseline source missing in git: {rel}")
            continue
        if hashes["git"] != expected_git:
            errors.append(f"baseline inventory hash mismatch: {rel}")
        worktree_valid = expected_worktree in {hashes["lf"], hashes["crlf"]}
        if not worktree_valid:
            errors.append(f"baseline worktree hash is not a valid LF/CRLF form: {rel}")
        inventory_results.append(
            {
                "file": rel,
                "git_hash_valid": hashes["git"] == expected_git,
                "worktree_hash_valid": worktree_valid,
                "accepted_worktree_hashes": [hashes["lf"], hashes["crlf"]],
            }
        )

    candidate_results = []
    for candidate in manifest.get("candidates", []):
        try:
            hashes = newline_hashes(git_show(repo, revision, candidate["source"]))
        except subprocess.CalledProcessError:
            errors.append(f"candidate baseline source missing: {candidate.get('source')}")
            continue
        baseline_valid = hashes["git"] == str(candidate.get("baseline_hash", "")).upper()
        if not baseline_valid:
            errors.append(f"candidate baseline hash mismatch: {candidate.get('id')}")
        worktree_hash = str(candidate.get("worktree_hash", "")).upper()
        worktree_valid = False
        inventory_record = inventory_files.get(candidate.get("source"), {})
        worktree_valid = worktree_hash in {hashes["lf"], hashes["crlf"]}
        if not worktree_valid:
            errors.append(f"candidate worktree hash is not a valid LF/CRLF form: {candidate.get('id')}")
        if not isinstance(inventory_record, dict) or worktree_hash != str(
            inventory_record.get("worktree_sha256", "")
        ).upper():
            errors.append(f"candidate/inventory worktree hash drift: {candidate.get('id')}")
        candidate_results.append(
            {
                "id": candidate.get("id"),
                "baseline_hash_valid": baseline_valid,
                "worktree_hash_checked": True,
                "worktree_hash_valid": worktree_valid,
            }
        )

    protected_status = {}
    for rel in manifest.get("protected_existing_uncommitted", []):
        status = git_output(repo, "status", "--porcelain", "--", rel).decode("utf-8", errors="replace").strip()
        protected_status[rel] = status
        if not status:
            errors.append(f"pre-existing uncommitted protection lost or not evidenced: {rel}")

    semantics_path = repo / str(manifest.get("protected_semantics_file", ""))
    try:
        semantics = load_json(semantics_path).get("mappings", [])
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        errors.append(f"protected semantics invalid: {exc}")
        semantics = []
    semantic_fields = ("id", "source", "target", "owner", "assertion", "evidence")
    for item in semantics:
        for field in semantic_fields:
            if item.get(field) in (None, "", []):
                errors.append(f"protected semantic {item.get('id')} missing field: {field}")
    if len(semantics) < 10:
        errors.append(f"protected semantic mappings must be >=10, actual={len(semantics)}")

    protected_contract_results = []
    for item in manifest.get("protected_existing_contracts", []):
        rel = str(item.get("file", ""))
        assertions = item.get("assertion", [])
        if not rel or not isinstance(assertions, list) or not assertions:
            errors.append(f"protected existing contract invalid: {item}")
            continue
        path = repo / rel
        try:
            text = read_utf8(path)
        except (OSError, UnicodeDecodeError, ValueError) as exc:
            errors.append(f"protected existing contract unreadable: {rel}: {exc}")
            continue
        missing = [token for token in assertions if token not in text]
        if missing:
            errors.append(f"protected existing contract missing tokens: {rel}: {missing}")
        protected_contract_results.append({"file": rel, "missing": missing, "valid": not missing})

    consumer_errors, consumer_data = phase_consumer(repo, manifest)
    errors.extend(consumer_errors)

    data.update(
        {
            "baseline_inventory_count": len(inventory_files),
            "baseline_inventory_results": inventory_results,
            "candidate_hash_results": candidate_results,
            "protected_semantic_count": len(semantics),
            "protected_existing_status": protected_status,
            "protected_existing_contract_results": protected_contract_results,
            "baseline_consumer_check": consumer_data,
        }
    )
    return errors, data


def contains_any(text: str, tokens: tuple[str, ...]) -> bool:
    return any(token in text for token in tokens)


def route_prompt(prompt: str) -> tuple[str, str]:
    """按总控优先级确定单一 owner/route，用真实自然语言 fixture 防止静态自证。"""
    text = re.sub(r"\s+", "", unicodedata.normalize("NFKC", prompt).casefold())
    if contains_any(text, ("停止", "不要继续", "到此为止", "不要下一步")):
        return "stop", "no-new-action"
    if contains_any(text, ("实施计划", "先给计划", "计划和步骤", "先列步骤", "完整计划")):
        return "implementation-planning-rules", "planning"
    if contains_any(text, ("上次", "之前怎么", "历史怎么", "过去怎么")):
        return "history-recall-rules", "history"
    if "测试" in text and contains_any(text, ("审查", "审核")) and contains_any(text, ("放行", "最终验收")):
        return "final-acceptance-rules", "final-acceptance"
    if "验证" in text and contains_any(text, ("实现后", "修改后", "功能行为", "页面交互")):
        return "functional-validation-rules", "functional-validation"
    if contains_any(text, ("实施前", "编码前")) and contains_any(
        text, ("做到什么算完成", "完成标准", "验收标准")
    ):
        return "acceptance-criteria-rules", "acceptance"
    if contains_any(text, ("原实现", "已有实现")) and contains_any(
        text, ("不符合", "结果不符", "错误", "修复")
    ):
        return "bug-intake-rules", "bug"
    if contains_any(text, ("编码中", "已确认需求", "需求变更")) and contains_any(
        text, ("新增", "修改默认值", "改变默认值", "优先级", "交付物", "范围")
    ):
        return "requirement-change-rules", "change"
    if contains_any(text, ("本次范围", "顺手改旧逻辑", "兼容", "归属不清", "上下游影响")):
        return "requirement-boundary-rules", "boundary"
    if contains_any(text, ("多个模块", "多模块", "多个页面", "多页面", "多个接口", "多接口", "多个独立子系统")) and contains_any(
        text, ("单一闭环", "多个角色", "角色", "独立子系统", "拆分")
    ):
        return "requirement-splitting-rules", "splitting"
    if contains_any(text, ("已经查过", "侦察后", "查证后")) and contains_any(
        text, ("仍", "缺少", "关键字段", "成功标准", "合理解释")
    ):
        return "requirement-intake-rules", "gap-routing"
    if contains_any(text, ("粗略idea", "粗略想法", "一句话idea", "老板式方向", "先从项目代码", "官方资料查清")):
        return "requirement-intake-rules", "initial-discovery"
    if contains_any(text, ("需求", "新功能", "新页面", "新接口", "新模块")):
        return "requirement-intake-rules", "intake"
    return "none", "none"


def phase_trigger(repo: Path, manifest: dict) -> tuple[list[str], dict]:
    errors: list[str] = []
    fixtures_path = repo / str(manifest.get("fixtures", ""))
    try:
        cases = load_json(fixtures_path).get("cases", [])
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        return [f"fixture load failed: {exc}"], {"case_results": []}
    case_ids = [case.get("id") for case in cases]
    if len(cases) != len(EXPECTED_CASES) or len(case_ids) != len(set(case_ids)):
        errors.append("fixture contract must contain exactly 14 unique cases")
    if set(case_ids) != set(EXPECTED_CASES):
        errors.append("fixture IDs do not match the frozen 14-case contract")
    banned_prompt_names = set(CORE_SKILLS) | set(OLD_ROUTES)
    banned_prompt_names.update(owner for owner, _route in EXPECTED_CASES.values() if owner.endswith("-rules"))
    for case in cases:
        banned_prompt_names.update(str(item).split("#", 1)[0] for item in case.get("negative", []))
    unrelated_route = route_prompt("这是一句与研发路由完全无关的自然语言。")
    if unrelated_route != ("none", "none"):
        errors.append(f"unrelated prompt must remain unmatched, actual={unrelated_route}")
    case_results = []
    for case in cases:
        case_id = case.get("id")
        required = ("prompt", "expected_owner", "owner_file", "route", "negative", "assertion_tokens")
        missing_fields = [field for field in required if case.get(field) in (None, "", [])]
        if missing_fields:
            errors.append(f"{case_id} missing fields: {missing_fields}")
            continue
        expected = EXPECTED_CASES.get(case_id)
        if expected != (case.get("expected_owner"), case.get("route")):
            errors.append(f"{case_id} owner/route drift: {case.get('expected_owner')}#{case.get('route')}")
        prompt_lower = case["prompt"].casefold()
        prompt_name_hits = sorted(name for name in banned_prompt_names if name and name.casefold() in prompt_lower)
        if prompt_name_hits:
            errors.append(f"{case_id} prompt is not natural language: contains Skill names {prompt_name_hits}")
        owner_path = repo / case["owner_file"]
        try:
            owner_text = read_utf8(owner_path)
        except (OSError, UnicodeDecodeError, ValueError) as exc:
            errors.append(f"{case_id} owner file invalid: {exc}")
            continue
        missing_tokens = [token for token in case["assertion_tokens"] if token not in owner_text]
        if missing_tokens:
            errors.append(f"{case_id} missing assertion tokens: {missing_tokens}")
        if case["expected_owner"] in case["negative"]:
            errors.append(f"{case_id} expected owner appears in negative list")
        actual_owner, actual_route = route_prompt(case["prompt"])
        deterministic = route_prompt(case["prompt"]) == (actual_owner, actual_route)
        normalized_stable = route_prompt(f" \n{case['prompt']}\t ") == (actual_owner, actual_route)
        if not deterministic:
            errors.append(f"{case_id} route is not deterministic")
        if not normalized_stable:
            errors.append(f"{case_id} route changes after whitespace normalization")
        actual_labels = {actual_owner, f"{actual_owner}#{actual_route}"}
        negative_hits = [item for item in case["negative"] if item in actual_labels]
        route_valid = (actual_owner, actual_route) == expected
        if not route_valid:
            errors.append(
                f"{case_id} routed to {actual_owner}#{actual_route}, expected {expected[0]}#{expected[1]}"
            )
        if negative_hits:
            errors.append(f"{case_id} negative route matched: {negative_hits}")
        case_results.append(
            {
                "id": case_id,
                "expected_owner": case["expected_owner"],
                "route": case["route"],
                "actual_owner": actual_owner,
                "actual_route": actual_route,
                "negative": case["negative"],
                "negative_hits": negative_hits,
                "deterministic": deterministic,
                "normalized_stable": normalized_stable,
                "assertion_tokens": case["assertion_tokens"],
                "valid": not missing_tokens and route_valid and not negative_hits and deterministic and normalized_stable,
            }
        )

    for candidate in manifest.get("candidates", []):
        target = repo / str(candidate.get("target", ""))
        if not target.is_file():
            continue
        text = read_utf8(target)
        missing = [token for token in candidate.get("trigger_contract", []) if token not in text]
        if missing:
            errors.append(f"candidate trigger contract missing {candidate.get('id')}: {missing}")
    return errors, {"fixture_count": len(cases), "case_results": case_results}


def phase_consumer(repo: Path, manifest: dict) -> tuple[list[str], dict]:
    found = active_old_refs(repo)
    errors = [f"active old route: {item['file']}:{item['line']}" for item in found]
    consumer_results = []
    for rel in manifest.get("active_consumers", []):
        path = repo / rel
        if not path.exists():
            errors.append(f"active consumer missing: {rel}")
            continue
        text = read_utf8(path)
        old_hits = [old for old in OLD_ROUTES if old in text]
        if old_hits:
            errors.append(f"active consumer still references old route: {rel}: {old_hits}")
        consumer_results.append({"file": rel, "old_hits": old_hits, "valid": not old_hits})
    return errors, {"active_old_refs": found, "active_old_count": len(found), "consumers": consumer_results}


def markdown_link_errors(repo: Path) -> tuple[list[str], list[dict]]:
    errors: list[str] = []
    checked: list[dict] = []
    for skill in CORE_SKILLS:
        skill_root = repo / skill
        for path in skill_root.rglob("*.md"):
            text = read_utf8(path)
            declared = [(raw, "markdown") for raw in LINK_RE.findall(text)]
            declared.extend((raw, "inline") for raw in INLINE_PATH_RE.findall(text))
            for raw, kind in declared:
                target = raw.strip().strip("<>").split("#", 1)[0].strip()
                if not target or target.startswith(("http://", "https://", "mailto:", "data:")):
                    continue
                if "YYYY" in target or "<" in target or ">" in target or "{" in target:
                    continue
                decoded = unquote(target)
                candidates = (
                    (path.parent / decoded).resolve(),
                    (skill_root / decoded).resolve(),
                    (repo / decoded).resolve(),
                )
                valid = any(
                    candidate.exists() and (repo == candidate or repo in candidate.parents)
                    for candidate in candidates
                )
                checked.append(
                    {
                        "source": path.relative_to(repo).as_posix(),
                        "target": target,
                        "kind": kind,
                        "valid": valid,
                    }
                )
                if not valid:
                    errors.append(f"broken Markdown reference: {path.relative_to(repo).as_posix()} -> {target}")
    return errors, checked


def resolve_declared_target(source: Path, skill_root: Path, repo: Path, raw: str) -> Path | None:
    target = raw.strip().strip("<>").split("#", 1)[0].strip()
    if not target or target.startswith(("http://", "https://", "mailto:", "data:")):
        return None
    if "YYYY" in target or "<" in target or ">" in target or "{" in target:
        return None
    decoded = unquote(target)
    for candidate in ((source.parent / decoded), (skill_root / decoded), (repo / decoded)):
        resolved = candidate.resolve()
        if resolved.is_file() and (repo == resolved or repo in resolved.parents):
            return resolved
    return None


def reachable_reference_assets(repo: Path, skill: str) -> tuple[list[str], list[str]]:
    """从根 SKILL.md 递归追踪 references，避免仅凭文件名碰巧出现而误放行。"""
    skill_root = (repo / skill).resolve()
    references_root = skill_root / "references"
    queue = [skill_root / "SKILL.md"]
    visited: set[Path] = set()
    reachable: set[Path] = set()
    while queue:
        source = queue.pop()
        if source in visited or not source.is_file():
            continue
        visited.add(source)
        text = read_utf8(source)
        declared = list(LINK_RE.findall(text)) + list(INLINE_PATH_RE.findall(text))
        for raw in declared:
            target = resolve_declared_target(source, skill_root, repo, raw)
            if target is None or references_root not in target.parents:
                continue
            if target not in reachable:
                reachable.add(target)
                if target.suffix.lower() == ".md":
                    queue.append(target)
    all_references = {path.resolve() for path in references_root.rglob("*") if path.is_file()}
    orphan = sorted(path.relative_to(repo).as_posix() for path in all_references - reachable)
    reached = sorted(path.relative_to(repo).as_posix() for path in reachable)
    return orphan, reached


def gap_semantic_coverage(repo: Path, revision: str) -> tuple[list[str], list[dict]]:
    errors: list[str] = []
    old = git_show(
        repo,
        revision,
        "requirement-intake-rules/references/gap-routing-source/migrated-gap-rule.md",
    ).decode("utf-8")
    new = read_utf8(repo / "requirement-intake-rules/references/gap-routing.md")
    pairs = (
        ("识别需求描述中的关键缺失项", "识别需求描述中的关键缺失项"),
        ("先做了再补需求", "先做了再补需求"),
        ("TBD/TODO/待补", "TBD/TODO/待补"),
        ("图缺失或图文冲突应作为缺口处理", "图缺失或图文冲突应作为缺口处理"),
        ("正文摘要 + 附录详解", "正文摘要 + 附录详解"),
        ("临时缺口文档", "临时缺口文档"),
        ("多种合理解释", "多种合理解释"),
        ("不允许“先做一版看看”", "不允许“先做一版看看”"),
        ("doc/data/images/", "doc/data/images/"),
        ("artifact-delivery-gate-rules", "artifact-delivery-gate-rules"),
        ("P0/P1", "P0/P1"),
        ("blocked", "blocked"),
        ("用户确认并补齐缺口后", "用户确认并补齐缺口后"),
        ("关键缺口未清零", "关键缺口未清零"),
        ("回填主需求文档", "回填主需求文档"),
    )
    results = []
    for source, target in pairs:
        source_ok = source in old
        target_ok = target in new
        if not source_ok or not target_ok:
            errors.append(f"gap semantic mapping failed: {source} -> {target}")
        results.append({"source": source, "target": target, "source_ok": source_ok, "target_ok": target_ok})
    return errors, results


def phase_reference(repo: Path, manifest: dict) -> tuple[list[str], dict]:
    errors, data = validate_manifest(repo, manifest)
    link_errors, links = markdown_link_errors(repo)
    errors.extend(link_errors)

    utf8_count = 0
    single_line = []
    agent_results = []
    reference_reachability = []
    script_results = []
    for skill in CORE_SKILLS:
        skill_root = repo / skill
        for path in skill_root.rglob("*"):
            if not path.is_file():
                continue
            if path.suffix.lower() in {".md", ".yaml", ".yml", ".py", ".json"}:
                try:
                    text = read_utf8(path)
                except (UnicodeDecodeError, ValueError) as exc:
                    errors.append(str(exc))
                    continue
                utf8_count += 1
                if path.suffix.lower() == ".md" and len(text.splitlines()) <= 1:
                    single_line.append(path.relative_to(repo).as_posix())
        agent_files = [path for path in (skill_root / "agents").rglob("*") if path.is_file()]
        agent = skill_root / "agents/openai.yaml"
        unique_agent = len(agent_files) == 1 and agent_files[0].resolve() == agent.resolve()
        if not unique_agent:
            errors.append(
                f"agent metadata must contain only agents/openai.yaml: {skill}: "
                f"{[path.relative_to(repo).as_posix() for path in agent_files]}"
            )
        agent_mentions_owner = False
        try:
            load_yaml(agent)
            agent_mentions_owner = skill in read_utf8(agent)
            if not agent_mentions_owner:
                errors.append(f"agent metadata does not name owner Skill: {skill}")
        except (OSError, ValueError, yaml.YAMLError) as exc:
            errors.append(f"agent YAML invalid: {agent.relative_to(repo).as_posix()}: {exc}")
        agent_results.append(
            {"skill": skill, "unique_openai_yaml": unique_agent, "mentions_owner": agent_mentions_owner}
        )

        orphan, reached = reachable_reference_assets(repo, skill)
        actual_reference_names = {
            path.name for path in (skill_root / "references").rglob("*") if path.is_file()
        }
        expected_reference_names = EXPECTED_REFERENCE_ASSETS[skill]
        if actual_reference_names != expected_reference_names:
            errors.append(
                f"reference asset set drift for {skill}: "
                f"missing={sorted(expected_reference_names - actual_reference_names)}, "
                f"extra={sorted(actual_reference_names - expected_reference_names)}"
            )
        if orphan:
            errors.append(f"unreachable reference assets for {skill}: {orphan}")
        reference_reachability.append(
            {
                "skill": skill,
                "expected_assets": sorted(expected_reference_names),
                "actual_assets": sorted(actual_reference_names),
                "reachable": reached,
                "orphan": orphan,
            }
        )

        scripts_root = skill_root / "scripts"
        script_files = [path for path in scripts_root.rglob("*") if path.is_file()] if scripts_root.exists() else []
        if script_files:
            errors.append(
                f"unexpected scripts in requirement owner {skill}: "
                f"{[path.relative_to(repo).as_posix() for path in script_files]}"
            )
        script_results.append({"skill": skill, "scripts": [path.relative_to(repo).as_posix() for path in script_files]})
    if single_line:
        errors.append(f"single-line Markdown files: {single_line}")

    revision = str(manifest.get("baseline_commit", ""))
    gap_errors, gap_coverage = gap_semantic_coverage(repo, revision)
    errors.extend(gap_errors)

    semantics = load_json(repo / str(manifest.get("protected_semantics_file", ""))).get("mappings", [])
    semantic_results = []
    core_corpus = "\n".join(read_utf8(repo / skill / "SKILL.md") for skill in CORE_SKILLS)
    for item in semantics:
        target = str(item.get("target", ""))
        if target == "四个当前 SKILL.md" or target == "四个需求 SKILL.md":
            target_text = core_corpus
        else:
            target_path = repo / target.split("#", 1)[0]
            target_text = read_utf8(target_path) if target_path.is_file() else ""
        missing = [token for token in item.get("assertion", []) if token not in target_text]
        if missing:
            errors.append(f"protected semantic missing {item.get('id')}: {missing}")
        semantic_results.append({"id": item.get("id"), "missing": missing, "valid": not missing})

    splitting_root = repo / "requirement-splitting-rules"
    change_root = repo / "requirement-change-rules"
    splitting = read_utf8(splitting_root / "SKILL.md")
    change = read_utf8(change_root / "SKILL.md")
    splitting_corpus = "\n".join(
        read_utf8(path)
        for path in splitting_root.rglob("*")
        if path.is_file() and path.suffix.lower() in {".md", ".yaml", ".yml"}
    )
    change_corpus = "\n".join(
        read_utf8(path)
        for path in change_root.rglob("*")
        if path.is_file() and path.suffix.lower() in {".md", ".yaml", ".yml"}
    )
    splitting_required = (
        "本 Skill 不冻结代码文件/符号",
        "不创建实施总览或周期",
        "不定义真实测试命令",
        "implementation-planning-rules",
    )
    change_required = (
        "不定义实施总览、周期、文件/符号或测试命令",
        "implementation-planning-rules",
    )
    if any(token not in splitting for token in splitting_required):
        errors.append("splitting responsibility delegation is incomplete")
    if any(token not in change for token in change_required):
        errors.append("change responsibility delegation is incomplete")
    for heading in BANNED_IMPLEMENTATION_HEADINGS:
        if heading in splitting_corpus:
            errors.append(f"splitting owns forbidden implementation heading: {heading}")
        if heading in change_corpus:
            errors.append(f"change owns forbidden implementation heading: {heading}")

    data.update(
        {
            "markdown_links_checked": len(links),
            "broken_links": link_errors,
            "utf8_file_count": utf8_count,
            "single_line_markdown": single_line,
            "agent_results": agent_results,
            "reference_reachability": reference_reachability,
            "script_results": script_results,
            "gap_semantic_coverage": gap_coverage,
            "protected_semantic_results": semantic_results,
        }
    )
    return errors, data


def phase_post_cleanup(repo: Path, manifest: dict) -> tuple[list[str], dict]:
    consumer_errors, consumer_data = phase_consumer(repo, manifest)
    reference_errors, reference_data = phase_reference(repo, manifest)
    errors = consumer_errors + reference_errors

    root_skill_directories = sum(1 for path in repo.glob("*/SKILL.md") if path.is_file())
    try:
        summary = dictionary_summary(repo)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        errors.append(f"dictionary invalid: {exc}")
        summary = {}
    if summary.get("implemented_total") != manifest.get("expected_skill_total"):
        errors.append(f"dictionary implemented_total mismatch: {summary.get('implemented_total')}")
    if summary.get("planned_missing") != manifest.get("expected_planned_missing"):
        errors.append(f"dictionary planned_missing mismatch: {summary.get('planned_missing')}")

    cache_files = [
        path.relative_to(repo).as_posix()
        for path in (repo / "doc/5-tests/2026-07-22_231500/requirement-domain-streamlining").rglob("*")
        if path.is_file() and ("__pycache__" in path.parts or path.suffix == ".pyc")
    ]
    if cache_files:
        errors.append(f"runtime cache assets present: {cache_files}")
    return errors, {
        **consumer_data,
        **reference_data,
        "skill_total": summary.get("implemented_total"),
        "root_skill_directories": root_skill_directories,
        "dictionary_summary": summary,
        "runtime_cache_assets": cache_files,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument(
        "--phase",
        choices=("baseline", "trigger", "consumer", "reference", "post-cleanup"),
        required=True,
    )
    args = parser.parse_args()
    repo = args.repo_root.resolve()
    try:
        manifest = load_yaml(args.manifest.resolve())
        functions = {
            "baseline": phase_baseline,
            "trigger": phase_trigger,
            "consumer": phase_consumer,
            "reference": phase_reference,
            "post-cleanup": phase_post_cleanup,
        }
        errors, data = functions[args.phase](repo, manifest)
    except Exception as exc:  # 验证器必须把意外失败转成明确 FAIL，而不是误报 PASS。
        errors, data = [f"validator exception: {type(exc).__name__}: {exc}"], {}
    output = {
        "valid": not errors,
        "phase": args.phase,
        "repo_root": str(repo),
        "errors": errors,
        "data": data,
    }
    print(json.dumps(output, ensure_ascii=False, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    sys.exit(main())
