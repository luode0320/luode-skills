"""测试专用的结构化场景晋级文件证据。"""

from __future__ import annotations

import tempfile
import uuid
from pathlib import Path
from typing import Any, Mapping

from release_test_engine.scenario_loader import build_verification_evidence, persist_verification_artifact, promote_to_verified
from release_test_engine.scenario_model import ExternalScenario


_VERIFICATION_DIRECTORY = tempfile.TemporaryDirectory(prefix="external-verification-fixture-")


def verification_project_root() -> Path:
    """返回当前测试进程独占的 verification artifact 项目根。

    [参数] 无。
    [返回] 进程退出时由 TemporaryDirectory 自动清理的 local 临时项目根。
    最近修改时间：2026-07-26 01:05:00，为 verified loader 提供真实文件回读根目录。
    """

    # 1. 所有测试 artifact 只写入系统临时目录，不进入仓库或外部环境。
    return Path(_VERIFICATION_DIRECTORY.name)


def verification_evidence(scenario: ExternalScenario, *, project_root: Path | None = None) -> dict[str, Any]:
    """为已由测试 fixture 覆盖的 candidate 写入并回读验证 artifact。

    [参数] scenario: 即将进入真实协议测试的 candidate 场景；project_root: 可选的调用方临时项目根。
    [返回] 绑定正向运行、故障识别、清理、来源、文件路径和 SHA-256 的晋级输入。
    最近修改时间：2026-07-26 01:05:00，测试不再用内存状态字典直接晋级。
    """

    # 1. 每次使用唯一 verification run，避免不同测试共享或覆盖证据文件。
    verification_run_id = f"fixture-{uuid.uuid4().hex}"
    positive_run_id = f"positive-{uuid.uuid4().hex}"
    root = project_root.resolve() if project_root is not None else verification_project_root()
    reference = persist_verification_artifact(
        root,
        scenario,
        verification_run_id=verification_run_id,
        positive_result={"run_id": positive_run_id, "scenario_id": scenario.scenario_id, "status": "PASS"},
        fault_result={"run_id": f"fault-{uuid.uuid4().hex}", "scenario_id": scenario.scenario_id, "status": "FAIL", "failure_type": "FAULT_INJECTION_DETECTED"},
        cleanup_result={"run_id": positive_run_id, "scenario_id": scenario.scenario_id, "status": "PASS", "failed_steps": 0},
    )
    # 2. 构造器必须从刚写入的真实文件回读摘要，不复用调用方内存映射。
    return build_verification_evidence(scenario, project_root=root, artifact_path=reference["artifact_path"], artifact_sha256=reference["artifact_sha256"])


def promote_fixture_scenario(scenario: ExternalScenario, *, project_root: Path | None = None) -> ExternalScenario:
    """通过测试 artifact 和正式晋级入口生成 verified 场景。

    [参数] scenario: 已加载 candidate；project_root: 可选的调用方临时项目根。
    [返回] loader 已回读 verification 文件并验签的 verified 场景。
    最近修改时间：2026-07-26 01:05:00，集中测试晋级的项目根与文件证据传递。
    """

    # 1. 先写文件证据，再由正式 promote 和 loader 使用同一项目根完成双重回读。
    root = project_root.resolve() if project_root is not None else verification_project_root()
    return promote_to_verified(scenario, verification_evidence(scenario, project_root=root), project_root=root)


def load_verified_catalog(document: Mapping[str, Any]):
    """使用测试 verification 项目根回读 verified 目录。

    [参数] document: 含 artifact 相对路径与 SHA-256 的场景目录。
    [返回] 通过正式 loader 文件复核的 ScenarioCatalog。
    最近修改时间：2026-07-26 01:05:00，避免 verified 映射绕过 artifact root。
    """

    # 1. 延迟导入保持测试 fixture 只暴露最小公共入口。
    from release_test_engine.scenario_loader import load_scenario_catalog

    return load_scenario_catalog(document, project_root=verification_project_root())
