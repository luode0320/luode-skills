# 项目接入 apifox 预检与强制执行清单（硬动作级）

> 本模块是 apifox skill 的**规则↔动作总入口**——把分散在 `test-case` / `api-design` / `environment` / `test-case-generation` / `api-sync` 等模块里的规则对应到 5 个流程节点的**必须执行的动作**，每个动作明确：触发时机 · 执行命令 · 通过标准 · 不通过则阻断。本模块是「规则↔落地 GAP」的兜底层——它的存在就是为了堵住"规则写在文档里但没人触发执行"的断点。

## 何时加载

- 新项目**接入 apifox** 第一次配置时（项目级一次性强制动作）
- 一个 sprint / 阶段**收口前质量审计**时（项目级定期审查）
- 当前项目接口/用例**质量不达标**（如截图所示：正向用例只有 1 个、JSON 未格式化、Mock 示例空壳、字段无说明、环境端口错），需要批量修复时
- 任何「创建/更新/导入/同步接口」前的预检

## 核心原则

> **规则不是文档，是动作**——每条规则都必须能在「某个具体步骤」里被触发并阻断。

文档级规则与本模块硬动作的对应关系：

| 文档级规则（在哪写） | 硬动作级（在本模块怎么触发） | 触发节点 |
|--------------------|------------------------|---------|
| `test-case-generation.md` 规则 E-1 分层组合 | A4：创建用例前自动按 L1/L2/L3/L4 生成 | 节点 2 |
| `test-case.md` 规则 T-1 JSON 格式化（新增） | A5：用例 body 必须 pretty-print 入字符串 | 节点 2 |
| `test-case.md` 规则 T-2 Mock 真实性（新增） | A6：Mock 200 响应示例必须含真实数据 | 节点 2 |
| `test-case.md` 参数完整性校验（双重闸门） | A7：创建后 test-case get 对账 endpoint schema | 节点 2 |
| `api-design.md` 字段说明铁律 | A1：创建后立即 endpoint get 校验 description | 节点 1 |
| `api-folder-organization.md` folder 归类铁律 | A11：创建/导入后立即校验业务 folder 归类 | 节点 1 |
| `environment.md` 端口三级链 | A2：环境创建/更新后立即探测实际监听端口 | 节点 3 |
| `test-selection-policy.md` 三档执行策略 | A8：生成用例前查 PROJECT_TEST 受限/豁免表 | 节点 4 |
| `api-sync-to-apifox.md` 字段说明+契约校验 | A3：同步后立即 endpoint list/get 验证 | 节点 5 |

## 5 个流程节点 × 10+ 个硬动作

### 节点 1：创建 / 更新 endpoint（接口）

#### A1：endpoint get 校验 description（强制）

- **触发时机**：创建或更新接口后立刻
- **执行命令**：`apifox endpoint get <endpointId>`，对账 schema `parameters[*].description`、`requestBody.schema.properties[*].description`、`responses[*].schema.properties[*].description`、`headers[*].description`
- **通过标准**：每个字段都有非空中文/英文 description
- **不通过则阻断**：缺失字段 → 必须先用 swag-openapi-maintainer-rules 的 description-rules.md 流程补代码注释 → 重新 swag init → 重新生成 → 再补 apifox；接口侧 + 代码侧两边都补不遗漏
- **关联规则**：`api-design.md` 「字段说明铁律」节

#### A11：folder 归类即时校验（强制）

- **触发时机**：创建/更新接口后立即、导入 swag 后立即、项目质量审计（A9/A10）时
- **执行命令**：`apifox endpoint list --output endpoints.json`，解析每个 endpoint 的 folder 归属；`apifox folder list` 对照业务模块结构
- **通过标准**：接口全部落在业务 folder（产品模块/业务域/功能域）下，无「默认模块 / 接口」平铺层滞留、无归类错误、无空 folder 残留
- **不通过则阻断**：未归类/归类错误 → 按 `api-folder-organization.md`「持续维护工作流」迁移归位，迁移后 `endpoint get` 回读验证，复扫归零才收口；**接口生成了不是就完事，归类欠账必须随本轮清零**
- **关联规则**：`api-folder-organization.md` 全文、`api-design.md` 「folder 选择规范」节

### 节点 2：创建 / 更新测试用例

#### A4：创建用例前按规则 E-1 分层生成（强制）

- **触发时机**：每个 endpoint 第一次建用例时
- **执行命令**：用 schema 必填 + 关键业务参数生成正/负/边界三类用例，正向按 E-1 分层：
  - L1 单参数：每关键参数 1 个
  - L2 pairwise 精选：2~3 个高风险组合（必填×枚举、枚举×范围）
  - L3 全参数满配：1 个
  - L4 过滤×分页交互：1 个
- **通过标准**：正向用例数 ≥ `min(关键参数数+3, 10)`；<10 个关键参数 → 严格按分层生成；≥10 个关键参数 → 裁剪 L2 低风险组合，裁剪原因写入覆盖矩阵「计划补」列
- **不通过则阻断**：每接口正向用例只有一个（如图 1）→ 必须按 E-1 重构，补齐分层，不允许「先建 1 个正向先收口」
- **关联规则**：`test-case-generation.md` 规则 E-1

#### A5：JSON body 格式化（强制）

- **触发时机**：构造用例 `requestBody.data` 时、Mock 响应示例填写时、所有 JSON 字段（params/data/expected）写值时
- **执行命令**：`requestBody.data` 必须是**带 `\n` 的格式化字符串**（2 空格缩进），不是单行压缩字符串
- **通过标准**：JSON 内容可读性对齐 apifox 编辑器的「美化输出」（2 空格缩进、字段逐行排列）
- **不通过则阻断**：单行压缩 → 必须先格式化再写入（如 CLI 生成时使用 `json.dumps(obj, indent=2, ensure_ascii=False).replace('"', '\\"').replace('\n', '\\n')` 工具函数）
- **关联规则**：`test-case.md` 规则 T-1（新增）

#### A6：Mock 200 响应示例真实性（强制）

- **触发时机**：配置接口 Mock 或填写成功响应示例时；新建用例自动生成示例时
- **执行命令**：success response 示例（200/201）的 `data` / `examples` 字段必须含**与请求匹配的完整真实业务数据**（如创建资费策略接口，200 示例必须含完整的 id/channel/name/description/createdTime 响应对象）
- **通过标准**：Mock 示例能让开发者一眼看出"调通后接口长什么样"；响应字段与 schema 字段对得上
- **不通过则阻断**：`{}` 空壳示例（如图 3）→ 必须删除该示例或补全数据；纯空壳示例拖慢用户对接口的理解
- **关联规则**：`test-case.md` 规则 T-2（新增）

#### A7：参数完整性校验双重闸门（强制）

- **触发时机**：创建/更新用例后、运行用例后
- **执行命令**：
  - 闸门 1（创建/更新后）：`test-case get <caseId>` 对账 `endpoint get <endpointId>` 的 schema，必填 100% 带上、关键业务参数按 E-1 覆盖、POST body 必填字段保留
  - 闸门 2（运行后）：用例运行时若接口有参但用例无参 → 判定「不通过/无效」
- **通过标准**：闸门 1 全通过；闸门 2 有参用例必须带参
- **不通过则阻断**：缺参 → 必补全才能收口；无参用例运行结果不计入通过
- **关联规则**：`test-case.md` 「参数完整性校验（强制）」节、`test-data-and-judgement.md」 「不通过」条件第 8 条

### 节点 3：创建 / 更新环境

#### A2：端口探测三级链与纠偏（强制）

- **触发时机**：创建开发环境时立即、更新环境 baseUrl 时立即
- **执行命令**：
  - L1：读项目后端本地启动配置（`config_local*` / docker-compose / 启动脚本）
  - L2：`ss -tlnp` / `netstat -an` / `lsof -iTCP -sTCP:LISTEN` 探测本机实际监听端口
  - L3：`PROJECT_TEST.md`「项目端口」登记值兜底
  - **以 L2 实际监听端口为最终裁决**，与登记值不一致 → 纠偏（更新 apifox baseUrl + 回写 PROJECT_TEST.md），说明依据
- **通过标准**：环境 baseUrl 端口与本机后端实际监听端口一致；WSL2 跨系统场景按 `environment.md` 「WSL2 跨系统网络访问」节选地址路径
- **不通过则阻断**：`127.0.0.1:18080` 默认端口（如图 5）→ 必须先跑 L2 探测得到真实端口再写入 baseUrl；端口错则所有测试必然失败
- **关联规则**：`environment.md` 「本地服务端口探测（强制）」节

### 节点 4：受限 / 豁免接口识别

#### A8：受限/豁免接口前置识别（强制）

- **触发时机**：生成用例前
- **执行命令**：查 `PROJECT_TEST.md` 「受限/豁免接口登记」表
- **识别规则**：
  - 副作用/费用候选（upload/obs/sms/pay/短信/邮件/支付回调）→ 建议**豁免**，不建常规用例，仅变更时人工回归
  - 基础配置候选（permission/role/menu/dict/enum）→ 建议**受限**，只建负向+边界（无权限/越权）
  - 默认**全量执行**（L1-L4 + 负向 + 边界）
- **通过标准**：每接口已登记策略（P0 资金交易类禁止默认豁免），生成用例时按策略选择
- **不通过则阻断**：未登记 + 命中候选关键词 → 必须用户确认后登记再继续；规避误豁免 P0
- **关联规则**：`test-selection-policy.md` 「接口执行策略三档分类」节

### 节点 5：代码 → swag → apifox 同步

#### A3：端到端契约校验（强制）

- **触发时机**：代码侧 swag init 生成 openapi.yaml 后导入 apifox 后立即；接口变更后立即
- **执行命令**：`apifox endpoint list` + `endpoint get <endpointId>` 对账：
  - method+path 与代码 controller 一致
  - 参数/响应字段（含字段说明）与 swag 注解一致
  - 接口变更（新增字段/类型变更/删除字段）必须同步更新字段说明
- **通过标准**：接口与代码契约 100% 对齐，字段说明及时更新
- **不通过则阻断**：差异（method 改了/路径改了/字段丢了说明）→ 先修正代码侧 swag 注解→ 重新生成 → 重新导入；字段说明缺失同 A1
- **关联规则**：`api-sync-to-apifox.md` 「契约校验」+「字段说明完整性校验」

#### A9：API 文档完整性终检（强制）

- **触发时机**：项目最终验收或上线前
- **执行命令**：批量 `endpoint get` 全量项目，输出「接口质量审计报告」：
  - 缺 description 接口数 / 占比
  - 缺参数或参数错误的接口数 / 占比
  - 用例覆盖率不达标的接口数 / 占比
  - 环境 baseUrl 与实际监听端口不一致的环境数
- **通过标准**：所有指标 P1 以上接口 100% 达标
- **不通过则阻断**：报告中存在红色指标 → 必须修复到绿再上线
- **关联规则**：`project-onboarding-checklist.md` 全文（终检时跑全表）

### 节点 6（流程收口）：合并 / 创建 MR 前必跑

#### A10：预检清单全过（强制）

- **触发时机**：MR 创建前
- **执行命令**：按本模块 10 个动作全跑一遍（建议封装为 `apifox audit pre-merge` 子命令脚本，逐项输出）
- **通过标准**：所有动作都通过 / 用户已确认豁免项
- **不通过则阻断**：还有红色指标 → 不允许创建 MR，先修复

## 现有项目批量修复命令集（针对截图所示的「已建但质量不达标」情况）

> 适用场景：项目已接入 apifox，但接口/用例存在质量缺口（如截图所示 5 类问题）。下面的命令集按节点组织，逐项跑、逐步修复。

### 1. 入口：列出全量接口 / 用例

```bash
# 列全量 endpoint（保存到本地用于扫描）
apifox endpoint list --project <projectId> --branch <branch> --output endpoints.json

# 列全量 test-case（保存到本地用于扫描）
apifox test-case list --project <projectId> --branch <branch> --output testcases.json

# 列全量环境
apifox environment list --project <projectId> --output environments.json
```

### 2. 修复 description（节点 1 → A1）

```bash
# 扫描缺 description 的接口
python tools/scan_missing_descriptions.py endpoints.json > missing-desc.json

# 对每个缺 description 接口，逐一 get 然后 put（用 swag 注释回填）
apifox endpoint get <endpointId>  # 拉真实结构
# 在 editor 中补 description（参考 swag-openapi-maintainer-rules/references/description-rules.md 的字段说明规范）
apifox endpoint update <endpointId> --file <patched-endpoint.json>
```

### 3. 修复 JSON 格式化（节点 2 → A5）

```bash
# 扫描单行压缩 JSON 用例
python tools/scan_unformatted_json.py testcases.json > unformatted.json

# 工具函数（建议沉淀到 skill）
def pretty_jsonb(data: dict) -> str:
    return json.dumps(data, indent=2, ensure_ascii=False).replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n')

# 逐个 update 用例（保留原有 preProcessors/postProcessors，见 test-case.md 「更新测试用例」节）
apifox test-case get <caseId>  # 拉原结构
# 在 editor 用 pretty_jsonb 重构 requestBody.data
apifox test-case update <caseId> --file <patched-case.json>
```

### 4. 修复 Mock 真实性（节点 2 → A6）

```bash
# 扫描空壳 Mock 200 响应示例
python tools/scan_empty_mock_examples.py endpoints.json > empty-mocks.json

# 删除空壳示例或补全真实数据（按 schema 自动生成 Mock 数据：每个字段填合法值，参考 test-case-generation.md 的 schema 驱动数据构造规则）
apifox endpoint get <endpointId>  # 看 response component
# 在 editor 中补 200 真实示例（id=*, createdTime=now, ...所有 schema 字段全部填值）
apifox endpoint update <endpointId> --file <patched-endpoint.json>
```

### 5. 按规则 E-1 补正向用例（节点 2 → A4）

```bash
# 扫描正向用例数不达标的接口（按 L1-L4 分层预期数量）
python tools/scan_insufficient_positive.py endpoints.json testcases.json > insufficient-pos.json

# 对每个不达标接口，按 E-1 生成正向用例（参考 modules/test-case-generation.md 规则 E-1 的分层表格）
# L1: 每个关键参数 1 个正例
# L2: pairwise 精选 2~3 个高风险组合
# L3: 1 个全参数满配
# L4: 1 个过滤 × 分页
# 数量上限 ≤ min(关键参数数+3, 10)

# 逐个创建
apifox test-case create --project <projectId> --branch <branch> --file <layer1-case.json>
...（重复 L2/L3/L4）
```

### 6. 修复环境端口（节点 3 → A2）

```bash
# 1) 探测本机实际监听端口
ss -tlnp | grep LISTEN
# 或
netstat -an | grep LISTEN
# 或
lsof -iTCP -sTCP:LISTEN -nP

# 2) 对比 PROJECT_TEST.md 登记端口：登记值与实际不一致 → 纠偏
# 3) 更新 apifox 环境 baseUrl
apifox environment get <environmentId>  # 拉原结构
# 在 editor 中把 baseUrl 改为 http://127.0.0.1:<实际监听端口>
apifox environment update <environmentId> --file <patched-env.json>

# 4) 回写 PROJECT_TEST.md 「项目端口」列
```

### 7. 限制/豁免接口登记（节点 4 → A8）

```bash
# 自动识别候选接口
python tools/scan_exemption_candidates.py endpoints.json > exemption-candidates.json

# 用户确认后写入 PROJECT_TEST.md 「受限/豁免接口登记」表
```

### 8. 终检（节点 5 → A3 + A9）

```bash
# 全量审计（汇总所有 5 类问题）
python tools/audit_apifox_quality.py \
  --endpoints endpoints.json \
  --testcases testcases.json \
  --environments environments.json \
  --output quality-report.md

# 报告红色指标全部消除后才能合并
```

### 9. 修复 folder 归类（节点 1 → A11）

```bash
# 1) 列出全量 endpoint，解析 folder 归属（命中「默认模块/接口」平铺层或归类错误的列为待归类）
apifox endpoint list --project <projectId> --branch <branch> --output endpoints.json

# 2) 对照业务模块结构（产品模块/业务域/功能域），先建缺失的 folder
apifox folder list --project <projectId> --branch <branch>
apifox folder create --project <projectId> --branch <branch> --file <folder.json>  # 按需

# 3) 逐个迁移：拉 endpoint 真实结构 → 改 folder 归属 → update → get 回读验证
apifox endpoint get <endpointId>
apifox endpoint update <endpointId> --file <patched-endpoint.json>
apifox endpoint get <endpointId>  # 确认 folder 归属已生效

# 4) 删除迁移后遗留的空 folder
# 5) 复扫 endpoints.json，待归类数归零才算收口
```

> 归类识别方法见 `modules/api-folder-organization.md`「业务模块识别法」；迁移后同步检查相关 test-case 引用（见 `test-case.md` 更新流程）。

> 工具脚本应沉淀到项目 `tools/` 目录或 skill 的 `tools/` 目录，避免重复造轮子。第一次用时按本模块命令写出来后，后续项目复用。

## 不可违反规则

1. 节点 1 描述校验与节点 3 端口探测是**两个绝对动作**——这两个动作没跑就不算"接口已就绪"
2. 节点 2 每条用例都必须通过 A5/A6/A7 三项校验
3. 节点 4 未登记前不允许生成用例（防止误豁免 P0 资金/交易/支付类接口）
4. 节点 5 终检报告有红色指标时不允许合并 MR
5. 项目级强制：`PROJECT_TEST.md` 写入本模块作为「项目测试质量铁律」节首条
6. **接口必须落在业务 folder 下**（A11）：「默认模块 / 接口」平铺层滞留或归类错误 → 视为归类缺口，迁移归位后才算接口就绪；「生成了就不调整」是反面模式

## 关联文档

- `modules/api-design.md` — 节点 1（接口设计、字段说明铁律、folder 选择规范）
- `modules/api-folder-organization.md` — 节点 1（folder 归类与持续维护、硬动作 A11）
- `modules/test-case.md` — 节点 2（用例创建、T-1/T-2/参数完整性）
- `modules/test-case-generation.md` — 规则 E-1 分层组合
- `modules/environment.md` — 节点 3（端口三级链、WSL2 网络）
- `modules/test-selection-policy.md` — 节点 4（三档执行策略）
- `modules/api-sync-to-apifox.md` — 节点 5（端到端契约校验）
- `references/project-test-md-template.md` — 模板与 `PROJECT_TEST.md` 写入口径
- `SKILL.md` — 路由表（新增本模块条目）
