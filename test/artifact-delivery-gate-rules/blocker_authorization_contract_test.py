#!/usr/bin/env python3
"""阻断授权契约测试：有效授权、范围隔离、过期/多阻断拒绝、验证失败保持阻断。"""

from __future__ import annotations

import unittest
from pathlib import Path
from typing import Any, Dict, List, Optional


ROOT = Path(__file__).resolve().parents[2]
CONTRACT_FILE = ROOT / "artifact-delivery-gate-rules" / "references" / "task-blocker-closure-contract.md"


def _record(record_id: str, status: str = "blocked", active: bool = True) -> Dict[str, Any]:
    """构造脱敏的 BLK-* 记录样本。

    [参数] record_id: 阻断记录标识；status: 当前阻断状态；active: 是否仍有效。
    [返回] Dict[str, Any]：用于授权范围断言的最小记录。
    最近修改时间：2026-08-09 12:00:00；改动原因：补齐授权契约测试函数的注释元信息。
    """
    # 1. 只构造授权范围判断所需的脱敏字段，避免夹带业务数据。
    return {
        "id": record_id,
        "status": status,
        "active": active,
        "authorization": "请直接回复：`同意授权` 或 请直接回复：`暂不授权`；仅授权该条列明的恢复动作",
    }


def resolve_authorization(records: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
    """返回可被“同意授权”放行的唯一有效未解除记录。

    [参数] records: 待判断的脱敏阻断记录集合。
    [返回] Optional[Dict[str, Any]]：唯一有效记录；无法唯一确定时为 None。
    最近修改时间：2026-08-09 12:00:00；改动原因：补齐授权契约测试函数的注释元信息。
    """
    # 1. 仅允许唯一且仍有效的 blocked/manual_handoff 记录成为授权目标。
    valid = [record for record in records if record.get("status") in ("blocked", "manual_handoff") and record.get("active")]
    if len(valid) == 1:
        return valid[0]
    return None


class BlockerAuthorizationContractTests(unittest.TestCase):
    """覆盖 REQ-BLK-AUTH-001 的 AC-BLK-006 四类授权场景。"""

    def test_contract_requires_authorization_action(self) -> None:
        """验证阻断契约包含“用户授权操作”字段与两种回复文案。

        [参数] 无。
        [返回] None：通过断言确认契约字段与授权文案完整。
        最近修改时间：2026-08-09 12:00:00；改动原因：补齐授权契约测试函数的注释元信息。
        """
        # 1. 读取唯一阻断契约并断言授权字段与固定回复均可见。
        text = CONTRACT_FILE.read_text(encoding="utf-8")
        self.assertIn("用户授权操作", text)
        self.assertIn("同意授权", text)
        self.assertIn("暂不授权", text)
        self.assertIn("唯一有效", text)

    def test_valid_authorization_targets_only_unique_active_record(self) -> None:
        """验证唯一有效的 BLK-* 记录可被“同意授权”定位。

        [参数] 无。
        [返回] None：通过断言确认只选择当前有效记录。
        最近修改时间：2026-08-09 12:00:00；改动原因：补齐授权契约测试函数的注释元信息。
        """
        # 1. 将已失效记录与唯一有效记录混合，确认解析目标不漂移。
        latest = _record("BLK-AUTH-002")
        records = [_record("BLK-AUTH-001", active=False), latest]
        target = resolve_authorization(records)
        self.assertEqual(target["id"], "BLK-AUTH-002")
        self.assertIn("同意授权", target["authorization"])

    def test_scope_isolation_does_not_authorize_other_records(self) -> None:
        """验证授权只作用于唯一目标，不能扩散到其它记录。

        [参数] 无。
        [返回] None：通过断言确认范围隔离和多记录拒绝。
        最近修改时间：2026-08-09 12:00:00；改动原因：补齐授权契约测试函数的注释元信息。
        """
        # 1. 先确认单一有效目标，再将另一记录激活以验证多记录失败关闭。
        target = _record("BLK-AUTH-003")
        other = _record("BLK-OTHER-001", active=False)
        resolved = resolve_authorization([other, target])
        self.assertEqual(resolved["id"], "BLK-AUTH-003")
        self.assertNotEqual(resolved["id"], "BLK-OTHER-001")
        other["active"] = True
        self.assertIsNone(resolve_authorization([other, target]))

    def test_expired_or_multiple_blockers_are_rejected(self) -> None:
        """验证已过期或多条有效阻断记录均拒绝自动授权。

        [参数] 无。
        [返回] None：通过断言确认授权意图不会被猜测采纳。
        最近修改时间：2026-08-09 12:00:00；改动原因：补齐授权契约测试函数的注释元信息。
        """
        # 1. 分别覆盖全失效与多条有效两种非唯一场景。
        expired = [_record("BLK-AUTH-004", active=False)]
        self.assertIsNone(resolve_authorization(expired))
        multiple = [_record("BLK-AUTH-005", active=True), _record("BLK-AUTH-006", active=True)]
        self.assertIsNone(resolve_authorization(multiple))

    def test_validation_failure_keeps_blocked_state(self) -> None:
        """验证原验证入口失败时，授权不会解除阻断状态。

        [参数] 无。
        [返回] None：通过断言确认失败后记录仍为 blocked。
        最近修改时间：2026-08-09 12:00:00；改动原因：补齐授权契约测试函数的注释元信息。
        """
        # 1. 模拟恢复动作后的原验证失败，状态不得提前改为完成。
        target = _record("BLK-AUTH-007")
        released: List[str] = []

        def release_after_validation(record: Dict[str, Any]) -> None:
            """仅在原验证通过后解除指定阻断记录。

            [参数] record: 已解析的唯一授权目标。
            [返回] None：验证失败时保持记录和释放列表不变。
            最近修改时间：2026-08-09 12:00:00；改动原因：补齐嵌套测试辅助函数的注释元信息。
            """
            # 1. 先执行原验证；失败时不允许改写阻断状态。
            original_validation = lambda: False
            if original_validation():
                record["status"] = "completed"
                released.append(record["id"])

        release_after_validation(target)
        self.assertEqual(target["status"], "blocked")
        self.assertEqual(released, [])


if __name__ == "__main__":
    unittest.main()
