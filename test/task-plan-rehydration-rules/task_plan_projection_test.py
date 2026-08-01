"""任务投影脚本的单元和 CLI 契约测试。"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import re
import subprocess
import sys
import tempfile
import threading
import time
import unittest
from pathlib import Path
from unittest import mock


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
ROOT = REPOSITORY_ROOT / "task-plan-rehydration-rules"
SCRIPT = ROOT / "scripts" / "task_plan_projection.py"
SPEC = importlib.util.spec_from_file_location("task_plan_projection", SCRIPT)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError("unable to load task_plan_projection.py")
projection = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(projection)


class TaskPlanProjectionTests(unittest.TestCase):
    """验证托管区、状态、原子写入和 CLI 契约。"""

    TEST_SESSION_ID = "test-session"

    def setUp(self) -> None:
        """隔离宿主会话环境，避免显式测试会话与当前 Desktop 串线。

        [参数] 无。
        [返回] None：完成每个测试的宿主环境隔离。
        最近修改时间：2026-07-26 00:00:00；改动原因：让新增会话回退测试不受真实宿主环境污染。
        """
        # 1. 移除宿主会话变量并注册清理回调，确保每个用例独立运行。
        self._host_thread_id = os.environ.pop(projection.SESSION_ENV_NAME, None)
        self.addCleanup(self._restore_host_thread_id)

    def _restore_host_thread_id(self) -> None:
        """恢复测试前的宿主会话环境。

        [参数] 无。
        [返回] None：恢复测试前的环境变量状态。
        最近修改时间：2026-07-26 00:00:00；改动原因：避免测试清理影响后续宿主会话。
        """
        # 1. 仅在测试前存在宿主会话时恢复，保持原本缺失状态不变。
        if self._host_thread_id is not None:
            os.environ[projection.SESSION_ENV_NAME] = self._host_thread_id

    # _sample 构造合法活动或失活投影。
    # [参数] statuses: 步骤状态；state: 投影状态；updated_at: UTC 时间。
    # [返回] dict：带正确指纹的投影。
    # 最近修改时间：2026-07-23；改动原因：统一测试样本并减少无关重复。
    def _sample(
        self,
        statuses: tuple[str, ...] = ("completed", "in_progress", "pending"),
        *,
        state: str = "active",
        updated_at: str = "2026-07-23T00:00:00Z",
    ) -> dict[str, object]:
        """构造合法活动或失活投影。"""
        # 1. 根据状态数量生成稳定任务 ID 和悬浮窗文案。
        steps = [
            {"id": f"TASK-RTP-{index:02d}", "step": f"[TASK-RTP-{index:02d}] 步骤 {index}", "status": status}
            for index, status in enumerate(statuses, 1)
        ]
        # 2. 使用生产函数计算指纹，确保样本只改变被测字段。
        return {
            "version": 1,
            "state": state,
            "plan_key": "REQ-RTP-001/CYCLE-RTP-01",
            "source_document": "doc/3-实施/plan.md",
            "plan_fingerprint": projection.compute_plan_fingerprint(steps),
            "updated_at": updated_at,
            "steps": steps,
        }

    def _sample_v2(
        self,
        statuses: tuple[str, ...] = ("completed", "in_progress", "pending"),
        *,
        synthesis_mode: str = "exact",
        updated_at: str = "2026-07-24T00:00:00Z",
    ) -> dict[str, object]:
        """构造合法 version:2 精确或兜底投影。"""
        steps = [
            {"id": f"TASK-SYN-{index:02d}", "step": f"[TASK-SYN-{index:02d}] 步骤 {index}", "status": status}
            for index, status in enumerate(statuses, 1)
        ]
        return {
            "version": 2,
            "projection_origin": "synthesized",
            "synthesis_mode": synthesis_mode,
            "state": "active" if any(status != "completed" for status in statuses) else "inactive",
            "plan_key": (
                f"{projection.EXACT_PREFIX}plan" if synthesis_mode == "exact" else f"{projection.FALLBACK_PREFIX}20260724T000000Z"
            ),
            "source_document": "doc/3-实施/plan.md" if synthesis_mode == "exact" else "",
            "plan_fingerprint": projection.compute_plan_fingerprint(steps),
            "updated_at": updated_at,
            "steps": steps,
        }


    def _goal_sample(
        self,
        statuses: tuple[str, ...] = ("in_progress", "pending", "pending"),
        *,
        state: str = "active",
        synthesis_mode: str = "goal_default",
    ) -> dict[str, object]:
        """构造不含 Goal 原文的合法 version:3 Goal 投影。

        [参数] statuses: 固定安全三步状态；state: Goal 投影状态；synthesis_mode: Goal 合成模式。
        [返回] dict：符合 Goal v3 身份和指纹约束的测试投影。
        最近修改时间：2026-07-25 00:00:00；改动原因：覆盖 Goal 安全三步、阻断和完成迁移。
        """
        # 1. 仅从生产常量组装测试样本，防止测试意外允许自定义 Goal 文案。
        steps = [
            {"id": item[0], "step": item[1], "status": status}
            for item, status in zip(projection.GOAL_DEFAULT_STEPS, statuses, strict=True)
        ]
        return {
            "version": 3,
            "projection_origin": "goal",
            "synthesis_mode": synthesis_mode,
            "state": state,
            "plan_key": projection.GOAL_PLAN_KEY,
            "source_document": "",
            "plan_fingerprint": projection.compute_plan_fingerprint(steps),
            "updated_at": "2026-07-25T00:00:00Z",
            "steps": steps,
        }

    def _sample_v4_entry(
        self,
        session_id: str,
        statuses: tuple[str, ...] = ("completed", "in_progress", "pending"),
        *,
        state: str = "active",
    ) -> dict[str, object]:
        """构造带会话归属的 v4 注册表投影条目。"""
        projection_value = self._sample(statuses, state=state)
        # 用会话前缀区分步骤，payload 断言可以发现跨会话串线。
        normalized_session = re.sub(r"[^A-Za-z0-9]+", "-", session_id).strip("-").upper() or "SESSION"
        for index, step in enumerate(projection_value["steps"], 1):
            task_id = f"TASK-{normalized_session}-{index:02d}"
            step["id"] = task_id
            step["step"] = f"[{task_id}] 会话 {session_id} 步骤 {index}"
        projection_value["plan_key"] = f"REQ-RTP-{normalized_session}/CYCLE-RTP-01"
        projection_value["plan_fingerprint"] = projection.compute_plan_fingerprint(projection_value["steps"])
        normalized = projection.validate_projection(projection_value)
        return {
            "projection_id": projection.compute_projection_id(session_id, normalized),
            "session_id": session_id,
            "projection_origin": normalized.get("projection_origin", "persisted"),
            "synthesis_mode": normalized.get("synthesis_mode", "none"),
            "state": normalized["state"],
            "plan_key": normalized["plan_key"],
            "source_document": normalized["source_document"],
            "plan_fingerprint": normalized["plan_fingerprint"],
            "updated_at": normalized["updated_at"],
            "steps": normalized["steps"],
        }

    def _sample_v4_projection(
        self,
        session_id: str,
        statuses: tuple[str, ...] = ("completed", "in_progress", "pending"),
        *,
        state: str = "active",
    ) -> dict[str, object]:
        """构造供 write/upsert API 接收的带会话区分步骤的 v3 投影。"""
        entry = self._sample_v4_entry(session_id, statuses, state=state)
        return {
            "version": 3,
            "projection_origin": entry["projection_origin"],
            "synthesis_mode": entry["synthesis_mode"],
            "state": entry["state"],
            "plan_key": entry["plan_key"],
            "source_document": entry["source_document"],
            "plan_fingerprint": entry["plan_fingerprint"],
            "updated_at": entry["updated_at"],
            "steps": entry["steps"],
        }

    # _write_current 创建带普通正文的临时 PROJECT_CURRENT.md。
    # [参数] root: 临时目录；text: 初始正文。
    # [返回] Path：创建的文件路径。
    # 最近修改时间：2026-07-23；改动原因：复用用户正文保护样本。
    def _write_current(self, root: Path, text: str = "# 项目当前状态\n\n用户正文。\n") -> Path:
        """创建带普通正文的临时 PROJECT_CURRENT.md。"""
        path = root / "PROJECT_CURRENT.md"
        path.write_text(text, encoding="utf-8", newline="")
        return path

    def _write_legacy_projection(self, root: Path, legacy: dict[str, object]) -> Path:
        """写入未迁移的 v1-v3 单投影托管区。"""
        legacy_json = json.dumps(legacy, ensure_ascii=False, indent=2)
        return self._write_current(
            root,
            "# 项目当前状态\n\n用户正文。\n"
            + "\n".join(
                (
                    projection.BEGIN_MARKER,
                    "```json",
                    legacy_json,
                    "```",
                    projection.END_MARKER,
                )
            ),
        )

    # _run_cli 执行脚本子命令并固定 UTF-8 子进程环境。
    # [参数] arguments: CLI 参数。
    # [返回] CompletedProcess[str]：stdout/stderr 和退出码。
    # 最近修改时间：2026-07-23；改动原因：验证真实命令入口而非仅调用函数。
    def _run_cli(self, *arguments: str) -> subprocess.CompletedProcess[str]:
        """执行脚本子命令并固定 UTF-8 子进程环境。"""
        # 1. 复制环境并强制子进程使用 UTF-8，避免 Windows 代码页污染断言。
        environment = os.environ.copy()
        environment["PYTHONUTF8"] = "1"
        # 2. 使用真实 Python 子进程执行 CLI，保留 stdout、stderr 和退出码。
        return subprocess.run(
            [sys.executable, "-B", str(SCRIPT), *arguments],
            check=False,
            capture_output=True,
            text=True,
            encoding="utf-8",
            env=environment,
        )

    def _synthesis_context(
        self,
        *,
        trigger: str = "continue",
        current_step_hint: str | None = "TASK-SYN-02",
        completed_step_hints: list[str] | None = None,
        candidate_source_documents: list[str] | None = None,
        conflicts: list[str] | None = None,
    ) -> dict[str, object]:
        """构造 synthesize 输入上下文。

        [参数] trigger: 合成触发类型；current_step_hint: 当前步骤；completed_step_hints: 已完成步骤；candidate_source_documents: 候选来源；conflicts: 兼容保留参数。
        [返回] dict：可供 continue 或 timeout 路径使用的证据上下文。
        最近修改时间：2026-07-25 00:00:00；改动原因：复用既有样本覆盖超时升级入口。
        """
        # 1. 保持原有证据结构，只允许测试按场景替换触发类型和步骤提示。
        return {
            "trigger": trigger,
            "current_message": "继续",
            "project_current_summary": {
                "goal": "恢复无投影任务",
                "current_scope": "补建悬浮任务列表",
                "next_execution_point": "继续当前任务执行",
                "source_document_hint": "doc/3-实施/plan.md",
            },
            "thread_evidence": {
                "recent_task_labels": ["REQ-SYN-001", "TASK-SYN-02"],
                "completed_step_hints": ["TASK-SYN-01"] if completed_step_hints is None else completed_step_hints,
                "current_step_hint": current_step_hint,
            },
            "candidate_source_documents": ["doc/3-实施/plan.md"] if candidate_source_documents is None else candidate_source_documents,
        }

    def test_fingerprint_ignores_status_and_time(self) -> None:
        """[参数] 无；[返回] None；最近修改时间：2026-07-23；改动原因：锁定指纹身份字段。"""
        first = self._sample()
        second = self._sample(("pending", "pending", "pending"), updated_at="2026-07-23T01:00:00Z")
        self.assertEqual(first["plan_fingerprint"], second["plan_fingerprint"])

    def test_active_projection_builds_exact_payload(self) -> None:
        """[参数] 无；[返回] None；最近修改时间：2026-07-23；改动原因：锁定 update_plan payload。"""
        sample = self._sample()
        payload = projection.build_update_plan_payload(sample)
        self.assertEqual(payload["explanation"], projection.EXPLANATION)
        self.assertEqual(payload["plan"], [{"step": item["step"], "status": item["status"]} for item in sample["steps"]])

    def test_version_two_projection_builds_mode_specific_payload(self) -> None:
        """[参数] 无；[返回] None；最近修改时间：2026-07-24；改动原因：锁定补建 explanation 分支。"""
        exact = self._sample_v2()
        fallback = self._sample_v2(("in_progress", "pending", "pending"), synthesis_mode="fallback")
        self.assertEqual(
            projection.build_update_plan_payload(exact)["explanation"],
            projection.EXPLANATION_SYNTH_EXACT,
        )
        self.assertEqual(
            projection.build_update_plan_payload(fallback)["explanation"],
            projection.EXPLANATION_SYNTH_FALLBACK,
        )

    def test_state_migrations_survive_new_reads(self) -> None:
        """[参数] 无；[返回] None；最近修改时间：2026-07-23；改动原因：覆盖跨进程等价重读。"""
        # 1. 在临时 PROJECT_CURRENT 中连续写入三组状态迁移。
        with tempfile.TemporaryDirectory() as directory:
            path = self._write_current(Path(directory))
            # 2. 每次都从磁盘重新读取，确认新进程可见的三态与写入一致。
            for statuses in (("in_progress", "pending"), ("completed", "in_progress"), ("completed", "completed")):
                state = "inactive" if all(status == "completed" for status in statuses) else "active"
                projection.upsert_projection(path, self._sample(statuses, state=state), session_id=self.TEST_SESSION_ID)
                loaded = projection.load_projection(path, session_id=self.TEST_SESSION_ID)
                self.assertEqual([item["status"] for item in loaded["steps"]], list(statuses))

    def test_inactive_projection_rejects_payload(self) -> None:
        """[参数] 无；[返回] None；最近修改时间：2026-07-23；改动原因：防止完成计划重放。"""
        sample = self._sample(("completed",), state="inactive")
        with self.assertRaises(projection.ProjectionContractError):
            projection.build_update_plan_payload(sample)

    def test_append_and_replace_preserve_user_text(self) -> None:
        """[参数] 无；[返回] None；最近修改时间：2026-07-23；改动原因：保护非托管正文和幂等更新。"""
        # 1. 首次追加托管区，确认 CRLF 用户正文逐字保留。
        with tempfile.TemporaryDirectory() as directory:
            original = "# 项目当前状态\r\n\r\n用户正文。\r\n"
            path = self._write_current(Path(directory), original)
            projection.upsert_projection(path, self._sample(), session_id=self.TEST_SESSION_ID)
            first = path.read_bytes()
            self.assertTrue(first.startswith(original.encode("utf-8")))
            # 2. 再次更新只替换唯一托管区，不重复标记或删除用户内容。
            projection.upsert_projection(path, self._sample(("completed", "in_progress")), session_id=self.TEST_SESSION_ID)
            second = path.read_text(encoding="utf-8")
            self.assertEqual(second.count(projection.BEGIN_MARKER), 1)
            self.assertIn("用户正文。", second)
            self.assertIn('"version": 4', second)

    def test_marker_damage_is_rejected(self) -> None:
        """[参数] 无；[返回] None；最近修改时间：2026-07-23；改动原因：覆盖半标记、重复和逆序。"""
        # 1. 构造半标记、重复标记和逆序标记三类损坏样本。
        cases = (
            projection.BEGIN_MARKER,
            projection.BEGIN_MARKER + "\n" + projection.BEGIN_MARKER + "\n" + projection.END_MARKER,
            projection.END_MARKER + "\n" + projection.BEGIN_MARKER,
        )
        # 2. 每个损坏样本都必须稳定拒绝。
        for text in cases:
            with self.subTest(text=text):
                with self.assertRaises(projection.ProjectionContractError):
                    projection.extract_projection(text)

    def test_invalid_json_and_non_utf8_are_rejected(self) -> None:
        """[参数] 无；[返回] None；最近修改时间：2026-07-23；改动原因：覆盖损坏持久化输入。"""
        # 1. 托管区 JSON 损坏时返回契约错误。
        damaged = f"{projection.BEGIN_MARKER}\n```json\n{{bad\n```\n{projection.END_MARKER}"
        with self.assertRaises(projection.ProjectionContractError):
            projection.extract_projection(damaged)
        # 2. 文件不是 UTF-8 时返回 I/O 错误，不做替换解码。
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "PROJECT_CURRENT.md"
            path.write_bytes(b"\xff\xfe")
            with self.assertRaises(projection.ProjectionIOError):
                projection.load_projection(path)

    def test_unknown_and_sensitive_fields_are_rejected(self) -> None:
        """[参数] 无；[返回] None；最近修改时间：2026-07-23；改动原因：锁定字段白名单和敏感键。"""
        # 1. 顶层未知字段违反精确白名单。
        unknown = self._sample()
        unknown["extra"] = "value"
        with self.assertRaises(projection.ProjectionContractError):
            projection.validate_projection(unknown)
        # 2. 敏感字段即使有合法值也必须拒绝。
        sensitive = self._sample()
        sensitive["prompt"] = "secret"
        with self.assertRaises(projection.ProjectionContractError):
            projection.validate_projection(sensitive)

    def test_invalid_status_and_multiple_in_progress_are_rejected(self) -> None:
        """[参数] 无；[返回] None；最近修改时间：2026-07-23；改动原因：锁定三态和单进行中约束。"""
        # 1. 未知状态不允许进入投影。
        invalid = self._sample()
        invalid["steps"][0]["status"] = "running"
        with self.assertRaises(projection.ProjectionContractError):
            projection.validate_projection(invalid)
        # 2. 同一投影最多只能有一个进行中步骤。
        multiple = self._sample(("in_progress", "in_progress"))
        with self.assertRaises(projection.ProjectionContractError):
            projection.validate_projection(multiple)

    def test_step_count_text_and_duplicate_id_limits(self) -> None:
        """[参数] 无；[返回] None；最近修改时间：2026-07-23；改动原因：覆盖步骤数量和文本边界。"""
        # 1. 分别覆盖步骤总数和单条文案长度上限。
        too_many = self._sample(tuple("pending" for _ in range(21)))
        with self.assertRaises(projection.ProjectionContractError):
            projection.validate_projection(too_many)
        too_long = self._sample(("pending",))
        too_long["steps"][0]["step"] = "中" * 257
        with self.assertRaises(projection.ProjectionContractError):
            projection.validate_projection(too_long)
        # 2. 任务 ID 重复时拒绝，避免恢复后无法区分步骤。
        duplicate = self._sample(("pending", "in_progress"))
        duplicate["steps"][1]["id"] = duplicate["steps"][0]["id"]
        with self.assertRaises(projection.ProjectionContractError):
            projection.validate_projection(duplicate)

    def test_fingerprint_and_source_expectations_are_enforced(self) -> None:
        """[参数] 无；[返回] None；最近修改时间：2026-07-23；改动原因：防止过期或错源计划恢复。"""
        # 1. 投影自身指纹与有序任务不一致时拒绝。
        sample = self._sample()
        damaged = dict(sample)
        damaged["plan_fingerprint"] = "0" * 64
        with self.assertRaises(projection.ProjectionContractError):
            projection.validate_projection(damaged)
        # 2. 恢复期预期指纹或来源不一致时同样拒绝。
        with self.assertRaises(projection.ProjectionContractError):
            projection.validate_projection(sample, expected_fingerprint="f" * 64)
        with self.assertRaises(projection.ProjectionContractError):
            projection.validate_projection(sample, expected_source_document="other.md")

    def test_timestamp_requires_utc(self) -> None:
        """[参数] 无；[返回] None；最近修改时间：2026-07-23；改动原因：统一跨进程时间口径。"""
        for value in ("2026-07-23T00:00:00", "2026-07-23T08:00:00+08:00", "invalid"):
            sample = self._sample(updated_at=value)
            with self.subTest(value=value), self.assertRaises(projection.ProjectionContractError):
                projection.validate_projection(sample)

    def test_size_limit_and_replace_failure_preserve_original(self) -> None:
        """[参数] 无；[返回] None；最近修改时间：2026-07-23；改动原因：覆盖大小闸门和原子失败清理。"""
        # 1. 候选全文超过上限时，在原子写入前拒绝并保持哈希不变。
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            path = self._write_current(root, "x" * projection.MAX_FILE_BYTES)
            before = hashlib.sha256(path.read_bytes()).hexdigest()
            with self.assertRaises(projection.ProjectionContractError):
                projection.upsert_projection(path, self._sample(), session_id=self.TEST_SESSION_ID)
            self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), before)
            # 2. 原子替换失败时保留原正文并清理同目录临时文件。
            path.write_text("用户正文\n", encoding="utf-8")
            before_bytes = path.read_bytes()
            with mock.patch.object(projection.os, "replace", side_effect=OSError("boom")):
                with self.assertRaises(projection.ProjectionIOError):
                    projection.upsert_projection(path, self._sample(), session_id=self.TEST_SESSION_ID)
            self.assertEqual(path.read_bytes(), before_bytes)
            self.assertEqual(list(root.glob(".PROJECT_CURRENT.md.*.tmp")), [])

    def test_exact_file_size_limit_is_allowed(self) -> None:
        """[参数] 无；[返回] None；最近修改时间：2026-07-23；改动原因：锁定 51,200 字节闭区间边界。"""
        # 1. 根据渲染块长度构造恰好命中 51,200 字节的候选全文。
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            sample = self._sample()
            block = projection.render_projection_block(sample, "\n", session_id=self.TEST_SESSION_ID)
            prefix_length = projection.MAX_FILE_BYTES - len(block.encode("utf-8")) - 2
            path = self._write_current(root, "x" * prefix_length)
            # 2. 边界值允许写入，最终文件大小必须精确相等。
            projection.upsert_projection(path, sample, session_id=self.TEST_SESSION_ID)
            self.assertEqual(len(path.read_bytes()), projection.MAX_FILE_BYTES)

    def test_empty_inactive_slot_is_valid(self) -> None:
        """[参数] 无；[返回] None；最近修改时间：2026-07-23；改动原因：支持新项目模板预留槽位。"""
        # 1. 构造新项目模板使用的空失活槽位。
        slot = {
            "version": 1,
            "state": "inactive",
            "plan_key": "",
            "source_document": "",
            "plan_fingerprint": "",
            "updated_at": "1970-01-01T00:00:00Z",
            "steps": [],
        }
        # 2. 校验后字段和值保持不变。
        self.assertEqual(projection.validate_projection(slot), slot)

    def test_version_two_contracts_validate_exact_and_fallback(self) -> None:
        """[参数] 无；[返回] None；最近修改时间：2026-07-24；改动原因：覆盖 version:2 合法分支。"""
        exact = self._sample_v2()
        fallback = self._sample_v2(("in_progress", "pending", "pending"), synthesis_mode="fallback")
        self.assertEqual(projection.validate_projection(exact)["projection_origin"], "synthesized")
        self.assertEqual(projection.validate_projection(fallback)["synthesis_mode"], "fallback")

    def test_version_two_contract_rejects_invalid_origin_mode_and_source(self) -> None:
        """[参数] 无；[返回] None；最近修改时间：2026-07-24；改动原因：防止补建投影混用 persisted 语义。"""
        invalid = self._sample_v2()
        invalid["projection_origin"] = "persisted"
        with self.assertRaises(projection.ProjectionContractError):
            projection.validate_projection(invalid)
        fallback = self._sample_v2(("in_progress", "pending", "pending"), synthesis_mode="fallback")
        fallback["source_document"] = "doc/3-实施/plan.md"
        with self.assertRaises(projection.ProjectionContractError):
            projection.validate_projection(fallback)

    def test_goal_version_three_contract_rejects_original_goal_content(self) -> None:
        """验证 Goal 投影拒绝原文、标识与自定义步骤。

        [参数] 无。
        [返回] None。
        最近修改时间：2026-07-25 00:00:00；改动原因：防止 Goal 原文或运行时身份被持久化到悬浮窗投影。
        """
        # 1. 基线样本必须可通过 v3 Goal 契约，随后逐项注入被禁止的敏感字段。
        valid = self._goal_sample()
        self.assertEqual(projection.validate_projection(valid)["projection_origin"], "goal")
        for field in ("objective", "goal_objective", "goal_id", "goal_prompt", "thread_id", "user_input"):
            candidate = dict(valid)
            candidate[field] = "不得保存的原文"
            with self.subTest(field=field), self.assertRaises(projection.ProjectionContractError):
                projection.validate_projection(candidate)
        # 2. 即使重新计算指纹，也不得通过自定义步骤文案绕过固定安全列表。
        altered_steps = [dict(step) for step in valid["steps"]]
        altered_steps[0]["step"] = "[GOAL-01] 泄漏 Goal 原文"
        valid["steps"] = altered_steps
        valid["plan_fingerprint"] = projection.compute_plan_fingerprint(altered_steps)
        with self.assertRaises(projection.ProjectionContractError):
            projection.validate_projection(valid)

    def test_goal_blocked_and_inactive_state_rules(self) -> None:
        """验证阻断 Goal 只观察，完成 Goal 不可重放。

        [参数] 无。
        [返回] None。
        最近修改时间：2026-07-25 00:00:00；改动原因：锁定 blocked 无进行中步骤和 complete 无 payload 的安全边界。
        """
        # 1. 阻断投影仍可展示历史完成进度，但绝不保留进行中状态。
        blocked = self._goal_sample(("completed", "pending", "pending"), state="blocked", synthesis_mode="goal_blocked")
        payload = projection.build_update_plan_payload(blocked)
        self.assertEqual(payload["explanation"], projection.EXPLANATION_GOAL_BLOCKED)
        self.assertNotIn("in_progress", [item["status"] for item in payload["plan"]])
        # 2. 契约拒绝阻断中的进行中步骤，失活 Goal 同样不得生成 UI payload。
        invalid = self._goal_sample(("completed", "in_progress", "pending"), state="blocked", synthesis_mode="goal_blocked")
        with self.assertRaises(projection.ProjectionContractError):
            projection.validate_projection(invalid)
        inactive = self._goal_sample(("completed", "completed", "completed"), state="inactive")
        with self.assertRaises(projection.ProjectionContractError):
            projection.build_update_plan_payload(inactive)

    def test_goal_events_create_restore_block_complete_and_preserve_formal(self) -> None:
        """验证 Goal 生命周期、正式计划保护和 fallback 替换边界。

        [参数] 无。
        [返回] None。
        最近修改时间：2026-07-26 00:00:00；改动原因：锁定 Goal 完成收口 payload 与正式计划保护。
        """
        # 1. 新建、恢复、阻断和完成必须只迁移固定安全三步，并以 inactive 终止重放。
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            path = self._write_current(root)
            created = projection.handle_goal_event(path, "create", session_id=self.TEST_SESSION_ID)
            self.assertEqual(created["action"], "created")
            self.assertEqual(created["projection"]["version"], 3)
            self.assertEqual(created["projection"]["steps"][0]["status"], "in_progress")
            before_restore = path.read_bytes()
            restored = projection.handle_goal_event(path, "restore", session_id=self.TEST_SESSION_ID)
            self.assertEqual(restored["action"], "restored")
            self.assertEqual(path.read_bytes(), before_restore)
            blocked = projection.handle_goal_event(path, "blocked", session_id=self.TEST_SESSION_ID)
            self.assertEqual(blocked["projection"]["state"], "blocked")
            self.assertNotIn("in_progress", [item["status"] for item in blocked["projection"]["steps"]])
            with self.assertRaises(projection.ProjectionContractError):
                projection.handle_goal_event(path, "restore", session_id=self.TEST_SESSION_ID)
            completed = projection.handle_goal_event(path, "complete", session_id=self.TEST_SESSION_ID)
            self.assertTrue(completed["payload"])
            self.assertTrue(all(item["status"] == "completed" for item in completed["payload"]["plan"]))
            self.assertEqual(completed["projection"]["state"], "inactive")
            self.assertTrue(all(item["status"] == "completed" for item in completed["projection"]["steps"]))
            # 2. 活动 persisted 正式计划必须被保护，Goal 创建不能覆盖真实实施任务。
            projection.upsert_projection(path, self._sample(), session_id=self.TEST_SESSION_ID)
            formal_before = path.read_bytes()
            preserved = projection.handle_goal_event(path, "create", session_id=self.TEST_SESSION_ID)
            self.assertEqual(preserved["action"], "preserved_formal")
            self.assertEqual(path.read_bytes(), formal_before)
            # 3. 正式计划不关联 Goal 默认三步，后续 Goal 事件必须无副作用地保持真实实施任务。
            for event in ("restore", "blocked", "complete"):
                preserved_after_event = projection.handle_goal_event(path, event, session_id=self.TEST_SESSION_ID)
                self.assertEqual(preserved_after_event["action"], "preserved_formal")
                self.assertIsNone(preserved_after_event["payload"])
                self.assertEqual(path.read_bytes(), formal_before)
            # 4. synthesized fallback 仅是恢复兜底，创建 Goal 时必须替换为 Goal 安全三步。
            fallback = self._sample_v2(("in_progress", "pending", "pending"), synthesis_mode="fallback")
            projection.upsert_projection(path, fallback, session_id=self.TEST_SESSION_ID)
            created_from_fallback = projection.handle_goal_event(path, "create", session_id=self.TEST_SESSION_ID)
            self.assertEqual(created_from_fallback["action"], "created")
            self.assertEqual(created_from_fallback["projection"]["projection_origin"], "goal")
            self.assertEqual([item["id"] for item in created_from_fallback["projection"]["steps"]], ["GOAL-01", "GOAL-02", "GOAL-03"])

    def test_goal_projection_is_replaced_by_formal_write(self) -> None:
        """验证正式最小任务写入会替换活动 Goal 安全三步。

        [参数] 无。
        [返回] None。
        最近修改时间：2026-07-26 00:00:00；改动原因：固定正式计划写入与 session 精确读取的兼容路径。
        """
        # 1. 先建立活动 Goal 投影，再通过常规 write 写入正式最小任务。
        with tempfile.TemporaryDirectory() as directory:
            path = self._write_current(Path(directory))
            projection.handle_goal_event(path, "create", session_id=self.TEST_SESSION_ID)
            projection.upsert_projection(path, self._sample(), session_id=self.TEST_SESSION_ID)
            # 2. 写入后必须以正式来源为准，避免 Goal 默认步骤遮挡真实实施进度。
            replaced = projection.load_projection(path, session_id=self.TEST_SESSION_ID)
            self.assertEqual(replaced["projection_origin"], "persisted")
            self.assertEqual(replaced["steps"][0]["id"], "TASK-RTP-01")

    def test_goal_cli_and_invalid_event_preserve_original_file(self) -> None:
        """验证 Goal CLI 生命周期及失败时的原文件保护。

        [参数] 无。
        [返回] None。
        最近修改时间：2026-07-25 00:00:00；改动原因：确保 CLI 入口与函数调用具有相同的原子迁移和失败语义。
        """
        # 1. CLI 依次创建、阻断和完成 Goal，完成后恢复必须稳定返回契约错误。
        with tempfile.TemporaryDirectory() as directory:
            path = self._write_current(Path(directory))
            create = self._run_cli("goal", "--project-current", str(path), "--event", "create", "--session-id", "legacy/default")
            self.assertEqual(create.returncode, 0, create.stderr)
            self.assertEqual(json.loads(create.stdout)["action"], "created")
            blocked = self._run_cli("goal", "--project-current", str(path), "--event", "blocked", "--session-id", "legacy/default")
            self.assertEqual(blocked.returncode, 0, blocked.stderr)
            complete = self._run_cli("goal", "--project-current", str(path), "--event", "complete", "--session-id", "legacy/default")
            self.assertEqual(complete.returncode, 0, complete.stderr)
            before = hashlib.sha256(path.read_bytes()).hexdigest()
            restore = self._run_cli("goal", "--project-current", str(path), "--event", "restore", "--session-id", "legacy/default")
            self.assertEqual(restore.returncode, 2)
            self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), before)

    def test_legacy_versions_upgrade_to_version_three_only_when_written(self) -> None:
        """验证 v1/v2 兼容读取和成功写入时升级 v3。

        [参数] 无。
        [返回] None。
        最近修改时间：2026-07-25 00:00:00；改动原因：确保 Goal v3 引入不拒绝既有常规投影。
        """
        # 1. 旧版本常规投影写回后统一升级，旧版本 Goal 语义仍必须被拒绝。
        with tempfile.TemporaryDirectory() as directory:
            path = self._write_current(Path(directory))
            legacy = self._sample_v2()
            projection.upsert_projection(path, legacy, session_id=self.TEST_SESSION_ID)
            loaded = projection.load_projection(path, session_id=self.TEST_SESSION_ID)
            self.assertEqual(loaded["version"], 3)
            self.assertEqual(loaded["projection_origin"], "synthesized")
            v2_goal = self._sample_v2()
            v2_goal["projection_origin"] = "goal"
            v2_goal["synthesis_mode"] = "goal_default"
            with self.assertRaises(projection.ProjectionContractError):
                projection.validate_projection(v2_goal)

    def test_synthesize_projection_builds_exact_from_unique_source(self) -> None:
        """[参数] 无；[返回] None；最近修改时间：2026-07-26 00:00:00；改动原因：覆盖绑定 session 的无投影精确补建路径。"""
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            current_path = self._write_current(root)
            source_dir = root / "doc" / "3-实施"
            source_dir.mkdir(parents=True)
            source_path = source_dir / "plan.md"
            source_path.write_text(
                "- [TASK-SYN-01] 冻结补建契约\n- [TASK-SYN-02] 实现补建引擎\n- [TASK-SYN-03] 回归验证\n",
                encoding="utf-8",
            )
            result = projection.synthesize_projection(current_path, self._synthesis_context(), session_id=self.TEST_SESSION_ID)
            self.assertEqual(result["mode"], "exact")
            self.assertEqual(result["projection"]["version"], 2)
            self.assertEqual(result["projection"]["projection_origin"], "synthesized")
            self.assertEqual(result["projection"]["synthesis_mode"], "exact")
            self.assertEqual(result["projection"]["steps"][0]["status"], "completed")
            self.assertEqual(result["projection"]["steps"][1]["status"], "in_progress")
            self.assertEqual(result["payload"]["explanation"], projection.EXPLANATION_SYNTH_EXACT)

    def test_synthesize_projection_reads_task_columns_by_header(self) -> None:
        """验证正式清单可在顺序列之后提取任务 ID 与目标。

        [参数] 无。
        [返回] None。
        最近修改时间：2026-07-26 00:00:00；改动原因：保持正式周期表 session 绑定与任务列提取兼容。
        """
        # 1. 使用工程文档门禁的标准标题及“顺序、任务 ID、唯一目标”列布局构造来源文档。
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            current_path = self._write_current(root)
            source_dir = root / "doc" / "3-实施"
            source_dir.mkdir(parents=True)
            (source_dir / "plan.md").write_text(
                "## 周期内最小任务执行顺序\n\n"
                "| 顺序 | 任务 ID | 唯一目标 | 状态 |\n"
                "|---:|---|---|---|\n"
                "| 1 | `TASK-SYN-01` | 冻结补建契约 | completed |\n"
                "| 2 | `TASK-SYN-02` | 实现补建引擎 | in_progress |\n"
                "| 3 | `TASK-SYN-03` | 回归验证 | pending |\n",
                encoding="utf-8",
            )
            # 2. exact 结果必须按表头提取三项任务并保留显式完成与进行中状态。
            result = projection.synthesize_projection(current_path, self._synthesis_context(), session_id=self.TEST_SESSION_ID)
            self.assertEqual(result["mode"], "exact")
            self.assertEqual(
                [step["id"] for step in result["projection"]["steps"]],
                ["TASK-SYN-01", "TASK-SYN-02", "TASK-SYN-03"],
            )
            self.assertEqual(result["projection"]["steps"][0]["status"], "completed")
            self.assertEqual(result["projection"]["steps"][1]["status"], "in_progress")

    def test_synthesize_projection_falls_back_when_source_is_ambiguous(self) -> None:
        """[参数] 无；[返回] None；最近修改时间：2026-07-26 00:00:00；改动原因：保持 session 绑定下的多来源安全 fallback。"""
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            current_path = self._write_current(root)
            result = projection.synthesize_projection(
                current_path,
                self._synthesis_context(candidate_source_documents=["a.md", "b.md"]),
                session_id=self.TEST_SESSION_ID,
            )
            self.assertEqual(result["mode"], "fallback")
            self.assertEqual(result["projection"]["synthesis_mode"], "fallback")
            self.assertEqual(
                [step["id"] for step in result["projection"]["steps"]],
                ["RECOVERY-01", "RECOVERY-02", "RECOVERY-03"],
            )
            self.assertEqual(result["payload"]["explanation"], projection.EXPLANATION_SYNTH_FALLBACK)

    def test_synthesize_projection_falls_back_when_explicit_hints_are_missing(self) -> None:
        """[参数] 无；[返回] None；最近修改时间：2026-07-26 00:00:00；改动原因：保持 session 绑定下的缺证据 fallback。"""
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            current_path = self._write_current(root)
            result = projection.synthesize_projection(
                current_path,
                self._synthesis_context(current_step_hint=None, completed_step_hints=[]),
                session_id=self.TEST_SESSION_ID,
            )
            self.assertEqual(result["mode"], "fallback")

    def test_synthesize_projection_uses_first_unfinished_step_when_only_completed_hints_exist(self) -> None:
        """[参数] 无；[返回] None；最近修改时间：2026-07-26 00:00:00；改动原因：保持 session 绑定下的未完成步骤保守映射。"""
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            current_path = self._write_current(root)
            source_dir = root / "doc" / "3-实施"
            source_dir.mkdir(parents=True)
            (source_dir / "plan.md").write_text(
                "- [TASK-SYN-01] 冻结补建契约\n- [TASK-SYN-02] 实现补建引擎\n- [TASK-SYN-03] 回归验证\n",
                encoding="utf-8",
            )
            result = projection.synthesize_projection(
                current_path,
                self._synthesis_context(current_step_hint=None, completed_step_hints=["TASK-SYN-01"]),
                session_id=self.TEST_SESSION_ID,
            )
            self.assertEqual(result["mode"], "exact")
            self.assertEqual(result["projection"]["steps"][1]["status"], "in_progress")
            self.assertEqual(result["evidence"]["status_confidence"], "conservative")

    def test_synthesize_projection_falls_back_when_no_source_document_exists(self) -> None:
        """[参数] 无；[返回] None；最近修改时间：2026-07-26 00:00:00；改动原因：保持 session 绑定下的无来源兜底路径。"""
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            current_path = self._write_current(root)
            result = projection.synthesize_projection(
                current_path,
                self._synthesis_context(candidate_source_documents=[]),
                session_id=self.TEST_SESSION_ID,
            )
            self.assertEqual(result["mode"], "fallback")

    def test_probe_timeout_is_read_only_at_boundary_and_when_due(self) -> None:
        """验证 599/600/601 秒边界只返回资格状态且不写文件。"""
        with tempfile.TemporaryDirectory() as directory:
            current_path = self._write_current(Path(directory))
            before = current_path.read_bytes()
            directory_before = set(current_path.parent.iterdir())
            observations = (
                ("2026-07-25T00:09:59Z", "not_due"),
                ("2026-07-25T00:10:00Z", "not_due"),
                ("2026-07-25T00:10:00.001Z", "goal_check_required"),
                ("2026-07-25T00:10:01Z", "goal_check_required"),
            )
            with mock.patch.object(
                projection,
                "_projection_file_lock",
                side_effect=AssertionError("probe-timeout must not create a lock file"),
            ):
                for observed_at, expected_action in observations:
                    result = projection.probe_timeout_projection(
                        current_path,
                        started_at="2026-07-25T00:00:00Z",
                        observed_at=observed_at,
                        session_id=self.TEST_SESSION_ID,
                    )
                    self.assertEqual(result["action"], expected_action)
                    self.assertIsNone(result["payload"])
                    self.assertEqual(current_path.read_bytes(), before)
                    self.assertEqual(set(current_path.parent.iterdir()), directory_before)

    def test_probe_timeout_subtracts_pause_and_preserves_existing_states(self) -> None:
        """验证暂停扣除、活动投影和阻断 Goal 均不会进入 Goal 检查。"""
        with tempfile.TemporaryDirectory() as directory:
            current_path = self._write_current(Path(directory))
            before = current_path.read_bytes()
            paused = projection.probe_timeout_projection(
                current_path,
                started_at="2026-07-25T00:00:00Z",
                observed_at="2026-07-25T00:15:01Z",
                paused_seconds=301,
                session_id=self.TEST_SESSION_ID,
            )
            self.assertEqual(paused["action"], "not_due")
            active = self._sample()
            projection.upsert_projection(current_path, active, session_id=self.TEST_SESSION_ID)
            active_bytes = current_path.read_bytes()
            active_result = projection.probe_timeout_projection(
                current_path,
                started_at="2026-07-25T00:00:00Z",
                observed_at="2026-07-25T00:10:01Z",
                session_id=self.TEST_SESSION_ID,
            )
            self.assertEqual(active_result["action"], "already_active")
            self.assertEqual(current_path.read_bytes(), active_bytes)
            blocked = self._goal_sample(("completed", "pending", "pending"), state="blocked", synthesis_mode="goal_blocked")
            projection.upsert_projection(current_path, blocked, session_id=self.TEST_SESSION_ID)
            blocked_bytes = current_path.read_bytes()
            blocked_result = projection.probe_timeout_projection(
                current_path,
                started_at="2026-07-25T00:00:00Z",
                observed_at="2026-07-25T00:10:01Z",
                session_id=self.TEST_SESSION_ID,
            )
            self.assertEqual(blocked_result["action"], "blocked_goal_preserved")
            self.assertEqual(current_path.read_bytes(), blocked_bytes)
            self.assertNotEqual(before, active_bytes)

    def test_probe_timeout_isolates_sessions_and_allows_inactive_current_session(self) -> None:
        """验证其它会话活动投影不阻断当前会话，当前失活投影仍可升级。"""
        with tempfile.TemporaryDirectory() as directory:
            current_path = self._write_current(Path(directory))
            projection.upsert_projection(current_path, self._sample(), session_id="other-session")
            other_only = projection.probe_timeout_projection(
                current_path,
                started_at="2026-07-25T00:00:00Z",
                observed_at="2026-07-25T00:10:00.001Z",
                session_id=self.TEST_SESSION_ID,
            )
            self.assertEqual(other_only["action"], "goal_check_required")
            inactive = self._sample(("completed", "completed", "completed"), state="inactive")
            projection.upsert_projection(current_path, inactive, session_id=self.TEST_SESSION_ID)
            current_inactive = projection.probe_timeout_projection(
                current_path,
                started_at="2026-07-25T00:00:00Z",
                observed_at="2026-07-25T00:10:01Z",
                session_id=self.TEST_SESSION_ID,
            )
            self.assertEqual(current_inactive["action"], "goal_check_required")

    def test_probe_timeout_rejects_invalid_input_and_damaged_registry_without_writing(self) -> None:
        """验证非法时间和损坏 registry 都保持原文件字节不变。"""
        with tempfile.TemporaryDirectory() as directory:
            current_path = self._write_current(Path(directory))
            for started_at, observed_at, paused_seconds in (
                ("invalid", "2026-07-25T00:10:01Z", 0),
                ("2026-07-25T00:10:01Z", "2026-07-25T00:00:00Z", 0),
                ("2026-07-25T00:00:00Z", "2026-07-25T00:10:01Z", 602),
            ):
                before = current_path.read_bytes()
                with self.assertRaises(projection.ProjectionContractError):
                    projection.probe_timeout_projection(
                        current_path,
                        started_at=started_at,
                        observed_at=observed_at,
                        paused_seconds=paused_seconds,
                        session_id=self.TEST_SESSION_ID,
                    )
                self.assertEqual(current_path.read_bytes(), before)
            current_path.write_text(
                f"# 当前\n\n{projection.BEGIN_MARKER}\n```json\n{{broken}}\n```\n{projection.END_MARKER}\n",
                encoding="utf-8",
            )
            before = current_path.read_bytes()
            with self.assertRaises(projection.ProjectionContractError):
                projection.probe_timeout_projection(
                    current_path,
                    started_at="2026-07-25T00:00:00Z",
                    observed_at="2026-07-25T00:10:01Z",
                    session_id=self.TEST_SESSION_ID,
                )
            self.assertEqual(current_path.read_bytes(), before)

    def test_probe_timeout_cli_returns_goal_check_required_without_writing(self) -> None:
        """验证真实 CLI 返回 Goal 检查动作且不改写 PROJECT_CURRENT。"""
        with tempfile.TemporaryDirectory() as directory:
            current_path = self._write_current(Path(directory))
            before = current_path.read_bytes()
            result = self._run_cli(
                "probe-timeout",
                "--project-current",
                str(current_path),
                "--started-at",
                "2026-07-25T00:00:00Z",
                "--observed-at",
                "2026-07-25T00:10:01Z",
                "--session-id",
                "cli-probe-timeout",
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            output = json.loads(result.stdout)
            self.assertEqual(output["action"], "goal_check_required")
            self.assertIsNone(output["payload"])
            self.assertEqual(current_path.read_bytes(), before)

    def test_ensure_timeout_uses_strict_boundary_and_persists_exact_projection(self) -> None:
        """验证 599、600、601 秒边界及 exact 原子持久化。

        [参数] 无。
        [返回] None。
        最近修改时间：2026-07-25 00:00:00；改动原因：锁定严格大于十分钟才创建悬浮任务投影。
        """
        # 1. 每个边界使用独立文件，确保未到期场景没有被前一轮写入污染。
        observations = (
            ("2026-07-25T00:09:59Z", "not_due"),
            ("2026-07-25T00:10:00Z", "not_due"),
            ("2026-07-25T00:10:01Z", "escalated"),
        )
        for observed_at, expected_action in observations:
            with self.subTest(observed_at=observed_at), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                current_path = self._write_current(root)
                source_dir = root / "doc" / "3-实施"
                source_dir.mkdir(parents=True)
                (source_dir / "plan.md").write_text(
                    "- [TASK-SYN-01] 冻结补建契约\n- [TASK-SYN-02] 实现补建引擎\n",
                    encoding="utf-8",
                )
                before = current_path.read_bytes()
                # 2. 调用超时入口并验证 600 秒仍不写、601 秒才持久化 exact 投影。
                result = projection.ensure_timeout_projection(
                    current_path,
                    started_at="2026-07-25T00:00:00Z",
                    observed_at=observed_at,
                    context=self._synthesis_context(trigger="timeout"),
                    session_id=self.TEST_SESSION_ID,
                )
                self.assertEqual(result["action"], expected_action)
                if expected_action == "not_due":
                    self.assertEqual(current_path.read_bytes(), before)
                    self.assertIsNone(result["payload"])
                else:
                    self.assertEqual(result["mode"], "exact")
                    persisted = projection.load_projection(current_path, session_id=self.TEST_SESSION_ID)
                    self.assertEqual(persisted["synthesis_mode"], "exact")
                    self.assertEqual(result["payload"], projection.build_update_plan_payload(persisted))

    def test_ensure_timeout_subtracts_paused_seconds_before_boundary_check(self) -> None:
        """验证暂停时间从墙钟耗时扣除后再应用严格阈值。

        [参数] 无。
        [返回] None。
        最近修改时间：2026-07-25 00:00:00；改动原因：Plan Mode、等待用户、blocked 和 manual_handoff 暂停不得计入十分钟。
        """
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            current_path = self._write_current(root)
            source_dir = root / "doc" / "3-实施"
            source_dir.mkdir(parents=True)
            (source_dir / "plan.md").write_text(
                "- [TASK-SYN-01] 冻结补建契约\n- [TASK-SYN-02] 实现补建引擎\n",
                encoding="utf-8",
            )
            before = current_path.read_bytes()
            # 1. 墙钟 901 秒扣除 301 秒后恰为 600 秒，必须保持不写。
            not_due = projection.ensure_timeout_projection(
                current_path,
                started_at="2026-07-25T00:00:00Z",
                observed_at="2026-07-25T00:15:01Z",
                paused_seconds=301,
                context=self._synthesis_context(trigger="timeout"),
                session_id=self.TEST_SESSION_ID,
            )
            self.assertEqual(not_due["action"], "not_due")
            self.assertEqual(not_due["effective_elapsed_seconds"], 600)
            self.assertEqual(current_path.read_bytes(), before)
            # 2. 墙钟增加一秒后有效耗时为 601 秒，必须创建当前会话投影。
            escalated = projection.ensure_timeout_projection(
                current_path,
                started_at="2026-07-25T00:00:00Z",
                observed_at="2026-07-25T00:15:02Z",
                paused_seconds=301,
                context=self._synthesis_context(trigger="timeout"),
                session_id=self.TEST_SESSION_ID,
            )
            self.assertEqual(escalated["action"], "escalated")
            self.assertEqual(escalated["effective_elapsed_seconds"], 601)

    def test_ensure_timeout_uses_fallback_when_exact_evidence_is_ambiguous(self) -> None:
        """验证超时升级沿用固定三步 fallback。

        [参数] 无。
        [返回] None。
        最近修改时间：2026-07-25 00:00:00；改动原因：来源无法唯一确认时禁止猜测正式任务。
        """
        # 1. 多来源证据必须走 fallback，且持久化结果与返回 payload 一致。
        with tempfile.TemporaryDirectory() as directory:
            current_path = self._write_current(Path(directory))
            result = projection.ensure_timeout_projection(
                current_path,
                started_at="2026-07-25T00:00:00Z",
                observed_at="2026-07-25T00:10:01Z",
                context=self._synthesis_context(
                    trigger="timeout", candidate_source_documents=["a.md", "b.md"]
                ),
                session_id=self.TEST_SESSION_ID,
            )
            self.assertEqual(result["action"], "escalated")
            self.assertEqual(result["mode"], "fallback")
            persisted = projection.load_projection(current_path, session_id=self.TEST_SESSION_ID)
            self.assertEqual(persisted["synthesis_mode"], "fallback")
            self.assertEqual([step["id"] for step in persisted["steps"]], ["RECOVERY-01", "RECOVERY-02", "RECOVERY-03"])

    def test_ensure_timeout_keeps_existing_active_session_projection_unchanged(self) -> None:
        """验证当前会话已有活动投影时不重复写入。

        [参数] 无。
        [返回] None。
        最近修改时间：2026-07-25 00:00:00；改动原因：避免超时检查覆盖已存在的正式任务悬浮窗。
        """
        # 1. 预置当前会话活动投影，超时检查应返回 already_active 并保持文件字节不变。
        with tempfile.TemporaryDirectory() as directory:
            current_path = self._write_current(Path(directory))
            projection.upsert_projection(current_path, self._sample(), session_id=self.TEST_SESSION_ID)
            before = current_path.read_bytes()
            result = projection.ensure_timeout_projection(
                current_path,
                started_at="2026-07-25T00:00:00Z",
                observed_at="2026-07-25T00:10:01Z",
                context=self._synthesis_context(trigger="timeout"),
                session_id=self.TEST_SESSION_ID,
            )
            self.assertEqual(result["action"], "already_active")
            self.assertEqual(current_path.read_bytes(), before)
            self.assertEqual(result["payload"]["explanation"], projection.EXPLANATION)

    def test_ensure_timeout_preserves_blocked_goal_and_replaces_inactive_projection(self) -> None:
        """验证 blocked Goal 受保护而 inactive 投影可被超时升级替换。

        [参数] 无。
        [返回] None。
        最近修改时间：2026-07-25 00:00:00；改动原因：区分暂停观察状态与可安全替换的历史终态。
        """
        # 1. blocked Goal 必须原字节保留，并返回只观察用途的 payload。
        with tempfile.TemporaryDirectory() as directory:
            current_path = self._write_current(Path(directory))
            projection.handle_goal_event(current_path, "create", session_id=self.TEST_SESSION_ID)
            projection.handle_goal_event(current_path, "blocked", session_id=self.TEST_SESSION_ID)
            before = current_path.read_bytes()
            blocked = projection.ensure_timeout_projection(
                current_path,
                started_at="2026-07-25T00:00:00Z",
                observed_at="2026-07-25T00:10:01Z",
                context=self._synthesis_context(trigger="timeout"),
                session_id=self.TEST_SESSION_ID,
            )
            self.assertEqual(blocked["action"], "blocked_goal_preserved")
            self.assertEqual(blocked["payload"]["explanation"], projection.EXPLANATION_GOAL_BLOCKED)
            self.assertEqual(current_path.read_bytes(), before)
        # 2. inactive 投影不再代表当前悬浮窗，超过阈值后允许被 fallback 替换。
        with tempfile.TemporaryDirectory() as directory:
            current_path = self._write_current(Path(directory))
            inactive = self._sample(("completed", "completed"), state="inactive")
            projection.upsert_projection(current_path, inactive, session_id=self.TEST_SESSION_ID)
            replaced = projection.ensure_timeout_projection(
                current_path,
                started_at="2026-07-25T00:00:00Z",
                observed_at="2026-07-25T00:10:01Z",
                context=self._synthesis_context(
                    trigger="timeout", candidate_source_documents=["a.md", "b.md"]
                ),
                session_id=self.TEST_SESSION_ID,
            )
            self.assertEqual(replaced["action"], "escalated")
            self.assertEqual(replaced["mode"], "fallback")
            self.assertEqual(
                projection.load_projection(current_path, session_id=self.TEST_SESSION_ID)["state"],
                "active",
            )

    def test_ensure_timeout_serializes_active_check_synthesis_and_upsert(self) -> None:
        """验证同会话并发超时检查只有一个调用执行合成和写入。

        [参数] 无。
        [返回] None。
        最近修改时间：2026-07-25 00:00:00；改动原因：防止检查后写入之间的 TOCTOU 覆盖。
        """
        with tempfile.TemporaryDirectory() as directory:
            current_path = self._write_current(Path(directory))
            context = self._synthesis_context(
                trigger="timeout", candidate_source_documents=["a.md", "b.md"]
            )
            synthesis_started = threading.Event()
            release_synthesis = threading.Event()
            second_started = threading.Event()
            results: list[dict[str, object]] = []
            errors: list[BaseException] = []
            call_count = 0
            count_lock = threading.Lock()
            original_synthesize = projection.synthesize_projection

            def delayed_synthesize(*args: object, **kwargs: object) -> dict[str, object]:
                """暂停首个合成调用，为第二线程制造稳定竞争窗口。

                [参数] args/kwargs: 原合成函数参数。
                [返回] dict：原合成结果。
                最近修改时间：2026-07-25 00:00:00；改动原因：验证锁覆盖完整条件写入临界区。
                """
                nonlocal call_count
                # 1. 记录真实合成次数并等待测试线程允许继续写入。
                with count_lock:
                    call_count += 1
                synthesis_started.set()
                release_synthesis.wait(timeout=2)
                return original_synthesize(*args, **kwargs)

            def run_timeout(mark_second: bool = False) -> None:
                """执行一次同会话超时检查并收集线程结果。

                [参数] mark_second: 是否标记第二线程已开始调用。
                [返回] None。
                最近修改时间：2026-07-25 00:00:00；改动原因：集中捕获并发线程结果与异常。
                """
                # 1. 第二线程在进入生产函数前发出信号，主线程据此释放首个合成。
                if mark_second:
                    second_started.set()
                try:
                    results.append(
                        projection.ensure_timeout_projection(
                            current_path,
                            started_at="2026-07-25T00:00:00Z",
                            observed_at="2026-07-25T00:10:01Z",
                            context=context,
                            session_id=self.TEST_SESSION_ID,
                        )
                    )
                except BaseException as error:  # pragma: no cover - 失败内容由主线程断言
                    errors.append(error)

            # 1. 首线程持锁停在 synthesize，第二线程开始后应阻塞在同一文件锁。
            with mock.patch.object(projection, "synthesize_projection", side_effect=delayed_synthesize):
                first = threading.Thread(target=run_timeout)
                second = threading.Thread(target=run_timeout, kwargs={"mark_second": True})
                first.start()
                self.assertTrue(synthesis_started.wait(timeout=2))
                second.start()
                self.assertTrue(second_started.wait(timeout=2))
                time.sleep(0.1)
                release_synthesis.set()
                first.join(timeout=3)
                second.join(timeout=3)
            # 2. 只有一个线程允许合成和写入，后到线程必须观察到 active 后无副作用返回。
            self.assertFalse(first.is_alive())
            self.assertFalse(second.is_alive())
            self.assertEqual(errors, [])
            self.assertEqual(call_count, 1)
            self.assertEqual({item["action"] for item in results}, {"escalated", "already_active"})
            self.assertEqual(len(projection.load_registry(current_path)["projections"]), 1)

    def test_ensure_timeout_rejects_invalid_time_and_pause_without_writing(self) -> None:
        """验证非法 UTC 时间、倒序时间和暂停秒数均不写文件。

        [参数] 无。
        [返回] None。
        最近修改时间：2026-07-25 00:00:00；改动原因：锁定失败路径的原文件保护。
        """
        # 1. 每组非法输入都使用同一成功标准：契约错误且原文件字节完全不变。
        invalid_cases = (
            ("invalid", "2026-07-25T00:10:01Z", 0),
            ("2026-07-25T00:00:00", "2026-07-25T00:10:01Z", 0),
            ("2026-07-25T00:10:02Z", "2026-07-25T00:10:01Z", 0),
            ("2026-07-25T00:00:00Z", "2026-07-25T00:10:01Z", -1),
            ("2026-07-25T00:00:00Z", "2026-07-25T00:10:01Z", 602),
        )
        for started_at, observed_at, paused_seconds in invalid_cases:
            with self.subTest(started_at=started_at, paused_seconds=paused_seconds), tempfile.TemporaryDirectory() as directory:
                current_path = self._write_current(Path(directory))
                before = current_path.read_bytes()
                with self.assertRaises(projection.ProjectionContractError):
                    projection.ensure_timeout_projection(
                        current_path,
                        started_at=started_at,
                        observed_at=observed_at,
                        paused_seconds=paused_seconds,
                        context=self._synthesis_context(trigger="timeout"),
                        session_id=self.TEST_SESSION_ID,
                    )
                self.assertEqual(current_path.read_bytes(), before)
        # 2. ensure-timeout 只接受 timeout 触发，continue 仍只属于显式恢复入口。
        with tempfile.TemporaryDirectory() as directory:
            current_path = self._write_current(Path(directory))
            before = current_path.read_bytes()
            with self.assertRaises(projection.ProjectionContractError):
                projection.ensure_timeout_projection(
                    current_path,
                    started_at="2026-07-25T00:00:00Z",
                    observed_at="2026-07-25T00:10:01Z",
                    context=self._synthesis_context(trigger="continue"),
                    session_id=self.TEST_SESSION_ID,
                )
            self.assertEqual(current_path.read_bytes(), before)

    def test_ensure_timeout_rejects_damaged_registry_without_writing(self) -> None:
        """验证损坏 registry 不得被当成无投影后覆盖。

        [参数] 无。
        [返回] None。
        最近修改时间：2026-07-25 00:00:00；改动原因：保护现有多会话 registry 的故障现场。
        """
        # 1. 构造 JSON 损坏的唯一托管区，超时入口必须非写入失败。
        with tempfile.TemporaryDirectory() as directory:
            current_path = self._write_current(
                Path(directory),
                "# 项目当前状态\n\n"
                + "\n".join((projection.BEGIN_MARKER, "```json", "{broken", "```", projection.END_MARKER)),
            )
            before = current_path.read_bytes()
            with self.assertRaises(projection.ProjectionContractError):
                projection.ensure_timeout_projection(
                    current_path,
                    started_at="2026-07-25T00:00:00Z",
                    observed_at="2026-07-25T00:10:01Z",
                    context=self._synthesis_context(trigger="timeout"),
                    session_id=self.TEST_SESSION_ID,
                )
            self.assertEqual(current_path.read_bytes(), before)

    def test_ensure_timeout_rejects_sensitive_context_and_oversized_result_without_writing(self) -> None:
        """验证敏感证据和超限候选都保持原文件不变。

        [参数] 无。
        [返回] None。
        最近修改时间：2026-07-25 00:00:00；改动原因：把隐私与 51,200 字节闸门覆盖到超时升级路径。
        """
        # 1. 上下文包含递归敏感字段时，在读取和写入 registry 前直接拒绝。
        with tempfile.TemporaryDirectory() as directory:
            current_path = self._write_current(Path(directory))
            before = current_path.read_bytes()
            sensitive_context = self._synthesis_context(trigger="timeout")
            sensitive_context["token"] = "不得持久化"
            with self.assertRaises(projection.ProjectionContractError):
                projection.ensure_timeout_projection(
                    current_path,
                    started_at="2026-07-25T00:00:00Z",
                    observed_at="2026-07-25T00:10:01Z",
                    context=sensitive_context,
                    session_id=self.TEST_SESSION_ID,
                )
            self.assertEqual(current_path.read_bytes(), before)
        # 2. 合成后的完整 PROJECT_CURRENT 超过上限时，原子写入前拒绝并保留原字节。
        with tempfile.TemporaryDirectory() as directory:
            current_path = self._write_current(Path(directory), "# 项目当前状态\n" + ("x" * 51_000))
            before = current_path.read_bytes()
            with self.assertRaises(projection.ProjectionContractError):
                projection.ensure_timeout_projection(
                    current_path,
                    started_at="2026-07-25T00:00:00Z",
                    observed_at="2026-07-25T00:10:01Z",
                    context=self._synthesis_context(
                        trigger="timeout", candidate_source_documents=["a.md", "b.md"]
                    ),
                    session_id=self.TEST_SESSION_ID,
                )
            self.assertEqual(current_path.read_bytes(), before)

    def test_ensure_timeout_cli_persists_payload_and_keeps_errors_non_destructive(self) -> None:
        """验证 ensure-timeout CLI 的成功输出和稳定错误码。

        [参数] 无。
        [返回] None。
        最近修改时间：2026-07-25 00:00:00；改动原因：覆盖真实子进程参数解析、持久化与错误模型。
        """
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            current_path = self._write_current(root)
            context_path = root / "timeout-context.json"
            context_path.write_text(
                json.dumps(
                    self._synthesis_context(
                        trigger="timeout", candidate_source_documents=["a.md", "b.md"]
                    ),
                    ensure_ascii=False,
                ),
                encoding="utf-8",
            )
            # 1. 真实 CLI 超过阈值后必须先持久化 fallback，再返回可用 payload。
            escalated = self._run_cli(
                "ensure-timeout",
                "--project-current",
                str(current_path),
                "--started-at",
                "2026-07-25T00:00:00Z",
                "--observed-at",
                "2026-07-25T00:15:02Z",
                "--paused-seconds",
                "301",
                "--input",
                str(context_path),
                "--session-id",
                "cli-timeout",
            )
            self.assertEqual(escalated.returncode, 0, escalated.stderr)
            escalated_output = json.loads(escalated.stdout)
            self.assertEqual(escalated_output["action"], "escalated")
            self.assertEqual(escalated_output["mode"], "fallback")
            self.assertIn("plan", escalated_output["payload"])
            # 2. 后续非法时间返回契约错误，且不得改写刚才已持久化的 registry。
            before = current_path.read_bytes()
            invalid = self._run_cli(
                "ensure-timeout",
                "--project-current",
                str(current_path),
                "--started-at",
                "invalid",
                "--observed-at",
                "2026-07-25T00:15:02Z",
                "--input",
                str(context_path),
                "--session-id",
                "cli-timeout",
            )
            self.assertEqual(invalid.returncode, 2)
            self.assertEqual(json.loads(invalid.stderr)["error"], "contract")
            self.assertEqual(current_path.read_bytes(), before)
            # 3. 缺少必填 session_id 时 argparse 返回 2，且同样不能改写现有 registry。
            missing_required = self._run_cli(
                "ensure-timeout",
                "--project-current",
                str(current_path),
                "--started-at",
                "2026-07-25T00:00:00Z",
                "--observed-at",
                "2026-07-25T00:10:01Z",
                "--input",
                str(context_path),
            )
            self.assertEqual(missing_required.returncode, 2)
            self.assertEqual(current_path.read_bytes(), before)

    def test_deactivate_completes_steps_atomically(self) -> None:
        """[参数] 无；[返回] None；最近修改时间：2026-07-23；改动原因：最后一步完成和失活不留中间态。"""
        # 1. 写入含进行中步骤的活动投影，再执行单次失活迁移。
        with tempfile.TemporaryDirectory() as directory:
            path = self._write_current(Path(directory))
            projection.upsert_projection(path, self._sample(("completed", "in_progress")), session_id=self.TEST_SESSION_ID)
            result = projection.deactivate_projection(
                path, session_id=self.TEST_SESSION_ID, updated_at="2026-07-23T02:00:00Z"
            )
            # 2. 所有步骤必须完成，且失活结果不能生成 UI payload。
            self.assertEqual(result["state"], "inactive")
            self.assertTrue(all(step["status"] == "completed" for step in result["steps"]))
            with self.assertRaises(projection.ProjectionContractError):
                projection.build_update_plan_payload(result)

    def test_cli_subcommands_and_exit_codes(self) -> None:
        """[参数] 无；[返回] None；最近修改时间：2026-07-26 00:00:00；改动原因：验证会话回退和 payload 返回后的全部 CLI 入口。"""
        # 1. 准备临时状态文件和合法 JSON，通过 write 初始化活动投影。
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            path = self._write_current(root)
            input_path = root / "projection.json"
            input_path.write_text(json.dumps(self._sample(), ensure_ascii=False), encoding="utf-8")
            write_result = self._run_cli("write", "--project-current", str(path), "--input", str(input_path), "--session-id", "legacy/default")
            self.assertEqual(write_result.returncode, 0, write_result.stderr)
            # 2. 顺序验证读取、payload、指纹和失活四个真实命令。
            self.assertEqual(self._run_cli("validate", "--project-current", str(path), "--session-id", "legacy/default").returncode, 0)
            payload_result = self._run_cli("payload", "--project-current", str(path), "--session-id", "legacy/default")
            self.assertEqual(payload_result.returncode, 0, payload_result.stderr)
            self.assertIn("plan", json.loads(payload_result.stdout))
            source_dir = root / "doc" / "3-实施"
            source_dir.mkdir(parents=True)
            source_path = source_dir / "plan.md"
            source_path.write_text(
                "- [TASK-SYN-01] 冻结补建契约\n- [TASK-SYN-02] 实现补建引擎\n",
                encoding="utf-8",
            )
            synthesis_input = root / "synthesis.json"
            synthesis_input.write_text(
                json.dumps(self._synthesis_context(), ensure_ascii=False),
                encoding="utf-8",
            )
            synthesize_result = self._run_cli(
                "synthesize",
                "--project-current",
                str(path),
                "--input",
                str(synthesis_input),
                "--session-id",
                "legacy/default",
            )
            self.assertEqual(synthesize_result.returncode, 0, synthesize_result.stderr)
            self.assertIn("mode", json.loads(synthesize_result.stdout))
            fingerprint_result = self._run_cli("fingerprint", "--input", str(input_path))
            self.assertEqual(fingerprint_result.returncode, 0, fingerprint_result.stderr)
            deactivate_result = self._run_cli(
                "deactivate",
                "--project-current",
                str(path),
                "--session-id",
                "legacy/default",
                "--updated-at",
                "2026-07-23T02:00:00Z",
            )
            self.assertEqual(deactivate_result.returncode, 0, deactivate_result.stderr)
            self.assertEqual(json.loads(deactivate_result.stdout)["projection"]["state"], "inactive")
            # 3. 契约输入和缺失文件分别返回稳定的 2、3 退出码。
            damaged_path = root / "damaged.json"
            damaged_path.write_text("{}", encoding="utf-8")
            contract_result = self._run_cli("write", "--project-current", str(path), "--input", str(damaged_path), "--session-id", "legacy/default")
            self.assertEqual(contract_result.returncode, 2)
            missing_result = self._run_cli("validate", "--project-current", str(root / "missing.md"), "--session-id", "legacy/default")
            self.assertEqual(missing_result.returncode, 3)

    def test_v4_registry_keeps_two_sessions_and_interleaved_upserts(self) -> None:
        """验证两个会话可在同一托管区并存，交错写入不会互相覆盖。"""
        # 1. 交错写入两个会话，再分别读取验证注册表没有丢失更新。
        with tempfile.TemporaryDirectory() as directory:
            path = self._write_current(Path(directory))
            session_a = "thread-alpha"
            session_b = "thread-beta"
            entry_a = self._sample_v4_projection(session_a)
            entry_b = self._sample_v4_projection(session_b)

            projection.upsert_projection(path, entry_a, session_id=session_a)
            projection.upsert_projection(path, entry_b, session_id=session_b)
            entry_a_updated = self._sample_v4_projection(session_a, ("completed", "completed", "in_progress"))
            projection.upsert_projection(path, entry_a_updated, session_id=session_a)

            registry = projection.load_registry(path)
            self.assertEqual(registry["version"], 4)
            self.assertEqual(
                {item["session_id"] for item in registry["projections"]},
                {session_a, session_b},
            )
            loaded_a = projection.load_projection(path, session_id=session_a)
            loaded_b = projection.load_projection(path, session_id=session_b)
            self.assertEqual(loaded_a["steps"][-1]["status"], "in_progress")
            self.assertEqual(loaded_b["steps"][1]["status"], "in_progress")
            self.assertNotEqual(loaded_a["steps"][0]["id"], loaded_b["steps"][0]["id"])

    def test_payload_and_deactivate_are_scoped_to_session(self) -> None:
        """验证 payload 与失活只操作指定会话投影。"""
        # 1. 建立两个会话，验证 payload 和失活都只作用于目标会话。
        with tempfile.TemporaryDirectory() as directory:
            path = self._write_current(Path(directory))
            session_a = "session-a"
            session_b = "session-b"
            projection.upsert_projection(path, self._sample_v4_projection(session_a), session_id=session_a)
            projection.upsert_projection(path, self._sample_v4_projection(session_b), session_id=session_b)

            payload_a = projection.build_update_plan_payload(
                projection.load_projection(path, session_id=session_a)
            )
            self.assertTrue(all("SESSION-A" in item["step"] for item in payload_a["plan"]))
            self.assertFalse(any("SESSION-B" in item["step"] for item in payload_a["plan"]))

            deactivated_b = projection.deactivate_projection(
                path,
                session_id=session_b,
                updated_at="2026-07-25T02:00:00Z",
            )
            self.assertEqual(deactivated_b["state"], "inactive")
            self.assertEqual(projection.load_projection(path, session_id=session_a)["state"], "active")
            self.assertEqual(projection.load_projection(path, session_id=session_b)["state"], "inactive")

    def test_goal_events_are_isolated_by_session(self) -> None:
        """验证 Goal 生命周期只迁移当前会话的安全投影。"""
        # 1. 分别创建两个会话的 Goal，再只阻断其中一个。
        with tempfile.TemporaryDirectory() as directory:
            path = self._write_current(Path(directory))
            session_a = "goal-a"
            session_b = "goal-b"
            created_a = projection.handle_goal_event(path, "create", session_id=session_a)
            created_b = projection.handle_goal_event(path, "create", session_id=session_b)
            self.assertEqual(created_a["action"], "created")
            self.assertEqual(created_b["action"], "created")
            self.assertEqual(
                {item["session_id"] for item in projection.load_registry(path)["projections"]},
                {session_a, session_b},
            )

            blocked_a = projection.handle_goal_event(path, "blocked", session_id=session_a)
            self.assertEqual(blocked_a["projection"]["state"], "blocked")
            self.assertEqual(projection.load_projection(path, session_id=session_b)["state"], "active")

    def test_v1_v3_migrate_wraps_legacy_projection_without_loss(self) -> None:
        """验证 v1-v3 单投影迁移为 v4 注册表且保留原任务字段。"""
        # 1. 逐个迁移 v1、v2、v3 样本，核对版本与任务指纹均被保留。
        legacy_v1 = self._sample()
        legacy_v2 = self._sample_v2()
        legacy_v3 = dict(legacy_v2)
        legacy_v3["version"] = 3
        for legacy in (legacy_v1, legacy_v2, legacy_v3):
            with self.subTest(version=legacy["version"]), tempfile.TemporaryDirectory() as directory:
                # 将迁移入口作用于仍为 legacy 的文件，避免把写入升级与 migrate 混为一谈。
                path = self._write_legacy_projection(Path(directory), legacy)
                migration = self._run_cli(
                    "migrate", "--project-current", str(path), "--session-id", "legacy-session"
                )
                self.assertEqual(migration.returncode, 0, migration.stderr)
                migrated = projection.load_registry(path)
                self.assertEqual(migrated["version"], 4)
                self.assertEqual(len(migrated["projections"]), 1)
                self.assertEqual(migrated["projections"][0]["session_id"], "legacy-session")
                self.assertEqual(
                    migrated["projections"][0]["plan_fingerprint"],
                    legacy["plan_fingerprint"],
                )

    def test_active_legacy_projection_requires_session_id_but_inactive_remains_readable(self) -> None:
        """验证旧版活动投影不能在缺少会话归属时恢复，失活单投影仍可只读。

        [参数] 无。
        [返回] None：断言旧格式活动与失活投影的会话归属边界。
        最近修改时间：2026-07-26 00:00:00；改动原因：覆盖旧格式读取与显式 session 兼容边界。
        """
        # 1. 活动旧投影必须拒绝无归属恢复，失活旧投影仍允许只读兼容。
        active_v1 = self._sample()
        active_v2 = self._sample_v2()
        active_v3 = dict(active_v2)
        active_v3["version"] = 3
        inactive_v1 = self._sample(("completed",), state="inactive")
        inactive_v2 = self._sample_v2(("completed",))
        inactive_v3 = dict(inactive_v2)
        inactive_v3["version"] = 3

        for legacy in (active_v1, active_v2, active_v3):
            with self.subTest(version=legacy["version"], state="active"), tempfile.TemporaryDirectory() as directory:
                path = self._write_legacy_projection(Path(directory), legacy)
                with self.assertRaises(projection.ProjectionContractError):
                    projection.load_projection(path)
                with self.assertRaises(projection.ProjectionContractError):
                    projection.load_registry(path)

        for legacy in (inactive_v1, inactive_v2, inactive_v3):
            with self.subTest(version=legacy["version"], state="inactive"), tempfile.TemporaryDirectory() as directory:
                path = self._write_legacy_projection(Path(directory), legacy)
                self.assertEqual(
                    projection.load_projection(path, session_id=self.TEST_SESSION_ID)["state"],
                    "inactive",
                )
                registry = projection.load_registry(path, session_id=self.TEST_SESSION_ID)
                self.assertEqual(registry["projections"][0]["state"], "inactive")

    def test_registry_rejects_duplicate_session_id(self) -> None:
        """验证每个会话最多保存一个当前投影。"""
        # 1. 构造同一会话的两个不同计划，确认注册表拒绝重复归属。
        session_id = "duplicate-session"
        first = self._sample_v4_entry(session_id)
        second_projection = self._sample_v4_projection(session_id)
        second_projection["plan_key"] = "REQ-RTP-DUPLICATE/CYCLE-RTP-02"
        second = {
            "projection_id": projection.compute_projection_id(session_id, second_projection),
            "session_id": session_id,
            "projection_origin": second_projection["projection_origin"],
            "synthesis_mode": second_projection["synthesis_mode"],
            "state": second_projection["state"],
            "plan_key": second_projection["plan_key"],
            "source_document": second_projection["source_document"],
            "plan_fingerprint": second_projection["plan_fingerprint"],
            "updated_at": second_projection["updated_at"],
            "steps": second_projection["steps"],
        }
        registry = {
            "version": 4,
            "registry_schema": "task_plan_projection_registry",
            "registry_updated_at": "2026-07-25T00:00:00Z",
            "projections": [first, second],
        }
        self.assertNotEqual(first["projection_id"], second["projection_id"])
        with self.assertRaises(projection.ProjectionContractError):
            projection.validate_registry(registry)

    def test_session_id_is_allowed_only_in_controlled_field(self) -> None:
        """验证原始 session_id 可保存，其它敏感字段仍被递归拒绝。"""
        # 1. 受控 session_id 可通过校验，其它敏感字段必须拒绝。
        entry = self._sample_v4_entry("raw-thread-id")
        registry = {
            "version": 4,
            "registry_schema": "task_plan_projection_registry",
            "registry_updated_at": "2026-07-25T00:00:00Z",
            "projections": [entry],
        }
        self.assertEqual(projection.validate_registry(registry)["projections"][0]["session_id"], "raw-thread-id")
        for field in ("thread_id", "prompt", "response", "token", "api_key", "password", "secret", "private_key"):
            candidate = json.loads(json.dumps(registry, ensure_ascii=False))
            candidate["projections"][0][field] = "不得持久化"
            with self.subTest(field=field), self.assertRaises(projection.ProjectionContractError):
                projection.validate_registry(candidate)

    def test_cli_requires_session_id_for_registry_operations(self) -> None:
        """验证 CLI 的 validate/write/payload/deactivate/goal 均按 session_id 定位。"""
        # 1. 所有状态相关 CLI 都显式传入 session_id，并验证命令链路成功。
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            path = self._write_current(root)
            input_path = root / "projection.json"
            input_path.write_text(json.dumps(self._sample(), ensure_ascii=False), encoding="utf-8")
            write = self._run_cli(
                "write", "--project-current", str(path), "--input", str(input_path), "--session-id", "cli-a"
            )
            self.assertEqual(write.returncode, 0, write.stderr)
            self.assertEqual(
                self._run_cli("validate", "--project-current", str(path), "--session-id", "cli-a").returncode,
                0,
            )
            payload = self._run_cli("payload", "--project-current", str(path), "--session-id", "cli-a")
            self.assertEqual(payload.returncode, 0, payload.stderr)
            deactivate = self._run_cli(
                "deactivate", "--project-current", str(path), "--session-id", "cli-a"
            )
            self.assertEqual(deactivate.returncode, 0, deactivate.stderr)
            goal = self._run_cli(
                "goal", "--project-current", str(path), "--event", "create", "--session-id", "cli-b"
            )
            self.assertEqual(goal.returncode, 0, goal.stderr)

    def test_state_changing_python_api_requires_session_id(self) -> None:
        """验证 Python 状态变更入口不再静默写入 legacy/default 会话。

        [参数] 无。
        [返回] None。
        最近修改时间：2026-07-26 00:00:00；改动原因：补充 synthesize 入口缺失会话的失败关闭断言。
        """
        # 1. 缺少 session_id 的 Python 状态变更入口必须返回契约错误。
        with tempfile.TemporaryDirectory() as directory:
            path = self._write_current(Path(directory))
            with self.assertRaises(projection.ProjectionContractError):
                projection.upsert_projection(path, self._sample())
            with self.assertRaises(projection.ProjectionContractError):
                projection.handle_goal_event(path, "create")
            with self.assertRaises(projection.ProjectionContractError):
                projection.deactivate_projection(path)
            with self.assertRaises(projection.ProjectionContractError):
                projection.render_projection_block(self._sample())
            with self.assertRaises(projection.ProjectionContractError):
                projection.synthesize_projection(path, self._synthesis_context())

    def test_ensure_start_persists_then_returns_payload_for_current_session(self) -> None:
        """验证首次持久化和悬浮任务 payload 在同一入口完成。

        [参数] 无。
        [返回] None：断言当前会话先写盘并返回可同步 payload。
        最近修改时间：2026-07-26 00:00:00；改动原因：覆盖首次持久化即悬浮窗同步契约。
        """
        # 1. 用合法活动投影执行 ensure-start，并核对返回 payload 与磁盘内容一致。
        with tempfile.TemporaryDirectory() as directory:
            path = self._write_current(Path(directory))
            result = projection.ensure_start_projection(
                path,
                self._sample(),
                session_id=self.TEST_SESSION_ID,
            )
            self.assertEqual(result["action"], "created")
            self.assertEqual(result["session_id"], self.TEST_SESSION_ID)
            self.assertTrue(result["payload"]["plan"])
            persisted = projection.load_projection(path, session_id=self.TEST_SESSION_ID)
            self.assertEqual(result["payload"], projection.build_update_plan_payload(persisted))

    def test_ensure_start_isolated_from_other_session_and_idempotent(self) -> None:
        """验证其它会话不阻断当前会话创建，当前会话重复调用只恢复 payload。

        [参数] 无。
        [返回] None：断言多会话隔离和重复调用幂等。
        最近修改时间：2026-07-26 00:00:00；改动原因：防止首次投影覆盖其它宿主会话。
        """
        # 1. 先写入其它会话，再重复创建当前会话，确认 registry 和字节内容均受保护。
        with tempfile.TemporaryDirectory() as directory:
            path = self._write_current(Path(directory))
            projection.upsert_projection(path, self._sample_v4_projection("other-session"), session_id="other-session")
            first = projection.ensure_start_projection(path, self._sample(), session_id=self.TEST_SESSION_ID)
            before_repeat = path.read_bytes()
            second = projection.ensure_start_projection(path, self._sample(("pending", "in_progress", "pending")), session_id=self.TEST_SESSION_ID)
            self.assertEqual(first["action"], "created")
            self.assertEqual(second["action"], "already_active")
            self.assertEqual(path.read_bytes(), before_repeat)
            registry = projection.load_registry(path)
            self.assertEqual(
                {entry["session_id"] for entry in registry["projections"]},
                {"other-session", self.TEST_SESSION_ID},
            )

    def test_session_resolution_prefers_explicit_and_fails_conflict_or_missing(self) -> None:
        """验证显式会话优先、环境回退、冲突和缺失均失败关闭。

        [参数] 无。
        [返回] None：断言会话来源冲突和缺失均不写盘。
        最近修改时间：2026-07-26 00:00:00；改动原因：锁定显式 session 与宿主环境的失败关闭边界。
        """
        # 1. 依次构造显式/环境、冲突和缺失输入，观察归属与原子保护结果。
        with tempfile.TemporaryDirectory() as directory:
            path = self._write_current(Path(directory))
            with mock.patch.dict(os.environ, {projection.SESSION_ENV_NAME: "env-session"}, clear=False):
                with self.assertRaises(projection.ProjectionContractError):
                    projection.ensure_start_projection(path, self._sample(), session_id="explicit-session")
                result = projection.ensure_start_projection(path, self._sample())
                self.assertEqual(result["session_id"], "env-session")
            path_without_session = self._write_current(Path(directory), "# 新文件\n")
            with self.assertRaises(projection.ProjectionContractError):
                projection.ensure_start_projection(path_without_session, self._sample())

    def test_cli_state_entry_uses_environment_session_and_rejects_conflict(self) -> None:
        """验证 CLI 缺省参数回退宿主会话，冲突时保持文件不变。

        [参数] 无。
        [返回] None：断言 CLI 使用环境会话并在冲突时失败关闭。
        最近修改时间：2026-07-26 00:00:00；改动原因：覆盖 CLI 会话解析与原文件哈希保护。
        """
        # 1. 先验证环境回退成功，再以冲突显式值确认 CLI 不写入原文件。
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            path = self._write_current(root)
            input_path = root / "projection.json"
            input_path.write_text(json.dumps(self._sample(), ensure_ascii=False), encoding="utf-8")
            with mock.patch.dict(os.environ, {projection.SESSION_ENV_NAME: "env-cli"}, clear=False):
                write = self._run_cli(
                    "write",
                    "--project-current",
                    str(path),
                    "--input",
                    str(input_path),
                )
                self.assertEqual(write.returncode, 0, write.stderr)
                self.assertEqual(
                    projection.load_projection(path, session_id="env-cli")["state"],
                    "active",
                )
                before_conflict = path.read_bytes()
                conflict = self._run_cli(
                    "write",
                    "--project-current",
                    str(path),
                    "--input",
                    str(input_path),
                    "--session-id",
                    "explicit-cli",
                )
                self.assertNotEqual(conflict.returncode, 0)
                self.assertEqual(path.read_bytes(), before_conflict)

    def test_ensure_start_context_builds_fallback_and_cli_write_returns_payload(self) -> None:
        """验证 start 上下文可生成 fallback，write CLI 在持久化后直接返回 payload。

        [参数] 无。
        [返回] None：断言 start 补建与 write 返回值均可直接同步 UI。
        最近修改时间：2026-07-26 00:00:00；改动原因：覆盖首次上下文入口和兼容 write payload。
        """
        # 1. 用缺少来源文档的 start 上下文走安全 fallback，再核对 write CLI payload。
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            path = self._write_current(root)
            context = self._synthesis_context(
                trigger="start",
                current_step_hint=None,
                candidate_source_documents=[],
            )
            result = projection.ensure_start_projection(path, context, session_id=self.TEST_SESSION_ID)
            self.assertEqual(result["action"], "created")
            self.assertEqual(result["mode"], "fallback")
            self.assertEqual(result["payload"]["plan"][0]["status"], "in_progress")

            input_path = root / "projection.json"
            input_path.write_text(json.dumps(self._sample(), ensure_ascii=False), encoding="utf-8")
            write = self._run_cli(
                "write",
                "--project-current",
                str(path),
                "--input",
                str(input_path),
                "--session-id",
                "cli-payload",
            )
            self.assertEqual(write.returncode, 0, write.stderr)
            write_output = json.loads(write.stdout)
            self.assertTrue(write_output["payload"]["plan"])

    def test_deactivate_and_goal_complete_return_one_time_completion_payload(self) -> None:
        """验证失活与 Goal 完成均返回全完成收口 payload，失活后不可重放。

        [参数] 无。
        [返回] None：断言完成 payload 一次性返回且终态不可再次刷新。
        最近修改时间：2026-07-26 00:00:00；改动原因：覆盖完成收口与 inactive 重放保护。
        """
        # 1. 通过 CLI 完成失活并检查全完成 payload，随后验证 inactive 不再生成 UI payload。
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            path = self._write_current(root)
            projection.upsert_projection(path, self._sample(), session_id=self.TEST_SESSION_ID)
            input_path = root / "projection.json"
            input_path.write_text(json.dumps(self._sample(), ensure_ascii=False), encoding="utf-8")
            result = self._run_cli(
                "deactivate",
                "--project-current",
                str(path),
                "--session-id",
                self.TEST_SESSION_ID,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            output = json.loads(result.stdout)
            self.assertEqual(output["projection"]["state"], "inactive")
            self.assertTrue(output["payload"])
            self.assertTrue(all(item["status"] == "completed" for item in output["payload"]["plan"]))
            with self.assertRaises(projection.ProjectionContractError):
                projection.build_update_plan_payload(output["projection"])

    def test_continue_route_is_mandatory_in_hit_check(self) -> None:
        """[参数] 无；[返回] None；最近修改时间：2026-07-24；改动原因：防止继续回合漏命中恢复 Owner。"""
        # 1. 总控入口与命中清单都必须直接声明继续类消息的恢复路由。
        hit_skill = (REPOSITORY_ROOT / "skill-hit-check-rules" / "SKILL.md").read_text(encoding="utf-8")
        hit_checklist = (
            REPOSITORY_ROOT / "skill-hit-check-rules" / "references" / "hit-checklist.md"
        ).read_text(encoding="utf-8")
        for document in (hit_skill, hit_checklist):
            self.assertIn("task-plan-rehydration-rules", document)
            self.assertIn("PROJECT_CURRENT.md", document)
            self.assertIn("继续", document)
            self.assertIn("update_plan", document)
        for phrase in ("接着做", "接着执行", "恢复任务", "恢复执行", "按原计划继续", "继续上次任务", "往下做", "继续刚才的工作"):
            self.assertIn(phrase, hit_skill)
            self.assertIn(phrase, hit_checklist)

    def test_documented_cli_uses_real_project_current_option(self) -> None:
        """[参数] 无；[返回] None；最近修改时间：2026-07-24；改动原因：锁定可执行恢复命令。"""
        # 1. 恢复 Owner 文档必须使用解析器真实提供的参数名，避免命中后执行失败。
        skill_document = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("validate --project-current PROJECT_CURRENT.md", skill_document)
        self.assertIn("ensure-start --project-current PROJECT_CURRENT.md", skill_document)
        self.assertIn("payload --project-current PROJECT_CURRENT.md", skill_document)
        self.assertIn("synthesize --project-current PROJECT_CURRENT.md --input synthesis_context.json", skill_document)
        self.assertIn("goal --project-current PROJECT_CURRENT.md --event create", skill_document)
        self.assertNotIn("--file PROJECT_CURRENT.md", skill_document)

    def test_goal_lifecycle_route_documents_keep_order_and_plan_mode_boundary(self) -> None:
        """验证 Goal 生命周期文档锁定 Owner、持久化顺序与 Plan Mode 边界。

        [参数] 无。
        [返回] None。
        最近修改时间：2026-07-25 00:00:00；改动原因：防止 Goal 路由漏交接、UI 先于持久化刷新或 Plan Mode 越界。
        """
        # 1. 任务投影 Owner 必须覆盖三个 Goal 工具，并明确先落盘再刷新 UI。
        rehydration_document = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        contract_document = (ROOT / "references" / "task-plan-projection-contract.md").read_text(encoding="utf-8")
        for token in ("create_goal", "get_goal", "update_goal", "先持久化", "Plan Mode"):
            self.assertIn(token, rehydration_document)
        self.assertIn("成功持久化 -> 读取返回 payload -> 下一动作调用 `update_plan`", contract_document)
        # 2. 自主执行 Owner 只能交接生命周期，不得借悬浮窗扩大执行授权。
        autonomous_document = (REPOSITORY_ROOT / "autonomous-execution-rules" / "SKILL.md").read_text(encoding="utf-8")
        for token in ("create_goal", "get_goal", "update_goal", "不因此自动取得", "不得把 blocked payload", "Plan Mode"):
            self.assertIn(token, autonomous_document)

    def test_contract_document_mentions_version_three_goal_and_synthesize(self) -> None:
        """验证契约文档锁定 v3 Goal 与补建 CLI。

        [参数] 无。
        [返回] None。
        最近修改时间：2026-07-25 00:00:00；改动原因：防止 Goal 生命周期命令或 Plan Mode 安全边界从文档契约中丢失。
        """
        # 1. v3 字段、固定 Goal 身份和四个 CLI 事件必须在公开契约中可追溯。
        contract_document = (ROOT / "references" / "task-plan-projection-contract.md").read_text(encoding="utf-8")
        self.assertIn("projection_origin", contract_document)
        self.assertIn("synthesis_mode", contract_document)
        self.assertIn("SYNTH-FALLBACK/", contract_document)
        self.assertIn("GOAL/ACTIVE", contract_document)
        self.assertIn("goal_default", contract_document)
        self.assertIn("fallback 只是恢复兜底，替换为 Goal 固定安全三步", contract_document)
        for event in ("create", "restore", "blocked", "complete"):
            self.assertIn(f"goal --project-current PROJECT_CURRENT.md --event {event}", contract_document)
        self.assertIn("Plan Mode 不读取、写入或刷新投影", contract_document)
        self.assertIn("synthesize --project-current PROJECT_CURRENT.md --input synthesis_context.json", contract_document)
        self.assertIn("ensure-start", contract_document)
        self.assertIn("CODEX_THREAD_ID", contract_document)

    def test_auto_goal_timeout_contract_is_consistent(self) -> None:
        """验证超时 Goal 优先、单次创建、脱敏摘要和普通投影降级在所有 Owner 入口一致。"""
        documents = {
            "owner": (ROOT / "SKILL.md").read_text(encoding="utf-8"),
            "contract": (ROOT / "references" / "task-plan-projection-contract.md").read_text(encoding="utf-8"),
            "agent": (ROOT / "agents" / "openai.yaml").read_text(encoding="utf-8"),
            "autonomous": (REPOSITORY_ROOT / "autonomous-execution-rules" / "SKILL.md").read_text(encoding="utf-8"),
            "pause": (
                REPOSITORY_ROOT / "autonomous-execution-rules" / "references" / "continuation-and-pause.md"
            ).read_text(encoding="utf-8"),
            "agents_rules": (REPOSITORY_ROOT / "AGENTS.md").read_text(encoding="utf-8"),
            "claude_rules": (REPOSITORY_ROOT / "CLAUDE.md").read_text(encoding="utf-8"),
        }
        for name, document in documents.items():
            with self.subTest(document=name):
                self.assertIn("probe-timeout", document)
                self.assertIn("get_goal", document)
                self.assertIn("create_goal", document)
                self.assertIn("ensure-timeout", document)
                self.assertIn("600 秒", document)
                self.assertIn("Plan Mode", document)
        for name in ("owner", "contract", "agent", "agents_rules", "claude_rules"):
            with self.subTest(summary_document=name):
                self.assertIn("80", documents[name])
                self.assertIn("脱敏", documents[name])
        self.assertIn("完成当前已确认的长任务并完成验证收口", documents["owner"])
        self.assertIn("完成当前已确认的长任务并完成验证收口", documents["contract"])
        self.assertIn("只允许再调用一次 `get_goal`", documents["owner"])
        self.assertIn("禁止无变化重试 `create_goal`", documents["owner"])
        self.assertIn("子 Agent 不得调用", documents["owner"])

    def test_platform_rules_and_bootstrap_keep_continue_route(self) -> None:
        """[参数] 无；[返回] None；最近修改时间：2026-07-24；改动原因：防止受管平台规则遗漏恢复路由。"""
        # 1. Codex、Claude 与自举模板必须同步继续类消息的恢复前置条件。
        documents = (
            REPOSITORY_ROOT / "AGENTS.md",
            REPOSITORY_ROOT / "CLAUDE.md",
            REPOSITORY_ROOT / "project-rule-file-bootstrap-rules" / "scripts" / "bootstrap_agents.sh",
        )
        for document_path in documents:
            document = document_path.read_text(encoding="utf-8")
            self.assertIn("task-plan-rehydration-rules", document)
            self.assertIn("首条命中列表", document)
            self.assertIn("任意“继续”或恢复意图", document)
            self.assertIn("update_plan", document)

    def test_plan_mode_does_not_rehydrate_task_list(self) -> None:
        """验证 Plan Mode 不读取投影或重建任务悬浮窗。

        [参数] 无。
        [返回] None。
        最近修改时间：2026-07-24 02:08:25；改动原因：覆盖规划阶段与执行阶段的任务悬浮窗边界。
        """
        # 1. 读取恢复 Owner、总控路由和平台规则的全部受影响入口。
        rehydration_skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        documents = (
            rehydration_skill,
            (REPOSITORY_ROOT / "skill-hit-check-rules" / "SKILL.md").read_text(encoding="utf-8"),
            (REPOSITORY_ROOT / "skill-hit-check-rules" / "references" / "hit-checklist.md").read_text(
                encoding="utf-8"
            ),
            (REPOSITORY_ROOT / "AGENTS.md").read_text(encoding="utf-8"),
            (REPOSITORY_ROOT / "CLAUDE.md").read_text(encoding="utf-8"),
        )
        # 2. Plan Mode 必须明确禁止读取投影、调用 update_plan 与创建悬浮窗。
        for document in documents:
            self.assertIn("Plan Mode", document)
            self.assertIn("不读取", document)
            self.assertIn("update_plan", document)
        # 3. 实施规划规则仍保留用户选择流程，不能因恢复规则放宽。
        planning_coverage = (
            REPOSITORY_ROOT / "implementation-planning-rules" / "references" / "plan-question-coverage.md"
        ).read_text(encoding="utf-8")
        self.assertIn("request_user_input", planning_coverage)


if __name__ == "__main__":
    unittest.main(verbosity=2)
