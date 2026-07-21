#!/usr/bin/env python3
"""验证 Skill 拆分的静态映射、触发契约和删除前后 fixture 状态。"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

import yaml


EXPECTED_FORMAL_SKILL_COUNT = 84
EXPECTED_DISK_SKILL_DIRECTORY_COUNT = 111
EXPECTED_EXTENSION_SEED_COUNT = 27
DEFAULT_CASE_ROOT = Path(__file__).resolve().parent / "cases"
TEST_TIMESTAMP_ROOT = Path(__file__).resolve().parents[1]


# [参数] 无。
# [返回] Path：当前测试脚本对应的仓库根目录。
# 最近修改时间：2026-07-17 18:00:00 + 建立 TASK-SPLIT-01-03 通用测试入口。
def default_root() -> Path:
    """按测试资产固定目录层级推导仓库根目录。"""
    return Path(__file__).resolve().parents[4]


# [参数] path: 待检查的本地路径；boundary: 允许访问的边界目录。
# [返回] bool：路径位于边界内时为 True，否则为 False。
# 最近修改时间：2026-07-17 18:00:38 + 增加测试入口的路径越界判定。
def is_path_within(path: Path, boundary: Path) -> bool:
    """判断解析后的路径是否位于指定目录及其子目录内。"""
    # 1. 尝试计算路径相对边界目录的相对路径。
    try:
        path.relative_to(boundary)
    except ValueError:
        return False
    return True


# [参数] root: 仓库根目录；configured_path: fixture 中的相对或绝对路径；label: 路径用途说明。
# [返回] Path：通过仓库边界检查后的解析路径。
# 最近修改时间：2026-07-17 18:00:38 + 收紧报告和矩阵路径的仓库边界。
def resolve_path(root: Path, configured_path: str, label: str) -> Path:
    """解析 fixture 路径并拒绝离开仓库根目录的路径。"""
    # 1. 解析相对路径或绝对路径，统一为磁盘上的规范路径。
    path = Path(configured_path)
    resolved = path.resolve() if path.is_absolute() else (root / path).resolve()
    boundary = root.resolve()

    # 2. 只允许报告和矩阵留在仓库根目录及其子目录。
    require(
        is_path_within(resolved, boundary),
        f"{label} 路径越界：{resolved} 不在仓库根目录 {boundary} 内",
    )
    return resolved


# [参数] case_root: 命令行传入的 fixture 根目录。
# [返回] None：fixture 根目录通过时间戳测试根边界检查。
# 最近修改时间：2026-07-17 18:00:38 + 固定样本目录只能位于当前测试时间戳目录。
def validate_case_root(case_root: Path) -> None:
    """拒绝从当前测试时间戳目录外读取 fixture。"""
    # 1. 确认当前测试脚本所属的时间戳根目录仍存在。
    timestamp_root = TEST_TIMESTAMP_ROOT.resolve()
    require(timestamp_root.is_dir(), f"测试时间戳根目录不存在：{timestamp_root}")

    # 2. 先确认传入目录存在，再校验其不能越出时间戳根目录。
    require(case_root.is_dir(), f"fixture 根目录不存在或不是目录：{case_root}")
    require(
        is_path_within(case_root, timestamp_root),
        f"fixture 根目录越界：{case_root} 不在测试时间戳目录 {timestamp_root} 内",
    )


# [参数] path: UTF-8 JSON 文件路径。
# [返回] dict：JSON 对象。
# 最近修改时间：2026-07-17 18:00:00 + 固化测试 fixture 的 UTF-8 读取入口。
def read_json(path: Path) -> dict[str, object]:
    """读取并解析 JSON fixture，拒绝非对象根节点。"""
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"JSON 根节点必须是对象：{path}")
    return payload


# [参数] path: 需要计算摘要的本地文件路径。
# [返回] str：小写十六进制 SHA-256 摘要。
# 最近修改时间：2026-07-17 18:00:00 + 增加矩阵与报告完整性核验。
def sha256_file(path: Path) -> str:
    """计算本地文件的 SHA-256，避免只依赖文件名判断内容。"""
    return hashlib.sha256(path.read_bytes()).hexdigest()


# [参数] condition: 当前断言；message: 失败时的脱敏说明。
# [返回] None：断言通过；失败时抛出 ValueError。
# 最近修改时间：2026-07-17 18:00:00 + 统一 fixture 断言失败出口。
def require(condition: bool, message: str) -> None:
    """将测试条件转换为可定位的失败信息。"""
    if not condition:
        raise ValueError(message)


# [参数] case_root: fixture 根目录；name: fixture 文件名。
# [返回] dict：已解析的 fixture 对象。
# 最近修改时间：2026-07-17 18:00:38 + 统一模式 fixture 加载和缺失文件报错。
def load_fixture(case_root: Path, name: str) -> dict[str, object]:
    """读取当前模式的 fixture，并检查文件存在。"""
    path = (case_root / name).resolve()
    require(is_path_within(path, case_root), f"fixture 路径越界：{path}")
    require(path.is_file(), f"fixture 不存在：{path}")
    return read_json(path)


# [参数] root: 仓库根目录；case_root: fixture 根目录。
# [返回] None：统计报告结构和数量口径通过。
# 最近修改时间：2026-07-17 18:00:38 + 增加 size 模式以复用既有统计报告。
def run_size_mode(root: Path, case_root: Path) -> None:
    """校验正式 skill 统计报告的 schema、数量和关键字段。"""
    # 1. 读取并校验统计报告及其固定数量口径。
    manifest = load_fixture(case_root, "mapping_cases.json")
    report_path = resolve_path(root, str(manifest["report_path"]), "统计报告")
    report = read_json(report_path)
    print(f"[步骤] 读取统计报告：{report_path}")

    # 2. 核对 schema、数量和每个统计条目的固定字段。
    require(report.get("schema_version") == 1, "统计报告 schema_version 不为 1")
    require(report.get("skill_count") == EXPECTED_FORMAL_SKILL_COUNT, "正式 skill 数量不是 84")
    require(
        report.get("disk_skill_directory_count") == EXPECTED_DISK_SKILL_DIRECTORY_COUNT,
        "磁盘 skill 目录数量不是 111",
    )
    require(
        report.get("excluded_extension_seed_count") == EXPECTED_EXTENSION_SEED_COUNT,
        "扩展种子数量不是 27",
    )
    skills = report.get("skills")
    require(isinstance(skills, list) and len(skills) == EXPECTED_FORMAL_SKILL_COUNT, "统计条目数量不为 84")
    required_fields = {
        "name",
        "skill_md_bytes",
        "reference_total_bytes",
        "reference_max_bytes",
        "default_text_bytes",
        "budget_level",
    }
    for item in skills:
        require(isinstance(item, dict), "统计条目不是对象")
        require(required_fields <= set(item), f"统计条目缺少字段：{item.get('name', '<unknown>')}")

    # 3. 用 fixture 摘要复核报告内容，避免只依赖文件名。
    expected_hash = str(manifest["report_sha256"]).lower()
    require(sha256_file(report_path) == expected_hash, "统计报告 SHA-256 不一致")
    print(f"[通过] size：84 个正式 skill、111 个磁盘目录、27 个扩展种子")


# [参数] root: 仓库根目录；case_root: fixture 根目录。
# [返回] None：矩阵路径、哈希、候选和追踪字段通过。
# 最近修改时间：2026-07-17 18:00:38 + 增加 mapping 模式以保护 TASK-SPLIT-01-02 产物。
def run_mapping_mode(root: Path, case_root: Path) -> None:
    """校验候选矩阵的冻结摘要和关键职责入口。"""
    # 1. 读取候选矩阵并先核对冻结哈希。
    manifest = load_fixture(case_root, "mapping_cases.json")
    matrix_path = resolve_path(root, str(manifest["matrix_path"]), "候选矩阵")
    matrix_text = matrix_path.read_text(encoding="utf-8")
    print(f"[步骤] 读取候选矩阵：{matrix_path}")

    # 2. 核对候选 token 和正式/扩展种子数量边界。
    require(sha256_file(matrix_path) == str(manifest["matrix_sha256"]).lower(), "候选矩阵 SHA-256 不一致")
    for token in manifest["required_matrix_tokens"]:
        require(str(token) in matrix_text, f"候选矩阵缺少关键字段或候选：{token}")
    require(matrix_text.count("registry_scope:") >= EXPECTED_FORMAL_SKILL_COUNT, "正式矩阵条目数量不足")
    require(matrix_text.count("extension_seed_entries:") == 1, "扩展种子矩阵区缺失")

    # 3. 输出可供任务证据登记的确定性通过信息。
    print("[通过] mapping：矩阵哈希、84/27 边界、候选顺序和职责入口均可复核")


# [参数] root: 仓库根目录；mapping_path: 待校验的原子化规则映射 YAML 路径。
# [返回] None：全部条目校验通过；否则抛出 ValueError。
# 最近修改时间：2026-07-18 00:00:00 + 支持单 skill 原子化映射的零丢失覆盖校验（TASK-SPLIT-02-01）。
def run_atomized_mapping_mode(root: Path, mapping_path: Path) -> None:
    """校验单个候选 skill 的原子化规则映射：每条规则/资源必须有唯一 id、owner 和 migration_action，覆盖率必须 100%。"""
    # 1. 解析映射文件路径并限制在仓库根目录内，拒绝越界读取。
    resolved = resolve_path(root, str(mapping_path), "原子化映射")
    require(resolved.is_file(), f"原子化映射文件不存在：{resolved}")
    data = yaml.safe_load(resolved.read_text(encoding="utf-8"))
    require(isinstance(data, dict), f"映射根节点必须是对象：{resolved}")
    print(f"[步骤] 读取原子化映射：{resolved}")

    seen_ids: set[str] = set()
    unowned: list[str] = []

    # 2. 校验 shared_resources 与 rules 两类条目均具备唯一 id、owner 和迁移动作。
    def check_items(items: object, label: str) -> None:
        require(isinstance(items, list) and items, f"{label} 必须是非空列表")
        for item in items:
            require(isinstance(item, dict), f"{label} 存在非对象条目")
            item_id = item.get("id")
            require(isinstance(item_id, str) and item_id, f"{label} 存在缺少 id 的条目")
            require(item_id not in seen_ids, f"{label} 出现重复 id：{item_id}")
            seen_ids.add(item_id)
            owner = item.get("owner")
            require(isinstance(owner, str) and owner, f"{item_id} 缺少 owner")
            if not item.get("migration_action"):
                unowned.append(item_id)

    check_items(data.get("shared_resources", []), "shared_resources")
    check_items(data.get("rules", []), "rules")
    require(not unowned, f"以下条目缺少 migration_action：{unowned}")

    # 3. 交叉核对 coverage_summary 与 stop_condition_check 的自报告是否与实测条目数一致。
    summary = data.get("coverage_summary")
    require(isinstance(summary, dict), "缺少 coverage_summary")
    require(summary.get("unmapped_items") == 0, "coverage_summary 声明存在未映射条目")
    require(
        summary.get("total_atomized_items") == len(seen_ids),
        f"coverage_summary 声明总数 {summary.get('total_atomized_items')} 与实测条目数 {len(seen_ids)} 不一致",
    )

    stop_check = data.get("stop_condition_check")
    require(isinstance(stop_check, dict), "缺少 stop_condition_check")
    require(stop_check.get("result") == "pass", "stop_condition_check 未通过")
    require(stop_check.get("any_rule_without_owner") is False, "存在无主规则")
    require(stop_check.get("any_script_resource_without_owner") is False, "存在无主脚本资源")
    require(stop_check.get("duplicate_owner_conflict") is False, "存在 owner 冲突")

    # 4. 输出可供任务证据登记的确定性通过信息。
    print(f"[通过] mapping：原子化映射 {len(seen_ids)} 条目全部有 owner 与 migration_action，覆盖率 100%")


# [参数] root: 仓库根目录；mapping_path: 待校验的 MCP 路由矩阵 YAML 路径。
# [返回] None：全部结构、命中数与结论一致性校验通过；否则抛出 ValueError。
# 最近修改时间：2026-07-20 15:30:00 + 建立 CYCLE-SPLIT-07 的 MCP 路由矩阵复评校验（TASK-SPLIT-07-01）。
def run_route_matrix_mode(root: Path, mapping_path: Path) -> None:
    """校验 MCP 路由矩阵：候选组结构、样本命中重算、体积证据与拆/不拆结论的内部一致性。"""
    # 1. 解析矩阵路径并限制在仓库根目录内，拒绝越界读取。
    resolved = resolve_path(root, str(mapping_path), "MCP 路由矩阵")
    require(resolved.is_file(), f"MCP 路由矩阵文件不存在：{resolved}")
    data = yaml.safe_load(resolved.read_text(encoding="utf-8"))
    require(isinstance(data, dict), f"矩阵根节点必须是对象：{resolved}")
    print(f"[步骤] 读取 MCP 路由矩阵：{resolved}")

    # 2. 用磁盘上的真实 SKILL.md 字节数交叉核对矩阵里声明的体积证据，避免复评依据过期数字。
    skill_md_path = resolve_path(root, str(data.get("skill_md_path", "")), "MCP skill SKILL.md")
    require(skill_md_path.is_file(), f"MCP skill SKILL.md 不存在：{skill_md_path}")
    actual_bytes = skill_md_path.stat().st_size
    require(
        data.get("skill_md_bytes") == actual_bytes,
        f"矩阵声明体积 {data.get('skill_md_bytes')} 与磁盘实测 {actual_bytes} 不一致",
    )

    # 3. 校验候选组结构：每个组必须有唯一 id、职责说明和唯一 config_owner 归属。
    groups = data.get("candidate_groups")
    require(isinstance(groups, list) and groups, "candidate_groups 必须是非空列表")
    group_ids: set[str] = set()
    for group in groups:
        require(isinstance(group, dict), "candidate_groups 存在非对象条目")
        group_id = group.get("id")
        require(isinstance(group_id, str) and group_id, "候选组缺少 id")
        require(group_id not in group_ids, f"候选组出现重复 id：{group_id}")
        group_ids.add(group_id)
        require(bool(group.get("responsibility")), f"{group_id} 缺少 responsibility")
        require(bool(group.get("config_owner")), f"{group_id} 缺少 config_owner")

    # 4. 校验样本命中列表只引用已登记的候选组 id，并据此重新计算命中统计。
    samples = data.get("samples")
    require(isinstance(samples, list) and samples, "samples 必须是非空列表")
    total_hit_count = 0
    co_occurring_sample_count = 0
    for sample in samples:
        require(isinstance(sample, dict), "samples 存在非对象条目")
        require(bool(sample.get("id")), "样本缺少 id")
        require(bool(sample.get("prompt")), f"{sample.get('id')} 缺少 prompt")
        hits = sample.get("expected_groups_hit")
        require(isinstance(hits, list), f"{sample.get('id')} 的 expected_groups_hit 必须是列表")
        for hit in hits:
            require(hit in group_ids, f"{sample.get('id')} 引用未登记候选组：{hit}")
        total_hit_count += len(hits)
        if len(hits) >= 2:
            co_occurring_sample_count += 1

    # 5. 重算平均命中数、独立组数量与共同命中占比，并与矩阵自报告的 metrics 交叉核对。
    total_samples = len(samples)
    metrics = data.get("metrics")
    require(isinstance(metrics, dict), "缺少 metrics")
    require(metrics.get("total_samples") == total_samples, "metrics.total_samples 与实测样本数不一致")
    require(metrics.get("total_hit_count") == total_hit_count, "metrics.total_hit_count 与重算命中数不一致")
    computed_average = round(total_hit_count / total_samples, 4)
    declared_average = round(float(metrics.get("average_hits_per_sample", -1)), 4)
    require(computed_average == declared_average, "metrics.average_hits_per_sample 与重算平均命中数不一致")
    require(metrics.get("independent_group_count") == len(group_ids), "metrics.independent_group_count 与候选组数量不一致")
    require(
        metrics.get("co_occurring_sample_count") == co_occurring_sample_count,
        "metrics.co_occurring_sample_count 与重算共同命中样本数不一致",
    )
    computed_co_rate = round(co_occurring_sample_count / total_samples, 4)
    declared_co_rate = round(float(metrics.get("co_occurrence_rate", -1)), 4)
    require(computed_co_rate == declared_co_rate, "metrics.co_occurrence_rate 与重算共同命中占比不一致")

    # 6. 校验拆/不拆结论与三项数字门槛（>=2 独立组、平均命中<=3、配置 owner 唯一）自洽；
    #    结论为 split 时必须满足全部数字门槛，结论为 no_split/gated 时必须给出非空 reason 与 next_review_condition。
    conclusion = data.get("conclusion")
    require(isinstance(conclusion, dict), "缺少 conclusion")
    decision = conclusion.get("decision")
    require(decision in ("split", "no_split", "gated"), f"conclusion.decision 取值非法：{decision}")
    require(bool(conclusion.get("reason")), "conclusion 缺少 reason")
    require(bool(conclusion.get("next_review_condition")), "conclusion 缺少 next_review_condition")
    owners = [group.get("config_owner") for group in groups]
    unique_owner = len(owners) == len(set(owners))
    if decision == "split":
        require(len(group_ids) >= 2, "结论为 split 但独立组数量不足 2")
        require(computed_average <= 3, "结论为 split 但平均命中数超过 3")
        require(unique_owner, "结论为 split 但存在重复 config_owner")

    # 7. 输出可供任务证据登记的确定性通过信息，明确本次复评的拆/不拆结论。
    print(
        f"[通过] route-matrix：{len(group_ids)} 个候选组、{total_samples} 条样本、"
        f"平均命中 {computed_average}、共同命中占比 {computed_co_rate}，结论 decision={decision}"
    )


# [参数] case_root: fixture 根目录；phase: trigger/pre-delete/post-delete 阶段。
# [返回] int：通过的样本数量。
# 最近修改时间：2026-07-17 18:00:38 + 增加基于 observed_hits 的确定性路由契约校验。
def run_trigger_cases(case_root: Path, phase: str | None = None) -> int:
    """校验触发样本的必需命中、禁止命中和阶段标识。"""
    # 1. 读取触发 fixture，并按阶段筛选样本。
    fixture = load_fixture(case_root, "trigger_cases.json")
    cases = fixture.get("cases")
    require(isinstance(cases, list) and cases, "触发 fixture 没有样本")
    passed = 0

    # 2. 对每个阶段样本核对 required、forbidden 和 observed_hits 的关系。
    for case in cases:
        require(isinstance(case, dict), "触发样本不是对象")
        if phase and case.get("phase") != phase:
            continue
        case_id = str(case.get("id", "<unknown>"))
        required = {str(item) for item in case.get("required", [])}
        forbidden = {str(item) for item in case.get("forbidden", [])}
        observed = {str(item) for item in case.get("observed_hits", [])}
        require(case.get("source") == "fixture_observation", f"{case_id} 缺少 fixture 观察来源标记")
        require(required <= observed, f"{case_id} 缺少必需命中：{sorted(required - observed)}")
        require(not (forbidden & observed), f"{case_id} 命中禁止 skill：{sorted(forbidden & observed)}")
        passed += 1
        print(f"[通过] trigger：{case_id} phase={case.get('phase')}")

    # 3. 禁止空阶段通过，避免 fixture 被误删或阶段拼写漂移。
    require(passed > 0, f"没有匹配 phase={phase}")
    return passed


# [参数] case_root: fixture 根目录；phase: pre-delete 或 post-delete。
# [返回] int：通过的删除前后状态样本数量。
# 最近修改时间：2026-07-17 18:00:38 + 建立删除前后 fixture 状态边界，禁止真实删除 skill。
def run_delete_phase(case_root: Path, phase: str) -> int:
    """校验删除前后 fixture 的旧入口和新入口状态。"""
    # 1. 读取删除阶段快照，不执行真实目录操作。
    fixture = load_fixture(case_root, "delete_cases.json")
    cases = fixture.get("cases")
    require(isinstance(cases, list) and cases, "删除阶段 fixture 没有样本")
    passed = 0

    # 2. 只核对旧/新入口快照，不对真实 skill 目录执行删除。
    for case in cases:
        if case.get("phase") != phase:
            continue
        case_id = str(case.get("id", "<unknown>"))
        require(case.get("state_source") == "fixture_snapshot", f"{case_id} 不是 fixture 快照")
        require(case.get("new_skills_present") is True, f"{case_id} 新 skill 状态不是 present")
        expected_old = phase == "pre-delete"
        require(case.get("old_skill_present") is expected_old, f"{case_id} 旧 skill 状态不符合 {phase}")
        require(case.get("mapping_status") == "frozen", f"{case_id} 映射状态未冻结")
        passed += 1
        print(f"[通过] {phase}：{case_id}（仅验证 fixture，不删除真实目录）")

    # 3. 禁止没有匹配样本的阶段被错误判定为通过。
    require(passed > 0, f"没有匹配 phase={phase}")
    return passed


# [参数] 无；参数由 argparse 从命令行读取。
# [返回] argparse.Namespace：测试模式、仓库根目录和 fixture 路径。
# 最近修改时间：2026-07-17 18:00:38 + 固化 TASK-SPLIT-01-03 的可复用命令接口。
def parse_args() -> argparse.Namespace:
    """解析通用拆分测试入口参数。"""
    # 1. 建立固定的模式集合和本地路径参数。
    parser = argparse.ArgumentParser(
        description="验证 Skill 拆分的 size、mapping、trigger、pre-delete、post-delete 契约。"
    )
    parser.add_argument(
        "--mode",
        required=True,
        choices=("all", "size", "mapping", "trigger", "pre-delete", "post-delete", "route-matrix"),
        help="验证模式；all 依次执行全部本地 fixture 模式；route-matrix 需配合 --mapping 单独运行",
    )
    parser.add_argument("--root", type=Path, default=default_root(), help="仓库根目录")
    parser.add_argument("--cases", type=Path, default=DEFAULT_CASE_ROOT, help="ASCII fixture 根目录")
    parser.add_argument(
        "--mapping",
        type=Path,
        default=None,
        help="单个候选 skill 的原子化规则映射 YAML；提供时 mode=mapping 改为校验该映射而非候选矩阵",
    )

    # 2. 返回 argparse 解析结果，保持入口参数可由 help 直接发现。
    return parser.parse_args()


# [参数] 无；命令行参数由 parse_args 读取。
# [返回] int：0 表示通过，1 表示 fixture/断言/编码失败。
# 最近修改时间：2026-07-17 18:00:38 + 完成通用入口的过程日志和退出码收口。
def main() -> int:
    """按模式执行本地拆分验证，不连接业务环境且不修改 skill 目录。"""
    try:
        args = parse_args()
        root = args.root.resolve()
        case_root = args.cases.resolve()
        require(root.is_dir(), f"仓库根目录不存在或不是目录：{root}")
        validate_case_root(case_root)
        modes = (
            ("size", "mapping", "trigger", "pre-delete", "post-delete")
            if args.mode == "all"
            else (args.mode,)
        )
        # 1. 先固定仓库和 fixture 边界，避免错误样本访问测试根目录之外的文件。
        print(f"[开始] Skill 拆分验证 mode={args.mode}")
        print(f"[步骤] 仓库根目录：{root}")
        print(f"[步骤] fixture 根目录：{case_root}")

        # 2. 按请求模式执行静态统计、映射、触发和删除前后状态断言。
        for mode in modes:
            if mode == "size":
                run_size_mode(root, case_root)
            elif mode == "mapping":
                if args.mapping is not None:
                    run_atomized_mapping_mode(root, args.mapping)
                else:
                    run_mapping_mode(root, case_root)
            elif mode == "trigger":
                run_trigger_cases(case_root)
            elif mode == "route-matrix":
                require(args.mapping is not None, "route-matrix 模式必须提供 --mapping")
                run_route_matrix_mode(root, args.mapping)
            else:
                run_trigger_cases(case_root, mode)
                run_delete_phase(case_root, mode)
        # 3. 只报告 fixture 验证结果，不执行真实 skill 删除或字典刷新。
        print(f"[完成] Skill 拆分验证通过 mode={args.mode}")
        return 0
    except (OSError, UnicodeError, ValueError, KeyError, TypeError) as error:
        print(f"[失败] {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
