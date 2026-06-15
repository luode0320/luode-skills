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

- `~/.codex/auth.json` -> `OPENAI_API_KEY`
- `~/.codex/config.toml` -> `OPENAI_BASE_URL`
- current process env vars should stay highest priority
- if the shared Codex auth/config does not expose usable image models, the bridge may fall back to a project-local image channel declared in the repo `AGENTS.md`

If the relevant env vars are already set, preserve them.
Only fall back to reading those files when env vars are absent.

Recommended priority:

1. current process environment variables
2. project `AGENTS.md` image config
3. `~/.codex/auth.json` + `~/.codex/config.toml`

Recommended project `AGENTS.md` format:

```text
## 图像生成配置

- 当共享 `~/.codex/config.toml + auth.json` 对接的默认图像通道不可用、缺少 `gpt-image-2` / `gpt-image-1.5` / `gpt-image-1`，或返回 `model_not_found`、`No available channel` 时，允许 `imagegen` skill 优先读取本项目 `AGENTS.md` 中声明的项目级图像通道，作为当前项目的临时/专用图像生成配置。
- `imagegen` 的配置优先级默认是：当前进程环境变量 > 本项目 `AGENTS.md` 图像配置 > `~/.codex/auth.json` + `~/.codex/config.toml`。
- 该项目级图像配置只用于图像生成相关流程，不用于覆盖普通文本模型配置。
- 如果项目级图像通道也不可用，必须明确告知当前图像入口仍不可用，并提示继续补充新的图像通道，而不是假装已生成成功。
- 图像配置格式固定如下，供 `imagegen` skill 自动读取：

图像配置:
api: ???
baseurl: ???
```

This project-level fallback is only for image generation. It should not be treated as a generic text-model override.
The `???` placeholders are intentionally invalid. Treat them as missing config until the user fills real values locally.

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
