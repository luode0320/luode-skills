#!/usr/bin/env python3
"""Generate daily/weekly/monthly/yearly reports from multiple git repositories."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from zoneinfo import ZoneInfo


WEEKDAY_CN = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"]
BEIJING_TZ_NAME = "Asia/Shanghai"
BEIJING_TZ = ZoneInfo(BEIJING_TZ_NAME)
DEFAULT_REPORT_OUTPUT_DIR = "/home/luode/code"
REPORT_NAME_MAP = {
    "daily": "日报",
    "weekly": "周报",
    "monthly": "月报",
    "yearly": "年报",
}
PERIOD_SCOPE_TEXT = {
    "daily": "今日",
    "weekly": "本周",
    "monthly": "本月",
    "yearly": "本年",
}
TYPE_LABELS = {
    "feat": "功能",
    "fix": "修复",
    "refactor": "重构",
    "docs": "文档",
    "test": "测试",
    "chore": "维护",
    "perf": "性能",
    "style": "样式",
    "build": "构建",
    "ci": "流水线",
    "revert": "回滚",
}
DEFAULT_EXCLUDED_TYPES = {"docs", "test", "build", "revert"}
DEFAULT_EXCLUDED_KEYWORDS = {
    "rename",
    "renaming",
    "重命名",
    "rollback",
    "roll back",
    "回滚",
    "文档",
    "docs",
    "测试",
    "test",
    "build",
    "构建",
}
DEFAULT_UNCOMMITTED_EXCLUDED_PATHS = {
    "dist/",
    "build/",
    "coverage/",
    "node_modules/",
}
DEFAULT_UNCOMMITTED_ANALYSIS_EXCLUDED_PATHS = {
    "doc/",
    "docs/",
    "design/",
    "designs/",
    "figma/",
    "mockup/",
    "prototype/",
    ".codegraph/",
}
DEFAULT_UNCOMMITTED_ANALYSIS_EXCLUDED_EXTENSIONS = {
    ".md",
    ".markdown",
    ".txt",
    ".pdf",
    ".doc",
    ".docx",
    ".ppt",
    ".pptx",
    ".xls",
    ".xlsx",
    ".fig",
    ".sketch",
    ".xd",
    ".drawio",
    ".png",
    ".jpg",
    ".jpeg",
    ".gif",
    ".webp",
    ".pid",
    ".lock",
    ".log",
}
MODULE_LABELS = {
    "app/buysell": "买卖币",
    "app/exchange": "兑换",
    "app/marketactivity": "市场活动",
    "app/system": "系统服务",
    "app/wallet": "钱包服务",
    "internal/controller": "接口层",
    "internal/router": "路由层",
    "internal/service": "服务层",
    "crontask": "定时任务",
    "cmd/migrate": "数据迁移",
    "frontend": "前端页面",
    "web": "前端页面",
}

@dataclass
class CommitEntry:
    commit_hash: str
    commit_ts: int
    subject: str
    author_name: str
    author_email: str


@dataclass
class ProjectResult:
    name: str
    path: str
    report_items: list[str]
    ongoing_items: list[str]
    warning: str | None = None
    release_pending_summary: str | None = None
    release_progress_percent: int | None = None


@dataclass
class WorktreeEntry:
    status: str
    path: str


def parse_args() -> argparse.Namespace:
    default_date = dt.datetime.now(BEIJING_TZ).date().isoformat()
    default_config = Path(__file__).resolve().parents[1] / "references" / "projects.json"
    parser = argparse.ArgumentParser(description="基于 Git 提交生成日报/周报/月报/年报。")
    parser.add_argument(
        "--period",
        choices=["daily", "weekly", "monthly", "yearly"],
        required=True,
        help="报告类型。",
    )
    parser.add_argument(
        "--date",
        default=default_date,
        help="基准日期，格式 YYYY-MM-DD。默认按北京时间今天。",
    )
    parser.add_argument(
        "--config",
        default=str(default_config),
        help="projects.json 配置路径。",
    )
    parser.add_argument(
        "--author",
        action="append",
        default=[],
        help="作者过滤关键字（可重复）。传入后覆盖配置文件中的 authors。",
    )
    return parser.parse_args()


def load_config(config_path: Path) -> dict:
    """
    [参数]
    - config_path: 配置文件路径。
    [返回]
    - dict: 解析后的工作报告配置对象。
    最近修改时间: 2026-07-03 19:20:00 兼容 Windows UTF-8 BOM 配置文件，避免本地生成的 JSON 读取失败。
    """
    # 1. 统一按 UTF-8-SIG 读取配置，兼容 Windows 下可能带 BOM 的 JSON 文件。
    if not config_path.exists():
        raise FileNotFoundError(f"配置文件不存在：{config_path}")
    raw = config_path.read_text(encoding="utf-8-sig")
    data = json.loads(raw)
    if not isinstance(data, dict):
        raise ValueError("配置根节点必须是对象。")
    projects = data.get("projects")
    if not isinstance(projects, list) or not projects:
        raise ValueError("配置必须包含非空的 projects 列表。")
    return data


def calc_range(period: str, ref_date: dt.date) -> tuple[dt.date, dt.date]:
    if period == "daily":
        start = ref_date
        end = start + dt.timedelta(days=1)
        return start, end

    if period == "weekly":
        start = ref_date - dt.timedelta(days=ref_date.weekday())
        end = start + dt.timedelta(days=7)
        return start, end

    if period == "monthly":
        start = ref_date.replace(day=1)
        if start.month == 12:
            end = dt.date(start.year + 1, 1, 1)
        else:
            end = dt.date(start.year, start.month + 1, 1)
        return start, end

    if period == "yearly":
        start = dt.date(ref_date.year, 1, 1)
        end = dt.date(ref_date.year + 1, 1, 1)
        return start, end

    raise ValueError(f"不支持的报告类型: {period}")


def format_day_with_weekday(day: dt.date) -> str:
    return f"{day.isoformat()} {WEEKDAY_CN[day.weekday()]}"


def format_period_label(period: str, start: dt.date, end: dt.date) -> str:
    end_inclusive = end - dt.timedelta(days=1)
    if period == "daily":
        return format_day_with_weekday(start)
    return f"{format_day_with_weekday(start)} - {format_day_with_weekday(end_inclusive)}"


def run_git_log(repo_path: Path, start: dt.date, end: dt.date) -> list[CommitEntry]:
    """
    [参数]
    - repo_path: Git 仓库路径。
    - start: 统计开始日期。
    - end: 统计结束日期（开区间）。
    [返回]
    - list[CommitEntry]: 指定时间范围内的提交列表。
    最近修改时间: 2026-07-03 19:20:00 统一 Git 子进程为 UTF-8 输出，避免 Windows 中文路径和中文提交解码失败。
    """
    # 1. 读取指定时间范围内的 Git 提交，并关闭路径转义保证中文内容可直接进入报告。
    since = f"{start.isoformat()} 00:00:00"
    until = f"{(end - dt.timedelta(days=1)).isoformat()} 23:59:59"
    cmd = [
        "git",
        "-c",
        "core.quotepath=false",
        "-C",
        str(repo_path),
        "log",
        "--no-merges",
        "--reverse",
        f"--since={since}",
        f"--until={until}",
        "--pretty=format:%H%x09%ct%x09%s%x09%an%x09%ae",
    ]
    proc = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace", check=False)
    if proc.returncode != 0:
        stderr = proc.stderr.strip()
        if "does not have any commits yet" in stderr:
            return []
        raise RuntimeError(stderr or "git 日志读取失败")

    commits: list[CommitEntry] = []
    for line in proc.stdout.splitlines():
        line = line.strip()
        if not line:
            continue
        parts = line.split("\t")
        if len(parts) != 5:
            continue
        try:
            commit_ts = int(parts[1])
        except ValueError:
            continue
        commits.append(
            CommitEntry(
                commit_hash=parts[0],
                commit_ts=commit_ts,
                subject=parts[2].strip(),
                author_name=parts[3].strip(),
                author_email=parts[4].strip(),
            )
        )
    return commits


def normalize_identity(value: str) -> str:
    return value.strip().lower()


def filter_commits_by_author(commits: list[CommitEntry], filters: list[str]) -> list[CommitEntry]:
    normalized_filters = {normalize_identity(item) for item in filters if item.strip()}
    if not normalized_filters:
        return []

    filtered: list[CommitEntry] = []
    for entry in commits:
        author_name = normalize_identity(entry.author_name)
        author_email = normalize_identity(entry.author_email)
        if author_name in normalized_filters or author_email in normalized_filters:
            filtered.append(entry)
    return filtered


def read_global_git_identity() -> list[str]:
    """
    [参数]
    - 无。
    [返回]
    - list[str]: 全局 Git 用户名和邮箱列表。
    最近修改时间: 2026-07-03 19:20:00 统一 Git 配置读取编码，避免 Windows 环境返回中文身份时解码异常。
    """
    # 1. 按 UTF-8 读取全局 Git 身份，作为作者过滤的最后兜底来源。
    values: list[str] = []
    for key in ("user.name", "user.email"):
        cmd = ["git", "config", "--global", key]
        proc = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace", check=False)
        if proc.returncode == 0:
            value = proc.stdout.strip()
            if value:
                values.append(value)
    return values


def resolve_author_filters(cli_filters: list[str], configured_authors: list[str]) -> list[str]:
    if cli_filters:
        return cli_filters

    cleaned = [str(item).strip() for item in configured_authors if str(item).strip()]
    if cleaned:
        return cleaned

    return read_global_git_identity()


def ensure_author_filters(author_filters: list[str]) -> list[str]:
    cleaned = [item.strip() for item in author_filters if item.strip()]
    if cleaned:
        return cleaned
    raise ValueError(
        "未获取到作者身份，无法保证只统计你的提交。请在 references/projects.json 的 authors 中配置姓名/邮箱，或传入 --author。"
    )


def resolve_report_timezone() -> ZoneInfo:
    return BEIJING_TZ


def configure_utf8_streams() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8")


def clean_subject(subject: str) -> str:
    return re.sub(r"\s+", " ", subject).strip()


def parse_commit_subject(subject: str) -> tuple[str | None, str]:
    text = clean_subject(subject)
    match = re.match(r"^([a-zA-Z]+)(\([^)]+\))?!?:\s*(.+)$", text)
    if not match:
        return None, text

    commit_type = match.group(1).lower()
    detail = match.group(3).strip()
    return commit_type, detail


def summarize_commit_subject(subject: str) -> str:
    commit_type, detail = parse_commit_subject(subject)
    if commit_type is None:
        return detail

    label = TYPE_LABELS.get(commit_type)
    if label:
        return f"{label}: {detail}"
    return clean_subject(subject)


def normalize_str_list(values: object) -> list[str]:
    if not isinstance(values, list):
        return []
    return [str(item).strip() for item in values if str(item).strip()]


def normalize_optional_text(value: object) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    return text or None


def normalize_optional_percent(value: object) -> int | None:
    """
    [参数]
    - value: 待归一化的百分比配置值。
    [返回]
    - int | None: 合法百分比或空值。
    最近修改时间: 2026-07-03 19:20:00 复用到未提交工作区配置解析，统一百分比边界处理。
    """
    # 1. 仅接受可转为整数的配置值，并统一裁剪到 0-100。
    if value is None:
        return None
    try:
        percent = int(str(value).strip())
    except (TypeError, ValueError):
        return None
    if percent < 0:
        return 0
    if percent > 100:
        return 100
    return percent


def normalize_optional_bool(value: object, default: bool) -> bool:
    """
    [参数]
    - value: 待归一化的布尔配置值。
    - default: 配置为空时使用的默认值。
    [返回]
    - bool: 归一化后的布尔结果。
    最近修改时间: 2026-07-03 19:20:00 新增布尔配置解析，支持是否统计未提交工作区事项。
    """
    # 1. 配置缺失时回退默认值，显式字符串或数字时按常见布尔语义解析。
    if value is None:
        return default
    if isinstance(value, bool):
        return value

    text = str(value).strip().lower()
    if text in {"1", "true", "yes", "on"}:
        return True
    if text in {"0", "false", "no", "off"}:
        return False
    return default


def resolve_excluded_types(cfg: dict) -> set[str]:
    configured = normalize_str_list(cfg.get("excluded_types"))
    if configured:
        return {item.lower() for item in configured}
    return set(DEFAULT_EXCLUDED_TYPES)


def resolve_excluded_keywords(cfg: dict) -> list[str]:
    """
    [参数]
    - cfg: 工作报告配置对象。
    [返回]
    - list[str]: 已提交事项过滤关键词列表。
    最近修改时间: 2026-07-03 19:20:00 与未提交工作区过滤配置并行，保留提交过滤逻辑独立解析。
    """
    # 1. 已配置时优先使用配置；否则回退到默认低价值关键词。
    configured = normalize_str_list(cfg.get("excluded_keywords"))
    if configured:
        return [item.lower() for item in configured]
    return [item.lower() for item in DEFAULT_EXCLUDED_KEYWORDS]


def resolve_include_uncommitted_changes(cfg: dict) -> bool:
    """
    [参数]
    - cfg: 工作报告配置对象。
    [返回]
    - bool: 是否启用未提交工作区事项补充。
    最近修改时间: 2026-07-03 19:20:00 新增工作区补充开关，支持按配置决定是否纳入进行中事项。
    """
    # 1. 默认开启工作区补充，只有配置明确关闭时才跳过。
    return normalize_optional_bool(cfg.get("include_uncommitted_changes"), True)


def resolve_uncommitted_excluded_keywords(cfg: dict) -> list[str]:
    """
    [参数]
    - cfg: 工作报告配置对象。
    [返回]
    - list[str]: 未提交工作区事项过滤关键词列表。
    最近修改时间: 2026-07-03 19:20:00 新增工作区过滤关键词，避免低价值改动进入周报进行中事项。
    """
    # 1. 已配置时优先使用工作区专用关键词；否则复用提交过滤关键词。
    configured = normalize_str_list(cfg.get("uncommitted_excluded_keywords"))
    if configured:
        return [item.lower() for item in configured]
    return resolve_excluded_keywords(cfg)


def resolve_uncommitted_excluded_paths(cfg: dict) -> list[str]:
    """
    [参数]
    - cfg: 工作报告配置对象。
    [返回]
    - list[str]: 未提交工作区路径过滤前缀列表。
    最近修改时间: 2026-07-03 19:20:00 新增工作区路径过滤，默认排除构建产物和依赖目录。
    """
    # 1. 已配置时优先使用配置；否则回退到默认低价值路径前缀。
    configured = normalize_str_list(cfg.get("uncommitted_excluded_paths"))
    if configured:
        return configured
    return list(DEFAULT_UNCOMMITTED_EXCLUDED_PATHS)


def resolve_uncommitted_max_paths(cfg: dict) -> int:
    """
    [参数]
    - cfg: 工作报告配置对象。
    [返回]
    - int: 单个项目未提交事项中最多展示的路径数量。
    最近修改时间: 2026-07-03 19:20:00 新增路径数量限制，避免进行中事项过长影响周报可读性。
    """
    # 1. 优先读取配置，并把异常值裁剪到合理范围。
    raw_value = cfg.get("uncommitted_max_paths")
    try:
        value = int(str(raw_value).strip()) if raw_value is not None else 5
    except (TypeError, ValueError):
        value = 5
    if value < 1:
        return 1
    if value > 20:
        return 20
    return value


def resolve_uncommitted_analysis_excluded_paths(cfg: dict) -> list[str]:
    """
    [参数]
    - cfg: 工作报告配置对象。
    [返回]
    - list[str]: 不参与未提交任务分析的目录前缀。
    最近修改时间: 2026-07-10 设计文件排除改为独立配置，避免设计材料成为进行中任务依据。
    """
    configured = normalize_str_list(cfg.get("uncommitted_analysis_excluded_paths"))
    if configured:
        return [item.replace("\\", "/").lower() for item in configured]
    return list(DEFAULT_UNCOMMITTED_ANALYSIS_EXCLUDED_PATHS)


def resolve_uncommitted_analysis_excluded_extensions(cfg: dict) -> list[str]:
    """
    [参数]
    - cfg: 工作报告配置对象。
    [返回]
    - list[str]: 不参与未提交任务分析的文件扩展名。
    最近修改时间: 2026-07-10 设计文件排除改为独立配置，避免文档和设计文件污染任务摘要。
    """
    configured = normalize_str_list(cfg.get("uncommitted_analysis_excluded_extensions"))
    extensions = configured or list(DEFAULT_UNCOMMITTED_ANALYSIS_EXCLUDED_EXTENSIONS)
    return [item.lower() if item.startswith(".") else f".{item.lower()}" for item in extensions]

def filter_commits_by_importance(
    commits: list[CommitEntry],
    excluded_types: set[str],
    excluded_keywords: list[str],
) -> list[CommitEntry]:
    """
    [参数]
    - commits: 待过滤的提交列表。
    - excluded_types: 需要排除的提交类型集合。
    - excluded_keywords: 需要排除的关键词列表。
    [返回]
    - list[CommitEntry]: 过滤后的提交列表。
    最近修改时间: 2026-07-03 19:20:00 继续保留已提交事项过滤，和未提交事项过滤形成并行入口。
    """
    # 1. 仅保留具有业务语义的提交，排除低价值提交噪音。
    if not commits:
        return commits

    filtered: list[CommitEntry] = []
    for entry in commits:
        commit_type, detail = parse_commit_subject(entry.subject)
        text = f"{entry.subject} {detail}".lower()

        if commit_type and commit_type in excluded_types:
            continue
        if any(keyword in text for keyword in excluded_keywords):
            continue
        filtered.append(entry)
    return filtered


def run_git_status_porcelain(repo_path: Path) -> list[WorktreeEntry]:
    """
    [参数]
    - repo_path: Git 仓库路径。
    [返回]
    - list[WorktreeEntry]: 当前工作区未提交改动列表。
    最近修改时间: 2026-07-03 19:20:00 新增工作区扫描，支持从未提交改动补充进行中事项。
    """
    # 1. 使用 porcelain 输出稳定读取工作区状态，并统一提取状态与路径。
    cmd = [
        "git",
        "-c",
        "core.quotepath=false",
        "-C",
        str(repo_path),
        "status",
        "--short",
        "--untracked-files=all",
    ]
    proc = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace", check=False)
    if proc.returncode != 0:
        stderr = proc.stderr.strip()
        raise RuntimeError(stderr or "git 工作区状态读取失败")

    entries: list[WorktreeEntry] = []
    for raw_line in proc.stdout.splitlines():
        line = raw_line.rstrip()
        if not line:
            continue

        status_code = line[:2]
        path_text = line[3:].strip()
        if " -> " in path_text:
            path_text = path_text.split(" -> ", 1)[1].strip()

        normalized_path = path_text.replace("\\", "/")
        if not normalized_path:
            continue

        entries.append(WorktreeEntry(status=status_code, path=normalized_path))
    return entries


def filter_worktree_entries_by_importance(
    entries: list[WorktreeEntry],
    excluded_keywords: list[str],
    excluded_paths: list[str],
) -> list[WorktreeEntry]:
    """
    [参数]
    - entries: 待过滤的工作区改动列表。
    - excluded_keywords: 需要排除的关键词列表。
    - excluded_paths: 需要排除的路径前缀列表。
    [返回]
    - list[WorktreeEntry]: 过滤后的工作区改动列表。
    最近修改时间: 2026-07-03 19:20:00 新增工作区低价值改动过滤，避免文档和构建噪音进入周报。
    """
    # 1. 同时按关键词和路径前缀过滤低价值工作区改动。
    filtered: list[WorktreeEntry] = []
    normalized_paths = [item.replace("\\", "/").lower() for item in excluded_paths]
    for entry in entries:
        path_text = entry.path.lower()
        if any(path_text.startswith(prefix) for prefix in normalized_paths):
            continue
        if any(keyword in path_text for keyword in excluded_keywords):
            continue
        filtered.append(entry)
    return filtered


def is_analysis_excluded_path(path: str, excluded_paths: list[str], excluded_extensions: list[str]) -> bool:
    """
    [参数]
    - path: 工作区改动相对路径。
    - excluded_paths: 设计和文档目录前缀。
    - excluded_extensions: 设计和文档文件扩展名。
    [返回]
    - bool: 是否排除该路径的任务语义分析。
    最近修改时间: 2026-07-10 明确禁止使用设计文件和文档文件生成进行中任务摘要。
    """
    normalized_path = path.replace("\\", "/").lower()
    file_suffix = Path(normalized_path).suffix
    return any(normalized_path.startswith(prefix) for prefix in excluded_paths) or file_suffix in excluded_extensions


def run_git_diff_head(repo_path: Path) -> str:
    """
    [参数]
    - repo_path: Git 仓库路径。
    [返回]
    - str: 当前 HEAD 到工作区的已跟踪文件差异。
    最近修改时间: 2026-07-10 新增 diff 读取，让进行中摘要基于真实代码变更内容。
    """
    cmd = ["git", "-C", str(repo_path), "diff", "HEAD", "--no-ext-diff", "--unified=0", "--"]
    proc = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace", check=False)
    if proc.returncode != 0:
        stderr = proc.stderr.strip()
        raise RuntimeError(stderr or "git 工作区差异读取失败")
    return proc.stdout


def read_untracked_code_lines(repo_path: Path, entries: list[WorktreeEntry], excluded_paths: list[str], excluded_extensions: list[str]) -> list[str]:
    """
    [参数]
    - repo_path: Git 仓库路径。
    - entries: 工作区未提交改动列表。
    - excluded_paths: 设计和文档目录前缀。
    - excluded_extensions: 设计和文档文件扩展名。
    [返回]
    - list[str]: 新增代码文件中的有限行内容。
    最近修改时间: 2026-07-10 支持从未跟踪代码文件补充 diff 语义，同时跳过设计和文档文件。
    """
    lines: list[str] = []
    for entry in entries:
        if "?" not in entry.status or is_analysis_excluded_path(entry.path, excluded_paths, excluded_extensions):
            continue
        file_path = repo_path / entry.path
        try:
            raw = file_path.read_bytes()
        except OSError:
            continue
        if b"\x00" in raw or len(raw) > 256 * 1024:
            continue
        lines.extend(raw.decode("utf-8", errors="replace").splitlines()[:400])
    return lines


def collect_changed_code_lines(diff_text: str, excluded_paths: list[str], excluded_extensions: list[str]) -> list[str]:
    """
    [参数]
    - diff_text: Git diff 文本。
    - excluded_paths: 设计和文档目录前缀。
    - excluded_extensions: 设计和文档文件扩展名。
    [返回]
    - list[str]: 已跟踪代码文件的新增和删除行。
    最近修改时间: 2026-07-10 只保留代码文件 diff，排除设计文件和纯上下文行。
    """
    changed_lines: list[str] = []
    current_path = ""
    for raw_line in diff_text.splitlines():
        if raw_line.startswith("diff --git a/"):
            match = re.match(r"diff --git a/(.+) b/(.+)$", raw_line)
            current_path = match.group(2) if match else ""
            continue
        if not current_path or is_analysis_excluded_path(current_path, excluded_paths, excluded_extensions):
            continue
        if raw_line.startswith(("+++", "---", "@@")):
            continue
        if raw_line.startswith(("+", "-")):
            changed_lines.append(raw_line[1:].strip())
    return changed_lines

def infer_module_label(paths: list[str], project_name: str) -> str:
    """
    [参数]
    - paths: 参与分析的代码路径。
    - project_name: 项目名称。
    [返回]
    - str: 从代码路径推导出的模块名称。
    最近修改时间: 2026-07-10 用代码目录推导任务范围，不再依赖设计文件名。
    """
    normalized_paths = [path.replace("\\", "/").lower() for path in paths]
    for module_prefix, label in MODULE_LABELS.items():
        if any(path.startswith(module_prefix) for path in normalized_paths):
            return label
    return project_name


def extract_diff_signals(lines: list[str]) -> list[str]:
    """
    [参数]
    - lines: 代码 diff 的新增和删除行。
    [返回]
    - list[str]: 可用于任务摘要的变更语义片段。
    最近修改时间: 2026-07-10 从代码变更中的中文业务词和标记提取任务线索。
    """
    signals: list[str] = []
    seen: set[str] = set()
    for line in lines:
        if not line or line.startswith(("//", "/*", "*", "#")):
            continue
        candidates = re.findall(r"\[[^\]\n]{2,30}\]|[\u4e00-\u9fff]{4,}", line)
        for candidate in candidates:
            cleaned = candidate.strip("[]，。；：:、 \\\"'")
            if len(cleaned) < 2 or not re.search(r"[\u4e00-\u9fff]", cleaned) or cleaned in seen:
                continue
            seen.add(cleaned)
            signals.append(cleaned)
            if len(signals) >= 3:
                return signals
    return signals


def summarize_code_worktree_changes(
    project_name: str,
    repo_path: Path,
    entries: list[WorktreeEntry],
    max_paths: int,
    excluded_paths: list[str],
    excluded_extensions: list[str],
) -> list[str]:
    """
    [参数]
    - project_name: 项目名称。
    - repo_path: Git 仓库路径。
    - entries: 过滤后的工作区改动列表。
    - max_paths: 最多展示的路径数量。
    - excluded_paths: 设计和文档目录前缀。
    - excluded_extensions: 设计和文档文件扩展名。
    [返回]
    - list[str]: 基于代码 diff 的进行中任务摘要。
    最近修改时间: 2026-07-10 以代码 diff 为主要证据生成进行中任务，设计文件不参与分析。
    """
    code_entries = [entry for entry in entries if not is_analysis_excluded_path(entry.path, excluded_paths, excluded_extensions)]
    if not code_entries:
        return []

    diff_lines = collect_changed_code_lines(run_git_diff_head(repo_path), excluded_paths, excluded_extensions)
    diff_lines.extend(read_untracked_code_lines(repo_path, code_entries, excluded_paths, excluded_extensions))
    paths = [entry.path for entry in code_entries]
    module = infer_module_label(paths, project_name)
    signals = extract_diff_signals(diff_lines)
    displayed_paths = list(dict.fromkeys(paths))[:max_paths]
    path_text = "、".join(displayed_paths)
    if len(set(paths)) > len(displayed_paths):
        path_text = f"{path_text} 等 {len(set(paths))} 处"

    if signals:
        signal_text = "、".join(signals[:2])
        return [f"进行中: 正在推进{module}相关开发，代码变更集中在{signal_text}，涉及 {path_text}"]
    return [f"进行中: 正在推进{module}相关开发，主要改动文件为 {path_text}"]

def build_worktree_path_summary(entries: list[WorktreeEntry], max_paths: int) -> str:
    """
    [参数]
    - entries: 过滤后的工作区改动列表。
    - max_paths: 最多展示的路径数量。
    [返回]
    - str: 基于路径和状态统计生成的兜底摘要。
    最近修改时间: 2026-07-03 20:05:00 拆出路径兜底摘要，供任务名提取失败时回退使用。
    """
    # 1. 先按状态统计工作区改动数量，避免只给路径列表看不出当前进展形态。
    modified_count = 0
    added_count = 0
    deleted_count = 0
    renamed_count = 0
    other_count = 0
    unique_paths: list[str] = []
    seen_paths: set[str] = set()

    for entry in entries:
        status_text = entry.status.replace(" ", "")
        if "M" in status_text:
            modified_count += 1
        elif "A" in status_text or "?" in status_text:
            added_count += 1
        elif "D" in status_text:
            deleted_count += 1
        elif "R" in status_text or "C" in status_text:
            renamed_count += 1
        else:
            other_count += 1

        if entry.path not in seen_paths:
            seen_paths.add(entry.path)
            unique_paths.append(entry.path)

    # 2. 再限制路径展示数量，保持周报可读性，同时保留总数提示。
    displayed_paths = unique_paths[:max_paths]
    path_suffix = "、".join(displayed_paths)
    if len(unique_paths) > len(displayed_paths):
        path_suffix = f"{path_suffix} 等 {len(unique_paths)} 处"

    segments: list[str] = []
    if modified_count:
        segments.append(f"修改 {modified_count} 项")
    if added_count:
        segments.append(f"新增 {added_count} 项")
    if deleted_count:
        segments.append(f"删除 {deleted_count} 项")
    if renamed_count:
        segments.append(f"重命名 {renamed_count} 项")
    if other_count:
        segments.append(f"其他 {other_count} 项")

    summary = " / ".join(segments) if segments else f"{len(unique_paths)} 项"
    return f"工作区仍有未提交改动（{summary}），涉及 {path_suffix}"


def summarize_worktree_changes(
    project_name: str,
    repo_path: Path,
    entries: list[WorktreeEntry],
    max_paths: int,
    analysis_excluded_paths: list[str],
    analysis_excluded_extensions: list[str],
) -> list[str]:
    """
    [参数]
    - project_name: 项目名称。
    - repo_path: Git 仓库路径。
    - entries: 过滤后的工作区改动列表。
    - max_paths: 最多展示的路径数量。
    - analysis_excluded_paths: 不参与任务分析的目录前缀。
    - analysis_excluded_extensions: 不参与任务分析的文件扩展名。
    [返回]
    - list[str]: 可直接写入报告的进行中事项列表。
    最近修改时间: 2026-07-10 优先使用代码 diff，分析失败时才回退到代码路径摘要。
    """
    if not entries:
        return []
    code_summary = summarize_code_worktree_changes(
        project_name,
        repo_path,
        entries,
        max_paths,
        analysis_excluded_paths,
        analysis_excluded_extensions,
    )
    if code_summary:
        return code_summary

    code_entries = [entry for entry in entries if not is_analysis_excluded_path(entry.path, analysis_excluded_paths, analysis_excluded_extensions)]
    if not code_entries:
        return []
    return [f"进行中: {build_worktree_path_summary(code_entries, max_paths)}"]

def summarize_project(
    project_name: str,
    project_path: str,
    commits: list[CommitEntry],
    ongoing_items: list[str],
) -> ProjectResult:
    """
    [参数]
    - project_name: 项目中文名称。
    - project_path: 项目路径。
    - commits: 已过滤的提交列表。
    - ongoing_items: 已整理的进行中事项列表。
    [返回]
    - ProjectResult: 单个项目的报告结果。
    最近修改时间: 2026-07-03 19:20:00 项目汇总新增进行中事项字段，支持已提交与未提交并存输出。
    """
    # 1. 先把已提交事项转成报告条目，再合并工作区进行中事项。
    report_items: list[str] = []

    for item in commits:
        report_items.append(summarize_commit_subject(item.subject))

    return ProjectResult(
        name=project_name,
        path=project_path,
        report_items=report_items,
        ongoing_items=ongoing_items,
    )


def build_release_progress_summary_lines(period: str, cfg: dict, results: list[ProjectResult]) -> list[str]:
    """
    [参数]
    - period: 报告周期类型。
    - cfg: 工作报告配置对象。
    - results: 项目统计结果列表。
    [返回]
    - list[str]: 总体归纳统计区块行列表。
    最近修改时间: 2026-07-03 19:20:00 总体归纳统计兼容进行中事项，避免无提交但有在做项目被遗漏。
    """
    # 1. 总体归纳统计同时考虑警告、已提交事项和进行中事项。
    scope = PERIOD_SCOPE_TEXT[period]
    summary_results = [
        item
        for item in results
        if item.warning
        or item.report_items
        or item.ongoing_items
        or item.release_pending_summary
        or item.release_progress_percent is not None
    ]
    if not summary_results:
        return ["当前开发待发布版本总体进度:", "本周期无提交记录"]

    overall_percent = normalize_optional_percent(cfg.get("release_overall_progress_percent"))
    if overall_percent is None:
        percents = [item.release_progress_percent for item in summary_results if item.release_progress_percent is not None]
        if percents:
            overall_percent = round(sum(percents) / len(percents))

    if overall_percent is None:
        lines: list[str] = ["当前开发待发布版本总体进度:"]
    else:
        lines = [f"当前开发待发布版本总体进度({overall_percent}%):"]

    for item in summary_results:
        if item.release_pending_summary:
            pending = item.release_pending_summary
        elif item.warning:
            pending = f"{scope}统计异常（{item.warning}）"
        else:
            pending = "待补充未完成事项"

        if item.release_progress_percent is None:
            lines.append(f"{item.name}: {pending} -> 项目完成度: 未配置")
            continue
        lines.append(f"{item.name}: {pending} -> 项目完成度: {item.release_progress_percent}%")

    return lines


def render_report(period: str, period_label: str, results: list[ProjectResult], cfg: dict) -> str:
    """
    [参数]
    - period: 报告周期类型。
    - period_label: 已格式化的日期范围标签。
    - results: 项目统计结果列表。
    - cfg: 工作报告配置对象。
    [返回]
    - str: 最终报告正文。
    最近修改时间: 2026-07-03 19:20:00 渲染层新增进行中事项输出，并保持已提交与未提交来源可区分。
    """
    # 1. 只展示真正有警告、已提交事项或进行中事项的项目。
    period_name = REPORT_NAME_MAP[period]
    displayed_results = [item for item in results if item.warning or item.report_items or item.ongoing_items]

    lines: list[str] = [f"{period_name}（{period_label}）"]
    if period != "daily":
        lines.append("")
        lines.append("总体归纳统计:")
        lines.extend(build_release_progress_summary_lines(period, cfg, results))

    lines.append("")
    lines.append("各项目明细:")
    if not displayed_results:
        lines.append("")
        lines.append("本周期无提交记录")
        return "\n".join(lines)

    for result in displayed_results:
        lines.append("")
        lines.append(f"{result.name}:")
        lines.append("报告内容点:")
        if result.warning:
            lines.append(f"- {result.warning}")
            continue

        for item in result.report_items:
            lines.append(f"- {item}")
        for item in result.ongoing_items:
            lines.append(f"- {item}")

    return "\n".join(lines).rstrip()


def resolve_report_output_dir(cfg: dict) -> Path:
    raw = str(cfg.get("report_output_dir") or DEFAULT_REPORT_OUTPUT_DIR).strip()
    return Path(raw).expanduser()


def build_report_filename(period: str) -> str:
    timestamp = dt.datetime.now(BEIJING_TZ).strftime("%Y%m%d%H%M%S")
    return f"{REPORT_NAME_MAP[period]}-{timestamp}"


def save_report_file(report_text: str, output_dir: Path, period: str) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    file_path = output_dir / build_report_filename(period)
    file_path.write_text(report_text, encoding="utf-8")
    return file_path


def main() -> int:
    """
    [参数]
    - 无。
    [返回]
    - int: 进程退出码，0 表示成功。
    最近修改时间: 2026-07-03 19:20:00 主流程新增未提交工作区扫描，并把进行中事项补进各项目周报。
    """
    # 1. 先解析参数、配置和统计周期，再准备作者与过滤配置。
    configure_utf8_streams()
    args = parse_args()

    try:
        ref_date = dt.date.fromisoformat(args.date)
    except ValueError:
        print(f"--date 参数无效：{args.date}，期望格式 YYYY-MM-DD。", file=sys.stderr)
        return 1

    config_path = Path(args.config).expanduser().resolve()
    try:
        cfg = load_config(config_path)
    except Exception as exc:  # noqa: BLE001
        print(f"读取配置失败：{exc}", file=sys.stderr)
        return 1

    start, end = calc_range(args.period, ref_date)
    period_label = format_period_label(args.period, start, end)

    configured_authors = cfg.get("authors") if isinstance(cfg.get("authors"), list) else []
    try:
        author_filters = ensure_author_filters(resolve_author_filters(args.author, configured_authors))
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 1
    excluded_types = resolve_excluded_types(cfg)
    excluded_keywords = resolve_excluded_keywords(cfg)
    include_uncommitted_changes = resolve_include_uncommitted_changes(cfg)
    uncommitted_excluded_keywords = resolve_uncommitted_excluded_keywords(cfg)
    uncommitted_excluded_paths = resolve_uncommitted_excluded_paths(cfg)
    uncommitted_max_paths = resolve_uncommitted_max_paths(cfg)
    uncommitted_analysis_excluded_paths = resolve_uncommitted_analysis_excluded_paths(cfg)
    uncommitted_analysis_excluded_extensions = resolve_uncommitted_analysis_excluded_extensions(cfg)

    results: list[ProjectResult] = []
    for project in cfg["projects"]:
        project_name = str(project.get("name", "未命名项目")).strip() or "未命名项目"
        project_path_raw = str(project.get("path", "")).strip()
        project_path = Path(project_path_raw).expanduser()
        project_release_pending_summary = normalize_optional_text(project.get("release_pending_summary"))
        project_release_progress_percent = normalize_optional_percent(project.get("release_progress_percent"))

        if not project_path_raw:
            results.append(
                ProjectResult(
                    name=project_name,
                    path=project_path_raw,
                    report_items=[],
                    ongoing_items=[],
                    warning="项目路径为空，无法统计",
                    release_pending_summary=project_release_pending_summary,
                    release_progress_percent=project_release_progress_percent,
                )
            )
            continue

        if not project_path.exists():
            results.append(
                ProjectResult(
                    name=project_name,
                    path=project_path_raw,
                    report_items=[],
                    ongoing_items=[],
                    warning=f"项目路径不存在: {project_path_raw}",
                    release_pending_summary=project_release_pending_summary,
                    release_progress_percent=project_release_progress_percent,
                )
            )
            continue

        if not (project_path / ".git").exists():
            results.append(
                ProjectResult(
                    name=project_name,
                    path=project_path_raw,
                    report_items=[],
                    ongoing_items=[],
                    warning=f"不是 Git 仓库: {project_path_raw}",
                    release_pending_summary=project_release_pending_summary,
                    release_progress_percent=project_release_progress_percent,
                )
            )
            continue

        # 2. 对每个项目先统计已提交事项，再按配置补充未提交进行中事项。
        try:
            commits = run_git_log(project_path, start, end)
            commits = filter_commits_by_author(commits, author_filters)
            commits = filter_commits_by_importance(commits, excluded_types, excluded_keywords)
            ongoing_items: list[str] = []
            if include_uncommitted_changes:
                worktree_entries = run_git_status_porcelain(project_path)
                worktree_entries = filter_worktree_entries_by_importance(
                    worktree_entries,
                    uncommitted_excluded_keywords,
                    uncommitted_excluded_paths,
                )
                ongoing_items = summarize_worktree_changes(
                    project_name,
                    project_path,
                    worktree_entries,
                    uncommitted_max_paths,
                    uncommitted_analysis_excluded_paths,
                    uncommitted_analysis_excluded_extensions,
                )

            summary_result = summarize_project(project_name, project_path_raw, commits, ongoing_items)
            summary_result.release_pending_summary = project_release_pending_summary
            summary_result.release_progress_percent = project_release_progress_percent
            results.append(summary_result)
        except Exception as exc:  # noqa: BLE001
            results.append(
                ProjectResult(
                    name=project_name,
                    path=project_path_raw,
                    report_items=[],
                    ongoing_items=[],
                    warning=f"统计失败: {exc}",
                    release_pending_summary=project_release_pending_summary,
                    release_progress_percent=project_release_progress_percent,
                )
            )

    # 3. 生成报告正文并保存到目标目录，确保控制台输出与文件内容保持一致。
    report_text = render_report(args.period, period_label, results, cfg)
    output_dir = resolve_report_output_dir(cfg)
    try:
        saved_path = save_report_file(report_text, output_dir, args.period)
    except Exception as exc:  # noqa: BLE001
        print(f"保存报告失败：{exc}", file=sys.stderr)
        return 1

    print(report_text)
    print(f"\n报告已保存：{saved_path}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
