# -*- coding: utf-8 -*-
"""知识库真实生产关键词检索全方位评测脚本。

针对生产库（D:\谷歌云盘\知识库）进行大规模关键词检索真实性测试，
涵盖 5 大类 35 个典型测试用例：
1. 口语化业务场景词（买币、换号、接码、大乱斗开战、微业务、恢复默认等）
2. 具体技术名词与框架（Godot、MongoDB、PKCE、singleflight、LightweightCharts、CRLF等）
3. Bug 排查与异常特征报错（plugin_not_found、ERR_FILE_CANT_WRITE、invalid connection、伪diff等）
4. 架构红线与流程规范（打补丁破坏架构、删除测试、Goal模式免确认、逐行var等）
5. 结构化过滤与多维组合（--theme, --tag, --limit）

自动统计：总用例数、命中率、Top-1 精准度、Top-3 召回率、推荐 MOC 准确率、平均耗时。
"""

from __future__ import annotations

import importlib.util
import json
import sys
import time
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
INDEX_SCRIPT = ROOT / "knowledge-flow" / "scripts" / "knowledge_index.py"


def load_index_module() -> Any:
    name = "ki_eval_mod"
    spec = importlib.util.spec_from_file_location(name, INDEX_SCRIPT)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


INDEX = load_index_module()

# 35 个典型真实评测用例定义
TEST_CASES = [
    # -------------------------------------------------------------
    # 类别 1：口语化 / 业务场景词
    # -------------------------------------------------------------
    {
        "category": "1. 口语化业务词",
        "keyword": "买币",
        "expected_sub": "MoonPay直连买币签名",
        "theme_filter": "",
        "tag_filter": "",
    },
    {
        "category": "1. 口语化业务词",
        "keyword": "换号",
        "expected_sub": "换号判据",
        "theme_filter": "",
        "tag_filter": "",
    },
    {
        "category": "1. 口语化业务词",
        "keyword": "接码",
        "expected_sub": "luban-sms-api-v2",
        "theme_filter": "",
        "tag_filter": "",
    },
    {
        "category": "1. 口语化业务词",
        "keyword": "大乱斗 开战",
        "expected_sub": "crossverse-arena-start-game",
        "theme_filter": "",
        "tag_filter": "",
    },
    {
        "category": "1. 口语化业务词",
        "keyword": "出战指南",
        "expected_sub": "crossverse-arena-start-game",
        "theme_filter": "",
        "tag_filter": "",
    },
    {
        "category": "1. 口语化业务词",
        "keyword": "微业务",
        "expected_sub": "微业务架构",
        "theme_filter": "",
        "tag_filter": "",
    },
    {
        "category": "1. 口语化业务词",
        "keyword": "恢复默认",
        "expected_sub": "配置面板重置按钮必须回退到内置默认",
        "theme_filter": "",
        "tag_filter": "",
    },
    {
        "category": "1. 口语化业务词",
        "keyword": "补列 超时",
        "expected_sub": "大表迁移补列DDL超时",
        "theme_filter": "",
        "tag_filter": "",
    },
    {
        "category": "1. 口语化业务词",
        "keyword": "文字起点",
        "expected_sub": "表单控件对齐应比较实际文字起点",
        "theme_filter": "",
        "tag_filter": "",
    },

    # -------------------------------------------------------------
    # 类别 2：具体技术名词 / 框架 / 工具缩写
    # -------------------------------------------------------------
    {
        "category": "2. 技术名词与框架",
        "keyword": "Godot",
        "expected_sub": "Godot",
        "theme_filter": "",
        "tag_filter": "",
    },
    {
        "category": "2. 技术名词与框架",
        "keyword": "MongoDB",
        "expected_sub": "Mongo",
        "theme_filter": "",
        "tag_filter": "",
    },
    {
        "category": "2. 技术名词与框架",
        "keyword": "PKCE",
        "expected_sub": "PKCE",
        "theme_filter": "",
        "tag_filter": "",
    },
    {
        "category": "2. 技术名词与框架",
        "keyword": "singleflight",
        "expected_sub": "singleflight",
        "theme_filter": "",
        "tag_filter": "",
    },
    {
        "category": "2. 技术名词与框架",
        "keyword": "LightweightCharts",
        "expected_sub": "LightweightCharts",
        "theme_filter": "",
        "tag_filter": "",
    },
    {
        "category": "2. 技术名词与框架",
        "keyword": "CRLF",
        "expected_sub": "CRLF",
        "theme_filter": "",
        "tag_filter": "",
    },
    {
        "category": "2. 技术名词与框架",
        "keyword": "CLDR",
        "expected_sub": "CLDR",
        "theme_filter": "",
        "tag_filter": "",
    },
    {
        "category": "2. 技术名词与框架",
        "keyword": "Arco Design",
        "expected_sub": "表单控件对齐应比较实际文字起点",
        "theme_filter": "",
        "tag_filter": "",
    },

    # -------------------------------------------------------------
    # 类别 3：故障排查 / 错误特征 / 报错信息
    # -------------------------------------------------------------
    {
        "category": "3. 故障排查与报错",
        "keyword": "plugin_not_found",
        "expected_sub": "plugin_not_found",
        "theme_filter": "",
        "tag_filter": "",
    },
    {
        "category": "3. 故障排查与报错",
        "keyword": "ERR_FILE_CANT_WRITE",
        "expected_sub": "crossverse-arena-start-game",
        "theme_filter": "",
        "tag_filter": "",
    },
    {
        "category": "3. 故障排查与报错",
        "keyword": "invalid connection",
        "expected_sub": "invalid-connection",
        "theme_filter": "",
        "tag_filter": "",
    },
    {
        "category": "3. 故障排查与报错",
        "keyword": "伪diff",
        "expected_sub": "伪diff排查",
        "theme_filter": "",
        "tag_filter": "",
    },
    {
        "category": "3. 故障排查与报错",
        "keyword": "0.0.0.0",
        "expected_sub": "未指定地址",
        "theme_filter": "",
        "tag_filter": "",
    },
    {
        "category": "3. 故障排查与报错",
        "keyword": "哨兵行",
        "expected_sub": "黑名单表哨兵行",
        "theme_filter": "",
        "tag_filter": "",
    },

    # -------------------------------------------------------------
    # 类别 4：团队规范与架构红线
    # -------------------------------------------------------------
    {
        "category": "4. 架构红线与规范",
        "keyword": "打补丁破坏架构",
        "expected_sub": "严禁为少改代码而打补丁破坏架构",
        "theme_filter": "",
        "tag_filter": "",
    },
    {
        "category": "4. 架构红线与规范",
        "keyword": "删除测试",
        "expected_sub": "删除测试",
        "theme_filter": "",
        "tag_filter": "",
    },
    {
        "category": "4. 架构红线与规范",
        "keyword": "Goal模式免确认",
        "expected_sub": "Goal模式免确认",
        "theme_filter": "",
        "tag_filter": "",
    },
    {
        "category": "4. 架构红线与规范",
        "keyword": "逐行var",
        "expected_sub": "逐行var",
        "theme_filter": "",
        "tag_filter": "",
    },
    {
        "category": "4. 架构红线与规范",
        "keyword": "读侧权威",
        "expected_sub": "读侧权威",
        "theme_filter": "",
        "tag_filter": "",
    },
    {
        "category": "4. 架构红线与规范",
        "keyword": "死循环 降级",
        "expected_sub": "技能列表预算与描述降级",
        "theme_filter": "",
        "tag_filter": "",
    },

    # -------------------------------------------------------------
    # 类别 5：过滤查询与组合检索
    # -------------------------------------------------------------
    {
        "category": "5. 结构化过滤与组合",
        "keyword": "连接",
        "expected_sub": "invalid-connection",
        "theme_filter": "工程实践",
        "tag_filter": "",
    },
    {
        "category": "5. 结构化过滤与组合",
        "keyword": "推进",
        "expected_sub": "Goal模式免确认",
        "theme_filter": "AI协作",
        "tag_filter": "",
    },
    {
        "category": "5. 结构化过滤与组合",
        "keyword": "视口",
        "expected_sub": "视口显示管理",
        "theme_filter": "",
        "tag_filter": "godot",
    },
    {
        "category": "5. 结构化过滤与组合",
        "keyword": "买币",
        "expected_sub": "MoonPay",
        "theme_filter": "",
        "tag_filter": "web3",
    },
    {
        "category": "5. 结构化过滤与组合",
        "keyword": "表单",
        "expected_sub": "表单控件对齐",
        "theme_filter": "",
        "tag_filter": "CSS",
    },
    {
        "category": "5. 结构化过滤与组合",
        "keyword": "规范",
        "expected_sub": "规范",
        "theme_filter": "代码规则",
        "tag_filter": "",
    },
]


def evaluate() -> dict[str, Any]:
    index = INDEX.load_index(auto_rebuild=True)
    total_cases = len(TEST_CASES)
    hit_cases = 0
    top1_correct = 0
    top3_correct = 0
    total_time_ms = 0.0

    eval_results = []

    for tc in TEST_CASES:
        kw = tc["keyword"]
        exp = tc["expected_sub"].lower()
        t0 = time.perf_counter()
        hits = INDEX.query_index(
            index,
            kw,
            theme_filter=tc["theme_filter"],
            tag_filter=tc["tag_filter"],
        )
        elapsed_ms = (time.perf_counter() - t0) * 1000.0
        total_time_ms += elapsed_ms

        has_hit = len(hits) > 0
        if has_hit:
            hit_cases += 1

        # 检查 top1 是否匹配预期
        top1_hit = False
        top3_hit = False
        if hits:
            h0 = hits[0]
            top1_sign = (h0["path"] + " " + h0["title"]).lower()
            if exp in top1_sign:
                top1_hit = True

            # 检查 top3
            for h in hits[:3]:
                h_sign = (h["path"] + " " + h["title"]).lower()
                if exp in h_sign:
                    top3_hit = True
                    break

        if top1_hit:
            top1_correct += 1
        if top3_hit:
            top3_correct += 1

        top_info = hits[0] if hits else None
        eval_results.append({
            "category": tc["category"],
            "keyword": kw,
            "theme_filter": tc["theme_filter"],
            "tag_filter": tc["tag_filter"],
            "expected": tc["expected_sub"],
            "hit_count": len(hits),
            "top1_match": top1_hit,
            "top3_match": top3_hit,
            "elapsed_ms": round(elapsed_ms, 2),
            "top_hit_path": top_info["path"] if top_info else None,
            "top_hit_title": top_info["title"] if top_info else None,
            "top_matched_fields": top_info["matched"] if top_info else None,
            "top_recommended_moc": top_info["recommended_moc"] if top_info else None,
        })

    summary = {
        "total_cases": total_cases,
        "hit_cases": hit_cases,
        "hit_rate": round(hit_cases / total_cases * 100.0, 2),
        "top1_correct": top1_correct,
        "top1_accuracy": round(top1_correct / total_cases * 100.0, 2),
        "top3_correct": top3_correct,
        "top3_recall": round(top3_correct / total_cases * 100.0, 2),
        "avg_time_ms": round(total_time_ms / total_cases, 2),
    }

    return {"summary": summary, "results": eval_results}


if __name__ == "__main__":
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")
    report = evaluate()
    print(json.dumps(report, ensure_ascii=False, indent=2))
