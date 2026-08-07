"""验证 Obsidian 桥接的命令白名单、参数校验与迭代治理文档口径。"""

from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
BRIDGE_PATH = ROOT / "obsidian-knowledge-flow" / "scripts" / "obsidian_cli_bridge.py"
ADAPTER_PATH = ROOT / "obsidian-knowledge-flow" / "scripts" / "obsidian_cli_windows.ps1"
CLI_OPERATIONS = ROOT / "obsidian-knowledge-flow" / "references" / "cli-operations.md"
VALIDATION_CHECKLIST = ROOT / "obsidian-knowledge-flow" / "references" / "validation-checklist.md"
CONFLICT_STALENESS = ROOT / "obsidian-knowledge-flow" / "references" / "conflict-staleness.md"
NOTE_SCHEMA = ROOT / "obsidian-knowledge-flow" / "references" / "note-schema.md"
EXECUTION_CASE_NOTES = ROOT / "obsidian-knowledge-flow" / "references" / "execution-case-notes.md"
CAPTURE_FLOW = ROOT / "obsidian-knowledge-flow" / "references" / "capture-retrieve-distill.md"
OBSIDIAN_SKILL = ROOT / "obsidian-knowledge-flow" / "SKILL.md"

READONLY_COMMANDS = ("property-read", "properties", "backlinks", "files", "orphans")
WRITE_COMMANDS = ("property-set", "move", "delete")
SAMPLE_PATH = "知识库/20-Knowledge/topic/note.md"
EXECUTION_CASE_PATH = "知识库/20-Knowledge/execution-failure-cases/owner/case-slug.md"


def load_bridge() -> Any:
    """按文件路径加载桥接模块，避免依赖带连字符的目录可导入。

    [参数] 无。
    [返回] Any：已加载的桥接模块对象。
    最近修改时间: 2026-08-05 16:40:00 新增桥接参数校验契约测试。
    """
    name = "obsidian_cli_bridge_under_test"
    spec = importlib.util.spec_from_file_location(name, BRIDGE_PATH)
    module = importlib.util.module_from_spec(spec)
    # 先注册再执行：桥接内的 dataclass 装饰器会按模块名回查命名空间。
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def read_text(path: Path) -> str:
    """按 UTF-8 读取目标文件全文，编码异常直接暴露为测试失败。

    [参数] path：目标文件路径。
    [返回] str：文件的 UTF-8 文本。
    最近修改时间: 2026-08-05 16:40:00 新增桥接参数校验契约测试。
    """
    return path.read_text(encoding="utf-8")


BRIDGE = load_bridge()


class ReadonlyCommandContractTest(unittest.TestCase):
    """只读组：校验五个只读命令进入白名单且参数校验到位。"""

    def test_readonly_commands_are_allowed(self) -> None:
        """五个只读命令必须全部进入白名单。

        [参数] 无。
        [返回] None：断言失败时抛出 AssertionError。
        最近修改时间: 2026-08-05 16:40:00 新增桥接参数校验契约测试。
        """
        for command in READONLY_COMMANDS:
            self.assertIn(command, BRIDGE.ALLOWED_COMMANDS, f"{command} 未进入白名单")

    def test_property_read_requires_name(self) -> None:
        """读属性缺少属性名时必须以参数错误拒绝。

        [参数] 无。
        [返回] None：断言失败时抛出 AssertionError。
        最近修改时间: 2026-08-05 16:40:00 新增桥接参数校验契约测试。
        """
        with self.assertRaises(BRIDGE.BridgeError) as ctx:
            BRIDGE.build_request("property-read", path=SAMPLE_PATH)
        self.assertEqual(ctx.exception.code, "INVALID_ARGUMENT")

    def test_readonly_path_commands_reject_escape(self) -> None:
        """路径型只读命令必须拒绝越出固定知识前缀的路径。

        [参数] 无。
        [返回] None：断言失败时抛出 AssertionError。
        最近修改时间: 2026-08-05 16:40:00 新增桥接参数校验契约测试。
        """
        for command in ("properties", "backlinks"):
            with self.assertRaises(BRIDGE.BridgeError) as ctx:
                BRIDGE.build_request(command, path="其它目录/note.md")
            self.assertEqual(ctx.exception.code, "PATH_OUTSIDE_KNOWLEDGE", f"{command} 未拦截越界路径")

    def test_files_folder_is_optional_but_validated(self) -> None:
        """枚举文件的目录可省略，但给出时必须落在固定知识前缀内。

        [参数] 无。
        [返回] None：断言失败时抛出 AssertionError。
        最近修改时间: 2026-08-05 16:40:00 新增桥接参数校验契约测试。
        """
        self.assertNotIn("folder", BRIDGE.build_request("files"))
        self.assertEqual(BRIDGE.build_request("files", folder="知识库/20-Knowledge")["folder"], "知识库/20-Knowledge")
        with self.assertRaises(BRIDGE.BridgeError) as ctx:
            BRIDGE.build_request("files", folder="D:/obsidian_data")
        self.assertEqual(ctx.exception.code, "PATH_OUTSIDE_KNOWLEDGE")

    def test_orphans_takes_no_path(self) -> None:
        """枚举孤儿不接受任何路径参数。

        [参数] 无。
        [返回] None：断言失败时抛出 AssertionError。
        最近修改时间: 2026-08-05 16:40:00 新增桥接参数校验契约测试。
        """
        request = BRIDGE.build_request("orphans")
        self.assertNotIn("path", request)
        self.assertEqual(request["operation"], "orphans")

    def test_stdout_is_pinned_to_utf8(self) -> None:
        """桥接必须把输出流固定为 UTF-8，否则中文路径无法回传。

        [参数] 无。
        [返回] None：断言失败时抛出 AssertionError。
        最近修改时间: 2026-08-05 16:40:00 新增桥接参数校验契约测试。
        """
        source = read_text(BRIDGE_PATH)
        self.assertIn('reconfigure(encoding="utf-8")', source)


class WriteCommandContractTest(unittest.TestCase):
    """写操作组：校验三个写命令的参数校验、回收站语义与执行案例保护。"""

    def test_write_commands_are_allowed(self) -> None:
        """三个写命令必须全部进入白名单。

        [参数] 无。
        [返回] None：断言失败时抛出 AssertionError。
        最近修改时间: 2026-08-05 16:40:00 新增桥接参数校验契约测试。
        """
        for command in WRITE_COMMANDS:
            self.assertIn(command, BRIDGE.ALLOWED_COMMANDS, f"{command} 未进入白名单")

    def test_property_set_requires_name_and_value(self) -> None:
        """写属性缺少属性名或属性值时必须以参数错误拒绝。

        [参数] 无。
        [返回] None：断言失败时抛出 AssertionError。
        最近修改时间: 2026-08-05 16:40:00 新增桥接参数校验契约测试。
        """
        with self.assertRaises(BRIDGE.BridgeError):
            BRIDGE.build_request("property-set", path=SAMPLE_PATH, value="superseded")
        with self.assertRaises(BRIDGE.BridgeError):
            BRIDGE.build_request("property-set", path=SAMPLE_PATH, name="status")

    def test_property_type_is_restricted(self) -> None:
        """属性类型只允许官方命令行支持的六种，缺省按文本处理。

        [参数] 无。
        [返回] None：断言失败时抛出 AssertionError。
        最近修改时间: 2026-08-05 16:40:00 新增桥接参数校验契约测试。
        """
        request = BRIDGE.build_request("property-set", path=SAMPLE_PATH, name="status", value="superseded")
        self.assertEqual(request["property_type"], "text")
        self.assertEqual(BRIDGE.PROPERTY_TYPES, frozenset({"text", "list", "number", "checkbox", "date", "datetime"}))
        with self.assertRaises(BRIDGE.BridgeError) as ctx:
            BRIDGE.build_request("property-set", path=SAMPLE_PATH, name="status", value="x", property_type="yaml")
        self.assertEqual(ctx.exception.code, "INVALID_ARGUMENT")

    def test_move_requires_distinct_in_scope_target(self) -> None:
        """移动必须给出目标路径，且目标既不能越界也不能与源路径相同。

        [参数] 无。
        [返回] None：断言失败时抛出 AssertionError。
        最近修改时间: 2026-08-05 16:40:00 新增桥接参数校验契约测试。
        """
        request = BRIDGE.build_request("move", path=SAMPLE_PATH, to="知识库/90-Archive/note.md")
        self.assertEqual(request["to"], "知识库/90-Archive/note.md")
        with self.assertRaises(BRIDGE.BridgeError) as escape:
            BRIDGE.build_request("move", path=SAMPLE_PATH, to="../outside.md")
        self.assertEqual(escape.exception.code, "PATH_OUTSIDE_KNOWLEDGE")
        with self.assertRaises(BRIDGE.BridgeError) as same:
            BRIDGE.build_request("move", path=SAMPLE_PATH, to=SAMPLE_PATH)
        self.assertEqual(same.exception.code, "INVALID_ARGUMENT")

    def test_delete_never_accepts_permanent(self) -> None:
        """删除只接受路径，且请求中不得出现永久删除开关。

        [参数] 无。
        [返回] None：断言失败时抛出 AssertionError。
        最近修改时间: 2026-08-05 16:40:00 新增桥接参数校验契约测试。
        """
        request = BRIDGE.build_request("delete", path=SAMPLE_PATH, permanent=True)
        self.assertNotIn("permanent", request)
        # 适配器可以在注释里说明不透传，但不得把 permanent 作为 CLI 参数字面量拼进命令。
        self.assertNotIn("'permanent'", read_text(ADAPTER_PATH))

    def test_execution_case_notes_reject_relocation(self) -> None:
        """执行案例笔记必须拒绝移动与删除，追加式历史不得被破坏。

        [参数] 无。
        [返回] None：断言失败时抛出 AssertionError。
        最近修改时间: 2026-08-05 16:40:00 新增桥接参数校验契约测试。
        """
        for command in ("move", "delete"):
            kwargs = {"path": EXECUTION_CASE_PATH}
            if command == "move":
                kwargs["to"] = "知识库/90-Archive/case-slug.md"
            with self.assertRaises(BRIDGE.BridgeError) as ctx:
                BRIDGE.build_request(command, **kwargs)
            self.assertEqual(ctx.exception.code, "EXECUTION_CASE_IMMUTABLE", f"{command} 未保护执行案例笔记")
        self.assertEqual(BRIDGE.exit_code_for("EXECUTION_CASE_IMMUTABLE"), 2)

    def test_execution_case_directory_rejects_incoming_move(self) -> None:
        """执行案例目录也不得作为移动目标，避免绕过追加式契约。

        [参数] 无。
        [返回] None：断言失败时抛出 AssertionError。
        最近修改时间: 2026-08-05 16:40:00 新增桥接参数校验契约测试。
        """
        with self.assertRaises(BRIDGE.BridgeError):
            BRIDGE.build_request("move", path=SAMPLE_PATH, to=EXECUTION_CASE_PATH)


class DocumentSyncContractTest(unittest.TestCase):
    """文档组：校验命令模板与验证清单和脚本白名单保持一致。"""

    def test_cli_operations_lists_every_allowed_command(self) -> None:
        """命令模板必须逐项覆盖白名单里的每个命令。

        [参数] 无。
        [返回] None：断言失败时抛出 AssertionError。
        最近修改时间: 2026-08-05 16:40:00 新增桥接参数校验契约测试。
        """
        content = read_text(CLI_OPERATIONS)
        for command in sorted(BRIDGE.ALLOWED_COMMANDS):
            self.assertIn(command, content, f"命令模板缺少 {command}")

    def test_cli_operations_states_readback_and_boundaries(self) -> None:
        """命令模板必须写清三类回读判据与两条硬边界。

        [参数] 无。
        [返回] None：断言失败时抛出 AssertionError。
        最近修改时间: 2026-08-05 16:40:00 新增桥接参数校验契约测试。
        """
        content = read_text(CLI_OPERATIONS)
        for phrase in (
            "回读该属性",
            "新路径必须可读",
            "原路径必须不可读",
            "一律进回收站",
            "目标目录必须已存在",
            "执行案例",
        ):
            self.assertIn(phrase, content, f"命令模板缺少约束：{phrase}")

    def test_validation_checklist_registers_new_evidence(self) -> None:
        """验证清单必须登记迭代治理三项验证并进入证据映射。

        [参数] 无。
        [返回] None：断言失败时抛出 AssertionError。
        最近修改时间: 2026-08-05 16:40:00 新增桥接参数校验契约测试。
        """
        content = read_text(VALIDATION_CHECKLIST)
        for marker in ("TEST-OBS-017", "TEST-OBS-018", "TEST-OBS-019"):
            self.assertIn(marker, content, f"验证清单缺少 {marker}")


class GradedDispositionContractTest(unittest.TestCase):
    """分级组：校验三档处置规则与接替关系字段已取代旧禁令。"""

    def test_never_delete_rule_is_retired(self) -> None:
        """旧的「不要删除」禁令必须已从冲突规则中移除。

        [参数] 无。
        [返回] None：断言失败时抛出 AssertionError。
        最近修改时间: 2026-08-05 17:05:00 新增三档处置分级组断言。
        """
        content = read_text(CONFLICT_STALENESS)
        self.assertNotIn("不要删除", content)
        self.assertIn("知识库是可迭代更新的，不是只增量堆积", content)

    def test_three_tier_disposition_is_defined(self) -> None:
        """三档处置必须各自写明适用条件与动作。

        [参数] 无。
        [返回] None：断言失败时抛出 AssertionError。
        最近修改时间: 2026-08-05 17:05:00 新增三档处置分级组断言。
        """
        content = read_text(CONFLICT_STALENESS)
        self.assertIn("## 分级处置", content)
        for marker in ("标记取代", "归档退场", "删除"):
            self.assertIn(marker, content, f"分级处置缺少档次：{marker}")
        for rule in ("RULE-OBS-SUPERSEDE-001", "RULE-OBS-SUPERSEDE-002", "RULE-OBS-SUPERSEDE-003"):
            self.assertIn(rule, content, f"分级处置缺少规则 {rule}")

    def test_backlinks_precheck_is_mandatory(self) -> None:
        """三档处置前必须强制查引用数，引用不为零不得移动或删除。

        [参数] 无。
        [返回] None：断言失败时抛出 AssertionError。
        最近修改时间: 2026-08-05 17:05:00 新增三档处置分级组断言。
        """
        content = read_text(CONFLICT_STALENESS)
        self.assertIn("处置前置检查（强制）", content)
        self.assertIn("引用数不为 0 时**不得** `move` 或 `delete`", content)
        self.assertIn("RULE-OBS-SUPERSEDE-004", content)

    def test_execution_cases_are_excluded(self) -> None:
        """执行案例笔记必须被显式排除在三档处置之外。

        [参数] 无。
        [返回] None：断言失败时抛出 AssertionError。
        最近修改时间: 2026-08-05 17:05:00 新增三档处置分级组断言。
        """
        content = read_text(CONFLICT_STALENESS)
        self.assertIn("执行案例笔记排除范围", content)
        self.assertIn("不适用", content)
        self.assertIn("追加式状态事件", content)

    def test_automation_boundary_requires_reporting(self) -> None:
        """三档处置自动执行，但必须在总结的知识引用小节登记。

        [参数] 无。
        [返回] None：断言失败时抛出 AssertionError。
        最近修改时间: 2026-08-05 17:05:00 新增三档处置分级组断言。
        """
        content = read_text(CONFLICT_STALENESS)
        self.assertIn("自动化边界", content)
        self.assertIn("自动执行", content)
        self.assertIn("知识引用", content)
        self.assertIn("未登记的处置视为未闭环", content)

    def test_supersede_fields_are_declared(self) -> None:
        """笔记字段定义必须含双向接替字段与状态互斥约束。

        [参数] 无。
        [返回] None：断言失败时抛出 AssertionError。
        最近修改时间: 2026-08-05 17:05:00 新增三档处置分级组断言。
        """
        content = read_text(NOTE_SCHEMA)
        self.assertIn("supersedes: []", content)
        self.assertIn("superseded_by: []", content)
        self.assertIn("该字段非空时 `status` 不得为 `active`", content)
        self.assertIn("RULE-OBS-SUPERSEDE-005", read_text(CONFLICT_STALENESS))

    def test_execution_case_contract_is_untouched(self) -> None:
        """执行案例的追加式契约文本必须逐字保持不变。

        [参数] 无。
        [返回] None：断言失败时抛出 AssertionError。
        最近修改时间: 2026-08-05 17:05:00 新增三档处置分级组断言。
        """
        content = read_text(EXECUTION_CASE_NOTES)
        self.assertIn("`append` 是唯一更新方式；不得用 `create` 覆盖已有 `case_key`", content)


class ConflictDetectionContractTest(unittest.TestCase):
    """检测组：校验写入前三态判定、双向接替与接替跳转已落到流程与主入口。"""

    def test_three_state_decision_is_mandatory(self) -> None:
        """写入前必须显式判定补充、矛盾未裁决或取代三态之一。

        [参数] 无。
        [返回] None：断言失败时抛出 AssertionError。
        最近修改时间: 2026-08-05 17:20:00 新增写入前冲突判定检测组断言。
        """
        content = read_text(CAPTURE_FLOW)
        self.assertIn("必须显式判定三态之一", content)
        self.assertIn("RULE-OBS-DETECT-001", content)
        for state in ("`补充`", "`矛盾未裁决`", "`取代`"):
            self.assertIn(state, content, f"三态判定缺少 {state}")
        self.assertIn("不允许只写新笔记就收工", content)

    def test_iterative_update_flow_requires_bidirectional_link(self) -> None:
        """迭代更新流程必须要求双向写入接替关系。

        [参数] 无。
        [返回] None：断言失败时抛出 AssertionError。
        最近修改时间: 2026-08-05 17:20:00 新增写入前冲突判定检测组断言。
        """
        content = read_text(CAPTURE_FLOW)
        self.assertIn("## 迭代更新流程", content)
        self.assertIn("supersedes=[[旧笔记]]", content)
        self.assertIn("superseded_by=[[新笔记]]", content)
        self.assertIn("只写一侧视为治理未闭环", content)

    def test_audit_flow_is_documented_as_readonly(self) -> None:
        """巡检流程必须写明只读、手动入口且不替代语义裁决。

        [参数] 无。
        [返回] None：断言失败时抛出 AssertionError。
        最近修改时间: 2026-08-05 17:20:00 新增写入前冲突判定检测组断言。
        """
        content = read_text(CAPTURE_FLOW)
        self.assertIn("## 知识库巡检流程", content)
        self.assertIn("audit_vault_knowledge.py", content)
        self.assertIn("不做任何写入", content)
        self.assertIn("候选不等于结论", content)

    def test_retrieval_follows_supersede_pointer(self) -> None:
        """检索到已取代或已归档笔记时必须顺着接替关系跳转。

        [参数] 无。
        [返回] None：断言失败时抛出 AssertionError。
        最近修改时间: 2026-08-05 17:20:00 新增写入前冲突判定检测组断言。
        """
        for path in (CAPTURE_FLOW, OBSIDIAN_SKILL):
            content = read_text(path)
            self.assertIn("superseded_by", content, f"{path.name} 缺少接替跳转")
            self.assertIn("历史上下文", content, f"{path.name} 未限定旧笔记只作历史上下文")
        self.assertIn("RULE-OBS-DETECT-002", read_text(CAPTURE_FLOW))

    def test_ledger_operations_cover_new_commands(self) -> None:
        """引用台账的操作枚举必须覆盖本轮新增的读取与处置命令。

        [参数] 无。
        [返回] None：断言失败时抛出 AssertionError。
        最近修改时间: 2026-08-05 17:05:00 补齐台账操作枚举与分级处置一致性。
        """
        content = read_text(CAPTURE_FLOW)
        for operation in ("`properties`", "`property-read`", "`property-set`", "`move`", "`delete`"):
            self.assertIn(operation, content, f"引用台账操作枚举缺少 {operation}")
        self.assertIn("读取包括 `read`、`properties` 与 `property-read`", content)

    def test_skill_declares_iterate_loop(self) -> None:
        """技能主入口必须新增迭代循环并给出分级处置与巡检入口。

        [参数] 无。
        [返回] None：断言失败时抛出 AssertionError。
        最近修改时间: 2026-08-05 17:20:00 新增写入前冲突判定检测组断言。
        """
        content = read_text(OBSIDIAN_SKILL)
        self.assertIn("`iterate`", content)
        self.assertIn("可迭代更新，而不是只增量堆积", content)
        self.assertIn("只写新笔记不处置旧笔记是禁止行为", content)
        self.assertIn("audit_vault_knowledge.py", content)

    def test_four_state_and_fixed_root_are_untouched(self) -> None:
        """四态判定与固定根目录条款必须逐字保持不变。

        [参数] 无。
        [返回] None：断言失败时抛出 AssertionError。
        最近修改时间: 2026-08-05 17:20:00 新增写入前冲突判定检测组断言。
        """
        content = read_text(OBSIDIAN_SKILL)
        self.assertIn("`不适用`: 当前问题不依赖历史知识、知识库内容、长期用户偏好或重复实体", content)
        self.assertIn("Windows 固定根目录：`D:\\obsidian_data`", content)
        self.assertIn("真实知识工作区：`D:\\obsidian_data\\知识库\\`", content)


if __name__ == "__main__":
    unittest.main()
