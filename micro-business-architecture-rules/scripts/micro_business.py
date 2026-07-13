#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""微业务架构脚手架与隔离校验脚本。

子命令:
  scaffold <业务名>  新建一个业务目录包骨架并套用统一 README 模板(幂等)
  check              校验业务包之间是否存在非法横向 import(跨业务直连)

退出码: 0 表示通过, 非 0 表示存在违规或执行错误。
仅使用 Python 标准库, 无第三方依赖; 所有文件读写显式 UTF-8。
最近修改时间: 2026-07-13
"""
import argparse
import re
import sys
from pathlib import Path

# 脚本自身位置, 用于定位同仓库的 templates 目录
SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent
README_TEMPLATE = SKILL_DIR / "templates" / "business-readme-template.md"

# 业务包内默认子目录(分层落点沿用 package-structure-rules, 此处仅建目录占位)
DEFAULT_SUBDIRS = ["handler", "logic", "model", "store"]

# 匹配 import 路径中的业务包路径段: .../business/<名字>
BUSINESS_IMPORT_RE = re.compile(r'(?:^|/)business/([A-Za-z0-9_]+)')


def log(message):
    """向控制台输出过程日志(带前缀便于观察执行进度)。

    [参数] message: 日志正文
    [返回] 无
    最近修改时间: 2026-07-13
    """
    print(f"[micro-business] {message}")


def list_business_packages(business_root):
    """列出业务根目录下的业务包名集合。

    [参数] business_root: 业务根目录 Path(如 <root>/internal/business)
    [返回] 业务包名列表(一级子目录名, 不含 README.md 等文件)
    最近修改时间: 2026-07-13
    """
    if not business_root.is_dir():
        return []
    # 只取一级子目录作为业务包, 忽略 README.md 等散文件
    names = [child.name for child in sorted(business_root.iterdir()) if child.is_dir()]
    return names


def extract_import_paths(go_source):
    """从 Go 源码文本中提取所有 import 路径字符串。

    [参数] go_source: 单个 .go 文件的文本内容
    [返回] import 路径字符串列表(引号内路径)
    最近修改时间: 2026-07-13
    """
    paths = []
    # 1. 块状 import ( ... ), 提取块内所有引号路径
    for block in re.findall(r'import\s*\(([\s\S]*?)\)', go_source):
        paths.extend(re.findall(r'"([^"]+)"', block))
    # 2. 单行 import "x" 或 import alias "x"
    for path in re.findall(r'import\s+(?:[A-Za-z0-9_.]+\s+)?"([^"]+)"', go_source):
        paths.append(path)
    return paths


def check_isolation(root, business_dir):
    """校验业务包之间是否存在非法横向 import。

    [参数] root: 项目根目录 Path
    [参数] business_dir: 业务根相对路径(默认 internal/business)
    [返回] 违规记录列表, 每项为 (业务包, 文件, 违规import, 被直连业务)
    最近修改时间: 2026-07-13
    """
    business_root = root / business_dir
    packages = list_business_packages(business_root)
    if not packages:
        log(f"未发现业务包目录: {business_root}")
        return []
    package_set = set(packages)
    log(f"发现业务包: {', '.join(packages)}")
    violations = []
    # 逐个业务包扫描其 .go 文件的 import
    for pkg in packages:
        pkg_dir = business_root / pkg
        for go_file in sorted(pkg_dir.rglob("*.go")):
            text = go_file.read_text(encoding="utf-8")
            for imp in extract_import_paths(text):
                match = BUSINESS_IMPORT_RE.search(imp)
                if not match:
                    continue
                other = match.group(1)
                # 只有指向"另一个真实存在的业务包"才算跨业务直连违规
                if other in package_set and other != pkg:
                    violations.append((pkg, str(go_file), imp, other))
    return violations


def render_readme(business_name):
    """读取统一 README 模板并填入业务名。

    [参数] business_name: 业务包名
    [返回] 渲染后的 README 文本; 模板缺失时返回最小骨架
    最近修改时间: 2026-07-13
    """
    if README_TEMPLATE.is_file():
        text = README_TEMPLATE.read_text(encoding="utf-8")
        # 只替换业务名占位, 其余占位符保留供人工填空
        return text.replace("<业务名>", business_name)
    # 模板缺失时的最小兜底骨架
    return f"# {business_name} 业务包\n\n<按 micro-business md 规范补全>\n"


def cmd_check(args):
    """check 子命令: 校验业务包间是否存在非法横向 import。

    [参数] args: argparse 解析结果(含 root, business_dir)
    [返回] 退出码 0(通过) / 1(存在违规)
    最近修改时间: 2026-07-13
    """
    root = Path(args.root).resolve()
    log(f"开始隔离校验: root={root}, business_dir={args.business_dir}")
    violations = check_isolation(root, args.business_dir)
    if violations:
        log(f"发现 {len(violations)} 处跨业务非法 import(禁止 business 直连 business):")
        for pkg, go_file, imp, other in violations:
            log(f'  [违规] 业务包 {pkg} -> {other}: {go_file} 中 import "{imp}"')
        log("修复: 跨业务调用改走 contract/<被调用业务> 接口(见 references/isolation-and-communication.md)")
        return 1
    log("隔离校验通过: 未发现跨业务非法 import")
    return 0


def cmd_scaffold(args):
    """scaffold 子命令: 新建业务包骨架并套用 README 模板(幂等)。

    [参数] args: argparse 解析结果(含 name, root, business_dir, with_contract)
    [返回] 退出码 0
    最近修改时间: 2026-07-13
    """
    root = Path(args.root).resolve()
    business_root = root / args.business_dir
    pkg_dir = business_root / args.name
    log(f"开始创建业务包骨架: {pkg_dir}")
    created = []
    # 1. 创建业务包及子目录(已存在则跳过, 保证幂等)
    for sub in DEFAULT_SUBDIRS:
        sub_dir = pkg_dir / sub
        if not sub_dir.exists():
            sub_dir.mkdir(parents=True, exist_ok=True)
            created.append(str(sub_dir))
    # 2. 写业务包 README(已存在则不覆盖, 保证幂等且不破坏已有内容)
    readme = pkg_dir / "README.md"
    if not readme.exists():
        pkg_dir.mkdir(parents=True, exist_ok=True)
        readme.write_text(render_readme(args.name), encoding="utf-8")
        created.append(str(readme))
    # 3. 按需创建公共接口包目录
    if args.with_contract:
        contract_dir = root / "internal" / "contract" / args.name
        if not contract_dir.exists():
            contract_dir.mkdir(parents=True, exist_ok=True)
            created.append(str(contract_dir))
    if created:
        log(f"已创建 {len(created)} 项:")
        for item in created:
            log(f"  + {item}")
    else:
        log("目标已存在, 未新增任何内容(幂等)")
    log(f"提示: 记得在 {business_root / 'README.md'} 的业务包索引中登记 {args.name}")
    return 0


# 微业务标记: 写入目标项目规则文件的受管章节标题与正文
MARKER_SECTION_HEADER = "微业务架构约束"
MARKER_SECTION_BODY = """本项目采用微业务(伪微服务)架构, 由 `micro-business-architecture-rules` skill 守护。

- 不同业务放在 `internal/business/<域>/` 下, 各自自包含; 业务包之间禁止直接 import(横向零依赖)。
- 跨业务调用只经公共接口包 `internal/contract/<域>/` 以接口形式通信(依赖倒置)。
- 新业务新开目录包, 旧业务只在自己包内演进, 互不影响。
- 每个业务包必须有统一 README; 全局业务索引在 `internal/business/README.md`, 接口契约清单在 `internal/contract/README.md`。
- 新增业务用 `micro_business.py scaffold <业务名>`, 改动后用 `micro_business.py check` 校验隔离。"""

# 微业务标记: 写入根目录 项目设计.md 的业务索引段标题与正文
DESIGN_SECTION_HEADER = "微业务架构与业务包索引"
DESIGN_SECTION_BODY = """本项目采用微业务架构。业务包索引见 `internal/business/README.md`, 公共接口契约清单见 `internal/contract/README.md`; 架构约束见规则文件的「微业务架构约束」章节。"""


def upsert_section(file_path, header, body):
    """幂等 upsert 一个 `## 章节` 到 Markdown 文件。

    [参数] file_path: 目标 Markdown 文件 Path
    [参数] header: 章节标题(不含 `## ` 前缀)
    [参数] body: 章节正文
    [返回] "created"(新建文件) / "updated"(替换已有章节) / "appended"(追加到文末)
    最近修改时间: 2026-07-13
    规则: 按 `## header` 定位; 已存在则替换该章节正文直到下一个 `## `; 不存在则追加; 保证重复运行不重复堆叠。
    """
    header_line = f"## {header}"
    section = f"{header_line}\n\n{body}\n"
    # 1. 文件不存在: 先确保父目录存在, 再创建最小文件 + 章节
    if not file_path.exists():
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(f"# {file_path.stem}\n\n{section}", encoding="utf-8")
        return "created"
    lines = file_path.read_text(encoding="utf-8").split("\n")
    out = []
    i = 0
    total = len(lines)
    replaced = False
    # 2. 逐行扫描, 命中目标章节标题则用最新正文替换整段
    while i < total:
        if lines[i].strip() == header_line:
            out.append(header_line)
            out.append("")
            out.extend(body.split("\n"))
            out.append("")
            i += 1
            # 跳过旧章节正文, 直到下一个 `## ` 或文件末尾
            while i < total and not lines[i].startswith("## "):
                i += 1
            replaced = True
            continue
        out.append(lines[i])
        i += 1
    # 3. 未命中: 追加到文末
    if not replaced:
        while out and out[-1].strip() == "":
            out.pop()
        out.append("")
        out.append(header_line)
        out.append("")
        out.extend(body.split("\n"))
        out.append("")
    file_path.write_text("\n".join(out), encoding="utf-8")
    return "updated" if replaced else "appended"


def cmd_init(args):
    """init 子命令: 幂等写入微业务标记到目标项目规则文件与 项目设计.md。

    [参数] args: argparse 解析结果(含 root)
    [返回] 退出码 0
    最近修改时间: 2026-07-13
    """
    root = Path(args.root).resolve()
    log(f"开始写入微业务标记: root={root}")
    # 1. upsert 规则文件(CLAUDE.md / AGENTS.md)的架构约束章节
    for rule_file in ["CLAUDE.md", "AGENTS.md"]:
        result = upsert_section(root / rule_file, MARKER_SECTION_HEADER, MARKER_SECTION_BODY)
        log(f"  {rule_file}: 微业务架构约束章节 -> {result}")
    # 2. upsert 项目设计.md 的业务索引段
    result = upsert_section(root / "项目设计.md", DESIGN_SECTION_HEADER, DESIGN_SECTION_BODY)
    log(f"  项目设计.md: 微业务架构与业务包索引段 -> {result}")
    log("微业务标记写入完成(幂等, 重复运行不重复堆叠)")
    return 0


def build_parser():
    """构造命令行参数解析器。

    [参数] 无
    [返回] argparse.ArgumentParser 实例
    最近修改时间: 2026-07-13
    """
    parser = argparse.ArgumentParser(
        prog="micro_business",
        description="微业务架构脚手架与隔离校验",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    # scaffold 子命令
    p_scaffold = sub.add_parser("scaffold", help="新建业务包骨架(幂等)")
    p_scaffold.add_argument("name", help="业务包名(ASCII, 如 order)")
    p_scaffold.add_argument("--root", default=".", help="项目根目录(默认当前目录)")
    p_scaffold.add_argument("--business-dir", default="internal/business", help="业务根相对路径")
    p_scaffold.add_argument("--with-contract", action="store_true", help="同时创建 internal/contract/<name> 目录")
    p_scaffold.set_defaults(func=cmd_scaffold)

    # check 子命令
    p_check = sub.add_parser("check", help="校验业务包间是否存在非法横向 import")
    p_check.add_argument("--root", default=".", help="项目根目录(默认当前目录)")
    p_check.add_argument("--business-dir", default="internal/business", help="业务根相对路径")
    p_check.set_defaults(func=cmd_check)

    # init 子命令
    p_init = sub.add_parser("init", help="幂等写入微业务标记到目标项目规则文件")
    p_init.add_argument("--root", default=".", help="项目根目录(默认当前目录)")
    p_init.set_defaults(func=cmd_init)

    return parser


def main(argv=None):
    """脚本入口: 解析参数并分发到对应子命令。

    [参数] argv: 可选参数列表(默认读取 sys.argv)
    [返回] 子命令退出码
    最近修改时间: 2026-07-13
    """
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
