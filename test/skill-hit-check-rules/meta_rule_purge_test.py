"""元规则清除与安全红线守卫。

2026-10-31 的 skill 体系中等重构删除了全部自我校验型元规则（五字段打卡、闸门预告、
并行线程台账、固定话术模板），并退役了投影 registry、记忆计数吸收与三个纯元规则 skill。
这些删除有一个共同风险：它们只把「要求 AI 证明自己守规矩」的文本删掉了，没有任何
行为会因此报错——一旦后来者从历史提交里把某个 skill 还原回来，或顺手把打卡字段
重新加进模板，流程链会在无人察觉的情况下重新变长。

本守卫把两类不可退让的事实钉成断言：
1. 元规则字面量与已删除的 skill 目录不得回归；
2. 六条安全红线必须在 `AGENTS.md` 与自举脚本常量里同时存在，且两份规则文件字节一致。

第 2 项是这次重构唯一不能出错的地方：删规则时把红线一起带走，比流程链过长严重得多。
"""

from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
AGENTS = ROOT / "AGENTS.md"
CLAUDE = ROOT / "CLAUDE.md"
BOOTSTRAP = ROOT / "context-recovery-rules" / "scripts" / "bootstrap_agents.sh"
GATE_REGISTRY = ROOT / "skill-hit-check-rules" / "references" / "deferred-gate-registry.md"
SEED_SUFFIX = "__skillhub"

# 已退役的元规则字面量。命中任一项说明自我校验机制被重新引入。
RETIRED_META_RULE_TOKENS = (
    "命中检查:通过",
    "命中检查：通过",
    "闸门预告",
    "并行技能:",
    "并行技能：",
    "usage_count",
    "absorbed_to",
    "probe-timeout",
    "UI_SYNC_BLOCKED",
    "TASK PLAN PROJECTION",
)

# 已删除的 skill 目录。它们的能力已被宿主原生机制或其他 owner 承接。
RETIRED_SKILL_DIRS = (
    "skill-audit-rules",
    "team-development-rules",
    "memory-usage-tracking-rules",
    "task-plan-rehydration-rules",
    "thread-title-rules",
    "code-context-resync-rules",
    "context-compression-rules",
    "recent-context-bootstrap-rules",
    "project-rule-file-bootstrap-rules",
    "skill-execution-compliance-gate-rules",
)

# 六条安全红线的锚点原文。任何一条从 AGENTS.md 消失即视为破坏了红线。
RED_LINE_ANCHORS = {
    "RED-1 本地连接调试": "local` 本地环境",
    "RED-2 测试不得污染生产代码": "完全禁止为了测试目的改动生产代码",
    "RED-3 跨项目写入": "会话级跨项目写入授权",
    "RED-4 严禁自动提交 Git": "绝对禁止在用户未于「当前这轮消息」显式提出提交",
    "RED-5 凭据不回显": "过程性输出中回显凭据原值",
    "RED-6 个人文件安全与删除保护": "个人文件安全与删除保护",
}


def active_skill_files() -> list[Path]:
    """收集仓库内自建（非第三方种子）的 SKILL.md。

    [参数] 无。
    [返回] list[Path]：按路径排序的活动 skill 入口文件。
    最近修改时间：2026-10-31；改动原因：为元规则清除建立常驻守卫。
    """
    return sorted(
        path
        for path in ROOT.glob("*/SKILL.md")
        if not path.parent.name.endswith(SEED_SUFFIX)
    )


class MetaRulePurgeTest(unittest.TestCase):
    """元规则组：打卡字面量与退役 skill 目录都不得回归。"""

    def test_no_retired_meta_rule_tokens_in_active_skills(self) -> None:
        """活动 SKILL.md 不得再出现任何已退役的打卡字面量。

        [参数] 无。
        [返回] None：断言失败时抛出 AssertionError。
        最近修改时间：2026-10-31；改动原因：为元规则清除建立常驻守卫。
        """
        offenders: list[str] = []
        for path in active_skill_files():
            text = path.read_text(encoding="utf-8")
            hits = [token for token in RETIRED_META_RULE_TOKENS if token in text]
            if hits:
                offenders.append(f"{path.relative_to(ROOT).as_posix()} -> {hits}")
        self.assertEqual(offenders, [], f"活动 skill 重新出现已退役的元规则：{offenders}")

    def test_retired_skill_directories_stay_removed(self) -> None:
        """已合并或删除的 skill 目录不得重新出现。

        [参数] 无。
        [返回] None：断言失败时抛出 AssertionError。
        最近修改时间：2026-10-31；改动原因：为元规则清除建立常驻守卫。
        """
        revived = [name for name in RETIRED_SKILL_DIRS if (ROOT / name).exists()]
        self.assertEqual(revived, [], f"已退役的 skill 目录重新出现：{revived}")

    def test_gate_registry_stays_a_timing_table(self) -> None:
        """延迟 gate 清单必须保持为一张简短时机表，不得回长成流程编排文档。

        [参数] 无。
        [返回] None：断言失败时抛出 AssertionError。
        最近修改时间：2026-10-31；改动原因：为元规则清除建立常驻守卫。
        """
        self.assertTrue(GATE_REGISTRY.is_file(), "延迟 gate 清单缺失")
        lines = GATE_REGISTRY.read_text(encoding="utf-8").splitlines()
        self.assertLessEqual(len(lines), 25, f"延迟 gate 清单回长到 {len(lines)} 行")

    def test_scan_scope_is_not_empty(self) -> None:
        """扫描范围不得为空，避免路径写错后守卫静默通过。

        [参数] 无。
        [返回] None：断言失败时抛出 AssertionError。
        最近修改时间：2026-10-31；改动原因：为元规则清除建立常驻守卫。
        """
        self.assertGreater(len(active_skill_files()), 100, "活动 skill 扫描范围异常")


class SafetyRedLineTest(unittest.TestCase):
    """红线组：六条安全红线必须在规则文件与自举脚本中同时存在。"""

    def test_red_lines_present_in_agents_rules(self) -> None:
        """六条安全红线的锚点原文必须仍在 AGENTS.md 中。

        [参数] 无。
        [返回] None：断言失败时抛出 AssertionError。
        最近修改时间：2026-10-31；改动原因：重构删规则后守住安全红线。
        """
        agents = AGENTS.read_text(encoding="utf-8")
        missing = [label for label, anchor in RED_LINE_ANCHORS.items() if anchor not in agents]
        self.assertEqual(missing, [], f"AGENTS.md 丢失安全红线：{missing}")

    def test_red_lines_present_in_bootstrap_source(self) -> None:
        """自举脚本常量必须同样守住红线，否则下次自举会把它们冲掉。

        [参数] 无。
        [返回] None：断言失败时抛出 AssertionError。
        最近修改时间：2026-10-31；改动原因：重构删规则后守住安全红线。
        """
        script = BOOTSTRAP.read_text(encoding="utf-8")
        missing = [label for label, anchor in RED_LINE_ANCHORS.items() if anchor not in script]
        self.assertEqual(missing, [], f"自举脚本丢失安全红线：{missing}")

    def test_rule_files_are_byte_identical(self) -> None:
        """AGENTS.md 与 CLAUDE.md 必须逐字节一致。

        [参数] 无。
        [返回] None：断言失败时抛出 AssertionError。
        最近修改时间：2026-10-31；改动原因：重构删规则后守住安全红线。
        """
        self.assertEqual(AGENTS.read_bytes(), CLAUDE.read_bytes(), "两份规则文件不一致")


if __name__ == "__main__":
    unittest.main()
