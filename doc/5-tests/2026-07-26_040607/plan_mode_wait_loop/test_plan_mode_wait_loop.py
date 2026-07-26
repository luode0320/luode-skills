#!/usr/bin/env python3
"""验证 Plan Mode 决策选择框的永久等待、循环重发和总结闸门。"""

from __future__ import annotations

from dataclasses import dataclass, field
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[4]
PLANNING_SKILL = ROOT / "implementation-planning-rules" / "SKILL.md"
QUESTION_RULES = ROOT / "implementation-planning-rules" / "references" / "plan-question-coverage.md"
OUTPUT_GATE = ROOT / "implementation-planning-rules" / "references" / "plan-output-gate.md"
SUMMARY_SKILL = ROOT / "reasoning-summary-structure-rules" / "SKILL.md"
OPENAI_AGENT = ROOT / "implementation-planning-rules" / "agents" / "openai.yaml"
HISTORICAL_FIXTURE = Path(__file__).resolve().parent / "fixtures" / "historical_empty_then_summary.json"
OPEN_DIALOG = object()
FORBIDDEN_WAITING_OUTPUTS = frozenset(
    {
        "commentary",
        "limited_plan",
        "pending_summary",
        "proposed_plan",
        "final",
        "summary",
        "final_answer",
        "task_complete",
        "result_and_conclusion",
    }
)


class ContractViolation(ValueError):
    """表示决策调用不满足永久等待契约。"""


@dataclass(frozen=True)
class Question:
    """冻结一个可重发的决策问题。"""

    question_id: str
    prompt: str
    options: tuple[str, ...]
    recommended_option: str | None = None


@dataclass
class DecisionState:
    """在测试中模拟宿主返回与 Agent 状态迁移。"""

    questions: tuple[Question, ...]
    answered: dict[str, str] = field(default_factory=dict)
    status: str = "WAITING_DECISION"
    calls: list[dict[str, Any]] = field(default_factory=list)
    outputs: list[str] = field(default_factory=list)
    active_dialogs: int = 0

    def pending_questions(self) -> tuple[Question, ...]:
        """返回尚未回答的问题，保持原问题顺序和文案。[参数] self：当前决策状态；[返回] 尚未回答的问题元组；最近修改时间：2026-07-26 04:50:06 保持部分答案重发顺序。"""

        return tuple(question for question in self.questions if question.question_id not in self.answered)


def assert_true(condition: bool, message: str) -> None:
    """以稳定中文错误结束失败用例。[参数] condition：断言条件；message：失败说明；[返回] 无；最近修改时间：2026-07-26 04:50:06 强化空答案与闸门断言。"""

    if not condition:
        raise AssertionError(message)


def read_text(path: Path) -> str:
    """统一按 UTF-8 读取规则与 Agent 提示。[参数] path：待读取文件路径；[返回] UTF-8 文本；最近修改时间：2026-07-26 04:50:06 保持规则文本回归可复核。"""

    return path.read_text(encoding="utf-8")


def build_decision_call(state: DecisionState) -> dict[str, Any]:
    """只构造冻结问题，确保重发保留推荐项且不携带自动解析字段。[参数] state：当前决策状态；[返回] 冻结的选择框载荷；最近修改时间：2026-07-26 04:50:06 增加推荐标记回归。"""

    # 1. 构造冻结问题载荷，并保留推荐标记。
    payload = {
        "questions": [
            {
                "id": question.question_id,
                "question": question.prompt,
                "options": list(question.options),
                "recommended": question.recommended_option,
            }
            for question in state.pending_questions()
        ]
    }
    validate_decision_call(payload)
    return payload


def validate_decision_call(payload: dict[str, Any]) -> None:
    """拒绝所有 autoResolutionMs 变体，不把宿主空返回当作授权。[参数] payload：待校验的选择框载荷；[返回] 无，失败时抛出 ContractViolation；最近修改时间：2026-07-26 04:50:06 固定无超时字段契约。"""

    # 1. 拒绝任何自动放行字段。
    if "autoResolutionMs" in payload:
        raise ContractViolation("决策调用不得出现 autoResolutionMs 字段")
    # 2. 保证每次调用都有未决问题。
    if not payload.get("questions"):
        raise ContractViolation("决策调用必须至少包含一个未决问题")


def resend_decision_call(state: DecisionState) -> None:
    """旧调用返回后只创建一个新的活动选择框。[参数] state：当前决策状态；[返回] 无；最近修改时间：2026-07-26 04:50:06 增加单活动框保护。"""

    # 1. 旧调用已结束后才创建唯一的新活动框。
    assert_true(state.active_dialogs == 0, "旧选择框尚未结束就并发创建了新选择框")
    state.calls.append(build_decision_call(state))
    state.active_dialogs = 1


def is_directive(result: dict[str, Any], *directives: str) -> bool:
    """匹配用户明确发出的停止或代选授权。[参数] result：宿主返回；directives：允许的明确指令；[返回] 是否命中明确指令；最近修改时间：2026-07-26 04:50:06 保持停止与授权边界。"""

    message = str(result.get("user_message", "")).strip()
    return result.get("directive") in directives or message in directives


def process_tool_return(state: DecisionState, result: dict[str, Any] | None | object) -> str:
    """处理一次宿主返回，并返回本轮唯一允许的后续动作。[参数] state：当前决策状态；result：选择框返回、空返回或仍打开哨兵；[返回] wait、resend、continue、stop 或 report_blocked；最近修改时间：2026-07-26 06:00:00 扩大终态短路并阻止陈旧返回重发。"""

    # 1. 所有已离开等待的状态都忽略陈旧返回，不得再次创建选择框。
    if state.status == "STOPPED":
        state.active_dialogs = 0
        return "stop"
    if state.status == "HOST_BLOCKED":
        state.active_dialogs = 0
        return "report_blocked"
    if state.status in {"DECISION_RESOLVED", "USER_DELEGATED"}:
        state.active_dialogs = 0
        return "continue"

    # 2. 选择框仍然打开时只保持等待，不创建第二个调用或输出文本。
    if result is OPEN_DIALOG:
        assert_true(state.status == "WAITING_DECISION", "选择框打开期间必须保持 WAITING_DECISION")
        assert_true(state.active_dialogs == 1, "选择框打开期间活动框数量不是 1")
        return "wait"

    # 3. 宿主返回 null/空对象/缺失答案时，仍视为未决并立即串行重发。
    state.active_dialogs = 0
    if result is None or not isinstance(result, dict):
        resend_decision_call(state)
        return "resend"

    # 4. 明确停止、代选和工具故障优先于普通答案解析。
    if is_directive(result, "STOP_TASK", "停止任务"):
        state.status = "STOPPED"
        return "stop"
    if is_directive(result, "USER_DELEGATED", "你来定", "按推荐", "随便"):
        state.status = "USER_DELEGATED"
        return "continue"
    if result.get("tool_error"):
        state.status = "HOST_BLOCKED"
        return "report_blocked"

    # 5. 空答案或未知问题 ID 都只触发同一选择框的重发。
    answers = result.get("answers")
    if not isinstance(answers, dict):
        resend_decision_call(state)
        return "resend"
    pending_ids = {question.question_id for question in state.pending_questions()}
    accepted = {key: value for key, value in answers.items() if key in pending_ids}
    if not accepted:
        resend_decision_call(state)
        return "resend"

    # 6. 保存部分答案；未决问题仍然只能重发剩余问题。
    state.answered.update({key: str(value) for key, value in accepted.items()})
    if state.pending_questions():
        resend_decision_call(state)
        return "resend"
    state.status = "DECISION_RESOLVED"
    return "continue"


def allow_final_summary(state: DecisionState) -> bool:
    """只有决策完成或明确代选后才允许消费最终总结。[参数] state：当前决策状态；[返回] 是否允许最终总结；最近修改时间：2026-07-26 04:50:06 保持未决总结闸门。"""

    return state.status in {"DECISION_RESOLVED", "USER_DELEGATED"}


def emit_output(state: DecisionState, output_type: str) -> bool:
    """模拟总结消费方，只在闸门放行时写入可见输出。[参数] state：当前决策状态；output_type：输出类型；[返回] 是否实际写入输出；最近修改时间：2026-07-26 06:00:00 覆盖完整冻结输出集合。"""

    # 1. 未决或阻断状态拒绝所有冻结集合内的可见输出。
    if output_type in FORBIDDEN_WAITING_OUTPUTS and not allow_final_summary(state):
        return False
    # 2. 仅记录已被闸门放行的可见输出。
    state.outputs.append(output_type)
    return True


def history_allows_final_summary(events: list[dict[str, Any]]) -> bool:
    """回放历史事件，验证空答案后的总结确实会被消费方拒绝。[参数] events：脱敏历史事件；[返回] 历史轨迹是否允许最终总结；最近修改时间：2026-07-26 06:00:00 回放完整冻结输出集合。"""

    # 1. 从同一未决初始状态开始回放历史。
    state = new_state()
    # 2. 任何空答案后的总结事件都必须经过消费方闸门。
    for event in events:
        if event["type"] == "tool_return":
            result = {"answers": event.get("answers")} if "answers" in event else None
            process_tool_return(state, result)
            continue
        if event["type"] in FORBIDDEN_WAITING_OUTPUTS:
            if not emit_output(state, event["type"]):
                return False
    return True


def new_state() -> DecisionState:
    """创建与回归样本一致的两个决策问题。[参数] 无；[返回] 带一个活动选择框的初始状态；最近修改时间：2026-07-26 04:50:06 固定推荐标记与活动框基线。"""

    # 1. 冻结两个问题及其推荐选项。
    state = DecisionState(
        questions=(
            Question("scope", "是否接入全部范围？", ("全部接入", "仅核心链路"), "仅核心链路"),
            Question("cost", "是否启用费用闸门？", ("启用", "不启用"), "启用"),
        )
    )
    # 2. 建立唯一初始活动选择框。
    state.calls.append(build_decision_call(state))
    state.active_dialogs = 1
    return state


def test_no_auto_resolution_field() -> None:
    """决策型调用完全省略自动解析字段。[参数] 无；[返回] 无；最近修改时间：2026-07-26 04:50:06 覆盖超时字段负例。"""

    # 1. 检查首次调用不携带自动解析字段。
    state = new_state()
    assert_true("autoResolutionMs" not in state.calls[0], "首次决策调用错误携带 autoResolutionMs")
    # 2. 检查显式超时负例全部被拒绝。
    for value in (60000, None, 0):
        try:
            validate_decision_call({"questions": [{"id": "scope"}], "autoResolutionMs": value})
        except ContractViolation:
            continue
        raise AssertionError(f"autoResolutionMs={value!r} 未被拒绝")


def test_empty_answers_are_unbounded() -> None:
    """连续 2、10、100 次空答案都保持等待并立即重发。[参数] 无；[返回] 无；最近修改时间：2026-07-26 04:50:06 补齐 null、空对象和缺失答案。"""

    # 1. 连续多轮空答案始终保持等待并重发。
    for cycles in (2, 10, 100):
        state = new_state()
        # 1.1 每次宿主返回后只保留一个活动选择框。
        for _ in range(cycles):
            action = process_tool_return(state, {"answers": {}})
            assert_true(action == "resend", f"空答案第 {cycles} 轮未重发")
            assert_true(state.status == "WAITING_DECISION", "空答案改变了未决状态")
            assert_true(not state.outputs, "等待循环期间产生了可见输出")
            assert_true(state.active_dialogs == 1, "空答案重发没有保持单活动选择框")
        assert_true(len(state.calls) == cycles + 1, "重发次数与空答案次数不一致")
        assert_true(all("autoResolutionMs" not in call for call in state.calls), "重发调用带有自动解析字段")

    # 2. 覆盖 null、空对象和缺失 answers 的空返回。
    for empty_return in (None, {}, {"answers": None}):
        state = new_state()
        action = process_tool_return(state, empty_return)
        assert_true(action == "resend", "null/空对象/缺失答案没有立即重发")
        assert_true(state.status == "WAITING_DECISION", "null/空对象/缺失答案改变了未决状态")
        assert_true(len(state.calls) == 2, "null/空对象/缺失答案没有创建唯一串行重发")
        assert_true(state.active_dialogs == 1, "null/空对象/缺失答案没有保持单活动选择框")


def test_resend_preserves_questions() -> None:
    """空答案重发保持问题 ID、选项、推荐文案和顺序。[参数] 无；[返回] 无；最近修改时间：2026-07-26 04:50:06 增加推荐标记断言。"""

    # 1. 保存原始载荷并触发一次空答案重发。
    state = new_state()
    original = state.calls[0]
    process_tool_return(state, {"answers": {}})
    assert_true(state.calls[-1] == original, "空答案重发没有保持冻结问题载荷")
    assert_true(original["questions"][0]["recommended"] == "仅核心链路", "重发丢失推荐标记")


def test_partial_answers_are_preserved() -> None:
    """部分答案必须保存，只重发剩余问题。[参数] 无；[返回] 无；最近修改时间：2026-07-26 04:50:06 保持部分答案回归。"""

    # 1. 提交一个答案并检查剩余问题载荷。
    state = new_state()
    action = process_tool_return(state, {"answers": {"scope": "仅核心链路"}})
    assert_true(action == "resend", "部分答案没有重发剩余问题")
    assert_true(state.answered == {"scope": "仅核心链路"}, "部分答案没有保存")
    assert_true([item["id"] for item in state.calls[-1]["questions"]] == ["cost"], "重发包含已回答问题")


def test_delayed_choice_resolves() -> None:
    """用户长时间未选择后回来完成选择，计划才恢复。[参数] 无；[返回] 无；最近修改时间：2026-07-26 04:50:06 保持百轮延迟恢复回归。"""

    # 1. 先跨越 100 次空答案重发。
    state = new_state()
    for _ in range(100):
        process_tool_return(state, {"answers": {}})
    # 2. 用户回来后提交完整选择，计划才恢复。
    action = process_tool_return(state, {"answers": {"scope": "全部接入", "cost": "启用"}})
    assert_true(action == "continue", "延迟完整选择没有恢复计划")
    assert_true(state.status == "DECISION_RESOLVED", "完整选择未进入 DECISION_RESOLVED")
    assert_true(allow_final_summary(state), "完整选择后仍拒绝计划收敛")


def test_explicit_delegation_and_stop() -> None:
    """代选和停止必须由用户明确表达，且终态陈旧返回不再重发。[参数] 无；[返回] 无；最近修改时间：2026-07-26 06:00:00 增加解决、代选和停止终态保护断言。"""

    # 1. 明确授权代选后允许计划继续。
    delegated = new_state()
    assert_true(process_tool_return(delegated, {"user_message": "按推荐"}) == "continue", "明确代选未获授权")
    assert_true(delegated.status == "USER_DELEGATED", "代选状态错误")
    assert_true(allow_final_summary(delegated), "明确代选后不允许计划继续")

    # 2. 明确停止后进入终态且不再重发。
    stopped = new_state()
    assert_true(process_tool_return(stopped, {"user_message": "停止任务"}) == "stop", "明确停止未结束等待")
    assert_true(stopped.status == "STOPPED", "停止状态错误")
    assert_true(len(stopped.calls) == 1, "明确停止后仍然重发选择框")
    assert_true(stopped.active_dialogs == 0, "明确停止后仍保留活动选择框")
    assert_true(process_tool_return(stopped, {"answers": {}}) == "stop", "停止后空答案错误触发重发")
    assert_true(len(stopped.calls) == 1, "停止后空答案新增了选择框")

    # 3. 已解决、已代选和宿主阻断状态都忽略迟到空答案。
    resolved = new_state()
    assert_true(process_tool_return(resolved, {"answers": {"scope": "全部接入", "cost": "启用"}}) == "continue", "完整选择未完成")
    assert_true(process_tool_return(resolved, {"answers": {}}) == "continue", "已解决状态错误重发")
    assert_true(len(resolved.calls) == 1, "已解决状态新增了选择框")

    delegated_late = new_state()
    assert_true(process_tool_return(delegated_late, {"user_message": "按推荐"}) == "continue", "代选状态未完成")
    assert_true(process_tool_return(delegated_late, {"answers": {}}) == "continue", "已代选状态错误重发")
    assert_true(len(delegated_late.calls) == 1, "已代选状态新增了选择框")


def test_host_fault_blocks_summary() -> None:
    """工具明确不可恢复故障时保持阻断，不输出总结。[参数] 无；[返回] 无；最近修改时间：2026-07-26 06:00:00 增加阻断状态陈旧返回保护。"""

    # 1. 模拟不可恢复工具故障并检查阻断状态。
    state = new_state()
    assert_true(process_tool_return(state, {"tool_error": "无法再次调用"}) == "report_blocked", "工具故障未进入阻断")
    assert_true(state.status == "HOST_BLOCKED", "工具故障状态错误")
    assert_true(not allow_final_summary(state), "工具故障错误放行最终总结")
    assert_true(state.active_dialogs == 0, "工具故障后仍保留活动选择框")
    assert_true(process_tool_return(state, {"answers": {}}) == "report_blocked", "阻断状态错误重发")
    assert_true(len(state.calls) == 1, "阻断状态新增了选择框")


def test_waiting_state_rejects_final() -> None:
    """任何未决选择都拒绝冻结集合内的可见输出。[参数] 无；[返回] 无；最近修改时间：2026-07-26 06:00:00 扩大输出闸门负例集合。"""

    # 1. 选择框仍打开时只等待，不创建并行框。
    state = new_state()
    assert_true(not allow_final_summary(state), "WAITING_DECISION 错误允许最终总结")
    assert_true(process_tool_return(state, OPEN_DIALOG) == "wait", "选择框仍打开时错误触发了重发")
    # 2. 逐类验证总结消费方拒绝写入。
    for forbidden in sorted(FORBIDDEN_WAITING_OUTPUTS):
        assert_true(not emit_output(state, forbidden), f"等待期间错误放行 {forbidden}")
    assert_true(not state.outputs, "等待期间消费方写入了禁止输出")


def test_historical_empty_then_summary_is_rejected() -> None:
    """历史违规轨迹“空答案 -> 结果与结论”必须判为失败。[参数] 无；[返回] 无；最近修改时间：2026-07-26 06:00:00 覆盖完整冻结输出集合回放。"""

    # 1. 读取脱敏历史轨迹并确认其确实包含违规顺序。
    events = json.loads(HISTORICAL_FIXTURE.read_text(encoding="utf-8"))["events"]
    empty_seen = any(event["type"] == "tool_return" and event.get("answers") == {} for event in events)
    forbidden_after_empty = any(event["type"] in {"summary", "task_complete"} for event in events)
    # 2. 调用消费方回放判定器，不能只检查 fixture 文本。
    assert_true(empty_seen and forbidden_after_empty, "历史违规 fixture 未命中空答案后总结轨迹")
    assert_true(not history_allows_final_summary(events), "历史空答案后总结轨迹未被消费方拒绝")
    # 3. 对冻结集合内每种可见输出逐一回放，防止历史路径漏闸门。
    for output_type in sorted(FORBIDDEN_WAITING_OUTPUTS):
        replay = [{"type": "tool_return", "answers": {}}, {"type": output_type}]
        assert_true(not history_allows_final_summary(replay), f"历史空答案后错误放行 {output_type}")


def test_rule_text_contract() -> None:
    """规则、总结 Owner 和 Agent 提示必须共同表达永久等待闸门。[参数] 无；[返回] 无；最近修改时间：2026-07-26 05:35:38 对齐 result_and_conclusion 冻结标识。"""

    # 1. 读取规划、总结和 Agent 提示文本。
    planning = read_text(PLANNING_SKILL)
    questions = read_text(QUESTION_RULES)
    output_gate = read_text(OUTPUT_GATE)
    summary = read_text(SUMMARY_SKILL)
    agent = read_text(OPENAI_AGENT)
    # 2. 校验稳定 ID 与永久等待关键词均存在。
    required = (
        "RULE-PMW-001",
        "WAITING_DECISION",
        "answers:{}",
        "空答案后的下一动作只能是重新调用同一选择框",
        "重发次数没有上限",
        "commentary",
        "limited_plan",
        "pending_summary",
        "proposed_plan",
        "final_answer",
        "result_and_conclusion",
        "AC-PMW-001",
        "SUMMARY-GATE-PMW-001",
    )
    # 3. 对所有 Owner 文本执行统一断言。
    combined = "\n".join((planning, questions, output_gate, summary, agent))
    for needle in required:
        assert_true(needle in combined, f"规则文本缺少 {needle}")
    assert_true("final_answer" in summary and "task_complete" in summary, "总结 Owner 缺少 final 闸门")


def main() -> None:
    """执行全部永久等待行为回归。[参数] 无；[返回] 无；最近修改时间：2026-07-26 04:50:06 输出可复核的十项回归结果。"""

    # 1. 固定回归用例顺序，便于定位首个失败点。
    tests = (
        test_no_auto_resolution_field,
        test_empty_answers_are_unbounded,
        test_resend_preserves_questions,
        test_partial_answers_are_preserved,
        test_delayed_choice_resolves,
        test_explicit_delegation_and_stop,
        test_host_fault_blocks_summary,
        test_waiting_state_rejects_final,
        test_historical_empty_then_summary_is_rejected,
        test_rule_text_contract,
    )
    # 2. 逐项执行并打印可回放结果。
    for test in tests:
        test()
        print(f"PASS {test.__name__}")
    print(f"plan-mode-wait-loop: PASS ({len(tests)} cases)")


if __name__ == "__main__":
    main()
