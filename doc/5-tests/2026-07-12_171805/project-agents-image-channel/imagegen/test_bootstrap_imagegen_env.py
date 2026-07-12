from __future__ import annotations

import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

REPOSITORY_ROOT = Path(__file__).resolve().parents[5]
SCRIPT_PATH = REPOSITORY_ROOT / "imagegen" / "scripts" / "bootstrap_imagegen_env.py"
sys.path.insert(0, str(SCRIPT_PATH.parent))
import bootstrap_imagegen_env as bootstrap


class BootstrapImagegenEnvTests(unittest.TestCase):
    def setUp(self) -> None:
        """隔离当前测试进程的图像环境变量。

        [参数] self: 测试实例。
        [返回] 无。
        最近修改时间：2026-07-12 17:32:24；保证 fixture 优先级测试不污染宿主环境。
        """
        # 1. 保存并清除测试涉及的环境变量。
        self._environment = {
            name: os.environ.get(name)
            for name in (
                "IMAGEGEN_API_KEY",
                "IMAGEGEN_BASE_URL",
                "OPENAI_API_KEY",
                "OPENAI_BASE_URL",
            )
        }
        for name in self._environment:
            os.environ.pop(name, None)

    def tearDown(self) -> None:
        """恢复测试前的图像环境变量。

        [参数] self: 测试实例。
        [返回] 无。
        最近修改时间：2026-07-12 17:32:24；保证 local fixture 测试结束后恢复进程状态。
        """
        # 1. 按测试前快照恢复或删除环境变量。
        for name, value in self._environment.items():
            if value is None:
                os.environ.pop(name, None)
            else:
                os.environ[name] = value

    @staticmethod
    def _write_fixture(codex_home: Path, project_root: Path, *, provider: str | None, base_url: str | None) -> None:
        """写入脱敏的 Codex provider fixture。

        [参数] codex_home: 临时 Codex 目录；project_root: 临时项目目录；provider: 活动 provider；base_url: provider URL。
        [返回] 无。
        最近修改时间：2026-07-12 17:32:24；集中构造 OpenAI/custom/缺失 provider 测试输入。
        """
        # 1. 创建目录并写入非真实鉴权 fixture。
        codex_home.mkdir(parents=True, exist_ok=True)
        project_root.mkdir(parents=True, exist_ok=True)
        (codex_home / "auth.json").write_text(
            '{"OPENAI_API_KEY": "fixture-key"}\n',
            encoding="utf-8",
        )
        provider_lines = []
        if provider is not None:
            provider_lines.append(f'model_provider = "{provider}"')
            provider_lines.append("")
            provider_lines.append(f"[model_providers.{provider}]")
            if base_url is not None:
                provider_lines.append(f'base_url = "{base_url}"')
        (codex_home / "config.toml").write_text("\n".join(provider_lines) + "\n", encoding="utf-8")

    @staticmethod
    def _run_cli(codex_home: Path, project_root: Path, *, extra_env: dict[str, str] | None = None) -> str:
        """在临时 local fixture 中执行环境 bootstrap CLI。

        [参数] codex_home: 临时 Codex 目录；project_root: 临时项目目录；extra_env: 可选环境变量覆盖。
        [返回] CLI 输出文本。
        最近修改时间：2026-07-12 17:32:24；验证 provider-neutral 与旧环境变量优先级。
        """
        # 1. 清理宿主鉴权变量并合并当前用例的临时变量。
        environment = os.environ.copy()
        for name in ("IMAGEGEN_API_KEY", "IMAGEGEN_BASE_URL", "OPENAI_API_KEY", "OPENAI_BASE_URL"):
            environment.pop(name, None)
        if extra_env:
            environment.update(extra_env)
        # 2. 以不联网的解析器入口执行并返回标准输出。
        result = subprocess.run(
            [
                sys.executable,
                str(SCRIPT_PATH),
                "--shell",
                "bash",
                "--codex-home",
                str(codex_home),
                "--project-root",
                str(project_root),
            ],
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
            env=environment,
        )
        return result.stdout

    def test_reads_active_custom_provider_base_url(self) -> None:
        """验证 custom provider URL 解析。

        [参数] self: 测试实例。
        [返回] 无。
        最近修改时间：2026-07-12 17:32:24；覆盖当前渠道跟随需求的 custom 分支。
        """
        # 1. 构造 custom provider 并读取活动配置。
        with tempfile.TemporaryDirectory() as root:
            base = Path(root)
            codex_home = base / "codex"
            project_root = base / "project"
            self._write_fixture(codex_home, project_root, provider="custom", base_url="https://custom.invalid/v1")

            provider, base_url = bootstrap.read_active_provider(codex_home)

            self.assertEqual(provider, "custom")
            self.assertEqual(base_url, "https://custom.invalid/v1")

    def test_reads_active_openai_provider_base_url(self) -> None:
        """验证 OpenAI provider URL 解析。

        [参数] self: 测试实例。
        [返回] 无。
        最近修改时间：2026-07-12 17:32:24；补齐 OpenAI/custom 双 provider 回归覆盖。
        """
        # 1. 构造 OpenAI provider 并读取活动配置。
        with tempfile.TemporaryDirectory() as root:
            base = Path(root)
            codex_home = base / "codex"
            project_root = base / "project"
            self._write_fixture(codex_home, project_root, provider="openai", base_url="https://openai.invalid/v1")

            provider, base_url = bootstrap.read_active_provider(codex_home)

            self.assertEqual(provider, "openai")
            self.assertEqual(base_url, "https://openai.invalid/v1")

    def test_reads_legacy_top_level_base_url_without_provider(self) -> None:
        """验证旧版顶层 base_url 兼容读取。

        [参数] self: 测试实例。
        [返回] 无。
        最近修改时间：2026-07-12 17:32:24；保留旧 Codex 配置兼容路径。
        """
        # 1. 构造只有旧顶层 URL 的配置并验证兼容结果。
        with tempfile.TemporaryDirectory() as root:
            codex_home = Path(root) / "codex"
            codex_home.mkdir()
            (codex_home / "config.toml").write_text('base_url = "https://legacy.invalid/v1"\n', encoding="utf-8")

            provider, base_url = bootstrap.read_active_provider(codex_home)

            self.assertIsNone(provider)
            self.assertEqual(base_url, "https://legacy.invalid/v1")

    def test_active_provider_tokens_resolve_project_config(self) -> None:
        """验证项目规则中的 active-provider token。

        [参数] self: 测试实例。
        [返回] 无。
        最近修改时间：2026-07-12 17:32:24；确保新模板 token 能桥接 key 与 URL。
        """
        # 1. 写入 active-provider 项目配置并解析 Codex fixture。
        with tempfile.TemporaryDirectory() as root:
            base = Path(root)
            codex_home = base / "codex"
            project_root = base / "project"
            self._write_fixture(codex_home, project_root, provider="custom", base_url="https://custom.invalid/v1")
            (project_root / "AGENTS.md").write_text(
                """## 图像生成配置

图像配置:
api: codex-auth:active_provider_api_key
baseurl: codex-config:active_provider_base_url
model: gpt-image-2
""",
                encoding="utf-8",
            )

            api, base_url, *_rest = bootstrap.read_agents_image_config(project_root, codex_home)

            self.assertEqual(api, "fixture-key")
            self.assertEqual(base_url, "https://custom.invalid/v1")

    def test_provider_neutral_environment_precedes_legacy_environment(self) -> None:
        """验证 provider-neutral 环境变量优先于旧变量。

        [参数] self: 测试实例。
        [返回] 无。
        最近修改时间：2026-07-12 17:32:24；锁定当前进程环境变量最高优先级。
        """
        # 1. 同时设置新旧变量并执行 CLI 解析。
        with tempfile.TemporaryDirectory() as root:
            base = Path(root)
            codex_home = base / "codex"
            project_root = base / "project"
            self._write_fixture(codex_home, project_root, provider="custom", base_url="https://custom.invalid/v1")

            output = self._run_cli(
                codex_home,
                project_root,
                extra_env={
                    "IMAGEGEN_API_KEY": "generic-key",
                    "IMAGEGEN_BASE_URL": "https://generic.invalid/v1",
                    "OPENAI_API_KEY": "legacy-key",
                    "OPENAI_BASE_URL": "https://legacy.invalid/v1",
                },
            )

            self.assertIn('export OPENAI_API_KEY="generic-key"', output)
            self.assertIn('export OPENAI_BASE_URL="https://generic.invalid/v1"', output)
            self.assertIn('export IMAGEGEN_PROVIDER="custom"', output)
            self.assertIn('export IMAGEGEN_API_KEY_SOURCE="env"', output)
            self.assertIn('export IMAGEGEN_BASE_URL_SOURCE="env"', output)

    def test_missing_provider_does_not_inject_fixed_openai_url(self) -> None:
        """验证缺失 provider 时不注入固定渠道 URL。

        [参数] self: 测试实例。
        [返回] 无。
        最近修改时间：2026-07-12 17:32:24；防止无法解析时静默伪造默认渠道。
        """
        # 1. 使用空 provider 配置执行 CLI 并检查脱敏输出。
        with tempfile.TemporaryDirectory() as root:
            base = Path(root)
            codex_home = base / "codex"
            project_root = base / "project"
            self._write_fixture(codex_home, project_root, provider=None, base_url=None)

            output = self._run_cli(codex_home, project_root)

            self.assertNotIn("https://api.openai.com/v1", output)
            self.assertIn('export IMAGEGEN_PROVIDER="unknown"', output)
            self.assertIn('export IMAGEGEN_BASE_URL_SOURCE="missing"', output)

    def test_generated_template_is_provider_neutral(self) -> None:
        """验证生成模板使用 provider-neutral token。

        [参数] self: 测试实例。
        [返回] 无。
        最近修改时间：2026-07-12 17:32:24；防止模板回归固定供应商配置。
        """
        # 1. 检查模板 token、默认模型和固定 URL 禁止条件。
        self.assertIn("codex-auth:active_provider_api_key", bootstrap.AGENTS_IMAGE_CONFIG_TEMPLATE)
        self.assertIn("codex-config:active_provider_base_url", bootstrap.AGENTS_IMAGE_CONFIG_TEMPLATE)
        self.assertIn("model: gpt-image-2", bootstrap.AGENTS_IMAGE_CONFIG_TEMPLATE)
        self.assertNotIn("https://api.openai.com/v1", bootstrap.AGENTS_IMAGE_CONFIG_TEMPLATE)


if __name__ == "__main__":
    unittest.main()
