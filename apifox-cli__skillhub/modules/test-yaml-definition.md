# YAML 测试定义方法论 — test-yaml-definition

> 归属 owner：`apifox`。本模块把"YAML 无代码定义测试套件"的方法论映射到 apifox 原生资源，用于大批量接口的测试定义设计。吸收来源：API测试自动化专家版（YAMLRunner / yaml_test_guide.md）方法论。执行红线：**最终执行一律走 apifox 真实测试**（`test-strategy-rules` 接口测试执行通道），YAML 仅作为设计表达层。

## 何时加载

- 用户要求"批量测试""YAML 定义测试""无代码测试套件"
- 有一组接口需要系统化定义测试（如 CRUD 全链路）
- 需要把 YAML 测试设计转成 apifox 用例

## YAML 套件结构（方法论参考）

```yaml
name: "用户管理API测试套件"
config:
  base_url: "${env.base_url}"     # 环境变量引用
  auth: { type: bearer, token: "${env.api_token}" }
  timeout: 30
  retry: 3
tests:
  - name: "获取用户列表"
    method: GET
    path: /api/users
    query: { page: 1, limit: 20 }
    expect: { status: 200, body_contains: "data" }
    extract:
      first_user_id: "response.data[0].id"   # 变量提取，链式传递
  - name: "获取单个用户"
    method: GET
    path: "/api/users/${first_user_id}"
    expect: { status: 200 }
```

### 字段表（设计层）

| 字段 | 说明 |
|------|------|
| `tests[].method/path/query/headers/body` | 请求定义（path 支持变量插值） |
| `tests[].expect` | 期望：status / body_contains / json_path / json_schema / response_time / header_contains |
| `tests[].extract` | 变量提取：`response.data.x` / `response.data.arr[0].y` / `headers.X` / `status` |
| `tests[].when` | 条件执行（见下） |
| `tests[].loop` | 循环批量 |
| `config.parallel` | 并行执行 |
| `hooks` | 前置/后置钩子 |

## 条件执行 when（10 操作符）

| 操作符 | 示例 |
|--------|------|
| `==` / `!=` | `${status} == 200` / `${role} != guest` |
| `>` `<` `>=` `<=` | `${count} > 0` / `${age} >= 18` |
| `and` / `or` | `${a} > 0 and ${b} < 100` |
| `in` / `not in` | `${role} in admin,manager` / `${status} not in deleted,banned` |
| `is empty` / `is not empty` | `${name} is empty` / `${token} is not empty` |

条件不满足 → 测试跳过（对应 apifox：前置条件不足时标记跳过/PENDING，判定规则见 `modules/test-data-and-judgement.md`）。

## apifox 逐项映射（强制，执行走 apifox）

| YAML 设计要素 | apifox 落点 |
|---------------|-------------|
| `tests[]` 请求定义 | `test-case`（`modules/test-case.md` 标准创建流程） |
| `expect.status` | assertion `httpCode` + `equal` |
| `expect.json_path/body_contains` | assertion `responseJson` + path / `responseText` + `include` |
| `extract` 变量提取 | postProcessors extractor（`subject: responseJson` + 表达式，`shareScope: PROJECT`） |
| 变量链式传递 | 多 case 间提取变量传递（shareScope=PROJECT）或 `test-scenario` 步骤编排 |
| 用例间依赖顺序 | `test-scenario` 场景编排（`modules/test-scenario.md`） |
| 批量执行/CI | `test-suite` + 定时任务 + runner（`modules/test-automation.md`） |
| `config` 环境/认证 | `environment` 管理（`modules/environment.md`） |
| `when` 条件 | apifox 无同名能力 → **设计参考**，实现为前置数据准备或数据驱动（test-data 迭代） |
| `loop` 循环 | **设计参考**：用 test-data 数据集迭代实现（`modules/test-case.md` test-data） |
| `parallel` 并行 | **设计参考**：apifox runner 执行机制以 CLI help 为准 |
| `hooks` 前后置钩子 | **设计参考**：用前置处理器/后置处理器（preProcessor/postProcessor）实现 |

> 无直接映射的语法（when/loop/parallel/hooks）标注"仅设计参考，执行走 apifox"，不引入 YAML runner 脚本。

## 设计→落地流程

1. 按 YAML 结构设计测试定义（先在纸面/文档层把"测什么"理清）
2. 逐项映射到 apifox：创建 test-case（含断言、提取器）
3. 依赖链用 test-scenario 编排
4. 批量回归并入 test-suite
5. 全部用例在 apifox 真实运行通过（`test-case run` / `test-suite run`）

## 常见恢复

| 现象 | 处理 |
|------|------|
| 变量提取为空 | 检查 extractor 的 subject/expression 是否命中真实响应路径 |
| 用例顺序依赖失败 | 用 `test-scenario` 显式编排，不靠执行顺序碰运气 |
| 批量用例太多 | 按接口分组建 category，每接口 ≥3 类用例（正/异/边界）校准 |
| 想用 YAML 直接执行 | 拒绝：执行统一走 apifox，YAML 只作设计表达 |
