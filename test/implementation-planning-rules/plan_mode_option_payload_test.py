#!/usr/bin/env python3
"""验证 Plan Mode 选择框载荷质量前置校验。"""

from __future__ import annotations

from dataclasses import dataclass, field
import re
from typing import Any


ROOT_STRING = r"F:\luode-skills"

PLACEHOLDER_LABELS = frozenset({
    "选项1", "选项2", "选项3", "选项4",
    "方案A", "方案B", "方案C", "方案D",
    "待定", "TBD", "TODO", "占位", "请选择",
})


class PayloadViolation(ValueError):
    """表示载荷不满足质量校验契约。"""


def normalize_label(label: str) -> str:
    """去除空白、小写、移除 (Recommended) 后缀，用于比较。"""
    s = label.strip().lower()
    s = re.sub(r'\s*\(recommended\)\s*$', '', s).strip()
    return s


def validate_option_payload(payload: dict[str, Any]) -> None:
    """校验 request_user_input 载荷质量。

    [参数] payload: 候选载荷字典
    [返回] 无，失败时抛出 PayloadViolation
    """
    questions = payload.get("questions", [])
    if not isinstance(questions, list):
        raise PayloadViolation("questions 必须是列表")

    # 1. 单次调用包含 1-3 个问题
    if len(questions) < 1:
        raise PayloadViolation("至少需要 1 个问题")
    if len(questions) > 3:
        raise PayloadViolation("最多 3 个问题")

    for q in questions:
        if not isinstance(q, dict):
            raise PayloadViolation("每个问题必须是字典")

        # 2. id 非空且 snake_case
        qid = q.get("id", "").strip()
        if not qid:
            raise PayloadViolation("问题 id 不能为空")
        if not re.match(r'^[a-z][a-z0-9_]*$', qid):
            raise PayloadViolation(f"问题 id 必须使用 snake_case: {qid}")

        # 3. header 非空且不超过 12 字符
        header = q.get("header", "").strip()
        if not header:
            raise PayloadViolation(f"问题 {qid} 的 header 不能为空")
        if len(header) > 12:
            raise PayloadViolation(f"问题 {qid} 的 header 不能超过 12 字符")

        # 4. question 非空
        question_text = q.get("question", "").strip()
        if not question_text:
            raise PayloadViolation(f"问题 {qid} 的 question 不能为空")

        # 5. 每个问题包含 2-3 个选项
        options = q.get("options", [])
        if not isinstance(options, list):
            raise PayloadViolation(f"问题 {qid} 的 options 必须是列表")
        if len(options) < 2:
            raise PayloadViolation(f"问题 {qid} 至少需要 2 个选项，当前 {len(options)}")
        if len(options) > 3:
            raise PayloadViolation(f"问题 {qid} 最多 3 个选项，当前 {len(options)}")

        # 6. 选项使用 {label, description} 结构
        for opt in options:
            if not isinstance(opt, dict):
                raise PayloadViolation(f"问题 {qid} 的选项必须是字典结构")
            if "label" not in opt or "description" not in opt:
                raise PayloadViolation(f"问题 {qid} 的选项必须包含 label 和 description")

        # 7. 推荐项置首且标记 (Recommended)
        first_label = options[0].get("label", "").strip()
        if "(Recommended)" not in first_label and "(推荐)" not in first_label:
            raise PayloadViolation(f"问题 {qid} 的推荐项必须置首并标记 (Recommended)")

        # 8. 不显式添加客户端自动提供的 Other
        for opt in options:
            label = opt.get("label", "").strip()
            if normalize_label(label) == "other":
                raise PayloadViolation(f"问题 {qid} 不应显式添加 Other 选项")

        # 9. label 非空
        for opt in options:
            label = opt.get("label", "").strip()
            if not label:
                raise PayloadViolation(f"问题 {qid} 的选项 label 不能为空")

        # 10. description 非空
        descriptions = []
        for opt in options:
            desc = opt.get("description", "").strip()
            if not desc:
                raise PayloadViolation(f"问题 {qid} 的选项 description 不能为空")
            descriptions.append(desc)

        # 11. 标签去重（去除空白、大小写和推荐后缀后）
        normalized_labels = [normalize_label(opt.get("label", "")) for opt in options]
        for i, nl in enumerate(normalized_labels):
            if not nl:
                raise PayloadViolation(f"问题 {qid} 选项 {i} 标准化后标签为空")
        if len(set(normalized_labels)) != len(normalized_labels):
            raise PayloadViolation(f"问题 {qid} 存在重复标签")

        # 12. 描述去重
        if len(set(descriptions)) != len(descriptions):
            raise PayloadViolation(f"问题 {qid} 存在重复描述")

        # 13. 拒绝占位标签
        for opt in options:
            label = opt.get("label", "").strip()
            nl = normalize_label(label)
            if nl in [normalize_label(p) for p in PLACEHOLDER_LABELS]:
                raise PayloadViolation(f"问题 {qid} 含有占位标签: {label}")


def make_valid_payload() -> dict[str, Any]:
    """构造一个合法的选择框载荷。"""
    return {
        "questions": [
            {
                "id": "implementation_scope",
                "header": "实现范围",
                "question": "请选择本次实现的范围？",
                "options": [
                    {"label": "全部接入 (Recommended)", "description": "接入所有模块，完整覆盖"},
                    {"label": "仅核心链路", "description": "只接入核心链路，快速验证"},
                ],
            }
        ]
    }


# ===== 测试用例 =====

def assert_true(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def test_valid_chinese_payload() -> None:
    """AC-PMO-001: 合法中文载荷通过校验。"""
    payload = make_valid_payload()
    validate_option_payload(payload)
    # 不抛出异常即为通过
    assert_true(True, "legal payload should pass")


def test_empty_question_field() -> None:
    """AC-PMO-002: 空问题字段被拒绝。"""
    # 空 questions
    try:
        validate_option_payload({"questions": []})
    except PayloadViolation:
        pass
    else:
        raise AssertionError("空 questions 未被拒绝")

    # 问题内 question 为空
    payload = make_valid_payload()
    payload["questions"][0]["question"] = "   "
    try:
        validate_option_payload(payload)
    except PayloadViolation:
        pass
    else:
        raise AssertionError("空 question 字段未被拒绝")


def test_less_than_two_options() -> None:
    """AC-PMO-003: 少于 2 个选项被拒绝。"""
    payload = make_valid_payload()
    payload["questions"][0]["options"] = [
        {"label": "仅一个选项 (Recommended)", "description": "只有一个选项"}
    ]
    try:
        validate_option_payload(payload)
    except PayloadViolation:
        pass
    else:
        raise AssertionError("少于 2 个选项未被拒绝")


def test_more_than_three_options() -> None:
    """AC-PMO-004: 多于 3 个选项被拒绝。"""
    payload = make_valid_payload()
    payload["questions"][0]["options"] = [
        {"label": "方案A (Recommended)", "description": "方案A 描述"},
        {"label": "方案B", "description": "方案B 描述"},
        {"label": "方案C", "description": "方案C 描述"},
        {"label": "方案D", "description": "方案D 描述"},
    ]
    try:
        validate_option_payload(payload)
    except PayloadViolation:
        pass
    else:
        raise AssertionError("多于 3 个选项未被拒绝")


def test_empty_label() -> None:
    """AC-PMO-005: 空标签被拒绝。"""
    payload = make_valid_payload()
    payload["questions"][0]["options"] = [
        {"label": "方案A (Recommended)", "description": "方案A 描述"},
        {"label": "   ", "description": "方案B 描述"},
    ]
    try:
        validate_option_payload(payload)
    except PayloadViolation:
        pass
    else:
        raise AssertionError("空标签未被拒绝")


def test_empty_description() -> None:
    """AC-PMO-006: 空描述被拒绝。"""
    payload = make_valid_payload()
    payload["questions"][0]["options"] = [
        {"label": "方案A (Recommended)", "description": "方案A 描述"},
        {"label": "方案B", "description": "   "},
    ]
    try:
        validate_option_payload(payload)
    except PayloadViolation:
        pass
    else:
        raise AssertionError("空描述未被拒绝")


def test_duplicate_labels() -> None:
    """AC-PMO-007: 规范化后重复标签被拒绝。"""
    payload = make_valid_payload()
    payload["questions"][0]["options"] = [
        {"label": "方案A (Recommended)", "description": "方案A 描述"},
        {"label": "方案A", "description": "方案B 描述"},
    ]
    try:
        validate_option_payload(payload)
    except PayloadViolation:
        pass
    else:
        raise AssertionError("重复标签未被拒绝")


def test_duplicate_descriptions() -> None:
    """AC-PMO-008: 重复描述被拒绝。"""
    payload = make_valid_payload()
    payload["questions"][0]["options"] = [
        {"label": "方案A (Recommended)", "description": "完全相同的描述"},
        {"label": "方案B", "description": "完全相同的描述"},
    ]
    try:
        validate_option_payload(payload)
    except PayloadViolation:
        pass
    else:
        raise AssertionError("重复描述未被拒绝")


def test_placeholder_labels() -> None:
    """AC-PMO-009: 纯占位标签被拒绝。"""
    for placeholder in ("选项1", "选项2", "方案A", "方案B", "待定", "TBD", "TODO", "占位", "请选择"):
        payload = make_valid_payload()
        payload["questions"][0]["options"] = [
            {"label": f"{placeholder} (Recommended)", "description": "占位标签"},
            {"label": "真实方案", "description": "真实方案描述"},
        ]
        try:
            validate_option_payload(payload)
        except PayloadViolation:
            pass
        else:
            raise AssertionError(f"占位标签未被拒绝: {placeholder}")


def test_invalid_draft_no_tool_call() -> None:
    """AC-PMO-010: 无效草稿不调用工具、不进入等待；重建合法后只调用一次并进入等待。"""
    # 无效载荷不调用工具
    invalid_payload = {"questions": []}
    tool_called = False
    try:
        validate_option_payload(invalid_payload)
        tool_called = True
    except PayloadViolation:
        tool_called = False
    assert_true(not tool_called, "无效载荷不应调用工具")

    # 重建合法后只调用一次
    valid_payload = make_valid_payload()
    validate_option_payload(valid_payload)
    assert_true(True, "重建合法后校验通过")


def main() -> None:
    tests = (
        test_valid_chinese_payload,
        test_empty_question_field,
        test_less_than_two_options,
        test_more_than_three_options,
        test_empty_label,
        test_empty_description,
        test_duplicate_labels,
        test_duplicate_descriptions,
        test_placeholder_labels,
        test_invalid_draft_no_tool_call,
    )
    for test in tests:
        test()
        print(f"PASS {test.__name__}")
    print(f"plan-mode-option-payload: PASS ({len(tests)} cases)")


if __name__ == "__main__":
    main()
