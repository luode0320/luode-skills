#!/usr/bin/env python3
"""
上线前接口测试资产初始化与计划生成工具

能力：
1. bootstrap-inventory: 冷启动扫描项目接口，生成初版接口基线
2. reconcile-inventory: 扫描当前接口事实并与已有基线对账
3. generate-plan: 基于更新后的接口基线生成测试计划
4. init-release-test-task: 初始化上线前接口测试任务目录骨架
"""

from __future__ import annotations

import argparse
import json
import os
import re
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Dict, Iterable, List, Tuple

import yaml


ROUTE_PATTERNS: List[Tuple[str, re.Pattern[str]]] = [
    (
        "route",
        re.compile(
            r"""(?ix)
            (?P<method>GET|POST|PUT|PATCH|DELETE)\s*
            [(:=,\s"']+
            (?P<path>/[A-Za-z0-9_\-./:{}]+)
            """
        ),
    ),
    (
        "route",
        re.compile(
            r"""(?ix)
            \.(?P<method>GET|POST|PUT|PATCH|DELETE)\s*
            \(\s*
            ["'](?P<path>/[A-Za-z0-9_\-./:{}]+)["']
            """
        ),
    ),
    (
        "swagger",
        re.compile(
            r"""(?mx)
            ^\s*(?P<path>/[A-Za-z0-9_\-./:{}]+)\s*:\s*$
            """
        ),
    ),
]

METHOD_PATH_LINE_PATTERN = re.compile(
    r"""(?ix)
    (?P<method>GET|POST|PUT|PATCH|DELETE)\s+
    (?P<path>/[A-Za-z0-9_\-./:{}]+)
    """
)

PATH_HINT_PATTERN = re.compile(r"/[A-Za-z0-9_\-./:{}]+")
CHANGED_FILE_MODULE_HINT = re.compile(r"[/\\](api|apis|controller|controllers|handler|handlers|router|routes?)[/\\]")

DEFAULT_RISK_BY_KEYWORD = {
    "支付": "P0",
    "退款": "P0",
    "结算": "P0",
    "交易": "P0",
    "订单": "P0",
    "登录": "P0",
    "鉴权": "P0",
    "权限": "P0",
    "auth": "P0",
    "login": "P0",
    "pay": "P0",
    "order": "P0",
}


def utc_now_str() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def read_yaml(path: Path, default):
    if not path.exists():
        return default
    with path.open("r", encoding="utf-8") as file:
        data = yaml.safe_load(file)
    return default if data is None else data


def write_yaml(path: Path, data) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as file:
        yaml.safe_dump(data, file, allow_unicode=True, sort_keys=False)


def load_interface_inventory(inventory_path: Path) -> List[Dict]:
    inventory = read_yaml(inventory_path, [])
    if not isinstance(inventory, list):
        raise ValueError(f"接口基线文件格式非法，应为列表：{inventory_path}")
    return inventory


def normalize_path(path: str) -> str:
    normalized = path.strip()
    if not normalized.startswith("/"):
        normalized = f"/{normalized.lstrip('/')}"
    return normalized


def infer_module(path: str, file_path: Path) -> str:
    parts = [segment for segment in normalize_path(path).split("/") if segment]
    if len(parts) >= 2 and parts[0].lower() in {"api", "openapi", "rest"}:
        return parts[1]
    if parts:
        return parts[0]

    file_parts = [part.lower() for part in file_path.parts]
    for index, part in enumerate(file_parts):
        if part in {"controller", "controllers", "handler", "handlers", "router", "routers", "routes"} and index + 1 < len(file_parts):
            return file_path.parts[index + 1]
    return file_path.parent.name or "unknown"


def infer_risk(interface_name: str, path: str) -> str:
    text = f"{interface_name} {path}".lower()
    for keyword, level in DEFAULT_RISK_BY_KEYWORD.items():
        if keyword.lower() in text:
            return level
    return "P1" if any(word in text for word in ("create", "update", "delete", "submit")) else "P2"


def build_interface_id(module: str, path: str, method: str) -> str:
    cleaned_path = normalize_path(path).strip("/").replace("/", "_").replace("{", "").replace("}", "").replace(":", "")
    cleaned_module = re.sub(r"[^a-zA-Z0-9_]+", "_", module or "unknown")
    return f"{cleaned_module}_{cleaned_path or 'root'}_{method.upper()}".strip("_")


def build_interface_name(path: str, method: str, module: str) -> str:
    tail = normalize_path(path).strip("/").split("/")[-1] or "root"
    return f"{module}模块{tail}接口({method.upper()})"


def inventory_record(method: str, path: str, source: str, evidence: str, file_path: Path) -> Dict:
    normalized_path = normalize_path(path)
    module = infer_module(normalized_path, file_path)
    interface_id = build_interface_id(module, normalized_path, method)
    interface_name = build_interface_name(normalized_path, method, module)
    risk_level = infer_risk(interface_name, normalized_path)

    return {
        "接口标识": interface_id,
        "接口名称": interface_name,
        "HTTP 方法": method.upper(),
        "接口路径": normalized_path,
        "所属模块": module,
        "鉴权要求": "待确认",
        "请求参数 schema": "{}",
        "响应结构摘要": "{}",
        "业务成功判定": "待确认",
        "业务失败判定": "待确认",
        "依赖数据": "待确认",
        "数据副作用": "待确认",
        "清理方式": "待确认",
        "风险等级": risk_level,
        "是否上线必测": "是" if risk_level == "P0" else "否",
        "最近扫描时间": utc_now_str(),
        "最近测试时间": "",
        "最近测试结论": "待确认",
        "发现来源": source,
        "发现证据": evidence,
        "完整度": "部分",
        "待确认项": [
            "鉴权要求",
            "请求参数 schema",
            "响应结构摘要",
            "业务成功判定",
            "业务失败判定",
            "依赖数据",
            "数据副作用",
            "清理方式",
        ],
        "最近扫描提交": "",
    }


def is_candidate_file(file_path: Path) -> bool:
    if any(part.startswith(".") and part != ".github" for part in file_path.parts):
        return False
    if any(part in {"node_modules", "vendor", "dist", "build", "coverage", ".git"} for part in file_path.parts):
        return False
    return file_path.suffix.lower() in {
        ".go",
        ".ts",
        ".tsx",
        ".js",
        ".jsx",
        ".java",
        ".kt",
        ".py",
        ".php",
        ".rb",
        ".yaml",
        ".yml",
        ".json",
        ".md",
    }


def scan_project_interfaces(project_root: Path) -> List[Dict]:
    discovered: Dict[Tuple[str, str], Dict] = {}

    for file_path in project_root.rglob("*"):
        if not file_path.is_file() or not is_candidate_file(file_path):
            continue

        try:
            content = file_path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue

        for source, pattern in ROUTE_PATTERNS:
            for match in pattern.finditer(content):
                method = match.groupdict().get("method")
                path = match.groupdict().get("path")
                if not path:
                    continue
                if not method:
                    method = "GET" if source == "swagger" else "UNKNOWN"
                key = (method.upper(), normalize_path(path))
                evidence = f"{file_path.relative_to(project_root)}:{content[: match.start()].count(chr(10)) + 1}"
                record = inventory_record(method, path, source, evidence, file_path)
                existing = discovered.get(key)
                if existing:
                    if source not in existing["发现来源"].split(","):
                        existing["发现来源"] = f"{existing['发现来源']},{source}"
                    if evidence not in existing["发现证据"]:
                        existing["发现证据"] = f"{existing['发现证据']}; {evidence}"
                else:
                    discovered[key] = record

        for line_number, line in enumerate(content.splitlines(), 1):
            match = METHOD_PATH_LINE_PATTERN.search(line)
            if not match:
                continue
            key = (match.group("method").upper(), normalize_path(match.group("path")))
            evidence = f"{file_path.relative_to(project_root)}:{line_number}"
            record = inventory_record(match.group("method"), match.group("path"), "doc", evidence, file_path)
            existing = discovered.get(key)
            if existing:
                if "doc" not in existing["发现来源"].split(","):
                    existing["发现来源"] = f"{existing['发现来源']},doc"
                if evidence not in existing["发现证据"]:
                    existing["发现证据"] = f"{existing['发现证据']}; {evidence}"
            else:
                discovered[key] = record

    return sorted(discovered.values(), key=lambda item: (item["所属模块"], item["接口路径"], item["HTTP 方法"]))


def key_by_identity(interface: Dict) -> Tuple[str, str]:
    return interface["HTTP 方法"].upper(), normalize_path(interface["接口路径"])


def reconcile_inventory(existing_inventory: List[Dict], scanned_inventory: List[Dict], current_revision: str) -> Dict:
    existing_map = {key_by_identity(item): item for item in existing_inventory}
    scanned_map = {key_by_identity(item): item for item in scanned_inventory}

    additions: List[Dict] = []
    removals: List[Dict] = []
    changes: List[Dict] = []
    pending: List[Dict] = []
    updated_inventory: List[Dict] = []

    all_keys = sorted(set(existing_map) | set(scanned_map))
    tracked_fields = [
        "接口标识",
        "接口名称",
        "所属模块",
        "鉴权要求",
        "请求参数 schema",
        "响应结构摘要",
        "业务成功判定",
        "业务失败判定",
        "依赖数据",
        "数据副作用",
        "清理方式",
        "风险等级",
        "是否上线必测",
    ]

    for key in all_keys:
        existing = existing_map.get(key)
        scanned = scanned_map.get(key)

        if existing is None and scanned is not None:
            scanned["最近扫描提交"] = current_revision
            additions.append(
                {
                    "接口标识": scanned["接口标识"],
                    "HTTP 方法": scanned["HTTP 方法"],
                    "接口路径": scanned["接口路径"],
                    "差异类型": "新增",
                    "来源证据": scanned["发现证据"],
                }
            )
            if scanned.get("待确认项"):
                pending.append(
                    {
                        "接口标识": scanned["接口标识"],
                        "HTTP 方法": scanned["HTTP 方法"],
                        "接口路径": scanned["接口路径"],
                        "差异类型": "待确认",
                        "待确认项": scanned["待确认项"],
                    }
                )
            updated_inventory.append(scanned)
            continue

        if existing is not None and scanned is None:
            retired = dict(existing)
            retired["完整度"] = "待确认"
            retired["待确认项"] = sorted(set(retired.get("待确认项", [])) | {"废弃标记"})
            retired["最近扫描时间"] = utc_now_str()
            retired["最近扫描提交"] = current_revision
            removals.append(
                {
                    "接口标识": retired["接口标识"],
                    "HTTP 方法": retired["HTTP 方法"],
                    "接口路径": retired["接口路径"],
                    "差异类型": "删除",
                }
            )
            updated_inventory.append(retired)
            continue

        assert existing is not None and scanned is not None

        merged = dict(existing)
        merged["最近扫描时间"] = utc_now_str()
        merged["最近扫描提交"] = current_revision
        merged["发现来源"] = scanned["发现来源"]
        merged["发现证据"] = scanned["发现证据"]

        changed_fields: List[str] = []
        for field in tracked_fields:
            if existing.get(field) != scanned.get(field) and scanned.get(field) not in {"待确认", "{}", "", None}:
                merged[field] = scanned[field]
                changed_fields.append(field)

        if changed_fields:
            changes.append(
                {
                    "接口标识": merged["接口标识"],
                    "HTTP 方法": merged["HTTP 方法"],
                    "接口路径": merged["接口路径"],
                    "差异类型": "变更",
                    "变更字段": changed_fields,
                }
            )

        pending_items = list(dict.fromkeys(scanned.get("待确认项", []) + existing.get("待确认项", [])))
        if pending_items:
            pending.append(
                {
                    "接口标识": merged["接口标识"],
                    "HTTP 方法": merged["HTTP 方法"],
                    "接口路径": merged["接口路径"],
                    "差异类型": "待确认",
                    "待确认项": pending_items,
                }
            )
        merged["待确认项"] = pending_items
        merged["完整度"] = "完整" if not pending_items else "待确认"
        updated_inventory.append(merged)

    updated_inventory.sort(key=lambda item: (item["所属模块"], item["接口路径"], item["HTTP 方法"]))
    return {
        "summary": {
            "新增接口数": len(additions),
            "删除接口数": len(removals),
            "变更接口数": len(changes),
            "待确认接口数": len(pending),
            "扫描时间": utc_now_str(),
            "最近扫描提交": current_revision,
        },
        "additions": additions,
        "removals": removals,
        "changes": changes,
        "pending": pending,
        "updated_inventory": updated_inventory,
    }


def changed_modules_from_inventory(inventory: List[Dict], changed_modules: List[str]) -> List[str]:
    if changed_modules:
        return changed_modules
    return sorted({item.get("所属模块", "unknown") for item in inventory if item.get("所属模块")})


def filter_test_interfaces(inventory: List[Dict], changed_modules: List[str], include_p2: bool = False) -> Dict:
    p0_list: List[Dict] = []
    p1_list: List[Dict] = []
    p2_list: List[Dict] = []
    skipped_list: List[Dict] = []

    changed_modules = changed_modules_from_inventory(inventory, changed_modules)

    for interface in inventory:
        risk_level = interface.get("风险等级", "P2")
        module = interface.get("所属模块", "")
        must_test = interface.get("是否上线必测", "否") == "是"

        if risk_level == "P0":
            p0_list.append(interface)
            continue

        if risk_level == "P1":
            if module in changed_modules or must_test:
                p1_list.append(interface)
            else:
                skipped_list.append({"接口": interface["接口标识"], "理由": "非改动模块 P1 接口，本次跳过"})
            continue

        if include_p2 and (module in changed_modules or must_test):
            p2_list.append(interface)
        else:
            skipped_list.append({"接口": interface["接口标识"], "理由": "非改动模块 P2 接口，本次跳过"})

    return {
        "summary": {
            "总接口数": len(inventory),
            "必测P0接口数": len(p0_list),
            "必测P1接口数": len(p1_list),
            "必测P2接口数": len(p2_list),
            "跳过接口数": len(skipped_list),
            "本次改动模块": changed_modules,
        },
        "p0_interfaces": p0_list,
        "p1_interfaces": p1_list,
        "p2_interfaces": p2_list,
        "skipped_interfaces": skipped_list,
    }


def ensure_release_task_root(task_root: Path, title: str) -> Dict[str, str]:
    task_root.mkdir(parents=True, exist_ok=True)
    chinese_dir = task_root / title
    ascii_dir = task_root / "ascii-artifacts"
    artifacts_dir = ascii_dir / "artifacts"
    logs_dir = artifacts_dir / "logs"
    raw_request_dir = artifacts_dir / "raw-request"
    raw_response_dir = artifacts_dir / "raw-response"
    masked_response_dir = artifacts_dir / "masked-response"
    scripts_dir = ascii_dir / "scripts"
    plan_path = ascii_dir / "release-test-plan.yaml"
    reconcile_path = ascii_dir / "inventory-reconcile.yaml"
    results_path = ascii_dir / "interface-test-results.md"
    execute_log_path = logs_dir / "execute.log"

    for directory in (chinese_dir, ascii_dir, artifacts_dir, logs_dir, raw_request_dir, raw_response_dir, masked_response_dir, scripts_dir):
        directory.mkdir(parents=True, exist_ok=True)

    readme_path = chinese_dir / "README.md"
    if not readme_path.exists():
        readme_path.write_text(
            "\n".join(
                [
                    "# 上线前项目接口测试",
                    "",
                    "## 说明",
                    f"- 创建时间：{utc_now_str()}",
                    "- 当前目录用于承接项目级上线接口测试门禁。",
                    "- 若本次为冷启动，请在此记录扫描来源、对账结果与待确认项。",
                ]
            ),
            encoding="utf-8",
        )

    if not plan_path.exists():
        plan_path.write_text(
            "\n".join(
                [
                    "summary:",
                    "  总接口数: 0",
                    "  必测P0接口数: 0",
                    "  必测P1接口数: 0",
                    "  必测P2接口数: 0",
                    "  跳过接口数: 0",
                    "  本次改动模块: []",
                    "p0_interfaces: []",
                    "p1_interfaces: []",
                    "p2_interfaces: []",
                    "skipped_interfaces: []",
                ]
            ),
            encoding="utf-8",
        )

    if not reconcile_path.exists():
        reconcile_path.write_text(
            "\n".join(
                [
                    "summary:",
                    "  新增接口数: 0",
                    "  删除接口数: 0",
                    "  变更接口数: 0",
                    "  待确认接口数: 0",
                    "  扫描时间: ''",
                    "  最近扫描提交: ''",
                    "additions: []",
                    "removals: []",
                    "changes: []",
                    "pending: []",
                ]
            ),
            encoding="utf-8",
        )

    if not results_path.exists():
        results_path.write_text(
            "\n".join(
                [
                    "# 接口测试明细",
                    "",
                    "## 说明",
                    "- 本文件用于记录接口级测试结果，禁止改为 Markdown 表格。",
                    "- 每个接口使用块状格式记录请求参数、简要响应、判定理由和最终结论。",
                ]
            ),
            encoding="utf-8",
        )

    if not execute_log_path.exists():
        execute_log_path.write_text("", encoding="utf-8")

    return {
        "task_root": str(task_root),
        "readme": str(readme_path),
        "ascii_dir": str(ascii_dir),
        "logs_dir": str(logs_dir),
        "plan": str(plan_path),
        "reconcile": str(reconcile_path),
        "results": str(results_path),
    }


def current_revision(project_root: Path) -> str:
    git_head = project_root / ".git"
    return "working-tree" if not git_head.exists() else os.environ.get("GIT_REVISION", "working-tree")


def print_json(data) -> None:
    print(json.dumps(data, ensure_ascii=False, indent=2))


def command_bootstrap_inventory(args: argparse.Namespace) -> None:
    project_root = Path(args.project_root).resolve()
    inventory_path = Path(args.inventory).resolve()
    scanned_inventory = scan_project_interfaces(project_root)
    revision = current_revision(project_root)
    for item in scanned_inventory:
        item["最近扫描提交"] = revision
    write_yaml(inventory_path, scanned_inventory)
    print_json(
        {
            "mode": "bootstrap-inventory",
            "inventory_path": str(inventory_path),
            "interface_count": len(scanned_inventory),
            "recent_scan_revision": revision,
        }
    )


def command_reconcile_inventory(args: argparse.Namespace) -> None:
    project_root = Path(args.project_root).resolve()
    inventory_path = Path(args.inventory).resolve()
    reconcile_output = Path(args.output).resolve()
    existing_inventory = load_interface_inventory(inventory_path) if inventory_path.exists() else []
    scanned_inventory = scan_project_interfaces(project_root)
    revision = current_revision(project_root)
    reconcile_result = reconcile_inventory(existing_inventory, scanned_inventory, revision)
    write_yaml(inventory_path, reconcile_result["updated_inventory"])
    reconcile_payload = {key: value for key, value in reconcile_result.items() if key != "updated_inventory"}
    write_yaml(reconcile_output, reconcile_payload)
    print_json(
        {
            "mode": "reconcile-inventory",
            "inventory_path": str(inventory_path),
            "reconcile_output": str(reconcile_output),
            **reconcile_result["summary"],
        }
    )


def command_generate_plan(args: argparse.Namespace) -> None:
    inventory_path = Path(args.inventory).resolve()
    output_path = Path(args.output).resolve()
    inventory = load_interface_inventory(inventory_path)
    changed_modules = args.modules or []
    test_plan = filter_test_interfaces(inventory, changed_modules, args.include_p2)
    write_yaml(output_path, test_plan)
    print_json(
        {
            "mode": "generate-plan",
            "output_path": str(output_path),
            **test_plan["summary"],
        }
    )


def command_init_release_test_task(args: argparse.Namespace) -> None:
    task_root = Path(args.task_root).resolve()
    result = ensure_release_task_root(task_root, args.title)
    print_json({"mode": "init-release-test-task", **result})


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="上线前接口测试资产初始化与计划生成工具")
    subparsers = parser.add_subparsers(dest="command", required=True)

    bootstrap_parser = subparsers.add_parser("bootstrap-inventory", help="冷启动扫描项目接口并生成初版接口基线")
    bootstrap_parser.add_argument("--project-root", required=True, help="项目根目录")
    bootstrap_parser.add_argument("--inventory", required=True, help="输出接口基线文件路径")
    bootstrap_parser.set_defaults(func=command_bootstrap_inventory)

    reconcile_parser = subparsers.add_parser("reconcile-inventory", help="扫描当前接口事实并与已有基线对账")
    reconcile_parser.add_argument("--project-root", required=True, help="项目根目录")
    reconcile_parser.add_argument("--inventory", required=True, help="接口基线文件路径")
    reconcile_parser.add_argument("--output", default="inventory-reconcile.yaml", help="对账结果输出路径")
    reconcile_parser.set_defaults(func=command_reconcile_inventory)

    generate_parser = subparsers.add_parser("generate-plan", help="基于更新后的接口基线生成测试计划")
    generate_parser.add_argument("--inventory", required=True, help="接口基线文件路径")
    generate_parser.add_argument("--modules", nargs="*", default=[], help="本次上线改动的模块列表，空格分隔")
    generate_parser.add_argument("--include-p2", action="store_true", help="是否包含改动模块的 P2 接口，默认不包含")
    generate_parser.add_argument("--output", default="release-test-plan.yaml", help="输出测试计划文件路径")
    generate_parser.set_defaults(func=command_generate_plan)

    init_parser = subparsers.add_parser("init-release-test-task", help="初始化上线前接口测试任务目录骨架")
    init_parser.add_argument("--task-root", required=True, help="测试任务时间戳根目录路径")
    init_parser.add_argument("--title", default="上线前项目接口测试", help="中文说明目录名")
    init_parser.set_defaults(func=command_init_release_test_task)

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
