#!/usr/bin/env python3
"""Distill every Markdown note from one Obsidian vault into a target vault.

The source vault is read from the filesystem after the Obsidian CLI proves the
vault is registered. Target notes are written only through the Obsidian CLI.
"""

from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
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


def run_cli(cli: Path, args: list[str], timeout: int, retries: int = 1) -> str:
    """执行 Obsidian CLI 并返回标准输出。

    [参数] cli: Obsidian CLI 可执行文件路径；args: CLI 参数；timeout: 超时秒数；retries: 失败重试次数。
    [返回] CLI 标准输出文本。
    最近修改时间: 2026-07-07 为新增脚本补齐 CLI 调用说明。
    """
    command = [str(cli), *args]
    last_error = ""
    for attempt in range(retries + 1):
        try:
            completed = subprocess.run(
                command,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=timeout,
                check=False,
            )
        except subprocess.TimeoutExpired:
            last_error = f"timeout after {timeout}s"
        else:
            if completed.returncode == 0:
                return completed.stdout.strip()
            last_error = completed.stderr.strip() or completed.stdout.strip()
        if attempt < retries:
            time.sleep(1.0 + attempt)
    raise RuntimeError(f"CLI failed: {' '.join(command)} :: {last_error}")


def to_cli_content(text: str) -> str:
    """把多行 Markdown 转成 CLI content 参数可接受的文本。

    [参数] text: 待写入的 Markdown 正文。
    [返回] 将换行规整为字面量换行标记后的文本。
    最近修改时间: 2026-07-07 为新增脚本补齐内容转换说明。
    """
    return text.replace("\r\n", "\n").replace("\r", "\n").replace("\n", r"\n")


def parse_vaults_verbose(output: str) -> dict[str, str]:
    """解析 `obsidian vaults verbose` 输出。

    [参数] output: Obsidian CLI 返回的 vault 列表文本。
    [返回] vault 名称到 vault 根目录的映射。
    最近修改时间: 2026-07-07 为新增脚本补齐 vault 列表解析说明。
    """
    vaults: dict[str, str] = {}
    for line in output.splitlines():
        line = line.strip()
        if not line:
            continue
        if "\t" in line:
            name, path = line.split("\t", 1)
        else:
            parts = line.split(None, 1)
            if len(parts) != 2:
                continue
            name, path = parts
        vaults[name.strip()] = path.strip()
    return vaults


def comparable_path(path: str | Path) -> str:
    """生成用于比较的规整绝对路径。

    [参数] path: 需要比较的文件系统路径。
    [返回] 去除尾部分隔符并忽略大小写差异的绝对路径文本。
    最近修改时间: 2026-07-07 校验 CLI 注册路径与用户传入 root 是否一致。
    """
    return str(Path(path).expanduser().resolve()).rstrip("\\/").casefold()


def assert_registered_root(
    vaults: dict[str, str],
    vault_name: str,
    expected_root: Path,
    role: str,
) -> None:
    """确认 CLI 注册的 vault 路径与脚本入参一致。

    [参数] vaults: CLI 返回的 vault 映射；vault_name: 待检查的 vault 名；expected_root: 期望根目录；role: 错误信息中的角色名。
    [返回] 无；不一致时抛出 RuntimeError。
    最近修改时间: 2026-07-07 防止读写路径与已注册 vault 不一致。
    """
    registered_root = vaults[vault_name]
    if comparable_path(registered_root) != comparable_path(expected_root):
        raise RuntimeError(
            f"{role} vault root mismatch: vault={vault_name} "
            f"registered={registered_root} expected={expected_root}"
        )


def validate_cli_and_vaults(args: argparse.Namespace) -> dict[str, str]:
    """校验 Obsidian CLI、源 vault 和目标 vault 的注册状态。

    [参数] args: 命令行参数。
    [返回] CLI 认识的 vault 名称到根目录的映射。
    最近修改时间: 2026-07-07 增加注册路径与入参 root 一致性校验。
    """
    version = run_cli(args.cli, ["version"], args.cli_timeout, retries=1)
    vaults = parse_vaults_verbose(
        run_cli(args.cli, ["vaults", "verbose"], args.cli_timeout, retries=1)
    )
    if args.source_vault not in vaults:
        raise RuntimeError(f"source vault not registered: {args.source_vault}")
    if args.target_vault not in vaults:
        raise RuntimeError(f"target vault not registered: {args.target_vault}")
    source_root = Path(args.source_root).resolve()
    target_root = Path(args.target_root).resolve()
    if not source_root.exists() or not source_root.is_dir():
        raise RuntimeError(f"source root is not a directory: {source_root}")
    if not target_root.exists() or not target_root.is_dir():
        raise RuntimeError(f"target root is not a directory: {target_root}")
    assert_registered_root(vaults, args.source_vault, source_root, "source")
    assert_registered_root(vaults, args.target_vault, target_root, "target")
    print(f"obsidian_version={version}")
    print(f"source_vault={args.source_vault} path={vaults[args.source_vault]}")
    print(f"target_vault={args.target_vault} path={vaults[args.target_vault]}")
    return vaults


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


def create_or_overwrite_note(
    cli: Path,
    target_vault: str,
    path: str,
    content: str,
    timeout: int,
) -> None:
    """通过 Obsidian CLI 创建或覆盖目标笔记。

    [参数] cli: CLI 路径；target_vault: 目标 vault 名；path: 目标相对路径；content: Markdown 内容；timeout: 超时秒数。
    [返回] 无。
    最近修改时间: 2026-07-07 为新增脚本补齐目标笔记写入说明。
    """
    run_cli(
        cli,
        [
            f"vault={target_vault}",
            "create",
            f"path={path}",
            "content=" + to_cli_content(content),
            "overwrite",
        ],
        timeout,
        retries=1,
    )


def append_note(cli: Path, target_vault: str, path: str, content: str, timeout: int) -> None:
    """通过 Obsidian CLI 追加目标笔记内容。

    [参数] cli: CLI 路径；target_vault: 目标 vault 名；path: 目标相对路径；content: 待追加文本；timeout: 超时秒数。
    [返回] 无。
    最近修改时间: 2026-07-07 为新增脚本补齐分块追加说明。
    """
    if not content:
        return
    run_cli(
        cli,
        [
            f"vault={target_vault}",
            "append",
            f"path={path}",
            "content=" + to_cli_content(content),
        ],
        timeout,
        retries=1,
    )


def process_category(
    args: argparse.Namespace,
    source_root: Path,
    folder: str,
    paths: list[Path],
) -> BatchResult:
    """处理一个顶层目录批次并生成逐篇沉淀笔记。

    [参数] args: 命令行参数；source_root: 源 vault 根目录；folder: 顶层目录名；paths: 本批次文件列表。
    [返回] 本批次处理结果。
    最近修改时间: 2026-07-07 为新增脚本补齐批次处理说明。
    """
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
    if not args.dry_run:
        create_or_overwrite_note(args.cli, args.target_vault, target_path, header, args.cli_timeout)

    chunk = ""
    chunk_rows = 0
    for row in rows:
        line = (
            f"| {row.index} | `{clean_cell(row.path, 150)}` | {clean_cell(row.subgroup, 80)} | "
            f"{row.summary} | {row.keywords} | {row.status} |\n"
        )
        if len(chunk) + len(line) > args.chunk_chars or chunk_rows >= args.chunk_rows:
            if not args.dry_run:
                append_note(args.cli, args.target_vault, target_path, chunk, args.cli_timeout)
                if args.append_delay:
                    time.sleep(args.append_delay)
            chunk = ""
            chunk_rows = 0
        chunk += line
        chunk_rows += 1
    if chunk and not args.dry_run:
        append_note(args.cli, args.target_vault, target_path, chunk, args.cli_timeout)
        if args.append_delay:
            time.sleep(args.append_delay)

    if errors and not args.dry_run:
        error_text = "\n## 读取失败\n\n" + "\n".join(
            f"- `{path}`: {clean_cell(error, 220)}" for path, error in errors
        )
        append_note(args.cli, args.target_vault, target_path, error_text, args.cli_timeout)

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
    最近修改时间: 2026-07-07 为新增脚本补齐总览写入说明。
    """
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
| 目标 vault | `知识库` |
| 目标路径 | `D:/obsidian_data/知识库` |
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
        create_or_overwrite_note(args.cli, args.target_vault, target_path, content, args.cli_timeout)
        index_append = f"""

## blog-data 全量逐篇沉淀

- [[{args.target_prefix}/全量逐篇沉淀总览|blog-data 全量逐篇沉淀总览]]：逐篇读取并归类沉淀 `F:/blog/data` 的 Markdown。
"""
        index = run_cli(args.cli, [f"vault={args.target_vault}", "read", "path=INDEX.md"], args.cli_timeout, retries=1)
        if "blog-data 全量逐篇沉淀总览" not in index:
            append_note(args.cli, args.target_vault, "INDEX.md", index_append, args.cli_timeout)


def parse_args() -> argparse.Namespace:
    """解析命令行参数。

    [参数] 无。
    [返回] 解析后的命令行参数。
    最近修改时间: 2026-07-07 为新增脚本补齐参数入口说明。
    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cli", type=Path, default=Path(r"C:\Users\luode\AppData\Local\Programs\Obsidian\Obsidian.com"))
    parser.add_argument("--source-vault", default="data")
    parser.add_argument("--target-vault", default="知识库")
    parser.add_argument("--source-root", type=Path, default=Path(r"F:\blog\data"))
    parser.add_argument("--target-root", type=Path, default=Path(r"D:\obsidian_data\知识库"))
    parser.add_argument("--target-prefix", default="30-MOCs/blog-data")
    parser.add_argument("--include", nargs="*", default=None, help="top-level folders to process")
    parser.add_argument("--max-files", type=int, default=0, help="limit files per category for smoke tests")
    # Obsidian CLI is sensitive to long command-line payloads, so keep appends small.
    parser.add_argument("--chunk-chars", type=int, default=1800)
    parser.add_argument("--chunk-rows", type=int, default=2)
    parser.add_argument("--cli-timeout", type=int, default=90)
    parser.add_argument("--append-delay", type=float, default=0.05)
    parser.add_argument("--dry-run", action="store_true")
    return parser.parse_args()


def main() -> int:
    """按批次执行源 vault 逐篇沉淀。

    [参数] 无。
    [返回] 进程退出码。
    最近修改时间: 2026-07-07 增加 CLI 注册路径一致性校验后的主流程说明。
    """
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
