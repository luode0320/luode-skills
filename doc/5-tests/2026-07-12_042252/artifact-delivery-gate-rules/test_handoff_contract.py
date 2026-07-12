#!/usr/bin/env python3
"""T01-02 研发文档零决策交接契约与 profile 的本地正反验证。"""

from __future__ import annotations

import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable


if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


# 测试资产位于 doc/5-tests/<timestamp>/ 下，向上回到仓库根目录读取被测资产。
ROOT = Path(__file__).resolve().parents[4]
SCRIPT_DIR = ROOT / "artifact-delivery-gate-rules" / "scripts"
sys.path.insert(0, str(SCRIPT_DIR))

import validate_engineering_docs as validator  # noqa: E402


PROFILE_FILE = ROOT / "artifact-delivery-gate-rules" / "references" / "document-quality-profiles.yaml"
CONTRACT_FILE = ROOT / "artifact-delivery-gate-rules" / "references" / "document-handoff-contract.md"
FIXTURE_DIR = Path(__file__).resolve().parent / "fixtures"


def log(kind: str, message: str) -> None:
    """输出可回放的测试过程日志。

    [参数] kind：日志阶段；message：阶段信息。
    [返回] 无。
    最近修改时间：2026-07-12 04:28:00；补齐测试证据脚本的过程日志元信息。
    """

    timestamp = datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")
    print(f"[{timestamp}] {kind}: {message}", flush=True)


def require(condition: bool, message: str) -> None:
    """在断言失败时记录失败点并终止当前测试。

    [参数] condition：断言结果；message：失败原因。
    [返回] 无；条件不满足时抛出 AssertionError。
    最近修改时间：2026-07-12 04:28:00；补齐负例失败路由。
    """

    if not condition:
        log("失败点", message)
        raise AssertionError(message)


def read_utf8(path: Path) -> str:
    """以 UTF-8 读取测试输入并拒绝缺失或乱码文件。

    [参数] path：待读取文件路径。
    [返回] 文件文本。
    最近修改时间：2026-07-12 04:28:00；固定测试证据输入编码。
    """

    require(path.is_file(), f"文件不存在: {path}")
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError as error:
        raise AssertionError(f"文件不是有效 UTF-8: {path}: {error}") from error


def positive_profile_cases(payload: dict) -> Iterable[tuple[str, Path]]:
    """枚举五类 profile 对应的当前正式文档正例。

    [参数] payload：已加载的质量 profile 配置。
    [返回] profile 名称与文档路径迭代器。
    最近修改时间：2026-07-12 04:28:00；补齐五类 profile 覆盖入口。
    """

    documents = {
        "requirement": ROOT / "doc/2-需求/2026-07-12_033322_需求与实施文档极致完备化.md",
        "acceptance": ROOT / "doc/7-验收/2026-07-12_033322_需求与实施文档极致完备化_验收标准.md",
        "implementation_master": ROOT / "doc/3-实施/2026-07-12_033322_需求与实施文档极致完备化_需求与实施计划全量顺序实施方案.md",
        "implementation_overview": ROOT / "doc/3-实施/2026-07-12_033322_需求与实施文档极致完备化_实施总览.md",
        "implementation_cycle": ROOT / "doc/3-实施/2026-07-12_033322_需求与实施文档极致完备化_实施周期01_契约与基线.md",
    }
    for profile_name, document in documents.items():
        require(profile_name in payload["profiles"], f"profile 缺失: {profile_name}")
        yield profile_name, document


def test_positive_profiles(payload: dict) -> None:
    """验证五类正式文档均通过对应 profile。

    [参数] payload：已加载的质量 profile 配置。
    [返回] 无；任一正例失败时抛出 AssertionError。
    最近修改时间：2026-07-12 04:28:00；增加 T01-02 正例证据。
    """

    log("步骤", "执行五类文档 profile 正例校验")
    # 1. 逐个运行 profile，确保失败能定位到具体文档类型。
    for profile_name, document in positive_profile_cases(payload):
        profile = payload["profiles"][profile_name]
        result = validator.validate_document(document, profile_name, profile, payload, ROOT)
        require(result["valid"], f"{profile_name} 正例失败: {result['errors']}")
        log("步骤", f"{profile_name} PASS: {document.relative_to(ROOT)}")


def test_contract_and_profiles(payload: dict) -> None:
    """验证交接契约关键条款和五类 profile 的字段矩阵。

    [参数] payload：已加载的质量 profile 配置。
    [返回] 无；关键条款或字段缺失时抛出 AssertionError。
    最近修改时间：2026-07-12 04:28:00；增加契约静态证据。
    """

    log("步骤", "检查交接契约关键条款与 profile 字段矩阵")
    # 1. 读取契约并检查普通模型交接所依赖的硬约束。
    contract = read_utf8(CONTRACT_FILE)
    required_terms = (
        "MUST",
        "CONDITIONAL MUST",
        "N/A",
        "双向追踪矩阵",
        "覆盖率低于 100%",
        "Mermaid 真解析",
        "普通模型执行演练",
    )
    # 2. 检查五类 profile 均具备可机械解释的字段集合。
    for term in required_terms:
        require(term in contract, f"交接契约缺少关键条款: {term}")
    expected_profiles = {
        "requirement",
        "acceptance",
        "implementation_master",
        "implementation_overview",
        "implementation_cycle",
    }
    actual_profiles = set(payload["profiles"])
    require(expected_profiles.issubset(actual_profiles), "profile 集合未覆盖五类文档")
    required_keys = {"required_sections", "id_prefixes", "diagrams", "min_tables", "required_phrases"}
    for name in sorted(expected_profiles):
        missing = required_keys.difference(payload["profiles"][name])
        require(not missing, f"{name} profile 缺少字段: {sorted(missing)}")
    log("步骤", "交接契约与 profile 关键条款 PASS")


def test_negative_fixtures(payload: dict) -> None:
    """验证缺章节、占位词和 N/A 无证据负例均被阻断。

    [参数] payload：已加载的质量 profile 配置。
    [返回] 无；任一负例被放行或错误类型不匹配时抛出 AssertionError。
    最近修改时间：2026-07-12 04:28:00；新增 T01-02 负例证据。
    """

    log("步骤", "执行缺章节、占位词和 N/A 无证据负例")
    cases = (
        (
            "acceptance 缺章节",
            "acceptance",
            FIXTURE_DIR / "acceptance_missing_section.md",
            "missing required section: 验收场景",
        ),
        (
            "requirement 占位词",
            "requirement",
            FIXTURE_DIR / "requirement_placeholder.md",
            "placeholder or vague terms found",
        ),
        (
            "implementation_cycle N/A 无证据",
            "implementation_cycle",
            FIXTURE_DIR / "implementation_cycle_na_without_reason.md",
            "N/A requires reason/evidence",
        ),
    )
    # 1. 每个负例独立执行，避免一个错误掩盖其它失败点。
    for label, profile_name, document, expected_error in cases:
        profile = payload["profiles"][profile_name]
        result = validator.validate_document(document, profile_name, profile, payload, ROOT)
        require(not result["valid"], f"负例错误放行: {label}")
        require(any(expected_error in error for error in result["errors"]), f"负例未命中预期错误: {label}; {result['errors']}")
        log("步骤", f"{label} BLOCKED 按预期")


def test_positive_na_reason() -> None:
    """验证带原因和证据的 N/A 字段不会被误报。

    [参数] 无。
    [返回] 无；误报时抛出 AssertionError。
    最近修改时间：2026-07-12 04:28:00；补齐 N/A 条件字段正例。
    """

    log("步骤", "执行 N/A 有原因与证据正例")
    # 1. 直接调用 N/A 规则函数，隔离正例语义而不依赖其它章节。
    errors: list[str] = []
    text = read_utf8(FIXTURE_DIR / "na_with_reason.md")
    validator.check_na_reasons(text, errors)
    require(errors == [], f"N/A 合规正例误报: {errors}")
    log("步骤", "N/A 有原因与证据 PASS")


def main() -> int:
    """执行 T01-02 全部静态正反验证并返回进程状态。

    [参数] 无。
    [返回] 0 表示通过，1 表示断言或输入错误。
    最近修改时间：2026-07-12 04:28:00；建立可复验的测试入口。
    """

    log("开始", "T01-02 交接契约与质量 profile local 只读验证")
    log("步骤", f"仓库根目录: {ROOT}")
    try:
        # 1. 加载 UTF-8 profile，再按契约、正例、负例顺序执行。
        payload = validator.load_profiles(PROFILE_FILE)
        test_contract_and_profiles(payload)
        test_positive_profiles(payload)
        test_negative_fixtures(payload)
        test_positive_na_reason()
    except (AssertionError, KeyError, OSError, TypeError, ValueError) as error:
        log("结束", f"FAIL: {error}")
        return 1
    log("结束", "PASS: 五类 profile、契约条款、正反 fixture 均符合预期")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
