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
COMMON_UTIL_EXTENSIONS = {
    "go": {".go"},
    "java": {".java"},
    "node": {".ts", ".js"},
    "python": {".py"},
}
ENTRYPOINT_EXTENSIONS = {
    "go": {".go"},
    "java": {".java"},
    "node": {".ts", ".js"},
    "python": {".py"},
}
ALL_ENTRYPOINT_EXTENSIONS = set().union(*ENTRYPOINT_EXTENSIONS.values())
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
    最近修改时间: 2026-08-04 12:00:00 增加 source-util 到 common-util 的兼容查询路由。
    """
    # 1. 仅为 database 的公开连字符名称补充内部下划线候选，保持其它 artifact 的既有名称不变。
    artifact_kinds = {args.artifact} if args.artifact is not None else set()
    if args.artifact is not None and args.artifact.startswith("database-"):
        artifact_kinds.add(args.artifact.replace("-", "_"))

    # 2. 仅将调用方明确提供的维度参与 Catalog 匹配。
    mappings = {
        "project_kind": args.project_kind,
        "category": args.category,
        "technology": args.technology,
        "operation": args.operation,
        "language": args.language,
    }
    # 3. source-util 是历史查询别名，统一路由到 backend.common.util；旧语言参数只保留兼容，不参与匹配。
    if args.artifact == "source-util":
        artifact_kinds = {"common-util"}
        mappings["language"] = None
    entries = [
        entry for entry in catalog["entries"]
        if (not artifact_kinds or entry.get("artifact_kind") in artifact_kinds)
        and all(value is None or entry.get(field) == value for field, value in mappings.items())
    ]
    # 4. database-migration 根目录承载通用迁移入口；未指定分类和操作时优先返回根条目，避免与 field/index 子条目产生多结果。
    if args.artifact in {"database-migration", "database_migration"} and args.category is None and args.operation is None:
        root_entries = [entry for entry in entries if entry.get("canonical_path") == "database/migration"]
        if root_entries:
            return root_entries
    return entries


def command_query(catalog: dict[str, Any], args: argparse.Namespace) -> int:
    """输出唯一 Catalog 条目；多结果或无结果均失败关闭。

    [参数] catalog 为位置 Catalog，args 为解析后的查询参数。
    [返回] 成功返回 0，查询条件不唯一返回 2。
    最近修改时间: 2026-08-04 12:00:00 将 source-util 保留为 common-util 的兼容查询别名。
    """
    # 1. 通过兼容别名或 canonical artifact 查询唯一条目。
    entries = query_entries(catalog, args)
    if len(entries) != 1:
        print(json.dumps({"ok": False, "matches": len(entries), "entries": entries}, ensure_ascii=False, indent=2))
        return 2
    print(json.dumps({"ok": True, "entry": entries[0]}, ensure_ascii=False, indent=2))
    return 0



def command_guide(catalog: dict[str, Any], args: argparse.Namespace) -> int:
    """按分类或技术查询目录用法，返回关联 skill、recipe 和包别名。

    [参数] catalog 为位置 Catalog，args 为解析后的查询参数。
    [返回] 成功返回 0，无匹配返回 2。
    """
    category_aliases = {
        "time": "time",
        "convert": "conversion",
        "conversion": "conversion",
        "cache": "cache",
        "mq": "mq",
        "message": "mq",
        "search": "search",
        "storage": "storage",
        "rpc": "rpc",
        "api": "api",
        "auth": "auth",
        "secret": "secret",
        "notification": "notification",
        "payment": "payment",
        "discovery": "discovery",
        "ip": "ip",
        "json": "serialization",
        "serialization": "serialization",
        "log": "logging",
        "logging": "logging",
        "cron": "scheduler",
        "scheduler": "scheduler",
        "async": "async",
        "http": "http",
        "protobuf": "protobuf",
        "all": "all",
    }
    category_value = category_aliases.get(args.category, args.category) if args.category else "all"
    entries = catalog["entries"]
    result = []
    project_kinds = ("backend",)
    for entry in entries:
        if entry["project_kind"] not in project_kinds:
            continue
        if args.language and entry.get("language") and entry["language"] != args.language:
            continue
        if category_value and category_value != "all":
            cat = entry.get("category", "")
            if cat != category_value:
                continue
        if args.technology:
            if entry.get("technology") != args.technology:
                continue
        if "canonical_path" not in entry:
            continue
        result.append({
            "project_kind": entry["project_kind"],
            "category": entry.get("category", ""),
            "canonical_path": entry["canonical_path"],
            "purpose": entry.get("purpose", ""),
            "owner_skill": entry.get("owner_skill", ""),
            "related_skills": entry.get("related_skills", []),
            "usage_recipes": entry.get("usage_recipes", []),
            "package_alias": entry.get("package_alias", ""),
            "example_scope": entry.get("example_scope", ""),
        })
    if not result:
        print(json.dumps({"ok": False, "usage": [], "message": "未找到匹配的目录用法"}, ensure_ascii=False))
        return 2
    result.sort(key=lambda x: x["canonical_path"])
    print(json.dumps({"ok": True, "usage": result}, ensure_ascii=False, indent=2))
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
    最近修改时间: 2026-07-28 23:55:00 为业务域版本目录 init 解析 Java 源码根。
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
    最近修改时间: 2026-07-28 23:55:00 为业务域版本目录 init 补齐四语言物理路径。
    """
    if language == "java":
        normalized = normalized_base_package(base_package)
        return None if normalized is None else f"src/main/java/{normalized}"
    return SOURCE_ROOTS.get(language)


def valid_domain(domain: str | None) -> bool:
    """校验业务域目录名不包含路径穿越或字面量占位符。

    [参数] domain：调用方传入的业务域名称。
    [返回] bool：名称可安全用于单个目录片段时返回真。
    最近修改时间: 2026-07-28 23:55:00 新增业务域版本目录 init 的目录名保护。
    """
    return domain is not None and re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_-]*", domain) is not None


def expand_init_path(canonical_path: str, args: argparse.Namespace) -> str | None:
    """将带源码根、业务域和版本占位符的 Catalog 路径解析为真实目录。

    [参数] canonical_path：Catalog 规范路径；args：init 参数。
    [返回] str | None：完整上下文下的可创建路径，否则返回 None。
    最近修改时间: 2026-08-18 14:41:00 版本目录占位符默认解析为 v1，router/controller 下沉到版本目录。
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
    # 1. 版本目录占位符默认创建首个版本 v1，新增版本由 micro-business 的 scaffold 递增。
    if "<v?>" in expanded:
        expanded = expanded.replace("<v?>", "v1")
    return expanded


def command_init(catalog: dict[str, Any], args: argparse.Namespace) -> int:
    """创建必需骨架、根治理文件与明确启用条目，绝不批量创建所有条件目录。

    [参数] catalog 为位置 Catalog，args 为初始化参数。
    [返回] 成功返回 0，未知启用 ID 返回 2。
    最近修改时间: 2026-07-29 23:00:00 增加三类项目根治理文件的位置初始化。
    """
    target = Path(args.root).resolve()
    enabled = set(filter(None, (args.enable or "").split(",")))
    # 1. 旧 util ID 必须显式失败，不能悄悄退化为只创建骨架。
    known_ids = {entry["id"] for entry in catalog["entries"] if entry["project_kind"] == args.project_kind}
    unknown_ids = sorted(enabled - known_ids)
    if unknown_ids:
        print(json.dumps({"ok": False, "errors": [f"未知启用 ID: {item}" for item in unknown_ids]}, ensure_ascii=False))
        return 2
    directories = list(catalog["skeletons"][args.project_kind])
    files: list[str] = []
    argument_errors: list[str] = []
    for entry in catalog["entries"]:
        if entry["project_kind"] != args.project_kind:
            continue
        is_required_file = entry.get("node_kind") == "file" and entry["creation_policy"] == "required"
        if entry["id"] in enabled or is_required_file:
            if entry.get("node_kind") == "pattern":
                # 动态入口需要人工提供语言和 binary 名称，禁止 init 误建字面量占位路径。
                argument_errors.append(f"{entry['id']} 是动态入口 pattern，init 不创建入口文件或占位路径")
                continue
            expanded = expand_init_path(entry["canonical_path"], args)
            if expanded is None:
                if entry.get("requires_domain"):
                    argument_errors.append(f"{entry['id']} 初始化必须提供合法的 --domain、--language；Java 另需 --base-package")
                else:
                    argument_errors.append(f"无法解析启用路径: {entry['id']}")
                continue
            if entry.get("node_kind") == "file":
                files.append(expanded)
            else:
                directories.append(expanded)
    if argument_errors:
        print(json.dumps({"ok": False, "errors": sorted(set(argument_errors))}, ensure_ascii=False, indent=2))
        return 2
    file_conflicts = [relative for relative in sorted(set(files)) if (target / relative).exists() and not (target / relative).is_file()]
    if file_conflicts:
        print(json.dumps({"ok": False, "errors": [f"必需根文件不能是目录: {item}" for item in file_conflicts]}, ensure_ascii=False, indent=2))
        return 2
    # 2. 先创建目录，再只 touch 目录规则拥有的文件位置；正文仍由各自 Owner 填充。
    for relative in sorted(set(directories)):
        (target / relative).mkdir(parents=True, exist_ok=True)
    for relative in sorted(set(files)):
        file_path = target / relative
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.touch(exist_ok=True)
    print(json.dumps({"ok": True, "created": sorted(set(directories) | set(files))}, ensure_ascii=False, indent=2))
    return 0


def deprecated_source_util_root(relative: str, language: str) -> str | None:
    """识别需要拒绝的新项目源码根 util 遗留路径。

    [参数] relative 为项目相对路径，language 为后端语言。
    [返回] 命中时返回源码根 util 路径，未命中返回 None。
    最近修改时间: 2026-08-04 12:00:00 将源码根 util 改为严格拒绝的旧位置识别。
    """
    parts = relative.split("/")
    # 1. Go、Node.js 与 Python 有固定源码根路径。
    if language == "go" and parts[:2] == ["internal", "util"]:
        return "internal/util"
    if language == "node" and parts[:2] == ["src", "util"]:
        return "src/util"
    if language == "python" and len(parts) >= 3 and parts[0] == "src" and parts[2] == "util":
        return "/".join(parts[:3])
    # 2. Java 源码根为 src/main/java/<base_package>；业务域直连源码根后，源码根 util 不再能借
    #    router/controller/business 关键词与业务域 util 区分。缺少 --base-package 时无法判定基础包
    #    深度，故仅保守识别 util 紧邻 src/main/java 之后的明确废弃位置，避免误伤业务域 util。
    if language == "java" and parts == ["src", "main", "java", "util"]:
        return "src/main/java/util"
    return None


def check_common_util_path(relative: str, is_file: bool, project_kind: str, language: str | None) -> list[str]:
    """校验 backend common/util 只能直接存放当前语言代码文件。

    [参数] relative 为项目相对路径，is_file 表示文件，project_kind 为项目类型，language 为后端语言。
    [返回] 当前路径的 common/util 严格策略错误列表。
    最近修改时间: 2026-08-04 12:00:00 新增 common/util 的项目类型、文件与子目录边界。
    """
    # 1. 先确认当前路径是否位于独立后端公共工具根。
    root = "common/util"
    if not is_under(relative, root) or relative == root:
        return []
    # 2. 非独立后端不得复用该根级目录。
    if project_kind != "backend":
        return [f"common/util 仅允许独立后端项目: {relative}"]
    if language is None:
        return []
    # 3. 独立后端只允许当前语言源码直接落盘。
    child = relative[len(root) + 1:]
    if "/" in child or not is_file:
        return [f"common/util 禁止子目录: {relative}"]
    if Path(relative).suffix.lower() not in COMMON_UTIL_EXTENSIONS[language]:
        return [f"common/util 仅允许 {language} 代码文件: {relative}"]
    return []


def check_deprecated_source_util_path(relative: str, is_file: bool, language: str) -> list[str]:
    """拒绝源码根 util 旧路径；adoption 快照由上层单独放行。

    [参数] relative 为项目相对路径，is_file 表示文件，language 为后端语言。
    [返回] 源码根 util 旧路径错误列表。
    最近修改时间: 2026-08-04 12:00:00 新增旧源码根严格拒绝并保留 adoption 放行边界。
    """
    # 1. 旧源码根仅在 strict 路径中报错，adoption 由上层先行短路。
    root = deprecated_source_util_root(relative, language)
    if root is None:
        return []
    return [f"源码根 util 已废弃，请迁移到 common/util: {relative}"]

def entrypoint_extensions(language: str | None) -> set[str]:
    """返回当前检查上下文允许的二进制入口扩展名。

    [参数] language：后端语言；fullstack 未指定语言时可为空。
    [返回] set[str]：允许的入口文件扩展名集合。
    最近修改时间: 2026-08-02 新增二进制入口 pattern 的语言扩展约束。
    """
    # 1. fullstack 未指定语言时保留全部受支持扩展，后端严格检查则使用单一语言集合。
    if language is None:
        return ALL_ENTRYPOINT_EXTENSIONS
    return ENTRYPOINT_EXTENSIONS[language]


def valid_binary_name(value: str) -> bool:
    """判断额外二进制目录名是否为单个安全路径片段。

    [参数] value：`cmd/` 下的 binary 目录名。
    [返回] bool：目录名非空且不含路径穿越时为真。
    最近修改时间: 2026-08-02 新增 cmd 二进制目录层级检查。
    """
    # 1. 只接受单个安全目录片段，避免 cmd 层级混入空名称或路径穿越。
    return re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_-]*", value) is not None


def is_entrypoint_filename(value: str, extensions: set[str]) -> bool:
    """判断文件名是否为当前语言允许的 `main.<ext>` 入口。

    [参数] value：文件名；extensions：当前检查上下文允许的扩展名。
    [返回] bool：文件名为 main 且扩展名符合语言约束时为真。
    最近修改时间: 2026-08-02 新增入口文件名匹配。
    """
    # 1. 文件名和扩展名必须同时满足，不能把任意 main 文件当作当前语言入口。
    path = Path(value)
    return path.stem == "main" and path.suffix.lower() in extensions


def check_binary_entrypoint_path(
    relative: str, is_file: bool, project_kind: str | None, language: str | None,
) -> list[str]:
    """校验独立后端和同仓后端的主/额外二进制入口路径。

    [参数] relative：项目根相对路径；is_file：当前路径是否为文件；project_kind：项目类型；language：后端语言。
    [返回] list[str]：不符合入口 pattern 的稳定错误列表。
    最近修改时间: 2026-08-02 新增根主入口与 cmd 额外入口的统一检查。
    """
    # 1. 前端没有本轮二进制入口契约，直接保持现有目录检查语义。
    if project_kind not in {"backend", "fullstack"}:
        return []
    parts = relative.split("/")
    extensions = entrypoint_extensions(language)
    valid = False

    # 2. 独立后端只识别根 main、cmd 及语言源码根中的入口候选，避免误伤普通业务目录的 main 文件。
    if project_kind == "backend":
        if len(parts) == 1 and is_file:
            if is_entrypoint_filename(parts[0], extensions):
                return []
            if Path(parts[0]).stem == "main" and Path(parts[0]).suffix.lower() in ALL_ENTRYPOINT_EXTENSIONS:
                return [f"二进制入口路径非法: {relative}"]
            return []
        elif parts[0] == "cmd":
            if len(parts) == 1 and not is_file:
                return []
            if len(parts) == 2 and not is_file and valid_binary_name(parts[1]):
                return []
            valid = len(parts) == 3 and is_file and valid_binary_name(parts[1]) and is_entrypoint_filename(parts[2], extensions)
        elif parts[0] in {"internal", "src"} and is_file and Path(parts[-1]).stem == "main" and Path(parts[-1]).suffix.lower() in ALL_ENTRYPOINT_EXTENSIONS:
            return [f"二进制入口路径非法: {relative}"]
        else:
            return []
    # 3. 同仓项目仅让 backend 子项目承载后端入口，工作区根和根 cmd 一律不作为后端入口。
    else:
        if len(parts) == 1 and not is_file and parts[0] == "backend":
            return []
        if len(parts) == 2 and is_file and parts[0] == "backend":
            if not is_entrypoint_filename(parts[1], extensions):
                return []
            valid = is_entrypoint_filename(parts[1], extensions)
        elif parts[:2] == ["backend", "cmd"]:
            if len(parts) == 2 and not is_file:
                return []
            if len(parts) == 3 and not is_file and valid_binary_name(parts[2]):
                return []
            valid = len(parts) == 4 and is_file and valid_binary_name(parts[2]) and is_entrypoint_filename(parts[3], extensions)
        elif parts[0] == "backend" and len(parts) >= 3 and parts[1] in {"internal", "src"} and is_file and is_entrypoint_filename(parts[-1], extensions):
            return [f"二进制入口路径非法: {relative}"]
        elif parts[0] == "cmd" or (parts[0] != "backend" and is_file and is_entrypoint_filename(parts[-1], extensions)):
            return [f"二进制入口路径非法: {relative}"]
        else:
            return []

    return [] if valid else [f"二进制入口路径非法: {relative}"]


def legal_main_entrypoint_relative(relative: str, project_kind: str, language: str) -> bool:
    """判断相对路径是否为当前项目类型合法的 Go 主入口。"""
    return Path(relative).name == "main.go" and not check_binary_entrypoint_path(relative, True, project_kind, language)


def configuration_root(project_kind: str | None) -> str | None:
    """返回当前项目类型唯一的后端配置根。

    [参数] project_kind：项目类型。
    [返回] str | None：后端配置根路径；前端项目返回 None。
    最近修改时间: 2026-08-02 21:30:00 收敛独立后端与同仓后端配置根。
    """
    # 1. 只映射两类后端项目，避免前端项目误触发配置目录校验。
    return {"backend": "config", "fullstack": "backend/config"}.get(project_kind)


def check_environment_config_mutual_exclusion(
    root: Path, project_kind: str | None,
) -> list[str]:
    """校验 config 互斥。

    [参数] root：待检查项目根；project_kind：项目类型。
    [返回] list[str]：配置模式冲突或非法配置根的错误列表。
    最近修改时间: 2026-08-09 新增 config/embedded/ 与 config/yaml/ 互斥 check。
    """
    if project_kind not in {"backend", "fullstack"}:
        return []
    errors: list[str] = []
    config_root = configuration_root(project_kind)
    assert config_root is not None
    yaml_dir = root / config_root / "yaml"
    embedded_dir = root / config_root / "embedded"
    if yaml_dir.exists() and embedded_dir.exists():
        errors.append(f"{config_root}/yaml/ 与 {config_root}/embedded/ 互斥，只能二选一，推荐优先使用 {config_root}/embedded/")
    return errors


def check_environment_config_path(
    catalog: dict[str, Any], relative: str, is_file: bool, project_kind: str | None, language: str | None,
) -> list[str]:
    """校验后端环境配置的目录、文件名和语言扩展名边界。

    [参数] catalog：配置 Catalog；relative：项目根相对路径；is_file：当前路径是否为文件；project_kind：项目类型；language：后端语言。
    [返回] list[str]：不符合配置位置或命名契约的稳定错误列表。
    最近修改时间: 2026-08-05 新增 config 根 load/model 源码文件放行与稳定失败文案。
    """
    # 1. 非后端项目不参与环境配置目录检查，保留前端既有语义。
    if project_kind not in {"backend", "fullstack"}:
        return []

    errors: list[str] = []
    root = configuration_root(project_kind)
    assert root is not None
    wrong_roots = {"backend": ["backend/config"], "fullstack": ["config"]}[project_kind]
    if any(is_under(relative, wrong_root) for wrong_root in wrong_roots):
        return [f"后端配置必须位于 {root}/: {relative}"]
    if not is_under(relative, root) or relative == root:
        return []

    child = relative[len(root) + 1:]
    # 2. config 根直接源码文件只放行当前语言的 load.<ext> / model.<ext> 两个命名；扩展名映射与二进制入口一致。
    if is_file and "/" not in child:
        extensions = entrypoint_extensions(language)
        stem = Path(child).stem
        suffix = Path(child).suffix.lower()
        if stem in {"load", "model"} and suffix in extensions:
            return []
        if stem in {"load", "model"}:
            return [f"配置根源码文件扩展名不符合规则: {relative}"]
        return [f"配置根源码文件必须为 load.<ext> 或 model.<ext>: {relative}"]

    category, separator, filename = child.partition("/")
    if category not in {"yaml", "embedded"}:
        return [f"配置目录只允许 yaml/ 或 embedded/: {relative}"]
    if not separator:
        return []
    if not is_file or "/" in filename:
        return [f"环境配置文件必须直接位于 {root}/{category}/: {relative}"]

    entries = [
        entry for entry in catalog["entries"]
        if entry["project_kind"] == project_kind
        and entry.get("artifact_kind") == "config"
        and entry.get("category") == category
    ]
    if len(entries) != 1:
        return [f"配置 Catalog 条目不唯一: {project_kind}/{category}"]
    entry = entries[0]
    suffix = Path(filename).suffix.lower()
    allowed_extensions = set(entry.get("allowed_extensions", []))
    if language is not None and category == "embedded":
        allowed_extensions &= COMMON_UTIL_EXTENSIONS[language]
    if suffix not in allowed_extensions:
        return [f"环境配置文件扩展名不符合规则: {relative}"]

    environment_pattern = entry.get("environment_name_pattern", r"[a-z][a-z0-9_]*")
    if category == "yaml":
        filename_pattern = rf"config_{environment_pattern}\.(yaml|yml)"
        if re.fullmatch(filename_pattern, filename) is None:
            return [f"YAML 环境配置文件名必须符合 config_<env>.yaml|yml: {relative}"]
    elif suffix == ".go":
        # 1. 要求格式名后置：config_test.go 会被 Go 当成测试文件并排除出 go build，因此必须写成 config_test_yaml.go。
        #    环境名允许下划线，所以额外排除以 _yaml 结尾的环境名，避免 config_test_yaml_yaml.go 无法唯一切分环境名与格式名。
        filename_pattern = rf"config_{environment_pattern}_yaml\.go"
        environment = filename[len("config_"):-len("_yaml.go")]
        if environment.endswith("_yaml") or re.fullmatch(filename_pattern, filename) is None:
            return [f"Go embedded 环境配置文件名必须符合 config_<env>_yaml.go: {relative}"]
    return []


def check_required_file_content_contracts(
    catalog: dict[str, Any], root: Path, project_kind: str | None,
) -> list[str]:
    """校验同项目根受 Catalog 约束的文件正文保持一致。

    [参数] catalog 为位置 Catalog，root 为待检查项目根，project_kind 为项目类型。
    [返回] list[str]：存在且应当同内容的文件不一致时返回稳定错误。
    最近修改时间: 2026-07-29 23:45:00 新增 AGENTS.md 与 CLAUDE.md 的只读一致性检查。
    """
    if project_kind is None:
        return []
    errors: list[str] = []
    # 1. 仅校验当前项目类型、文件节点且显式声明内容契约的 Catalog 条目。
    for entry in catalog["entries"]:
        expected_path = entry.get("content_must_match")
        if entry["project_kind"] != project_kind or entry.get("node_kind") != "file" or not expected_path:
            continue
        target = root / entry["canonical_path"]
        expected = root / expected_path
        # 2. 旧项目可以暂未补齐双文件；只有二者实际存在时才拒绝正文漂移。
        if target.is_file() and expected.is_file() and target.read_bytes() != expected.read_bytes():
            errors.append(f"规则文件内容不一致: {entry['canonical_path']} 必须与 {expected_path} 一致")
    return errors


def check_required_root_files(
    catalog: dict[str, Any], root: Path, project_kind: str | None,
) -> list[str]:
    """校验 Catalog 声明的必需项目根文件实际存在。

    [参数] catalog 为位置 Catalog，root 为待检查项目根，project_kind 为项目类型。
    [返回] list[str]：必需根文件缺失或被目录占用时返回稳定错误。
    最近修改时间: 2026-08-04 新增三类项目根 Dockerfile 的 strict 存在性检查。
    """
    if project_kind is None:
        return []
    errors: list[str] = []
    # 1. 仅检查 Catalog 中标记为 dockerfile 的必需文件，保留其它治理文件的既有渐进采纳语义。
    for entry in catalog["entries"]:
        if (
            entry["project_kind"] != project_kind
            or entry.get("artifact_kind") != "project-governance"
            or entry.get("category") != "dockerfile"
            or entry.get("node_kind") != "file"
            or entry.get("creation_policy") != "required"
        ):
            continue
        relative = entry["canonical_path"]
        target = root / relative
        if target.is_dir():
            errors.append(f"必需根文件不能是目录: {relative}")
        elif not target.is_file():
            errors.append(f"缺少必需根文件: {relative}")
    return errors


def check_database_storage_source_path(
    catalog: dict[str, Any], relative: str, is_file: bool,
) -> list[str]:
    """校验数据存储连接和模型目录只承载生产源码。

    [参数] catalog：目录事实源；relative：项目相对路径；is_file：当前路径是否为文件。
    [返回] list[str]：数据存储源码扩展名不合规时的稳定错误。
    最近修改时间: 2026-07-31 22:16:49 连接与模型覆盖多类数据存储服务。
    """
    errors: list[str] = []
    # 1. 连接目录与三类模型目录共用 Catalog 声明的源码扩展名，避免在 CLI 重复硬编码技术分类。
    for entry in catalog["entries"]:
        if entry["artifact_kind"] not in {"database_connection", "database_model"}:
            continue
        canonical_path = entry["canonical_path"]
        if not is_file or not relative.startswith(canonical_path + "/"):
            continue
        if Path(relative).suffix.lower() not in set(entry.get("allowed_extensions", [])):
            errors.append(f"数据存储源码目录仅允许生产源码: {relative}")
    return errors


def check_database_sql_path(catalog: dict[str, Any], relative: str, is_file: bool) -> list[str]:
    """校验每个独立 SQL 叶子目录只直接存放 .sql 文件。

    [参数] catalog：目录事实源；relative：项目相对路径；is_file：当前路径是否为文件。
    [返回] list[str]：SQL 扩展名或嵌套层级不合规时的稳定错误。
    最近修改时间: 2026-07-31 22:16:49 新增字段 create、update、delete 独立 SQL 目录。
    """
    errors: list[str] = []
    # 1. 只把 Catalog 声明的 SQL 叶子目录视为文件边界，字段分类根仍由 allowed_children 管理。
    for entry in catalog["entries"]:
        if entry["artifact_kind"] != "database_sql":
            continue
        canonical_path = entry["canonical_path"]
        if relative == canonical_path or not relative.startswith(canonical_path + "/"):
            continue
        child = relative[len(canonical_path) + 1:]
        if not is_file or "/" in child:
            errors.append(f"独立 SQL 目录只允许直接 .sql 文件: {relative}")
        elif Path(relative).suffix.lower() not in set(entry.get("allowed_extensions", [])):
            errors.append(f"独立 SQL 目录只允许 .sql 文件: {relative}")
    return errors


def check_path(
    catalog: dict[str, Any], relative: str, is_file: bool, project_kind: str | None, language: str | None,
) -> list[str]:
    """针对单一路径返回全部严格策略错误。

    [参数] catalog 为位置 Catalog，relative 为项目相对路径，is_file 表示文件，project_kind 与 language 为检查上下文。
    [返回] 当前路径的严格策略错误列表。
    最近修改时间: 2026-08-05 config 根直接源码文件交由配置专项校验唯一裁决，不再命中子目录边界。
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
            # 1.1 config 根直接源码文件由 check_environment_config_path 唯一裁决 load/model 命名与扩展名。
            if is_file and parent in {"config", "backend/config"} and "/" not in relative[len(parent) + 1:]:
                continue
            if first_child not in children:
                errors.append(f"非法子目录: {relative} 不属于 {parent}")
    suffix = Path(relative).suffix.lower()
    if is_file and is_under(relative, "database/migration") and suffix == ".sql":
        errors.append(f"自动迁移目录禁止 SQL 文件: {relative}")
    if is_file and is_under(relative, "database/sql") and suffix in SOURCE_EXTENSIONS:
        errors.append(f"独立 SQL 目录禁止生产源码: {relative}")
    errors.extend(check_database_storage_source_path(catalog, relative, is_file))
    errors.extend(check_database_sql_path(catalog, relative, is_file))
    # 2. 后端根 utils 只承载工具包子目录，common/util 与源码根旧 util 分别执行边界校验。
    if project_kind == "backend" and is_file and Path(relative).parent.as_posix() == "utils":
        errors.append(f"根 utils 禁止直接文件: {relative}")
    if project_kind is not None:
        errors.extend(check_common_util_path(relative, is_file, project_kind, language))
    if project_kind == "backend" and language is not None:
        errors.extend(check_deprecated_source_util_path(relative, is_file, language))
    # 3. 配置与二进制入口属于本轮新增边界，集中追加专用校验并保持原有错误顺序。
    errors.extend(check_environment_config_path(catalog, relative, is_file, project_kind, language))
    errors.extend(check_binary_entrypoint_path(relative, is_file, project_kind, language))
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
    source_extensions = COMMON_UTIL_EXTENSIONS.get(args.language, SOURCE_EXTENSIONS)
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
    最近修改时间: 2026-08-02 23:00:00 放行 Catalog 合法的动态根二进制入口。
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
        # 1. 独立后端根入口是 Catalog 的动态合法路径，不属于静态源码根目录。
        is_dynamic_binary_entrypoint = (
            not check_binary_entrypoint_path(relative, True, project_kind, language)
        )
        if relative.split("/", 1)[0] not in ADOPTION_V2_SOURCE_ROOTS[project_kind] and not is_dynamic_binary_entrypoint:
            errors.append(f"未登记的遗留源码路径: {relative}")
    return errors


def command_check(catalog: dict[str, Any], args: argparse.Namespace) -> int:
    """只读扫描项目目录并输出严格错误或兼容告警。

    [参数] catalog 为位置 Catalog，args 为检查参数。
    [返回] strict 违规或参数缺失返回 2，其余返回 0。
    最近修改时间: 2026-08-04 00:46:50 新增 strict 下三类项目根 Dockerfile 的只读存在性检查。
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
    # 3.1 配置模式互斥检查依赖全目录事实，单独在扫描后执行。
    if args.policy == "strict":
        errors.extend(check_environment_config_mutual_exclusion(root, args.project_kind))
    # 4. strict 校验新项目根 Dockerfile 和双平台规则正文；adoption 不借此强迫旧项目补迁移文件。
    if args.policy == "strict":
        errors.extend(check_required_root_files(catalog, root, args.project_kind))
        errors.extend(check_required_file_content_contracts(catalog, root, args.project_kind))
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
    guide = subparsers.add_parser("guide")
    guide.add_argument("--category", default="all")
    guide.add_argument("--technology")
    guide.add_argument("--language", choices=["go", "java", "node", "python"])
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
    if args.command == "guide":
        return command_guide(catalog, args)
    return command_hash(args)


if __name__ == "__main__":
    raise SystemExit(main())
