"""全仓库资产健康回归：LF 强制文件不得含 CRLF，agents 配置必须可解析且无控制字符。

`.gitattributes` 把 `*.sh` / `*.bash` / `*.yml` / `*.yaml` 固定为 `eol=lf`，但工作树仍会被
Windows 侧工具以 CRLF 重新写回：CRLF 的 `.sh` 在 WSL / Linux 下会因行尾 `\\r` 执行失败，
CRLF 的 agents 配置则让 git 归一化内容与工作树字节长期不一致，排查时极易误判为"无改动"。
2026-08-12 一次性修掉 8 份 `agents/openai.yaml` 后，把这类检查固化成常驻断言。

控制字符断言的由来：`knowledge-flow/agents/openai.yaml` 曾把 `\\audit_...` 当 Python 转义写入，
`audit` 首字母被吞成 BEL（`\\x07`），整份配置语义静默漂移。

与 `test/knowledge-flow/path_prefix_contract_test.py` 中的资产健康检查是范围互补：
那里守 knowledge-flow 域内的定点文件，这里守全仓库面上的同类回归。
"""

from __future__ import annotations

import unittest
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[2]
# `.gitattributes` 明确声明 eol=lf 的后缀，必须与该文件保持同步。
LF_ENFORCED_SUFFIXES = (".sh", ".bash", ".yaml", ".yml")
# 排除目录：doc 为历史归档只读（其中测试证据 fixture 的字节内容已被 MD5/行数写进验证文档，
# 按 `.gitattributes` 约定不得因空白检查改写），其余为版本控制与缓存产物。
EXCLUDED_DIRS = (
    ".git",
    ".codegraph",
    ".codex",
    "doc",
    "__pycache__",
    "node_modules",
)
CRLF = b"\x0d\x0a"


def is_active(path: Path) -> bool:
    """判断文件是否参与当前执行口径。

    [参数] path：待判定的文件绝对路径。
    [返回] bool：True 表示纳入健康检查。
    最近修改时间：2026-08-12；改动原因：新增全仓库行尾与控制字符回归。
    """
    return not any(part in EXCLUDED_DIRS for part in path.relative_to(ROOT).parts)


def iter_lf_enforced_files() -> list[Path]:
    """收集 `.gitattributes` 要求 LF 的活动文件。

    [参数] 无。
    [返回] list[Path]：按路径排序的待检查文件列表。
    最近修改时间：2026-08-12；改动原因：新增全仓库行尾与控制字符回归。
    """
    files = [
        path
        for path in ROOT.rglob("*")
        if path.is_file() and path.suffix in LF_ENFORCED_SUFFIXES and is_active(path)
    ]
    return sorted(files)


def iter_agents_configs() -> list[Path]:
    """收集全仓库 skill 的 `agents/` 配置。

    覆盖 `.system/` 下的系统 skill：其中部分目录被 `.gitignore` 忽略、不进版本库，
    但仍是本机真实生效的执行口径，行尾与解析健康同样要守。

    [参数] 无。
    [返回] list[Path]：按路径排序的 agents 配置列表。
    最近修改时间：2026-08-12；改动原因：新增全仓库行尾与控制字符回归。
    """
    files = [
        path
        for path in ROOT.rglob("agents/*")
        if path.is_file() and path.suffix in (".yaml", ".yml") and is_active(path)
    ]
    return sorted(files)


class LfEnforcedAssetTest(unittest.TestCase):
    """行尾组：`.gitattributes` 规定 LF 的资产在工作树也必须是 LF。"""

    def test_lf_enforced_files_have_no_crlf(self) -> None:
        """`.sh` / `.bash` / `.yaml` / `.yml` 不得出现 CRLF。

        [参数] 无。
        [返回] None：断言失败时抛出 AssertionError。
        最近修改时间：2026-08-12；改动原因：新增全仓库行尾与控制字符回归。
        """
        offenders = []
        for path in iter_lf_enforced_files():
            count = path.read_bytes().count(CRLF)
            if count:
                offenders.append(f"{path.relative_to(ROOT).as_posix()} -> CRLF x{count}")
        self.assertEqual(offenders, [], f"应为 LF 的文件出现 CRLF：{offenders}")

    def test_scan_scope_is_not_empty(self) -> None:
        """扫描范围不得为空，避免排除规则写错后测试静默通过。

        [参数] 无。
        [返回] None：断言失败时抛出 AssertionError。
        最近修改时间：2026-08-12；改动原因：新增全仓库行尾与控制字符回归。
        """
        self.assertGreater(len(iter_lf_enforced_files()), 0, "LF 强制文件扫描范围为空")
        self.assertGreater(len(iter_agents_configs()), 0, "agents 配置扫描范围为空")


class AgentsConfigHealthTest(unittest.TestCase):
    """agents 配置组：全仓库 agents 配置必须可解析且不含控制字符。"""

    def test_agents_configs_are_parseable(self) -> None:
        """每份 agents 配置都必须解析为映射。

        [参数] 无。
        [返回] None：断言失败时抛出 AssertionError。
        最近修改时间：2026-08-12；改动原因：新增全仓库行尾与控制字符回归。
        """
        offenders = []
        for path in iter_agents_configs():
            rel = path.relative_to(ROOT).as_posix()
            # 1. 先确认能解析，控制字符与坏缩进都会在这一步暴露。
            try:
                data = yaml.safe_load(path.read_text(encoding="utf-8"))
            except yaml.YAMLError as exc:
                offenders.append(f"{rel} -> 解析失败：{exc.__class__.__name__}")
                continue
            # 2. 再确认顶层是映射，空文件与裸标量同样会让下游读取口径落空。
            if not isinstance(data, dict):
                offenders.append(f"{rel} -> 顶层不是映射：{type(data).__name__}")
        self.assertEqual(offenders, [], f"agents 配置不可用：{offenders}")

    def test_agents_configs_have_no_control_characters(self) -> None:
        """agents 配置不得含除换行与制表符以外的控制字符。

        [参数] 无。
        [返回] None：断言失败时抛出 AssertionError。
        最近修改时间：2026-08-12；改动原因：新增全仓库行尾与控制字符回归。
        """
        offenders = []
        for path in iter_agents_configs():
            text = path.read_text(encoding="utf-8")
            bad = {repr(ch) for ch in text if ord(ch) < 32 and ch not in "\n\t"}
            if bad:
                offenders.append(f"{path.relative_to(ROOT).as_posix()} -> {sorted(bad)}")
        self.assertEqual(offenders, [], f"agents 配置含控制字符：{offenders}")


if __name__ == "__main__":
    unittest.main()
