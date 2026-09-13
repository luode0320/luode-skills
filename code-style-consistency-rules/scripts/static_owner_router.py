"""共享静态 Owner 路由与 `6-review` 检查流水线。

本模块只根据变更路径和已确认的语义信号计算规则 Owner，不执行规则内容，
也不判断业务正确性。`6-review` 和持续代码质量监督可以复用同一份路由结果。

`6-review` 的检查步骤由 `route_review_pipeline()` 从「已加载的来源映射」推导：
来源映射必须真实加载并通过一致性断言（禁止重复 Owner、禁止 v1 对象形态、
Owner 集合必须与 `OWNER_NAMES` 完全一致、声明路径必须存在），
流水线不得引用未登记的 Owner，也不得让任何已登记 Owner 失去检查落点。
"""

from __future__ import annotations

import json
from pathlib import Path
import re
from typing import Iterable


OWNER_NAMES = {
    "api-contract-rules",
    "comment-rules",
    "code-generation-style-rules",
    "code-quality-rules",
    "code-style-consistency-rules",
    "common-util-rules",
    "database-query-rules",
    "database-schema-rules",
    "error-handling-rules",
    "frontend-component-rules",
    "frontend-ui-visual-rules",
    "golang-patterns",
    "logging-trace-rules",
    "micro-business-architecture-rules",
    "naming-rules",
    "package-structure-rules",
    "test-program-rules",
    "time-util-rules",
    "vercel-react-best-practices",
    "vue-best-practices",
    "vue-router-best-practices",
    "windows-encoding-rules",
}

BASE_OWNER_NAMES = (
    "code-generation-style-rules",
    "code-quality-rules",
    "code-style-consistency-rules",
    "naming-rules",
    "comment-rules",
)

FRONTEND_SUFFIXES = (".vue", ".ts", ".tsx", ".js", ".jsx")
REACT_SUFFIXES = (".tsx", ".jsx")
TEST_FILE_PATTERN = re.compile(
    r"(?:^|[/_.-])(?:test|spec|fixture|mock|stub)s?(?:[/_.-]|$)"
    r"|(?:_test|_mock|_stub)\.[a-z0-9]+$|\.(?:test|spec)\.[a-z0-9]+$"
)
WINDOWS_SCRIPT_SUFFIXES = (".ps1", ".bat", ".cmd")
ENCODING_FILES = {".gitattributes", ".editorconfig"}
ENCODING_SIGNALS = {
    "windows-encoding",
    "chinese-text",
    "encoding",
    "bom",
    "eol",
    "mojibake",
    "redirect",
    "charset",
}
COMPONENT_SIGNALS = {
    "component",
    "components",
    "props",
    "emits",
    "events",
    "state",
    "effect",
    "watch",
    "computed",
    "composable",
    "hook",
    "lifecycle",
}
VISUAL_SIGNALS = {
    "frontend-visual",
    "ui",
    "css",
    "style",
    "styles",
    "layout",
    "aria",
    "responsive",
    "a11y",
    "class",
    "classname",
    "color",
}
REACT_SIGNALS = {
    "react",
    "nextjs",
    "next",
    "rsc",
    "hydration",
    "bundle",
    "react-performance",
}
VUE_ROUTER_SIGNALS = {
    "vue-router",
    "route",
    "routes",
    "router",
    "routers",
    "navigation-guard",
    "beforerouteenter",
    "onbeforerouteupdate",
}
MICRO_BUSINESS_SIGNALS = {
    "micro-business",
    "business-isolation",
    "cross-business-import",
    "contract-communication",
}
MICRO_BUSINESS_PATH_TERMS = {
    "business",
    "businesses",
    "contract",
    "contracts",
    "interfaces",
    "assembly",
    "module",
    "modules",
}


def route_owners(changed_files: Iterable[str], signals: Iterable[str] = ()) -> list[str]:
    """按路径和已确认信号返回允许 Owner 的稳定顺序。

    [参数] changed_files：本次变更的仓库相对路径；signals：已确认语义信号
    [返回] 去重后的 Owner 名称列表；空变更返回空列表
    最近修改时间：2026-08-01 00:00:00；统一 6-review 与持续监控的静态 Owner 路由。
    """

    # 1. 规范化输入并为路径、语义信号建立稳定的查找集合。
    files = [str(item) for item in changed_files]
    if not files:
        return []
    normalized_files = [item.replace("\\", "/").lower() for item in files]
    signal_set = {str(item).strip().lower() for item in signals if str(item).strip()}
    result = list(BASE_OWNER_NAMES)
    path_parts = [{part for part in item.split("/") if part} for item in normalized_files]
    path_tokens = [set(re.findall(r"[a-z0-9]+", item)) for item in normalized_files]

    def has_path_term(*terms: str) -> bool:
        """判断完整路径段或文件名 token 是否命中给定术语。

        [参数] terms：待比较的受控路径术语。
        [返回] 是否存在至少一个命中术语。
        最近修改时间：2026-08-01 00:00:00；补齐共享路由局部判定函数的注释元信息。
        """

        # 1. 只对完整路径段和 token 比较，避免任意子串误命中。
        expected = set(terms)
        return any(
            expected.intersection(parts) or expected.intersection(tokens)
            for parts, tokens in zip(path_parts, path_tokens)
        )

    def has_file_suffix(*suffixes: str) -> bool:
        """判断变更集中是否存在给定后缀的文件。

        [参数] suffixes：允许匹配的文件后缀。
        [返回] 是否存在后缀匹配的文件。
        最近修改时间：2026-08-01 00:00:00；补齐共享路由局部判定函数的注释元信息。
        """

        # 1. 使用标准库元组后缀匹配，保持与路径路由规则一致。
        return any(item.endswith(suffixes) for item in normalized_files)

    def has_same_file_term_and_suffix(terms: set[str], suffixes: tuple[str, ...]) -> bool:
        """判断同一文件是否同时满足术语与后缀条件。

        [参数] terms：受控路径术语；suffixes：允许匹配的文件后缀。
        [返回] 是否存在同时命中两类条件的文件。
        最近修改时间：2026-08-01 00:00:00；补齐共享路由局部判定函数的注释元信息。
        """

        # 1. 限制为同一文件的交集，避免跨文件组合造成过度路由。
        return any(
            item.endswith(suffixes) and terms.intersection(parts.union(tokens))
            for item, parts, tokens in zip(normalized_files, path_parts, path_tokens)
        )

    def add(*owners: str) -> None:
        """按声明顺序追加尚未出现的 Owner。

        [参数] owners：待追加的 Owner 名称。
        [返回] 无。
        最近修改时间：2026-08-01 00:00:00；补齐共享路由局部判定函数的注释元信息。
        """

        # 1. 保留首次出现顺序并阻止同一 Owner 重复进入结果。
        for owner in owners:
            if owner not in result:
                result.append(owner)

    if has_path_term("api", "controller", "controllers", "handler", "handlers", "openapi", "swagger") or signal_set.intersection(
        {"http-api", "api-endpoint", "api-request", "api-response", "api-swagger"}
    ):
        add("api-contract-rules")
    if has_path_term("migration", "migrations", "schema", "schemas") or signal_set.intersection({"database-schema", "schema"}):
        add("database-schema-rules")
    if has_file_suffix(".sql") or has_path_term("repository", "repositories", "repo", "dao", "mapper", "query", "queries") or signal_set.intersection(
        {"database-query", "sql", "transaction", "lock"}
    ):
        add("database-query-rules")
    if has_path_term("exception", "exceptions", "error", "errors") or signal_set.intersection({"error-handling", "retry"}):
        add("error-handling-rules")
    if has_path_term("logger", "logging", "tracing") or signal_set.intersection({"logging", "trace", "span"}):
        add("logging-trace-rules")
    if has_path_term("timezone", "scheduler", "cron") or signal_set.intersection({"time", "date", "time-window", "schedule"}):
        add("time-util-rules")
    if has_path_term("package", "module") or any(item.endswith("/main.go") or item == "main.go" for item in normalized_files) or "package-structure" in signal_set:
        add("package-structure-rules")
    if has_path_term("util", "utils", "common", "shared") or "common-util" in signal_set:
        add("common-util-rules")
    if has_file_suffix(".go", "go.mod", "go.sum", "go.work"):
        add("golang-patterns")

    vue_file = has_file_suffix(".vue")
    frontend_code_file = has_file_suffix(*FRONTEND_SUFFIXES)
    if vue_file or "vue" in signal_set:
        add("vue-best-practices")
    if signal_set.intersection(COMPONENT_SIGNALS) or has_same_file_term_and_suffix({"component", "components"}, FRONTEND_SUFFIXES):
        add("frontend-component-rules")
    if signal_set.intersection(VISUAL_SIGNALS) or has_file_suffix(".css", ".scss", ".less", ".html") or has_same_file_term_and_suffix({"style", "styles", "theme", "themes", "layout"}, FRONTEND_SUFFIXES):
        add("frontend-ui-visual-rules")
    if signal_set.intersection(VUE_ROUTER_SIGNALS) or has_same_file_term_and_suffix({"router", "routers", "route", "routes"}, FRONTEND_SUFFIXES):
        if vue_file or frontend_code_file or "vue" in signal_set or "vue-router" in signal_set:
            add("vue-best-practices", "vue-router-best-practices")
    react_file = has_file_suffix(*REACT_SUFFIXES)
    if react_file or signal_set.intersection(REACT_SIGNALS):
        add("vercel-react-best-practices")
        if react_file or signal_set.intersection(COMPONENT_SIGNALS):
            add("frontend-component-rules")
        if signal_set.intersection(VISUAL_SIGNALS):
            add("frontend-ui-visual-rules")
    if any(TEST_FILE_PATTERN.search(item) for item in normalized_files) or signal_set.intersection({"test-program", "fixture", "mock", "stub"}):
        add("test-program-rules")
    if has_file_suffix(*WINDOWS_SCRIPT_SUFFIXES) or any(Path(item).name in ENCODING_FILES for item in normalized_files) or signal_set.intersection(ENCODING_SIGNALS):
        add("windows-encoding-rules")
    if signal_set.intersection(MICRO_BUSINESS_SIGNALS) and (
        has_path_term(*MICRO_BUSINESS_PATH_TERMS)
        or signal_set.intersection({"cross-business-import", "contract-communication"})
    ):
        add("micro-business-architecture-rules")
    return result


def owner_source_map_path(repository_root: str | Path) -> Path:
    """返回共享 Owner 静态来源映射的仓库绝对路径。

    [参数] repository_root：待解析来源映射的仓库根目录。
    [返回] 静态 Owner 来源映射的绝对路径。
    最近修改时间：2026-08-01 00:00:00；暴露共享路由唯一的来源映射入口。
    """

    # 1. 统一由风格 Owner 解析来源映射的绝对路径。
    return Path(repository_root).expanduser().resolve() / "code-style-consistency-rules" / "references" / "static-owner-source-map.json"


SOURCE_MAP_VERSION = 2
OWNER_KEY_PATTERN = re.compile(r'"owner":\s*"([a-z0-9-]+)"')
SITE_KEY_PATTERN = re.compile(r'"source_paths":\s*\[')

# 规则来源只收 Markdown：非 Markdown 的脚本与配置由各自的登记位点单独负责。
RULE_REFERENCE_SUFFIX = ".md"

# 非规则资产名单：溯源登记、吸收映射与仓库治理文件不承载判定口径，
# 因此不要求登记进来源映射，也不参与 6-review 的检查来源投影。
NON_RULE_FILE_NAMES = frozenset(
    {
        "readme.md",
        "license.md",
        "license",
        "sync.md",
        "agents.md",
        "claude.md",
        "changelog.md",
        "source-notes.md",
        "workbuddy-absorption-map.md",
    }
)
NON_RULE_FILE_PATTERN = re.compile(r"^case-[a-z0-9-]+-absorption\.md$")
NON_RULE_DIR_NAMES = frozenset(
    {"templates", "data", "assets", "scripts", "__pycache__", ".workbuddy"}
)


class OwnerSourceMapError(RuntimeError):
    """来源映射结构失真或违反加载契约。

    最近修改时间：2026-09-11 00:00:00；新增来源映射加载失败的统一异常。
    """


def _read_source_map_text(repository_root: str | Path) -> str:
    """读取来源映射原文，缺失即失败关闭。

    [参数] repository_root：仓库根目录。
    [返回] 来源映射的 UTF-8 原文。
    最近修改时间：2026-09-11 00:00:00；为文本层对账提供原文入口。
    """

    # 1. 读取失败必须显式抛出，不能退回空映射造成静默漏检。
    path = owner_source_map_path(repository_root)
    if not path.is_file():
        raise OwnerSourceMapError(f"来源映射不存在：{path}")
    return path.read_text(encoding="utf-8")


def _assert_text_matches_parsed(text: str, owners: list[dict]) -> None:
    """对账文本声明与解析结果，拦截静默覆盖。

    [参数] text：来源映射原文；owners：解析后的 Owner 列表。
    [返回] 无；不一致时抛出 OwnerSourceMapError。
    最近修改时间：2026-09-11 00:00:00；让重复 Owner 覆盖在加载期就报错。
    """

    # 1. 文本层独立计数，任何"少一块"都在这里暴露。
    declared_owners = OWNER_KEY_PATTERN.findall(text)
    declared_sites = len(SITE_KEY_PATTERN.findall(text))
    parsed_sites = sum(len(item.get("sites") or []) for item in owners if isinstance(item, dict))
    if len(declared_owners) != len(owners):
        raise OwnerSourceMapError(
            f"Owner 声明数与解析数不一致：文本 {len(declared_owners)} / 解析 {len(owners)}。"
        )
    if declared_sites != parsed_sites:
        raise OwnerSourceMapError(
            f"来源分组数与解析数不一致：文本 {declared_sites} / 解析 {parsed_sites}。"
        )

    # 2. 去重后数量不变才说明没有同键覆盖。
    duplicated = sorted({name for name in declared_owners if declared_owners.count(name) > 1})
    if duplicated:
        raise OwnerSourceMapError(f"来源映射重复声明 Owner：{duplicated}")


def _assert_site_paths(repository_root: Path, owner: str, site_index: int, site: dict) -> list[str]:
    """校验单个来源分组并返回其仓库相对路径。

    [参数] repository_root：仓库根目录；owner：归属 Owner；site_index：分组序号；site：分组内容。
    [返回] 该分组的仓库相对路径列表；违例时抛出 OwnerSourceMapError。
    最近修改时间：2026-09-11 00:00:00；落实静态路由契约中的路径拒绝条件。
    """

    # 1. 分组必须声明来源类型，且至少有一条来源路径，glob 不得为空字符串。
    consumption = site.get("consumption")
    if not isinstance(consumption, str) or not consumption.strip():
        raise OwnerSourceMapError(f"{owner} 第 {site_index} 组缺少 consumption。")
    paths = site.get("source_paths")
    if not isinstance(paths, list) or not paths:
        raise OwnerSourceMapError(f"{owner} 第 {site_index} 组 source_paths 必须是非空列表。")
    globs = site.get("source_globs", [])
    if not isinstance(globs, list) or any(not isinstance(item, str) or not item.strip() for item in globs):
        raise OwnerSourceMapError(f"{owner} 第 {site_index} 组 source_globs 不得包含空 glob。")

    # 2. 拒绝绝对路径、路径穿越、跨 Owner 路径与缺失文件。
    collected = []
    for raw in paths:
        if not isinstance(raw, str) or not raw.strip():
            raise OwnerSourceMapError(f"{owner} 第 {site_index} 组存在空路径。")
        normalized = raw.replace("\\", "/")
        if normalized.startswith("/") or re.match(r"^[A-Za-z]:", normalized):
            raise OwnerSourceMapError(f"{owner} 第 {site_index} 组不得使用绝对路径：{raw}")
        if ".." in normalized.split("/"):
            raise OwnerSourceMapError(f"{owner} 第 {site_index} 组不得路径穿越：{raw}")
        if not normalized.startswith(f"{owner}/"):
            raise OwnerSourceMapError(f"{owner} 第 {site_index} 组存在跨 Owner 路径：{raw}")
        if not (repository_root / normalized).is_file():
            raise OwnerSourceMapError(f"{owner} 声明了不存在的来源文件：{raw}")
        collected.append(normalized)
    return collected


def iter_rule_reference_files(repository_root: str | Path, owner: str) -> list[str]:
    """列出单个 Owner 目录下应当登记为规则来源的 Markdown 文件。

    [参数] repository_root：仓库根目录；owner：Owner 名称。
    [返回] 按路径排序的仓库相对路径列表。
    最近修改时间：2026-09-11 00:00:00；为来源映射覆盖率断言提供唯一枚举口径。
    """

    # 1. 只枚举 Markdown，并排除非规则资产目录与命名。
    owner_dir = Path(repository_root) / owner
    if not owner_dir.is_dir():
        return []
    found: list[str] = []
    for path in sorted(owner_dir.rglob(f"*{RULE_REFERENCE_SUFFIX}")):
        relative = path.relative_to(repository_root)
        if set(relative.parts[:-1]) & NON_RULE_DIR_NAMES:
            continue
        name = path.name.lower()
        if name in NON_RULE_FILE_NAMES or NON_RULE_FILE_PATTERN.match(name):
            continue
        found.append(str(relative).replace("\\", "/"))
    return found


def _assert_rule_file_coverage(repository_root: Path, mapping: dict[str, dict]) -> None:
    """断言目录内每个规则文件都已登记，防止来源映射静默漏登记。

    [参数] repository_root：仓库根目录；mapping：已校验的来源映射。
    [返回] 无；存在未登记的规则文件时抛出 OwnerSourceMapError。
    最近修改时间：2026-09-11 00:00:00；让漏登记的规则文件在加载期就暴露。
    """

    # 1. 逐 Owner 比对目录枚举结果与登记结果，任一遗漏都失败关闭。
    unregistered: list[str] = []
    for owner in sorted(mapping):
        declared = set(mapping[owner]["source_paths"])
        for path in iter_rule_reference_files(repository_root, owner):
            if path not in declared:
                unregistered.append(path)
    if unregistered:
        raise OwnerSourceMapError(
            "以下规则文件未在来源映射登记，会导致 6-review 失去检查落点："
            + "、".join(unregistered)
            + "；请补登记，或按 NON_RULE_FILE_NAMES / NON_RULE_DIR_NAMES 明确豁免。"
        )


def load_owner_source_map(repository_root: str | Path = ".") -> dict[str, dict]:
    """加载并校验静态 Owner 来源映射。

    [参数] repository_root：仓库根目录，用于解析相对路径。
    [返回] {owner: {"sites": [...], "source_paths": [...]}} 的映射。
    最近修改时间：2026-09-11 00:00:00；把来源映射从死数据变成带断言的加载入口。
    """

    # 1. 原文与结构形态先过关，v1 对象形态直接失败关闭。
    text = _read_source_map_text(repository_root)
    try:
        document = json.loads(text)
    except json.JSONDecodeError as error:
        raise OwnerSourceMapError(f"来源映射不是合法 JSON：{error}") from error
    if document.get("version") != SOURCE_MAP_VERSION:
        raise OwnerSourceMapError(
            f"来源映射 version 必须是 {SOURCE_MAP_VERSION}（当前 {document.get('version')}）；"
            "v1 用对象 key 承载 Owner，同一 Owner 的多个位点会被 JSON 静默覆盖。"
        )
    owners = document.get("owners")
    if not isinstance(owners, list) or not owners:
        raise OwnerSourceMapError("来源映射 owners 必须是非空数组。")

    # 2. 文本层对账，拦截重复声明与分组丢失。
    _assert_text_matches_parsed(text, owners)

    # 3. 逐 Owner 校验登记状态、重复与来源路径合法性。
    root = Path(repository_root).expanduser().resolve()
    mapping: dict[str, dict] = {}
    for index, item in enumerate(owners):
        if not isinstance(item, dict):
            raise OwnerSourceMapError(f"owners[{index}] 必须是对象。")
        owner = item.get("owner")
        if not isinstance(owner, str) or not owner.strip():
            raise OwnerSourceMapError(f"owners[{index}] 缺少 owner。")
        if owner not in OWNER_NAMES:
            raise OwnerSourceMapError(f"来源映射出现未登记 Owner：{owner}；请先登记 OWNER_NAMES。")
        if owner in mapping:
            raise OwnerSourceMapError(f"来源映射重复声明 Owner：{owner}")
        sites = item.get("sites")
        if not isinstance(sites, list) or not sites:
            raise OwnerSourceMapError(f"{owner} 的 sites 必须是非空数组。")
        merged: list[str] = []
        for site_index, site in enumerate(sites, start=1):
            if not isinstance(site, dict):
                raise OwnerSourceMapError(f"{owner} 第 {site_index} 组必须是对象。")
            for path in _assert_site_paths(root, owner, site_index, site):
                if path not in merged:
                    merged.append(path)
        mapping[owner] = {"sites": sites, "source_paths": merged}

    # 4. Owner 集合必须与路由声明完全一致，任一方向漂移都失败关闭。
    if set(mapping) != set(OWNER_NAMES):
        missing = sorted(set(OWNER_NAMES) - set(mapping))
        extra = sorted(set(mapping) - set(OWNER_NAMES))
        raise OwnerSourceMapError(f"来源映射与 OWNER_NAMES 不一致；缺少 {missing}，多余 {extra}。")

    # 5. 目录内的规则文件必须全部登记，否则 6-review 会静默漏检。
    _assert_rule_file_coverage(root, mapping)
    return mapping


def owner_source_paths(repository_root: str | Path, owner: str) -> tuple[str, ...]:
    """返回单个 Owner 的去重来源路径。

    [参数] repository_root：仓库根目录；owner：Owner 名称。
    [返回] 仓库相对路径元组；Owner 未登记时抛出 OwnerSourceMapError。
    最近修改时间：2026-09-11 00:00:00；为消费者提供按 Owner 取来源的稳定入口。
    """

    # 1. 统一走加载入口，消费者不得自行读取 JSON 绕过断言。
    mapping = load_owner_source_map(repository_root)
    if owner not in mapping:
        raise OwnerSourceMapError(f"Owner 未在来源映射登记：{owner}")
    return tuple(mapping[owner]["source_paths"])


REVIEW_STEPS = (
    {
        "step_id": "STYLE-01",
        "name": "静态格式与编码一致性",
        "dimensions": "维度2 编写习惯与风格；维度5 静态风格命名与位置",
        "owners": ("code-style-consistency-rules", "windows-encoding-rules"),
    },
    {
        "step_id": "STYLE-02",
        "name": "命名与符号引用一致",
        "dimensions": "维度3 命名方式；维度4 引用方式、方法名、包别名",
        "owners": ("naming-rules",),
    },
    {
        "step_id": "STYLE-03",
        "name": "注释分层与定义位置",
        "dimensions": "维度3 注释与代码、变量的定义位置",
        "owners": ("comment-rules",),
    },
    {
        "step_id": "STYLE-04",
        "name": "函数签名与参数结构",
        "dimensions": "维度6 函数参数顺序、数量与单参数/结构体取舍",
        "owners": ("code-quality-rules",),
    },
    {
        "step_id": "STYLE-05",
        "name": "结构与落点（结构体角色 / 目录位置 / 依赖方向）",
        "dimensions": "维度1 架构与模块划分；维度7 结构体按类型与作用分层",
        "owners": ("package-structure-rules", "micro-business-architecture-rules"),
    },
    {
        "step_id": "STYLE-06",
        "name": "公共复用与工具落点（纯转换函数 / 工具索引）",
        "dimensions": "维度8 纯转换工具函数落点；维度9 工具函数索引文档",
        "owners": ("common-util-rules",),
    },
    {
        "step_id": "STYLE-07",
        "name": "接口契约与数据访问",
        "dimensions": "维度1 架构与模块划分（接口与数据边界）",
        "owners": (
            "api-contract-rules",
            "database-query-rules",
            "database-schema-rules",
            "error-handling-rules",
            "logging-trace-rules",
            "time-util-rules",
        ),
    },
    {
        "step_id": "STYLE-08",
        "name": "语言与框架特异写法",
        "dimensions": "维度2 编写习惯与代码风格（语言与框架层）",
        "owners": (
            "golang-patterns",
            "vue-best-practices",
            "vue-router-best-practices",
            "vercel-react-best-practices",
            "frontend-component-rules",
            "frontend-ui-visual-rules",
        ),
    },
    {
        "step_id": "STYLE-09",
        "name": "测试资产与编码前契约",
        "dimensions": "维度5 静态风格命名与位置（测试资产归位）",
        "owners": ("test-program-rules", "code-generation-style-rules"),
    },
)


def route_review_pipeline(
    changed_files: Iterable[str],
    signals: Iterable[str] = (),
    repository_root: str | Path = ".",
) -> list[dict]:
    """由已加载的来源映射推导 `6-review` 的有序检查步骤。

    [参数] changed_files：本次变更的仓库相对路径；signals：已确认语义信号；repository_root：仓库根目录。
    [返回] 有序步骤列表，每步含 step_id / name / dimensions / owners / sources。
    最近修改时间：2026-09-11 00:00:00；把来源映射加载纳入 6-review 流水线。
    """

    # 1. 先按既有路由计算相关 Owner；无变更直接返回空步骤。
    owners = route_owners(changed_files, signals)
    if not owners:
        return []

    # 2. 加载来源映射；未通过断言的映射不得进入流水线。
    mapping = load_owner_source_map(repository_root)

    # 3. 流水线不得引用未登记 Owner，也不得让任何已登记 Owner 失去检查落点。
    step_owners = {owner for step in REVIEW_STEPS for owner in step["owners"]}
    unregistered = sorted(step_owners - set(mapping))
    if unregistered:
        raise OwnerSourceMapError(f"流水线引用了未登记的 Owner：{unregistered}")
    uncovered = sorted(set(mapping) - step_owners)
    if uncovered:
        raise OwnerSourceMapError(f"以下已登记 Owner 在流水线中没有检查落点：{uncovered}")

    # 4. 按步骤投影命中的 Owner 与来源路径，保持声明顺序。
    selected = set(owners)
    pipeline = []
    for step in REVIEW_STEPS:
        hit = [owner for owner in step["owners"] if owner in selected]
        if not hit:
            continue
        sources: list[str] = []
        for owner in hit:
            for path in mapping[owner]["source_paths"]:
                if path not in sources:
                    sources.append(path)
        pipeline.append(
            {
                "step_id": step["step_id"],
                "name": step["name"],
                "dimensions": step["dimensions"],
                "owners": hit,
                "sources": sources,
            }
        )
    return pipeline


def render_review_pipeline(pipeline: Iterable[dict]) -> str:
    """把流水线渲染成可粘贴进 `6-review` 记录的 Markdown 清单。

    [参数] pipeline：`route_review_pipeline` 的返回值。
    [返回] Markdown 文本；空流水线返回空字符串。
    最近修改时间：2026-09-11 00:00:00；让检查步骤可直接进入 6-review 记录。
    """

    # 1. 逐步输出步骤、覆盖维度、Owner 与来源，判定口径指向流水线文档。
    steps = list(pipeline)
    if not steps:
        return ""
    lines = ["## 检查步骤（由来源映射推导）", ""]
    for step in steps:
        anchor = step["step_id"].lower()
        lines.append(f"### {step['step_id']} {step['name']}")
        lines.append(f"- 覆盖维度：{step['dimensions']}")
        lines.append(f"- 规则 Owner：{'、'.join(step['owners'])}")
        lines.append(f"- 判定口径与证据格式：`references/style-review-pipeline.md#{anchor}`")
        lines.append("- 规则来源：")
        for source in step["sources"]:
            lines.append(f"  - `{source}`")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def _main(argv: list[str] | None = None) -> int:
    """命令行入口：按变更路径输出 `6-review` 检查流水线。

    [参数] argv：命令行参数，缺省取 `sys.argv`。
    [返回] 进程退出码；来源映射校验失败返回 2。
    最近修改时间：2026-09-11 00:00:00；让 6-review 可直接运行并逐步检查。
    """

    import argparse
    import sys

    # 1. Windows 控制台默认编码会破坏中文输出，显式统一为 UTF-8。
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(description="按变更路径输出 6-review 检查流水线")
    parser.add_argument("--changed", action="append", default=[], help="变更文件相对路径，可重复或逗号分隔")
    parser.add_argument("--signal", action="append", default=[], help="已确认语义信号，可重复")
    parser.add_argument("--root", default=".", help="仓库根目录")
    parser.add_argument("--json", action="store_true", help="输出 JSON 而非 Markdown")
    args = parser.parse_args(argv)

    changed: list[str] = []
    for item in args.changed:
        changed.extend(part.strip() for part in item.split(",") if part.strip())
    try:
        pipeline = route_review_pipeline(changed, args.signal, args.root)
    except OwnerSourceMapError as error:
        print(f"来源映射校验失败：{error}", file=sys.stderr)
        return 2
    if args.json:
        print(json.dumps(pipeline, ensure_ascii=False, indent=2))
    else:
        print(render_review_pipeline(pipeline), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(_main())


__all__ = [
    "BASE_OWNER_NAMES",
    "NON_RULE_DIR_NAMES",
    "NON_RULE_FILE_NAMES",
    "NON_RULE_FILE_PATTERN",
    "OWNER_NAMES",
    "REVIEW_STEPS",
    "RULE_REFERENCE_SUFFIX",
    "SOURCE_MAP_VERSION",
    "OwnerSourceMapError",
    "iter_rule_reference_files",
    "load_owner_source_map",
    "owner_source_map_path",
    "owner_source_paths",
    "render_review_pipeline",
    "route_owners",
    "route_review_pipeline",
]
