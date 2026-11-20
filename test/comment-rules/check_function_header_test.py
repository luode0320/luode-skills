from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "comment-rules" / "scripts" / "check_function_header.py"

PASS_CASE = '''def good():
    """合格样例。

    [参数] 无。
    [返回] int：固定返回 1。
    最近修改时间：2026-10-31 22:00:00；新增合格样例。
    """
    return 1
'''

MISSING_CASE = '''def no_doc():
    return 1
'''

INVALID_ORDER_CASE = '''def bad_order():
    """顺序错误。

    [返回] 无。
    [参数] 无。
    最近修改时间：2026-10-31 22:00:00；新增探测。
    """
    return 1
'''

INVALID_VAGUE_CASE = '''def vague_note():
    """说明空泛。

    [参数] 无。
    [返回] 无。
    最近修改时间：2026-10-31 22:00:00；优化一下。
    """
    return 1
'''


class CheckFunctionHeaderTests(unittest.TestCase):
    # 用例只创建临时文件并调用真实脚本，不写入仓库，也不依赖工作树状态。
    # [参数] 无。
    # [返回] 无。
    # 最近修改时间：2026-10-31 22:40:00；新增函数头校验脚本回归，覆盖四种判定路径与退出码。
    def _run(self, source: str) -> subprocess.CompletedProcess:
        """在临时目录写样例并执行校验脚本。

        [参数] source: 待写入的 Python 源码文本。
        [返回] CompletedProcess：脚本的完整执行结果。
        最近修改时间：2026-10-31 22:40:00；新增脚本调用封装。
        """
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "sample.py"
            target.write_text(source, encoding="utf-8")
            return subprocess.run(
                [sys.executable, str(SCRIPT), "--root", str(ROOT), "--path", str(target)],
                capture_output=True,
                text=True,
                encoding="utf-8",
                cwd=ROOT,
            )

    def test_valid_header_passes(self) -> None:
        """验证完整元信息通过校验且退出码为 0。

        [参数] 无：使用模块级 PASS_CASE 样例。
        [返回] None：断言通过结论。
        最近修改时间：2026-10-31 22:40:00；新增合格路径用例。
        """
        result = self._run(PASS_CASE)
        self.assertEqual(0, result.returncode, result.stdout)
        self.assertIn("HEADER: PASS", result.stdout)

    def test_missing_docstring_blocks(self) -> None:
        """验证无 docstring 的函数被判定为 MISSING 并阻断。

        [参数] 无：使用模块级 MISSING_CASE 样例。
        [返回] None：断言阻断结论与 MISSING 明细。
        最近修改时间：2026-10-31 22:40:00；新增缺失路径用例。
        """
        result = self._run(MISSING_CASE)
        self.assertEqual(1, result.returncode, result.stdout)
        self.assertIn("[MISSING]", result.stdout)
        self.assertIn("HEADER: FAIL", result.stdout)

    def test_wrong_order_is_invalid(self) -> None:
        """验证元信息顺序错误被判定为 INVALID。

        [参数] 无：使用模块级 INVALID_ORDER_CASE 样例。
        [返回] None：断言顺序错误被识别。
        最近修改时间：2026-10-31 22:40:00；新增顺序判据用例。
        """
        result = self._run(INVALID_ORDER_CASE)
        self.assertEqual(1, result.returncode, result.stdout)
        self.assertIn("元信息顺序", result.stdout)

    def test_vague_note_is_invalid(self) -> None:
        """验证空泛改动说明被判定为 INVALID。

        [参数] 无：使用模块级 INVALID_VAGUE_CASE 样例。
        [返回] None：断言空泛说明被识别。
        最近修改时间：2026-10-31 22:40:00；新增空泛说明判据用例。
        """
        result = self._run(INVALID_VAGUE_CASE)
        self.assertEqual(1, result.returncode, result.stdout)
        self.assertIn("过于空泛", result.stdout)


if __name__ == "__main__":
    unittest.main()
