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
    warning: str | None = None
    release_pending_summary: str | None = None
    release_progress_percent: int | None = None


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
    if not config_path.exists():
        raise FileNotFoundError(f"配置文件不存在：{config_path}")
    raw = config_path.read_text(encoding="utf-8")
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
    since = f"{start.isoformat()} 00:00:00"
    until = f"{(end - dt.timedelta(days=1)).isoformat()} 23:59:59"
    cmd = [
        "git",
        "-C",
        str(repo_path),
        "log",
        "--no-merges",
        "--reverse",
        f"--since={since}",
        f"--until={until}",
        "--pretty=format:%H%x09%ct%x09%s%x09%an%x09%ae",
    ]
    proc = subprocess.run(cmd, capture_output=True, text=True, check=False)
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
    values: list[str] = []
    for key in ("user.name", "user.email"):
        cmd = ["git", "config", "--global", key]
        proc = subprocess.run(cmd, capture_output=True, text=True, check=False)
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


def resolve_excluded_types(cfg: dict) -> set[str]:
    configured = normalize_str_list(cfg.get("excluded_types"))
    if configured:
        return {item.lower() for item in configured}
    return set(DEFAULT_EXCLUDED_TYPES)


def resolve_excluded_keywords(cfg: dict) -> list[str]:
    configured = normalize_str_list(cfg.get("excluded_keywords"))
    if configured:
        return [item.lower() for item in configured]
    return [item.lower() for item in DEFAULT_EXCLUDED_KEYWORDS]


def filter_commits_by_importance(
    commits: list[CommitEntry],
    excluded_types: set[str],
    excluded_keywords: list[str],
) -> list[CommitEntry]:
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


def summarize_project(
    project_name: str,
    project_path: str,
    commits: list[CommitEntry],
    timezone: ZoneInfo,
) -> ProjectResult:
    report_items: list[str] = []

    for item in commits:
        report_items.append(summarize_commit_subject(item.subject))

    return ProjectResult(
        name=project_name,
        path=project_path,
        report_items=report_items,
    )


def build_release_progress_summary_lines(period: str, cfg: dict, results: list[ProjectResult]) -> list[str]:
    scope = PERIOD_SCOPE_TEXT[period]
    summary_results = [
        item
        for item in results
        if item.warning
        or item.report_items
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
    period_name = REPORT_NAME_MAP[period]
    displayed_results = [item for item in results if item.warning or item.report_items]

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
    report_timezone = resolve_report_timezone()
    excluded_types = resolve_excluded_types(cfg)
    excluded_keywords = resolve_excluded_keywords(cfg)

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
                    warning=f"不是 Git 仓库: {project_path_raw}",
                    release_pending_summary=project_release_pending_summary,
                    release_progress_percent=project_release_progress_percent,
                )
            )
            continue

        try:
            commits = run_git_log(project_path, start, end)
            commits = filter_commits_by_author(commits, author_filters)
            commits = filter_commits_by_importance(commits, excluded_types, excluded_keywords)
            summary_result = summarize_project(project_name, project_path_raw, commits, report_timezone)
            summary_result.release_pending_summary = project_release_pending_summary
            summary_result.release_progress_percent = project_release_progress_percent
            results.append(summary_result)
        except Exception as exc:  # noqa: BLE001
            results.append(
                ProjectResult(
                    name=project_name,
                    path=project_path_raw,
                    report_items=[],
                    warning=f"统计失败: {exc}",
                    release_pending_summary=project_release_pending_summary,
                    release_progress_percent=project_release_progress_percent,
                )
            )

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
