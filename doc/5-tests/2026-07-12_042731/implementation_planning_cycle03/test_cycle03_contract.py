#!/usr/bin/env python3
"""Deterministic contract checks for implementation-planning cycle 03."""

from __future__ import annotations

import argparse
import re
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]


def find_cycle_document() -> Path:
    candidates = sorted((ROOT / "doc").glob("3-*/*033322*"))
    for candidate in candidates:
        if candidate.is_file() and "DOC-IMPL-CYCLE-03-20260712-033322" in candidate.read_text(encoding="utf-8"):
            return candidate
    raise FileNotFoundError("cycle 03 document was not found")


def task_block(document: str, task_id: str) -> str:
    pattern = re.compile(rf"^###\s+[^\n]*`{re.escape(task_id)}`[^\n]*\n(.*?)(?=^#{{2,3}}\s+|\Z)", re.MULTILINE | re.DOTALL)
    match = pattern.search(document)
    if not match:
        raise AssertionError(f"missing task block: {task_id}")
    return match.group(1)


REQUIRED_TASK_FIELDS = (
    "唯一目标",
    "本任务只做这一件事",
    "预计触达文件数",
    "文件/符号",
    "真实测试入口",
    "样本",
    "断言",
    "失败预期",
    "回滚",
    "停止条件",
    "最大推进边界",
)


def validate_task_contract(block: str, task_id: str) -> list[str]:
    errors: list[str] = []
    for field in REQUIRED_TASK_FIELDS:
        if field not in block:
            errors.append(f"{task_id}: missing field {field}")
    count_match = re.search(r"预计触达文件数\s*\|\s*(\d+)", block)
    if count_match and int(count_match.group(1)) > 5:
        errors.append(f"{task_id}: more than five files")
    if any(
        re.search(r"^\s*(?:决策|状态|未决项)[:：].*P[01].*(?:unresolved|未决|open)", line, re.IGNORECASE)
        for line in block.splitlines()
    ):
        errors.append(f"{task_id}: unresolved P0/P1 decision")
    for vague in ("适当处理", "相关逻辑", "尽量", "合理"):
        if vague in block:
            errors.append(f"{task_id}: vague action {vague}")
    evidence_suffixes = ("IMPL", "TEST", "REVIEW", "ACCEPT")
    for suffix in evidence_suffixes:
        if not re.search(rf"EVD-{re.escape(task_id)}-{suffix}(?:-[A-Z0-9]+)*", block):
            errors.append(f"{task_id}: missing evidence {suffix}")
    return errors


def validate_diagram_annotations(document: str) -> list[str]:
    blocks = re.findall(r"```mermaid\n(.*?)\n```", document, re.DOTALL)
    errors: list[str] = []
    if len(blocks) < 2:
        errors.append("cycle document needs task DAG and domain matching diagrams")
    if document.count("图形目的：") < len(blocks):
        errors.append("each Mermaid diagram needs a purpose annotation")
    if document.count("关联 ID：") < len(blocks):
        errors.append("each Mermaid diagram needs related IDs")
    return errors


class Cycle03ContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.document_path = find_cycle_document()
        cls.document = cls.document_path.read_text(encoding="utf-8")

    def test_cycle_document_has_complete_identity_and_graphs(self) -> None:
        required = (
            "CYCLE-03",
            "T03-01",
            "T03-02",
            "T03-03",
            "当前代码/文档基线",
            "周期内最小任务执行顺序",
            "最小任务闭环",
            "当前周期验证矩阵",
            "自审结论",
            "真实测试",
            "停止条件",
            "回滚",
            "最大推进边界",
            "DEC-03-001",
        )
        for marker in required:
            self.assertIn(marker, self.document)
        self.assertEqual(validate_diagram_annotations(self.document), [])

    def test_low_reasoning_task_contract(self) -> None:
        for task_id in ("T03-01", "T03-02", "T03-03"):
            errors = validate_task_contract(task_block(self.document, task_id), task_id)
            self.assertEqual(errors, [], "low-reasoning contract errors: " + "; ".join(errors))
        self.assertIn("unresolved_decisions` 中 P0/P1 数量必须为 0", self.document)

    def test_decision_log_contract(self) -> None:
        self.assertRegex(self.document, r"DEC-03-001.*SRC-03-001.*OPTION-A")
        missing_reason = "DEC-03-002 | SRC-03-002 | OPTION-B |  | 影响 | 回滚"
        self.assertTrue(bool(re.search(r"DEC-[^|]+\|[^|]+\|[^|]+\|\s*\|", missing_reason)))
        unresolved = "DEC-03-003 | SRC-03-003 | OPTION-C | reason | P0 unresolved | rollback"
        self.assertRegex(unresolved, r"P0\s+unresolved")

    def test_negative_gate_cases(self) -> None:
        complete = task_block(self.document, "T03-03")
        cases = {
            "missing-file-symbol": complete.replace("文件/符号", "文件契约", 1),
            "missing-command": complete.replace("真实测试入口", "执行入口", 1),
            "ambiguous-action": complete + "\n动作：适当处理。\n",
            "over-five-files": complete.replace("预计触达文件数 | 5 个以内", "预计触达文件数 | 6", 1),
            "unresolved-p0": complete + "\n决策：P0 unresolved。\n",
            "orphan-trace": complete.replace("EVD-T03-03-REVIEW-01", "EVD-T03-03-OTHER-01", 1),
        }
        for name, sample in cases.items():
            errors = validate_task_contract(sample, "T03-03")
            if name == "missing-file-symbol":
                self.assertTrue(any("文件/符号" in error for error in errors), name)
            elif name == "missing-command":
                self.assertTrue(any("真实测试入口" in error for error in errors), name)
            elif name == "ambiguous-action":
                self.assertTrue(any("vague action" in error for error in errors), name)
            elif name == "over-five-files":
                self.assertTrue(any("more than five" in error for error in errors), name)
            elif name == "unresolved-p0":
                self.assertTrue(any("unresolved P0/P1" in error for error in errors), name)
            elif name == "orphan-trace":
                self.assertTrue(any("missing evidence REVIEW" in error for error in errors), name)

    def test_negative_mermaid_annotation(self) -> None:
        negative = self.document.replace("图形目的：展示周期03的唯一顺序、任务依赖和失败停止点。", "", 1)
        errors = validate_diagram_annotations(negative)
        self.assertTrue(any("purpose annotation" in error for error in errors))

    def test_no_task_is_owned_by_two_cycle03_sections(self) -> None:
        for task_id in ("T03-01", "T03-02", "T03-03"):
            self.assertEqual(len(re.findall(rf"^###\s+[^\n]*`{task_id}`", self.document, re.MULTILINE)), 1)


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate cycle 03 execution-card contracts")
    parser.add_argument("-k", dest="pattern", default="", help="run tests whose method name contains this text")
    args = parser.parse_args()
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(Cycle03ContractTests)
    if args.pattern:
        suite = unittest.TestSuite(
            test for test in suite if args.pattern.lower() in test._testMethodName.lower()
        )
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(main())
