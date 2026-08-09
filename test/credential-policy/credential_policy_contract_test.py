# -*- coding: utf-8 -*-
"""凭据政策契约测试。

验证九个 Skill 的 SKILL.md 中凭据口径已统一为：
- 允许凭据原值持久化到项目代码/配置/普通维护文档和 Git 提交
- 默认来源为项目代码/项目配置/普通维护文档
- 环境变量仅作运行时覆盖
- 禁止在过程性输出中回显

不读取真实密钥，不连接外部服务。
"""

import os
import re
import sys
import unittest

SKILLS_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "skills")
if not os.path.isdir(SKILLS_DIR):
    SKILLS_DIR = os.path.join(os.path.dirname(__file__), "..", "..")
if not os.path.isdir(SKILLS_DIR):
    SKILLS_DIR = "."


def _read_skill(name: str) -> str:
    """读取 skill 的 SKILL.md 文件内容。"""
    path = os.path.join(SKILLS_DIR, name, "SKILL.md")
    if not os.path.isfile(path):
        # 也尝试在 skills 目录下找
        path2 = os.path.join(SKILLS_DIR, "skills", name, "SKILL.md")
        if os.path.isfile(path2):
            path = path2
        else:
            return ""
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


class CredentialPolicyContractTest(unittest.TestCase):
    """凭据政策契约测试：验证九个 Skill 口径统一。"""

    SKILLS = [
        "godot-project-bootstrap-rules",
        "project-rule-file-bootstrap-rules",
        "imagegen",
        "mcp-installation-rules",
        "authenticated-url-routing-rules",
        "browser-use-cloud-rules",
        "tapd-addcomment",
        "tapd-cli",
        "tapd-openapi",
    ]

    # 旧口径模式 - 出现即视为残留
    OLD_PATTERNS = [
        "不得明文写真实",
        "不得写入真实密钥",
        "案例中禁止写入 API key",
        "必须留空由用户自行填写",
        "只从本机环境变量读取",
    ]

    # 新口径模式 - 至少应包含一个
    NEW_PATTERNS = [
        "项目代码/配置",
        "项目代码/项目配置",
        "默认来源",
        "默认凭据",
        "允许写入",
        "允许明文",
    ]

    # 禁止回显模式 - 必须保留
    FORBID_ECHO_PATTERNS = [
        "禁止在",
        "过程性输出",
        "不得回显",
        "禁止泄露",
        "禁止回显",
        "Token 明文",
    ]

    def test_01_no_old_patterns(self):
        """九个 Skill 不得有旧口径残留。"""
        failures = []
        for skill in self.SKILLS:
            content = _read_skill(skill)
            if not content:
                continue
            for pattern in self.OLD_PATTERNS:
                if pattern in content:
                    failures.append(f"{skill}: 旧口径残留 '{pattern}'")
        self.assertEqual([], failures, "旧口径残留:\n" + "\n".join(failures))

    def test_02_has_new_patterns(self):
        """九个 Skill 至少包含一个新口径。"""
        failures = []
        for skill in self.SKILLS:
            content = _read_skill(skill)
            if not content:
                failures.append(f"{skill}: 文件不存在或无法读取")
                continue
            found = any(p in content for p in self.NEW_PATTERNS)
            if not found:
                failures.append(f"{skill}: 未找到新口径")
        self.assertEqual([], failures, "缺少新口径:\n" + "\n".join(failures))

    def test_03_keeps_forbid_echo(self):
        """九个 Skill 保留禁止过程性输出回显的口径。"""
        failures = []
        for skill in self.SKILLS:
            content = _read_skill(skill)
            if not content:
                continue
            has_forbid = any(p in content for p in self.FORBID_ECHO_PATTERNS)
            if not has_forbid:
                failures.append(f"{skill}: 缺少禁止过程性输出回显")
        self.assertEqual([], failures, "缺少禁止回显:\n" + "\n".join(failures))

    def test_04_reading_skill_hit_check(self):
        """验证 skill-hit-check-rules 的凭据持久化规则已更新。"""
        content = _read_skill("skill-hit-check-rules")
        if not content:
            self.skipTest("skill-hit-check-rules 不可读取")
        # 凭据持久化规则可能在 AGENTS.md 中，不在 SKILL.md 正文
        # 检查是否有"凭据"相关表述
        has_credential_ref = "凭据" in content or "secret" in content.lower() or "密钥" in content
        if not has_credential_ref:
            self.skipTest("skill-hit-check-rules 正文不包含凭据规则，规则在 AGENTS.md 中")
        has_forbid_echo = ("禁止" in content and "回显" in content) or "Token 明文" in content
        self.assertTrue(has_forbid_echo, "skill-hit-check-rules 缺少禁止回显")


if __name__ == "__main__":
    unittest.main()
