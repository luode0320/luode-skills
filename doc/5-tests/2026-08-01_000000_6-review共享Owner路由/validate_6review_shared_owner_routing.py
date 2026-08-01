"""验证 6-review 与持续监控共享静态 Owner 路由。"""

from __future__ import annotations

import re
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[3]
ROUTER_DIR = ROOT / "code-style-consistency-rules" / "scripts"
sys.path.insert(0, str(ROUTER_DIR))

from static_owner_router import OWNER_NAMES, BASE_OWNER_NAMES, owner_source_map_path, route_owners  # noqa: E402


def check(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> None:
    monitor = (ROOT / "continuous-code-quality-supervisor-rules" / "scripts" / "supervisor_state.py").read_text(encoding="utf-8")
    matrix = (ROOT / "continuous-code-quality-supervisor-rules" / "references" / "owner-routing-matrix.md").read_text(encoding="utf-8")
    style = (ROOT / "code-style-consistency-rules" / "SKILL.md").read_text(encoding="utf-8")
    check(owner_source_map_path(ROOT).is_file(), "共享来源映射不存在")
    check(len(OWNER_NAMES) == 28, "共享 Owner 数量漂移")
    check(route_owners([]) == [], "空改动不应生成 Owner")
    check(list(route_owners(["src/service/user.py"])) == list(BASE_OWNER_NAMES), "普通代码基础 Owner 顺序漂移")
    api = set(route_owners(["src/api/user_controller.py"]))
    check({"api-endpoint-rules", "api-request-rules", "api-response-rules", "api-swagger-rules"}.issubset(api), "API Owner 路由缺失")
    check("api-endpoint-rules" not in route_owners(["src/service/user.py"]), "普通业务文件误触发 API Owner")
    check("test-program-rules" in route_owners(["tests/fixtures/user_stub.py"]), "测试资产未路由到 test-program-rules")
    check("code-style-consistency-rules/references/static-owner-source-map.json" in matrix, "监控矩阵未指向共享 source map")
    check("owner-static-source-map.json" not in monitor and "owner-static-source-map.json" not in matrix, "旧 source map 名称残留")
    check(not re.search(r"^\s*(OWNER_NAMES|BASE_OWNER_NAMES)\s*=", monitor, re.MULTILINE), "监控仍复制 Owner 常量")
    check(not re.search(r"^def\s+route_owners\(", monitor, re.MULTILINE), "监控仍复制路由函数")
    check("STYLE: PASS" in style and "业务正确性" in style, "6-review 风格边界缺失")
    check("业务逻辑是否正确" not in style.split("6-review", 1)[0], "风格入口正文异常")
    print("6-review-shared-owner-routing: PASS")


if __name__ == "__main__":
    main()
