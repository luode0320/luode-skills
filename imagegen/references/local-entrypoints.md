# Local imagegen entrypoints

Use this file when the user wants a reusable local image generation entrypoint that works across projects, or asks how to configure image generation once and reuse it later.

## Goal

Provide a stable system-level way to run image generation without re-explaining:

- where auth comes from
- how to bridge Codex auth into `image_gen.py`
- how to check the environment
- how to run the CLI on Windows or Linux

## Auth bridge

The system-level bridge should prefer existing Codex local auth:

- current process env vars should stay highest priority
- if the project `AGENTS.md` declares fallback image config, prefer that fallback `api` / `baseurl` before shared Codex local auth
- otherwise, use the project-local image channel declared in the repo `AGENTS.md` before shared Codex local auth
- `~/.codex/auth.json` -> `OPENAI_API_KEY`
- `~/.codex/config.toml` -> `OPENAI_BASE_URL`

If the relevant env vars are already set, preserve them.
Only fall back to reading those files when env vars are absent.

Recommended priority:

1. current process environment variables
2. project `AGENTS.md` fallback image config
3. project `AGENTS.md` image config
4. `~/.codex/auth.json` + `~/.codex/config.toml`

Recommended project `AGENTS.md` format:

```text
## 图像生成配置

- `AGENTS.md` 里只允许写图像通道的读取位置、`baseurl`、模型名、优先级和回退规则；不得明文写真实 `OPENAI_API_KEY`。
- `api` 字段推荐写成 `env:PROJECT_IMAGE_OPENAI_API_KEY`、`env:OPENAI_API_KEY`、`codex-auth:OPENAI_API_KEY` 这类读取约定，而不是明文密钥。
- `baseurl` 字段推荐写成 `env:PROJECT_IMAGE_OPENAI_BASE_URL`、`env:OPENAI_BASE_URL`、`codex-config:base_url` 这类读取约定。
- `model` 字段用于声明当前项目默认图像模型；如果调用时没有显式传 `--model`，脚本会优先使用这里的模型。
- 如果用户在 `AGENTS.md` 里明确配置了 `回退规则：回退配置` 下的 `api` / `baseurl`，则在当前进程环境变量之后优先使用这组回退配置；这是用户主动声明的项目图像通道，应先于共享 Codex local 配置。
- 当项目未声明回退配置，或回退配置解析不出有效值时，再使用本项目 `AGENTS.md` 中声明的常规项目级图像通道。
- `imagegen` 的配置优先级默认是：当前进程环境变量 > 本项目 `AGENTS.md` 回退配置 > 本项目 `AGENTS.md` 图像配置 > `~/.codex/auth.json` + `~/.codex/config.toml`。
- 该项目级图像配置只用于图像生成相关流程，不用于覆盖普通文本模型配置。
- 如果项目级图像通道也不可用，必须明确告知当前图像入口仍不可用，并提示继续补充新的图像通道，而不是假装已生成成功。
- 图像配置格式固定如下，供 `imagegen` skill 自动读取：

图像配置:
api: env:PROJECT_IMAGE_OPENAI_API_KEY
baseurl: env:PROJECT_IMAGE_OPENAI_BASE_URL
model: gpt-image-2
fallback_model: gpt-image-1.5
priority: env > project-fallback > project-agents > codex-local
回退规则：回退配置
api: env:PROJECT_IMAGE_FALLBACK_OPENAI_API_KEY
baseurl: env:PROJECT_IMAGE_FALLBACK_OPENAI_BASE_URL
```

This project-level fallback is only for image generation. It should not be treated as a generic text-model override.
Recommended safe fill methods:

- Use `env:YOUR_ENV_NAME` when the real key or base URL lives in local/project runtime env vars.
- Use `codex-auth:OPENAI_API_KEY` to bridge the shared local `~/.codex/auth.json` key.
- Use `codex-config:base_url` to bridge the shared local `~/.codex/config.toml` base URL.

Do not store real secrets in `AGENTS.md`.

Initialize the project template when it is missing:

```powershell
powershell -ExecutionPolicy Bypass -File "$env:USERPROFILE\.codex\skills\imagegen\scripts\run_imagegen.ps1" -Action init-project-agents
```

```bash
bash "$HOME/.codex/skills/imagegen/scripts/run_imagegen.sh" init-project-agents
```

## Cross-platform scripts

System-level scripts should exist for both:

- Windows PowerShell
- Linux/macOS bash

Recommended script roles:

- `bootstrap_imagegen_env.py`
- `run_imagegen.ps1`
- `run_imagegen.sh`

## Default commands

Windows check:

```powershell
powershell -ExecutionPolicy Bypass -File "$env:USERPROFILE\.codex\skills\imagegen\scripts\run_imagegen.ps1" -Action check
```

Windows generate:

```powershell
powershell -ExecutionPolicy Bypass -File "$env:USERPROFILE\.codex\skills\imagegen\scripts\run_imagegen.ps1" `
  -Action generate `
  -Prompt "top-down arena map preview" `
  -Out "output/imagegen/map-preview.png"
```

Linux check:

```bash
bash "$HOME/.codex/skills/imagegen/scripts/run_imagegen.sh" check
```

Linux init project `AGENTS.md` image config template:

```bash
bash "$HOME/.codex/skills/imagegen/scripts/run_imagegen.sh" init-project-agents
```

Linux generate:

```bash
bash "$HOME/.codex/skills/imagegen/scripts/run_imagegen.sh" \
  generate "top-down arena map preview" output/imagegen/map-preview.png
```

## Trigger guidance

This path should be used when:

- the user wants to generate images in the current project
- the user wants a reusable image generation setup for future projects
- the built-in image tool is unavailable
- the user wants CLI/API/model-path control

## Validation

Environment validation should always confirm:

- imagegen CLI exists
- auth bridge succeeded or clearly reports missing auth
- auth/baseurl source is visible: env, project `AGENTS.md`, or Codex local config
- `openai` import works
- `PIL` import works
- dry-run succeeds

## Boundaries

This setup does not replace design review, art direction, or confirmation gates.
It only solves the execution and environment side of image generation.
