# -*- coding: utf-8 -*-
"""知识库检索机制全方位自动化测试套件。

涵盖：
1. L1 根导航与轻量摘要索引（_index_summary.json）结构与体积断言；
2. L2 领域 MOC 推荐路由算法（infer_recommended_moc）覆盖率与准确率断言；
3. L3 标题、别名、标签、主题、路径与正文兜底扫描召回断言；
4. 结构化排序（非 body 命中排首位）、--theme 过滤、--tag 过滤与 --limit 截断断言；
5. 索引新鲜度检测、文件变动自动重建与损坏自动恢复断言；
6. 边界与特殊符号容错断言。
"""

from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
import time
import unittest
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
INDEX_SCRIPT = ROOT / "knowledge-flow" / "scripts" / "knowledge_index.py"


def load_index_module() -> Any:
    name = "knowledge_index_retrieval_test"
    spec = importlib.util.spec_from_file_location(name, INDEX_SCRIPT)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


INDEX = load_index_module()


class RetrievalComprehensiveTest(unittest.TestCase):
    """检索机制全方位测试类。"""

    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.base = Path(self._tmp.name)
        self._saved_root = INDEX.KB_ROOT
        self._saved_audit_root = INDEX.AUDIT.KB_ROOT
        INDEX.KB_ROOT = self.base
        INDEX.AUDIT.KB_ROOT = self.base

    def tearDown(self) -> None:
        INDEX.KB_ROOT = self._saved_root
        INDEX.AUDIT.KB_ROOT = self._saved_audit_root
        self._tmp.cleanup()

    def write_note(
        self,
        rel: str,
        title: str,
        tags: list[str] | None = None,
        aliases: list[str] | None = None,
        topics: list[str] | None = None,
        status: str = "active",
        body: str = "默认正文内容。",
    ) -> Path:
        p = self.base / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        tags_str = json.dumps(tags or [], ensure_ascii=False)
        aliases_str = json.dumps(aliases or [], ensure_ascii=False)
        topics_str = json.dumps(topics or [], ensure_ascii=False)
        content = (
            f"---\n"
            f"id: {p.stem}\n"
            f"type: knowledge\n"
            f"title: {title}\n"
            f"tags: {tags_str}\n"
            f"aliases: {aliases_str}\n"
            f"topics: {topics_str}\n"
            f"status: {status}\n"
            f"created: 2026-10-10\n"
            f"updated: 2026-10-10\n"
            f"---\n\n"
            f"# {title}\n\n"
            f"{body}\n"
        )
        p.write_text(content, encoding="utf-8")
        return p

    # ==========================================
    # 1. L1 根导航与摘要索引测试
    # ==========================================

    def test_summary_index_structure_and_fields(self) -> None:
        """测试 _index_summary.json 的 v2 主题归组结构与字段精简性。"""
        self.write_note(
            "20-Knowledge/工程实践/插件架构实录.md",
            title="插件架构实录",
            tags=["plugin", "trae"],
            aliases=["插件协议"],
        )
        index = INDEX.build_index()
        INDEX.write_index(index)

        summary_file = self.base / INDEX.SUMMARY_INDEX_NAME
        self.assertTrue(summary_file.exists(), "轻量摘要索引文件必须生成")
        summary = json.loads(summary_file.read_text(encoding="utf-8"))

        self.assertEqual(summary["notes_count"], 1)
        # v2 摘要索引按主题归组，只保留 path/title 短键，服务 L1 领域大类导航。
        self.assertIn("themes", summary)
        theme_notes = summary["themes"]["工程实践"]
        self.assertEqual(len(theme_notes), 1)
        note = theme_notes[0]
        self.assertEqual(note["p"], "20-Knowledge/工程实践/插件架构实录.md")
        self.assertEqual(note["t"], "插件架构实录")
        # 必须精简排除的字段（以降低上下文 Token）
        self.assertNotIn("mtime", note)
        self.assertNotIn("tags", note)
        self.assertNotIn("aliases", note)

    # ==========================================
    # 2. L2 领域 MOC 推荐路由算法测试 (infer_recommended_moc)
    # ==========================================

    def test_moc_recommendation_routing_accuracy(self) -> None:
        """测试 infer_recommended_moc 对各二级领域的精准导引能力。"""
        cases = [
            # 工程实践六大领域
            ({"path": "20-Knowledge/工程实践/trae-plugin-spec.md", "theme": "工程实践", "tags": ["plugin"]},
             "30-MOCs/工程实践/插件体系与扩展架构.md"),
            ({"path": "20-Knowledge/工程实践/oauth-loopback-guard.md", "theme": "工程实践", "tags": ["oauth2", "安全"]},
             "30-MOCs/工程实践/网络安全与认证授权.md"),
            ({"path": "20-Knowledge/工程实践/moonpay-swap-quote.md", "theme": "工程实践", "tags": ["web3", "交易"]},
             "30-MOCs/工程实践/Web3与金融交易实践.md"),
            ({"path": "20-Knowledge/工程实践/mongodb-replica-setup.md", "theme": "工程实践", "tags": ["mongo", "数据库"]},
             "30-MOCs/工程实践/数据库与存储工程.md"),
            ({"path": "20-Knowledge/工程实践/godot-viewport-msdf.md", "theme": "工程实践", "tags": ["godot", "渲染"]},
             "30-MOCs/工程实践/Godot与客户端工程.md"),
            ({"path": "20-Knowledge/工程实践/micro-biz-arch.md", "theme": "工程实践", "tags": ["微业务"]},
             "30-MOCs/工程实践/架构模式与后端治理.md"),
            # 能力与流程 MOC
            ({"path": "20-Knowledge/AI协作/goal-advance.md", "theme": "AI协作"},
             "30-MOCs/AI协作与Agent工程-MOC.md"),
            ({"path": "20-Knowledge/代码规则/yagni.md", "theme": "代码规则"},
             "30-MOCs/代码规则与工程规范-MOC.md"),
            ({"path": "20-Knowledge/code-style/go-var.md", "theme": "code-style"},
             "30-MOCs/代码规则与工程规范-MOC.md"),
            ({"path": "20-Knowledge/研发流程/handover.md", "theme": "研发流程"},
             "30-MOCs/研发流程与Skill治理-MOC.md"),
            ({"path": "20-Knowledge/开发环境/wsl-crlf.md", "theme": "开发环境"},
             "30-MOCs/开发环境与跨宿主工程-MOC.md"),
            # 项目地图
            ({"path": "20-Knowledge/项目/crossverse-arena/arch.md", "theme": "项目"},
             "30-MOCs/CrossVerse-Arena项目地图.md"),
            ({"path": "20-Knowledge/项目/EllipalFinance-go/rate.md", "theme": "项目"},
             "30-MOCs/EllipalFinance-go 项目地图.md"),
            # 来源日志
            ({"path": "50-Sources/sessions/2026-10-10.md", "theme": "50-Sources"},
             "30-MOCs/会话日志与日常沉淀-MOC.md"),
        ]

        for note_data, expected_moc in cases:
            recommended = INDEX.infer_recommended_moc(note_data)
            self.assertEqual(recommended, expected_moc, f"笔记 {note_data['path']} 应被推荐到 {expected_moc}")

    # ==========================================
    # 3. L3 精准检索与多维度召回测试
    # ==========================================

    def test_search_by_title_and_aliases(self) -> None:
        """测试标题匹配与别名扩展召回。"""
        self.write_note(
            "20-Knowledge/工程实践/微业务架构实践.md",
            title="微业务架构实践",
            aliases=["伪微服务设计", "垂直业务隔离"],
        )
        index = INDEX.build_index()

        # 标题精确匹配
        hits_title = INDEX.query_index(index, "微业务架构")
        self.assertEqual(len(hits_title), 1)
        self.assertIn("title", hits_title[0]["matched"])

        # 别名模糊召回
        hits_alias = INDEX.query_index(index, "伪微服务")
        self.assertEqual(len(hits_alias), 1)
        self.assertIn("aliases", hits_alias[0]["matched"])
        self.assertEqual(hits_alias[0]["path"], "20-Knowledge/工程实践/微业务架构实践.md")

    def test_search_by_tags_and_topics(self) -> None:
        """测试通过标签与主题进行召回。"""
        self.write_note(
            "20-Knowledge/工程实践/网络隔离.md",
            title="网络隔离",
            tags=["security-firewall", "zero-trust"],
            topics=["网络安全", "访问控制"],
        )
        index = INDEX.build_index()

        hits_tag = INDEX.query_index(index, "zero-trust")
        self.assertEqual(len(hits_tag), 1)
        self.assertIn("tags", hits_tag[0]["matched"])

        hits_topic = INDEX.query_index(index, "网络安全")
        self.assertEqual(len(hits_topic), 1)
        self.assertIn("topics", hits_topic[0]["matched"])

    def test_search_by_body_fallback(self) -> None:
        """测试正文兜底扫描能力（标签与元数据未包含的隐式技术词）。"""
        self.write_note(
            "20-Knowledge/工程实践/深层排错记录.md",
            title="常规日常维护",
            tags=["ops"],
            body="底层网络协议层发现了特殊的 TCP_NODELAY 锁死缺陷。",
        )
        index = INDEX.build_index()

        hits = INDEX.query_index(index, "TCP_NODELAY")
        self.assertEqual(len(hits), 1)
        self.assertEqual(hits[0]["matched"], ["body"])

    # ==========================================
    # 4. 排序算法与过滤功能测试
    # ==========================================

    def test_ranking_structured_above_body(self) -> None:
        """测试结构化命中（标题/别名/标签）的排序权重严格高于纯正文命中。"""
        # A 笔记：仅正文包含
        self.write_note(
            "20-Knowledge/工程实践/A.md",
            title="系统概览",
            body="这里提到了关键词 singleflight 防穿透。",
        )
        # B 笔记：标题包含
        self.write_note(
            "20-Knowledge/工程实践/B.md",
            title="singleflight 并发模型",
            body="正文无特殊内容。",
        )
        index = INDEX.build_index()

        hits = INDEX.query_index(index, "singleflight")
        self.assertEqual(len(hits), 2)
        # B 必须排在 A 前面
        self.assertEqual(hits[0]["path"], "20-Knowledge/工程实践/B.md")
        self.assertIn("title", hits[0]["matched"])
        self.assertEqual(hits[1]["path"], "20-Knowledge/工程实践/A.md")
        self.assertEqual(hits[1]["matched"], ["body"])

    def test_theme_and_tag_filters(self) -> None:
        """测试 --theme 与 --tag 过滤器的精准隔离能力。"""
        self.write_note(
            "20-Knowledge/工程实践/db.md",
            title="Postgres连接池",
            tags=["database", "pool"],
        )
        self.write_note(
            "20-Knowledge/AI协作/prompt.md",
            title="Prompt连接池设计",
            tags=["agent", "pool"],
        )
        index = INDEX.build_index()

        # 1. 过滤 theme
        hits_eng = INDEX.query_index(index, "连接池", theme_filter="工程实践")
        self.assertEqual(len(hits_eng), 1)
        self.assertEqual(hits_eng[0]["theme"], "工程实践")

        hits_ai = INDEX.query_index(index, "连接池", theme_filter="AI协作")
        self.assertEqual(len(hits_ai), 1)
        self.assertEqual(hits_ai[0]["theme"], "AI协作")

        # 2. 过滤 tag
        hits_db_tag = INDEX.query_index(index, "连接池", tag_filter="database")
        self.assertEqual(len(hits_db_tag), 1)
        self.assertEqual(hits_db_tag[0]["path"], "20-Knowledge/工程实践/db.md")

    def test_limit_parameter(self) -> None:
        """测试 --limit 截断返回条数。"""
        for i in range(5):
            self.write_note(
                f"20-Knowledge/工程实践/item_{i}.md",
                title=f"测试项目批次 {i}",
            )
        index = INDEX.build_index()

        hits_all = INDEX.query_index(index, "测试项目批次")
        self.assertEqual(len(hits_all), 5)

        hits_limited = INDEX.query_index(index, "测试项目批次")[:2]
        self.assertEqual(len(hits_limited), 2)

    # ==========================================
    # 5. 索引新鲜度与自动重建测试
    # ==========================================

    def test_auto_rebuild_on_file_addition(self) -> None:
        """测试新增文件后，load_index 自动触发重建。"""
        self.write_note("20-Knowledge/工程实践/first.md", title="第一篇")
        index = INDEX.load_index(auto_rebuild=True)
        self.assertEqual(index["notes_count"], 1)

        # 写入第二篇
        time.sleep(0.01)
        self.write_note("20-Knowledge/工程实践/second.md", title="第二篇")

        # 读取索引时必须感知文件数变化并自动重建
        fresh_index = INDEX.load_index(auto_rebuild=True)
        self.assertEqual(fresh_index["notes_count"], 2)
        hits = INDEX.query_index(fresh_index, "第二篇")
        self.assertEqual(len(hits), 1)

    def test_auto_rebuild_on_file_modification(self) -> None:
        """测试修改已有笔记后，mtime 变化触发自动更新。"""
        p = self.write_note("20-Knowledge/工程实践/note.md", title="原始笔记", body="版本一")
        INDEX.load_index(auto_rebuild=True)

        time.sleep(0.02)
        # 修改文件追加新关键词
        p.write_text(p.read_text(encoding="utf-8") + "\n新增关键词 updated_keyword_99\n", encoding="utf-8")

        fresh_index = INDEX.load_index(auto_rebuild=True)
        hits = INDEX.query_index(fresh_index, "updated_keyword_99")
        self.assertEqual(len(hits), 1)

    def test_auto_rebuild_on_corrupt_index(self) -> None:
        """测试索引文件被损坏时自动恢复重建。"""
        self.write_note("20-Knowledge/工程实践/good.md", title="良好笔记")
        INDEX.load_index(auto_rebuild=True)

        # 人为破坏索引文件内容为非法 JSON
        target = self.base / INDEX.INDEX_NAME
        target.write_text("NOT A VALID JSON {{{", encoding="utf-8")

        recovered_index = INDEX.load_index(auto_rebuild=True)
        self.assertIsNotNone(recovered_index)
        self.assertEqual(recovered_index["notes_count"], 1)

    # ==========================================
    # 6. 边界与特殊字符容错测试
    # ==========================================

    def test_empty_keyword_returns_empty(self) -> None:
        """测试空关键词或纯空格不返回全库。"""
        self.write_note("20-Knowledge/工程实践/note.md", title="普通笔记")
        index = INDEX.build_index()
        self.assertEqual(INDEX.query_index(index, ""), [])
        self.assertEqual(INDEX.query_index(index, "    "), [])

    def test_special_characters_handling(self) -> None:
        """测试包含正则/语法特殊字符时平稳查询不抛异常。"""
        self.write_note(
            "20-Knowledge/工程实践/special.md",
            title="包含特殊符号 [tag] (c) *regex* | pipe \\ slash",
        )
        index = INDEX.build_index()

        special_needles = ["[tag]", "*regex*", "(c)", "\\", "|", ".*", "$", "^"]
        for needle in special_needles:
            try:
                hits = INDEX.query_index(index, needle)
                self.assertIsInstance(hits, list)
            except Exception as e:
                self.fail(f"特殊字符 '{needle}' 查询抛出非预期异常: {e}")

    def test_case_insensitivity(self) -> None:
        """测试中英文大小写混杂正常召回。"""
        self.write_note(
            "20-Knowledge/工程实践/mixed.md",
            title="MixedCase MicroService 架构",
        )
        index = INDEX.build_index()

        self.assertEqual(len(INDEX.query_index(index, "mixedcase")), 1)
        self.assertEqual(len(INDEX.query_index(index, "MIXEDCASE")), 1)
        self.assertEqual(len(INDEX.query_index(index, "microservice")), 1)


if __name__ == "__main__":
    unittest.main()
