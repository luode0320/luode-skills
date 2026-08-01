"""共享静态 Owner 路由的本地契约测试。"""

from __future__ import annotations

from pathlib import Path
import sys
import unittest


SCRIPTS_DIR = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

from static_owner_router import (  # noqa: E402
    BASE_OWNER_NAMES,
    OWNER_NAMES,
    owner_source_map_path,
    route_owners,
)


class StaticOwnerRouterTests(unittest.TestCase):
    """验证共享 Owner 路由的顺序、条件和路径边界。"""

    def test_empty_changes_have_no_owner(self) -> None:
        """验证空变更不会产生静态 Owner。

        [参数] 无
        [返回] 无；断言失败时由 unittest 抛出异常。
        最近修改时间：2026-08-01 00:00:00；覆盖共享路由的空输入边界。
        """

        # 1. 空变更不能触发基础或条件 Owner。
        self.assertEqual(route_owners([]), [])

    def test_base_owner_order_is_stable(self) -> None:
        """验证基础 Owner 的顺序稳定且不重复。

        [参数] 无
        [返回] 无；断言失败时由 unittest 抛出异常。
        最近修改时间：2026-08-01 00:00:00；覆盖共享路由的基础结果契约。
        """

        # 1. 普通代码文件必须先得到固定基础 Owner 序列。
        owners = route_owners(["src/service/user.py"])
        self.assertEqual(owners[: len(BASE_OWNER_NAMES)], list(BASE_OWNER_NAMES))
        self.assertEqual(len(owners), len(set(owners)))

    def test_specialist_routing_matches_existing_monitor_semantics(self) -> None:
        """验证共享路由保留监控场景的专项 Owner 语义。

        [参数] 无
        [返回] 无；断言失败时由 unittest 抛出异常。
        最近修改时间：2026-08-01 00:00:00；覆盖数据库、Go、React 和测试资产路由。
        """

        # 1. 专项路径和信号必须附加对应 Owner 并保留既有先后关系。
        owners = route_owners(["db/migrations/001_user_schema.sql"], ["database-query"])
        self.assertLess(owners.index("database-schema-rules"), owners.index("database-query-rules"))
        self.assertIn("golang-patterns", route_owners(["cmd/app/main.go"]))
        self.assertIn("vercel-react-best-practices", route_owners(["src/App.tsx"]))
        self.assertIn("test-program-rules", route_owners(["tests/fixtures/user_stub.py"]))

    def test_frontend_signals_do_not_overroute(self) -> None:
        """验证前端语义信号不会过度路由无关 Owner。

        [参数] 无
        [返回] 无；断言失败时由 unittest 抛出异常。
        最近修改时间：2026-08-01 00:00:00；覆盖组件、视觉和路由信号的负向边界。
        """

        # 1. 组件与视觉信号各自只引入对应前端 Owner。
        computed = route_owners(["src/views/User.vue"], ["computed"])
        self.assertIn("vue-best-practices", computed)
        self.assertIn("frontend-component-rules", computed)
        self.assertNotIn("frontend-ui-visual-rules", computed)
        visual = route_owners(["src/views/User.vue"], ["aria", "css"])
        self.assertIn("frontend-ui-visual-rules", visual)
        self.assertNotIn("vue-router-best-practices", visual)

    def test_path_tokens_and_encoding_boundaries(self) -> None:
        """验证带空格路径、后缀和编码信号的边界。

        [参数] 无
        [返回] 无；断言失败时由 unittest 抛出异常。
        最近修改时间：2026-08-01 00:00:00；覆盖路径 token 与编码条件路由。
        """

        # 1. 文件名 token 必须独立匹配，不能由普通文本误触发语言 Owner。
        owners = route_owners(["tests with spaces/fixtures/user stub.py", "src with spaces/App.tsx"])
        self.assertIn("test-program-rules", owners)
        self.assertIn("vercel-react-best-practices", owners)
        self.assertNotIn("golang-patterns", route_owners(["docs/draft.go notes/readme.txt"]))
        self.assertIn("windows-encoding-rules", route_owners(["scripts/build.ps1"]))
        self.assertIn("windows-encoding-rules", route_owners(["config/app.yaml"], ["bom"]))

    def test_owner_source_map_path_is_shared_and_absolute(self) -> None:
        """验证来源映射由共享路由返回绝对路径。

        [参数] 无
        [返回] 无；断言失败时由 unittest 抛出异常。
        最近修改时间：2026-08-01 00:00:00；覆盖唯一来源映射的归属路径。
        """

        # 1. 消费者只能通过共享入口获得风格 Owner 的来源映射。
        path = owner_source_map_path(".")
        self.assertTrue(path.is_absolute())
        self.assertEqual(path.name, "static-owner-source-map.json")
        self.assertEqual(path.parent.name, "references")
        self.assertEqual(path.parent.parent.name, "code-style-consistency-rules")

    def test_all_returned_owners_are_declared(self) -> None:
        """验证每个路由结果都在 Owner 清单中声明。

        [参数] 无
        [返回] 无；断言失败时由 unittest 抛出异常。
        最近修改时间：2026-08-01 00:00:00；防止共享路由返回未注册的 Owner。
        """

        # 1. 对接口和前端路由样本校验结果集合属于声明全集。
        for files, signals in ((["src/api/user_controller.py"], ()), (["src/router/auth.ts"], ("vue-router",))):
            self.assertTrue(set(route_owners(files, signals)).issubset(OWNER_NAMES))


if __name__ == "__main__":
    unittest.main()
