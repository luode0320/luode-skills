# -*- coding: utf-8 -*-
"""知识库端到端生命周期闭环自动化测试（沉淀 -> 挂网 -> 校验 -> 阶梯检索 -> 版本演进 -> 归档退役）。

在完全隔离的沙箱临时知识库中模拟完整人机协同知识沉淀流转：
1. 捕获写入（Capture）：写入全新工程实践笔记；
2. 防孤岛入网（Weave）：挂载入二级领域 MOC，断言孤岛清零；
3. 质量门禁（Gate）：自动化运行 check，确保零违规零死链；
4. 阶梯检索（Retrieve）：验证 L1 摘要索引命中、L2 MOC 推荐路由、L3 原子精准召回；
5. 版本迭代（Iterate）：发布 v2 升级版，建立成对接替链，校验降级合规；
6. 归档退役（Archive）：将旧版归入 90-Archive，验证冷存储流转；
7. 现场回收（Teardown）：沙箱自动销毁。
"""

from __future__ import annotations

import importlib.util
import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
INDEX_SCRIPT = ROOT / "knowledge-flow" / "scripts" / "knowledge_index.py"
AUDIT_SCRIPT = ROOT / "knowledge-flow" / "scripts" / "audit_vault_knowledge.py"


def load_module(name: str, path: Path) -> Any:
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


INDEX = load_module("e2e_index_mod", INDEX_SCRIPT)
AUDIT = load_module("e2e_audit_mod", AUDIT_SCRIPT)


class EndToEndLifecycleSandboxTest(unittest.TestCase):
    """端到端生命周期闭环沙箱测试。"""

    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.sandbox = Path(self._tmp.name)
        self._saved_index_root = INDEX.KB_ROOT
        self._saved_audit_root = AUDIT.KB_ROOT
        INDEX.KB_ROOT = self.sandbox
        INDEX.AUDIT.KB_ROOT = self.sandbox
        AUDIT.KB_ROOT = self.sandbox

        # 初始化沙箱目录骨架
        (self.sandbox / "20-Knowledge" / "工程实践").mkdir(parents=True, exist_ok=True)
        (self.sandbox / "30-MOCs" / "工程实践").mkdir(parents=True, exist_ok=True)
        (self.sandbox / "90-Archive" / "工程实践").mkdir(parents=True, exist_ok=True)

        # 写入根导航 INDEX.md 和二级领域 MOC
        (self.sandbox / "INDEX.md").write_text(
            "---\nid: index\ntype: root\ntitle: 导航Hub\nstatus: active\ncreated: 2026-10-10\nupdated: 2026-10-10\n---\n"
            "# 导航Hub\n\n- [[30-MOCs/工程实践/架构模式与后端治理]]\n",
            encoding="utf-8",
        )
        (self.sandbox / "30-MOCs" / "工程实践" / "架构模式与后端治理.md").write_text(
            "---\nid: moc-arch\ntype: moc\ntitle: 架构模式与后端治理\nstatus: active\ncreated: 2026-10-10\nupdated: 2026-10-10\n---\n"
            "# 架构模式与后端治理\n\n## 实践列表\n",
            encoding="utf-8",
        )

    def tearDown(self) -> None:
        INDEX.KB_ROOT = self._saved_index_root
        INDEX.AUDIT.KB_ROOT = self._saved_audit_root
        AUDIT.KB_ROOT = self._saved_audit_root
        self._tmp.cleanup()

    def test_full_knowledge_lifecycle(self) -> None:
        """完整生命周期流转断言。"""

        # ---------------------------------------------------------
        # 第一阶段：捕获沉淀 (Capture)
        # ---------------------------------------------------------
        v1_path = self.sandbox / "20-Knowledge" / "工程实践" / "eBPF高性能网络排障组件实践.md"
        v1_path.write_text(
            "---\n"
            "id: ebpf-network-tracing-v1\n"
            "type: knowledge\n"
            "title: eBPF高性能网络排障组件实践\n"
            "aliases: [eBPF网络排障, 内核旁路可观测性]\n"
            "tags: [ebpf, observability, network-tracing]\n"
            "topics: [架构设计, 网络排障, 系统可观测性]\n"
            "status: active\n"
            "created: 2026-10-10\n"
            "updated: 2026-10-10\n"
            "---\n\n"
            "# eBPF高性能网络排障组件实践\n\n"
            "基于 TC 与 kprobe 实现零侵入网络时延捕获与丢包排障。\n",
            encoding="utf-8",
        )

        # 此时尚未织入 MOC，巡检应当捕获到 1 篇孤儿笔记
        facts = [AUDIT.collect_note_facts(v1_path)]
        orphans = AUDIT.find_orphans(facts)
        self.assertIn("20-Knowledge/工程实践/eBPF高性能网络排障组件实践.md", orphans, "未挂网笔记应被判为孤儿")

        # ---------------------------------------------------------
        # 第二阶段：织网挂入 (Weave into MOC)
        # ---------------------------------------------------------
        moc_file = self.sandbox / "30-MOCs" / "工程实践" / "架构模式与后端治理.md"
        moc_text = moc_file.read_text(encoding="utf-8")
        moc_file.write_text(
            moc_text + "- [[20-Knowledge/工程实践/eBPF高性能网络排障组件实践]]：零侵入时延与丢包排障\n",
            encoding="utf-8",
        )

        # 挂网后再测孤儿，孤岛状态应立刻解除
        all_facts = [
            AUDIT.collect_note_facts(v1_path),
            AUDIT.collect_note_facts(moc_file),
            AUDIT.collect_note_facts(self.sandbox / "INDEX.md"),
        ]
        self.assertEqual(len(AUDIT.find_orphans(all_facts)), 0, "挂入 MOC 后全库孤岛数应为 0")

        # ---------------------------------------------------------
        # 第三阶段：质量门禁自检 (Gate Self-check)
        # ---------------------------------------------------------
        fm_report = INDEX.check_frontmatter()
        self.assertTrue(fm_report["ok"], "Frontmatter 与白名单应全部通过")
        dead_report = INDEX.check_dead_links()
        self.assertTrue(dead_report["ok"], "双链应解析成功，零死链")
        super_report = INDEX.check_supersession()
        self.assertTrue(super_report["ok"], "版本接替无悬空违规")

        # ---------------------------------------------------------
        # 第四阶段：构建索引与阶梯式检索 (Build & Hierarchical Retrieval)
        # ---------------------------------------------------------
        idx = INDEX.build_index()
        INDEX.write_index(idx)

        # 验证 L1 摘要索引
        summary_path = self.sandbox / INDEX.SUMMARY_INDEX_NAME
        self.assertTrue(summary_path.exists())
        summary_data = json.loads(summary_path.read_text(encoding="utf-8"))
        summary_titles = [n["title"] for n in summary_data["notes"]]
        self.assertIn("eBPF高性能网络排障组件实践", summary_titles)

        # 验证 L2 推荐 MOC 与 L3 原子召回
        hits = INDEX.query_index(idx, "eBPF网络排障")
        self.assertEqual(len(hits), 1)
        self.assertEqual(hits[0]["path"], "20-Knowledge/工程实践/eBPF高性能网络排障组件实践.md")
        self.assertEqual(hits[0]["recommended_moc"], "30-MOCs/工程实践/架构模式与后端治理.md", "应准确推荐后端治理 MOC")

        # ---------------------------------------------------------
        # 第五阶段：版本演进与取代 (Iterate & Supersede)
        # ---------------------------------------------------------
        # 发布 v2 版本
        v2_path = self.sandbox / "20-Knowledge" / "工程实践" / "eBPF高性能网络排障组件实践-v2.md"
        v2_path.write_text(
            "---\n"
            "id: ebpf-network-tracing-v2\n"
            "type: knowledge\n"
            "title: eBPF高性能网络排障组件实践 v2\n"
            "aliases: [eBPF网络排障v2]\n"
            "tags: [ebpf, observability, ringbuffer]\n"
            "topics: [架构设计, 网络排障]\n"
            "status: active\n"
            "supersedes: [\"[[20-Knowledge/工程实践/eBPF高性能网络排障组件实践]]\"]\n"
            "created: 2026-10-10\n"
            "updated: 2026-10-10\n"
            "---\n\n"
            "# eBPF高性能网络排障组件实践 v2\n\n"
            "重构使用 BPF RingBuffer 替代 perf buffer，极大降低事件丢包率。\n",
            encoding="utf-8",
        )

        # 将 v1 降级为 superseded 并写入成对接替指针
        v1_path.write_text(
            "---\n"
            "id: ebpf-network-tracing-v1\n"
            "type: knowledge\n"
            "title: eBPF高性能网络排障组件实践\n"
            "aliases: [eBPF网络排障]\n"
            "tags: [ebpf, observability]\n"
            "topics: [架构设计, 网络排障]\n"
            "status: superseded\n"
            "superseded_by: [\"[[20-Knowledge/工程实践/eBPF高性能网络排障组件实践-v2]]\"]\n"
            "created: 2026-10-10\n"
            "updated: 2026-10-10\n"
            "---\n\n"
            "# 旧版已接替\n",
            encoding="utf-8",
        )

        # 更新 MOC 挂载 v2
        moc_file.write_text(
            moc_file.read_text(encoding="utf-8") + "- [[20-Knowledge/工程实践/eBPF高性能网络排障组件实践-v2]]\n",
            encoding="utf-8",
        )

        # 门禁自检接替关系
        super_check = INDEX.check_supersession()
        self.assertTrue(super_check["ok"], "v1 与 v2 双向接替应当完全闭环并通过")

        # 重新加载索引并查询
        idx2 = INDEX.load_index(auto_rebuild=True)
        hits2 = INDEX.query_index(idx2, "eBPF")
        # 应召回 v1, v2 以及引用了它们的 MOC 笔记
        self.assertGreaterEqual(len(hits2), 2)
        # v2 为 active，v1 为 superseded
        hit_v2 = next(h for h in hits2 if "v2" in h["path"])
        hit_v1 = next(h for h in hits2 if "v2" not in h["path"] and h["theme"] == "工程实践")
        self.assertEqual(hit_v2["status"], "active")
        self.assertEqual(hit_v1["status"], "superseded")
        self.assertIn("'[[20-Knowledge/工程实践/eBPF高性能网络排障组件实践-v2]]'", str(hit_v1["superseded_by"]))

        # ---------------------------------------------------------
        # 第六阶段：归档退役 (Archive)
        # ---------------------------------------------------------
        archive_v1 = self.sandbox / "90-Archive" / "工程实践" / "eBPF高性能网络排障组件实践.md"
        shutil.move(str(v1_path), str(archive_v1))
        # 调整 v1 状态为 archived 并解除双向严格接替校验
        archive_v1.write_text(
            archive_v1.read_text(encoding="utf-8").replace("status: superseded", "status: archived"),
            encoding="utf-8",
        )

        # 归档后全库重新构建索引
        idx_archived = INDEX.load_index(auto_rebuild=True)
        self.assertEqual(idx_archived["notes_count"], 4)  # INDEX, MOC, v2, v1(archived)


if __name__ == "__main__":
    unittest.main()
