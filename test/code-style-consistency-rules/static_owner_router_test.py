"""共享静态 Owner 路由的本地契约测试。"""

from __future__ import annotations

import json
from pathlib import Path
import sys
import tempfile
import unittest


SCRIPTS_DIR = Path(__file__).resolve().parents[2] / "code-style-consistency-rules" / "scripts"
REPO_ROOT = Path(__file__).resolve().parents[2]
SOURCE_MAP_RELATIVE = Path("code-style-consistency-rules") / "references" / "static-owner-source-map.json"
sys.path.insert(0, str(SCRIPTS_DIR))

from static_owner_router import (  # noqa: E402
    BASE_OWNER_NAMES,
    NON_RULE_FILE_NAMES,
    OWNER_NAMES,
    REVIEW_STEPS,
    OwnerSourceMapError,
    iter_rule_reference_files,
    load_owner_source_map,
    owner_source_map_path,
    owner_source_paths,
    render_review_pipeline,
    route_owners,
    route_review_pipeline,
)


def _build_temp_repo(document: dict) -> tempfile.TemporaryDirectory:
    """在临时仓库根写入来源映射，供加载期负向用例使用。

    [参数] document：要写入的来源映射文档。
    [返回] 持有临时目录生命周期的 `TemporaryDirectory` 对象。
    最近修改时间：2026-09-11 00:00:00；为加载断言提供隔离的失败用例夹具。
    """

    # 1. 按真实目录形态落盘，保证 owner_source_map_path 能解析到目标文件。
    holder = tempfile.TemporaryDirectory()
    target = Path(holder.name) / SOURCE_MAP_RELATIVE
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(document, ensure_ascii=False, indent=2), encoding="utf-8")
    return holder


def _build_minimal_repo(extra_files: dict[str, list[str]] | None = None) -> tempfile.TemporaryDirectory:
    """生成声明完整的最小仓库，供来源映射覆盖率用例使用。

    [参数] extra_files：额外落盘但不登记的 owner -> 相对该 Owner 目录的路径列表。
    [返回] 持有临时目录生命周期的 `TemporaryDirectory` 对象。
    最近修改时间：2026-09-11 00:00:00；为覆盖率断言提供可控制缺失项的真实目录夹具。
    """

    # 1. 每个 Owner 都落 SKILL.md 并完成登记，保证基础加载契约先成立。
    holder = tempfile.TemporaryDirectory()
    root = Path(holder.name)
    owners = []
    for owner in sorted(OWNER_NAMES):
        (root / owner).mkdir(parents=True, exist_ok=True)
        (root / owner / "SKILL.md").write_text("# stub\n", encoding="utf-8")
        owners.append(
            {
                "owner": owner,
                "sites": [
                    {
                        "source_paths": [f"{owner}/SKILL.md"],
                        "source_globs": [],
                        "consumption": "static-only",
                    }
                ],
            }
        )

    # 2. 额外文件只落盘不登记，用于制造覆盖率缺口或豁免样本。
    for owner, names in (extra_files or {}).items():
        for name in names:
            target = root / owner / name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text("# stub\n", encoding="utf-8")

    target = root / SOURCE_MAP_RELATIVE
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(
        json.dumps({"version": 2, "owners": owners}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return holder


class StaticOwnerRouterTests(unittest.TestCase):
    """验证共享 Owner 路由的顺序、条件和路径边界。"""

    def test_empty_changes_have_no_owner(self) -> None:
        """验证空变更不会产生静态 Owner。

        [参数] 无
        [返回] 无；断言失败时由 unittest 抛出异常。
        最近修改时间：2026-08-01 00:00:00；覆盖共享路由的空输入边界。
        """

        # 1. 空变更不能触发基础或条件 Owner。
        self.assertEqual(route_owners([]), [])

    def test_base_owner_order_is_stable(self) -> None:
        """验证基础 Owner 的顺序稳定且不重复。

        [参数] 无
        [返回] 无；断言失败时由 unittest 抛出异常。
        最近修改时间：2026-08-01 00:00:00；覆盖共享路由的基础结果契约。
        """

        # 1. 普通代码文件必须先得到固定基础 Owner 序列。
        owners = route_owners(["src/service/user.py"])
        self.assertEqual(owners[: len(BASE_OWNER_NAMES)], list(BASE_OWNER_NAMES))
        self.assertEqual(len(owners), len(set(owners)))

    def test_specialist_routing_matches_existing_monitor_semantics(self) -> None:
        """验证共享路由保留监控场景的专项 Owner 语义。

        [参数] 无
        [返回] 无；断言失败时由 unittest 抛出异常。
        最近修改时间：2026-08-01 00:00:00；覆盖数据库、Go、React 和测试资产路由。
        """

        # 1. 专项路径和信号必须附加对应 Owner 并保留既有先后关系。
        owners = route_owners(["db/migrations/001_user_schema.sql"], ["database-query"])
        self.assertLess(owners.index("database-schema-rules"), owners.index("database-query-rules"))
        self.assertIn("golang-patterns", route_owners(["cmd/app/main.go"]))
        self.assertIn("vercel-react-best-practices", route_owners(["src/App.tsx"]))
        self.assertIn("test-program-rules", route_owners(["tests/fixtures/user_stub.py"]))

    def test_frontend_signals_do_not_overroute(self) -> None:
        """验证前端语义信号不会过度路由无关 Owner。

        [参数] 无
        [返回] 无；断言失败时由 unittest 抛出异常。
        最近修改时间：2026-08-01 00:00:00；覆盖组件、视觉和路由信号的负向边界。
        """

        # 1. 组件与视觉信号各自只引入对应前端 Owner。
        computed = route_owners(["src/views/User.vue"], ["computed"])
        self.assertIn("vue-best-practices", computed)
        self.assertIn("frontend-component-rules", computed)
        self.assertNotIn("frontend-ui-visual-rules", computed)
        visual = route_owners(["src/views/User.vue"], ["aria", "css"])
        self.assertIn("frontend-ui-visual-rules", visual)
        self.assertNotIn("vue-router-best-practices", visual)

    def test_path_tokens_and_encoding_boundaries(self) -> None:
        """验证带空格路径、后缀和编码信号的边界。

        [参数] 无
        [返回] 无；断言失败时由 unittest 抛出异常。
        最近修改时间：2026-08-01 00:00:00；覆盖路径 token 与编码条件路由。
        """

        # 1. 文件名 token 必须独立匹配，不能由普通文本误触发语言 Owner。
        owners = route_owners(["tests with spaces/fixtures/user stub.py", "src with spaces/App.tsx"])
        self.assertIn("test-program-rules", owners)
        self.assertIn("vercel-react-best-practices", owners)
        self.assertNotIn("golang-patterns", route_owners(["docs/draft.go notes/readme.txt"]))
        self.assertIn("windows-encoding-rules", route_owners(["scripts/build.ps1"]))
        self.assertIn("windows-encoding-rules", route_owners(["config/app.yaml"], ["bom"]))

    def test_owner_source_map_path_is_shared_and_absolute(self) -> None:
        """验证来源映射由共享路由返回绝对路径。

        [参数] 无
        [返回] 无；断言失败时由 unittest 抛出异常。
        最近修改时间：2026-08-01 00:00:00；覆盖唯一来源映射的归属路径。
        """

        # 1. 消费者只能通过共享入口获得风格 Owner 的来源映射。
        path = owner_source_map_path(".")
        self.assertTrue(path.is_absolute())
        self.assertEqual(path.name, "static-owner-source-map.json")
        self.assertEqual(path.parent.name, "references")
        self.assertEqual(path.parent.parent.name, "code-style-consistency-rules")

    def test_all_returned_owners_are_declared(self) -> None:
        """验证每个路由结果都在 Owner 清单中声明。

        [参数] 无
        [返回] 无；断言失败时由 unittest 抛出异常。
        最近修改时间：2026-08-01 00:00:00；防止共享路由返回未注册的 Owner。
        """

        # 1. 对接口和前端路由样本校验结果集合属于声明全集。
        for files, signals in ((["src/api/user_controller.py"], ()), (["src/router/auth.ts"], ("vue-router",))):
            self.assertTrue(set(route_owners(files, signals)).issubset(OWNER_NAMES))


    def test_source_map_has_no_duplicate_owner_and_matches_router(self) -> None:
        """验证来源映射无重复 Owner 且与路由声明一致。

        [参数] 无
        [返回] 无；断言失败时由 unittest 抛出异常。
        最近修改时间：2026-09-11 00:00:00；覆盖 v1 重复 key 静默覆盖缺陷的回归防线。
        """

        # 1. 必须是 v2 数组形态，同一 Owner 名不得重复出现。
        text = (REPO_ROOT / SOURCE_MAP_RELATIVE).read_text(encoding="utf-8")
        document = json.loads(text)
        self.assertEqual(document["version"], 2)
        names = [item["owner"] for item in document["owners"]]
        self.assertEqual(len(names), len(set(names)))
        self.assertEqual(set(names), set(OWNER_NAMES))

        # 2. 文本层分组数必须与解析层分组数一致，防止结构退回会被覆盖的形态。
        site_total = sum(len(item["sites"]) for item in document["owners"])
        self.assertEqual(text.count('"source_paths"'), site_total)
        self.assertGreater(site_total, len(names))

    def test_source_map_paths_are_scoped_and_exist(self) -> None:
        """验证来源路径限定在所属 Owner 目录且真实存在。

        [参数] 无
        [返回] 无；断言失败时由 unittest 抛出异常。
        最近修改时间：2026-09-11 00:00:00；覆盖来源映射的路径合法性契约。
        """

        # 1. 加载器已内置校验，这里再独立核对作用域与文件存在性。
        mapping = load_owner_source_map(REPO_ROOT)
        for owner, entry in mapping.items():
            self.assertTrue(entry["sites"])
            self.assertTrue(entry["source_paths"])
            for source in entry["source_paths"]:
                self.assertTrue(source.startswith(f"{owner}/"))
                self.assertTrue((REPO_ROOT / source).is_file())

    def test_owner_source_paths_is_scoped_and_validated(self) -> None:
        """验证按 Owner 取来源时保持作用域并拒绝未登记 Owner。

        [参数] 无
        [返回] 无；断言失败时由 unittest 抛出异常。
        最近修改时间：2026-09-11 00:00:00；覆盖消费者取来源的稳定入口。
        """

        # 1. 返回路径必须属于该 Owner，未登记 Owner 必须失败关闭。
        paths = owner_source_paths(REPO_ROOT, "naming-rules")
        self.assertTrue(paths)
        self.assertTrue(all(item.startswith("naming-rules/") for item in paths))
        with self.assertRaises(OwnerSourceMapError):
            owner_source_paths(REPO_ROOT, "not-a-registered-owner")

    def test_loader_rejects_legacy_object_shape(self) -> None:
        """验证 v1 对象形态被加载期拒绝。

        [参数] 无
        [返回] 无；断言失败时由 unittest 抛出异常。
        最近修改时间：2026-09-11 00:00:00；覆盖重复 key 覆盖缺陷的入口防线。
        """

        # 1. v1 用对象 key 承载 Owner，必须直接失败关闭而不是静默接受。
        holder = _build_temp_repo(
            {
                "version": 1,
                "owners": {
                    "naming-rules": {
                        "source_paths": ["naming-rules/SKILL.md"],
                        "source_globs": [],
                        "consumption": "static-only",
                    }
                },
            }
        )
        self.addCleanup(holder.cleanup)
        with self.assertRaisesRegex(OwnerSourceMapError, "version"):
            load_owner_source_map(holder.name)

    def test_loader_rejects_duplicate_owner_declaration(self) -> None:
        """验证同一 Owner 重复声明被拒绝。

        [参数] 无
        [返回] 无；断言失败时由 unittest 抛出异常。
        最近修改时间：2026-09-11 00:00:00；覆盖一对多被压平为重复声明的形态。
        """

        # 1. 同一 Owner 的多个位点必须写进 sites 数组，不能重复声明 Owner。
        site = {
            "source_paths": ["naming-rules/SKILL.md"],
            "source_globs": [],
            "consumption": "static-only",
        }
        holder = _build_temp_repo(
            {
                "version": 2,
                "owners": [
                    {"owner": "naming-rules", "sites": [dict(site)]},
                    {"owner": "naming-rules", "sites": [dict(site)]},
                ],
            }
        )
        self.addCleanup(holder.cleanup)
        with self.assertRaisesRegex(OwnerSourceMapError, "重复"):
            load_owner_source_map(holder.name)

    def test_loader_rejects_missing_and_cross_owner_paths(self) -> None:
        """验证缺失文件与跨 Owner 路径被拒绝。

        [参数] 无
        [返回] 无；断言失败时由 unittest 抛出异常。
        最近修改时间：2026-09-11 00:00:00；覆盖来源映射的路径拒绝条件。
        """

        # 1. 声明不存在的文件必须失败关闭。
        holder = _build_temp_repo(
            {
                "version": 2,
                "owners": [
                    {
                        "owner": "naming-rules",
                        "sites": [
                            {
                                "source_paths": ["naming-rules/not-there.md"],
                                "source_globs": [],
                                "consumption": "static-only",
                            }
                        ],
                    }
                ],
            }
        )
        self.addCleanup(holder.cleanup)
        with self.assertRaisesRegex(OwnerSourceMapError, "不存在"):
            load_owner_source_map(holder.name)

        # 2. 路径跳出所属 Owner 目录必须失败关闭。
        holder = _build_temp_repo(
            {
                "version": 2,
                "owners": [
                    {
                        "owner": "naming-rules",
                        "sites": [
                            {
                                "source_paths": ["comment-rules/SKILL.md"],
                                "source_globs": [],
                                "consumption": "static-only",
                            }
                        ],
                    }
                ],
            }
        )
        self.addCleanup(holder.cleanup)
        with self.assertRaisesRegex(OwnerSourceMapError, "跨 Owner"):
            load_owner_source_map(holder.name)

    def test_review_pipeline_covers_every_registered_owner(self) -> None:
        """验证九步流水线覆盖全部已登记 Owner 且不引用未登记 Owner。

        [参数] 无
        [返回] 无；断言失败时由 unittest 抛出异常。
        最近修改时间：2026-09-11 00:00:00；保证来源映射的加载真正进入编排。
        """

        # 1. 步骤 Owner 集合必须与已登记集合完全一致。
        step_owners = {owner for step in REVIEW_STEPS for owner in step["owners"]}
        self.assertEqual(step_owners, set(OWNER_NAMES))
        self.assertEqual(len({step["step_id"] for step in REVIEW_STEPS}), len(REVIEW_STEPS))

    def test_review_pipeline_projects_routed_owners_with_sources(self) -> None:
        """验证流水线只投影命中步骤并附带真实来源。

        [参数] 无
        [返回] 无；断言失败时由 unittest 抛出异常。
        最近修改时间：2026-09-11 00:00:00；覆盖流水线的步骤投影与来源合并。
        """

        # 1. 命中 Owner 必须是路由结果的子集，来源文件必须存在。
        changed = ["src/service/user.py", "src/components/UserForm.vue", "db/migrations/001.sql"]
        pipeline = route_review_pipeline(changed, repository_root=REPO_ROOT)
        self.assertTrue(pipeline)
        routed = set(route_owners(changed))
        step_ids = [step["step_id"] for step in pipeline]
        self.assertEqual(step_ids, sorted(step_ids))
        self.assertIn("STYLE-01", step_ids)
        for step in pipeline:
            self.assertTrue(set(step["owners"]).issubset(routed))
            self.assertTrue(step["sources"])
            for source in step["sources"]:
                self.assertTrue((REPO_ROOT / source).is_file())

    def test_review_pipeline_is_empty_for_empty_change(self) -> None:
        """验证空变更不产生步骤也不产生渲染内容。

        [参数] 无
        [返回] 无；断言失败时由 unittest 抛出异常。
        最近修改时间：2026-09-11 00:00:00；覆盖流水线空输入边界。
        """

        # 1. 没有改动就不应伪造检查步骤。
        self.assertEqual(route_review_pipeline([], repository_root=REPO_ROOT), [])
        self.assertEqual(render_review_pipeline([]), "")

    def test_review_pipeline_render_is_paste_ready(self) -> None:
        """验证渲染结果包含步骤标题与文档锚点。

        [参数] 无
        [返回] 无；断言失败时由 unittest 抛出异常。
        最近修改时间：2026-09-11 00:00:00；覆盖 6-review 记录的步骤段落产出。
        """

        # 1. 每个步骤都必须在渲染文本里可定位，且锚点指向流水线文档。
        pipeline = route_review_pipeline(["src/service/user.py"], repository_root=REPO_ROOT)
        text = render_review_pipeline(pipeline)
        self.assertIn("## 检查步骤", text)
        for step in pipeline:
            self.assertIn(f"### {step['step_id']} {step['name']}", text)
            self.assertIn(f"references/style-review-pipeline.md#{step['step_id'].lower()}", text)


    def test_source_map_covers_every_rule_file_in_repo(self) -> None:
        """验证仓库内每个规则文件都已在来源映射登记。

        [参数] 无
        [返回] 无；断言失败时由 unittest 抛出异常。
        最近修改时间：2026-09-11 00:00:00；覆盖 6-review 检查落点不缺失的完整不变式。
        """

        # 1. 逐 Owner 比对目录枚举与登记结果，漏登记即代表该规则没有检查落点。
        mapping = load_owner_source_map(REPO_ROOT)
        unregistered = []
        for owner, entry in mapping.items():
            declared = set(entry["source_paths"])
            for path in iter_rule_reference_files(REPO_ROOT, owner):
                if path not in declared:
                    unregistered.append(path)
        self.assertEqual(unregistered, [])

        # 2. 非规则资产必须被枚举口径排除，避免把溯源与吸收记录当成判定依据。
        exempt = iter_rule_reference_files(REPO_ROOT, "api-contract-rules")
        self.assertNotIn("api-contract-rules/references/source-notes.md", exempt)
        self.assertNotIn("api-contract-rules/workbuddy-absorption-map.md", exempt)
        self.assertIn("api-contract-rules/references/endpoint-examples.md", exempt)
        self.assertTrue(NON_RULE_FILE_NAMES)

    def test_coverage_assertion_rejects_unregistered_rule_file(self) -> None:
        """验证未登记的规则文件会让加载失败关闭。

        [参数] 无
        [返回] 无；断言失败时由 unittest 抛出异常。
        最近修改时间：2026-09-11 00:00:00；覆盖漏登记在加载期被拦下的防线。
        """

        # 1. 新增规则文件但不登记，必须在加载期报错而不是静默漏检。
        holder = _build_minimal_repo({"naming-rules": ["references/brand-new-rule.md"]})
        self.addCleanup(holder.cleanup)
        with self.assertRaisesRegex(OwnerSourceMapError, "未在来源映射登记"):
            load_owner_source_map(holder.name)

    def test_coverage_assertion_exempts_non_rule_assets(self) -> None:
        """验证非规则资产不触发覆盖率断言。

        [参数] 无
        [返回] 无；断言失败时由 unittest 抛出异常。
        最近修改时间：2026-09-11 00:00:00；覆盖豁免口径，防止断言误伤溯源与吸收记录。
        """

        # 1. 溯源登记、吸收映射与吸收案例都允许不登记，加载仍须通过。
        holder = _build_minimal_repo(
            {
                "naming-rules": [
                    "references/source-notes.md",
                    "workbuddy-absorption-map.md",
                    "references/case-naming-absorption.md",
                ]
            }
        )
        self.addCleanup(holder.cleanup)
        mapping = load_owner_source_map(holder.name)
        self.assertEqual(set(mapping), set(OWNER_NAMES))


if __name__ == "__main__":
    unittest.main()
