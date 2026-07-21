---
schema_version: 1
doc_id: TEST-SKILL-SPLIT-20260717
doc_type: test
source_ids:
  - SRC-SKILL-SPLIT-20260716
  - REQ-SKILL-SPLIT-20260716
  - AC-SKILL-SPLIT-20260716
status: accepted
version: v1.2
template_version: 1
current_slice: CYCLE-SPLIT-01 closed / CYCLE-SPLIT-02 not entered
updated_at: 2026-07-17 18:33:28
reader_level: business_general
writing_style: plain_chinese
appendix_policy: preserve_existing_or_one_terminal_appendix
review_acceptance_gates:
  - stage: review
    applicability: applicable
    reason: 本测试任务新增通用拆分入口、触发 fixture 和路径边界，需要审查入口契约与失败出口。
    basis: CYCLE-SPLIT-01 的 TASK-SPLIT-01-01 与 TASK-SPLIT-01-02 已完成，TASK-SPLIT-01-03 已进入实现。
    required_by_source: true
    required_now: true
    completed_validation:
      - EVD-TASK-SPLIT-01-02-REVIEW
      - EVD-TASK-SPLIT-01-03-REVIEW
    substitute_validation:
      - TEST-SPLIT-002
    manual_follow_up: N/A
    pass_standard: 五类模式、fixture 路由、路径边界和退出码可复核且无 P0/P1。
  - stage: acceptance
    applicability: applicable
    reason: 当前任务必须验收测试入口本身，但不验收 skill 资产拆分结果。
    basis: 测试脚本、fixture 和 README 已进入本任务允许文件；真实 skill、字典和旧目录仍未修改。
    required_by_source: true
    required_now: true
    completed_validation:
      - EVD-TASK-SPLIT-01-02-ACCEPT
      - EVD-TASK-SPLIT-01-03-ACCEPT
    substitute_validation:
      - TEST-SPLIT-002
    manual_follow_up: 真实 skill 拆分仍须按后续 skill 资产周期的验收标准重新验证。
    pass_standard: 当前任务四项证据齐全；仅测试入口通过不等于 skill 拆分通过。
  - stage: third_party
    applicability: not_applicable
    reason: 只读取本地仓库文件和本地 Python。
    basis: 不连接数据库、缓存、消息队列、HTTP/RPC 或非 local 服务。
    required_by_source: false
    required_now: false
    completed_validation: []
    substitute_validation: []
    manual_follow_up: N/A
    pass_standard: N/A
---

# Skill 体积拆分验证说明

结论：当前已建立可复用的 Skill 拆分测试入口并完成正向、负向和路径边界验证；影响：后续周期可以用同一入口核对 size、mapping、trigger、pre-delete、post-delete 五类契约；范围：84 个正式 skill 的统计报告、27 个扩展种子边界、候选矩阵、触发样本、删除前后 fixture 和入口路径边界；非范围：不删除真实 skill、不刷新字典、不连接业务服务；变化：测试说明从统计/候选冻结扩展为可执行的通用入口；完成标准：五类模式、PowerShell wrapper、越界拒绝、UTF-8、退出码和证据槽位均闭环；术语说明：fixture 是固定在当前测试时间戳目录内的离线样本，不代表真实 skill 已完成迁移；验证状态：通用测试入口的实现、测试、审查和验收均已登记，周期 01 已收口且未进入下一周期；图片资产决策：`N/A + 原因 + 证据`，本测试只验证文本、YAML、JSON、PowerShell 和文档结构，不涉及 UI、截图或位图产物。

## 文档信息

| 字段 | 内容 |
|---|---|
| 测试任务 | `CYCLE-SPLIT-01 / TASK-SPLIT-01-01`、`TASK-SPLIT-01-02`、`TASK-SPLIT-01-03` |
| 当前状态 | 当前通用入口已完成实现、真实正负测试、审查和任务验收；真实 skill 拆分仍未开始 |
| 执行环境 | 本地工作区、Python 标准库、文档 profile 校验器 |
| 真实资产入口 | `../skill-split-validation/` |
| 图片资产决策 | `N/A + 原因 + 证据`：本测试只验证文本、YAML、JSON 和文档结构，不涉及 UI、截图或位图产物 |

## 测试目的

本测试任务服务于 `CYCLE-SPLIT-01` 的三个顺序任务：先统计正式字典主规划中的 84 个 skill，再将统计结果冻结为候选矩阵，最后建立后续周期复用的五类测试入口。根目录实际存在的 27 个扩展种子不纳入正式预算基线，但会作为排除数量单独报告；`2d-asset-design` 按冻结需求作为 P1 扩展种子例外保留。当前入口只读取本地报告、矩阵和 fixture，不执行真实 skill 删除。

## 路径与日期决策

- 当前测试根目录：`doc/5-tests/2026-07-17_155229/`。
- 中文说明目录：本目录，只存放本 `README.md`。
- ASCII 真实测试资产目录：`../skill-split-validation/`。
- 变更依据：`CHG-SPLIT-20260717-002`。原计划目录日期已早于当前运行日，且中文目录不能承载真实脚本，因此不复用旧目录。
- 当前任务切换依据：`CHG-SPLIT-20260717-003`。候选矩阵和四份计划文档仍位于同一时间戳根目录的 ASCII 资产路径与中央文档路径。

## 执行方式

在仓库根目录执行：

```powershell
python -X utf8 "doc/5-tests/2026-07-17_155229/skill-split-validation/skill_size_report.py" --root "D:\luode\luode-skills" --output "doc/5-tests/2026-07-17_155229/skill-split-validation/skill-size-report.json"
python -X utf8 "doc/5-tests/2026-07-17_155229/skill-split-validation/validate_skill_split.py" --mode all --root "D:\luode\luode-skills" --cases "D:\luode\luode-skills\doc\5-tests\2026-07-17_155229\skill-split-validation\cases"
pwsh -NoProfile -File "doc/5-tests/2026-07-17_155229/skill-split-validation/run_trigger_cases.ps1" -Phase all -RepoRoot "D:\luode\luode-skills" -CasesRoot "D:\luode\luode-skills\doc\5-tests\2026-07-17_155229\skill-split-validation\cases"
```

## 依赖与环境

- 只使用本地仓库文件和 Python 标准库。
- 不连接数据库、缓存、消息队列、HTTP/RPC、业务服务或非 local 环境。
- 注册清单来源：仓库根目录 `字典.md` 的主规划域；扩展种子从 `11.扩展种子` 起不纳入统计。

## 覆盖范围与通过标准

- 注册 skill 数为 84。
- 每个条目具备 `skill_md_bytes`、`reference_total_bytes`、`reference_max_bytes`、`default_text_bytes` 和 `budget_level`。
- JSON 可解析，所有统计文件能以 UTF-8 回读，报告长度和哈希可复核。
- 报告同时记录磁盘 skill 目录数和排除的扩展种子数，解释 84 与磁盘实际数量的差异。
- `validate_skill_split.py --mode all` 依次通过 `size`、`mapping`、`trigger`、`pre-delete`、`post-delete` 五类模式。
- `trigger` 样本要求必需命中全部出现在 `observed_hits`，禁止命中不出现在 `observed_hits`；删除阶段只读取 fixture 快照。
- `--root` 解析出的报告和矩阵必须位于仓库根目录内；`--cases` / `-CasesRoot` 必须位于当前测试时间戳目录内。
- 越界路径必须退出码非 0，并输出 `[失败]` 或 wrapper 的 `[FAIL]`；通过负向样本不得修改真实 skill 目录。

## 当前结论

- 状态：`completed`，统计、候选矩阵和通用拆分测试入口均已真实落盘；实现、真实测试、审查、任务验收和周期状态同步均已完成。
- 统计结果：正式注册 skill `84` 个；磁盘 skill 目录 `111` 个；排除扩展种子 `27` 个；预算等级为 `normal=71`、`review=7`、`split_candidate=2`、`hard_warning=4`。
- 报告：`../skill-split-validation/skill-size-report.json`；脚本：`../skill-split-validation/skill_size_report.py`。
- 证据槽位：`EVD-TASK-SPLIT-01-01-IMPL`、`EVD-TASK-SPLIT-01-01-TEST`、`EVD-TASK-SPLIT-01-01-REVIEW`、`EVD-TASK-SPLIT-01-01-ACCEPT`。
- 复核摘要：脚本 SHA-256 为 `F4960F11F858326E5C0DDD4398CA465D88CD81FE43094D4BB2C08610DE669DB9`；报告 SHA-256 为 `76A73A61AD843EDDFD6C62F9846F2C8AD8FBBA588278EA963F507CA3D26DA062`。
- 统计或候选冻结失败时回到对应的 `TASK-SPLIT-01-01` / `TASK-SPLIT-01-02`；当前入口失败时回到 `TASK-SPLIT-01-03`，保留失败输出，不得修改 skill、字典或 Git 历史。

## `TASK-SPLIT-01-03` 通用入口验证

- Python 入口：`../skill-split-validation/validate_skill_split.py`，参数为 `--mode all|size|mapping|trigger|pre-delete|post-delete`、`--root` 和 `--cases`。
- PowerShell wrapper：`../skill-split-validation/run_trigger_cases.ps1`，参数为 `-Phase all|pre-delete|post-delete`、`-RepoRoot`、`-CasesRoot` 和 `-Help`；wrapper 只转发到 Python，不删除真实目录。
- size 断言：报告 schema 为 1，正式 skill 为 84，磁盘目录为 111，扩展种子为 27，每条统计项具备五个预算字段，报告 SHA-256 与 fixture 一致。
- mapping 断言：候选矩阵 SHA-256、84/27 边界、候选顺序、候选入口和 `TEST-SPLIT-003` 关键 token 一致。
- trigger 断言：5 个 fixture 样本的 `required` 全部命中，`forbidden` 不命中，来源标记为 `fixture_observation`。
- pre-delete/post-delete 断言：旧入口分别为 present/absent，新入口均为 present，映射状态为 `frozen`；日志明确“仅验证 fixture，不删除真实目录”。
- 路径负向断言：`--cases "D:\luode\luode-skills\doc\5-tests"` 必须非零并提示 fixture 根目录越界；`resolve_path` 收到仓库根目录外路径必须非零并提示仓库路径越界。

真实负向命令：

```powershell
python -X utf8 "doc/5-tests/2026-07-17_155229/skill-split-validation/validate_skill_split.py" --mode trigger --root "D:\luode\luode-skills" --cases "D:\luode\luode-skills\doc\5-tests"
pwsh -NoProfile -File "doc/5-tests/2026-07-17_155229/skill-split-validation/run_trigger_cases.ps1" -Phase pre-delete -RepoRoot "D:\luode\luode-skills" -CasesRoot "D:\luode\luode-skills\doc\5-tests"
```

预期：Python 退出码为 `1` 且输出 `[失败] fixture 根目录越界`；PowerShell wrapper 退出码为 `1` 且转发 `[FAIL] validator failed`，两者均不产生 skill 删除动作。

## `TASK-SPLIT-01-02` 候选矩阵验证

- 矩阵：`../skill-split-validation/mapping/candidate-matrix.yaml`。
- 当前入口：`TEST-SPLIT-002`，由四个工程文档 profile 和 UTF-8 YAML 结构断言组成；不使用不存在的 `validate_skill_split.py --mode mapping`。
- 结构断言：正式条目 `84`、磁盘目录 `111`、扩展种子 `27`；报告哈希和正式/种子名称集合一致；4 个正式 `enter_split` 条目各有两个独立职责组；候选顺序 `7` 条；所有条目有资源范围、停止条件、复评条件和追踪字段。
- 文档 profile：`requirement`、`acceptance`、`implementation_master`、`implementation_overview`、`implementation_cycle`、`test` 和当前 `review` 文档均返回 `valid=true`、`errors=[]`、`unresolved_decisions.count=0`。
- 结果：`TASK-SPLIT-01-02` 已完成四项闭环；矩阵 SHA-256 为 `8C587F3316F7651979617EBF410823A1A2968E4ED3F79F441D91FF34ED38C673`。validator 状态为 `LIMITED`，仅表示 skill 资产拆分尚未实施，不影响当前计划证据通过。
- 证据槽位：`EVD-TASK-SPLIT-01-02-IMPL`、`EVD-TASK-SPLIT-01-02-TEST`、`EVD-TASK-SPLIT-01-02-REVIEW`、`EVD-TASK-SPLIT-01-02-ACCEPT`。

## 完成标准

- 当前任务必须完成 84/111/27 数量口径、报告哈希、正式/种子名称集合、4 个正式二分候选和 7 个候选顺序断言，并通过五类通用入口模式。
- Python、PowerShell help/all/pre-delete/post-delete、语法编译、UTF-8 回读和路径越界负向断言必须有真实退出码证据。
- 四份工程文档 profile 与周期 01 `implementation_cycle` profile 必须返回 `valid=true`、`errors=[]`、P0/P1 未决数为 0。
- 通过本测试只表示通用测试入口契约完成，不表示任何新 skill 已创建、旧 skill 已删除或字典已刷新。

## 执行附录

- `TEST-SPLIT-002` 使用 `artifact-delivery-gate-rules/scripts/validate_engineering_docs.py` 依次校验五个适用 profile，并使用 UTF-8 Python 读取 YAML/JSON 完成矩阵断言。
- `TEST-SPLIT-003` 使用上述 Python 和 PowerShell 入口完成五类模式、路径边界和 pre/post-delete fixture 断言。
- 清理：删除 `__pycache__`、临时输出和负向命令缓存；保留正式报告、矩阵、fixture、入口脚本和 README。
- 回滚：仅删除本任务新增的 `validate_skill_split.py`、`run_trigger_cases.ps1` 及本任务 README 变更，恢复到 `TASK-SPLIT-01-02` 证据；不删除真实 skill、不刷新字典、不写 Git 历史。

## 追踪附录

- 来源：`SRC-SKILL-SPLIT-20260716` -> `REQ-SKILL-SPLIT-20260716` -> `AC-SKILL-SPLIT-20260716` -> `CYCLE-SPLIT-01`。
- 当前测试：`TEST-SPLIT-001`、`TEST-SPLIT-002`、`TEST-SPLIT-003`。
- 真实产物：`../skill-split-validation/skill-size-report.json`、`../skill-split-validation/mapping/candidate-matrix.yaml`、`../skill-split-validation/validate_skill_split.py`、`../skill-split-validation/run_trigger_cases.ps1`、`../skill-split-validation/cases/*.json`。
- 当前证据槽位：`EVD-TASK-SPLIT-01-03-IMPL`、`EVD-TASK-SPLIT-01-03-TEST`、`EVD-TASK-SPLIT-01-03-REVIEW`、`EVD-TASK-SPLIT-01-03-ACCEPT`。
- 当前仅验证 fixture 契约，不代表真实 skill 已删除；完整 skill 拆分仍需在后续周期重新建立真实资产证据，本轮不进入 CYCLE-SPLIT-02。
