#!/usr/bin/env python3
"""
parse_xmind_tcases.py - Parse XMind file exported from TAPD to extract test cases.

This script directly parses XMind files (ZIP + JSON) without any third-party
xmind library. It outputs JSON structures that can be directly used as TAPD
AddTcase API request bodies (see references/tcases/addtcase.md).

Output JSON structure:
{
  "meta": {
    "source": "test_cases.xmind",
    "total": 5,
    "workspace_id": "12345"       // if --workspace-id is provided
  },
  "tcases": [
    {
      "workspace_id": "12345",    // if --workspace-id is provided
      "name": "用例名称",
      "precondition": "前置条件",
      "steps": "1. 步骤1\n2. 步骤2",
      "expectation": "1. 预期结果1\n2. 预期结果2",
      "type": "功能测试",
      "priority": "高",
      "status": "normal",
      "category_path": "目录A/目录B"  // auxiliary field for category lookup
    },
    ...
  ]
}

XMind Structure (TAPD export format):
┌──────────────────────────────────────────────────────────────────────┐
│  Root Node (file name, ignored)                                      │
│    └── Group/Category nodes (multi-level directories)                │
│          └── Test Case node (title starts with "tc:" or "tc-")       │
│                ├── Precondition node (title starts with "pc:")        │
│                ├── Step node (plain text, no prefix)                  │
│                │     └── Expected result (child of step node)         │
│                └── ...more steps                                     │
└──────────────────────────────────────────────────────────────────────┘

Usage:
    python3 parse_xmind_tcases.py <xmind_file> [--workspace-id <id>] [--out-file <path>]

Examples:
    python3 parse_xmind_tcases.py test_cases.xmind
    python3 parse_xmind_tcases.py test_cases.xmind --workspace-id 12345 -f result.json
"""

import argparse
import json
import os
import re
import subprocess
import sys
import urllib.parse
import zipfile
from typing import Any


# --- Constants ---

# Valid TAPD tcase type values
VALID_TYPES = {"功能测试", "性能测试", "安全性测试", "其他", "其它"}

# Priority mapping: support multiple formats
PRIORITY_MAP = {
    "高": "高", "high": "高", "p1": "高", "1": "高",
    "中": "中", "medium": "中", "p2": "中", "2": "中",
    "低": "低", "low": "低", "p3": "低", "3": "低",
}

# Regex to detect CSS style content (TAPD export artifact, should be ignored)
CSS_PATTERN = re.compile(
    r"\.teditor-container|padding:\s*\d+px|font-size:\s*\d+px|line-height:\s*\d+px"
)

# Regex to parse test case node title: tc[-priority][-type]:name
# Supports: "tc:name", "tc-高:name", "tc-P1:name", "tc-高-功能测试:name", "tc-P1-功能测试:name"
TC_PATTERN = re.compile(
    r"^tc(?:-([^-:：]+))?(?:-([^:：]+))?[：:](.+)$",
    re.IGNORECASE,
)

# Regex to parse precondition node title: pc:content
PC_PATTERN = re.compile(r"^pc[：:](.*)$", re.IGNORECASE)


# --- Core Functions ---

def read_xmind_content(xmind_path: str) -> list[dict]:
    """
    Read and parse content.json from an XMind file (ZIP archive).

    Args:
        xmind_path: Path to the .xmind file.

    Returns:
        Parsed JSON content as a list of sheet dicts.

    Raises:
        FileNotFoundError: If the xmind file does not exist.
        ValueError: If content.json is not found in the archive.
    """
    if not os.path.exists(xmind_path):
        raise FileNotFoundError(f"XMind file not found: {xmind_path}")

    with zipfile.ZipFile(xmind_path, "r") as zf:
        names = zf.namelist()
        if "content.json" not in names:
            raise ValueError(
                f"content.json not found in XMind archive. "
                f"Available files: {names}. "
                f"This may be an older XMind format (XML-based) which is not supported."
            )
        raw = zf.read("content.json")
        return json.loads(raw)


def is_css_content(text: str) -> bool:
    """Check if text is CSS style content (TAPD export artifact)."""
    return bool(CSS_PATTERN.search(text))


def clean_text(text: str) -> str:
    """Clean text by stripping whitespace and removing empty content."""
    if not text:
        return ""
    return text.strip()


def parse_tc_title(title: str) -> dict[str, str] | None:
    """
    Parse a test case node title.

    Supported formats:
        - "tc:用例名称"
        - "tc-高:用例名称"
        - "tc-P1:用例名称"
        - "tc-功能测试:用例名称"
        - "tc-高-功能测试:用例名称"
        - "tc-P1-性能测试:用例名称"
        - "tc-正常:用例名称" (status prefix)

    Returns:
        Dict with keys: name, priority, type, status; or None if not a tc node.
    """
    title = clean_text(title)
    if not title:
        return None

    match = TC_PATTERN.match(title)
    if not match:
        return None

    part1 = clean_text(match.group(1) or "")
    part2 = clean_text(match.group(2) or "")
    name = clean_text(match.group(3))

    result = {"name": name, "priority": "", "type": "", "status": "normal"}

    # Parse part1 and part2 - they can be priority, type, or status in any order
    for part in [part1, part2]:
        if not part:
            continue
        part_lower = part.lower()

        # Check if it's a priority
        if part_lower in PRIORITY_MAP:
            result["priority"] = PRIORITY_MAP[part_lower]
        # Check if it's a type
        elif part in VALID_TYPES:
            result["type"] = part
        # Check if it's a status keyword
        elif part in ("正常", "normal"):
            result["status"] = "normal"
        elif part in ("待更新", "updating"):
            result["status"] = "updating"
        elif part in ("已废弃", "abandon"):
            result["status"] = "abandon"
        # Fallback: treat as priority if it looks like P1/P2/P3
        elif re.match(r"^[pP]\d$", part):
            result["priority"] = PRIORITY_MAP.get(part_lower, "")

    return result


def parse_pc_title(title: str) -> str | None:
    """
    Parse a precondition node title (prefixed with "pc:").

    Returns:
        Precondition text, or None if not a pc node.
        Returns empty string if matched but content is CSS or empty.
    """
    title = clean_text(title)
    if not title:
        return None

    match = PC_PATTERN.match(title)
    if match:
        content = clean_text(match.group(1))
        # Filter out CSS style content (TAPD export artifact)
        if content and is_css_content(content):
            return ""
        return content
    return None


def extract_step_and_expectation(step_node: dict) -> dict[str, str]:
    """
    Extract step description and expected result from a step node.

    The step node's title is the step description.
    Its child nodes' titles are the expected results (merged).
    CSS content is filtered out.

    Returns:
        Dict with keys: step, expectation.
    """
    step_text = clean_text(step_node.get("title", ""))

    # Skip CSS content
    if is_css_content(step_text):
        step_text = ""

    # Collect expected results from child nodes
    expectations = []
    children = step_node.get("children", {}).get("attached", [])
    for child in children:
        child_title = clean_text(child.get("title", ""))
        if child_title and not is_css_content(child_title):
            expectations.append(child_title)

    return {
        "step": step_text,
        "expectation": "\n".join(expectations),
    }


def parse_tcase_node(tc_node: dict, category_path: str) -> dict[str, Any]:
    """
    Parse a single test case node and its children into a tcase dict.

    Args:
        tc_node: The test case topic node.
        category_path: The directory/category path (e.g. "目录A/目录B/目录C").

    Returns:
        A dict representing a TAPD tcase entity.
    """
    tc_info = parse_tc_title(tc_node.get("title", ""))
    if not tc_info:
        return {}

    preconditions = []
    steps = []
    expectations = []

    children = tc_node.get("children", {}).get("attached", [])

    for child in children:
        child_title = clean_text(child.get("title", ""))

        # Check if this is a precondition node
        pc_text = parse_pc_title(child_title)
        if pc_text is not None:
            if pc_text:
                preconditions.append(pc_text)
            continue

        # Skip CSS-only nodes entirely (TAPD export artifact)
        if is_css_content(child_title):
            continue

        # Skip completely empty nodes
        if not child_title:
            continue

        # This is a real step node - collect raw text without numbering
        step_data = extract_step_and_expectation(child)
        if step_data["step"]:
            steps.append(step_data["step"])
        if step_data["expectation"]:
            expectations.append(step_data["expectation"])

    return {
        "name": tc_info["name"],
        "category_path": category_path,
        "precondition": "\n".join(preconditions),
        "steps": "\n".join(steps),
        "expectation": "\n".join(expectations),
        "type": tc_info.get("type", ""),
        "priority": tc_info.get("priority", ""),
        "status": tc_info.get("status", "normal"),
    }


def walk_topics(
    node: dict,
    category_path: str = "",
    results: list[dict] | None = None,
) -> list[dict]:
    """
    Recursively walk the XMind topic tree to find and parse test case nodes.

    Nodes with "tc:" prefix are treated as test cases.
    Other nodes are treated as category/directory nodes.

    Args:
        node: Current topic node.
        category_path: Accumulated category path.
        results: List to collect parsed test cases.

    Returns:
        List of parsed tcase dicts.
    """
    if results is None:
        results = []

    title = clean_text(node.get("title", ""))
    children = node.get("children", {}).get("attached", [])

    # Check if current node is a test case
    if parse_tc_title(title) is not None:
        tcase = parse_tcase_node(node, category_path)
        if tcase and tcase.get("name"):
            results.append(tcase)
        return results

    # Otherwise, treat as a category/directory node and recurse into children
    for child in children:
        child_title = clean_text(child.get("title", ""))

        # Build category path for non-tc children
        if parse_tc_title(child_title) is not None:
            # This child is a test case, parse it with current category_path
            tcase = parse_tcase_node(child, category_path)
            if tcase and tcase.get("name"):
                results.append(tcase)
        else:
            # This child is a category/directory node
            new_path = f"{category_path}/{child_title}" if category_path else child_title
            walk_topics(child, new_path, results)

    return results


def parse_xmind_tcases(xmind_path: str) -> list[dict]:
    """
    Main entry: parse an XMind file and return a list of TAPD tcase dicts.

    Args:
        xmind_path: Path to the .xmind file.

    Returns:
        List of tcase dicts with fields:
            name, category_path, precondition, steps, expectation,
            type, priority, status
    """
    sheets = read_xmind_content(xmind_path)
    all_tcases = []

    for sheet in sheets:
        root_topic = sheet.get("rootTopic", {})
        tcases = walk_topics(root_topic)
        all_tcases.extend(tcases)

    return all_tcases


# --- Output Functions ---

def to_api_body(tcase: dict, workspace_id: str | None = None) -> dict:
    """
    Convert a parsed tcase dict to a TAPD AddTcase API request body.

    Maps directly to the API parameters defined in addtcase.md:
      - workspace_id (required, injected if provided)
      - name (required)
      - precondition, steps, expectation, type, priority, status (optional)
      - category_path (auxiliary, not an API field, kept for category_id lookup)

    Empty/None values are omitted to keep the body clean.

    Args:
        tcase: Parsed tcase dict from parse_tcase_node().
        workspace_id: TAPD workspace/project ID to inject.

    Returns:
        A dict ready to be used as TAPD AddTcase API request body.
    """
    # API field mapping (field_name -> tcase_key)
    api_fields = [
        "name", "precondition", "steps", "expectation",
        "type", "priority", "status",
    ]

    body = {}

    # Inject workspace_id if provided
    if workspace_id:
        body["workspace_id"] = workspace_id

    # Map fields, omit empty values
    for field in api_fields:
        value = tcase.get(field, "")
        if value:
            body[field] = value

    # Keep category_path as auxiliary info (not a direct API field,
    # but useful for looking up category_id before API call)
    if tcase.get("category_path"):
        body["category_path"] = tcase["category_path"]

    return body


def build_output(tcases: list[dict], xmind_path: str,
                 workspace_id: str | None = None) -> dict:
    """
    Build the final JSON output structure with meta info and API-ready bodies.

    Args:
        tcases: List of parsed tcase dicts.
        xmind_path: Source XMind file path (for meta info).
        workspace_id: TAPD workspace/project ID.

    Returns:
        Dict with "meta" and "tcases" keys.
    """
    api_bodies = [to_api_body(tc, workspace_id) for tc in tcases]

    meta = {
        "source": os.path.basename(xmind_path),
        "total": len(api_bodies),
    }
    if workspace_id:
        meta["workspace_id"] = workspace_id

    return {
        "meta": meta,
        "tcases": api_bodies,
    }


# --- TAPD Category API Functions ---

def _tapd_api_get(endpoint: str, token: str, params: dict) -> dict:
    """
    Call TAPD GET API via curl.

    Args:
        endpoint: TAPD API base URL (e.g. https://api.tapd.cn).
        token: TAPD Bearer token.
        params: Query parameters dict.

    Returns:
        Parsed JSON response dict.

    Raises:
        RuntimeError: If the API call fails.
    """
    query = urllib.parse.urlencode(params)
    url = f"{endpoint}/tcase_categories?{query}"
    result = subprocess.run(
        ["curl", "-s", "-H", f"Authorization: Bearer {token}", url],
        capture_output=True, text=True, timeout=30,
    )
    if result.returncode != 0:
        raise RuntimeError(f"curl GET failed: {result.stderr}")
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError:
        raise RuntimeError(f"Invalid JSON response: {result.stdout[:200]}")


def _tapd_api_post(endpoint: str, token: str, data: dict) -> dict:
    """
    Call TAPD POST API via curl.

    Args:
        endpoint: TAPD API base URL.
        token: TAPD Bearer token.
        data: POST body dict.

    Returns:
        Parsed JSON response dict.

    Raises:
        RuntimeError: If the API call fails.
    """
    url = f"{endpoint}/tcase_categories"
    body = json.dumps(data, ensure_ascii=False)
    result = subprocess.run(
        [
            "curl", "-s", "-X", "POST",
            "-H", f"Authorization: Bearer {token}",
            "-H", "Content-Type: application/json",
            url, "-d", body,
        ],
        capture_output=True, text=True, timeout=30,
    )
    if result.returncode != 0:
        raise RuntimeError(f"curl POST failed: {result.stderr}")
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError:
        raise RuntimeError(f"Invalid JSON response: {result.stdout[:200]}")


def fetch_existing_categories(endpoint: str, token: str,
                              workspace_id: str) -> list[dict]:
    """
    Fetch all existing tcase categories from TAPD.

    Handles pagination automatically (max 200 per page).

    Args:
        endpoint: TAPD API base URL.
        token: TAPD Bearer token.
        workspace_id: TAPD workspace/project ID.

    Returns:
        List of category dicts with keys: id, name, parent_id.
    """
    all_categories = []
    page = 1
    while True:
        resp = _tapd_api_get(endpoint, token, {
            "workspace_id": workspace_id,
            "limit": 200,
            "page": page,
        })
        if resp.get("status") != 1:
            raise RuntimeError(
                f"Failed to fetch categories: {resp.get('info', 'unknown error')}"
            )
        data = resp.get("data", [])
        if not data:
            break
        for item in data:
            cat = item.get("TcaseCategory", {})
            all_categories.append({
                "id": cat.get("id", ""),
                "name": cat.get("name", ""),
                "parent_id": cat.get("parent_id", "0"),
            })
        if len(data) < 200:
            break
        page += 1

    return all_categories


def find_root_category_id(categories: list[dict]) -> str:
    """
    Find the root category ID for the project.

    TAPD projects have a default root category (usually "None Category")
    whose parent_id is "0". New top-level categories must use this root
    category's ID as their parent_id (not "0").

    Args:
        categories: List of category dicts from fetch_existing_categories().

    Returns:
        The root category ID, or "0" as fallback.
    """
    for cat in categories:
        if cat["parent_id"] == "0":
            return cat["id"]
    return "0"


def build_category_tree(categories: list[dict]) -> dict:
    """
    Build a lookup dict: full_path -> category_id.

    Supports multi-level nested directories.
    E.g. {"冒烟测试": "123", "冒烟测试/登录模块": "456"}

    Args:
        categories: List of category dicts from fetch_existing_categories().

    Returns:
        Dict mapping full category path to category ID.
    """
    # Build parent_id -> children mapping
    children_map: dict[str, list[dict]] = {}
    for cat in categories:
        pid = cat["parent_id"]
        children_map.setdefault(pid, []).append(cat)

    path_to_id: dict[str, str] = {}

    # Find the root category (parent_id="0") and start walking from its children
    root_id = find_root_category_id(categories)

    def _walk(parent_id: str, prefix: str):
        for cat in children_map.get(parent_id, []):
            # Skip the root category itself (e.g. "None Category")
            if cat["parent_id"] == "0":
                continue
            full_path = f"{prefix}/{cat['name']}" if prefix else cat["name"]
            path_to_id[full_path] = cat["id"]
            _walk(cat["id"], full_path)

    # Walk from root's children (parent_id = root_id)
    _walk(root_id, "")
    # Also walk from "0" for categories directly under root
    # (in case some categories have parent_id="0" but are not the root itself)
    _walk("0", "")

    return path_to_id


def ensure_category_path(
    path: str,
    endpoint: str,
    token: str,
    workspace_id: str,
    path_to_id: dict[str, str],
    root_category_id: str = "0",
) -> str:
    """
    Ensure a full category path exists, creating missing directories as needed.

    For path "A/B/C":
      1. Check if "A" exists, create if not
      2. Check if "A/B" exists, create if not
      3. Check if "A/B/C" exists, create if not

    Args:
        path: Full category path, e.g. "冒烟测试/登录模块".
        endpoint: TAPD API base URL.
        token: TAPD Bearer token.
        workspace_id: TAPD workspace/project ID.
        path_to_id: Mutable dict mapping path -> category_id (updated in-place).
        root_category_id: The root category ID for the project (top-level parent).

    Returns:
        The category_id of the leaf directory.
    """
    parts = [p.strip() for p in path.split("/") if p.strip()]
    if not parts:
        return ""

    current_path = ""
    parent_id = root_category_id

    for part in parts:
        current_path = f"{current_path}/{part}" if current_path else part

        if current_path in path_to_id:
            parent_id = path_to_id[current_path]
            continue

        # Create the missing directory
        print(f"  [CREATE] Category: {current_path} (parent_id={parent_id})",
              file=sys.stderr)
        resp = _tapd_api_post(endpoint, token, {
            "workspace_id": workspace_id,
            "name": part,
            "parent_id": parent_id,
        })

        if resp.get("status") != 1:
            raise RuntimeError(
                f"Failed to create category '{current_path}': "
                f"{resp.get('info', 'unknown error')}"
            )

        new_id = resp["data"]["TcaseCategory"]["id"]
        path_to_id[current_path] = new_id
        parent_id = new_id
        print(f"  [OK]     Category created: id={new_id}", file=sys.stderr)

    return parent_id


def resolve_category_ids(
    tcases: list[dict],
    endpoint: str,
    token: str,
    workspace_id: str,
) -> list[dict]:
    """
    Resolve category_path to category_id for each tcase.

    For each tcase with a category_path:
      1. Look up existing categories
      2. Create missing directories as needed
      3. Replace category_path with category_id in the tcase body

    Args:
        tcases: List of tcase API body dicts (with category_path field).
        endpoint: TAPD API base URL.
        token: TAPD Bearer token.
        workspace_id: TAPD workspace/project ID.

    Returns:
        Updated list of tcase dicts with category_id set.
    """
    # Collect all unique category paths
    paths = set()
    for tc in tcases:
        cp = tc.get("category_path", "")
        if cp:
            paths.add(cp)

    if not paths:
        print("  [INFO] No category paths to resolve.", file=sys.stderr)
        return tcases

    print(f"\n[CATEGORY] Resolving {len(paths)} unique category path(s)...",
          file=sys.stderr)

    # Fetch existing categories and build lookup tree
    existing = fetch_existing_categories(endpoint, token, workspace_id)
    path_to_id = build_category_tree(existing)
    root_category_id = find_root_category_id(existing)

    print(f"  [INFO] Found {len(existing)} existing categories, "
          f"{len(path_to_id)} unique paths.", file=sys.stderr)
    print(f"  [INFO] Root category ID: {root_category_id}", file=sys.stderr)

    # Ensure all required paths exist
    for path in sorted(paths):
        ensure_category_path(path, endpoint, token, workspace_id,
                             path_to_id, root_category_id)

    # Update tcases with resolved category_id
    for tc in tcases:
        cp = tc.get("category_path", "")
        if cp and cp in path_to_id:
            tc["category_id"] = path_to_id[cp]
            # Remove auxiliary field, keep only API field
            del tc["category_path"]
        elif cp:
            print(f"  [WARN] Could not resolve category path: {cp}",
                  file=sys.stderr)

    print(f"[CATEGORY] Done.\n", file=sys.stderr)
    return tcases


def output_json(tcases: list[dict], xmind_path: str,
                workspace_id: str | None = None,
                out_file: str | None = None) -> None:
    """Output parsed test cases as TAPD API-ready JSON."""
    result = build_output(tcases, xmind_path, workspace_id)
    json_str = json.dumps(result, ensure_ascii=False, indent=2)
    if out_file:
        with open(out_file, "w", encoding="utf-8") as f:
            f.write(json_str)
        print(f"[OK] {len(tcases)} test case(s) written to {out_file}")
    else:
        print(json_str)


def output_summary(tcases: list[dict]) -> None:
    """Print a summary of parsed test cases to stderr."""
    print(f"\n{'='*60}", file=sys.stderr)
    print(f"  Parsed {len(tcases)} test case(s)", file=sys.stderr)
    print(f"{'='*60}", file=sys.stderr)

    for i, tc in enumerate(tcases, 1):
        print(f"\n  [{i}] {tc['name']}", file=sys.stderr)
        print(f"      Category : {tc['category_path'] or '(none)'}", file=sys.stderr)
        print(f"      Priority : {tc['priority'] or '(none)'}", file=sys.stderr)
        print(f"      Type     : {tc['type'] or '(none)'}", file=sys.stderr)
        print(f"      Status   : {tc['status']}", file=sys.stderr)
        if tc["precondition"]:
            print(f"      Precond  : {tc['precondition'][:60]}...", file=sys.stderr)
        step_count = len(tc["steps"].split("\n")) if tc["steps"] else 0
        print(f"      Steps    : {step_count} step(s)", file=sys.stderr)

    print(f"\n{'='*60}\n", file=sys.stderr)


# --- CLI ---

def main():
    parser = argparse.ArgumentParser(
        description="Parse XMind file (TAPD export) to extract test cases as API-ready JSON.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Parse and output TAPD API-ready JSON
  python3 parse_xmind_tcases.py test_cases.xmind

  # With workspace_id injected into each tcase body
  python3 parse_xmind_tcases.py test_cases.xmind --workspace-id 12345

  # Output to file
  python3 parse_xmind_tcases.py test_cases.xmind --workspace-id 12345 -f result.json

Output JSON Structure:
  {
    "meta": {"source": "file.xmind", "total": N, "workspace_id": "..."},
    "tcases": [
      {"workspace_id": "...", "name": "...", "steps": "...", ...},
      ...
    ]
  }

  Each item in "tcases" can be directly used as TAPD AddTcase API body.

XMind Node Format:
  Test case:     tc:用例名称  or  tc-高:用例名称  or  tc-P1-功能测试:用例名称
  Precondition:  pc:前置条件内容
  Steps:         Plain text child nodes of test case
  Expectation:   Child nodes of step nodes
        """,
    )
    parser.add_argument("xmind_file", help="Path to the .xmind file")
    parser.add_argument(
        "--workspace-id", "-w",
        default=None,
        help="TAPD workspace/project ID. If provided, injected into each tcase body.",
    )
    parser.add_argument(
        "--out-file", "-f",
        default=None,
        help="Output file path. If not specified, prints to stdout.",
    )
    parser.add_argument(
        "--quiet", "-q",
        action="store_true",
        help="Suppress summary output to stderr.",
    )
    parser.add_argument(
        "--resolve-categories", "-r",
        action="store_true",
        help="Resolve category_path to category_id via TAPD API. "
             "Requires --workspace-id and TAPD_TOKEN/TAPD_API_ENDPOINT env vars "
             "(or --api-token/--api-endpoint).",
    )
    parser.add_argument(
        "--api-endpoint",
        default=None,
        help="TAPD API endpoint URL. Defaults to TAPD_API_ENDPOINT env var, "
             "fallback to https://api.tapd.cn.",
    )
    parser.add_argument(
        "--api-token",
        default=None,
        help="TAPD API Bearer token. Defaults to TAPD_TOKEN env var.",
    )

    args = parser.parse_args()

    try:
        tcases = parse_xmind_tcases(args.xmind_file)
    except FileNotFoundError as e:
        print(f"[ERROR] {e}", file=sys.stderr)
        sys.exit(1)
    except ValueError as e:
        print(f"[ERROR] {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"[ERROR] Failed to parse XMind file: {e}", file=sys.stderr)
        sys.exit(1)

    if not tcases:
        print(
            "[WARN] No test cases found. Make sure test case nodes use 'tc:' prefix.",
            file=sys.stderr,
        )

    if not args.quiet:
        output_summary(tcases)

    # Build API-ready bodies first
    workspace_id = args.workspace_id
    api_bodies = [to_api_body(tc, workspace_id) for tc in tcases]

    # Resolve category paths to category IDs if requested
    if args.resolve_categories:
        if not workspace_id:
            print("[ERROR] --workspace-id is required for --resolve-categories.",
                  file=sys.stderr)
            sys.exit(1)

        api_endpoint = (
            args.api_endpoint
            or os.environ.get("TAPD_API_ENDPOINT", "")
            or "https://api.tapd.cn"
        )
        api_token = (
            args.api_token
            or os.environ.get("TAPD_TOKEN", "")
        )
        if not api_token:
            print("[ERROR] TAPD_TOKEN env var or --api-token is required "
                  "for --resolve-categories.", file=sys.stderr)
            sys.exit(1)

        try:
            api_bodies = resolve_category_ids(
                api_bodies, api_endpoint, api_token, workspace_id
            )
        except RuntimeError as e:
            print(f"[ERROR] Category resolution failed: {e}", file=sys.stderr)
            sys.exit(1)

    # Use resolved api_bodies instead of raw tcases
    result = {
        "meta": {
            "source": os.path.basename(args.xmind_file),
            "total": len(api_bodies),
        },
        "tcases": api_bodies,
    }
    if workspace_id:
        result["meta"]["workspace_id"] = workspace_id

    json_str = json.dumps(result, ensure_ascii=False, indent=2)
    if args.out_file:
        with open(args.out_file, "w", encoding="utf-8") as f:
            f.write(json_str)
        print(f"[OK] {len(api_bodies)} test case(s) written to {args.out_file}")
    else:
        print(json_str)


if __name__ == "__main__":
    main()
