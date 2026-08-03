"""验证二进制入口与后端 cmd 目录的唯一位置契约。"""

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


def run_cli(*arguments: str) -> subprocess.CompletedProcess[str]:
    """调用本地 Catalog CLI 并保留机器输出。

    [参数] arguments：CLI 子命令及其参数。
    [返回] CompletedProcess[str]：UTF-8 标准输出、标准错误和退出码。
    最近修改时间: 2026-08-02 新增二进制入口行为测试入口。
    """
    # 1. 固定 UTF-8、本仓库 cwd 和非抛异常退出码，便于断言 CLI 的失败关闭行为。
    return subprocess.run(
        [sys.executable, "-X", "utf8", str(CLI), *arguments],
        cwd=ROOT,
        text=True,
        encoding="utf-8",
        capture_output=True,
        check=False,
    )


def directory_hash(root: Path) -> str:
    """计算临时 fixture 的稳定内容摘要，证明 check 只读。

    [参数] root：待计算的临时项目根。
    [返回] str：路径和文件内容组成的 SHA-256 摘要。
    最近修改时间: 2026-08-02 新增入口检查无写入断言。
    """
    # 1. 以稳定路径顺序聚合目录和文件内容，避免遍历顺序掩盖检查写入副作用。
    digest = hashlib.sha256()
    for path in sorted(root.rglob("*")):
        relative = path.relative_to(root).as_posix()
        digest.update(relative.encode("utf-8"))
        if path.is_file():
            digest.update(path.read_bytes())
    return digest.hexdigest()


class BinaryEntrypointTests(unittest.TestCase):
    """覆盖二进制入口的查询、初始化和策略检查。"""

    def test_catalog_query_render_and_schema_expose_patterns(self):
        """确认两类项目的 primary/additional pattern 均唯一可查且可渲染。

        [参数] self：unittest 测试实例。
        [返回] None：断言失败时由 unittest 报告。
        最近修改时间: 2026-08-04 为 strict 合法入口 fixture 补齐根 Dockerfile。
        """
        # 1. 查询四种入口 pattern，并验证 Catalog 和 Schema 的动态节点契约。
        cases = (
            ("backend", "primary", "main.<ext>"),
            ("backend", "additional", "cmd/<binary>/main.<ext>"),
            ("fullstack", "primary", "backend/main.<ext>"),
            ("fullstack", "additional", "backend/cmd/<binary>/main.<ext>"),
        )
        for project_kind, category, expected_path in cases:
            result = run_cli(
                "query", "--project-kind", project_kind, "--artifact", "binary-entrypoint", "--category", category,
            )
            self.assertEqual(0, result.returncode, result.stdout)
            entry = json.loads(result.stdout)["entry"]
            self.assertEqual(expected_path, entry["canonical_path"])
            self.assertEqual("pattern", entry["node_kind"])
            self.assertTrue(entry["dynamic"])

        backend_render = run_cli("render", "--project-kind", "backend")
        self.assertEqual(0, backend_render.returncode, backend_render.stderr)
        for value in ("main.<ext>", "cmd/", "<binary>/"):
            self.assertIn(value, backend_render.stdout)
        fullstack_render = run_cli("render", "--project-kind", "fullstack")
        self.assertEqual(0, fullstack_render.returncode, fullstack_render.stderr)
        for value in ("backend/", "main.<ext>", "cmd/", "<binary>/"):
            self.assertIn(value, fullstack_render.stdout)

        catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
        schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
        patterns = [entry for entry in catalog["entries"] if entry.get("artifact_kind") == "binary-entrypoint"]
        self.assertEqual(4, len(patterns))
        self.assertEqual({"directory", "file", "pattern"}, set(schema["properties"]["entries"]["items"]["properties"]["node_kind"]["enum"]))
        pattern_rule = next(rule for rule in schema["properties"]["entries"]["items"]["allOf"] if rule["if"].get("properties", {}).get("node_kind", {}).get("const") == "pattern")
        self.assertEqual(["path_pattern", "dynamic", "init_policy"], pattern_rule["then"]["required"])

    def test_strict_accepts_the_four_legal_entrypoint_paths(self):
        """确认独立后端和同仓后端的主、额外入口均可通过 strict。

        [参数] self：unittest 测试实例。
        [返回] None：断言失败时由 unittest 报告。
        最近修改时间: 2026-08-04 为 strict 合法入口 fixture 补齐根 Dockerfile。
        """
        # 1. 在临时项目中写入合法路径，确认 strict 仅接受四种规范入口。
        cases = (
            ("backend", ("Dockerfile", "main.go", "cmd/api/main.go")),
            ("fullstack", ("Dockerfile", "backend/main.go", "backend/cmd/worker/main.go", "backend/crontask/sync_order/main.go", "backend/AGENTS.md", "backend/CLAUDE.md")),
        )
        for project_kind, paths in cases:
            with self.subTest(project_kind=project_kind), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                for relative in paths:
                    target = root / relative
                    target.parent.mkdir(parents=True, exist_ok=True)
                    target.write_text("package main\n", encoding="utf-8")
                result = run_cli(
                    "check", "--root", str(root), "--project-kind", project_kind,
                    "--language", "go", "--policy", "strict",
                )
                self.assertEqual(0, result.returncode, result.stdout)

    def test_strict_rejects_invalid_entrypoint_paths_without_writing(self):
        """确认重点非法路径和其他 main 文件位置失败关闭且不写 fixture。

        [参数] self：unittest 测试实例。
        [返回] None：断言失败时由 unittest 报告。
        最近修改时间: 2026-08-02 补齐二进制入口测试元信息。
        """
        # 1. 比较失败关闭前后的 fixture 哈希，防止 check 在负向样本中产生写入副作用。
        cases = (
            ("backend", "cmd/main.go"),
            ("backend", "internal/main.go"),
            ("fullstack", "main.go"),
            ("fullstack", "cmd/worker/main.go"),
            ("fullstack", "backend/cmd/main.go"),
            ("fullstack", "backend/internal/main.go"),
        )
        for project_kind, relative in cases:
            with self.subTest(project_kind=project_kind, relative=relative), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                target = root / relative
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text("package main\n", encoding="utf-8")
                before = directory_hash(root)
                result = run_cli(
                    "check", "--root", str(root), "--project-kind", project_kind,
                    "--language", "go", "--policy", "strict",
                )
                after = directory_hash(root)
                self.assertEqual(2, result.returncode, result.stdout)
                self.assertIn("二进制入口路径非法", result.stdout)
                self.assertEqual(before, after)

    def test_legacy_warns_and_adoption_preserves_registered_snapshot(self):
        """确认 legacy 只告警，adoption 继续尊重已登记的历史入口快照。

        [参数] self：unittest 测试实例。
        [返回] None：断言失败时由 unittest 报告。
        最近修改时间: 2026-08-02 补齐二进制入口测试元信息。
        """
        # 1. 固定非法历史入口，分别验证 legacy 告警和 adoption 快照的只读兼容。
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            invalid = root / "cmd" / "main.go"
            invalid.parent.mkdir(parents=True)
            invalid.write_text("package main\n", encoding="utf-8")
            before = directory_hash(root)
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
                "legacy_source_roots": [{
                    "path": "cmd",
                    "responsibility": "历史二进制入口快照",
                    "existing_directories": ["cmd"],
                    "existing_files": ["cmd/main.go"],
                }],
            }, ensure_ascii=False), encoding="utf-8")
            adoption_before = directory_hash(root)
            adoption = run_cli(
                "check", "--root", str(root), "--project-kind", "backend", "--language", "go",
                "--policy", "adoption", "--adoption-manifest", "doc/1-架构/3-目录规则收敛清单.yaml",
            )
            self.assertEqual(0, adoption.returncode, adoption.stdout)
            self.assertEqual(adoption_before, directory_hash(root))

    def test_init_rejects_dynamic_entrypoints_without_creating_placeholders(self):
        """确认 init 不创建主入口、binary 目录或 ext 占位路径。

        [参数] self：unittest 测试实例。
        [返回] None：断言失败时由 unittest 报告。
        最近修改时间: 2026-08-02 补齐二进制入口测试元信息。
        """
        # 1. 显式启用动态 pattern，确认 init 失败关闭且临时根目录没有残留占位路径。
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            result = run_cli(
                "init", "--project-kind", "backend", "--root", str(root),
                "--enable", "backend.binary-entrypoint.primary,backend.binary-entrypoint.additional",
            )
            self.assertEqual(2, result.returncode, result.stdout)
            self.assertIn("动态入口 pattern", result.stdout)
            self.assertFalse((root / "main.<ext>").exists())
            self.assertFalse((root / "cmd").exists())
            self.assertFalse((root / "<binary>").exists())


if __name__ == "__main__":
    unittest.main()
