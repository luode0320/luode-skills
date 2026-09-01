# 测试场景建模 — test-scenario

> 本模块覆盖多步骤测试场景编排。已从 SKILL.md 继承：写入标准流程、分支参数规则。

## 何时加载

- 创建/更新多步骤自动化测试流程（如登录 → 创建 → 查询 → 清理）
- 编排多种步骤类型：接口请求、条件、循环、等待、脚本、数据库操作
- 步骤间变量传递、断言链路、前置/后置操作
- 将已有 endpoint、test-case、test-scenario 导入为场景步骤

## 不应使用

- 单接口测试用例 → 加载 `modules/test-case.md`
- 运行套件/CI → 加载 `modules/test-automation.md`

## 核心边界

| 概念 | 说明 |
|------|------|
| test-case | 绑定单个 endpoint 的用例 |
| test-scenario | 多步骤流程编排 |
| test-suite | 场景/用例集合 |

## 命令入口

```bash
apifox test-scenario --help
```

关键事实：**`test-scenario create` 只保存元数据。即使 create payload 含 `steps`，步骤也不会在 create 阶段保存。** 必须先 create 元数据，再用 `import-steps`、`add-ref` 或 `update --file` 添加步骤。

## 导入步骤命令

```bash
# 从接口导入
apifox test-scenario import-steps <scenarioId> --project <projectId> --source endpoint --ids <endpointIds> --sync manual

# 从测试用例导入
apifox test-scenario import-steps <scenarioId> --project <projectId> --source test-case --endpoint <endpointId> --ids <testCaseIds> --sync manual

# 从其他场景导入步骤
apifox test-scenario import-steps <scenarioId> --project <projectId> --source test-scenario --from-scenario <sourceScenarioId> --step-ids <stepIds>

# 添加场景引用
apifox test-scenario add-ref <scenarioId> --project <projectId> --scenario <sourceScenarioId>
```

语义边界：
- `import-steps` = 复制为当前场景自己的步骤
- `add-ref` = 引用其他场景，不复制内部步骤
- `--sync manual` = 默认，导入后可补业务参数
- `--sync auto` = 随源自动同步（仅支持 endpoint/test-case 来源）

**`--sync manual` 下改用例不会回灌到场景（2026-09-01 实测踩坑）**：步骤是导入那一刻的**副本**，之后用 `test-case update` 改了源用例（改 body、改断言、加前置脚本），场景里跑的仍是旧副本——表现为「用例明明改好了、回读也确认了，场景却还是按老逻辑失败」。两条出路：

- 导入时就用 `--sync auto`（源用例后续改动自动生效，写库闭环推荐）
- 已用 `manual` 导入且源用例有改动 → 重新 `import-steps`，或直接重建场景重导（步骤顺序敏感时重建更稳）

判断依据：`test-scenario get <id> --with-case-detail` 回读步骤真实 body，与 `test-case get` 的结果逐字对比，不要凭「我刚改过」推断。

## 场景建模标准流程

1. 明确业务目标：验证什么流程、成功条件、失败如何清理
2. 确认 project、branch、environment
3. 列出涉及的 endpoint、case、环境变量、测试数据
4. 用自然语言先设计步骤图，再转 JSON
5. 获取 `test-scenario-create` schema → 创建元数据
6. `test-scenario get --with-case-detail` 回读
7. 用 `import-steps` / `add-ref` 导入已有资源
8. 再次 `get --with-case-detail` 确认步骤写入
9. 导入后检查 params、headers、body 是否是 schema 示例值，需要业务值时用 `update --file` 补齐
10. 精细编辑时基于完整结构添加/修改 steps

## 步骤设计最佳实践

每步写明：stepName / stepType / input / output / dependsOn / assertions / onError / cleanup

复杂流程分层：
```
准备数据 → 鉴权/登录 → 主流程操作 → 结果查询与断言 → 副作用校验 → 清理资源
```

## 数据传递和变量引用

- 步骤间传递优先用 `{{$.1.response.body.token}}`、`{{$.2.response.body.data.id}}`
- 需跨模块复用或命名的变量 → 用后置操作 extractor
- 在脚本中使用前置步骤结果 → `pm.variables.get("$.1.response.body.token")`
- 步骤引用依赖步骤 ID/number，插入/删除/重排步骤后必须同步检查 `{{$.步骤号...}}`
- 生成 payload 时必须原样保留 `{{...}}` 占位符，不要转义

## 复杂步骤字段规则

| 步骤类型 | 关键字段 | 注意事项 |
|----------|----------|----------|
| 接口请求 | `type: "http"` + bindId | 优先用 import-steps，不要手写绑定 |
| 条件分支 | `parameters.keyVariable` + `operator` + `valueVariable` | 不要写 `expression` |
| 循环 | `parameters.count` | 不是 `times` |
| forEach | `parameters.array` | 子步骤用 `{{$.N.element.xxx}}` |
| 等待 | `parameters.timeout`（毫秒） | 不是 `duration` |
| 脚本 | `parameters.type="customScript"` | 不要写 `language/code` |
| 容器步骤 | 必须含 `disable=false`、`parameters`、`isOpen=true`、`children=[]` | 子步骤放 children |

## 断言规则

- 引用接口形成 HTTP 步骤时，优先使用原接口自带的契约测试
- 已启用契约测试时，不要重复添加同义断言
- 可视化断言字段：`httpCode`、`responseJson`、`responseText` + `include`
- 比较符：`equal`，不要用 `equals`

## 写操作闭环场景的验收标准（强制，2026-09-01 补）

写库场景（创建 → 改 → 查 → 删）**必须连跑两次且结果一致**才算通过，只跑一次全绿不算数：

- 第一次通过、第二次首步就失败 → 场景不幂等，测试数据带唯一性约束却用了固定值（修法见 `modules/test-case.md` 规则 T-4 坑③）
- 两次都通过但库里行数递增 → 清理链没闭合，末步 delete 没覆盖全部自建数据
- 收口证据要给出「连跑 N 次结果一致 + 残留条数 + 全表行数对照」，不能只给一次运行的断言数

## 不可违反规则

1. 不要把 `test-case` 结构直接当作 `test-scenario` 步骤
2. 不要只创建空场景名
3. 不要误以为 create 能保存 steps
4. 不要凭经验猜复杂步骤字段
5. 更新场景前必须先 `get --with-case-detail` 原结构
6. 不要在未确认环境的情况下执行有副作用步骤
7. 不要让后续步骤引用未确认来源的数据
8. 不要在 `--sync manual` 导入后改源用例却不重新导入（步骤是副本，改动不回灌，见上方「语义边界」）
9. 写库场景没有连跑两次验证就不得声称通过
