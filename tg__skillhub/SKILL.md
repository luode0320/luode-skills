---
name: tg
description: Telegram CLI：读取收件箱、搜索聊天记录、发送/回复消息、查联系人、群成员与管理员。当用户需要查看 Telegram 未读消息、搜索聊天记录、发送 Telegram 消息、回复消息、查群成员或联系人时触发。触发词：Telegram、电报、tg 消息、tg 发送、tg 收件箱、tg 搜索、tg 群、telegram 消息。注意：发送/回复是真实对外动作，必须经用户确认后执行。
license: MIT
metadata:
  displayName: "Telegram 消息助手"
  version: "1.1.0"
allowed-tools: Read, Write, Bash
---

# Telegram CLI

Telegram 消息助手：读取、搜索、发送消息，查联系人/群组。基于 `@cyberdrk/tg` CLI（npm 全局包）。

## 适用边界

- **做**：读未读消息、读聊天记录、搜索消息、发送/回复消息、查联系人/群成员/管理员、会话状态检查。
- **不做**：创建机器人、管理频道、批量拉群等高风险群管理操作，除非用户显式要求且逐项确认。

## 工作流（4 步，发送带强制闸门）

### 第 1 步：确认会话可用

- **输入**：用户想做的事（读/搜/发）。
- **动作**：先 `tg whoami` / `tg check` 确认已登录；未认证时引导 `tg auth`（凭据来自 https://my.telegram.org/apps）。
- **输出**：会话状态结论（可用 / 需认证）。

### 第 2 步：读与搜（只读操作，可执行）

- **输入**：要查的收件箱 / 聊天名 / 关键词。
- **动作**：
  - `tg inbox` 看未读摘要；`tg read "ChatName" -n 50` 读最近消息；`tg read "ChatName" --since "1h"` 按时间窗读。
  - `tg search "query" --chat "ChatName"` 或 `--all` 全量搜索。
- **输出**：消息列表（默认时间倒序，新消息在前）。

### 第 3 步：发送 / 回复（对外动作，强制确认闸门）

- **输入**：接收人（`@username` 或群名）与消息内容。
- **动作**：
  1. 先展示草稿：**接收人 + 消息全文**（引用/回复目标）。
  2. **闸门【必确认】**：向用户逐字确认内容与接收人无误后，才执行 `tg send @username "message"` 或 `tg reply "ChatName" <id> "response"`；用户未确认一律不发送。
  3. 发送后回读结果（成功回执或错误信息）给用户。
- **输出**：发送结果回执。

### 第 4 步：联系人 / 群 / 状态

- **输入**：要查的联系人、群、或会话状态。
- **动作**：`tg contact @username`、`tg members "GroupName"`、`tg admins "GroupName"`、`tg groups --admin`、`tg whoami`、`tg check`。
- **输出**：查询结果。

## 命令速查表

| 分类 | 命令 |
|---|---|
| 读取 | `tg inbox`、`tg chats`、`tg read "Chat" -n 50`、`tg read "Chat" --since "1h"`、`tg read @username -n 20` |
| 搜索 | `tg search "query" --chat "Chat"`、`tg search "query" --all` |
| 写入（需确认） | `tg send @username "message"`、`tg send "Group" "message"`、`tg reply "Chat" 12345 "response"` |
| 联系人/群 | `tg contact @username`、`tg members "Group"`、`tg admins "Group"`、`tg groups --admin` |
| 状态 | `tg whoami`、`tg check` |

所有命令支持 `--json` 结构化输出。

## 安装

```bash
npm install -g @cyberdrk/tg
```

首次使用需 `tg auth` 完成认证（API 凭据从 https://my.telegram.org/apps 获取）。

## 边界条件与异常处理

- **未认证/会话失效**：`tg check` 失败 → 提示重新 `tg auth`，不假装已登录继续操作。
- **聊天/联系人不存在**：命令报错 → 提示用户核对名称（群名支持部分匹配、用户名必须以 @ 开头），不猜测替代目标。
- **发送失败**（网络/限流/目标不可达）：如实回传 CLI 错误；确认消息未发出前**不重试发送**，避免重复发送造成打扰，先让用户决定是否重试。
- **消息内容敏感**：草稿含隐私/机密信息时，先提示用户确认发送范围，再走发送闸门。
- **只读 vs 写入**：`inbox/read/search/contact/members/admins` 只读可直行；`send/reply` 一律走第 3 步确认闸门。
- **隐私边界**：读取他人聊天记录前先确认用户对目标会话的访问权限；群成员列表等信息的用途要明确，不扩散。

## 退出机制

用户输入「结束」→ 停止，回复「Telegram 操作完成。」；发送类操作未获确认时不执行（第 3 步闸门）。

## 约束

- 发送/回复属于真实对外动作：内容与接收人必须逐字确认后才执行，禁止自行补发、代发或扩大发送范围。
- 所有命令输出如实呈现，`--json` 解析失败时展示原始输出，不编造成结构化结果。
- 用户名必须以 `@` 开头；群名支持部分匹配；`--since` 接受 `1h`/`30m`/`7d` 格式。
