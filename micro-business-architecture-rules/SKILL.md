---
name: micro-business-architecture-rules
description: 当新建项目 / 新会话首轮检测到新或空仓库（缺业务代码骨架），或用户提出「微业务 / 伪微服务 / 按业务分目录包 / 业务隔离 / 业务互不关联 / 公共接口包通信 / 新业务开新包 / 一个项目一个服务的伪微服务」等诉求，或项目已存在微业务标记时自动触发。负责把单项目单服务按业务垂直切分为互不关联的业务目录包，业务包之间禁止横向 import，跨业务只经公共接口包（contract）以接口形式通信；定义 Go 优先的目录布局、每业务包统一 README 与全局业务 / 接口契约索引 md 规则，并提供幂等脚本建业务包骨架、写微业务标记与校验跨业务非法依赖，让 AI 只读单个业务包上下文即可分析实现逻辑。目录 / 命名统一引用 `artifact-storage-rules`，分层落点交给 `package-structure-rules`，接口抽象服从 `code-readability-rules` 的反单实现接口判定；不要用它代替需求分析、实施规划、分层落点或实际编码。
---

# 微业务架构规则

## 目标

- 把「微业务（伪微服务）」架构固化为可自动命中、可校验、可交接的规则。
- 新项目开局即引导按「业务包隔离 + 公共接口包通信」组织代码。
- 每个业务包自带统一 README，使 AI 只读单业务上下文即可分析与实现。
- 新业务新开目录包，旧业务只在自己包内演进，互不影响、互不关联。

## 核心理念（为什么这么做）

- AI 天然适合「微服务」式上下文：每次只聚焦一个业务就能把实现逻辑读清楚。
- 真微服务（独立进程 / 独立部署 / 独立仓库）过重；微业务只在**一个项目、一个服务**内做伪微服务切分。
- 不同业务放到不同目录包，各自互不影响、互不关联；需要交互时统一经一个公共接口包以接口形式通信。

## 自动触发信号

- 用户提出「微业务 / 伪微服务 / 按业务拆目录包 / 业务互不关联 / 公共接口包通信 / 新业务新开包」等诉求。
- 新会话首轮检测到新或空仓库（无 `internal/business/` 等业务根、且无微业务标记）。
- 项目已存在微业务标记（`CLAUDE.md` 的 `## 微业务架构约束` 章节，或 `项目设计.md` 的微业务段）。
- 用户要求「用微业务架构建项目 / 新增一个业务包 / 校验业务隔离」。

## 进入后先做什么

1. 先明确触发发生地：本 skill 的引导对象是**当前业务项目**，不是本 skill 的存放仓库（`luode-skills`）。
2. 新会话首轮强制联动 `project-rule-file-bootstrap-rules`，确保规则文件（`CLAUDE.md` / `AGENTS.md`）已存在。
3. 检测是否为新 / 空仓库，或是否已有微业务标记（判定标准见 `references/trigger-and-marker.md`）。
4. 若为候选新项目：先**建议**采用微业务架构，经用户确认后再写标记；不得未经确认直接写入。
5. 若已有标记：进入守护模式，按隔离与通信契约检查后续改动。

## 默认执行流程

1. 先读 `references/trigger-and-marker.md`，确认触发判定、标记写入与守护流程。
2. 需要目录落点时读 `references/directory-layout.md`。
3. 需要判断业务隔离与跨业务通信时读 `references/isolation-and-communication.md`。
4. 需要产出或校验业务包 md 时读 `references/md-convention.md`。
5. 判断与相邻 skill 边界时读 `references/boundaries.md`。
6. 新建业务包用 `scripts/micro_business.py scaffold <业务名>`；写微业务标记用 `init`；校验隔离用 `check`。
7. 结构结论按需弱回写 `doc/1-架构/3-模块职责.md`（路径遵循 `artifact-storage-rules`）。

## 微业务核心原则（详见 references）

1. **业务垂直切分**：每个业务是一个自包含目录包，内部含自己的入口 / 逻辑 / 模型 / 存储访问。
2. **横向零依赖**：业务包 A 禁止直接 import 业务包 B 的任何内部路径。
3. **受控通信**：跨业务调用只经公共接口包 `contract/`，由被调用方实现并注册，调用方依赖接口（依赖倒置）。
4. **接口按需**：只为真实存在的跨业务调用点建接口；无外部调用者的业务包不预建接口（服从 `code-readability-rules`）。
5. **新增即新包**：新业务新开目录包，旧业务包不被改动。
6. **单业务可读**：每业务包统一 README + 全局索引，AI 读「全局索引 → 该业务包 README + 代码」即可分析，无需扫全仓。

## 与相邻 skill 的边界

- 不替代 `package-structure-rules` 定义技术分层（router / controller / service / repository）落点；本 skill 只补业务横向隔离 + `contract` 通信这一层。
- 接口抽象服从 `code-readability-rules`：只为真实跨业务调用点建接口，禁止「一个业务一个接口」式单实现接口预建。
- 目录 / 命名 / 文档产物路径统一引用 `artifact-storage-rules`，不自定义。
- 结构结论可弱回写 `architecture-doc-rules` 的 `doc/1-架构/3-模块职责.md`。
- 新会话首轮规则文件自举交给 `project-rule-file-bootstrap-rules`，本 skill 不侵入其脚本。
- 与 `implementation-planning-rules` 的「垂直切片」区分：那是任务拆分语义，本 skill 是代码业务包切分。

## references 读取规则

- 默认先读 `references/trigger-and-marker.md`（触发判定、标记与守护）。
- 需要目录布局时读 `references/directory-layout.md`。
- 需要隔离与通信判断时读 `references/isolation-and-communication.md`。
- 需要业务包 md 规范时读 `references/md-convention.md`。
- 判断相邻 skill 边界时读 `references/boundaries.md`。

## 执行结果归档要求

- 业务包骨架与 README 落在目标项目代码目录（如 `internal/business/<域>/`），不落 `doc/`。
- 全局业务包索引落 `internal/business/README.md`，公共接口契约清单落 `internal/contract/README.md`。
- 微业务采用决策与业务清单入口可弱回写根目录 `项目设计.md` 与 `doc/1-架构/3-模块职责.md`。
- 微业务标记 upsert 到目标项目 `CLAUDE.md` / `AGENTS.md` 的 `## 微业务架构约束` 章节。

## 极致完整性与零决策硬闸门

- 新增业务包必须同时产出该包 README，并更新全局业务索引；缺任一视为未收口。
- 跨业务调用必须经 `contract/` 接口，禁止 `business/A` 直接 import `business/B`；违规必须由 `check` 报出并修复。
- 未经用户确认不得写入微业务标记；即使判定为新仓库，也只先建议、不擅自写入。
- 目录 / 命名不得绕开 `artifact-storage-rules`；接口不得违反 `code-readability-rules` 的反单实现接口判定。
