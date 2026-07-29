"""微业务 JSON RPC 与 CodeGraph 导入审查真实行为测试。"""

import json
import shutil
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
MICRO_BUSINESS = ROOT / "micro-business-architecture-rules" / "scripts" / "micro_business.py"
FIXTURE_ROOT = Path(__file__).resolve().parent / "fixtures" / "micro-business-rpc"


def run_micro_business(*args):
    """执行本地微业务隔离检查并保留稳定的进程结果。

    [参数] args：传递给 micro_business.py 的命令行参数。
    [返回] CompletedProcess：包含退出码、标准输出和标准错误。
    最近修改时间: 2026-07-28 23:55:00 新增 RPC 导入确定性门禁测试入口。
    """
    return subprocess.run(
        [sys.executable, str(MICRO_BUSINESS), *args],
        cwd=ROOT,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        check=False,
    )


def run_codegraph(*args):
    """执行本地 CodeGraph 命令，为跨业务导入审查提供真实图谱证据。

    [参数] args：传递给 codegraph 的命令行参数。
    [返回] CompletedProcess：包含退出码、标准输出和标准错误。
    最近修改时间: 2026-07-28 23:55:00 新增 RPC 导入节点审查入口。
    """
    executable = shutil.which("codegraph")
    if executable is None:
        raise RuntimeError("未找到 CodeGraph；RPC 审查闸门不能降级为未执行")
    return subprocess.run(
        [executable, *args],
        cwd=ROOT,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        check=False,
    )


def rpc_response(code, status, message, data):
    """构造本轮 JSON RPC fixture 使用的统一响应语义。

    [参数] code：业务状态码；status：是否成功；message：无敏感结果说明；data：结构化数据或空值。
    [返回] str：可解析的 Response JSON 字符串。
    最近修改时间: 2026-07-28 23:55:00 覆盖跨业务边界的统一响应字段。
    """
    return json.dumps({"code": code, "status": status, "message": message, "data": data}, ensure_ascii=False)


def get_profile_rpc(request_json):
    """模拟目标业务域的公开 RPC：仅接受 JSON 字符串并始终返回 Response JSON。

    [参数] request_json：调用方传来的 JSON 字符串。
    [返回] str：成功、解析失败、校验失败或业务失败的统一 Response JSON。
    最近修改时间: 2026-07-28 23:55:00 新增 JSON 输入输出与错误不跨域抛出的行为样本。
    """
    # 1. 解析失败必须转换为响应，而不是把 JSON 异常泄漏给调用方。
    try:
        request = json.loads(request_json)
    except json.JSONDecodeError:
        return rpc_response(400, False, "请求 JSON 无法解析", None)
    # 2. 校验和业务失败也保持同一响应形态，调用方不接触目标域私有异常或实体。
    if not isinstance(request, dict) or not request.get("user_id"):
        return rpc_response(422, False, "缺少 user_id", None)
    if request["user_id"] == "business-failure":
        return rpc_response(409, False, "用户资料当前不可用", None)
    return rpc_response(200, True, "ok", {"display_name": "fixture-user"})


class BusinessRpcTests(unittest.TestCase):
    """验证 JSON RPC 契约、确定性隔离检查与 CodeGraph 审查证据。"""

    def test_json_response_covers_success_and_all_failure_kinds(self):
        """确认四类 JSON RPC 结果均可解析为统一 Response 字段。

        [参数] self：unittest 测试实例。
        [返回] 无。
        最近修改时间: 2026-07-28 23:55:00 覆盖成功、非法 JSON、校验失败和业务失败。
        """
        # 1. 对每种跨域返回状态验证统一字段、成功标识和数据可解析性。
        cases = (
            (json.dumps({"user_id": "u-1"}), True, "fixture-user"),
            ("{", False, None),
            (json.dumps({}), False, None),
            (json.dumps({"user_id": "business-failure"}), False, None),
        )
        for request_json, expected_status, expected_name in cases:
            with self.subTest(request_json=request_json):
                response = json.loads(get_profile_rpc(request_json))
                self.assertEqual({"code", "status", "message", "data"}, set(response))
                self.assertEqual(expected_status, response["status"])
                self.assertIsInstance(response["code"], int)
                self.assertIsInstance(response["message"], str)
                if expected_name is None:
                    self.assertIsNone(response["data"])
                else:
                    self.assertEqual(expected_name, response["data"]["display_name"])

    def test_deterministic_check_accepts_only_target_rpc_import(self):
        """确认微业务隔离脚本仅放行精确的目标域 rpc 导入。

        [参数] self：unittest 测试实例。
        [返回] 无。
        最近修改时间: 2026-07-28 23:55:00 覆盖一个合规与三个私有层违规样本。
        """
        # 1. 合规 orders -> users/rpc 必须通过，三类私有层直连必须稳定失败。
        good = run_micro_business("check", "--root", str(FIXTURE_ROOT / "good"))
        self.assertEqual(0, good.returncode, good.stdout + good.stderr)
        for name, private_path in (("bad-service", "service"), ("bad-entity", "entity"), ("bad-util", "util")):
            with self.subTest(fixture=name):
                result = run_micro_business("check", "--root", str(FIXTURE_ROOT / name))
                self.assertEqual(1, result.returncode, result.stdout + result.stderr)
                self.assertIn(f"users/{private_path}", result.stdout)

    def test_codegraph_review_locates_rpc_and_private_import_evidence(self):
        """确认 CodeGraph 能定位合规 RPC 与每个私有层违规导入的来源文件。

        [参数] self：unittest 测试实例。
        [返回] 无。
        最近修改时间: 2026-07-28 23:55:00 将 CodeGraph 导入节点纳入 RPC 审查闸门。
        """
        # 1. 先同步规则仓库索引，再逐条查询 fixture 的精确导入路径。
        synced = run_codegraph("sync", str(ROOT))
        self.assertEqual(0, synced.returncode, synced.stdout + synced.stderr)
        cases = (
            ("good", "rpc", "orders/service.go"),
            ("bad-service", "service", "orders/service.go"),
            ("bad-entity", "entity", "orders/service.go"),
            ("bad-util", "util", "orders/service.go"),
        )
        for fixture, imported_layer, source_suffix in cases:
            with self.subTest(fixture=fixture):
                imported = f"example.com/app/internal/business/users/{imported_layer}"
                result = run_codegraph("query", "-p", str(ROOT), "--kind", "import", "--limit", "1000", "--json", imported)
                self.assertEqual(0, result.returncode, result.stdout + result.stderr)
                self.assertIn(imported, result.stdout)
                self.assertIn(f"micro-business-rpc/{fixture}/internal/business/{source_suffix}", result.stdout.replace("\\", "/"))


if __name__ == "__main__":
    unittest.main()
