"""Catalog 结构、唯一性与禁止位置测试。"""

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
CATALOG = ROOT / "package-structure-rules" / "references" / "placement-catalog.yaml"
SCHEMA = ROOT / "package-structure-rules" / "references" / "placement-catalog.schema.json"


class CatalogSchemaTests(unittest.TestCase):
    """验证 JSON 兼容 YAML 的最小结构与关键唯一条目。"""

    def setUp(self):
        """加载每个用例共享的 Catalog 数据。

        [参数] self：unittest 测试实例。
        [返回] 无。
        最近修改时间: 2026-07-29 00:25:50 同时加载 Catalog 与收敛清单 Schema。
        """
        # 1. 每个用例从磁盘读取最新事实源，避免共享可变数据掩盖结构漂移。
        self.catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
        self.schema = json.loads(SCHEMA.read_text(encoding="utf-8"))

    def test_required_top_level_fields_exist(self):
        """确认 Catalog 仍保留查询和检查所需的顶层字段。

        [参数] self：unittest 测试实例。
        [返回] 无。
        最近修改时间: 2026-07-29 00:25:50 将 adoption 清单元数据纳入顶层结构断言。
        """
        # 1. 逐项确认 CLI 依赖的顶层字段没有在目录调整中丢失。
        for field in (
            "version", "owner_skill", "project_kinds", "forbidden_paths", "allowed_children", "adoption_manifest", "entries", "skeletons",
        ):
            self.assertIn(field, self.catalog)

    def test_adoption_manifest_contract_is_declared_in_catalog_and_schema(self):
        """确认旧项目收敛清单的字段、路径和后端语言约束已经冻结。

        [参数] self：unittest 测试实例。
        [返回] 无。
        最近修改时间: 2026-07-29 00:00:00 新增渐进采纳清单契约的静态回归断言。
        """
        # 1. Catalog 元数据必须声明清单版本、必填字段和禁止目录边界。
        rules = self.catalog["adoption_manifest"]
        self.assertEqual(1, rules["version"])
        self.assertEqual(
            ["version", "project_kind", "adopted_paths", "legacy_source_roots"], rules["required_fields"]["manifest"],
        )
        self.assertEqual(["language"], rules["required_fields"]["backend"])
        self.assertTrue(rules["path_rules"]["relative_only"])
        self.assertTrue(rules["path_rules"]["forbid_parent_segments"])
        self.assertTrue(rules["path_rules"]["adopted_paths_must_not_match_catalog_forbidden_paths"])

        # 2. JSON Schema 必须定义相同的结构、路径唯一性和后端语言条件。
        manifest = self.schema["$defs"]["adoption_manifest"]
        self.assertEqual(
            ["version", "project_kind", "adopted_paths", "legacy_source_roots"], manifest["required"],
        )
        self.assertTrue(manifest["properties"]["adopted_paths"]["uniqueItems"])
        self.assertTrue(manifest["properties"]["legacy_source_roots"]["uniqueItems"])
        self.assertEqual(["language"], manifest["allOf"][0]["then"]["required"])
        self.assertIn("\\.\\.", self.schema["$defs"]["relative_path"]["pattern"])

    def test_migration_and_discovery_entries_are_unique(self):
        """确认自动迁移和服务发现条目仍保持唯一。

        [参数] self：unittest 测试实例。
        [返回] 无。
        最近修改时间: 2026-07-28 22:40:00 为唯一性断言补齐用例说明。
        """
        # 1. 先验证 ID 唯一，再验证迁移路径没有重复条目。
        entries = self.catalog["entries"]
        ids = [entry["id"] for entry in entries]
        self.assertEqual(len(ids), len(set(ids)))
        paths = {entry["canonical_path"] for entry in entries if entry["artifact_kind"] == "database_migration"}
        self.assertEqual(8, len(paths))

    def test_legacy_adoption_example_has_a_unique_catalog_entry(self):
        """确认收敛清单示例引用的数据库仓储目录可被唯一定位。

        [参数] self：unittest 测试实例。
        [返回] 无。
        最近修改时间: 2026-07-29 00:10:00 补齐渐进采纳示例的实际 Catalog 入口。
        """
        # 1. 收敛清单不能引用未登记的 V2 目录，否则无法安全原地采纳。
        entries = [entry for entry in self.catalog["entries"] if entry["id"] == "backend.database.repository"]
        self.assertEqual(1, len(entries))
        self.assertEqual("database/repository", entries[0]["canonical_path"])

    def test_removed_paths_remain_forbidden(self):
        """确认根旧 util 与已删除的根 utils 子路径持续被拒绝。

        [参数] self 为 unittest 测试实例。
        [返回] 无。
        最近修改时间: 2026-07-28 21:45:00 适配后端根 utils 与源码根 util 分流。
        """
        # 1. 从 Catalog 的禁止路径集合逐项确认删除目录不会重新被允许。
        forbidden = set(self.catalog["forbidden_paths"])
        for path in ("util", "utils/graphql", "utils/asyncapi", "utils/avro", "utils/api/http", "common/event", "schema", "protocol"):
            self.assertIn(path, forbidden)

    def test_source_util_entries_cover_each_backend_language(self):
        """确认源码根 util 为四种后端语言分别保留唯一 Catalog 条目。

        [参数] self 为 unittest 测试实例。
        [返回] 无。
        最近修改时间: 2026-07-28 21:45:00 新增 source-util 四语言唯一性验证。
        """
        # 1. 筛选 source-util 条目后核对语言集合和条目数量。
        entries = [entry for entry in self.catalog["entries"] if entry["artifact_kind"] == "source-util"]
        self.assertEqual({"go", "java", "node", "python"}, {entry["language"] for entry in entries})
        self.assertEqual(4, len(entries))

    def test_business_rpc_entry_has_one_logical_path(self):
        """确认微业务 RPC 条目声明唯一逻辑目录和业务域占位要求。

        [参数] self：unittest 测试实例。
        [返回] 无。
        最近修改时间: 2026-07-28 23:55:00 新增跨微业务 RPC Catalog 结构断言。
        """
        # 1. RPC 的语言源码根由运行上下文解析，但 Catalog 只能有一个逻辑条目。
        entries = [entry for entry in self.catalog["entries"] if entry["artifact_kind"] == "business-rpc"]
        self.assertEqual(1, len(entries))
        self.assertEqual("<source-root>/business/<domain>/rpc", entries[0]["canonical_path"])
        self.assertTrue(entries[0]["requires_domain"])
        self.assertTrue(entries[0]["flat_files"])


if __name__ == "__main__":
    unittest.main()
