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

    def test_render_all_is_complete_and_annotated(self):
        """确认完整树同时展示根 utils 与源码根 util 的不同职责。

        [参数] self 为 unittest 测试实例。
        [返回] 无。
        最近修改时间: 2026-07-28 21:45:00 新增两个工具目录的渲染断言。
        """
        # 1. 渲染全部项目树，并核对关键节点和创建策略注释。
        result = run("render", "--all")
        self.assertEqual(0, result.returncode, result.stderr)
        for value in ("<fullstack-workspace>/", "<backend-project>/", "<frontend-project>/", "utils/", "源码根 util", "polaris/", "nacos/", "security-headers/", "mocks/", "业务公开的 JSON 字符串通信函数", "[必需·提交]"):
            self.assertIn(value, result.stdout)


if __name__ == "__main__":
    unittest.main()
