# Skills 拆分方案（按触发时机细分）

更新时间：2026-04-01

## 1. 目标

- 把“长 description + 多职责混合”的 skill 拆成单一触发类型的子 skill。
- 每个子 skill 只负责一种主要触发时机，降低命中歧义。
- 拆分后不丢规则细节：细节留在子 skill 的 `SKILL.md` 与 `references/`。

## 2. 拆分原则（执行版）

- 一个子 skill 的 `description` 建议只包含：
  - `当...时触发`
  - `负责...`
  - `不要用它代替...`
- 子 skill 的触发对象必须单一：
  - 例如“测试程序”与“模拟程序”分开，不混写。
- 如果一个改动经常同时命中 4 个以上子 skill，说明拆分过细，需回并。
- 每个子 skill 必须是“完整 skill”，不是仅有触发描述的壳子：
  - 必须有完整的 `SKILL.md`（frontmatter + 可执行流程）
  - 建议有 `agents/openai.yaml`，确保 UI 元信息与触发提示一致
  - 需要补齐配套资源目录（按需）：`references/`、`scripts/`、`assets/`
  - 如果父 skill 原本有参考资料，拆分后必须把对应资料迁入子 skill 的 `references/`，并在子 skill `SKILL.md` 中明确何时读取

## 2.1 命名与目录排序规则（新增）

- 为了让目录按名称排序时呈现“入口 skill -> 子 skill”的视觉顺序，子 skill 名必须复用父 skill 全前缀。
- 命名格式：
  - 父 skill：`<parent>-rules`
  - 子 skill：`<parent>-rules-<序号>-<主题>`
- 序号建议使用两位且按 `10/20/30...` 递增，给后续插入预留空间。
- 示例：
  - `test-program-rules`
  - `test-program-rules-10-case`
  - `test-program-rules-20-mock`
  - `test-program-rules-30-verify-script`
- 禁止同级出现“无父前缀”的子 skill 名，否则排序后会打散分组。

## 2.2 子 skill 完整性规则（新增）

- 子 skill 必须可独立被触发并独立完成本职责，不依赖“先读父 skill 才能执行”。
- 子 skill 的 `SKILL.md` 至少应包含：
  - 清晰触发边界（当...时触发）
  - 执行流程（步骤化）
  - 资源导航（引用本 skill 下 `references/`、`scripts/`、`assets/` 的读取/使用时机）
  - 边界声明（不要用它代替...）
- `references/` 不应空挂目录：
  - 有领域细节就下沉到 `references/`，避免把细节堆回父 skill
  - 无需参考资料时，应在 `SKILL.md` 明确“当前子 skill 无额外 references，直接按主流程执行”
- 父 skill 只做分流与索引，不再充当子 skill 的隐式知识仓库。

## 3. 第一批拆分（建议先落地）

## 3.1 拆分 `test-program-rules`

保留 `test-program-rules` 作为“测试程序总入口分流”。

新增子 skill：

1. `test-program-rules-10-case`
   description: 当新增或修改正式测试程序（承载断言与场景编排）时触发。负责正式测试程序的职责边界、程序结构与长期保留策略；不要用它代替测试目录落点或测试文档规则。

2. `test-program-rules-20-mock`
   description: 当新增或修改模拟程序（mock/stub/fake/假服务）时触发。负责模拟程序与正式测试程序的边界、复用策略与隔离要求；不要用它代替 fixture 命名或测试报告规则。

3. `test-program-rules-30-verify-script`
   description: 当新增或修改验证脚本、探测脚本、调用脚本时触发。负责脚本执行步骤、控制台过程日志与证据留痕；第三方 API 响应结构不明时优先由本 skill 驱动探测流程；不要用它代替功能验收结论规则。

4. `test-program-rules-40-fixture-data`
   description: 当新增或修改测试数据构造脚本、样例数据、fixture 生成逻辑时触发。负责数据构造职责、输入输出稳定性与复用边界；不要用它代替 mock 程序或正式测试程序规则。

5. `test-program-rules-50-helper`
   description: 当新增或修改测试辅助代码（公共断言、构造器、客户端封装）时触发。负责辅助代码抽象边界与复用约束；不要用它代替业务代码抽象或正式测试程序编排规则。

## 3.2 拆分 `implementation-review-rules`

保留 `implementation-review-rules` 作为“实现自审总闸门 + 汇总结论”。

新增子 skill：

1. `implementation-review-rules-10-core`
   description: 当代码实现完成准备进入测试前自审时触发。负责可读性、单一职责、命名、错误处理、日志与注释补齐的通用实现质量检查；不要用它代替目录归位或功能验证规则。

2. `implementation-review-rules-20-go-placement`
   description: 当 Go 改动涉及 `internal/service` 落点或 `internal/entity` 结构体归位时触发。负责 service 根目录落点与请求/响应结构体归位检查；不要用它代替包结构设计决策规则。

3. `implementation-review-rules-30-go-style`
   description: 当 Go 改动涉及函数签名或局部变量声明风格时触发。负责多参数签名、局部变量声明等编码风格闸门检查；不要用它代替格式化或命名策略规则。

4. `implementation-review-rules-40-go-thirdparty-response`
   description: 当 Go 接入第三方 API 并涉及响应解析时触发。负责“探测样例 -> 结构体建模 -> 禁止长期 map 硬编码解析”的自审闸门；若结构无法确认需暂停并反馈用户；不要用它代替测试脚本落点管理规则。

5. `implementation-review-rules-50-api-doc-sync`
   description: 当改动涉及后端 HTTP API 契约（路径、请求、响应、错误）时触发。负责测试前 Swagger/OpenAPI 同步检查；不要用它代替接口设计或请求响应模型定义规则。

## 3.3 拆分 `package-structure-rules`

保留 `package-structure-rules` 作为“结构总入口分流 + 最终裁决”。

新增子 skill：

1. `package-structure-rules-10-core`
   description: 当新增或修改包、目录、模块归属且需要判断基础分层职责时触发。负责通用目录职责、依赖方向与边界判定；不要用它代替语言专项规则。

2. `package-structure-rules-20-go-entry`
   description: 当 Go 项目涉及 `main.go` 启动入口、根级入口层目录（global/middleware/crontask/async）时触发。负责 Go 入口层落点与依赖方向约束；不要用它代替业务实现层风格规则。

3. `package-structure-rules-30-go-service-layout`
   description: 当 Go 改动涉及 `internal/service` 目录组织时触发。负责 service 子目录分层与根目录禁堆实现规则；不要用它代替实现质量自审规则。

4. `package-structure-rules-40-go-entity-placement`
   description: 当 Go 改动涉及请求/响应/第三方结果结构体定义时触发。负责 `internal/entity/<domain>` 归位规则与 service 行为层职责分离；不要用它代替请求响应字段设计规则。

5. `package-structure-rules-50-large-file-split`
   description: 当单文件达到 500 行及以上且持续扩展时触发。负责按功能拆文件与必要子目录/子包拆分落位；不要用它代替具体业务重构方案设计。

## 4. 第二批拆分（第一批稳定后）

## 4.1 拆分 `git-collaboration-rules`

1. `git-collaboration-rules-10-commit-granularity`
   description: 当准备提交且存在多业务改动时触发。负责提交粒度拆分策略与提交顺序；不要用它代替分支同步规则。

2. `git-collaboration-rules-20-commit-message`
   description: 当准备编写提交说明时触发。负责 `feat/fix` 提交规范、Windows 换行规范与消息结构；不要用它代替代码评审规则。

3. `git-collaboration-rules-30-readme-changelog`
   description: 当提交前需要更新根目录 `README.md` 改动日志时触发。负责时间格式、正序校验与日志条目规范；不要用它代替业务文档编写规则。

4. `git-collaboration-rules-40-go-precommit-guard`
   description: 当 Go 项目准备提交时触发。负责提交前阻断项（`test/` 外 `*_test.go`、`internal/service/*.go` 根目录直落等）扫描；不要用它代替实现自审规则。

## 4.2 拆分 `database-schema-rules`

1. `database-schema-rules-10-base`
   description: 当新增或修改表、字段、索引、约束、DDL 时触发。负责基础 schema 变更安全与兼容边界；不要用它代替查询实现规则。

2. `database-schema-rules-20-required-fields`
   description: 当设计或变更通用字段（如 created_at/updated_at/逻辑删除/毫秒时间戳）时触发。负责必备字段完整性与默认值要求；不要用它代替业务字段定义规则。

3. `database-schema-rules-30-money`
   description: 当新增或修改金额字段时触发。负责金额字段类型与精度约束（字符串存储）规则；不要用它代替业务换算逻辑规则。

4. `database-schema-rules-40-engine-charset`
   description: 当新增或修改表级参数时触发。负责 ENGINE/CHARSET/注释等表级标准约束；不要用它代替迁移发布流程规则。

## 5. 拆分后的命中顺序建议

以一次 Go 第三方 API 接入为例：

1. `package-structure-rules`（总入口分流）
2. `package-structure-rules-40-go-entity-placement`（结构体落点）
3. `test-program-rules-30-verify-script`（先探测响应）
4. `code-readability-rules`（实现清晰度）
5. `implementation-review-rules`（总闸门汇总）
6. `implementation-review-rules-40-go-thirdparty-response`（专项阻断）

## 6. 迁移执行建议

1. 先创建“完整子 skill 骨架”而非最小壳子：`SKILL.md` + `agents/openai.yaml` + 按需资源目录（`references/`、`scripts/`、`assets/`）。
2. 把父 skill 的对应章节与参考材料同时迁移到子 skill（优先下沉到 `references/`），父 skill 只保留“分流索引”。
3. 在每个子 skill `SKILL.md` 中显式声明资源读取路径与时机，避免隐式依赖父 skill 说明。
4. 更新 `agents/openai.yaml` 默认 prompt，避免仍命中过于宽泛的父 skill。
5. 每次只拆 1 个父 skill，避免一次性全仓震荡。
6. 每轮拆分后观察 1 周：
   - 误触发率是否下降
   - 漏触发是否上升
   - 平均命中 skill 数是否维持在 2~3
   - 子 skill 是否可独立执行（不回读父 skill 细节）

## 7. 验收标准

- 每个新子 skill 的 description 长度建议控制在 80~220 字。
- 每个子 skill 至少有 1 条明确“不要用它代替...”边界。
- 每个子 skill 必须具备完整功能结构：
  - `SKILL.md`（含执行流程与边界）
  - `agents/openai.yaml`（建议，且与 `SKILL.md` 一致）
  - 有细节资料时必须提供 `references/` 并在 `SKILL.md` 可导航
- 父 skill 不再承载过多执行细则，只保留分流与汇总职责。
- 拆分后同类任务的命中路径更短、更稳定、可复核。
