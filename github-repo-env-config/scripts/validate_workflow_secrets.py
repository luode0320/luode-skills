#!/usr/bin/env python3
"""校验 .github/workflows 是否已对齐「仓库级 Actions Secret 四要素」。

检查三件事（任一失败即视为未完成，不得用口头说明替代）：
  1. 每个工作流文件能被 YAML 解析；
  2. job 级 `env` 中不存在四要素明文键（如 `REMOTE_PORT: 22`）；
  3. 每个含 `host:` 的步骤（scp / ssh / rsync / 自定义 action），四要素均为 `secrets.*` 表达式；
  4. 全文无 `env.REMOTE_*` 中转残留。

用法：
    python validate_workflow_secrets.py .github/workflows
    python validate_workflow_secrets.py .github/workflows/main.yml --required REMOTE_HOST,REMOTE_PORT
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

# with 入参名 → 期望的 secret 名。ssh 用小写 -p、scp 用大写 -P 属于裸命令脚本范畴，此处只管 action 入参。
DEFAULT_MAPPING = {
    "host": "REMOTE_HOST",
    "port": "REMOTE_PORT",
    "username": "REMOTE_USER",
    "password": "REMOTE_PASSWORD",
}


def normalize(expr: object) -> str:
    """把 `${{  secrets.X  }}` 归一化为 `${{ secrets.X }}` 便于比较。"""
    return re.sub(r"\s+", " ", str(expr)).strip()


def collect_files(targets: list[str]) -> list[Path]:
    files: list[Path] = []
    for target in targets:
        path = Path(target)
        if path.is_dir():
            files.extend(sorted(p for p in path.rglob("*.yml") if p.is_file()))
            files.extend(sorted(p for p in path.rglob("*.yaml") if p.is_file()))
        elif path.is_file():
            files.append(path)
    return files


def check_file(path: Path, required: set[str], mapping: dict[str, str]) -> list[str]:
    import yaml  # 延迟导入，便于给出安装提示

    problems: list[str] = []
    text = path.read_text(encoding="utf-8")

    try:
        doc = yaml.safe_load(text)
    except Exception as exc:  # noqa: BLE001 - 解析失败需要原样呈现
        return [f"YAML 解析失败: {exc}"]

    if not isinstance(doc, dict) or "jobs" not in doc:
        return ["缺少 jobs 段，跳过（可能不是工作流文件）"]

    for job_name, job in (doc.get("jobs") or {}).items():
        if not isinstance(job, dict):
            continue

        # 检查 2：job.env 明文
        for key in (job.get("env") or {}):
            if key in required:
                problems.append(f"job<{job_name}>.env 存在明文 {key}，应改为 secrets 引用并删除")

        # 检查 3：含 host 的步骤四项必须指向 secrets
        for idx, step in enumerate(job.get("steps") or [], start=1):
            if not isinstance(step, dict):
                continue
            with_block = step.get("with") or {}
            if not isinstance(with_block, dict) or not mapping["host"] in with_block:
                continue
            label = step.get("name") or step.get("uses") or f"step#{idx}"
            for input_key, secret_name in mapping.items():
                if secret_name not in required:
                    continue
                if input_key not in with_block:
                    problems.append(f"step<{label}> 缺少 `{input_key}`，期望 ${{{{ secrets.{secret_name} }}}}")
                    continue
                actual = normalize(with_block[input_key])
                expected = f"${{{{ secrets.{secret_name} }}}}"
                if actual != expected:
                    problems.append(f"step<{label}>.{input_key} = {actual}，期望 {expected}")

    # 检查 4：env.* 中转残留
    for secret_name in sorted(required):
        if re.search(rf"\$\{{\{{\s*env\.{secret_name}\s*\}}\}}", text):
            problems.append(f"仍存在 env.{secret_name} 中转引用，应改为 secrets.{secret_name}")

    return problems


def main() -> int:
    parser = argparse.ArgumentParser(description="校验工作流是否已对齐仓库级 Actions Secret")
    parser.add_argument("targets", nargs="+", help="工作流文件或目录")
    parser.add_argument("--required", default=",".join(DEFAULT_MAPPING.values()),
                        help="要求的 secret 名，逗号分隔")
    parser.add_argument("--mapping", default=None,
                        help="with 入参到 secret 的映射，如 host=REMOTE_HOST,port=REMOTE_PORT")
    args = parser.parse_args()

    required = {item.strip() for item in args.required.split(",") if item.strip()}
    mapping = dict(DEFAULT_MAPPING)
    if args.mapping:
        mapping = {}
        for pair in args.mapping.split(","):
            key, _, value = pair.partition("=")
            mapping[key.strip()] = value.strip()

    try:
        import yaml  # noqa: F401
    except ImportError:
        sys.exit("缺少 PyYAML：python -m pip install pyyaml")

    files = collect_files(args.targets)
    if not files:
        sys.exit(f"未找到工作流文件: {args.targets}")

    failed = 0
    for path in files:
        problems = check_file(path, required, mapping)
        if problems:
            failed += 1
            print(f"FAIL {path}")
            for item in problems:
                print(f"     - {item}")
        else:
            print(f"PASS {path}")

    print(f"\n汇总：{len(files)} 个文件，{failed} 个未通过")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
