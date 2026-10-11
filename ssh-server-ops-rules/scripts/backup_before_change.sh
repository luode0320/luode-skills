#!/usr/bin/env bash
# ---------------------------------------------------------------------------
# backup_before_change.sh —— 改动前在远端创建可验证的还原点
#
# 用法:
#   bash scripts/backup_before_change.sh \
#     --host <host> --port <port> --user <user> \
#     --key "C:/Users/luode/.ssh/id_ed25519_<alias>" \
#     [--alias <alias>] [--tag "<说明>"] \
#     --path <远端路径> [--path <远端路径> ...]
#
# 行为:
#   1) 生成 UTC 时间戳与还原点 ID
#   2) 远端创建 ~/.agent-backups/<TS>/ 及子目录（权限 700）
#   3) 上传路径清单，逐项备份（文件 cp -a / 目录 tar czf / 不存在记 MISSING）
#   4) 生成 manifest.md（含 sha256 与回滚动作）
#   5) 生成并 chmod +x 一键回滚脚本 rollback.sh
#   6) 输出还原点 ID、备份目录、manifest 路径与回滚命令
#
# 退出码: 0 = 还原点已建立并验证; 非 0 = 备份未完成，禁止继续改动
# ---------------------------------------------------------------------------
set -euo pipefail

HOST=""; PORT="22"; USER=""; KEY=""; ALIAS=""; TAG="change"
PATHS=()

while [[ $# -gt 0 ]]; do
  case "$1" in
    --host)  HOST="$2"; shift 2;;
    --port)  PORT="$2"; shift 2;;
    --user)  USER="$2"; shift 2;;
    --key)   KEY="$2";  shift 2;;
    --alias) ALIAS="$2"; shift 2;;
    --tag)   TAG="$2";  shift 2;;
    --path)  PATHS+=("$2"); shift 2;;
    -h|--help) sed -n '2,20p' "$0"; exit 0;;
    *) echo "错误: 未知参数 $1" >&2; exit 2;;
  esac
done

[[ -n "$HOST" && -n "$USER" && -n "$KEY" ]] || { echo "错误: 缺少 --host / --user / --key" >&2; exit 2; }
[[ ${#PATHS[@]} -gt 0 ]] || { echo "错误: 至少需要一个 --path" >&2; exit 2; }

# Windows 反斜杠路径统一成正斜杠，避免 ssh/scp 误解析
KEY="${KEY//\\//}"

# 路径含单引号会破坏远端脚本内联，直接拒绝
for p in "${PATHS[@]}"; do
  if [[ "$p" == *"'"* ]]; then
    echo "错误: 路径含单引号，暂不支持: $p" >&2
    exit 2
  fi
done

TS="$(date -u +%Y%m%dT%H%M%SZ)"
RP_ID="RP-${ALIAS:-$HOST}-${TS}"

echo "→ 目标: ${ALIAS:-$HOST} (${HOST}:${PORT})"
echo "→ 还原点: ${RP_ID}"

SSH_OPTS=(-i "$KEY" -p "$PORT" -o StrictHostKeyChecking=accept-new -o ConnectTimeout=15)

# 1) 远端创建还原点目录（显式建目录，不依赖远端 shell 的 brace expansion）
# shellcheck disable=SC2029
ssh "${SSH_OPTS[@]}" "${USER}@${HOST}" \
  "set -e; B=\"\$HOME/.agent-backups/${TS}\"; for d in files dirs db docker misc; do mkdir -p \"\$B/\$d\"; done; chmod 700 \"\$HOME/.agent-backups\" \"\$B\""

# 2) 上传路径清单
TMPLIST="$(mktemp)"
trap 'rm -f "$TMPLIST"' EXIT
printf '%s\n' "${PATHS[@]}" > "$TMPLIST"
scp -i "$KEY" -P "$PORT" -o StrictHostKeyChecking=accept-new \
  "$TMPLIST" "${USER}@${HOST}:.agent-backups/${TS}/paths.list" >/dev/null

# 3) 远端执行备份（脚本经 stdin 传入，参数走环境变量，避免多层转义）
# shellcheck disable=SC2029
ssh "${SSH_OPTS[@]}" "${USER}@${HOST}" \
  "TS='${TS}' RP_ID='${RP_ID}' TAG='${TAG}' bash -s" <<'REMOTE_SCRIPT'
set -euo pipefail

B="$HOME/.agent-backups/$TS"
MAN="$B/manifest.md"
RB="$B/rollback.sh"
PLIST="$B/paths.list"

{
  echo "# 还原点 $RP_ID"
  echo ""
  echo "- 目标主机: $(hostname)"
  echo "- 创建时间(UTC): $TS"
  echo "- 标签: $TAG"
  echo ""
  echo "## 备份对象"
  echo ""
  echo "| # | 原路径 | 类型 | 备份文件 | 大小 | sha256(前12) | 回滚动作 |"
  echo "| --- | --- | --- | --- | --- | --- | --- |"
} > "$MAN"

{
  echo "#!/usr/bin/env bash"
  echo "# 一键回滚 $RP_ID  —— 恢复顺序为备份记录的逆序"
  echo "set -euo pipefail"
} > "$RB"

# 先收集条目，再逆序写入 rollback.sh（后备份的先还原，避免父子目录冲突）
TMP_RB="$B/.rollback.body"
: > "$TMP_RB"

i=0
while IFS= read -r p; do
  [ -z "$p" ] && continue
  i=$((i+1))

  if [ ! -e "$p" ]; then
    echo "| $i | \`$p\` | MISSING | - | - | - | 删除该路径（改动前不存在） |" >> "$MAN"
    echo "rm -rf -- '$p'   # 改动前不存在，回滚即删除" >> "$TMP_RB"
    continue
  fi

  if [ -d "$p" ]; then
    parent="$(dirname "$p")"; name="$(basename "$p")"
    out="$B/dirs/$name.tar.gz"
    tar czf "$out" -C "$parent" "$name"
    sz="$(du -h "$out" | cut -f1)"
    hash="$(sha256sum "$out" | cut -d' ' -f1)"
    echo "| $i | \`$p\` | 目录 | dirs/$name.tar.gz | $sz | ${hash:0:12} | rm -rf + tar xzf |" >> "$MAN"
    echo "rm -rf -- '$p' && tar xzf '$out' -C '$parent'" >> "$TMP_RB"
  else
    name="$(basename "$p")"
    out="$B/files/$name"
    cp -a "$p" "$out"
    sz="$(du -h "$out" | cut -f1)"
    hash="$(sha256sum "$out" | cut -d' ' -f1)"
    echo "| $i | \`$p\` | 文件 | files/$name | $sz | ${hash:0:12} | cp -a 覆盖 |" >> "$MAN"
    echo "cp -a '$out' '$p'" >> "$TMP_RB"
  fi
done < "$PLIST"

# 逆序追加到 rollback.sh（后备份的先还原）
if command -v tac >/dev/null 2>&1; then
  tac "$TMP_RB" >> "$RB"
elif tail -r /dev/null >/dev/null 2>&1; then
  tail -r "$TMP_RB" >> "$RB"
else
  awk '{a[NR]=$0} END{for(i=NR;i>=1;i--) print a[i]}' "$TMP_RB" >> "$RB"
fi
rm -f "$TMP_RB"
chmod +x "$RB"

{
  echo ""
  echo "## 一键回滚"
  echo ""
  echo '```bash'
  echo "ssh -i <keyPath> -p <port> <user>@$(hostname) \"bash $RB\""
  echo '```'
} >> "$MAN"

echo "=== 还原点已建立 ==="
echo "RP_ID=$RP_ID"
echo "BACKUP_DIR=$B"
echo "MANIFEST=$MAN"
echo "ROLLBACK_CMD=ssh -i <keyPath> -p <port> <user>@$(hostname) \"bash $RB\""
echo "OBJECTS=$i"
echo ""
cat "$MAN"
REMOTE_SCRIPT

echo ""
echo "✔ 还原点 ${RP_ID} 已建立并验证。改动失败或效果不符时执行:"
echo "  ssh -i \"${KEY}\" -p ${PORT} ${USER}@${HOST} \"bash ~/.agent-backups/${TS}/rollback.sh\""
