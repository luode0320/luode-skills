#!/usr/bin/env python3
"""
TAPD AddComment - 在业务对象下添加一条评论

用法:
  python3 add_comment.py --description '<p>评论内容</p>'
  python3 add_comment.py --description '## 标题\n- 列表项1\n- 列表项2'
  python3 add_comment.py --workspace-id 12345 --entry-type stories --entry-id 100001 --author user --description '<p>内容</p>'
  python3 add_comment.py --root-id 100040 --reply-id 100040 --description '<p>回复内容</p>'
  echo '<p>内容</p>' | python3 add_comment.py --description -
  echo '## Markdown 也行' | python3 add_comment.py --description -

环境变量:
  TAPD_API_ENDPOINT  API 端点（必须）
  TAPD_TOKEN         Bearer Token（必须）
  TAPD_WORKSPACE_IDS 项目 ID 列表（逗号分隔）
  TAPD_WORKSPACE_ID  单个项目 ID（降级）
  TAPD_ENTRY_TYPE    实体类型
  TAPD_ENTRY_ID      实体 ID
  TAPD_COMMENT_ID    触发评论 ID（用作 reply_id）
  TAPD_COMMENT_ROOT_ID 根评论 ID（用作 root_id）
  TAPD_NPC_ROLE      NPC 登录名（用作 author）
"""

import json
import os
import re
import sys
import urllib.request
import urllib.error
import urllib.parse


# ============================================================
# 配置
# ============================================================

API_ENDPOINT = os.environ.get("TAPD_API_ENDPOINT", "")
TOKEN = os.environ.get("TAPD_TOKEN", "")


def get_default_workspace_id():
    """从环境变量获取默认 workspace_id（取第一个）"""
    ws_ids = os.environ.get("TAPD_WORKSPACE_IDS", "") or os.environ.get("TAPD_WORKSPACE_ID", "")
    if ws_ids:
        return ws_ids.split(",")[0].strip()
    return ""


# ============================================================
# Markdown 检测 & 转 HTML
# ============================================================

# Markdown 特征正则列表（匹配任一即认为是 Markdown）
_MD_PATTERNS = [
    re.compile(r"^#{1,6}\s", re.MULTILINE),                # 标题  # / ## / ###
    re.compile(r"^[-*+]\s", re.MULTILINE),                  # 无序列表  - / * / +
    re.compile(r"^\d+\.\s", re.MULTILINE),                  # 有序列表  1.
    re.compile(r"^>\s", re.MULTILINE),                       # 引用  >
    re.compile(r"```", re.MULTILINE),                        # 代码块  ```
    re.compile(r"^\|.+\|", re.MULTILINE),                    # 表格  | xxx |
    re.compile(r"\[.+?\]\(.+?\)"),                           # 链接  [text](url)
    re.compile(r"!\[.*?\]\(.+?\)"),                          # 图片  ![alt](url)
    re.compile(r"\*\*.+?\*\*"),                              # 加粗  **text**
    re.compile(r"(?<!\*)\*(?!\*).+?(?<!\*)\*(?!\*)"),        # 斜体  *text*
    re.compile(r"~~.+?~~"),                                  # 删除线  ~~text~~
    re.compile(r"`.+?`"),                                    # 行内代码  `code`
    re.compile(r"^---$", re.MULTILINE),                      # 水平线  ---
    re.compile(r"^- \[[ x]\]\s", re.MULTILINE),             # 任务列表  - [ ] / - [x]
]

# 已经是 HTML 的特征（包含常见 HTML 标签）
_HTML_TAG_RE = re.compile(r"<(?:p|div|span|b|i|u|s|a|ul|ol|li|table|tr|td|th|pre|code|blockquote|br|hr|h[1-6]|img|strong|em)[\s>/]", re.IGNORECASE)


def _is_html(text):
    """检测文本是否已经是 HTML 格式"""
    return bool(_HTML_TAG_RE.search(text))


def _is_markdown(text):
    """检测文本是否包含 Markdown 语法特征"""
    matches = sum(1 for p in _MD_PATTERNS if p.search(text))
    # 匹配 2 个以上特征，或者文本较短时匹配 1 个即可
    return matches >= 2 or (matches >= 1 and len(text.strip().splitlines()) <= 3)


def _md_to_html(text):
    """
    使用 markdown 库将 Markdown 转换为 HTML。
    启用常用扩展：表格、代码高亮、删除线、任务列表等。
    """
    try:
        import markdown
    except ImportError:
        print("警告: markdown 库未安装（pip install markdown），将原样发送文本", file=sys.stderr)
        return f"<p>{text}</p>"

    extensions = [
        "markdown.extensions.tables",          # 表格
        "markdown.extensions.fenced_code",     # 围栏代码块 ```
        "markdown.extensions.codehilite",      # 代码高亮
        "markdown.extensions.nl2br",           # 换行转 <br>
        "markdown.extensions.sane_lists",      # 更合理的列表解析
        "markdown.extensions.smarty",          # 智能标点
    ]

    extension_configs = {
        "markdown.extensions.codehilite": {
            "css_class": "highlight",
            "guess_lang": False,
        },
    }

    html = markdown.markdown(
        text,
        extensions=extensions,
        extension_configs=extension_configs,
        output_format="html",
    )
    return html


def ensure_html(text):
    """
    智能检测输入内容格式：
    - 已经是 HTML → 直接返回
    - 是 Markdown → 转成 HTML 返回
    - 纯文本 → 包裹 <p> 标签返回
    """
    stripped = text.strip()

    # 优先检测 HTML
    if _is_html(stripped):
        print("📝 检测到 HTML 格式，直接使用", file=sys.stderr)
        return stripped

    # 检测 Markdown
    if _is_markdown(stripped):
        print("📝 检测到 Markdown 格式，自动转换为 HTML ...", file=sys.stderr)
        html = _md_to_html(stripped)
        print(f"📝 Markdown → HTML 转换完成（{len(stripped)} → {len(html)} 字符）", file=sys.stderr)
        return html

    # 纯文本，包裹 <p>
    print("📝 检测到纯文本，自动包裹 <p> 标签", file=sys.stderr)
    # 保留换行
    paragraphs = stripped.split("\n\n")
    if len(paragraphs) > 1:
        return "".join(f"<p>{p.strip()}</p>" for p in paragraphs if p.strip())
    return f"<p>{stripped}</p>"


# ============================================================
# 参数解析
# ============================================================


def parse_args(argv):
    """解析命令行参数，返回 dict"""
    args = {
        "workspace_id": "",
        "entry_type": "",
        "entry_id": "",
        "author": "",
        "description": "",
        "root_id": "",
        "reply_id": "",
    }

    i = 1
    while i < len(argv):
        arg = argv[i]
        if arg in ("--workspace-id", "--workspace_id") and i + 1 < len(argv):
            args["workspace_id"] = argv[i + 1]
            i += 2
        elif arg in ("--entry-type", "--entry_type") and i + 1 < len(argv):
            args["entry_type"] = argv[i + 1]
            i += 2
        elif arg in ("--entry-id", "--entry_id") and i + 1 < len(argv):
            args["entry_id"] = argv[i + 1]
            i += 2
        elif arg == "--author" and i + 1 < len(argv):
            args["author"] = argv[i + 1]
            i += 2
        elif arg == "--description" and i + 1 < len(argv):
            args["description"] = argv[i + 1]
            i += 2
        elif arg in ("--root-id", "--root_id") and i + 1 < len(argv):
            args["root_id"] = argv[i + 1]
            i += 2
        elif arg in ("--reply-id", "--reply_id") and i + 1 < len(argv):
            args["reply_id"] = argv[i + 1]
            i += 2
        elif arg in ("-h", "--help"):
            print(__doc__)
            sys.exit(0)
        else:
            print(f"未知参数: {arg}", file=sys.stderr)
            print("使用 --help 查看帮助", file=sys.stderr)
            sys.exit(1)
            i += 1

    return args


def resolve_params(args):
    """
    将命令行参数与环境变量合并，返回最终的请求参数 dict。
    命令行参数优先于环境变量。
    """
    params = {}

    # workspace_id
    workspace_id = args["workspace_id"] or get_default_workspace_id()
    if not workspace_id:
        print("错误: 未提供 workspace_id，请通过 --workspace-id 或环境变量 TAPD_WORKSPACE_IDS / TAPD_WORKSPACE_ID 配置", file=sys.stderr)
        sys.exit(1)
    params["workspace_id"] = workspace_id

    # entry_type
    entry_type = args["entry_type"] or os.environ.get("TAPD_ENTRY_TYPE", "")
    if not entry_type:
        print("错误: 未提供 entry_type，请通过 --entry-type 或环境变量 TAPD_ENTRY_TYPE 配置", file=sys.stderr)
        sys.exit(1)
    valid_entry_types = ("stories", "bug", "bug_remark", "tasks")
    if entry_type not in valid_entry_types:
        print(f"错误: entry_type 必须为 {'/'.join(valid_entry_types)}，当前值: {entry_type}", file=sys.stderr)
        sys.exit(1)
    params["entry_type"] = entry_type

    # entry_id
    entry_id = args["entry_id"] or os.environ.get("TAPD_ENTRY_ID", "")
    if not entry_id:
        print("错误: 未提供 entry_id，请通过 --entry-id 或环境变量 TAPD_ENTRY_ID 配置", file=sys.stderr)
        sys.exit(1)
    params["entry_id"] = entry_id

    # author
    author = args["author"] or os.environ.get("TAPD_NPC_ROLE", "")
    if not author:
        print("错误: 未提供 author，请通过 --author 或环境变量 TAPD_NPC_ROLE 配置", file=sys.stderr)
        sys.exit(1)
    params["author"] = author

    # description（支持从 stdin 读取，自动检测 Markdown 并转 HTML）
    description = args["description"]
    if description == "-":
        description = sys.stdin.read()
    if not description:
        print("错误: 未提供 description，请通过 --description 传入评论内容（支持 HTML / Markdown / 纯文本）", file=sys.stderr)
        sys.exit(1)
    params["description"] = ensure_html(description)

    # root_id（可选，回复评论时必填）
    root_id = args["root_id"] or os.environ.get("TAPD_COMMENT_ROOT_ID", "")
    if root_id and root_id != "0":
        params["root_id"] = root_id

    # reply_id（可选，回复评论时必填）
    reply_id = args["reply_id"] or os.environ.get("TAPD_COMMENT_ID", "")
    if reply_id and reply_id != "0":
        params["reply_id"] = reply_id

    # 校验：root_id 和 reply_id 需要同时存在
    has_root = "root_id" in params
    has_reply = "reply_id" in params
    if has_root != has_reply:
        print("警告: root_id 和 reply_id 需要同时提供。只提供了其中一个，将忽略回复参数。", file=sys.stderr)
        params.pop("root_id", None)
        params.pop("reply_id", None)

    return params


# ============================================================
# API 调用
# ============================================================


def add_comment(params):
    """
    调用 TAPD AddComment API，返回响应 JSON。
    使用 application/x-www-form-urlencoded 格式（推荐，避免 HTML 特殊字符编码问题）。
    """
    if not API_ENDPOINT:
        print("错误: 未配置 TAPD_API_ENDPOINT，请设置环境变量", file=sys.stderr)
        sys.exit(1)
    if not TOKEN:
        print("错误: 未配置 TAPD_TOKEN，请设置环境变量", file=sys.stderr)
        sys.exit(1)

    url = f"{API_ENDPOINT}/comments"
    data = urllib.parse.urlencode(params).encode("utf-8")

    req = urllib.request.Request(
        url,
        data=data,
        method="POST",
        headers={
            "Authorization": f"Bearer {TOKEN}",
            "Content-Type": "application/x-www-form-urlencoded",
        },
    )

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            body = json.loads(resp.read().decode("utf-8"))
            return body
    except urllib.error.HTTPError as e:
        error_body = ""
        try:
            error_body = e.read().decode("utf-8")
        except Exception:
            pass
        print(f"HTTP 错误 {e.code}: {e.reason}", file=sys.stderr)
        if error_body:
            print(f"响应: {error_body}", file=sys.stderr)
        sys.exit(1)
    except urllib.error.URLError as e:
        print(f"请求失败: {e.reason}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"请求异常: {e}", file=sys.stderr)
        sys.exit(1)


# ============================================================
# NPC 运行日志
# ============================================================


def print_npc_run_log(sdk_result: dict, comment_result: dict) -> None:
    """
    在脚本生命周期尾声打印 NPC 运行日志。
    日志格式与前端 JS 代码保持一致，便于统一采集和分析。

    参数:
        sdk_result: SDK 调用结果（可选），包含 success, model, usage, duration_ms 等字段
        comment_result: 评论 API 调用结果，包含 success, data 等字段
    """
    # agent_run_status: SDK 调用是否成功（1=成功, 2=失败）
    extra = {
        "none_sdk_version": True  # 此版本非npc sdk调用，因此无法在agent执行skill流程内获取模型、token消耗等信息。预留此标记位，供采集侧特殊处理。
        "model": "",
        "token_input": None,
        "token_output": None,
        "cnb_status": "",
        "cnb_duration_ms": None,
        "reply_content": comment_result.get("reply_content", ""),
    }

    # reply_status: 评论是否成功（1=成功, 2=失败）
    reply_status = 1 if comment_result.get("success") else 2

    log = {
        "workspace_id": get_default_workspace_id(),
        "entity_type": os.environ.get("TAPD_ENTRY_TYPE", ""),
        "entity_id": os.environ.get("TAPD_ENTRY_ID", ""),
        "user_id": os.environ.get("TAPD_USER_NAME", ""),
        "query_content": os.environ.get("TAPD_NPC_QUERY", ""),
        "company_id": os.environ.get("TAPD_COMPANY_ID", ""),
        "comment_location": os.environ.get("TAPD_COMMENT_LOCATION", ""),
        "agent_run_status": reply_status,  # 视同于评论回复状态
        "reply_status": reply_status,
        "log_time": __import__("datetime").datetime.now().isoformat(),
        "extra": extra,
    }

    print("[CNB_NPC_LOG_START]", file=sys.stderr)
    print(json.dumps(log, ensure_ascii=False), file=sys.stderr)
    print("[CNB_NPC_LOG_END]", file=sys.stderr)


# ============================================================
# 主入口
# ============================================================


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        print("错误: 至少需要 --description 参数", file=sys.stderr)
        sys.exit(1)

    args = parse_args(sys.argv)
    params = resolve_params(args)

    # 打印请求概要（不泄露 Token）
    summary = {k: (v[:80] + "..." if len(v) > 80 else v) for k, v in params.items()}
    print(f"正在添加评论...", file=sys.stderr)
    print(f"请求参数: {json.dumps(summary, ensure_ascii=False)}", file=sys.stderr)

    # 添加评论（try-finally 确保日志一定打印）
    comment_success = False
    comment_data = {}
    try:
        result = add_comment(params)
        comment_success = result.get("status") == 1
        if comment_success:
            comment_data = result.get("data", {}).get("Comment", {})
    except SystemExit:
        comment_success = False
    finally:
        # 构建评论结果（供日志使用）
        comment_result = {
            "success": comment_success,
            "data": comment_data,
            "reply_content": params.get("description", ""),
        }
        # 打印 NPC 运行日志（finally 步骤，无论成功失败都执行）
        print_npc_run_log(comment_result=comment_result)

    # 输出结果
    if comment_success:
        comment_id = comment_data.get("id", "")
        print(json.dumps(result, ensure_ascii=False, indent=2))
        print(f"\n✅ 评论添加成功！评论 ID: {comment_id}", file=sys.stderr)
    else:
        print(f"\n❌ 评论添加失败", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
