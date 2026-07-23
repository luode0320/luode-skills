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

    def test_documented_cli_uses_real_project_current_option(self) -> None:
        """[参数] 无；[返回] None；最近修改时间：2026-07-24；改动原因：锁定可执行恢复命令。"""
        # 1. 恢复 Owner 文档必须使用解析器真实提供的参数名，避免命中后执行失败。
        skill_document = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("validate --project-current PROJECT_CURRENT.md", skill_document)
        self.assertIn("payload --project-current PROJECT_CURRENT.md", skill_document)
        self.assertNotIn("--file PROJECT_CURRENT.md", skill_document)

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
            self.assertIn("继续任务", document)
            self.assertIn("update_plan", document)


if __name__ == "__main__":
    unittest.main(verbosity=2)
