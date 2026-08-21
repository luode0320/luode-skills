# API 设计 — endpoint / schema / folder / response-component / security-scheme

> 本模块覆盖 Apifox API 设计相关命令。已从 SKILL.md 继承：写入标准流程、分支参数规则。

## 何时加载

- 创建/更新/查询/删除接口（endpoint）
- 管理 Schema 数据模型
- 管理目录/文件夹结构
- 创建/管理响应组件、安全方案

## 命令入口

```bash
apifox endpoint --help
apifox schema --help
apifox response-component --help
apifox security-scheme --help
apifox folder --help
```

具体参数以当前 CLI help 为准。

## 核心边界

| 资源 | 用途 | 注意 |
|------|------|------|
| endpoint | 接口定义（method + path + params + body + response） | 不等同 test-case |
| schema | 可复用的数据模型 | 先创建再由 endpoint 引用 |
| response-component | 可复用的响应结构 | 减少重复定义 |
| security-scheme | 认证方案（Bearer/JWT/Basic 等） | 全局引用 |
| folder | 接口目录/分组 | 组织接口层级 |

## folder 选择规范（强制）

> 接口生成了不是就完事——**创建即归类**，归类是持续维护工作。接口堆在「默认模块 / 接口」平铺层、不按业务模块归类，视为严重缺口，必须归位（详见 `modules/api-folder-organization.md`，对应硬动作 A11）。

- 创建 endpoint **之前**先确认目标 folder：按「产品模块 / 业务域 / 功能域」定位（如 `交易所 > 币币交易 > 下单`），folder 不存在则先 `apifox folder create` 创建
- 禁止按 URL 路径机械建 folder（`/api/v1/xxx` → 建 `api/v1/xxx` 是反面模式）
- 创建后回读验证：`apifox endpoint get <id>` 确认已落在业务 folder 下，不在「默认模块 / 接口」平铺层
- 接口变更（新增 / 迁移 / 删除）时 folder 归属同步调整，不累积归类欠账

## 创建接口标准流程

1. 确认 project 和 branch
2. **确认目标 folder（按 `api-folder-organization.md` 业务模块识别法）**；先创建可复用资源（schema、response-component、security-scheme）
3. 获取 `endpoint-create` schema：`apifox cli-schema get endpoint-create`
4. 生成 JSON，通过 `cli-schema validate` 校验
5. 执行 `apifox endpoint create ...`
6. **`apifox endpoint get <id>` 双重验证（强制）**：
   - 验证保存结构（method/path/params/body/response 已成功存储）
   - **验证字段说明完整性**：参数 / 请求体 / 响应 / 头部**每个字段** `description` 非空——任一字段缺失必须补全（接口侧 + 代码侧 swag 注解），不允许留空收口（详见下一节「字段说明铁律」+ 硬动作 A1）

## 字段说明铁律（强制，最高优先级）

> 现状问题（用户已指明）：apifox 接口的参数、响应、头部**经常没有注释**，字段用途完全看不懂；代码侧若无注释，apifox 侧就是空的。这种现状**视为严重缺口**，必须补全并持续维护。如图 4 显示的「接口说明栏空、请求参数字段全部无 description」即为典型反面案例。

- **参数 / 请求体 / 响应 / 头部 每个字段必须有 `description` 说明用途**，不允许存在无说明字段——接口写了说明看不懂等于没写
- **说明覆盖范围**：query/path/header 参数、请求体 body 字段（含嵌套对象与数组元素对象）、响应字段（含统一包装字段与嵌套 data）、头部字段（鉴权/签名/语言/版本/设备/trace 等）
- **缺失处理（不阻断，但必须补全）**：发现字段缺 description 时，**根据业务上下文代码自行补充**——接口侧（apifox 的 description）与代码侧（swag 注解 / 结构体注释）**两边都要补，不要遗漏**；禁止留空
- **说明来源优先级**（引用 `swag-openapi-maintainer-rules/references/description-rules.md`）：真实代码注释 > 业务文档 > 受控推导；禁止为了补说明编造业务规则、校验条件或失败语义
- **创建/更新后必须校验**：`apifox endpoint get <id>` 检查参数/响应/头部 description 完整性；仍有缺失则补全后再宣称完成
- **接口变更时**：字段说明随接口定义**同步更新**，不允许只改字段不改说明

## 硬动作 A1：创建/更新后立即审计字段说明（强制）

> 把字段说明铁律从"必须"变成"必执行"——文档写了规则没人触发等于没写。本硬动作对应 `project-onboarding-checklist.md` 节点 1 → A1。

**触发时机**：每个 endpoint **创建后立即**、**更新后立即**、**导入 swag 后立即**。

**执行命令**：

```bash
apifox endpoint get <endpointId> --output endpoint.json

# 自动审计（建议沉淀到项目 tools/）：
python tools/audit_endpoint_descriptions.py endpoint.json
```

**审计脚本逻辑**（伪代码）：

```python
def audit_descriptions(endpoint: dict) -> list[str]:
    issues = []
    # 检查 parameters
    for p in endpoint.get("parameters", []):
        if not p.get("description", "").strip():
            issues.append(f"parameter.{p['name']}.description 为空")
    # 检查 requestBody
    schema = endpoint.get("requestBody", {}).get("schema", {})
    issues += check_schema_descriptions(schema, prefix="requestBody")
    # 检查 responses
    for code, resp in endpoint.get("responses", {}).items():
        for h in resp.get("headers", []):
            if not h.get("description", "").strip():
                issues.append(f"responses[{code}].headers.{h['name']}.description 为空")
        issues += check_schema_descriptions(resp.get("schema", {}), prefix=f"responses[{code}]")
    return issues
```

**通过标准**：`issues` 列表为空（每个字段都有非空 description）。

**不通过则报告并必须修复**（用户已确认"不阻断、自行补充"）：
- 列出所有缺失字段（字段路径 + 字段名）
- 自动从 swag 源码注解拉取中文注释（如可用），用户确认后写入 description
- 缺失 swag 注解 → 根据业务上下文+代码接口注释自行补全（接口侧+代码侧两边都补）
- 全部补全后重新跑审计，必须 issues 为空才算收口

**批量修复**（针对截图 4 等已有项目）：见 `project-onboarding-checklist.md` 「现有项目批量修复命令集」第 2 项。

## 不可违反规则

1. 不要把 endpoint 和 test-case 混写
2. 先建可复用资源，再引用到 endpoint
3. 创建后必须 `get` 验证
4. 环境变量不要写进 common-parameter
5. 不允许创建/更新出参数、响应或头部字段无 description 的接口；字段说明缺失时必须补全（接口侧 + 代码侧），禁止留空
