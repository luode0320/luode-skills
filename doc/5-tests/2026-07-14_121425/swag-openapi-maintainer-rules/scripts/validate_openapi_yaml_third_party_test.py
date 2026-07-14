"""离线验证 swag 根目录与上游子目录递归校验行为。"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any

from fixtures_builder import build_fixture


ROOT = Path(__file__).resolve().parents[5]
VALIDATOR = ROOT / "swag-openapi-maintainer-rules" / "scripts" / "validate_openapi_yaml.py"
TMP_ROOT = Path("D:/tmp")


def log(message: str) -> None:
    """[参数] message 为过程日志文本。
    [返回] 无。
    最近修改时间: 2026-07-14 12:14:25，补充离线测试过程日志。
    """
    print(message, flush=True)


def require(condition: bool, message: str) -> None:
    """[参数] condition 为断言条件，message 为失败摘要。
    [返回] 无；条件不满足时抛出 AssertionError。
    最近修改时间: 2026-07-14 12:14:25，统一 fixture 断言输出。
    """
    if not condition:
        raise AssertionError(message)


def run_validator(swag_dir: Path, expected_exit: int) -> tuple[dict[str, Any], str]:
    """[参数] swag_dir 为待校验目录，expected_exit 为预期退出码。
    [返回] 返回 JSON 结果和完整标准错误输出。
    最近修改时间: 2026-07-14 12:14:25，新增递归校验退出码断言。
    """
    # 1. 通过 CLI 验证真实入口、退出码和机器可解析 JSON。
    env = os.environ.copy()
    env["PYTHONUTF8"] = "1"
    completed = subprocess.run(
        [sys.executable, str(VALIDATOR), "--swag-dir", str(swag_dir)],
        capture_output=True,
        text=True,
        encoding="utf-8",
        env=env,
        check=False,
    )
    require(completed.returncode == expected_exit, f"退出码不符: expected={expected_exit}, actual={completed.returncode}\n{completed.stdout}\n{completed.stderr}")
    try:
        result = json.loads(completed.stdout)
    except json.JSONDecodeError as error:
        raise AssertionError(f"标准输出不是 JSON: {completed.stdout}") from error
    return result, completed.stderr


def test_valid() -> None:
    """[参数] 无。
    [返回] 无；正例失败时抛出断言异常。
    最近修改时间: 2026-07-14 12:14:25，覆盖根与上游正例。
    """
    log("[用例 1/7] 正例开始")
    with tempfile.TemporaryDirectory(prefix="swag-valid-", dir=TMP_ROOT) as path:
        result, _ = run_validator(build_fixture(Path(path), "valid"), 0)
        require(result["valid"] is True, "正例根 valid 应为 true")
        require(result["third_party"][0]["valid"] is True, "正例上游 valid 应为 true")
    log("[用例 1/7] 正例通过")


def test_missing_chinese_description() -> None:
    """[参数] 无。
    [返回] 无；预期错误未命中时抛出断言异常。
    最近修改时间: 2026-07-14 12:14:25，覆盖上游中文说明隔离。
    """
    log("[用例 2/7] 上游中文说明缺失开始")
    with tempfile.TemporaryDirectory(prefix="swag-missing-description-", dir=TMP_ROOT) as path:
        result, _ = run_validator(build_fixture(Path(path), "missing_chinese_description"), 1)
        require(result["valid"] is True, "缺中文说明时根 scope 应保持通过")
        require(result["third_party"][0]["valid"] is False, "缺中文说明应只击中上游 scope")
        require(any("missing Chinese description" in item for item in result["third_party"][0]["errors"]), "缺中文说明错误未命中")
        require(result["errors"] == [], "根 scope 不应被上游字段错误污染")
    log("[用例 2/7] 上游中文说明缺失通过")


def test_manifest_mismatch() -> None:
    """[参数] 无。
    [返回] 无；预期错误未命中时抛出断言异常。
    最近修改时间: 2026-07-14 12:14:25，覆盖 manifest 文件映射。
    """
    log("[用例 3/7] manifest 映射不匹配开始")
    with tempfile.TemporaryDirectory(prefix="swag-manifest-mismatch-", dir=TMP_ROOT) as path:
        result, _ = run_validator(build_fixture(Path(path), "manifest_mismatch"), 1)
        errors = result["third_party"][0]["errors"]
        require(any("manifest file mismatch" in item for item in errors), "manifest 映射错误未命中")
    log("[用例 3/7] manifest 映射不匹配通过")


def test_path_escape() -> None:
    """[参数] 无。
    [返回] 无；预期错误未命中时抛出断言异常。
    最近修改时间: 2026-07-14 12:14:25，覆盖裸文件名与路径逃逸。
    """
    log("[用例 4/7] 裸文件名与路径逃逸保护开始")
    with tempfile.TemporaryDirectory(prefix="swag-path-escape-", dir=TMP_ROOT) as path:
        result, _ = run_validator(build_fixture(Path(path), "path_escape"), 1)
        errors = result["third_party"][0]["errors"]
        require(any("裸文件名" in item or "manifest file escapes" in item for item in errors), "路径逃逸错误未命中")
    log("[用例 4/7] 裸文件名与路径逃逸保护通过")


def test_missing_source_type() -> None:
    """[参数] 无。
    [返回] 无；预期错误未命中时抛出断言异常。
    最近修改时间: 2026-07-14 12:14:25，覆盖上游 source_type 必填。
    """
    log("[用例 5/7] source_type 缺失开始")
    with tempfile.TemporaryDirectory(prefix="swag-source-type-", dir=TMP_ROOT) as path:
        result, _ = run_validator(build_fixture(Path(path), "missing_source_type"), 1)
        errors = result["third_party"][0]["errors"]
        require(any("source_type" in item for item in errors), "source_type 错误未命中")
    log("[用例 5/7] source_type 缺失通过")


def test_compatibility_single_directory() -> None:
    """[参数] 无。
    [返回] 无；根级兼容断言失败时抛出断言异常。
    最近修改时间: 2026-07-14 12:14:25，覆盖无上游子目录兼容。
    """
    log("[用例 6/7] 单目录兼容开始")
    with tempfile.TemporaryDirectory(prefix="swag-compatibility-", dir=TMP_ROOT) as path:
        swag = build_fixture(Path(path), "compatibility_single_directory")
        sys.path.insert(0, str(VALIDATOR.parent))
        import validate_openapi_yaml as validator_module

        legacy = validator_module.validate_swag_dir(swag)
        result, _ = run_validator(swag, 0)
        for key, value in legacy.items():
            require(result.get(key) == value, f"兼容键值变化: {key}")
        require(result["third_party"] == [], "单目录 third_party 应为空")
    log("[用例 6/7] 单目录兼容通过")


def test_stranger_directory_warning() -> None:
    """[参数] 无。
    [返回] 无；陌生目录 warning 断言失败时抛出异常。
    最近修改时间: 2026-07-14 12:14:25，覆盖陌生子目录告警。
    """
    log("[用例 7/7] 陌生子目录 warning 开始")
    with tempfile.TemporaryDirectory(prefix="swag-stranger-", dir=TMP_ROOT) as path:
        result, _ = run_validator(build_fixture(Path(path), "stranger_directory"), 0)
        require(result["valid"] is True, "陌生子目录不应导致根校验失败")
        require(result["tree_warnings"], "陌生子目录应进入 tree_warnings")
    log("[用例 7/7] 陌生子目录 warning 通过")


def main() -> None:
    """[参数] 无。
    [返回] 无，失败时抛出断言异常并以非零退出。
    最近修改时间: 2026-07-14 12:14:25，新增七用例离线验收入口。
    """
    TMP_ROOT.mkdir(parents=True, exist_ok=True)
    # 1. 按计划顺序执行七个隔离 fixture 用例。
    tests = [
        test_valid,
        test_missing_chinese_description,
        test_manifest_mismatch,
        test_path_escape,
        test_missing_source_type,
        test_compatibility_single_directory,
        test_stranger_directory_warning,
    ]
    try:
        for test in tests:
            test()
    except Exception as error:
        log(f"[结束] FAIL: {error}")
        raise
    log("[结束] PASS: 7/7 用例通过，临时 fixture 已由上下文管理器清理")


if __name__ == "__main__":
    main()
