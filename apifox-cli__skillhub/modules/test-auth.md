# 鉴权自动化：token/Authorization 获取、续期与注入（强制）

> 归属 owner：`apifox`。本模块解决接口测试中最常见的权限类问题：**登录需要用户名密码的系统（token / JWT / Authorization 鉴权）时，token 过期快、手工拿 token 麻烦、权限不足**。目标：让 apifox 用例**自动获得有效鉴权，全程不手工复制 token**。
>
> 前置依赖：项目须已登记 Apifox 项目与开发环境（见 `modules/ai-team-project.md`）；开发环境环境变量（登录账号/token）须已配置（见 `modules/environment.md`「开发环境环境变量（强制）」节）。

## 何时加载

- 接口需要登录后访问（401/403/token 无效/签名错误频繁出现）
- 用户要求"测试前自动登录""不要手工填 token""token 过期了怎么办"
- 有 securityScheme（Bearer/JWT/Basic）的项目补测试用例
- 上线门禁/回归/批量测试需要稳定鉴权

## 核心原则

1. **测试默认用管理员账号**（local 环境的管理员用户名/密码），权限最全、最方便测试——普通账号权限不足导致的 403 不是接口 bug，是测试账号选错
2. **token 必须在测试流程内自动获取**，禁止手工复制 token 粘贴到用例
3. **token 过期必须自动续期**，不能要求人守着刷新
4. **敏感值不落文档/日志**：token、密码只存在 apifox 环境变量，`PROJECT_TEST.md` 只登记名称/用途/来源

## 方案选型（按优先级）

| 方案 | 适用场景 | 自动化程度 | 推荐 |
|------|---------|-----------|------|
| A. 登录用例 + extractor 提取 | 常规 token（有效期较长） | 半自动（登录用例先跑一次） | ✅ 默认 |
| B. 前置脚本自动续期（preProcessor） | **token 过期快（分钟级/小时级）** | 全自动（每次请求前自动刷新） | ✅✅ 强烈推荐 |
| C. 本地脚本构造 token | 登录接口慢/有限流、JWT 可自签、批量预取 | 全自动（脚本生成→写环境变量） | 条件适用 |
| D. Apifox 全局身份认证 | 项目统一 Bearer/基础认证 | 全自动（平台级注入） | 优先启用 |

> **选择判断**：token 有效期 ≥ 1 小时且用例量小 → A；token 有效期 < 1 小时或批量跑 → **B**；JWT 自签/登录接口不稳 → C；项目所有接口统一一种鉴权 → 先启用 D 再看是否需 A/B/C 兜底。

---

## 方案 A：登录用例 + extractor 提取（默认）

**原理**：建一个「登录获取 Token」用例（管理员账号），后置 extractor 把 token 提取到环境变量，其他用例请求头引用 `{{token}}`。

1. **创建登录用例**：POST 登录接口，requestBody 用开发环境变量（`{{testUsername}}` / `{{testPassword}}`），断言 200 + 业务码
2. **后置 extractor**（`shareScope=PROJECT`，见 `modules/test-case.md` 处理器结构）：

```json
{
  "id": "postProcessors.0.extractor",
  "type": "extractor",
  "data": {
    "variableName": "token",
    "variableType": "globals",
    "shareScope": "PROJECT",
    "subject": "responseJson",
    "expression": "$.data.token"
  },
  "defaultEnable": true,
  "enable": true
}
```

> `expression` 按登录接口真实响应路径调整（如 `$.data.accessToken`、`$.data.jwt`）。

3. **其他用例请求头**：`Authorization: Bearer {{token}}`
4. **运行顺序**：先跑登录用例（写 token）→ 再跑业务用例；套件中把登录用例放最前（`test-scenario` 编排见 `modules/test-scenario.md`）

**局限**：token 过期后需重跑登录用例。**过期快的系统必须升级方案 B。**

---

## 方案 B：前置脚本自动续期（token 过期快场景，强制推荐）

**原理**：在每个需要鉴权的用例加 **preProcessor（前置处理器）customScript**——请求发出前检查 token 是否过期，过期则自动调用登录接口刷新并写回环境变量。**用户无感，每次跑都自动有效。**

### B1. Apifox 前置处理器结构（test-case）

```json
{
  "preProcessors": [
    {
      "id": "preProcessors.0.customScript",
      "type": "customScript",
      "data": "// 检查 token 是否过期，过期自动重登（脚本见下）",
      "defaultEnable": true,
      "enable": true
    }
  ]
}
```

> ⚠️ `preProcessors` 与 `postProcessors` 是同级字段。创建/更新用例时两者都带，`update` 是整体覆盖，必须保留原有 postProcessors。

### B2. 自动续期脚本模板（customScript，Postman/Apifox 兼容）

```javascript
// token 自动续期：请求前检查 JWT 过期时间，快过期则用管理员账号重登
// 依赖环境变量：token / testUsername / testPassword / loginUrl

function getJwtExp(token) {
  try {
    var payload = token.split('.')[1];
    var json = JSON.parse(atob(payload.replace(/-/g, '+').replace(/_/g, '/')));
    return json.exp ? json.exp * 1000 : null; // JWT exp 是秒
  } catch (e) { return null; }
}

var token = pm.environment.get('token');
var needRefresh = true;

if (token) {
  var exp = getJwtExp(token);
  // 距过期 < 5 分钟就刷新（可调；非 JWT 无法解析时改为检查 401 后重试）
  if (exp && exp - Date.now() > 5 * 60 * 1000) { needRefresh = false; }
}

if (needRefresh) {
  var login = {
    url: pm.environment.get('loginUrl'), // 如 http://127.0.0.1:8080/api/v1/login
    method: 'POST',
    header: { 'Content-Type': 'application/json' },
    body: {
      mode: 'raw',
      raw: JSON.stringify({
        username: pm.environment.get('testUsername'),
        password: pm.environment.get('testPassword')
      })
    }
  };
  pm.sendRequest(login, function (err, res) {
    if (!err && res.code === 200) {
      var body = res.json();
      var newToken = body.data && (body.data.token || body.data.accessToken || body.data.jwt || body.token);
      if (newToken) {
        pm.environment.set('token', newToken);
      }
    } else {
      console.log('token refresh failed: ' + (err ? err.message : res.code));
    }
  });
}
```

> **要点**：
> - `pm.environment.set` 写入后**同一次请求的请求头 `{{token}}` 是否能立即生效**取决于 Apifox runner 的变量求值时机：若不可立即生效，改为"上一用例刷新 token、下一用例使用"，或在测试场景中先放一个"刷新 token"步骤
> - 非 JWT token（opaque token）无法解析 exp → 改策略：前置脚本先调一个轻量"检查 token 有效性"接口（如 `/auth/check` 或用户信息接口），401 才刷新；或依赖场景第一步重登
> - 登录接口返回结构不一致时，调整 `body.data.token` 取值路径

### B3. 场景级续期（test-scenario，更稳）

在测试场景开头固定放一个「刷新 token」步骤（登录用例或脚本步骤），后续步骤全部引用 `{{token}}`；每次跑场景都先刷新，避免逐用例重复登录：

```text
[场景] 登录→业务
  步骤1: 登录获取 token（extractor 写 PROJECT 变量）
  步骤2..N: 业务用例（Authorization: Bearer {{token}}）
```

> 场景编排细节见 `modules/test-scenario.md`；若场景步骤支持脚本步骤，可在步骤1用 customScript 替代登录接口（复用 B2 脚本逻辑）。

---

## 方案 C：本地脚本构造 token（条件适用）

**适用**：JWT 可用密钥自签（无需打登录接口）；登录接口限流/响应慢；需要批量预取 token 写入 apifox 环境变量。

### C1. JWT 自签脚本（Python 示例，写入 apifox 环境变量）

```python
# jwt_gen.py — 用项目密钥自签测试 token（仅 local 测试用）
import time, json, base64, hmac, hashlib

SECRET = "local-test-secret"  # 只允许 local 配置里的密钥
HEADER = {"alg": "HS256", "typ": "JWT"}
PAYLOAD = {
    "sub": "admin",           # 默认管理员
    "role": "admin",
    "iat": int(time.time()),
    "exp": int(time.time()) + 3600,
}

def b64(d): return base64.urlsafe_b64encode(json.dumps(d, separators=(',', ':')).encode()).decode().rstrip('=')

h, p = b64(HEADER), b64(PAYLOAD)
sig = base64.urlsafe_b64encode(hmac.new(SECRET.encode(), f"{h}.{p}".encode(), hashlib.sha256).digest()).decode().rstrip('=')
print(f"{h}.{p}.{sig}")
```

```bash
# 生成后写入 apifox 环境变量（CLI；值不回显到聊天）
TOKEN=$(python jwt_gen.py)
apifox environment update --project <projectId> --environment <开发环境Id> --set-variable token="$TOKEN"
```

### C2. 登录接口脚本（用管理员账号批量拿 token）

```bash
# login_token.sh — 调本地登录接口拿管理员 token，写入 apifox 环境变量
TOKEN=$(curl -s -X POST http://127.0.0.1:8080/api/v1/login \
  -H 'Content-Type: application/json' \
  -d '{"username":"admin","password":"<local-password>"}' | python -c "import sys,json;print(json.load(sys.stdin)['data']['token'])")
apifox environment update --project <projectId> --environment <开发环境Id> --set-variable token="$TOKEN"
```

> 具体 CLI 参数以 `apifox environment --help` / `cli-schema get environment-update` 为准（skill「CLI 事实优先」）。

---

## 方案 D：Apifox 全局身份认证（优先启用）

- Apifox 项目支持配置**全局身份认证**（Bearer Token / Basic / API Key），对所有请求自动注入 `Authorization` 头
- 项目统一鉴权时**优先启用**，避免每个用例手工加头
- 启用方式：Apifox 客户端「项目设置 - 认证设置」配置；CLI 侧确认对应 schema 是否可配
- 与方案 A/B 的关系：D 解决"统一注入"，A/B 解决"token 从哪来、过期怎么办"——**D + B 组合最稳**（D 注入头，B 保 token 新鲜）

---

## 管理员账号约定（强制）

- **测试默认使用管理员账号**：权限最全，避免普通账号 403 误报为接口 bug
- 管理员账号密码只存 apifox 开发环境变量（`testUsername`/`testPassword`），值不落文档/日志
- 若 local 环境无管理员账号数据：先向用户确认管理员账号与 local 密码，不要猜测
- 需要验证权限边界时**另建普通账号用例**（负向），默认正向全用管理员

## 鉴权配置必须进 apifox（强制，即使本地免签）

> **本地免签 ≠ 不需要鉴权配置**。很多内部服务对内网来源免签，于是本地联调时"什么都不配也能 200"，鉴权就被整条跳过——接口文档里没有正确的安全方案、apifox 用例里没有签名/凭据。**这份文档一交出去，对接方按它写，上线必 401**。接口文档与用例必须反映线上真实调用方式，而不是本地便利路径。

**每个走鉴权的接口，三件事必须齐（缺一即视为接口未真正落地）**：

| # | 事项 | 判定标准 |
|---|------|----------|
| 1 | apifox 有**与真实机制一致**的鉴权组件 | `apifox security-scheme list/get` 能查到；`authConfigs` 的 type/in/name 与服务端实际校验方式一致；description 写清算法、参与签名的字段、密钥来源、免签例外 |
| 2 | 用例带鉴权（签名/token）注入 | 用例 `preProcessors` 有鉴权脚本；本地免签时脚本可在凭据缺失时跳过，但**脚本本身必须在**，保证"用例即线上调用示例" |
| 3 | 至少一组鉴权用例 | 正确凭据放行 + 缺失凭据被拒 + 错误凭据被拒（后两者不需要真实密钥，可立即通过） |

**先把真实机制查清，再配 apifox**（不要照抄"Bearer token"这类默认假设）：

```bash
# 鉴权中间件读哪个头、怎么算、密钥从哪来
grep -rn "Header.Get(\"Authorization\")\|md5.Sum\|hmac\|EqualFold" middleware/ internal/middleware/ 2>/dev/null
# 免签分支的判定范围（哪些来源不校验）
grep -rn "isLocalIP\|bypass\|whitelist" middleware/ 2>/dev/null
```

自定义签名（如 `md5(RequestURI + body + secret)`）**不是** `type: http, scheme: bearer`，而是 `type: apiKey, in: header, name: Authorization`。写错会让对接方按 `Authorization: Bearer xxx` 发请求，必然失败——真实案例见 `references/case-getactivityexposure-gap-backfill.md` 第七节。

### 凭据处理红线（强制）

- **agent 不把密钥/token 值填进 apifox**（apifox 是云端 SaaS，且"把凭据输入任何字段"属禁止操作）。agent 只做两件事：建**空值占位变量**、写**运行时取值的脚本**；真实值由用户在 apifox 客户端自行填入。
- 需要在本地验证签名算法时，让脚本自己从项目配置/源码读密钥并计算，**明文不进 agent 输出、不进文档、不进聊天摘要**（与 `modules/environment.md` 敏感变量规则一致）。
- 签名脚本里禁止写死密钥；必须 `pm.environment.get("<变量名>")` 运行时取，取不到就跳过（本地免签仍可跑通），并在用例名或说明里标注"需环境变量 X"。

### 签名前置脚本模板（自定义 md5 签名）

```javascript
// 线上调用必须带签名: Authorization = md5(RequestURI + 请求体原文 + 密钥)
// 密钥取自环境变量 authSecret（需在 apifox 客户端为开发环境填入，脚本内不落明文）
// 未配置时跳过: 本地内网来源本身免签，用例仍可正常跑通
var secret = pm.environment.get("authSecret");
if (secret) {
  var sign = CryptoJS.MD5("/api/xxx/yyy" + "{}" + secret).toString();
  pm.request.headers.add({ key: "Authorization", value: sign });
}
```

### 两条 CLI 事实（2026-08-21 于 apifox-cli 2.2.9 实测）

| 事实 | 影响与对策 |
|------|-----------|
| **environment 读写不到环境变量**：`environment get` 只返回 `id/name/projectId/baseUrls/parameters`；带 `variables` 的 `environment update` 报 `success=true` 但回读恒为 `null` | 密钥类变量**只能人工在客户端添加**。CLI 侧不要反复重试或猜字段；把"需在客户端添加变量 X"写进项目 `PROJECT_TEST.md`「环境变量登记」表。运行时 `pm.environment.get()` 不受此限制（那是 runner API，与 CLI 读写无关） |
| **导入 OpenAPI 的 operation-level `security` 不会绑定到接口鉴权**：导入后 `endpoint get` 的 `securityScheme` 为 `{}`，`apifox export` 出来的 `security` 也是 `[]`；鉴权组件是独立资源 | 鉴权组件会由导入自动创建（可 `security-scheme list` 查到），但**接口与组件的关联需人工在客户端点选**。`endpoint update` 的 `securityScheme` 字段 CLI 未给出结构定义，**不要猜着写**，以免损坏接口定义 |

## 免签分支与来源头耦合（强制先查）

很多内部服务对**内网来源免签**（判定形如 `isLocalIP(getClientIP(request))`），而取客户端 IP 的公共函数通常**优先读 `X-Forwarded-For`，其次 `X-Real-IP`，最后才是 `RemoteAddr`）。这带来一个容易误判的耦合：

**只要用请求头伪造来源 IP 去测业务维度（地区白名单、区域灰度、IP 风控、按来源分流），就会同时离开免签分支**——请求转为"外网来源"，必须带签名/凭据，否则直接被鉴权拒绝。表现是那个业务维度"怎么测都不通"，看起来像接口 bug。

进入这类测试前先查两件事：

1. 鉴权中间件与业务代码**是不是同一个取 IP 函数**（`grep` 免签判定与业务侧的 IP 获取调用）。是 → 存在耦合。
2. 该服务的签名算法与密钥来源（常见 `md5(url + body + secret)` / HMAC，密钥可能硬编码在中间件或 local 配置里）。

处置（按可行性排序）：

- **能拿到密钥** → 按方案 C 思路在前置脚本里算签名（`md5(RequestURI + body + secret)`），配合伪造来源头，即可测通该维度的放行路径；密钥只从 local 配置取，值不落文档。
- **拿不到密钥或成本过高** → 把"伪造公网来源 + 无签名 → 被拒"固化成**安全性用例**（真实可断言，顺带验证鉴权边界），并把该业务维度的**放行路径登记为待补测**；拦截路径可用 `modules/test-data-and-judgement.md`「fixture 优先级反向设计」间接验证。
- **任何情况下都不要**把"伪造来源被鉴权拦下"写成接口缺陷，也不要为了绕过鉴权去改生产代码（测试隔离红线）。

## 排查指引（401/403/签名错误）

| 现象 | 优先检查 | 处理 |
|------|---------|------|
| 401 Unauthorized | token 缺失/过期 | 跑方案 B 前置脚本或场景步骤 1 刷新 token；核对 `PROJECT_TEST.md`「环境变量登记」表 |
| 403 Forbidden | 账号权限不足 | 换管理员账号（`testUsername`/`testPassword`）；确认当前 token 对应账号角色 |
| 签名错误（invalid signature） | apiKey/apiSecret 过期或与请求参数不匹配 | 核对开发环境变量 apiKey/apiSecret；确认签名算法/时间戳参数一致 |
| token 无效（invalid token） | JWT 过期或密钥不匹配 | 方案 B 自动续期；方案 C 重新自签 |
| 部分接口 401 部分正常 | 该接口需独立鉴权（内部接口/micro 服务） | 单独为该接口配置鉴权变量，排查其 token 来源 |

> 判定红线：401/403/签名错误**优先归因环境变量/鉴权配置**，不要先怀疑接口代码（与 `modules/test-data-and-judgement.md` 阻断分类一致）。

## 不可违反规则

0. **本地免签不免鉴权配置**：接口文档的安全方案、apifox 鉴权组件、用例签名脚本三件事必须齐，且与服务端真实校验方式一致；自定义签名不得写成 `http bearer`
1. 测试默认用**管理员账号**，普通账号权限问题不得误报接口 bug
2. token **必须自动获取/续期**，禁止手工复制粘贴 token 到用例
3. 前置脚本刷新失败时**阻断并提示**，不得用过期 token 硬跑并断言通过
4. 敏感值（token/密码/secret）不落回复、日志、`PROJECT_TEST.md`、聊天摘要
5. JWT 自签密钥只允许 local 配置里的密钥，禁止 test/prod 密钥
6. 每个需要鉴权的用例必须先确认其鉴权来源（全局认证/环境变量/前置脚本），不留"不知道 token 哪来"的用例
