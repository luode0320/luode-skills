"""CLI query 与 render 真实行为测试。"""

import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
CLI = ROOT / "package-structure-rules" / "scripts" / "placement_catalog.py"


def run(*args):
    """调用本地 CLI 并返回不抛异常的进程结果。

    [参数] args：传递给 CLI 的子命令参数。
    [返回] CompletedProcess：包含退出码、标准输出和标准错误。
    最近修改时间: 2026-07-28 22:40:00 明确查询与渲染测试共享的本地执行入口。
    """
    return subprocess.run([sys.executable, str(CLI), *args], cwd=ROOT, text=True, encoding="utf-8", capture_output=True, check=False)


class QueryRenderTests(unittest.TestCase):
    def test_discovery_technology_has_unique_path(self):
        """确认服务发现工具只由根 utils 返回唯一目录。

        [参数] self 为 unittest 测试实例。
        [返回] 无。
        最近修改时间: 2026-07-28 21:45:00 根工具查询名称由 util 更新为 utils。
        """
        # 1. 对两个服务发现技术逐一查询并比较其唯一规范路径。
        for technology, path in (("polaris", "utils/discovery/polaris"), ("nacos", "utils/discovery/nacos")):
            result = run("query", "--artifact", "utils", "--category", "discovery", "--technology", technology)
            self.assertEqual(0, result.returncode, result.stderr)
            self.assertEqual(path, json.loads(result.stdout)["entry"]["canonical_path"])

    def test_ip_package_has_unique_path(self):
        """确认 IP 技术工具包只由根 utils 返回唯一目录。

        [参数] self 为 unittest 测试实例。
        [返回] 无。
        最近修改时间: 2026-07-29 00:00:00 新增 IP 地址工具包的唯一查询断言。
        """
        # 1. 查询 IP 工具包，避免请求地址处理被误归入业务层或源码根 util。
        result = run("query", "--artifact", "utils", "--category", "ip")
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertEqual("utils/ip", json.loads(result.stdout)["entry"]["canonical_path"])

    def test_source_util_language_has_unique_path(self):
        """确认 source-util 按语言返回唯一的源码根工具函数目录。

        [参数] self 为 unittest 测试实例。
        [返回] 无。
        最近修改时间: 2026-07-28 21:45:00 新增 Go、Java、Node.js 与 Python 映射验证。
        """
        # 1. 定义四种语言各自的源码根工具函数目录并逐一查询。
        expected = {
            "go": "internal/util",
            "java": "src/main/java/<base-package>/util",
            "node": "src/util",
            "python": "src/<package>/util",
        }
        for language, path in expected.items():
            result = run("query", "--artifact", "source-util", "--language", language)
            self.assertEqual(0, result.returncode, result.stderr)
            self.assertEqual(path, json.loads(result.stdout)["entry"]["canonical_path"])

        # 2. 旧 artifact 不能作为兼容查询被悄悄接受。
        removed = run("query", "--artifact", "util", "--category", "discovery", "--technology", "polaris")
        self.assertEqual(2, removed.returncode)

    def test_backend_governance_file_has_unique_path(self):
        """确认后端根 AGENTS 文件可由 Catalog 唯一查询。

        [参数] self：unittest 测试实例。
        [返回] 无。
        最近修改时间: 2026-07-29 23:00:00 新增根治理文件查询断言。
        """
        # 1. 通过 artifact 与 category 精确查询，避免文件位置回退到源码根或 doc。
        result = run("query", "--artifact", "project-governance", "--category", "agents")
        self.assertEqual(0, result.returncode, result.stderr)
        entry = json.loads(result.stdout)["entry"]
        self.assertEqual("AGENTS.md", entry["canonical_path"])
        self.assertEqual("file", entry["node_kind"])

    def test_claude_governance_file_has_unique_path_for_each_project_kind(self):
        """确认三类项目的 Claude 规则文件都可由 Catalog 唯一查询。

        [参数] self：unittest 测试实例。
        [返回] 无。
        最近修改时间: 2026-07-29 23:45:00 新增三类项目根 CLAUDE.md 查询断言。
        """
        # 1. 按项目类型查询 Claude 规则文件，确认不会回退为后端默认条目。
        for project_kind in ("fullstack", "backend", "frontend"):
            result = run(
                "query", "--project-kind", project_kind, "--artifact", "project-governance", "--category", "claude",
            )
            self.assertEqual(0, result.returncode, result.stderr)
            entry = json.loads(result.stdout)["entry"]
            self.assertEqual("CLAUDE.md", entry["canonical_path"])
            self.assertEqual("AGENTS.md", entry["content_must_match"])

    def test_migration_operation_has_unique_path(self):
        """确认原有自动迁移查询没有被工具目录调整破坏。

        [参数] self：unittest 测试实例。
        [返回] 无。
        最近修改时间: 2026-07-28 22:40:00 保留跨规则变更的迁移路径回归断言。
        """
        # 1. 查询字段创建迁移条目，确认非工具类 Catalog 条目仍唯一。
        result = run("query", "--artifact", "database_migration", "--category", "field", "--operation", "create")
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertEqual("database/migration/field/create", json.loads(result.stdout)["entry"]["canonical_path"])

    def test_storage_connection_models_and_field_sql_have_unique_paths(self):
        """确认数据存储连接、模型和字段 SQL 均可由 CLI 唯一查询。

        [参数] self：unittest 测试实例。
        [返回] 无。
        最近修改时间: 2026-07-31 22:16:49 新增数据存储目录查询断言。
        """
        # 1. 逐项调用公开 query，避免 Catalog 新增条目只可静态读取而无法通过 CLI 使用。
        cases = (
            (("database_connection", None, None), "database/connection"),
            (("database_model", "db", None), "database/model/db"),
            (("database_model", "redis", None), "database/model/redis"),
            (("database_model", "mongo", None), "database/model/mongo"),
            (("database_sql", "field", "create"), "database/sql/field/create"),
            (("database_sql", "field", "update"), "database/sql/field/update"),
            (("database_sql", "field", "delete"), "database/sql/field/delete"),
        )
        for (artifact, category, operation), expected_path in cases:
            arguments = ["query", "--artifact", artifact]
            if category is not None:
                arguments.extend(("--category", category))
            if operation is not None:
                arguments.extend(("--operation", operation))
            result = run(*arguments)
            self.assertEqual(0, result.returncode, result.stderr)
            self.assertEqual(expected_path, json.loads(result.stdout)["entry"]["canonical_path"])

    def test_documented_database_artifact_aliases_have_unique_paths(self):
        """确认公开文档的 database 连字符 artifact 名称可以直接查询。

        [参数] self：unittest 测试实例。
        [返回] 无。
        最近修改时间: 2026-07-31 22:16:49 修复公开示例与 Catalog 内部 artifact 名称不一致。
        """
        # 1. 使用文档对外公开的名称，避免调用方需要了解 Catalog 内部下划线字段。
        cases = (
            (("database-connection", None, None), "database/connection"),
            (("database-sql", "field", "delete"), "database/sql/field/delete"),
            (("database-migration", "field", "create"), "database/migration/field/create"),
        )
        for (artifact, category, operation), expected_path in cases:
            arguments = ["query", "--artifact", artifact]
            if category is not None:
                arguments.extend(("--category", category))
            if operation is not None:
                arguments.extend(("--operation", operation))
            result = run(*arguments)
            self.assertEqual(0, result.returncode, result.stderr)
            self.assertEqual(expected_path, json.loads(result.stdout)["entry"]["canonical_path"])

    def test_business_rpc_has_unique_logical_path(self):
        """确认业务域 RPC 查询只返回一个带源码根和业务域占位的目录。

        [参数] self：unittest 测试实例。
        [返回] 无。
        最近修改时间: 2026-07-28 23:55:00 新增跨业务公开入口查询断言。
        """
        # 1. 目录解析留给 init 的语言上下文，query 必须稳定返回唯一规范路径。
        result = run("query", "--artifact", "business-rpc")
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertEqual("<source-root>/business/<domain>/rpc", json.loads(result.stdout)["entry"]["canonical_path"])

    def test_removed_backend_data_has_no_catalog_path_or_tree_node(self):
        """确认后端根 data 既不可查询，也不会被完整树渲染。

        [参数] self：unittest 测试实例。
        [返回] 无。
        最近修改时间: 2026-07-31 删除后端无职责静态数据根目录。
        """
        # 1. 根 data 已被删除，Catalog 不得为它保留兼容条目。
        query = run("query", "--artifact", "data")
        self.assertEqual(2, query.returncode)

        # 2. 前端和文档仍可拥有自己的 data 目录，故仅断言后端完整树不再包含根节点。
        backend = run("render", "--project-kind", "backend")
        self.assertEqual(0, backend.returncode, backend.stderr)
        self.assertNotIn("├── data/", backend.stdout)

    def test_render_all_is_complete_and_annotated(self):
        """确认完整树同时展示根 utils 与源码根 util 的不同职责。

        [参数] self 为 unittest 测试实例。
        [返回] 无。
        最近修改时间: 2026-07-29 23:45:00 增加双平台规则文件与根治理文件的渲染断言。
        """
        # 1. 渲染全部项目树，并核对关键节点和创建策略注释。
        result = run("render", "--all")
        self.assertEqual(0, result.returncode, result.stderr)
        for value in ("<fullstack-workspace>/", "<backend-project>/", "<frontend-project>/", "database/", "数据存储模型分类根", "新增字段 `.sql` 文件", "utils/", "ip/", "请求 IP 提取、标准化、公私网判断与地址归属查询工具", "源码根 util", "polaris/", "nacos/", "security-headers/", "mocks/", "业务公开的 JSON 字符串通信函数", "AGENTS.md", "CLAUDE.md", "正文与 AGENTS.md 一致", "PROJECT_CURRENT.md", "PROJECT_STYLE.md", "[必需·提交]"):
            self.assertIn(value, result.stdout)


if __name__ == "__main__":
    unittest.main()
