#!/usr/bin/env bash
# Template: TAPD Weekly Progress Reporter
# Purpose: Open TAPD My Work, extract "this week" task progress, and generate a report.
# Usage: ./tapd-weekly-report.sh [base-date] [output-dir]
#
# Environment variables:
#   TAPD_WORK_URL             Default: https://www.tapd.cn/tapd_fe/my/work
#   TAPD_SESSION_NAME         Default: tapd_weekly
#   TAPD_STATE_FILE           Optional saved state file path
#   TAPD_LOGIN_WAIT_SECONDS   Default: 180
#   TAPD_FORCE_CLEAN_START    Default: 0 (set 1 to run close --all before start)
#
# Notes:
# - First run may still require one manual login (SSO/QR).
# - After login, keep using the same session name or state file for near-zero interaction.

set -euo pipefail

BASE_DATE="${1:-$(TZ=Asia/Shanghai date +%F)}"
OUTPUT_DIR="${2:-./tapd-weekly-$(TZ=Asia/Shanghai date +%Y%m%d%H%M%S)}"
TARGET_URL="${TAPD_WORK_URL:-https://www.tapd.cn/tapd_fe/my/work}"
SESSION_NAME="${TAPD_SESSION_NAME:-tapd_weekly}"
STATE_FILE="${TAPD_STATE_FILE:-}"
LOGIN_WAIT_SECONDS="${TAPD_LOGIN_WAIT_SECONDS:-180}"
FORCE_CLEAN_START="${TAPD_FORCE_CLEAN_START:-0}"

if command -v agent-browser >/dev/null 2>&1; then
  AB_CMD=(agent-browser)
else
  AB_CMD=(npx -y agent-browser)
fi

log() {
  printf '[tapd-weekly] %s\n' "$*"
}

warn() {
  printf '[tapd-weekly][warn] %s\n' "$*" >&2
}

die() {
  printf '[tapd-weekly][error] %s\n' "$*" >&2
  exit 1
}

ab() {
  "${AB_CMD[@]}" "$@"
}

open_target() {
  local extra_args=("$@")
  if [[ -n "$STATE_FILE" && -f "$STATE_FILE" ]]; then
    ab --session-name "$SESSION_NAME" --state "$STATE_FILE" "${extra_args[@]}" open "$TARGET_URL"
  else
    ab --session-name "$SESSION_NAME" "${extra_args[@]}" open "$TARGET_URL"
  fi
}

mkdir -p "$OUTPUT_DIR"

if [[ "$FORCE_CLEAN_START" == "1" ]]; then
  log "cleaning old browser sessions"
  ab close --all || true
fi

log "opening TAPD work page"
open_target
ab wait --load networkidle || true

title="$(ab get title || true)"
body="$(ab get text body || true)"
echo "$title" >"$OUTPUT_DIR/page-title.txt"
echo "$body" >"$OUTPUT_DIR/page-body.txt"

if [[ "$title" == *"WAF"* ]] || [[ "$body" == *"请求已中断"* ]]; then
  warn "WAF detected, retrying with anti-automation launch args"
  ab close --all || true
  open_target \
    --args '--disable-blink-features=AutomationControlled,--lang=zh-CN' \
    --user-agent 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36'
  ab wait --load networkidle || true
  title="$(ab get title || true)"
  body="$(ab get text body || true)"
fi

if [[ "$title" == *"登录-TAPD"* ]] || [[ "$body" == *"欢迎来到TAPD"* ]]; then
  warn "login required, waiting up to ${LOGIN_WAIT_SECONDS}s for manual auth"
  ab screenshot "$OUTPUT_DIR/login-required.png" || true
  waited=0
  while (( waited < LOGIN_WAIT_SECONDS )); do
    sleep 5
    waited=$((waited + 5))
    title="$(ab get title || true)"
    if [[ "$title" == *"我的工作-TAPD平台"* ]]; then
      break
    fi
  done
fi

title="$(ab get title || true)"
url_now="$(ab get url || true)"
if [[ "$title" != *"我的工作-TAPD平台"* ]]; then
  die "not on TAPD work page after retries/login wait; current title: $title"
fi

log "current url: $url_now"

log "switching to processed view and opening time filter"
ab find text 已办 click || true
ab wait 600 || true
ab find text 时间 click || true
ab wait 600 || true

SNAPSHOT_FILE="$OUTPUT_DIR/tapd-snapshot-week.txt"
ab snapshot -i >"$SNAPSHOT_FILE"

log "parsing weekly section from snapshot"
python3 - "$SNAPSHOT_FILE" "$BASE_DATE" "$OUTPUT_DIR" <<'PY'
import json
import re
import sys
from collections import Counter
from datetime import date, datetime, timedelta
from pathlib import Path

snapshot_file = Path(sys.argv[1])
base_date = date.fromisoformat(sys.argv[2])
output_dir = Path(sys.argv[3])

week_start = base_date - timedelta(days=base_date.weekday())
week_end = week_start + timedelta(days=6)

lines = snapshot_file.read_text(encoding="utf-8").splitlines()
start = None
end = None
for i, line in enumerate(lines):
    if "本周 (" in line and start is None:
        start = i
        continue
    if start is not None and ("今年 (" in line or "上周 (" in line):
        end = i
        break

section = lines[start:end] if start is not None else []
cell_pat = re.compile(r'^- cell "(.*)" \[ref=')
cells = []
for line in section:
    m = cell_pat.match(line.strip())
    if m:
        cells.append(m.group(1))

rows = []
i = 0
while i + 5 < len(cells):
    if re.fullmatch(r"\d{7}", cells[i]):
        row = {
            "id": cells[i],
            "title": cells[i + 1],
            "status": cells[i + 2],
            "handler": cells[i + 3],
            "priority": cells[i + 4],
            "time": cells[i + 5],
        }
        rows.append(row)
        i += 6
    else:
        i += 1

filtered = []
for row in rows:
    try:
        t = datetime.strptime(row["time"], "%Y-%m-%d %H:%M")
    except ValueError:
        continue
    if week_start <= t.date() <= week_end:
        filtered.append(row)

status_counter = Counter(r["status"] for r in filtered)
priority_counter = Counter(r["priority"] for r in filtered)
done_statuses = {"已实现", "已关闭", "已解决"}
done = sum(1 for r in filtered if r["status"] in done_statuses)
in_progress = len(filtered) - done
done_rate = (done / len(filtered) * 100) if filtered else 0.0

summary = {
    "base_date": base_date.isoformat(),
    "week_start": week_start.isoformat(),
    "week_end": week_end.isoformat(),
    "total": len(filtered),
    "done": done,
    "in_progress": in_progress,
    "done_rate": round(done_rate, 2),
    "status_distribution": dict(status_counter),
    "priority_distribution": dict(priority_counter),
    "rows": filtered,
}

(output_dir / "tapd-weekly-summary.json").write_text(
    json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8"
)

md = []
md.append(f"# TAPD Weekly Progress ({week_start} to {week_end})")
md.append("")
md.append("## Metrics")
md.append(f"- Total: {summary['total']}")
md.append(f"- Done: {summary['done']}")
md.append(f"- In Progress: {summary['in_progress']}")
md.append(f"- Done Rate: {summary['done_rate']}%")
md.append("")
md.append("## Status Distribution")
if status_counter:
    for k, v in status_counter.items():
        md.append(f"- {k}: {v}")
else:
    md.append("- No data")
md.append("")
md.append("## Priority Distribution")
if priority_counter:
    for k, v in priority_counter.items():
        md.append(f"- {k}: {v}")
else:
    md.append("- No data")
md.append("")
md.append("## Done Items")
done_rows = [r for r in filtered if r["status"] in done_statuses]
if done_rows:
    for r in done_rows:
        md.append(f"- {r['id']} | {r['title']} | {r['status']} | {r['time']}")
else:
    md.append("- None")
md.append("")
md.append("## All Weekly Items")
if filtered:
    for r in filtered:
        md.append(
            f"- {r['id']} | {r['title']} | {r['status']} | {r['handler']} | {r['priority']} | {r['time']}"
        )
else:
    md.append("- No weekly rows matched.")

(output_dir / "tapd-weekly-report.md").write_text("\n".join(md) + "\n", encoding="utf-8")
print(json.dumps(summary, ensure_ascii=False))
PY

log "report generated:"
log "  - $OUTPUT_DIR/tapd-weekly-report.md"
log "  - $OUTPUT_DIR/tapd-weekly-summary.json"
log "  - $SNAPSHOT_FILE"
