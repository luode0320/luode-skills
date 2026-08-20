"""共享静态 Owner 路由。

本模块只根据变更路径和已确认的语义信号计算规则 Owner，不执行规则内容，
也不判断业务正确性。`6-review` 和持续代码质量监督可以复用同一份路由结果。
"""

from __future__ import annotations

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
        add("api-contract-rules", "api-contract-rules", "api-contract-rules", "api-contract-rules")
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


__all__ = ["OWNER_NAMES", "BASE_OWNER_NAMES", "route_owners", "owner_source_map_path"]
