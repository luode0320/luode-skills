---
name: architecture-doc-rules
description: 当需要创建、更新、审查或解释 `doc/1-架构/` 下的长期架构文档时自动触发，适用于项目架构、目录树、目录职责、主要业务/功能设计架构、模块关系、关键链路、运行时设计和架构专题说明；负责区分专题架构文档与根目录 `项目设计.md` 的分层关系，并确保路径、命名和复用策略服从 `artifact-storage-rules`。不要用它代替 project-design-doc-rules 的根目录项目总览同步、implementation-planning-rules 的当前需求实施计划、package-structure-rules 的生产代码目录归位或 codegraph-analysis-rules 的源码图谱探索。
---

# 架构文档规则

只在“长期架构文档应该如何沉淀到 `doc/1-架构/`”这个问题上使用本 skill。
如果当前只是同步根目录项目总览，转交 `project-design-doc-rules`；如果只是当前需求实施方案，转交 `implementation-planning-rules`。

## Skill 作用与适用场景

- 维护 `doc/1-架构/` 下的长期架构专题文档。
- 规范项目架构、目录树、目录职责、模块关系、主要业务或功能设计架构的写法。
- 明确 `doc/1-架构/` 与根目录 `项目设计.md` 的分层关系。
- 防止把当前一次需求的实施计划、测试结论或审查结论混入长期架构文档。
- 当架构专题发生变化时，判断是否需要同步提醒更新根目录 `项目设计.md`。
- 需要具体路径、命名和扫描范围时，统一读取 `artifact-storage-rules/references/path-map.yaml`，不在本 skill 另立路径真相源。

## 自动触发信号

- 用户要求整理项目架构、系统架构、模块架构、功能架构、目录树或目录职责。
- 用户要求新增或更新 `doc/1-架构/` 下的长期设计文档。
- 当前讨论的是跨需求、跨模块长期有效的业务设计或功能设计，而不是单次需求实施计划。
- 发现根目录 `项目设计.md` 过长，需要把专题细节拆到 `doc/1-架构/`。
- 架构专题文档仍引用旧目录、旧模块边界或旧路径，需要跟随当前仓库规则迁移。

## 进入后先做什么

1. 先确认当前内容是否属于长期架构专题，而不是需求、实施、Bug、测试或审查记录。
2. 默认先读 `../artifact-storage-rules/references/path-map.yaml` 和 `../artifact-storage-rules/references/root-directories.md`，确认当前架构文档根目录。
3. 再读 `references/layering-with-project-design.md`，确认与根目录 `项目设计.md` 的分层边界。
4. 如果需要新建或重写架构专题文档，再读 `references/architecture-doc-template.md`。
5. 如果需要判断旧架构文档是否继续复用，再读 `references/update-policy.md`。

## 默认执行流程

1. 识别架构文档主题：项目级、目录职责、模块关系、业务功能设计、运行时链路或专题约束。
2. 确认当前事实来源：真实代码、当前有效文档、最近变更、现有架构文档。
3. 若事实来源不足，先补充读取或回流 `codegraph-analysis-rules` / `project-design-doc-rules`，不要凭空写架构结论。
4. 按主题更新同一份架构文档；同一专题不新建多个平行入口。
5. 架构文档只记录长期设计事实、边界和约束；当前实施步骤、测试证据和审查结论分别回到对应目录。
6. 若专题变化会影响根目录项目总览，提醒或联动 `project-design-doc-rules` 同步 `项目设计.md`。

## 权责边界与不负责事项

- 不负责根目录 `项目设计.md` 的主入口同步，那属于 `project-design-doc-rules`。
- 不负责决定研发产物根目录和命名模板，那属于 `artifact-storage-rules`。
- 不负责当前需求的实施总览或实施周期，那属于 `implementation-planning-rules`。
- 不负责生产代码包结构归位和依赖方向审查，那属于 `package-structure-rules` 或 `implementation-review-rules`。
- 不负责源码调用链事实发现；需要图谱分析时先使用 `codegraph-analysis-rules`。

## 需要暂停并确认的条件

- 架构事实来源不足，只能基于猜测生成文档。
- 同一专题已有多份冲突架构文档，无法判断当前主入口。
- 当前内容明显只是一次需求实施计划，却被要求写入长期架构目录。
- 目录路径本身发生争议或迁移未完成，需要先由 `artifact-storage-rules` 收口。

## 执行通过 / 驳回标准

- 通过：架构专题文档位于 `doc/1-架构/`，主题清晰，事实来源明确，说明了目录树、目录职责、模块关系或业务功能设计中的长期约束，并且没有混入当前一次实施、测试或审查记录。
- 驳回：架构文档只是空泛愿景、路径口径仍引用旧目录，或把根目录项目总览、当前需求实施计划和长期专题架构混成一份文档。

## 执行结果归档要求

- 长期架构专题统一归档到 `doc/1-架构/`。
- 同一专题优先更新原文档，不新建同义平行文档。
- 文档至少包含：文档用途、事实来源、适用范围、目录/模块结构、职责边界、主要链路或功能设计、与 `项目设计.md` 的关系、待同步项。
- 如果本轮只做判断不更新文档，最终结论必须说明不更新原因和后续触发条件。

## references 读取规则

- 默认先读 `references/layering-with-project-design.md`。
- 只有在新建或重写架构专题文档时，再读 `references/architecture-doc-template.md`。
- 只有在判断旧文档是否复用或拆分时，再读 `references/update-policy.md`。
