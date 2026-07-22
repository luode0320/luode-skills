from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import yaml

# 验证周期 04 的条件路由、触发契约、迁移资产和 source 退役状态。
CYCLE_SOURCES = {
    "bug-assertion-diagnostic-rules",
    "bug-debug-log-rules",
    "bug-discovery-rules",
    "bug-gap-rules",
    "bug-runtime-debug-rules",
}
RETAINED_SKILLS = {
    "bug-fix-proposal-rules",
    "bug-intake-rules",
    "bug-regression-risk-rules",
    "bug-reproduction-rules",
    "bug-root-cause-rules",
    "bug-validation-rules",
}
ALLOWED_HISTORICAL_LEGACY_REFERENCES = {
    "README.md": {"bug-discovery-rules"},
}

REQUIRED_SEMANTICS = {
    "discovery-and-gap": [
        "先主动查看代码",
        "一次推进一个真实问题",
        "local 配置",
        "禁止增删改",
        "Mermaid 流程图",
        "Mermaid 时序图",
        "暂停",
        "回滚",
    ],
    "runtime-diagnostics": [
        "状态不变量",
        "诊断断言",
        "临时 debug 日志",
        "项目 logger",
        "退出条件",
        "local 配置",
        "清理",
        "回滚",
    ],
}


def parse_args() -> argparse.Namespace:
    """[参数]：无，读取命令行参数；[返回]：已校验的参数对象；最近修改时间：2026-07-21。"""
    # 1. 固定验证输入，避免调用方绕过 source、mapping 或阶段约束。
    parser = argparse.ArgumentParser(description="验证周期04 Bug owner route、资产迁移、触发契约和退役状态")
    parser.add_argument("--repo-root", required=True)
    parser.add_argument("--manifest", required=True)
    parser.add_argument("--migration-map", required=True)
    parser.add_argument("--phase", choices=["pre-delete", "post-delete"], required=True)
    return parser.parse_args()


def read_tree(root: Path) -> str:
    """[参数]：Skill 根目录；[返回]：全部 UTF-8 文件的合并文本；最近修改时间：2026-07-21。"""
    # 1. 将 owner 的 SKILL、references 和 agents 统一纳入触发与规则承接断言。
    return "\n".join(path.read_text(encoding="utf-8") for path in sorted(root.rglob("*")) if path.is_file())


def main() -> int:
    """[参数]：通过 parse_args 取得输入；[返回]：0 表示通过，1 表示存在确定性错误；最近修改时间：2026-07-21。"""
    # 1. 读取冻结清单、迁移映射、触发 fixtures 和消费者索引，建立同一轮验证事实。
    args = parse_args()
    root = Path(args.repo_root).resolve()
    manifest = yaml.safe_load(Path(args.manifest).read_text(encoding="utf-8"))
    route_map = yaml.safe_load(Path(args.migration_map).read_text(encoding="utf-8"))
    fixtures = yaml.safe_load(
        (root / "doc/5-tests/2026-07-21_221037/six-domain-skill-streamlining/fixtures/trigger-cases.yaml").read_text(encoding="utf-8")
    )["cases"]
    consumer_index: dict[str, list[str]] = json.loads(
        (root / "doc/5-tests/2026-07-21_221037/six-domain-skill-streamlining/inventory/active-consumers.json").read_text(encoding="utf-8")
    )
    errors: list[str] = []
    candidates = {
        item["source_skill"]: item
        for item in manifest["candidates"]
        if item["source_skill"] in CYCLE_SOURCES
    }
    maps = {item["source_skill"]: item for item in route_map["owner_routes"]}
    if set(candidates) != CYCLE_SOURCES:
        errors.append(f"manifest 周期04候选不完整: {sorted(candidates)}")
    if set(maps) != CYCLE_SOURCES:
        errors.append(f"route map 周期04 source 不完整: {sorted(maps)}")

    # 2. 逐一检查每个待退役 source 的 canonical owner、route、资产和保护语义。
    for source in sorted(CYCLE_SOURCES):
        candidate = candidates.get(source)
        migration = maps.get(source)
        if candidate is None or migration is None:
            continue
        owner = root / candidate["target_owner"]
        route = candidate["target_route"]
        route_doc = root / migration.get("target_route_document", "")
        if not (owner / "SKILL.md").is_file():
            errors.append(f"target owner 缺失: {source} -> {candidate['target_owner']}")
            continue
        target_text = read_tree(owner)
        if f"条件路由：{route}" not in (owner / "SKILL.md").read_text(encoding="utf-8"):
            errors.append(f"owner route marker 缺失: {source} -> {route}")
        if not route_doc.is_file():
            errors.append(f"条件路由文档缺失: {source} -> {route_doc}")
        else:
            route_text = route_doc.read_text(encoding="utf-8")
            if "bug-intake-rules 的 `" in route_text:
                errors.append(f"路由文档存在嵌套反引号: {route_doc}")
        for alias in candidate.get("trigger_contract", {}).get("trigger_aliases", []):
            if alias not in target_text:
                errors.append(f"触发别名未承接: {source}: {alias}")
        for token in REQUIRED_SEMANTICS[route]:
            if token not in target_text:
                errors.append(f"保护语义未承接: {source}/{route}: {token}")
        for asset in migration.get("migrated_assets", []):
            if not (root / asset).is_file():
                errors.append(f"迁移资源缺失: {source}: {asset}")
        if args.phase == "pre-delete":
            source_files = {path.relative_to(root).as_posix() for path in (root / source).rglob("*") if path.is_file()}
            if not source_files:
                errors.append(f"pre-delete source 缺失: {source}")
            if set(migration.get("source_assets", [])) != source_files:
                errors.append(f"source 资产清单不完整或漂移: {source}")
        else:
            if (root / source).exists():
                errors.append(f"post-delete source 仍存在: {source}")
            stale_paths = [path for path in consumer_index.get(source, []) if path.startswith(source + "/")]
            if stale_paths:
                errors.append(f"consumer index 仍保留 source 自引用: {source}: {stale_paths}")

    # 3. 用冻结的正负 fixtures 确认自动触发别名没有因入口合并而丢失或误扩张。
    fixture_by_id = {case["id"]: case for case in fixtures if case["source_skill"] in CYCLE_SOURCES}
    for source, candidate in candidates.items():
        for fixture_id in candidate["trigger_contract"]["positive_fixture_ids"]:
            case = fixture_by_id.get(fixture_id)
            if case is None:
                errors.append(f"缺少正例 fixture: {fixture_id}")
                continue
            target_text = read_tree(root / case["target_owner"])
            for token in case.get("required_target_tokens", []):
                if token not in target_text:
                    errors.append(f"正例 target token 缺失: {fixture_id}: {token}")
            if not case.get("required_source_tokens"):
                errors.append(f"正例 source token 为空: {fixture_id}")
        for fixture_id in candidate["trigger_contract"]["negative_fixture_ids"]:
            case = fixture_by_id.get(fixture_id)
            if case is None:
                errors.append(f"缺少负例 fixture: {fixture_id}")
                continue
            if case.get("required_source_tokens") or case.get("required_target_tokens"):
                errors.append(f"负例不应携带 required token: {fixture_id}")

    # 4. 防止边界扩大：六个保留 Bug Skill 必须仍然存在。
    for retained in sorted(RETAINED_SKILLS):
        if not (root / retained / "SKILL.md").is_file():
            errors.append(f"不应退役的 Bug skill 缺失: {retained}")

    # 5. 索引只能引用现存资产；.tmp 历史快照不属于活跃消费者。
    for source, paths in consumer_index.items():
        for raw in paths:
            if raw.startswith(".tmp/"):
                continue
            if not (root / raw).exists():
                errors.append(f"active consumer index 指向不存在路径: {source}: {raw}")

    # 6. 删除后禁止活跃消费者继续直指旧入口；迁移资源文件名和 README 历史记录例外可追溯。
    for source in sorted(CYCLE_SOURCES):
        migration = maps[source]
        for raw in consumer_index.get(source, []):
            if raw.startswith(".tmp/") or raw in {"skill-dictionary/data.js", "字典.md"}:
                continue
            path = root / raw
            if not path.is_file():
                continue
            content = path.read_text(encoding="utf-8")
            for asset in migration.get("migrated_assets", []):
                content = content.replace(asset, "")
            if source in content and source not in ALLOWED_HISTORICAL_LEGACY_REFERENCES.get(raw, set()):
                errors.append(f"活跃 consumer 仍引用退役 source: {source}: {raw}")

    # 7. 仅在全部断言满足时返回成功，供 pre-delete 与 post-delete 门禁复用。
    report: dict[str, Any] = {
        "schema_version": 1,
        "phase": args.phase,
        "candidate_count": len(candidates),
        "retained_count": len(RETAINED_SKILLS),
        "valid": not errors,
        "errors": errors,
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
