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

    def _layered_document(self, gate_yaml: str, opening: str = "本次结果已经清楚，业务人员可以继续查看完成标准。", technical: str = "技术细节放在原有章节。") -> str:
        return f"""---
schema_version: 1
doc_id: DOC-1
doc_type: test
source_ids: [SRC-1]
status: draft
version: v1.0
current_slice: current
updated_at: 2026-07-12
reader_level: business_general
writing_style: plain_chinese
appendix_policy: preserve_existing_or_one_terminal_appendix
review_acceptance_gates:
{gate_yaml}
---
# 文档说明
{opening}

## 文档信息
这是用于测试的文档信息。

## 完成标准
读者可以根据本节判断是否完成。

## 技术细节
{technical}

图片资产决策：N/A + 原因 + 证据：本次 fixture 不需要图片。
"""

    def test_review_acceptance_gate_not_applicable_is_non_blocking(self) -> None:
        """第三方接口不适用时，不需要伪造证据，也不阻断。"""
        text = self._layered_document("""  - stage: third_party
    applicability: not_applicable
    reason: 本次范围不调用第三方接口。
    basis: 需求范围只包含本地流程。
    required_by_source: false
    required_now: false
    completed_validation: []
    substitute_validation: []
    manual_follow_up: N/A
    pass_standard: N/A""")
        with tempfile.TemporaryDirectory() as directory:
            document = Path(directory) / "document.md"
            document.write_text(text, encoding="utf-8")
            result = validator.validate_document(document, "test", self.payload["profiles"]["test"], self.payload, Path(directory))
        self.assertTrue(result["valid"], result["errors"])
        self.assertEqual(result["gates"]["release_status"], "allowed")
        self.assertFalse(result["gates"]["blocking"])

    def test_review_acceptance_gate_limited_allows_progress_but_not_release(self) -> None:
        """受限验证可以继续准备，但不能当作正式放行。"""
        text = self._layered_document("""  - stage: browser_integration
    applicability: limited
    reason: 浏览器授权环境当前不可用。
    basis: 当前环境只有本地功能验证条件。
    required_by_source: true
    required_now: true
    completed_validation: []
    substitute_validation: [EVD-LOCAL-VALIDATION-01]
    manual_follow_up: 条件具备后补做浏览器联调。
    pass_standard: 页面主流程和关键异常场景均通过。""")
        document = Path("document.md")
        document.write_text(text, encoding="utf-8")
        try:
            result = validator.validate_document(document, "test", self.payload["profiles"]["test"], self.payload, Path("."))
        finally:
            document.unlink(missing_ok=True)
        self.assertTrue(result["valid"], result["errors"])
        self.assertEqual(result["gates"]["release_status"], "limited")
        self.assertFalse(result["gates"]["blocking"])
        self.assertEqual(result["status"], "LIMITED")

    def test_new_profile_document_requires_plain_language_fields(self) -> None:
        """新建受管文档缺少白话字段时不能绕过契约。"""
        text = "---\nschema_version: 1\ndoc_id: DOC-1\ndoc_type: test\nsource_ids: [SRC-1]\nstatus: draft\nversion: v1\ncurrent_slice: current\nupdated_at: 2026-07-13\n---\n# 文档说明\n这是普通中文结论。\n\n## 文档信息\n说明。\n\n## 完成标准\n说明。\n"
        with tempfile.TemporaryDirectory() as directory:
            document = Path(directory) / "document.md"
            document.write_text(text, encoding="utf-8")
            result = validator.validate_document(document, "test", self.payload["profiles"]["test"], self.payload, Path(directory))
        self.assertFalse(result["valid"])
        self.assertTrue(any("reader_level" in error for error in result["errors"]))
        self.assertTrue(any("review_acceptance_gates" in error for error in result["errors"]))

    def test_unchanged_historical_document_keeps_legacy_contract(self) -> None:
        """未修改的历史文档不因新契约缺字段而被强制迁移。"""
        text = "---\nschema_version: 1\ndoc_id: DOC-OLD\ndoc_type: test\nsource_ids: [SRC-OLD]\nstatus: accepted\nversion: v1\ncurrent_slice: old\nupdated_at: 2026-07-01\n---\n# 历史文档\n历史正文没有白话元数据。\n\n图片资产决策：N/A + 原因 + 证据：历史文档不新增图片。\n"
        with tempfile.TemporaryDirectory() as directory:
            document = Path(directory) / "historical.md"
            document.write_text(text, encoding="utf-8")
            original = validator.document_is_new_or_modified
            try:
                validator.document_is_new_or_modified = lambda *_: False
                result = validator.validate_document(document, "test", self.payload["profiles"]["test"], self.payload, Path(directory))
            finally:
                validator.document_is_new_or_modified = original
        self.assertTrue(result["valid"], result["errors"])

    def test_heading_baseline_preserves_numbering_text(self) -> None:
        """标题编号变化也必须被 HEAD 基线识别。"""
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            document = root / "document.md"
            document.write_text("# 文档\n开场。\n\n## 2. 目标\n内容。\n", encoding="utf-8")
            errors: list[str] = []
            original = validator.subprocess.run
            try:
                def fake_run(command, **kwargs):
                    if command[:2] == ["git", "ls-files"]:
                        return type("Result", (), {"returncode": 0, "stdout": "document.md\n"})()
                    if command[:3] == ["git", "show", "HEAD:document.md"]:
                        return type("Result", (), {"returncode": 0, "stdout": "# 文档\n开场。\n\n## 1. 目标\n内容。\n"})()
                    return type("Result", (), {"returncode": 0, "stdout": ""})()
                validator.subprocess.run = fake_run
                validator.check_heading_baseline(document, document.read_text(encoding="utf-8"), root, errors, [])
            finally:
                validator.subprocess.run = original
        self.assertTrue(any("heading baseline mismatch" in error for error in errors))

    def test_review_acceptance_gate_required_without_validation_blocks_release(self) -> None:
        """来源明确要求且当前必须完成的验证没有证据时阻断。"""
        text = self._layered_document("""  - stage: acceptance
    applicability: applicable
    reason: 来源明确要求第三方接口验收。
    basis: 验收标准规定必须检查约定返回结果。
    required_by_source: true
    required_now: true
    completed_validation: []
    substitute_validation: []
    manual_follow_up: N/A
    pass_standard: 接口返回约定结果。""")
        errors: list[str] = []
        report = validator.check_plain_language_contract(text, errors)
        self.assertFalse(report["valid"])
        self.assertTrue(report["blocking"])
        self.assertEqual(report["release_status"], "blocked")
        self.assertIn("gate.required_validation_missing", report["error_codes"])

    def test_review_acceptance_gate_applicable_with_completed_validation_passes(self) -> None:
        """适用验证有完成证据时允许正式放行。"""
        text = self._layered_document("""  - stage: functional_validation
    applicability: applicable
    reason: 本地功能验证属于当前范围。
    basis: 当前需求要求验证本地流程。
    required_by_source: true
    required_now: true
    completed_validation: [EVD-LOCAL-FUNCTIONAL-01]
    substitute_validation: []
    manual_follow_up: N/A
    pass_standard: 本地功能测试全部通过。""")
        errors: list[str] = []
        report = validator.check_plain_language_contract(text, errors)
        self.assertEqual(errors, [])
        self.assertEqual(report["release_status"], "allowed")

    def test_plain_language_opening_rejects_machine_details(self) -> None:
        """机器字段只能出现在技术章节，不能泄漏到 H1 后开场。"""
        text = self._layered_document("  []", opening="REQ-1 已完成，详见 F:/work/test.py:12。")
        errors: list[str] = []
        validator.check_plain_language_contract(text, errors)
        self.assertTrue(any("stable IDs" in error for error in errors))
        self.assertTrue(any("paths or line numbers" in error for error in errors))

    def test_plain_language_opening_requires_h1_and_content(self) -> None:
        """白话契约必须有 H1，且 H1 后第一段不能为空。"""
        missing_h1 = self._layered_document("  []").replace("# 文档说明", "## 文档说明", 1)
        errors: list[str] = []
        validator.check_plain_language_contract(missing_h1, errors)
        self.assertTrue(any("must contain an H1" in error for error in errors))

        empty_opening = self._layered_document("  []", opening="")
        errors = []
        validator.check_plain_language_contract(empty_opening, errors)
        self.assertTrue(any("must not be empty" in error for error in errors))

    def test_plain_language_document_allows_zero_or_one_terminal_appendix(self) -> None:
        """没有附录或只有末尾附录都符合新策略。"""
        text = self._layered_document("  []", technical="技术章节包含 REQ-1 和 `python test.py`。\n\n## 附录\n补充说明。")
        errors: list[str] = []
        validator.check_plain_language_contract(text, errors)
        self.assertEqual(errors, [])

    def test_plain_language_document_rejects_multiple_or_non_terminal_appendix(self) -> None:
        """重复附录或附录后又出现同级章节时阻断。"""
        text = self._layered_document("  []", technical="## 附录\n第一个附录。\n\n## 其他章节\n不应出现在附录后。\n\n## 附录：第二个\n重复。")
        errors: list[str] = []
        validator.check_plain_language_contract(text, errors)
        self.assertTrue(any("at most one" in error for error in errors))

    def test_plain_language_document_rejects_non_terminal_appendix_alone(self) -> None:
        """唯一附录后仍有同级章节时必须单独阻断。"""
        text = self._layered_document("  []", technical="## 附录\n补充说明。\n\n## 后续章节\n不应出现在附录后。")
        errors: list[str] = []
        validator.check_plain_language_contract(text, errors)
        self.assertIn("plain-language appendix must be terminal", errors)

    def test_review_acceptance_gate_missing_fields_is_rejected(self) -> None:
        """门禁记录缺少固定字段时不能被当作空门禁放行。"""
        text = self._layered_document("  - stage: review\n    applicability: applicable")
        errors: list[str] = []
        report = validator.check_plain_language_contract(text, errors)
        self.assertFalse(report["valid"])
        self.assertTrue(any("gate.schema_invalid" in error for error in errors))

    def test_headings_ignore_code_fence_titles(self) -> None:
        """代码块中的伪标题不应参与章节解析。"""
        text = "# 正式标题\n开场说明。\n\n```markdown\n## 代码示例标题\n```\n\n## 正式章节\n"
        self.assertEqual(validator.headings(text), ["正式标题", "正式章节"])

    def test_tilde_fence_titles_do_not_change_heading_baseline(self) -> None:
        """波浪线代码围栏中的伪标题也不参与标题解析。"""
        text = "# 正式标题\n开场说明。\n\n~~~markdown\n## 代码示例标题\n~~~\n\n## 正式章节\n"
        self.assertEqual(validator.headings(text), ["正式标题", "正式章节"])

    def test_generic_document_profiles_accept_layered_document(self) -> None:
        """所有新增文档类型 profile 都接受同一份分层文档。"""
        text = self._layered_document("  []", technical="图片资产决策：N/A + 原因 + 证据：本次不需要视觉材料。")
        profile_names = ("bug", "test", "review", "final_acceptance", "architecture", "delivery", "project_design", "work_report")
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            document = root / "layered.md"
            document.write_text(text, encoding="utf-8")
            for profile_name in profile_names:
                with self.subTest(profile=profile_name):
                    profile = self.payload["profiles"][profile_name]
                    result = validator.validate_document(document, profile_name, profile, self.payload, root)
                    self.assertTrue(result["valid"], result["errors"])


if __name__ == "__main__":
    unittest.main()
