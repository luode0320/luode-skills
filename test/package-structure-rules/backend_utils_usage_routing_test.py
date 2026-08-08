"""验证 package-structure-rules 目录用法索引模块。

覆盖 guide 子命令查询、Catalog 一致性、recipe 样本验证。"""

from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CLI = ROOT / "package-structure-rules" / "scripts" / "placement_catalog.py"
CATALOG = ROOT / "package-structure-rules" / "references" / "placement-catalog.yaml"
LAYOUT = ROOT / "package-structure-rules" / "references" / "backend-util-layout.md"


def run_cli(*arguments: str) -> subprocess.CompletedProcess[str]:
    """调用本地 Catalog CLI。

    [参数] arguments：CLI 子命令及参数。
    [返回] subprocess.CompletedProcess[str]：本地命令结果。
    """
    return subprocess.run(
        [sys.executable, "-X", "utf8", str(CLI), *arguments],
        cwd=ROOT,
        text=True,
        encoding="utf-8",
        capture_output=True,
        check=False,
    )


class BackendUtilsUsageRoutingTests(unittest.TestCase):
    """覆盖 guide 子命令查询、Catalog 一致性、recipe 样本验证。"""

    def test_guide_returns_time_util_recipe(self):
        """guide --category time --language go 返回 timeUtil 别名。

        [参数] self：测试实例。
        [返回] None：断言失败时由 unittest 报告。
        """
        # 1. 查询 time 类别的 guide，校验返回包含 timeUtil 别名。
        result = run_cli("guide", "--category", "time", "--language", "go")
        self.assertEqual(0, result.returncode, result.stdout)
        data = json.loads(result.stdout)
        self.assertTrue(data["ok"])
        self.assertGreaterEqual(len(data["usage"]), 1)
        time_entry = [e for e in data["usage"] if e["canonical_path"] == "utils/time"]
        self.assertEqual(1, len(time_entry), "应有唯一 utils/time 条目")
        self.assertEqual("timeUtil", time_entry[0]["package_alias"])
        self.assertIn("time-util-rules", time_entry[0]["related_skills"])
        self.assertIn("usage-recipes-go.md#time", time_entry[0]["usage_recipes"])

    def test_guide_returns_conversion_recipe(self):
        """guide --category conversion --language go 返回 utils/convert 目录。

        [参数] self：测试实例。
        [返回] None：断言失败时由 unittest 报告。
        """
        # 1. 查询 conversion 类别，校验返回 utils/convert 条目的 purpose。
        result = run_cli("guide", "--category", "conversion", "--language", "go")
        self.assertEqual(0, result.returncode, result.stdout)
        data = json.loads(result.stdout)
        self.assertTrue(data["ok"])
        convert_entry = [e for e in data["usage"] if e["canonical_path"] == "utils/convert"]
        self.assertEqual(1, len(convert_entry), "应有唯一 utils/convert 条目")
        self.assertIn("转换", convert_entry[0]["purpose"])

    def test_guide_returns_cache_redis_recipe(self):
        """guide --category cache --technology redis --language go 返回 utils/cache/redis。

        [参数] self：测试实例。
        [返回] None：断言失败时由 unittest 报告。
        """
        # 1. 查询 cache/redis 类别，校验返回 utils/cache/redis。
        result = run_cli("guide", "--category", "cache", "--technology", "redis", "--language", "go")
        self.assertEqual(0, result.returncode, result.stdout)
        data = json.loads(result.stdout)
        self.assertTrue(data["ok"])
        self.assertEqual(1, len(data["usage"]))
        self.assertEqual("utils/cache/redis", data["usage"][0]["canonical_path"])

    def test_guide_all_util_entries_have_related_skills(self):
        """所有 backend.utils.* 条目均已标注 related_skills。

        [参数] self：测试实例。
        [返回] None：断言失败时由 unittest 报告。
        """
        # 1. 加载 Catalog 并检查所有 utils 条目都有 related_skills。
        catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
        utils_entries = [e for e in catalog["entries"] if e.get("artifact_kind") == "utils"]
        missing = [e["id"] for e in utils_entries if not e.get("related_skills")]
        self.assertEqual([], missing, f"以下 utils 条目缺少 related_skills: {missing}")

    def test_backend_util_layout_consistency(self):
        """backend-util-layout.md 中每个工具目录在 Catalog 中都有对应条目。

        [参数] self：测试实例。
        [返回] None：断言失败时由 unittest 报告。
        """
        # 1. 从 backend-util-layout.md 提取工具目录名，与 Catalog 条目的 canonical_path 比对。
        layout = LAYOUT.read_text(encoding="utf-8")
        catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
        catalog_paths = {e["canonical_path"] for e in catalog["entries"] if e.get("artifact_kind") == "utils"}
        # 2. 从 layout 的表格中提取 utils/ 目录路径
        layout_utils = set()
        for line in layout.split("\n"):
            if "`utils/" in line and "|" in line:
                import re
                for m in re.finditer(r"`(utils/[^`]+)`", line):
                    layout_utils.add(m.group(1).rstrip("/"))
        # 3. 每一个 layout 中的 utils/ 目录在 Catalog 中至少有一个匹配条目
        # 3. 过滤掉通配符路径（含 < 或 *），只检查具体目录名
        unmatched = [p for p in sorted(layout_utils) if p not in catalog_paths and "*" not in p and "<" not in p]
        self.assertEqual([], unmatched, f"以下 layout 目录在 Catalog 中无匹配: {unmatched}")


if __name__ == "__main__":
    unittest.main()
