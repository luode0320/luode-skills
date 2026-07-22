from __future__ import annotations

import argparse
import json
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="验证需求域 discovery 活跃消费者已迁移")
    parser.add_argument("--repo-root", required=True)
    parser.add_argument("--index", required=True)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = Path(args.repo_root).resolve()
    index_path = Path(args.index).resolve()
    data = json.loads(index_path.read_text(encoding="utf-8"))
    errors: list[str] = []
    consumers = data.get("requirement-discovery-rules")
    if not isinstance(consumers, list) or not consumers:
        errors.append("requirement-discovery-rules consumer list 为空")
        consumers = []
    for raw in consumers:
        path = (root / str(raw)).resolve()
        if root not in path.parents:
            errors.append(f"consumer 越界：{raw}")
            continue
        if not path.is_file():
            errors.append(f"consumer 不存在：{raw}")
            continue
        text = path.read_text(encoding="utf-8")
        active_text = text.split("## 变更记录", 1)[0] if raw == "PROJECT_MEMORY.md" else text
        if "requirement-discovery-rules" in active_text:
            errors.append(f"活跃 consumer 残留旧入口：{raw}")
        if raw.endswith((".md", ".yaml", ".yml")) and "initial-discovery" not in active_text and raw not in {
            "PROJECT_MEMORY.md",
            "PROJECT_STYLE.md",
        }:
            errors.append(f"consumer 未出现 canonical route：{raw}")
    # 迁移范围内的 live consumer 不能再通过引用旧入口形成竞争触发。
    required_live = {
        "artifact-delivery-gate-rules/references/plain-language-template-registry.yaml",
        "bug-discovery-rules/references/bug-domain-routing.md",
        "bug-discovery-rules/SKILL.md",
        "README.md",
        "requirement-gap-rules/SKILL.md",
        "team-development-rules/references/routing-rules.md",
        "编码skill.md",
    }
    if set(consumers) != required_live | {"PROJECT_MEMORY.md", "PROJECT_STYLE.md"}:
        errors.append("discovery consumer index 未冻结为本任务的 live write set")
    report = {"task": "TASK-SS-02-02", "valid": not errors, "consumer_count": len(consumers), "errors": errors}
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())