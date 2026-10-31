"""校验函数头注释元信息 [参数]/[返回]/最近修改时间 是否成立。

用法：
    python comment-rules/scripts/check_function_header.py --root . --diff-only
    python comment-rules/scripts/check_function_header.py --root . --path <file.py>
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from header_metadata_judge import judge
from header_metadata_parser import collect_headers

SKIP_DIR_MARKERS = ("__skillhub", ".system", "node_modules", "skill-dictionary", "Python/pythoncore")


def _should_skip(path: Path, root: Path) -> bool:
    """判断目标文件是否属于不参与校验的范围。

    [参数] path: 待判断文件；root: 仓库根。
    [返回] bool：命中第三方种子、系统目录、本机残留目录或位于仓库外时为 True。
    最近修改时间：2026-10-31 22:40:00；新增扫描排除口径与仓库外路径防御。
    """
    try:
        rel = path.relative_to(root).as_posix()
    except ValueError:
        return False
    return any(marker in rel for marker in SKIP_DIR_MARKERS)


def _changed_files(root: Path) -> list[Path]:
    """列出本轮工作树中改动过的 Python 文件。

    [参数] root: 仓库根。
    [返回] list[Path]：存在的改动文件列表，含未跟踪目录下的新增文件。
    最近修改时间：2026-10-31 22:40:00；新增 diff-only 文件枚举，补齐未跟踪目录展开。
    """
    result = subprocess.run(
        ["git", "status", "--porcelain", "--untracked-files=normal"],
        cwd=root,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    files: list[Path] = []
    for line in result.stdout.splitlines():
        rel = line[3:].strip().strip('"')
        if not rel:
            continue
        candidate = root / rel.rstrip("/")
        if candidate.is_dir():
            files.extend(candidate.rglob("*.py"))
        elif candidate.suffix == ".py":
            files.append(candidate)
    return [f for f in files if f.is_file()]


def _all_files(root: Path) -> list[Path]:
    """列出仓库内全部待校验的 Python 文件。

    [参数] root: 仓库根。
    [返回] list[Path]：排除跳过目录后的文件列表。
    最近修改时间：2026-10-31 22:40:00；新增全量枚举。
    """
    return [p for p in root.rglob("*.py") if not _should_skip(p, root)]


def main() -> int:
    """解析命令行参数并输出校验结论。

    [参数] 无：全部参数来自命令行。
    [返回] int：未通过校验时返回 1，否则返回 0。
    最近修改时间：2026-10-31 22:40:00；新增校验入口，path 模式同样阻断 MISSING。
    """
    parser = argparse.ArgumentParser(description="校验函数头注释元信息")
    parser.add_argument("--root", default=".")
    parser.add_argument("--path", action="append", default=[])
    parser.add_argument("--diff-only", action="store_true")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    if args.path:
        targets = [(root / p).resolve() for p in args.path]
    elif args.diff_only:
        targets = _changed_files(root)
    else:
        targets = _all_files(root)
    targets = [t for t in targets if t.is_file() and not _should_skip(t, root)]

    invalid: list[str] = []
    missing: list[str] = []
    passed = 0
    for path in targets:
        for header in collect_headers(path, root):
            verdict = judge(header)
            location = f"{header.path}:{header.line} {header.name}"
            if verdict.status == "PASS":
                passed += 1
            elif verdict.status == "INVALID":
                invalid.append(f"{location} -> {'; '.join(verdict.reasons)}")
            else:
                missing.append(location)

    print(f"扫描文件 {len(targets)} 个；PASS={passed} INVALID={len(invalid)} MISSING={len(missing)}")
    for item in invalid:
        print(f"[INVALID] {item}")
    if args.diff_only or args.path:
        for item in missing:
            print(f"[MISSING] {item}")
    blocking_missing = args.diff_only or bool(args.path)
    print(f"HEADER: {'FAIL' if invalid or (blocking_missing and missing) else 'PASS'}")
    return 1 if invalid or (blocking_missing and missing) else 0


if __name__ == "__main__":
    raise SystemExit(main())
