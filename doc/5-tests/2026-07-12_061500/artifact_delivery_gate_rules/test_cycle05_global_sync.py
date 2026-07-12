#!/usr/bin/env python3
"""周期 05 的入口同步、记忆收口、固定 vault 和最终放行集成测试。"""

from __future__ import annotations

import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
SCRIPT_DIR = ROOT / "artifact-delivery-gate-rules" / "scripts"
sys.path.insert(0, str(SCRIPT_DIR))
import validate_engineering_docs as validator  # noqa: E402


DOCS = [
    ROOT / "doc/2-需求/2026-07-12_033322_需求与实施文档极致完备化.md",
    ROOT / "doc/7-验收/2026-07-12_033322_需求与实施文档极致完备化_验收标准.md",
    ROOT / "doc/3-实施/2026-07-12_033322_需求与实施文档极致完备化_需求与实施计划全量顺序实施方案.md",
    ROOT / "doc/3-实施/2026-07-12_033322_需求与实施文档极致完备化_实施总览.md",
    ROOT / "doc/3-实施/2026-07-12_033322_需求与实施文档极致完备化_实施周期01_契约与基线.md",
    ROOT / "doc/3-实施/2026-07-12_042832_需求与实施文档极致完备化_实施周期02_需求入口与验收契约.md",
    ROOT / "doc/3-实施/2026-07-12_033322_需求与实施文档极致完备化_实施周期03_执行卡与输出门禁.md",
    ROOT / "doc/3-实施/2026-07-12_045805_需求与实施文档极致完备化_实施周期04_机械校验与图形验证.md",
    ROOT / "doc/3-实施/2026-07-12_061500_需求与实施文档极致完备化_实施周期05_全局同步与最终验收.md",
]


# run_command 在固定 local 工作区执行验证命令并返回 UTF-8 结果。
# [参数] command: 命令及参数列表；cwd: 可选工作目录；timeout: 超时秒数。
# [返回] CompletedProcess[str]：包含退出码、标准输出和标准错误。
# 最近修改时间：2026-07-12 新增统一命令包装，保证 Obsidian 与 Mermaid 测试使用相同编码和超时策略。
def run_command(command: list[str], cwd: Path | None = None, timeout: int = 60) -> subprocess.CompletedProcess[str]:
    """在固定 local 工作区执行验证命令并返回 UTF-8 结果。"""
    # 1. 以捕获输出、UTF-8 和超时约束执行命令。
    return subprocess.run(
        command,
        cwd=cwd or ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=timeout,
    )


class Cycle05GlobalSyncTests(unittest.TestCase):
    # test_current_documents_pass_profiles 验证需求、验收、总表、总览和周期文档全部通过质量 profile。
    # [参数] 无：使用 C05 固定文档清单和仓库 profile。
    # [返回] None：断言每份文档的 valid 标志为真。
    # 最近修改时间：2026-07-12 增加全量 profile 集成断言，覆盖 C05 收口输入。
    def test_current_documents_pass_profiles(self) -> None:
        """验证需求、验收、总表、总览和周期文档全部通过质量 profile。"""
        # 1. 加载 profile 并逐份校验当前交付文档。
        payload = validator.load_profiles(ROOT / "artifact-delivery-gate-rules/references/document-quality-profiles.yaml")
        targets = [
            ("requirement", DOCS[0]),
            ("acceptance", DOCS[1]),
            ("implementation_master", DOCS[2]),
            ("implementation_overview", DOCS[3]),
            ("implementation_cycle", DOCS[4]),
            ("implementation_cycle", DOCS[5]),
            ("implementation_cycle", DOCS[6]),
            ("implementation_cycle", DOCS[7]),
            ("implementation_cycle", DOCS[8]),
        ]
        for profile_name, document in targets:
            result = validator.validate_document(document, profile_name, payload["profiles"][profile_name], payload, ROOT)
            self.assertTrue(result["valid"], f"{document}: {result['errors']}")

    # test_final_acceptance_inputs_are_current 验证最终验收文档已引用 C02 至 C05 的最新输入。
    # [参数] 无：读取固定来源对象对应的最终验收文档。
    # [返回] None：断言周期证据、审查证据和最终验收 ID 均存在。
    # 最近修改时间：2026-07-12 增加最终验收输入一致性断言，防止旧文档内容回退。
    def test_final_acceptance_inputs_are_current(self) -> None:
        """验证最终验收文档已引用 C02 至 C05 的最新输入并移除旧阻断口径。"""
        # 1. 定位最终验收文档并检查最新周期互链和旧结论清理。
        final_acceptance = next(
            path
            for path in (ROOT / "doc/7-验收").glob("2026-07-12_033322_*")
            if path.name.endswith("最终验收.md")
        )
        content = final_acceptance.read_text(encoding="utf-8")
        for evidence_name in (
            "C02-CLOSE-验收证据.md",
            "C03-CLOSE-验收证据.md",
            "C04-CLOSE-验收证据.md",
            "C05-CLOSE-验收证据.md",
        ):
            self.assertIn(evidence_name, content)
        self.assertIn("C05-CLOSE", content)
        self.assertNotIn("后续周期未开始", content)
        self.assertNotIn("解析器不可用", content)
        self.assertIn("REVIEW-DOC-COMPLETENESS-20260712-033322", content)
        self.assertIn("FINAL-AC-DOC-COMPLETENESS-20260712-033322", content)

    # test_storage_and_owner_entrypoints_are_consistent 验证存储路径、仓库规则和核心 skill 入口契约一致。
    # [参数] 无：读取路径映射、仓库规则和核心 skill 文档。
    # [返回] None：断言目录入口、极致完整性和真实测试要求均存在。
    # 最近修改时间：2026-07-12 增加入口一致性断言，避免规则更新只落在单一文件。
    def test_storage_and_owner_entrypoints_are_consistent(self) -> None:
        """验证存储路径、仓库规则和四个核心 skill 的入口契约保持一致。"""
        # 1. 对照路径映射、平台规则和四个核心 skill 的共同契约。
        path_map = (ROOT / "artifact-storage-rules/references/path-map.yaml").read_text(encoding="utf-8")
        for expected in ("doc/2-需求", "doc/3-实施", "doc/5-tests", "doc/6-审查", "doc/7-验收"):
            self.assertIn(expected, path_map)
        agents = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
        claude = (ROOT / "CLAUDE.md").read_text(encoding="utf-8")
        encoding = (ROOT / "编码skill.md").read_text(encoding="utf-8")
        self.assertIn("极致完整性", agents)
        self.assertIn("极致完整性", claude)
        self.assertIn("编码", encoding)
        for skill_name in (
            "requirement-intake-rules",
            "acceptance-criteria-rules",
            "implementation-planning-rules",
            "artifact-delivery-gate-rules",
        ):
            skill = (ROOT / skill_name / "SKILL.md").read_text(encoding="utf-8")
            self.assertIn("普通模型", skill, skill_name)
            self.assertTrue("真实测试" in skill or "可测试" in skill or "测试" in skill, skill_name)

    # test_project_memory_and_dictionary_are_current 验证项目四件套和 skill 字典已同步到 C05 收口状态。
    # [参数] 无：读取当前状态、稳定记忆、历史、字典和生成数据。
    # [返回] None：断言周期状态、机器索引和核心 skill 条目均存在。
    # 最近修改时间：2026-07-12 增加字典生成和敏感 diff 扫描断言，保证交接信息完整。
    def test_project_memory_and_dictionary_are_current(self) -> None:
        """验证项目四件套和 skill 字典已同步到 C05 收口状态。"""
        # 1. 读取并检查四件套大小、周期状态和字典生成结果。
        current = (ROOT / "PROJECT_CURRENT.md").read_text(encoding="utf-8")
        memory = (ROOT / "PROJECT_MEMORY.md").read_text(encoding="utf-8")
        history = (ROOT / "PROJECT_HISTORY.md").read_text(encoding="utf-8")
        dictionary = (ROOT / "字典.md").read_text(encoding="utf-8")
        data_js = (ROOT / "skill-dictionary/data.js").read_text(encoding="utf-8")
        self.assertLessEqual((ROOT / "PROJECT_CURRENT.md").stat().st_size, 51200)
        self.assertIn("周期 05", current)
        self.assertIn("机器索引区", memory)
        self.assertIn("周期 05", history)
        self.assertIn("implementation-planning-rules", dictionary)
        self.assertIn("implementation-planning-rules", data_js)
        # 2. 重新运行生成器并扫描当前 diff，避免只凭静态文件存在性放行。
        generated = run_command([sys.executable, "-X", "utf8", "skill-dictionary/generate_dictionary.py"])
        self.assertEqual(generated.returncode, 0, generated.stderr or generated.stdout)
        self.assertIn('"planned_missing": 0', generated.stdout)
        diff = run_command(["git", "diff", "--unified=0"])
        self.assertEqual(diff.returncode, 0, diff.stderr or diff.stdout)
        sensitive = re.compile(r"sk-[A-Za-z0-9]{20,}|AKIA[0-9A-Z]{16}")
        self.assertIsNone(sensitive.search(diff.stdout))

    # test_obsidian_cli_reads_fixed_vault 验证 Obsidian CLI 只使用固定 local vault 并能读回沉淀笔记。
    # [参数] 无：使用固定 D:\\obsidian_data vault 和知识库路径。
    # [返回] None：断言 CLI、vault、搜索和读取命令全部成功。
    # 最近修改时间：2026-07-12 增加固定 vault 真实读取验证，锁定知识沉淀链路。
    def test_obsidian_cli_reads_fixed_vault(self) -> None:
        """验证 Obsidian CLI 只使用固定 local vault 并能读回沉淀笔记。"""
        # 1. 定位 CLI 并验证版本、vault 注册、搜索和笔记读取。
        executable = shutil.which("obsidian") or shutil.which("obsidian.com")
        self.assertIsNotNone(executable, "obsidian CLI is required")
        cwd = Path(r"D:\obsidian_data")
        version = run_command([executable, "version"], cwd=cwd)
        self.assertEqual(version.returncode, 0, version.stderr or version.stdout)
        self.assertIn("1.12.7", version.stdout)
        vaults = run_command([executable, "vaults", "verbose"], cwd=cwd)
        self.assertEqual(vaults.returncode, 0, vaults.stderr or vaults.stdout)
        self.assertIn(r"D:\obsidian_data\知识库", vaults.stdout)
        search = run_command([executable, "vault=知识库", "search", "query=需求与实施文档", "limit=10"], cwd=cwd)
        self.assertEqual(search.returncode, 0, search.stderr or search.stdout)
        self.assertIn("需求与实施文档零决策交接.md", search.stdout)
        read = run_command(
            [executable, "vault=知识库", "read", "path=知识库/20-Knowledge/需求与实施文档零决策交接.md"],
            cwd=cwd,
        )
        self.assertEqual(read.returncode, 0, read.stderr or read.stdout)
        self.assertIn("普通模型零决策执行", read.stdout)
        self.assertIn("周期 05 收口", read.stdout)

    # test_cycle05_mermaid_cli_renders_nonempty_svg 验证 C05 文档经 Mermaid CLI 真实解析后生成非空 SVG。
    # [参数] 无：使用 C05 周期文档和本地 npx Mermaid CLI。
    # [返回] None：断言命令成功且至少生成两个非空 SVG。
    # 最近修改时间：2026-07-12 增加 Mermaid 真解析门禁，避免轻量检查误放坏图。
    def test_cycle05_mermaid_cli_renders_nonempty_svg(self) -> None:
        """验证 C05 周期文档经 Mermaid CLI 真实解析后生成非空 SVG。"""
        # 1. 在临时目录运行 Mermaid CLI 并核对 SVG 产物。
        npx = shutil.which("npx") or shutil.which("npx.cmd")
        self.assertIsNotNone(npx, "npx is required for Mermaid true parsing")
        document = DOCS[8]
        with tempfile.TemporaryDirectory(prefix="codex-mermaid-c05-") as directory:
            output = Path(directory) / "cycle05.md"
            result = run_command(
                [npx, "--offline", "--yes", "@mermaid-js/mermaid-cli", "-i", str(document), "-o", str(output), "-q"],
                timeout=60,
            )
            self.assertEqual(result.returncode, 0, result.stderr or result.stdout)
            svgs = list(Path(directory).glob("cycle05*.svg"))
            self.assertGreaterEqual(len(svgs), 2)
            self.assertTrue(all(svg.stat().st_size > 0 for svg in svgs))


if __name__ == "__main__":
    unittest.main(verbosity=2)
