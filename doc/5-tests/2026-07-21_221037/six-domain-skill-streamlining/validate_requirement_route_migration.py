from __future__ import annotations

import argparse
import json
from pathlib import Path

import yaml


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="验证需求域 initial-discovery 路由迁移")
    parser.add_argument("--repo-root", required=True)
    parser.add_argument("--fixtures", required=True)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = Path(args.repo_root).resolve()
    fixtures_path = Path(args.fixtures).resolve()
    owner = root / "requirement-intake-rules"
    source = root / "requirement-discovery-rules"
    skill_path = owner / "SKILL.md"
    route_path = owner / "references" / "initial-discovery-route.md"
    required_refs = [
        owner / "references" / "initial-discovery-checklist.md",
        owner / "references" / "initial-discovery-evidence-and-memory.md",
        owner / "references" / "initial-discovery-output-template.md",
        owner / "references" / "initial-discovery-domain-routing.md",
    ]
    errors: list[str] = []
    if not skill_path.is_file():
        errors.append("主入口 SKILL.md 不存在")
    if not route_path.is_file():
        errors.append("initial-discovery route reference 不存在")
    if not source.joinpath("SKILL.md").is_file():
        errors.append("删除前冻结基线 source 不存在")
    text = skill_path.read_text(encoding="utf-8") if skill_path.is_file() else ""
    route_text = route_path.read_text(encoding="utf-8") if route_path.is_file() else ""
    if "initial-discovery" not in text:
        errors.append("主入口缺少 initial-discovery marker")
    if "只读优先" not in route_text or "local" not in route_text or "project-memory-rules" not in route_text:
        errors.append("route reference 缺少只读/local/记忆回写保护语义")
    if "requirement-discovery-rules" in text or "requirement-discovery-rules" in route_text:
        errors.append("目标 owner 仍残留旧竞争入口名称")
    for path in required_refs:
        if not path.is_file():
            errors.append(f"迁移 reference 不存在：{path.relative_to(root).as_posix()}")
    fixture_data = yaml.safe_load(fixtures_path.read_text(encoding="utf-8"))
    cases = fixture_data.get("cases", []) if isinstance(fixture_data, dict) else []
    selected = [
        case for case in cases
        if isinstance(case, dict)
        and case.get("source_skill") == "requirement-discovery-rules"
    ]
    if len(selected) != 2:
        errors.append(f"discovery fixtures 数量应为 2，实际为 {len(selected)}")
    for case in selected:
        prompt = str(case.get("prompt", ""))
        required = [str(item) for item in case.get("required_target_tokens", [])]
        if case.get("id", "").endswith("-POS"):
            for token in required:
                if token not in text:
                    errors.append(f"正例 token 未在 owner 中出现：{token}")
            if case.get("target_owner") != "requirement-intake-rules":
                errors.append("正例 target_owner 不是 requirement-intake-rules")
            if case.get("target_route") != "initial-discovery":
                errors.append("正例 target_route 不是 initial-discovery")
        if case.get("id", "").endswith("-NEG") and required:
            errors.append(f"负例不应声明 required_target_tokens：{prompt}")
    report = {"task": "TASK-SS-02-01", "valid": not errors, "errors": errors}
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())