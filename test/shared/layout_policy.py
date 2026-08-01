"""根 test 目录的测试资产位置与历史边界校验。"""

from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path


EXECUTABLE_SUFFIXES = frozenset({".bat", ".cmd", ".go", ".js", ".ps1", ".py", ".sh", ".ts"})
SPECIAL_TEST_DIRECTORIES = frozenset({"shared", "test-asset-governance"})


def repository_root() -> Path:
    """返回当前测试治理代码所属的仓库根目录。

    [参数] 无。
    [返回] Path：`test/shared/` 上两级的项目根目录。
    最近修改时间：2026-08-01；改动原因：统一根测试目录的相对路径计算。
    """
    return Path(__file__).resolve().parents[2]


def is_within(path: Path, directory: Path) -> bool:
    """判断路径是否位于指定目录内。

    [参数] path：待判定路径；directory：允许的祖先目录。
    [返回] bool：路径可相对化时返回真。
    最近修改时间：2026-08-01；改动原因：避免字符串前缀误判目录边界。
    """
    try:
        path.resolve().relative_to(directory.resolve())
    except ValueError:
        return False
    return True


def executable_doc5_assets(root: Path) -> list[tuple[str, str]]:
    """生成历史 `doc/5-tests/` 可执行资产的稳定指纹输入。

    [参数] root：仓库根目录。
    [返回] list：按相对路径排序的“路径、SHA-256”元组。
    最近修改时间：2026-08-01；改动原因：历史测试包只读边界需要可复验基线。
    """
    # 1. 只扫描可执行后缀，文档、日志和图片仍可作为历史证据原样保留。
    doc_root = root / "doc" / "5-tests"
    if not doc_root.exists():
        return []
    assets = [
        path
        for path in doc_root.rglob("*")
        if path.is_file() and path.suffix.lower() in EXECUTABLE_SUFFIXES
    ]
    # 2. 路径与摘要一起排序，确保 Windows 与其他平台都得到相同的基线输入。
    return [
        (path.relative_to(root).as_posix(), sha256(path.read_bytes()).hexdigest())
        for path in sorted(assets, key=lambda item: item.relative_to(root).as_posix())
    ]


def legacy_manifest(root: Path) -> dict[str, object]:
    """构造当前历史可执行资产的压缩指纹清单。

    [参数] root：仓库根目录。
    [返回] dict：包含文件数量和目录树 SHA-256 的 JSON 兼容对象。
    最近修改时间：2026-08-01；改动原因：阻断历史测试资产被静默新增或修改。
    """
    assets = executable_doc5_assets(root)
    lines = [f"{path}\t{digest}" for path, digest in assets]
    payload = ("\n".join(lines) + "\n").encode("utf-8")
    return {
        "schema_version": 1,
        "algorithm": "sha256",
        "root": "doc/5-tests",
        "file_count": len(assets),
        "tree_sha256": sha256(payload).hexdigest(),
    }


def validate_legacy_manifest(root: Path, manifest_path: Path) -> list[str]:
    """检查历史可执行资产是否仍与只读基线一致。

    [参数] root：仓库根目录；manifest_path：基线 JSON 路径。
    [返回] list：不一致时的可读错误列表，空列表表示通过。
    最近修改时间：2026-08-01；改动原因：将首次修改必须迁出历史目录变为机器可判定规则。
    """
    expected = json.loads(manifest_path.read_text(encoding="utf-8"))
    actual = legacy_manifest(root)
    expected_keys = {"schema_version", "algorithm", "root", "file_count", "tree_sha256"}
    if set(expected) != expected_keys:
        return ["历史测试资产指纹清单字段不完整或存在未知字段"]
    if expected != actual:
        return [
            "doc/5-tests/ 历史可执行资产发生变化；"
            "新增、改名或修改的测试代码必须迁至根 test/ 后再更新基线。"
        ]
    return []


def expected_test_path(root: Path, source_path: Path) -> Path:
    """根据被测源码路径计算单文件测试的唯一镜像位置。

    [参数] root：仓库根目录；source_path：被测源码的绝对或根相对路径。
    [返回] Path：`test/<源码目录>/<名称>_test.<后缀>` 目标路径。
    最近修改时间：2026-08-01；改动原因：固定单文件测试的镜像和命名契约。
    """
    source = source_path if source_path.is_absolute() else root / source_path
    relative = source.resolve().relative_to(root.resolve())
    return root / "test" / relative.parent / f"{relative.stem}_test{relative.suffix}"


def validate_test_file_location(root: Path, source_path: Path, test_path: Path) -> list[str]:
    """校验单文件测试是否镜像对应被测源码。

    [参数] root：仓库根目录；source_path：被测源码路径；test_path：实际测试路径。
    [返回] list：位置或命名错误，空列表表示通过。
    最近修改时间：2026-08-01；改动原因：让目录级测试之外的单文件测试可精确校验。
    """
    expected = expected_test_path(root, source_path)
    actual = test_path if test_path.is_absolute() else root / test_path
    if actual.resolve() == expected.resolve():
        return []
    return [f"测试文件必须位于 {expected.relative_to(root).as_posix()}，实际为 {actual.relative_to(root).as_posix()}"]


def validate_root_test_layout(root: Path) -> list[str]:
    """检查活动 Python/Go 测试是否只使用根 `test/` 目录。

    [参数] root：仓库根目录。
    [返回] list：活动测试的目录、命名和 Go 白盒路径错误。
    最近修改时间：2026-08-01；改动原因：统一活动测试根并拒绝旧目录新增入口。
    """
    # 1. 根 test 不存在时直接报告，避免后续扫描把缺失误当成空测试集。
    test_root = root / "test"
    if not test_root.is_dir():
        return ["缺少唯一活动测试代码根目录 test/"]

    errors: list[str] = []
    for path in test_root.rglob("*.py"):
        relative = path.relative_to(test_root)
        top_level = relative.parts[0] if relative.parts else ""
        if path.name.startswith("test_"):
            errors.append(f"Python 测试必须使用 *_test.py 命名：{path.relative_to(root).as_posix()}")
        if path.name.endswith("_test.py") and top_level not in SPECIAL_TEST_DIRECTORIES:
            source_directory = root / top_level
            if not source_directory.is_dir():
                errors.append(f"测试镜像缺少被测目录：{path.relative_to(root).as_posix()}")

    for path in root.rglob("test_*.py"):
        if not is_within(path, root / "doc"):
            errors.append(f"禁止活动 Python 测试使用 test_ 前缀：{path.relative_to(root).as_posix()}")

    for path in root.rglob("*_test.go"):
        if not is_within(path, test_root) and not is_within(path, root / "doc"):
            errors.append(f"Go 源码目录禁止 *_test.go：{path.relative_to(root).as_posix()}")
    return errors
