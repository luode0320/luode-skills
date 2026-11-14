#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""04 AI 视频分镜确定性自检器

把 `references/04-ai-video-storyboard.md` 第 3 节「分镜硬规则」与第 9 节
「快速自检」里可机械核对的部分变成可跑检查：11 必填字段是否齐全、字段是否留空、
运镜是否写了摄影机行为、光影是否只写空话、限制是否双向、下一段衔接是否为空、
是否把硬时间码混进分镜正文。

用法：
    python scripts/check_storyboard_output.py --file 分镜.md
    python scripts/check_storyboard_output.py --file 分镜.md --json

退出码：0 无 ERROR；1 存在 ERROR；2 文件或参数问题。

检查项：
    E1 某个分镜缺少 11 必填字段中的若干项
    E2 `台词与语气` 留空且该镜含对白标记（`台词：` 或引号台词）
    E3 `下一段衔接` 留空
    E4 `限制` 只写单向（只有「保持」或只有「禁止」）
    W1 `运镜` 未写摄影机行为要素（距离/高度/方向/速度/稳定/起止）
    W2 `光影` 只写空话（电影感 / 高级光影 / 氛围感），无光源与方向
    W3 `下一段衔接` 写成管理话术（接下一大分镜 / 接下一段 / 接分镜）
    W4 分镜正文出现硬时间码（00:03 / 第3秒 / 3s）或绝对秒数切片
    E5 未找到任何分镜（缺少 11 字段块）

零第三方依赖，仅标准库；纯静态检查，不调模型。
"""

import argparse
import json
import re
import sys

FIELDS = [
    "焦段",
    "光圈",
    "景深与焦点锁",
    "机位",
    "构图",
    "运镜",
    "主体动作/表情",
    "台词与语气",
    "光影",
    "限制",
    "下一段衔接",
]

CAMERA_KEYS = ["距离", "高度", "方向", "速度", "稳定", "起止", "位置", "固定", "推", "拉", "摇", "移", "跟", "升", "降"]

LIGHT_KEYS = ["光源", "主光", "方向", "亮区", "暗区", "受光", "轮廓光", "色温", "反差", "照度", "窗", "灯"]

LIGHT_EMPTY = ["电影感", "高级光影", "氛围感", "有质感", "很带感"]

MANAGEMENT = ["接下一大分镜", "接下一段", "承接下一段", "接分镜", "见下段"]

TIME_CODE = re.compile(r"(?<!\d)\d{1,2}:\d{2}(?!\d)|第\s*\d+\s*秒|(?<!\d)\d+(?:\.\d+)?\s*s(?:ec)?\b")

FIELD_LINE = re.compile(
    r"^\s*[-*]?\s*(焦段|光圈|景深与焦点锁|机位|构图|运镜|主体动作/表情|台词与语气|光影|限制|下一段衔接)\s*[:：]\s*(.*)$"
)


def read_text(path):
    """读取 UTF-8 文本，兼容 BOM。"""
    with open(path, "r", encoding="utf-8-sig") as handle:
        return handle.read()


def issue(level, code, message):
    """构造一条检查结论。"""
    return {"level": level, "code": code, "message": message}


def split_shots(lines):
    """按字段出现顺序切分镜：每遇到「焦段」开启一个新分镜。"""
    shots = []
    current = None
    for raw in lines:
        match = FIELD_LINE.match(raw)
        if not match:
            continue
        name, value = match.group(1), match.group(2).strip()
        if name == "焦段":
            current = {}
            shots.append(current)
        if current is None:
            current = {}
            shots.append(current)
        current[name] = value
    return shots


def check_missing(shots):
    """E1：11 必填字段齐全性。"""
    problems = []
    for index, shot in enumerate(shots, 1):
        missing = [name for name in FIELDS if name not in shot]
        if missing:
            problems.append(
                issue("ERROR", "E1", "第 %d 个分镜缺少字段 %s" % (index, "、".join(missing)))
            )
    return problems


def check_dialogue(shot, index):
    """E2：有对白却没有台词与语气。"""
    value = shot.get("台词与语气", "")
    if value.strip():
        return []
    pool = " ".join(shot.values())
    if "台词" in pool or "“" in pool or '"' in pool:
        return [issue("ERROR", "E2", "第 %d 个分镜有对白痕迹但「台词与语气」为空" % index)]
    return []


def check_gaps(shot, index):
    """E3：下一段衔接不得留空。"""
    value = shot.get("下一段衔接", "")
    if value.strip():
        return []
    return [issue("ERROR", "E3", "第 %d 个分镜「下一段衔接」为空" % index)]


def check_limit(shot, index):
    """E4：限制必须双向。"""
    value = shot.get("限制", "")
    if not value.strip():
        return []
    keep = any(word in value for word in ["保持", "保留", "维持"])
    forbid = any(word in value for word in ["禁止", "不允许", "不要", "不得"])
    if keep and forbid:
        return []
    return [
        issue(
            "ERROR",
            "E4",
            "第 %d 个分镜「限制」只写单向：必须同时写清保持什么、禁止什么" % index,
        )
    ]


def check_camera(shot, index):
    """W1：运镜要写摄影机行为。"""
    value = shot.get("运镜", "")
    if not value.strip():
        return []
    if any(key in value for key in CAMERA_KEYS):
        return []
    return [
        issue(
            "WARN",
            "W1",
            "第 %d 个分镜「运镜」未写摄影机行为要素（位置/距离/高度/方向/速度/稳定/起止）"
            % index,
        )
    ]


def check_light(shot, index):
    """W2：光影要可执行。"""
    value = shot.get("光影", "")
    if not value.strip():
        return []
    if any(key in value for key in LIGHT_KEYS):
        return []
    hit = [word for word in LIGHT_EMPTY if word in value]
    if hit:
        return [
            issue(
                "WARN",
                "W2",
                "第 %d 个分镜「光影」只有空话 %s：要写光源、主光方向、亮暗区、色温与反差"
                % (index, "、".join(hit)),
            )
        ]
    return []


def check_link_words(shot, index):
    """W3：衔接写管理话术。"""
    value = shot.get("下一段衔接", "")
    hit = [phrase for phrase in MANAGEMENT if phrase in value]
    if not hit:
        return []
    return [
        issue(
            "WARN",
            "W3",
            "第 %d 个分镜「下一段衔接」写了管理话术 %s：要写可继承的姿态、视线、道具、光线与镜头方向"
            % (index, "、".join(hit)),
        )
    ]


def check_timecode(text):
    """W4：硬时间码不该进分镜正文。"""
    hits = sorted({match.group(0).strip() for match in TIME_CODE.finditer(text)})
    if not hits:
        return []
    return [
        issue(
            "WARN",
            "W4",
            "正文出现硬时间码 %s：分镜用节奏档位与镜头密度表达时长，不写绝对秒数切片"
            % "、".join(hits[:6]),
        )
    ]


def run_checks(text):
    """跑全部检查，返回问题清单与分镜数量。"""
    lines = text.splitlines()
    shots = split_shots(lines)
    if not shots:
        return [issue("ERROR", "E5", "未找到分镜：每个分镜必须以「焦段：」开头并带 11 必填字段")], 0
    problems = list(check_missing(shots))
    for index, shot in enumerate(shots, 1):
        problems.extend(check_dialogue(shot, index))
        problems.extend(check_gaps(shot, index))
        problems.extend(check_limit(shot, index))
        problems.extend(check_camera(shot, index))
        problems.extend(check_light(shot, index))
        problems.extend(check_link_words(shot, index))
    problems.extend(check_timecode(text))
    return problems, len(shots)


def render(path, problems, count):
    """人读版报告。"""
    errors = [item for item in problems if item["level"] == "ERROR"]
    warns = [item for item in problems if item["level"] == "WARN"]
    print("=" * 72)
    print("04 AI 视频分镜自检：%s" % path)
    print("=" * 72)
    print("识别分镜数：%d" % count)
    print("结论：ERROR %d 条 / WARN %d 条" % (len(errors), len(warns)))
    for item in errors + warns:
        print("  [%s/%s] %s" % (item["code"], item["level"], item["message"]))
    if not problems:
        print("  PASS：11 字段齐全，台词/衔接/限制/运镜/光影/时间码全部通过。")
    return 0 if not errors else 1


def main():
    """命令行入口。"""
    parser = argparse.ArgumentParser(description="04 AI 视频分镜确定性自检器")
    parser.add_argument("--file", required=True, metavar="FILE", help="待检查的分镜 Markdown")
    parser.add_argument("--json", action="store_true", help="输出 JSON")
    args = parser.parse_args()
    try:
        text = read_text(args.file)
    except OSError as error:
        print("[X] 读取失败：%s" % error)
        return 2
    problems, count = run_checks(text)
    if args.json:
        payload = {"file": args.file, "shots": count, "issues": problems}
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 0 if not any(item["level"] == "ERROR" for item in problems) else 1
    return render(args.file, problems, count)


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    sys.exit(main())
