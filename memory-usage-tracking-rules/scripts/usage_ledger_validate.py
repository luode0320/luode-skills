#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""usage_ledger_validate.py — 记忆使用计数回写前置校验（只读）

校验收口闸门提交的使用计数 claim 是否真实、可定位、无重复，防止 AI 虚报计数。

用法：
  python usage_ledger_validate.py \
      --project-root D:/谷歌云盘/luode-skills \
      --claims '[{"file": "PROJECT_MEMORY.md", "anchor": "rule.apifox-test-separate-db", "reason": "..."}]'

参数：
  --project-root  项目根目录（默认自动检测当前目录或环境变量 PROJECT_ROOT）
  --memory-file / --style-file / --history-file  三文件显式路径（缺省在 project-root 下按固定名找）
  --claims        使用计数 claim 的 JSON 字符串（必须）
  --claims-file   从文件读取 claims JSON（与 --claims 二选一）

claim 格式：
  [{"file": "PROJECT_MEMORY.md|PROJECT_STYLE.md|PROJECT_HISTORY.md",
    "anchor": "<entity_id 或条目标题或事件主题短语>",
    "reason": "<一句话引用场景，用于审计>"}]

校验规则：
  1. 锚点存在性：anchor 必须能定位到对应文件的计数锚点区
     - PROJECT_MEMORY.md：entities[].entity_id 精确匹配
     - PROJECT_STYLE.md：计数锚点区 anchors[].title 精确匹配
     - PROJECT_HISTORY.md：计数锚点区 anchors[].title 前缀/包含匹配（事件主题短语）
  2. 可定位性：锚点必须能回指人类阅读区的真实条目/事件
     - MEMORY：entity_id 或 name 出现在文件正文
     - STYLE：`### <title>` 出现在文件正文
     - HISTORY：`- YYYY-MM-DD：<title 前缀>` 出现在文件正文
  3. 会话内去重：(file, anchor) 相同只保留第一条

输出（stdout JSON，供闸门判断）：
  {"ok": true/false, "valid_claims": [...], "invalid_claims": [...],
   "duplicates_dropped": N, "detail": {...}}

退出码：0 = ok=true；1 = ok=false（含参数错误）；2 = 文件读取异常。
只读脚本，不修改任何记忆文件。
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime

MEMORY_NAME = "PROJECT_MEMORY.md"
STYLE_NAME = "PROJECT_STYLE.md"
HISTORY_NAME = "PROJECT_HISTORY.md"
ALLOWED_FILES = {
    "PROJECT_MEMORY.md": "memory",
    "PROJECT_STYLE.md": "style",
    "PROJECT_HISTORY.md": "history",
    "memory": "memory",
    "style": "style",
    "history": "history",
}


def extract_yaml_block(text, section_title):
    """提取 markdown 中指定小节标题后第一个 ```yaml ... ``` 块文本。"""
    pattern = re.compile(
        r"^##\s*" + re.escape(section_title) + r"\s*\n.*?```yaml\s*\n(.*?)\n```",
        re.MULTILINE | re.DOTALL,
    )
    m = pattern.search(text)
    return m.group(1) if m else None


def parse_memory_anchors(text):
    """解析 PROJECT_MEMORY.md 机器索引区 yaml，返回 {entity_id: entity}。"""
    import yaml

    block = extract_yaml_block(text, "机器索引区")
    if not block:
        return {}
    try:
        data = yaml.safe_load(block) or {}
    except yaml.YAMLError:
        return {}
    result = {}
    for ent in data.get("entities", []) or []:
        if isinstance(ent, dict) and ent.get("entity_id"):
            result[ent["entity_id"]] = ent
    return result


def parse_anchor_section_anchors(text, section_title="计数锚点区"):
    """解析 PROJECT_STYLE.md / PROJECT_HISTORY.md 底部计数锚点区 yaml 的 anchors[]。"""
    import yaml

    block = extract_yaml_block(text, section_title)
    if not block:
        return []
    try:
        data = yaml.safe_load(block) or {}
    except yaml.YAMLError:
        return []
    return [a for a in data.get("anchors", []) or [] if isinstance(a, dict) and a.get("title")]


def locate_file(project_root, kind, explicit_path):
    """定位记忆文件绝对路径。"""
    if explicit_path:
        return explicit_path
    names = {MEMORY_NAME, STYLE_NAME, HISTORY_NAME}
    for name in names:
        if kind in name.lower():
            return os.path.join(project_root, name)
    raise ValueError(f"无法定位文件: {kind}")


def validate_claim(claim, anchors_map):
    """返回 (valid, invalid_reason)。"""
    file_key = claim.get("file", "")
    anchor = claim.get("anchor", "")
    reason = claim.get("reason", "")
    norm = ALLOWED_FILES.get(file_key)
    if norm is None:
        return False, f"file 不允许的值: {file_key!r}"
    if not anchor:
        return False, "anchor 为空"
    if not reason:
        return False, "reason 为空（必须写一句话引用场景，用于审计）"

    # 锚点存在性
    if norm == "memory":
        if anchor not in anchors_map.get("memory", {}):
            return False, f"实体 entity_id={anchor!r} 不在机器索引区 entities[] 中"
        ent = anchors_map["memory"][anchor]
        # 可定位性：entity_id 或 name 出现在文件正文
        body = anchors_map["_body"]["memory"]
        if ent.get("name") and ent["name"] in body:
            return True, ""
        if anchor in body:
            return True, ""
        return False, f"实体 {anchor!r} 无法在人类阅读区定位（entity_id/name 未出现在正文）"
    if norm == "style":
        titles = anchors_map.get("style", [])
        if anchor not in titles:
            return False, f"锚点 title={anchor!r} 不在计数锚点区 anchors[] 中"
        if f"### {anchor}" in anchors_map["_body"]["style"]:
            return True, ""
        return False, f"条目 `### {anchor}` 未出现在 PROJECT_STYLE.md 正文中"
    if norm == "history":
        titles = anchors_map.get("history", [])
        matched = any(
            anchor == t or anchor in t or t in anchor for t in titles
        )
        if not matched:
            return False, f"锚点 title={anchor!r} 不在计数锚点区 anchors[] 中（支持前缀/包含匹配）"
        # 可定位性：事件行 `- YYYY-MM-DD：<主题>` 前缀匹配
        body = anchors_map["_body"]["history"]
        evt_pattern = re.compile(r"^- \d{4}-\d{2}-\d{2}：", re.MULTILINE)
        found = any(
            (evt_line.split("：", 1)[1].strip().startswith(anchor))
            or (anchor in evt_line.split("：", 1)[1])
            for evt_line in [l for l in body.splitlines() if evt_pattern.match(l.strip())]
        )
        if not found:
            return False, f"事件主题 {anchor!r} 未在 PROJECT_HISTORY.md 事件条目中定位"
        return True, ""
    return False, f"未知 file: {file_key!r}"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-root", default=os.environ.get("PROJECT_ROOT") or ".")
    parser.add_argument("--memory-file", default=None)
    parser.add_argument("--style-file", default=None)
    parser.add_argument("--history-file", default=None)
    parser.add_argument("--claims", default=None, help="claims JSON 字符串")
    parser.add_argument("--claims-file", default=None, help="claims JSON 文件路径")
    args = parser.parse_args()

    if not args.claims and not args.claims_file:
        print(json.dumps({"ok": False, "error": "缺少 --claims 或 --claims-file"}, ensure_ascii=False))
        sys.exit(1)

    try:
        raw = args.claims if args.claims else open(args.claims_file, encoding="utf-8").read()
        claims = json.loads(raw)
    except (json.JSONDecodeError, OSError) as e:
        print(json.dumps({"ok": False, "error": f"claims 解析失败: {e}"}, ensure_ascii=False))
        sys.exit(1)

    if not isinstance(claims, list):
        print(json.dumps({"ok": False, "error": "claims 必须是数组"}, ensure_ascii=False))
        sys.exit(1)

    try:
        paths = {
            "memory": locate_file(args.project_root, "memory", args.memory_file),
            "style": locate_file(args.project_root, "style", args.style_file),
            "history": locate_file(args.project_root, "history", args.history_file),
        }
        bodies = {}
        for k, p in paths.items():
            with open(p, encoding="utf-8") as f:
                bodies[k] = f.read()
    except (OSError, ValueError) as e:
        print(json.dumps({"ok": False, "error": f"读取记忆文件失败: {e}"}, ensure_ascii=False))
        sys.exit(2)

    anchors_map = {
        "memory": parse_memory_anchors(bodies["memory"]),
        "style": [a["title"] for a in parse_anchor_section_anchors(bodies["style"])],
        "history": [a["title"] for a in parse_anchor_section_anchors(bodies["history"])],
        "_body": bodies,
    }

    seen = set()
    valid_claims = []
    invalid_claims = []
    duplicates_dropped = 0
    for c in claims:
        norm = ALLOWED_FILES.get(c.get("file", ""))
        key = (norm, c.get("anchor", ""))
        if key in seen:
            duplicates_dropped += 1
            continue
        seen.add(key)
        ok, reason = validate_claim(c, anchors_map)
        entry = {"file": c.get("file"), "anchor": c.get("anchor"), "reason": c.get("reason", "")}
        if ok:
            valid_claims.append(entry)
        else:
            entry["invalid_reason"] = reason
            invalid_claims.append(entry)

    result = {
        "ok": len(invalid_claims) == 0,
        "valid_claims": valid_claims,
        "invalid_claims": invalid_claims,
        "duplicates_dropped": duplicates_dropped,
        "detail": {
            "checked_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "anchors": {k: len(v) if isinstance(v, list) else len(v) for k, v in anchors_map.items() if k != "_body"},
        },
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    sys.exit(0 if result["ok"] else 1)


if __name__ == "__main__":
    main()
