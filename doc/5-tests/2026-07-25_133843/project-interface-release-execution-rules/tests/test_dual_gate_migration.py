"""C17-01 接口结果、消费者场景结果和正式附属产物回归。"""

from __future__ import annotations

import hashlib
import json
import sys
import tempfile
import threading
import unittest
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[5]
ENGINE_ROOT = ROOT / "project-interface-release-execution-rules" / "scripts"
sys.path.insert(0, str(ENGINE_ROOT))

from release_test_engine.report import write_report
from release_test_engine.cli import run_pipeline
from release_test_engine.gate import compare_gate_tracks, enforce_gate_mode, evaluate_scenario_cutover, persist_cutover_evidence, scenario_gate, seal_cutover_record
from release_test_engine.scenario_migration import load_compatible_scenario_results, migrate_scenario_results
from release_test_engine.scenario_loader import load_scenario_catalog, promote_to_verified, source_fingerprint
from scenario_verification_fixture import load_verified_catalog, promote_fixture_scenario, verification_evidence, verification_project_root


def make_cutover_record(project_root: Path, run_id: str) -> tuple[dict[str, object], str]:
    """写入一份真实 shadow evidence 并生成绑定记录。

    [参数] project_root: 临时项目根；run_id: 唯一运行标识。
    [返回] 已封存历史记录和场景目录指纹。
    最近修改时间：2026-07-25 23:45:00，切换测试不再使用纯内存自签摘要。
    """

    # 1. 场景目录全集和真实结果共同生成可被 gate.py 回读重算的证据。
    expected = {"read-flow": {"risk": "P0", "source_fingerprint": "source-a", "cleanup_required": False}}
    fingerprint = hashlib.sha256(json.dumps(expected, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()
    results = [{"scenario_id": "read-flow", "risk": "P0", "source_fingerprint": "source-a", "status": "PASS", "cleanup_required": False, "cleanup": []}]
    persisted = persist_cutover_evidence(project_root, run_id=run_id, environment="local", scenario_fingerprint=fingerprint, expected_scenarios=expected, scenario_results=results, legacy_gate={"gate": "PASS"})
    truth = persisted["scenario_gate"]
    diff = persisted["dual_gate_diff"]
    record = seal_cutover_record({
        "run_id": run_id,
        "environment": "local",
        "scenario_gate": truth["gate"],
        "coverage_complete": truth["coverage"]["coverage_complete"],
        "cleanup_failed": len(truth["cleanup_failures"]),
        "unexplained_differences": diff["unexplained_differences"],
        "scenario_fingerprint": fingerprint,
        "evidence_path": persisted["evidence_path"],
        "artifact_sha256": persisted["artifact_sha256"],
    })
    return record, fingerprint


class ShadowHandler(BaseHTTPRequestHandler):
    """提供 legacy 和场景轨道共用的 local HTTP 响应。"""

    def do_GET(self) -> None:  # noqa: N802
        """返回可被两条轨道验证的确定性 JSON。

        [参数] 无。
        [返回] 无。
        最近修改时间: 2026-07-25 16:50:00 改动原因: 提供 C17-02 CLI shadow 回环 fixture。
        """

        # 1. 两条消费者轨道读取同一个只读 local 资源，确保差异只来自门禁逻辑。
        payload = json.dumps({"data": {"id": "item-42", "state": "ready"}}).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def log_message(self, _format: str, *_args: object) -> None:
        """关闭 shadow fixture 默认访问日志。

        [参数] _format: 默认日志格式；_args: 日志参数。
        [返回] 无。
        最近修改时间：2026-07-25 21:15:00，避免双轨测试输出混入不可控访问日志。
        """

        return


class ReportSplitTest(unittest.TestCase):
    """报告测试只使用 local 临时目录，不连接任何外部环境。"""

    def test_interface_and_scenario_results_are_separate_and_redacted(self) -> None:
        """验证接口报告、场景报告和脱敏证据清单彼此独立。

        [参数] 无。
        [返回] 无。
        最近修改时间：2026-07-25 21:59:37，增加 JSON、Markdown 和 README 自由文本脱敏断言。
        """

        # 1. 使用一条接口结果和一条真实场景结果验证双报告边界。
        interface_result = {
            "operation_id": "read-item",
            "status": "FAIL",
            "reason": ["structured-secret-marker"],
            "error": {"detail": ["structured-secret-marker"]},
            "message": ("structured-secret-marker",),
            "request": {"token": "secret-token", "item_id": "item-42"},
            "response": {"body": {"data": {"id": "item-42", "state": "ready"}}},
            "evidence": {"run_id": "interface-run"},
        }
        scenario_result = {
            "run_id": "scenario-run",
            "scenario_id": "read-item-flow",
            "risk": "P0",
            "status": "PASS",
            "reason": ["structured-secret-marker"],
            "captures": {"token": "secret-token"},
            "steps": [{
                "run_id": "scenario-run",
                "scenario_id": "read-item-flow",
                "step_id": "read",
                "action": "http.request",
                "status": "PASS",
                "duration_ms": 4,
                "failure_type": "",
                "output": {"status": 200, "token": "secret-token"},
            }],
            "cleanup": [{"step_id": "delete", "action": "http.request", "status": "PASS", "duration_ms": 2, "failure_type": ""}],
        }
        with tempfile.TemporaryDirectory() as directory:
            # 1.1 在隔离目录写入双报告和附属资产，再从磁盘回读正式证据。
            output = Path(directory)
            artifacts = write_report(
                output,
                [interface_result],
                {"gate": "FAIL", "allow_release": False, "passed": 0, "failed": 1, "pending": 0},
                run_id="report-run",
                interfaces=[{"operation_id": "read-item", "risk": "P0"}],
                environment="local",
                scenario_results=[scenario_result],
            )

            interface_report = json.loads((output / "interface-results.json").read_text(encoding="utf-8"))
            scenario_report = json.loads((output / "scenario-results.json").read_text(encoding="utf-8"))
            compatibility_report = json.loads((output / "release-test-report.json").read_text(encoding="utf-8"))
            manifest = json.loads((output / "evidence-manifest.json").read_text(encoding="utf-8"))
            coverage = json.loads(Path(artifacts["consumer_coverage"]).read_text(encoding="utf-8"))
            cleanup = json.loads(Path(artifacts["cleanup_report"]).read_text(encoding="utf-8"))
            markdown_report = (output / "interface-test-results.md").read_text(encoding="utf-8")
            readme_report = (output / "README.md").read_text(encoding="utf-8")

        self.assertEqual(["read-item"], [item["operation_id"] for item in interface_report["results"]])
        self.assertEqual(["read-item-flow"], [item["scenario_id"] for item in scenario_report["results"]])
        self.assertEqual("http.request", scenario_report["results"][0]["steps"][0]["action"])
        self.assertEqual("scenario-run", scenario_report["results"][0]["steps"][0]["run_id"])
        self.assertEqual(["read-item"], [item["operation_id"] for item in compatibility_report["results"]])
        self.assertNotIn("secret-token", json.dumps(interface_report, ensure_ascii=False))
        self.assertNotIn("secret-token", json.dumps(scenario_report, ensure_ascii=False))
        self.assertNotIn("structured-secret-marker", json.dumps(interface_report, ensure_ascii=False))
        self.assertNotIn("structured-secret-marker", json.dumps(scenario_report, ensure_ascii=False))
        self.assertNotIn("structured-secret-marker", markdown_report)
        self.assertNotIn("structured-secret-marker", readme_report)
        self.assertIn("report detail redacted", markdown_report)
        self.assertEqual(1, coverage["passed"])
        self.assertEqual("PASS", cleanup["status"])
        self.assertEqual(1, cleanup["passed_steps"])
        self.assertTrue(all(not Path(entry["path"]).is_absolute() for entry in manifest["entries"]))
        self.assertTrue(all(entry["redacted"] for entry in manifest["entries"]))
        self.assertTrue(all(entry["redaction_status"] == "verified_absent" for entry in manifest["entries"]))

    def test_evidence_manifest_detects_unredacted_preexisting_file(self) -> None:
        """验证证据清单不会把含敏感原值的文件伪报为已脱敏。

        [参数] 无。
        [返回] 无。
        最近修改时间：2026-07-25 21:59:37，证据清单改为按本轮敏感输入原值逐文件复核。
        """

        # 1. 在输出根预置同一敏感值，正式报告会脱敏，而未经过流水线的文件必须使清单失败。
        marker = "manifest-sensitive-marker"
        interface_result = {"operation_id": "failed-item", "status": "FAIL", "reason": marker}
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory)
            (output / "untrusted.log").write_text(marker, encoding="utf-8")
            write_report(output, [interface_result], {"gate": "FAIL", "allow_release": False}, run_id="manifest-run", interfaces=[{"operation_id": "failed-item", "risk": "P0"}], environment="local")
            manifest = json.loads((output / "evidence-manifest.json").read_text(encoding="utf-8"))
        untrusted = next(item for item in manifest["entries"] if item["path"] == "untrusted.log")
        self.assertEqual("FAIL", manifest["status"])
        self.assertFalse(untrusted["redacted"])
        self.assertEqual("sensitive_value_detected", untrusted["redaction_status"])

    def test_evidence_manifest_handles_numeric_and_short_sensitive_values(self) -> None:
        """验证数字敏感值可检出，单字符敏感值不会触发全目录误报。

        [参数] 无。
        [返回] 无。
        最近修改时间：2026-07-25 23:08:00，覆盖数字原值泄漏和短值验证受限状态。
        """

        # 1. 数字型失败原因保留在预置文件时必须被可靠扫描并使证据清单失败。
        with tempfile.TemporaryDirectory() as numeric_directory:
            numeric_output = Path(numeric_directory)
            (numeric_output / "untrusted.log").write_text("13800138000", encoding="utf-8")
            write_report(numeric_output, [{"operation_id": "numeric", "status": "FAIL", "reason": 13800138000}], {"gate": "FAIL", "allow_release": False}, run_id="numeric-run", interfaces=[{"operation_id": "numeric", "risk": "P0"}], environment="local")
            numeric_manifest = json.loads((numeric_output / "evidence-manifest.json").read_text(encoding="utf-8"))
        numeric_entry = next(item for item in numeric_manifest["entries"] if item["path"] == "untrusted.log")
        self.assertEqual("FAIL", numeric_manifest["status"])
        self.assertEqual("sensitive_value_detected", numeric_entry["redaction_status"])
        # 2. 单字符敏感值不能用子串扫描污染普通产物，清单必须明确表示验证受限。
        with tempfile.TemporaryDirectory() as short_directory:
            short_output = Path(short_directory)
            write_report(short_output, [{"operation_id": "short", "status": "FAIL", "reason": "A"}], {"gate": "FAIL", "allow_release": False}, run_id="short-run", interfaces=[{"operation_id": "short", "risk": "P0"}], environment="local")
            short_manifest = json.loads((short_output / "evidence-manifest.json").read_text(encoding="utf-8"))
        self.assertEqual("PENDING", short_manifest["status"])
        self.assertTrue(all(item["redaction_status"] == "verification_limited" for item in short_manifest["entries"]))
        self.assertTrue(all(not item["redacted"] for item in short_manifest["entries"]))

    def test_evidence_manifest_rejects_internal_file_symlink(self) -> None:
        """验证证据清单不会跟随输出目录内的文件 symlink。

        [参数] 无。
        [返回] 无。
        最近修改时间：2026-07-25 23:37:04，覆盖根外文件不得被读取或纳入清单的安全边界。
        """

        # 1. 在输出根预置指向根外普通文件的 symlink，生成清单时必须稳定阻断。
        with tempfile.TemporaryDirectory() as output_directory, tempfile.TemporaryDirectory() as outside_directory:
            output = Path(output_directory)
            outside = Path(outside_directory) / "outside-secret.log"
            outside.write_text("outside-sensitive-value", encoding="utf-8")
            (output / "linked.log").symlink_to(outside)
            with self.assertRaisesRegex(PermissionError, "REPORT_OUTPUT_SYMLINK_FORBIDDEN"):
                write_report(output, [], {"gate": "PENDING", "allow_release": False}, run_id="internal-file-symlink", environment="local")
            self.assertFalse((output / "evidence-manifest.json").exists())

    def test_canonical_report_rejects_symlink_and_indexes_root_readme(self) -> None:
        """验证 canonical 输出拒绝 symlink 越界并索引根级 README。

        [参数] 无。
        [返回] 无。
        最近修改时间：2026-07-25 23:18:15，覆盖直接与父级 symlink 输出边界及根级正式证据清单。
        """

        # 1. 预置 ascii-artifacts 目录 symlink 时，写报告必须在根外产生产物前阻断。
        with tempfile.TemporaryDirectory() as project_directory, tempfile.TemporaryDirectory() as outside_directory:
            output = Path(project_directory)
            outside = Path(outside_directory)
            (output / "ascii-artifacts").symlink_to(outside, target_is_directory=True)
            with self.assertRaisesRegex(PermissionError, "REPORT_OUTPUT_SYMLINK_FORBIDDEN"):
                write_report(output, [], {"gate": "PENDING", "allow_release": False}, run_id="symlink-report", environment="local", canonical_layout=True)
            self.assertEqual([], list(outside.iterdir()))
        # 2. 输出根尚不存在但父目录是 symlink 时，也必须在根外创建任何目录前阻断。
        with tempfile.TemporaryDirectory() as project_directory, tempfile.TemporaryDirectory() as outside_directory:
            project_root = Path(project_directory)
            outside = Path(outside_directory)
            (project_root / "linked-parent").symlink_to(outside, target_is_directory=True)
            with self.assertRaisesRegex(PermissionError, "REPORT_OUTPUT_SYMLINK_FORBIDDEN"):
                write_report(project_root / "linked-parent" / "new-output", [], {"gate": "PENDING", "allow_release": False}, run_id="parent-symlink-report", environment="local", canonical_layout=True)
            self.assertFalse((outside / "new-output").exists())
        # 3. 正常 canonical 布局必须把输出根 README 作为安全逻辑路径纳入清单。
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory)
            write_report(output, [], {"gate": "PENDING", "allow_release": False}, run_id="canonical-report", environment="local", canonical_layout=True)
            manifest = json.loads((output / "ascii-artifacts" / "evidence-manifest.json").read_text(encoding="utf-8"))
        readme = next(item for item in manifest["entries"] if item["path"] == "output-root/README.md")
        self.assertEqual("PASS", manifest["status"])
        self.assertTrue(readme["redacted"])
        self.assertEqual("no_sensitive_input", readme["redaction_status"])

    def test_manifest_non_pass_overrides_release_gate_and_reports(self) -> None:
        """验证 manifest FAIL/PENDING 会阻止发布并重写正式门禁摘要。

        [参数] 无。
        [返回] 无。
        最近修改时间：2026-07-25 23:37:04，同时校验门禁重写后的最终文件摘要。
        """

        # 1. 长数字敏感值残留时，即使原门禁 PASS 也必须升级安全 BLOCKED 并同步 JSON/README。
        with tempfile.TemporaryDirectory() as fail_directory:
            output = Path(fail_directory)
            (output / "untrusted.log").write_text("13800138000", encoding="utf-8")
            artifacts = write_report(output, [{"operation_id": "safe", "status": "PASS"}], {"gate": "PASS", "allow_release": True, "passed": 1, "failed": 0, "pending": 0}, run_id="manifest-fail-gate", interfaces=[{"operation_id": "safe", "risk": "P0", "message": 13800138000}], environment="local")
            interface_report = json.loads((output / "interface-results.json").read_text(encoding="utf-8"))
            readme = (output / "README.md").read_text(encoding="utf-8")
            manifest = json.loads((output / "evidence-manifest.json").read_text(encoding="utf-8"))
            # 1.1 门禁重写后逐项重算最终文件摘要，防止 manifest 保留重写前的过期哈希。
            sha_matches = all(hashlib.sha256((output / item["path"]).read_bytes()).hexdigest() == item["sha256"] for item in manifest["entries"])
        self.assertEqual("BLOCKED", artifacts["gate"]["gate"])
        self.assertFalse(artifacts["gate"]["allow_release"])
        self.assertEqual("BLOCKED", interface_report["gate"]["gate"])
        self.assertIn("### 结论等级：BLOCKED", readme)
        self.assertIn("- 是否允许上线：否", readme)
        self.assertTrue(sha_matches)
        # 2. 单字符敏感值无法可靠扫描时，原 PASS 必须降为 PENDING 而不是继续自动放行。
        with tempfile.TemporaryDirectory() as pending_directory:
            output = Path(pending_directory)
            artifacts = write_report(output, [{"operation_id": "safe", "status": "PASS"}], {"gate": "PASS", "allow_release": True, "passed": 1, "failed": 0, "pending": 0}, run_id="manifest-pending-gate", interfaces=[{"operation_id": "safe", "risk": "P0", "message": "A"}], environment="local")
        self.assertEqual("PENDING", artifacts["gate"]["gate"])
        self.assertFalse(artifacts["gate"]["allow_release"])
        self.assertEqual("PENDING", artifacts["evidence_manifest_status"])

    def test_empty_scenario_input_is_explicitly_unconfigured(self) -> None:
        """验证缺少真实场景输入时不会伪造场景通过。

        [参数] 无。
        [返回] 无。
        最近修改时间: 2026-07-25 16:25:00 改动原因: 固定未配置场景的安全状态。
        """

        # 1. 旧接口调用不传场景结果时，报告应显式输出 not_configured。
        with tempfile.TemporaryDirectory() as directory:
            # 1.1 在无场景输入的隔离目录生成报告，核对所有场景资产保持未配置。
            output = Path(directory)
            write_report(
                output,
                [],
                {"gate": "PENDING", "allow_release": False, "passed": 0, "failed": 0, "pending": 0},
                run_id="empty-run",
                environment="local",
            )
            scenario_report = json.loads((output / "scenario-results.json").read_text(encoding="utf-8"))
            coverage = json.loads((output / "consumer-coverage.json").read_text(encoding="utf-8"))
            capabilities = json.loads((output / "protocol-capabilities.json").read_text(encoding="utf-8"))

        self.assertEqual("not_configured", scenario_report["status"])
        self.assertEqual([], scenario_report["results"])
        self.assertEqual("not_configured", coverage["status"])
        self.assertEqual("not_configured", capabilities["status"])

    def test_supplied_summaries_cannot_hide_failed_runtime_or_cleanup(self) -> None:
        """验证附加摘要不能覆盖真实场景失败和清理阻断。

        [参数] 无。
        [返回] 无。
        最近修改时间: 2026-07-25 16:25:00 改动原因: 防止外部摘要绕过场景门禁事实。
        """

        # 1. 注入失败场景和清理失败，确认派生状态优先于附加摘要。
        scenario_result = {
            "run_id": "scenario-run",
            "scenario_id": "failed-flow",
            "risk": "P1",
            "status": "FAIL",
            "steps": [{
                "run_id": "scenario-run",
                "scenario_id": "failed-flow",
                "step_id": "read",
                "action": "http.request",
                "status": "FAIL",
                "duration_ms": 3,
                "failure_type": "SCENARIO_ASSERTION_FAILED",
            }],
            "cleanup": [{"step_id": "delete", "action": "http.request", "status": "FAIL", "duration_ms": 1, "failure_type": "CLEANUP_FAILED"}],
        }
        with tempfile.TemporaryDirectory() as directory:
            # 1.1 在隔离目录写入失败 runtime 和清理证据，附加摘要不得覆盖派生状态。
            output = Path(directory)
            write_report(
                output,
                [],
                {"gate": "PENDING", "allow_release": False, "passed": 0, "failed": 0, "pending": 0},
                run_id="report-run",
                environment="local",
                scenario_results=[scenario_result],
                consumer_coverage={"status": "PASS", "source": "external"},
                cleanup_report={"status": "PASS", "source": "external"},
            )
            scenario_report = json.loads((output / "scenario-results.json").read_text(encoding="utf-8"))
            coverage = json.loads((output / "consumer-coverage.json").read_text(encoding="utf-8"))
            cleanup = json.loads((output / "cleanup-report.json").read_text(encoding="utf-8"))

        self.assertEqual("FAIL", scenario_report["status"])
        self.assertEqual("FAIL", coverage["status"])
        self.assertEqual("BLOCKED", cleanup["status"])

    def test_shadow_tracks_pass_only_when_p0_p1_scenarios_and_cleanup_pass(self) -> None:
        """验证 legacy 与场景轨道一致通过时 shadow 差异为空。

        [参数] 无。
        [返回] 无。
        最近修改时间: 2026-07-25 16:45:00 改动原因: 增加 C17-02 双轨一致性正向样本。
        """

        # 1. 同一 P0/P1 场景同时满足步骤和清理通过，双轨应无未解释差异。
        scenario = {"scenario_id": "read-item-flow", "risk": "P0", "status": "PASS", "cleanup": [{"status": "PASS"}]}
        result = compare_gate_tracks({"gate": "PASS", "allow_release": True}, [scenario], run_id="shadow-run", expected_scenarios={"read-item-flow": {"risk": "P0"}})
        self.assertEqual("PASS", scenario_gate([scenario], expected_scenarios={"read-item-flow": {"risk": "P0"}})["gate"])
        self.assertEqual("PASS", result["status"])
        self.assertEqual([], result["differences"])
        self.assertEqual([], result["unexplained_differences"])

    def test_shadow_tracks_classify_non_pass_and_coverage_gap(self) -> None:
        """验证双轨差异分类以及 P0/P1 覆盖缺口阻断。

        [参数] 无。
        [返回] 无。
        最近修改时间: 2026-07-25 16:45:00 改动原因: 增加 C17-02 失败和缺口样本。
        """

        # 1. 场景失败和清理失败必须分类，且没有解释时保持 PENDING。
        failed = {"scenario_id": "write-item-flow", "risk": "P1", "status": "FAIL", "cleanup": [{"status": "FAIL"}]}
        result = compare_gate_tracks({"gate": "PASS", "allow_release": True}, [failed], run_id="shadow-fail", expected_scenarios={"write-item-flow": {"risk": "P1", "cleanup_required": True}})
        types = {item["type"] for item in result["differences"]}
        self.assertEqual("FAIL", result["scenario_gate"]["gate"])
        self.assertEqual({"STATUS_DISAGREEMENT", "SCENARIO_NON_PASS", "CLEANUP_INCOMPLETE"}, types)
        self.assertEqual("PENDING", result["status"])
        self.assertEqual("BLOCKED", scenario_gate([])["gate"])
        self.assertEqual("SCENARIO_COVERAGE_MISSING", scenario_gate([])["failure_type"])

    def test_scenario_gate_rejects_incomplete_or_untrusted_coverage(self) -> None:
        """验证目录全集、来源指纹和清理要求不能由结果子集伪造。

        [参数] 无。
        [返回] 无。
        最近修改时间：2026-07-25 21:59:37，增加 P0/P1 双向风险漂移阻断样本。
        """

        # 1. 只返回一个 PASS 不能覆盖目录中另一个 P1，且缺少显式目录全集也必须阻断。
        result = {"scenario_id": "read-flow", "risk": "P0", "source_fingerprint": "source-a", "status": "PASS", "cleanup": []}
        expected = {"read-flow": {"risk": "P0", "source_fingerprint": "source-a"}, "write-flow": {"risk": "P1", "source_fingerprint": "source-b", "cleanup_required": True}}
        self.assertEqual("BLOCKED", scenario_gate([result])["gate"])
        incomplete = scenario_gate([result], expected_scenarios=expected)
        self.assertEqual(["write-flow"], incomplete["coverage"]["missing"])
        self.assertFalse(incomplete["allow_release"])
        # 2. 来源漂移和写场景空清理分别稳定阻断或失败。
        drifted = scenario_gate([{**result, "source_fingerprint": "wrong"}], expected_scenarios={"read-flow": expected["read-flow"]})
        self.assertEqual(["read-flow"], drifted["coverage"]["source_mismatch"])
        # 3. 目录与结果之间的 P0/P1 双向风险漂移都必须阻断，结果不能自行降级或升级风险。
        downgraded = scenario_gate([{**result, "risk": "P1"}], expected_scenarios={"read-flow": expected["read-flow"]})
        upgraded = scenario_gate([{"scenario_id": "write-flow", "risk": "P0", "source_fingerprint": "source-b", "status": "PASS", "cleanup": [{"status": "PASS"}]}], expected_scenarios={"write-flow": expected["write-flow"]})
        self.assertEqual(["read-flow"], downgraded["coverage"]["risk_mismatch"])
        self.assertEqual(["write-flow"], upgraded["coverage"]["risk_mismatch"])
        self.assertFalse(downgraded["coverage"]["coverage_complete"])
        self.assertFalse(upgraded["coverage"]["coverage_complete"])
        write_result = {"scenario_id": "write-flow", "risk": "P1", "source_fingerprint": "source-b", "status": "PASS", "cleanup_required": True, "cleanup": []}
        self.assertEqual("CLEANUP_INCOMPLETE", scenario_gate([write_result], expected_scenarios={"write-flow": expected["write-flow"]})["failure_type"])

    def test_cli_shadow_runs_both_tracks_against_local_fixture(self) -> None:
        """验证 CLI shadow 模式真实运行 legacy 和 verified 场景两条轨道。

        [参数] 无。
        [返回] 无。
        最近修改时间：2026-07-26 00:30:00，shadow 场景目录改用结构化晋级证据。
        """

        # 1. 用随机回环端口启动同一 local HTTP 服务，禁止接入外部环境。
        evidence = [{"source": "local-openapi", "operation_id": "read-item"}]
        scenario_document = {
            "schema_version": "external-scenario/1.0",
            "scenarios": {
                "read-item": {
                    "scenario_id": "read-item",
                    "risk": "P0",
                    "consumers": ["local-shadow-client"],
                    "source_evidence": evidence,
                    "source_fingerprint": source_fingerprint(evidence),
                    "lifecycle": "candidate",
                    "preconditions": [{"environment": "local"}],
                    "steps": [{
                        "step_id": "read",
                        "action": "http.request",
                        "config": {"method": "GET", "url": "http://127.0.0.1:0/items/42", "config_environment": "local"},
                        "captures": {},
                        "assertions": [{"path": "/status", "op": "equal", "expected": 200}],
                        "parallel_group": "",
                    }],
                    "assertions": [],
                    "cleanup": [],
                    "verification": {},
                }
            },
        }
        with tempfile.TemporaryDirectory() as directory:
            # 1.1 创建 local OpenAPI、场景目录和随机回环服务，真实运行 shadow 双轨。
            root = Path(directory)
            (root / "openapi.yaml").write_text(yaml.safe_dump({"openapi": "3.0.3", "info": {"title": "shadow", "version": "1"}, "paths": {"/items/42": {"get": {"operationId": "read-item", "responses": {"200": {"description": "ok"}}}}}}, sort_keys=False), encoding="utf-8")
            scenario_path = root / "scenario-catalog.yaml"
            server = ThreadingHTTPServer(("127.0.0.1", 0), ShadowHandler)
            thread = threading.Thread(target=server.serve_forever, daemon=True)
            thread.start()
            scenario_document["scenarios"]["read-item"]["steps"][0]["config"]["url"] = f"http://127.0.0.1:{server.server_port}/items/42"
            candidate = load_scenario_catalog(scenario_document).scenarios["read-item"]
            verified = promote_fixture_scenario(candidate, project_root=root)
            scenario_document = {"schema_version": "external-scenario/1.0", "scenarios": {"read-item": verified.to_dict()}}
            scenario_path.write_text(yaml.safe_dump(scenario_document, sort_keys=False), encoding="utf-8")
            try:
                # 1.2 服务存活期间执行完整 pipeline，finally 必须回收端口和线程。
                result = run_pipeline(
                    root,
                    output_dir=root / "artifacts",
                    environment="local",
                    env={"local_config": f"http://127.0.0.1:{server.server_port}"},
                    gate_mode="shadow",
                    scenario_catalog=scenario_path,
                )
            finally:
                server.shutdown()
                server.server_close()
                thread.join(timeout=3)
            diff = json.loads((root / "artifacts" / "dual-gate-diff.json").read_text(encoding="utf-8"))
            coverage = json.loads((root / "artifacts" / "consumer-coverage.json").read_text(encoding="utf-8"))
            evidence_path = root / diff["current_record"]["evidence_path"]
            shadow_evidence = json.loads(evidence_path.read_text(encoding="utf-8"))
            self.assertEqual(diff["run_id"], shadow_evidence["run_id"])
            self.assertEqual("PASS", shadow_evidence["scenario_gate"]["gate"])

        self.assertEqual("PASS", result["status"])
        self.assertEqual("shadow", result["gate_mode"])
        self.assertEqual("PASS", diff["status"])
        self.assertEqual([], diff["differences"])
        self.assertEqual({"total": 1, "passed": 1}, coverage["consumers"]["local-shadow-client"])

    def test_cutover_requires_three_consecutive_local_passes(self) -> None:
        """验证场景硬切必须绑定三次真实且可重算的 local evidence。

        [参数] 无。
        [返回] 无。
        最近修改时间：2026-07-25 23:45:00，覆盖内存伪造、文件篡改和目录漂移阻断。
        """

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            # 1. 三次记录各自绑定项目根内真实 artifact，只有完整连续窗口可通过。
            records_and_fingerprints = [make_cutover_record(root, f"run-{index}") for index in range(3)]
            qualified = [item[0] for item in records_and_fingerprints]
            fingerprint = records_and_fingerprints[0][1]
            self.assertEqual("BLOCKED", evaluate_scenario_cutover(qualified[:1], current_run_id="run-0", scenario_fingerprint=fingerprint, project_root=root)["status"])
            self.assertEqual("PASS", evaluate_scenario_cutover(qualified, current_run_id="run-2", scenario_fingerprint=fingerprint, project_root=root)["status"])
            # 2. 重复记录、自签摘要篡改和调用方目录漂移均不能取得资格。
            duplicate = [qualified[0], qualified[0], qualified[0]]
            self.assertIn("RUN_ID_INVALID", evaluate_scenario_cutover(duplicate, current_run_id="run-0", scenario_fingerprint=fingerprint, project_root=root)["reasons"])
            tampered_record = [dict(item) for item in qualified]
            tampered_record[-1]["scenario_gate"] = "FAIL"
            self.assertIn("HISTORY_EVIDENCE_INVALID", evaluate_scenario_cutover(tampered_record, current_run_id="run-2", scenario_fingerprint=fingerprint, project_root=root)["reasons"])
            self.assertIn("SCENARIO_FINGERPRINT_MISMATCH", evaluate_scenario_cutover(qualified, current_run_id="run-2", scenario_fingerprint="new-catalog", project_root=root)["reasons"])
            # 3. 纯内存自签记录缺少 artifact，必须固定返回 HISTORY_EVIDENCE_INVALID。
            memory_only = [seal_cutover_record({"run_id": f"fake-{index}", "environment": "local", "scenario_gate": "PASS", "coverage_complete": True, "cleanup_failed": 0, "unexplained_differences": [], "scenario_fingerprint": fingerprint}) for index in range(3)]
            memory_result = evaluate_scenario_cutover(memory_only, current_run_id="fake-2", scenario_fingerprint=fingerprint, project_root=root)
            self.assertEqual("BLOCKED", memory_result["status"])
            self.assertIn("HISTORY_EVIDENCE_INVALID", memory_result["reasons"])
            # 4. artifact 字节被篡改后，即使记录摘要未变也必须失效。
            evidence_path = root / qualified[-1]["evidence_path"]
            evidence_path.write_text(evidence_path.read_text(encoding="utf-8") + " ", encoding="utf-8")
            artifact_result = evaluate_scenario_cutover(qualified, current_run_id="run-2", scenario_fingerprint=fingerprint, project_root=root)
            self.assertIn("HISTORY_EVIDENCE_INVALID", artifact_result["reasons"])

    def test_cutover_evidence_rejects_outside_symlink_before_write(self) -> None:
        """验证 evidence 父目录 symlink 越界时不会先在根外创建目录。

        [参数] 无。
        [返回] 无。
        最近修改时间：2026-07-26 00:10:00，覆盖 shadow 证据写入前的路径竞态边界。
        """

        # 1. .release-test-engine 指向另一个临时目录，persist 必须在 mkdir 前阻断。
        with tempfile.TemporaryDirectory() as project_directory, tempfile.TemporaryDirectory() as outside_directory:
            project_root = Path(project_directory)
            outside_root = Path(outside_directory)
            (project_root / ".release-test-engine").symlink_to(outside_root, target_is_directory=True)
            with self.assertRaisesRegex(PermissionError, "CUTOVER_EVIDENCE_PATH_OUTSIDE_PROJECT"):
                make_cutover_record(project_root, "symlink-run")
            self.assertFalse((outside_root / "shadow-evidence").exists())

    def test_shadow_evidence_redacts_injected_sensitive_fields(self) -> None:
        """验证 shadow artifact、重算门禁和双轨差异都不持久化敏感字段。

        [参数] 无。
        [返回] 无。
        最近修改时间：2026-07-25 21:59:37，覆盖调用方注入敏感结果和目录字段的写盘边界。
        """

        # 1. 指纹按脱敏后的门禁目录计算，持久化入口必须对原始输入生成同一安全副本。
        expected = {"read-flow": {"risk": "P0", "source_fingerprint": "source-a", "token": "secret-token", "message": ["structured-secret-marker"]}}
        safe_expected = {"read-flow": {"risk": "P0", "source_fingerprint": "source-a", "token": "***", "message": "report detail redacted"}}
        fingerprint = hashlib.sha256(json.dumps(safe_expected, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()
        results = [{"scenario_id": "read-flow", "risk": "P0", "source_fingerprint": "source-a", "status": "PASS", "reason": ["structured-secret-marker"], "error": {"detail": ["structured-secret-marker"]}, "token": "secret-token", "cleanup": []}]
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            persisted = persist_cutover_evidence(root, run_id="redacted-run", environment="local", scenario_fingerprint=fingerprint, expected_scenarios=expected, scenario_results=results, legacy_gate={"gate": "PASS"})
            evidence_text = (root / persisted["evidence_path"]).read_text(encoding="utf-8")

        self.assertNotIn("secret-token", evidence_text)
        self.assertNotIn("structured-secret-marker", evidence_text)
        self.assertIn('"token":"***"', evidence_text)
        self.assertIn("report detail redacted", evidence_text)

    def test_cutover_forbids_legacy_fallback_after_scenario_switch(self) -> None:
        """验证硬切后运行时不能回退 legacy 门禁。

        [参数] 无。
        [返回] 无。
        最近修改时间: 2026-07-25 17:20:00 改动原因: 增加 C17-03 回退阻断样本。
        """

        # 1. scenario 状态下请求 legacy 必须返回固定阻断分类。
        blocked = enforce_gate_mode("legacy", {"active_mode": "scenario"})
        self.assertFalse(blocked["allowed"])
        self.assertEqual("LEGACY_FALLBACK_FORBIDDEN", blocked["failure_type"])
        shadow = enforce_gate_mode("shadow", {"active_mode": "scenario"})
        self.assertFalse(shadow["allowed"])
        self.assertEqual("LEGACY_FALLBACK_FORBIDDEN", shadow["failure_type"])
        not_activated = enforce_gate_mode("scenario", {})
        self.assertFalse(not_activated["allowed"])
        self.assertEqual("SCENARIO_CUTOVER_NOT_ACTIVATED", not_activated["failure_type"])

    def test_legacy_interface_result_is_readable_but_cannot_be_promoted(self) -> None:
        """验证旧列表式接口结果可读但迁移后仍为待验证状态。

        [参数] 无。
        [返回] 无。
        最近修改时间: 2026-07-25 17:45:00 改动原因: 增加 C18-01 旧资产兼容负向样本。
        """

        # 1. 旧接口结果保留原证据，但不把 status PASS 继承到新场景门禁。
        legacy = [{"operation_id": "health", "status": "PASS", "response": "{}"}]
        migrated = load_compatible_scenario_results(legacy)
        self.assertTrue(migrated["deprecated"])
        self.assertEqual("PENDING", migrated["results"][0]["status"])
        self.assertEqual("LEGACY_INTERFACE_RESULT", migrated["results"][0]["failure_type"])

    def test_legacy_migration_writes_new_file_without_overwriting_input(self) -> None:
        """验证旧资产迁移输出独立写入并保留弃用提示。

        [参数] 无。
        [返回] 无。
        最近修改时间: 2026-07-25 23:37:04 改动原因: 增加新旧迁移文件的敏感字段负向回归。
        """

        # 1. 只使用 local 临时目录，迁移失败或成功都不覆盖输入文件。
        with tempfile.TemporaryDirectory() as directory:
            # 1.1 在隔离目录迁移旧列表资产并分别回读源文件和新文件。
            root = Path(directory)
            source = root / "legacy.json"
            target = root / "migrated.json"
            source.write_text(json.dumps([{"operation_id": "health", "status": "PASS", "response": {"authorization": "Bearer legacy-secret", "password": "legacy-password", "reason": 13800138000}}], ensure_ascii=False), encoding="utf-8")
            summary = migrate_scenario_results(source, target)
            source_text = source.read_text(encoding="utf-8")
            output = json.loads(target.read_text(encoding="utf-8"))
        self.assertEqual("PASS", summary["status"])
        self.assertTrue(summary["deprecated"])
        self.assertIn("Bearer legacy-secret", source_text)
        self.assertEqual("deprecated", output["status"])
        migrated_text = json.dumps(output, ensure_ascii=False)
        self.assertNotIn("legacy-secret", migrated_text)
        self.assertNotIn("legacy-password", migrated_text)
        self.assertNotIn("13800138000", migrated_text)
        self.assertEqual("***", output["results"][0]["legacy_result"]["response"]["authorization"])
        self.assertEqual("report detail redacted", output["results"][0]["legacy_result"]["response"]["reason"])

    def test_current_scenario_migration_redacts_sensitive_fields(self) -> None:
        """验证新版场景结果迁移同样不会重新持久化敏感原值。

        [参数] 无。
        [返回] 无。
        最近修改时间：2026-07-25 23:37:04，覆盖新版映射分支的递归脱敏写盘边界。
        """

        # 1. 新版结果内嵌套凭据和自由错误文本均必须在迁移文件中被收敛。
        current = {"schema_version": "external-scenario/1.0", "results": [{"scenario_id": "current-flow", "status": "FAIL", "response": {"api_key": "current-secret"}, "error": {"detail": "current-sensitive-detail"}}]}
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "migrated.json"
            migrate_scenario_results(current, target)
            migrated_text = target.read_text(encoding="utf-8")
            output = json.loads(migrated_text)
        self.assertNotIn("current-secret", migrated_text)
        self.assertNotIn("current-sensitive-detail", migrated_text)
        self.assertEqual("***", output["results"][0]["response"]["api_key"])
        self.assertEqual("report detail redacted", output["results"][0]["error"])

if __name__ == "__main__":
    unittest.main()
