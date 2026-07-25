"""任务投影脚本的单元和 CLI 契约测试。"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
REPOSITORY_ROOT = ROOT.parent
SCRIPT = ROOT / "scripts" / "task_plan_projection.py"
SPEC = importlib.util.spec_from_file_location("task_plan_projection", SCRIPT)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError("unable to load task_plan_projection.py")
projection = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(projection)


class TaskPlanProjectionTests(unittest.TestCase):
    """验证托管区、状态、原子写入和 CLI 契约。"""

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
        最近修改时间：2026-07-25；改动原因：覆盖 Goal 安全三步、阻断和完成迁移。
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

    # _write_current 创建带普通正文的临时 PROJECT_CURRENT.md。
    # [参数] root: 临时目录；text: 初始正文。
    # [返回] Path：创建的文件路径。
    # 最近修改时间：2026-07-23；改动原因：复用用户正文保护样本。
    def _write_current(self, root: Path, text: str = "# 项目当前状态\n\n用户正文。\n") -> Path:
        """创建带普通正文的临时 PROJECT_CURRENT.md。"""
        path = root / "PROJECT_CURRENT.md"
        path.write_text(text, encoding="utf-8", newline="")
        return path

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
        current_step_hint: str | None = "TASK-SYN-02",
        completed_step_hints: list[str] | None = None,
        candidate_source_documents: list[str] | None = None,
        conflicts: list[str] | None = None,
    ) -> dict[str, object]:
        """构造 synthesize 输入上下文。"""
        return {
            "trigger": "continue",
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
                projection.upsert_projection(path, self._sample(statuses, state=state))
                loaded = projection.load_projection(path)
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
            projection.upsert_projection(path, self._sample())
            first = path.read_bytes()
            self.assertTrue(first.startswith(original.encode("utf-8")))
            # 2. 再次更新只替换唯一托管区，不重复标记或删除用户内容。
            projection.upsert_projection(path, self._sample(("completed", "in_progress")))
            second = path.read_text(encoding="utf-8")
            self.assertEqual(second.count(projection.BEGIN_MARKER), 1)
            self.assertIn("用户正文。", second)
            self.assertIn('"version": 3', second)

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
                projection.upsert_projection(path, self._sample())
            self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), before)
            # 2. 原子替换失败时保留原正文并清理同目录临时文件。
            path.write_text("用户正文\n", encoding="utf-8")
            before_bytes = path.read_bytes()
            with mock.patch.object(projection.os, "replace", side_effect=OSError("boom")):
                with self.assertRaises(projection.ProjectionIOError):
                    projection.upsert_projection(path, self._sample())
            self.assertEqual(path.read_bytes(), before_bytes)
            self.assertEqual(list(root.glob(".PROJECT_CURRENT.md.*.tmp")), [])

    def test_exact_file_size_limit_is_allowed(self) -> None:
        """[参数] 无；[返回] None；最近修改时间：2026-07-23；改动原因：锁定 51,200 字节闭区间边界。"""
        # 1. 根据渲染块长度构造恰好命中 51,200 字节的候选全文。
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            sample = self._sample()
            block = projection.render_projection_block(sample, "\n")
            prefix_length = projection.MAX_FILE_BYTES - len(block.encode("utf-8")) - 2
            path = self._write_current(root, "x" * prefix_length)
            # 2. 边界值允许写入，最终文件大小必须精确相等。
            projection.upsert_projection(path, sample)
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
        最近修改时间：2026-07-25；改动原因：防止 Goal 原文或运行时身份被持久化到悬浮窗投影。
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
        最近修改时间：2026-07-25；改动原因：锁定 blocked 无进行中步骤和 complete 无 payload 的安全边界。
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
        最近修改时间：2026-07-25；改动原因：锁定四个 Goal 事件、正式最小任务优先和 fallback 安全列表让位。
        """
        # 1. 新建、恢复、阻断和完成必须只迁移固定安全三步，并以 inactive 终止重放。
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            path = self._write_current(root)
            created = projection.handle_goal_event(path, "create")
            self.assertEqual(created["action"], "created")
            self.assertEqual(created["projection"]["version"], 3)
            self.assertEqual(created["projection"]["steps"][0]["status"], "in_progress")
            before_restore = path.read_bytes()
            restored = projection.handle_goal_event(path, "restore")
            self.assertEqual(restored["action"], "restored")
            self.assertEqual(path.read_bytes(), before_restore)
            blocked = projection.handle_goal_event(path, "blocked")
            self.assertEqual(blocked["projection"]["state"], "blocked")
            self.assertNotIn("in_progress", [item["status"] for item in blocked["projection"]["steps"]])
            with self.assertRaises(projection.ProjectionContractError):
                projection.handle_goal_event(path, "restore")
            completed = projection.handle_goal_event(path, "complete")
            self.assertEqual(completed["payload"], None)
            self.assertEqual(completed["projection"]["state"], "inactive")
            self.assertTrue(all(item["status"] == "completed" for item in completed["projection"]["steps"]))
            # 2. 活动 persisted 正式计划必须被保护，Goal 创建不能覆盖真实实施任务。
            projection.upsert_projection(path, self._sample())
            formal_before = path.read_bytes()
            preserved = projection.handle_goal_event(path, "create")
            self.assertEqual(preserved["action"], "preserved_formal")
            self.assertEqual(path.read_bytes(), formal_before)
            # 3. 正式计划不关联 Goal 默认三步，后续 Goal 事件必须无副作用地保持真实实施任务。
            for event in ("restore", "blocked", "complete"):
                preserved_after_event = projection.handle_goal_event(path, event)
                self.assertEqual(preserved_after_event["action"], "preserved_formal")
                self.assertIsNone(preserved_after_event["payload"])
                self.assertEqual(path.read_bytes(), formal_before)
            # 4. synthesized fallback 仅是恢复兜底，创建 Goal 时必须替换为 Goal 安全三步。
            fallback = self._sample_v2(("in_progress", "pending", "pending"), synthesis_mode="fallback")
            projection.upsert_projection(path, fallback)
            created_from_fallback = projection.handle_goal_event(path, "create")
            self.assertEqual(created_from_fallback["action"], "created")
            self.assertEqual(created_from_fallback["projection"]["projection_origin"], "goal")
            self.assertEqual([item["id"] for item in created_from_fallback["projection"]["steps"]], ["GOAL-01", "GOAL-02", "GOAL-03"])

    def test_goal_projection_is_replaced_by_formal_write(self) -> None:
        """验证正式最小任务写入会替换活动 Goal 安全三步。

        [参数] 无。
        [返回] None。
        最近修改时间：2026-07-25；改动原因：固定正式实施计划优先于默认 Goal 悬浮列表的运行中切换。
        """
        # 1. 先建立活动 Goal 投影，再通过常规 write 写入正式最小任务。
        with tempfile.TemporaryDirectory() as directory:
            path = self._write_current(Path(directory))
            projection.handle_goal_event(path, "create")
            projection.upsert_projection(path, self._sample())
            # 2. 写入后必须以正式来源为准，避免 Goal 默认步骤遮挡真实实施进度。
            replaced = projection.load_projection(path)
            self.assertEqual(replaced["projection_origin"], "persisted")
            self.assertEqual(replaced["steps"][0]["id"], "TASK-RTP-01")

    def test_goal_cli_and_invalid_event_preserve_original_file(self) -> None:
        """验证 Goal CLI 生命周期及失败时的原文件保护。

        [参数] 无。
        [返回] None。
        最近修改时间：2026-07-25；改动原因：确保 CLI 入口与函数调用具有相同的原子迁移和失败语义。
        """
        # 1. CLI 依次创建、阻断和完成 Goal，完成后恢复必须稳定返回契约错误。
        with tempfile.TemporaryDirectory() as directory:
            path = self._write_current(Path(directory))
            create = self._run_cli("goal", "--project-current", str(path), "--event", "create")
            self.assertEqual(create.returncode, 0, create.stderr)
            self.assertEqual(json.loads(create.stdout)["action"], "created")
            blocked = self._run_cli("goal", "--project-current", str(path), "--event", "blocked")
            self.assertEqual(blocked.returncode, 0, blocked.stderr)
            complete = self._run_cli("goal", "--project-current", str(path), "--event", "complete")
            self.assertEqual(complete.returncode, 0, complete.stderr)
            before = hashlib.sha256(path.read_bytes()).hexdigest()
            restore = self._run_cli("goal", "--project-current", str(path), "--event", "restore")
            self.assertEqual(restore.returncode, 2)
            self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), before)

    def test_legacy_versions_upgrade_to_version_three_only_when_written(self) -> None:
        """验证 v1/v2 兼容读取和成功写入时升级 v3。

        [参数] 无。
        [返回] None。
        最近修改时间：2026-07-25；改动原因：确保 Goal v3 引入不拒绝既有常规投影。
        """
        # 1. 旧版本常规投影写回后统一升级，旧版本 Goal 语义仍必须被拒绝。
        with tempfile.TemporaryDirectory() as directory:
            path = self._write_current(Path(directory))
            legacy = self._sample_v2()
            projection.upsert_projection(path, legacy)
            loaded = projection.load_projection(path)
            self.assertEqual(loaded["version"], 3)
            self.assertEqual(loaded["projection_origin"], "synthesized")
            v2_goal = self._sample_v2()
            v2_goal["projection_origin"] = "goal"
            v2_goal["synthesis_mode"] = "goal_default"
            with self.assertRaises(projection.ProjectionContractError):
                projection.validate_projection(v2_goal)

    def test_synthesize_projection_builds_exact_from_unique_source(self) -> None:
        """[参数] 无；[返回] None；最近修改时间：2026-07-24；改动原因：覆盖无投影精确补建路径。"""
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
            result = projection.synthesize_projection(current_path, self._synthesis_context())
            self.assertEqual(result["mode"], "exact")
            self.assertEqual(result["projection"]["version"], 2)
            self.assertEqual(result["projection"]["projection_origin"], "synthesized")
            self.assertEqual(result["projection"]["synthesis_mode"], "exact")
            self.assertEqual(result["projection"]["steps"][0]["status"], "completed")
            self.assertEqual(result["projection"]["steps"][1]["status"], "in_progress")
            self.assertEqual(result["payload"]["explanation"], projection.EXPLANATION_SYNTH_EXACT)

    def test_synthesize_projection_falls_back_when_source_is_ambiguous(self) -> None:
        """[参数] 无；[返回] None；最近修改时间：2026-07-24；改动原因：防止多候选来源时猜业务步骤。"""
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            current_path = self._write_current(root)
            result = projection.synthesize_projection(
                current_path,
                self._synthesis_context(candidate_source_documents=["a.md", "b.md"]),
            )
            self.assertEqual(result["mode"], "fallback")
            self.assertEqual(result["projection"]["synthesis_mode"], "fallback")
            self.assertEqual(
                [step["id"] for step in result["projection"]["steps"]],
                ["RECOVERY-01", "RECOVERY-02", "RECOVERY-03"],
            )
            self.assertEqual(result["payload"]["explanation"], projection.EXPLANATION_SYNTH_FALLBACK)

    def test_synthesize_projection_falls_back_when_explicit_hints_are_missing(self) -> None:
        """[参数] 无；[返回] None；最近修改时间：2026-07-24；改动原因：防止无状态证据时误做 exact。"""
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            current_path = self._write_current(root)
            result = projection.synthesize_projection(
                current_path,
                self._synthesis_context(current_step_hint=None, completed_step_hints=[]),
            )
            self.assertEqual(result["mode"], "fallback")

    def test_synthesize_projection_uses_first_unfinished_step_when_only_completed_hints_exist(self) -> None:
        """[参数] 无；[返回] None；最近修改时间：2026-07-24；改动原因：覆盖 only-completed-hints 的保守映射。"""
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
            )
            self.assertEqual(result["mode"], "exact")
            self.assertEqual(result["projection"]["steps"][1]["status"], "in_progress")
            self.assertEqual(result["evidence"]["status_confidence"], "conservative")

    def test_synthesize_projection_falls_back_when_no_source_document_exists(self) -> None:
        """[参数] 无；[返回] None；最近修改时间：2026-07-24；改动原因：覆盖无来源文档兜底路径。"""
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            current_path = self._write_current(root)
            result = projection.synthesize_projection(
                current_path,
                self._synthesis_context(candidate_source_documents=[]),
            )
            self.assertEqual(result["mode"], "fallback")

    def test_deactivate_completes_steps_atomically(self) -> None:
        """[参数] 无；[返回] None；最近修改时间：2026-07-23；改动原因：最后一步完成和失活不留中间态。"""
        # 1. 写入含进行中步骤的活动投影，再执行单次失活迁移。
        with tempfile.TemporaryDirectory() as directory:
            path = self._write_current(Path(directory))
            projection.upsert_projection(path, self._sample(("completed", "in_progress")))
            result = projection.deactivate_projection(path, updated_at="2026-07-23T02:00:00Z")
            # 2. 所有步骤必须完成，且失活结果不能生成 UI payload。
            self.assertEqual(result["state"], "inactive")
            self.assertTrue(all(step["status"] == "completed" for step in result["steps"]))
            with self.assertRaises(projection.ProjectionContractError):
                projection.build_update_plan_payload(result)

    def test_cli_subcommands_and_exit_codes(self) -> None:
        """[参数] 无；[返回] None；最近修改时间：2026-07-23；改动原因：验证五个真实 CLI 入口。"""
        # 1. 准备临时状态文件和合法 JSON，通过 write 初始化活动投影。
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            path = self._write_current(root)
            input_path = root / "projection.json"
            input_path.write_text(json.dumps(self._sample(), ensure_ascii=False), encoding="utf-8")
            write_result = self._run_cli("write", "--project-current", str(path), "--input", str(input_path))
            self.assertEqual(write_result.returncode, 0, write_result.stderr)
            # 2. 顺序验证读取、payload、指纹和失活四个真实命令。
            self.assertEqual(self._run_cli("validate", "--project-current", str(path)).returncode, 0)
            payload_result = self._run_cli("payload", "--project-current", str(path))
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
            )
            self.assertEqual(synthesize_result.returncode, 0, synthesize_result.stderr)
            self.assertIn("mode", json.loads(synthesize_result.stdout))
            fingerprint_result = self._run_cli("fingerprint", "--input", str(input_path))
            self.assertEqual(fingerprint_result.returncode, 0, fingerprint_result.stderr)
            deactivate_result = self._run_cli(
                "deactivate",
                "--project-current",
                str(path),
                "--updated-at",
                "2026-07-23T02:00:00Z",
            )
            self.assertEqual(deactivate_result.returncode, 0, deactivate_result.stderr)
            self.assertEqual(json.loads(deactivate_result.stdout)["projection"]["state"], "inactive")
            # 3. 契约输入和缺失文件分别返回稳定的 2、3 退出码。
            damaged_path = root / "damaged.json"
            damaged_path.write_text("{}", encoding="utf-8")
            contract_result = self._run_cli("write", "--project-current", str(path), "--input", str(damaged_path))
            self.assertEqual(contract_result.returncode, 2)
            missing_result = self._run_cli("validate", "--project-current", str(root / "missing.md"))
            self.assertEqual(missing_result.returncode, 3)

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
        self.assertIn("payload --project-current PROJECT_CURRENT.md", skill_document)
        self.assertIn("synthesize --project-current PROJECT_CURRENT.md --input synthesis_context.json", skill_document)
        self.assertIn("goal --project-current PROJECT_CURRENT.md --event create", skill_document)
        self.assertNotIn("--file PROJECT_CURRENT.md", skill_document)

    def test_goal_lifecycle_route_documents_keep_order_and_plan_mode_boundary(self) -> None:
        """验证 Goal 生命周期文档锁定 Owner、持久化顺序与 Plan Mode 边界。

        [参数] 无。
        [返回] None。
        最近修改时间：2026-07-25；改动原因：防止 Goal 路由漏交接、UI 先于持久化刷新或 Plan Mode 越界。
        """
        # 1. 任务投影 Owner 必须覆盖三个 Goal 工具，并明确先落盘再刷新 UI。
        rehydration_document = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        contract_document = (ROOT / "references" / "task-plan-projection-contract.md").read_text(encoding="utf-8")
        for token in ("create_goal", "get_goal", "update_goal", "先持久化", "Plan Mode"):
            self.assertIn(token, rehydration_document)
        self.assertIn("成功持久化 -> 读取返回 payload -> 调用 `update_plan`", contract_document)
        # 2. 自主执行 Owner 只能交接生命周期，不得借悬浮窗扩大执行授权。
        autonomous_document = (REPOSITORY_ROOT / "autonomous-execution-rules" / "SKILL.md").read_text(encoding="utf-8")
        for token in ("create_goal", "get_goal", "update_goal", "不因此自动取得", "不得把 blocked payload", "Plan Mode"):
            self.assertIn(token, autonomous_document)

    def test_contract_document_mentions_version_three_goal_and_synthesize(self) -> None:
        """验证契约文档锁定 v3 Goal 与补建 CLI。

        [参数] 无。
        [返回] None。
        最近修改时间：2026-07-25；改动原因：防止 Goal 生命周期命令或 Plan Mode 安全边界从文档契约中丢失。
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
