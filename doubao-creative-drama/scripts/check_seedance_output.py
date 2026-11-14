#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Seedance 2.0 提示词包确定性自检器

把 SKILL.md「06 Seedance 2.0 适配」里的硬红线变成可跑检查，
避免字数、素材编号、平台参数和管理话术只能靠模型自己数。

用法：
    python scripts/check_seedance_output.py --file 提示词包.md
    python scripts/check_seedance_output.py --file 提示词包.md --json

退出码：0 无 ERROR；1 存在 ERROR；2 文件或参数问题。

检查项：
    E0 未找到代码框（纯净提示词必须放在 ``` 代码框内）
    E1 代码框纯净提示词字数 > 2000（硬上限）
    E2 全局控制写入了平台参数（画幅 / 时长 / 分辨率 / 生成模式）
    E3 镜头轨引用了素材锚定未定义的 @图片N
    E4 代码框内出现只给人看的管理话术（接下一大分镜 / 接下一段 / 接分镜）
    E5 单组图片参考去重后 > 9 张
    E6 缺少 C 模板必需段落
    W1 代码框字数 > 1900（默认目标）
    W2 代码框内出现 BGM / 背景音乐（BGM 归 07 后期）
    W3 代码框内出现否定式管理话术（未启用 / 无则删除 / 不使用 / 不继承 / 不替代）
    W4 镜头轨行不是五段格式
    W5 素材段定义了编号但代码框未使用

零第三方依赖，仅标准库；纯静态检查，不调模型。
"""

import argparse
import json
import re
import sys

MAX_HARD = 2000
MAX_SOFT = 1900
MAX_REFS = 9

REQUIRED_BLOCKS = [
    "特别注意",
    "素材锚定",
    "场景锚定",
    "镜头轨",
    "声音轨",
    "硬锁",
    "段末状态",
]

PLATFORM_TOKENS = [
    "9:16",
    "16:9",
    "1:1",
    "3:4",
    "4:3",
    "21:9",
    "1080p",
    "1080P",
    "720p",
    "480p",
    "4K",
    "参考生视频",
    "多模态参考",
    "图生视频",
    "文生视频",
]

MANAGEMENT_PHRASES = ["接下一大分镜", "接下一段", "承接下一段", "接分镜", "见上一段", "见下段"]

NEGATIVE_PHRASES = ["未启用", "无则删除", "不使用", "不继承", "不替代"]

REF_PATTERN = re.compile(r"@(?:图片|图像|图|image|Image)\s*([0-9]+)")

CODE_FENCE = re.compile(r"```[^\n]*\n(.*?)```", re.S)


def read_text(path):
    """读取 UTF-8 文本，去掉可能存在的 BOM。"""
    with open(path, "r", encoding="utf-8-sig") as handle:
        return handle.read()


def extract_code(text):
    """拼接全部代码框内容，作为「可投喂纯净提示词」的检查范围。"""
    blocks = CODE_FENCE.findall(text)
    return "\n".join(blocks).strip()


def issue(level, code, message):
    """构造一条检查结论。"""
    return {"level": level, "code": code, "message": message}


def check_budget(code):
    """E1 / W1：代码框字数上限。"""
    size = len(re.sub(r"\s", "", code))
    if size > MAX_HARD:
        return [
            issue(
                "ERROR",
                "E1",
                "代码框纯净提示词 %d 字，超过 %d 字硬上限，先删低收益后缀与重复字段，"
                "再按镜头边界拆单元" % (size, MAX_HARD),
            )
        ]
    if size > MAX_SOFT:
        return [
            issue(
                "WARN",
                "W1",
                "代码框纯净提示词 %d 字，超过默认目标 %d 字（硬上限 %d）"
                % (size, MAX_SOFT, MAX_HARD),
            )
        ]
    return []


def check_platform_params(code):
    """E2：全局控制只写画面与执行原则，不许写平台参数。"""
    hit = [token for token in PLATFORM_TOKENS if token in code]
    if not hit:
        return []
    return [
        issue(
            "ERROR",
            "E2",
            "代码框内出现平台参数 %s：画幅 / 分辨率 / 时长 / 生成模式一律只放代码框外"
            % "、".join(sorted(set(hit))),
        )
    ]


def check_management(code):
    """E4：代码框内不许出现只给人看的管理话术。"""
    hit = [phrase for phrase in MANAGEMENT_PHRASES if phrase in code]
    if not hit:
        return []
    return [
        issue(
            "ERROR",
            "E4",
            "代码框内出现管理话术 %s：衔接必须写成模型可生成的可见画面状态或动作转接"
            % "、".join(hit),
        )
    ]


def check_negative(code):
    """W3：否定式管理话术，人工复核。"""
    hit = [phrase for phrase in NEGATIVE_PHRASES if phrase in code]
    if not hit:
        return []
    return [
        issue(
            "WARN",
            "W3",
            "代码框内出现否定式话术 %s：确认它是画面级禁止项，而不是「本项未启用」这类说明"
            % "、".join(hit),
        )
    ]


def check_bgm(code):
    """W2：纯净提示词默认不生成 BGM。"""
    if not any(token in code for token in ["BGM", "bgm", "背景音乐"]):
        return []
    return [
        issue(
            "WARN",
            "W2",
            "代码框内出现 BGM 相关要求：06 默认只保留环境声 / 对白原声 / 同步音效，"
            "配乐交给 07 后期声音设计",
        )
    ]


def check_ref_count(code):
    """E5：单组图片参考最多 9 张。"""
    refs = sorted({int(number) for number in REF_PATTERN.findall(code)})
    if len(refs) <= MAX_REFS:
        return []
    return [
        issue(
            "ERROR",
            "E5",
            "单组引用 %d 个图片编号（%s），超过 %d 张上限：先筛选、合并、转文字或拆到下一组"
            % (len(refs), "、".join("@图%d" % number for number in refs), MAX_REFS),
        )
    ]


def split_shot_section(code):
    """取出「镜头轨」段落的字符区间；找不到返回 (0, 0)。"""
    lines = code.splitlines(keepends=True)
    offset = 0
    start = None
    end = None
    for line in lines:
        stripped = line.strip()
        if start is None and stripped.startswith("镜头轨"):
            start = offset + len(line)
        elif start is not None and (
            stripped.startswith("声音轨") or stripped.startswith("硬锁") or stripped.startswith("段末状态")
        ):
            end = offset
            break
        offset += len(line)
    if start is None:
        return 0, 0
    return start, (end if end is not None else len(code))


def check_ref_defined(text, code):
    """E3：镜头轨引用的编号必须已定义（素材锚定 / 参考-连续性声明 / 框外素材段）。

    定义位置两处都算：C 模板里位于 `镜头轨` 之前的 `素材锚定`、`参考/连续性声明`
    （在代码框内），以及 §6 普通段落里的「素材：…」写法（在代码框外）。
    """
    start, end = split_shot_section(code)
    shot_section = code[start:end] if end > start else code
    used = {int(number) for number in REF_PATTERN.findall(shot_section)}
    defined = {int(number) for number in REF_PATTERN.findall(CODE_FENCE.sub("\n", text) + "\n" + code[:start])}
    missing = sorted(used - defined)
    outside_refs = {int(number) for number in REF_PATTERN.findall(CODE_FENCE.sub("\n", text))}
    code_refs = {int(number) for number in REF_PATTERN.findall(code)}
    unused = sorted(outside_refs - code_refs)
    issues = []
    if missing:
        issues.append(
            issue(
                "ERROR",
                "E3",
                "镜头轨引用了未定义的编号 %s：编号必须先在 `素材锚定` 或"
                "`参考/连续性声明` 中定义" % "、".join("@图%d" % number for number in missing),
            )
        )
    if unused:
        issues.append(
            issue(
                "WARN",
                "W5",
                "素材段定义了但代码框未使用的编号 %s：确认是筛选后刻意不用，还是漏投喂"
                % "、".join("@图%d" % number for number in unused),
            )
        )
    return issues


def check_blocks(code):
    """E6：C 模板必需段落缺失检查（只看代码框内，段落写到框外等于没交付）。"""
    missing = [name for name in REQUIRED_BLOCKS if name not in code]
    if not missing:
        return []
    return [
        issue(
            "ERROR",
            "E6",
            "代码框内缺少 C 模板必需段落 %s（按需段：参考-连续性声明 / 风格锁定 可省）"
            % "、".join(missing),
        )
    ]


def check_shot_lines(code):
    """W4：镜头轨应为 `N｜标签｜镜头/焦点｜动作/台词｜光影/转接` 五段。"""
    bad = []
    for line in code.splitlines():
        stripped = line.strip()
        if "｜" not in stripped:
            continue
        if not re.match(r"^[0-9]+｜", stripped):
            continue
        if len(stripped.split("｜")) != 5:
            bad.append(stripped.split("｜")[0])
    if not bad:
        return []
    return [
        issue(
            "WARN",
            "W4",
            "镜头 %s 不是五段格式：应为 `N｜镜头功能标签｜镜头/焦点｜动作/台词｜光影/转接`"
            % "、".join(bad),
        )
    ]


def run_checks(text):
    """按顺序跑全部检查，返回问题清单。"""
    code = extract_code(text)
    issues = []
    if not code:
        issues.append(issue("ERROR", "E0", "未找到代码框：纯净提示词必须放在 ``` 代码框内"))
        return issues, 0
    issues.extend(check_budget(code))
    issues.extend(check_platform_params(code))
    issues.extend(check_management(code))
    issues.extend(check_negative(code))
    issues.extend(check_bgm(code))
    issues.extend(check_ref_count(code))
    issues.extend(check_ref_defined(text, code))
    issues.extend(check_blocks(code))
    issues.extend(check_shot_lines(code))
    return issues, len(re.sub(r"\s", "", code))


def render(path, issues, size):
    """人读版报告。"""
    errors = [item for item in issues if item["level"] == "ERROR"]
    warns = [item for item in issues if item["level"] == "WARN"]
    print("=" * 72)
    print("Seedance 2.0 提示词包自检：%s" % path)
    print("=" * 72)
    print("代码框纯净提示词字数：%d（默认目标 %d / 硬上限 %d）" % (size, MAX_SOFT, MAX_HARD))
    print("结论：ERROR %d 条 / WARN %d 条" % (len(errors), len(warns)))
    for item in errors + warns:
        print("  [%s/%s] %s" % (item["code"], item["level"], item["message"]))
    if not issues:
        print("  PASS：字数、平台参数、编号、管理话术、段落结构、镜头轨格式全部通过。")
    return 0 if not errors else 1


def main():
    """命令行入口。"""
    parser = argparse.ArgumentParser(description="Seedance 2.0 提示词包确定性自检器")
    parser.add_argument("--file", required=True, metavar="FILE", help="待检查的提示词包 Markdown")
    parser.add_argument("--json", action="store_true", help="输出 JSON")
    args = parser.parse_args()

    try:
        text = read_text(args.file)
    except OSError as error:
        print("[X] 读取失败：%s" % error)
        return 2

    issues, size = run_checks(text)
    if args.json:
        payload = {"file": args.file, "chars": size, "issues": issues}
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 0 if not any(item["level"] == "ERROR" for item in issues) else 1
    return render(args.file, issues, size)


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    sys.exit(main())
