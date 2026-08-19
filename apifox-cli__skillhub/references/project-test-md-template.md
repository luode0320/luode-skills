# 项目测试约定（PROJECT_TEST.md）— 标准模板

> 本文件是**所有项目接入测试域 / apifox 时的标配文件模板**，由 apifox skill 在「新项目接入」流程中自动生成到项目根目录。
> 用途：作为项目测试域**单一事实源（SSOT）**——Apifox 项目绑定、测试覆盖度铁律、测试执行约定统一记录于此，任何 AI 工具（WorkBuddy / Codex / Claude Code / Cursor 等）都可读取。
>
> 使用方式：复制本模板到项目根目录 `PROJECT_TEST.md`，回填「Apifox 项目绑定」表后即生效。**未登记 Apifox 项目前，任何 apifox 操作必须阻断并要求用户指明。**

---

```markdown
# 项目测试约定（PROJECT_TEST.md）

> 本项目测试域**单一事实源（SSOT）**：Apifox 项目绑定、测试覆盖度约定、测试执行约定统一记录于此。
> 任何 AI 工具（WorkBuddy / Codex / Claude Code / Cursor 等）做 apifox 操作前，先读本文件确认项目身份与测试约定；未登记 Apifox 项目时**必须先向用户指明，禁止猜测或"先试试"**。

## Apifox 项目绑定

| 字段 | 值 |
| ---- | -- |
| 团队 | [AI] |
| Apifox 项目名 | *待登记（用户指明后填写）* |
| projectId | *待登记* |
| 默认分支 | *待登记* |
| 登记时间 | *待登记* |

### 本地测试环境（开发环境 = local）

| 字段 | 值 |
| ---- | -- |
| 环境名 | 开发环境（Development） |
| baseUrl | http://127.0.0.1:<项目端口> |
| 项目端口 | *待登记（按项目后端启动配置）* |
| 环境 ID | *待登记（apifox environment list 后回填）* |

- **默认测试执行环境 = apifox「开发环境」**：新项目接入 apifox 时，若项目无可用开发环境，默认创建，baseUrl 用 `http://127.0.0.1:<项目端口>`，用于 API 接口调试与测试。
- **三环境约定**：Apifox 项目默认自带 开发环境 / 测试环境 / 正式环境——开发环境 = local（允许，baseUrl 指向 127.0.0.1:端口）；**测试环境 / 正式环境保留存在但 agent 禁止选用**（不删除、不修改、不选用，仅由人/CI 使用）。
- 端口来源：项目后端本地启动端口（如 `config_local*`、docker-compose、启动脚本声明的端口）。
- 测试前先确认本地服务已启动且端口可达（`curl http://127.0.0.1:<端口>/health` 或等价检查）。
- 禁止新建指向 test / prod / staging / pre / release 的 environment。

### 环境变量登记（开发环境）

| 变量名 | 用途 | 来源 | 是否敏感 |
| ------ | ---- | ---- | -------- |
| *待登记，如 apiKey / apiSecret* | 鉴权签名 | *local 配置/用户提供* | 是 |
| *待登记，如 testUsername / testPassword* | 默认测试登录（**管理员账号**） | *local 配置/用户提供* | 是 |
| *待登记，如 token* | 登录后提取回写 | *登录用例 extractor / 前置脚本续期* | 是 |
| *待登记，如 loginUrl* | 登录接口地址（前置续期脚本用） | *项目启动配置* | 否 |

- **开发环境必须配置齐备环境变量**（鉴权签名 apiKey/apiSecret、默认测试登录账号密码等），缺失即视为开发环境未就绪，用例运行失败先查环境变量。
- **敏感变量值不落本文件**：只登记名称/用途/来源，值在 apifox 环境变量中配置（用 CLI 写入避免暴露）。
- 取值只从 local 本地配置（`config_local*` / `.env.local` / `.env.development`）或用户提供，禁止从 test/prod/staging 配置取。

### 鉴权自动化约定（token/401/403）

- **测试默认使用管理员账号**（`testUsername`/`testPassword`），权限最全，普通账号 403 不是接口 bug。
- **token 必须自动获取/续期**，禁止手工复制粘贴：登录用例 extractor 提取（方案 A）→ 前置脚本自动重登（方案 B，token 过期快必用）→ 本地脚本构造（方案 C）→ 全局身份认证（方案 D）。完整方案见 apifox skill `modules/test-auth.md`。
- **401/403/签名错误优先查环境变量/鉴权配置**（token 过期、账号权限、apiKey 不匹配），再查接口代码——不算接口失败。

### 说明

- 本项目所有 apifox 操作（接口导入、测试用例创建/补全、自动化测试运行、契约校验）默认作用于上述 projectId。
- 除非用户显式说明切换到其他项目，否则不再重复询问。
- 登记方式：用户提供 Apifox 项目名或 projectId（「项目设置 - 基本设置 - 项目 ID」），确认后回填上表。
- 多工具通用约定：`AGENTS.md` / `CLAUDE.md` 仅保留指向本文件的一行指针，**不重复写入 projectId**，避免口径漂移。

## 测试覆盖度铁律（强制）

- **每个接口必须有 正向 + 负向 + 边界值 三类用例**，缺一类视为覆盖缺口，不得宣称"用例已建好"。
- **正向用例必须覆盖业务参数**（Query/Body 全参数），不能只测分页（pageSize/pageIndex）。
- **POST / PUT / PATCH / DELETE 接口必须有完整用例**（≥ 正向含完整 body + 负向 + 边界值），禁止 0 用例。
- 有鉴权（securityScheme）的接口必须补安全性用例（无 Token / Token 过期 / 权限不足）。
- 补全前先按接口列覆盖矩阵（现有正向/负向/边界值/计划补），给用户确认后再逐个创建。

## 测试执行约定

- 接口级测试执行统一走 apifox 测试链路（`apifox test-case run` / `test-suite run`）。
- **apifox CLI 是硬依赖（强制）**：任何 apifox 操作前先 `apifox --version`；**未安装必须立即安装**（`npm install -g apifox-cli`，慢则切 `--registry=https://registry.npmmirror.com/`），装完验证版本并登录，不得以"CLI 未安装"跳过任务（完整规则见 apifox skill SKILL.md「安装（强制，最高优先级）」节）。
- **默认测试执行环境 = apifox「开发环境」**：baseUrl 固定 `http://127.0.0.1:<项目端口>`（见上「本地测试环境」表）；本地服务未启动时先启动再测。
- **开发环境环境变量必须齐备**：鉴权签名 apiKey/apiSecret、默认测试登录账号密码等（见上「环境变量登记」表）；用例运行失败（401/403/签名错误）先查环境变量是否缺失。
- **三环境红线**：开发环境 = local（允许）；测试环境 / 正式环境 agent 禁止选用（保留存在，仅由人/CI 使用）。运行测试显式 `--environment <开发环境Id>` 防误选。
- 用例真实运行通过 = 在 apifox runner 中全绿，不是写完就收口。
- 覆盖达标 = 「自动化测试」菜单下 正向 / 负向 / 边界值 三个分类都有用例，非 GET 接口有完整覆盖。

## 变更记录

- YYYY-MM-DD：创建本文件，确立测试域单一事实源；Apifox 绑定待用户首次指明后登记。
- YYYY-MM-DD：新增「本地测试环境」表；明确默认测试执行环境 = apifox「开发环境」（baseUrl `http://127.0.0.1:<项目端口>`），测试/正式环境禁止选用。
- YYYY-MM-DD：新增「环境变量登记」表；开发环境必须配置齐备鉴权签名/登录账号等环境变量，敏感变量值不落本文件。
```

---

## 生成与维护约定（skill 侧）

- **生成时机**：新项目首次进入 apifox / 测试任务、且项目根目录不存在 `PROJECT_TEST.md` 时，由 apifox skill「新项目接入」流程自动生成本模板（见 `modules/ai-team-project.md` 规则二）。
- **同步规则**：本模板与 `modules/test-case-generation.md`（覆盖度铁律）、`modules/test-case.md`（CLI 操作）、`modules/environment.md`（开发环境约定）同源；skill 规则更新时同步回填本模板的「测试覆盖度铁律」「测试执行约定」两节与「本地测试环境」表。
- **多工具通用**：`AGENTS.md` / `CLAUDE.md` 各自只放一行指针（"Apifox 操作先读项目根 `PROJECT_TEST.md`；未登记先询问"），不重复写 projectId。
- **覆盖关系**：项目已有其他测试文档（如 `doc/5-tests/` 下文档）时，`PROJECT_TEST.md` 作为顶层入口与绑定事实源，细节文档保持原有归属，不迁移。
