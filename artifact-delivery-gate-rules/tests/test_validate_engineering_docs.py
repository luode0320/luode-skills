#!/usr/bin/env python3
"""验证工程文档质量校验器的正例、负例和 N/A 处理。"""

from __future__ import annotations

import re
import tempfile
import unittest
from pathlib import Path
import sys


SCRIPT_DIR = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPT_DIR))

import validate_engineering_docs as validator  # noqa: E402


ROOT = Path(__file__).resolve().parents[2]
PROFILE_FILE = ROOT / "artifact-delivery-gate-rules" / "references" / "document-quality-profiles.yaml"
TEMPLATE_REGISTRY_FILE = ROOT / "artifact-delivery-gate-rules" / "references" / "plain-language-template-registry.yaml"
LAYERED_OPENING = (
    "结论：本次结果已经明确；影响：业务读者可据此了解变化；范围：本文件说明当前事项；"
    "非范围：不处理未列出的工作；变化：正文和附录按职责分层；完成标准：读者能判断是否完成；"
    "术语说明：无；验证状态：本地规则核对完成。"
)


class EngineeringDocumentValidatorTests(unittest.TestCase):
    def setUp(self) -> None:
        self.payload = validator.load_profiles(PROFILE_FILE)
        self.template_registry = validator.yaml.safe_load(TEMPLATE_REGISTRY_FILE.read_text(encoding="utf-8"))

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

    # test_na_reason_check_skips_fenced_mermaid 验证 Mermaid 的非阻断分支不会触发正文 N/A 校验。
    # [参数] 无：构造仅含围栏内“不适用”的最小图示。
    # [返回] None：断言不产生 N/A 原因或证据缺失错误。
    # 最近修改时间：2026-07-14 修复 Mermaid 分支被通用 N/A 校验误判的问题。
    def test_na_reason_check_skips_fenced_mermaid(self) -> None:
        """验证围栏内的不适用文本不作为正文 N/A 声明。"""
        # 1. 对 Mermaid 围栏执行 N/A 原因与证据校验。
        errors: list[str] = []
        validator.check_na_reasons("```mermaid\nA --> B[不适用]\n```", errors)

        # 2. 围栏内容应被跳过，不能产生正文缺失错误。
        self.assertEqual(errors, [])

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

    # _layered_document 构造符合白话契约的最小通用文档夹具。
    # [参数] gate_yaml: review_acceptance_gates YAML 片段；opening: H1 后固定摘要；technical: 技术章节正文。
    # [返回] str：可传入白话契约校验器的最小 Markdown 文本。
    # 最近修改时间：2026-07-14 00:00:00 + 使用八项固定摘要和双附录策略夹具。
    def _layered_document(
        self,
        gate_yaml: str,
        opening: str = LAYERED_OPENING,
        technical: str = "技术细节放在原有章节。",
        status: str = "draft",
        doc_type: str = "test",
    ) -> str:
        # 1. 保持 YAML 元数据完整，让测试只聚焦白话摘要和附录边界。
        return f"""---
schema_version: 1
doc_id: DOC-1
doc_type: {doc_type}
source_ids: [SRC-1]
status: {status}
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

    def _task_blocker_closure(self) -> str:
        """构造满足统一 BLK-* 契约的真实阻断收口章节。"""
        return """## 任务阻断收口

- 阻断记录 ID: BLK-DOC-001
- 任务状态: blocked
- 阻断阶段: 最终验收
- 阻断依据与证据: blocker.required_validation_missing；EVD-DOC-001。
- 已尝试与停止边界: 已执行本地验证；缺少必要验收条件后停止。
- 影响: 不得宣布任务完成或正式放行。
- 解决计划: 1. 责任方: 验收 owner；前置条件: 本地环境可用；动作: 补齐验收验证；完成判据: 验收通过；验证入口: python tests。
- 恢复后重入点: 重新执行最终验收。
- 去重键: blocker.required_validation_missing + EVD-DOC-001
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
        self.assertFalse(result["task_blocker_closure"]["required"])

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

    def test_blocked_status_requires_task_blocker_closure(self) -> None:
        """状态已标记阻断时，缺少恢复交接章节必须被拒绝。"""
        text = self._layered_document("  []", status="blocked")
        with tempfile.TemporaryDirectory() as directory:
            document = Path(directory) / "blocked.md"
            document.write_text(text, encoding="utf-8")
            result = validator.validate_document(document, "test", self.payload["profiles"]["test"], self.payload, Path(directory))
        self.assertFalse(result["valid"])
        self.assertIn("blocker.closure_missing", result["error_codes"])

    def test_review_blocked_conclusion_requires_task_blocker_closure(self) -> None:
        """审查结论明确阻断时，即使状态未改也必须完成收口。"""
        text = self._layered_document("  []", technical="- 审查结论：阻断。")
        with tempfile.TemporaryDirectory() as directory:
            document = Path(directory) / "review.md"
            document.write_text(text, encoding="utf-8")
            result = validator.validate_document(document, "review", self.payload["profiles"]["review"], self.payload, Path(directory))
        self.assertFalse(result["valid"])
        self.assertEqual(result["task_blocker_closure"]["triggers"], ["review_conclusion_blocked"])

    def test_final_acceptance_non_release_requires_task_blocker_closure(self) -> None:
        """最终验收不通过或待重验都必须带统一阻断收口。"""
        for conclusion in ("不通过", "待重验"):
            with self.subTest(conclusion=conclusion), tempfile.TemporaryDirectory() as directory:
                document = Path(directory) / "acceptance.md"
                document.write_text(
                    self._layered_document("  []", technical=f"- 最终验收结论：{conclusion}。"),
                    encoding="utf-8",
                )
                result = validator.validate_document(
                    document,
                    "final_acceptance",
                    self.payload["profiles"]["final_acceptance"],
                    self.payload,
                    Path(directory),
                )
            self.assertFalse(result["valid"])
            self.assertIn("final_acceptance_not_released", result["task_blocker_closure"]["triggers"])

    def test_task_blocker_closure_accepts_complete_recovery_plan(self) -> None:
        """完整 BLK 记录可使真实阻断文档保留可验证交接。"""
        text = self._layered_document("  []", status="blocked", technical=self._task_blocker_closure())
        with tempfile.TemporaryDirectory() as directory:
            document = Path(directory) / "blocked.md"
            document.write_text(text, encoding="utf-8")
            result = validator.validate_document(document, "test", self.payload["profiles"]["test"], self.payload, Path(directory))
        self.assertTrue(result["valid"], result["errors"])
        self.assertEqual(result["task_blocker_closure"]["records"], ["BLK-DOC-001"])

    def test_limited_not_applicable_and_normal_documents_do_not_require_task_blocker_closure(self) -> None:
        """受限、不适用和正常通过不应被误报为任务阻断。"""
        for gate_yaml in (
            "  []",
            """  - stage: third_party
    applicability: not_applicable
    reason: 本次范围不调用第三方接口。
    basis: 需求范围只包含本地流程。
    required_by_source: false
    required_now: false
    completed_validation: []
    substitute_validation: []
    manual_follow_up: N/A
    pass_standard: N/A""",
        ):
            with self.subTest(gate_yaml=gate_yaml), tempfile.TemporaryDirectory() as directory:
                document = Path(directory) / "normal.md"
                document.write_text(self._layered_document(gate_yaml), encoding="utf-8")
                result = validator.validate_document(document, "test", self.payload["profiles"]["test"], self.payload, Path(directory))
            self.assertTrue(result["valid"], result["errors"])
            self.assertFalse(result["task_blocker_closure"]["required"])

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
        text = self._layered_document("  []", opening=f"{LAYERED_OPENING} REQ-1 已完成，详见 F:/work/test.py:12。")
        errors: list[str] = []
        validator.check_plain_language_contract(text, errors)
        self.assertTrue(any("stable IDs" in error for error in errors))
        self.assertTrue(any("paths or line numbers" in error for error in errors))

    def test_plain_language_opening_requires_all_fixed_summary_labels(self) -> None:
        """固定摘要缺少任一标签时必须被机器识别。"""
        text = self._layered_document("  []", opening=LAYERED_OPENING.replace("范围：本文件说明当前事项；", "涉及内容：本文件说明当前事项；"))
        errors: list[str] = []
        validator.check_plain_language_contract(text, errors)
        self.assertIn("plain-language opening must contain summary field: 范围", errors)

    def test_plain_language_opening_allows_chinese_periods_and_no_terminology_declaration(self) -> None:
        """固定摘要允许中文句号分隔，并接受契约规定的无术语声明。"""
        opening = LAYERED_OPENING.replace("；", "。").replace("术语说明：无", "术语说明：无技术术语需要解释")
        text = self._layered_document("  []", opening=opening)
        errors: list[str] = []
        validator.check_plain_language_contract(text, errors)
        self.assertEqual(errors, [])

    # test_strict_trace_scopes_documents_by_target_source 验证严格追踪只读取目标来源对象文档。
    # [参数] 无：在临时目录创建一组完整目标文档和一组缺证据的无关文档。
    # [返回] None：断言无关来源对象不会污染目标严格追踪结果。
    # 最近修改时间：2026-07-23；改动原因：覆盖按目标 source_ids 选域并防止旧来源硬编码回归。
    def test_strict_trace_scopes_documents_by_target_source(self) -> None:
        """验证严格追踪只读取与目标文档共享根来源 ID 的文档。"""
        # 1. 构造目标完整周期和无关缺证据周期，确保两者 source_ids 不相交。
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            target = root / "目标_实施周期01.md"
            target.write_text(
                "---\ndoc_id: CYCLEDOC-A\nsource_ids: [SRC-A]\n---\n"
                "REQ-A AC-A CYCLE-A T01-01 TEST-A EVIDENCE-A\n"
                "T01-01 真实测试 停止 EVD-T01-01-IMPL-01 EVD-T01-01-TEST-01 "
                "EVD-T01-01-REVIEW-01 EVD-T01-01-ACCEPT-01",
                encoding="utf-8",
            )
            (root / "无关_实施周期02.md").write_text(
                "---\ndoc_id: CYCLEDOC-B\nsource_ids: [SRC-B]\n---\n"
                "REQ-B AC-B CYCLE-B T02-01 TEST-B EVIDENCE-B\n"
                "T02-01 真实测试 停止 EVD-T02-01-IMPL-01",
                encoding="utf-8",
            )
            errors: list[str] = []
            trace = validator.check_strict_trace(root, errors, target)

        # 2. 目标来源必须独立通过，报告不得包含无关任务。
        self.assertEqual(errors, [])
        self.assertEqual(trace["documents"], 1)
        self.assertEqual(trace["tasks"], ["T01-01"])

    def test_plain_language_opening_rejects_unexplained_terminology(self) -> None:
        """术语说明不能只列技术词，必须声明无术语或给出中文解释。"""
        text = self._layered_document("  []", opening=LAYERED_OPENING.replace("术语说明：无", "术语说明：本次使用 API"))
        errors: list[str] = []
        validator.check_plain_language_contract(text, errors)
        self.assertIn("plain-language opening terminology must be 无 or a readable Chinese explanation", errors)

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

    def test_plain_language_document_allows_generic_or_named_terminal_appendix(self) -> None:
        """旧通用附录和新命名双附录组都可作为末尾技术承载区。"""
        text = self._layered_document("  []", technical="技术章节包含 REQ-1 和 `python test.py`。\n\n## 执行附录\n命令与样本。\n\n## 追踪附录\n稳定 ID 与证据。")
        errors: list[str] = []
        validator.check_plain_language_contract(text, errors)
        self.assertEqual(errors, [])

    def test_plain_language_document_allows_numbered_named_terminal_appendix_group(self) -> None:
        """带数字前缀的命名附录也属于有效的末尾附录组。"""
        text = self._layered_document("  []", technical="## 5. 执行附录\n命令与样本。\n\n## 6. 追踪附录\n稳定 ID 与证据。")
        errors: list[str] = []
        validator.check_plain_language_contract(text, errors)
        self.assertEqual(errors, [])

    def test_plain_language_document_rejects_reversed_numbered_named_appendix_group(self) -> None:
        """编号存在时，命名附录仍必须先执行后追踪。"""
        text = self._layered_document("  []", technical="## 5. 追踪附录\n稳定 ID 与证据。\n\n## 6. 执行附录\n命令与样本。")
        errors: list[str] = []
        validator.check_plain_language_contract(text, errors)
        self.assertIn("plain-language appendix group must order 执行附录 before 追踪附录 at the same heading level", errors)

    def test_plain_language_document_rejects_multiple_or_non_terminal_appendix(self) -> None:
        """重复附录或附录后又出现同级章节时阻断。"""
        text = self._layered_document("  []", technical="## 附录\n第一个附录。\n\n## 其他章节\n不应出现在附录后。\n\n## 附录：第二个\n重复。")
        errors: list[str] = []
        validator.check_plain_language_contract(text, errors)
        self.assertTrue(any("at most one" in error for error in errors))

    def test_plain_language_document_rejects_non_terminal_appendix_alone(self) -> None:
        """唯一附录后仍有同级章节时必须单独阻断。"""
        text = self._layered_document("  []", technical="## 执行附录\n补充说明。\n\n## 后续章节\n不应出现在附录后。")
        errors: list[str] = []
        validator.check_plain_language_contract(text, errors)
        self.assertIn("plain-language appendix group must be terminal", errors)

    def test_plain_language_document_rejects_non_contiguous_named_appendix_group(self) -> None:
        """执行附录和追踪附录之间夹入业务章节时必须阻断。"""
        text = self._layered_document(
            "  []",
            technical="## 执行附录\n命令与样本。\n\n## 补充业务说明\n不属于附录组。\n\n## 追踪附录\n稳定 ID 与证据。",
        )
        errors: list[str] = []
        validator.check_plain_language_contract(text, errors)
        self.assertIn("plain-language appendix group must be contiguous", errors)

    def test_plain_language_document_allows_named_group_under_generic_parent_appendix(self) -> None:
        """通用父附录下的执行与追踪子附录属于兼容的单个末尾附录组。"""
        text = self._layered_document(
            "  []",
            technical="## 附录\n\n### 执行附录\n命令与样本。\n\n### 追踪附录\n稳定 ID 与证据。",
        )
        errors: list[str] = []
        validator.check_plain_language_contract(text, errors)
        self.assertEqual(errors, [])

    def test_plain_language_document_rejects_parallel_generic_and_named_appendices(self) -> None:
        """并列通用附录和命名附录不是兼容父子结构，必须阻断。"""
        text = self._layered_document("  []", technical="## 附录\n旧说明。\n\n## 执行附录\n命令与样本。")
        errors: list[str] = []
        validator.check_plain_language_contract(text, errors)
        self.assertIn("plain-language document must not mix generic and named appendix groups", errors)

    # test_template_registry_covers_all_managed_templates 验证 registry 声明与每个模板的三层结构同步。
    # [参数] 无：读取仓库内模板注册表与实际模板文件。
    # [返回] None：逐项断言模板存在、固定摘要完整且末尾双附录组实际存在并有效。
    # 最近修改时间：2026-07-14 00:00:00 + 强制 registry 中每个模板落实双附录而非仅允许其缺失。
    def test_template_registry_covers_all_managed_templates(self) -> None:
        """所有受管模板都必须声明并落实白话摘要和双附录结构。"""
        # 1. 注册表是受管模板的唯一枚举来源，数量、层次和路径必须一致。
        templates = self.template_registry["templates"]
        self.assertEqual(self.template_registry["template_count"], len(templates))
        self.assertEqual(
            self.template_registry["summary_opening"]["required_labels"],
            list(validator.PLAIN_LANGUAGE_SUMMARY_LABELS),
        )
        self.assertEqual(
            self.template_registry["terminal_appendix_group"]["required_order"],
            list(validator.PLAIN_LANGUAGE_NAMED_APPENDICES),
        )

        # 2. 每个注册模板必须实际存在，并具备 H1 固定摘要、执行附录和追踪附录。
        for entry in templates:
            with self.subTest(template_id=entry["template_id"]):
                template_path = ROOT / entry["path"]
                self.assertTrue(template_path.is_file(), entry["path"])
                self.assertEqual(entry["layers"], ["h1_summary", "execution_appendix", "tracking_appendix"])
                template_text = template_path.read_text(encoding="utf-8")
                opening = validator.h1_opening(template_text)
                for label in validator.PLAIN_LANGUAGE_SUMMARY_LABELS:
                    self.assertRegex(opening, rf"{label}\s*[：:]")
                appendix_records = validator.markdown_heading_records(template_text, normalize_numbering=False)
                appendix_matches = {
                    name: [
                        record
                        for record in appendix_records
                        if re.match(
                            rf"{validator.APPENDIX_NUMBER_PREFIX_PATTERN}{name}{validator.APPENDIX_HEADING_SUFFIX_PATTERN}",
                            record[1],
                        )
                    ]
                    for name in validator.PLAIN_LANGUAGE_NAMED_APPENDICES
                }
                self.assertEqual(len(appendix_matches["执行附录"]), 1, entry["path"])
                self.assertEqual(len(appendix_matches["追踪附录"]), 1, entry["path"])
                self.assertLess(
                    appendix_matches["执行附录"][0][2],
                    appendix_matches["追踪附录"][0][2],
                    entry["path"],
                )
                errors: list[str] = []
                validator.check_appendix_policy(template_text, errors)
                self.assertEqual(errors, [], entry["path"])

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
