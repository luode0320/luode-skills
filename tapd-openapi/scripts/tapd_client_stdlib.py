"""
TAPD API 客户端（仅使用 Python 标准库）。

依赖：urllib.request, json, os, base64, argparse。
环境变量：TAPD_ACCESS_TOKEN 或 TAPD_API_USER + TAPD_API_PASSWORD；
         TAPD_API_BASE_URL（可选，默认 https://api.tapd.cn）；可选 TAPD_BASE_URL（默认 https://www.tapd.cn）, BOT_URL, CURRENT_USER_NICK。

命令行用法（AI 可直接调用）：
    python tapd_client_stdlib.py projects [--nick NICK]
    python tapd_client_stdlib.py workspace --workspace-id ID
    python tapd_client_stdlib.py stories --workspace-id ID [--entity-type stories|tasks] [--limit N] [--page N] [--id ID] [--name NAME] [--status STATUS]
    python tapd_client_stdlib.py bugs --workspace-id ID [--limit N] [--page N] [--id ID]
    python tapd_client_stdlib.py iterations --workspace-id ID [--limit N] [--page N]
    python tapd_client_stdlib.py releases --workspace-id ID [--limit N] [--page N]
    python tapd_client_stdlib.py get --endpoint "stories/count" -p workspace_id=123 -p entity_type=stories
    python tapd_client_stdlib.py post --endpoint "stories" -b '{"workspace_id":123,"name":"需求标题"}'

Python 调用示例：
    from tapd_client_stdlib import request, get_stories, get_workspace_info
    resp = request("GET", "stories", params={"workspace_id": 123, "limit": 10})
    stories = get_stories(123, {"entity_type": "stories", "limit": 5})
"""

import argparse
import json
import os
import re
import sys
import urllib.parse
import urllib.request
from base64 import b64encode
from typing import Any, Optional


# 默认 TAPD 云环境地址，未配置环境变量时使用
DEFAULT_TAPD_API_BASE_URL = "https://api.tapd.cn"
DEFAULT_TAPD_BASE_URL = "https://www.tapd.cn"


def _get_base_url() -> str:
    # 兼容本地 env-bootstrap 变量名（TAPD_API_ENDPOINT）与外部版变量名（TAPD_API_BASE_URL）
    base = (os.environ.get("TAPD_API_BASE_URL")
            or os.environ.get("TAPD_API_ENDPOINT")
            or DEFAULT_TAPD_API_BASE_URL)
    return base.rstrip("/")


def _get_headers() -> dict:
    # 兼容本地 env-bootstrap 变量名（TAPD_TOKEN）与外部版变量名（TAPD_ACCESS_TOKEN）
    token = os.environ.get("TAPD_ACCESS_TOKEN") or os.environ.get("TAPD_TOKEN")
    if token:
        return {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "Via": "mcp",
        }
    user = os.environ.get("TAPD_API_USER")
    password = os.environ.get("TAPD_API_PASSWORD")
    if not user or not password:
        raise ValueError(
            "请设置 TAPD_ACCESS_TOKEN/TAPD_TOKEN 或 TAPD_API_USER + TAPD_API_PASSWORD"
        )
    auth = b64encode(f"{user}:{password}".encode()).decode()
    return {
        "Authorization": f"Basic {auth}",
        "Content-Type": "application/json",
        "Via": "mcp",
    }


def _is_cloud() -> bool:
    base = (os.environ.get("TAPD_API_BASE_URL")
            or os.environ.get("TAPD_API_ENDPOINT")
            or DEFAULT_TAPD_API_BASE_URL)
    return "api.tapd.cn" in base


def to_long_id(short_id: str, workspace_id: int) -> str:
    """将短 ID（≤9 位数字）转为 TAPD 长 ID。"""
    s = str(short_id).strip()
    if not s.isdigit() or len(s) > 9:
        return s
    prefix = "11" if _is_cloud() else "10"
    return f"{prefix}{workspace_id}{s.zfill(9)}"


def request(
    method: str,
    endpoint: str,
    params: Optional[dict] = None,
    data: Optional[dict] = None,
    timeout: int = 30,
) -> dict:
    """
    发送 TAPD API 请求。URL 自动追加 ?s=mcp 或 &s=mcp。

    :param method: GET 或 POST
    :param endpoint: 路径，如 "stories", "workspaces/get_workspace_info"
    :param params: GET 查询参数或 POST 时也可拼在 URL（部分接口习惯用 query）
    :param data: POST 请求体（JSON）
    :param timeout: 超时秒数
    :return: 响应 JSON（dict）
    """
    base = _get_base_url()
    url = f"{base}/{endpoint.lstrip('/')}"
    sep = "&" if "?" in url else "?"
    url = f"{url}{sep}s=mcp"

    if params:
        encoded = urllib.parse.urlencode(params, doseq=True)
        url = f"{url}&{encoded}" if "?" in url else f"{url}?{encoded}"

    headers = _get_headers()
    req_body = None
    if method.upper() == "POST" and data is not None:
        req_body = json.dumps(data).encode("utf-8")

    req = urllib.request.Request(url, data=req_body, headers=headers, method=method.upper())
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8"))


def get_stories(
    workspace_id: int,
    options: Optional[dict] = None,
) -> dict:
    """
    获取需求或任务列表。entity_type 在 options 中指定为 stories 或 tasks。
    """
    opts = options or {}
    entity_type = opts.get("entity_type", "stories")
    endpoint = "stories" if entity_type == "stories" else "tasks"
    params = {"workspace_id": workspace_id, "page": 1, "limit": 10}
    params.update(opts)
    return request("GET", endpoint, params=params)


def get_workspace_info(workspace_id: int) -> dict:
    """根据项目 ID 获取项目信息。"""
    return request(
        "GET",
        f"workspaces/get_workspace_info?workspace_id={workspace_id}",
    )


def get_user_participant_projects(nick: str) -> dict:
    """获取用户参与的项目列表。"""
    return request("GET", "workspaces/user_participant_projects", params={"nick": nick})


def get_bugs(workspace_id: int, options: Optional[dict] = None) -> dict:
    """获取缺陷列表。"""
    params = {"workspace_id": workspace_id, "page": 1, "limit": 10}
    if options:
        params.update(options)
    return request("GET", "bugs", params=params)


def get_iterations(workspace_id: int, options: Optional[dict] = None) -> dict:
    """获取迭代列表。"""
    params = {"workspace_id": workspace_id}
    if options:
        params.update(options)
    return request("GET", "iterations", params=params)


def get_releases(workspace_id: int, options: Optional[dict] = None) -> dict:
    """获取发布计划列表。"""
    params = {"workspace_id": workspace_id}
    if options:
        params.update(options)
    return request("GET", "releases", params=params)


# 实体类型 -> (列表接口, 返回项的外层键)
_ENTITY_MAP = {
    "bug": ("bugs", "Bug"),
    "story": ("stories", "Story"),
    "task": ("tasks", "Task"),
}


def download(url: str, out_path: str, timeout: int = 60) -> str:
    """把 URL 下载到本地文件，返回路径。TAPD 的 download_url 自带签名，不需要再带 Authorization。"""
    os.makedirs(os.path.dirname(os.path.abspath(out_path)) or ".", exist_ok=True)
    req = urllib.request.Request(url, headers={"User-Agent": "tapd-client"})
    with urllib.request.urlopen(req, timeout=timeout) as resp, open(out_path, "wb") as f:
        f.write(resp.read())
    return out_path


def get_image_url(workspace_id: int, image_path: str) -> str:
    """换取图片下载链接（有效期 300 秒）。image_path 支持 /tfl/... 路径或完整 URL。"""
    image_path = image_path.split("?", 1)[0]  # 描述里的 src 带缓存戳，带上会 422 ParamError
    resp = request("GET", "files/get_image", params={"workspace_id": workspace_id, "image_path": image_path})
    data = resp.get("data") or {}
    # 文档写返回键是 Image，实际返回 Attachment，两者都收
    node = data.get("Image") or data.get("Attachment") or {}
    return node.get("download_url", "")


def download_entity_images(workspace_id: int, entity_type: str, entry_id: str, out_dir: str) -> list:
    """下载某个缺陷/需求/任务描述里内嵌的所有图片，返回本地路径列表。"""
    endpoint, key = _ENTITY_MAP[entity_type]
    resp = request("GET", endpoint, params={"workspace_id": workspace_id, "id": entry_id})
    rows = resp.get("data") or []
    html = "".join((it.get(key) or {}).get("description") or "" for it in rows)

    saved = []
    seen = set()
    for src in re.findall(r"""<img[^>]+src=["']([^"']+)["']""", html, re.I):
        if src in seen:
            continue
        seen.add(src)
        url = get_image_url(workspace_id, src)
        if not url:
            continue
        name = os.path.basename(urllib.parse.urlparse(src).path) or f"img_{len(saved)}.png"
        saved.append(download(url, os.path.join(out_dir, f"{entry_id}_{name}")))
    return saved


# ponytail: 只覆盖描述内嵌图片（最常见）。附件走 attachments/down，等真有需求再包。


def entity_url(kind: str, workspace_id: int, entity_id: str) -> str:
    """实体详情页链接。kind: bug / story / task / iteration。"""
    site = (os.environ.get("TAPD_SITE_URL") or DEFAULT_TAPD_BASE_URL).rstrip("/")
    action = "card" if kind == "iteration" else "detail"
    return f"{site}/tapd_fe/{workspace_id}/{kind}/{action}/{entity_id}"


def list_iterations(workspace_id: int) -> list:
    """迭代列表（拍平的 Iteration 字典）。"""
    resp = request("GET", "iterations", params={"workspace_id": workspace_id, "limit": 200})
    return [i["Iteration"] for i in (resp.get("data") or [])]


def get_current_iteration(workspace_id: int) -> dict:
    """返回今天落在区间内的迭代；多个重叠时取开始最晚的那个。"""
    from datetime import date
    today = date.today().isoformat()
    hits = [i for i in list_iterations(workspace_id)
            if (i.get("startdate") or "") <= today <= (i.get("enddate") or "")]
    return max(hits, key=lambda x: x.get("startdate") or "") if hits else {}


def resolve_iteration(workspace_id: int, spec: str) -> tuple:
    """把 current / all / 迭代 ID / 迭代名 解析成 (说明文字, iteration_id)。名字不区分大小写、支持部分匹配。"""
    if spec == "all":
        return "全部迭代", ""
    if spec == "current":
        cur = get_current_iteration(workspace_id)
        return (f"迭代 {cur.get('name')}", cur["id"]) if cur else ("全部迭代（未找到当前迭代）", "")
    if spec.isdigit():
        return f"迭代 {spec}", spec

    all_iters = list_iterations(workspace_id)
    key = spec.strip().lower()
    hits = [i for i in all_iters if key == (i.get("name") or "").strip().lower()] \
        or [i for i in all_iters if key in (i.get("name") or "").lower()]
    if not hits:
        names = "、".join((i.get("name") or "") for i in sorted(all_iters, key=lambda x: x.get("startdate") or "")[-8:])
        raise SystemExit(f"没有匹配「{spec}」的迭代。最近几个：{names}")
    best = max(hits, key=lambda x: x.get("startdate") or "")
    if len(hits) > 1:
        print(f"提示：「{spec}」匹配到 {len(hits)} 个迭代，取最新的 {best.get('name')}", file=sys.stderr)
    return f"迭代 {best.get('name')}", best["id"]


_STATUS_MAP_CACHE = {}

# 默认只看未提测的。同一个状态键在不同项目含义不一样（如 status_4 在 A 项目是「实现中」、
# 在 B 项目是「测试已验证」），所以按中文名过滤，不按键过滤。
_ACTIVE_LABELS = ("规划中", "实现中", "开发中", "新", "接受/处理", "重新打开")


def status_map(workspace_id, kind: str) -> dict:
    """状态键 -> 中文名。按 (项目, 类型) 缓存，一次 mine 只查一遍。"""
    key = (str(workspace_id), kind)
    if key not in _STATUS_MAP_CACHE:
        try:
            resp = request("GET", "workflows/status_map",
                           params={"workspace_id": workspace_id, "system": kind})
            _STATUS_MAP_CACHE[key] = resp.get("data") or {}
        except Exception:
            _STATUS_MAP_CACHE[key] = {}
    return _STATUS_MAP_CACHE[key]


def get_my_workitems(workspace_id: int, user: str, kinds=("bug", "story"),
                     status: str = "", iteration_id: str = "",
                     active_only: bool = False) -> list:
    """查处理人是 user 的工作项，返回 [(kind, id, status, priority, owner, title, path)]。"""
    rows = []
    for kind in kinds:
        endpoint, key = _ENTITY_MAP[kind]
        # 需求的处理人字段是 owner，缺陷是 current_owner
        params = {"workspace_id": workspace_id, "limit": 200,
                  "owner" if kind == "story" else "current_owner": user}
        if status:
            params["status"] = status
        if iteration_id:
            params["iteration_id"] = iteration_id
        labels = status_map(workspace_id, kind)
        for it in request("GET", endpoint, params=params).get("data") or []:
            e = it.get(key) or {}
            label = labels.get(e.get("status", ""), e.get("status", ""))
            if active_only and label not in _ACTIVE_LABELS:
                continue
            rows.append((kind, e.get("id", ""), label,
                         e.get("priority_label") or e.get("priority") or "-",
                         (e.get("owner") or e.get("current_owner") or "-").strip(";"),
                         e.get("name") or e.get("title") or "",
                         e.get("path") or ""))
    return rows


# 需求优先级是数字 1-4，缺陷是 urgent/high/medium/low 字符串，统一成越大越优先的分数
_PRIO_RANK = {"urgent": 5, "high": 4, "middle": 3, "medium": 3, "low": 2,
              "nice to have": 1, "insignificant": 1}


def prio_rank(prio: str) -> int:
    """优先级排序分，越大越优先；认不出的归 0 排最后。"""
    s = str(prio or "").strip().lower()
    return int(s) if s.isdigit() else _PRIO_RANK.get(s, 0)


def _chain(path: str, self_id: str) -> list:
    """Story.path 形如 '祖先:...:自身:'，拆成从根到自身的 ID 链。"""
    ids = [i for i in (path or "").split(":") if i and i != "0"]
    return ids or [self_id]


def with_ancestors(workspace_id: int, rows: list) -> list:
    """补齐父需求，返回 (标题行前缀, 续行前缀, row) 的先序列表。缺陷没有层级，平铺在最后。"""
    nodes = {r[1]: r for r in rows if r[0] == "story"}
    chains = {sid: _chain(r[6], sid) for sid, r in nodes.items()}
    missing = {i for c in chains.values() for i in c} - set(nodes)
    if missing:
        resp = request("GET", "stories", params={"workspace_id": workspace_id,
                                                 "id": ",".join(sorted(missing)), "limit": 200})
        for it in resp.get("data") or []:
            e = it.get("Story") or {}
            sid = e.get("id", "")
            nodes[sid] = ("story", sid,
                          status_map(workspace_id, "story").get(
                              e.get("status", ""), e.get("status", "")),
                          e.get("priority_label") or e.get("priority") or "-",
                          (e.get("owner") or "-").strip(";"),
                          e.get("name") or "", e.get("path") or "")
            chains[sid] = _chain(e.get("path") or "", sid)

    children, roots = {}, []
    for sid, chain in chains.items():
        parent = chain[-2] if len(chain) > 1 and chain[-1] == sid else None
        if parent in nodes:
            children.setdefault(parent, []).append(sid)
        else:
            roots.append(sid)

    out = []

    def _by_prio(sid):
        return (-prio_rank(nodes[sid][3]), sid)

    def walk(sid, prefix, cont):
        out.append((prefix, cont, nodes[sid]))
        kids = sorted(children.get(sid, []), key=_by_prio)
        for i, c in enumerate(kids):
            last = i == len(kids) - 1
            walk(c, cont + ("└─ " if last else "├─ "),
                 cont + ("   " if last else "│  "))

    for sid in sorted(roots, key=_by_prio):
        walk(sid, "", "")
    bugs = sorted((r for r in rows if r[0] != "story"),
                  key=lambda r: (-prio_rank(r[3]), r[1]))
    return out + [("", "", r) for r in bugs]


def get_current_user() -> str:
    """当前 Token 对应的登录名，优先取 TAPD_USER 省一次请求。"""
    return os.environ.get("TAPD_USER") or (request("GET", "users/info").get("data") or {}).get("name", "")

def _cli():
    parser = argparse.ArgumentParser(
        description="TAPD API 命令行客户端（仅标准库）。需设置 TAPD_ACCESS_TOKEN 或 TAPD_API_USER/TAPD_API_PASSWORD；TAPD_API_BASE_URL 可选（默认 https://api.tapd.cn）。"
    )
    sub = parser.add_subparsers(dest="command", required=True, help="子命令")

    # projects
    p_projects = sub.add_parser("projects", help="获取用户参与的项目列表")
    p_projects.add_argument("--nick", default=os.environ.get("CURRENT_USER_NICK", ""), help="用户昵称，默认 CURRENT_USER_NICK")

    # workspace
    p_ws = sub.add_parser("workspace", help="获取项目信息")
    p_ws.add_argument("--workspace-id", type=int, required=True, dest="workspace_id", help="项目 ID")

    # stories（含 tasks）
    p_stories = sub.add_parser("stories", help="获取需求或任务列表")
    p_stories.add_argument("--workspace-id", type=int, required=True, dest="workspace_id")
    p_stories.add_argument("--entity-type", choices=("stories", "tasks"), default="stories", dest="entity_type")
    p_stories.add_argument("--limit", type=int, default=10)
    p_stories.add_argument("--page", type=int, default=1)
    p_stories.add_argument("--id", dest="id_", metavar="ID", help="需求/任务 ID，支持逗号分隔多 ID")
    p_stories.add_argument("--name", help="标题模糊匹配")
    p_stories.add_argument("--status", help="状态")
    p_stories.add_argument("--fields", help="返回字段，逗号分隔")

    # bugs
    p_bugs = sub.add_parser("bugs", help="获取缺陷列表")
    p_bugs.add_argument("--workspace-id", type=int, required=True, dest="workspace_id")
    p_bugs.add_argument("--limit", type=int, default=10)
    p_bugs.add_argument("--page", type=int, default=1)
    p_bugs.add_argument("--id", dest="id_", metavar="ID", help="缺陷 ID")
    p_bugs.add_argument("--title", help="标题")

    # iterations
    p_iter = sub.add_parser("iterations", help="获取迭代列表")
    p_iter.add_argument("--workspace-id", type=int, required=True, dest="workspace_id")
    p_iter.add_argument("--limit", type=int, default=30)
    p_iter.add_argument("--page", type=int, default=1)
    p_iter.add_argument("--name", help="迭代名称")

    # releases
    p_rel = sub.add_parser("releases", help="获取发布计划列表")
    p_rel.add_argument("--workspace-id", type=int, required=True, dest="workspace_id")
    p_rel.add_argument("--limit", type=int, default=30)
    p_rel.add_argument("--page", type=int, default=1)

    # mine
    p_mine = sub.add_parser("mine", help="列出我名下的需求和缺陷（表格输出，非 JSON）")
    p_mine.add_argument("--workspace-id", dest="workspace_id",
                        default=os.environ.get("TAPD_WORKSPACE_IDS", ""),
                        help="项目 ID，逗号分隔可查多个，默认 TAPD_WORKSPACE_IDS 全部")
    p_mine.add_argument("--user", default="", help="处理人，默认取 TAPD_USER 或当前 Token 用户")
    p_mine.add_argument("--type", choices=("bug", "story", "all"), default="all", dest="kind")
    p_mine.add_argument("--bugs", action="store_true", help="只看缺陷，等价 --type bug")
    p_mine.add_argument("--storys", "--stories", action="store_true", dest="storys", help="只看需求，等价 --type story")
    p_mine.add_argument("--status", default="active",
                        help="默认 active：只看规划中/实现中，已提测的不显示；all 不过滤；其他值透传 TAPD，如 new、<>closed")
    p_mine.add_argument("--iteration", default="current",
                        help="迭代：current（默认，按今天定位）/ all（不限）/ 迭代名如 V4.15 / 迭代 ID")

    # images
    p_img = sub.add_parser("images", help="下载缺陷/需求/任务描述里内嵌的图片")
    p_img.add_argument("--workspace-id", type=int, required=True, dest="workspace_id")
    p_img.add_argument("--type", choices=tuple(_ENTITY_MAP), default="bug", dest="entity_type")
    p_img.add_argument("--id", required=True, dest="id_", metavar="ID", help="实体 ID")
    p_img.add_argument("--out-dir", default="tapd_images", dest="out_dir", help="输出目录，默认 tapd_images")

    # 通用 get / post
    p_get = sub.add_parser("get", help="通用 GET：--endpoint 路径，-p key=val 多个参数")
    p_get.add_argument("--endpoint", required=True, help="API 路径，如 stories、bugs/count")
    p_get.add_argument("-p", "--param", dest="params", action="append", default=[], metavar="KEY=VAL", help="查询参数，可多次")

    p_post = sub.add_parser("post", help="通用 POST：--endpoint 路径，-b JSON 或 -p key=val")
    p_post.add_argument("--endpoint", required=True, help="API 路径，如 stories、comments")
    p_post.add_argument("-b", "--body", help="JSON 请求体")
    p_post.add_argument("-p", "--param", dest="params", action="append", default=[], metavar="KEY=VAL", help="作为 body 的键值，可多次（与 -b 二选一）")

    args = parser.parse_args()
    out = None

    if args.command == "projects":
        nick = (args.nick or "").strip()
        if not nick:
            print(json.dumps({"error": "请提供 --nick 或设置 CURRENT_USER_NICK"}, ensure_ascii=False), file=sys.stderr)
            raise SystemExit(1)
        out = get_user_participant_projects(nick)
    elif args.command == "workspace":
        out = get_workspace_info(args.workspace_id)
    elif args.command == "stories":
        opts = {"entity_type": args.entity_type, "limit": args.limit, "page": args.page}
        if getattr(args, "id_", None):
            opts["id"] = args.id_
        if getattr(args, "name", None):
            opts["name"] = args.name
        if getattr(args, "status", None):
            opts["status"] = args.status
        if getattr(args, "fields", None):
            opts["fields"] = args.fields
        out = get_stories(args.workspace_id, opts)
    elif args.command == "bugs":
        opts = {"limit": args.limit, "page": args.page}
        if getattr(args, "id_", None):
            opts["id"] = args.id_
        if getattr(args, "title", None):
            opts["title"] = args.title
        out = get_bugs(args.workspace_id, opts)
    elif args.command == "iterations":
        opts = {"limit": args.limit, "page": args.page}
        if getattr(args, "name", None):
            opts["name"] = args.name
        out = get_iterations(args.workspace_id, opts)
    elif args.command == "releases":
        out = get_releases(args.workspace_id, {"limit": args.limit, "page": args.page})
    elif args.command == "mine":
        user = args.user or get_current_user()
        kind = "bug" if args.bugs else "story" if args.storys else args.kind
        kinds = ("bug", "story") if kind == "all" else (kind,)

        ws_ids = [w.strip() for w in str(args.workspace_id).split(",") if w.strip()]
        if not ws_ids:
            raise SystemExit("未指定项目：用 --workspace-id 或配置 TAPD_WORKSPACE_IDS")

        for i, ws in enumerate(ws_ids):
            if i:
                print()
            scope, iter_id = resolve_iteration(ws, args.iteration)
            rows = get_my_workitems(ws, user, kinds,
                                    "" if args.status in ("active", "all") else args.status,
                                    iter_id, active_only=args.status == "active")
            ws_name = (get_workspace_info(ws).get("data") or {}).get("Workspace", {}).get("name") or ws
            print(f"{user} @ {ws_name} · {scope}：{len(rows)} 项")
            for prefix, cont, (k, id_, status, prio, owner, title, _p) in with_ancestors(ws, rows):
                print(f"{prefix}{k:5} {id_}  {status:10} {prio:10} {owner:8} {title[:60]}")
                print(f"{cont}      {entity_url(k, ws, id_)}")
        raise SystemExit(0)
    elif args.command == "images":
        out = {"files": download_entity_images(args.workspace_id, args.entity_type, args.id_, args.out_dir)}
    elif args.command == "get":
        params = {}
        for s in args.params:
            if "=" in s:
                k, v = s.split("=", 1)
                params[k.strip()] = v.strip()
        out = request("GET", args.endpoint, params=params if params else None)
    elif args.command == "post":
        if args.body:
            try:
                data = json.loads(args.body)
            except json.JSONDecodeError as e:
                print(json.dumps({"error": f"无效 JSON: {e}"}, ensure_ascii=False), file=sys.stderr)
                raise SystemExit(1)
        else:
            data = {}
            for s in args.params:
                if "=" in s:
                    k, v = s.split("=", 1)
                    data[k.strip()] = v.strip()
        out = request("POST", args.endpoint, data=data if data else None)

    if out is not None:
        print(json.dumps(out, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    _cli()
