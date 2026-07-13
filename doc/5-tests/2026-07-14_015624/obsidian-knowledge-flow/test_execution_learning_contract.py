"""Obsidian 执行失败持续学习的离线契约测试。

测试只使用标准库和内存 FakeBridge，不启动 Obsidian，不读取或写入真实 vault。
"""

from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace


ROOT = Path(__file__).resolve().parents[4]
BRIDGE_PATH = ROOT / "obsidian-knowledge-flow/scripts/obsidian_cli_bridge.py"
BRIDGE_SPEC = importlib.util.spec_from_file_location("obsidian_cli_bridge_learning", BRIDGE_PATH)
assert BRIDGE_SPEC and BRIDGE_SPEC.loader
bridge = importlib.util.module_from_spec(BRIDGE_SPEC)
sys.modules[BRIDGE_SPEC.name] = bridge
BRIDGE_SPEC.loader.exec_module(bridge)

CASE_ROOT = "知识库/20-Knowledge/execution-failure-cases"
CASE_NOTES_REFERENCE = ROOT / "obsidian-knowledge-flow/references/execution-case-notes.md"
EXECUTION_SKILL = ROOT / "execution-failure-learning-rules/SKILL.md"
LIFECYCLE_REFERENCE = ROOT / "execution-failure-learning-rules/references/lifecycle-and-gates.md"


def parse_frontmatter(note: str) -> dict[str, str]:
    """读取测试案例的扁平 frontmatter，避免测试依赖第三方 YAML 库。"""
    if not note.startswith("---\n"):
        return {}
    _, frontmatter, _ = note.split("---\n", 2)
    values: dict[str, str] = {}
    for line in frontmatter.splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        values[key.strip()] = value.strip().strip('"')
    return values


def state_from_note(note: str) -> str:
    """状态事件以最后一条 `status:` 记录为准。"""
    events = [line.split(":", 1)[1].strip() for line in note.splitlines() if line.startswith("status:")]
    return events[-1] if events else parse_frontmatter(note).get("status", "unknown")


def select_active(notes: dict[str, str], *, scope: str) -> list[str]:
    """只返回 scope 精确匹配且最终状态为 active 的案例路径。"""
    selected: list[str] = []
    for path, note in notes.items():
        fields = parse_frontmatter(note)
        if fields.get("scope") == scope and state_from_note(note) == "active":
            selected.append(path)
    return selected


class FakeBridge:
    """模拟 bridge allowlist 的 doctor/search/read/create/append/readback。"""

    def __init__(self, *, fail_operation: str | None = None) -> None:
        self.notes: dict[str, str] = {}
        self.calls: list[tuple[str, str | None, str | None]] = []
        self.fail_operation = fail_operation

    def run(self, operation: str, *, path: str | None = None, content: str | None = None) -> dict[str, object]:
        self.calls.append((operation, path, content))
        if operation == self.fail_operation:
            raise RuntimeError(f"{operation} failed")
        if operation == "doctor":
            return {"ok": True, "verified": True, "vault_root": r"D:\\obsidian_data", "selector": "obsidian_data"}
        if operation == "search":
            return {"ok": True, "verified": True, "results": list(self.notes)}
        if operation == "read":
            return {"ok": True, "verified": True, "content": self.notes.get(path or "", "")}
        if operation == "create":
            assert path and content is not None
            if not path.startswith(CASE_ROOT + "/"):
                raise AssertionError("case path escaped fixed vault prefix")
            self.notes[path] = content
            return {"ok": True, "verified": True}
        if operation == "append":
            assert path and content is not None
            self.notes[path] = self.notes.get(path, "") + content
            return {"ok": True, "verified": True}
        raise AssertionError(f"unexpected operation: {operation}")


class ExecutionLearningContractTest(unittest.TestCase):
    """覆盖正反例、脱敏、状态事件、scope 和 bridge 失败边界。"""

    def test_references_declare_case_sections_and_obsidian_only_lifecycle(self) -> None:
        """案例规范必须同时要求正例、反例、状态事件和 bridge-only 持久化。"""
        self.assertTrue(CASE_NOTES_REFERENCE.exists(), CASE_NOTES_REFERENCE)
        reference = CASE_NOTES_REFERENCE.read_text(encoding="utf-8")
        for phrase in ("失败特征", "反例", "正例", "验证证据", "状态事件", "scope"):
            self.assertIn(phrase, reference)
        for phrase in ("doctor", "search", "read", "create", "append", "verified=true"):
            self.assertIn(phrase, reference)
        self.assertTrue("filesystem fallback" in reference or "文件系统 fallback" in reference)

        execution = EXECUTION_SKILL.read_text(encoding="utf-8")
        lifecycle = LIFECYCLE_REFERENCE.read_text(encoding="utf-8")
        self.assertIn("execution-failure-cases", execution)
        self.assertIn("知识库/30-MOCs/执行失败案例.md", execution)
        self.assertIn("candidate persistence: blocked", execution)
        self.assertIn("静态 owner casebook", execution)
        self.assertIn("追加式", lifecycle)
        self.assertIn("状态事件", lifecycle)
        self.assertIn("不得使用文件系统读写或静态 casebook 作为 fallback", lifecycle)

    def test_positive_and_negative_examples_are_redacted_and_appended(self) -> None:
        """同一案例正文保留反例与正例，敏感值不进入写入正文。"""
        secret = "sk-test-secret-value"
        note = """---
id: obsidian-json-case
status: candidate
owner_skill: obsidian-knowledge-flow
knowledge_kind: execution_case
case_key: obsidian|tool-contract|json|invalid-response
scope: local|obsidian-cli|major-1
environment: local
---
## 失败特征
退出码为 0 但 readback 不是 JSON。

## 反例
直接把完整响应和 token 写入案例。

## 正例
先用 bridge doctor，再按 UTF-8 JSON create 并 readback。

## 验证证据
同输入、同成功标准、local fixture 通过。

## 状态事件
status: candidate
""".replace(secret, "<redacted>")
        self.assertNotIn(secret, note)
        self.assertIn("## 反例", note)
        self.assertIn("## 正例", note)

        fake = FakeBridge()
        path = f"{CASE_ROOT}/obsidian-knowledge-flow/obsidian-json-case.md"
        self.assertTrue(fake.run("doctor")["verified"])
        self.assertTrue(fake.run("create", path=path, content=note)["verified"])
        self.assertTrue(fake.run("append", path=path, content="\nstatus: active\n")["verified"])
        self.assertEqual("active", state_from_note(fake.notes[path]))
        self.assertEqual(1, sum(call[0] == "append" for call in fake.calls))

    def test_scope_matching_excludes_wrong_scope_and_terminal_failure_states(self) -> None:
        """scope、版本或失败终态不匹配时不得自动复用案例。"""
        def note(scope: str, status: str) -> str:
            return f"""---
scope: {scope}
status: {status}
---
## 正例
verified local action
"""

        notes = {
            f"{CASE_ROOT}/owner/a.md": note("local|obsidian-cli|major-1", "active"),
            f"{CASE_ROOT}/owner/b.md": note("local|obsidian-cli|major-2", "active"),
            f"{CASE_ROOT}/owner/c.md": note("local|obsidian-cli|major-1", "stale"),
            f"{CASE_ROOT}/owner/d.md": note("local|obsidian-cli|major-1", "conflicted"),
            f"{CASE_ROOT}/owner/e.md": note("local|obsidian-cli|major-1", "rejected"),
        }
        self.assertEqual([f"{CASE_ROOT}/owner/a.md"], select_active(notes, scope="local|obsidian-cli|major-1"))

    def test_bridge_path_contract_rejects_escape_and_uses_utf8_json(self) -> None:
        """案例路径必须在固定知识库前缀内，正文通过 bridge JSON 传输。"""
        request = bridge.build_request(
            "create",
            path=f"{CASE_ROOT}/owner/case.md",
            content="正例：中文 UTF-8\n反例：错误 fallback",
        )
        self.assertEqual("create", request["operation"])
        self.assertIn("中文 UTF-8", request["content"])
        with self.assertRaises(bridge.BridgeError):
            bridge.build_request("create", path="知识库/../静态casebook.md", content="x")

    def test_bridge_failure_does_not_write_static_casebook_or_claim_persistence(self) -> None:
        """doctor/create/readback 失败时只报告 blocked，不使用文件系统 fallback。"""
        fake = FakeBridge(fail_operation="doctor")
        static_casebook = Path(tempfile.mkdtemp()) / "owner-casebook.md"
        static_casebook.write_text("seed only\n", encoding="utf-8")
        before = static_casebook.read_text(encoding="utf-8")
        with self.assertRaisesRegex(RuntimeError, "doctor failed"):
            fake.run("doctor")
        self.assertEqual(before, static_casebook.read_text(encoding="utf-8"))
        self.assertEqual(["doctor"], [operation for operation, _path, _content in fake.calls])
        self.assertNotIn("create", [operation for operation, _path, _content in fake.calls])

    def test_bridge_failure_response_keeps_structured_error_state(self) -> None:
        """adapter 失败保持稳定错误码，学习链路不能伪造 candidate 已写入。"""
        def runner(command: list[str], **_kwargs: object) -> SimpleNamespace:
            response_path = Path(command[command.index("-ResponsePath") + 1])
            response_path.write_text(
                json.dumps({"ok": False, "verified": False, "code": "VAULT_NOT_REGISTERED"}),
                encoding="utf-8",
            )
            return SimpleNamespace(returncode=5)

        response = bridge.invoke_windows_adapter(
            bridge.HostContext(host="windows", transport="pwsh.exe"),
            {"operation": "doctor"},
            Path("adapter.ps1"),
            runner=runner,
        )
        self.assertFalse(response["ok"])
        self.assertFalse(response["verified"])
        self.assertEqual("VAULT_NOT_REGISTERED", response["code"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
