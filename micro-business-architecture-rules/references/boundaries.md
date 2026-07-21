# 微业务架构规则与相邻 skill 边界

本文件定义 `micro-business-architecture-rules`（下称「本 skill」）与相邻 skill 的职责边界，并澄清易混淆的关键术语。目的：让本 skill 只承担「业务横向隔离 + 公共接口包（contract）通信 + 触发/标记」这一差异化职责，其它职责一律委托、依赖或衔接给对应 skill，避免规则重叠、越权改写与误触发。

本 skill 的差异化职责（只做这三件）：

1. 业务垂直切分：把单项目单服务按业务切成互不横向依赖的业务目录包（`business/*`）。
2. 受控通信：跨业务只经公共接口包 `contract/` 以接口形式通信，禁止 `business/A` 直连 `business/B`。
3. 触发与标记：新项目首轮引导、用户确认后写微业务标记、据标记守护。

其余一切（技术分层落点、接口抽象取舍、文档路径命名、架构文档沉淀、规则文件与四件套自举、任务级拆分）都不归本 skill，见下表。

---

## 边界总览表

| skill | 关系 | 边界说明 |
|---|---|---|
| `package-structure-rules` | 强联动 | 业务包**层内**的技术分层落点（router/controller/service/repository/handler/logic/model/store）全权交给它；本 skill 只在其之上补「business 横向隔离 + contract 通信」这一层，不重写分层。 |
| `code-readability-rules` | 强边界 / 防冲突 | `contract/` 接口只为**真实存在的跨业务调用点**建立；本 skill 服从其反过度抽象、反单实现接口判定，禁止为「解耦/以后扩展」预建单实现接口。 |
| `artifact-storage-rules` | 依赖 | 任何 doc 产物的路径与命名一律引用其 `references/path-map.yaml`，本 skill 不自定义目录或命名规则。 |
| `architecture-doc-rules` | 弱联动 | 业务包与接口契约的结构结论**可**回写到 `doc/1-架构/3-模块职责.md`，属可选增强，不是本 skill 的强制产物。 |
| `project-rule-file-bootstrap-rules` / `project-memory-file-bootstrap-rules` | 衔接 | 新会话首轮的规则文件（前者）与项目记忆四件套（后者）自举交给它们；微业务标记的 upsert 由本 skill 自有脚本完成，不侵入 bootstrap 脚本。 |
| `implementation-planning-rules` | 术语区分 | 其「垂直切片」是**任务拆分**语义，本 skill 的「业务包切分」是**代码目录**语义，两者不可混用、不得互相误触发。 |

---

## 1. `package-structure-rules`（强联动）

- 委托内容：业务包**内部**的技术分层落点，例如 Go 的 `handler/` `logic/` `model/` `store/`，或其它语言等价的 router/controller/service/repository 分层规则，全部沿用 `package-structure-rules` 的 `structure-general.md` 与 `go-package-layout.md`。
- 本 skill 只补一层：`internal/business/*` 之间的横向零依赖，以及跨业务经 `internal/contract/*` 通信。这一层是 `package-structure-rules` 未覆盖的差异化价值（它只管「一个业务/一个模块内部怎么分层」，不管「多个业务之间如何隔离与通信」）。
- 禁止行为：本 skill 不得重新定义、复述或改写分层措辞；涉及层内目录时只引用 `package-structure-rules`，不在本 skill 的 references 里另立一套分层标准。

## 2. `code-readability-rules`（强边界 / 防冲突）

- 冲突风险：若把「业务之间一律抽接口」写死，会与 `code-readability-rules` 的「反单实现接口 / 反过度抽象 / 深模块优先」判定直接冲突。
- 本 skill 的硬约束：`contract/` 接口**只在能写出真实调用方**（存在真实跨业务调用边界）时才建立；单业务包没有外部业务调用者时，**禁止**预建接口。无跨业务调用的业务包不建 `contract/` 目录。
- 服从关系：当本 skill 的接口建议与 `code-readability-rules` 的反过度抽象判定出现张力时，以 `code-readability-rules` 为准。本条同时在 `references/isolation-and-communication.md` 与本文件双处显式声明，确保读者从任一入口都能看到「服从 `code-readability-rules`」的口径。

## 3. `artifact-storage-rules`（依赖）

- 依赖内容：本 skill 涉及的所有 doc 产物路径与命名（例如需求、实施、测试、审查、架构文档的根目录与主入口命名）一律以 `artifact-storage-rules/references/path-map.yaml` 为单一真相源。
- 禁止行为：本 skill 不自定义 doc 目录、不自定义主入口文件命名、不新增平行的路径约定。凡是本 skill 需要引用某个 doc 落点，只写「引用 `path-map.yaml` 的对应键」，不硬编码路径字符串。
- 说明边界：业务代码目录（`internal/business/`、`internal/contract/` 等）属于**代码结构**，不是 doc 产物，由本 skill 的 `directory-layout.md` 定义；`artifact-storage-rules` 只约束 `doc/` 与 `skill/` 等研发产物根目录，两者不重叠。

## 4. `architecture-doc-rules`（弱联动）

- 弱联动内容：业务包清单、公共接口契约（谁暴露 / 谁实现 / 谁调用）等结构结论，**可以**回写到 `doc/1-架构/3-模块职责.md`，作为项目架构文档的一部分沉淀。
- 弱在何处：这是**可选增强**而非强制产物。本 skill 的强制产物是各业务包 README、全局业务包索引与公共接口契约清单（见 `md-convention.md`）；是否额外回写架构文档由项目按需决定。
- 落点约束：若回写，路径仍遵循 `artifact-storage-rules` 的 `path-map.yaml`，不因回写而绕开路径单一真相源。

## 5. `project-rule-file-bootstrap-rules` / `project-memory-file-bootstrap-rules`（衔接）

- 衔接内容：新会话首轮的规则文件（`CLAUDE.md` / `AGENTS.md`）检测与创建由 `project-rule-file-bootstrap-rules` 负责，项目记忆四件套（`PROJECT_CURRENT.md` / `PROJECT_MEMORY.md` / `PROJECT_HISTORY.md` 等）的自举由 `project-memory-file-bootstrap-rules` 负责；两者共用同一份 `project-rule-file-bootstrap-rules/scripts/bootstrap_agents.sh`。
- 本 skill 的接续点：在 bootstrap 完成通用规则文件自举之后，本 skill 负责微业务专项引导（建议采用微业务架构）与标记写入。
- 关键隔离：微业务标记的幂等 upsert（向 `CLAUDE.md` / `AGENTS.md` 追加受管章节 `## 微业务架构约束`、向根目录 `项目设计.md` 追加业务索引段）由本 skill 自有脚本 `micro_business.py init` 完成，**不侵入、不修改** bootstrap 的脚本；本 skill 只复用 bootstrap 的 header upsert 语义（定位替换 / 追加），不改写其实现。

## 6. `implementation-planning-rules`（术语区分）

- 易混术语：`implementation-planning-rules` 中的「垂直切片」指**任务拆分**语义——把一个需求拆成端到端、可独立闭环的最小实施任务（跨前后端一条链路的一个功能片）。
- 本 skill 的「业务包切分」是**代码目录**语义——把一个服务的代码按业务垂直切成互不横向依赖的目录包（`business/order`、`business/user`）。
- 区分要点：一个是「计划怎么拆任务」，一个是「代码怎么摆目录」；两者可以同时存在但不是同一件事。本 skill 的 description 必须显式区分该术语，避免规划阶段的「垂直切片」误触发本 skill，或本 skill 被误当作任务拆分工具。

---

## 触发发生地澄清

本 skill 的自动触发发生在**用户新建的业务项目**里，触发链路为：

1. harness 全局加载所有 skill（本 skill 作为全局可见的规则 skill 之一被加载）；
2. `skill-hit-check-rules` 每轮据本 skill 的 `description` 关键词命中；
3. 命中后检测当前是否为新 / 空仓库（无 `internal/business/` 等业务根且无既有微业务标记）；
4. 判定为候选新项目时，向用户**建议**采用微业务架构，经确认后写标记并引导。

需要明确区分的两个仓库：

- `luode-skills` 仓库（即当前 `D:\luode\luode-skills`）：只是**开发与存放**本 skill 的地方。它自身不是微业务业务项目，本 skill 不应在这个仓库里对「是否采用微业务架构」发起引导或写标记。
- 用户未来新建的业务项目仓库：才是本 skill 真正的触发发生地与作用对象。

因此，在 `luode-skills` 仓库里编辑、测试、注册本 skill，与本 skill 在业务项目中被命中触发，是两件不同的事，不得混淆。
