#!/usr/bin/env python3
"""三类项目代码位置 Catalog 的查询、渲染、初始化与只读检查入口。"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any

# 收敛清单优先支持普通 YAML；依赖缺失时保留 JSON 兼容清单的只读降级。
try:
    import yaml
except ModuleNotFoundError:
    yaml = None


ROOT = Path(__file__).resolve().parents[1]
CATALOG_PATH = ROOT / "references" / "placement-catalog.yaml"
LAYOUT_PATH = ROOT / "references" / "project-layout-v2.md"
SOURCE_EXTENSIONS = {".go", ".java", ".ts", ".js", ".py"}
SOURCE_UTIL_EXTENSIONS = {
    "go": {".go"},
    "java": {".java"},
    "node": {".ts", ".js"},
    "python": {".py"},
}
SOURCE_ROOTS = {
    "go": "internal",
    "node": "src",
    "python": "src/<package>",
}
ADOPTION_MANIFEST_PATH = "doc/1-架构/3-目录规则收敛清单.yaml"
ADOPTION_V2_SOURCE_ROOTS = {
    "backend": {"cmd", "config", "data", "database", "swag", "resources", "utils", "common", "global", "crontask", "async", "middleware", "internal", "src", "scripts", "tools", "deploy", "doc"},
    "frontend": {"config", "public", "src", "mocks", "scripts", "tools", "deploy", "doc", ".storybook"},
    "fullstack": {"backend", "frontend", "integration", "doc"},
}

# Windows 控制台默认代码页可能不是 UTF-8；CLI 的机器输出必须稳定为 UTF-8。
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")


def load_catalog() -> dict[str, Any]:
    """读取 JSON 兼容 YAML，避免引入额外 YAML 运行依赖。

    [参数] 无。
    [返回] dict：目录规则的机器可读数据。
    最近修改时间: 2026-07-28 22:40:00 移除旧树后保留唯一 Catalog 数据入口。
    """
    return json.loads(CATALOG_PATH.read_text(encoding="utf-8"))


def normalize_path(path: Path) -> str:
    """统一为无前导斜杠的 POSIX 相对路径。

    [参数] path：需要标准化的路径对象。
    [返回] str：无前导斜杠的 POSIX 相对路径。
    最近修改时间: 2026-07-28 22:40:00 明确检查与哈希共享的路径格式。
    """
    return path.as_posix().strip("/")


def is_under(path: str, parent: str) -> bool:
    """判断路径是否为父目录自身或其子路径。

    [参数] path：待判断相对路径；parent：候选父路径。
    [返回] bool：路径位于父路径或等于父路径时为真。
    最近修改时间: 2026-07-28 22:40:00 明确禁止路径与内容边界的共同判断。
    """
    return path == parent or path.startswith(parent + "/")


def query_entries(catalog: dict[str, Any], args: argparse.Namespace) -> list[dict[str, Any]]:
    """根据已提供的筛选字段查询唯一目录条目。

    [参数] catalog 为位置 Catalog，args 为解析后的查询参数。
    [返回] 符合全部已提供筛选条件的条目列表。
    最近修改时间: 2026-07-28 21:26:06 扩展 source-util 的语言筛选条件。
    """
    # 1. 仅将调用方明确提供的维度参与 Catalog 匹配。
    mappings = {
        "project_kind": args.project_kind,
        "artifact_kind": args.artifact,
        "category": args.category,
        "technology": args.technology,
        "operation": args.operation,
        "language": args.language,
    }
    return [
        entry for entry in catalog["entries"]
        if all(value is None or entry.get(field) == value for field, value in mappings.items())
    ]


def command_query(catalog: dict[str, Any], args: argparse.Namespace) -> int:
    """输出唯一 Catalog 条目；多结果或无结果均失败关闭。

    [参数] catalog 为位置 Catalog，args 为解析后的查询参数。
    [返回] 成功返回 0，查询条件不唯一返回 2。
    最近修改时间: 2026-07-28 21:26:06 要求 source-util 查询显式指定语言。
    """
    # 1. source-util 的四种语言位置不同，缺少语言时不能返回不确定结果。
    if args.artifact == "source-util" and args.language is None:
        print(json.dumps({"ok": False, "errors": ["source-util 查询必须指定 --language"]}, ensure_ascii=False))
        return 2
    entries = query_entries(catalog, args)
    if len(entries) != 1:
        print(json.dumps({"ok": False, "matches": len(entries), "entries": entries}, ensure_ascii=False, indent=2))
        return 2
    print(json.dumps({"ok": True, "entry": entries[0]}, ensure_ascii=False, indent=2))
    return 0


def tree_lines(kind: str) -> list[str]:
    """从与 Catalog 绑定的完整目录文档提取单个项目树，禁止脚本维护简写树。

    [参数] kind：项目类型。
    [返回] list[str]：完整注释目录树的逐行文本。
    最近修改时间: 2026-07-28 22:40:00 删除重复旧树，确保 render 只读取唯一事实源。
    """
    # 1. 根据项目类型定位完整目录文档中的唯一章节。
    headings = {
        "fullstack": "## 前后端在同一个项目",
        "backend": "## 后端独立项目",
        "frontend": "## 前端独立项目",
    }
    content = LAYOUT_PATH.read_text(encoding="utf-8")
    section = content.split(headings[kind], 1)[1]
    start = section.index("```text") + len("```text")
    end = section.index("```", start)
    return [line for line in section[start:end].strip().splitlines() if line]


def command_render(catalog: dict[str, Any], args: argparse.Namespace) -> int:
    """渲染一个或全部项目类型的带用途目录树。

    [参数] catalog：位置 Catalog；args：渲染命令参数。
    [返回] int：渲染完成时返回 0。
    最近修改时间: 2026-07-28 22:40:00 移除旧树实现，保证仅使用完整目录文档。
    """
    # 1. `--all` 依序读取各项目类型的唯一完整树。
    kinds = catalog["project_kinds"] if args.all else [args.project_kind]
    for index, kind in enumerate(kinds):
        if index:
            print()
        print("\n".join(tree_lines(kind)))
    return 0


def normalized_base_package(base_package: str | None) -> str | None:
    """把 Java 包名转换为稳定的源码相对路径。

    [参数] base_package：点号或斜杠分隔的 Java 基础包名。
    [返回] str | None：合法时返回斜杠分隔路径，否则返回 None。
    最近修改时间: 2026-07-28 23:55:00 为业务域 RPC 初始化解析 Java 源码根。
    """
    if base_package is None:
        return None
    # 1. 仅接受包名片段，避免 init 将占位符或路径穿越写入项目目录。
    parts = [part for part in re.split(r"[./]", base_package) if part]
    if not parts or any(re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", part) is None for part in parts):
        return None
    return "/".join(parts)


def source_root_for_init(language: str | None, base_package: str | None) -> str | None:
    """返回 init 可实际创建的语言源码根目录。

    [参数] language：后端语言；base_package：Java 基础包名。
    [返回] str | None：可解析的源码根，缺失必需上下文时返回 None。
    最近修改时间: 2026-07-28 23:55:00 为业务域 RPC 初始化补齐四语言物理路径。
    """
    if language == "java":
        normalized = normalized_base_package(base_package)
        return None if normalized is None else f"src/main/java/{normalized}"
    return SOURCE_ROOTS.get(language)


def valid_domain(domain: str | None) -> bool:
    """校验业务域目录名不包含路径穿越或字面量占位符。

    [参数] domain：调用方传入的业务域名称。
    [返回] bool：名称可安全用于单个目录片段时返回真。
    最近修改时间: 2026-07-28 23:55:00 新增业务域 RPC 初始化的目录名保护。
    """
    return domain is not None and re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_-]*", domain) is not None


def expand_init_path(canonical_path: str, args: argparse.Namespace) -> str | None:
    """将带源码根和业务域占位符的 Catalog 路径解析为真实目录。

    [参数] canonical_path：Catalog 规范路径；args：init 参数。
    [返回] str | None：完整上下文下的可创建路径，否则返回 None。
    最近修改时间: 2026-07-28 23:55:00 支持业务域 RPC 的显式初始化。
    """
    expanded = canonical_path
    if "<source-root>" in expanded:
        source_root = source_root_for_init(args.language, args.base_package)
        if source_root is None:
            return None
        expanded = expanded.replace("<source-root>", source_root)
    if "<domain>" in expanded:
        if not valid_domain(args.domain):
            return None
        expanded = expanded.replace("<domain>", args.domain)
    return expanded


def command_init(catalog: dict[str, Any], args: argparse.Namespace) -> int:
    """创建必需骨架与明确启用条目，绝不批量创建所有条件目录。

    [参数] catalog 为位置 Catalog，args 为初始化参数。
    [返回] 成功返回 0，未知启用 ID 返回 2。
    最近修改时间: 2026-07-28 21:26:06 拒绝旧 util 启用 ID，避免静默兼容。
    """
    target = Path(args.root).resolve()
    enabled = set(filter(None, (args.enable or "").split(",")))
    # 1. 旧 util ID 必须显式失败，不能悄悄退化为只创建骨架。
    known_ids = {entry["id"] for entry in catalog["entries"] if entry["project_kind"] == args.project_kind}
    unknown_ids = sorted(enabled - known_ids)
    if unknown_ids:
        print(json.dumps({"ok": False, "errors": [f"未知启用 ID: {item}" for item in unknown_ids]}, ensure_ascii=False))
        return 2
    paths = list(catalog["skeletons"][args.project_kind])
    argument_errors: list[str] = []
    for entry in catalog["entries"]:
        if entry["project_kind"] == args.project_kind and entry["id"] in enabled:
            expanded = expand_init_path(entry["canonical_path"], args)
            if expanded is None:
                if entry.get("requires_domain"):
                    argument_errors.append("backend.business-rpc 初始化必须提供合法的 --domain、--language；Java 另需 --base-package")
                else:
                    argument_errors.append(f"无法解析启用目录: {entry['id']}")
                continue
            paths.append(expanded)
    if argument_errors:
        print(json.dumps({"ok": False, "errors": sorted(set(argument_errors))}, ensure_ascii=False, indent=2))
        return 2
    for relative in sorted(set(paths)):
        (target / relative).mkdir(parents=True, exist_ok=True)
    print(json.dumps({"ok": True, "created": sorted(set(paths))}, ensure_ascii=False, indent=2))
    return 0


def source_util_root(relative: str, language: str) -> str | None:
    """识别指定语言的源码根 util 目录。

    [参数] relative 为项目相对路径，language 为后端语言。
    [返回] 命中时返回源码根 util 路径，未命中返回 None。
    最近修改时间: 2026-07-28 21:26:06 新增四种语言的源码根 util 识别。
    """
    parts = relative.split("/")
    # 1. Go、Node.js 与 Python 有固定源码根路径。
    if language == "go" and parts[:2] == ["internal", "util"]:
        return "internal/util"
    if language == "node" and parts[:2] == ["src", "util"]:
        return "src/util"
    if language == "python" and len(parts) >= 3 and parts[0] == "src" and parts[2] == "util":
        return "/".join(parts[:3])
    # 2. Java 基础包允许多段路径，但业务域 util 不属于源码根 util。
    if language == "java" and parts[:3] == ["src", "main", "java"]:
        for index, part in enumerate(parts[3:], start=3):
            if part == "util" and not any(segment in {"router", "controller", "business"} for segment in parts[3:index]):
                return "/".join(parts[:index + 1])
    return None


def check_source_util_path(relative: str, is_file: bool, language: str) -> list[str]:
    """校验源码根 util 只能直接存放指定语言代码文件。

    [参数] relative 为项目相对路径，is_file 表示文件，language 为后端语言。
    [返回] 当前路径的源码根 util 严格策略错误列表。
    最近修改时间: 2026-07-28 21:26:06 新增源码根 util 的文件与子目录边界。
    """
    # 1. 先定位源码根 util；未命中或目录本身不产生错误。
    root = source_util_root(relative, language)
    if root is None or relative == root:
        return []
    child = relative[len(root) + 1:]
    # 2. 子目录与非指定语言文件均违反源码根 util 的扁平边界。
    if "/" in child or not is_file:
        return [f"源码根 util 禁止子目录: {relative}"]
    if Path(relative).suffix.lower() not in SOURCE_UTIL_EXTENSIONS[language]:
        return [f"源码根 util 仅允许 {language} 代码文件: {relative}"]
    return []


def business_rpc_root(relative: str, language: str) -> str | None:
    """识别当前语言源码根下某个业务域的 rpc 目录。

    [参数] relative：项目相对路径；language：后端语言。
    [返回] str | None：命中时返回业务域 rpc 根，未命中时返回 None。
    最近修改时间: 2026-07-28 23:55:00 新增跨微业务 RPC 目录识别。
    """
    parts = relative.split("/")
    # 1. 先按固定源码根识别 Go、Node.js 与 Python 的业务域 rpc。
    if language == "go" and len(parts) >= 4 and parts[:2] == ["internal", "business"] and parts[3] == "rpc":
        return "/".join(parts[:4])
    if language == "node" and len(parts) >= 4 and parts[:2] == ["src", "business"] and parts[3] == "rpc":
        return "/".join(parts[:4])
    if language == "python" and len(parts) >= 5 and parts[0] == "src" and parts[2] == "business" and parts[4] == "rpc":
        return "/".join(parts[:5])
    # 2. Java 的基础包深度不固定，定位 `business/<domain>/rpc` 作为源码根后的尾部结构。
    if language == "java" and parts[:3] == ["src", "main", "java"]:
        for index, part in enumerate(parts[3:], start=3):
            if part == "business" and len(parts) > index + 2 and parts[index + 2] == "rpc":
                return "/".join(parts[:index + 3])
    return None


def check_business_rpc_path(relative: str, is_file: bool, language: str) -> list[str]:
    """校验业务域 rpc 只直接存放当前语言的公开函数文件。

    [参数] relative：项目相对路径；is_file：当前路径是否为文件；language：后端语言。
    [返回] list[str]：不符合扁平 JSON RPC 入口规则的错误列表。
    最近修改时间: 2026-07-28 23:55:00 新增业务域 RPC 的扁平文件边界。
    """
    root = business_rpc_root(relative, language)
    if root is None or relative == root:
        return []
    child = relative[len(root) + 1:]
    # 1. RPC 目录是公开函数入口，禁止继续按技术或操作创建子目录。
    if "/" in child or not is_file:
        return [f"业务域 rpc 禁止子目录: {relative}"]
    if Path(relative).suffix.lower() not in SOURCE_UTIL_EXTENSIONS[language]:
        return [f"业务域 rpc 仅允许 {language} 代码文件: {relative}"]
    return []


def check_path(
    catalog: dict[str, Any], relative: str, is_file: bool, project_kind: str | None, language: str | None,
) -> list[str]:
    """针对单一路径返回全部严格策略错误。

    [参数] catalog 为位置 Catalog，relative 为项目相对路径，is_file 表示文件，project_kind 与 language 为检查上下文。
    [返回] 当前路径的严格策略错误列表。
    最近修改时间: 2026-07-28 21:26:06 加入 utils 根文件与源码根 util 校验。
    """
    errors: list[str] = []
    # 1. 先应用 Catalog 的通用禁止路径和子目录边界。
    for forbidden in catalog["forbidden_paths"]:
        if is_under(relative, forbidden):
            errors.append(f"禁止路径: {relative}")
            break
    for parent, children in catalog["allowed_children"].items():
        if relative.startswith(parent + "/"):
            first_child = relative[len(parent) + 1:].split("/", 1)[0]
            if first_child not in children:
                errors.append(f"非法子目录: {relative} 不属于 {parent}")
    suffix = Path(relative).suffix.lower()
    if is_file and is_under(relative, "database/migration") and suffix == ".sql":
        errors.append(f"自动迁移目录禁止 SQL 文件: {relative}")
    if is_file and is_under(relative, "database/sql") and suffix in SOURCE_EXTENSIONS:
        errors.append(f"独立 SQL 目录禁止生产源码: {relative}")
    # 2. 后端根 utils 只承载工具包子目录，源码根 util 则按语言限制直接文件。
    if project_kind == "backend" and is_file and Path(relative).parent.as_posix() == "utils":
        errors.append(f"根 utils 禁止直接文件: {relative}")
    if project_kind == "backend" and language is not None:
        errors.extend(check_source_util_path(relative, is_file, language))
        errors.extend(check_business_rpc_path(relative, is_file, language))
    return errors


def manifest_relative_path(value: Any, label: str, errors: list[str]) -> str | None:
    """校验收敛清单中使用的项目根相对 POSIX 路径。

    [参数] value：待校验字段；label：字段在错误信息中的定位名称；errors：收集稳定错误的列表。
    [返回] str | None：合法路径或 None。
    最近修改时间: 2026-07-29 00:25:50 新增 adoption 清单的路径越界保护。
    """
    # 1. 拒绝绝对路径、Windows 盘符、反斜杠、空段和父级穿越，避免清单越出项目根。
    if not isinstance(value, str) or not value or value != value.strip() or "\\" in value:
        errors.append(f"收敛清单路径非法: {label}")
        return None
    if value.startswith("/") or re.match(r"^[A-Za-z]:", value) or any(part in {"", ".", ".."} for part in value.split("/")):
        errors.append(f"收敛清单路径非法: {label}")
        return None
    return value


def load_adoption_manifest(
    catalog: dict[str, Any], root: Path, args: argparse.Namespace,
) -> tuple[dict[str, Any] | None, list[str]]:
    """读取并验证旧项目收敛清单，不为缺失事实补写任何内容。

    [参数] catalog：目录规则事实源；root：待检查项目根；args：check 命令参数。
    [返回] tuple[dict[str, Any] | None, list[str]]：有效快照与全部参数或清单错误。
    最近修改时间: 2026-07-29 01:12:27 支持普通 YAML 收敛清单并保留 JSON 降级。
    """
    errors: list[str] = []
    if args.adoption_manifest is None:
        return None, ["adoption 策略必须指定 --adoption-manifest"]

    # 1. 清单必须位于当前项目且使用固定位置，不能借绝对路径读取其它项目的清单。
    requested = Path(args.adoption_manifest)
    manifest_file = (root / requested).resolve() if not requested.is_absolute() else requested.resolve()
    try:
        manifest_relative = normalize_path(manifest_file.relative_to(root))
    except ValueError:
        return None, ["收敛清单必须位于项目根目录内"]
    if manifest_relative != ADOPTION_MANIFEST_PATH:
        return None, [f"收敛清单固定路径必须为: {ADOPTION_MANIFEST_PATH}"]
    if not manifest_file.is_file():
        return None, [f"收敛清单不存在: {manifest_relative}"]

    # 2. 优先读取普通 YAML；缺少 PyYAML 时仅保留 JSON 兼容 YAML 的降级能力。
    try:
        text = manifest_file.read_text(encoding="utf-8")
        manifest = yaml.safe_load(text) if yaml is not None else json.loads(text)
    except (OSError, UnicodeDecodeError, json.JSONDecodeError, yaml.YAMLError if yaml is not None else ValueError) as exc:
        return None, [f"收敛清单必须是 UTF-8 YAML: {exc}"]
    if not isinstance(manifest, dict):
        return None, ["收敛清单根节点必须是对象"]

    allowed_fields = {"version", "project_kind", "language", "adopted_paths", "legacy_source_roots"}
    unknown_fields = sorted(set(manifest) - allowed_fields)
    required_fields = {"version", "project_kind", "adopted_paths", "legacy_source_roots"}
    missing_fields = sorted(required_fields - set(manifest))
    if unknown_fields:
        errors.append(f"收敛清单存在未知字段: {', '.join(unknown_fields)}")
    if missing_fields:
        errors.append(f"收敛清单缺少字段: {', '.join(missing_fields)}")
    if manifest.get("version") != 1:
        errors.append("收敛清单 version 必须为 1")
    if manifest.get("project_kind") != args.project_kind:
        errors.append("收敛清单 project_kind 与 --project-kind 不一致")
    if args.project_kind == "backend" and manifest.get("language") != args.language:
        errors.append("收敛清单 language 与 --language 不一致")

    adopted_paths = manifest.get("adopted_paths")
    legacy_roots = manifest.get("legacy_source_roots")
    if not isinstance(adopted_paths, list):
        errors.append("收敛清单 adopted_paths 必须是数组")
        adopted_paths = []
    if not isinstance(legacy_roots, list):
        errors.append("收敛清单 legacy_source_roots 必须是数组")
        legacy_roots = []

    # 3. 已采纳路径只能精确匹配无占位符的唯一 Catalog 条目，且必须已真实存在。
    adopted: set[str] = set()
    for index, item in enumerate(adopted_paths):
        label = f"adopted_paths[{index}]"
        if not isinstance(item, dict) or set(item) != {"path", "catalog_id", "responsibility"}:
            errors.append(f"收敛清单字段非法: {label}")
            continue
        path = manifest_relative_path(item["path"], f"{label}.path", errors)
        catalog_id = item["catalog_id"]
        responsibility = item["responsibility"]
        if path is None:
            continue
        if path in adopted:
            errors.append(f"收敛清单 adopted_paths 重复路径: {path}")
            continue
        if not isinstance(catalog_id, str) or not catalog_id or not isinstance(responsibility, str) or not responsibility.strip():
            errors.append(f"收敛清单字段非法: {label}")
            continue
        if any(is_under(path, forbidden) for forbidden in catalog["forbidden_paths"]):
            errors.append(f"已采纳路径命中禁止目录: {path}")
            continue
        matches = [entry for entry in catalog["entries"] if entry["id"] == catalog_id and entry["project_kind"] == args.project_kind]
        if len(matches) != 1 or "<" in matches[0]["canonical_path"] or matches[0]["canonical_path"] != path:
            errors.append(f"已采纳路径未唯一匹配 Catalog: {path}")
            continue
        if not (root / path).is_dir():
            errors.append(f"已采纳目录不存在或不是目录: {path}")
            continue
        adopted.add(path)

    # 4. 遗留根必须记录当时存在的目录和源码文件；目录或文件缺失时拒绝伪造快照。
    legacy: dict[str, dict[str, set[str]]] = {}
    source_extensions = SOURCE_UTIL_EXTENSIONS.get(args.language, SOURCE_EXTENSIONS)
    for index, item in enumerate(legacy_roots):
        label = f"legacy_source_roots[{index}]"
        required = {"path", "responsibility", "existing_directories", "existing_files"}
        if not isinstance(item, dict) or set(item) != required:
            errors.append(f"收敛清单字段非法: {label}")
            continue
        path = manifest_relative_path(item["path"], f"{label}.path", errors)
        directories = item["existing_directories"]
        files = item["existing_files"]
        if path is None:
            continue
        if path in legacy:
            errors.append(f"收敛清单 legacy_source_roots 重复路径: {path}")
            continue
        # 4.1. 一份历史文件只能归属一个遗留根；拒绝父子根避免快照覆盖关系不确定。
        if any(is_under(path, legacy_path) or is_under(legacy_path, path) for legacy_path in legacy):
            errors.append(f"收敛清单 legacy_source_roots 不能嵌套或重叠: {path}")
            continue
        if not isinstance(item["responsibility"], str) or not item["responsibility"].strip() or not isinstance(directories, list) or not isinstance(files, list):
            errors.append(f"收敛清单字段非法: {label}")
            continue
        declared_directories: set[str] = set()
        declared_files: set[str] = set()
        for directory in directories:
            declared = manifest_relative_path(directory, f"{label}.existing_directories", errors)
            if declared is not None and (not is_under(declared, path) or declared in declared_directories):
                errors.append(f"遗留目录必须位于根且不可重复: {label}")
            elif declared is not None:
                declared_directories.add(declared)
        for file_path in files:
            declared = manifest_relative_path(file_path, f"{label}.existing_files", errors)
            if declared is not None and (not is_under(declared, path) or declared in declared_files):
                errors.append(f"遗留文件必须位于根且不可重复: {label}")
            elif declared is not None:
                declared_files.add(declared)
        if path not in declared_directories:
            errors.append(f"遗留根必须登记在 existing_directories: {path}")
        if not (root / path).is_dir():
            errors.append(f"遗留源码根不存在或不是目录: {path}")
        for directory in declared_directories:
            if not (root / directory).is_dir():
                errors.append(f"遗留快照目录不存在: {directory}")
        for file_path in declared_files:
            if Path(file_path).suffix.lower() not in source_extensions or not (root / file_path).is_file():
                errors.append(f"遗留快照源码文件不存在或类型非法: {file_path}")
        legacy[path] = {"directories": declared_directories, "files": declared_files}

    # 5. 已采纳目录和遗留根不能交叠，避免用清单绕过 V2 路径的新增检查。
    for adopted_path in adopted:
        for legacy_path in legacy:
            if is_under(adopted_path, legacy_path) or is_under(legacy_path, adopted_path):
                errors.append(f"已采纳路径与遗留根不能重叠: {adopted_path} / {legacy_path}")
    return ({"adopted": adopted, "legacy": legacy, "source_extensions": source_extensions} if not errors else None), errors


def adoption_legacy_root(relative: str, legacy: dict[str, dict[str, set[str]]]) -> str | None:
    """返回包含当前路径的最深遗留源码根。

    [参数] relative：项目相对路径；legacy：已验证的遗留快照映射。
    [返回] str | None：命中的遗留根或 None。
    最近修改时间: 2026-07-29 00:25:50 为 adoption 扫描隔离历史存量。
    """
    matches = [root for root in legacy if is_under(relative, root)]
    return max(matches, key=len) if matches else None


def check_adoption_path(
    catalog: dict[str, Any], state: dict[str, Any], relative: str, path: Path, project_kind: str | None, language: str | None,
) -> list[str]:
    """检查 adoption 下的单一路径，遗留快照外的内容仍按 V2 严格规则处理。

    [参数] catalog：目录事实源；state：已验证收敛清单；relative：项目相对路径；path：实际文件系统路径；project_kind 与 language：检查上下文。
    [返回] list[str]：当前路径的全部违规原因。
    最近修改时间: 2026-07-29 00:25:50 新增旧项目渐进采纳的只读路径分流。
    """
    legacy_root = adoption_legacy_root(relative, state["legacy"])
    if legacy_root is not None:
        # 1. 遗留路径只允许快照时已有目录和源码文件；不再套用新树禁止目录。
        snapshot = state["legacy"][legacy_root]
        if path.is_dir() and relative not in snapshot["directories"]:
            return [f"遗留源码目录不在快照: {relative}"]
        if path.is_file() and Path(relative).suffix.lower() in state["source_extensions"] and relative not in snapshot["files"]:
            return [f"遗留源码文件不在快照: {relative}"]
        return []

    # 2. 已采纳和新建路径严格检查；顶层不在 V2 树的源码必须先人工登记为遗留根。
    errors = check_path(catalog, relative, path.is_file(), project_kind, language)
    if path.is_file() and Path(relative).suffix.lower() in state["source_extensions"]:
        if relative.split("/", 1)[0] not in ADOPTION_V2_SOURCE_ROOTS[project_kind]:
            errors.append(f"未登记的遗留源码路径: {relative}")
    return errors


def command_check(catalog: dict[str, Any], args: argparse.Namespace) -> int:
    """只读扫描项目目录并输出严格错误或兼容告警。

    [参数] catalog 为位置 Catalog，args 为检查参数。
    [返回] strict 违规或参数缺失返回 2，其余返回 0。
    最近修改时间: 2026-07-29 00:25:50 新增 adoption 收敛清单与遗留快照的只读检查。
    """
    root = Path(args.root).resolve()
    if not root.is_dir():
        print(json.dumps({"ok": False, "errors": [f"目录不存在: {root}"]}, ensure_ascii=False))
        return 2
    # 1. strict 与 adoption 必须显式声明项目类型，后端还必须声明源码语言。
    argument_errors: list[str] = []
    if args.policy in {"strict", "adoption"} and args.project_kind is None:
        argument_errors.append(f"{args.policy} 策略必须指定 --project-kind")
    if args.policy in {"strict", "adoption"} and args.project_kind == "backend" and args.language is None:
        argument_errors.append(f"backend {args.policy} 必须指定 --language")
    if argument_errors:
        print(json.dumps({"ok": False, "policy": args.policy, "errors": argument_errors}, ensure_ascii=False, indent=2))
        return 2

    # 2. adoption 先验证人工清单；任何格式或基线冲突都失败关闭，避免自动扩大遗留范围。
    adoption_state: dict[str, Any] | None = None
    if args.policy == "adoption":
        adoption_state, manifest_errors = load_adoption_manifest(catalog, root, args)
        if manifest_errors:
            print(json.dumps({"ok": False, "policy": args.policy, "errors": manifest_errors, "warnings": []}, ensure_ascii=False, indent=2))
            return 2
    errors: list[str] = []
    # 3. 扫描始终只读；legacy 降级为 warnings，adoption 仅对清单快照保留历史兼容。
    for path in sorted(root.rglob("*")):
        relative = normalize_path(path.relative_to(root))
        if adoption_state is not None:
            errors.extend(check_adoption_path(catalog, adoption_state, relative, path, args.project_kind, args.language))
        else:
            errors.extend(check_path(catalog, relative, path.is_file(), args.project_kind, args.language))
    payload = {
        "ok": not errors or args.policy == "legacy",
        "policy": args.policy,
        "errors": [] if args.policy == "legacy" else errors,
        "warnings": errors if args.policy == "legacy" else [],
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0 if payload["ok"] else 2


def command_hash(args: argparse.Namespace) -> int:
    """为测试证明 check 无写入提供目录内容摘要。

    [参数] args：包含待计算根目录的命令参数。
    [返回] int：摘要输出完成时返回 0。
    最近修改时间: 2026-07-28 22:40:00 明确哈希只用于验证检查的只读性质。
    """
    # 1. 按稳定路径顺序累积目录名和文件内容，避免遍历顺序影响断言。
    root = Path(args.root).resolve()
    digest = hashlib.sha256()
    for path in sorted(root.rglob("*")):
        digest.update(normalize_path(path.relative_to(root)).encode("utf-8"))
        if path.is_file():
            digest.update(path.read_bytes())
    print(json.dumps({"sha256": digest.hexdigest()}, ensure_ascii=False))
    return 0


def build_parser() -> argparse.ArgumentParser:
    """构建公开命令行参数。

    [参数] 无。
    [返回] 配置完成的命令行参数解析器。
    最近修改时间: 2026-07-29 00:25:50 为 check 增加 adoption 清单参数与策略枚举。
    """
    # 1. 统一声明子命令参数，避免各入口拥有不同的语言枚举。
    parser = argparse.ArgumentParser(description="代码位置目录 Catalog")
    subparsers = parser.add_subparsers(dest="command", required=True)
    query = subparsers.add_parser("query")
    query.add_argument("--project-kind", choices=["fullstack", "backend", "frontend"], default="backend")
    query.add_argument("--artifact", required=True)
    query.add_argument("--category")
    query.add_argument("--technology")
    query.add_argument("--operation")
    query.add_argument("--language", choices=["go", "java", "node", "python"])
    render = subparsers.add_parser("render")
    render.add_argument("--project-kind", choices=["fullstack", "backend", "frontend"], default="backend")
    render.add_argument("--all", action="store_true")
    init = subparsers.add_parser("init")
    init.add_argument("--project-kind", choices=["fullstack", "backend", "frontend"], required=True)
    init.add_argument("--root", required=True)
    init.add_argument("--enable")
    init.add_argument("--domain")
    init.add_argument("--language", choices=["go", "java", "node", "python"])
    init.add_argument("--base-package")
    check = subparsers.add_parser("check")
    check.add_argument("--root", required=True)
    check.add_argument("--policy", choices=["strict", "legacy", "adoption"], default="strict")
    check.add_argument("--project-kind", choices=["fullstack", "backend", "frontend"])
    check.add_argument("--language", choices=["go", "java", "node", "python"])
    check.add_argument("--adoption-manifest")
    digest = subparsers.add_parser("hash")
    digest.add_argument("--root", required=True)
    return parser


def main() -> int:
    """执行 CLI 并保持异常输出稳定。

    [参数] 无。
    [返回] int：子命令的稳定退出码。
    最近修改时间: 2026-07-28 22:40:00 保持所有公开命令由同一 Catalog 入口分发。
    """
    # 1. 解析命令并加载唯一 Catalog，再按子命令分发。
    parser = build_parser()
    args = parser.parse_args()
    catalog = load_catalog()
    if args.command == "query":
        return command_query(catalog, args)
    if args.command == "render":
        return command_render(catalog, args)
    if args.command == "init":
        return command_init(catalog, args)
    if args.command == "check":
        return command_check(catalog, args)
    return command_hash(args)


if __name__ == "__main__":
    raise SystemExit(main())
