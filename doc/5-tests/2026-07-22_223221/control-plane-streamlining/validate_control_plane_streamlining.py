#!/usr/bin/env python3
"""验证总控层 Skill 精简、合并、触发契约和退役结果。"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Any, Iterable

import yaml

MANIFEST_ID = "MANIFEST-TC-20260722"
RETIRE = {
    "subagent-dispatch-rules": "parallel-task-dispatch-rules",
    "project-memory-file-bootstrap-rules": "project-rule-file-bootstrap-rules",
}
ACTIVE_ROOT_FILES = {"AGENTS.md", "CLAUDE.md", "README.md", "编码skill.md", "PROJECT_CURRENT.md", "PROJECT_MEMORY.md", "PROJECT_STYLE.md", "项目设计.md"}
EXPECTED_TRIGGER_CASES = {
    "TR-TC-001": ({"skill-hit-check-rules"}, set()),
    "TR-TC-002": ({"skill-hit-check-rules", "git-collaboration-rules"}, set()),
    "TR-TC-003": ({"skill-hit-check-rules"}, {"git-collaboration-rules"}),
    "TR-TC-004": ({"implementation-planning-rules"}, set()),
    "TR-TC-005": ({"context-compression-rules"}, {"recent-context-bootstrap-rules"}),
    "TR-TC-006": ({"recent-context-bootstrap-rules"}, {"context-compression-rules"}),
    "TR-TC-007": ({"project-rule-file-bootstrap-rules"}, {"project-memory-file-bootstrap-rules"}),
    "TR-TC-008": ({"project-rule-file-bootstrap-rules"}, {"project-memory-file-bootstrap-rules"}),
    "TR-TC-009": ({"parallel-task-dispatch-rules"}, {"subagent-dispatch-rules"}),
    "TR-TC-010": ({"parallel-task-dispatch-rules"}, {"subagent-dispatch-rules"}),
    "TR-TC-011": ({"implementation-review-rules"}, set()),
    "TR-TC-012": ({"code-change-finalization-gate-rules", "comment-completion-gate-rules"}, set()),
    "TR-TC-013": ({"skill-execution-compliance-gate-rules"}, {"code-change-finalization-gate-rules"}),
    "TR-TC-014": ({"final-acceptance-rules"}, {"artifact-delivery-gate-rules"}),
    "TR-TC-015": ({"artifact-delivery-gate-rules"}, {"final-acceptance-rules"}),
    "TR-TC-016": ({"autonomous-execution-rules"}, set()),
}


def log(message: str) -> None:
    """
    [参数] message: 需要输出到控制台的测试过程说明。
    [返回] 无返回值。
    最近修改时间：2026-07-22，原因：补充测试脚本关键过程日志。
    """
    print(f"[control-plane] {message}", file=sys.stderr)


def read(path: Path) -> str:
    """
    [参数] path: 需要按 UTF-8 读取的文件路径。
    [返回] 文件完整文本。
    最近修改时间：2026-07-22，原因：统一验证器 UTF-8 读取入口。
    """
    return path.read_text(encoding="utf-8")


def load_yaml(path: Path) -> Any:
    """
    [参数] path: YAML 文件路径。
    [返回] YAML 解析后的 Python 对象。
    最近修改时间：2026-07-22，原因：统一 manifest 与 fixture 解析入口。
    """
    return yaml.safe_load(read(path))


def fail(errors: list[str], message: str) -> None:
    """
    [参数] errors: 当前阶段错误列表；message: 新增错误说明。
    [返回] 无返回值，直接向错误列表追加一项。
    最近修改时间：2026-07-22，原因：统一失败证据收集。
    """
    errors.append(message)


def git(root: Path, *args: str) -> str:
    """
    [参数] root: 仓库根目录；args: 传给 Git 的只读参数。
    [返回] 去除首尾空白后的 Git 标准输出。
    最近修改时间：2026-07-22，原因：固定基线哈希读取方式。
    """
    return subprocess.check_output(
        ["git", *args], cwd=root, text=True, encoding="utf-8"
    ).strip()


def validate_manifest(
    root: Path, manifest_path: Path, phase: str, errors: list[str]
) -> dict[str, Any]:
    """
    [参数] root: 仓库根目录；manifest_path: 映射清单路径；phase: 当前验证阶段；errors: 错误列表。
    [返回] 解析后的 manifest；格式错误时返回空字典或带缺口的原对象。
    最近修改时间：2026-07-22，原因：补齐保护语义、回滚定位与冻结写集的基线门禁。
    """
    # 1. 解析 manifest 根结构并核对固定身份。
    log(f"{phase}: 校验 manifest 结构与候选数量")
    data = load_yaml(manifest_path)
    if not isinstance(data, dict):
        fail(errors, "manifest root must be mapping")
        return {}
    if data.get("manifest_id") != MANIFEST_ID:
        fail(errors, "manifest_id mismatch")

    # 2. 核对候选、退役数量和每个候选的触发/回滚契约。
    scope = data.get("scope") or {}
    candidates = data.get("candidates") or []
    if scope.get("candidate_count") != 18 or len(candidates) != 18:
        fail(errors, "candidate_count must be 18")
    retired = [item for item in candidates if item.get("action") == "merge_retire"]
    if scope.get("retire_candidate_count") != 2 or len(retired) != 2:
        fail(errors, "retire count must be 2")

    ids: set[str] = set()
    sources: set[str] = set()
    for item in candidates:
        candidate_id = item.get("candidate_id")
        source_skill = item.get("source_skill")
        if not candidate_id or candidate_id in ids:
            fail(errors, f"duplicate candidate id: {candidate_id}")
        ids.add(candidate_id)
        if not source_skill or source_skill in sources:
            fail(errors, f"duplicate source: {source_skill}")
        sources.add(source_skill)
        if not item.get("protected_semantics"):
            fail(errors, f"{candidate_id} missing protected semantics")
        contract = item.get("trigger_contract") or {}
        if (
            contract.get("preserve_description") is not True
            or contract.get("positive_negative_required") is not True
            or contract.get("neighbor_competition_required") is not True
        ):
            fail(errors, f"{candidate_id} trigger contract incomplete")
        rollback = item.get("rollback_locator") or {}
        if (
            not rollback.get("baseline_commit")
            or rollback.get("source_root") != source_skill
        ):
            fail(errors, f"{candidate_id} rollback locator incomplete")
        if not item.get("write_set"):
            fail(errors, f"{candidate_id} frozen write set missing")

        # 2.1 使用 Git 对象库验证退役目录仍可从基线恢复。
        baseline = item.get("baseline") or {}
        try:
            actual_tree = git(root, "rev-parse", f"{baseline.get('commit')}:{source_skill}")
        except Exception as exc:  # noqa: BLE001 - 需要把 Git 基线不可用写入统一错误列表。
            fail(errors, f"{candidate_id} baseline tree unavailable: {exc}")
            continue
        if actual_tree != baseline.get("tree"):
            fail(errors, f"{candidate_id} baseline tree mismatch")

    # 3. 核对清单引用的保护语义、资产清单和触发样本真实存在。
    for key in ["protected_semantics", "asset_inventory", "trigger_fixtures"]:
        relative = data.get(key)
        target = manifest_path.parent.parent / relative if isinstance(relative, str) else None
        if target is None or not target.is_file():
            fail(errors, f"{key} missing: {relative}")
    return data


def validate_trigger_fixtures(root: Path, fixtures_path: Path, errors: list[str]) -> None:
    """
    [参数] root: 仓库根目录；fixtures_path: 触发样本文件；errors: 错误列表。
    [返回] 无返回值，正向、负向或邻域样本不完整时追加错误。
    最近修改时间：2026-07-22，原因：让 trigger fixtures 从“仅存在”升级为机器可校验契约。
    """
    # 1. 核对 16 个稳定样本及其 expect/reject 集合未漂移。
    log("trigger: 校验正向、负向与邻域竞争样本")
    fixtures = load_yaml(fixtures_path) or {}
    cases = fixtures.get("cases") or []
    actual_ids = {case.get("id") for case in cases}
    if actual_ids != set(EXPECTED_TRIGGER_CASES):
        fail(errors, "trigger fixture ids mismatch")

    for case in cases:
        case_id = case.get("id")
        if case_id not in EXPECTED_TRIGGER_CASES:
            continue
        expected_expect, expected_reject = EXPECTED_TRIGGER_CASES[case_id]
        actual_expect = set(case.get("expect") or [])
        actual_reject = set(case.get("reject") or [])
        if actual_expect != expected_expect:
            fail(errors, f"{case_id} expect mismatch: {sorted(actual_expect)}")
        if actual_reject != expected_reject:
            fail(errors, f"{case_id} reject mismatch: {sorted(actual_reject)}")
        if not str(case.get("input") or "").strip():
            fail(errors, f"{case_id} input missing")

        # 1.1 正向目标必须存在；退役入口只允许出现在 reject 集合中。
        for skill in actual_expect:
            if not (root / skill / "SKILL.md").is_file():
                fail(errors, f"{case_id} expected skill missing: {skill}")
        for retired_skill in set(RETIRE) & actual_expect:
            fail(errors, f"{case_id} retired skill cannot be expected: {retired_skill}")



def validate_retired_alias_contract(root: Path, contract_path: Path, errors: list[str]) -> None:
    """
    [参数] root: 仓库根目录；contract_path: 退役触发别名契约；errors: 错误列表。
    [返回] 无返回值，基线 description 或目标 Owner 承接语义不完整时追加错误。
    最近修改时间：2026-07-22，原因：增加逐退役入口 source description 到目标 Owner 的可执行断言。
    """
    # 1. 从 Git 基线重新读取原 description，防止人工契约伪造或遗漏来源语义。
    log("trigger: 校验退役入口 description 与目标 Owner 别名承接")
    data = json.loads(read(contract_path))
    contracts = data.get("contracts") or []
    if len(contracts) != len(RETIRE):
        fail(errors, "retired alias contract count mismatch")
    for contract in contracts:
        source = contract.get("source_skill")
        target = contract.get("target_owner")
        baseline_commit = contract.get("baseline_commit")
        if RETIRE.get(source) != target:
            fail(errors, f"retired alias owner mismatch: {source} -> {target}")
            continue
        raw = subprocess.check_output(
            ["git", "show", f"{baseline_commit}:{source}/SKILL.md"],
            cwd=root,
            text=True,
            encoding="utf-8",
        )
        match = re.search(r"^description:\s*(.+)$", raw, re.MULTILINE)
        source_description = match.group(1).strip() if match else ""
        actual_hash = hashlib.sha256(source_description.encode("utf-8")).hexdigest()
        if source_description != contract.get("source_description"):
            fail(errors, f"source description mismatch: {source}")
        if actual_hash != contract.get("source_description_sha256"):
            fail(errors, f"source description hash mismatch: {source}")

        # 2. 聚合目标 Owner 的入口、Agent 元数据与 references，逐 token 证明旧触发语义已有落点。
        target_root = root / target
        target_texts: list[str] = []
        for path in target_root.rglob("*"):
            if path.is_file() and path.suffix.lower() in {".md", ".yaml", ".yml", ".py", ".json"}:
                target_texts.append(read(path))
        aggregate = "\n".join(target_texts)
        for token in contract.get("required_target_tokens") or []:
            if token not in aggregate:
                fail(errors, f"retired alias token missing in {target}: {token}")

def validate_baseline(
    root: Path, manifest_path: Path, manifest: dict[str, Any], errors: list[str]
) -> None:
    """
    [参数] root: 仓库根目录；manifest_path: manifest 路径；manifest: 解析清单；errors: 错误列表。
    [返回] 无返回值，基线资产或 fixture 不完整时追加错误。
    最近修改时间：2026-07-22，原因：冻结 18 个候选的资产和触发样本基线。
    """
    # 1. 核对资产 inventory 覆盖每个候选且记录了文件清单。
    log("baseline: 校验 18 个候选的资产清单")
    base = manifest_path.parent.parent
    inventory = json.loads(read(base / manifest["asset_inventory"]))
    if len(inventory) != 18:
        fail(errors, "asset inventory must cover 18 skills")
    for source, record in inventory.items():
        if record.get("root") != source or not record.get("files"):
            fail(errors, f"inventory incomplete: {source}")

    # 2. 同步验证正向、负向和邻域竞争样本。
    validate_trigger_fixtures(root, base / manifest["trigger_fixtures"], errors)


def require_text(root: Path, relative: str, required: list[str], errors: list[str]) -> str:
    """
    [参数] root: 仓库根目录；relative: 相对文件路径；required: 必须出现的标记；errors: 错误列表。
    [返回] 目标文件文本；文件不存在时返回空字符串。
    最近修改时间：2026-07-22，原因：统一静态保护语义断言。
    """
    path = root / relative
    if not path.is_file():
        fail(errors, f"missing file: {relative}")
        return ""
    text = read(path)
    for token in required:
        if token not in text:
            fail(errors, f"{relative} missing token: {token}")
    return text


def validate_trigger(
    root: Path, manifest_path: Path, manifest: dict[str, Any], errors: list[str]
) -> None:
    """
    [参数] root: 仓库根目录；manifest_path: manifest 路径；manifest: 解析清单；errors: 错误列表。
    [返回] 无返回值，触发契约或 Skill 结构失败时追加错误。
    最近修改时间：2026-07-22，原因：覆盖入口、恢复、自举、并行和收口的触发回归。
    """
    # 1. 核对每个总控 Owner 的最小保护语义仍在目标资产中。
    log("trigger: 校验总控 Owner 的保护语义")
    require_text(
        root,
        "skill-hit-check-rules/SKILL.md",
        ["每轮用户新消息", "命中检查", "Git规则", "parallel-task-dispatch-rules"],
        errors,
    )
    require_text(root, "team-development-rules/SKILL.md", ["阶段", "冲突", "不负责"], errors)
    compression = require_text(
        root,
        "context-compression-rules/SKILL.md",
        ["context-recovery-contract", "编码许可"],
        errors,
    )
    if re.search(r"(立即|强制)联动\s*`recent-context-bootstrap-rules`", compression):
        fail(errors, "context compression still unconditionally invokes recent context")
    require_text(
        root,
        "recent-context-bootstrap-rules/SKILL.md",
        ["新会话", "context-recovery-contract"],
        errors,
    )
    require_text(
        root,
        "project-rule-file-bootstrap-rules/SKILL.md",
        ["rule-bootstrap", "memory-bootstrap", "51,200", "PROJECT_HISTORY.md", "非受管"],
        errors,
    )
    require_text(
        root,
        "parallel-task-dispatch-rules/SKILL.md",
        ["串行", "条件并行", "可并行", "计划线程数", "实际启动", "完成数", "关闭数", "写集", "系统"],
        errors,
    )
    require_text(root, "autonomous-execution-rules/SKILL.md", ["执行授权", "停止", "最大推进边界"], errors)
    require_text(
        root,
        "git-collaboration-rules/SKILL.md",
        ["当前轮", "skill-hit-check-rules", "pre_commit_gate.sh", "post_commit_gate.sh"],
        errors,
    )
    require_text(root, "implementation-review-rules/SKILL.md", ["唯一自动测试前", "references"], errors)
    require_text(
        root,
        "skill-execution-compliance-gate-rules/SKILL.md",
        ["reasoning-summary-structure-rules", "PASS", "FAIL"],
        errors,
    )
    require_text(
        root,
        "code-change-finalization-gate-rules/SKILL.md",
        ["reasoning-summary-structure-rules", "comment-completion-gate-rules"],
        errors,
    )
    require_text(
        root,
        "reasoning-summary-structure-rules/references/conditional-sections-rules.md",
        ["等待用户新指令", "可选优化", "blocked"],
        errors,
    )

    # 2. 核对触发 fixture 本身及所有改动 Skill 的结构有效性。
    base = manifest_path.parent.parent
    validate_trigger_fixtures(root, base / manifest["trigger_fixtures"], errors)
    validate_retired_alias_contract(root, base / "mapping/retired-trigger-alias-contract.json", errors)

    # 2.1 上层 Agent 元数据只允许引用注释 Owner 的结果，不得复制字段级注释规则。
    for relative in [
        "implementation-review-rules/agents/openai.yaml",
        "code-change-finalization-gate-rules/agents/openai.yaml",
    ]:
        agent_text = require_text(root, relative, ["PASS/FAIL", "不复制"], errors)
        for forbidden in ["[参数]", "[返回]", "最近修改时间", "1.1/1.2"]:
            if forbidden in agent_text:
                fail(errors, f"comment detail duplicated in agent metadata: {relative}: {forbidden}")

    skills = [
        "skill-hit-check-rules",
        "team-development-rules",
        "context-compression-rules",
        "recent-context-bootstrap-rules",
        "project-rule-file-bootstrap-rules",
        "parallel-task-dispatch-rules",
        "autonomous-execution-rules",
        "git-collaboration-rules",
        "implementation-review-rules",
        "skill-execution-compliance-gate-rules",
        "code-change-finalization-gate-rules",
        "reasoning-summary-structure-rules",
    ]
    for skill in skills:
        # 2.1 Windows 默认区域编码不是 UTF-8，显式把子进程固定为 UTF-8，避免 GBK 误判合法 Skill。
        child_env = os.environ.copy()
        child_env["PYTHONUTF8"] = "1"
        child_env["PYTHONIOENCODING"] = "utf-8"
        process = subprocess.run(
            [
                sys.executable,
                "-B",
                str(root / ".system/skill-creator/scripts/quick_validate.py"),
                str(root / skill),
            ],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            env=child_env,
            check=False,
        )
        if process.returncode != 0:
            fail(errors, f"quick_validate failed {skill}: {process.stdout}{process.stderr}")


def active_consumer_files(root: Path) -> Iterable[Path]:
    """
    [参数] root: 仓库根目录。
    [返回] 可能承担活跃 Skill 路由职责的文件迭代器。
    最近修改时间：2026-07-22，原因：限定退役名称消费者扫描范围并排除历史证据。
    """
    # 1. 只枚举活跃规则、Agent 元数据、脚本和根级说明，避免历史文档误报。
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        relative = path.relative_to(root).as_posix()
        if relative.startswith(".git/") or relative.startswith("doc/") or relative.startswith("skill-dictionary/"):
            continue
        if relative == "PROJECT_HISTORY.md":
            continue
        if (
            path.name in {"SKILL.md", "openai.yaml"}
            or relative in ACTIVE_ROOT_FILES
            or relative.endswith(".sh")
            or relative.endswith(".py")
        ):
            yield path


def validate_lifecycle_evidence(root: Path, errors: list[str]) -> None:
    """
    [参数] root: 仓库根目录；errors: 错误列表。
    [返回] 无返回值，子代理生命周期数量不一致时追加错误。
    最近修改时间：2026-07-22，原因：机器校验计划、启动、完成和关闭证据。
    """
    # 1. 读取当前实施轮次的真实生命周期记录。
    evidence_path = root / "doc/5-tests/2026-07-22_223221/control-plane-streamlining/evidence/subagent-lifecycle.json"
    if not evidence_path.is_file():
        fail(errors, "subagent lifecycle evidence missing")
        return
    evidence = json.loads(read(evidence_path))
    planned = evidence.get("planned_count")
    started = evidence.get("started_count")
    completed = evidence.get("completed_count")
    closed = evidence.get("closed_count")
    records = evidence.get("agents") or []

    # 2. 数量必须与逐 agent 记录一致，且并发峰值不能超过统一 Owner 的上限。
    if not all(isinstance(value, int) and value >= 0 for value in [planned, started, completed, closed]):
        fail(errors, "subagent lifecycle counts invalid")
        return
    if not (planned == started == completed == closed == len(records)):
        fail(errors, "subagent lifecycle counts mismatch")
    if evidence.get("max_active") is None or evidence.get("max_active") > 5:
        fail(errors, "subagent max_active exceeds 5 or is missing")
    for record in records:
        if record.get("status") != "completed" or record.get("closed") is not True:
            fail(errors, f"subagent lifecycle incomplete: {record.get('agent_id')}")
        for field in ["spawn_tool_result_observed", "completion_notification_observed", "close_tool_result_observed"]:
            if record.get(field) is not True:
                fail(errors, f"subagent runtime evidence missing: {record.get('agent_id')}: {field}")


def validate_post_delete(root: Path, errors: list[str]) -> None:
    """
    [参数] root: 仓库根目录；errors: 错误列表。
    [返回] 无返回值，退役目录、消费者或迁移资产不完整时追加错误。
    最近修改时间：2026-07-22，原因：为两个物理删除候选增加消费者与资产门禁。
    """
    # 1. 退役目录必须消失，目标 Owner 必须存在，活跃消费者必须清零。
    log("post-delete: 校验退役目录与活跃消费者")
    for source, target in RETIRE.items():
        if (root / source).exists():
            fail(errors, f"retired source still exists: {source}")
        if not (root / target / "SKILL.md").is_file():
            fail(errors, f"target owner missing: {target}")
        hits: list[str] = []
        for path in active_consumer_files(root):
            try:
                text = read(path)
            except UnicodeDecodeError:
                continue
            if source in text:
                hits.append(path.relative_to(root).as_posix())
        if hits:
            fail(errors, f"active consumers still reference {source}: {hits}")

    # 2. 迁移后的脚本、references 和项目记忆模板必须归属于最终 Owner。
    required_assets = [
        "parallel-task-dispatch-rules/scripts/generate_subagent_plan.py",
        "parallel-task-dispatch-rules/references/delegation-decision-matrix.md",
        "parallel-task-dispatch-rules/references/launch-plan-schema.md",
        "project-rule-file-bootstrap-rules/references/项目记忆模板/四件套模板.md",
    ]
    for relative in required_assets:
        if not (root / relative).is_file():
            fail(errors, f"migrated asset missing: {relative}")

    # 3. 生命周期证据必须证明真实启动、完成和关闭均已发生。
    validate_lifecycle_evidence(root, errors)


def main() -> int:
    """
    [参数] 无显式函数参数；从命令行读取仓库、manifest 和验证阶段。
    [返回] 验证通过返回 0，存在任何错误返回 1。
    最近修改时间：2026-07-22，原因：统一 baseline、trigger、post-delete 三阶段入口。
    """
    # 1. 解析命令行并初始化当前阶段的错误收集器。
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", required=True)
    parser.add_argument("--manifest", required=True)
    parser.add_argument("--phase", choices=["baseline", "trigger", "post-delete"], required=True)
    args = parser.parse_args()
    root = Path(args.repo_root).resolve()
    manifest_path = Path(args.manifest).resolve()
    errors: list[str] = []

    # 2. 所有阶段先验证同一份 manifest，再执行阶段专属门禁。
    manifest = validate_manifest(root, manifest_path, args.phase, errors)
    if args.phase == "baseline":
        validate_baseline(root, manifest_path, manifest, errors)
    elif args.phase == "trigger":
        validate_trigger(root, manifest_path, manifest, errors)
    else:
        validate_trigger(root, manifest_path, manifest, errors)
        validate_post_delete(root, errors)

    # 3. 输出机器可读结果，交由文档和最终验收证据引用。
    result = {"phase": args.phase, "valid": not errors, "errors": errors}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
