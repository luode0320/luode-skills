#!/usr/bin/env python3
"""
parse_excel_tcases.py - Parse TAPD-exported Excel (.xls/.xlsx) test case files.

This script parses Excel files exported from TAPD's test case module and outputs
JSON structures that can be directly used as TAPD AddTcase/BatchAddTcase API
request bodies (see references/tcases/addtcase.md, batchaddtcase.md).

The output JSON structure is identical to parse_xmind_tcases.py:
{
  "meta": {
    "source": "云端TAPD平台_测试用例_20260408141250.xls",
    "total": 5,
    "workspace_id": "12345"       // if --workspace-id is provided
  },
  "tcases": [
    {
      "workspace_id": "12345",    // if --workspace-id is provided
      "name": "用例名称",
      "precondition": "前置条件",
      "steps": "1. 步骤1\\n2. 步骤2",
      "expectation": "1. 预期结果1\\n2. 预期结果2",
      "type": "功能测试",
      "priority": "高",
      "status": "normal",
      "category_path": "目录A/目录B"  // auxiliary field for category lookup
    },
    ...
  ]
}

TAPD Excel Export Format:
  - Row 0: Header row with column names
  - Data rows: Each test case occupies one or more rows
  - Continuation rows: When a test case has multiple "关联需求" (related stories),
    extra rows appear with only the "关联需求" column filled (other columns empty).
    These continuation rows are merged into the parent test case.

Expected columns (TAPD default export):
  测试用例ID | 用例名称 | 用例类型 | 用例状态 | 用例等级 | 创建人 | 创建时间 |
  用例目录 | 是否实现自动化 | 自动化测试类型 | 自动化测试平台 | 是否上架 |
  用例步骤 | 前置条件 | 预期结果 | 关联需求 | 最后修改人 | 最后修改时间

Usage:
    python3 parse_excel_tcases.py <excel_file> [--workspace-id <id>] [--out-file <path>]

Examples:
    python3 parse_excel_tcases.py test_cases.xls
    python3 parse_excel_tcases.py test_cases.xls --workspace-id 12345 -f result.json
    python3 parse_excel_tcases.py test_cases.xlsx -w 12345 -f result.json

Dependencies:
    - pandas: pip install pandas
    - openpyxl (for .xlsx files): pip install openpyxl
    - xlrd (for .xls files): pip install xlrd
"""

import argparse
import json
import os
import sys
import xlrd

import pandas as pd

from typing import Any


# --- Constants ---

# Column name -> field key mapping (TAPD export column names)
COLUMN_MAP: dict[str, str] = {
    "测试用例ID": "tcase_id",
    "用例名称": "name",
    "用例类型": "type",
    "用例状态": "status",
    "用例等级": "priority",
    "创建人": "creator",
    "创建时间": "created",
    "用例目录": "category_path",
    "是否实现自动化": "is_automated",
    "自动化测试类型": "automation_type",
    "自动化测试平台": "automation_platform",
    "是否上架": "is_published",
    "用例步骤": "steps",
    "前置条件": "precondition",
    "预期结果": "expectation",
    "关联需求": "related_stories",
    "最后修改人": "modifier",
    "最后修改时间": "modified",
}

# Status mapping: Chinese -> API value
STATUS_MAP: dict[str, str] = {
    "正常": "normal",
    "待更新": "updating",
    "已废弃": "abandon",
    "normal": "normal",
    "updating": "updating",
    "abandon": "abandon",
}

# Valid TAPD tcase type values
VALID_TYPES: set[str] = {"功能测试", "性能测试", "安全性测试", "其他", "其它"}

# Valid priority values
VALID_PRIORITIES: set[str] = {"高", "中", "低"}

# Fields to include in API output body
API_FIELDS: list[str] = [
    "name", "precondition", "steps", "expectation", "type", "priority", "status",
]


# --- Excel Reading ---

def read_excel(filepath: str) -> list[list[str]]:
    """Read Excel file (.xls or .xlsx) and return rows as string lists.

    Uses pandas with openpyxl engine for .xlsx files.
    For .xls files, uses xlrd directly with ``ignore_workbook_corruption=True``
    to handle TAPD-exported files that may have corruption markers, then wraps
    the xlrd workbook in a pandas DataFrame.

    Args:
        filepath: Path to the Excel file (.xls or .xlsx).

    Returns:
        List of rows, where the first row is the header and each row is
        a list of string cell values.

    Raises:
        FileNotFoundError: If the file does not exist.
        ValueError: If the file extension is not supported.
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Excel file not found: {filepath}")

    ext = os.path.splitext(filepath)[1].lower()
    if ext not in (".xls", ".xlsx"):
        raise ValueError(f"Unsupported file extension: {ext}. Expected .xls or .xlsx")

    if ext == ".xlsx":
        df = pd.read_excel(filepath, header=None, engine="openpyxl", dtype=str)
    else:
        # TAPD-exported .xls files often have corruption markers.
        # Use xlrd directly with ignore_workbook_corruption=True to bypass.
        workbook = xlrd.open_workbook(
            filepath, ignore_workbook_corruption=True
        )
        df = pd.read_excel(
            workbook, header=None, engine="xlrd", dtype=str
        )

    df = df.fillna("")
    return _dataframe_to_rows(df)


def _dataframe_to_rows(df: "pd.DataFrame") -> list[list[str]]:  # noqa: F821
    """Convert a pandas DataFrame to a list of string row lists."""
    rows: list[list[str]] = []
    for _, row in df.iterrows():
        cells: list[str] = []
        for val in row:
            text = str(val).strip()
            # Convert float-like integer strings (e.g. "12345.0" -> "12345")
            if text.endswith(".0"):
                try:
                    cells.append(str(int(float(text))))
                    continue
                except (ValueError, OverflowError):
                    pass
            cells.append(text)
        rows.append(cells)
    return rows


# --- Parsing ---

def detect_columns(header_row: list[str]) -> dict[int, str]:
    """Detect column indices from the header row.

    Args:
        header_row: First row of the Excel file (column names).

    Returns:
        Dict mapping column index -> field key.
    """
    col_map: dict[int, str] = {}
    for i, col_name in enumerate(header_row):
        col_name = col_name.strip()
        if col_name in COLUMN_MAP:
            col_map[i] = COLUMN_MAP[col_name]
    return col_map


def is_data_row(row: list[str], col_map: dict[int, str]) -> bool:
    """Check if a row is a primary data row (has tcase_id or name).

    Continuation rows (for multi-value fields like 关联需求) have empty
    tcase_id and name columns.
    """
    for idx, field in col_map.items():
        if field in ("tcase_id", "name") and row[idx].strip():
            return True
    return False


def row_to_dict(row: list[str], col_map: dict[int, str]) -> dict[str, str]:
    """Convert a row to a field dict using the column mapping."""
    result: dict[str, str] = {}
    for idx, field in col_map.items():
        if idx < len(row):
            result[field] = row[idx].strip()
        else:
            result[field] = ""
    return result


def clean_steps(text: str) -> str:
    """Clean step/expectation text from TAPD Excel export.

    TAPD exports steps with leading/trailing whitespace and newlines.
    This normalizes the text while preserving meaningful line breaks.
    """
    if not text:
        return ""
    # Remove leading/trailing whitespace from each line
    lines = [line.strip() for line in text.split("\n")]
    # Remove empty leading/trailing lines
    while lines and not lines[0]:
        lines.pop(0)
    while lines and not lines[-1]:
        lines.pop()
    return "\n".join(lines)


def normalize_category_path(raw_path: str) -> str:
    """Normalize category path from TAPD export format.

    TAPD exports category paths with " - " as separator
    (e.g. "迭代16 - 模块A - 子模块B").
    Convert to "/" separator for consistency with parse_xmind_tcases.py.
    """
    if not raw_path:
        return ""
    # TAPD uses " - " as path separator in Excel export
    parts = [p.strip() for p in raw_path.split(" - ") if p.strip()]
    return "/".join(parts)


def parse_excel_tcases(filepath: str) -> list[dict[str, Any]]:
    """Parse an Excel file and return a list of TAPD tcase dicts.

    Handles TAPD's multi-row export format where continuation rows
    (for 关联需求 etc.) are merged into the parent test case.

    Args:
        filepath: Path to the Excel file (.xls or .xlsx).

    Returns:
        List of tcase dicts with fields:
            name, category_path, precondition, steps, expectation,
            type, priority, status
    """
    rows = read_excel(filepath)

    if len(rows) < 2:
        return []

    # Detect column layout from header
    col_map = detect_columns(rows[0])
    if not col_map:
        raise ValueError(
            f"Could not detect TAPD column layout from header row: {rows[0]}"
        )

    # Parse data rows, merging continuation rows
    tcases: list[dict[str, Any]] = []
    current_tcase: dict[str, Any] | None = None

    for row in rows[1:]:
        if is_data_row(row, col_map):
            # Save previous tcase
            if current_tcase and current_tcase.get("name"):
                tcases.append(current_tcase)

            # Start new tcase
            data = row_to_dict(row, col_map)
            raw_type = data.get("type", "")
            raw_priority = data.get("priority", "")
            current_tcase = {
                "name": data.get("name", ""),
                "category_path": normalize_category_path(
                    data.get("category_path", "")
                ),
                "precondition": clean_steps(data.get("precondition", "")),
                "steps": clean_steps(data.get("steps", "")),
                "expectation": clean_steps(data.get("expectation", "")),
                "type": raw_type if raw_type in VALID_TYPES else "",
                "priority": raw_priority if raw_priority in VALID_PRIORITIES else "",
                "status": STATUS_MAP.get(data.get("status", ""), "normal"),
                # Extra fields (not in API body, but useful for reference)
                "_tcase_id": data.get("tcase_id", ""),
                "_related_stories": [],
            }
            # Collect related stories
            related = data.get("related_stories", "")
            if related:
                current_tcase["_related_stories"].append(related)
        else:
            # Continuation row - merge related stories into current tcase
            if current_tcase:
                data = row_to_dict(row, col_map)
                related = data.get("related_stories", "")
                if related:
                    current_tcase["_related_stories"].append(related)

    # Don't forget the last tcase
    if current_tcase and current_tcase.get("name"):
        tcases.append(current_tcase)

    return tcases


# --- Output Functions ---

def to_api_body(
    tcase: dict[str, Any],
    workspace_id: str | None = None,
) -> dict[str, Any]:
    """Convert a parsed tcase dict to a TAPD AddTcase API request body.

    Empty/None values are omitted to keep the body clean.

    Args:
        tcase: Parsed tcase dict from parse_excel_tcases().
        workspace_id: TAPD workspace/project ID to inject.

    Returns:
        A dict ready to be used as TAPD AddTcase API request body.
    """
    body: dict[str, Any] = {}

    if workspace_id:
        body["workspace_id"] = workspace_id

    for field in API_FIELDS:
        value = tcase.get(field, "")
        if value:
            body[field] = value

    # Keep category_path as auxiliary info for category_id lookup
    if tcase.get("category_path"):
        body["category_path"] = tcase["category_path"]

    return body


def build_output(
    tcases: list[dict[str, Any]],
    filepath: str,
    workspace_id: str | None = None,
) -> dict[str, Any]:
    """Build the final JSON output structure with meta info and API-ready bodies.

    Args:
        tcases: List of parsed tcase dicts.
        filepath: Source Excel file path (for meta info).
        workspace_id: TAPD workspace/project ID.

    Returns:
        Dict with "meta" and "tcases" keys.
    """
    api_bodies = [to_api_body(tc, workspace_id) for tc in tcases]

    meta: dict[str, Any] = {
        "source": os.path.basename(filepath),
        "total": len(api_bodies),
    }
    if workspace_id:
        meta["workspace_id"] = workspace_id

    return {
        "meta": meta,
        "tcases": api_bodies,
    }


def output_json(
    tcases: list[dict[str, Any]],
    filepath: str,
    workspace_id: str | None = None,
    out_file: str | None = None,
) -> None:
    """Output parsed test cases as TAPD API-ready JSON."""
    result = build_output(tcases, filepath, workspace_id)
    json_str = json.dumps(result, ensure_ascii=False, indent=2)
    if out_file:
        with open(out_file, "w", encoding="utf-8") as f:
            f.write(json_str)
        print(f"[OK] {len(tcases)} test case(s) written to {out_file}")
    else:
        print(json_str)


def output_summary(tcases: list[dict[str, Any]]) -> None:
    """Print a summary of parsed test cases to stderr."""
    print(f"\n{'=' * 60}", file=sys.stderr)
    print(f"  Parsed {len(tcases)} test case(s)", file=sys.stderr)
    print(f"{'=' * 60}", file=sys.stderr)

    for i, tc in enumerate(tcases, 1):
        print(f"\n  [{i}] {tc['name']}", file=sys.stderr)
        print(
            f"      ID       : {tc.get('_tcase_id', '(none)')}",
            file=sys.stderr,
        )
        print(
            f"      Category : {tc['category_path'] or '(none)'}",
            file=sys.stderr,
        )
        print(
            f"      Priority : {tc['priority'] or '(none)'}",
            file=sys.stderr,
        )
        print(
            f"      Type     : {tc['type'] or '(none)'}",
            file=sys.stderr,
        )
        print(f"      Status   : {tc['status']}", file=sys.stderr)
        if tc["precondition"]:
            pc_preview = tc["precondition"][:60]
            print(f"      Precond  : {pc_preview}...", file=sys.stderr)
        step_count = len(tc["steps"].split("\n")) if tc["steps"] else 0
        print(f"      Steps    : {step_count} step(s)", file=sys.stderr)
        related = tc.get("_related_stories", [])
        if related:
            print(
                f"      Related  : {len(related)} story(ies)",
                file=sys.stderr,
            )

    print(f"\n{'=' * 60}\n", file=sys.stderr)


# --- CLI ---

def main() -> None:
    """CLI entry point for parsing TAPD Excel test case files."""
    parser = argparse.ArgumentParser(
        description=(
            "Parse TAPD-exported Excel (.xls/.xlsx) test case files "
            "to API-ready JSON."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""\
Examples:
  # Parse and output TAPD API-ready JSON
  python3 parse_excel_tcases.py test_cases.xls

  # With workspace_id injected into each tcase body
  python3 parse_excel_tcases.py test_cases.xls --workspace-id 12345

  # Output to file
  python3 parse_excel_tcases.py test_cases.xls --workspace-id 12345 -f result.json

Output JSON Structure:
  {
    "meta": {"source": "file.xls", "total": N, "workspace_id": "..."},
    "tcases": [
      {"workspace_id": "...", "name": "...", "steps": "...", ...},
      ...
    ]
  }

  Each item in "tcases" can be directly used as TAPD AddTcase/BatchAddTcase
  API body.
        """,
    )
    parser.add_argument("excel_file", help="Path to the .xls or .xlsx file")
    parser.add_argument(
        "--workspace-id",
        "-w",
        default=None,
        help=(
            "TAPD workspace/project ID. If provided, injected into each "
            "tcase body."
        ),
    )
    parser.add_argument(
        "--out-file",
        "-f",
        default=None,
        help="Output file path. If not specified, prints to stdout.",
    )
    parser.add_argument(
        "--quiet",
        "-q",
        action="store_true",
        help="Suppress summary output to stderr.",
    )

    args = parser.parse_args()

    try:
        tcases = parse_excel_tcases(args.excel_file)
    except FileNotFoundError as e:
        print(f"[ERROR] {e}", file=sys.stderr)
        sys.exit(1)
    except ValueError as e:
        print(f"[ERROR] {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"[ERROR] Failed to parse Excel file: {e}", file=sys.stderr)
        sys.exit(1)

    if not tcases:
        print(
            "[WARN] No test cases found. Check if the Excel file has the "
            "expected TAPD export format.",
            file=sys.stderr,
        )

    if not args.quiet:
        output_summary(tcases)

    output_json(tcases, args.excel_file, args.workspace_id, args.out_file)


if __name__ == "__main__":
    main()
