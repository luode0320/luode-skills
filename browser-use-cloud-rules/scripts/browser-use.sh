#!/bin/bash
# Browser Use Cloud REST API helper
# 面向「项目程序操作公网浏览器」场景：提交任务、轮询结果、停止任务、环境自检。
#
# 用法:
#   browser-use.sh [--no-wait] "任务描述"    提交并轮询（默认等待结果）
#   browser-use.sh --check                   环境自检（只读，不消费额度）
#   browser-use.sh --balance                 查询余额/免费层（只读）
#
# 凭据（单一权威）:
#   默认读取 ~/.browser-use/.env 中的 BROWSER_USE_API_KEY
#   环境变量 BROWSER_USE_API_KEY 仅作运行时覆盖
#   任何输出不回显 key 原值

set -euo pipefail

API_URL="https://api.browser-use.com/api/v2"
POLL_INTERVAL=5
MAX_WAIT=300
ENV_FILE="${HOME}/.browser-use/.env"

# 读取密钥：~/.browser-use/.env 为默认，环境变量覆盖
load_api_key() {
  if [[ -n "${BROWSER_USE_API_KEY:-}" ]]; then
    API_KEY="$BROWSER_USE_API_KEY"
    return 0
  fi
  if [[ -f "$ENV_FILE" ]]; then
    API_KEY=$(grep -E '^BROWSER_USE_API_KEY=' "$ENV_FILE" | head -n1 | cut -d= -f2- | tr -d '\r\n' || true)
    if [[ -n "$API_KEY" ]]; then
      return 0
    fi
  fi
  return 1
}

# 环境自检（只读，不消费额度）
check_env() {
  echo "== Browser Use 环境自检 =="
  if [[ -f "$ENV_FILE" ]]; then
    echo "[ok] 密钥文件存在: $ENV_FILE"
    if grep -qE '^BROWSER_USE_API_KEY=.+' "$ENV_FILE"; then
      echo "[ok] BROWSER_USE_API_KEY 已配置（值不回显）"
    else
      echo "[fail] $ENV_FILE 中缺少 BROWSER_USE_API_KEY 行"
    fi
  else
    echo "[fail] 密钥文件缺失: $ENV_FILE"
    echo "  修复: mkdir -p ~/.browser-use && echo 'BROWSER_USE_API_KEY=your-key' > ~/.browser-use/.env"
  fi
  command -v curl >/dev/null 2>&1 && echo "[ok] curl 可用" || echo "[fail] curl 未安装"
  command -v python3 >/dev/null 2>&1 && echo "[ok] python3 可用" || echo "[warn] python3 缺失（JSON 解析降级，可能无法显示结构结果）"
  if load_api_key; then
    echo "[ok] 密钥可读取（来源: ${BROWSER_USE_API_KEY:+环境变量}${BROWSER_USE_API_KEY:-$ENV_FILE}）"
  else
    echo "[fail] 无法读取 BROWSER_USE_API_KEY（.env 与环境变量均缺失）"
  fi
}

# 查询余额（只读；实测 2026-08-23：GET /credits 已下线返回 404，正确端点为 /billing/account）
check_balance() {
  if ! load_api_key; then
    echo "Error: BROWSER_USE_API_KEY 缺失（检查 $ENV_FILE 或环境变量）" >&2
    exit 1
  fi
  BODY=$(curl -s "$API_URL/billing/account" \
    -H "X-Browser-Use-API-Key: $API_KEY" \
    -H "Content-Type: application/json")
  echo "$BODY" | python3 -c "
import sys, json
try:
    d = json.load(sys.stdin)
except Exception:
    print('Error: 余额响应无法解析（网络异常或端点变更）', file=sys.stderr)
    sys.exit(1)
if 'totalCreditsBalanceUsd' not in d:
    print('Error: 余额查询失败: %s' % d.get('detail', d), file=sys.stderr)
    sys.exit(1)
print('== Browser Use 账户余额（脱敏摘要）==')
print(f\"免费层: {'是' if d.get('isFreeTier') else '否'}\")
print(f\"总余额: \${d.get('totalCreditsBalanceUsd')} USD\")
print(f\"月赠余额: \${d.get('monthlyCreditsBalanceUsd')} USD\")
print(f\"附加余额: \${d.get('additionalCreditsBalanceUsd')} USD\")
print(f\"速率限制: {d.get('rateLimit', '?')}\")
"
}

if [[ "${1:-}" == "--check" ]]; then
  check_env
  exit 0
fi

if [[ "${1:-}" == "--balance" ]]; then
  check_balance
  exit 0
fi

NO_WAIT=false
if [[ "${1:-}" == "--no-wait" ]]; then
  NO_WAIT=true
  shift
fi

TASK="${1:-}"
if [[ -z "$TASK" ]]; then
  echo "Usage: browser-use.sh [--no-wait] \"task description\"" >&2
  echo "       browser-use.sh --check" >&2
  echo "       browser-use.sh --balance" >&2
  exit 1
fi

if ! load_api_key; then
  echo "Error: BROWSER_USE_API_KEY 缺失（检查 $ENV_FILE 或环境变量）" >&2
  exit 1
fi

# 提交任务
RESPONSE=$(curl -s -X POST "$API_URL/tasks" \
  -H "X-Browser-Use-API-Key: $API_KEY" \
  -H "Content-Type: application/json" \
  -d "{\"task\": $(echo "$TASK" | python3 -c 'import json,sys; print(json.dumps(sys.stdin.read().strip()))')}")

TASK_ID=$(echo "$RESPONSE" | python3 -c "import sys,json; print(json.load(sys.stdin).get('id',''))" 2>/dev/null || echo "")

if [[ -z "$TASK_ID" ]]; then
  echo "Error submitting task: $RESPONSE" >&2
  exit 1
fi

echo "Task ID: $TASK_ID" >&2

if $NO_WAIT; then
  echo "$TASK_ID"
  exit 0
fi

# 轮询至完成
ELAPSED=0
while [[ $ELAPSED -lt $MAX_WAIT ]]; do
  RESULT=$(curl -s "$API_URL/tasks/$TASK_ID" \
    -H "X-Browser-Use-API-Key: $API_KEY")

  STATUS=$(echo "$RESULT" | python3 -c "import sys,json; print(json.load(sys.stdin).get('status',''))" 2>/dev/null || echo "")

  case "$STATUS" in
    finished)
      echo "$RESULT" | python3 -c "
import sys, json
data = json.load(sys.stdin)
print('Status: SUCCESS' if data.get('isSuccess') else 'Status: FAILED')
print(f\"Cost: \${data.get('cost', '?')}\")
print('---')
print(data.get('output', 'No output'))
"
      exit 0
      ;;
    failed)
      echo "Task failed" >&2
      echo "$RESULT"
      exit 1
      ;;
    created|pending|started)
      echo "Status: $STATUS (${ELAPSED}s)" >&2
      sleep $POLL_INTERVAL
      ELAPSED=$((ELAPSED + POLL_INTERVAL))
      ;;
    *)
      echo "Unknown status: $STATUS" >&2
      echo "$RESULT"
      exit 1
      ;;
  esac
done

echo "Timeout after ${MAX_WAIT}s" >&2
exit 1
