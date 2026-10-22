"""Git 提交 pre gate 的提交边界回归测试。"""

from __future__ import annotations

import unittest

from pre_commit_gate_fixture import GateTestCase


class CommitScopeGateTests(GateTestCase):
    """验证提交范围与落点边界。"""

    def test_business_scope_can_commit_together(self) -> None:
        """验证同一业务目标的实现、测试、文档与状态文件可同笔提交。

        [参数] 无。
        [返回] 无；断言失败时由 unittest 抛出异常。
        最近修改时间：2026-09-10 17:20:00；覆盖按业务合并提交正例。
        """
        # 1. 构造同一业务目标的实现、可执行测试、流程文档与项目状态同步文件。
        result = self.run_gate(
            title="feat: [订单创建规则] 新增订单创建能力并同步流程文档",
            files={
                "src/order/create_order.py": "def create_order():\n    return True\n",
                "test/order/create_order_test.py": "import unittest\n",
                "doc/2-需求/2026-08-02_订单创建规则.md": "需求",
                "doc/3-实施/2026-08-02_订单创建规则_实施总览.md": "实施",
                "doc/5-tests/2026-08-02_订单创建规则/README.md": "测试说明",
                "doc/6-review/2026-08-02_订单创建规则_6-review.md": "STYLE: PASS",
                "PROJECT_CURRENT.md": "# 项目当前状态\n",
                "PROJECT_MEMORY.md": "# 项目长期记忆\n",
                "字典.md": "# 字典\n",
                "skill-dictionary/data.js": "export default {};\n",
            },
        )

        # 2. 按业务合并提交必须通过门禁，不再因跨域混提阻断。
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("PASS: pre-commit gate", result.stdout + result.stderr)

    def test_docs_and_executable_test_no_longer_blocked(self) -> None:
        """验证文档与可执行测试同笔提交不再被提交域门禁阻断。

        [参数] 无。
        [返回] 无；断言失败时由 unittest 抛出异常。
        最近修改时间：2026-09-10 17:20:00；覆盖原提交域阻断规则被移除后的行为。
        """
        # 1. 构造流程文档和根 test 目录中的可执行测试。
        result = self.run_gate(
            title="docs: [订单创建规则] 更新需求实施记录并补充回归用例",
            files={
                "doc/2-需求/2026-08-02_订单创建规则.md": "需求",
                "test/order/create_order_test.py": "import unittest\n",
            },
        )

        # 2. 同一业务目标的文档与测试合并提交必须通过，且不再出现提交域阻断文案。
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertNotIn("commit domains", result.stdout + result.stderr)

    def test_persisted_sentinel_does_not_block_or_echo(self) -> None:
        """代码、配置和普通文档中的 sentinel 不得被门禁阻断或回显。"""
        sentinel = "fixture-secret"
        result = self.run_gate(
            title="feat: [凭据边界] 更新持久化规则",
            files={
                "config/local.yaml": f"token: {sentinel}\\n",
                "src/config.py": f"TOKEN = '{sentinel}'\\n",
                "docs/config.md": f"token: {sentinel}\\n",
            },
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertNotIn(sentinel, result.stdout + result.stderr)

    def test_go_test_outside_root_test_still_blocked(self) -> None:
        """验证 Go 测试落点约束未因合并提交而放宽。

        [参数] 无。
        [返回] 无；断言失败时由 unittest 抛出异常。
        最近修改时间：2026-09-10 17:20:00；覆盖 Go 测试落点阻断仍生效。
        """
        # 1. 构造根 test/ 之外的新增 Go 测试文件。
        result = self.run_gate(
            title="feat: [订单创建] 新增订单创建能力",
            files={
                "internal/order/create_order_test.go": "package order\n",
            },
        )

        # 2. 落点违规必须继续阻断，退出码与原文案保持不变。
        self.assertEqual(result.returncode, 15, result.stdout + result.stderr)
        self.assertIn("BLOCK: staged *_test.go must be under root test/", result.stderr)

    def test_service_layer_root_file_still_blocked(self) -> None:
        """验证服务层根目录直落约束未因合并提交而放宽。

        [参数] 无。
        [返回] 无；断言失败时由 unittest 抛出异常。
        最近修改时间：2026-09-10 17:20:00；覆盖服务层落点阻断仍生效。
        """
        # 1. 构造 internal/service 根目录直落的实现文件。
        result = self.run_gate(
            title="feat: [订单创建] 新增订单创建能力",
            files={
                "internal/service/create_order.go": "package service\n",
            },
        )

        # 2. 落点违规必须继续阻断，退出码与原文案保持不变。
        self.assertEqual(result.returncode, 16, result.stdout + result.stderr)
        self.assertIn("BLOCK: staged file in internal/service/*.go root", result.stderr)


if __name__ == "__main__":
    unittest.main(verbosity=2)
