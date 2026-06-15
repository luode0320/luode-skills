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
    "<your-api-key>",
    "<your-base-url>",
    "<project image api key>",
    "<project image base url>",
    "your-api-key",
    "your-base-url",
}

AGENTS_IMAGE_CONFIG_TEMPLATE = """
## 图像生成配置

- 当共享 `~/.codex/config.toml + auth.json` 对接的默认图像通道不可用、缺少 `gpt-image-2` / `gpt-image-1.5` / `gpt-image-1`，或返回 `model_not_found`、`No available channel` 时，允许 `imagegen` skill 优先读取本项目 `AGENTS.md` 中声明的项目级图像通道，作为当前项目的临时/专用图像生成配置。
- `imagegen` 的配置优先级默认是：当前进程环境变量 > 本项目 `AGENTS.md` 图像配置 > `~/.codex/auth.json` + `~/.codex/config.toml`。
- 该项目级图像配置只用于图像生成相关流程，不用于覆盖普通文本模型配置。
- 如果项目级图像通道也不可用，必须明确告知当前图像入口仍不可用，并提示继续补充新的图像通道，而不是假装已生成成功。
- 图像配置格式固定如下，供 `imagegen` skill 自动读取：

图像配置:
api: ???
baseurl: ???
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


def read_agents_image_config(project_root: Path | None) -> tuple[str | None, str | None, Path | None]:
    if project_root is None:
        return None, None, None

    agents_path = find_agents_md(project_root)
    if agents_path is None:
        return None, None, None

    try:
        text = agents_path.read_text(encoding="utf-8")
    except Exception:
        return None, None, agents_path

    pattern = re.compile(
        r"图像配置\s*[:：]\s*(?:\r?\n)+\s*api\s*[:：]\s*(?P<api>\S+)\s*(?:\r?\n)+\s*baseurl\s*[:：]\s*(?P<baseurl>\S+)",
        re.IGNORECASE,
    )
    match = pattern.search(text)
    if not match:
        return None, None, agents_path

    api = normalize_config_value(match.group("api"))
    base_url = normalize_config_value(match.group("baseurl"))
    return api, base_url, agents_path


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
    agents_key, agents_base_url, agents_path = read_agents_image_config(project_root)

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
    else:
        emit_powershell(key, base_url)
        emit_powershell_meta(key_source, base_url_source, agents_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
