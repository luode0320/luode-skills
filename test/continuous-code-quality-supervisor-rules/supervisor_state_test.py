"""持续代码质量监督状态、路由和安全边界的本地契约测试。"""

from __future__ import annotations

import json
from pathlib import Path
import sys
import tempfile
import unittest


SCRIPTS_DIR = (
    Path(__file__).resolve().parents[2]
    / "continuous-code-quality-supervisor-rules"
    / "scripts"
)
sys.path.insert(0, str(SCRIPTS_DIR))

from supervisor_state import (  # noqa: E402
    OWNER_NAMES,
    activation_status,
    finding_fingerprint,
    read_owner_sources,
    record_scan,
    register_owner,
    route_owners,
    start,
    state_path,
    status,
    stop,
)


class SupervisorStateTests(unittest.TestCase):
    """验证双条件触发、Owner 注册、finding 去重和安全拒绝。"""

    def setUp(self) -> None:
        """为每个测试创建隔离的 local 状态目录。

        [参数] 无
        [返回] 无
        最近修改时间：2026-07-25 08:00:00；隔离状态脚本测试数据。
        """

        # 1. 创建临时 checkout 和独立状态根目录。
        self.tempdir = tempfile.TemporaryDirectory()
        self.root = Path(self.tempdir.name)
        self.checkout = self.root / "checkout"
        self.checkout.mkdir()

    def tearDown(self) -> None:
        """清理临时状态目录。

        [参数] 无
        [返回] 无
        最近修改时间：2026-07-25 08:00:00；避免测试状态污染工作树。
        """

        # 1. 删除本测试创建的临时目录。
        self.tempdir.cleanup()

    def test_trigger_requires_goal_and_monitor_intent(self) -> None:
        """只有 Goal active 和监控意图同时满足时才允许启动。

        [参数] 无
        [返回] 无；断言失败时由 unittest 抛出异常
        最近修改时间：2026-07-25 08:00:00；覆盖双条件和 Plan Mode 负向边界。
        """

        # 1. 验证 Goal、用户意图和 Plan Mode 的四种关键组合。
        self.assertEqual(activation_status(False, "监控代码")[0], "inactive")
        self.assertEqual(activation_status(True, "继续开发")[0], "inactive")
        self.assertEqual(activation_status(True, "监控代码")[0], "active")
        self.assertEqual(activation_status(True, "监控代码", plan_mode=True)[0], "inactive")

    def test_start_register_scan_deduplicates_and_stops(self) -> None:
        """状态生命周期和相同 fingerprint 的合并必须稳定。

        [参数] 无
        [返回] 无；断言失败时由 unittest 抛出异常
        最近修改时间：2026-07-25 08:00:00；覆盖状态生命周期和 finding 去重。
        """

        # 1. 启动监督、登记 Owner、扫描两次并验证同指纹合并。
        started = start(self.checkout, True, "监控代码", self.root / "state")
        self.assertEqual(started["status"], "active")
        registered = register_owner(self.checkout, "code-readability-rules", "code-readability-rules/SKILL.md", "代码改动", self.root / "state")
        self.assertEqual(len(registered["owners"]), 1)
        finding = {
            "owner_skill": "code-readability-rules",
            "rule_source": "code-readability-rules/SKILL.md",
            "file": "src/example.py",
            "evidence": "function has excessive branching",
            "severity": "P1",
            "fingerprint": finding_fingerprint(
                "code-readability-rules",
                "code-readability-rules/SKILL.md",
                "src/example.py",
                "function has excessive branching",
            ),
            "status": "open",
        }
        first = record_scan(self.checkout, "diff-001", ["src/example.py"], [finding], self.root / "state")
        second = record_scan(self.checkout, "diff-002", ["src/example.py"], [finding], self.root / "state")
        self.assertEqual(first["added"], 1)
        self.assertEqual(second["added"], 0)
        self.assertEqual(second["updated"], 1)
        current = status(self.checkout, self.root / "state")["state"]
        self.assertEqual(len(current["findings"]), 1)
        self.assertEqual(current["findings"][0]["scan_count"], 2)
        self.assertEqual(stop(self.checkout, self.root / "state")["status"], "stopped")

    def test_missing_owner_and_sensitive_finding_are_rejected(self) -> None:
        """未知 Owner、敏感字段和多行证据不得进入状态。

        [参数] 无
        [返回] 无；断言失败时由 unittest 抛出异常
        最近修改时间：2026-07-25 08:00:00；覆盖 Owner 和敏感字段拒绝边界。
        """

        # 1. 验证未知 Owner 和敏感字段都不能写入监督状态。
        start(self.checkout, True, "监控代码", self.root / "state")
        with self.assertRaises(ValueError):
            register_owner(self.checkout, "unknown-owner", "missing", "anything", self.root / "state")
        invalid = {
            "owner_skill": "code-readability-rules",
            "rule_source": "owner/SKILL.md",
            "file": "src/example.py",
            "evidence": "safe",
            "severity": "P1",
            "fingerprint": "fp-002",
            "status": "open",
            "token": "must-not-persist",
        }
        with self.assertRaises(ValueError):
            record_scan(self.checkout, "diff-003", ["src/example.py"], [invalid], self.root / "state")
        with self.assertRaises(ValueError):
            record_scan(self.checkout, "diff-004", [str(self.root / "secret.py")], [], self.root / "state")

    def test_owner_routing_covers_api_and_excludes_stage_skills(self) -> None:
        """API 改动命中四个接口 Owner，路由结果不包含排除 Skill。

        [参数] 无
        [返回] 无；断言失败时由 unittest 抛出异常
        最近修改时间：2026-08-01 00:00:00；改用共享路由并覆盖 API 路由排除。
        """

        # 1. 验证 API 四 Owner 同时命中且排除列表完全不进入结果。
        owners = route_owners(["src/api/user_controller.py"])
        expected_allowed = {
            "api-endpoint-rules",
            "api-request-rules",
            "api-response-rules",
            "api-swagger-rules",
            "chinese-comment-rules",
            "code-generation-style-rules",
            "code-minimal-change-rules",
            "code-readability-rules",
            "code-style-consistency-rules",
            "comment-completion-gate-rules",
            "comment-placement-granularity-rules",
            "common-util-rules",
            "database-query-rules",
            "database-schema-rules",
            "error-handling-rules",
            "frontend-component-rules",
            "frontend-ui-visual-rules",
            "golang-patterns",
            "logging-trace-rules",
            "micro-business-architecture-rules",
            "naming-rules",
            "package-structure-rules",
            "test-program-rules",
            "time-util-rules",
            "vercel-react-best-practices",
            "vue-best-practices",
            "vue-router-best-practices",
            "windows-encoding-rules",
        }
        self.assertEqual(OWNER_NAMES, expected_allowed)
        self.assertIn("code-generation-style-rules", owners)
        self.assertIn("api-endpoint-rules", owners)
        self.assertIn("api-request-rules", owners)
        self.assertIn("api-response-rules", owners)
        self.assertIn("api-swagger-rules", owners)
        excluded = {
            "implementation-planning-rules",
            "agent-runtime-recovery-rules",
            "artifact-delivery-gate-rules",
            "artifact-storage-rules",
            "autonomous-execution-rules",
            "browser-advanced-testing-rules",
            "browser-session-automation-rules",
            "code-change-finalization-gate-rules",
            "code-context-resync-rules",
            "git-collaboration-rules",
            "codegraph-analysis-rules",
            "context-compression-rules",
            "delivery-summary-rules",
            "execution-failure-learning-rules",
            "delivery-summary-rules",
            "frontend-design",
            "functional-validation-rules",
            "git-collaboration-rules",
            "implementation-planning-rules",
            "knowledge-flow",
            "parallel-task-dispatch-rules",
            "project-local-skills-rules",
            "project-memory-rules",
            "project-style-rules",
            "skill-audit-rules",
            "skill-execution-compliance-gate-rules",
            "swag-openapi-maintainer-rules",
            "task-plan-rehydration-rules",
            "team-development-rules",
            "test-strategy-rules",
            "test-regression-rules",
            "functional-validation-rules",
            "thread-title-rules",
            "web-design-guidelines",
        }
        self.assertTrue(excluded.isdisjoint(owners))
        self.assertTrue(excluded.isdisjoint(OWNER_NAMES))

    def test_condition_routing_does_not_trigger_unrelated_specialists(self) -> None:
        """普通 Python 改动不误触发 API、数据库、语言和测试 Owner。

        [参数] 无
        [返回] 无；断言失败时由 unittest 抛出异常
        最近修改时间：2026-07-25 08:00:00；覆盖条件 Owner 的不误触发边界。
        """

        # 1. 使用普通服务文件验证条件专项不会误报。
        owners = set(route_owners(["src/service/user.py"]))
        self.assertNotIn("api-endpoint-rules", owners)
        self.assertNotIn("database-query-rules", owners)
        self.assertNotIn("golang-patterns", owners)
        self.assertNotIn("test-program-rules", owners)

    def test_database_routing_orders_schema_before_query(self) -> None:
        """数据库改动必须先路由 Schema，再路由 Query。

        [参数] 无
        [返回] 无；断言失败时由 unittest 抛出异常
        最近修改时间：2026-07-25 08:00:00；覆盖数据库 Owner 的固定优先级。
        """

        # 1. 使用迁移 SQL 同时命中两个数据库 Owner 并检查顺序。
        owners = route_owners(["db/migrations/001_user_schema.sql"], ["database-query"])
        self.assertLess(owners.index("database-schema-rules"), owners.index("database-query-rules"))

    def test_language_framework_and_test_program_routing(self) -> None:
        """Go、Vue Router、React 和测试程序命中各自专项且不误触发测试执行 Skill。

        [参数] 无
        [返回] 无；断言失败时由 unittest 抛出异常
        最近修改时间：2026-07-25 08:00:00；覆盖语言框架和测试代码条件路由。
        """

        # 1. 分别验证 Go、Vue Router、React 和测试程序的专项 Owner。
        self.assertIn("golang-patterns", route_owners(["cmd/app/main.go"]))
        vue_owners = route_owners(["src/router/App.vue"], ["vue-router"])
        self.assertIn("vue-best-practices", vue_owners)
        self.assertIn("vue-router-best-practices", vue_owners)
        self.assertNotIn("api-endpoint-rules", vue_owners)
        self.assertIn("vercel-react-best-practices", route_owners(["src/App.tsx"]))
        test_owners = route_owners(["tests/fixtures/user_stub.py"])
        self.assertIn("test-program-rules", test_owners)
        self.assertNotIn("test-strategy-rules", test_owners)
        self.assertNotIn("functional-validation-rules", test_owners)

    def test_routing_preserves_paths_with_spaces(self) -> None:
        """带空格文件名仍按完整路径识别语言、测试目录和编码扩展名。

        [参数] 无
        [返回] 无；断言失败时由 unittest 抛出异常
        最近修改时间：2026-07-25 08:00:00；防止路径拼接后按空格拆分导致条件 Owner 漏触发。
        """

        # 1. 以包含空格的真实相对路径覆盖多个扩展名和目录特征。
        owners = route_owners(["tests with spaces/fixtures/user stub.py", "src with spaces/App.tsx"])
        self.assertIn("test-program-rules", owners)
        self.assertIn("vercel-react-best-practices", owners)
        self.assertIn("frontend-component-rules", owners)
        self.assertNotIn("golang-patterns", route_owners(["docs/draft.go notes/readme.txt"]))

    def test_routing_keeps_file_semantics_isolated(self) -> None:
        """不同文件的独立特征不得串联成 Vue Router 或数据库路由。

        [参数] 无
        [返回] 无；断言失败时由 unittest 抛出异常
        最近修改时间：2026-07-25 08:00:00；覆盖跨文件语义串联和无边界子串误报。
        """

        # 1. 文档中的 router 和 jquery 文件名均不构成专项代码语义。
        owners = route_owners(["src/App.vue", "docs/router-notes.md"])
        self.assertNotIn("vue-router-best-practices", owners)
        self.assertNotIn("database-query-rules", route_owners(["src/vendor/jquery.ts"]))

    def test_cross_cutting_and_micro_business_routing(self) -> None:
        """日志、异常、时间、工具、结构、编码和微业务信号命中对应 Owner。

        [参数] 无
        [返回] 无；断言失败时由 unittest 抛出异常
        最近修改时间：2026-07-25 08:00:00；覆盖横切和条件业务 Owner。
        """

        # 1. 使用受控语义标签验证所有横切和条件 Owner。
        owners = route_owners(
            ["src/common/config.yaml", "src/business/user/contracts/user_contract.py", ".editorconfig"],
            [
                "logging",
                "error-handling",
                "time",
                "common-util",
                "package-structure",
                "cross-business-import",
            ],
        )
        for owner in (
            "logging-trace-rules",
            "error-handling-rules",
            "time-util-rules",
            "common-util-rules",
            "package-structure-rules",
            "windows-encoding-rules",
            "micro-business-architecture-rules",
        ):
            self.assertIn(owner, owners)
        self.assertLess(owners.index("package-structure-rules"), owners.index("common-util-rules"))

    def test_frontend_routing_uses_specific_signals(self) -> None:
        """前端专项只在对应文件、框架或语义信号下触发，避免粗粒度误报。

        [参数] 无
        [返回] 无；断言失败时由 unittest 抛出异常
        最近修改时间：2026-07-25 19:05:00；覆盖 Vue、Router、React、组件和视觉负路由。
        """

        # 1. Vue 计算属性只触发 Vue 与基础/注释 Owner，不误触发视觉或 Router。
        vue_computed = route_owners(["src/views/User.vue"], ["computed"])
        self.assertIn("vue-best-practices", vue_computed)
        self.assertNotIn("frontend-ui-visual-rules", vue_computed)
        self.assertNotIn("vue-router-best-practices", vue_computed)
        # 2. 组件契约和视觉语义分别触发组件 Owner 与视觉 Owner。
        vue_props = route_owners(["src/views/User.vue"], ["props", "emits"])
        self.assertIn("frontend-component-rules", vue_props)
        self.assertNotIn("frontend-ui-visual-rules", vue_props)
        vue_visual = route_owners(["src/views/User.vue"], ["aria", "css"])
        self.assertIn("frontend-ui-visual-rules", vue_visual)
        self.assertNotIn("vue-router-best-practices", vue_visual)
        # 3. Router 和 React 只命中自身相关 Owner，不把视觉检查泛化到所有前端文件。
        router = route_owners(["src/router/auth.ts"], ["vue-router", "navigation-guard"])
        self.assertIn("vue-router-best-practices", router)
        self.assertNotIn("frontend-ui-visual-rules", router)
        react = route_owners(["src/hooks/useUser.tsx"], ["effect"])
        self.assertIn("vercel-react-best-practices", react)
        self.assertIn("frontend-component-rules", react)
        self.assertNotIn("frontend-ui-visual-rules", react)

    def test_encoding_and_micro_business_require_evidence(self) -> None:
        """Windows 编码与微业务 Owner 必须具备明确证据，普通配置和业务路径不得误触发。

        [参数] 无
        [返回] 无；断言失败时由 unittest 抛出异常
        最近修改时间：2026-07-25 19:05:00；覆盖条件 Owner 的正负路由边界。
        """

        # 1. 普通 UTF-8 文档或 YAML 不触发 Windows 编码，编码信号、脚本和 charset 文件才触发。
        self.assertNotIn("windows-encoding-rules", route_owners(["README.md", "config/app.yaml"]))
        self.assertIn("windows-encoding-rules", route_owners(["scripts/build.ps1"]))
        self.assertIn("windows-encoding-rules", route_owners([".gitattributes"]))
        self.assertIn("windows-encoding-rules", route_owners(["config/app.yaml"], ["bom"]))
        # 2. 普通业务代码不触发微业务架构；跨业务 import 或 contract 通信才触发。
        self.assertNotIn("micro-business-architecture-rules", route_owners(["src/business/user/service.py"]))
        micro = route_owners(["src/business/user/contracts/user_contract.py"], ["contract-communication"])
        self.assertIn("micro-business-architecture-rules", micro)

    def test_source_map_reads_references_and_rejects_unsafe_entries(self) -> None:
        """source map 必须读取 reference 最新内容，并把不安全声明降级为 limited。

        [参数] 无
        [返回] 无；断言失败时由 unittest 抛出异常
        最近修改时间：2026-08-01 00:00:00；改用共享来源映射并覆盖不安全声明。
        """

        # 1. 构造最小 Owner 与 source map，确认 reference 改动会改变摘要。
        owner_dir = self.root / "code-readability-rules"
        ref_dir = owner_dir / "references"
        ref_dir.mkdir(parents=True)
        (owner_dir / "SKILL.md").write_text("---\nname: code-readability-rules\n---\nbody\n", encoding="utf-8")
        ref_file = ref_dir / "readability-general.md"
        ref_file.write_text("first reference\n", encoding="utf-8")
        map_dir = self.root / "code-style-consistency-rules" / "references"
        map_dir.mkdir(parents=True)

        def write_map(source_paths: list[str] | None = None, source_globs: list[str] | None = None) -> None:
            """写入供当前测试使用的最小共享来源映射。

            [参数] source_paths：显式来源路径；source_globs：通配来源路径。
            [返回] 无。
            最近修改时间：2026-08-01 00:00:00；将 fixture 写入共享来源映射目录。
            """

            # 1. 仅构造单一 Owner 的临时来源映射，隔离无关规则。
            payload = {
                "version": 1,
                "owners": {
                    "code-readability-rules": {
                        "source_paths": source_paths if source_paths is not None else [
                            "code-readability-rules/SKILL.md",
                            "code-readability-rules/references/readability-general.md",
                        ],
                        "source_globs": source_globs if source_globs is not None else [],
                        "consumption": "static-only",
                    }
                },
            }
            (map_dir / "static-owner-source-map.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

        write_map()
        first = read_owner_sources(self.root, ["code-readability-rules"], "src/example.py")
        ref_file.write_text("second reference\n", encoding="utf-8")
        second = read_owner_sources(self.root, ["code-readability-rules"], "src/example.py")
        first_ref = next(item for item in first["sources"] if item["rule_source"].endswith("readability-general.md"))
        second_ref = next(item for item in second["sources"] if item["rule_source"].endswith("readability-general.md"))
        self.assertNotEqual(first_ref["content_digest"], second_ref["content_digest"])

        # 2. 不安全或不可解析来源不得被猜测使用，只能生成 limited finding。
        invalid_cases = [
            (["C:/outside/SKILL.md"], []),
            (["../code-readability-rules/SKILL.md"], []),
            (["naming-rules/SKILL.md"], []),
            (["code-readability-rules/missing.md"], []),
            ([], ["code-readability-rules/references/no-match-*.md"]),
        ]
        for source_paths, source_globs in invalid_cases:
            write_map(source_paths=source_paths, source_globs=source_globs)
            limited = read_owner_sources(self.root, ["code-readability-rules"], "src/example.py")
            self.assertEqual(len(limited["limited_findings"]), 1)
            self.assertEqual(limited["limited_findings"][0]["owner_skill"], "unclassified")
            self.assertEqual(limited["limited_findings"][0]["status"], "limited")

    def test_owner_sources_refresh_and_missing_owner_is_limited(self) -> None:
        """Owner 更新后读取最新摘要，缺失或名称不一致时只生成 limited finding。

        [参数] 无
        [返回] 无；断言失败时由 unittest 抛出异常
        最近修改时间：2026-07-25 08:00:00；覆盖 Owner 最新读取和安全降级。
        """

        # 1. 创建临时 Owner，修改内容后确认下一次读取摘要变化。
        owner_dir = self.root / "code-readability-rules"
        owner_dir.mkdir()
        skill_file = owner_dir / "SKILL.md"
        skill_file.write_text("---\nname: code-readability-rules\n---\nfirst\n", encoding="utf-8")
        first = read_owner_sources(self.root, ["code-readability-rules"], "src/example.py")
        skill_file.write_text("---\nname: code-readability-rules\n---\nsecond\n", encoding="utf-8")
        second = read_owner_sources(self.root, ["code-readability-rules"], "src/example.py")
        self.assertNotEqual(first["sources"][0]["content_digest"], second["sources"][0]["content_digest"])
        # 2. 缺失、未知名称和文件声明名称不一致都只能形成 unclassified/limited。
        mismatched_dir = self.root / "naming-rules"
        mismatched_dir.mkdir()
        (mismatched_dir / "SKILL.md").write_text("---\nname: other-rules\n---\n", encoding="utf-8")
        limited = read_owner_sources(self.root, ["api-endpoint-rules", "renamed-owner"], "src/example.py")
        mismatched = read_owner_sources(self.root, ["naming-rules"], "src/example.py")
        limited["limited_findings"].extend(mismatched["limited_findings"])
        self.assertEqual(len(limited["limited_findings"]), 3)
        self.assertTrue(all(item["owner_skill"] == "unclassified" for item in limited["limited_findings"]))
        self.assertTrue(all(item["status"] == "limited" for item in limited["limited_findings"]))

    def test_state_is_utf8_json_without_original_checkout_path(self) -> None:
        """状态文件可读取且只保存 checkout hash，不保存原始路径。

        [参数] 无
        [返回] 无；断言失败时由 unittest 抛出异常
        最近修改时间：2026-07-25 08:00:00；覆盖 UTF-8 和路径脱敏边界。
        """

        # 1. 启动状态并验证 JSON 编码和 checkout 路径脱敏。
        result = start(self.checkout, True, "监控代码", self.root / "state")
        path = Path(result["state_path"])
        payload = json.loads(path.read_text(encoding="utf-8"))
        self.assertIn("checkout_hash", payload)
        self.assertNotIn(str(self.checkout), path.read_text(encoding="utf-8"))
        self.assertEqual(path, state_path(self.checkout, self.root / "state"))

    def test_finding_rule_source_must_be_relative(self) -> None:
        """finding 的规则来源不得写入绝对路径或路径穿越。

        [参数] 无
        [返回] 无；断言失败时由 unittest 抛出异常
        最近修改时间：2026-07-25 08:00:00；覆盖规则来源脱敏边界。
        """

        # 1. 分别拒绝 Windows 盘符路径和路径穿越来源。
        start(self.checkout, True, "监控代码", self.root / "state")
        finding = {
            "owner_skill": "code-readability-rules",
            "rule_source": str(self.root / "owner" / "SKILL.md"),
            "file": "src/example.py",
            "evidence": "safe",
            "severity": "P1",
            "fingerprint": "fp-003",
            "status": "open",
        }
        with self.assertRaises(ValueError):
            record_scan(self.checkout, "diff-005", ["src/example.py"], [finding], self.root / "state")
        finding["rule_source"] = "../owner/SKILL.md"
        with self.assertRaises(ValueError):
            record_scan(self.checkout, "diff-006", ["src/example.py"], [finding], self.root / "state")

    def test_relative_paths_and_limited_pair_are_enforced(self) -> None:
        """扫描文件、finding 文件和 unclassified/limited 必须满足双向安全约束。

        [参数] 无
        [返回] 无；断言失败时由 unittest 抛出异常
        最近修改时间：2026-07-25 08:00:00；补齐路径穿越和受限 finding 负向覆盖。
        """

        # 1. 路径穿越不能进入扫描摘要，unclassified 也不能伪装成普通 open finding。
        start(self.checkout, True, "监控代码", self.root / "state")
        with self.assertRaises(ValueError):
            record_scan(self.checkout, "diff-007", ["../outside.py"], [], self.root / "state")
        finding = {
            "owner_skill": "unclassified",
            "rule_source": "missing-owner",
            "file": "../outside.py",
            "evidence": "Owner source unavailable",
            "severity": "P1",
            "fingerprint": "fp-004",
            "status": "limited",
        }
        with self.assertRaises(ValueError):
            record_scan(self.checkout, "diff-008", ["src/example.py"], [finding], self.root / "state")
        finding["file"] = "src/example.py"
        finding["status"] = "open"
        finding["fingerprint"] = finding_fingerprint(
            finding["owner_skill"], finding["rule_source"], finding["file"], finding["evidence"]
        )
        with self.assertRaises(ValueError):
            record_scan(self.checkout, "diff-009", ["src/example.py"], [finding], self.root / "state")
        # 2. 已分类 finding 的指纹必须与四个稳定字段完全一致。
        finding["owner_skill"] = "code-readability-rules"
        finding["rule_source"] = "code-readability-rules/SKILL.md"
        finding["status"] = "open"
        finding["fingerprint"] = "forged-fingerprint"
        with self.assertRaises(ValueError):
            record_scan(self.checkout, "diff-010", ["src/example.py"], [finding], self.root / "state")


if __name__ == "__main__":
    unittest.main()
