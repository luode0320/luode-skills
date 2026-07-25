"""C18-02 隔离工具环境、doctor 和 local 触发边界回归。"""

from __future__ import annotations

import contextlib
import io
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import yaml

ROOT = Path(__file__).resolve().parents[5]
ENGINE_ROOT = ROOT / "project-interface-release-execution-rules" / "scripts"
TEST_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ENGINE_ROOT))
sys.path.insert(0, str(TEST_ROOT))

from generate_release_test_plan import build_parser
from release_test_engine.cli import run_doctor, run_pipeline
from release_test_engine.scenario_loader import load_scenario_catalog, source_fingerprint
from scenario_verification_fixture import promote_fixture_scenario
from release_test_engine.tool_env import inspect_tool_environment


class ToolEnvironmentAndTriggerTest(unittest.TestCase):
    """工具环境测试只读取 local 配置和当前隔离解释器。"""

    def test_tool_environment_doctor_reports_locked_runtime_without_network(self) -> None:
        """验证隔离工具环境 doctor 能识别锁定版本和协议 runtime。

        [参数] 无。
        [返回] 无。
        最近修改时间: 2026-07-25 18:15:00 改动原因: 增加 C18-02 工具环境正向探针。
        """

        # 1. doctor 只读取解释器和已安装包，不建立任何 HTTP/WS 连接。
        result = inspect_tool_environment()
        self.assertEqual("PASS", result["status"])
        self.assertEqual("not_attempted", result["network_access"])
        self.assertFalse(result["project_dependency_mutation"])
        self.assertTrue(all(result["protocol_runtime"].values()))

    def test_tool_environment_doctor_blocks_missing_runtime_dependency(self) -> None:
        """验证缺少锁定依赖时 doctor 返回阻断而非伪造能力。

        [参数] 无。
        [返回] 无。
        最近修改时间: 2026-07-25 18:15:00 改动原因: 增加 C18-02 缺依赖负向探针。
        """

        # 1. 用不存在的分发包构造只读探针，不安装也不改当前环境。
        result = inspect_tool_environment(required_packages={"missing-test-package": ("missing_test_module", "1.0.0")})
        self.assertEqual("BLOCKED", result["status"])
        self.assertEqual(["missing-test-package"], result["missing_packages"])

    def test_tool_environment_doctor_blocks_non_local_configuration(self) -> None:
        """验证 doctor 对非 local 配置直接阻断。

        [参数] 无。
        [返回] 无。
        最近修改时间: 2026-07-25 18:15:00 改动原因: 固定 local 连接红线。
        """

        # 1. 非 local 只返回环境阻断摘要，不读取或连接其地址。
        with tempfile.TemporaryDirectory() as directory:
            result = run_doctor({"project_root": Path(directory), "environment": "staging"})
        self.assertEqual("BLOCKED", result["status"])
        self.assertEqual("ENV_BLOCKED", result["failure_type"])

    def test_real_cli_exposes_external_release_entry(self) -> None:
        """验证真实 CLI 主入口继续暴露消费者场景发布命令。

        [参数] 无。
        [返回] 无。
        最近修改时间: 2026-07-25 16:45:00 改动原因: 锁定旧解析器与新版 CLI 的双层兼容边界。
        """

        # 1. 使用当前隔离解释器启动真实脚本，帮助输出不得触发网络或项目依赖写入。
        script = ENGINE_ROOT / "generate_release_test_plan.py"
        completed = subprocess.run(
            [sys.executable, "-X", "utf8", str(script), "release-run", "--help"],
            check=False,
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        self.assertEqual(0, completed.returncode, completed.stderr)
        self.assertIn("--gate-mode", completed.stdout)

    def test_external_run_defaults_to_scenario_without_changing_release_compatibility(self) -> None:
        """验证 external-run 默认执行场景轨道且旧入口仍默认 legacy。

        [参数] 无。
        [返回] 无。
        最近修改时间：2026-07-25 21:59:37，增加真实子进程对场景断言失败退出码 1 的覆盖。
        """

        # 1. 三个入口使用同一参数集合，但 external-run 的 gate-mode action 必须独立。
        parser = build_parser(include_external_scenarios=True)
        external_args = parser.parse_args(["external-run", "--project-root", "."])
        release_args = parser.parse_args(["release-run", "--project-root", "."])
        legacy_args = parser.parse_args(["run", "--project-root", "."])
        self.assertEqual("scenario", external_args.gate_mode)
        self.assertEqual("legacy", release_args.gate_mode)
        self.assertEqual("legacy", legacy_args.gate_mode)
        # 2. 真实 command_run 委派收到 scenario，证明缺省执行不会落入 legacy 分支。
        with mock.patch("generate_release_test_plan._invoke_engine", return_value={"status": "PENDING"}) as invoke:
            self.assertEqual(4, external_args.func(external_args))
        self.assertEqual("scenario", invoke.call_args.args[1].gate_mode)
        # 3. 激活 scenario 状态并提供 verified catalog，真实执行 local 请求失败场景而非停在模式前置门禁。
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            evidence = [{"source": "test-openapi", "operation_id": "external-default-flow"}]
            candidate_document = {
                "schema_version": "external-scenario/1.0",
                "scenarios": {
                    "external-default-flow": {
                        "scenario_id": "external-default-flow",
                        "risk": "P0",
                        "consumers": ["frontend.trigger-test"],
                        "source_evidence": evidence,
                        "source_fingerprint": source_fingerprint(evidence),
                        "lifecycle": "candidate",
                        "preconditions": [{"environment": "local"}],
                        "steps": [{"step_id": "connect-refused", "action": "http.request", "config": {"method": "GET", "url": "http://127.0.0.1:1/unavailable", "timeout_seconds": 0.2, "config_environment": "local"}, "captures": {}, "assertions": [], "parallel_group": ""}],
                        "assertions": [],
                        "cleanup": [],
                        "verification": {},
                    }
                },
            }
            candidate = load_scenario_catalog(candidate_document).scenarios["external-default-flow"]
            verified = promote_fixture_scenario(candidate, project_root=root)
            catalog_path = root / "scenario-catalog.json"
            state_path = root / "gate-state.json"
            catalog_path.write_text(json.dumps({"schema_version": "external-scenario/1.0", "scenarios": {verified.scenario_id: verified.to_dict()}}, ensure_ascii=False), encoding="utf-8")
            state_path.write_text(json.dumps({"active_mode": "scenario"}), encoding="utf-8")
            actual_args = parser.parse_args(["external-run", "--project-root", str(root), "--output-dir", str(root / "artifacts"), "--scenario-catalog", catalog_path.name, "--gate-state", state_path.name])
            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                actual_exit = actual_args.func(actual_args)
            # 3.1 同一 verified local 失败场景再经真实脚本进程执行，锁定发布流水线可直接消费的退出码 1。
            script = ENGINE_ROOT / "generate_release_test_plan.py"
            process_result = subprocess.run(
                [sys.executable, "-X", "utf8", str(script), "external-run", "--project-root", str(root), "--output-dir", str(root / "subprocess-artifacts"), "--scenario-catalog", catalog_path.name, "--gate-state", state_path.name],
                check=False,
                capture_output=True,
                text=True,
                encoding="utf-8",
            )
        self.assertEqual(1, actual_exit, output.getvalue())
        self.assertEqual(1, process_result.returncode, process_result.stdout + process_result.stderr)
        self.assertIn('"scenario_id": "external-default-flow"', output.getvalue())
        self.assertNotIn("SCENARIO_CUTOVER_NOT_ACTIVATED", output.getvalue())
        # 4. 显式 shadow 仍可覆盖默认值，保证迁移期双轨入口可用。
        shadow_args = parser.parse_args(["external-run", "--project-root", ".", "--gate-mode", "shadow"])
        self.assertEqual("shadow", shadow_args.gate_mode)

    def test_release_run_uses_doctor_as_execution_gate(self) -> None:
        """验证 release-run 在工具依赖阻断时不会继续项目发现。

        [参数] 无。
        [返回] 无。
        最近修改时间: 2026-07-25 20:15:00 改动原因: doctor 必须成为发布执行前置门禁。
        """

        # 1. 模拟只读 doctor 阻断，并确认发现入口完全没有被调用。
        blocked = {"status": "BLOCKED", "missing_packages": ["websockets"], "mismatched_packages": [], "protocol_runtime": {}}
        with tempfile.TemporaryDirectory() as directory, mock.patch("release_test_engine.cli.inspect_tool_environment", return_value=blocked), mock.patch("release_test_engine.cli.discover_project") as discovery:
            result = run_pipeline(Path(directory), output_dir=Path(directory) / "artifacts", environment="local")
        self.assertEqual("BLOCKED", result["status"])
        self.assertEqual("TOOL_ENV_BLOCKED", result["failure_type"])
        discovery.assert_not_called()

    def test_pipeline_adopts_manifest_gate_for_cli_exit_status(self) -> None:
        """验证报告清单门禁成为 pipeline 状态和 CLI 退出码依据。

        [参数] 无。
        [返回] 无。
        最近修改时间：2026-07-25 23:18:15，禁止 manifest 非 PASS 被 CLI 原门禁覆盖。
        """

        # 1. 使用 local 空项目并替换报告落盘结果，精确验证 pipeline 对最终清单门禁的编排。
        report_result = {"gate": {"gate": "BLOCKED", "allow_release": False, "failure_type": "EVIDENCE_REDACTION_BLOCKED"}, "evidence_manifest_status": "FAIL"}
        with tempfile.TemporaryDirectory() as directory, mock.patch("release_test_engine.cli.write_report", return_value=report_result):
            result = run_pipeline(Path(directory), output_dir=Path(directory) / "artifacts", environment="local")
        self.assertEqual("BLOCKED", result["status"])
        self.assertEqual("BLOCKED", result["gate"]["gate"])
        self.assertEqual("FAIL", result["evidence_manifest_status"])

    def test_manifest_gate_uses_real_process_blocked_and_pending_exit_codes(self) -> None:
        """验证 manifest 敏感泄漏和短值限制映射真实进程退出码 3/4。

        [参数] 无。
        [返回] 无。
        最近修改时间：2026-07-25 23:37:04，同时锁定安全退出码与长敏感原值不进入子进程输出。
        """

        # 1. 子进程直接执行正式 write_report 和 CLI 状态映射，不把原始敏感值重新暴露给 pipeline 返回体。
        driver = """
import json
import sys
from pathlib import Path
from generate_release_test_plan import _status_exit_code
from release_test_engine.report import write_report

output = Path(sys.argv[1])
marker = sys.argv[2]
if len(marker) >= 4:
    (output / "untrusted.log").write_text(marker, encoding="utf-8")
artifacts = write_report(output, [{"operation_id": "safe", "status": "PASS"}], {"gate": "PASS", "allow_release": True, "passed": 1, "failed": 0, "pending": 0}, run_id="manifest-process", interfaces=[{"operation_id": "safe", "risk": "P0", "message": marker}], environment="local")
print(json.dumps({"gate": artifacts["gate"], "evidence_manifest_status": artifacts["evidence_manifest_status"]}))
raise SystemExit(_status_exit_code({"status": artifacts["gate"]["gate"]}))
"""
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            outcomes: list[tuple[str, int, str]] = []
            for name, marker in (("long", "manifest-sensitive-value"), ("short", "A")):
                output = root / name
                output.mkdir()
                completed = subprocess.run([sys.executable, "-X", "utf8", "-c", driver, str(output), marker], check=False, capture_output=True, text=True, encoding="utf-8", env={**os.environ, "PYTHONPATH": str(ENGINE_ROOT)})
                manifest = json.loads((output / "evidence-manifest.json").read_text(encoding="utf-8"))
                outcomes.append((manifest["status"], completed.returncode, completed.stdout + completed.stderr))
        # 2. 进程码分别对应安全 BLOCKED 和候选/验证缺口 PENDING，不依赖解析业务 JSON。
        self.assertEqual(("FAIL", 3), outcomes[0][:2], outcomes[0][2])
        self.assertEqual(("PENDING", 4), outcomes[1][:2], outcomes[1][2])
        self.assertNotIn("manifest-sensitive-value", outcomes[0][2])

    def test_external_cli_commands_and_exit_codes(self) -> None:
        """验证六个 external 入口及 0/2/3/4 退出码真实生效。

        [参数] 无。
        [返回] 无。
        最近修改时间: 2026-07-25 20:15:00 改动原因: 发布流水线必须依赖进程码而不是解析 JSON。
        """

        script = ENGINE_ROOT / "generate_release_test_plan.py"
        # 1. 主帮助必须同时暴露 doctor/generate/validate/verify/run/migrate 六个入口。
        help_result = subprocess.run([sys.executable, "-X", "utf8", str(script), "--help"], check=False, capture_output=True, text=True, encoding="utf-8")
        self.assertEqual(0, help_result.returncode, help_result.stderr)
        for command in ("external-doctor", "external-generate", "external-validate", "external-verify", "external-run", "external-migrate"):
            self.assertIn(command, help_result.stdout)
        # 2. candidate 生成返回 4，合法目录 validate 返回 0，未晋级 verify 返回 4。
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            interfaces = root / "interfaces.yaml"
            catalog = root / "scenario-catalog.yaml"
            interfaces.write_text(yaml.safe_dump([{"protocol": "http", "operation_id": "read-item", "risk": "P0", "adapter": "openapi", "entrypoint": {"method": "GET", "path": "/items/{id}"}}], sort_keys=False), encoding="utf-8")
            base = [sys.executable, "-X", "utf8", str(script)]
            generated = subprocess.run([*base, "external-generate", "--project-root", str(root), "--interfaces", interfaces.name, "--output", catalog.name, "--consumer", "frontend.item", "--source-name", interfaces.name], check=False, capture_output=True, text=True, encoding="utf-8")
            self.assertEqual(4, generated.returncode, generated.stdout + generated.stderr)
            validated = subprocess.run([*base, "external-validate", "--project-root", str(root), "--catalog", catalog.name], check=False, capture_output=True, text=True, encoding="utf-8")
            self.assertEqual(0, validated.returncode, validated.stdout + validated.stderr)
            verified = subprocess.run([*base, "external-verify", "--project-root", str(root), "--catalog", catalog.name], check=False, capture_output=True, text=True, encoding="utf-8")
            self.assertEqual(4, verified.returncode, verified.stdout + verified.stderr)
            # 3. 非 local 执行返回 3，非法场景契约返回 2。
            blocked = subprocess.run([*base, "release-run", "--project-root", str(root), "--environment", "production"], check=False, capture_output=True, text=True, encoding="utf-8")
            self.assertEqual(3, blocked.returncode, blocked.stdout + blocked.stderr)
            invalid = root / "invalid.yaml"
            invalid.write_text("""schema_version: wrong
scenarios: {}
""", encoding="utf-8")
            rejected = subprocess.run([*base, "external-validate", "--project-root", str(root), "--catalog", invalid.name], check=False, capture_output=True, text=True, encoding="utf-8")
            self.assertEqual(2, rejected.returncode, rejected.stdout + rejected.stderr)


if __name__ == "__main__":
    unittest.main()
