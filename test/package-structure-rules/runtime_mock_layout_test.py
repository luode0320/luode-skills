"""验证 Go 运行时 Mock 的目录、selector、装配桥与只读检查。"""

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
REFERENCE = ROOT / "package-structure-rules" / "references" / "runtime-mock-layout-go.md"

GO_MOD = "module example.com/proj\n"


def run_cli(*arguments: str) -> subprocess.CompletedProcess[str]:
    """调用本地 Catalog CLI 并保留机器输出。"""
    return subprocess.run(
        [sys.executable, "-X", "utf8", str(CLI), *arguments],
        cwd=ROOT,
        text=True,
        encoding="utf-8",
        capture_output=True,
        check=False,
    )


def directory_hash(root: Path) -> str:
    """计算临时 fixture 的稳定内容摘要，证明 check 只读。"""
    digest = hashlib.sha256()
    for path in sorted(root.rglob("*")):
        relative = path.relative_to(root).as_posix()
        digest.update(relative.encode("utf-8"))
        if path.is_file():
            digest.update(path.read_bytes())
    return digest.hexdigest()


def write(path: Path, text: str) -> None:
    """以 UTF-8 写入测试 fixture 文件。"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def write_good_backend(root: Path) -> None:
    """写入符合运行时 Mock 契约的独立后端正例。"""
    write(root / "go.mod", GO_MOD)
    write(root / "Dockerfile", "FROM golang:1.26\n")
    write(root / "main.go", "package main\n\nfunc main() { _ = newGateway() }\n")
    write(root / "main_mock.go", "//go:build mock\n\npackage main\n\nimport \"example.com/proj/mock/assembly\"\n\nfunc newGateway() string { return assembly.NewGateway() }\n")
    write(root / "main_real.go", "//go:build !mock\n\npackage main\n\nfunc newGateway() string { return \"real\" }\n")
    write(root / "internal/business/scalp/api/api.go", "package api\n\ntype Gateway struct{}\n")
    write(root / "mock/assembly/assembly.go", "//go:build mock\n\npackage assembly\n\nfunc NewGateway() string { return \"mock\" }\n")
    write(root / "mock/business/scalp/api/gateway_mock.go", "//go:build mock\n\npackage mock_api\n\ntype MockGateway struct{}\n")


def write_good_fullstack(root: Path) -> None:
    """写入符合运行时 Mock 契约的前后端同仓后端正例。"""
    write(root / "go.mod", GO_MOD)
    write(root / "Dockerfile", "FROM golang:1.26\n")
    governance = "backend governance\n"
    write(root / "backend/AGENTS.md", governance)
    write(root / "backend/CLAUDE.md", governance)
    write(root / "backend/main.go", "package main\n\nfunc main() { _ = newGateway() }\n")
    write(root / "backend/main_mock.go", "//go:build mock\n\npackage main\n\nimport \"example.com/proj/mock/assembly\"\n\nfunc newGateway() string { return assembly.NewGateway() }\n")
    write(root / "backend/main_real.go", "//go:build !mock\n\npackage main\n\nfunc newGateway() string { return \"real\" }\n")
    write(root / "backend/internal/business/scalp/api/api.go", "package api\n\ntype Gateway struct{}\n")
    write(root / "mock/assembly/assembly.go", "//go:build mock\n\npackage assembly\n\nfunc NewGateway() string { return \"mock\" }\n")
    write(root / "mock/business/scalp/api/gateway_mock.go", "//go:build mock\n\npackage mock_api\n\ntype MockGateway struct{}\n")


def adoption_manifest(legacy_mock: bool) -> dict[str, object]:
    """构造 backend 收敛清单，legacy_mock 表示 mock 根是否冻结为遗留快照。"""
    legacy_roots: list[dict[str, object]] = []
    if legacy_mock:
        legacy_roots.append({
            "path": "mock",
            "responsibility": "既有运行时 Mock 快照",
            "existing_directories": [
                "mock",
                "mock/assembly",
                "mock/business",
                "mock/business/scalp",
                "mock/business/scalp/api",
            ],
            "existing_files": ["mock/assembly/assembly.go", "mock/business/scalp/api/gateway_mock.go"],
        })
    return {
        "version": 1,
        "project_kind": "backend",
        "language": "go",
        "adopted_paths": [],
        "legacy_source_roots": legacy_roots,
    }


class RuntimeMockLayoutTests(unittest.TestCase):
    """覆盖 Mock Catalog 查询、strict/adoption 检查与 reference 一致性。"""

    def test_catalog_mock_categories_are_unique_and_guide_returns_recipe(self):
        """确认 backend/fullstack 五种 Mock 分类唯一可查，guide 返回完整配方。"""
        catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
        expected = {
            "backend": {
                "root": "mock",
                "selector-mock": "main_mock.go",
                "selector-real": "main_real.go",
                "assembly": "mock/assembly",
                "implementation": "mock/<internal-relative-path>",
            },
            "fullstack": {
                "root": "mock",
                "selector-mock": "backend/main_mock.go",
                "selector-real": "backend/main_real.go",
                "assembly": "mock/assembly",
                "implementation": "mock/<internal-relative-path>",
            },
        }
        for project_kind, categories in expected.items():
            for category, canonical_path in categories.items():
                with self.subTest(project_kind=project_kind, category=category):
                    result = run_cli(
                        "query", "--project-kind", project_kind, "--artifact", "mock", "--category", category,
                    )
                    self.assertEqual(0, result.returncode, result.stdout)
                    entry = json.loads(result.stdout)["entry"]
                    self.assertEqual(canonical_path, entry["canonical_path"])
                    self.assertEqual("forbidden", entry["init_policy"])
                    self.assertEqual("package-structure-rules", entry["owner_skill"])
                    expected_mock_fields = {
                        "selector-mock": ("required_build_tag", "mock"),
                        "selector-real": ("required_exclude_build_tag", "!mock"),
                        "assembly": ("required_build_tag", "mock"),
                    }
                    field, value = expected_mock_fields.get(category, (None, None))
                    if field:
                        self.assertEqual(value, entry[field], f"{category} 缺少 {field}={value}")
                    if category == "implementation":
                        self.assertEqual(
                            {"backend": "internal", "fullstack": "backend/internal"}[project_kind],
                            entry["mirror_source_root"],
                        )

        guide = run_cli("guide", "--category", "runtime-mock", "--language", "go")
        self.assertEqual(0, guide.returncode, guide.stdout)
        usage = json.loads(guide.stdout)["usage"]
        self.assertEqual(10, len(usage), "runtime-mock 配方应包含 backend/fullstack 各 5 类")
        self.assertEqual(
            {"backend", "fullstack"},
            {item["project_kind"] for item in usage},
        )
        self.assertTrue(
            all(item["owner_skill"] == "package-structure-rules" for item in usage),
            "runtime-mock 配方 owner_skill 应统一为 package-structure-rules",
        )

        for category in ("time", "json", "log"):
            with self.subTest(non_mock_guide_category=category):
                non_mock = run_cli("guide", "--category", category, "--language", "go")
                self.assertEqual(0, non_mock.returncode, non_mock.stdout)
                non_mock_usage = json.loads(non_mock.stdout)["usage"]
                self.assertTrue(non_mock_usage, "既有 guide 分类不应为空")
                self.assertEqual(
                    {"backend"},
                    {item["project_kind"] for item in non_mock_usage},
                    "仅 runtime-mock 分类启用 fullstack，其余分类保持 backend-only",
                )

        schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
        properties = schema["properties"]["entries"]["items"]["properties"]
        for field in (
            "category", "paired_with", "required_build_tag",
            "required_exclude_build_tag", "mirror_source_root", "forbidden_direct_imports",
        ):
            self.assertIn(field, properties, f"Schema 缺少字段 {field}")
        required = schema["properties"]["entries"]["items"]["required"]
        for field in ("owner_skill", "artifact_kind"):
            self.assertIn(field, required, f"Schema entries 缺少必填字段 {field}")

    def test_strict_accepts_good_runtime_mock_layout(self):
        """确认独立后端和同仓后端的完整运行时 Mock 结构通过 strict。"""
        for project_kind, writer in (
            ("backend", write_good_backend),
            ("fullstack", write_good_fullstack),
        ):
            with self.subTest(project_kind=project_kind), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                writer(root)
                before = directory_hash(root)
                result = run_cli(
                    "check", "--root", str(root), "--project-kind", project_kind,
                    "--language", "go", "--policy", "strict",
                )
                self.assertEqual(0, result.returncode, result.stdout)
                self.assertEqual(before, directory_hash(root))

    def test_strict_rejects_bad_runtime_mock_layouts_without_writing(self):
        """确认每类 Mock 违规均失败关闭且不写入 fixture。"""
        cases = (
            ("缺 real selector", lambda root: (root / "main_real.go").unlink(), "Mock selector 缺失: main_real.go"),
            ("mock selector 标签错误", lambda root: write(root / "main_mock.go", "//go:build !mock\n\npackage main\n\nfunc newGateway() string { return \"x\" }\n"), "selector 构建标签错误"),
            ("selector 函数不一致", lambda root: write(root / "main_real.go", "//go:build !mock\n\npackage main\n\nfunc newOther() string { return \"real\" }\n"), "Mock selector 函数集合不一致"),
            ("Mock 未镜像", lambda root: write(root / "mock/random/thing.go", "//go:build mock\n\npackage mock_thing\n\ntype Thing struct{}\n"), "Mock 镜像源缺失"),
            ("Mock 包名错误", lambda root: write(root / "mock/business/scalp/api/gateway_mock.go", "//go:build mock\n\npackage api\n\ntype MockGateway struct{}\n"), "Mock 包名必须为 mock_<源包名>"),
            ("入口直导入 Mock", lambda root: write(root / "main_mock.go", "//go:build mock\n\npackage main\n\nimport \"example.com/proj/mock/business/scalp/api\"\n\nfunc newGateway() string { return api.NewMockGateway() }\n"), "入口禁止直接导入 Mock 实现"),
            ("Mock 放入 internal", lambda root: write(root / "internal/business/scalp/api/mock_gateway.go", "//go:build mock\n\npackage mock_api\n\ntype MockGateway struct{}\n"), "运行时 Mock 禁止放入 internal"),
            ("assembly 包名错误", lambda root: write(root / "mock/assembly/assembly.go", "//go:build mock\n\npackage assemblyx\n\nfunc NewGateway() string { return \"x\" }\n"), "Mock assembly 包名必须为 assembly"),
        )
        for label, mutate, expected in cases:
            with self.subTest(label=label), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                write_good_backend(root)
                mutate(root)
                before = directory_hash(root)
                result = run_cli(
                    "check", "--root", str(root), "--project-kind", "backend",
                    "--language", "go", "--policy", "strict",
                )
                self.assertEqual(2, result.returncode, result.stdout)
                self.assertIn(expected, result.stdout)
                self.assertEqual(before, directory_hash(root))

    def test_adoption_skips_legacy_mock_and_validates_new_mock(self):
        """确认 adoption 冻结遗留 Mock 快照，同时仍校验新增/已采纳 Mock。"""
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write_good_backend(root)
            # 1. 故意破坏 legacy mock 的 build tag；冻结快照时不应触发新规则。
            write(root / "mock/assembly/assembly.go", "//go:build !mock\n\npackage assembly\n\nfunc NewGateway() string { return \"x\" }\n")
            manifest = root / "doc" / "1-架构" / "3-目录规则收敛清单.yaml"
            manifest.parent.mkdir(parents=True)
            manifest.write_text(json.dumps(adoption_manifest(True), ensure_ascii=False), encoding="utf-8")
            legacy_result = run_cli(
                "check", "--root", str(root), "--project-kind", "backend", "--language", "go",
                "--policy", "adoption", "--adoption-manifest", "doc/1-架构/3-目录规则收敛清单.yaml",
            )
            self.assertEqual(0, legacy_result.returncode, legacy_result.stdout)

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write_good_backend(root)
            write(root / "mock/assembly/assembly.go", "//go:build !mock\n\npackage assembly\n\nfunc NewGateway() string { return \"x\" }\n")
            manifest = root / "doc" / "1-架构" / "3-目录规则收敛清单.yaml"
            manifest.parent.mkdir(parents=True)
            manifest.write_text(json.dumps(adoption_manifest(False), ensure_ascii=False), encoding="utf-8")
            new_result = run_cli(
                "check", "--root", str(root), "--project-kind", "backend", "--language", "go",
                "--policy", "adoption", "--adoption-manifest", "doc/1-架构/3-目录规则收敛清单.yaml",
            )
            self.assertEqual(2, new_result.returncode, new_result.stdout)
            self.assertIn("Mock 文件必须使用 //go:build mock", new_result.stdout)

    def test_reference_and_catalog_are_consistent(self):
        """确认 runtime-mock-layout-go.md 与 Catalog 的镜像、标签和装配契约一致。"""
        reference = REFERENCE.read_text(encoding="utf-8")
        catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
        for required_text in (
            "//go:build mock",
            "//go:build !mock",
            "mock_<源包名>",
            "mock/assembly",
            "internal/",
        ):
            self.assertIn(required_text, reference, f"Reference 缺少 {required_text}")
        implementations = [entry for entry in catalog["entries"] if entry.get("category") == "implementation"]
        self.assertEqual(2, len(implementations))
        self.assertEqual(
            {"internal", "backend/internal"},
            {entry["mirror_source_root"] for entry in implementations},
        )
        self.assertTrue(all(entry["init_policy"] == "forbidden" for entry in implementations))
        self.assertTrue(all(entry["required_build_tag"] == "mock" for entry in implementations))


if __name__ == "__main__":
    unittest.main()
