"""根 test 目录中的 Go 外部黑盒测试布局回归。"""

from __future__ import annotations

from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest


class GoBlackboxLayoutTests(unittest.TestCase):
    """验证 Go 测试仅从根 test 目录调用导出 API。"""

    def test_go_test_runs_external_package_under_root_test(self) -> None:
        """临时 Go 模块必须能以 go test ./test/... 运行黑盒测试。"""
        go = shutil.which("go")
        if go is None:
            self.fail("未找到 Go，无法验证根 test/ 的黑盒编译路径")

        # 1. 构造最小模块和导出 API，测试包使用独立 service_test 包。
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "service").mkdir()
            (root / "test" / "service").mkdir(parents=True)
            (root / "go.mod").write_text("module example.com/root-test-layout\n\ngo 1.22\n", encoding="utf-8")
            (root / "service" / "service.go").write_text(
                "package service\n\nfunc Name() string { return \"ok\" }\n",
                encoding="utf-8",
            )
            (root / "test" / "service" / "service_test.go").write_text(
                "package service_test\n\nimport (\n    \"testing\"\n\n    \"example.com/root-test-layout/service\"\n)\n\nfunc TestName(t *testing.T) {\n    if service.Name() != \"ok\" {\n        t.Fatal(\"unexpected name\")\n    }\n}\n",
                encoding="utf-8",
            )
            result = subprocess.run(
                [go, "test", "./test/..."],
                cwd=root,
                capture_output=True,
                check=False,
                text=True,
                encoding="utf-8",
            )
        self.assertEqual(result.returncode, 0, result.stderr)


if __name__ == "__main__":
    unittest.main(verbosity=2)
