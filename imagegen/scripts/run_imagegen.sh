#!/usr/bin/env bash
set -euo pipefail

ACTION="${1:-}"
PROMPT="${2:-}"
OUT="${3:-output/imagegen/output.png}"
SIZE="${4:-1024x1024}"
QUALITY="${5:-medium}"
MODEL="${6:-}"
DRY_RUN="${7:-}"

SCRIPT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DEFAULT_CODEX_HOME="${HOME}/.codex"
RELATIVE_CODEX_HOME="$(cd "$SCRIPT_ROOT/../../../.." && pwd)"
CODEX_HOME_DIR="${CODEX_HOME:-}"
PROJECT_ROOT="${IMAGEGEN_PROJECT_ROOT:-$(pwd)}"
if [[ -z "$CODEX_HOME_DIR" ]]; then
  if [[ -d "$DEFAULT_CODEX_HOME" ]]; then
    CODEX_HOME_DIR="$DEFAULT_CODEX_HOME"
  else
    CODEX_HOME_DIR="$RELATIVE_CODEX_HOME"
  fi
fi

eval "$(python "$SCRIPT_ROOT/bootstrap_imagegen_env.py" --shell bash --codex-home "$CODEX_HOME_DIR" --project-root "$PROJECT_ROOT")"

if [[ -z "$MODEL" ]]; then
  MODEL="${IMAGEGEN_MODEL:-gpt-image-2}"
fi

if [[ "$ACTION" == "check" ]]; then
  echo "CODEX_HOME: $CODEX_HOME_DIR"
  echo "IMAGEGEN_PROJECT_ROOT: $PROJECT_ROOT"
  echo "ImageGen CLI: $SCRIPT_ROOT/image_gen.py"
  [[ -n "${OPENAI_API_KEY:-}" ]] && echo "OPENAI_API_KEY: SET" || echo "OPENAI_API_KEY: MISSING"
  [[ -n "${OPENAI_BASE_URL:-}" ]] && echo "OPENAI_BASE_URL: SET" || echo "OPENAI_BASE_URL: MISSING"
  echo "OPENAI_API_KEY source: ${IMAGEGEN_OPENAI_API_KEY_SOURCE:-unknown}"
  echo "OPENAI_BASE_URL source: ${IMAGEGEN_OPENAI_BASE_URL_SOURCE:-unknown}"
  echo "IMAGEGEN_MODEL: ${MODEL}"
  echo "IMAGEGEN_FALLBACK_MODEL: ${IMAGEGEN_FALLBACK_MODEL:-unset}"
  echo "IMAGEGEN_PRIORITY_RULE: ${IMAGEGEN_PRIORITY_RULE:-unset}"
  [[ -n "${IMAGEGEN_PROJECT_AGENTS_MD:-}" ]] && echo "Project AGENTS.md: ${IMAGEGEN_PROJECT_AGENTS_MD}"
  python - <<'PY'
import importlib.util
mods=["openai","PIL"]
for mod in mods:
    status = "OK" if importlib.util.find_spec(mod) else "MISSING"
    print(f"{mod}={status}")
PY
  python "$SCRIPT_ROOT/image_gen.py" generate \
    --prompt "dry run test imagegen system entry" \
    --size 1024x1024 \
    --out output/imagegen/dry-run-test.png \
    --dry-run
  exit 0
fi

if [[ "$ACTION" == "init-project-agents" ]]; then
  python "$SCRIPT_ROOT/bootstrap_imagegen_env.py" --shell bash --codex-home "$CODEX_HOME_DIR" --project-root "$PROJECT_ROOT" --init-project-agents-image-config >/dev/null
  echo "Initialized AGENTS.md imagegen template at project root if it was missing."
  exit 0
fi

if [[ "$ACTION" != "generate" ]]; then
  echo "Usage:"
  echo "  run_imagegen.sh check"
  echo "  run_imagegen.sh init-project-agents"
  echo "  run_imagegen.sh generate <prompt> [out] [size] [quality] [model] [--dry-run]"
  exit 1
fi

if [[ -z "$PROMPT" ]]; then
  echo "Prompt is required for generate"
  exit 1
fi

CMD=(python "$SCRIPT_ROOT/image_gen.py" generate --prompt "$PROMPT" --model "$MODEL" --quality "$QUALITY" --size "$SIZE" --out "$OUT")
if [[ "$DRY_RUN" == "--dry-run" ]]; then
  CMD+=(--dry-run)
fi
"${CMD[@]}"
