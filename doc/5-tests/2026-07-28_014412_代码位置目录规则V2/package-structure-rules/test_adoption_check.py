"""旧项目渐进采纳 CLI 的本地真实行为测试。"""

import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
CLI = ROOT / "package-structure-rules" / "scripts" / "placement_catalog.py"
MANIFEST = Path("doc/1-架构/3-目录规则收敛清单.yaml")


def run(*args):
    """调用本地 Catalog CLI 并保留失败输出供断言使用。

    [参数] args：传递给 CLI 的子命令参数。
    [返回] CompletedProcess：包含退出码、标准输出和标准错误。
    最近修改时间: 2026-07-29 00:25:50 新增 adoption 真实行为测试的本地调用入口。
    """
    return subprocess.run([sys.executable, str(CLI), *args], cwd=ROOT, text=True, encoding="utf-8", capture_output=True, check=False)


def fixture_hash(root: Path) -> str:
    """计算 fixture 目录和文件内容的稳定摘要。

    [参数] root：临时项目根目录。
    [返回] str：目录结构和文件内容的 SHA-256 摘要。
    最近修改时间: 2026-07-29 00:25:50 证明 adoption 检查没有写入临时项目。
    """
    digest = hashlib.sha256()
    # 1. 以排序后的相对路径和文件内容累计摘要，避免遍历顺序影响结果。
    for path in sorted(root.rglob("*")):
        digest.update(path.relative_to(root).as_posix().encode("utf-8"))
        if path.is_file():
            digest.update(path.read_bytes())
    return digest.hexdigest()


def write_manifest(root: Path, manifest: dict) -> None:
    """以 JSON 兼容 YAML 格式写入固定位置的收敛清单。

    [参数] root：临时项目根目录；manifest：待测试的清单内容。
    [返回] 无。
    最近修改时间: 2026-07-29 00:25:50 新增固定清单位置的测试 fixture 构造。
    """
    target = root / MANIFEST
    target.parent.mkdir(parents=True)
    target.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")


def backend_manifest(adopted_paths: list[dict] | None = None, legacy_roots: list[dict] | None = None) -> dict:
    """构造最小合法的 Go 后端收敛清单。

    [参数] adopted_paths：可原地扩展的 V2 目录；legacy_roots：冻结的遗留源码根。
    [返回] dict：JSON 兼容 YAML 清单对象。
    最近修改时间: 2026-07-29 00:25:50 复用 adoption 正反向 fixture 的共同上下文。
    """
    # 1. 固定后端和语言上下文，使各用例只替换待验证的目录基线。
    return {
        "version": 1,
        "project_kind": "backend",
        "language": "go",
        "adopted_paths": [] if adopted_paths is None else adopted_paths,
        "legacy_source_roots": [] if legacy_roots is None else legacy_roots,
    }


class AdoptionCheckTests(unittest.TestCase):
    """验证收敛清单只能承认历史事实，不能扩张遗留目录。"""

    def check_adoption(self, root: Path):
        """执行固定参数的 Go 后端 adoption 检查。

        [参数] self：unittest 测试实例；root：临时项目根目录。
        [返回] CompletedProcess：CLI 检查结果。
        最近修改时间: 2026-07-29 00:25:50 收敛重复的 adoption 命令参数。
        """
        return run(
            "check", "--root", str(root), "--project-kind", "backend", "--language", "go", "--policy", "adoption",
            "--adoption-manifest", MANIFEST.as_posix(),
        )

    def test_adoption_accepts_registered_legacy_and_adopted_paths_without_writing(self):
        """确认已登记遗留快照和已采纳目录可原地通过且检查不写入。

        [参数] self：unittest 测试实例。
        [返回] 无。
        最近修改时间: 2026-07-29 00:25:50 新增旧目录复用和 V2 原地采纳的正向断言。
        """
        # 1. 构造根旧 util 快照，并在两个已采纳 V2 目录中保留既有实现。
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "util").mkdir()
            (root / "util" / "legacy.go").write_text("package util", encoding="utf-8")
            (root / "utils" / "discovery" / "polaris").mkdir(parents=True)
            (root / "utils" / "discovery" / "polaris" / "register.go").write_text("package polaris", encoding="utf-8")
            (root / "database" / "repository").mkdir(parents=True)
            (root / "database" / "repository" / "order.go").write_text("package repository", encoding="utf-8")
            write_manifest(
                root,
                backend_manifest(
                    [
                        {"path": "utils/discovery/polaris", "catalog_id": "backend.utils.discovery.polaris", "responsibility": "现有服务发现适配"},
                        {"path": "database/repository", "catalog_id": "backend.database.repository", "responsibility": "现有数据库访问实现"},
                    ],
                    [{"path": "util", "responsibility": "历史工具根", "existing_directories": ["util"], "existing_files": ["util/legacy.go"]}],
                ),
            )
            # 2. 比较调用前后内容摘要，证明 check 只读并允许登记事实继续存在。
            before = fixture_hash(root)
            result = self.check_adoption(root)
            after = fixture_hash(root)
            self.assertEqual(0, result.returncode, result.stdout)
            self.assertEqual(before, after)

    def test_adoption_accepts_standard_yaml_manifest(self):
        """确认用户可按目录规则示例填写普通 YAML 收敛清单。

        [参数] self：unittest 测试实例。
        [返回] 无。
        最近修改时间: 2026-07-29 01:12:27 支持普通 YAML 收敛清单解析。
        """
        # 1. 使用缩进 YAML 而非 JSON 子集，验证公开清单格式与用户示例一致。
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "database" / "repository").mkdir(parents=True)
            (root / MANIFEST).parent.mkdir(parents=True)
            (root / MANIFEST).write_text(
                "version: 1\n"
                "project_kind: backend\n"
                "language: go\n"
                "adopted_paths:\n"
                "  - path: database/repository\n"
                "    catalog_id: backend.database.repository\n"
                "    responsibility: 已符合 V2 的数据库访问实现\n"
                "legacy_source_roots: []\n",
                encoding="utf-8",
            )
            result = self.check_adoption(root)
            self.assertEqual(0, result.returncode, result.stdout)

    def test_adoption_accepts_new_v2_business_utils_and_source_util(self):
        """确认未依赖遗留根的新业务、新工具和源码根工具符合 V2。

        [参数] self：unittest 测试实例。
        [返回] 无。
        最近修改时间: 2026-07-29 00:25:50 覆盖新代码必须进入 V2 的三个后端落点。
        """
        # 1. 新增代码分别落入业务域、根 utils 工具包和源码根 util 的合法位置。
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for relative in ("internal/business/orders/service/create.go", "utils/time/format.go", "internal/util/request_context.go"):
                target = root / relative
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text("package sample", encoding="utf-8")
            write_manifest(root, backend_manifest())
            result = self.check_adoption(root)
            self.assertEqual(0, result.returncode, result.stdout)

    def test_adoption_accepts_crontask_root_directory(self):
        """确认 corntask 拼写修正为 crontask 后，adoption 策略仍接受该后端根级目录。

        [参数] self：unittest 测试实例。
        [返回] 无。
        最近修改时间: 2026-07-29 覆盖 corntask 改名 crontask 后的根级目录与业务域内层回归。
        """
        # 1. 新增代码同时落入改名后的根级 crontask 与业务域内部 crontask，验证脚本常量已同步更新。
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for relative in (
                "crontask/sync_order/main.go",
                "internal/business/orders/crontask/cleanup_job.go",
            ):
                target = root / relative
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text("package sample", encoding="utf-8")
            write_manifest(root, backend_manifest())
            result = self.check_adoption(root)
            self.assertEqual(0, result.returncode, result.stdout)

    def test_adoption_rejects_new_legacy_source_files_and_directories_without_writing(self):
        """确认遗留根新增源码文件或目录会失败且不会改写 fixture。

        [参数] self：unittest 测试实例。
        [返回] 无。
        最近修改时间: 2026-07-29 00:25:50 固定旧目录只维护既有快照的负向边界。
        """
        # 1. 快照只登记既有文件；新增文件和目录都必须在 adoption 下拒绝。
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "util" / "new").mkdir(parents=True)
            (root / "util" / "legacy.go").write_text("package util", encoding="utf-8")
            (root / "util" / "new.go").write_text("package util", encoding="utf-8")
            (root / "util" / "new" / "child.go").write_text("package util", encoding="utf-8")
            write_manifest(
                root,
                backend_manifest(
                    legacy_roots=[{"path": "util", "responsibility": "历史工具根", "existing_directories": ["util"], "existing_files": ["util/legacy.go"]}],
                ),
            )
            before = fixture_hash(root)
            result = self.check_adoption(root)
            after = fixture_hash(root)
            self.assertEqual(2, result.returncode)
            self.assertEqual(before, after)
            errors = "\n".join(json.loads(result.stdout)["errors"])
            self.assertIn("遗留源码文件不在快照: util/new.go", errors)
            self.assertIn("遗留源码目录不在快照: util/new", errors)

    def test_adoption_rejects_unregistered_legacy_source_path(self):
        """确认未登记的旧服务目录不能借 adoption 继续新增源码。

        [参数] self：unittest 测试实例。
        [返回] 无。
        最近修改时间: 2026-07-29 00:25:50 新增未登记历史源码路径的失败断言。
        """
        # 1. service 不是 V2 后端根；没有快照登记的源码必须失败关闭。
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            target = root / "service" / "order.go"
            target.parent.mkdir(parents=True)
            target.write_text("package service", encoding="utf-8")
            write_manifest(root, backend_manifest())
            result = self.check_adoption(root)
            self.assertEqual(2, result.returncode)
            self.assertIn("未登记的遗留源码路径: service/order.go", result.stdout)

    def test_adoption_rejects_missing_or_invalid_manifest_context(self):
        """确认缺清单、项目语言不符、重复、嵌套和越界路径均稳定失败。

        [参数] self：unittest 测试实例。
        [返回] 无。
        最近修改时间: 2026-07-29 00:50:55 覆盖 adoption 清单上下文、嵌套根与安全边界。
        """
        # 1. 缺少清单参数时必须失败，不能退化为 legacy 或 strict。
        with tempfile.TemporaryDirectory() as directory:
            missing = run("check", "--root", directory, "--project-kind", "backend", "--language", "go", "--policy", "adoption")
            self.assertEqual(2, missing.returncode)
            self.assertIn("--adoption-manifest", missing.stdout)

        # 2. 项目类型、语言、重复根和路径穿越分别不得扩大遗留基线。
        cases = (
            ("project_kind", "frontend", "project_kind 与 --project-kind 不一致"),
            ("language", "node", "language 与 --language 不一致"),
        )
        for field, value, expected in cases:
            with self.subTest(field=field), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                manifest = backend_manifest()
                manifest[field] = value
                write_manifest(root, manifest)
                result = self.check_adoption(root)
                self.assertEqual(2, result.returncode)
                self.assertIn(expected, result.stdout)

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "util").mkdir()
            manifest = backend_manifest(
                legacy_roots=[
                    {"path": "util", "responsibility": "历史工具根", "existing_directories": ["util"], "existing_files": []},
                    {"path": "util", "responsibility": "重复根", "existing_directories": ["util"], "existing_files": []},
                ],
            )
            write_manifest(root, manifest)
            duplicate = self.check_adoption(root)
            self.assertEqual(2, duplicate.returncode)
            self.assertIn("legacy_source_roots 重复路径", duplicate.stdout)

        # 3. 父子遗留根会让同一文件的快照归属不确定，必须在扫描前失败关闭。
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "service" / "order").mkdir(parents=True)
            manifest = backend_manifest(
                legacy_roots=[
                    {"path": "service", "responsibility": "历史服务根", "existing_directories": ["service", "service/order"], "existing_files": []},
                    {"path": "service/order", "responsibility": "嵌套订单根", "existing_directories": ["service/order"], "existing_files": []},
                ],
            )
            write_manifest(root, manifest)
            nested = self.check_adoption(root)
            self.assertEqual(2, nested.returncode)
            self.assertIn("legacy_source_roots 不能嵌套或重叠: service/order", nested.stdout)

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            manifest = backend_manifest(legacy_roots=[{"path": "../util", "responsibility": "越界根", "existing_directories": ["../util"], "existing_files": []}])
            write_manifest(root, manifest)
            traversal = self.check_adoption(root)
            self.assertEqual(2, traversal.returncode)
            self.assertIn("收敛清单路径非法", traversal.stdout)

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            manifest = backend_manifest(
                adopted_paths=[{"path": "util", "catalog_id": "backend.utils.discovery.polaris", "responsibility": "禁止目录"}],
            )
            write_manifest(root, manifest)
            forbidden = self.check_adoption(root)
            self.assertEqual(2, forbidden.returncode)
            self.assertIn("已采纳路径命中禁止目录", forbidden.stdout)

    def test_strict_and_legacy_keep_their_existing_policy_meaning(self):
        """确认新增 adoption 后 strict 仍失败、legacy 仍只告警。

        [参数] self：unittest 测试实例。
        [返回] 无。
        最近修改时间: 2026-07-29 00:25:50 保护既有两种检查策略不回归。
        """
        # 1. 根旧 util 对 strict 是错误，对 legacy 只输出 warning。
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "util").mkdir()
            strict = run("check", "--root", str(root), "--project-kind", "backend", "--language", "go", "--policy", "strict")
            legacy = run("check", "--root", str(root), "--project-kind", "backend", "--language", "go", "--policy", "legacy")
            self.assertEqual(2, strict.returncode)
            self.assertEqual(0, legacy.returncode)
            self.assertTrue(json.loads(legacy.stdout)["warnings"])


if __name__ == "__main__":
    unittest.main()
