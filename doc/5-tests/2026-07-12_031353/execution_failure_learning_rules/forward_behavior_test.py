#!/usr/bin/env python3
"""execution-failure-learning-rules 的确定性契约测试。"""

from dataclasses import dataclass
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[4]


@dataclass(frozen=True)
class Failure:
    category: str
    owner: str | None
    expected: bool = False
    business_bug: bool = False
    input_summary: str = "safe-input"
    success_standard: str = "artifact exists and is parseable"


def load(path: str) -> str:
    """读取仓库内 UTF-8 Skill 资产。

    [参数] path: 相对仓库根目录的文件路径。
    [返回] 文件文本。
    最近修改时间: 2026-07-12 03:13:53 增加前向行为测试的规则读取入口。
    """
    # 1. 以 UTF-8 读取规则文件，避免平台默认编码污染断言。
    return (ROOT / path).read_text(encoding="utf-8")


def sanitize(value: str) -> str:
    """移除测试输入中的凭据和私有路径。

    [参数] value: 待脱敏的错误摘要。
    [返回] 不含 secret 和本机私有路径的摘要。
    最近修改时间: 2026-07-12 03:13:53 增加脱敏门禁的前向验证。
    """
    # 1. 先清理 token，再清理私有路径，保持候选案例可复用。
    value = re.sub(r"sk-[A-Za-z0-9_-]+", "<redacted-secret>", value)
    value = re.sub(r"(?i)(token|password|secret)\s*[=:]\s*[^\s,;]+", r"\1=<redacted>", value)
    value = re.sub(r"[A-Za-z]:\\Users\\[^\s]+", "<workspace>", value)
    return value


def precheck(failure: Failure, active_cases: set[str]) -> str | None:
    """模拟执行前 active 案例预检。

    [参数] failure: 当前调用失败特征；active_cases: 已授权 owner 集合。
    [返回] 命中的 owner，未命中返回 None。
    最近修改时间: 2026-07-12 03:13:53 增加高风险调用 prevent 契约验证。
    """
    # 1. 预期负向输入不得误命中可执行案例。
    if failure.owner and failure.owner in active_cases and not failure.expected:
        return failure.owner
    return None


def recover(failure: Failure, repaired: bool, same_input: bool, same_standard: bool) -> str:
    """模拟 recover 阶段的有限复验判定。

    [参数] failure: 当前失败特征；repaired: 是否已应用修复；same_input: 是否保持原输入；same_standard: 是否保持原成功标准。
    [返回] routed、diagnose 或 verified 状态。
    最近修改时间: 2026-07-12 03:13:53 增加同输入同标准复验门禁。
    """
    # 1. 业务 Bug 和预期失败直接回流对应领域。
    if failure.expected or failure.business_bug:
        return "routed"
    if not repaired or not same_input or not same_standard:
        return "diagnose"
    return "verified"


def learn(
    failure: Failure,
    recovery_state: str,
    authorized: bool,
    conflicting_root_cause: bool = False,
) -> str:
    """模拟 learn 阶段的 candidate/active 晋级与冲突路由。

    [参数] failure: 失败特征；recovery_state: 复验状态；authorized: 当前轮维护授权；conflicting_root_cause: 是否存在根因冲突。
    [返回] rejected、skill-evolution、candidate、active 或 conflicted 状态。
    最近修改时间: 2026-07-12 03:13:53 增加案例晋级和唯一 owner 契约验证。
    """
    # 1. 先排除预期失败和业务 Bug，再判断 owner 与复验状态。
    if failure.expected or failure.business_bug:
        return "rejected"
    if failure.owner is None:
        return "skill-evolution"
    if recovery_state != "verified":
        return "rejected"
    if conflicting_root_cause:
        return "conflicted"
    return "active" if authorized else "candidate"


def check(condition: bool, label: str) -> None:
    """输出一条带标签的断言结果。

    [参数] condition: 断言结果；label: 场景说明。
    [返回] 无。
    最近修改时间: 2026-07-12 03:13:53 增加逐场景可追溯测试日志。
    """
    # 1. 失败立即抛出，避免把部分通过误报为完整通过。
    if not condition:
        raise AssertionError(label)
    # 2. 通过时输出稳定的机读前缀。
    print(f"[PASS] {label}")


def main() -> None:
    """执行 AC-001 至 AC-008 的前向行为契约测试。

    [参数] 无。
    [返回] 无。
    最近修改时间: 2026-07-12 03:13:53 完成周期 03 的八项验收场景覆盖。
    """
    print("[START] forward behavior contract tests")
    # 1. 读取规则资产并检查 owner、状态和边界契约。
    routing = load("execution-failure-learning-rules/references/classification-and-routing.md")
    lifecycle = load("execution-failure-learning-rules/references/lifecycle-and-gates.md")
    template = load("execution-failure-learning-rules/references/case-template.md")
    skill = load("execution-failure-learning-rules/SKILL.md")

    # 2. 验证 AC-001 至 AC-008 的文档合同。
    for owner in (
        "imagegen",
        "windows-wsl-execution-rules",
        "agent-browser",
        "authenticated-url-routing-rules",
        "mcp-installation-rules",
        "plugin-installation-rules",
        "obsidian-knowledge-flow",
    ):
        check(owner in routing, f"AC-001 registered owner: {owner}")
    check("\u540c\u4e00\u8f93\u5165" in lifecycle and "\u540c\u4e00\u6210\u529f\u6807\u51c6" in skill, "AC-002 same-input verification gate")
    check("status: candidate" in template and "owner_skill" in template, "AC-003 candidate template")
    check("active" in lifecycle and "\u5f53\u524d\u8f6e" in lifecycle, "AC-004 active authorization gate")
    check("bug-*" in skill and "\u4e1a\u52a1" in skill, "AC-005 business bug boundary")
    check("API key" in skill and "token" in skill, "AC-006 sensitive data boundary")
    check("conflicted" in lifecycle, "AC-007 conflict state")
    check("\u9884\u671f\u8d1f\u5411\u6d4b\u8bd5" in skill, "AC-008 expected-negative exclusion")

    # 3. 运行 prevent、recover、learn 的确定性行为镜像。
    active = {"imagegen", "windows-wsl-execution-rules"}
    known = Failure("input-contract", "imagegen")
    check(precheck(known, active) == "imagegen", "known active case is prechecked")
    unknown = Failure("tool-contract", "imagegen")
    recovered = recover(unknown, repaired=True, same_input=True, same_standard=True)
    check(recovered == "verified", "unknown failure recovers with original input and standard")
    check(learn(unknown, recovered, authorized=False) == "candidate", "verified unknown failure remains candidate without authorization")
    check(learn(unknown, recovered, authorized=True) == "active", "authorized verified candidate can become active")

    business = Failure("artifact", "imagegen", business_bug=True)
    check(learn(business, "verified", authorized=True) == "rejected", "business bug is not learned as execution case")
    expected = Failure("input-contract", "imagegen", expected=True)
    check(recover(expected, repaired=True, same_input=True, same_standard=True) == "routed", "expected negative does not enter recovery")
    check(learn(expected, "verified", authorized=True) == "rejected", "expected negative is not promoted")

    secret = "token=sk-test-only / path=C:\\Users\\private\\prompt.txt"
    clean = sanitize(secret)
    check("sk-test-only" not in clean and "C:\\Users\\private" not in clean, "secrets and private paths are redacted")
    no_owner = Failure("unknown", None)
    check(learn(no_owner, "verified", authorized=True) == "skill-evolution", "missing owner routes to skill evolution")
    check(learn(unknown, recovered, authorized=True, conflicting_root_cause=True) == "conflicted", "conflicting active and candidate cases are blocked")
    check(recover(unknown, repaired=False, same_input=True, same_standard=True) == "diagnose", "failed verification stops repeated unchanged retry")
    # 4. 输出最终汇总，失败断言会在此前直接退出。
    print("[END] forward behavior contract tests: PASS")


if __name__ == "__main__":
    main()
