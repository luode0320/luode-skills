"""Git 提交 pre gate 的最基本编译闸门回归测试。"""

from __future__ import annotations

import unittest

from pre_commit_gate_fixture import GateTestCase


class CompileGateTests(GateTestCase):
    """验证代码项目编译闸门的正负分支与跳过分支。"""

    def test_python_syntax_error_blocks_commit(self) -> None:
        """验证 Python 代码项目存在语法错误时提交被阻断。

        [参数] 无。
        [返回] 无；断言失败时由 unittest 抛出异常。
        最近修改时间：2026-10-22 10:00:00；覆盖最基本编译闸门的负向分支。
        """
        # 1. 构造带语法错误的 Python 代码项目与坏文件。
        result = self.run_gate(
            title="feat: [订单创建] 新增订单创建能力",
            files={
                "pyproject.toml": "[project]\nname = \"fixture\"\n",
                "src/order/create_order.py": "def create_order(:\n    pass\n",
            },
        )

        # 2. 语法错误必须阻断，并保留可定位的退出码与文案。
        self.assertEqual(result.returncode, 19, result.stdout + result.stderr)
        self.assertIn("BLOCK: baseline compile failed for code project", result.stderr)
        self.assertIn("src/order/create_order.py", result.stdout + result.stderr)

    def test_python_syntax_ok_passes_compile_gate(self) -> None:
        """验证 Python 代码项目语法正确时编译闸门放行。

        [参数] 无。
        [返回] 无；断言失败时由 unittest 抛出异常。
        最近修改时间：2026-10-22 10:00:00；覆盖最基本编译闸门的正向分支。
        """
        # 1. 构造语法正确的 Python 代码项目。
        result = self.run_gate(
            title="feat: [订单创建] 新增订单创建能力",
            files={
                "pyproject.toml": "[project]\nname = \"fixture\"\n",
                "src/order/create_order.py": "def create_order():\n    return True\n",
            },
        )

        # 2. 语法检查通过后必须正常放行，并留下编译证据。
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("PASS: compile gate", result.stdout)

    def test_go_compile_error_blocks_commit(self) -> None:
        """验证 Go 代码项目包级编译失败时提交被阻断。

        [参数] 无。
        [返回] 无；断言失败时由 unittest 抛出异常。
        最近修改时间：2026-10-22 10:00:00；覆盖 Go 真实编译器调用而非静态猜测。
        """
        # 1. 构造可编译失败的 Go 代码项目：调用不存在的符号。
        result = self.run_gate(
            title="feat: [订单创建] 新增订单创建能力",
            files={
                "go.mod": "module fixture\n\ngo 1.21\n",
                "order/create.go": "package order\n\nfunc Create() int { return missingSymbol }\n",
            },
        )

        # 2. go build 失败必须阻断提交，不得只看文件是否存在。
        self.assertEqual(result.returncode, 19, result.stdout + result.stderr)
        self.assertIn("BLOCK: baseline compile failed for code project", result.stderr)
        self.assertIn("go build", result.stdout)

    def test_non_code_project_skips_compile_gate(self) -> None:
        """验证非代码仓库不会被编译闸门误阻断。

        [参数] 无。
        [返回] 无；断言失败时由 unittest 抛出异常。
        最近修改时间：2026-10-22 10:00:00；覆盖纯文档仓库的跳过分支。
        """
        # 1. 构造仅含文档的仓库，不提供任何代码项目标记。
        result = self.run_gate(
            title="docs: [订单创建规则] 更新需求记录",
            files={
                "doc/2-需求/2026-08-02_订单创建规则.md": "需求",
            },
        )

        # 2. 无代码标记时必须跳过并放行，避免规则误伤文档仓库。
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("N/A: 未检测到代码项目标记", result.stdout)

    def test_typescript_without_local_tsc_blocks(self) -> None:
        """验证 TypeScript 项目缺少本地 tsc 时明确阻断而非联网取包。

        [参数] 无。
        [返回] 无；断言失败时由 unittest 抛出异常。
        最近修改时间：2026-10-22 10:20:00；防止 npx 回落到 registry 上的同名无关包。
        """
        # 1. 构造只有 tsconfig.json、未安装任何依赖的 TypeScript 项目。
        result = self.run_gate(
            title="feat: [编译闸门] 验证 TypeScript 入口",
            files={
                "tsconfig.json": '{"compilerOptions":{"strict":true}}\n',
                "src/index.ts": "export const value: number = 1;\n",
            },
        )

        # 2. 必须给出“缺少本地 tsc”的明确阻断，不得静默放行或静默跳过。
        self.assertEqual(result.returncode, 19, result.stdout + result.stderr)
        self.assertIn("BLOCK: TypeScript 项目缺少本地 tsc", result.stderr)

    def test_node_project_without_build_script_skips(self) -> None:
        """验证无 build 脚本的 package.json 不被当成代码项目阻断。

        [参数] 无。
        [返回] 无；断言失败时由 unittest 抛出异常。
        最近修改时间：2026-10-22 10:20:00；覆盖本仓库这类纯资产仓库的跳过路径。
        """
        # 1. 构造仅含依赖声明、没有 build 脚本的 package.json。
        result = self.run_gate(
            title="chore: [依赖声明] 更新开发依赖",
            files={
                "package.json": '{"devDependencies":{"left-pad":"^1.3.0"}}\n',
            },
        )

        # 2. 无编译入口时必须跳过并放行，避免纯资产仓库被误伤。
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("N/A: 未检测到代码项目标记", result.stdout)

    def test_unusable_node_blocks_instead_of_skipping(self) -> None:
        """验证 node 无法执行时阻断，而不是静默当成非代码项目跳过。

        [参数] 无。
        [返回] 无；断言失败时由 unittest 抛出异常。
        最近修改时间：2026-10-22 10:40:00；覆盖“工具链异常即阻断”口径。
        """
        # 1. 构造定义了 build 脚本的 Node 项目，并用失效 node 桩替换真实解释器。
        with_script = '{"scripts":{"build":"exit 0"}}\n'
        stub = "#!/bin/sh\nexit 127\n"
        result = self.run_gate(
            title="chore: [依赖声明] 更新开发依赖",
            files={"package.json": with_script},
            fake_node=stub,
        )

        # 2. node 不可用时无法判定编译入口，必须阻断而不是放行。
        self.assertEqual(result.returncode, 19, result.stdout + result.stderr)
        self.assertIn("BLOCK: package.json 无法解析或 node 不可用", result.stderr)


if __name__ == "__main__":
    unittest.main(verbosity=2)
