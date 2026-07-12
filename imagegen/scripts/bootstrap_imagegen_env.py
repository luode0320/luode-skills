#!/usr/bin/env python3
"""Bootstrap image generation env vars from project or the active Codex channel.

Resolution order:
1. current process env vars
2. project AGENTS.md fallback config
3. project AGENTS.md primary image config
4. the active provider in ~/.codex/config.toml and ~/.codex/auth.json
"""

from __future__ import annotations

import argparse
import json
import os
import re
import tomllib
from pathlib import Path

PLACEHOLDER_VALUES = {
    "???",
    "<api>",
    "<baseurl>",
    "<model>",
    "<your-api-key>",
    "<your-base-url>",
    "<your-model>",
    "<project image api key>",
    "<project image base url>",
    "<project image model>",
    "your-api-key",
    "your-base-url",
    "your-model",
}

AGENTS_IMAGE_CONFIG_TEMPLATE = """
## 图像生成配置

- `AGENTS.md` 里只允许写图像通道的读取位置、`baseurl`、模型名、优先级和回退规则；不得明文写真实密钥。
- `api` 字段推荐写成 `env:IMAGEGEN_API_KEY`、`env:OPENAI_API_KEY`、`codex-auth:active_provider_api_key` 这类读取约定，而不是明文密钥。
- `baseurl` 字段推荐写成 `env:IMAGEGEN_BASE_URL`、`env:OPENAI_BASE_URL`、`codex-config:active_provider_base_url` 这类读取约定；如确需项目专用地址，也允许写明确的 `https://...`。
- `model` 字段用于声明当前项目默认图像模型；若调用方没有显式传 `--model`，运行脚本会优先读取这里的模型。
- 如果用户在 `AGENTS.md` 里明确配置了 `回退规则：回退配置` 下的 `api` / `baseurl`，则在当前进程环境变量之后优先使用这组回退配置；这是用户主动声明的项目图像通道，应先于共享 Codex local 配置。
- 当项目未声明回退配置，或回退配置解析不出有效值时，再使用本项目 `AGENTS.md` 中声明的常规项目级图像通道。
- `imagegen` 的配置优先级默认是：当前进程环境变量 > 本项目 `AGENTS.md` 回退配置 > 本项目 `AGENTS.md` 图像配置 > 当前 Codex provider 配置与 auth bridge。
- 该项目级图像配置只用于图像生成相关流程，不用于覆盖普通文本模型配置。
- 如果当前 provider 不是 OpenAI-compatible 图像通道，必须明确告知当前图像入口 unavailable，不得回退到预置渠道 URL或假装已生成成功。
- 图像配置格式固定如下，供 `imagegen` skill 自动读取：

图像配置:
api: codex-auth:active_provider_api_key
baseurl: codex-config:active_provider_base_url
model: gpt-image-2
fallback_model: gpt-image-1.5
priority: env > project-fallback > project-agents > codex-current-provider

回退规则：回退配置
api: ''
baseurl: ''
""".strip()


def find_agents_md(start: Path) -> Path | None:
    current = start.resolve()
    candidates = [current, *current.parents] if current.is_dir() else [current.parent, *current.parent.parents]
    for base in candidates:
        agents_path = base / "AGENTS.md"
        if agents_path.exists():
            return agents_path
    return None


def normalize_config_value(value: str | None) -> str | None:
    if value is None:
        return None
    cleaned = value.strip()
    if not cleaned:
        return None
    if cleaned.lower() in PLACEHOLDER_VALUES:
        return None
    return cleaned


def ensure_agents_image_config_block(project_root: Path | None) -> tuple[Path | None, bool]:
    if project_root is None:
        return None, False

    agents_path = find_agents_md(project_root)
    if agents_path is None:
        base = project_root.resolve()
        if not base.is_dir():
            base = base.parent
        agents_path = base / "AGENTS.md"
        agents_path.write_text("# AGENTS.md\n\n" + AGENTS_IMAGE_CONFIG_TEMPLATE + "\n", encoding="utf-8")
        return agents_path, True

    try:
        text = agents_path.read_text(encoding="utf-8")
    except Exception:
        return agents_path, False

    if "## 图像生成配置" in text and "图像配置:" in text and "回退规则：回退配置" in text:
        return agents_path, False

    new_text = text.rstrip() + "\n\n" + AGENTS_IMAGE_CONFIG_TEMPLATE + "\n"
    agents_path.write_text(new_text, encoding="utf-8")
    return agents_path, True


def _read_named_block_map(text: str, heading_pattern: str) -> dict[str, str]:
    lines = text.splitlines()
    start_index = None
    for index, line in enumerate(lines):
        if re.match(heading_pattern, line):
            start_index = index + 1
            break

    if start_index is None:
        return {}

    config: dict[str, str] = {}
    for line in lines[start_index:]:
        stripped = line.strip()
        if not stripped:
            if config:
                break
            continue
        if stripped.startswith("#"):
            if config:
                break
            continue
        if re.match(r"^(##\s+|[-*]\s+)", stripped):
            if config:
                break
        match = re.match(r"^(?P<key>[A-Za-z0-9_-]+)\s*[:：]\s*(?P<value>.+?)\s*$", stripped)
        if match:
            config[match.group("key").lower()] = match.group("value").strip()
            continue
        if config:
            break

    return config


def _resolve_project_config_value(
    raw_value: str | None,
    *,
    codex_home: Path,
    value_kind: str,
) -> str | None:
    """解析项目图像配置 token。

    [参数] raw_value: 项目规则中的原始配置值；codex_home: Codex 用户配置目录；value_kind: 值类型。
    [返回] 解析后的 API key、base URL 或其他配置值；无法解析时返回 None。
    最近修改时间：2026-07-12 17:32:24；支持 active-provider token 并保留旧 token 兼容。
    """
    cleaned = normalize_config_value(raw_value)
    if cleaned is None:
        return None

    lower = cleaned.lower()
    # 1. 先解析当前进程环境变量，保持项目运行时覆盖优先级。
    if lower.startswith("env:"):
        env_name = cleaned.split(":", 1)[1].strip()
        if not env_name:
            return None
        return normalize_config_value(os.environ.get(env_name))

    # 2. 读取 Codex auth/config bridge，active-provider token 与旧 token 共用实现。
    if lower.startswith("codex-auth:"):
        key_name = cleaned.split(":", 1)[1].strip()
        if key_name.lower() not in {"openai_api_key", "active_provider_api_key"}:
            return None
        return normalize_config_value(read_auth_key(codex_home))

    if lower.startswith("codex-config:"):
        key_name = cleaned.split(":", 1)[1].strip()
        if key_name.lower() not in {"base_url", "active_provider_base_url"}:
            return None
        return normalize_config_value(read_base_url(codex_home))

    # 3. 处理显式 literal 和普通项目值，API 字段禁止误读为 URL。
    if lower.startswith("literal:"):
        return normalize_config_value(cleaned.split(":", 1)[1])

    if value_kind == "api" and cleaned.startswith("http"):
        return None

    return cleaned


def read_agents_image_config(
    project_root: Path | None,
    codex_home: Path,
) -> tuple[str | None, str | None, str | None, str | None, str | None, str | None, str | None, Path | None]:
    if project_root is None:
        return None, None, None, None, None, None, None, None

    agents_path = find_agents_md(project_root)
    if agents_path is None:
        return None, None, None, None, None, None, None, None

    try:
        text = agents_path.read_text(encoding="utf-8")
    except Exception:
        return None, None, None, None, None, None, None, agents_path

    primary_map = _read_named_block_map(text, r"^\s*图像配置\s*[:：]\s*$")
    fallback_map = _read_named_block_map(text, r"^\s*回退规则\s*[:：]\s*回退配置\s*$")
    if not primary_map and not fallback_map:
        return None, None, None, None, None, None, None, agents_path

    api = _resolve_project_config_value(primary_map.get("api"), codex_home=codex_home, value_kind="api")
    base_url = _resolve_project_config_value(primary_map.get("baseurl"), codex_home=codex_home, value_kind="baseurl")
    model = normalize_config_value(primary_map.get("model"))
    fallback_model = normalize_config_value(primary_map.get("fallback_model"))
    priority = normalize_config_value(primary_map.get("priority"))
    fallback_api = _resolve_project_config_value(fallback_map.get("api"), codex_home=codex_home, value_kind="api")
    fallback_base_url = _resolve_project_config_value(
        fallback_map.get("baseurl"),
        codex_home=codex_home,
        value_kind="baseurl",
    )
    return api, base_url, model, fallback_model, priority, fallback_api, fallback_base_url, agents_path


def read_auth_key(codex_home: Path) -> str | None:
    auth_path = codex_home / "auth.json"
    if not auth_path.exists():
        return None
    try:
        data = json.loads(auth_path.read_text(encoding="utf-8"))
    except Exception:
        return None
    value = data.get("OPENAI_API_KEY")
    return value if isinstance(value, str) and value.strip() else None


def read_codex_config(codex_home: Path) -> dict[str, object]:
    """读取并解析 Codex TOML 配置。

    [参数] codex_home: Codex 用户配置目录。
    [返回] TOML 配置字典；文件缺失、编码或语法错误时返回空字典。
    最近修改时间：2026-07-12 17:32:24；改用标准库 TOML 解析活动 provider 配置。
    """
    config_path = codex_home / "config.toml"
    # 1. 缺少用户配置时返回空结果，避免猜测默认渠道。
    if not config_path.exists():
        return {}
    # 2. 读取并解析当前 Codex 配置，解析失败时保持 unavailable 语义。
    try:
        return tomllib.loads(config_path.read_text(encoding="utf-8"))
    except (OSError, tomllib.TOMLDecodeError):
        return {}


def read_active_provider(codex_home: Path) -> tuple[str | None, str | None]:
    """解析当前活动 provider 及其 base URL。

    [参数] codex_home: Codex 用户配置目录。
    [返回] provider 名称与对应 base URL；缺失时分别返回 None。
    最近修改时间：2026-07-12 17:32:24；新增 model_provider 到 provider base_url 的解析链路。
    """
    # 1. 读取活动 provider 名称和 provider 配置块。
    config = read_codex_config(codex_home)
    raw_provider = config.get("model_provider")
    provider = normalize_config_value(raw_provider if isinstance(raw_provider, str) else None)
    providers = config.get("model_providers")
    provider_config = providers.get(provider) if provider and isinstance(providers, dict) else None
    base_url = None
    # 2. 优先使用活动 provider 的 base_url，避免跨渠道串用地址。
    if isinstance(provider_config, dict):
        raw_base_url = provider_config.get("base_url")
        if isinstance(raw_base_url, str):
            base_url = normalize_config_value(raw_base_url)
    if base_url is None:
        # 3. 仅兼容旧版顶层 base_url，不创建新的固定渠道回退。
        raw_base_url = config.get("base_url")
        if isinstance(raw_base_url, str):
            base_url = normalize_config_value(raw_base_url)
    # 4. 返回 provider 和 URL；缺失值由上层转换为 unavailable 诊断。
    return provider, base_url


def read_base_url(codex_home: Path) -> str | None:
    """返回活动 provider 的 base URL，并兼容旧版顶层配置。

    [参数] codex_home: Codex 用户配置目录。
    [返回] 活动 provider URL 或 None。
    最近修改时间：2026-07-12 17:32:24；让旧读取入口复用 active-provider 解析。
    """
    # 先读取当前 provider，再兼容旧版顶层 base_url，避免静默回退到固定渠道。
    _provider, base_url = read_active_provider(codex_home)
    return base_url


def emit_bash(key: str | None, base_url: str | None) -> None:
    if key:
        print(f'export OPENAI_API_KEY="{key}"')
    if base_url:
        print(f'export OPENAI_BASE_URL="{base_url}"')


def emit_bash_meta(
    provider: str | None,
    key_source: str,
    base_url_source: str,
    agents_path: Path | None,
) -> None:
    """输出 Bash 诊断元数据。

    [参数] provider: 当前 provider；key_source: API key 来源；base_url_source: base URL 来源；agents_path: 项目规则文件路径。
    [返回] 无。
    最近修改时间：2026-07-12 17:32:24；新增 provider-neutral source 诊断并保留旧元数据。
    """
    # 1. 输出不含密钥原值的 provider/source 元数据。
    print(f'export IMAGEGEN_PROVIDER="{provider or "unknown"}"')
    print(f'export IMAGEGEN_API_KEY_SOURCE="{key_source}"')
    print(f'export IMAGEGEN_BASE_URL_SOURCE="{base_url_source}"')
    print(f'export IMAGEGEN_OPENAI_API_KEY_SOURCE="{key_source}"')
    print(f'export IMAGEGEN_OPENAI_BASE_URL_SOURCE="{base_url_source}"')
    if agents_path:
        print(f'export IMAGEGEN_PROJECT_AGENTS_MD="{agents_path}"')


def emit_powershell(key: str | None, base_url: str | None) -> None:
    if key:
        print(f'$env:OPENAI_API_KEY="{key}"')
    if base_url:
        print(f'$env:OPENAI_BASE_URL="{base_url}"')


def emit_powershell_meta(
    provider: str | None,
    key_source: str,
    base_url_source: str,
    agents_path: Path | None,
) -> None:
    """输出 PowerShell 诊断元数据。

    [参数] provider: 当前 provider；key_source: API key 来源；base_url_source: base URL 来源；agents_path: 项目规则文件路径。
    [返回] 无。
    最近修改时间：2026-07-12 17:32:24；同步 Bash 诊断字段并保留旧元数据。
    """
    # 1. 输出不含密钥原值的 provider/source 元数据。
    print(f'$env:IMAGEGEN_PROVIDER="{provider or "unknown"}"')
    print(f'$env:IMAGEGEN_API_KEY_SOURCE="{key_source}"')
    print(f'$env:IMAGEGEN_BASE_URL_SOURCE="{base_url_source}"')
    print(f'$env:IMAGEGEN_OPENAI_API_KEY_SOURCE="{key_source}"')
    print(f'$env:IMAGEGEN_OPENAI_BASE_URL_SOURCE="{base_url_source}"')
    if agents_path:
        print(f'$env:IMAGEGEN_PROJECT_AGENTS_MD="{agents_path}"')


def main() -> int:
    """解析配置优先级并输出 SDK 环境桥接脚本。

    [参数] 无；命令行参数通过 argparse 读取。
    [返回] 成功时返回 0。
    最近修改时间：2026-07-12 17:32:24；接入 active provider 和 provider-neutral 环境变量。
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--shell", choices=["bash", "powershell"], required=True)
    parser.add_argument("--codex-home")
    parser.add_argument("--project-root")
    parser.add_argument("--init-project-agents-image-config", action="store_true")
    args = parser.parse_args()

    # 1. 确定 Codex 配置目录和项目规则文件位置。
    codex_home = Path(args.codex_home or os.environ.get("CODEX_HOME") or (Path.home() / ".codex"))
    project_root_arg = args.project_root or os.environ.get("IMAGEGEN_PROJECT_ROOT") or os.getcwd()
    project_root = Path(project_root_arg)
    # 2. 按需初始化 provider-neutral 项目模板。
    if args.init_project_agents_image_config:
        ensure_agents_image_config_block(project_root)

    (
        agents_key,
        agents_base_url,
        agents_model,
        agents_fallback_model,
        agents_priority,
        fallback_key,
        fallback_base_url,
        agents_path,
    ) = read_agents_image_config(project_root, codex_home)

    env_key = normalize_config_value(os.environ.get("IMAGEGEN_API_KEY"))
    env_key = env_key or normalize_config_value(os.environ.get("OPENAI_API_KEY"))
    env_base_url = normalize_config_value(os.environ.get("IMAGEGEN_BASE_URL"))
    env_base_url = env_base_url or normalize_config_value(os.environ.get("OPENAI_BASE_URL"))
    auth_key = read_auth_key(codex_home)
    provider, config_base_url = read_active_provider(codex_home)

    # 3. 依照 env、项目回退、项目主配置、Codex 当前 provider 的顺序解析值。
    if env_key:
        key = env_key
        key_source = "env"
    elif fallback_key:
        key = fallback_key
        key_source = "project-fallback"
    elif agents_key:
        key = agents_key
        key_source = "project-agents"
    else:
        key = auth_key
        key_source = "codex-auth" if auth_key else "missing"

    if env_base_url:
        base_url = env_base_url
        base_url_source = "env"
    elif fallback_base_url:
        base_url = fallback_base_url
        base_url_source = "project-fallback"
    elif agents_base_url:
        base_url = agents_base_url
        base_url_source = "project-agents"
    else:
        base_url = config_base_url
        base_url_source = "codex-config" if config_base_url else "missing"

    # 4. 输出 OpenAI-compatible SDK 变量和 provider-neutral 诊断字段。
    if args.shell == "bash":
        emit_bash(key, base_url)
        emit_bash_meta(provider, key_source, base_url_source, agents_path)
        if agents_model:
            print(f'export IMAGEGEN_MODEL="{agents_model}"')
        if agents_fallback_model:
            print(f'export IMAGEGEN_FALLBACK_MODEL="{agents_fallback_model}"')
        if agents_priority:
            print(f'export IMAGEGEN_PRIORITY_RULE="{agents_priority}"')
    else:
        emit_powershell(key, base_url)
        emit_powershell_meta(provider, key_source, base_url_source, agents_path)
        if agents_model:
            print(f'$env:IMAGEGEN_MODEL="{agents_model}"')
        if agents_fallback_model:
            print(f'$env:IMAGEGEN_FALLBACK_MODEL="{agents_fallback_model}"')
        if agents_priority:
            print(f'$env:IMAGEGEN_PRIORITY_RULE="{agents_priority}"')
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
