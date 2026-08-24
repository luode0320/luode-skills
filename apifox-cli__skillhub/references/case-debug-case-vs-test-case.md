# Case study：调试用例与测试用例是两套资源（2026-08-24 gap 回补）

> 归属 owner：`apifox`。本案例记录一次**由错误论断导致的假通过**，以及五步取证如何定位 CLI 的真实能力边界。供下次遇到"CLI 说成功但客户端看不到"类问题时对照。

## 一、现象

EllipalFinance-go 项目为 5 个活动曝光管理接口（`/api/swap/v2/admin/activity/*`）建了 21 个 test-case，跑出 88 断言 0 失败，且按当时的参数完整性闸门取证：必填字段零缺失、T-1 格式化全通过。

用户随后截图：客户端「接口管理」里点开 `新增或编辑活动曝光配置` → 用例「成功」→ Body(JSON) **完全空白**，并问"是 apifox 的 skill 还不够完善吗"。

## 二、根因：skill 的论断与实测相反

本 skill `modules/test-case.md` 当时写着：

> 接口树里接口下方的"成功/失败"等子项 = 接口用例
> 不存在"把测试用例复制到调试用例"这个操作——接口用例本身即带完整参数的调试例子

agent 据此认为"建完 test-case 接口树下就有带参例子"，于是参数完整性闸门**只查了 `test-case` 一路**，得出全通过。而用户看到的是另一套资源。

**这是假通过的典型成因：验收口径覆盖不全，且 skill 明文背书了错误口径。**

## 三、五步取证（每步都推翻一个可能的解法）

| 步 | 验证 | 结果 |
|---|---|---|
| 1 | `test-case list --endpoint 505838489` 是否含那个「成功」 | ❌ 只返回 7 个自建用例，body 均 103~510 字节非空；「成功」不在列表 |
| 2 | `export --format apifox` 看它到底是什么 | 它在 `api.cases[0]`，`type=DEBUG_CASE`，`categoryId=0`，`requestBody.data=""` |
| 3 | `endpoint get` 能否读到 `cases` | ❌ 返回的 39 个顶层键里没有 `cases` |
| 4 | `endpoint-update` schema 是否接受 `cases` | ❌ schema 里既无 `cases` 也无 `DEBUG_CASE` |
| 5 | `endpoint update` 写 `requestBody.example` | ❌ 5/5 报 `success: true`，但回读 example 长度全为 0（假成功） |

结论：**CLI 完全写不到调试用例**，只能在 `import` 时经 example 灌入。

## 四、决定性实验：example 该放哪一层

前四步只证明了"写不进去"，没解决"怎么才能有"。于是导入一个**临时探针接口**（带 example，验完即删）：

```yaml
content:
  application/json:
    schema: {...}
    example:            # MediaType 层级
      activityId: probe_demo_001
      type: 1
```

探针的 `DEBUG_CASE` **自带 69 字节 body** → 证明 example 是唯一入口。

但第一次给正式接口补 example 时放进了 `schema.example`，删接口重导后验收 **0/5 仍为空**；改到 MediaType 层级重导，**5/5 生效**。

> **OpenAPI 里 `MediaType.example` 与 `Schema.example` 都合法，apifox 生成调试用例 body 时只认前者。** 这一条是本案例最容易踩且最难自查的点——放错位置不报错、不告警，只是静默没有。

## 五、修复代价（为什么要在导入前就写对）

已存在接口没有第三条路：

1. **删接口重导**：`endpoint delete` → 带 example `import` → 重绑 securityScheme → **重建全部测试用例**（endpointId 变，21 个 caseId 全部失效）→ 重跑回归。本次实际执行了**两轮**（第一轮因 example 放错层级白做）。
2. **用户客户端点「自动生成」**：零风险但需人工逐接口点击。

所以规则 T-3 把关口前移到"写 OpenAPI 时"，而不是"发现问题后再补"。

## 六、沉淀

- `modules/test-case.md`：重写「两类用例是两套资源」节（纠错）+ 新增规则 T-3 + 纠正 T-2 修复路径 + 不可违反规则第 5/6 条
- `modules/project-onboarding-checklist.md`：硬动作 A12
- `modules/api-sync-to-apifox.md`：不可违反规则第 10 条
- 净增约 62 行，其中约 12 行为替换原错误论断

## 七、可迁移的教训

1. **"CLI 报 success" 不等于落库**——本 skill 已知两个假成功字段（`endpoint update` 的 `requestBody.example`、`environment update` 的 `variables`），写完都必须回读确认。遇到新字段默认怀疑。
2. **一个概念对应几套资源，要先用 `export --format apifox` 看原生结构**，不要凭客户端 UI 的层级关系推断 CLI 资源模型。
3. **skill 里的论断也会错**——当实测与 skill 冲突时以实测为准，并回头修 skill（本 skill「CLI 事实优先」原则）。这次若不修，下个项目会原样再踩一遍。
4. **验收口径要覆盖交付物的全部可见面**：用户看的是客户端接口树，agent 查的是 CLI 列表，两者不重合就会出现"我说全绿、你说是空的"。
