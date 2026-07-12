#!/usr/bin/env python3
"""验证工程文档质量校验器的正例、负例和 N/A 处理。"""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
import sys


SCRIPT_DIR = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPT_DIR))

import validate_engineering_docs as validator  # noqa: E402


ROOT = Path(__file__).resolve().parents[2]
PROFILE_FILE = ROOT / "artifact-delivery-gate-rules" / "references" / "document-quality-profiles.yaml"


class EngineeringDocumentValidatorTests(unittest.TestCase):
    def setUp(self) -> None:
        self.payload = validator.load_profiles(PROFILE_FILE)

    def test_requirement_fixture_passes(self) -> None:
        document = ROOT / "doc" / "2-需求" / "2026-07-12_033322_需求与实施文档极致完备化.md"
        profile = self.payload["profiles"]["requirement"]
        result = validator.validate_document(document, "requirement", profile, self.payload, ROOT)
        self.assertTrue(result["valid"], result["errors"])

    def test_missing_section_is_rejected(self) -> None:
        source = ROOT / "doc" / "7-验收" / "2026-07-12_033322_需求与实施文档极致完备化_验收标准.md"
        text = source.read_text(encoding="utf-8").replace("## 4. 验收场景", "## 4. 删除的验收场景", 1)
        with tempfile.TemporaryDirectory() as directory:
            document = Path(directory) / "negative.md"
            document.write_text(text, encoding="utf-8")
            profile = self.payload["profiles"]["acceptance"]
            result = validator.validate_document(document, "acceptance", profile, self.payload, Path(directory))
        self.assertFalse(result["valid"])
        self.assertTrue(any("验收场景" in error for error in result["errors"]))

    def test_na_with_reason_is_allowed(self) -> None:
        errors: list[str] = []
        validator.check_na_reasons("字段：`N/A`；原因与证据：本任务不涉及数据库。", errors)
        self.assertEqual(errors, [])

    def test_markdown_image_policy_accepts_relative_png(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            document_dir = root / "doc" / "2-需求"
            image_dir = root / "doc" / "data" / "images"
            document_dir.mkdir(parents=True)
            image_dir.mkdir(parents=True)
            image = image_dir / "requirement.login-state-v1.png"
            image.write_bytes(b"\x89PNG\r\n\x1a\nfixture")
            text = (
                "图片资产决策：需要\n\n"
                "![IMG-DOC-001 登录状态对比](../data/images/requirement.login-state-v1.png)\n\n"
                "## 图片资产清单\n\n"
                "| 图片 ID | 用途 / 生成输入 | 来源 | 相对路径 | 版本 | 关联 REQ/RULE / AC / CYCLE / TASK | 引用章节 | 敏感状态 | 版权状态 |\n"
                "| --- | --- | --- | --- | --- | --- | --- | --- | --- |\n"
                "| `IMG-DOC-001` | 登录状态视觉对比 | imagegen | `../data/images/requirement.login-state-v1.png` | `v1` | `REQ-DOC-013 / AC-DOC-024` | 第 3 节 | 无敏感信息 | 已确认 |\n"
            )
            errors: list[str] = []
            report = validator.check_images(text, root, document_dir / "requirement.md", self.payload, errors)
        self.assertEqual(errors, [])
        self.assertEqual(report["ids"], ["IMG-DOC-001"])
        self.assertEqual(report["count"], 1)

    # test_shared_image_reference_is_allowed 验证同一资产可被不同 Markdown 文档共享引用。
    # [参数] 无：使用 requirement 文档命名的图片并从 overview 文档引用。
    # [返回] None：断言共享引用通过路径、签名、命名和清单校验。
    # 最近修改时间：2026-07-12 放宽共享资产的引用文档 stem 限制，保持唯一命名契约。
    def test_shared_image_reference_is_allowed(self) -> None:
        """验证共享图片不会因引用文档不同而被误判。"""
        # 1. 构造一个由 overview 文档共享引用的 requirement 图片资产。
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            document_dir = root / "doc" / "3-实施"
            image_dir = root / "doc" / "data" / "images"
            document_dir.mkdir(parents=True)
            image_dir.mkdir(parents=True)
            image = image_dir / "requirement.login-state-v1.png"
            image.write_bytes(b"\x89PNG\r\n\x1a\nfixture")
            text = (
                "图片资产决策：需要\n\n"
                "![IMG-DOC-001 登录状态对比](../data/images/requirement.login-state-v1.png)\n\n"
                "## 图片资产清单\n\n"
                "| 图片 ID | 用途 / 生成输入 | 来源 | 相对路径 | 版本 | 关联 REQ/RULE / AC / CYCLE / TASK | 引用章节 | 敏感状态 | 版权状态 |\n"
                "| --- | --- | --- | --- | --- | --- | --- | --- | --- |\n"
                "| `IMG-DOC-001` | 登录状态视觉对比 | imagegen | `../data/images/requirement.login-state-v1.png` | `v1` | `REQ-DOC-013 / AC-DOC-024` | 第 3 节 | 无敏感信息 | 已确认 |\n"
            )
            errors: list[str] = []
            report = validator.check_images(text, root, document_dir / "overview.md", self.payload, errors)
        self.assertEqual(errors, [])
        self.assertTrue(report["valid"])

    # test_markdown_image_policy_rejects_manifest_mismatch_and_bad_filename 验证清单缺字段、路径/版本不一致和命名违规均阻断。
    # [参数] 无：使用一个带图片但清单不一致的临时需求文档。
    # [返回] None：断言校验器输出三类明确错误。
    # 最近修改时间：2026-07-12 增加图片清单与命名模板的负向覆盖。
    def test_markdown_image_policy_rejects_manifest_mismatch_and_bad_filename(self) -> None:
        """验证图片清单不一致或文件名不符合模板时稳定阻断。"""
        # 1. 构造路径、版本和版权字段均不一致的图片资产清单。
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            document_dir = root / "doc" / "2-需求"
            image_dir = root / "doc" / "data" / "images"
            document_dir.mkdir(parents=True)
            image_dir.mkdir(parents=True)
            (image_dir / "wrong-name.png").write_bytes(b"\x89PNG\r\n\x1a\nfixture")
            text = (
                "图片资产决策：需要\n\n"
                "![IMG-DOC-002 登录状态对比](../data/images/wrong-name.png)\n\n"
                "## 图片资产清单\n\n"
                "| 图片 ID | 用途 / 生成输入 | 来源 | 相对路径 | 版本 | 关联 REQ/RULE / AC / CYCLE / TASK | 引用章节 | 敏感状态 | 版权状态 |\n"
                "| --- | --- | --- | --- | --- | --- | --- | --- | --- |\n"
                "| `IMG-DOC-002` | 登录状态视觉对比 | imagegen | `../data/images/other.png` | `v2` | `REQ-DOC-013` | 第 3 节 | 无敏感信息 | 已确认 |\n"
            )
            errors: list[str] = []
            validator.check_images(text, root, document_dir / "requirement.md", self.payload, errors)
        self.assertTrue(any("filename must match" in error for error in errors))
        self.assertTrue(any("path does not match" in error for error in errors))

    # test_image_manifest_version_mismatch_rejected 验证合法文件名的版本号必须与资产清单一致。
    # [参数] 无：使用合法文件名但错误清单版本的临时需求文档。
    # [返回] None：断言校验器输出版本不一致错误。
    # 最近修改时间：2026-07-12 拆分命名与版本负例，避免非法文件名掩盖版本解析。
    def test_image_manifest_version_mismatch_rejected(self) -> None:
        """验证资产清单版本必须匹配图片文件名。"""
        # 1. 构造合法命名但清单版本错误的图片资产。
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            document_dir = root / "doc" / "2-需求"
            image_dir = root / "doc" / "data" / "images"
            document_dir.mkdir(parents=True)
            image_dir.mkdir(parents=True)
            (image_dir / "requirement.login-state-v1.png").write_bytes(b"\x89PNG\r\n\x1a\nfixture")
            text = (
                "图片资产决策：需要\n\n"
                "![IMG-DOC-003 登录状态对比](../data/images/requirement.login-state-v1.png)\n\n"
                "## 图片资产清单\n\n"
                "| 图片 ID | 用途 / 生成输入 | 来源 | 相对路径 | 版本 | 关联 REQ/RULE / AC / CYCLE / TASK | 引用章节 | 敏感状态 | 版权状态 |\n"
                "| --- | --- | --- | --- | --- | --- | --- | --- | --- |\n"
                "| `IMG-DOC-003` | 登录状态视觉对比 | imagegen | `../data/images/requirement.login-state-v1.png` | `v2` | `REQ-DOC-013 / AC-DOC-024` | 第 3 节 | 无敏感信息 | 已确认 |\n"
            )
            errors: list[str] = []
            validator.check_images(text, root, document_dir / "requirement.md", self.payload, errors)
        self.assertTrue(any("version does not match" in error for error in errors))

    # test_orphan_image_scan_rejects_direct_data_root_image 验证 doc/data 根目录位图即使未被引用也会阻断。
    # [参数] 无：在允许图片目录外创建一个 PNG 文件。
    # [返回] None：断言孤儿扫描报告错位资产。
    # 最近修改时间：2026-07-12 增加旧图片根目录的机器拒绝覆盖。
    def test_orphan_image_scan_rejects_direct_data_root_image(self) -> None:
        """验证直接位于 doc/data 的图片被机器扫描拒绝。"""
        # 1. 构造 doc/data 根目录位图并执行孤儿扫描。
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            data_dir = root / "doc" / "data"
            data_dir.mkdir(parents=True)
            (data_dir / "legacy.png").write_bytes(b"\x89PNG\r\n\x1a\nlegacy")
            errors: list[str] = []
            report = validator.check_orphan_images(root, errors, self.payload)
        self.assertEqual(report["misplaced"], ["doc/data/legacy.png"])
        self.assertTrue(any("must be under doc/data/images" in error for error in errors))

    def test_markdown_image_policy_rejects_old_path_and_bad_signature(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            document_dir = root / "doc" / "2-需求"
            image_dir = root / "doc" / "data"
            document_dir.mkdir(parents=True)
            image_dir.mkdir(parents=True)
            image = image_dir / "old.png"
            image.write_bytes(b"not-a-png")
            errors: list[str] = []
            validator.check_images(
                "图片资产决策：需要\n![登录状态](../data/old.png)",
                root,
                document_dir / "requirement.md",
                self.payload,
                errors,
            )
        self.assertTrue(any("doc/data/images" in error for error in errors))
        self.assertTrue(any("IMG-*" in error for error in errors))

    def test_orphan_image_scan_rejects_unreferenced_asset(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            document_dir = root / "doc" / "2-需求"
            image_dir = root / "doc" / "data" / "images"
            document_dir.mkdir(parents=True)
            image_dir.mkdir(parents=True)
            referenced = image_dir / "used.png"
            orphan = image_dir / "orphan.png"
            referenced.write_bytes(b"\x89PNG\r\n\x1a\nused")
            orphan.write_bytes(b"\x89PNG\r\n\x1a\norphan")
            (document_dir / "requirement.md").write_text(
                "![IMG-DOC-001 Used](../data/images/used.png)", encoding="utf-8"
            )
            errors: list[str] = []
            report = validator.check_orphan_images(root, errors, self.payload)
        self.assertEqual(report["orphans"], ["doc/data/images/orphan.png"])
        self.assertTrue(any("orphan image asset" in error for error in errors))

    def test_fenced_image_example_is_not_an_asset_reference(self) -> None:
        errors: list[str] = []
        report = validator.check_images(
            "图片资产决策：N/A + 原因 + 证据：本节仅说明语法。\n\n"
            "```markdown\n![示例]()\n```\n",
            Path("."),
            Path("requirement.md"),
            self.payload,
            errors,
        )
        self.assertEqual(errors, [])
        self.assertEqual(report["count"], 0)

    def test_html_image_tag_is_rejected(self) -> None:
        errors: list[str] = []
        validator.check_images(
            "图片资产决策：N/A + 原因 + 证据：本节不需要图片。\n<img src='remote.png'>",
            Path("."),
            Path("requirement.md"),
            self.payload,
            errors,
        )
        self.assertTrue(any("HTML image tags" in error for error in errors))

    def test_image_na_decision_requires_reason_and_evidence(self) -> None:
        errors: list[str] = []
        validator.check_images(
            "图片资产决策：N/A",
            Path("."),
            Path("requirement.md"),
            self.payload,
            errors,
        )
        self.assertTrue(any("N/A requires reason/evidence" in error for error in errors))

    def test_fenced_image_decision_does_not_satisfy_document_decision(self) -> None:
        errors: list[str] = []
        validator.check_images(
            "```markdown\n图片资产决策：N/A + 原因 + 证据：仅示例\n```",
            Path("."),
            Path("requirement.md"),
            self.payload,
            errors,
        )
        self.assertTrue(any("decision must be explicit" in error for error in errors))

    def test_inline_na_value_is_allowed_when_decision_is_explicit(self) -> None:
        errors: list[str] = []
        validator.check_images(
            "图片资产决策：`N/A` + 原因 + 证据：本节仅定义规则。",
            Path("."),
            Path("requirement.md"),
            self.payload,
            errors,
        )
        self.assertEqual(errors, [])

    # test_normative_placeholder_reference_allowed 验证规范条款引用禁用词不会被误判为实际占位。
    # [参数] 无：使用包含“禁用占位词”说明的最小文本。
    # [返回] None：断言规范性引用不产生占位词错误。
    # 最近修改时间：2026-07-12 补充“禁用”同义规范词回归覆盖。
    def test_normative_placeholder_reference_allowed(self) -> None:
        """验证规范条款引用禁用词不会被误判为实际占位。"""
        # 1. 运行占位词检查并确认规则说明行被忽略。
        errors: list[str] = []
        validator.check_placeholders("M-004 禁用占位词：`待定`、`按经验`。", self.payload, errors)
        self.assertEqual(errors, [])

    # test_short_task_and_evidence_ids_are_collected 验证短任务 ID 与 EVD 证据 ID 会被统一提取。
    # [参数] 无：使用固定最小字符串样本。
    # [返回] None：断言提取结果包含任务与证据 ID。
    # 最近修改时间：2026-07-12 增加短 ID 回归样例，覆盖严格追踪新增正则。
    def test_short_task_and_evidence_ids_are_collected(self) -> None:
        """验证短任务 ID 与 EVD 证据 ID 会被统一提取。"""
        # 1. 调用 ID 提取函数并核对两个关键 ID。
        ids = validator.check_ids(
            "T01-02 has EVD-T01-02-IMPL-01 and EVD-T01-02-TEST-01.",
            {"id_prefixes": ["TASK"]},
            [],
        )
        self.assertIn("T01-02", ids)
        self.assertIn("EVD-T01-02-IMPL-01", ids)

    # test_mermaid_syntax_rejects_unbalanced_fixture 验证 Mermaid 括号不平衡时会被前置语法检查拒绝。
    # [参数] 无：使用一个故意损坏的 flowchart 样本。
    # [返回] None：断言错误列表包含括号不平衡提示。
    # 最近修改时间：2026-07-12 增加 Mermaid 语法负例，防止坏图绕过文档门禁。
    def test_mermaid_syntax_rejects_unbalanced_fixture(self) -> None:
        """验证 Mermaid 括号不平衡时会被前置语法检查拒绝。"""
        # 1. 执行图块检查并断言返回明确错误。
        errors: list[str] = []
        validator.check_diagram_annotations(
            "```mermaid\nflowchart TD\n  A[broken --> B[ok]\n```",
            errors,
        )
        self.assertTrue(any("unbalanced Mermaid delimiter" in error for error in errors))

    # test_strict_trace_rejects_orphan_task 验证缺少 REVIEW 证据的孤立任务会被严格追踪拒绝。
    # [参数] 无：在临时目录创建最小周期文档。
    # [返回] None：断言严格追踪报告缺少 REVIEW 证据。
    # 最近修改时间：2026-07-12 增加严格追踪负例，覆盖任务闭环不完整场景。
    def test_strict_trace_rejects_orphan_task(self) -> None:
        """验证缺少 REVIEW 证据的孤立任务会被严格追踪拒绝。"""
        # 1. 构造缺证据 fixture，执行严格追踪并断言阻断。
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "实施周期01.md").write_text(
                "T01-01 真实测试 停止 EVD-T01-01-IMPL-01 EVD-T01-01-TEST-01",
                encoding="utf-8",
            )
            errors: list[str] = []
            trace = validator.check_strict_trace(root, errors)
        self.assertEqual(trace["tasks"], ["T01-01"])
        self.assertTrue(any("REVIEW" in error for error in errors))

    # test_strict_trace_accepts_complete_task_chain 验证包含完整追踪链的任务可以通过。
    # [参数] 无：在临时目录创建最小完整周期文档。
    # [返回] None：断言严格追踪错误列表为空。
    # 最近修改时间：2026-07-12 增加严格追踪正例，锁定完整任务证据契约。
    def test_strict_trace_accepts_complete_task_chain(self) -> None:
        """验证包含完整 REQ/AC/CYCLE/TASK/TEST/EVIDENCE 链的任务可以通过。"""
        # 1. 构造完整 fixture，执行严格追踪并断言全部通过。
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "实施周期01.md").write_text(
                "REQ-1 AC-1 CYCLE-1 T01-01 TEST-1 EVIDENCE-1\n"
                "T01-01 真实测试 停止 EVD-T01-01-IMPL-01 "
                "EVD-T01-01-TEST-01 EVD-T01-01-REVIEW-01 EVD-T01-01-ACCEPT-01",
                encoding="utf-8",
            )
            errors: list[str] = []
            validator.check_strict_trace(root, errors)
        self.assertEqual(errors, [])

    # test_strict_trace_report_fields 验证严格模式所需机器报告字段始终存在。
    # [参数] 无：使用最小完整追踪 fixture。
    # [返回] None：断言报告含状态、追踪、覆盖率和未决决策字段。
    # 最近修改时间：2026-07-12 增加机器报告契约断言，避免只返回 valid/ids 的不完整报告。
    def test_strict_trace_report_fields(self) -> None:
        """验证严格模式机器报告具备验收标准要求的结构化字段。"""
        # 1. 运行单文档校验并核对统一机器报告字段。
        document = ROOT / "doc" / "2-需求" / "2026-07-12_033322_需求与实施文档极致完备化.md"
        profile = self.payload["profiles"]["requirement"]
        result = validator.validate_document(document, "requirement", profile, self.payload, ROOT)
        for field in ("status", "errors", "warnings", "ids", "traceability", "diagrams", "unresolved_decisions", "coverage"):
            self.assertIn(field, result)


if __name__ == "__main__":
    unittest.main()
