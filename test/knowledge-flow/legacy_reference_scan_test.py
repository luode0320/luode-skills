"""扫描活动 skill 资产，确保 Obsidian / bridge 时代的失效引用不再残留。

知识库承载体已迁到 `D:\\谷歌云盘\\知识库\\`，CLI 桥接脚本已删除。
任何活动规则若仍指向 Obsidian vault、`obsidian_cli_bridge.py` 或 `obsidian-knowledge-flow/`，
执行方按其口径操作会直接失败，因此把这类残留固化成常驻断言。
"""

from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
# 已失效的标识：出现在活动资产里即视为口径未收口。
FORBIDDEN_TOKENS = (
    "obsidian_data",
    "obsidian_cli_bridge",
    "obsidian_cli_windows",
    "obsidian-knowledge-flow",
    "distill_vault",
)
# 已删除的脚本：不得再被任何活动资产引用。
DELETED_SCRIPTS = (
    "knowledge-flow/scripts/obsidian_cli_bridge.py",
    "knowledge-flow/scripts/obsidian_cli_windows.ps1",
    "knowledge-flow/scripts/distill_vault.py",
)
# 排除目录：doc 为历史归档只读，vercel 的 AGENTS.md 是历史拼接污染，均不参与活动口径。
EXCLUDED_DIRS = (
    ".git",
    ".codegraph",
    ".codex",
    ".system",
    "doc",
    "skill-dictionary",
    "vercel-react-best-practices",
    "__pycache__",
)
SCAN_SUFFIXES = (".md", ".py", ".yaml", ".yml", ".sh", ".ps1")
# 允许保留 Obsidian 字样的文件：它们记录的是迁移历史脉络或来源事实，不是当前执行口径。
HISTORY_ALLOWLIST = (
    "PROJECT_MEMORY.md",
    "PROJECT_HISTORY.md",
    "PROJECT_CURRENT.md",
    "PROJECT_STYLE.md",
    "README.md",
    "字典.md",
    "编码skill.md",
    "test/knowledge-flow/legacy_reference_scan_test.py",
    "test/knowledge-flow/path_prefix_contract_test.py",
)


def iter_active_files() -> list[Path]:
    """收集参与当前执行口径的活动文件。

    [参数] 无。
    [返回] list[Path]：待扫描文件路径列表。
    最近修改时间: 2026-08-12 新增遗留引用扫描测试。
    """
    files = []
    for path in ROOT.rglob("*"):
        if not path.is_file() or path.suffix not in SCAN_SUFFIXES:
            continue
        parts = path.relative_to(ROOT).parts
        if any(part in EXCLUDED_DIRS for part in parts):
            continue
        files.append(path)
    return files


class LegacyReferenceScanTest(unittest.TestCase):
    """遗留引用组：活动资产不得指向已废除的 Obsidian / bridge 链路。"""

    def test_no_forbidden_token_in_active_assets(self) -> None:
        """活动资产不得出现已失效的 Obsidian / bridge 标识。

        [参数] 无。
        [返回] None：断言失败时抛出 AssertionError。
        最近修改时间: 2026-08-12 新增遗留引用扫描测试。
        """
        offenders = []
        for path in iter_active_files():
            rel = path.relative_to(ROOT).as_posix()
            if rel in HISTORY_ALLOWLIST:
                continue
            lowered = path.read_text(encoding="utf-8").lower()
            for token in FORBIDDEN_TOKENS:
                if token in lowered:
                    offenders.append(f"{rel} -> {token}")
        self.assertEqual(offenders, [], f"活动资产残留失效引用：{offenders}")

    def test_deleted_scripts_do_not_exist(self) -> None:
        """bridge 相关脚本必须确实已从仓库移除。

        [参数] 无。
        [返回] None：断言失败时抛出 AssertionError。
        最近修改时间: 2026-08-12 新增遗留引用扫描测试。
        """
        for rel in DELETED_SCRIPTS:
            self.assertFalse((ROOT / rel).exists(), f"应已删除的脚本仍存在：{rel}")

    def test_skill_directory_is_renamed(self) -> None:
        """skill 目录必须已从 obsidian-knowledge-flow 改名为 knowledge-flow。

        [参数] 无。
        [返回] None：断言失败时抛出 AssertionError。
        最近修改时间: 2026-08-12 新增遗留引用扫描测试。
        """
        self.assertTrue((ROOT / "knowledge-flow" / "SKILL.md").exists())
        self.assertFalse((ROOT / "obsidian-knowledge-flow").exists())

    def test_knowledge_flow_assets_have_no_bare_obsidian_word(self) -> None:
        """knowledge-flow 自身资产不得残留任何 Obsidian 字样。

        裸 `obsidian` 曾以 `storage: obsidian` / `obsidian_path:` 形式藏在渲染脚本里，
        与 case-template 的字段契约不一致，因此对本 skill 目录做更严格的全词扫描。

        [参数] 无。
        [返回] None：断言失败时抛出 AssertionError。
        最近修改时间: 2026-08-12 补强扫描粒度，覆盖 frontmatter 字段名残留。
        """
        offenders = []
        for path in (ROOT / "knowledge-flow").rglob("*"):
            if not path.is_file() or path.suffix not in SCAN_SUFFIXES:
                continue
            if "__pycache__" in path.parts:
                continue
            if "obsidian" in path.read_text(encoding="utf-8").lower():
                offenders.append(path.relative_to(ROOT).as_posix())
        self.assertEqual(offenders, [], f"knowledge-flow 资产残留 Obsidian 字样：{offenders}")

    def test_execution_case_field_contract_matches_template(self) -> None:
        """渲染脚本产出的 frontmatter 字段必须与案例模板契约一致。

        [参数] 无。
        [返回] None：断言失败时抛出 AssertionError。
        最近修改时间: 2026-08-12 新增字段契约一致性断言。
        """
        script = (ROOT / "knowledge-flow" / "scripts" / "render_execution_case.py").read_text(encoding="utf-8")
        template = (
            ROOT / "execution-failure-learning-rules" / "references" / "case-template.md"
        ).read_text(encoding="utf-8")
        for field in ("storage: knowledge-base", "note_path"):
            self.assertIn(field, script, f"渲染脚本缺少契约字段：{field}")
            self.assertIn(field, template, f"案例模板缺少契约字段：{field}")
        self.assertNotIn("obsidian_path", script)
        self.assertNotIn("obsidian_path", template)


class AssetHealthTest(unittest.TestCase):
    """资产健康组：knowledge-flow 的配置文件必须可解析且不含控制字符。"""

    def test_agents_config_is_parseable(self) -> None:
        """agents 配置必须是可解析的 YAML。

        迁移时曾因把 `\\a` 当转义写入而产生 BEL 控制字符（`audit` 被吞成 `\\x07udit`），
        导致整份配置无法解析，因此固化成常驻断言。

        [参数] 无。
        [返回] None：断言失败时抛出 AssertionError。
        最近修改时间: 2026-08-12 新增 agents 配置可解析断言。
        """
        import yaml

        path = ROOT / "knowledge-flow" / "agents" / "openai.yaml"
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        self.assertIsInstance(data, dict, "agents 配置必须解析为映射")

    def test_skill_assets_have_no_control_characters(self) -> None:
        """knowledge-flow 资产不得含除换行与制表符以外的控制字符。

        [参数] 无。
        [返回] None：断言失败时抛出 AssertionError。
        最近修改时间: 2026-08-12 新增控制字符断言。
        """
        offenders = []
        for path in (ROOT / "knowledge-flow").rglob("*"):
            if not path.is_file() or path.suffix not in SCAN_SUFFIXES:
                continue
            if "__pycache__" in path.parts:
                continue
            text = path.read_text(encoding="utf-8")
            bad = {repr(ch) for ch in text if ord(ch) < 32 and ch not in "\n\t"}
            if bad:
                offenders.append(f"{path.relative_to(ROOT).as_posix()} -> {sorted(bad)}")
        self.assertEqual(offenders, [], f"资产含控制字符：{offenders}")

    def test_lf_only_assets_keep_lf(self) -> None:
        """`.gitattributes` 规定 LF 的资产在工作树也必须是 LF。

        `.sh` 与 `.yaml` 若被写成 CRLF，在 WSL / Linux 下会因行尾 `\\r` 执行或解析失败。

        [参数] 无。
        [返回] None：断言失败时抛出 AssertionError。
        最近修改时间: 2026-08-12 新增行尾断言。
        """
        targets = [
            ROOT / "knowledge-flow" / "agents" / "openai.yaml",
            ROOT / "project-rule-file-bootstrap-rules" / "scripts" / "bootstrap_agents.sh",
        ]
        offenders = []
        for path in targets:
            if path.read_bytes().count(b"\x0d\x0a"):
                offenders.append(path.relative_to(ROOT).as_posix())
        self.assertEqual(offenders, [], f"应为 LF 的文件出现 CRLF：{offenders}")


class StatusFieldRenameTest(unittest.TestCase):
    """状态字段组：每轮可见的状态字段必须已改名为知识库。"""

    def test_rule_files_use_knowledge_field(self) -> None:
        """AGENTS.md 与 CLAUDE.md 必须使用 知识库: 状态字段。

        [参数] 无。
        [返回] None：断言失败时抛出 AssertionError。
        最近修改时间: 2026-08-12 新增状态字段断言。
        """
        for name in ("AGENTS.md", "CLAUDE.md"):
            text = (ROOT / name).read_text(encoding="utf-8")
            self.assertIn("`知识库:<检索/沉淀/不适用/阻断>`", text, f"{name} 缺少新状态字段")
            self.assertNotIn("Obsidian:", text, f"{name} 残留旧状态字段")

    def test_rule_files_and_bootstrap_template_match(self) -> None:
        """自举模板必须与规则文件逐字一致，否则下次自举会写回旧文案。

        [参数] 无。
        [返回] None：断言失败时抛出 AssertionError。
        最近修改时间: 2026-08-12 新增自举模板一致性断言。
        """
        agents = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
        claude = (ROOT / "CLAUDE.md").read_text(encoding="utf-8")
        self.assertEqual(agents, claude, "AGENTS.md 与 CLAUDE.md 内容已漂移")

        bootstrap = (ROOT / "project-rule-file-bootstrap-rules" / "scripts" / "bootstrap_agents.sh").read_text(
            encoding="utf-8"
        )
        # 取受管章节标题所在的整段，逐行核对模板与规则文件一致
        marker = "### 知识库知识流选择性默认触发（强制）"
        self.assertIn(marker, agents, "规则文件缺少受管章节标题")
        self.assertIn(marker, bootstrap, "自举模板缺少受管章节标题")
        agents_block = agents.split(marker, 1)[1].split("\n##", 1)[0].strip()
        bootstrap_block = bootstrap.split(marker, 1)[1].split("\nEOF", 1)[0].strip()
        self.assertEqual(agents_block, bootstrap_block, "自举模板与规则文件受管章节不一致")


if __name__ == "__main__":
    unittest.main()
