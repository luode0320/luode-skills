"""外部场景 YAML/JSON 加载、严格校验与来源漂移检查。"""

from __future__ import annotations

import hashlib
import json
import re
import uuid
from pathlib import Path
from typing import Any, Mapping

from .scenario_model import (
    SCENARIO_ACTIONS,
    SCENARIO_LIFECYCLES,
    SCENARIO_RISKS,
    SCENARIO_SCHEMA_VERSION,
    ExternalScenario,
    ScenarioCatalog,
    ScenarioStep,
    ScenarioValidationError,
    scenario_requires_cleanup,
)


CATALOG_FIELDS = {"schema_version", "scenarios"}
SCENARIO_FIELDS = {
    "scenario_id",
    "risk",
    "consumers",
    "source_evidence",
    "source_fingerprint",
    "lifecycle",
    "preconditions",
    "steps",
    "assertions",
    "cleanup",
    "verification",
}
STEP_FIELDS = {"step_id", "action", "config", "captures", "assertions", "parallel_group"}
VERIFICATION_GATE_FIELDS = ("contract_valid", "positive_passed", "fault_detected", "cleanup_passed", "source_current")
VERIFICATION_EVIDENCE_FIELDS = {"verification_run_id", "positive_result", "fault_result", "cleanup_result", "source_fingerprint", "artifact_path", "artifact_sha256"}
PROMOTION_METHOD = "external-verify/1.0"
PROMOTION_FIELDS = {"method", "candidate_fingerprint", "verification_digest"}
VERIFICATION_RUN_ID_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_-]{0,127}$")
VERIFICATION_ARTIFACT_SCHEMA = "external-verification-evidence/1.0"


def source_fingerprint(source_evidence: Any) -> str:
    """计算来源证据的稳定 SHA-256 指纹。

    [参数] source_evidence: OpenAPI、AsyncAPI、客户端或路由来源证据。
    [返回] 规范化 JSON 的 SHA-256 十六进制摘要。
    最近修改时间：2026-07-25 20:55:00，补齐来源漂移判定的稳定输入输出。
    """

    payload = json.dumps(source_evidence, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def _fingerprint_value(value: Any) -> Any:
    """把场景内存值规范化为可稳定摘要的 JSON 值。

    [参数] value: 场景身份、步骤、断言或清理中的任意声明值。
    [返回] 保持结构的 JSON 值；字节转换为长度和 SHA-256，不保留原文。
    最近修改时间：2026-07-25 23:15:00，支持 multipart 内存候选参与晋级指纹。
    """

    # 1. 映射和序列递归规范化，确保嵌套 multipart 配置也可稳定比较。
    if isinstance(value, Mapping):
        return {str(key): _fingerprint_value(child) for key, child in value.items()}
    if isinstance(value, (list, tuple)):
        return [_fingerprint_value(item) for item in value]
    # 2. 原始字节只绑定长度和摘要，既可检测漂移也不把内容写入 promotion 记录。
    if isinstance(value, bytes):
        return {"$bytes": {"length": len(value), "sha256": hashlib.sha256(value).hexdigest()}}
    return value


def scenario_candidate_fingerprint(scenario: ExternalScenario) -> str:
    """计算排除生命周期和验证记录的候选场景指纹。

    [参数] scenario: 已通过结构校验的候选或 verified 场景。
    [返回] 绑定身份、来源、步骤、断言和清理的 SHA-256 指纹。
    最近修改时间：2026-07-26 00:20:00，候选指纹与结构化运行证据共同组成晋级证明。
    """

    # 1. 生命周期和 verification 会在晋级时变化，必须排除以避免递归摘要。
    payload = scenario.to_dict()
    payload.pop("lifecycle", None)
    payload.pop("verification", None)
    encoded = json.dumps(_fingerprint_value(payload), ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(encoded.encode("utf-8")).hexdigest()


def _read_verification_artifact(project_root: str | Path | None, verification: Mapping[str, Any]) -> Mapping[str, Any] | None:
    """回读项目根内 verification artifact 并校验文件摘要。

    [参数] project_root: 场景所属项目根；verification: 含相对路径与 SHA-256 的晋级证据。
    [返回] 合法 artifact 映射；缺失、越界、解析或摘要失败时返回 None。
    最近修改时间：2026-07-26 00:55:00，verified 加载不再信任调用方自报结构化字典。
    """

    # 1. verified 必须显式提供项目根、相对路径和文件摘要，内存自报不能替代文件证据。
    if project_root is None:
        return None
    relative = Path(str(verification.get("artifact_path", "")))
    expected_digest = str(verification.get("artifact_sha256", ""))
    if not str(relative) or relative.is_absolute() or len(expected_digest) != 64:
        return None
    root = Path(project_root).resolve()
    path = (root / relative).resolve()
    try:
        path.relative_to(root)
        payload = path.read_bytes()
    except (ValueError, OSError):
        return None
    if hashlib.sha256(payload).hexdigest() != expected_digest:
        return None
    try:
        document = json.loads(payload.decode("utf-8"))
    except (UnicodeError, ValueError):
        return None
    return document if isinstance(document, Mapping) and document.get("schema_version") == VERIFICATION_ARTIFACT_SCHEMA else None


def _verification_evidence_valid(scenario: ExternalScenario, verification: Mapping[str, Any], project_root: str | Path | None) -> bool:
    """校验晋级输入是否绑定真实运行 artifact、故障识别和清理摘要。

    [参数] scenario: 待晋级或已晋级场景；verification: 五项门槛与结构化验证证据；project_root: artifact 所属项目根。
    [返回] 字段、文件、运行身份、状态、场景身份和来源全部一致时返回 True。
    最近修改时间：2026-07-26 00:55:00，晋级必须回读项目根内真实 verification artifact。
    """

    # 1. 晋级输入字段必须精确，五项结果仍需全真但不能替代文件证据。
    required = set(VERIFICATION_GATE_FIELDS) | VERIFICATION_EVIDENCE_FIELDS
    if set(verification) != required or any(verification.get(field) is not True for field in VERIFICATION_GATE_FIELDS):
        return False
    verification_run_id = str(verification.get("verification_run_id", ""))
    if not VERIFICATION_RUN_ID_PATTERN.fullmatch(verification_run_id) or verification.get("source_fingerprint") != scenario.source_fingerprint:
        return False

    # 2. 正向、故障和清理摘要必须来自具名运行，并与当前场景身份一致。
    positive = verification.get("positive_result")
    fault = verification.get("fault_result")
    cleanup = verification.get("cleanup_result")
    if not all(isinstance(item, Mapping) for item in (positive, fault, cleanup)):
        return False
    if set(positive) != {"verification_run_id", "run_id", "scenario_id", "status"} or set(fault) != {"verification_run_id", "run_id", "scenario_id", "status", "failure_type"} or set(cleanup) != {"verification_run_id", "run_id", "scenario_id", "status", "failed_steps"}:
        return False
    if any(item.get("verification_run_id") != verification_run_id for item in (positive, fault, cleanup)):
        return False
    if positive.get("scenario_id") != scenario.scenario_id or positive.get("status") != "PASS" or not str(positive.get("run_id", "")):
        return False
    if fault.get("scenario_id") != scenario.scenario_id or fault.get("status") != "FAIL" or not str(fault.get("run_id", "")) or not str(fault.get("failure_type", "")):
        return False
    if cleanup.get("scenario_id") != scenario.scenario_id or cleanup.get("status") != "PASS" or cleanup.get("run_id") != positive.get("run_id"):
        return False
    failed_steps = cleanup.get("failed_steps")
    if not (isinstance(failed_steps, int) and not isinstance(failed_steps, bool) and failed_steps == 0):
        return False

    # 3. 回读文件并逐字段对账；artifact 还必须绑定当前 candidate 指纹和 verification run。
    artifact = _read_verification_artifact(project_root, verification)
    if artifact is None:
        return False
    expected_artifact = {
        "schema_version": VERIFICATION_ARTIFACT_SCHEMA,
        "scenario_id": scenario.scenario_id,
        "candidate_fingerprint": scenario_candidate_fingerprint(scenario),
        "verification_run_id": verification_run_id,
        "positive_result": dict(positive),
        "fault_result": dict(fault),
        "cleanup_result": dict(cleanup),
        "source_fingerprint": scenario.source_fingerprint,
    }
    return dict(artifact) == expected_artifact


def persist_verification_artifact(
    project_root: str | Path,
    scenario: ExternalScenario,
    *,
    verification_run_id: str,
    positive_result: Mapping[str, Any],
    fault_result: Mapping[str, Any],
    cleanup_result: Mapping[str, Any],
) -> dict[str, str]:
    """持久化 candidate 晋级所需的脱敏运行 evidence。

    [参数] project_root/scenario/verification_run_id/positive_result/fault_result/cleanup_result: 项目根、候选和三类真实验证结果。
    [返回] 项目根内 artifact 相对路径与文件 SHA-256。
    最近修改时间：2026-07-26 00:55:00，为 external-verify 建立可回读的晋级文件证据。
    """

    # 1. 只提取门禁机器字段，构造前先拒绝非法验证批次和结果形状。
    if not VERIFICATION_RUN_ID_PATTERN.fullmatch(str(verification_run_id)):
        raise ScenarioValidationError([f"scenarios.{scenario.scenario_id} verification run id is invalid"])
    positive = {"verification_run_id": verification_run_id, **{key: positive_result.get(key) for key in ("run_id", "scenario_id", "status")}}
    fault = {"verification_run_id": verification_run_id, **{key: fault_result.get(key) for key in ("run_id", "scenario_id", "status", "failure_type")}}
    cleanup = {"verification_run_id": verification_run_id, **{key: cleanup_result.get(key) for key in ("run_id", "scenario_id", "status", "failed_steps")}}
    if positive.get("scenario_id") != scenario.scenario_id or positive.get("status") != "PASS" or not positive.get("run_id"):
        raise ScenarioValidationError([f"scenarios.{scenario.scenario_id} positive verification result is invalid"])
    if fault.get("scenario_id") != scenario.scenario_id or fault.get("status") != "FAIL" or not fault.get("run_id") or not fault.get("failure_type"):
        raise ScenarioValidationError([f"scenarios.{scenario.scenario_id} fault verification result is invalid"])
    if cleanup.get("scenario_id") != scenario.scenario_id or cleanup.get("status") != "PASS" or cleanup.get("run_id") != positive.get("run_id") or cleanup.get("failed_steps") != 0:
        raise ScenarioValidationError([f"scenarios.{scenario.scenario_id} cleanup verification result is invalid"])

    # 2. 在 mkdir 前拒绝指向项目根外的既有 symlink，文件名使用 candidate 与批次摘要。
    root = Path(project_root).resolve()
    evidence_root = root / ".release-test-engine"
    evidence_dir = evidence_root / "verification-evidence"
    for candidate in (evidence_root, evidence_dir):
        if candidate.exists() or candidate.is_symlink():
            try:
                candidate.resolve().relative_to(root)
            except ValueError as exc:
                raise PermissionError("VERIFICATION_EVIDENCE_PATH_OUTSIDE_PROJECT") from exc
    evidence_dir.mkdir(parents=True, exist_ok=True)
    file_key = hashlib.sha256(f"{scenario.scenario_id}:{verification_run_id}".encode("utf-8")).hexdigest()
    final_path = evidence_dir / f"{file_key}.json"
    if final_path.exists() or final_path.is_symlink():
        raise FileExistsError("VERIFICATION_EVIDENCE_ALREADY_EXISTS")

    # 3. artifact 绑定当前 candidate、验证批次、三类结果和来源，使用随机临时文件原子写入。
    document = {
        "schema_version": VERIFICATION_ARTIFACT_SCHEMA,
        "scenario_id": scenario.scenario_id,
        "candidate_fingerprint": scenario_candidate_fingerprint(scenario),
        "verification_run_id": verification_run_id,
        "positive_result": positive,
        "fault_result": fault,
        "cleanup_result": cleanup,
        "source_fingerprint": scenario.source_fingerprint,
    }
    payload = (json.dumps(document, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")
    temporary_path = evidence_dir / f".{file_key}.{uuid.uuid4().hex}.tmp"
    created = False
    try:
        with temporary_path.open("xb") as stream:
            created = True
            stream.write(payload)
        temporary_path.replace(final_path)
    finally:
        if created and (temporary_path.exists() or temporary_path.is_symlink()):
            temporary_path.unlink()
    return {"artifact_path": final_path.relative_to(root).as_posix(), "artifact_sha256": hashlib.sha256(payload).hexdigest()}


def build_verification_evidence(
    scenario: ExternalScenario,
    *,
    project_root: str | Path,
    artifact_path: str,
    artifact_sha256: str,
) -> dict[str, Any]:
    """从项目根内真实 artifact 构造 candidate 晋级输入。

    [参数] scenario: 已加载 candidate；project_root: 项目根；artifact_path/artifact_sha256: evidence 相对路径和文件摘要。
    [返回] 由 artifact 推导五项门槛并绑定运行摘要、来源和文件身份的晋级输入。
    最近修改时间：2026-07-26 00:55:00，调用方状态字典不再直接成为晋级依据。
    """

    # 1. 先只用路径和摘要回读 artifact，再从文件内容派生全部状态字段。
    reference = {"artifact_path": artifact_path, "artifact_sha256": artifact_sha256}
    artifact = _read_verification_artifact(project_root, reference)
    if artifact is None:
        raise ScenarioValidationError([f"scenarios.{scenario.scenario_id} verification artifact is invalid"])
    evidence = {
        "contract_valid": True,
        "positive_passed": artifact.get("positive_result", {}).get("status") == "PASS",
        "fault_detected": artifact.get("fault_result", {}).get("status") == "FAIL" and bool(artifact.get("fault_result", {}).get("failure_type")),
        "cleanup_passed": artifact.get("cleanup_result", {}).get("status") == "PASS" and artifact.get("cleanup_result", {}).get("failed_steps") == 0,
        "source_current": artifact.get("source_fingerprint") == scenario.source_fingerprint,
        "verification_run_id": artifact.get("verification_run_id"),
        "positive_result": artifact.get("positive_result"),
        "fault_result": artifact.get("fault_result"),
        "cleanup_result": artifact.get("cleanup_result"),
        "source_fingerprint": artifact.get("source_fingerprint"),
        **reference,
    }
    # 2. 构造入口自身再次执行候选、文件和摘要全量对账。
    if not _verification_evidence_valid(scenario, evidence, project_root):
        raise ScenarioValidationError([f"scenarios.{scenario.scenario_id} verification evidence is invalid"])
    return evidence

def promotion_verification_digest(scenario: ExternalScenario, verification: Mapping[str, Any]) -> str:
    """计算绑定候选与结构化运行证据的晋级摘要。

    [参数] scenario: 待验证场景；verification: 五项门槛、运行摘要及晋级元数据。
    [返回] external-verify/1.0 晋级记录的稳定 SHA-256 摘要。
    最近修改时间：2026-07-26 00:20:00，摘要绑定正向、故障、清理、来源和 verification run。
    """

    # 1. 摘要绑定冻结方法、候选指纹和全部脱敏验证证据，任一运行摘要漂移都会失效。
    candidate_fingerprint = scenario_candidate_fingerprint(scenario)
    evidence_fields = set(VERIFICATION_GATE_FIELDS) | VERIFICATION_EVIDENCE_FIELDS
    payload = {
        "method": PROMOTION_METHOD,
        "candidate_fingerprint": candidate_fingerprint,
        "verification_evidence": {field: verification.get(field) for field in sorted(evidence_fields)},
    }
    encoded = json.dumps(_fingerprint_value(payload), ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(encoded.encode("utf-8")).hexdigest()

def _load_document(source: str | Path | Mapping[str, Any]) -> Mapping[str, Any]:
    """从内存映射或 UTF-8 local 文件读取场景目录。

    [参数] source: 场景映射或 YAML/JSON 文件路径。
    [返回] 目录根对象；读取、解析或根类型错误时抛出契约异常。
    最近修改时间：2026-07-25 20:55:00，明确文件读取和解析失败边界。
    """

    # 1. 调用方已提供映射时直接复用，不进行文件系统写入。
    if isinstance(source, Mapping):
        return source
    # 2. 文件来源固定按 UTF-8 读取，编码或 IO 错误统一转成场景契约错误。
    path = Path(source)
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        raise ScenarioValidationError([f"catalog read failed: {exc}"]) from exc
    # 3. JSON 与 YAML 共享同一根对象契约，缺少 YAML runtime 时禁止伪造解析成功。
    try:
        # 3.1 文件扩展名只决定 JSON 或 YAML 解析器，不改变后续根对象契约。
        if path.suffix.lower() == ".json":
            value = json.loads(text)
        else:
            import yaml

            value = yaml.safe_load(text)
    except (ImportError, ValueError) as exc:
        raise ScenarioValidationError([f"catalog parse failed: {exc}"]) from exc
    # 4. 解析结果必须是映射，数组或标量不能进入后续场景加载。
    if not isinstance(value, Mapping):
        raise ScenarioValidationError(["catalog root must be an object"])
    return value


def _mapping_list(value: Any, path: str, errors: list[str]) -> tuple[Mapping[str, Any], ...]:
    """校验并复制对象数组。

    [参数] value: 待校验值；path: 错误字段路径；errors: 聚合错误列表。
    [返回] 只包含浅复制映射的不可变元组，非法时返回空元组。
    最近修改时间：2026-07-25 20:55:00，补齐目录数组字段的错误聚合说明。
    """

    if not isinstance(value, list) or any(not isinstance(item, Mapping) for item in value):
        errors.append(f"{path} must be an array of objects")
        return ()
    return tuple(dict(item) for item in value)


def _parse_step(value: Any, path: str, errors: list[str]) -> ScenarioStep | None:
    """把单个步骤映射解析为白名单场景步骤。

    [参数] value: 原始步骤值；path: 步骤字段路径；errors: 聚合错误列表。
    [返回] 可执行步骤；根类型错误时返回 None。
    最近修改时间：2026-07-25 20:55:00，明确未知字段、动作和 JSON Pointer 的拒绝边界。
    """

    # 1. 步骤根值必须是映射，未知字段和缺失身份统一加入契约错误。
    if not isinstance(value, Mapping):
        errors.append(f"{path} must be an object")
        return None
    unknown = set(value) - STEP_FIELDS
    if unknown:
        errors.append(f"{path} has unknown fields: {sorted(unknown)}")
    step_id = str(value.get("step_id", "")).strip()
    action = str(value.get("action", "")).strip()
    if not step_id:
        errors.append(f"{path}.step_id is required")
    if action not in SCENARIO_ACTIONS:
        errors.append(f"{path}.action is not allowed")
    # 2. 配置必须是映射，捕获路径必须全部是结构化 JSON Pointer。
    config = value.get("config", {})
    captures = value.get("captures", {})
    if not isinstance(config, Mapping):
        errors.append(f"{path}.config must be an object")
        config = {}
    if not isinstance(captures, Mapping) or any(not str(item).startswith("/") for item in captures.values()):
        errors.append(f"{path}.captures must contain JSON Pointer values")
        captures = {}
    assertions = _mapping_list(value.get("assertions", []), f"{path}.assertions", errors)
    return ScenarioStep(step_id, action, dict(config), dict(captures), assertions, str(value.get("parallel_group", "")))


def _parse_scenario(key: str, value: Any, errors: list[str], project_root: str | Path | None = None) -> ExternalScenario | None:
    """校验并构造单个消费者场景。

    [参数] key: catalog 映射键；value: 场景原始值；errors: 聚合错误列表；project_root: verified artifact 根。
    [返回] 不可变外部场景；根类型错误时返回 None。
    最近修改时间：2026-07-26 01:20:00，verified 加载时回读 artifact 并重算两层证明。
    """

    if not isinstance(value, Mapping):
        errors.append(f"scenarios.{key} must be an object")
        return None
    # 1. 固定字段和身份，避免执行模型自行补默认契约。
    unknown = set(value) - SCENARIO_FIELDS
    missing = SCENARIO_FIELDS - set(value)
    if unknown:
        errors.append(f"scenarios.{key} has unknown fields: {sorted(unknown)}")
    if missing:
        errors.append(f"scenarios.{key} missing fields: {sorted(missing)}")
    scenario_id = str(value.get("scenario_id", "")).strip()
    if scenario_id != key:
        errors.append(f"scenarios.{key}.scenario_id must match catalog key")
    risk = str(value.get("risk", ""))
    lifecycle = str(value.get("lifecycle", ""))
    if risk not in SCENARIO_RISKS:
        errors.append(f"scenarios.{key}.risk is invalid")
    if lifecycle not in SCENARIO_LIFECYCLES:
        errors.append(f"scenarios.{key}.lifecycle is invalid")

    # 2. 校验来源指纹、消费者和步骤，来源漂移必须在执行前显式暴露。
    consumers = value.get("consumers", [])
    if not isinstance(consumers, list) or not consumers or any(not str(item).strip() for item in consumers):
        errors.append(f"scenarios.{key}.consumers must be a non-empty string array")
        consumers = []
    evidence = _mapping_list(value.get("source_evidence", []), f"scenarios.{key}.source_evidence", errors)
    fingerprint = str(value.get("source_fingerprint", ""))
    if fingerprint != source_fingerprint(list(evidence)):
        errors.append(f"scenarios.{key}.source_fingerprint drifted")
    steps_value = value.get("steps", [])
    if not isinstance(steps_value, list) or not steps_value:
        errors.append(f"scenarios.{key}.steps must be a non-empty array")
        steps_value = []
    steps = tuple(item for index, raw in enumerate(steps_value) if (item := _parse_step(raw, f"scenarios.{key}.steps[{index}]", errors)) is not None)
    if len({item.step_id for item in steps}) != len(steps):
        errors.append(f"scenarios.{key}.step_id values must be unique")

    # 3. 前置条件只允许声明 local 环境，未知条件不能在运行时被静默忽略。
    preconditions = _mapping_list(value.get("preconditions", []), f"scenarios.{key}.preconditions", errors)
    if not preconditions:
        errors.append(f"scenarios.{key}.preconditions must declare local environment")
    for index, condition in enumerate(preconditions):
        if set(condition) != {"environment"} or condition.get("environment") != "local":
            errors.append(f"scenarios.{key}.preconditions[{index}] must be environment: local")
    assertions = _mapping_list(value.get("assertions", []), f"scenarios.{key}.assertions", errors)
    cleanup = _mapping_list(value.get("cleanup", []), f"scenarios.{key}.cleanup", errors)
    verification = value.get("verification", {})
    if not isinstance(verification, Mapping):
        errors.append(f"scenarios.{key}.verification must be an object")
        verification = {}

    # 4. verified 资产必须带可重算晋级证明；五个布尔值本身不能证明经历过验证入口。
    verification_evidence_fields = set(VERIFICATION_GATE_FIELDS) | VERIFICATION_EVIDENCE_FIELDS
    required_verification = verification_evidence_fields | PROMOTION_FIELDS
    scenario = ExternalScenario(scenario_id, risk, tuple(str(item) for item in consumers), evidence, fingerprint, lifecycle, preconditions, steps, assertions, cleanup, dict(verification))
    if lifecycle == "verified":
        # 4.1 字段全集、方法、运行证据和五项门槛必须完全匹配冻结契约。
        evidence_input = {field: verification.get(field) for field in verification_evidence_fields}
        if set(verification) != required_verification or not _verification_evidence_valid(scenario, evidence_input, project_root):
            errors.append(f"scenarios.{key}.verified lifecycle requires structured runtime verification evidence")
        elif verification.get("method") != PROMOTION_METHOD:
            errors.append(f"scenarios.{key}.verification promotion method is invalid")
        else:
            # 4.2 loader 重算候选与验证摘要，任何步骤、来源、运行摘要或清理漂移都会失效。
            candidate_fingerprint = scenario_candidate_fingerprint(scenario)
            if verification.get("candidate_fingerprint") != candidate_fingerprint:
                errors.append(f"scenarios.{key}.verification candidate fingerprint is invalid")
            if verification.get("verification_digest") != promotion_verification_digest(scenario, verification):
                errors.append(f"scenarios.{key}.verification digest is invalid")
    if lifecycle == "verified" and scenario_requires_cleanup(scenario) and not cleanup:
        errors.append(f"scenarios.{key}.verified write scenario requires cleanup")
    return scenario


def load_scenario_catalog(source: str | Path | Mapping[str, Any], *, project_root: str | Path | None = None) -> ScenarioCatalog:
    """加载并严格校验 `external-scenario/1.0` 场景目录。

    [参数] source: 场景映射或 local YAML/JSON 路径；project_root: verified artifact 所属项目根。
    [返回] 通过全部结构校验的场景目录。
    最近修改时间：2026-07-26 01:20:00，目录加载增加 verified artifact 项目根。
    """

    # 1. 先校验目录版本和场景映射，再逐场景聚合全部契约错误。
    document = _load_document(source)
    errors: list[str] = []
    unknown = set(document) - CATALOG_FIELDS
    if unknown:
        errors.append(f"catalog has unknown fields: {sorted(unknown)}")
    if document.get("schema_version") != SCENARIO_SCHEMA_VERSION:
        errors.append(f"schema_version must be {SCENARIO_SCHEMA_VERSION}")
    raw_scenarios = document.get("scenarios")
    if not isinstance(raw_scenarios, Mapping):
        errors.append("scenarios must be an object")
        raw_scenarios = {}
    scenarios = {str(key): item for key, value in raw_scenarios.items() if (item := _parse_scenario(str(key), value, errors, project_root)) is not None}
    # 2. 任一错误都会阻断整个目录，禁止只运行其中看似合法的子集。
    if errors:
        raise ScenarioValidationError(errors)
    return ScenarioCatalog(SCENARIO_SCHEMA_VERSION, scenarios)


def can_promote_to_verified(scenario: ExternalScenario, verification: Mapping[str, Any], *, project_root: str | Path | None = None) -> bool:
    """判断 candidate 是否具备完整结构化验证证据。

    [参数] scenario: 当前候选场景；verification: 文件绑定验证证据；project_root: artifact 项目根。
    [返回] 生命周期为 candidate 且结构化运行证据完整一致时返回 True。
    最近修改时间：2026-07-26 01:20:00，晋级前回读项目根内 evidence 文件。
    """

    # 1. 生命周期和结构化证据必须同时满足，布尔门槛不能脱离运行摘要单独使用。
    return scenario.lifecycle == "candidate" and _verification_evidence_valid(scenario, verification, project_root)


def promote_to_verified(scenario: ExternalScenario, verification: Mapping[str, Any], *, project_root: str | Path) -> ExternalScenario:
    """用结构化验证证据生成不可变的 verified 场景副本。

    [参数] scenario: 待晋级候选；verification: 文件绑定验证输入；project_root: artifact 项目根。
    [返回] 重新经过完整 loader 校验的 verified 场景。
    最近修改时间：2026-07-26 01:20:00，晋级和 loader 双重回读验证 artifact。
    """

    # 1. 任一运行证据缺失、身份不符或当前生命周期错误时立即拒绝晋级。
    if not can_promote_to_verified(scenario, verification, project_root=project_root):
        raise ScenarioValidationError([f"scenarios.{scenario.scenario_id} cannot be promoted to verified"])
    # 2. 通过后生成新文档并重新走完整 loader，避免复制对象绕过其它契约。
    value = scenario.to_dict()
    value["lifecycle"] = "verified"
    promotion = dict(verification)
    promotion["method"] = PROMOTION_METHOD
    promotion["candidate_fingerprint"] = scenario_candidate_fingerprint(scenario)
    promotion["verification_digest"] = promotion_verification_digest(scenario, promotion)
    value["verification"] = promotion
    document = {"schema_version": SCENARIO_SCHEMA_VERSION, "scenarios": {scenario.scenario_id: value}}
    return load_scenario_catalog(document, project_root=project_root).scenarios[scenario.scenario_id]
