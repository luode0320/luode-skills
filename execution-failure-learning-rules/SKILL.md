---
name: execution-failure-learning-rules
description: 当 Agent 执行 CLI、API、MCP、浏览器、安装器、生成器、测试入口或其他工具时出现非预期失败、错误产物、退出码为 0 但结果不可信、重复试错或已确认可复用的恢复方案时自动触发。负责执行前预防、失败后分类与快速恢复、同输入复验、脱敏去重、candidate 案例回写和 active 授权晋级；不代替业务 Bug、代码错误处理或 skill 缺口诊断。
---

# Execution Failure Learning Rules

将一次执行失败变成可复用的预防与恢复知识。此 skill 是跨领域路由器；案例正文始终归属于唯一领域 skill，不在这里建立全局错误大杂烩。动态案例的唯一持久化位置是固定 Obsidian vault，静态 owner casebook 只作为种子、模板和回归基线。

## 三种模式

根据当前执行阶段选择一种模式，不要把未验证的猜测写成解决方案：

- `prevent`：调用高风险外部工具、CLI、浏览器、安装器、生成器或验证器前，读取路由表并匹配 `active` 案例。精确命中时先应用已验证的预防步骤；只有模糊相似时不得强套案例。
- `recover`：非预期退出、异常响应、错误产物或退出码为 0 但结果不可信时，先分类并读取已有案例，再按原输入和原成功标准验证恢复。禁止无变化重复试错。
- `learn`：根因已确认、方案已应用且同输入复验通过时，按案例模板脱敏、去重并经 Obsidian bridge 自动写入唯一 owner 的 `candidate`。`active` 晋级必须满足授权和全部门禁。

## 执行流程

1. **识别触发**：记录工具/阶段、输入摘要、环境来源和可观察结果；只保留最小必要证据。
2. **分类与路由**：阅读 [classification-and-routing.md](references/classification-and-routing.md)，确定失败类别和唯一 owner skill。无法唯一归属时转交 `skill-evolution-rules`，不要创建临时重复案例库。
3. **预防或恢复**：`prevent` 只执行 `active` 案例允许的动作；`recover` 先查匹配案例，再定位根因，最多对同一输入做一次无变化复验，之后必须改变假设或停止。
4. **验证**：使用原输入、同一成功标准和 local 环境验证修复。只通过静态阅读、偶然成功或不同输入的结果不足以晋级。
5. **学习回写**：阅读 [lifecycle-and-gates.md](references/lifecycle-and-gates.md) 与 [case-template.md](references/case-template.md)。满足复现、根因、验证、脱敏、唯一 owner 和去重门禁后，先按 Obsidian bridge 规则执行 `doctor`、`search`/`search-context` 和 `read`，再在固定 vault 的 owner 路径创建或追加 `candidate`；冲突案例追加 `conflicted` 状态事件，不得覆盖旧案例。`create`/`append` 必须返回 `verified=true`，否则案例仍视为未持久化。
6. **报告**：最终说明失败类别、根因、采取的恢复动作、验证证据、案例 ID/状态和是否需要 `skill-evolution-rules`；若产生工作树变更必须明确列出。恢复预算耗尽、同一输入的无变化复验已用尽或安全边界拒绝继续时，生成共享 `BLK-*` 事实并交给 `reasoning-summary-structure-rules`，不得只写泛化后续建议。

## 强制边界

- 证据、复现和验证只能使用 `local` 配置；不得连接或写入 test、staging、pre、release、prod/production 环境。local 配置指配置归属，不以地址是否为 localhost 判断。
- API key、token、密码、私钥、完整鉴权响应、用户私有输入、原始图片和未经脱敏的本机路径不得进入案例。
- 业务或产品 Bug 交给 `bug-*`；代码异常处理设计交给 `error-handling-rules`；需求/规则缺口交给 `skill-evolution-rules`；跨项目稳定知识才交给 `obsidian-knowledge-flow`。不要把这些问题伪装成执行案例。
- 预期负向测试、用户取消、明确权限阻断、一次性网络抖动和未经复验的猜测不晋级；可记录为当轮诊断，但不得写成可执行案例。
- `candidate` 只表示待审经验，不得在没有当前轮 skill 维护授权时晋级 `active`。active 失效时标记 `superseded`/`stale`，保留替代关系和验证证据。
- 动态 `candidate`、`active`、`conflicted`、`stale`、`superseded` 和 `rejected` 状态只写入 Obsidian 案例笔记；状态变更采用追加式状态事件并保留旧证据，不回写静态 casebook。
- 固定 Obsidian 入口为 `D:\obsidian_data\知识库\20-Knowledge\execution-failure-cases\<owner>\<case-id>.md`，导航 MOC 为 `知识库/30-MOCs/执行失败案例.md`。vault 内检索、创建、追加和读回只能经 `obsidian-knowledge-flow/scripts/obsidian_cli_bridge.py` 的公开 allowlist 完成；不得使用 `rg`、`Get-Content`、`Set-Content` 或其它文件系统操作冒充持久化成功。
- 静态 owner casebook（各领域 skill 的 `references/*casebook*.md`）只读：用于初始种子、离线 schema/回归基线和迁移来源。执行期间不得把新 candidate/active 追加到静态文件，也不得把静态文件当作动态状态的唯一事实来源。
- bridge doctor、检索、写入或 readback 失败时，停止 Obsidian 写入并报告 `candidate persistence: blocked`；不得改用静态 casebook fallback、无变化重试或声称案例已写入。该 bridge 故障按 `obsidian-knowledge-flow` owner 继续走 `recover`，当前案例保留结构化脱敏交接。
- 真实阻断必须遵守 `../artifact-delivery-gate-rules/references/task-blocker-closure-contract.md`：记录失败阶段、脱敏证据、已尝试动作、停止边界、影响、最多三步恢复计划和原成功标准的重入入口。`limited`、用户取消和预期负向测试不得生成 `BLK-*`。

## 参考文件

- [classification-and-routing.md](references/classification-and-routing.md)：失败分类、高风险预检与唯一 owner 路由。
- [lifecycle-and-gates.md](references/lifecycle-and-gates.md)：状态机、复验、授权、脱敏、冲突与边界门禁。
- [case-template.md](references/case-template.md)：案例字段、去重键和 candidate 记录模板。
