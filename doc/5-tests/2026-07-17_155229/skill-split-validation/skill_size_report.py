#!/usr/bin/env python3
"""统计正式 skill 注册清单的文件体积、文本包和预算等级。"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


EXPECTED_REGISTERED_SKILL_COUNT = 84
REGISTRY_ENTRY_PATTERN = re.compile(r"^\s+\* \*\*[^`]*`([^`]+)`（(?:已实现|规划中)）\*\*$")
THRESHOLDS = {
    "skill_md": {
        "normal_max_bytes": 16_000,
        "review_max_bytes": 20_000,
        "hard_warning_bytes": 24_000,
    },
    "reference": {
        "normal_max_bytes": 12_000,
        "review_max_bytes": 16_000,
    },
    "default_text": {
        "normal_max_bytes": 48_000,
        "hard_warning_bytes": 64_000,
    },
}


# [参数] 无。
# [返回] Path：当前统计脚本所在仓库根目录。
# 最近修改时间：2026-07-17 16:01:31 + 默认测试脚本从当前测试镜像目录定位仓库根目录。
def default_root() -> Path:
    """按当前测试资产的固定目录层级推导仓库根目录。"""
    return Path(__file__).resolve().parents[4]


# [参数] path: 需要读取的 UTF-8 文件路径。
# [返回] int：文件原始字节数。
# 最近修改时间：2026-07-17 16:01:31 + 统计原始字节数并同时校验文本编码。
def read_utf8_bytes(path: Path) -> int:
    """读取文件原始字节并验证其可以按 UTF-8 解码。"""
    # 1. 先读取原始字节，保证统计值不受换行转换影响。
    data = path.read_bytes()
    data.decode("utf-8")
    return len(data)


# [参数] registry_path: 根目录正式 skill 字典路径。
# [返回] list[str]：主规划域中的 skill 目录名，保持字典顺序。
# 最近修改时间：2026-07-17 16:01:31 + 从主规划域提取 84 个正式注册 skill 并排除扩展种子。
def parse_registered_skills(registry_path: Path) -> list[str]:
    """从字典主规划域提取正式注册 skill，遇到扩展种子域即停止。"""
    # 1. 读取字典并只解析扩展种子标题之前的技能条目。
    text = registry_path.read_text(encoding="utf-8")
    names: list[str] = []
    for line in text.splitlines():
        if line.startswith("* **11."):
            break
        match = REGISTRY_ENTRY_PATTERN.match(line)
        if match:
            names.append(match.group(1))

    # 2. 先检查数量和唯一性，再把缺失的正式目录交给后续扫描失败处理。
    if len(names) != EXPECTED_REGISTERED_SKILL_COUNT:
        raise ValueError(
            f"正式字典主规划 skill 数量为 {len(names)}，预期 {EXPECTED_REGISTERED_SKILL_COUNT}"
        )
    if len(set(names)) != len(names):
        raise ValueError("正式字典主规划存在重复 skill 名称")
    return names


# [参数] root: 仓库根目录。
# [返回] list[Path]：仓库根目录下直接带 SKILL.md 的目录，按名称排序。
# 最近修改时间：2026-07-17 16:01:31 + 盘点正式仓库目录与扩展种子目录的实际数量。
def iter_disk_skill_directories(root: Path) -> list[Path]:
    """盘点仓库根目录下实际存在的 skill 目录。"""
    # 1. 只扫描根目录直接子目录，避免把 references 或测试 fixture 误判为 skill。
    return sorted(
        (
            path
            for path in root.iterdir()
            if path.is_dir() and (path / "SKILL.md").is_file()
        ),
        key=lambda path: path.name,
    )


# [参数] skill_dir: 单个 skill 目录。
# [返回] list[tuple[str, int]]：reference 相对路径与原始字节数。
# 最近修改时间：2026-07-17 16:01:31 + 统计 references 全部文本资源并保留最大文件证据。
def collect_reference_sizes(skill_dir: Path) -> list[tuple[str, int]]:
    """递归统计单个 skill 的 references 文件。"""
    references_dir = skill_dir / "references"
    if not references_dir.is_dir():
        return []

    # 1. 递归收集 references 下的所有普通文件，按相对路径稳定排序。
    files = sorted(
        (path for path in references_dir.rglob("*") if path.is_file()),
        key=lambda path: path.relative_to(skill_dir).as_posix(),
    )
    return [
        (path.relative_to(skill_dir).as_posix(), read_utf8_bytes(path))
        for path in files
    ]


# [参数] skill_dir: 单个 skill 目录。
# [返回] dict：单个 skill 的体积、文本包、reference 和预算等级字段。
# 最近修改时间：2026-07-17 16:01:31 + 组装后续候选冻结任务所需的固定统计结构。
def measure_skill(skill_dir: Path) -> dict[str, object]:
    """生成单个 skill 的稳定统计记录。"""
    # 1. 读取 SKILL.md 和 references，所有读取同时执行 UTF-8 校验。
    skill_md_path = skill_dir / "SKILL.md"
    skill_md_bytes = read_utf8_bytes(skill_md_path)
    reference_sizes = collect_reference_sizes(skill_dir)
    reference_total_bytes = sum(size for _, size in reference_sizes)
    reference_max_bytes = max((size for _, size in reference_sizes), default=0)
    default_text_bytes = skill_md_bytes + reference_total_bytes

    # 2. 按冻结阈值计算等级，并保留 reference 文件数量方便报告复核。
    budget_level = classify_budget(skill_md_bytes, reference_max_bytes, default_text_bytes)
    return {
        "name": skill_dir.name,
        "skill_md_bytes": skill_md_bytes,
        "reference_total_bytes": reference_total_bytes,
        "reference_max_bytes": reference_max_bytes,
        "reference_file_count": len(reference_sizes),
        "default_text_bytes": default_text_bytes,
        "budget_level": budget_level,
    }


# [参数] skill_md_bytes: SKILL.md 字节数；reference_max_bytes: 最大 reference 字节数；default_text_bytes: 默认文本包字节数。
# [返回] str：`normal`、`review`、`split_candidate` 或 `hard_warning`。
# 最近修改时间：2026-07-17 16:01:31 + 固化预算等级优先级并与需求文档阈值保持一致。
def classify_budget(skill_md_bytes: int, reference_max_bytes: int, default_text_bytes: int) -> str:
    """按冻结阈值从高风险到正常状态分级。"""
    # 1. 先命中 SKILL.md 硬警戒，再判断拆分候选和普通复评。
    if skill_md_bytes > THRESHOLDS["skill_md"]["hard_warning_bytes"]:
        return "hard_warning"
    if (
        skill_md_bytes > THRESHOLDS["skill_md"]["review_max_bytes"]
        or reference_max_bytes > THRESHOLDS["reference"]["review_max_bytes"]
        or default_text_bytes > THRESHOLDS["default_text"]["hard_warning_bytes"]
    ):
        return "split_candidate"
    if (
        skill_md_bytes > THRESHOLDS["skill_md"]["normal_max_bytes"]
        or reference_max_bytes > THRESHOLDS["reference"]["normal_max_bytes"]
        or default_text_bytes > THRESHOLDS["default_text"]["normal_max_bytes"]
    ):
        return "review"
    return "normal"


# [参数] root: 仓库根目录；registered_names: 正式注册 skill 名称；disk_directories: 实际 skill 目录。
# [返回] dict：完整 JSON 报告对象。
# 最近修改时间：2026-07-17 16:01:31 + 汇总 84 个正式 skill 与 27 个扩展种子的边界证据。
def build_report(
    root: Path,
    registered_names: list[str],
    disk_directories: list[Path],
) -> dict[str, object]:
    """汇总正式注册清单、磁盘目录差异和逐 skill 统计结果。"""
    # 1. 先建立磁盘目录索引，确保注册清单中的每个 skill 都有真实落点。
    disk_by_name = {path.name: path for path in disk_directories}
    missing = [name for name in registered_names if name not in disk_by_name]
    if missing:
        raise ValueError(f"正式字典 skill 缺少磁盘目录：{', '.join(missing)}")

    # 2. 统计正式 skill，并把未进入主规划域的目录作为扩展种子单独列出。
    skills = [measure_skill(disk_by_name[name]) for name in registered_names]
    registered_set = set(registered_names)
    excluded_seeds = sorted(name for name in disk_by_name if name not in registered_set)
    level_counts: dict[str, int] = {}
    for item in skills:
        level = str(item["budget_level"])
        level_counts[level] = level_counts.get(level, 0) + 1

    return {
        "schema_version": 1,
        "root": str(root),
        "registry_source": "字典.md：主规划域（11.扩展种子之前）",
        "skill_count": len(skills),
        "disk_skill_directory_count": len(disk_directories),
        "excluded_extension_seed_count": len(excluded_seeds),
        "excluded_extension_seed_names": excluded_seeds,
        "budget_level_counts": level_counts,
        "thresholds": THRESHOLDS,
        "skills": skills,
    }


# [参数] output_path: JSON 报告输出路径；payload: 报告对象。
# [返回] None：报告写入完成。
# 最近修改时间：2026-07-17 16:01:31 + 以 UTF-8 写入稳定 JSON 报告并保留末尾换行。
def write_report(output_path: Path, payload: dict[str, object]) -> None:
    """将统计报告以 UTF-8 JSON 写入指定路径。"""
    # 1. 创建报告父目录，并以不带 BOM 的 UTF-8 写入可复核文本。
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


# [参数] 无；参数由 argparse 从命令行读取。
# [返回] argparse.Namespace：解析后的仓库根目录和报告路径。
# 最近修改时间：2026-07-17 16:01:31 + 固化统计入口参数和默认仓库定位方式。
def parse_args() -> argparse.Namespace:
    """解析统计脚本命令行参数。"""
    # 1. 固定 root/output 两个入口，保持实施计划中的命令可直接执行。
    parser = argparse.ArgumentParser(description="统计正式 skill 的体积和默认文本包。")
    parser.add_argument("--root", type=Path, default=default_root(), help="仓库根目录")
    parser.add_argument("--output", type=Path, required=True, help="JSON 报告输出路径")
    return parser.parse_args()


# [参数] 无；命令行参数由 parse_args 读取。
# [返回] int：0 表示报告成功，1 表示扫描或写入失败。
# 最近修改时间：2026-07-17 16:01:31 + 完成统计流程日志、失败退出和报告落盘入口。
def main() -> int:
    """执行注册清单读取、体积统计和 JSON 报告写入。"""
    try:
        # 1. 解析参数并确认根目录、正式字典和输出路径。
        args = parse_args()
        root = args.root.resolve()
        registry_path = root / "字典.md"
        output_path = args.output.resolve()
        print(f"[开始] 统计根目录：{root}")
        print(f"[开始] 注册清单：{registry_path}")

        # 2. 先核对 84 个正式 skill 与磁盘实际目录的差异。
        registered_names = parse_registered_skills(registry_path)
        disk_directories = iter_disk_skill_directories(root)
        print(
            f"[统计] 正式注册 skill：{len(registered_names)}；"
            f"磁盘 skill 目录：{len(disk_directories)}；"
            f"排除扩展种子：{len(disk_directories) - len(registered_names)}"
        )

        # 3. 逐项计算体积和预算等级，写入正式 JSON 报告。
        payload = build_report(root, registered_names, disk_directories)
        write_report(output_path, payload)
        print(f"[完成] 报告已写入：{output_path}")
        print(f"[完成] 预算等级：{json.dumps(payload['budget_level_counts'], ensure_ascii=False, sort_keys=True)}")
        return 0
    except (OSError, UnicodeError, ValueError) as error:
        print(f"[失败] {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
