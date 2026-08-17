#!/usr/bin/env python3
"""扫描生产代码中的测试污染：只被 test/ 引用的符号、仅测试可达分支与命名嫌疑。"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path


# 目录分桶：test/ 为测试根，mock/ 为运行时 Mock（两侧都不计），其余源码目录为生产。
TEST_ROOT = "test"
RUNTIME_MOCK_ROOT = "mock"
EXCLUDED_DIRS = {".git", "doc", "node_modules", "vendor", "__pycache__", ".venv", "dist", "build"}

ALLOWLIST_FILENAME = ".test-pollution-allowlist"

# 生产符号定义正则：键为扩展名，值为 (正则, 捕获组序号) 列表。
SYMBOL_PATTERNS: dict[str, list[tuple[re.Pattern[str], int]]] = {
    ".go": [
        (re.compile(r"^func\s+(\w+)\s*\("), 1),
        (re.compile(r"^func\s+\([^)]*\)\s+(\w+)\s*\("), 1),
        (re.compile(r"^(?:var|const)\s+(\w+)\s*[=\[\]\w*]"), 1),
    ],
    ".py": [
        (re.compile(r"^def\s+(\w+)\s*\("), 1),
        (re.compile(r"^class\s+(\w+)\b"), 1),
        (re.compile(r"^([A-Z][A-Z0-9_]*)\s*[:=]"), 1),
    ],
    ".ts": [
        (re.compile(r"^export\s+(?:async\s+)?function\s+(\w+)\s*\("), 1),
        (re.compile(r"^export\s+(?:const|let|class)\s+(\w+)\b"), 1),
    ],
    ".js": [
        (re.compile(r"^export\s+(?:async\s+)?function\s+(\w+)\s*\("), 1),
        (re.compile(r"^export\s+(?:const|let|class)\s+(\w+)\b"), 1),
    ],
    ".java": [
        (re.compile(r"^\s*(?:public|protected)\s+(?:static\s+)?[\w<>\[\],\s]+\s+(\w+)\s*\("), 1),
    ],
}

# Go 的 var/const 分组块：块内每行首个标识符也是包级符号。
GO_GROUP_OPEN = re.compile(r"^(?:var|const)\s*\($")
GO_GROUP_MEMBER = re.compile(r"^\s+(\w+)\s*[=\s]")

# P4 仅测试可达分支：命中即判污染。
TEST_BRANCH_PATTERNS = [
    re.compile(r"\bif\s+.*\bis[_]?[Tt]est\b"),
    re.compile(r"""\b(?:env|Env|ENV|mode|Mode|profile)\b\s*[=!]=\s*["']test["']"""),
    re.compile(r"""\bGetenv\(\s*["'][A-Z_]*TEST[A-Z_]*["']\s*\)"""),
    re.compile(r"""\bos\.environ(?:\.get)?[\(\[]\s*["'][A-Z_]*TEST[A-Z_]*["']"""),
]

# 命名嫌疑：出现在生产目录即提示，不单独阻断。
SUSPECT_NAME = re.compile(r"(?:^|_)(?:seed|fixture|dummy|sample)|(?:ForTest|TestOnly|Mock|Stub|Fake|Probe)", re.IGNORECASE)

VERDICT_POLLUTION = "POLLUTION"
VERDICT_SUSPECT = "SUSPECT"
VERDICT_ORPHAN = "ORPHAN"
VERDICT_EXEMPTED = "EXEMPTED"

# Windows 控制台默认代码页可能不是 UTF-8；CLI 的机器输出必须稳定为 UTF-8。
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")


@dataclass
class Finding:
    """一条扫描结论，对应一个生产符号或一处仅测试可达分支。"""

    path: str
    symbol: str
    line: int
    verdict: str
    reason: str
    prod_refs: int = 0
    test_refs: int = 0
    mock_refs: int = 0


@dataclass
class ScanResult:
    """一次完整扫描的聚合结果。"""

    findings: list[Finding] = field(default_factory=list)
    scanned_files: int = 0

    def blocking(self) -> list[Finding]:
        """返回阻断级结论。

        [参数] 无。
        [返回] list[Finding]：判定为 POLLUTION 的条目。
        最近修改时间: 2026-08-17 新增生产代码测试污染扫描。
        """
        return [item for item in self.findings if item.verdict == VERDICT_POLLUTION]


def bucket_of(relative_path: str) -> str:
    """按相对路径判断文件属于生产、测试还是运行时 Mock。

    [参数] relative_path：相对项目根的 POSIX 路径。
    [返回] str：`prod`、`test` 或 `mock`。
    最近修改时间: 2026-08-17 新增生产代码测试污染扫描。
    """
    head = relative_path.split("/", 1)[0]
    if head == TEST_ROOT:
        return "test"
    if head == RUNTIME_MOCK_ROOT:
        return "mock"
    return "prod"


def iter_source_files(root: Path) -> list[Path]:
    """收集项目内可识别语言的源码文件。

    [参数] root：项目根目录。
    [返回] list[Path]：已排除文档、依赖和缓存目录的源码文件列表。
    最近修改时间: 2026-08-17 新增生产代码测试污染扫描。
    """
    files: list[Path] = []
    for path in sorted(root.rglob("*")):
        if not path.is_file() or path.suffix not in SYMBOL_PATTERNS:
            continue
        relative = path.relative_to(root)
        if EXCLUDED_DIRS.intersection(relative.parts):
            continue
        files.append(path)
    return files


def load_allowlist(root: Path) -> set[tuple[str, str]]:
    """读取豁免登记文件。

    [参数] root：项目根目录。
    [返回] set[tuple[str, str]]：`(相对路径, 符号名)` 的豁免集合。
    最近修改时间: 2026-08-17 新增生产代码测试污染扫描。
    """
    allowlist_path = root / ALLOWLIST_FILENAME
    if not allowlist_path.exists():
        return set()

    entries: set[tuple[str, str]] = set()
    # 1. 逐行解析 `<相对路径>::<符号名>  # <理由>`，忽略空行与整行注释。
    for raw in allowlist_path.read_text(encoding="utf-8").splitlines():
        line = raw.split("#", 1)[0].strip()
        if not line or "::" not in line:
            continue
        path_part, symbol_part = line.split("::", 1)
        entries.add((path_part.strip().replace("\\", "/"), symbol_part.strip()))
    return entries


def extract_symbols(path: Path, relative: str) -> list[tuple[str, int]]:
    """提取单个生产文件中的顶层符号定义。

    [参数] path：源码文件绝对路径；relative：相对项目根的 POSIX 路径。
    [返回] list[tuple[str, int]]：`(符号名, 定义行号)` 列表。
    最近修改时间: 2026-08-17 新增生产代码测试污染扫描。
    """
    patterns = SYMBOL_PATTERNS.get(path.suffix, [])
    symbols: list[tuple[str, int]] = []
    in_go_group = False

    # 1. 逐行匹配语言对应的顶层定义正则，Go 额外处理 var/const 分组块。
    for number, line in enumerate(path.read_text(encoding="utf-8", errors="replace").splitlines(), start=1):
        if path.suffix == ".go":
            if in_go_group:
                if line.strip() == ")":
                    in_go_group = False
                else:
                    member = GO_GROUP_MEMBER.match(line)
                    if member:
                        symbols.append((member.group(1), number))
                continue
            if GO_GROUP_OPEN.match(line):
                in_go_group = True
                continue

        for pattern, group in patterns:
            matched = pattern.match(line)
            if matched:
                symbols.append((matched.group(group), number))
                break

    # 2. 过滤语言入口和惯例名，它们由运行时或框架调用，静态引用面天然为空。
    reserved = {"main", "init", "__init__", "__main__", "setUp", "tearDown"}
    return [(name, number) for name, number in symbols if name not in reserved]


def symbol_spans(symbols: list[tuple[str, int]], total_lines: int) -> dict[str, tuple[int, int]]:
    """按相邻定义行推算每个符号的体范围，用于级联污染判定。

    [参数] symbols：`(符号名, 定义行号)` 列表；total_lines：文件总行数。
    [返回] dict[str, tuple[int, int]]：符号名到 `(起始行, 结束行)` 的映射。
    最近修改时间: 2026-08-17 新增生产代码测试污染扫描。
    """
    ordered = sorted(symbols, key=lambda item: item[1])
    spans: dict[str, tuple[int, int]] = {}
    # 1. 用「本定义行到下一个定义行前一行」近似体范围，语言无关且足够定位引用归属。
    for index, (name, number) in enumerate(ordered):
        end = ordered[index + 1][1] - 1 if index + 1 < len(ordered) else total_lines
        spans[name] = (number, max(number, end))
    return spans


def count_references(root: Path, symbols: set[str]) -> dict[str, dict[str, list[str]]]:
    """单次 rg 调用统计全部符号的引用位置并按目录分桶。

    逐符号启动子进程在真实项目上会退化到不可用（数百个符号即需数分钟），
    因此用 `-f -` 从 stdin 批量传入 pattern，一次拿回全部命中。

    [参数] root：项目根目录；symbols：待统计的符号名集合。
    [返回] dict[str, dict[str, list[str]]]：符号名到「桶名 -> `路径:行号` 列表」的映射。
    最近修改时间: 2026-08-17 新增生产代码测试污染扫描。
    """
    references: dict[str, dict[str, list[str]]] = {symbol: defaultdict(list) for symbol in symbols}
    if not symbols:
        return references

    command = [
        "rg",
        "--no-heading",
        "--line-number",
        "--word-regexp",
        "--fixed-strings",
        "--only-matching",
        "--file",
        "-",
        ".",
    ]
    completed = subprocess.run(
        command,
        cwd=root,
        input="\n".join(sorted(symbols)),
        capture_output=True,
        check=False,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    # rg 退出码 1 表示无命中，属正常结果；大于 1 才是真实执行失败。
    if completed.returncode > 1:
        raise RuntimeError(f"rg 执行失败（退出码 {completed.returncode}）：{completed.stderr.strip()}")

    # 1. 输出形如 `./dir/file.go:6:symbolName`，末段即命中的符号本身。
    for raw in completed.stdout.splitlines():
        parts = raw.rsplit(":", 2)
        if len(parts) < 3:
            continue
        symbol = parts[2].strip()
        if symbol not in references:
            continue
        # Windows 下 rg 输出 `.\dir\file` 形式，先统一分隔符再去掉 `./` 前缀。
        relative = parts[0].replace("\\", "/").removeprefix("./")
        if EXCLUDED_DIRS.intersection(Path(relative).parts):
            continue
        references[symbol][bucket_of(relative)].append(f"{relative}:{parts[1]}")
    return references


def scan_test_branches(path: Path, relative: str) -> list[Finding]:
    """扫描文件中的仅测试可达分支。

    [参数] path：源码文件绝对路径；relative：相对项目根的 POSIX 路径。
    [返回] list[Finding]：命中 P4 的污染条目。
    最近修改时间: 2026-08-17 新增生产代码测试污染扫描。
    """
    findings: list[Finding] = []
    for number, line in enumerate(path.read_text(encoding="utf-8", errors="replace").splitlines(), start=1):
        for pattern in TEST_BRANCH_PATTERNS:
            if pattern.search(line):
                findings.append(
                    Finding(
                        path=relative,
                        symbol=line.strip()[:60],
                        line=number,
                        verdict=VERDICT_POLLUTION,
                        reason="P4 仅测试可达分支：生产执行路径出现测试判定条件",
                    )
                )
                break
    return findings


def changed_files(root: Path) -> set[str] | None:
    """读取 git 工作区改动文件，用于 --diff-only 增量扫描。

    [参数] root：项目根目录。
    [返回] set[str] | None：改动文件相对路径集合；git 不可用时返回 None。
    最近修改时间: 2026-08-17 新增生产代码测试污染扫描。
    """
    # -uall 强制逐文件展开未跟踪目录，否则新增目录会被折叠成一条而漏扫其中的生产文件。
    completed = subprocess.run(
        ["git", "status", "--porcelain", "-uall"],
        cwd=root,
        capture_output=True,
        check=False,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    if completed.returncode != 0:
        return None

    changed: set[str] = set()
    # 1. porcelain 前两列是状态位，第 4 个字符起是路径；重命名取 `->` 后的新路径。
    for raw in completed.stdout.splitlines():
        entry = raw[3:].strip()
        if " -> " in entry:
            entry = entry.split(" -> ", 1)[1]
        changed.add(entry.strip('"').replace("\\", "/"))
    return changed


def reference_owner(reference: str, spans: dict[str, dict[str, tuple[int, int]]]) -> tuple[str, str] | None:
    """定位一处引用落在哪个符号的体范围内。

    [参数] reference：`路径:行号` 形式的引用位置；spans：文件到符号体范围的映射。
    [返回] tuple[str, str] | None：`(路径, 符号名)`，无归属时为 None。
    最近修改时间: 2026-08-17 新增生产代码测试污染扫描。
    """
    path, _, line_text = reference.rpartition(":")
    if not line_text.isdigit():
        return None
    line = int(line_text)
    for symbol, (start, end) in spans.get(path, {}).items():
        if start <= line <= end:
            return (path, symbol)
    return None


def scan(root: Path, diff_only: bool = False) -> ScanResult:
    """执行一次完整的测试污染扫描。

    [参数] root：项目根目录；diff_only：仅扫描 git 工作区改动的生产文件。
    [返回] ScanResult：聚合后的扫描结果。
    最近修改时间: 2026-08-17 新增生产代码测试污染扫描。
    """
    allowlist = load_allowlist(root)
    scope = changed_files(root) if diff_only else None
    result = ScanResult()
    records: list[dict[str, object]] = []
    spans: dict[str, dict[str, tuple[int, int]]] = {}

    # 1. 先提取全部生产符号定义，引用统计合并成单次 rg 调用。
    definitions: list[tuple[str, str, int]] = []
    for path in iter_source_files(root):
        relative = path.relative_to(root).as_posix()
        if bucket_of(relative) != "prod":
            continue
        if scope is not None and relative not in scope:
            continue

        result.scanned_files += 1
        result.findings.extend(scan_test_branches(path, relative))

        content = path.read_text(encoding="utf-8", errors="replace").splitlines()
        symbols = extract_symbols(path, relative)
        spans[relative] = symbol_spans(symbols, len(content))
        definitions.extend((relative, symbol, number) for symbol, number in symbols)

    references = count_references(root, {symbol for _, symbol, _ in definitions})

    # 2. 组装每个符号的引用面，排除其定义行自身。
    for relative, symbol, number in definitions:
        buckets = references.get(symbol, {})
        records.append(
            {
                "path": relative,
                "symbol": symbol,
                "line": number,
                "prod_refs": [item for item in buckets.get("prod", []) if item != f"{relative}:{number}"],
                "test_refs": buckets.get("test", []),
                "mock_refs": buckets.get("mock", []),
            }
        )

    # 3. 首轮判定：生产无调用方且测试有引用，直接命中引用面判据。
    polluted: set[tuple[str, str]] = set()
    reasons: dict[tuple[str, str], str] = {}
    for record in records:
        key = (record["path"], record["symbol"])
        if not record["prod_refs"] and record["test_refs"]:
            polluted.add(key)
            reasons[key] = f"引用面判据：生产引用 0 处，测试引用 {len(record['test_refs'])} 处"

    # 4. 级联传播：生产引用全部来自已污染符号体内的符号，同样是测试污染。
    changed = True
    while changed:
        changed = False
        for record in records:
            key = (record["path"], record["symbol"])
            if key in polluted or not record["prod_refs"]:
                continue
            owners = {reference_owner(item, spans) for item in record["prod_refs"]}
            owners.discard(key)
            if owners and all(owner in polluted for owner in owners):
                polluted.add(key)
                reasons[key] = "级联污染：生产侧引用全部来自已判定为测试污染的符号"
                changed = True

    # 5. 汇总结论，豁免登记在最后统一降级。
    for record in records:
        key = (record["path"], record["symbol"])
        symbol = record["symbol"]

        if key in polluted:
            verdict = VERDICT_POLLUTION
            reason = reasons[key]
        elif record["prod_refs"]:
            continue
        elif SUSPECT_NAME.search(symbol):
            verdict = VERDICT_SUSPECT
            reason = "命名嫌疑：生产目录出现测试语义命名，且无生产调用方"
        else:
            verdict = VERDICT_ORPHAN
            reason = "疑似死代码：全仓无引用，转 6-review 判断是否删除"

        if key in allowlist:
            verdict = VERDICT_EXEMPTED
            reason = f"已登记豁免（原判定 {reason}）"

        result.findings.append(
            Finding(
                path=record["path"],
                symbol=symbol,
                line=record["line"],
                verdict=verdict,
                reason=reason,
                prod_refs=len(record["prod_refs"]),
                test_refs=len(record["test_refs"]),
                mock_refs=len(record["mock_refs"]),
            )
        )

    return result


def render_text(result: ScanResult) -> str:
    """渲染人类可读的扫描报告。

    [参数] result：扫描结果。
    [返回] str：报告正文，末行为 PASS / FAIL 结论。
    最近修改时间: 2026-08-17 新增生产代码测试污染扫描。
    """
    lines = [f"扫描生产文件 {result.scanned_files} 个，命中 {len(result.findings)} 条。", ""]

    # 1. 按严重程度分组输出，阻断级在前。
    for verdict in (VERDICT_POLLUTION, VERDICT_SUSPECT, VERDICT_ORPHAN, VERDICT_EXEMPTED):
        group = [item for item in result.findings if item.verdict == verdict]
        if not group:
            continue
        lines.append(f"[{verdict}] {len(group)} 条")
        for item in group:
            lines.append(f"  {item.path}:{item.line}  {item.symbol}")
            lines.append(f"    {item.reason}")
        lines.append("")

    blocking = result.blocking()
    if blocking:
        lines.append(f"POLLUTION: FAIL（{len(blocking)} 条阻断级污染，须先迁移到 test/ 或登记豁免）")
    else:
        lines.append("POLLUTION: PASS")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    """命令行入口。

    [参数] argv：命令行参数列表，默认取 sys.argv。
    [返回] int：进程退出码，存在阻断级污染时为 1。
    最近修改时间: 2026-08-17 新增生产代码测试污染扫描。
    """
    parser = argparse.ArgumentParser(description="扫描生产代码中的测试污染")
    parser.add_argument("--root", default=".", help="项目根目录，默认当前目录")
    parser.add_argument("--diff-only", action="store_true", help="仅扫描 git 工作区改动的生产文件")
    parser.add_argument("--json", action="store_true", help="以 JSON 输出，便于机器消费")
    args = parser.parse_args(argv)

    root = Path(args.root).resolve()
    if not root.is_dir():
        print(f"项目根目录不存在：{root}", file=sys.stderr)
        return 2

    try:
        result = scan(root, diff_only=args.diff_only)
    except RuntimeError as error:
        print(str(error), file=sys.stderr)
        return 2

    if args.json:
        payload = {
            "scanned_files": result.scanned_files,
            "verdict": "FAIL" if result.blocking() else "PASS",
            "findings": [vars(item) for item in result.findings],
        }
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print(render_text(result))

    return 1 if result.blocking() else 0


if __name__ == "__main__":
    sys.exit(main())
