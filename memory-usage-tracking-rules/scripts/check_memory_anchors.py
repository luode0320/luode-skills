#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""check_memory_anchors.py — 项目记忆计数锚点结构健康检查（只读）

在「计数回写」与「吸收候选扫描」之前，先证明锚点结构本身是健康的。
本脚本存在的理由：文本写进去了 ≠ 解析器读得出来。`grep -c` 能命中的内容，
`yaml.safe_load` 可能整块抛错；而读取侧脚本一律 `except: return {}`，
于是「解析失败」和「确实没有数据」返回值完全相同、退出码都是 0，静默潜伏。

用法：
  python check_memory_anchors.py --project-root D:/path/to/repo
  python check_memory_anchors.py --project-root . --json        # 仅输出 JSON
  python check_memory_anchors.py --project-root . --list-missing # 附带待回补锚点清单

参数：
  --project-root   项目根目录（默认当前目录或环境变量 PROJECT_ROOT）
  --memory-file / --style-file / --history-file  三文件显式路径（缺省按固定名找）
  --json           只输出 JSON，不输出人类可读摘要
  --list-missing   在 JSON 中附带缺失锚点的完整清单（供回补时直接取用）

检查项：
  C1 yaml 可解析性     三个 yaml 块能否被 yaml.safe_load 读出（失败给出文件行号与原因）
  C2 非法裸标量        值以 YAML 保留符开头、或值内含 ": " / " #"（C1 失败时这就是修复指引）
  C3 schema 一致性     usage_tracking.counted_files 三项齐全 + policy_ref；entities 四个计数字段
  C4 锚点条目对应      STYLE 的 `### 标题` 与 HISTORY 的事件行，是否与 anchors[] 一一对应
  C5 锚点区位于底部    机器索引区 / 计数锚点区之后不得再有正文内容

输出（stdout JSON）：
  {"ok": true/false, "checks": {...}, "problems": [...], "summary": {...}}

退出码：0 = 全部通过；1 = 存在问题；2 = 文件读取异常。
只读脚本，不修改任何记忆文件。
"""

import argparse
import json
import os
import re
import sys

import yaml

MEMORY_NAME = "PROJECT_MEMORY.md"
STYLE_NAME = "PROJECT_STYLE.md"
HISTORY_NAME = "PROJECT_HISTORY.md"

# usage_tracking 的权威定义源：references/usage-anchor-schema.md 第 1 节。
# 此处是校验用副本，改 schema 必须同步改这里与 bootstrap_agents.sh 的三处模板。
EXPECTED_COUNTED_FILES = [MEMORY_NAME, STYLE_NAME, HISTORY_NAME]
EXPECTED_POLICY_REF = "memory-usage-tracking-rules/references/usage-tracking-policy.md"
COUNT_FIELDS = ["usage_count", "usage_days", "last_used_at", "absorbed_to"]

# YAML 中不能作为 plain scalar 首字符的保留符号
BAD_FIRST_CHARS = set("`*&!%@{}[],#?|>'\"")

EVENT_LINE = re.compile(r"^- \d{4}-\d{2}-\d{2}：")


def read_text(path):
    """读取 UTF-8 文本；文件缺失返回 None。

    [参数] path: 文件绝对路径
    [返回] 文件全文字符串，或 None
    """
    if not os.path.isfile(path):
        return None
    with open(path, encoding="utf-8") as f:
        return f.read()


def locate_yaml_block(text, section_title):
    """定位指定小节标题后的第一个 ```yaml 块。

    [参数] text: 文件全文；section_title: 二级标题文字（不含 ##）
    [返回] (块文本, 块起始文件行号, 块结束文件行号)；未命中返回 (None, 0, 0)
    """
    pattern = re.compile(
        r"^##\s*" + re.escape(section_title) + r"\s*\n.*?```yaml\s*\n(.*?)\n```",
        re.MULTILINE | re.DOTALL,
    )
    m = pattern.search(text)
    if not m:
        return None, 0, 0
    start_line = text[: m.start(1)].count("\n") + 1
    end_line = text[: m.end()].count("\n") + 1
    return m.group(1), start_line, end_line


def scan_bad_scalars(block, start_line):
    """扫描 yaml 块内非法 plain scalar 行。

    中文技术描述极易写出以反引号开头的值（`定义: `xxx` 是...`），或以星号开头的
    列表项（`- *_test.go`，会被当成未定义 alias），二者都让整块解析失败。

    [参数] block: yaml 块文本；start_line: 块首行对应的文件行号
    [返回] [{line, reason, snippet}] 列表
    """
    kv = re.compile(r"^(\s*)(?:-\s+)?([^:\s][^:]*):\s+(\S.*)$")
    item = re.compile(r"^(\s*)-\s+(\S.*)$")
    hits = []
    for i, line in enumerate(block.splitlines()):
        value = None
        mm = kv.match(line)
        if mm:
            value = mm.group(3)
        else:
            mi = item.match(line)
            if mi and ":" not in mi.group(2):
                value = mi.group(2)
        if not value:
            continue
        # 已用引号完整包裹的 quoted scalar 正是修复后的写法，不再判为非法
        if len(value) > 1 and value[0] in "\"'" and value[-1] == value[0]:
            continue
        # {} / [] 等完整配平的 flow collection 是合法写法，不算非法裸标量
        if value in ("{}", "[]"):
            continue
        if value[0] in "{[" and value[-1] in "}]":
            continue
        reasons = []
        if value[0] in BAD_FIRST_CHARS:
            reasons.append("首字符 %r 是 YAML 保留符，需用双引号包裹整个值" % value[0])
        if ": " in value:
            reasons.append("值内含冒号+空格，会被解析成嵌套映射，需用双引号包裹")
        if " #" in value:
            reasons.append("值内含空格+井号，会被当成行内注释，需用双引号包裹")
        if reasons:
            hits.append({"line": start_line + i, "reason": "；".join(reasons), "snippet": line.strip()[:100]})
    return hits


def parse_block(block, start_line):
    """解析 yaml 块，失败时把块内行号换算成文件行号。

    [参数] block: yaml 块文本；start_line: 块首行对应的文件行号
    [返回] (data, error)；成功时 error 为 None
    """
    try:
        return yaml.safe_load(block) or {}, None
    except yaml.YAMLError as e:
        mark = getattr(e, "problem_mark", None)
        err = {"message": str(e).replace("\n", " ")[:300]}
        if mark is not None:
            err["file_line"] = start_line + mark.line
            err["column"] = mark.column + 1
        return None, err


def check_tail_clean(text, block_end_line):
    """检查锚点区之后是否还有正文内容（锚点区必须位于文件底部）。

    [参数] text: 文件全文；block_end_line: yaml 块结束的文件行号
    [返回] [{line, snippet}] 违规行列表
    """
    lines = text.splitlines()
    offenders = []
    for i in range(block_end_line, len(lines)):
        stripped = lines[i].strip()
        if stripped:
            offenders.append({"line": i + 1, "snippet": stripped[:100]})
    return offenders


def check_memory(text, problems, summary, list_missing):
    """检查 PROJECT_MEMORY.md 的机器索引区。"""
    block, start, end = locate_yaml_block(text, "机器索引区")
    if block is None:
        problems.append({"check": "C1", "file": MEMORY_NAME, "detail": "未找到「## 机器索引区」下的 ```yaml 块"})
        return
    bad = scan_bad_scalars(block, start)
    data, err = parse_block(block, start)
    if err is not None:
        detail = "机器索引区 yaml 解析失败：%s" % err["message"]
        if "file_line" in err:
            detail += "（文件第 %d 行第 %d 列）" % (err["file_line"], err["column"])
        problems.append({"check": "C1", "file": MEMORY_NAME, "detail": detail, "bad_scalars": bad})
        return
    if bad:
        problems.append({
            "check": "C2", "file": MEMORY_NAME,
            "detail": "yaml 可解析，但存在 %d 行高风险裸标量，后续追加内容易整块打断" % len(bad),
            "bad_scalars": bad,
        })

    entities = data.get("entities") or []
    summary["memory_entities"] = len(entities)

    # C3 usage_tracking schema
    ut = data.get("usage_tracking")
    if not isinstance(ut, dict):
        problems.append({"check": "C3", "file": MEMORY_NAME, "detail": "机器索引区缺少 usage_tracking 顶层键"})
    else:
        counted = ut.get("counted_files") or []
        missing_files = [f for f in EXPECTED_COUNTED_FILES if f not in counted]
        if missing_files:
            problems.append({
                "check": "C3", "file": MEMORY_NAME,
                "detail": "usage_tracking.counted_files 缺少 %s（当前 %d 项，应为 3 项）"
                          % ("、".join(missing_files), len(counted)),
            })
        if not ut.get("policy_ref"):
            problems.append({
                "check": "C3", "file": MEMORY_NAME,
                "detail": "usage_tracking 缺少 policy_ref，应为 %s" % EXPECTED_POLICY_REF,
            })

    # C3 实体计数字段
    lacking = []
    for ent in entities:
        if not isinstance(ent, dict) or not ent.get("entity_id"):
            continue
        miss = [k for k in COUNT_FIELDS if k not in ent]
        if miss:
            lacking.append({"entity_id": ent["entity_id"], "missing": miss})
    summary["memory_entities_lacking_fields"] = len(lacking)
    if lacking:
        item = {
            "check": "C3", "file": MEMORY_NAME,
            "detail": "%d/%d 个实体缺计数字段（存量项目需一次性回补，否则计数恒 0、吸收永不触发）"
                      % (len(lacking), len(entities)),
        }
        if list_missing:
            item["entities"] = lacking
        problems.append(item)

    # C5 底部
    tail = check_tail_clean(text, end)
    if tail:
        problems.append({
            "check": "C5", "file": MEMORY_NAME,
            "detail": "机器索引区之后仍有 %d 行正文（机器索引区必须位于文件底部），首行为第 %d 行"
                      % (len(tail), tail[0]["line"]),
            "offenders": tail[:5],
        })


def check_anchor_section(text, filename, expected_titles, match_mode, problems, summary, list_missing):
    """检查 PROJECT_STYLE.md / PROJECT_HISTORY.md 的计数锚点区。

    [参数] expected_titles: 人类阅读区提取出的条目标题/事件正文列表
           match_mode: "exact"（STYLE 精确匹配）或 "contains"（HISTORY 前缀/包含匹配）
    """
    key = filename.replace("PROJECT_", "").replace(".md", "").lower()
    block, start, end = locate_yaml_block(text, "计数锚点区")
    if block is None:
        problems.append({
            "check": "C1", "file": filename,
            "detail": "未找到「## 计数锚点区」下的 ```yaml 块（存量项目需一次性初始化，共 %d 个条目待建锚点）"
                      % len(expected_titles),
        })
        summary["%s_anchors" % key] = 0
        summary["%s_entries" % key] = len(expected_titles)
        return
    bad = scan_bad_scalars(block, start)
    data, err = parse_block(block, start)
    if err is not None:
        detail = "计数锚点区 yaml 解析失败：%s" % err["message"]
        if "file_line" in err:
            detail += "（文件第 %d 行第 %d 列）" % (err["file_line"], err["column"])
        problems.append({"check": "C1", "file": filename, "detail": detail, "bad_scalars": bad})
        return
    if bad:
        problems.append({
            "check": "C2", "file": filename,
            "detail": "yaml 可解析，但存在 %d 行高风险裸标量" % len(bad),
            "bad_scalars": bad,
        })

    anchors = [a for a in (data.get("anchors") or []) if isinstance(a, dict) and a.get("title")]
    titles = [a["title"] for a in anchors]
    summary["%s_anchors" % key] = len(anchors)
    summary["%s_entries" % key] = len(expected_titles)

    # C3 锚点字段完整性
    lacking = [t["title"] for t in anchors if any(k not in t for k in COUNT_FIELDS)]
    if lacking:
        problems.append({
            "check": "C3", "file": filename,
            "detail": "%d 个锚点缺计数字段" % len(lacking),
        })

    # C4 一一对应
    def matched(entry):
        if match_mode == "exact":
            return entry in titles
        return any(t in entry or entry.startswith(t) for t in titles)

    missing = [e for e in expected_titles if not matched(e)]
    if match_mode == "exact":
        orphan = [t for t in titles if t not in expected_titles]
    else:
        orphan = [t for t in titles if not any(t in e or e.startswith(t) for e in expected_titles)]

    if missing:
        item = {
            "check": "C4", "file": filename,
            "detail": "%d 个条目没有对应锚点（新增条目未同步补锚点，或存量项目从未初始化）" % len(missing),
        }
        if list_missing:
            item["missing_titles"] = missing
        problems.append(item)
    if orphan:
        item = {
            "check": "C4", "file": filename,
            "detail": "%d 个锚点找不到对应条目（条目被删除或改名后锚点未同步）" % len(orphan),
        }
        if list_missing:
            item["orphan_titles"] = orphan
        problems.append(item)

    # C5 底部
    tail = check_tail_clean(text, end)
    if tail:
        problems.append({
            "check": "C5", "file": filename,
            "detail": "计数锚点区之后仍有 %d 行正文（锚点区必须位于文件底部），首行为第 %d 行"
                      % (len(tail), tail[0]["line"]),
            "offenders": tail[:5],
        })


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-root", default=os.environ.get("PROJECT_ROOT") or ".")
    parser.add_argument("--memory-file", default=None)
    parser.add_argument("--style-file", default=None)
    parser.add_argument("--history-file", default=None)
    parser.add_argument("--json", action="store_true", help="只输出 JSON")
    parser.add_argument("--list-missing", action="store_true", help="JSON 中附带缺失锚点完整清单")
    args = parser.parse_args()

    root = args.project_root
    paths = {
        MEMORY_NAME: args.memory_file or os.path.join(root, MEMORY_NAME),
        STYLE_NAME: args.style_file or os.path.join(root, STYLE_NAME),
        HISTORY_NAME: args.history_file or os.path.join(root, HISTORY_NAME),
    }
    try:
        texts = {name: read_text(path) for name, path in paths.items()}
    except OSError as e:
        print(json.dumps({"ok": False, "error": "读取记忆文件失败: %s" % e}, ensure_ascii=False))
        sys.exit(2)

    problems = []
    summary = {}

    if texts[MEMORY_NAME] is None:
        problems.append({"check": "C0", "file": MEMORY_NAME, "detail": "文件不存在"})
    else:
        check_memory(texts[MEMORY_NAME], problems, summary, args.list_missing)

    if texts[STYLE_NAME] is None:
        summary["style_entries"] = 0
        summary["style_anchors"] = 0
    else:
        style_titles = [
            line[4:].strip()
            for line in texts[STYLE_NAME].splitlines()
            if line.startswith("### ")
        ]
        check_anchor_section(
            texts[STYLE_NAME], STYLE_NAME, style_titles, "exact", problems, summary, args.list_missing
        )

    if texts[HISTORY_NAME] is None:
        problems.append({"check": "C0", "file": HISTORY_NAME, "detail": "文件不存在"})
    else:
        events = [
            line.split("：", 1)[1].strip()
            for line in texts[HISTORY_NAME].splitlines()
            if EVENT_LINE.match(line.strip()) and "：" in line
        ]
        check_anchor_section(
            texts[HISTORY_NAME], HISTORY_NAME, events, "contains", problems, summary, args.list_missing
        )

    result = {
        "ok": len(problems) == 0,
        "problems": problems,
        "summary": summary,
        "checks": {
            "C1": "yaml 可解析性",
            "C2": "非法裸标量",
            "C3": "schema 一致性（counted_files / policy_ref / 四个计数字段）",
            "C4": "锚点与条目一一对应",
            "C5": "锚点区位于文件底部",
        },
    }

    if not args.json:
        status = "PASS" if result["ok"] else "FAIL"
        print("[%s] 记忆计数锚点健康检查 — %s" % (status, root), file=sys.stderr)
        for p in problems:
            print("  [%s] %s: %s" % (p["check"], p["file"], p["detail"]), file=sys.stderr)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    sys.exit(0 if result["ok"] else 1)


if __name__ == "__main__":
    main()
