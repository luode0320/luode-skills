"""场景 JSON Pointer 捕获和确定性断言。"""

from __future__ import annotations

import hashlib
import json
import re
import time
from typing import Any, Callable, Mapping


class ScenarioAssertionError(AssertionError):
    """场景断言没有满足确定性预期。"""


def json_pointer(value: Any, pointer: str) -> Any:
    """读取 RFC 6901 JSON Pointer。

    [参数] value: 待读取的结构化值；pointer: RFC 6901 路径。
    [返回] 路径对应的值；路径无效时抛出场景断言异常。
    最近修改时间：2026-07-25 20:45:00，补齐场景断言公共函数的输入输出和失败边界。
    """

    # 1. 空路径直接返回根对象，非空路径必须使用斜杠开头。
    if pointer == "":
        return value
    if not pointer.startswith("/"):
        raise ScenarioAssertionError(f"invalid JSON Pointer: {pointer}")
    # 2. 逐段解码对象键或数组下标，任何不存在的路径都确定性失败。
    current = value
    for raw_part in pointer[1:].split("/"):
        # 2.1 当前段先解码转义，再按对象键或数组下标读取。
        part = raw_part.replace("~1", "/").replace("~0", "~")
        if isinstance(current, Mapping) and part in current:
            # 2.2 映射与数组路径互斥，未命中任何分支即视为路径不存在。
            current = current[part]
        elif isinstance(current, list) and part.isdigit() and int(part) < len(current):
            current = current[int(part)]
        else:
            raise ScenarioAssertionError(f"JSON Pointer not found: {pointer}")
    return current


def _type_matches(value: Any, expected: str) -> bool:
    """判断结构化值是否满足白名单类型名称。

    [参数] value: 实际值；expected: object/array/string 等类型名称。
    [返回] 类型名称合法且实际值匹配时返回 True。
    最近修改时间：2026-07-25 20:45:00，补齐布尔值与数值类型隔离的说明。
    """

    types = {"object": Mapping, "array": list, "string": str, "integer": int, "number": (int, float), "boolean": bool, "null": type(None)}
    target = types.get(expected)
    return bool(target) and isinstance(value, target) and not (expected in {"integer", "number"} and isinstance(value, bool))


def assert_value(value: Any, assertion: Mapping[str, Any]) -> None:
    """执行单条白名单断言。

    [参数] value: 实际值；assertion: 声明式断言配置。
    [返回] 无；断言不满足或操作不受支持时抛出场景断言异常。
    最近修改时间：2026-07-25 20:45:00，明确断言白名单和失败契约。
    """

    # 1. 只解释冻结的断言操作，不执行表达式或任意代码。
    operation = str(assertion.get("op", "equal"))
    expected = assertion.get("expected")
    if operation == "equal" and value != expected:
        raise ScenarioAssertionError(f"expected {expected!r}, got {value!r}")
    if operation == "type" and not _type_matches(value, str(expected)):
        raise ScenarioAssertionError(f"expected type {expected}, got {type(value).__name__}")
    if operation == "enum" and value not in assertion.get("values", []):
        raise ScenarioAssertionError(f"value {value!r} is outside enum")
    if operation == "contains" and expected not in value:
        raise ScenarioAssertionError(f"value does not contain {expected!r}")
    if operation == "regex" and re.search(str(expected), str(value)) is None:
        raise ScenarioAssertionError(f"value does not match {expected!r}")
    if operation == "count" and len(value) != int(expected):
        raise ScenarioAssertionError(f"expected count {expected}, got {len(value)}")
    if operation == "sha256":
        raw = value if isinstance(value, bytes) else str(value).encode("utf-8")
        if hashlib.sha256(raw).hexdigest() != str(expected):
            raise ScenarioAssertionError("sha256 digest mismatch")
    if operation not in {"equal", "type", "enum", "contains", "regex", "count", "sha256"}:
        raise ScenarioAssertionError(f"unsupported assertion: {operation}")


def assert_document(document: Any, assertions: tuple[Mapping[str, Any], ...] | list[Mapping[str, Any]]) -> None:
    """对文档执行结构化断言集合。

    [参数] document: 场景步骤或整体结果；assertions: 白名单断言集合。
    [返回] 无，任一断言失败时抛出 ScenarioAssertionError。
    最近修改时间：2026-07-25 15:00:00，增加跨路径相等、顺序和唯一性 oracle。
    """

    # 1. 路径间相等直接比较同一结构化文档，避免执行字符串表达式。
    for assertion in assertions:
        value = json_pointer(document, str(assertion.get("path", "")))
        operation = str(assertion.get("op", "equal"))
        if operation == "equal_path":
            other = json_pointer(document, str(assertion.get("other_path", "")))
            if value != other:
                raise ScenarioAssertionError(f"cross-path values differ: {value!r} != {other!r}")
            continue

        # 2. 顺序和唯一性只读取数组内的相对 JSON Pointer 字段。
        if operation in {"ordered", "unique"}:
            # 2.1 顺序与唯一性只接受数组，并先投影比较字段。
            if not isinstance(value, list):
                raise ScenarioAssertionError(f"{operation} assertion requires an array")
            field = str(assertion.get("field", ""))
            values = [json_pointer(item, field) for item in value]
            if operation == "unique" and len(set(str(item) for item in values)) != len(values):
                raise ScenarioAssertionError("array contains duplicate values")
            if operation == "ordered":
                # 2.2 顺序断言只接受升序或降序并与稳定排序结果比较。
                direction = str(assertion.get("direction", "asc"))
                if direction not in {"asc", "desc"}:
                    raise ScenarioAssertionError("ordered direction must be asc or desc")
                expected = sorted(values, reverse=direction == "desc")
                if values != expected:
                    raise ScenarioAssertionError(f"array order mismatch: {values!r}")
            continue
        assert_value(value, assertion)


def wait_until(reader: Callable[[], Any], assertion: Mapping[str, Any], *, timeout_ms: int, interval_ms: int = 50) -> Any:
    """在确定超时内轮询最终一致性断言。

    [参数] reader: 每次轮询读取最新值的函数；assertion: 目标断言；timeout_ms: 超时；interval_ms: 间隔。
    [返回] 首次满足断言的实际值。
    最近修改时间：2026-07-25 20:45:00，补齐最终一致性等待的确定性边界。
    """

    # 1. 使用单调时钟和固定间隔重试，超时后保留最后一次断言错误。
    deadline = time.monotonic() + timeout_ms / 1000
    last_error: Exception | None = None
    while time.monotonic() <= deadline:
        # 1.1 每次读取最新值，并在同一次迭代内执行相同断言。
        value = reader()
        try:
            # 1.2 断言一旦满足立即返回，失败则保留错误并等待下一次轮询。
            assert_value(value, assertion)
            return value
        except ScenarioAssertionError as exc:
            last_error = exc
            time.sleep(interval_ms / 1000)
    raise ScenarioAssertionError(f"eventual assertion timed out: {last_error}")


def stable_json(value: Any) -> str:
    """生成用于事件关联和摘要的稳定 JSON。

    [参数] value: 可 JSON 序列化的结构化值。
    [返回] UTF-8 友好、键排序且无多余空白的 JSON 字符串。
    最近修改时间：2026-07-25 20:45:00，明确摘要输入输出稳定性。
    """

    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
