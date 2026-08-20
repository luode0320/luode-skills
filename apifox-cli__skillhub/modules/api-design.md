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

## 创建接口标准流程

1. 确认 project 和 branch
2. 先创建可复用资源（schema、response-component、security-scheme）
3. 获取 `endpoint-create` schema：`apifox cli-schema get endpoint-create`
4. 生成 JSON，通过 `cli-schema validate` 校验
5. 执行 `apifox endpoint create ...`
6. `apifox endpoint get <id>` 验证保存结构

## 字段说明铁律（强制，最高优先级）

> 现状问题（用户已指明）：apifox 接口的参数、响应、头部**经常没有注释**，字段用途完全看不懂；代码侧若无注释，apifox 侧就是空的。这种现状**视为严重缺口**，必须补全并持续维护。

- **参数 / 请求体 / 响应 / 头部 每个字段必须有 `description` 说明用途**，不允许存在无说明字段——接口写了说明看不懂等于没写
- **说明覆盖范围**：query/path/header 参数、请求体 body 字段（含嵌套对象与数组元素对象）、响应字段（含统一包装字段与嵌套 data）、头部字段（鉴权/签名/语言/版本/设备/trace 等）
- **缺失处理（不阻断，但必须补全）**：发现字段缺 description 时，**根据业务上下文代码自行补充**——接口侧（apifox 的 description）与代码侧（swag 注解 / 结构体注释）**两边都要补，不要遗漏**；禁止留空
- **说明来源优先级**（引用 `swag-openapi-maintainer-rules/references/description-rules.md`）：真实代码注释 > 业务文档 > 受控推导；禁止为了补说明编造业务规则、校验条件或失败语义
- **创建/更新后必须校验**：`apifox endpoint get <id>` 检查参数/响应/头部 description 完整性；仍有缺失则补全后再宣称完成
- **接口变更时**：字段说明随接口定义**同步更新**，不允许只改字段不改说明

## 不可违反规则

1. 不要把 endpoint 和 test-case 混写
2. 先建可复用资源，再引用到 endpoint
3. 创建后必须 `get` 验证
4. 环境变量不要写进 common-parameter
5. 不允许创建/更新出参数、响应或头部字段无 description 的接口；字段说明缺失时必须补全（接口侧 + 代码侧），禁止留空
