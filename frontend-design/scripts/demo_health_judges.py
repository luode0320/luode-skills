"""示例页健康扫描的命中判定：控制台豁免面与告警过滤。

[职责] 只回答「量到的信号算不算命中、哪些可以豁免」，不含页内量测与流程编排。
[豁免] 控制台告警豁免面集中在 KNOWN_CONSOLE_ALLOW 一处定义，
  每条必须写明根因、归属与解除条件，禁止把「查不动」当豁免理由。
最近修改时间：2026-10-18 19:32:00；改动原因：6-review 发现 check_demo_health.py 379 行超 200 行基准，按 diamond 拆分，判据字节未改写。
"""

# 已知控制台告警豁免面：集中一处定义，每条写明根因、归属与解除条件。
# 上游 139 文件逐字节冻结，这类告警在本地没有干净修法——修它要么改冻结文件，
# 要么全局关掉 GSAP 的空目标诊断（会连带压掉今后真实的空选择器告警），两者都不划算。
KNOWN_CONSOLE_ALLOW = [
    {
        "match": "GSAP target [object NodeList] not found",
        "reason": "上游 src/composables/motion.ts 的 pageEnter 对 .bento 只给时间轴加了 cards.length 守卫，"
                  "gsap.set(cards, ...) 那一行没加；示例页没有 .bento 元素，空 NodeList 触发 GSAP 空目标告警。"
                  "属冻结面缺陷，上游修法是在 gsap.set(cards, ...) 外补 if (cards.length)；重新冻结上游后应移除本条。",
    },
]

def allowed(text: str) -> bool:
    """判断一条控制台文本是否落在已登记的豁免面里。

    [参数] text 控制台消息原文 [返回] 命中任一豁免条目的子串即返回 True。
    """
    return any(item["match"] in text for item in KNOWN_CONSOLE_ALLOW)

def judge_console(msgs: list[dict]) -> list[str]:
    """把控制台消息按判据 2 过滤成命中清单。

    [参数] msgs 每条形如 {type, text} [返回] 未豁免的告警与错误描述列表。
    """
    hits = []
    for m in msgs:
        text = m.get("text", "")
        if allowed(text):
            continue
        if m.get("type") == "error":
            hits.append(f"console.error: {text[:160]}")
        elif m.get("type") == "warning" and ("[Vue warn]" in text or "Invalid prop" in text):
            hits.append(f"Vue 告警: {text[:160]}")
    return hits
