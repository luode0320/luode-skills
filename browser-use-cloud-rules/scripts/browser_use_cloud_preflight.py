#!/usr/bin/env python3
"""在创建 Browser Use Cloud session 前执行只读安全预检。"""

from __future__ import annotations

import argparse
import json
import os
import sys
from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Any, Mapping
from urllib import error, parse, request


API_KEY_ENV = "BROWSER_USE_API_KEY"
OFFICIAL_BILLING_URL = "https://api.browser-use.com/api/v2/billing/account"
API_KEY_HEADER = "X-Browser-Use-API-Key"
MISSING_KEY_REMINDER = (
    "Browser Use Cloud 已命中，但本机未检测到 `BROWSER_USE_API_KEY`。"
    "请从 Browser Use Cloud 设置页取得 key，在本机用户环境变量中配置后重启 Codex；"
    "不要在聊天中粘贴 key。"
)
ALLOWED_STATUSES = {
    "ready_for_confirmation",
    "blocked_key_missing",
    "blocked_auth",
    "blocked_billing",
    "blocked_no_credit",
    "blocked_hard_cap_unavailable",
}
HARD_CAP_FIELD = "maxCostUsd"
ALLOWED_ACTIONS = {"run_session", "send_task"}
LOOPBACK_HOSTS = {"127.0.0.1", "localhost", "::1"}
ACTIVE_SESSION_STATUSES = {"created", "idle", "running"}
STOPPED_SESSION_STATUS = "stopped"
OPTIONAL_COST_FIELDS = ("llmCostUsd", "proxyCostUsd", "browserCostUsd")


@dataclass(frozen=True)
class BillingSummary:
    """只保留允许展示的账单字段。"""

    total_credits_balance_usd: Decimal
    monthly_credits_balance_usd: Decimal
    additional_credits_balance_usd: Decimal
    rate_limit: int
    is_free_tier: bool


def _result(status: str, **fields: Any) -> dict[str, Any]:
    """构造字段白名单结果，阻止原始响应进入输出。

    [参数] status: 预检状态；fields: 允许返回的脱敏字段
    [返回] 仅包含允许状态与脱敏字段的字典
    最近修改时间: 2026-07-26 13:56:24，补齐预检结果构造的注释契约
    """

    # 1. 先拒绝未知状态，避免调用方输出未冻结的结果类型
    if status not in ALLOWED_STATUSES:
        raise ValueError("预检状态不在允许集合中")
    return {"status": status, **fields}


def _decimal(value: Any) -> Decimal:
    """把账单金额转换为有限十进制数。

    [参数] value: Billing 响应中的金额字段
    [返回] 有限的十进制金额
    最近修改时间: 2026-07-26 13:56:24，补齐金额校验的注释契约
    """

    # 1. 拒绝无法转换或非有限金额，避免余额判断失真
    try:
        amount = Decimal(str(value))
    except (InvalidOperation, ValueError, TypeError) as exc:
        raise ValueError("账单金额字段无效") from exc
    if not amount.is_finite():
        raise ValueError("账单金额字段无效")
    return amount


def _billing_summary(payload: Any) -> BillingSummary:
    """校验官方账单响应并丢弃身份字段。

    [参数] payload: Billing endpoint 返回的已解析 JSON
    [返回] 仅保留余额、免费层与速率限制的脱敏摘要
    最近修改时间: 2026-07-26 13:56:24，补齐账单白名单解析的注释契约
    """

    # 1. 校验响应结构和全部必填字段，未知结构一律失败关闭
    if not isinstance(payload, Mapping):
        raise ValueError("账单响应不是对象")
    required = (
        "totalCreditsBalanceUsd",
        "monthlyCreditsBalanceUsd",
        "additionalCreditsBalanceUsd",
        "rateLimit",
        "isFreeTier",
    )
    if any(field not in payload for field in required):
        raise ValueError("账单响应缺少必填字段")

    # 2. 独立校验非金额字段，防止布尔值被当成整数接受
    rate_limit = payload["rateLimit"]
    if isinstance(rate_limit, bool) or not isinstance(rate_limit, int) or rate_limit < 0:
        raise ValueError("账单速率限制字段无效")
    if not isinstance(payload["isFreeTier"], bool):
        raise ValueError("免费层字段无效")

    # 3. 只构造允许展示的摘要，不携带姓名、项目或订阅标识
    return BillingSummary(
        total_credits_balance_usd=_decimal(payload["totalCreditsBalanceUsd"]),
        monthly_credits_balance_usd=_decimal(payload["monthlyCreditsBalanceUsd"]),
        additional_credits_balance_usd=_decimal(payload["additionalCreditsBalanceUsd"]),
        rate_limit=rate_limit,
        is_free_tier=payload["isFreeTier"],
    )


def _validate_billing_url(url: str) -> None:
    """只允许官方 Billing 或本机 mock URL。

    [参数] url: 待请求的 Billing URL
    [返回] 无；URL 不合规时抛出 ValueError
    最近修改时间: 2026-07-26 13:56:24，补齐 Billing URL 白名单的注释契约
    """

    # 1. 官方 endpoint 直接通过，其余地址必须满足 loopback mock 约束
    if url == OFFICIAL_BILLING_URL:
        return
    parsed = parse.urlsplit(url)

    # 2. 拒绝非本机、带认证信息、无路径或带 fragment 的 mock URL
    if (
        parsed.scheme not in {"http", "https"}
        or parsed.hostname not in LOOPBACK_HOSTS
        or parsed.username is not None
        or parsed.password is not None
        or not parsed.path
        or parsed.fragment
    ):
        raise ValueError("billing URL 只允许官方 endpoint 或 loopback local mock")


def _fetch_billing(api_key: str, billing_url: str, timeout_seconds: float) -> BillingSummary:
    """请求账单 endpoint，不把 key 或原始响应写入异常。

    [参数] api_key: 当前进程中的 Cloud key；billing_url: 账单地址；timeout_seconds: 请求超时秒数
    [返回] 已脱敏并校验的账单摘要
    最近修改时间: 2026-07-26 13:56:24，补齐账单请求的注释契约
    """

    # 1. 先验证目标地址，再创建仅携带必要 header 的只读请求
    _validate_billing_url(billing_url)
    billing_request = request.Request(
        billing_url,
        headers={API_KEY_HEADER: api_key, "Accept": "application/json"},
        method="GET",
    )

    # 2. 只接受成功 JSON 响应，并立即收敛为字段白名单摘要
    with request.urlopen(billing_request, timeout=timeout_seconds) as response:
        if response.status != 200:
            raise ValueError("账单 endpoint 返回非成功状态")
        payload = json.loads(response.read().decode("utf-8"))
    return _billing_summary(payload)


def _load_schema(schema_file: str | None) -> Any:
    """读取运行时工具 schema；缺失时由调用方失败关闭。

    [参数] schema_file: 当前 MCP `run_session` schema 文件路径
    [返回] 解析后的 schema；未提供路径时返回 None
    最近修改时间: 2026-07-26 13:56:24，补齐 schema 读取的注释契约
    """

    # 1. 不猜测缺失 schema；只有显式文件才按 UTF-8 读取
    if not schema_file:
        return None
    return json.loads(Path(schema_file).read_text(encoding="utf-8"))


def _find_hard_cap_field(schema: Any) -> str | None:
    """只在工具可写入的 input schema 中查找官方硬上限字段。

    [参数] schema: `run_session` 或 `send_task` 的当前工具 schema
    [返回] 命中的硬费用上限字段名；未命中时返回 None
    最近修改时间: 2026-07-26 14:03:00，阻止 output schema 或描述字段误触发硬上限放行
    """

    # 1. 兼容完整工具描述和直接 input schema 两种文件形态
    if not isinstance(schema, Mapping):
        return None
    input_schema = schema.get("inputSchema", schema)
    if not isinstance(input_schema, Mapping):
        return None

    # 2. 只读取可写 properties 下的官方字段，禁止扫描输出、示例或说明文字
    properties = input_schema.get("properties")
    if not isinstance(properties, Mapping):
        return None
    hard_cap_schema = properties.get(HARD_CAP_FIELD)
    if not isinstance(hard_cap_schema, Mapping):
        return None

    # 3. 只有明确可写数值字段才视为服务端硬费用上限
    if hard_cap_schema.get("type") != "number" or hard_cap_schema.get("readOnly") is True:
        return None
    return HARD_CAP_FIELD


def build_session_cleanup_instruction(payload: Any) -> dict[str, Any]:
    """根据 session 状态生成停止或费用回读指令。

    [参数] payload: `get_session` 返回的 session 对象
    [返回] 固定停止整个 session 的指令，或已停止状态的费用摘要
    最近修改时间: 2026-07-26 14:03:00，固化 session 级清理和费用回读闸门
    """

    # 1. 只接受具备已知状态的对象，未知响应不能进入清理完成路径
    if not isinstance(payload, Mapping) or not isinstance(payload.get("status"), str):
        raise ValueError("session 响应缺少有效状态")
    status = payload["status"]

    # 2. 活跃状态必须停止整个 session，禁止使用只停当前 task 的策略
    if status in ACTIVE_SESSION_STATUSES:
        return {
            "session_status": status,
            "stop_required": True,
            "stop_strategy": "session",
        }

    # 3. 只有 stopped 状态才允许读取并报告服务端实际费用
    if status == STOPPED_SESSION_STATUS:
        return {
            "session_status": status,
            "stop_required": False,
            "actual_costs": _stopped_session_costs(payload),
        }
    raise ValueError("session 状态不在允许集合中")


def _stopped_session_costs(payload: Mapping[str, Any]) -> dict[str, str]:
    """读取已停止 session 的非负有限实际费用。

    [参数] payload: 状态已确认为 stopped 的 session 对象
    [返回] 必含总费用、按服务端可用性附带拆分费用的字典
    最近修改时间: 2026-07-26 14:03:00，阻止缺失或异常费用被报告为清理成功
    """

    # 1. 总费用是最终报告必填字段，缺失或非法时失败关闭
    if "totalCostUsd" not in payload:
        raise ValueError("已停止 session 缺少总费用")
    total_cost = _decimal(payload["totalCostUsd"])
    if total_cost < 0:
        raise ValueError("session 总费用不能为负数")
    costs = {"totalCostUsd": str(total_cost)}

    # 2. 费用拆分按服务端实际返回读取，但每个值都必须非负且有限
    for field in OPTIONAL_COST_FIELDS:
        if field not in payload:
            continue
        amount = _decimal(payload[field])
        if amount < 0:
            raise ValueError("session 费用拆分不能为负数")
        costs[field] = str(amount)
    return costs


def run_preflight(
    *,
    billing_url: str,
    schema_file: str | None,
    timeout_seconds: float,
    action: str = "run_session",
    environ: Mapping[str, str] | None = None,
) -> dict[str, Any]:
    """执行完整预检，并只返回脱敏状态摘要。

    [参数] billing_url: 账单地址；schema_file: 当前动作的 MCP schema；timeout_seconds: 超时秒数；action: 收费动作；environ: 可注入环境变量映射
    [返回] 六态之一的脱敏预检结果
    最近修改时间: 2026-07-26 14:08:00，关闭认证和账单失败响应并保留逐动作预检
    """

    # 1. 只接受两种收费动作，并从冻结环境变量读取 key
    if action not in ALLOWED_ACTIONS:
        raise ValueError("预检动作不在允许集合中")
    env = os.environ if environ is None else environ
    api_key = env.get(API_KEY_ENV, "")
    if not api_key:
        return _result(
            "blocked_key_missing",
            key_present=False,
            action=action,
            reminder=MISSING_KEY_REMINDER,
        )

    # 2. 查询并校验账单；认证和其它 Billing 错误分别失败关闭
    try:
        summary = _fetch_billing(api_key, billing_url, timeout_seconds)
    except error.HTTPError as exc:
        # 2.1. 先保存状态码并关闭错误响应，避免负向预检残留网络资源
        response_code = exc.code
        exc.close()
        status = "blocked_auth" if response_code in {401, 403} else "blocked_billing"
        return _result(status, key_present=True, action=action)
    except (error.URLError, TimeoutError, json.JSONDecodeError, UnicodeDecodeError, ValueError):
        return _result("blocked_billing", key_present=True, action=action)

    # 3. 仅组装允许展示的账单字段，并先阻断无可用余额账户
    public_billing = {
        "key_present": True,
        "action": action,
        "is_free_tier": summary.is_free_tier,
        "total_credits_balance_usd": str(summary.total_credits_balance_usd),
        "monthly_credits_balance_usd": str(summary.monthly_credits_balance_usd),
        "additional_credits_balance_usd": str(summary.additional_credits_balance_usd),
        "rate_limit": summary.rate_limit,
    }
    if summary.total_credits_balance_usd <= 0:
        return _result("blocked_no_credit", **public_billing)

    # 4. 从当前收费动作的可写 input schema 查找硬上限，未命中即默认停止
    try:
        hard_cap_field = _find_hard_cap_field(_load_schema(schema_file))
    except (OSError, json.JSONDecodeError, UnicodeDecodeError, ValueError):
        hard_cap_field = None
    if not hard_cap_field:
        return _result(
            "blocked_hard_cap_unavailable",
            **public_billing,
            hard_cap_available=False,
        )

    # 5. 只有密钥、账单、余额和硬上限全部通过才允许进入用户确认
    return _result(
        "ready_for_confirmation",
        **public_billing,
        hard_cap_available=True,
        hard_cap_field=hard_cap_field,
    )


def _parse_args(argv: list[str] | None) -> argparse.Namespace:
    """解析命令行参数并限制超时范围。

    [参数] argv: 可选命令行参数列表
    [返回] 已校验的 argparse 命名空间
    最近修改时间: 2026-07-26 14:03:00，增加收费动作参数并保持短超时约束
    """

    # 1. 只暴露 Billing URL、schema 文件与短超时三个预检参数
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--billing-url", default=OFFICIAL_BILLING_URL)
    parser.add_argument("--schema-file")
    parser.add_argument("--action", choices=sorted(ALLOWED_ACTIONS), default="run_session")
    parser.add_argument("--timeout-seconds", type=float, default=5.0)
    args = parser.parse_args(argv)

    # 2. 限制超时范围，避免无限等待或无意义的极短请求
    if not 0.1 <= args.timeout_seconds <= 30:
        parser.error("--timeout-seconds 必须在 0.1 到 30 之间")
    return args


def main(argv: list[str] | None = None) -> int:
    """输出单行脱敏 JSON；阻断状态使用退出码 2。

    [参数] argv: 可选命令行参数列表
    [返回] ready 返回 0，任一阻断状态返回 2
    最近修改时间: 2026-07-26 14:03:00，把收费动作传入预检并保持阻断退出码
    """

    # 1. 解析参数并执行预检，顶层参数错误统一返回脱敏 Billing 阻断
    args = _parse_args(argv)
    try:
        result = run_preflight(
            billing_url=args.billing_url,
            schema_file=args.schema_file,
            timeout_seconds=args.timeout_seconds,
            action=args.action,
        )
    except ValueError:
        result = _result("blocked_billing", key_present=bool(os.environ.get(API_KEY_ENV)))

    # 2. stdout 只输出单行脱敏 JSON，并用退出码区分可确认与阻断
    sys.stdout.write(json.dumps(result, ensure_ascii=False, separators=(",", ":")) + "\n")
    return 0 if result["status"] == "ready_for_confirmation" else 2


if __name__ == "__main__":
    raise SystemExit(main())
