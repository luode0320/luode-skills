#!/usr/bin/env python3
"""Distill every Markdown note from one Obsidian vault into a target vault.

The source vault is read from the configured local directory. Target notes are
written only through the public Obsidian CLI bridge.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import tempfile
import time
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path


SENSITIVE_WORDS = re.compile(
    r"(钱包|服务器|vpn|VPN|备份|内网|邮件|smtp|SMTP|私钥|助记词|密码|密钥|"
    r"token|secret|api[_-]?key|private[_-]?key|地址|交易所|资产|兑换|"
    r"后台管理|部署|数据库连接)",
    re.IGNORECASE,
)

SECRET_PATTERNS = [
    re.compile(
        r"(?i)(api[_-]?key|secret|token|password|passwd|pwd|private[_-]?key|"
        r"mnemonic|助记词|私钥|密码|密钥)\s*[:=：]\s*[^\s`]+"
    ),
    re.compile(r"(?i)(bearer\s+)[A-Za-z0-9._\-]{16,}"),
    re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b"),
    re.compile(r"(?i)(mongodb|mysql|postgresql|redis)://[^\s`]+"),
]

BRIDGE_PATH = Path(__file__).with_name("obsidian_cli_bridge.py")


def run_bridge(operation: str, path: str | None = None, content: str | None = None) -> str:
    """通过公开 bridge 执行固定 vault 的目标读写。

    [参数] operation: allowlist 操作；path: 知识库相对路径；content: UTF-8 Markdown 正文。
    [返回] bridge read 操作的正文，其他操作返回空字符串。
    最近修改时间: 2026-07-13 17:32:38 目标读写统一交给 bridge，批处理不保留独立 transport。
    """
    # 1. 正文通过临时 UTF-8 文件传给 bridge，避免 Windows 命令行参数长度限制。
    command = [sys.executable, str(BRIDGE_PATH), operation]
    if path:
        command.extend(["--path", path])
    temporary_path: Path | None = None
    if content is not None:
        with tempfile.NamedTemporaryFile("w", encoding="utf-8", suffix=".md", delete=False) as temporary_file:
            temporary_file.write(content)
            temporary_path = Path(temporary_file.name)
        command.extend(["--content-file", str(temporary_path)])
    command.append("--json")
    try:
        completed = subprocess.run(command, capture_output=True, text=True, encoding="utf-8", check=False)
    finally:
        if temporary_path is not None:
            temporary_path.unlink(missing_ok=True)
    # 2. bridge 的退出码和 JSON 成功标记都必须通过，不能让失败写入继续执行。
    if completed.returncode != 0:
        raise RuntimeError(f"bridge {operation} failed: {completed.stderr.strip() or completed.stdout.strip()}")
    response = json.loads(completed.stdout)
    if not response.get("ok"):
        raise RuntimeError(f"bridge {operation} failed: {response.get('code')}")
    return str(response.get("data", {}).get("output", ""))


@dataclass
class NoteRow:
    """逐篇沉淀表格中的单行摘要记录。"""

    index: int
    path: str
    subgroup: str
    summary: str
    keywords: str
    status: str


@dataclass
class BatchResult:
    """单个顶层目录批次的处理结果。"""

    folder: str
    title: str
    target: str
    files: int
    read: int
    errors: int
    seconds: float


def validate_cli_and_vaults(args: argparse.Namespace) -> None:
    """校验 Obsidian CLI、源 vault 和目标 vault 的注册状态。

    [参数] args: 命令行参数。
    [返回] 无。
    最近修改时间: 2026-07-13 17:32:38 删除旧 CLI 注册校验，仅保留源目录与固定目标根校验。
    """
    # 1. 固定目标 vault 的发现和 transport 仅由 bridge 负责。
    run_bridge("doctor")
    source_root = Path(args.source_root).resolve()
    if not source_root.exists() or not source_root.is_dir():
        raise RuntimeError(f"source root is not a directory: {source_root}")
    if str(args.target_root).rstrip("\\/").casefold() == r"d:\obsidian_data\知识库".casefold():
        raise RuntimeError("LEGACY_NESTED_VAULT_MODEL: target-root must be D:\\obsidian_data")
    if str(args.target_root).rstrip("\\/").casefold() != r"d:\obsidian_data".casefold():
        raise RuntimeError("target-root must be D:\\obsidian_data")
    print(f"source_vault={args.source_vault} path={source_root}")
    print("target_vault=fixed bridge vault")


def iter_markdown_files(source_root: Path) -> list[Path]:
    """遍历源 vault 中非隐藏目录下的 Markdown 文件。

    [参数] source_root: 源 vault 根目录。
    [返回] 按相对路径排序后的 Markdown 文件列表。
    最近修改时间: 2026-07-07 为新增脚本补齐遍历规则说明。
    """
    files: list[Path] = []
    for path in source_root.rglob("*.md"):
        relative_parts = path.relative_to(source_root).parts
        if any(part.startswith(".") for part in relative_parts):
            continue
        files.append(path)
    return sorted(files, key=lambda p: p.relative_to(source_root).as_posix())


def read_text(path: Path) -> tuple[str, str]:
    """按常见编码读取源 Markdown。

    [参数] path: 源 Markdown 文件路径。
    [返回] 文本内容和实际采用的编码名称。
    最近修改时间: 2026-07-07 为新增脚本补齐编码兜底说明。
    """
    data = path.read_bytes()
    for encoding in ("utf-8-sig", "utf-8", "gb18030"):
        try:
            return data.decode(encoding), encoding
        except UnicodeDecodeError:
            continue
    return data.decode("utf-8", errors="replace"), "utf-8-replace"


def strip_frontmatter(text: str) -> str:
    """移除 Markdown frontmatter，便于提取正文摘要。

    [参数] text: Markdown 原文。
    [返回] 去掉 frontmatter 后的正文。
    最近修改时间: 2026-07-07 为新增脚本补齐正文提取说明。
    """
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) == 3:
            return parts[2]
    return text


def sanitize(text: str) -> str:
    """脱敏文本中的凭据、地址和连接串。

    [参数] text: 待脱敏文本。
    [返回] 已替换敏感片段的文本。
    最近修改时间: 2026-07-07 为新增脚本补齐敏感信息保护说明。
    """
    result = text
    for pattern in SECRET_PATTERNS:
        result = pattern.sub(
            lambda match: (match.group(1) if match.groups() else "") + "[REDACTED]",
            result,
        )
    return result


def clean_cell(value: object, limit: int = 180) -> str:
    """清洗 Markdown 表格单元格文本。

    [参数] value: 原始值；limit: 最大字符数。
    [返回] 可安全放入 Markdown 表格的短文本。
    最近修改时间: 2026-07-07 为新增脚本补齐表格清洗说明。
    """
    text = sanitize(str(value))
    text = re.sub(r"\s+", " ", text).strip().replace("|", "/")
    if len(text) > limit:
        text = text[: limit - 1] + "…"
    return text or "-"


def clean_slug(name: str) -> str:
    """把目录名转换为可用于目标笔记路径的短名称。

    [参数] name: 原始目录名。
    [返回] 去掉序号并替换非法路径字符后的名称。
    最近修改时间: 2026-07-07 为新增脚本补齐路径名称清洗说明。
    """
    slug = re.sub(r"^\d+[.、_-]*", "", name).strip() or name
    return re.sub(r'[<>:"/\\|?*]', "-", slug)


def extract_summary(relative_path: str, title: str, text: str) -> tuple[str, str, str, bool]:
    """从单篇 Markdown 中提取摘要、关键词、状态和敏感标记。

    [参数] relative_path: 源文件相对路径；title: 文件标题；text: Markdown 原文。
    [返回] 摘要、关键词、状态和是否敏感的布尔值。
    最近修改时间: 2026-07-07 为新增脚本补齐摘要提取说明。
    """
    body = strip_frontmatter(text)
    body_without_code = re.sub(r"```.*?```", " ", body, flags=re.S)
    headings = [
        re.sub(r"[#`*_\[\]]", "", match.group(1)).strip()
        for match in re.finditer(r"^#{1,4}\s+(.+)$", body_without_code, flags=re.M)
    ]
    headings = [heading for heading in headings if heading][:8]
    paragraph = ""
    for line in body_without_code.splitlines():
        line = line.strip()
        if not line or line.startswith(("#", ">", "|", "- ", "* ", "!", "```")):
            continue
        if re.match(r"^\d+[.、)]\s*$", line):
            continue
        if len(line) >= 18:
            paragraph = line
            break
    sensitive = bool(SENSITIVE_WORDS.search(relative_path + "\n" + body[:1200]))
    if sensitive:
        summary = (
            f"围绕《{title}》整理；该主题可能包含敏感配置、资产或环境上下文，"
            "本次只沉淀标题、小节和通用知识线索，不摘录密钥/账号/token/地址原值。"
        )
    elif paragraph:
        summary = f"围绕《{title}》整理；摘要线索：{paragraph}"
    else:
        summary = f"围绕《{title}》整理。"
    if headings:
        summary += " 主要小节：" + "、".join(headings[:4]) + "。"
    keywords = "、".join(dict.fromkeys([title, *headings[:6]]))
    status = "未完成" if "未完成" in relative_path or "未完成" in body[:600] else "active"
    return clean_cell(summary, 150), clean_cell(keywords, 100), status, sensitive


def build_category_index(files: list[Path], source_root: Path) -> dict[str, list[Path]]:
    """按顶层目录给源 Markdown 分批。

    [参数] files: Markdown 文件列表；source_root: 源 vault 根目录。
    [返回] 顶层目录到文件列表的映射。
    最近修改时间: 2026-07-07 为新增脚本补齐批次拆分说明。
    """
    categories: dict[str, list[Path]] = defaultdict(list)
    for path in files:
        relative = path.relative_to(source_root).as_posix()
        top = relative.split("/", 1)[0] if "/" in relative else "根目录"
        categories[top].append(path)
    return dict(sorted(categories.items(), key=lambda item: item[0]))


def process_category(
    args: argparse.Namespace,
    source_root: Path,
    folder: str,
    paths: list[Path],
) -> BatchResult:
    """处理一个顶层目录批次并生成逐篇沉淀笔记。

    [参数] args: 命令行参数；source_root: 源 vault 根目录；folder: 顶层目录名；paths: 本批次文件列表。
    [返回] 本批次处理结果。
    最近修改时间: 2026-07-13 17:32:38 目标笔记创建和分块追加直接复用 bridge。
    """
    # 1. 先从源目录生成本批次的脱敏摘要和目标笔记路径。
    started = time.time()
    title = clean_slug(folder)
    target_path = f"{args.target_prefix}/{title}-逐篇沉淀.md"
    rows: list[NoteRow] = []
    errors: list[tuple[str, str]] = []
    sub_counts: Counter[str] = Counter()
    sensitive_count = 0
    encodings: Counter[str] = Counter()

    for index, path in enumerate(paths, 1):
        relative = path.relative_to(source_root).as_posix()
        rest = relative[len(folder) :].lstrip("/") if relative.startswith(folder) else relative
        subgroup = rest.split("/", 1)[0] if "/" in rest else "(根目录)"
        sub_counts[subgroup] += 1
        try:
            text, encoding = read_text(path)
            encodings[encoding] += 1
            note_title = path.stem
            summary, keywords, status, sensitive = extract_summary(relative, note_title, text)
            if sensitive:
                sensitive_count += 1
            rows.append(NoteRow(index, relative, subgroup, summary, keywords, status))
        except Exception as exc:  # noqa: BLE001
            errors.append((relative, str(exc)))

    header = f"""---
id: 20260707-blog-data-{clean_slug(folder)}-distilled
type: moc
title: blog-data {title}逐篇沉淀
aliases:
  - {title}逐篇沉淀
  - blog-data {title}
tags:
  - blog-data/distilled
  - technical-knowledge/{clean_slug(folder)}
status: active
created: 2026-07-07
updated: 2026-07-07
source_sessions: []
source_refs:
  - F:/blog/data/{folder}
related:
  - [[30-MOCs/blog-data-技术知识地图|blog-data 技术知识地图]]
  - [[{args.target_prefix}/全量逐篇沉淀总览|全量逐篇沉淀总览]]
entities:
  - Obsidian
topics:
  - {title}
confidence: medium
---

# blog-data {title}逐篇沉淀

> [!NOTE]
> 本笔记由批处理脚本逐篇读取源 vault `data` 中 `{folder}` 下的 Markdown 后生成。它保留每篇文档的归类、摘要线索、关键小节和状态；敏感字段按规则脱敏或不摘录原值。

## 批次概览

| 项目 | 值 |
| --- | --- |
| 源目录 | `F:/blog/data/{folder}` |
| 文档数 | {len(paths)} |
| 成功读取 | {len(rows)} |
| 读取失败 | {len(errors)} |
| 敏感主题标记 | {sensitive_count} |
| 编码 | {clean_cell(dict(encodings), 240)} |
| 生成日期 | 2026-07-07 |

## 子类统计

| 子类 | 文档数 |
| --- | ---: |
"""
    for subgroup, count in sorted(sub_counts.items(), key=lambda item: (-item[1], item[0])):
        header += f"| {clean_cell(subgroup, 90)} | {count} |\n"
    header += (
        "\n## 文档摘要\n\n"
        "| # | 源文档 | 子类 | 摘要 | 关键词/小节 | 状态 |\n"
        "| ---: | --- | --- | --- | --- | --- |\n"
    )
    # 2. 非 dry-run 时只经 bridge 创建和追加目标笔记。
    if not args.dry_run:
        run_bridge("create", target_path, header)

    chunk = ""
    chunk_rows = 0
    for row in rows:
        line = (
            f"| {row.index} | `{clean_cell(row.path, 150)}` | {clean_cell(row.subgroup, 80)} | "
            f"{row.summary} | {row.keywords} | {row.status} |\n"
        )
        if len(chunk) + len(line) > args.chunk_chars or chunk_rows >= args.chunk_rows:
            if not args.dry_run:
                run_bridge("append", target_path, chunk)
                if args.append_delay:
                    time.sleep(args.append_delay)
            chunk = ""
            chunk_rows = 0
        chunk += line
        chunk_rows += 1
    if chunk and not args.dry_run:
        run_bridge("append", target_path, chunk)
        if args.append_delay:
            time.sleep(args.append_delay)

    if errors and not args.dry_run:
        error_text = "\n## 读取失败\n\n" + "\n".join(
            f"- `{path}`: {clean_cell(error, 220)}" for path, error in errors
        )
        run_bridge("append", target_path, error_text)

    return BatchResult(
        folder=folder,
        title=title,
        target=target_path,
        files=len(paths),
        read=len(rows),
        errors=len(errors),
        seconds=round(time.time() - started, 1),
    )


def write_rollup(args: argparse.Namespace, results: list[BatchResult]) -> None:
    """生成全量逐篇沉淀总览并维护 INDEX 入口。

    [参数] args: 命令行参数；results: 各批次处理结果。
    [返回] 无。
    最近修改时间: 2026-07-13 17:32:38 总览和 INDEX 入口的目标写入统一复用 bridge。
    """
    # 1. 汇总批次统计并生成固定知识库前缀下的总览内容。
    total_files = sum(result.files for result in results)
    total_read = sum(result.read for result in results)
    total_errors = sum(result.errors for result in results)
    target_path = f"{args.target_prefix}/全量逐篇沉淀总览.md"
    content = f"""---
id: 20260707-blog-data-full-distill-rollup
type: moc
title: blog-data 全量逐篇沉淀总览
aliases:
  - F blog data 全量沉淀
  - blog-data 全量读取总结
  - data vault 全量逐篇沉淀
tags:
  - blog-data/distilled
  - obsidian/import
  - technical-knowledge
status: active
created: 2026-07-07
updated: 2026-07-07
source_sessions: []
source_refs:
  - F:/blog/data
related:
  - [[30-MOCs/blog-data-技术知识地图|blog-data 技术知识地图]]
  - [[50-Sources/vaults/blog-data-vault|F blog data Obsidian vault]]
entities:
  - Obsidian
topics:
  - 全量沉淀
  - 技术知识库
confidence: medium
---

# blog-data 全量逐篇沉淀总览

> [!NOTE]
> 本轮对源 vault `data` 的 Markdown 进行逐篇读取、摘要提取、主题归类和目标 vault 写入。敏感主题只沉淀通用线索，不摘录密钥、账号、token、私钥、助记词、服务器地址等原值。

## 执行概览

| 项目 | 值 |
| --- | --- |
| 源 vault | `data` |
| 源路径 | `F:/blog/data` |
| 目标 vault 根 | `D:/obsidian_data` |
| 知识路径前缀 | `知识库/` |
| 应处理 Markdown | {total_files} |
| 成功读取并沉淀 | {total_read} |
| 读取失败 | {total_errors} |
| 生成日期 | 2026-07-07 |

## 批次入口

| 批次 | 源目录 | 文档数 | 成功读取 | 失败 | 耗时秒 | 目标笔记 |
| --- | --- | ---: | ---: | ---: | ---: | --- |
"""
    for result in results:
        target_no_ext = result.target[:-3] if result.target.endswith(".md") else result.target
        content += (
            f"| {result.title} | `{result.folder}` | {result.files} | {result.read} | "
            f"{result.errors} | {result.seconds} | [[{target_no_ext}|{result.title}逐篇沉淀]] |\n"
        )
    content += """
## 使用方式

- 需要按主题找知识时，先从本页进入对应批次，再用表格里的源文档标题、摘要、小节关键词检索。
- 需要追溯原文时，到源 vault `data` 中按“源文档”路径读取。
- 钱包、服务器、备份、VPN、内网组网等高敏主题已经按脱敏策略处理：本轮只保存通用线索，不保存凭据原值。

## 关联

- [[30-MOCs/blog-data-技术知识地图|blog-data 技术知识地图]]
- [[50-Sources/vaults/blog-data-vault|F blog data Obsidian vault]]
"""
    if not args.dry_run:
        run_bridge("create", target_path, content)
        index_append = f"""

## blog-data 全量逐篇沉淀

- [[{args.target_prefix}/全量逐篇沉淀总览|blog-data 全量逐篇沉淀总览]]：逐篇读取并归类沉淀 `F:/blog/data` 的 Markdown。
"""
        index = run_bridge("read", "知识库/INDEX.md")
        if "blog-data 全量逐篇沉淀总览" not in index:
            run_bridge("append", "知识库/INDEX.md", index_append)


def parse_args() -> argparse.Namespace:
    """解析命令行参数。

    [参数] 无。
    [返回] 解析后的命令行参数。
    最近修改时间: 2026-07-13 17:32:38 删除已无效的 CLI、目标 vault 和超时 transport 参数。
    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-vault", default="data")
    parser.add_argument("--source-root", type=Path, default=Path(r"F:\blog\data"))
    parser.add_argument("--target-root", type=Path, default=Path(r"D:\obsidian_data"))
    parser.add_argument("--target-prefix", default="知识库/30-MOCs/blog-data")
    parser.add_argument("--include", nargs="*", default=None, help="top-level folders to process")
    parser.add_argument("--max-files", type=int, default=0, help="limit files per category for smoke tests")
    # bridge 会通过临时 UTF-8 文件传递正文；这里仍限制批次分块大小以控制单次写入。
    parser.add_argument("--chunk-chars", type=int, default=1800)
    parser.add_argument("--chunk-rows", type=int, default=2)
    parser.add_argument("--append-delay", type=float, default=0.05)
    parser.add_argument("--dry-run", action="store_true")
    return parser.parse_args()


def main() -> int:
    """按批次执行源 vault 逐篇沉淀。

    [参数] 无。
    [返回] 进程退出码。
    最近修改时间: 2026-07-13 17:32:38 入口改为 bridge doctor 与固定目标根校验。
    """
    # 1. 先校验 bridge、源目录和固定目标根，再开始本地源文件批处理。
    args = parse_args()
    validate_cli_and_vaults(args)
    source_root = args.source_root.resolve()
    files = iter_markdown_files(source_root)
    categories = build_category_index(files, source_root)
    if args.include:
        include = set(args.include)
        categories = {name: paths for name, paths in categories.items() if name in include}
    if args.max_files:
        categories = {name: paths[: args.max_files] for name, paths in categories.items()}
    # 2. 每个顶层目录独立沉淀，最后统一生成 rollup 和 INDEX 入口。
    results: list[BatchResult] = []
    for folder, paths in categories.items():
        result = process_category(args, source_root, folder, paths)
        results.append(result)
        print(
            f"DONE {result.title}: files={result.files} read={result.read} "
            f"errors={result.errors} seconds={result.seconds} target={result.target}",
            flush=True,
        )
    write_rollup(args, results)
    print(
        f"ROLLUP total_files={sum(r.files for r in results)} "
        f"total_read={sum(r.read for r in results)} total_errors={sum(r.errors for r in results)}",
        flush=True,
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
