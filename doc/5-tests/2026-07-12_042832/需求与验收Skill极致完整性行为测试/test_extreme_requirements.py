"""周期 02 需求/验收 Skill 极致完整性契约行为测试。"""

from __future__ import annotations

import argparse
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[4]

CASES = {
    "T02-01": {
        "label": "需求入口字段与零决策闸门",
        "files": [
            "requirement-intake-rules/references/requirement-structure-template.md",
            "requirement-intake-rules/agents/openai.yaml",
        ],
        "tokens": [
            "SRC-*",
            "DEC-*",
            "REQ-*",
            "RULE-*",
            "AC-*",
            "unresolved_decisions",
            "N/A + 原因 + 证据",
            "flowchart",
            "sequenceDiagram",
            "blocked",
        ],
    },
    "T02-02": {
        "label": "缺口分级、授权与阻断",
        "files": [
            "requirement-gap-rules/SKILL.md",
            "requirement-gap-rules/references/missing-info-checklist.md",
            "requirement-gap-rules/agents/openai.yaml",
        ],
        "tokens": [
            "GAP-*",
            "P0",
            "P1",
            "P2",
            "授权人",
            "有效期",
            "复核",
            "blocked",
            "清理",
            "回滚",
        ],
    },
    "T02-03": {
        "label": "边界、切片与变更传播",
        "files": [
            "requirement-boundary-rules/references/boundary-checklist.md",
            "requirement-boundary-rules/agents/openai.yaml",
            "requirement-splitting-rules/references/splitting-dimensions.md",
            "requirement-splitting-rules/agents/openai.yaml",
            "requirement-change-rules/references/impact-recheck.md",
            "requirement-change-rules/agents/openai.yaml",
        ],
        "tokens": [
            "BOUND-*",
            "SLICE-*",
            "CHG-*",
            "In Scope",
            "Out of Scope",
            "文件/符号",
            "依赖 DAG",
            "REQ/RULE -> AC",
            "原值/新值",
            "回开",
        ],
    },
    "T02-04": {
        "label": "二值验收与 REQ-AC 覆盖",
        "files": [
            "acceptance-criteria-rules/references/acceptance-template.md",
            "acceptance-criteria-rules/agents/openai.yaml",
        ],
        "tokens": [
            "AC-*",
            "REQ-*",
            "PASS",
            "FAIL",
            "local",
            "失败预期",
            "清理",
            "回滚",
            "flowchart",
            "sequenceDiagram",
        ],
    },
}


def read_case(case: dict) -> str:
    chunks = []
    for relative in case["files"]:
        path = ROOT / relative
        if not path.is_file():
            raise AssertionError(f"文件不存在: {relative}")
        chunks.append(path.read_text(encoding="utf-8"))
    return "\n".join(chunks)


def assert_case(case_id: str) -> None:
    case = CASES[case_id]
    content = read_case(case)
    missing = [token for token in case["tokens"] if token not in content]
    if missing:
        raise AssertionError(f"{case_id} 正例缺少字段: {', '.join(missing)}")

    removed = case["tokens"][0]
    negative = content.replace(removed, "")
    if removed in negative:
        raise AssertionError(f"{case_id} 负例构造失败: {removed}")
    if all(token in negative for token in case["tokens"]):
        raise AssertionError(f"{case_id} 缺字段负例未阻断: {removed}")
    print(f"步骤 {case_id}: {case['label']} 正例 PASS，移除 {removed} 的负例按预期 BLOCKED")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--case", choices=[*CASES, "all"], default="all")
    args = parser.parse_args()
    selected = list(CASES) if args.case == "all" else [args.case]
    print("开始: 周期 02 需求/验收 Skill 极致完整性行为测试")
    try:
        for case_id in selected:
            assert_case(case_id)
    except AssertionError as error:
        print(f"失败点: {error}")
        return 1
    print("结束: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
