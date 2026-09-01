# 接口测试用例 — test-case / test-data

> 本模块覆盖接口测试用例和测试数据集管理。已从 SKILL.md 继承：写入标准流程、分支参数规则。

## 何时加载

- 创建/更新/删除/查看接口下的测试用例
- 管理测试步骤、断言、提取变量、前后置处理器
- 管理测试数据集（test-data）
- 排查"测试步骤无法展示""断言不生效""提取变量为空"
- 按 caseId、endpointId、categoryId 运行测试用例

## 不应使用

- 多接口流程编排 → 加载 `modules/test-scenario.md`
- 运行套件/CI → 加载 `modules/test-automation.md`
- 只改接口定义 → 加载 `modules/api-design.md`

## 核心概念

| 概念 | CLI 资源 | 说明 |
|------|----------|------|
| 接口测试用例 | `test-case` | 绑定接口 endpoint 的测试数据与步骤 |
| 测试分类 | `test-case category` | 创建 case 前用于获取有效 `categoryId` |
| 测试数据集 | `test-data` | 可供迭代运行的数据 |
| 接口定义 | `endpoint` | case 的依赖对象，不等同 case |

## 两类用例是两套资源（强制区分，2026-08-24 实测修正）

> **本节此前的论断是错的**：原文写"接口树里接口下方的成功/失败子项 = 接口用例（test-case）""不存在把测试用例复制到调试用例这个操作"。实测证明接口树下的子项与 CLI `test-case` **是两套独立资源**，按原论断做参数完整性校验会得出**假通过**——CLI 侧全绿，用户在客户端点开接口看到的却是空 body。

| | 调试用例（接口树下） | 自动化测试用例 |
|---|---|---|
| 客户端位置 | 接口管理 → 接口下方的「成功」等子项 | 自动化测试 → 正向/负向/边界值分类 |
| 导出结构 | `api.cases[]`，`type=DEBUG_CASE`，`categoryId=0` | `apiTestCaseCollection` |
| CLI 可见 | ❌ `test-case list --endpoint` **拿不到** | ✅ |
| CLI 可写 | ❌ 见下方「CLI 能力边界」 | ✅ `test-case create/update` |
| body 来源 | 只在 `import` 时按 OpenAPI 的 example 生成 | 由 `test-case create` 的 `requestBody.data` 写入 |

**CLI 能力边界（逐条实测，别再试）**：

- `endpoint get` 返回里**没有 `cases` 字段**，读不到调试用例
- `endpoint-update` 的 schema **不含 `cases` / `DEBUG_CASE`**，写不了调试用例
- `endpoint update` 写 `requestBody.example` → **报 `success: true` 但回读为空**（与 environment variables 同型的假成功，见 `modules/environment.md`）
- **但有一条隐藏通道（2026-08-26 实测）**：`import --format apifox` 用**原生导出文件 + match-name 模式**重导时，已存在接口的 **`api.cases[]`（DEBUG_CASE）会执行 update 语义**——`preProcessors`/`postProcessors` 等用例字段**真实落库**（实测 66 接口 endpointCase updateCount=138 全命中，重导后回读 66/66 脚本在）。接口契约字段（name/path/method/securityScheme/parameters/requestBody/responses）全部保留；唯一副作用是 `ordering` 归零（仅显示排序重置，无契约影响）。
- 结论修正：**DEBUG_CASE 的处理器（preProcessors/postProcessors）事后可经「导出 → 改 JSON → match-name 重导」批量补齐**；但 **body 示例仍只能在 `import` 时经 example 灌入**（重导不改 `requestBody.data`）。body 缺失的已存在接口仍走删接口重导（规则 T-3）或客户端「自动生成」。

**因此验收要分两路**（只查一路即为假通过）：

1. 自动化测试用例 → `test-case get` 对账 endpoint schema（见「参数完整性校验」节）
2. 调试用例 → `export --format apifox` 查 `api.cases[].requestBody.data` 是否非空（见规则 T-3）

**仍然成立的部分**："保存的请求"（`history` 资源）是账号维度私有、其他成员不可见、且 CLI 只读（仅 list/get，无 create）；团队共享的调试例子应落为接口下的调试用例，而非请求历史。`branch pick-to` 的 `--include-endpoint-cases` 指的就是调试用例。

## 命令入口

```bash
apifox test-case --help
apifox test-data --help
```

具体参数以当前 CLI help 为准。

## 创建测试用例标准流程

> 收口目标：在 apifox「自动化测试」菜单的 正向 / 负向 / 边界值 / 安全性 / 其他 分类下，每接口在「正向/负向/边界值」三个分类下都有用例，且正向上覆盖业务参数（非仅分页），POST 等非 GET 接口有完整覆盖。详见 `modules/test-case-generation.md` 的「覆盖度铁律」。

0. **创建前自检覆盖度（强制）**：先用 `test-case list --endpoint <endpointId>` 拉取当前接口下已有用例，按 正向 / 负向 / 边界值 三维列出缺口（POST/PUT/PATCH/DELETE 接口必须有 0→完整 的覆盖推进），缺口先呈现给用户确认后再继续
1. 确认项目和分支（参见 `modules/ai-team-project.md` 的「首轮必须指明 → 持久化」规则）
2. 定位 endpoint：`apifox endpoint list/get`
3. **必须执行** `apifox test-case category --project <projectId>` 获取有效 `categoryId`
4. 如有类似 case，先 `test-case list --endpoint <endpointId>` 再 `get` 一个作为模板
5. 获取 `test-case-create` schema 并校验
6. 构造完整 JSON（不要只写空壳 name/endpointId）
7. **参数完整性校验（强制）**：创建后立即 `test-case get <caseId>`，对照 `endpoint get <endpointId>` 的 schema 校验参数完整性（见「参数完整性校验（强制）」节）——**接口有参但用例无参 = 用例无效**，缺参必须补全后才能继续
8. 运行一次确认 requestBody、处理器、断言和脚本在 runner 中生效

> `categoryId` 是前端展示测试用例的**关键必填字段**。无效 `categoryId` 可能导致 CLI 能看到但客户端不可见。

## 参数完整性校验（强制）

> **核心原则**：接口需要参数，测试用例就必须带参数。**接口有参但用例无参 = 无效测试**，禁止宣称"测试通过"。生成侧覆盖规则见 `modules/test-case-generation.md` 规则 B/C/E/E-1，本节是落地校验闸门。

**「无参测试」判定**（任一命中即用例无效）：
- 接口 endpoint schema 定义了 query/path/body 参数，而用例 request 对应位置为空
- POST/PUT/PATCH 接口定义了 requestBody schema，而用例 `requestBody.data` 为空、为 `{}` 空壳、或遗漏任何必填字段
- 接口有业务参数但用例只带了分页参数（page/size），业务参数全部缺失（不符合规则 E/E-1）

**唯一例外：header-only 接口（强制按证据判定，不得凭 body 形状下结论）**

有的 POST 接口**本身没有 body 业务字段**，全部业务维度走请求头（语言、版本灰度、来源 IP、租户标识等）。此时 `requestBody.data` 为 `{}` 是**真实契约**，不是空壳违规——判定依据是 **schema 有没有必填字段**，不是 body 长什么样。

判定步骤（三条同时成立才认定为合法 header-only）：

1. `endpoint get <endpointId>` 显示 requestBody 对应 schema 的 `properties` 为空对象（`{}`）且无 `required`；
2. 该接口 `parameters.header` 非空，且其中存在承载业务语义的头（不只是 `Content-Type`、`Accept` 这类协议头）；
3. 用例的 `parameters.header` 已按规则 E-1 覆盖关键请求头（L1 逐个关键头 + 一个全头满配用例）。

三条任一不成立 → 仍按「无参测试」判无效。反例：接口 schema 明确有 3 个必填 body 字段，用例传 `{}` —— 这是空壳违规，不能借 header-only 例外放行。

> 与规则 T-1 的关系：header-only 接口的 `{}` 依然要走 `pretty_jsonb()`（`{}` 本身即最小合法形态），T-1 检查的是"多字段 JSON 有没有被压成一行"，不是"body 能不能为空"。

**双重闸门（创建校验 + 运行判定）**：

1. **创建/更新后校验（阻断）**：`test-case get <caseId>` 读取用例真实保存结构，与 `endpoint get <endpointId>` 的 schema 对账：
   - **必填参数一个不能少**（query/path/body 的 required 字段全部带上）
   - **关键业务参数按规则 E-1 覆盖**（L1 单参数 / L2 两两 / L3 全参数 / L4 过滤×分页；可选参数按 E-1 关键参数定义纳入，纯展示参数不强制）
   - **POST/PUT/PATCH 用例 `requestBody.data` 必须保留接口 schema 中的全部必填字段**，禁止删成空 body 或 `{}` 空壳
   - 校验不通过 → **阻断**：先补全参数再继续，禁止在缺参状态宣称"用例已建好"

2. **运行后判定（不通过）**：用例真实运行后，若接口 schema 有参数但该用例 request 无参/缺必填 → 该用例判定为**「不通过/无效」**，测试结果不计入通过；必须补全参数后重跑

**POST body JSON 专项（强制）**：
- body 中的 JSON 参数必须**保留在用例中**，不得删除、清空或替换为 `{}`；遗漏任何必填字段即视为无效用例
- `requestBody.data` 必须是包含完整参数的 JSON 字符串（用 `\n` 转义多行），不要把 JSON Body 写成对象

## 规则 T-1：JSON body 格式化（强制）

> 防止 JSON 单行压缩不可读（如图 2）。所有写入用例 `requestBody.data` 的 JSON 必须 **pretty-print**（2 空格缩进），便于在 apifox 编辑器中人工对比与维护。生成侧规则同步进 `project-onboarding-checklist.md` 节点 2 → A5。

**判定标准**：
- `requestBody.data` 必须是**带缩进的格式化 JSON 字符串**（每个字段逐行排列），不是单行压缩字符串
- 缩进按 apifox 编辑器默认 `2 空格`
- 中文字段值不被转义（`ensure_ascii=False`）

**CLI 写入小工具**（在脚本中复用，避免手工拼字符串出错）：
```python
import json

def pretty_jsonb(data: dict) -> str:
    """用于写入 apifox test-case requestBody.data（必须返回带 \\n 的字符串）"""
    s = json.dumps(data, indent=2, ensure_ascii=False)
    # apifox 的 data 字段是 JSON 字符串，所以 \n 必须保留为字面量
    return s

# 例：data = pretty_jsonb({"channel": "APIFOXTEST", "name": "策略-启用", "value": 0.035})
# 输出：
# {
#   "channel": "APIFOXTEST",
#   "name": "策略-启用",
#   "value": 0.035
# }
```

**不通过则阻断**：
- 单行压缩（如图 2 中 `{"channel":"APIFOXTEST","name":"apifoxtest-策略-启用",...}`）→ 必须先格式化再写入，否则禁止声称用例已建好
- 在测试用例审计（`project-onboarding-checklist.md` 节点 2 → A5）中识别出未格式化 → 阻断并提示用 `pretty_jsonb` 修正

**应用时机**：
- 步骤 6 构造完整 JSON 时，所有 `requestBody.data`、`examples.data`、`expected response.data` 都按此规则格式化
- 现有未格式化用例批量修复 → 见 `project-onboarding-checklist.md` 「现有项目批量修复命令集」节第 3 项

## 规则 T-2：Mock 200 响应示例真实性（强制）

> 防止 Mock 的"成功"示例与请求无关（如图 3：200 示例 body 是 `{}` 空壳）。Mock 必须让开发者一眼看出"调通后接口长什么样"，否则示例拖慢用户理解且无任何验证作用。

**判定标准**（任一命中即 Mock 示例无效）：
- 200/201 响应示例的 `examples[*].data` 或 `responses[*].examples[*].data` 为 `{}` 空壳
- 响应示例字段少于接口 schema 的必填响应字段
- 响应示例与请求参数**完全无关**（不能反映「请求 X → 响应 Y」的语义对偶）

**通过标准**：
- 200 响应示例必须含接口 schema 中**全部必填响应字段**，且数据合理（ID 非空、时间字段为真实格式、枚举值为合法值）
- 示例数据应能让前端/后端开发者直接拿来做对接参考

**CLI 修复路径**：
- **接口创建/导入时**就按 schema 把真实示例写进 OpenAPI（参考 `test-case-generation.md` 的「schema 驱动数据构造规则」表）——这是唯一可靠时机
- ⚠️ **不要指望 `endpoint update` 补示例**：实测写 `requestBody.example` 报 `success: true` 但回读为空（2026-08-24）。响应示例侧同理，回写后必须用 `export --format apifox` 回读确认，不能只看 update 的返回
- 已存在接口的空壳示例只能删除，或按规则 T-3 删接口重导

**不通过则阻断**：
- 创建用例/同步接口时若检测到 Mock 示例空壳 → 必须删除空壳或补全数据，不允许保留 `{}` 占位
- 审计（`project-onboarding-checklist.md` 节点 2 → A6）中识别出空壳 → 阻断并提示修复路径

**应用时机**：
- 节点 2（创建/更新用例）时同步校验 Mock
- 现有空壳示例批量修复 → 见 `project-onboarding-checklist.md` 「现有项目批量修复命令集」节第 4 项

## 规则 T-3：调试用例请求示例（强制，2026-08-24 新增）

> 防止「自动化测试用例全绿、但对接方点开接口只看到空 body」。调试用例是对接方理解接口的第一入口，空 body 等于没有示例。

**example 必须放 MediaType 层级——这是本规则的关键，放错位置静默无效**：

```yaml
requestBody:
  content:
    application/json:
      schema:                    # ← 放 schema.example 无效！实测重导后 0/5 仍为空
        type: object
        properties:
          id: {type: integer, description: 主键, example: 1}   # 字段级 example 另有用途，不能替代下面这个
      example:                   # ← 必须放这里（MediaType 层级，与 schema 同级），实测 5/5 生效
        id: 1
        enabled: 1
```

OpenAPI 规范里 `MediaType.example` 与 `Schema.example` 都合法，**apifox 生成调试用例 body 时只认前者**。

**判定标准**（任一命中即不通过）：

- `export --format apifox` 里该接口 `api.cases[].requestBody.data` 为空串
- OpenAPI 的 requestBody 缺 `content."application/json".example`
- example 只写在 `schema.example` 或仅字段级 `properties.*.example`

**通过标准**：每个有 body 的接口，`api.cases[]` 中至少一个 `DEBUG_CASE` 的 `requestBody.data` 非空，且内容是可直接发送的合法请求（必填字段齐全、枚举值合法）。

**已存在接口的修复路径**（body 补不了，只有两条路；处理器类字段另有第三条）：
  - 补 **body 示例**（`requestBody.data`）：
    1. **删接口重导**（可自动化）：`endpoint delete` → 用带 example 的 YAML `import` → 重新绑定 securityScheme → **重建该接口下的测试用例**（endpointId 会变，旧 caseId 全部失效）→ 重跑回归。破坏性操作，**apifox 测试专用项目内默认放开**（豁免见 `SKILL.md` 门控与确认清单）；非测试专用项目执行前须用户确认。
    2. **用户在客户端点「自动生成」**：零风险、不动任何 ID，但需人工逐接口点击。
  - 补 **preProcessors/postProcessors 等用例处理器**（2026-08-26 实测）：
    3. **原生导出 → 改 JSON → match-name 重导**：`export --format apifox` 全量导出 → 脚本改 `api.cases[]` 各 DEBUG_CASE 的 `preProcessors` → `import --project <id> --format apifox --file <json> --module-import-mode match-name`（模块冲突时加 `--module-map "source:<源>=<目标>"`）→ 导出回读验证。接口契约字段全保留、用例脚本真实落库，**不动任何 ID、不重建用例**；唯一副作用 `ordering` 归零。这是给全量接口用例批量补鉴权脚本的标准通道（完整证据链/命令/豁免清单见 `references/case-debug-case-vs-test-case.md` 第八节）。
    4. **接口节点本身的 preProcessors 也走同一通道**（2026-08-26 追加验证）：改 `api.preProcessors`（接口节点字段，非 cases 内），同一次 match-name 重导即落库（66/66）。**⚠️ 但接口层脚本会被所有下级用例级联执行**（Apifox 继承机制，用例默认继承接口前后置操作）——给接口层加脚本后必须同步检查豁免用例（负向缺凭据/安全性），否则它们被级联注入合法签名而失效；修复方式是给豁免用例加「清除鉴权头」脚本抵消（`pm.request.headers.remove('x-api-key')` + `remove('Authorization')`，实测 9/9 恢复）。**`inheritPreProcessors: {"enable": false}` 落库但 CLI 执行引擎不读，不可依赖**。完整证据链见 case study 第九节。

**应用时机**：写 OpenAPI / swag YAML 时就带上 example（节点 2 → A12）；导入后立即验收，不要等对接方反馈。

## 规则 T-4：伪失败四坑（强制，2026-09-01 实操补充）

> 这四种情况都表现为**业务码 500 / 断言失败**，看着像接口缺陷，实际是用例构造或运行方式问题。**先按本节排除，再去查接口代码**——把伪失败写进缺陷清单比漏测更糟，会让后续所有人怀疑一个没问题的接口。

**坑① 数字字段引用变量必须去掉外层引号**

apifox 的变量替换是**纯文本替换**，`"id": "{{fixtureId}}"` 替换后是 JSON 字符串，强类型后端直接拒绝：

```text
json: cannot unmarshal string into Go struct field XxxReq.id of type int
```

正确形态（变量占位裸放，此时 body 文本本身不是合法 JSON，但 apifox 发送前会替换）：

```jsonc
{
  "id": {{fixtureId}},
  "ids": [{{fixtureId}}]
}
```

生成侧写法（`pretty_jsonb` 之后再剥引号，避免手工拼串出错）：

```python
import json, re

def pretty_jsonb(data):
    text = json.dumps(data, indent=2, ensure_ascii=False)
    # 数字/数组元素位置的变量占位去掉外层引号；字符串字段的变量不受影响需另行处理
    return re.sub(r'"(\{\{[A-Za-z0-9_]+\}\})"', lambda m: m.group(1), text)
```

**坑② 单条 `run --test-case` 是独立进程，extractor 变量不跨运行传递**

`postProcessors` 的 extractor 写入的变量（即使 `variableType=globals` + `shareScope=PROJECT`）在**下一次独立 run 里取不到**。因此「依赖前序步骤产出的 id」这类用例**独立跑必失败**，且属伪失败：

- 依赖前序数据的用例必须编入 `test-scenario`（同一次运行内变量共享），见 `modules/test-scenario.md`
- 这类用例**不得计入独立可跑批次**：批量运行脚本要显式把它们排除，否则每轮回归都会有几条恒定失败，久了就被当成「已知失败」忽略
- 收口时如实登记为「仅在场景内成立」，不算覆盖缺口也不算通过

**坑③ 写库用例要能重复运行，靠运行时唯一后缀**

带唯一性校验的创建接口（币种组合、名称、编码等），固定测试数据只能跑一次，第二次运行首步就 500「已存在」。清理铁律解决的是「跑完不留残留」，**幂等解决的是「能不能再跑一次」**，两者都要：

```javascript
// 前置脚本：让写操作闭环可重复运行
var suffix = String(Date.now()).slice(-9);
pm.variables.set("fixtureSuffix", suffix);
// body 里引用：{"shortName": "APIFOXTEST{{fixtureSuffix}}"}（字符串字段保留引号）
```

配合场景末步 delete 回收，即可连跑 N 轮都全绿。**验收标准：场景必须连跑两次结果一致**，只跑一次通过不算数。

**坑④ CLI 输出前可能有人类可读提示，直接 `json.loads` 会失败**

`test-case create` 等命令会在 JSON 前后打「💡 创建后检查」「📖 运行 apifox test-case view <id>」等提示行。脚本里直接 `json.loads(stdout)` 会抛异常，**把已经创建成功的资源误判为失败**（本轮 41 条用例全部创建成功却被脚本报成 0 成功）。统一用正则截取 JSON 主体：

```python
match = re.search(r"\{.*\}", raw, re.S)
data = json.loads(match.group(0)) if match else None
```

同时注意：`test-case create` 的返回提示里「`commonParameters` 可能未正确保存」对 `{}` 空对象是**常态提示**，不是错误；`preProcessors 可能未正确保存` 出现在刻意留空的安全性用例上同理。判定落库真实性一律靠 `test-case get` 回读，不看提示文案。

## 不可违反规则（test-case 模块，硬动作级）

1. **无参测试 = 无效测试**：接口有参但用例无参必须补全，禁止"先建 1 个正向先收口"；唯一例外是经三条证据确认的 header-only 接口（见「参数完整性校验」节例外条款）
2. **JSON 不格式化不允许写入**：`requestBody.data` / `examples.data` / 响应示例必须用 `pretty_jsonb` 格式化
3. **Mock 空壳不允许存在**：200 响应示例必须是真实业务数据，禁止 `{}`
4. **创建后必须 test-case get 对账 endpoint schema**（节点 2 → A7 双重闸门）
5. **两类用例分别验收**：`test-case` 全绿不代表调试用例有参数，二者是两套资源；导入接口后必须按规则 T-3 用 `export --format apifox` 查 `api.cases[].requestBody.data`（节点 2 → A12）
6. **CLI 写入报 success 不等于落库**：`endpoint update` 的 `requestBody.example`、`environment update` 的 `variables` 都属"假成功"字段，写完必须回读确认
7. **失败先按规则 T-4 排除伪失败**：业务码 500 / 断言失败时，先排除「变量带引号、变量不跨运行、写库用例不幂等、CLI 输出解析错」四坑，再判定为接口缺陷；未排除即写进缺陷清单的一律驳回

## 更新测试用例

更新时必须先 `get` 原结构并基于完整结构修改，`update` 不是 JSON Patch，会整体覆盖。`test-case-update` schema 已包含 processor/assertion/extractor 的枚举值说明，不要凭经验猜字段名。

## 处理器结构

> 处理器分两类：**preProcessors（前置，请求发出前执行）** 与 **postProcessors（后置，响应返回后执行）**。前置处理器用于鉴权自动续期、动态签名、动态参数准备；后置处理器用于断言、提取变量。鉴权自动化的完整方案（登录用例 extractor / 前置脚本自动重登 / JWT 构造）见 `modules/test-auth.md`。

```json
{
  "requestBody": {
    "type": "application/json",
    "data": "{\n  \"name\": \"Demo\"\n}"
  },
  "preProcessors": [
    {
      "id": "preProcessors.0.customScript",
      "type": "customScript",
      "data": "// 请求前脚本：如 token 过期自动重登（模板见 modules/test-auth.md 方案 B）",
      "defaultEnable": true,
      "enable": true
    }
  ],
  "postProcessors": [
    {
      "id": "postProcessors.0.customScript",
      "type": "customScript",
      "data": "pm.test('返回 ID', function () {\n  var body = pm.response.json();\n  pm.expect(body.data.id).to.exist;\n});",
      "defaultEnable": true,
      "enable": true
    },
    {
      "id": "postProcessors.1.extractor",
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
  ]
}
```

规则：
- `requestBody.data` 必须是字符串，不要把 JSON Body 写成对象
- 处理器使用扁平结构 `{ id, type, data, defaultEnable, enable }`
- 处理器建议带稳定 `id`（preProcessor 用 `preProcessors.N.*`，postProcessor 用 `postProcessors.N.*`）
- `shareScope` 优先 `PROJECT`，不要默认 `TEAM`
- 多行内容用 `\n` 预格式化
- **`update` 是整体覆盖**：更新时保留原有 preProcessors + postProcessors，不要只带新增的处理器

## 断言规则

常规校验优先用可视化 `assertion`，自定义脚本只做兜底：
- HTTP 状态码用 `httpCode`，不要用 `responseCode`
- JSON 字段用 `responseJson`，不要用 `responseBody`
- 全文包含用 `responseText` + `include`
- 比较符用 `equal`，不要用 `equals`

```json
{
  "type": "assertion",
  "data": {
    "name": "HTTP 状态码为 200",
    "subject": "httpCode",
    "comparison": "equal",
    "value": "200",
    "path": ""
  },
  "defaultEnable": true,
  "enable": true
}
```

## 断言顺序（强制）

> 吸收自 API测试自动化专家版。每个用例的断言按固定顺序编写，避免"表面通过"：

1. **先查状态码**：`httpCode` + `equal`（先确认 HTTP 层正确）
2. **再查业务码**：`responseJson` + `$.code`（业务层是否正确）
3. **后查关键字段**：`responseJson` + path 断言关键响应字段非空/值正确

禁止只断言 2xx 不校验响应结构，也禁止把错误路径断言成"符合预期"。

## 断言速查（16 种映射）

> 吸收自 API测试自动化专家版 Assertions 分类，映射到 apifox assertion 字段。

| 断言意图 | apifox 落地 |
|----------|-------------|
| HTTP 状态码 | `httpCode` + `equal` + value（支持多值 `[200, 201]`） |
| 任意 2xx | 自定义脚本断言（pm.response.code 2xx） |
| JSON 字段存在 | `responseJson` + path + `notNull` 或 `include` |
| JSON 字段值 | `responseJson` + path + `equal` |
| JSON 嵌套路径 | `responseJson` + `$.data.items[0].id` |
| JSON Schema 结构 | 自定义脚本 + 关键字段类型断言兜底 |
| 响应全文包含 | `responseText` + `include` |
| Header 存在/值 | `responseHeader` + 名称 + `equal/include` |
| Content-Type | `responseHeader` + `Content-Type` + `equal` |
| 响应时间阈值 | 自定义脚本（pm.response.responseTime） |
| 字段非空 | `responseJson` + path + 自定义脚本断言非空 |
| 数组长度 | 自定义脚本（pm.expect(body.data.items.length)） |
| 字段类型 | 自定义脚本（typeof） |
| 数值大小比较 | 自定义脚本（pm.expect(Number(...)).to.be.above/below） |
| 枚举值校验 | `responseJson` + path + `equal` 逐一断言 |
| 错误结构校验 | `httpCode` 4xx + `responseJson` + `$.code` 非空 |

> 规则：常规校验优先用可视化 `assertion`（上表前 6 行），复杂校验用自定义脚本兜底（`pm.test` / `pm.expect`）。

## 字段风险提醒

- 不要把 `test-scenario` 的步骤结构写进 `test-case`
- 不要只写 case 名称和 endpointId（空壳）
- 不要使用未验证的 `categoryId`
- 不要凭经验猜 processor/assertion/extractor 的字段名
- test-case 不支持跨步骤数据传递，需要时加载 `test-scenario`

## 数据清理机制（写接口用例，强制）

> 方法论见 `modules/test-case-generation.md`「规则 F：写接口测试数据清理铁律」，本节只给 CLI 落地写法。

- **POST 用例清理**：在 `postProcessors` 加 `extractor` 提取新建资源主键（`shareScope=PROJECT`），随后用 `test-scenario` 把"创建 case → 断言 case → 删除 case（复用 {{提取的id}}）"编成一条场景；单独跑创建 case 时不清理，必须跑场景才算完整闭环。
- **PUT/PATCH 用例清理**：优先对 fixture（专用测试记录，不服务真实业务）操作；若必须改共享数据，在同一 case 的 `postProcessors` 末尾加一个还原请求（自定义脚本里发起还原调用，或场景里追加还原步骤）。
- **DELETE 用例清理**：本身即清理动作，但前置必须是"本场景创建的数据"，不要对已有业务数据跑删除用例；场景第一步用创建 case 的 extractor 产出 id，最后一步才是 delete case。
- **无删除接口的资源**：在 `PROJECT_TEST.md`「遗留测试数据」登记，不要跳过清理环节就直接收口。

## 运行规则

- `test-case run <caseId>` — 单个 case
- `test-case run --endpoint <endpointId>` — 按接口运行
- `--category <categoryId>` 必须和 `--endpoint <endpointId>` 一起使用
- `apifox run --test-case <caseId>` 只支持 caseId
- 建议显式指定 `--environment <开发环境Id>`
- **结果统计口径（强制）**：以报告表格的「断言数 总数 / 失败数」为准；**不要用 `grep -c '√'` 或 `grep -c '×'` 判定通过**——失败断言在报告里是 `1. 2.` 编号形式，`×` 恒为 0 会把失败读成全绿（详见 `modules/testing-pitfalls.md` 陷阱 12-1）。
- **运行前环境变量就绪检查（强制）**：用例依赖鉴权/登录/签名时，先核对开发环境变量是否齐备（对照 `PROJECT_TEST.md`「环境变量登记」表）；401/403/签名错误/token 无效 → 先查环境变量缺失/过期，再查接口——不要算成接口失败（详见 `modules/environment.md`「开发环境环境变量（强制）」节）

## 常见恢复

| 现象 | 处理 |
|------|------|
| 测试步骤不展示 | `test-case get` 看真实保存结构 |
| 断言不生效 | 对比现有成功 case 模板，检查 assertion 字段 |
| 提取变量为空 | 检查 extractor 层级、变量名、响应路径和执行报告 |
| endpoint 下找不到 case | 检查 `--branch` 和 `--endpoint` |
| 401/403/签名错误/token 无效 | 先核对开发环境变量（鉴权签名/登录账号/token）是否缺失或过期，对照 `PROJECT_TEST.md`「环境变量登记」表，再查接口 |
| 登录后 token 没生效 | 检查登录用例 extractor（`shareScope=PROJECT`）与后续用例环境变量引用 {{token}} |
| 用例无参/参数丢失（接口有参但用例不带） | 对照 `endpoint get` schema 补全 query/path/body 参数；POST/PUT/PATCH 用例保留 requestBody 全部必填字段，禁止空 body / `{}` 空壳；**无参测试判定不通过**，补参后重跑（见「参数完整性校验（强制）」节） |
