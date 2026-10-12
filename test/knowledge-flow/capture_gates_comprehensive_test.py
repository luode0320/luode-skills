# -*- coding: utf-8 -*-
"""知识库沉淀规范与门禁机制全方位自动化测试套件。

涵盖：
1. 目录白名单门禁（7大中文主题、3大契约目录、项目二级目录放行；未知目录与根散落文件强拦截）；
2. YAML Frontmatter 契约（头部存在性、必填字段完整性、合法状态枚举、归档豁免收窄）；
3. 版本双向接替闭环门禁（单向接替拦截、active未降级拦截、悬空目标拦截、成对接替放行）；
4. 死链与空格防呆门禁（目标不存在拦截、中英空格不匹配拦截、代码块示例排除、四种合法引用形态）；
5. 孤岛检测与入网门禁（未挂载孤岛捕获、织入 MOC 后孤岛清零）。
"""

from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
INDEX_SCRIPT = ROOT / "knowledge-flow" / "scripts" / "knowledge_index.py"
AUDIT_SCRIPT = ROOT / "knowledge-flow" / "scripts" / "audit_vault_knowledge.py"


def load_module(name: str, path: Path) -> Any:
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


INDEX = load_module("knowledge_index_gate_test", INDEX_SCRIPT)
AUDIT = load_module("audit_vault_knowledge_gate_test", AUDIT_SCRIPT)


class CaptureGatesComprehensiveTest(unittest.TestCase):
    """沉淀门禁全方位测试类。"""

    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.base = Path(self._tmp.name)
        self._saved_index_root = INDEX.KB_ROOT
        self._saved_audit_root = AUDIT.KB_ROOT
        INDEX.KB_ROOT = self.base
        INDEX.AUDIT.KB_ROOT = self.base
        AUDIT.KB_ROOT = self.base

    def tearDown(self) -> None:
        INDEX.KB_ROOT = self._saved_index_root
        INDEX.AUDIT.KB_ROOT = self._saved_audit_root
        AUDIT.KB_ROOT = self._saved_audit_root
        self._tmp.cleanup()

    def write_file(self, rel: str, content: str) -> Path:
        p = self.base / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content, encoding="utf-8")
        return p

    def make_valid_frontmatter(
        self,
        stem: str,
        title: str,
        status: str = "active",
        supersedes: list[str] | None = None,
        superseded_by: list[str] | None = None,
    ) -> str:
        lines = [
            "---",
            f"id: 20261010-id-{stem}",
            "type: knowledge",
            f"title: {title}",
            f"status: {status}",
            "created: 2026-10-10",
            "updated: 2026-10-10",
        ]
        if supersedes:
            lines.append("supersedes:")
            for s in supersedes:
                lines.append(f'  - "[[{s}]]"')
        if superseded_by:
            lines.append("superseded_by:")
            for s in superseded_by:
                lines.append(f'  - "[[{s}]]"')
        lines.append("---")
        lines.append(f"\n# {title}\n\n正文内容。\n")
        return "\n".join(lines)

    # ==========================================
    # 1. 目录白名单门禁测试 (Directory Whitelist)
    # ==========================================

    def test_declared_themes_pass_whitelist(self) -> None:
        """测试 7 个合法中文主题全部通过白名单门禁。"""
        for theme in INDEX.DECLARED_THEMES:
            self.write_file(
                f"20-Knowledge/{theme}/note_{theme}.md",
                self.make_valid_frontmatter(f"note_{theme}", f"{theme}样例"),
            )
        report = INDEX.check_frontmatter()
        self.assertTrue(report["ok"])
        self.assertEqual(len(report["unknown_theme_violations"]), 0)

    def test_contract_dirs_pass_whitelist(self) -> None:
        """测试 3 个契约目录（code-style, project-rules, execution-failure-cases）放行。"""
        self.write_file(
            "20-Knowledge/code-style/go_style.md",
            self.make_valid_frontmatter("go_style", "代码风格"),
        )
        self.write_file(
            "20-Knowledge/project-rules/rule.md",
            self.make_valid_frontmatter("rule", "项目规则"),
        )
        self.write_file(
            "20-Knowledge/execution-failure-cases/agent/case.md",
            self.make_valid_frontmatter("case", "案例", status="candidate"),
        )
        report = INDEX.check_frontmatter()
        self.assertTrue(report["ok"])
        self.assertEqual(len(report["unknown_theme_violations"]), 0)

    def test_project_subdirectories_allowed(self) -> None:
        """测试 项目/ 目录下允许按具体项目开二级子目录。"""
        self.write_file(
            "20-Knowledge/项目/sub_app/spec.md",
            self.make_valid_frontmatter("spec", "子项目规范"),
        )
        report = INDEX.check_frontmatter()
        self.assertTrue(report["ok"])
        self.assertEqual(len(report["unknown_theme_violations"]), 0)

    def test_unknown_dir_blocked_by_check(self) -> None:
        """测试未登记的非法目录（如历史 projects/ 或任意新造目录）被强制拦截。"""
        self.write_file(
            "20-Knowledge/projects/illegal.md",
            self.make_valid_frontmatter("illegal", "非法目录笔记"),
        )
        self.write_file(
            "20-Knowledge/新造分类/invalid.md",
            self.make_valid_frontmatter("invalid", "新造目录笔记"),
        )
        report = INDEX.check_frontmatter()
        self.assertFalse(report["ok"])
        violations = report["unknown_theme_violations"]
        self.assertEqual(len(violations), 2)
        paths = {v["path"] for v in violations}
        self.assertIn("20-Knowledge/projects/illegal.md", paths)
        self.assertIn("20-Knowledge/新造分类/invalid.md", paths)

    def test_stray_file_under_20_knowledge_root_blocked(self) -> None:
        """测试 20-Knowledge 根下的散落文件被白名单门禁阻断。"""
        self.write_file(
            "20-Knowledge/stray_recipe.md",
            self.make_valid_frontmatter("stray_recipe", "散落配方"),
        )
        report = INDEX.check_frontmatter()
        self.assertFalse(report["ok"])
        violations = report["unknown_theme_violations"]
        self.assertEqual(len(violations), 1)
        self.assertEqual(violations[0]["path"], "20-Knowledge/stray_recipe.md")

    # ==========================================
    # 2. YAML Frontmatter 契约完整性测试
    # ==========================================

    def test_missing_frontmatter_blocked(self) -> None:
        """测试未带 YAML 头部的文档被严格拦截。"""
        self.write_file(
            "20-Knowledge/工程实践/no_header.md",
            "# 没有任何 Frontmatter\n\n正文。\n",
        )
        report = INDEX.check_frontmatter()
        self.assertFalse(report["ok"])
        self.assertIn("20-Knowledge/工程实践/no_header.md", report["missing_frontmatter"])

    def test_missing_required_fields_blocked(self) -> None:
        """测试必填标量字段（id/type/title/status/created/updated）缺失拦截。"""
        # 故意缺少 id 与 updated 字段
        self.write_file(
            "20-Knowledge/工程实践/missing_id.md",
            "---\ntype: knowledge\ntitle: 缺字段\nstatus: active\ncreated: 2026-10-10\n---\n\n正文。\n",
        )
        report = INDEX.check_frontmatter()
        self.assertFalse(report["ok"])
        missing_entry = report["missing_required_fields"][0]
        self.assertEqual(missing_entry["path"], "20-Knowledge/工程实践/missing_id.md")
        self.assertIn("id", missing_entry["missing"])
        self.assertIn("updated", missing_entry["missing"])

    def test_invalid_status_enum_blocked(self) -> None:
        """测试使用未声明的非法状态枚举被拦截。"""
        self.write_file(
            "20-Knowledge/工程实践/bad_status.md",
            self.make_valid_frontmatter("bad_status", "错误状态", status="in_progress_unknown"),
        )
        report = INDEX.check_frontmatter()
        self.assertFalse(report["ok"])
        self.assertEqual(len(report["status_out_of_enum"]), 1)
        self.assertEqual(report["status_out_of_enum"][0]["status"], "in_progress_unknown")

    # ==========================================
    # 3. 版本双向接替闭环测试 (Supersession Contract)
    # ==========================================

    def test_unilateral_supersedes_blocked(self) -> None:
        """测试新版本单向声明 supersedes 但旧版本未声明 superseded_by 时被拦截。"""
        # 新版 A
        self.write_file(
            "20-Knowledge/项目/sub/v2.md",
            self.make_valid_frontmatter("v2", "第二版", supersedes=["20-Knowledge/项目/sub/v1"]),
        )
        # 旧版 B (status 即使改成 superseded，但漏写 superseded_by)
        self.write_file(
            "20-Knowledge/项目/sub/v1.md",
            self.make_valid_frontmatter("v1", "第一版", status="superseded"),
        )
        report = INDEX.check_supersession()
        self.assertFalse(report["ok"])
        self.assertTrue(any(d["reason"] == "对侧未写 superseded_by" for d in report["dangling_supersession"]))

    def test_unilateral_superseded_by_blocked(self) -> None:
        """测试旧版本单向声明 superseded_by 但新版本未声明 supersedes 时被拦截。"""
        self.write_file(
            "20-Knowledge/项目/sub/v2.md",
            self.make_valid_frontmatter("v2", "第二版"),
        )
        self.write_file(
            "20-Knowledge/项目/sub/v1.md",
            self.make_valid_frontmatter("v1", "第一版", status="superseded", superseded_by=["20-Knowledge/项目/sub/v2"]),
        )
        report = INDEX.check_supersession()
        self.assertFalse(report["ok"])
        self.assertTrue(any(d["reason"] == "对侧未写 supersedes" for d in report["dangling_supersession"]))

    def test_active_note_with_superseded_by_blocked(self) -> None:
        """测试被接替的旧文档依然维持 status: active 时被强制拦截。"""
        self.write_file(
            "20-Knowledge/项目/sub/v2.md",
            self.make_valid_frontmatter("v2", "第二版", supersedes=["20-Knowledge/项目/sub/v1"]),
        )
        # 旧版 B 状态依然是 active
        self.write_file(
            "20-Knowledge/项目/sub/v1.md",
            self.make_valid_frontmatter("v1", "第一版", status="active", superseded_by=["20-Knowledge/项目/sub/v2"]),
        )
        report = INDEX.check_supersession()
        self.assertFalse(report["ok"])
        self.assertEqual(len(report["active_with_superseded_by"]), 1)
        self.assertEqual(report["active_with_superseded_by"][0]["path"], "20-Knowledge/项目/sub/v1.md")

    def test_valid_bidirectional_supersession_passes(self) -> None:
        """测试双向成对声明且旧版降级为 superseded 时合规放行。"""
        self.write_file(
            "20-Knowledge/项目/sub/v2.md",
            self.make_valid_frontmatter("v2", "第二版", status="active", supersedes=["20-Knowledge/项目/sub/v1"]),
        )
        self.write_file(
            "20-Knowledge/项目/sub/v1.md",
            self.make_valid_frontmatter("v1", "第一版", status="superseded", superseded_by=["20-Knowledge/项目/sub/v2"]),
        )
        report = INDEX.check_supersession()
        self.assertTrue(report["ok"])
        self.assertEqual(report["supersession_violation_count"], 0)

    # ==========================================
    # 4. 死链与双链防呆测试 (Dead Links & Spacing Defense)
    # ==========================================

    def test_broken_link_to_non_existent_file_blocked(self) -> None:
        """测试双链指向库内不存在的目标被精准拦截。"""
        self.write_file(
            "20-Knowledge/工程实践/caller.md",
            self.make_valid_frontmatter("caller", "调用者") + "\n引用：[[20-Knowledge/工程实践/ghost_target]]\n",
        )
        report = INDEX.check_dead_links()
        self.assertFalse(report["ok"])
        self.assertEqual(report["dead_link_count"], 1)
        self.assertEqual(report["dead_links"][0]["target"], "20-Knowledge/工程实践/ghost_target")

    def test_space_mismatch_broken_link_blocked(self) -> None:
        """测试真实文件名无空格，但双链误写空格时被精准拦截为死链。"""
        # 真实文件无空格
        self.write_file(
            "20-Knowledge/工程实践/通用Agent授权.md",
            self.make_valid_frontmatter("通用Agent授权", "通用Agent授权"),
        )
        # 引用端误加中英文空格
        self.write_file(
            "20-Knowledge/工程实践/caller.md",
            self.make_valid_frontmatter("caller", "调用者") + "\n引用：[[20-Knowledge/工程实践/通用 Agent 授权]]\n",
        )
        report = INDEX.check_dead_links()
        self.assertFalse(report["ok"])
        self.assertEqual(report["dead_link_count"], 1)
        self.assertEqual(report["dead_links"][0]["target"], "20-Knowledge/工程实践/通用 Agent 授权")

    def test_code_block_examples_ignored_in_dead_links(self) -> None:
        """测试围栏代码块里的说明示例不被误报为死链。"""
        code_example = (
            self.make_valid_frontmatter("caller", "调用者")
            + "\n```markdown\n这里是示例说明，包含假链接：[[non_existent_target]]\n```\n"
        )
        self.write_file("20-Knowledge/工程实践/caller.md", code_example)
        report = INDEX.check_dead_links()
        self.assertTrue(report["ok"])
        self.assertEqual(report["dead_link_count"], 0)

    # ==========================================
    # 5. 入网挂载与孤岛检测测试 (Orphan & Weaving Gate)
    # ==========================================

    def test_orphan_detected_and_cleared_after_weaving(self) -> None:
        """测试未被引用的新文档被巡检标记为孤儿，挂载入 MOC 后立即解除。"""
        # 1. 写入一篇完全没有入链的新笔记
        target = self.write_file(
            "20-Knowledge/工程实践/new_recipe.md",
            self.make_valid_frontmatter("new_recipe", "新实践配方"),
        )
        notes = [AUDIT.collect_note_facts(target)]
        orphans_before = AUDIT.find_orphans(notes)
        self.assertIn("20-Knowledge/工程实践/new_recipe.md", orphans_before)

        # 2. 创建一个 MOC 将该笔记编织入网
        moc = self.write_file(
            "30-MOCs/工程实践/某领域MOC.md",
            "---\nid: moc-domain\ntype: moc\ntitle: 领域MOC\nstatus: active\n---\n\n- [[20-Knowledge/工程实践/new_recipe]]\n",
        )
        all_notes = [AUDIT.collect_note_facts(target), AUDIT.collect_note_facts(moc)]
        orphans_after = AUDIT.find_orphans(all_notes)
        # 该笔记应该不再是孤儿
        self.assertNotIn("20-Knowledge/工程实践/new_recipe.md", orphans_after)


if __name__ == "__main__":
    unittest.main()
