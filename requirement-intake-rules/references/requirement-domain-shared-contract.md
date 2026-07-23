# 需求域共享契约

## 对外心智模型

需求域统一采用“新需求接入单入口 + 条件路由 + 专项自动触发 + 下游移交”：

- 新需求接入：`Idea -> requirement-intake-rules`。
- 内部条件路由：`initial-discovery`、`gap-routing`。
- 独立专项 Owner：`requirement-boundary-rules`、`requirement-splitting-rules`、`requirement-change-rules`；专项信号出现时继续自动触发，不得被 intake 抢占。
- 下游移交：`acceptance-criteria-rules -> implementation-planning-rules -> Test -> Review -> final-acceptance-rules`。

`requirement-intake-rules` 是**新需求接入唯一自动触发入口和唯一需求主文档 Owner**，不是整个需求域唯一自动触发 Skill。

## Owner 与路由

1. `requirement-intake-rules`：接收新需求、整理资料并维护唯一需求主文档。
2. `initial-discovery`：粗略 idea、资料不足但可主动查证时，在 intake 内主动侦察；不形成第二个顶层 Skill。
3. `gap-routing`：只处理侦察后仍无法补齐、存在多个合理解释且会影响实现方向的关键缺口；保留原 gap aliases，但旧 Skill 名称不再作为运行入口。
4. `requirement-boundary-rules`：范围、兼容、上下游和历史问题归属裁决。
5. `requirement-splitting-rules`：业务切片、依赖关系和当前优先闭环。
6. `requirement-change-rules`：已确认需求的语义变更、影响失效和重规划信号。
7. 条件路由和专项 Owner 收敛后，需求域结束并向下游移交。

## 唯一事实来源

- 同一需求只能维护一份由 `artifact-storage-rules` 定位和命名的需求主文档。
- discovery、gap、边界、拆分和变更不得各建长期平行文档；gap 临时文档只在缺口未关闭时存在，确认后必须回填主文档并删除。
- 当前代码与真实资料优先于旧文档；结论冲突时保留来源、差异、决策和回滚证据，不得静默覆盖。
- 正式需求主文档未真实落盘前，禁止进入实施规划或正式编码；用户先前的开工表达不替代前置验收、正式实施计划和当前有效边界。

## 下游移交

1. `acceptance-criteria-rules` 唯一负责前置验收字段和 `AC-*`。
2. `implementation-planning-rules` 唯一负责实施总览、实施周期、文件/符号落点、真实测试命令、样本断言、清理、回滚和逐任务“实现 -> 测试 -> 审查 -> 验收”闭环。
3. `requirement-splitting-rules` 只输出业务切片、业务依赖和当前优先闭环，作为实施规划输入；不得在需求拆分阶段自建实施周期或冻结代码落点。
4. `requirement-change-rules` 只声明哪些需求、验收、计划、测试和审查结论失效，以及应回开什么 Owner；实施文档的结构和创建方式仍由 `implementation-planning-rules` 决定。
5. 测试与审查完成后，`final-acceptance-rules` 才能最终放行。

## 外部唯一 Owner

| 规则 | 唯一 Owner |
| --- | --- |
| 需求完整性、稳定 ID、`N/A + 原因 + 证据` 和追踪字段 | `extreme-completeness-standard.md` |
| 需求文档结构、图形与占位模板 | `requirement-structure-template.md` |
| 边界字段和 `BOUND-*` | `requirement-boundary-rules/references/boundary-checklist.md` |
| 业务切片、依赖 DAG 和 `SLICE-*` | `requirement-splitting-rules/references/splitting-dimensions.md` |
| 变更分类、失效传播和 `CHG-*` | `requirement-change-rules/references/impact-recheck.md` |
| 需求文档路径、命名、图片根目录和同文档更新 | `artifact-storage-rules` |
| 前置验收字段和 `AC-*` | `acceptance-criteria-rules` |
| 实施总览、周期、文件/符号与真实测试闭环 | `implementation-planning-rules` |
| 最终落盘存在性与普通语言门禁 | `artifact-delivery-gate-rules` |

根 `SKILL.md` 只保留触发、职责和移交；以上 Owner 的细则不得复制成竞争规则，也不得因引用化而跳过。

## 共享保护语义

- **自动触发**：不依赖用户点名；intake 只独占新需求接入，boundary、splitting、change 继续按专项信号自动触发。
- **先侦察后 gap**：能通过项目、代码、schema、上下游、URL、GitHub、网站或官方文档主动查证的内容，先进入 `initial-discovery`；侦察仍无法收敛才进入 `gap-routing`。
- **禁止猜测**：一次只推进一个真实关键问题；无证据内容只能是候选、假设或待确认项。
- **local 红线**：数据库、缓存、消息队列、HTTP/RPC 和服务连接只能使用 local 配置；test、staging、pre、release、prod/production 一律阻断。
- **授权**：未授权默认值、权限、兼容、数据、异常和方向选择不得写成确定结论；P0/P1 阻断，P2 必须记录授权人、有效期和复核证据。
- **暂停与停止**：关键 route 未收敛时保持 `blocked`；用户明确暂停、停止或不继续时立即停止扩散，恢复时从已落盘状态继续。
- **回滚与证据**：变更、回开、缺口关闭和路线回退必须保留来源、差异、清理、回滚和关闭证据。
- **最终落盘**：路径、图片、Mermaid、普通语言、验收适用性和文档存在性由外部 Owner 核验；未真实落盘不得口头宣称完成。

## 跳转规则

- 用户只给 idea：intake 后进入 `initial-discovery`。
- 用户给完整资料包：直接进入 intake；资料矛盾或需补查时进入 `initial-discovery`。
- 用户给项目路径、URL、数据库、GitHub、第三方服务或 API 文档入口：进入 `initial-discovery` 扩展侦察。
- `initial-discovery` 后立即创建或更新同一份需求主文档，再按信号进入 `gap-routing`、boundary、splitting 或 change。
- 侦察后仍缺关键业务取舍：进入 `gap-routing`，一次只推进一个真实关键问题，不预填答案。
- 范围、兼容、旧逻辑或历史问题归属不清：自动触发 boundary。
- 多模块、多页面、多接口、多角色或多个独立子系统：自动触发 splitting。
- 已确认需求出现新增条件、默认值、优先级、范围或交付物变化：自动触发 change。
- 原实现不符合原需求：进入 Bug 域，不包装成 change。
- 任一关键条件路由未收敛时，阻断进入 `acceptance-criteria-rules` 和 `implementation-planning-rules`。
- 需求稳定后先建立前置验收，再进入只读实施规划；正式编码仍需满足当前有效开工授权和执行边界。
