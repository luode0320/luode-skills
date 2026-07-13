"""离线验证 distill_vault 仅经 bridge 写入固定知识库路径。"""

from __future__ import annotations

import importlib.util
import io
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from types import SimpleNamespace
from unittest import mock


REPOSITORY_ROOT = Path(__file__).resolve().parents[5]
DISTILL_PATH = REPOSITORY_ROOT / "obsidian-knowledge-flow/scripts/distill_vault.py"
SPEC = importlib.util.spec_from_file_location("distill_vault", DISTILL_PATH)
assert SPEC and SPEC.loader
distill = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = distill
SPEC.loader.exec_module(distill)


class DistillVaultBridgeTest(unittest.TestCase):
    """用临时源 vault 和 bridge mock 验证批处理目标写入契约。"""

    def build_args(self, source_root: Path, target_root: Path | str = r"D:\obsidian_data") -> SimpleNamespace:
        """构造仅含 TASK-OBS-05 所需参数的批处理输入。

        [参数] source_root: 测试临时源 vault；target_root: 目标 vault 根目录入参。
        [返回] 可供 distill main 使用的最小参数对象。
        最近修改时间: 2026-07-13 17:32:38 删除废弃 transport 字段，防止 fixture 掩盖旧参数读取。
        """
        return SimpleNamespace(
            source_vault="fixture-source",
            source_root=source_root,
            target_root=target_root,
            target_prefix="知识库/30-MOCs/blog-data",
            include=None,
            max_files=0,
            chunk_chars=1800,
            chunk_rows=99,
            append_delay=0,
            dry_run=False,
        )

    def create_source_fixture(self, root: Path) -> None:
        """建立三个顶层批次、四篇 Markdown 的最小源 vault fixture。

        [参数] root: 临时源 vault 根目录。
        [返回] 无。
        最近修改时间: 2026-07-13 覆盖根目录、普通分类和敏感分类的批处理样本。
        """
        # 1. 样本在临时目录内创建，避免读取用户的真实 source 或 target vault。
        (root / "根目录.md").write_text("# 根目录\n\n这是根目录的公开知识摘要。\n", encoding="utf-8")
        public = root / "01-公开"
        nested = public / "子类"
        sensitive = root / "02-敏感"
        nested.mkdir(parents=True)
        sensitive.mkdir()
        (public / "基础.md").write_text("# 基础\n\n这是公开基础知识，供检索使用。\n", encoding="utf-8")
        (nested / "进阶.md").write_text("# 进阶\n\n这是进阶公开知识，含有完整说明。\n", encoding="utf-8")
        (sensitive / "连接配置.md").write_text(
            "# 连接配置\n\napi_key: real-secret-value\n服务器地址为 10.20.30.40。\n",
            encoding="utf-8",
        )

    def bridge_recorder(self) -> tuple[dict[str, str], list[tuple[str, str | None, str | None]], object]:
        """构造不启动 CLI 的 bridge recorder，并模拟 create/append/read 状态。

        [参数] 无。
        [返回] 目标笔记存储、调用记录和可替换的 bridge 函数。
        最近修改时间: 2026-07-13 测试侧模拟 bridge，禁止写入真实用户 vault。
        """
        notes: dict[str, str] = {}
        calls: list[tuple[str, str | None, str | None]] = []

        def fake_bridge(operation: str, path: str | None = None, content: str | None = None) -> str:
            """记录 bridge allowlist 调用并维护内存笔记状态。

            [参数] operation: bridge 操作；path: vault 相对路径；content: 待写 Markdown。
            [返回] read 操作的内存笔记正文，其他操作返回空文本。
            最近修改时间: 2026-07-13 为离线 fixture 提供最小 bridge 行为。
            """
            # 1. 该 fake 不执行 subprocess，确保本测试无法触达真实 Obsidian 或 vault。
            calls.append((operation, path, content))
            if operation == "create":
                assert path is not None and content is not None
                notes[path] = content
            elif operation == "append":
                assert path is not None and content is not None
                notes[path] = notes.get(path, "") + content
            elif operation == "read":
                assert path is not None
                return notes.get(path, "")
            elif operation != "doctor":
                raise AssertionError(f"unexpected bridge operation: {operation}")
            return ""

        return notes, calls, fake_bridge

    def test_distill_batches_writes_rollup_index_and_redacts_source_secrets(self) -> None:
        """验证批次、逐篇数、全部知识路径、总览、INDEX 与脱敏结果。

        [参数] 无。
        [返回] 无。
        最近修改时间: 2026-07-13 覆盖 TEST-OBS-014 的离线批处理核心断言。
        """
        with tempfile.TemporaryDirectory() as directory:
            source_root = Path(directory) / "source-vault"
            source_root.mkdir()
            self.create_source_fixture(source_root)
            args = self.build_args(source_root)
            notes, calls, fake_bridge = self.bridge_recorder()

            # 1. main 只接收 mock bridge，验证整条批处理链路不会调用真实 vault。
            with mock.patch.object(distill, "parse_args", return_value=args), mock.patch.object(
                distill,
                "run_bridge",
                side_effect=fake_bridge,
            ), redirect_stdout(io.StringIO()):
                self.assertEqual(0, distill.main())

        expected_batch_paths = {
            "知识库/30-MOCs/blog-data/根目录-逐篇沉淀.md",
            "知识库/30-MOCs/blog-data/公开-逐篇沉淀.md",
            "知识库/30-MOCs/blog-data/敏感-逐篇沉淀.md",
        }
        rollup_path = "知识库/30-MOCs/blog-data/全量逐篇沉淀总览.md"
        self.assertTrue(expected_batch_paths.issubset(notes), notes)
        self.assertIn(rollup_path, notes)
        self.assertIn("知识库/INDEX.md", notes)

        # 2. 每个写入调用都必须受固定知识库前缀约束，不能落入嵌套 vault 或任意路径。
        write_paths = [path for operation, path, _content in calls if operation in {"create", "append"}]
        self.assertGreaterEqual(len(write_paths), 8)
        self.assertTrue(all(path and path.startswith("知识库/") for path in write_paths), write_paths)

        rollup = notes[rollup_path]
        self.assertIn("| 应处理 Markdown | 4 |", rollup)
        self.assertIn("| 成功读取并沉淀 | 4 |", rollup)
        self.assertIn("| 根目录 | `根目录` | 1 | 1 |", rollup)
        self.assertIn("| 公开 | `01-公开` | 2 | 2 |", rollup)
        self.assertIn("| 敏感 | `02-敏感` | 1 | 1 |", rollup)
        self.assertIn("blog-data 全量逐篇沉淀总览", notes["知识库/INDEX.md"])

        generated = "\n".join(notes.values())
        self.assertIn("敏感配置、资产或环境上下文", generated)
        self.assertNotIn("real-secret-value", generated)
        self.assertNotIn("10.20.30.40", generated)

    def test_legacy_nested_target_root_fails_before_any_target_write(self) -> None:
        """验证旧 nested target-root 返回稳定迁移错误而不写入目标笔记。

        [参数] 无。
        [返回] 无。
        最近修改时间: 2026-07-13 覆盖 TEST-OBS-012 与 TASK-OBS-05 停止条件。
        """
        with tempfile.TemporaryDirectory() as directory:
            source_root = Path(directory) / "source-vault"
            source_root.mkdir()
            args = self.build_args(source_root, r"D:\obsidian_data\知识库")
            notes, calls, fake_bridge = self.bridge_recorder()

            # 1. validation 虽会执行 bridge doctor，但 legacy root 必须在任何 create/append 前阻断。
            with mock.patch.object(distill, "run_bridge", side_effect=fake_bridge):
                with self.assertRaisesRegex(RuntimeError, "LEGACY_NESTED_VAULT_MODEL"):
                    distill.validate_cli_and_vaults(args)

        self.assertEqual({}, notes)
        self.assertEqual([("doctor", None, None)], calls)


if __name__ == "__main__":
    unittest.main(verbosity=2)
