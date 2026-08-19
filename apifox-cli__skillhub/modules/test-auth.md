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

1. 测试默认用**管理员账号**，普通账号权限问题不得误报接口 bug
2. token **必须自动获取/续期**，禁止手工复制粘贴 token 到用例
3. 前置脚本刷新失败时**阻断并提示**，不得用过期 token 硬跑并断言通过
4. 敏感值（token/密码/secret）不落回复、日志、`PROJECT_TEST.md`、聊天摘要
5. JWT 自签密钥只允许 local 配置里的密钥，禁止 test/prod 密钥
6. 每个需要鉴权的用例必须先确认其鉴权来源（全局认证/环境变量/前置脚本），不留"不知道 token 哪来"的用例
