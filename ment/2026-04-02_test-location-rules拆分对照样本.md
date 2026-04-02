# `test-location-rules` 拆分对照样本

更新时间：`2026-04-03 00:35`

## 1. 样本目标

- 目标旧 skill：`test-location-rules`
- 样本模式：`deleting`
- 处理原则：
  - 旧 skill 仅短暂保留为冻结基线，用于和新 skill 集合做功能对照。
  - 对照完成后，所有现行入口都必须迁移到新 skill 集合，再删除旧 skill。
  - 历史对照证据可以保留，但不再让旧 skill 继续承接任何现行业务入口。

## 2. 为什么选择它做首拆样本

- 原 `description` 同时覆盖测试目录、测试文件、测试脚本、验证程序、fixture、mock 数据、测试说明文档等多个触发对象。
- 正文同时承载根目录布局、散落资产治理、Go 编译路径冲突与白盒 seam 处理三类职责。
- `skills拆分.md` 的分类二分示例本来就长期使用它举例，最适合作为第一份实战样本。

## 3. 分类二分路径

第一次二分：

1. `test-task-root-layout-rules`
   - 负责“新测试任务该怎么建根目录和布局”
2. 保留待继续拆分的治理组
   - 包含散落资产治理 + Go 编译路径冲突

第二次二分：

1. `test-scattered-asset-location-rules`
   - 负责“测试资产散落到错误目录时如何识别和迁移”
2. `go-test-compile-path-rules`
   - 负责“Go 可编译路径、源码目录 `_test.go` 与白盒 seam”

## 4. 新 skill 清单

| 新 skill | 当前状态 | 说明 |
|---|---|---|
| `test-task-root-layout-rules` | 已创建 | 负责 `test/` 根目录、当天时间戳目录、中文 README 目录和 ASCII 镜像布局 |
| `test-scattered-asset-location-rules` | 已创建 | 负责识别并迁移散落在 `test/` 根目录之外的测试资产 |
| `go-test-compile-path-rules` | 已创建 | 负责 Go 源码目录禁放 `*_test.go`、ASCII 可编译路径和白盒 seam 方案 |
| `test-location-rules` | 已删除 | 对照验证完成后，现行入口已迁移，旧目录已移除 |

## 5. 覆盖映射表

| 原规则ID | 原规则摘要 | 新 skill 名称 | 新规则落点 | 迁移动作 | 状态 | 主落点 | 等价性说明 |
|---|---|---|---|---|---|---|---|
| R-001 | 只在“测试资产应该放到哪里”问题上使用；命名/程序/文档边界要分流 | `test-task-root-layout-rules`、`test-scattered-asset-location-rules`、`go-test-compile-path-rules` | 各自 `SKILL.md / 权责边界与不负责事项` | 等价改写 | 已覆盖 | `test-task-root-layout-rules` | 旧边界按新职责拆到三个 skill 中分别承接 |
| R-002 | 严禁为了测试目的改动生产代码语义 | `test-scattered-asset-location-rules` | `SKILL.md / 强制规则` | 原样迁移 | 已覆盖 | `test-scattered-asset-location-rules` | 无 |
| R-003 | 测试脚本、数据、桩、夹具、样例与辅助逻辑必须放在中央测试资产目录，不得进生产目录 | `test-scattered-asset-location-rules` | `SKILL.md / Skill 作用与适用场景`、`references/scattered-asset-migration.md / 2` | 等价改写 | 已覆盖 | `test-scattered-asset-location-rules` | 拆成识别场景与禁止位置两部分表达，约束强度不变 |
| R-004 | 发现污染生产代码行为立即阻断并先回退 | `test-scattered-asset-location-rules` | `SKILL.md / 强制规则` | 等价改写 | 已覆盖 | `test-scattered-asset-location-rules` | 通过“严禁 + 迁移前先判断职责”承接阻断逻辑 |
| R-005 | 所有测试资产必须统一在中央测试根目录下 | `test-task-root-layout-rules`、`test-scattered-asset-location-rules` | `references/task-root-layout.md / 1`、`references/scattered-asset-migration.md / 1` | 组合覆盖 | 已覆盖 | `test-task-root-layout-rules` | 根目录约定由布局 skill 承接，违规识别由禁散落 skill 承接 |
| R-006 | 任何测试相关文件只要不在中央测试根目录下就立即迁移 | `test-scattered-asset-location-rules` | `SKILL.md / 强制规则`、`references/scattered-asset-migration.md / 1` | 原样迁移 | 已覆盖 | `test-scattered-asset-location-rules` | 无 |
| R-007 | Go 源码目录绝对不允许出现 `*_test.go` | `go-test-compile-path-rules` | `SKILL.md / 强制规则`、`references/go-compile-path.md / 1` | 原样迁移 | 已覆盖 | `go-test-compile-path-rules` | 无 |
| R-008 | 白盒同包诉求不是特例，统一改 seam 再落到中央测试根目录 ASCII 镜像路径 | `go-test-compile-path-rules` | `SKILL.md / 强制规则`、`references/go-compile-path.md / 3` | 原样迁移 | 已覆盖 | `go-test-compile-path-rules` | 无 |
| R-009 | 新测试任务统一采用“时间戳根目录 + 中文说明目录 + 真实代码路径镜像”结构 | `test-task-root-layout-rules` | `SKILL.md / Skill 作用与适用场景`、`references/task-root-layout.md / 2-4` | 等价改写 | 已覆盖 | `test-task-root-layout-rules` | 拆成结构职责与详细布局规则表达，语义不变 |
| R-010 | 时间戳根目录只允许时间戳，不再把中文拼进根目录名 | `test-task-root-layout-rules` | `references/task-root-layout.md / 2` | 原样迁移 | 已覆盖 | `test-task-root-layout-rules` | 无 |
| R-011 | 中文说明目录默认只存放 `README.md` | `test-task-root-layout-rules`、`test-scattered-asset-location-rules` | `references/task-root-layout.md / 3`、`references/scattered-asset-migration.md / 2` | 组合覆盖 | 已覆盖 | `test-task-root-layout-rules` | 布局约束由根布局 skill 承接，误放真实资产的治理由禁散落 skill 承接 |
| R-012 | 真实测试资产都放在同一时间戳根目录下的 ASCII 镜像路径中 | `test-task-root-layout-rules` | `SKILL.md / 强制规则`、`references/task-root-layout.md / 4` | 原样迁移 | 已覆盖 | `test-task-root-layout-rules` | 无 |
| R-013 | 中文不能进入 Go 可编译路径 | `go-test-compile-path-rules` | `references/go-compile-path.md / 2` | 原样迁移 | 已覆盖 | `go-test-compile-path-rules` | 无 |
| R-014 | 默认新测试任务必须创建当天时间戳目录 | `test-task-root-layout-rules` | `SKILL.md / 强制规则`、`references/task-root-layout.md / 2` | 原样迁移 | 已覆盖 | `test-task-root-layout-rules` | 无 |
| R-015 | 目标目录日期早于当天时必须中止并询问是否复用旧目录 | `test-task-root-layout-rules` | `SKILL.md / 强制规则`、`references/task-root-layout.md / 2` | 原样迁移 | 已覆盖 | `test-task-root-layout-rules` | 无 |
| R-016 | 未获明确许可前禁止向旧时间戳目录写新文件 | `test-task-root-layout-rules` | `SKILL.md / 强制规则`、`references/task-root-layout.md / 2` | 原样迁移 | 已覆盖 | `test-task-root-layout-rules` | 无 |
| R-017 | 允许读取历史目录参考，但新增与修改应落在当前时间戳目录 | `test-task-root-layout-rules` | `references/task-root-layout.md / 2` | 原样迁移 | 已覆盖 | `test-task-root-layout-rules` | 无 |
| R-018 | 最终交付前必须校验新增测试文件都位于当前任务时间戳目录 | `test-task-root-layout-rules` | `SKILL.md / 通过 / 驳回标准` | 等价改写 | 已覆盖 | `test-task-root-layout-rules` | 通过标准中保留了“未误写历史目录”的最终校验语义 |
| R-019 | 新增或修改测试目录、文件、脚本、验证程序、fixture、mock、说明文档落点时自动触发 | `test-task-root-layout-rules`、`test-scattered-asset-location-rules`、`go-test-compile-path-rules` | 各自 `description` 与 `自动触发信号` | 组合覆盖 | 已覆盖 | `test-task-root-layout-rules` | 旧 description 按新职责拆成三个独立 trigger 集合 |
| R-020 | 进入后先区分测试代码、数据、脚本、文档还是公共测试辅助资源 | `test-scattered-asset-location-rules` | `references/scattered-asset-migration.md / 1` | 等价改写 | 已覆盖 | `test-scattered-asset-location-rules` | 用“默认判定”承接资产类别识别 |
| R-021 | 为当前测试任务创建独立时间戳根目录并校验当天日期 | `test-task-root-layout-rules` | `SKILL.md / 默认执行流程`、`references/task-root-layout.md / 2` | 原样迁移 | 已覆盖 | `test-task-root-layout-rules` | 无 |
| R-022 | 如用户明确复用旧目录，需记录复用原因和旧任务 ID | `test-task-root-layout-rules` | `references/task-root-layout.md / 2` | 原样迁移 | 已覆盖 | `test-task-root-layout-rules` | 无 |
| R-023 | 同一需求需要多个测试程序或多轮独立验证时，分别创建多个时间戳根目录 | `test-task-root-layout-rules` | `SKILL.md / 强制规则`、`references/task-root-layout.md / 5` | 原样迁移 | 已覆盖 | `test-task-root-layout-rules` | 无 |
| R-024 | Go 场景额外检查源码目录 `*_test.go`；若有则改 seam 方案 | `go-test-compile-path-rules` | `SKILL.md / 默认执行流程`、`references/go-compile-path.md / 1,3` | 原样迁移 | 已覆盖 | `go-test-compile-path-rules` | 无 |
| R-025 | 默认先读 artifact-storage 的路径和命名约定 | `test-task-root-layout-rules`、`test-scattered-asset-location-rules`、`go-test-compile-path-rules` | 各自 `SKILL.md / 默认执行流程` 或 `references 读取规则` | 原样迁移 | 已覆盖 | `test-task-root-layout-rules` | 新 skill 均保留了对 artifact-storage 的依赖读取规则 |
| R-026 | 根目录只能是 `test/`，不能是 `tests/`、`qa/`、`verify/` 等 | `test-task-root-layout-rules` | `SKILL.md / 强制规则`、`references/task-root-layout.md / 1` | 原样迁移 | 已覆盖 | `test-task-root-layout-rules` | 无 |
| R-027 | 无法映射到单一源码文件时，至少按最接近的源码模块路径镜像且保持 ASCII | `test-task-root-layout-rules` | `SKILL.md / 强制规则`、`references/task-root-layout.md / 4` | 原样迁移 | 已覆盖 | `test-task-root-layout-rules` | 无 |
| R-028 | 旧时间戳根目录按周或按月归档到 `test/archive/` | `test-task-root-layout-rules` | `references/task-root-layout.md / 5` | 原样迁移 | 已覆盖 | `test-task-root-layout-rules` | 无 |
| R-029 | 仓库根目录、业务目录、文档目录、脚本目录、中文说明目录中都禁止混放测试资产 | `test-scattered-asset-location-rules` | `references/scattered-asset-migration.md / 2` | 原样迁移 | 已覆盖 | `test-scattered-asset-location-rules` | 无 |
| R-030 | 任何与测试相关的文件，只要不在 `test/` 下，就是违规 | `test-scattered-asset-location-rules` | `SKILL.md / 强制规则`、`references/scattered-asset-migration.md / 1` | 原样迁移 | 已覆盖 | `test-scattered-asset-location-rules` | 无 |
| R-031 | 迁移散落资产时只移动与当前任务直接相关的内容，避免借机大扫除 | `test-scattered-asset-location-rules` | `SKILL.md / 强制规则`、`references/scattered-asset-migration.md / 3` | 原样迁移 | 已覆盖 | `test-scattered-asset-location-rules` | 无 |
| R-032 | 如果某文件兼具生产和测试双重职责，先拆职责再归位 | `test-scattered-asset-location-rules` | `SKILL.md / 强制规则`、`references/scattered-asset-migration.md / 3` | 原样迁移 | 已覆盖 | `test-scattered-asset-location-rules` | 无 |
| R-033 | 任何 `*_test.go` 只要不在 `test/` 根目录下就应迁移并改 seam | `go-test-compile-path-rules`、`test-scattered-asset-location-rules` | `references/go-compile-path.md / 1,3`、`references/scattered-asset-migration.md / 4` | 组合覆盖 | 已覆盖 | `go-test-compile-path-rules` | Go 编译路径整改由 Go skill 主承接，散落识别由禁散落 skill 辅助承接 |
| R-034 | 同一需求的多个独立测试不能混在一个时间戳目录 | `test-task-root-layout-rules` | `SKILL.md / 强制规则`、`references/task-root-layout.md / 5` | 原样迁移 | 已覆盖 | `test-task-root-layout-rules` | 无 |
| R-035 | 每个时间戳根目录都必须包含中文说明目录和 `README.md`，否则结构不完整 | `test-task-root-layout-rules` | `SKILL.md / 通过 / 驳回标准`、`references/task-root-layout.md / 3,6` | 原样迁移 | 已覆盖 | `test-task-root-layout-rules` | 无 |

## 6. references 承接关系

| 原 references 文件 | 承接去向 | 说明 |
|---|---|---|
| `test-location-rules/references/test-root-and-task-folders.md` | `test-task-root-layout-rules/references/task-root-layout.md` | 根目录、时间戳目录、中文说明目录、ASCII 镜像和归档规则转入根布局 skill |
| `test-location-rules/references/forbidden-scattered-assets.md` | `test-scattered-asset-location-rules/references/scattered-asset-migration.md` | 散落资产识别、禁止位置和迁移原则转入禁散落 skill |
| `test-location-rules/references/location-examples.md` | 新 skill 的 `SKILL.md` 与各自 references | 样例中的根布局、散落反例和 Go 反例已按职责拆散进三个新 skill |

## 7. 当前对照结论

- 旧 `test-location-rules` 的冻结对照阶段已经完成，状态从 `comparing` 推进到 `deleted`。
- 新 skill 集合已经完成静态对照、边界验证、动态样例验证和 GitHub 真实项目演练，当前未发现必须回退的承接空洞。
- 保留 `test/2026-04-02_231122/...` 下的历史证据作为审计材料，但这些文档不再作为现行入口说明。

## 8. 删除完成结论

旧 `test-location-rules` 已按以下收口条件完成删除：

- 上表中的规则项继续保持 100% 已覆盖。
- 现行文档、字典索引与技能入口已经全部迁移到 `test-task-root-layout-rules`、`test-scattered-asset-location-rules` 与 `go-test-compile-path-rules`。
- 历史证据仅保留在 `ment/` 与 `test/2026-04-02_231122/` 这类审计材料中，不再作为运行中的依赖入口。
- `test-location-rules/` 目录及其 `references/`、`agents/`、`SKILL.md` 已从仓库中移除。
