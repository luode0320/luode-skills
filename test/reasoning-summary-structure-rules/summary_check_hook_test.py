"""summary-check.py Stop hook 端到端回归：真实子进程 + stdin payload → 断言 exit code / stderr。

覆盖两层修复的决策闭环：
  1. 压缩前触发条件（有害阈值 60/10 已清除，见 env-bootstrap-check 回归，此处不重复）；
  2. 压缩后中断打回（registry 损坏 / 平台 abort 痕迹 / 未完成 step 均不得伪装成完成）。
"""

from __future__ import annotations

import json
import os
import subprocess
import tempfile
import unittest


HOOK = os.path.expanduser(r"~/.workbuddy/hooks/summary-check.py")
PY = os.path.expanduser(
    r"~/.workbuddy/binaries/python/versions/3.13.12/python.exe"
)

GATE = "SUMMARY-GATE-PMW-002"

DONE_REGISTRY = {
    "version": 4,
    "registry_schema": "task_plan_projection_registry",
    "registry_updated_at": "2026-08-23T00:00:00Z",
    "projections": [
        {
            "session_id": "sess-1",
            "state": "active",
            "steps": [{"id": "A", "step": "A", "status": "completed"}],
        }
    ],
}
INCOMPLETE_REGISTRY = {
    "version": 4,
    "registry_schema": "task_plan_projection_registry",
    "registry_updated_at": "2026-08-23T00:00:00Z",
    "projections": [
        {
            "session_id": "sess-1",
            "state": "active",
            "steps": [{"id": "A", "step": "A", "status": "in_progress"}],
        }
    ],
}


def block(obj: dict) -> str:
    return (
        "<!-- BEGIN TASK PLAN PROJECTION -->\n```json\n%s\n```\n"
        "<!-- END TASK PLAN PROJECTION -->\n"
    ) % json.dumps(obj, ensure_ascii=False)


def run_hook(project_current: str | None, payload: dict, transcript_text: str = ""):
    """在临时 cwd 下真实调用 summary-check.py，返回 (exit_code, stderr)。"""
    tmp = tempfile.mkdtemp(prefix="sc_e2e_")
    if project_current is not None:
        with open(os.path.join(tmp, "PROJECT_CURRENT.md"), "w", encoding="utf-8") as f:
            f.write(project_current)
    payload = dict(payload, cwd=tmp)
    if transcript_text:
        tp = os.path.join(tmp, "transcript.jsonl")
        with open(tp, "w", encoding="utf-8") as f:
            f.write(transcript_text)
        payload["transcript_path"] = tp
    proc = subprocess.run(
        [PY, HOOK],
        input=json.dumps(payload),
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    return proc.returncode, proc.stderr


class SummaryCheckHookTests(unittest.TestCase):
    """summary-check.py 压缩后中断打回决策闭环。"""

    def test_clean_done_allows(self):
        """正常完成（全 completed + 无中断）→ 放行 exit 0。"""
        code, _ = run_hook(block(DONE_REGISTRY), {"session_id": "sess-1"},
                           "normal assistant reply, nothing special")
        self.assertEqual(code, 0)

    def test_incomplete_rejects(self):
        """存在未完成 step → 打回 exit 2 并注入网关标记。"""
        code, err = run_hook(block(INCOMPLETE_REGISTRY), {"session_id": "sess-1"},
                             "working on it")
        self.assertEqual(code, 2)
        self.assertIn(GATE, err)

    def test_interrupt_disguised_as_done_rejects(self):
        """压缩后中断被伪装成完成（registry 全 completed + 尾部含 abort 原话）→ 打回 exit 2。"""
        code, err = run_hook(
            block(DONE_REGISTRY), {"session_id": "sess-1"},
            "x" * 5000 + "Aborting session for context compaction" + "y" * 5000,
        )
        self.assertEqual(code, 2)
        self.assertIn(GATE, err)
        self.assertIn("中断痕迹", err)

    def test_corrupt_registry_rejects(self):
        """registry 损坏（marker 存在但 JSON 坏）→ 打回 exit 2。"""
        bad = "<!-- BEGIN TASK PLAN PROJECTION -->\n```json\n{broken json\n```\n"
        code, err = run_hook(bad, {"session_id": "sess-1"}, "some tail text")
        self.assertEqual(code, 2)
        self.assertIn("registry", err)

    def test_no_registry_allows(self):
        """完全无投影痕迹 → 放行 exit 0（不影响正常会话）。"""
        code, _ = run_hook(None, {"session_id": "sess-1"}, "")
        self.assertEqual(code, 0)

    def test_user_end_exemption_allows(self):
        """用户明确说「结束」+ 未完成 → 豁免放行 exit 0（不误伤正常收口）。"""
        code, _ = run_hook(block(INCOMPLETE_REGISTRY), {"session_id": "sess-1"},
                           "好的，到此结束，不要再继续了")
        self.assertEqual(code, 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
