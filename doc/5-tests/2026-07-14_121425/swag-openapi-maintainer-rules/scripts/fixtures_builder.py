"""构造离线 swag 树 fixture，供第三方目录校验测试复用。"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml


def _response_schema(property_description: str = "币种代码") -> dict[str, Any]:
    """[参数] property_description 为响应字段中文说明。
    [返回] 返回最小响应 schema。
    最近修改时间: 2026-07-14 12:14:25，构造离线响应字段 fixture。
    """
    return {
        "type": "object",
        "title": "币种响应",
        "properties": {
            "currency": {
                "type": "string",
                "description": property_description,
            }
        },
    }


def _document(path: str, method: str, summary: str, property_description: str) -> dict[str, Any]:
    """[参数] path、method、summary、property_description 为接口 fixture 字段。
    [返回] 返回完整 OpenAPI 3 文档对象。
    最近修改时间: 2026-07-14 12:14:25，构造根与上游独立文档。
    """
    operation = {
        "operationId": "v3_currencies_get" if path == "/v3/currencies" else "health_check_get",
        "summary": summary,
        "responses": {
            "200": {
                "description": "成功响应",
                "content": {"application/json": {"schema": _response_schema(property_description)}},
            }
        },
    }
    return {
        "openapi": "3.0.3",
        "info": {"title": summary, "version": "1.0.0"},
        "paths": {path: {method.lower(): operation}},
    }


def _write_yaml(path: Path, value: dict[str, Any]) -> None:
    """[参数] path 为目标文件，value 为 YAML 对象。
    [返回] 无。
    最近修改时间: 2026-07-14 12:14:25，统一使用 UTF-8 写入 fixture。
    """
    path.write_text(yaml.safe_dump(value, allow_unicode=True, sort_keys=False), encoding="utf-8")


def _root_manifest() -> dict[str, Any]:
    """[参数] 无。
    [返回] 返回自有接口 manifest。
    最近修改时间: 2026-07-14 12:14:25，构造根目录兼容 fixture。
    """
    return {
        "generated_by": "swag-openapi-maintainer-rules",
        "source_type": "self",
        "updated_at": "2026-07-14 12:14:25",
        "openapi_file": "openapi.yaml",
        "interfaces": [
            {
                "method": "GET",
                "path": "/health/check",
                "operationId": "health_check_get",
                "summary": "健康检查",
                "summary_source": "explicit",
                "file": "health_check_健康检查.yaml",
                "generated": True,
            }
        ],
    }


def _upstream_manifest() -> dict[str, Any]:
    """[参数] 无。
    [返回] 返回 upstream manifest。
    最近修改时间: 2026-07-14 12:14:25，构造上游目录契约 fixture。
    """
    return {
        "generated_by": "swag-openapi-maintainer-rules",
        "source_type": "upstream",
        "upstream": "moonpay",
        "base_url": "https://api.moonpay.com",
        "coverage": "partial",
        "updated_at": "2026-07-14 12:14:25",
        "openapi_file": "openapi.yaml",
        "interfaces": [
            {
                "method": "GET",
                "path": "/v3/currencies",
                "operationId": "v3_currencies_get",
                "summary": "币种列表",
                "summary_source": "explicit",
                "file": "v3_currencies_币种列表.yaml",
                "generated": True,
                "source_client_file": "internal/client/moonpay/currencies.go",
                "source_symbols": ["MoonpayClient.ListCurrencies"],
                "discovery_confidence": "high",
            }
        ],
    }


def build_fixture(root: Path, case: str) -> Path:
    """[参数] root 为 fixture 根目录，case 为用例名。
    [返回] 返回生成的 swag 目录路径。
    最近修改时间: 2026-07-14 12:14:25，新增离线上游校验 fixture。
    """
    # 1. 先构造根目录自有接口，作为所有用例的隔离基线。
    swag = root / "swag"
    moonpay = swag / "moonpay"
    swag.mkdir(parents=True, exist_ok=True)
    _write_yaml(swag / "openapi.yaml", _document("/health/check", "GET", "健康检查", "健康状态"))
    _write_yaml(swag / "health_check_健康检查.yaml", _document("/health/check", "GET", "健康检查", "健康状态"))
    _write_yaml(swag / ".swag-manifest.yaml", _root_manifest())

    if case == "compatibility_single_directory":
        return swag

    # 2. 构造一套与根目录隔离的 moonpay 上游资产。
    moonpay.mkdir(parents=True, exist_ok=True)
    _write_yaml(moonpay / "openapi.yaml", _document("/v3/currencies", "GET", "币种列表", "币种代码"))
    _write_yaml(moonpay / "v3_currencies_币种列表.yaml", _document("/v3/currencies", "GET", "币种列表", "币种代码"))
    _write_yaml(moonpay / ".swag-manifest.yaml", _upstream_manifest())

    if case == "missing_chinese_description":
        invalid = _document("/v3/currencies", "GET", "币种列表", "currency code")
        _write_yaml(moonpay / "v3_currencies_币种列表.yaml", invalid)
    elif case == "manifest_mismatch":
        manifest = _upstream_manifest()
        manifest["interfaces"][0]["file"] = "v3_currencies_错误映射.yaml"
        _write_yaml(moonpay / ".swag-manifest.yaml", manifest)
    elif case == "path_escape":
        manifest = _upstream_manifest()
        manifest["interfaces"][0]["file"] = "../escape.yaml"
        _write_yaml(moonpay / ".swag-manifest.yaml", manifest)
    elif case == "missing_source_type":
        manifest = _upstream_manifest()
        manifest.pop("source_type")
        _write_yaml(moonpay / ".swag-manifest.yaml", manifest)
    elif case == "stranger_directory":
        stranger = swag / "docs"
        stranger.mkdir(parents=True, exist_ok=True)
        _write_yaml(stranger / "note.yaml", {"note": "陌生目录不应被当成上游服务"})
    elif case != "valid":
        raise ValueError(f"unknown fixture case: {case}")

    return swag
