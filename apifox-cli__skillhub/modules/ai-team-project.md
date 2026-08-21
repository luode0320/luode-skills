# AI 团队项目定位 — project / settings

> 本模块覆盖「AI 团队对应项目」的 projectId 解析、默认项目登记、AI 分支工作流结合，以及**「用户为当前项目指定 Apifox 项目 → 持久化到项目 md → 后续会话自动复用」的强制规则**。已从 SKILL.md 继承：登录与项目、写入标准流程、AI 权限规则、AI 分支说明、必须询问用户。
>
> 背景：本仓库约定接口级测试与接口新增/更新统一落在 Apifox 组织下名为「AI」的团队对应项目中。本模块负责把「团队名 + 项目名」解析为 CLI 可用的 `--project <projectId>`，并确保**每个项目工作区**都明确登记过对应的 Apifox 项目，避免每次重复询问。

---

## ⚡ 强制规则：项目身份指明与持久化（首轮必读，最高优先级）

### 规则一：每个项目**首次**进入 Apifox 工作时，用户必须指明对应的 Apifox 项目

- 用户为本项目指定的 Apifox 项目位于 Apifox 组织下名为「AI」的团队下，**每个项目对应 [AI] 团队下的一个具体项目**
- 用户在第一次提"apifox / 接口 / 测试 / 同步 / 自动化测试"等相关任务时，**必须先确认具体是 [AI] 团队下的哪一个项目**（提供 projectId 或项目名）
- 不要替用户猜测项目，不要从历史 projectId 直接拿过来用 — 不同项目可能对接不同的 Apifox 项目

### 规则二：指明后必须**持久化到项目根目录的 `PROJECT_TEST.md`**（测试域单一事实源）

- 用户指明 Apifox 项目后，把以下信息**持久化写入项目根目录的 `PROJECT_TEST.md`**（若项目已有其他约定的测试文档路径，优先复用；默认推荐 `PROJECT_TEST.md`）：
  - Apifox 组织/团队名（如：组织名=「xx」，团队名=「AI」）
  - Apifox 项目名（如：「后管系统-golang-api」）
  - projectId（必须从 Apifox 客户端「项目设置 - 基本设置 - 项目 ID」或 `apifox project list` 获取）
  - 默认分支（如 `1.main`，或项目约定分支）
  - 登记时间（YYYY-MM-DD）
- **标准模板**：`PROJECT_TEST.md` 的完整模板见 `references/project-test-md-template.md`（含 Apifox 绑定表 + 测试覆盖度铁律 + 测试执行约定）。新项目接入时按模板生成；模板与 `modules/test-case-generation.md`（覆盖度铁律）、`modules/test-case.md`（CLI 操作）同源，skill 规则更新时同步回填模板的「测试覆盖度铁律」「测试执行约定」两节。
- **为什么是 `PROJECT_TEST.md` 而不是 `.workbuddy/`、`AGENTS.md`、`CLAUDE.md`、`PROJECT_MEMORY.md`、`README.md`**：
  - `.workbuddy/` 是 WorkBuddy 专属目录，Codex / Claude Code / Cursor 等工具不读取，导致多工具不通用
  - `AGENTS.md` / `CLAUDE.md` 是工具专属规则文件：写 AGENTS.md 只对默认平台生效，写 CLAUDE.md 只对 Claude 生效，且它们是"规则"不是"数据"，projectId 属数据
  - `PROJECT_MEMORY.md` 承载长期记忆（双区模型），157KB 级体量，projectId 属操作配置而非知识
  - `README.md` 面向人阅读，projectId 是内部配置不应进对外文档
  - `PROJECT_TEST.md` 与 `PROJECT_MEMORY.md` / `PROJECT_STYLE.md` 等 PROJECT_* 系列平级，职责单一（测试域），工具无关，任何 agent 工具都能读取
- **多工具通用方案**：`PROJECT_TEST.md` 是**单一事实源（SSOT）**；`AGENTS.md` 与 `CLAUDE.md` 各放**一行指针**（"Apifox 操作先读项目根 `PROJECT_TEST.md` 的 Apifox 项目绑定；未登记先询问用户"），不重复写 projectId，避免口径漂移
- 文件结构示例（详见标准模板）：

  ```markdown
  # 项目测试约定

  ## Apifox 项目绑定

  | 字段 | 值 |
  | ---- | -- |
  | 团队 | [AI] |
  | Apifox 项目名 | 后管系统-golang-api |
  | projectId | 1234567 |
  | 默认分支 | 1.main |
  | 登记时间 | 2026-08-19 |

  ## 说明
  - 本项目所有 apifox 操作（接口导入、测试用例创建/补全、运行）默认作用于上述 projectId。
  - 除非用户显式说明切换到其他项目，否则不再询问。
  ```

- 持久化前先询问用户是否同意写入本地文档（属于"写入本地配置文件"门控范围）
- 后续 apifox 操作默认从该 md 取 projectId，无需再问

### 规则二之补充：新项目接入 = 自动生成 PROJECT_TEST.md 模板（强制）

- **触发**：当前项目从未接入过测试域/apifox（项目根目录不存在 `PROJECT_TEST.md`），且用户首次提出 apifox / 接口 / 测试 / 自动化测试相关任务时
- **前置：确认 apifox CLI 已安装（强制）**：任何 apifox 操作前先 `apifox --version`；**未安装则立即按 SKILL.md「安装（强制，最高优先级）」流程安装**（npm install -g apifox-cli，慢则切 npmmirror，装完验证版本并确认登录），不得以"CLI 未安装"跳过任务
- **动作**：
  1. 按 `references/project-test-md-template.md` 标准模板生成 `PROJECT_TEST.md` 到项目根目录（Apifox 绑定表、本地测试环境表、环境变量登记表保持 *待登记* 占位）
  2. 询问用户指明 [AI] 团队下对应的 Apifox 项目（规则一）
  3. 用户指明后回填绑定表 → 完成接入
  4. **确认/创建开发环境**：若项目下无可用开发环境，按 `modules/environment.md` 创建，baseUrl `http://127.0.0.1:<项目端口>`，环境 ID 回填 `PROJECT_TEST.md` 的「本地测试环境（开发环境）」表
  5. **配置环境变量（强制）**：按 `modules/environment.md`「开发环境环境变量（强制）」节补齐开发环境变量——鉴权签名（apiKey/apiSecret/appId/nonce/signature）、默认测试登录账号密码（testUsername/testPassword）、token（登录用例 extractor 回写）等，变量清单回填 `PROJECT_TEST.md` 的「环境变量登记」表（只登记名称/用途/来源，**不登记敏感值**）
  6. 在 `AGENTS.md` / `CLAUDE.md` 各放一行指针（指向 `PROJECT_TEST.md`；若项目无这两个文件则跳过并在输出中说明）
- **后续其他项目**：同一 skill 在**每个新项目**首次接入时都会重复此流程，生成该项目自己的 `PROJECT_TEST.md`——该文件是**所有项目的标配**（如同 `AGENTS.md` / `PROJECT_MEMORY.md`），不是当前项目独有
- **何时不重复生成**：项目根目录已存在 `PROJECT_TEST.md`（或用户约定的其他测试文档）→ 直接复用，不覆盖已有内容
- **环境变量就绪校验（强制）**：用例运行失败出现 401/403/签名错误/token 无效时，**先查开发环境变量是否缺失/过期**（对照 `PROJECT_TEST.md`「环境变量登记」表逐项核对），再查接口/代码问题——不要把环境变量缺失导致的失败算成接口失败（与 `modules/test-data-and-judgement.md` 的阻断分类一致）

### 规则三：后续会话自动复用，无须重复指明

- 会话开始或任何 apifox 操作前，先读取项目根目录下的 `PROJECT_TEST.md`（或用户约定的测试文档路径）
- 命中登记记录 → 直接使用登记的 projectId，不再询问
- 未命中、记录过期、用户主动要求切换 → 走规则一/二

### 规则四：未指明时必须**阻断**会话

- 用户提 apifox 相关任务（接口导入、测试用例创建/补全、自动化测试运行、契约校验、API 同步）但**当前项目从未登记过 Apifox 项目**时：
  1. **立即停止执行 apifox 写操作 / 查询操作**（包括看起来无害的 list、whoami 之外的探测）
  2. 输出明确的指引话术（参见下文模板）
  3. 等待用户指明后再恢复
- 不要用「先随便选一个」「我先试试别的项目」绕过
- 不要因为用户提的是查询任务就跳过指明 — 查询也需要明确的作用对象

### 阻断话术模板（建议格式）

```
⚠️ 本项目尚未登记 Apifox 项目，apifox 操作已阻断。

请提供以下任一信息以完成登记：
- Apifox 项目名（如「后管系统-golang-api」），或
- projectId（在 Apifox 客户端「项目设置 - 基本设置 - 项目 ID」复制）

登记完成后我会写入项目根目录 `PROJECT_TEST.md`，后续不再重复询问。
```

### 规则五：用户指明即持久化前必须先确认

- 用户指明项目（口头/项目名/projectId 三种形式任一）后，**先复述确认一次**（"您指的是 [AI] 团队下「xxx」，projectId=xxxxxx，对吗？"），确认无误再持久化写入 md
- 多个候选项目（如「后管系统」「后管系统-v2」「后管系统-golang-api」并列）必须列出候选让用户选，不要猜测

---

## 解析 projectId 的标准流程（强制）

0. **确认 apifox CLI 已安装（强制前置）**：`apifox --version`；**未安装则立即安装**（npm install -g apifox-cli，慢则切 npmmirror 镜像），装完验证版本，未登录先登录——见 SKILL.md「安装（强制，最高优先级）」节。CLI 不可用则**阻断**，不得以任何形式跳过 apifox 任务
1. **尝试读登记文件**：先看项目根目录是否存在 `PROJECT_TEST.md`（或用户约定的其他测试文档），有则直接用登记的 projectId，跳到第 5 步验证
2. **确认登录**：`apifox whoami`；未登录先 `apifox login --with-token <TOKEN>`（token 由用户提供，凭证存 `~/.apifox/config.toml`，不要打印到日志或聊天摘要）
3. **列出可访问项目**：`apifox project list`
4. **按团队名「AI」过滤**：
   - 若输出含团队/团队 ID 字段，定位团队名为「AI」的项目
   - 若输出不含团队字段，按项目名与用户确认哪个是「AI 团队」对应项目
   - 多个候选项目时，必须询问用户，不要自行猜测
5. **持久化登记**：用户指明后写入 `PROJECT_TEST.md`（见规则二），同时 `.apifox/settings.json` 的 `projectId` 字段按需可选写入
6. **验证**：`apifox endpoint list --project <projectId> --limit 1` 或 `apifox project list` 复核 projectId 有效

## 默认项目登记（.apifox/settings.json）

- 项目未指定时，CLI 先查 `.apifox/settings.json` 中是否有默认 `projectId`
- 写入 `settings.json` 属于本地配置写入，执行前必须先询问用户
- 一个工作区可以有多个项目，`settings.json` 只记录默认项目；切换项目用显式 `--project`

## 分支策略：apifox 测试专用项目直接 main 分支（强制）

**用户为 apifox 测试单独创建的项目（apifox 测试专用项目）内，接口文档操作、测试、补充测试用例默认直接在 `main` 分支（如 `1.main`，即项目默认分支）操作**：

- **不新开分支**：不创建 AI 分支（`ai/年月日-...`），也不开 `api` 等临时分支做自动化测试
- **不做合并环节**：无「开分支 → 分支上自动化测试 → 合并回 main」的多余操作——apifox 测试专用项目本身已是项目级隔离，分支级隔离无必要
- 所有命令统一带 `--branch main`（或项目登记的默认分支名），保持同一分支上下文
- 直接编辑 main 分支需 Apifox 客户端 2.8.32+「项目设置 - 功能设置 - AI 功能设置 - 外部 AI 编辑权限」开启；未开启或主分支受保护（isProtected）时，先向用户说明并让其开启/选择处理方式，而非默认改走 AI 分支

### AI 分支工作流（仅非测试专用项目 / 主分支不可直接写时兜底）

接口新增/更新到 apifox 时，仅当目标项目**不是** apifox 测试专用项目（如共享主项目），或 main 分支受保护/外部 AI 直接编辑权限未开启时，才走 AI 分支隔离，避免直接污染主分支：

```text
确认源分支和目标项目（--project <projectId>）
  → 创建 AI 分支（命名：ai/年月日-from-来源分支名-接口同步）
  → pick-to 导入源分支已有接口（新建接口不需要）
  → 在 AI 分支上 import / endpoint create / update / test-case 落地
    （所有命令带 --branch <aiBranchName>）
  → 运行验证（test-case run --environment <开发环境Id>）
  → merge-request preview 让用户确认
  → 用户确认后 create merge-request 或 merge
```

- 主分支受保护时（isProtected）优先 `merge-request`，不要直接 `merge`
- AI 分支 24 小时内与来源分支无差异将自动归档；修改源分支已有资源前必须先 `pick-to`
- 直接编辑主分支需 Apifox 客户端 2.8.32+「项目设置 - 功能设置 - AI 功能设置 - 外部 AI 编辑权限」开启；未开启时选 AI 分支流程

## 不可违反规则

1. **首轮未指明 Apifox 项目 → 必须阻断会话**，不得用任何「先试试」绕过
2. 用户指明 Apifox 项目后必须**持久化到项目根目录 `PROJECT_TEST.md`**（单一事实源），后续复用；`AGENTS.md` / `CLAUDE.md` 只放一行指针，不重复写 projectId
3. 多候选项目必须列出让用户选，不要猜测
4. 写入 `.apifox/settings.json` 前必须询问用户
5. 目标主分支受保护时优先 merge-request，不直接 merge
6. 不要在 AI 分支里修改源分支已有资源而不先 pick-to
7. 不要在分支任务中省略 `--branch`
8. 团队名/项目名不明确时，先问用户，不要猜测
9. **apifox 测试专用项目直接在 `main` 分支操作（接口文档操作/测试/补用例），不新开 AI 分支 / api 分支，不做「开分支 → 自动化测试 → 合并回 main」的多余操作**
