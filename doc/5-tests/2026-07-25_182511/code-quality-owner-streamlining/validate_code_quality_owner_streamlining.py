#!/usr/bin/env python3
"""验证代码质量 Owner 首批精简后的路由、来源和去重契约。"""

from __future__ import annotations

import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[4]
SCRIPTS = ROOT / "code-style-consistency-rules" / "scripts"
sys.path.insert(0, str(SCRIPTS))

from static_owner_router import (  # noqa: E402
    BASE_OWNER_NAMES,
    OWNER_NAMES,
    owner_source_map_path,
    route_owners,
)

HERE = Path(__file__).resolve().parent


def load_json(name: str) -> dict:
    """读取 UTF-8 JSON 配置。"""

    return json.loads((HERE / name).read_text(encoding="utf-8"))


def assert_true(condition: bool, message: str) -> None:
    """失败时输出稳定错误。"""

    if not condition:
        raise AssertionError(message)


def validate_inventory() -> None:
    """验证 Owner 身份、基础顺序和共享来源映射完整性。

    [参数] 无。
    [返回] 无；断言失败时抛出异常。
    最近修改时间：2026-08-01 00:00:00；改由共享路由读取唯一来源映射。
    """

    # 1. 校验共享路由声明的 Owner 集合、基础顺序和来源映射完全一致。
    inventory = load_json("inventory.json")
    expected = set(inventory["owners"])
    assert_true(set(OWNER_NAMES) == expected, "OWNER_NAMES 与 inventory 不一致")
    assert_true(list(BASE_OWNER_NAMES) == inventory["base_owners"], "BASE_OWNER_NAMES 顺序不一致")
    source_map = json.loads(owner_source_map_path(ROOT).read_text(encoding="utf-8"))
    map_owners = set(source_map.get("owners", {}))
    assert_true(map_owners == expected, "static-owner-source-map.json Owner 覆盖不完整")
    for owner, entry in source_map["owners"].items():
        for key in ("source_paths", "source_globs"):
            assert_true(isinstance(entry.get(key, []), list), f"{owner}.{key} 不是列表")
        for rel in entry.get("source_paths", []):
            path = Path(rel)
            assert_true(not path.is_absolute() and ".." not in path.parts, f"{owner} source path 越界: {rel}")
            assert_true(rel.replace("\\", "/").startswith(owner + "/"), f"{owner} source path 跨 Owner: {rel}")
            assert_true((ROOT / rel).is_file(), f"{owner} source path 缺失: {rel}")
            (ROOT / rel).read_text(encoding="utf-8")
    for excluded in inventory["excluded_must_never_route"]:
        assert_true(excluded not in OWNER_NAMES, f"排除 Skill 进入 OWNER_NAMES: {excluded}")


def validate_routes() -> None:
    """验证条件路由正负例和顺序。"""

    for fixture in load_json("route-fixtures.json")["fixtures"]:
        owners = route_owners(fixture["files"], fixture.get("signals", []))
        for owner in fixture.get("include", []):
            assert_true(owner in owners, f"{fixture['name']} 未命中 {owner}: {owners}")
        for owner in fixture.get("exclude", []):
            assert_true(owner not in owners, f"{fixture['name']} 误命中 {owner}: {owners}")
        order = fixture.get("order", [])
        if order:
            indexes = [owners.index(owner) for owner in order]
            assert_true(indexes == sorted(indexes), f"{fixture['name']} 顺序错误: {owners}")


def validate_text_contract() -> None:
    """验证去重后的活跃消费者没有保留旧规则正文。"""

    contract = load_json("owner-contract.json")
    for item in contract["text_assertions"]:
        text = (ROOT / item["file"]).read_text(encoding="utf-8")
        for needle in item.get("must_contain", []):
            assert_true(needle in text, f"{item['file']} 缺少 {needle}")
        for needle in item.get("must_not_contain", []):
            assert_true(needle not in text, f"{item['file']} 仍包含旧口径 {needle}")
    for owner in contract["required_agent_yaml"]:
        assert_true((ROOT / owner / "agents" / "openai.yaml").is_file(), f"{owner} 缺少 agents/openai.yaml")


def main() -> None:
    """执行全部验证。"""

    validate_inventory()
    validate_routes()
    validate_text_contract()
    print("code-quality-owner-streamlining: PASS")


if __name__ == "__main__":
    main()
