# case study：/getActivityExposure 联调 → 执行中 gap 回补（2026-08-21）

> 归属 owner：`apifox`。本文是「执行中 gap 回补通道」的样例：一次真实接口联调如何暴露 skill 缺口、缺口如何裁决落点、以及哪些经验**不该**进 skill。下次遇到"这个案例不错，吸收进 skill"时对照本文流程。

## 一、实战背景

| 项 | 内容 |
| --- | --- |
| 项目 | EllipalFinance-go（Go + Gin + GORM） |
| 接口 | `POST /api/swap/v2/getActivityExposure`（兑换活动曝光下发） |
| 特征 | **无 body 业务字段**，三个过滤维度全在请求头：gLang（文案语言）/ gVersion（版本灰度）/ 客户端 IP（地区白名单）；另有时间窗口与开关；只返回一条命中结果；候选集有 60 秒进程内缓存 |
| 结果 | 导入 spec（`createCount=1, ignoreCount=0`）→ 10 用例（正向 5 / 负向 2 / 边界 2 / 安全性 1）→ 43 条断言全绿 |
| 证据 | 项目内 `doc/5-tests/2026-08-21_160751_getActivityExposure接口apifox测试.md` |

## 二、暴露的 5 个 gap（按 gap-signals 判定，均非业务/工程问题）

| gap | 现象 | 缺口类型 | 阻断级 |
| --- | --- | --- | --- |
| 1 | `test-case.md` 把 `requestBody.data = {}` 一律判"无参测试=无效"，但本接口 schema `properties: {}` 就是真实契约 | 判定标准缺例外 | **是**（不补会把合法用例判无效，或反过来放行真空壳） |
| 2 | 规则 E-1 的特殊场景只覆盖"仅分页"，没说 header-only 接口怎么分层、L4 是否适用 | 流程不全 | 否 |
| 3 | `environment.md` 有端口探测三级链，但没有关停/重启核验 → 踩了"重启没生效仍全绿"的坑 | 闸门缺失 | 否（结果正确，但差一步就误判） |
| 4 | 没有"前置数据改完要确认缓存生效"的要求 | 判定标准缺失 | 否 |
| 5 | 没有"伪造来源头会同时改变鉴权判定"的提示 → 地区维度测不了，一度像接口 bug | references 不足 | 否 |

## 三、两个最有价值的坑（细节值得完整保留）

### 3.1 "重启过了"是假的：包装式启动派生子进程

`go run main.go -env apifox` 的真实进程是 `/tmp/go-build*/exe/main -env apifox`。用 `pkill -f 'main.go -env apifox'` 只杀掉 `go run` 父进程，端口仍被子进程占用；新实例启动即 `bind: address already in use` 后退出，日志在后台重定向文件里没人看。

**最危险的地方不是启动失败，而是测试照样全绿**——用例读到了新数据，于是"看起来重启生效了"。真实原因是服务端候选集缓存 TTL 60 秒到期后自动回库，与重启无关。若当时改的是代码而不是数据，就会得出"改动已验证"的错误结论。

落点：`environment.md`「服务重启与关停核验」（关停三步 + 包装式启动对照表 + 重启后必须验证改动真的生效）、不可违反规则第 15 条、`testing-pitfalls.md` 陷阱 32。

### 3.2 伪造来源 IP 测地区白名单，撞上内网免签

原计划 `X-Forwarded-For: <日本 IP>` 验证白名单放行，实测 `status=false, msg="Authorization failed"`。根因是鉴权免签判定 `isLocalIP(GetClientIPWithContext(c))` 与业务侧用**同一个**取 IP 函数，而它优先读 `X-Forwarded-For` —— 伪造公网来源等于同时离开免签分支。

处置示范（三步都保留在 skill 里）：把"伪造公网来源 + 无签名 → 被拒"固化成安全性用例（真实可断言）；该维度的**放行路径**登记为待补测（补法：前置脚本算 `md5(RequestURI+body+secret)`）；**拦截路径**用 fixture 优先级反向设计间接验证，不写成接口缺陷。

落点：`test-auth.md`「免签分支与来源头耦合」、`testing-pitfalls.md` 陷阱 22-1。

## 四、一个可复用的正向技巧：fixture 优先级反向设计

4 条数据覆盖 4 个维度，却不需要 4 组用例：

```
demo_activity        sort=10  无任何限制        ← 期望命中
apifox_gate_version  sort=50  min_version=99999
apifox_gate_region   sort=60  region=JP
apifox_gate_expired  sort=70  窗口已过期
```

闸门对照记录的 `sort` **刻意高于**期望命中记录：只要请求命中 `demo_activity`，就同时证明三个闸门都真的挡住了——否则 sort 更高的会抢先返回。

代价必须一起记住：断言失败时看不出是哪个闸门失效，因此**测试主文档必须写清这套 sort 设计意图**，否则后人会误以为"只断言一个 activityId = 覆盖不足"。落点：`test-data-and-judgement.md`「二之二」（含适用/不适用/代价）。

## 五、什么不该进 skill

- 项目侧事实：caseId / endpointId / 具体库地址 / `apifox` 库缺 v1 老表 → 留在项目 `PROJECT_TEST.md`。
- 规则本体重复：「联调后必须关闭并核验进程」的规则权威在 `test-strategy-rules`，本 skill 只补 apifox 域的**执行细节**并引用它，不复制规则句子。这是同域去重的正例。

## 七、续篇（2026-08-21 同日）：鉴权被整条跳过

上一段收口时用户提出一个更根本的问题——"没有配置鉴权的步骤，虽然代码是内网测试不走鉴权，但作为接口文档应该要完善才对；拿到接口上线之后也是要使用的"。

这是一个**因本地便利而系统性漏配**的典型：服务对内网来源免签（`isLocalIP` 覆盖 `10/8`、`172.16/12`、`192.168/16`、`127/8`），本地怎么测都 200，于是整条鉴权链路（接口文档的安全方案、apifox 鉴权组件、用例签名注入）全部没做。

查证后发现的问题比预想严重：

- **53 个 swag YAML 全量写着 `BearerAuth: {type: http, scheme: bearer}`**，而真实机制是 `Authorization = md5(RequestURI + 请求体原文 + 密钥)`（十六进制，`EqualFold` 比较，无 `Bearer ` 前缀）。按这份文档对接，线上 100% 401。**错的安全方案比缺失更危险**：缺失时对接方会来问，写错时对方会照着写然后怀疑服务端。
- 密钥有两套（来源 `H5` / `APP`），本地验证证明：无签名被拒、错误签名被拒、两套密钥都放行、大写签名兼容（`EqualFold`）、内网免签优先于签名。
- 顺带解开了上一段登记的两个待补测项：公网来源 + 正确签名后，地区白名单**放行**路径与图片态弹窗（style=2）都验证通过。

修法与落点：

1. 安全方案全量修正（53 个 YAML → `apiKey` / `in: header` / `name: Authorization` + 算法与免签例外说明），并把口径沉进 `swag-openapi-maintainer-rules`「核心约束」——它是生成侧真相源，只改产物下次生成还会写错。
2. apifox 侧：鉴权组件由导入自动创建（`ApiSignAuth`），10 个既有用例统一注入签名前置脚本，新增 2 个签名安全性用例。
3. 落 `modules/test-auth.md`「鉴权配置必须进 apifox」：三件事齐（安全方案 + 用例签名脚本 + 鉴权用例）、凭据红线（agent 不代填）、签名脚本模板、两条 CLI 事实。

### 两条 CLI 事实（都是"报成功但没生效"）

- `environment update` 带 `variables` 返回 `success=true`，回读恒为 `null`——**CLI 2.2.9 读写不到环境变量**，只暴露 `baseUrls` 与 `parameters`。密钥类变量只能人工在客户端填；顺带修正了 `modules/environment.md` 原先"值写入 apifox 环境变量时用 CLI 写入"这条**做不到的存量规则**。
- 导入 OpenAPI 的 operation-level `security` 不会绑定到 apifox 接口：导入后 `endpoint get` 的 `securityScheme` 是 `{}`，`apifox export` 出来的 `security` 也是 `[]`。鉴权组件是独立资源，接口关联需人工点选；`endpoint update` 的 `securityScheme` 字段 CLI 无结构定义，**不猜着写**。

### 一个差点误报的坑（最值得记）

批量跑用例时用 `grep -c '√'` 与 `grep -c '×'` 统计，得出"12 个用例 fail=0"——**是假的**。apifox runner 报告里通过的断言前缀是 `√`，失败的却是 `1. 2. 3.` 编号，`×` 恒为 0。真实结果是 51 条断言 7 条失败（3 条文案断言 + 4 条待填密钥）。

正确口径是解析报告表格的「断言数 总数 / 失败数」两列，并且**先用一个已知会失败的用例校准统计脚本**再信它。已落 `modules/testing-pitfalls.md` 陷阱 12-1 与 `modules/test-case.md` 运行规则。

那 3 条文案断言失败也不是接口缺陷：Mongo 账号对被改过的库名 `ellipal_swap` 无权限（`not authorized`），业务代码对"取不到文案"的处理是记日志后继续，于是文案静默降级成空串。属 `ENV_BLOCKED`，把 apifox 测试配置指回有权限的库后 11/12 用例通过。已落陷阱 18-2：**断言从通过变失败而请求侧没改动时，先看服务日志，别急着改断言**。

## 六、体积与验证

- 新增约 78 行，整理删除约 15 行（`environment.md` A2 节与端口探测三级链重复的命令块收敛为引用），改写 1 条（pitfalls #23）→ 本次净增约 63 行。
- 同域冗余扫描：8 个关键词扫 5 个兄弟 skill，仅 1 处规则权威命中并已收敛为引用，其余零命中 → PASS。
- 棘轮验证与评分见 `../workbuddy-absorption-map.md` 2026-08-21 段。
