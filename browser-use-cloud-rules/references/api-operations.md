# Browser Use Cloud REST API 操作指南

> 职责：操作层——项目程序如何通过 Browser Use Cloud（browser-use.com）以 REST API 方式操作**公网浏览器**（https 有域名站点）。
> 安全闸门（密钥检查、费用确认、session 生命周期、业务副作用授权）以 SKILL.md 正文为唯一权威，本文件不重复定义。
> 来源：吸收 `browser-use-api__skillhub`（REST v2 端点）与 `browser-use-guide__skillhub`（云端对比/模型定价/场景）精华，2026-08-23 合并。

## 触发定位

本通道服务「项目程序需要操作浏览器」的场景——程序化提交浏览器任务、轮询结果、停止任务、查询余额。**不是**本地 URL / 本地页面交互（走 `browser-session-automation-rules`），也不是简单网页抓取（走 `web_fetch` / WebFetch）。

## 凭据（单一权威：`~/.browser-use`）

- 密钥统一存储在 `C:\Users\luode\.browser-use\.env`（该目录为 junction，指向 `D:\谷歌云盘\browser-use`，由 Google Drive 同步，换机器后重建 junction 即可恢复）。
- `.env` 文件格式：

  ```bash
  BROWSER_USE_API_KEY=your-key
  ```

- 读取顺序：`~/.browser-use/.env` 为默认来源；环境变量 `BROWSER_USE_API_KEY` 仅作运行时覆盖。
- 任何输出（stdout / 日志 / 聊天 / 文件）不得回显 key 原值，只报告存在或缺失。
- 环境自检见 SKILL.md「环境自检」小节。

## REST API v2 端点速查

Base URL：`https://api.browser-use.com/api/v2`

请求头（全部端点）：

```
X-Browser-Use-API-Key: <BROWSER_USE_API_KEY>
Content-Type: application/json
```

| 动作 | 方法与路径 | 说明 |
|---|---|---|
| 创建任务 | `POST /tasks` | body: `{"task": "自然语言任务", "llm": "可选模型"}`；返回 `id` / `sessionId` |
| 查询任务 | `GET /tasks/{taskId}` | 任务状态、输出、步骤、费用 |
| 停止任务 | `POST /tasks/{taskId}/stop` | 主动取消执行中的任务 |
| 余额查询 | `GET /billing/account` | 检查免费层 / 余额 / 速率限制（实测 2026-08-23：`GET /credits` 已下线返回 404，勿用） |

## 任务状态机

```
pending ─→ started ─→ finished
                 └──→ failed
```

`GET /tasks/{taskId}` 响应关键字段：

| 字段 | 类型 | 说明 |
|---|---|---|
| `status` | string | `pending` / `started` / `finished` / `failed` |
| `output` | string | 任务结果文本（finished 时） |
| `steps` | array | 动作序列（含截图），失败定位用 |
| `cost` | string | 费用美元字符串，如 `"0.02"` |
| `isSuccess` | boolean | 是否成功 |

## 快速开始（curl）

```bash
# 提交任务（不等待）
curl -s -X POST https://api.browser-use.com/api/v2/tasks \
  -H "X-Browser-Use-API-Key: $BROWSER_USE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"task": "Go to example.com and extract the main heading"}'

# 轮询结果（TASK_ID 替换为创建任务返回的 id）
curl -s "https://api.browser-use.com/api/v2/tasks/TASK_ID" \
  -H "X-Browser-Use-API-Key: $BROWSER_USE_API_KEY"

# 查询余额（脱敏字段：isFreeTier / totalCreditsBalanceUsd / monthlyCreditsBalanceUsd / additionalCreditsBalanceUsd / rateLimit）
curl -s https://api.browser-use.com/api/v2/billing/account \
  -H "X-Browser-Use-API-Key: $BROWSER_USE_API_KEY"
```

完整提交 + 轮询可用仓库脚本：`scripts/browser-use.sh "任务描述"`（自动从 `~/.browser-use/.env` 加载密钥）。

## 项目程序集成（Python）

标准库实现（无第三方依赖），供项目程序直接复用：

```python
import json
import os
import time
import urllib.request

BASE_URL = "https://api.browser-use.com/api/v2"


def load_api_key():
    """从 ~/.browser-use/.env 读取密钥；环境变量覆盖。失败时抛异常。"""
    env_key = os.environ.get("BROWSER_USE_API_KEY")
    if env_key:
        return env_key
    # Windows 下 expanduser 优先 USERPROFILE，Unix 下用 HOME；显式兜底保证两者一致
    home = os.environ.get("USERPROFILE") or os.path.expanduser("~")
    env_file = os.path.join(home, ".browser-use", ".env")
    if os.path.isfile(env_file):
        for line in open(env_file, encoding="utf-8"):
            line = line.strip()
            if line.startswith("BROWSER_USE_API_KEY="):
                return line.split("=", 1)[1].strip()
    raise RuntimeError("BROWSER_USE_API_KEY 缺失：请配置 ~/.browser-use/.env 或环境变量")


def _request(method, path, api_key, body=None):
    req = urllib.request.Request(
        BASE_URL + path,
        data=json.dumps(body).encode() if body else None,
        headers={
            "X-Browser-Use-API-Key": api_key,
            "Content-Type": "application/json",
        },
        method=method,
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.load(resp)


def run_task(task: str, llm: str | None = None, max_wait: int = 300) -> dict:
    """提交浏览器任务并轮询至结束，返回完整结果。"""
    api_key = load_api_key()
    created = _request("POST", "/tasks", api_key, {"task": task, **({"llm": llm} if llm else {})})
    task_id = created["id"]
    deadline = time.time() + max_wait
    while time.time() < deadline:
        result = _request("GET", f"/tasks/{task_id}", api_key)
        if result["status"] in ("finished", "failed"):
            return result
        time.sleep(5)
    raise TimeoutError(f"任务 {task_id} 超过 {max_wait}s 未完成")
```

## 模型与定价

| 模型 | 说明 |
|---|---|
| 服务商默认模型 | 不传 `llm` 字段时使用，费用最低 |
| `bu-30b-a3b-preview` | Browser Use 专用优化模型 |
| `claude-sonnet-4-6` | Anthropic 旗舰 |
| `gemini-3-flash-preview` | Google 高效模型 |

- ChatBrowserUse 模型定价（每 1M tokens）：输入 `$0.20` / 缓存输入 `$0.02` / 输出 `$2.00`。
- 单任务典型费用约 `$0.01–0.05`（取决于复杂度）；实际以服务端返回 `cost` 为准。
- 免费层有免费额度，但**免费层也不能跳过 SKILL.md 的费用确认闸门**。

## 应用场景

- 多步骤网页工作流（填表、搜索、比价、信息收集）。
- 站点屏蔽简单抓取、需要 Cloud Stealth / Proxy / CAPTCHA 合规处理。
- 需要步骤截图或执行痕迹。
- 无本地浏览器或本地浏览器不适用（如容器环境）。

## 边界（不做）

- 简单页面抓取 → `web_fetch` / WebFetch / 专用 HTTP 请求。
- 本地浏览器、本地 URL、本地页面交互 → `browser-session-automation-rules`。
- 高并发 / 大批量采集 → 专用爬虫或数据服务，不走本通道。
- 绕过权限 / 安全策略 / 站点限制、上传用户登录态、未授权的业务副作用 → 一律拒绝（见 SKILL.md 安全停止条件）。
- 任何收费动作前必须完成 SKILL.md 正文的费用确认，本文件不豁免。

## 参考来源

- REST v2 API 文档：<https://docs.browser-use.com/cloud/api-v2/>
- 开源库（概念参考，本项目走云端 API）：<https://github.com/browser-use/browser-use>
- MCP / 安全路由：见本 skill `references/routing-and-safety.md` 与 `mcp-installation-rules/references/tool-priority.md`
