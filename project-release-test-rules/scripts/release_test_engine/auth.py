"""local 鉴权句柄；报告和基线只保存引用，不保存 secret 原值。"""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from typing import Any, Mapping


class AuthResolutionError(RuntimeError):
    """鉴权配置缺失、环境不允许或引用无法解析。"""


@dataclass(frozen=True)
class AuthHandle:
    headers: Mapping[str, str] = field(default_factory=dict)
    cookies: Mapping[str, str] = field(default_factory=dict)
    reference: str = ""
    expires_at: str = ""

    def masked(self) -> dict[str, Any]:
        return {
            "headers": {key: "***" if key.lower() in {"authorization", "proxy-authorization", "cookie", "x-api-key"} else value for key, value in self.headers.items()},
            "cookies": {key: "***" for key in self.cookies},
            "reference": self.reference,
            "expires_at": self.expires_at,
        }


def resolve_auth(config: Mapping[str, Any] | None, *, environment: str = "local", environ: Mapping[str, str] | None = None) -> AuthHandle:
    """从 local 配置和环境变量引用解析短生命周期鉴权句柄。"""

    if environment.lower() not in {"local", "local-dev", "development"}:
        raise AuthResolutionError("authentication is restricted to local environment")
    config = config or {}
    environ = environ or os.environ
    auth = config.get("auth", config)
    if not isinstance(auth, Mapping):
        return AuthHandle()
    headers = dict(auth.get("headers", {}) or {})
    cookies = dict(auth.get("cookies", {}) or {})
    token_ref = auth.get("token_env") or auth.get("credential_ref")
    if token_ref:
        token = environ.get(str(token_ref), "")
        if not token:
            raise AuthResolutionError(f"local auth reference is unavailable: {token_ref}")
        header_name = str(auth.get("header", "Authorization"))
        prefix = str(auth.get("prefix", "Bearer"))
        headers[header_name] = f"{prefix} {token}" if prefix else token
    return AuthHandle(headers=headers, cookies=cookies, reference=str(token_ref or auth.get("reference", "")), expires_at=str(auth.get("expires_at", "")))


def merge_auth_headers(headers: Mapping[str, str], handle: AuthHandle) -> dict[str, str]:
    merged = dict(headers)
    merged.update(handle.headers)
    if handle.cookies:
        merged["Cookie"] = "; ".join(f"{key}={value}" for key, value in handle.cookies.items())
    return merged
