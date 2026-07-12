import contextlib
import importlib.util
import io
import sys
import tempfile
import types
import unittest
from pathlib import Path


SCRIPT_PATH = Path(__file__).resolve().parents[6] / "project-release-test-rules" / "scripts" / "generate_release_test_plan.py"


def load_cli_module():
    spec = importlib.util.spec_from_file_location("release_test_plan_cli_contract", SCRIPT_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class CliContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cli = load_cli_module()

    def test_parser_keeps_legacy_commands_and_adds_new_entries(self):
        parser = self.cli.build_parser()
        commands = parser._subparsers._group_actions[0].choices
        expected = {
            "bootstrap-inventory",
            "reconcile-inventory",
            "generate-plan",
            "init-release-test-task",
            "init-baseline-assets",
            "build-dependency-graph",
            "validate-reusable-params",
            "resolve-test-data",
            "update-baseline-assets",
            "sync-interface-contract-assets",
            "doctor",
            "run",
            "migrate-baseline",
        }
        self.assertEqual(expected, set(commands))

    def test_doctor_and_run_parameter_contract(self):
        parser = self.cli.build_parser()
        doctor = parser.parse_args(["doctor", "--project-root", "."])
        self.assertEqual("doctor", doctor.command)
        self.assertEqual("doc/5-tests/基线", doctor.baseline_root)
        self.assertEqual(["auto"], doctor.adapters)

        run = parser.parse_args(["run", "--project-root", ".", "--dry-run"])
        self.assertEqual("run", run.command)
        self.assertTrue(run.dry_run)
        self.assertEqual([], run.modules)
        self.assertEqual(["auto"], run.adapters)

    def test_legacy_command_without_compat_handler_keeps_legacy_behavior(self):
        calls = []
        package = types.ModuleType("release_test_engine")
        engine_cli = types.ModuleType("release_test_engine.cli")

        def run_pipeline(payload):
            calls.append(payload)
            raise AssertionError("legacy command must not invoke the complete run pipeline")

        engine_cli.run_pipeline = run_pipeline
        package.cli = engine_cli
        original = {name: sys.modules.get(name) for name in ("release_test_engine", "release_test_engine.cli")}
        sys.modules["release_test_engine"] = package
        sys.modules["release_test_engine.cli"] = engine_cli
        try:
            with tempfile.TemporaryDirectory() as temp_dir:
                root = Path(temp_dir)
                (root / "routes.py").write_text('GET("/health")\n', encoding="utf-8")
                inventory = root / "inventory.yaml"
                args = self.cli.build_parser().parse_args(
                    ["bootstrap-inventory", "--project-root", str(root), "--inventory", str(inventory)]
                )
                output = io.StringIO()
                with contextlib.redirect_stdout(output):
                    args.func(args)
                self.assertEqual([], calls)
                self.assertIn('"mode": "bootstrap-inventory"', output.getvalue())
                self.assertTrue(inventory.is_file())
        finally:
            for name, value in original.items():
                if value is None:
                    sys.modules.pop(name, None)
                else:
                    sys.modules[name] = value

    def test_legacy_command_delegates_only_to_explicit_compat_handler(self):
        calls = []
        package = types.ModuleType("release_test_engine")
        engine_cli = types.ModuleType("release_test_engine.cli")

        def compat_bootstrap_inventory(payload):
            calls.append(payload)
            return {"status": "PASS", "compat_command": payload["compat_command"]}

        engine_cli.compat_bootstrap_inventory = compat_bootstrap_inventory
        package.cli = engine_cli
        original = {name: sys.modules.get(name) for name in ("release_test_engine", "release_test_engine.cli")}
        sys.modules["release_test_engine"] = package
        sys.modules["release_test_engine.cli"] = engine_cli
        try:
            args = self.cli.build_parser().parse_args(
                ["bootstrap-inventory", "--project-root", ".", "--inventory", "inventory.yaml"]
            )
            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                args.func(args)
            self.assertEqual("bootstrap-inventory", calls[0]["compat_command"])
            self.assertNotIn("func", calls[0])
            self.assertIn('"status": "PASS"', output.getvalue())
        finally:
            for name, value in original.items():
                if value is None:
                    sys.modules.pop(name, None)
                else:
                    sys.modules[name] = value

    def test_missing_engine_returns_structured_pending_for_run(self):
        original_loader = self.cli._load_engine_entrypoint
        self.cli._load_engine_entrypoint = lambda name: None
        try:
            args = self.cli.build_parser().parse_args(["run", "--project-root", "."])
            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                args.func(args)
            self.assertIn('"status": "PENDING"', output.getvalue())
            self.assertIn('"failure_type": "UNSUPPORTED_ENGINE"', output.getvalue())
        finally:
            self.cli._load_engine_entrypoint = original_loader

    def test_nonlocal_environment_is_blocked_before_engine_call(self):
        args = self.cli.build_parser().parse_args(["run", "--project-root", ".", "--environment", "prod"])
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            args.func(args)
        self.assertIn('"status": "BLOCKED"', output.getvalue())
        self.assertIn('"failure_type": "ENV_BLOCKED"', output.getvalue())

    def test_dry_run_does_not_call_engine_without_dry_run_parameter(self):
        calls = []
        package = types.ModuleType("release_test_engine")
        engine_cli = types.ModuleType("release_test_engine.cli")

        def run_pipeline(project_root, *, output_dir):
            calls.append(project_root)
            return {"status": "PASS"}

        engine_cli.run_pipeline = run_pipeline
        package.cli = engine_cli
        original = {name: sys.modules.get(name) for name in ("release_test_engine", "release_test_engine.cli")}
        sys.modules["release_test_engine"] = package
        sys.modules["release_test_engine.cli"] = engine_cli
        try:
            args = self.cli.build_parser().parse_args(["run", "--project-root", ".", "--dry-run"])
            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                args.func(args)
            self.assertEqual([], calls)
            self.assertIn('"failure_type": "UNSUPPORTED_DRY_RUN"', output.getvalue())
        finally:
            for name, value in original.items():
                if value is None:
                    sys.modules.pop(name, None)
                else:
                    sys.modules[name] = value

    def test_run_forwards_local_asset_files_to_kernel(self):
        calls = []
        package = types.ModuleType("release_test_engine")
        engine_cli = types.ModuleType("release_test_engine.cli")

        def run_pipeline(
            project_root,
            *,
            output_dir,
            baseline_root=None,
            config=None,
            inventory=None,
            plan=None,
            modules=None,
            adapters=None,
            include_p2=False,
            continue_on_failure=False,
            dry_run=False,
            reusable=None,
            sources=None,
            baseline_path=None,
        ):
            calls.append(
                {
                    "project_root": project_root,
                    "output_dir": output_dir,
                    "baseline_root": baseline_root,
                    "config": config,
                    "inventory": inventory,
                    "plan": plan,
                    "modules": modules,
                    "adapters": adapters,
                    "include_p2": include_p2,
                    "continue_on_failure": continue_on_failure,
                    "dry_run": dry_run,
                    "reusable": reusable,
                    "sources": sources,
                    "baseline_path": baseline_path,
                }
            )
            return {"status": "PASS"}

        engine_cli.run_pipeline = run_pipeline
        package.cli = engine_cli
        original = {name: sys.modules.get(name) for name in ("release_test_engine", "release_test_engine.cli")}
        sys.modules["release_test_engine"] = package
        sys.modules["release_test_engine.cli"] = engine_cli
        try:
            with tempfile.TemporaryDirectory() as temp_dir:
                root = Path(temp_dir)
                reusable = root / "reusable.yaml"
                sources = root / "sources.yaml"
                inventory = root / "inventory.yaml"
                config = root / "local.yaml"
                plan = root / "plan.yaml"
                baseline_root = root / "baseline"
                reusable.write_text("params: {}\n", encoding="utf-8")
                sources.write_text("parameters: {}\n", encoding="utf-8")
                inventory.write_text("[]\n", encoding="utf-8")
                config.write_text("environment: local\n", encoding="utf-8")
                plan.write_text("scenarios: []\n", encoding="utf-8")
                args = self.cli.build_parser().parse_args(
                    [
                        "run",
                        "--project-root",
                        str(root),
                        "--output-dir",
                        str(root / "out"),
                        "--baseline-root",
                        str(baseline_root),
                        "--config",
                        str(config),
                        "--reusable-params",
                        str(reusable),
                        "--parameter-sources",
                        str(sources),
                        "--inventory",
                        str(inventory),
                        "--plan",
                        str(plan),
                        "--modules",
                        "orders",
                        "users",
                        "--adapters",
                        "http",
                        "graphql",
                        "--include-p2",
                        "--continue-on-failure",
                        "--dry-run",
                    ]
                )
                with contextlib.redirect_stdout(io.StringIO()):
                    args.func(args)
            self.assertEqual(str(Path(temp_dir).resolve()), calls[0]["project_root"])
            self.assertEqual(str(baseline_root), calls[0]["baseline_root"])
            self.assertEqual(str(config), calls[0]["config"])
            self.assertEqual(str(inventory), calls[0]["inventory"])
            self.assertEqual(str(plan), calls[0]["plan"])
            self.assertEqual(["orders", "users"], calls[0]["modules"])
            self.assertEqual(["http", "graphql"], calls[0]["adapters"])
            self.assertTrue(calls[0]["include_p2"])
            self.assertTrue(calls[0]["continue_on_failure"])
            self.assertTrue(calls[0]["dry_run"])
            self.assertEqual({"params": {}}, calls[0]["reusable"])
            self.assertEqual({"parameters": {}}, calls[0]["sources"])
            self.assertTrue(calls[0]["baseline_path"].endswith("inventory.yaml"))
        finally:
            for name, value in original.items():
                if value is None:
                    sys.modules.pop(name, None)
                else:
                    sys.modules[name] = value


if __name__ == "__main__":
    unittest.main()
