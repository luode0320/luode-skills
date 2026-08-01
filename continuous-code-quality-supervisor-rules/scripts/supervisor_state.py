"""持续代码质量监督的脱敏状态与 finding 去重原语。"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from glob import glob
from pathlib import Path
import re
import sys
import tempfile
from typing import Any, Iterable


# 共享静态 Owner 路由由 6-review 入口拥有；监督 Skill 只作为消费者。
SHARED_ROUTER_DIR = Path(__file__).resolve().parents[2] / "code-style-consistency-rules" / "scripts"
if str(SHARED_ROUTER_DIR) not in sys.path:
    sys.path.insert(0, str(SHARED_ROUTER_DIR))

from static_owner_router import (
    BASE_OWNER_NAMES,
    OWNER_NAMES,
    owner_source_map_path,
    route_owners,
)


STATE_VERSION = 1
DEFAULT_STATE_DIR = "continuous-code-quality-supervisor"
SENSITIVE_KEYS = {
    "api_key",
    "password",
    "private_key",
    "prompt",
    "response",
    "secret",
    "token",
}
ALLOWED_SEVERITIES = {"P0", "P1", "P2", "P3"}
ALLOWED_FINDING_STATUSES = {"open", "limited", "resolved", "suppressed"}


def utc_now() -> str:
    """返回带 UTC 时区的状态时间。

    [参数] 无
    [返回] ISO-8601 格式的 UTC 时间
    最近修改时间：2026-07-25 08:00:00；统一监督状态时间格式。
    """

    # 1. 统一使用带时区的 UTC 时间，避免不同监督会话比较本地时间。
    return datetime.now(timezone.utc).isoformat()


def digest(value: str) -> str:
    """为路径、标识和 finding 计算稳定摘要。

    [参数] value：待摘要的短标识
    [返回] SHA-256 十六进制摘要
    最近修改时间：2026-07-25 08:00:00；统一状态路径和去重指纹算法。
    """

    # 1. 只对标识做摘要，不把完整 diff 或代码正文持久化。
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def checkout_hash(checkout: str | Path) -> str:
    """计算 checkout 标识，不把原始路径写入持久化状态。

    [参数] checkout：checkout 路径或标识
    [返回] checkout 的 SHA-256 摘要
    最近修改时间：2026-07-25 08:00:00；固定监督状态文件命名。
    """

    # 1. 解析路径后立即摘要，返回值不暴露原始路径。
    return digest(str(Path(checkout).expanduser().resolve()))


def finding_fingerprint(owner_skill: str, rule_source: str, affected_file: str, evidence: str) -> str:
    """按 finding 契约计算稳定去重指纹。

    [参数] owner_skill：规则 Owner；rule_source：规则相对来源；affected_file：文件相对路径；evidence：短证据
    [返回] 四个稳定字段共同生成的 SHA-256 摘要
    最近修改时间：2026-07-25 08:00:00；阻断调用方伪造或误传去重指纹。
    """

    # 1. 使用不可出现在路径中的分隔符连接字段，避免普通文本拼接碰撞。
    return digest("\0".join((owner_skill, rule_source, affected_file, evidence)))


def state_path(checkout: str | Path, state_root: Path | None = None) -> Path:
    """返回固定状态目录下的 checkout 状态文件。

    [参数] checkout：checkout 路径或标识；state_root：测试用状态根目录
    [返回] 脱敏 checkout 摘要对应的 JSON 状态路径
    最近修改时间：2026-07-25 08:00:00；接入 CODEX_HOME 状态根目录。
    """

    # 1. 生产环境遵循 CODEX_HOME，测试环境允许注入隔离状态根目录。
    codex_home = Path(os.environ.get("CODEX_HOME", str(Path.home() / ".codex")))
    root = state_root or codex_home / "state"
    return root / DEFAULT_STATE_DIR / f"{checkout_hash(checkout)}.json"


def _reject_sensitive(value: Any) -> None:
    """递归拒绝凭据、提示词、响应和其它敏感字段。

    [参数] value：待检查的字典或列表
    [返回] 无；发现敏感字段时抛出 ValueError
    最近修改时间：2026-07-25 08:00:00；阻断监督状态敏感数据落盘。
    """

    # 1. 遍历对象字段，阻断凭据和提示词等敏感键。
    if isinstance(value, dict):
        for key, child in value.items():
            if str(key).lower() in SENSITIVE_KEYS:
                raise ValueError(f"sensitive field rejected: {key}")
            _reject_sensitive(child)
    elif isinstance(value, list):
        for child in value:
            _reject_sensitive(child)


def _atomic_write(path: Path, payload: dict[str, Any]) -> None:
    """以 UTF-8 临时文件和原子替换写入状态。

    [参数] path：状态文件路径；payload：待写入状态
    [返回] 无；写入失败时保留原文件
    最近修改时间：2026-07-25 08:00:00；增加状态写入的原子性和编码约束。
    """

    # 1. 先拒绝敏感数据，再准备同目录临时文件。
    _reject_sensitive(payload)
    path.parent.mkdir(parents=True, exist_ok=True)
    # 2. 写入 UTF-8 JSON 后原子替换目标状态文件。
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=path.parent, delete=False) as handle:
        json.dump(payload, handle, ensure_ascii=True, sort_keys=True)
        handle.write("\n")
        temporary = Path(handle.name)
    temporary.replace(path)


def _read(path: Path) -> dict[str, Any]:
    """读取并校验监督状态。

    [参数] path：状态文件路径
    [返回] 已校验的状态字典
    最近修改时间：2026-07-25 08:00:00；拒绝损坏或敏感状态继续流转。
    """

    # 1. 以 UTF-8 读取并把损坏 JSON 统一转换为状态错误。
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError, TypeError) as exc:
        raise ValueError("supervisor_state_invalid") from exc
    # 2. 校验版本、敏感字段和 findings 容器形状。
    if not isinstance(payload, dict) or payload.get("version") != STATE_VERSION:
        raise ValueError("supervisor_state_invalid")
    _reject_sensitive(payload)
    if not isinstance(payload.get("findings", []), list):
        raise ValueError("supervisor_findings_invalid")
    return payload


def _require_relative_path(value: str, field_name: str) -> str:
    """校验并返回不暴露本机目录的相对路径。

    [参数] value：待校验路径；field_name：错误信息中的字段名
    [返回] 原样保留的相对路径
    最近修改时间：2026-07-25 08:00:00；阻断绝对路径进入监督状态。
    """

    # 1. 拒绝盘符、根路径和路径穿越，状态只保存仓库相对位置。
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name}_must_be_nonempty")
    if Path(value).is_absolute() or value.startswith(("/", "\\")) or re.match(r"^[A-Za-z]:", value):
        raise ValueError(f"{field_name}_must_be_relative")
    if ".." in Path(value).parts:
        raise ValueError(f"{field_name}_path_traversal_rejected")
    return value


def activation_status(goal_active: bool, intent: str, plan_mode: bool = False) -> tuple[str, str]:
    """按 Goal、用户意图和 Plan Mode 判定监督是否可以启动。

    [参数] goal_active：Goal 是否 active；intent：当前用户意图；plan_mode：是否处于 Plan Mode
    [返回] `(状态, 原因)` 二元组
    最近修改时间：2026-07-25 08:00:00；冻结监督 Skill 的双条件触发闸门。
    """

    # 1. Plan Mode 优先退出，避免把计划状态当成监督执行授权。
    if plan_mode:
        return "inactive", "plan_mode"
    if not goal_active:
        return "inactive", "goal_inactive"
    if "监控代码" not in intent:
        return "inactive", "monitor_intent_missing"
    return "active", "trigger_matched"


def _limited_owner_finding(owner_skill: str, affected_file: str) -> dict[str, str]:
    """为缺失或名称不一致的 Owner 生成受限 finding。

    [参数] owner_skill：无法读取的 Owner 名称；affected_file：受影响文件相对路径
    [返回] 符合通知契约的 `unclassified/limited` finding
    最近修改时间：2026-07-25 08:00:00；补充 Owner 来源缺失的安全降级。
    """

    # 1. 只记录 Owner 名称和相对位置，不猜测缺失规则的内容。
    affected_file = _require_relative_path(affected_file, "finding_file")
    evidence = f"Owner source unavailable: {owner_skill}"
    rule_source = "missing-owner"
    return {
        "owner_skill": "unclassified",
        "rule_source": rule_source,
        "file": affected_file,
        "evidence": evidence,
        "severity": "P1",
        "fingerprint": finding_fingerprint("unclassified", rule_source, affected_file, evidence),
        "status": "limited",
    }


def _source_map_path(repository_root: Path) -> Path:
    """返回由共享静态 Owner 路由拥有的来源映射路径。

    [参数] repository_root：当前 Skill 仓库根目录。
    [返回] 共享静态 Owner 来源映射的绝对路径。
    最近修改时间：2026-08-01 00:00:00；改为委托 6-review 的唯一来源映射入口。
    """

    # 1. 不在监督目录复制来源映射常量或路径拼接逻辑。
    return owner_source_map_path(repository_root)


def _owner_source_candidates(repository_root: Path, owner_skill: str) -> list[Path]:
    """读取 Owner 的静态质量来源列表。

    [参数] repository_root：仓库根目录；owner_skill：允许 Owner 名称
    [返回] 已排序去重的绝对路径列表
    最近修改时间：2026-07-25 18:40:00；让直接 reference 更新能被下一轮扫描感知。
    """

    default = [(repository_root / owner_skill / "SKILL.md").resolve()]
    source_map = _source_map_path(repository_root)
    if not source_map.exists():
        return default
    try:
        payload = json.loads(source_map.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise ValueError(f"source_map_unreadable:{error}") from error
    owners = payload.get("owners")
    if not isinstance(owners, dict) or owner_skill not in owners:
        raise ValueError("source_map_owner_missing")
    entry = owners[owner_skill]
    if not isinstance(entry, dict):
        raise ValueError("source_map_owner_invalid")
    candidates: list[Path] = []
    for key in ("source_paths", "source_globs"):
        values = entry.get(key, [])
        if not isinstance(values, list) or not all(isinstance(item, str) and item.strip() for item in values):
            raise ValueError(f"source_map_{key}_invalid")
        for value in values:
            normalized = value.replace("\\", "/")
            parts = [part for part in normalized.split("/") if part]
            if normalized.startswith("/") or re.match(r"^[A-Za-z]:", normalized) or ".." in parts:
                raise ValueError("source_map_path_out_of_scope")
            if not normalized.startswith(f"{owner_skill}/"):
                raise ValueError("source_map_path_cross_owner")
            if key == "source_paths":
                candidate = (repository_root / normalized).resolve()
                if not candidate.is_file():
                    raise ValueError("source_map_declared_source_missing")
                candidates.append(candidate)
            else:
                matches = [Path(item).resolve() for item in glob(str(repository_root / normalized), recursive=True)]
                file_matches = [item for item in matches if item.is_file()]
                if not file_matches:
                    raise ValueError("source_map_glob_empty")
                candidates.extend(file_matches)
    unique = sorted(set(candidates), key=lambda item: item.as_posix())
    skill_path = (repository_root / owner_skill / "SKILL.md").resolve()
    if skill_path not in unique:
        unique.insert(0, skill_path)
    return unique


def _declared_owner_name(content: str) -> str | None:
    """读取 Skill frontmatter 中的 Owner 名称。

    [参数] content：当前磁盘上的完整 SKILL.md 内容
    [返回] 合法 frontmatter 中的 name；格式缺失时为 None
    最近修改时间：2026-07-25 08:00:00；识别目录名与 Skill 声明名不一致。
    """

    # 1. 只解析首个 YAML frontmatter 的 name 行，不缓存或复制规则正文。
    frontmatter = re.match(r"\A---[ \t]*\r?\n(?P<header>.*?)\r?\n---(?:\r?\n|\Z)", content, re.DOTALL)
    if not frontmatter:
        return None
    name = re.search(r"(?m)^name:[ \t]*([A-Za-z0-9][A-Za-z0-9-]*)[ \t]*$", frontmatter.group("header"))
    return name.group(1) if name else None


def read_owner_sources(repository_root: str | Path, owners: Iterable[str], affected_file: str) -> dict[str, list[dict[str, str]]]:
    """每次扫描重新读取 Owner 文件并返回来源摘要。

    [参数] repository_root：Skill 仓库根目录；owners：待读取 Owner；affected_file：受影响文件相对路径
    [返回] 可用来源摘要和 `limited` finding 列表
    最近修改时间：2026-07-25 18:40:00；确保 SKILL.md 与直接 reference 更新后不使用旧副本。
    """

    # 1. 按当前磁盘内容逐个读取 Owner，未知名称不进入路径拼接。
    root = Path(repository_root).resolve()
    sources: list[dict[str, str]] = []
    limited_findings: list[dict[str, str]] = []
    for owner_skill in owners:
        if owner_skill not in OWNER_NAMES:
            limited_findings.append(_limited_owner_finding(str(owner_skill), affected_file))
            continue
        try:
            source_paths = _owner_source_candidates(root, owner_skill)
        except ValueError:
            limited_findings.append(_limited_owner_finding(owner_skill, affected_file))
            continue
        try:
            skill_content = (root / owner_skill / "SKILL.md").read_text(encoding="utf-8")
        except (OSError, UnicodeError):
            limited_findings.append(_limited_owner_finding(owner_skill, affected_file))
            continue
        if _declared_owner_name(skill_content) != owner_skill:
            limited_findings.append(_limited_owner_finding(owner_skill, affected_file))
            continue
        try:
            contents = [(source, source.read_text(encoding="utf-8")) for source in source_paths]
        except (OSError, UnicodeError):
            limited_findings.append(_limited_owner_finding(owner_skill, affected_file))
            continue
        # 2. 只返回相对来源和内容摘要，调用方不缓存或持久化规则正文。
        for source, content in contents:
            sources.append(
                {
                    "owner_skill": owner_skill,
                    "rule_source": source.relative_to(root).as_posix(),
                    "content_digest": digest(content),
                }
            )
    return {"sources": sources, "limited_findings": limited_findings}


def start(
    checkout: str | Path,
    goal_active: bool,
    intent: str,
    state_root: Path | None = None,
    plan_mode: bool = False,
) -> dict[str, Any]:
    """在双条件满足时创建或重置一个脱敏监督状态。

    [参数] checkout：checkout 路径；goal_active：Goal 状态；intent：当前意图；state_root：状态根目录；plan_mode：Plan Mode 标记
    [返回] 启动状态、原因、状态路径和可选状态对象
    最近修改时间：2026-07-25 08:00:00；新增 Goal 双条件启动状态。
    """

    # 1. 先执行双条件闸门，未满足时不创建状态文件。
    status, reason = activation_status(goal_active, intent, plan_mode)
    path = state_path(checkout, state_root)
    if status != "active":
        return {"status": status, "reason": reason, "state_path": str(path)}
    # 2. 仅保存脱敏摘要、扫描列表和 finding 元数据。
    now = utc_now()
    payload = {
        "version": STATE_VERSION,
        "checkout_hash": checkout_hash(checkout),
        "status": "active",
        "goal_active": True,
        "started_at": now,
        "updated_at": now,
        "owners": [],
        "scans": [],
        "findings": [],
    }
    _atomic_write(path, payload)
    return {"status": "active", "reason": reason, "state_path": str(path), "state": payload}


def register_owner(
    checkout: str | Path,
    owner_skill: str,
    rule_source: str,
    trigger: str,
    state_root: Path | None = None,
) -> dict[str, Any]:
    """注册一个已读取的 Owner 元数据，不复制规则正文。

    [参数] checkout：checkout 路径；owner_skill：Owner 名称；rule_source：规则来源；trigger：触发摘要；state_root：状态根目录
    [返回] 更新后的监督状态
    最近修改时间：2026-07-25 08:00:00；增加 Owner 白名单和来源登记。
    """

    # 1. 先校验 Owner 白名单和最小来源信息。
    if owner_skill not in OWNER_NAMES:
        raise ValueError(f"owner_not_allowed: {owner_skill}")
    _require_relative_path(rule_source, "rule_source")
    if not trigger or "\n" in trigger or "\r" in trigger or len(trigger) > 256:
        raise ValueError("owner_source_and_trigger_required")
    # 2. 以同名 Owner 替换旧登记，避免规则更新后残留旧摘要。
    path = state_path(checkout, state_root)
    payload = _read(path)
    owner = {"owner_skill": owner_skill, "rule_source": rule_source, "trigger": trigger}
    payload["owners"] = [item for item in payload.get("owners", []) if item.get("owner_skill") != owner_skill]
    payload["owners"].append(owner)
    payload["updated_at"] = utc_now()
    _atomic_write(path, payload)
    return payload


def _normalize_finding(raw: dict[str, Any]) -> dict[str, Any]:
    """校验 finding 白名单，避免把代码正文写入状态。

    [参数] raw：待写入的 finding 字典
    [返回] 通过白名单和安全检查的 finding 副本
    最近修改时间：2026-07-25 08:00:00；冻结 finding 字段、相对路径和证据长度。
    """

    # 1. 校验字段白名单、Owner 和枚举值。
    required = {"owner_skill", "rule_source", "file", "evidence", "severity", "fingerprint", "status"}
    if set(raw) != required:
        missing = sorted(required.difference(raw))
        extra = sorted(set(raw).difference(required))
        raise ValueError(f"finding_fields_invalid:missing={missing},extra={extra}")
    if raw["owner_skill"] != "unclassified" and raw["owner_skill"] not in OWNER_NAMES:
        raise ValueError(f"owner_not_allowed: {raw['owner_skill']}")
    if raw["severity"] not in ALLOWED_SEVERITIES or raw["status"] not in ALLOWED_FINDING_STATUSES:
        raise ValueError("finding_enum_invalid")
    if not all(isinstance(raw[key], str) and raw[key].strip() for key in required):
        raise ValueError("finding_fields_must_be_nonempty_strings")
    # 2. 拒绝绝对路径、多行正文和超长证据，保护状态文件边界。
    _require_relative_path(raw["rule_source"], "finding_rule_source")
    _require_relative_path(raw["file"], "finding_file")
    evidence = raw["evidence"]
    if "\n" in evidence or "\r" in evidence or len(evidence) > 512:
        raise ValueError("finding_evidence_must_be_short_single_line")
    expected_fingerprint = finding_fingerprint(raw["owner_skill"], raw["rule_source"], raw["file"], evidence)
    if raw["fingerprint"] != expected_fingerprint:
        raise ValueError("finding_fingerprint_invalid")
    if (raw["status"] == "limited") != (raw["owner_skill"] == "unclassified"):
        raise ValueError("limited_finding_owner_must_be_unclassified")
    return dict(raw)


def record_scan(
    checkout: str | Path,
    diff_id: str,
    changed_files: Iterable[str],
    findings: Iterable[dict[str, Any]] = (),
    state_root: Path | None = None,
) -> dict[str, Any]:
    """记录一次扫描摘要并按 fingerprint 合并 finding。

    [参数] checkout：checkout 路径；diff_id：扫描标识；changed_files：变更文件；findings：本轮 finding；state_root：状态根目录
    [返回] 状态路径、新增数、更新数和更新后的状态
    最近修改时间：2026-07-25 08:00:00；实现扫描摘要和 fingerprint 去重。
    """

    # 1. 规范化扫描输入并确认监督仍处于 active。
    changed_files = list(changed_files)
    if not diff_id or not changed_files or not all(isinstance(item, str) and item for item in changed_files):
        raise ValueError("scan_input_invalid")
    changed_files = [_require_relative_path(item, "changed_file") for item in changed_files]
    path = state_path(checkout, state_root)
    payload = _read(path)
    if payload.get("status") != "active":
        raise ValueError("supervisor_not_active")
    # 2. 校验 finding 并合并相同 fingerprint 的观察次数。
    normalized = [_normalize_finding(item) for item in findings]
    now = utc_now()
    existing = {item["fingerprint"]: item for item in payload.get("findings", [])}
    added = 0
    updated = 0
    for finding in normalized:
        fingerprint = finding["fingerprint"]
        if fingerprint in existing:
            existing[fingerprint]["last_seen"] = now
            existing[fingerprint]["scan_count"] = int(existing[fingerprint].get("scan_count", 1)) + 1
            existing[fingerprint]["status"] = finding["status"]
            updated += 1
        else:
            finding["first_seen"] = now
            finding["last_seen"] = now
            finding["scan_count"] = 1
            existing[fingerprint] = finding
            added += 1
    # 3. 只写入 diff 摘要、文件位置和计数，不保存代码正文。
    payload["findings"] = list(existing.values())
    payload["scans"].append(
        {
            "diff_hash": digest(diff_id),
            "changed_files": sorted(set(changed_files)),
            "finding_count": len(normalized),
            "recorded_at": now,
        }
    )
    payload["updated_at"] = now
    _atomic_write(path, payload)
    return {"state_path": str(path), "added": added, "updated": updated, "state": payload}


def status(checkout: str | Path, state_root: Path | None = None) -> dict[str, Any]:
    """读取当前监督状态。

    [参数] checkout：checkout 路径；state_root：状态根目录
    [返回] 状态路径和已校验状态
    最近修改时间：2026-07-25 08:00:00；提供只读状态查询。
    """

    # 1. 通过统一读取入口校验状态后返回。
    path = state_path(checkout, state_root)
    return {"state_path": str(path), "state": _read(path)}


def stop(checkout: str | Path, state_root: Path | None = None) -> dict[str, Any]:
    """停止监督但保留脱敏扫描摘要和 finding。

    [参数] checkout：checkout 路径；state_root：状态根目录
    [返回] 停止后的监督状态
    最近修改时间：2026-07-25 08:00:00；补充显式停止和 Goal inactive 标记。
    """

    # 1. 读取当前状态并标记为 stopped，历史摘要保持可观察。
    path = state_path(checkout, state_root)
    payload = _read(path)
    payload["status"] = "stopped"
    payload["goal_active"] = False
    payload["updated_at"] = utc_now()
    _atomic_write(path, payload)
    return payload


def _parser() -> argparse.ArgumentParser:
    """创建状态 CLI 参数解析器。

    [参数] 无
    [返回] 配置完成的 argparse 解析器
    最近修改时间：2026-07-25 08:00:00；补充状态生命周期 CLI 入口。
    """

    # 1. 声明统一的生命周期操作和测试用状态根目录参数。
    parser = argparse.ArgumentParser(description="Manage continuous code quality supervisor state")
    parser.add_argument("operation", choices=("start", "register-owner", "record-scan", "status", "stop"))
    parser.add_argument("--checkout", required=True)
    parser.add_argument("--state-root", type=Path)
    parser.add_argument("--goal-active", action="store_true")
    parser.add_argument("--plan-mode", action="store_true")
    parser.add_argument("--intent", default="")
    parser.add_argument("--owner-skill")
    parser.add_argument("--rule-source")
    parser.add_argument("--trigger")
    parser.add_argument("--diff-id")
    parser.add_argument("--changed-file", action="append", default=[])
    parser.add_argument("--finding-json", type=Path)
    return parser


def main() -> int:
    """执行状态 CLI 并输出 JSON 结果。

    [参数] 无；参数由 argparse 从命令行读取
    [返回] 进程退出码，0 表示成功，1 表示状态或输入被阻断
    最近修改时间：2026-07-25 08:00:00；统一 CLI 错误输出和退出码。
    """

    # 1. 解析参数并调用唯一对应的状态原语。
    args = _parser().parse_args()
    try:
        if args.operation == "start":
            result = start(args.checkout, args.goal_active, args.intent, args.state_root, args.plan_mode)
        elif args.operation == "register-owner":
            result = register_owner(args.checkout, args.owner_skill or "", args.rule_source or "", args.trigger or "", args.state_root)
        elif args.operation == "record-scan":
            findings = []
            if args.finding_json:
                findings = json.loads(args.finding_json.read_text(encoding="utf-8"))
            result = record_scan(args.checkout, args.diff_id or "", args.changed_file, findings, args.state_root)
        elif args.operation == "status":
            result = status(args.checkout, args.state_root)
        else:
            result = stop(args.checkout, args.state_root)
    # 2. 将状态安全错误转换为机器可读的 blocked 结果。
    except (OSError, ValueError, TypeError) as exc:
        print(json.dumps({"status": "blocked", "error": str(exc)}, ensure_ascii=True, sort_keys=True))
        return 1
    print(json.dumps(result, ensure_ascii=True, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
