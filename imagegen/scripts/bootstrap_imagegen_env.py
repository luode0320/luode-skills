#!/usr/bin/env python3
"""Bootstrap OpenAI image generation env vars from Codex local or project config.

Reads:
- current process env vars first
- project AGENTS.md image config if present
- ~/.codex/auth.json for OPENAI_API_KEY
- ~/.codex/config.toml for base_url

Prints shell-ready exports for either bash or powershell.
"""

from __future__ import annotations

import argparse
import json
import os
import re
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

- `AGENTS.md` 里只允许写图像通道的读取位置、`baseurl`、模型名、优先级和回退规则；不得明文写真实 `OPENAI_API_KEY`。
- `api` 字段推荐写成 `env:PROJECT_IMAGE_OPENAI_API_KEY`、`env:OPENAI_API_KEY`、`codex-auth:OPENAI_API_KEY` 这类读取约定，而不是明文密钥。
- `baseurl` 字段推荐写成 `env:PROJECT_IMAGE_OPENAI_BASE_URL`、`env:OPENAI_BASE_URL`、`codex-config:base_url` 这类读取约定；如确需项目专用地址，也允许写明确的 `https://...`。
- `model` 字段用于声明当前项目默认图像模型；若调用方没有显式传 `--model`，运行脚本会优先读取这里的模型。
- 当共享 `~/.codex/config.toml + auth.json` 对接的默认图像通道不可用、缺少 `gpt-image-2` / `gpt-image-1.5` / `gpt-image-1`，或返回 `model_not_found`、`No available channel` 时，允许 `imagegen` skill 优先读取本项目 `AGENTS.md` 中声明的项目级图像通道读取约定，作为当前项目的临时/专用图像生成配置。
- `imagegen` 的配置优先级默认是：当前进程环境变量 > 本项目 `AGENTS.md` 图像配置 > `~/.codex/auth.json` + `~/.codex/config.toml`。
- 该项目级图像配置只用于图像生成相关流程，不用于覆盖普通文本模型配置。
- 如果项目级图像通道也不可用，必须明确告知当前图像入口仍不可用，并提示继续补充新的图像通道读取位置，而不是假装已生成成功。
- 图像配置格式固定如下，供 `imagegen` skill 自动读取：

图像配置:
api: env:PROJECT_IMAGE_OPENAI_API_KEY
baseurl: env:PROJECT_IMAGE_OPENAI_BASE_URL
model: gpt-image-2
fallback_model: gpt-image-1.5
priority: env > project-agents > codex-local
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

    if "## 图像生成配置" in text and "图像配置:" in text:
        return agents_path, False

    new_text = text.rstrip() + "\n\n" + AGENTS_IMAGE_CONFIG_TEMPLATE + "\n"
    agents_path.write_text(new_text, encoding="utf-8")
    return agents_path, True


def _read_config_block_map(text: str) -> dict[str, str]:
    lines = text.splitlines()
    start_index = None
    for index, line in enumerate(lines):
        if re.match(r"^\s*图像配置\s*[:：]\s*$", line):
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
    cleaned = normalize_config_value(raw_value)
    if cleaned is None:
        return None

    lower = cleaned.lower()
    if lower.startswith("env:"):
        env_name = cleaned.split(":", 1)[1].strip()
        if not env_name:
            return None
        return normalize_config_value(os.environ.get(env_name))

    if lower.startswith("codex-auth:"):
        key_name = cleaned.split(":", 1)[1].strip()
        if key_name.upper() != "OPENAI_API_KEY":
            return None
        return normalize_config_value(read_auth_key(codex_home))

    if lower.startswith("codex-config:"):
        key_name = cleaned.split(":", 1)[1].strip()
        if key_name != "base_url":
            return None
        return normalize_config_value(read_base_url(codex_home))

    if lower.startswith("literal:"):
        return normalize_config_value(cleaned.split(":", 1)[1])

    if value_kind == "api" and cleaned.startswith("http"):
        return None

    return cleaned


def read_agents_image_config(
    project_root: Path | None,
    codex_home: Path,
) -> tuple[str | None, str | None, str | None, str | None, str | None, Path | None]:
    if project_root is None:
        return None, None, None, None, None, None

    agents_path = find_agents_md(project_root)
    if agents_path is None:
        return None, None, None, None, None, None

    try:
        text = agents_path.read_text(encoding="utf-8")
    except Exception:
        return None, None, None, None, None, agents_path

    config_map = _read_config_block_map(text)
    if not config_map:
        return None, None, None, None, None, agents_path

    api = _resolve_project_config_value(config_map.get("api"), codex_home=codex_home, value_kind="api")
    base_url = _resolve_project_config_value(
        config_map.get("baseurl"),
        codex_home=codex_home,
        value_kind="baseurl",
    )
    model = normalize_config_value(config_map.get("model"))
    fallback_model = normalize_config_value(config_map.get("fallback_model"))
    priority = normalize_config_value(config_map.get("priority"))
    return api, base_url, model, fallback_model, priority, agents_path


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


def read_base_url(codex_home: Path) -> str | None:
    config_path = codex_home / "config.toml"
    if not config_path.exists():
        return None
    text = config_path.read_text(encoding="utf-8", errors="replace")
    match = re.search(r'base_url\s*=\s*"([^"]+)"', text)
    if not match:
        return None
    value = match.group(1).strip()
    return value or None


def emit_bash(key: str | None, base_url: str | None) -> None:
    if key:
        print(f'export OPENAI_API_KEY="{key}"')
    if base_url:
        print(f'export OPENAI_BASE_URL="{base_url}"')


def emit_bash_meta(key_source: str, base_url_source: str, agents_path: Path | None) -> None:
    print(f'export IMAGEGEN_OPENAI_API_KEY_SOURCE="{key_source}"')
    print(f'export IMAGEGEN_OPENAI_BASE_URL_SOURCE="{base_url_source}"')
    if agents_path:
        print(f'export IMAGEGEN_PROJECT_AGENTS_MD="{agents_path}"')


def emit_powershell(key: str | None, base_url: str | None) -> None:
    if key:
        print(f'$env:OPENAI_API_KEY="{key}"')
    if base_url:
        print(f'$env:OPENAI_BASE_URL="{base_url}"')


def emit_powershell_meta(key_source: str, base_url_source: str, agents_path: Path | None) -> None:
    print(f'$env:IMAGEGEN_OPENAI_API_KEY_SOURCE="{key_source}"')
    print(f'$env:IMAGEGEN_OPENAI_BASE_URL_SOURCE="{base_url_source}"')
    if agents_path:
        print(f'$env:IMAGEGEN_PROJECT_AGENTS_MD="{agents_path}"')


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--shell", choices=["bash", "powershell"], required=True)
    parser.add_argument("--codex-home")
    parser.add_argument("--project-root")
    parser.add_argument("--init-project-agents-image-config", action="store_true")
    args = parser.parse_args()

    codex_home = Path(args.codex_home or os.environ.get("CODEX_HOME") or (Path.home() / ".codex"))
    project_root_arg = args.project_root or os.environ.get("IMAGEGEN_PROJECT_ROOT") or os.getcwd()
    project_root = Path(project_root_arg)
    if args.init_project_agents_image_config:
        ensure_agents_image_config_block(project_root)
    agents_key, agents_base_url, agents_model, agents_fallback_model, agents_priority, agents_path = read_agents_image_config(
        project_root,
        codex_home,
    )

    env_key = os.environ.get("OPENAI_API_KEY")
    env_base_url = os.environ.get("OPENAI_BASE_URL")
    auth_key = read_auth_key(codex_home)
    config_base_url = read_base_url(codex_home)

    if env_key:
        key = env_key
        key_source = "env"
    elif agents_key:
        key = agents_key
        key_source = "project-agents"
    else:
        key = auth_key
        key_source = "codex-auth" if auth_key else "missing"

    if env_base_url:
        base_url = env_base_url
        base_url_source = "env"
    elif agents_base_url:
        base_url = agents_base_url
        base_url_source = "project-agents"
    else:
        base_url = config_base_url
        base_url_source = "codex-config" if config_base_url else "missing"

    if args.shell == "bash":
        emit_bash(key, base_url)
        emit_bash_meta(key_source, base_url_source, agents_path)
        if agents_model:
            print(f'export IMAGEGEN_MODEL="{agents_model}"')
        if agents_fallback_model:
            print(f'export IMAGEGEN_FALLBACK_MODEL="{agents_fallback_model}"')
        if agents_priority:
            print(f'export IMAGEGEN_PRIORITY_RULE="{agents_priority}"')
    else:
        emit_powershell(key, base_url)
        emit_powershell_meta(key_source, base_url_source, agents_path)
        if agents_model:
            print(f'$env:IMAGEGEN_MODEL="{agents_model}"')
        if agents_fallback_model:
            print(f'$env:IMAGEGEN_FALLBACK_MODEL="{agents_fallback_model}"')
        if agents_priority:
            print(f'$env:IMAGEGEN_PRIORITY_RULE="{agents_priority}"')
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
