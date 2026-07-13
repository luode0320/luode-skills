"""运行时阻断事实的本地契约测试。"""

from __future__ import annotations

import sys
from pathlib import Path
import unittest


SCRIPTS_DIR = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

from recovery_engine import RecoveryEngine, RecoveryRequest  # noqa: E402


class BlockerFactTests(unittest.TestCase):
    """验证终态与共享阻断契约的边界。"""

    def setUp(self) -> None:
        """创建不含敏感数据的恢复请求。"""

        self.request = RecoveryRequest(
            recovery_id="recovery-001",
            task_id_hash="task-hash",
            component_id="component-a",
            scope="local",
            failure_class="transport_timeout",
            idempotency_class="read_only",
            success_criterion="health check passes",
        )

    def test_blocked_result_contains_complete_blocker_fact(self) -> None:
        """blocked 结果必须携带完整且可重入的阻断事实。"""

        result = RecoveryEngine._result("blocked", "probe_failed", self.request)

        self.assertEqual(result["blocker"]["task_status"], "blocked")
        self.assertEqual(result["blocker"]["stage"], "运行时恢复")
        self.assertEqual(len(result["blocker"]["resolution_plan"]), 1)
        self.assertIn("probe_failed+component-a", result["blocker"]["dedupe_key"])

    def test_manual_handoff_contains_blocker_fact(self) -> None:
        """manual_handoff 同样是必须交接的任务阻断终态。"""

        result = RecoveryEngine._result("manual_handoff", "resume_missing", self.request)

        self.assertEqual(result["blocker"]["task_status"], "manual_handoff")
        self.assertIn("原成功标准", result["blocker"]["reentry_point"])

    def test_healthy_result_omits_blocker_fact(self) -> None:
        """健康结果不得误报任务阻断。"""

        result = RecoveryEngine._result("healthy", "healthy", self.request)

        self.assertNotIn("blocker", result)


if __name__ == "__main__":
    unittest.main()
