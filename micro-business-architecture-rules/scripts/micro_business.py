#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""微业务架构脚手架与隔离校验脚本。

子命令:
  scaffold <业务名>  新建业务域骨架(域级通用目录 + entity/router/controller/service 各自内嵌 <v?>/ 版本化目录 + init.go)并套用 README 模板(幂等)
  check              校验业务域之间是否存在非法横向 import(跨业务域直连)
  check --detect-new 候选新项目机器判定(无业务域且无标记 / 已有标记 / 有业务域无标记)

退出码: 0 表示通过, 非 0 表示存在违规或执行错误。
仅使用 Python 标准库, 无第三方依赖; 所有文件读写显式 UTF-8。
最近修改时间: 2026-08-18
"""
import argparse
import re
import sys
from pathlib import Path

# Windows 重定向到测试子进程时也必须保持 UTF-8，避免父进程无法稳定解析诊断信息。
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

# 脚本自身位置, 用于定位同仓库的 templates 目录
SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent
README_TEMPLATE = SKILL_DIR / "templates" / "business-readme-template.md"

# 业务域直连源码根(Go 下为 internal/)；域级通用目录跨版本共享，版本化目录各自内嵌 <v?>/
DOMAIN_LEVEL_DIRS = ["api", "base", "constant", "util"]
VERSIONABLE_DIRS = ["entity", "router", "controller", "service"]
DEFAULT_VERSION = "v1"
# 域初始化入口为单文件(Go 落地为 init.go)，不再建立 init/ 目录
INIT_FILENAME = "init.go"

# 匹配 import 路径中的业务域路径段: .../internal/<名字>（Go 源码根直连业务域）
BUSINESS_IMPORT_RE = re.compile(r'(?:^|/)internal/([A-Za-z0-9_]+)')


def log(message):
    """向控制台输出过程日志(带前缀便于观察执行进度)。

    [参数] message: 日志正文
    [返回] 无
    最近修改时间: 2026-07-13
    """
    print(f"[micro-business] {message}")


def list_business_packages(business_root):
    """列出源码根目录下的业务域名集合。

    [参数] business_root: 源码根目录 Path(如 <root>/internal)
    [返回] 业务域名列表(一级子目录名, 不含 README.md 等文件)
    最近修改时间: 2026-08-18 14:41:00 业务域直连源码根，不再经 business 中间层。
    """
    if not business_root.is_dir():
        return []
    # 只取一级子目录作为业务域, 忽略 README.md 等散文件
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
    """校验业务域之间禁止任何直接 import（无 rpc 例外）。

    [参数] root: 项目根目录 Path
    [参数] business_dir: 源码根相对路径(默认 internal，业务域直连其下)
    [返回] 违规记录列表, 每项为 (业务域, 文件, 违规import, 被直连业务域)
    最近修改时间: 2026-08-18 14:41:00 跨域导入改为完全禁止直连，无 rpc 白名单例外。
    """
    source_root = root / business_dir
    packages = list_business_packages(source_root)
    if not packages:
        log(f"未发现业务域目录: {source_root}")
        return []
    package_set = set(packages)
    log(f"发现业务域: {', '.join(packages)}")
    violations = []
    # 逐个业务域扫描其 .go 文件的 import
    for pkg in packages:
        pkg_dir = source_root / pkg
        for go_file in sorted(pkg_dir.rglob("*.go")):
            text = go_file.read_text(encoding="utf-8")
            for imp in extract_import_paths(text):
                match = BUSINESS_IMPORT_RE.search(imp)
                if not match:
                    continue
                other = match.group(1)
                # 业务域之间禁止直连：任何 import 其他业务域的路径均为违规。
                if other in package_set and other != pkg:
                    violations.append((pkg, str(go_file), imp, other))
    return violations


def has_marker(root):
    """判断目标项目是否已写入微业务标记。

    [参数] root: 项目根目录 Path
    [返回] True 当 CLAUDE.md/AGENTS.md 存在「微业务架构约束」章节或 项目设计.md 存在业务域索引段
    最近修改时间: 2026-08-18 供 --detect-new 判定与触发口径保持一致。
    """
    for rule_file in ["CLAUDE.md", "AGENTS.md"]:
        target = root / rule_file
        if target.is_file() and f"## {MARKER_SECTION_HEADER}" in target.read_text(encoding="utf-8"):
            return True
    design = root / "项目设计.md"
    if design.is_file() and f"## {DESIGN_SECTION_HEADER}" in design.read_text(encoding="utf-8"):
        return True
    return False


def detect_new_project(root, business_dir):
    """机器判定当前仓库是否为「候选新项目」。

    [参数] root: 项目根目录 Path
    [参数] business_dir: 源码根相对路径(默认 internal)
    [返回] (判定结果, 业务域列表)；判定结果取值:
        candidate_new  无业务域且无标记(含初始化阶段) -> 建议采用
        guard          已有标记 -> 进入守护模式
        skip           有业务域但无标记 -> 不引导
    最近修改时间: 2026-08-18 补上 trigger-and-marker.md 早已引用但脚本缺失的 --detect-new 机器判定。
    """
    source_root = root / business_dir
    packages = list_business_packages(source_root)
    if has_marker(root):
        return "guard", packages
    if not packages:
        return "candidate_new", packages
    return "skip", packages


def render_readme(business_name):
    """读取统一 README 模板并填入业务名。

    [参数] business_name: 业务域名
    [返回] 渲染后的 README 文本; 模板缺失时返回最小骨架
    最近修改时间: 2026-08-18 业务 README 模板已改为记录版本化目录结构。
    """
    if README_TEMPLATE.is_file():
        text = README_TEMPLATE.read_text(encoding="utf-8")
        # 只替换业务名占位, 其余占位符保留供人工填空
        return text.replace("<业务名>", business_name)
    # 模板缺失时的最小兜底骨架
    return f"# {business_name} 业务域\n\n<按 micro-business md 规范补全>\n"


def cmd_check(args):
    """check 子命令: 校验业务域间是否存在非法横向 import；--detect-new 时改为候选新项目判定。

    [参数] args: argparse 解析结果(含 root, business_dir, detect_new)
    [返回] 退出码 0(通过/判定完成) / 1(存在违规)
    最近修改时间: 2026-08-18 14:41:00 输出业务域禁止直连的确定性修复路径；新增 --detect-new 判定分支。
    """
    root = Path(args.root).resolve()
    if args.detect_new:
        result, packages = detect_new_project(root, args.business_dir)
        log(f"候选新项目判定: root={root}, business_dir={args.business_dir} -> {result}")
        if result == "candidate_new":
            log("结论: 候选新项目(无业务域且无标记, 或处于初始化阶段), 建议先向用户说明微业务架构收益并征得确认")
        elif result == "guard":
            log("结论: 已有微业务标记, 进入守护模式(改动后 check 校验跨域隔离)")
        else:
            log(f"结论: 存在业务域但无标记({', '.join(packages)}), 不引导也不写标记")
        return 0
    log(f"开始隔离校验: root={root}, business_dir={args.business_dir}")
    violations = check_isolation(root, args.business_dir)
    if violations:
        log(f"发现 {len(violations)} 处跨业务域非法 import(业务域之间禁止直连):")
        for pkg, go_file, imp, other in violations:
            log(f'  [违规] 业务域 {pkg} -> {other}: {go_file} 中 import "{imp}"')
        log("修复: 跨业务域共享结构仅走根 common/ 与 global/ 非业务运行引用(见 references/isolation-and-communication.md)")
        return 1
    log("隔离校验通过: 未发现跨业务域非法 import")
    return 0


def cmd_scaffold(args):
    """scaffold 子命令: 新建业务域骨架(域级通用目录 + 版本化目录 + init.go)并套用 README 模板(幂等)。

    [参数] args: argparse 解析结果(含 name, root, business_dir, version)
    [返回] 退出码 0
    最近修改时间: 2026-08-18 版本化目录下沉到 entity/router/controller/service 各自内部, 移除 crontask 与 rpc。
    """
    root = Path(args.root).resolve()
    source_root = root / args.business_dir
    pkg_dir = source_root / args.name
    log(f"开始创建业务域骨架: {pkg_dir} (版本 {args.version})")
    created = []
    # 1. 创建域级通用目录(跨版本共享, 已存在则跳过, 保证幂等)
    for sub in DOMAIN_LEVEL_DIRS:
        sub_dir = pkg_dir / sub
        if not sub_dir.exists():
            sub_dir.mkdir(parents=True, exist_ok=True)
            created.append(str(sub_dir))
    # 2. 创建版本化目录: entity/router/controller/service 各自内嵌 <v?>/ 目录
    for sub in VERSIONABLE_DIRS:
        sub_dir = pkg_dir / sub / args.version
        if not sub_dir.exists():
            sub_dir.mkdir(parents=True, exist_ok=True)
            created.append(str(sub_dir))
    # 3. 创建域初始化入口单文件 init.go(已存在则跳过)
    init_file = pkg_dir / INIT_FILENAME
    if not init_file.exists():
        init_file.parent.mkdir(parents=True, exist_ok=True)
        init_file.touch()
        created.append(str(init_file))
    # 4. 写业务域 README(已存在则不覆盖, 保证幂等且不破坏已有内容)
    readme = pkg_dir / "README.md"
    if not readme.exists():
        pkg_dir.mkdir(parents=True, exist_ok=True)
        readme.write_text(render_readme(args.name), encoding="utf-8")
        created.append(str(readme))
    if created:
        log(f"已创建 {len(created)} 项:")
        for item in created:
            log(f"  + {item}")
    else:
        log("目标已存在, 未新增任何内容(幂等)")
    log(f"提示: 记得在 {source_root / 'README.md'} 的业务域索引中登记 {args.name}")
    return 0


# 微业务标记: 写入目标项目规则文件的受管章节标题与正文
MARKER_SECTION_HEADER = "微业务架构约束"
MARKER_SECTION_BODY = """本项目采用微业务(伪微服务)架构, 由 `micro-business-architecture-rules` skill 守护。

- 不同业务域直连源码根 `internal/<域>/` 下, 各自自包含; 业务域之间禁止直接 import 对方任何目录。
- 业务相关逻辑通过版本化目录 `internal/<域>/router/<v?>/`、`controller/<v?>/`、`entity/<v?>/`、`service/<v?>/` 隔离, 包名用 `v?router`、`v?controller`、`v?entity`、`v?service` 别名引用; 其余为跨版本通用业务逻辑。
- 域级入口为单文件 `internal/<域>/init.go`, 全量注册本域所有版本路由, `/v1`、`/v2` 前缀区分。
- 新业务新开域目录, 旧版本与新版本并存对外, 不因新增版本而下线。
- 每个业务域必须有统一 README; 全局业务索引在 `internal/README.md`。
- 新增业务域用 `micro_business.py scaffold <业务名>`, 改动后用 `micro_business.py check` 校验隔离。"""

# 微业务标记: 写入根目录 项目设计.md 的业务索引段标题与正文
DESIGN_SECTION_HEADER = "微业务架构与业务域索引"
DESIGN_SECTION_BODY = """本项目采用微业务架构。业务域索引见 `internal/README.md`；业务域之间禁止直接 import，共享结构仅走根 `common/` 与 `global/`，架构约束见规则文件的「微业务架构约束」章节。"""


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
    log(f"  项目设计.md: 微业务架构与业务域索引段 -> {result}")
    log("微业务标记写入完成(幂等, 重复运行不重复堆叠)")
    return 0


def build_parser():
    """构造命令行参数解析器。

    [参数] 无
    [返回] argparse.ArgumentParser 实例
    最近修改时间: 2026-08-18 14:41:00 移除 --with-rpc，新增 --version 版本目录参数。
    """
    parser = argparse.ArgumentParser(
        prog="micro_business",
        description="微业务架构脚手架与隔离校验",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    # scaffold 子命令
    p_scaffold = sub.add_parser("scaffold", help="新建业务域骨架(幂等)")
    p_scaffold.add_argument("name", help="业务域名(ASCII, 如 order)")
    p_scaffold.add_argument("--root", default=".", help="项目根目录(默认当前目录)")
    p_scaffold.add_argument("--business-dir", default="internal", help="源码根相对路径(业务域直连其下)")
    p_scaffold.add_argument("--version", default=DEFAULT_VERSION, help="版本化目录内嵌的版本名(默认 v1)")
    p_scaffold.set_defaults(func=cmd_scaffold)

    # check 子命令
    p_check = sub.add_parser("check", help="校验业务域间是否存在非法横向 import")
    p_check.add_argument("--root", default=".", help="项目根目录(默认当前目录)")
    p_check.add_argument("--business-dir", default="internal", help="源码根相对路径(业务域直连其下)")
    p_check.add_argument("--detect-new", action="store_true", help="改为候选新项目机器判定(不校验隔离)")
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
