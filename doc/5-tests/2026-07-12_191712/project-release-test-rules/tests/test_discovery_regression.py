"""验证无 gRPC 声明的普通项目不会复用未绑定入口。"""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT_ROOT = Path(__file__).parents[5] / "project-release-test-rules" / "scripts"
if str(SCRIPT_ROOT) not in sys.path:
    sys.path.insert(0, str(SCRIPT_ROOT))

from release_test_engine.discovery import discover_project


class DiscoveryRegressionTests(unittest.TestCase):
    """覆盖 R1-R01 的无匹配 gRPC 发现路径。"""

    def test_non_grpc_project_does_not_reuse_unbound_grpc_item(self) -> None:
        """[参数] 无；[返回] 无；最近修改时间: 2026-07-12 19:17:12 验证普通项目首次发现不引用未绑定入口。"""

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "handlers.java").write_text('@KafkaListener(topics=["users"])', encoding="utf-8")
            (root / "README.md").write_text("普通项目说明", encoding="utf-8")

            result = discover_project(root)

            self.assertTrue(any(item.protocol == "message" for item in result.interfaces))
            self.assertFalse(any(item.protocol == "grpc" for item in result.interfaces))


if __name__ == "__main__":
    unittest.main()
