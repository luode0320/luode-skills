"""Platform-neutral checkpoint and single-flight state primitives."""

from __future__ import annotations

import argparse
from datetime import datetime, timedelta, timezone
import hashlib
import json
from pathlib import Path
import tempfile
from typing import Any


TERMINAL_STATES = {"healthy", "manual_handoff", "blocked"}
ALLOWED_TRANSITIONS = {
    "suspected": {"healthy", "diagnosed"},
    "diagnosed": {"recovering", "manual_handoff", "blocked"},
    "recovering": {"reconnected", "reloaded", "restarted", "blocked"},
    "reconnected": {"verified", "blocked"},
    "reloaded": {"verified", "blocked"},
    "restarted": {"verified", "blocked"},
    "verified": {"resumed", "manual_handoff", "blocked"},
    "resumed": {"healthy"},
}
SENSITIVE_KEYS = {"api_key", "token", "password", "secret", "private_key", "prompt", "response"}
CHECKPOINT_ALLOWED_KEYS = {
    "recovery_id",
    "task_id_hash",
    "component_id",
    "scope",
    "scope_hash",
    "idempotency_class",
    "failure_class",
    "platform_id",
    "adapter_id",
}
CHECKPOINT_RECORD_KEYS = CHECKPOINT_ALLOWED_KEYS | {
    "state",
    "created_at",
    "updated_at",
    "expires_at",
    "request_digest",
    "lock",
}


def utc_now() -> datetime:
    """返回状态记录使用的带时区 UTC 时间。

    [参数] 无
    [返回] 带 UTC 时区的 datetime
    最近修改时间：2026-07-12 21:20:00；补齐统一智能体脚本注释元信息。
    """

    return datetime.now(timezone.utc)


def _read(path: Path) -> dict[str, Any]:
    """读取 JSON 检查点。

    [参数] path：检查点文件路径
    [返回] 检查点字典
    最近修改时间：2026-07-12 21:20:00；补齐统一智能体脚本注释元信息。
    """
    return json.loads(path.read_text(encoding="utf-8"))


def _write_atomic(path: Path, value: dict[str, Any]) -> None:
    """以临时文件替换方式原子写入检查点。

    [参数] path：目标文件路径；value：待写入检查点
    [返回] 无
    最近修改时间：2026-07-12 21:20:00；补齐统一智能体脚本注释元信息。
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=path.parent, delete=False) as handle:
        json.dump(value, handle, ensure_ascii=True, sort_keys=True)
        handle.write("\n")
        temp_path = Path(handle.name)
    temp_path.replace(path)


def _reject_sensitive_keys(value: Any) -> None:
    """递归拒绝凭据、提示词和响应等敏感字段。

    [参数] value：待检查的字典或列表
    [返回] 无；发现敏感字段时抛出 ValueError
    最近修改时间：2026-07-12 21:20:00；补齐统一智能体脚本注释元信息。
    """
    if isinstance(value, dict):
        for key, child in value.items():
            if key.lower() in SENSITIVE_KEYS:
                raise ValueError(f"sensitive checkpoint field rejected: {key}")
            _reject_sensitive_keys(child)
    elif isinstance(value, list):
        for child in value:
            _reject_sensitive_keys(child)


def _scope_hash(scope: str) -> str:
    """计算作用域摘要，避免检查点持久化原始路径或权限信息。

    [参数] scope：adapter 声明的组件作用域
    [返回] scope 的 SHA-256 十六进制摘要
    最近修改时间：2026-07-12 22:30:00；统一 checkpoint 的 scope 脱敏口径。
    """

    return hashlib.sha256(scope.encode("utf-8")).hexdigest()


def read_checkpoint(path: Path, now: datetime | None = None) -> dict[str, Any]:
    """读取并校验未损坏、未过期的检查点记录。

    [参数] path：检查点文件路径；now：可注入的当前 UTC 时间
    [返回] 已校验的检查点字典
    最近修改时间：2026-07-12 22:30:00；补齐损坏与 TTL 拒绝边界。
    """

    try:
        record = _read(path)
    except (OSError, ValueError, TypeError) as exc:
        raise ValueError("checkpoint_invalid") from exc
    if not isinstance(record, dict):
        raise ValueError("checkpoint_invalid")
    unknown = set(record).difference(CHECKPOINT_RECORD_KEYS)
    if unknown:
        raise ValueError(f"checkpoint_fields_not_allowed:{','.join(sorted(unknown))}")
    required = {"recovery_id", "task_id_hash", "component_id", "scope_hash", "idempotency_class", "state", "created_at", "updated_at", "expires_at"}
    missing = sorted(required.difference(record))
    if missing:
        raise ValueError(f"checkpoint_fields_missing:{','.join(missing)}")
    try:
        expires_at = datetime.fromisoformat(str(record["expires_at"]))
    except (TypeError, ValueError) as exc:
        raise ValueError("checkpoint_expiry_invalid") from exc
    current = now or utc_now()
    if expires_at <= current:
        raise ValueError("checkpoint_expired")
    return record


def create_checkpoint(path: Path, payload: dict[str, Any], ttl_seconds: int = 600) -> dict[str, Any]:
    """创建带稳定恢复标识的脱敏检查点。

    [参数] path：检查点文件路径；payload：检查点控制字段；ttl_seconds：检查点 TTL 秒数
    [返回] 已写入的检查点记录
    最近修改时间：2026-07-12 21:20:00；补齐统一智能体脚本注释元信息。
    """

    _reject_sensitive_keys(payload)
    if not isinstance(ttl_seconds, int) or not 1 <= ttl_seconds <= 600:
        raise ValueError("checkpoint_ttl_out_of_range")
    unknown = set(payload).difference(CHECKPOINT_ALLOWED_KEYS)
    if unknown:
        raise ValueError(f"checkpoint_fields_not_allowed:{','.join(sorted(unknown))}")
    required = {"recovery_id", "task_id_hash", "component_id", "idempotency_class"}
    missing = sorted(required.difference(payload))
    if missing:
        raise ValueError(f"checkpoint fields missing: {','.join(missing)}")
    if "scope_hash" not in payload and not isinstance(payload.get("scope"), str):
        raise ValueError("checkpoint scope missing")
    now = utc_now()
    record = dict(payload)
    scope = record.pop("scope", None)
    if "scope_hash" not in record:
        record["scope_hash"] = _scope_hash(scope)
    record.update({
        "state": "suspected",
        "created_at": now.isoformat(),
        "updated_at": now.isoformat(),
        "expires_at": (now + timedelta(seconds=ttl_seconds)).isoformat(),
    })
    digest_payload = json.dumps(record, ensure_ascii=True, sort_keys=True)
    record["request_digest"] = hashlib.sha256(digest_payload.encode("utf-8")).hexdigest()
    _write_atomic(path, record)
    return record


def transition(path: Path, target: str) -> dict[str, Any]:
    """仅按已声明状态机推进检查点。

    [参数] path：检查点文件路径；target：目标状态
    [返回] 更新后的检查点记录
    最近修改时间：2026-07-12 21:20:00；补齐统一智能体脚本注释元信息。
    """

    record = read_checkpoint(path)
    current = record.get("state")
    if current in TERMINAL_STATES:
        raise ValueError(f"terminal checkpoint cannot transition: {current}")
    if target not in ALLOWED_TRANSITIONS.get(current, set()):
        raise ValueError(f"invalid transition: {current}->{target}")
    record["state"] = target
    record["updated_at"] = utc_now().isoformat()
    _write_atomic(path, record)
    return record


def claim(path: Path, recovery_id: str, ttl_seconds: int = 600) -> dict[str, Any]:
    """在 TTL 内取得检查点的单飞锁。

    [参数] path：检查点文件路径；recovery_id：恢复操作标识；ttl_seconds：锁 TTL 秒数
    [返回] 带锁信息的检查点记录
    最近修改时间：2026-07-12 21:20:00；补齐统一智能体脚本注释元信息。
    """

    record = read_checkpoint(path)
    now = utc_now()
    lock = record.get("lock")
    if lock and datetime.fromisoformat(lock["expires_at"]) > now and lock["recovery_id"] != recovery_id:
        raise RuntimeError("recovery lock already held")
    record["lock"] = {"recovery_id": recovery_id, "expires_at": (now + timedelta(seconds=ttl_seconds)).isoformat()}
    _write_atomic(path, record)
    return record


def release(path: Path, recovery_id: str) -> dict[str, Any]:
    """仅由锁持有者释放检查点单飞锁。

    [参数] path：检查点文件路径；recovery_id：恢复操作标识
    [返回] 已释放锁的检查点记录
    最近修改时间：2026-07-12 21:20:00；补齐统一智能体脚本注释元信息。
    """

    record = read_checkpoint(path)
    lock = record.get("lock")
    if lock and lock.get("recovery_id") != recovery_id:
        raise RuntimeError("recovery lock owned by another operation")
    record.pop("lock", None)
    record["updated_at"] = utc_now().isoformat()
    _write_atomic(path, record)
    return record


def main() -> int:
    """执行检查点命令行入口。

    [参数] 无；参数由 argparse 从命令行读取
    [返回] 进程退出码
    最近修改时间：2026-07-12 21:20:00；补齐统一智能体脚本注释元信息。
    """
    parser = argparse.ArgumentParser(description="Manage agent runtime recovery checkpoints")
    parser.add_argument("operation", choices=("create", "transition", "claim", "release"))
    parser.add_argument("--state", required=True, type=Path)
    parser.add_argument("--target")
    parser.add_argument("--recovery-id")
    args = parser.parse_args()
    # 1. 根据操作类型调用唯一对应的检查点原语。
    if args.operation == "create":
        result = create_checkpoint(args.state, json.loads(args.target or "{}"))
    elif args.operation == "transition":
        result = transition(args.state, args.target or "")
    elif args.operation == "claim":
        result = claim(args.state, args.recovery_id or "")
    else:
        result = release(args.state, args.recovery_id or "")
    print(json.dumps(result, ensure_ascii=True, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
