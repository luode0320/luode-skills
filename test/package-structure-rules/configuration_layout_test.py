"""验证后端环境配置目录、文件命名和初始化边界。"""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CLI = ROOT / "package-structure-rules" / "scripts" / "placement_catalog.py"
CATALOG = ROOT / "package-structure-rules" / "references" / "placement-catalog.yaml"
SCHEMA = ROOT / "package-structure-rules" / "references" / "placement-catalog.schema.json"
CONFIGURATION_LAYOUT = ROOT / "package-structure-rules" / "references" / "configuration-layout.md"


def run_cli(*arguments: str) -> subprocess.CompletedProcess[str]:
    """调用本地 Catalog CLI 并保留 UTF-8 机器输出。

    [参数] arguments：CLI 参数序列。
    [返回] subprocess.CompletedProcess[str]：命令执行结果。
    最近修改时间: 2026-08-02 21:30:00 补齐配置行为测试函数头元信息。
    """
    return subprocess.run(
        [sys.executable, "-X", "utf8", str(CLI), *arguments],
        cwd=ROOT,
        text=True,
        encoding="utf-8",
        capture_output=True,
        check=False,
    )


def directory_hash(root: Path) -> str:
    """计算临时 fixture 的稳定摘要，证明 check 只读。

    [参数] root：临时测试目录。
    [返回] str：目录结构和文件内容的 SHA-256 摘要。
    最近修改时间: 2026-08-02 21:30:00 补齐配置行为测试函数头元信息。
    """
    digest = hashlib.sha256()
    for path in sorted(root.rglob("*")):
        digest.update(path.relative_to(root).as_posix().encode("utf-8"))
        if path.is_file():
            digest.update(path.read_bytes())
    return digest.hexdigest()


def write_files(root: Path, paths: tuple[str, ...]) -> None:
    """创建测试样本文件，内容保持最小且不包含秘密原值。

    [参数] root：临时测试目录；paths：待创建的项目相对路径。
    [返回] None：仅创建测试 fixture。
    最近修改时间: 2026-08-02 21:30:00 补齐配置行为测试函数头元信息。
    """
    for relative in paths:
        target = root / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text("sample: true\n", encoding="utf-8")


class ConfigurationLayoutTests(unittest.TestCase):
    """覆盖配置查询、文件边界、策略分流和初始化语义。"""

    def test_catalog_query_and_schema_expose_environment_contract(self):
        """确认独立后端和同仓后端的四个配置查询均唯一且包含契约元数据。

        [参数] 无。
        [返回] None：断言配置 Catalog 与 Schema 契约。
        最近修改时间: 2026-08-02 21:30:00 补齐配置行为测试函数头元信息。
        """
        # 1. 先验证 backend/fullstack 的四类 config query 都暴露完整策略字段。
        cases = (
            ("backend", "yaml", "config/yaml"),
            ("backend", "embedded", "config/embedded"),
            ("fullstack", "yaml", "backend/config/yaml"),
            ("fullstack", "embedded", "backend/config/embedded"),
        )
        for project_kind, category, expected_path in cases:
            with self.subTest(project_kind=project_kind, category=category):
                result = run_cli(
                    "query", "--project-kind", project_kind, "--artifact", "config", "--category", category,
                )
                self.assertEqual(0, result.returncode, result.stdout)
                entry = json.loads(result.stdout)["entry"]
                self.assertEqual(expected_path, entry["canonical_path"])
                self.assertEqual(["local", "test", "prod"], entry["standard_environments"])
                self.assertEqual("[a-z][a-z0-9_]*", entry["environment_name_pattern"])
                self.assertTrue(entry["direct_files"])
                if category == "yaml":
                    self.assertEqual("config_<env>.yaml|config_<env>.yml", entry["file_name_pattern"])
                    self.assertEqual("forbid_plain_secret", entry["secret_policy"])
                    self.assertEqual("allowed_reference", entry["environment_variable_policy"])
                else:
                    self.assertEqual("config_<env>.go", entry["go_file_name_pattern"])
                    self.assertEqual("allow_plain_secret", entry["secret_policy"])
                    self.assertEqual("embedded_source_primary", entry["source_policy"])
                    self.assertEqual("not_default", entry["environment_variable_policy"])

        # 2. 再核对 Catalog 与 Schema 的策略字段定义。
        catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
        schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
        config_entries = [entry for entry in catalog["entries"] if entry.get("artifact_kind") == "config"]
        self.assertEqual(4, len(config_entries))
        properties = schema["properties"]["entries"]["items"]["properties"]
        for field in (
            "file_name_pattern", "go_file_name_pattern", "environment_name_pattern",
            "standard_environments", "direct_files", "secret_policy",
            "source_policy", "environment_variable_policy",
        ):
            self.assertIn(field, properties)

    def test_embedded_secret_boundary_is_distinct_from_yaml_boundary(self):
        """确认 embedded 允许源码私密配置，但 YAML 和外部输出仍保持禁止边界。

        [参数] 无。
        [返回] None：断言配置 reference 文字与机器策略一致。
        最近修改时间: 2026-08-02 21:30:00 新增 embedded 私密配置边界回归。
        """
        # 1. 对照 reference 正文确认 embedded/YAML 和外部输出边界。
        layout = CONFIGURATION_LAYOUT.read_text(encoding="utf-8")
        self.assertIn("允许直接写入 API key、密钥、密码等私密信息", layout)
        self.assertIn("源码配置是主来源，默认不依赖环境变量", layout)
        self.assertIn("不得写入 Agent 输出、日志、README、错误或测试报告", layout)
        self.assertIn("在 YAML 中直接写入真实密码、token、私钥或连接串：违反秘密原值边界", layout)

        # 2. 对照 Catalog 条目确认两类 embedded 放行、两类 YAML 禁止。
        catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
        embedded = [
            entry for entry in catalog["entries"]
            if entry.get("artifact_kind") == "config" and entry.get("category") == "embedded"
        ]
        yaml_entries = [
            entry for entry in catalog["entries"]
            if entry.get("artifact_kind") == "config" and entry.get("category") == "yaml"
        ]
        self.assertEqual(2, len(embedded))
        self.assertEqual(2, len(yaml_entries))
        self.assertTrue(all(entry["secret_policy"] == "allow_plain_secret" for entry in embedded))
        self.assertTrue(all(entry["source_policy"] == "embedded_source_primary" for entry in embedded))
        self.assertTrue(all(entry["environment_variable_policy"] == "not_default" for entry in embedded))
        self.assertTrue(all(entry["secret_policy"] == "forbid_plain_secret" for entry in yaml_entries))

    def test_render_contains_environment_examples(self):
        """确认 render 暴露占位契约，reference 正文保留具体环境示例。

        [参数] 无。
        [返回] None：断言目录渲染和 reference 示例。
        最近修改时间: 2026-08-02 21:30:00 补齐配置行为测试函数头元信息。
        """
        for project_kind in ("backend", "fullstack"):
            with self.subTest(project_kind=project_kind):
                result = run_cli("render", "--project-kind", project_kind)
                self.assertEqual(0, result.returncode, result.stderr)
                self.assertIn("config/", result.stdout)
                self.assertIn("yaml/", result.stdout)
                self.assertIn("embedded/", result.stdout)
                if project_kind == "backend":
                    self.assertIn("config_<env>.yaml", result.stdout)
                    self.assertIn("config_<env>.<ext>", result.stdout)

        layout = CONFIGURATION_LAYOUT.read_text(encoding="utf-8")
        for filename in (
            "config_prod.yaml", "config_test.yaml", "config_local.yaml",
            "config_prod.go", "config_test.go", "config_local.go",
        ):
            self.assertIn(filename, layout)

    def test_strict_accepts_split_and_unpaired_environment_files(self):
        """确认标准/扩展环境、单文件和 YAML/embedded 不配对均通过。

        [参数] 无。
        [返回] None：断言合法环境配置样本通过 strict。
        最近修改时间: 2026-08-02 21:30:00 补齐配置行为测试函数头元信息。
        """
        cases = (
            ("backend", ("config/yaml/config_prod.yaml", "config/yaml/config_pre_prod.yml", "config/embedded/config_local.go"), "go"),
            ("fullstack", ("backend/config/yaml/config_test.yaml", "backend/config/embedded/config_dev.go"), "go"),
            ("backend", ("config/embedded/config_local.java",), "java"),
        )
        for project_kind, paths, language in cases:
            with self.subTest(project_kind=project_kind, language=language), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                write_files(root, paths)
                result = run_cli(
                    "check", "--root", str(root), "--project-kind", project_kind,
                    "--language", language, "--policy", "strict",
                )
                self.assertEqual(0, result.returncode, result.stdout)

    def test_strict_rejects_invalid_names_locations_and_nesting(self):
        """确认非法环境名、旧 Go 命名、嵌套文件和错误配置根失败关闭。

        [参数] 无。
        [返回] None：断言非法配置样本失败关闭且不写入。
        最近修改时间: 2026-08-02 21:30:00 补齐配置行为测试函数头元信息。
        """
        cases = (
            ("backend", "go", "config/yaml/config_PROD.yaml", "环境配置文件名"),
            ("backend", "go", "config/yaml/config_prod.json", "环境配置文件扩展名"),
            ("backend", "go", "config/embedded/config_test_yaml.go", "Go embedded"),
            ("backend", "go", "config/embedded/nested/config_local.go", "直接位于"),
            ("backend", "go", "backend/config/yaml/config_local.yaml", "后端配置必须位于"),
            ("fullstack", "go", "config/yaml/config_local.yaml", "后端配置必须位于"),
        )
        for project_kind, language, relative, expected in cases:
            with self.subTest(project_kind=project_kind, relative=relative), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                write_files(root, (relative,))
                before = directory_hash(root)
                result = run_cli(
                    "check", "--root", str(root), "--project-kind", project_kind,
                    "--language", language, "--policy", "strict",
                )
                self.assertEqual(2, result.returncode, result.stdout)
                self.assertIn(expected, result.stdout)
                self.assertEqual(before, directory_hash(root))

    def test_policies_preserve_failure_semantics_and_hash(self):
        """确认 strict/adoption 失败关闭，legacy 只告警，三者均不写目录。

        [参数] 无。
        [返回] None：断言三种策略的退出码、告警和只读摘要。
        最近修改时间: 2026-08-02 21:30:00 补齐配置行为测试函数头元信息。
        """
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            invalid = root / "config" / "yaml" / "config_PROD.yaml"
            invalid.parent.mkdir(parents=True)
            invalid.write_text("sample: true\n", encoding="utf-8")
            before = directory_hash(root)

            strict = run_cli(
                "check", "--root", str(root), "--project-kind", "backend", "--language", "go", "--policy", "strict",
            )
            self.assertEqual(2, strict.returncode, strict.stdout)
            self.assertEqual(before, directory_hash(root))

            legacy = run_cli(
                "check", "--root", str(root), "--project-kind", "backend", "--language", "go", "--policy", "legacy",
            )
            self.assertEqual(0, legacy.returncode, legacy.stdout)
            self.assertTrue(json.loads(legacy.stdout)["warnings"])
            self.assertEqual(before, directory_hash(root))

            manifest = root / "doc" / "1-架构" / "3-目录规则收敛清单.yaml"
            manifest.parent.mkdir(parents=True)
            manifest.write_text(json.dumps({
                "version": 1,
                "project_kind": "backend",
                "language": "go",
                "adopted_paths": [],
                "legacy_source_roots": [],
            }), encoding="utf-8")
            adoption_before = directory_hash(root)
            adoption = run_cli(
                "check", "--root", str(root), "--project-kind", "backend", "--language", "go",
                "--policy", "adoption", "--adoption-manifest", "doc/1-架构/3-目录规则收敛清单.yaml",
            )
            self.assertEqual(2, adoption.returncode, adoption.stdout)
            self.assertEqual(adoption_before, directory_hash(root))

    def test_init_creates_directories_without_dynamic_environment_files(self):
        """确认 init 创建配置目录，但不猜测或生成任何环境文件。

        [参数] 无。
        [返回] None：断言 init 只创建静态配置目录。
        最近修改时间: 2026-08-02 21:30:00 补齐配置行为测试函数头元信息。
        """
        cases = (("backend", "config/yaml"), ("fullstack", "backend/config/yaml"))
        for project_kind, yaml_root in cases:
            with self.subTest(project_kind=project_kind), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                result = run_cli(
                    "init", "--project-kind", project_kind, "--root", str(root), "--language", "go",
                )
                self.assertEqual(0, result.returncode, result.stdout)
                self.assertTrue((root / yaml_root).is_dir())
                self.assertFalse(list(root.rglob("config_*.yaml")))
                self.assertFalse(list(root.rglob("config_*.yml")))
                self.assertFalse(list(root.rglob("config_*.go")))


if __name__ == "__main__":
    unittest.main()
