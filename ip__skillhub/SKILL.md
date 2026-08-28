---
name: ip-query
description: "根据 IP 查询归属地与运营商类型（极速数据 JisuAPI）。当用户说「这个 IP 是哪里的」「是不是机房 IP」「查一下 IP 归属地/运营商」或询问 IP 地址位置信息时触发。触发词：IP查询、IP归属地、IP地址、运营商、机房IP、ip location、ip lookup。需要环境变量 JISU_API_KEY（极速数据 AppKey），无密钥时向用户说明获取渠道，禁止编造归属结果。"
license: MIT
metadata:
  displayName: "IP 地址归属查询"
  version: "1.1.0"
  openclaw:
    emoji: "📡"
    requires:
      bins: ["python3"]
      env: ["JISU_API_KEY"]
    primaryEnv: "JISU_API_KEY"
allowed-tools: Read, Write, Bash
---

# IP 归属查询（极速数据 JisuAPI）

根据 IP 地址查询其归属地与运营商类型。数据由极速数据（JisuAPI，jisuapi.com）提供。

## 前置配置：获取 API Key

1. 前往极速数据官网（jisuapi.com）注册账号。
2. 进入「IP 查询 API」页面，点击「申请数据」。
3. 在会员中心获取 **AppKey**。
4. 配置环境变量：

```bash
# Linux / macOS
export JISU_API_KEY="your_appkey_here"

# Windows PowerShell
$env:JISU_API_KEY="your_appkey_here"
```

## 脚本位置与调用

脚本位于**本 skill 目录**的 `ip.py`（纯标准库，仅需 python3，无第三方依赖）。从任意工作目录用绝对/相对路径调用：

```bash
python3 <本skill目录>/ip.py '{"ip":"122.224.186.100"}'
```

请求 JSON 格式：

```json
{
  "ip": "122.224.186.100"
}
```

## 工作流（3 步）

### 第 1 步：确认密钥与输入

- **输入**：用户提供的 IP 或查询意图。
- **动作**：确认 `JISU_API_KEY` 已设置（未设置时向用户说明获取渠道）；确认 IP 格式合法（IPv4 为主，IPv6 以 API 支持为准）。
- **输出**：密钥就绪 + 合法 IP 值。

### 第 2 步：构造并调用

- **输入**：合法 IP。
- **动作**：构造 `{"ip":"<ip>"}` 并调用 `python3 ip.py '{"ip":"..."}'`。
- **输出**：脚本返回的 JSON（`result` 字段或错误对象）。

### 第 3 步：解析与汇报

- **输入**：脚本返回 JSON。
- **动作**：成功时读取 `area`（省市）与 `type`（运营商），向用户总结；失败时按错误码分流说明。
- **输出**：归属地与运营商结论（或明确错误原因）。

## 请求参数

| 字段名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| ip | string | 是 | IP 地址 |

## 返回结果示例

成功（脚本输出接口的 `result` 字段）：

```json
{
  "area": "浙江省杭州市",
  "type": "电信"
}
```

失败（如没有该 IP 信息）：

```json
{
  "error": "api_error",
  "code": 201,
  "message": "没有信息"
}
```

## 边界条件与错误处理

- **密钥缺失**：输出 `Error: JISU_API_KEY must be set in environment.` 并退出码 1；向用户说明获取渠道，不编造结果。
- **IP 字段缺失**：输出 `'ip' is required in request JSON.` 并退出码 1。
- **JSON 解析失败**：输出 `JSON parse error` 并退出码 1。
- **无参数调用**：打印 Usage 并退出码 1。
- **API 业务错误**：按错误码如实回传（如 `101 APPKEY 不存在`、`201 没有信息`），不猜测替代结果。
- **网络失败**：回传 `request_failed` 与错误信息，建议稍后重试。

### 常见错误码

| 代号 | 说明 |
|------|------|
| 201 | 没有信息 |
| 101 | APPKEY 为空或不存在 |
| 102 | APPKEY 已过期 |
| 103 | APPKEY 无请求权限 |
| 104 | 请求超过次数限制 |
| 105 | IP 被禁止 |

## 职责边界（交叉引用）

- **免费公开 API 聚合查询**（天气/快递/日历等免密钥场景）→ `free-api-50`
- 本 skill 专注 IP 归属查询单项，数据源固定为极速数据。

## 退出机制

查询完成或用户输入「结束」→ 停止，回复查询结论；信息不足（IP 缺失、格式非法）时先补齐再查。

## 约束

- 无 `JISU_API_KEY` 或查询失败时**禁止编造归属地/运营商**，如实报告错误。
- 只查询用户明确给出的 IP；批量查询时逐条调用，不拼接伪造。
- 数据源为极速数据 API，结果以其返回为准。
