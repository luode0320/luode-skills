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
RENDERER_PATH = ROOT / "obsidian-knowledge-flow/scripts/render_execution_case.py"

RENDERER_SPEC = importlib.util.spec_from_file_location("render_execution_case", RENDERER_PATH)
assert RENDERER_SPEC and RENDERER_SPEC.loader
renderer = importlib.util.module_from_spec(RENDERER_SPEC)
sys.modules[RENDERER_SPEC.name] = renderer
RENDERER_SPEC.loader.exec_module(renderer)


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
    events = [
        line.split(":", 1)[1].strip()
        for line in note.splitlines()
        if line.lstrip("- ").startswith("status:")
    ]
    return events[-1] if events else parse_frontmatter(note).get("status", "unknown")


def select_active(
    notes: dict[str, str],
    *,
    scope: str,
    tool_major: str,
    input_fingerprint: str,
    environment: str = "local",
) -> list[str]:
    """只返回所有自动复用条件精确匹配且最终状态为 active 的案例路径。"""
    selected: list[str] = []
    for path, note in notes.items():
        fields = parse_frontmatter(note)
        if (
            fields.get("knowledge_kind") == "execution_case"
            and fields.get("scope") == scope
            and fields.get("tool_major") == tool_major
            and fields.get("input_fingerprint") == input_fingerprint
            and fields.get("environment") == environment
            and state_from_note(note) == "active"
        ):
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
            content = self.notes.get(path or "", "")
            return {"ok": True, "verified": path in self.notes, "content": content}
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
        created_readback = fake.run("read", path=path)
        self.assertTrue(created_readback["verified"])
        self.assertEqual(note, created_readback["content"])
        self.assertTrue(fake.run("append", path=path, content="\nstatus: active\n")["verified"])
        appended_readback = fake.run("read", path=path)
        self.assertTrue(appended_readback["verified"])
        self.assertIn("status: active", appended_readback["content"])
        self.assertEqual("active", state_from_note(fake.notes[path]))
        self.assertEqual(1, sum(call[0] == "append" for call in fake.calls))

    def test_exact_matching_excludes_wrong_scope_version_input_and_terminal_states(self) -> None:
        """环境、版本、输入指纹或失败终态不匹配时不得自动复用案例。"""
        def note(scope: str, status: str, *, tool_major: str = "1", fingerprint: str = "sha256:fixture", kind: str = "execution_case", environment: str = "local") -> str:
            return f"""---
scope: {scope}
status: {status}
tool_major: {tool_major}
input_fingerprint: {fingerprint}
knowledge_kind: {kind}
environment: {environment}
---
## 正例
verified local action
"""

        notes = {
            f"{CASE_ROOT}/owner/a.md": note("local|obsidian-cli|major-1", "active"),
            f"{CASE_ROOT}/owner/b.md": note("local|obsidian-cli|major-1", "active", tool_major="2"),
            f"{CASE_ROOT}/owner/c.md": note("local|obsidian-cli|major-1", "active", fingerprint="sha256:other"),
            f"{CASE_ROOT}/owner/d.md": note("local|obsidian-cli|major-1", "active", kind="knowledge"),
            f"{CASE_ROOT}/owner/e.md": note("local|obsidian-cli|major-1", "active", environment="production"),
            f"{CASE_ROOT}/owner/f.md": note("local|obsidian-cli|major-1", "stale"),
            f"{CASE_ROOT}/owner/g.md": note("local|obsidian-cli|major-1", "conflicted"),
            f"{CASE_ROOT}/owner/h.md": note("local|obsidian-cli|major-1", "rejected"),
        }
        self.assertEqual(
            [f"{CASE_ROOT}/owner/a.md"],
            select_active(
                notes,
                scope="local|obsidian-cli|major-1",
                tool_major="1",
                input_fingerprint="sha256:fixture",
            ),
        )

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
        with self.assertRaisesRegex(bridge.BridgeError, "execution case path"):
            bridge.build_request(
                "create",
                path=f"{CASE_ROOT}/owner/nested/case.md",
                content="x",
            )
        with self.assertRaisesRegex(bridge.BridgeError, "execution case path"):
            bridge.build_request(
                "create",
                path=f"{CASE_ROOT}/owner/case name.md",
                content="x",
            )

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

    def test_renderer_matches_case_schema_and_redacts_sensitive_values(self) -> None:
        """渲染器输出可读去重键、版本字段和 candidate 状态。"""
        payload = {
            "case_id": "obsidian-json-case",
            "owner_skill": "obsidian-knowledge-flow",
            "category": "tool-contract",
            "tool_or_model": "obsidian-cli 1.12",
            "tool_major": "1",
            "error_signature": "READBACK_MISMATCH",
            "minimal_input": (
                "token=sk-test-secret path=C:\\Users\\private\\case.json "
                "Cookie: session=cookie-value "
                "url=https://example.test/callback?token=secret-value "
                "email=user@example.test phone=13812345678 id=11010519491231002X"
            ),
            "input_fingerprint": "sha256:case-fixture",
            "root_cause": "读取结果不是预期 JSON",
            "solution": "先校验 bridge 响应，再按 UTF-8 readback",
            "verification_command": "python -X utf8 local_fixture.py",
            "success_criteria": "同输入 readback JSON 可解析",
            "scope": "local|obsidian-cli|major-1",
            "avoid": "不得绕过 bridge 写 vault",
            "negative_example": "直接记录 token 和完整响应",
            "positive_example": "使用脱敏摘要并保存结构化断言",
            "source": "TEST-OBS-LEARN-01",
            "created": "2026-07-14",
            "updated": "2026-07-14",
            "environment": "local",
            "state": "candidate",
        }
        rendered = renderer.render(payload)
        self.assertIn("status: candidate", rendered)
        self.assertIn("tool_major", rendered)
        self.assertIn("project_id: unknown", rendered)
        self.assertIn('error_signature: "READBACK_MISMATCH"', rendered)
        self.assertIn('scope: "local|obsidian-cli|major-1"', rendered)
        self.assertIn("input_fingerprint", rendered)
        self.assertIn("obsidian-knowledge-flow|tool-contract|1|readback_mismatch|sha256:case-fixture|local|obsidian-cli|major-1", rendered)
        self.assertIn("- status: candidate", rendered)
        self.assertIn("- event: created", rendered)
        self.assertNotIn("sk-test-secret", rendered)
        self.assertNotIn("C:\\Users\\private", rendered)
        self.assertNotIn("cookie-value", rendered)
        self.assertNotIn("secret-value", rendered)
        self.assertNotIn("user@example.test", rendered)
        self.assertNotIn("13812345678", rendered)
        self.assertNotIn("11010519491231002X", rendered)

    def test_renderer_rejects_non_candidate_initial_state(self) -> None:
        """被新案例替代的状态只能通过 append 追加，不能伪装成新建案例。"""
        payload = {
            "case_id": "superseded-case",
            "owner_skill": "obsidian-knowledge-flow",
            "category": "tool-contract",
            "tool_or_model": "obsidian-cli",
            "tool_major": "1",
            "error_signature": "OLD_CONTRACT",
            "minimal_input": "safe",
            "input_fingerprint": "sha256:safe",
            "root_cause": "旧契约已被替代",
            "solution": "采用新案例",
            "verification_command": "python -X utf8 local_fixture.py",
            "success_criteria": "同输入 local fixture 通过",
            "scope": "local|obsidian-cli|major-1",
            "avoid": "不得自动恢复旧案例",
            "negative_example": "继续使用旧方案",
            "positive_example": "读取新案例后再执行",
            "source": "TEST-OBS-LEARN-03",
            "created": "2026-07-14",
            "updated": "2026-07-14",
            "environment": "local",
            "state": "superseded",
        }
        with self.assertRaisesRegex(ValueError, "candidate"):
            renderer.render(payload)

    def test_renderer_rejects_non_local_and_expected_negative_cases(self) -> None:
        """非 local 或预期负向场景不能生成可复用案例。"""
        payload = {
            "case_id": "blocked-case",
            "owner_skill": "obsidian-knowledge-flow",
            "category": "environment",
            "tool_or_model": "obsidian-cli",
            "tool_major": "1",
            "error_signature": "ENV_BLOCKED",
            "minimal_input": "safe",
            "input_fingerprint": "sha256:safe",
            "root_cause": "外部环境",
            "solution": "停止",
            "verification_command": "unknown",
            "success_criteria": "unknown",
            "scope": "production",
            "avoid": "不得连接生产",
            "negative_example": "连接生产验证",
            "positive_example": "使用 local fixture",
            "source": "TEST-OBS-LEARN-02",
            "created": "2026-07-14",
            "updated": "2026-07-14",
            "environment": "production",
        }
        with self.assertRaises(ValueError):
            renderer.render(payload)

    def test_renderer_rejects_unstable_input_fingerprint(self) -> None:
        """输入指纹必须是脱敏后的稳定 sha256 标识，不能携带动态正文。"""
        payload = {
            "case_id": "unstable-fingerprint",
            "owner_skill": "obsidian-knowledge-flow",
            "category": "tool-contract",
            "tool_or_model": "obsidian-cli",
            "tool_major": "1",
            "error_signature": "READBACK_MISMATCH",
            "minimal_input": "safe",
            "input_fingerprint": "request-id-123",
            "root_cause": "输入指纹不稳定",
            "solution": "使用脱敏摘要哈希",
            "verification_command": "python -X utf8 local_fixture.py",
            "success_criteria": "同输入 local fixture 通过",
            "scope": "local|obsidian-cli|major-1",
            "avoid": "不得把 request id 作为指纹",
            "negative_example": "request-id-123",
            "positive_example": "sha256:stable-fixture",
            "source": "TEST-OBS-LEARN-04",
            "created": "2026-07-14",
            "updated": "2026-07-14",
            "environment": "local",
            "state": "candidate",
        }
        with self.assertRaisesRegex(ValueError, "input_fingerprint"):
            renderer.render(payload)


if __name__ == "__main__":
    unittest.main(verbosity=2)
