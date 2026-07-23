---
name: requirement-splitting-rules
description: 当需求较大、涉及多个模块、接口、页面、步骤、角色协作，或一次覆盖多个独立子系统、产品子域、相对独立主线，无法作为单一闭环稳定推进时专项自动触发。负责业务切片、依赖关系和当前优先闭环，并将结果回写到 `requirement-intake-rules` 维护、由 `artifact-storage-rules` 定位的同一份需求主文档；文件/符号落点、实施周期、真实测试命令和任务级“实现-测试-审查-验收”由 `implementation-planning-rules` 负责，不代替需求接入、边界裁决或项目排期。
---

# 需求拆分规则

## 职责与触发

- 只在需求目标和主要边界已经成立、但体量或结构无法作为单一闭环推进时使用。
- 多模块、多接口、多页面、多步骤、多角色、跨端联动、多独立子系统或多个产品子域出现时自动触发。
- 负责顶层子系统拆分、垂直业务切片、业务依赖关系、推荐顺序和当前优先闭环。
- 每个需求点只能归属一个主 `SLICE-*`；共享能力单列依赖，依赖关系必须无环并写明阻断条件。

## 职责归位

- `references/splitting-dimensions.md` 唯一定义业务切片字段、依赖 DAG、暂停和移交输入。
- 本 Skill 不冻结代码文件/符号、不创建实施总览或周期、不定义真实测试命令、样本断言、清理和任务级回滚。
- 上述实施字段不得删除：拆分完成后必须移交 `implementation-planning-rules`，由其把当前优先 `SLICE-*` 转成文件/符号、周期、任务和逐任务“实现 -> 真实测试 -> 审查 -> 验收”闭环。
- 前置验收字段和 `AC-*` 由 `acceptance-criteria-rules` 负责；文档路径、图片和最终落盘分别由 `artifact-storage-rules`、`artifact-delivery-gate-rules` 负责。

## 最小执行流程

1. 读取 `../requirement-intake-rules/references/requirement-domain-shared-contract.md`，确认需求已稳定且仍使用唯一主文档。
2. 读取 `references/splitting-dimensions.md`，先判断按独立子系统、业务流程、角色、风险或依赖拆分。
3. 多个独立子系统先做顶层拆分，不在同一轮把所有子系统细节写深。
4. 读取 `references/splitting-sequence.md` 明确业务依赖和当前优先闭环；需要正反例时读取 `references/splitting-examples.md`。
5. 将 `SLICE-*`、范围、业务输入输出、依赖、阻断条件和推荐顺序回写同一份需求主文档。
6. 只把第一闭环或当前优先切片回流 intake/边界/变更继续收敛；稳定后先交 `acceptance-criteria-rules`，再交 `implementation-planning-rules`。

## 暂停、通过与驳回

- 暂停：目标或边界仍不稳定；切片仍互相纠缠；多个方案风险差异显著且未裁决；多个互不相关需求仍被打包。
- 暂停期间保持 `blocked`，P0/P1 未决不得包装成可执行切片；用户明确停止时立即停止扩散。
- 通过：形成清晰的业务切片、唯一归属、无环依赖、当前优先闭环和下游移交输入，并已回写同一主文档。
- 驳回：机械按技术层切块、把小需求过度拆碎、多个独立子系统未先顶层拆分、拆分阶段直接定义实施文件/命令，或创建平行拆分文档。
- 切片变化必须保留来源、差异、受影响验收/计划和回滚条件；恢复时从已落盘的 `SLICE-*` 状态继续。

## References

- 共享路由与保护语义：`../requirement-intake-rules/references/requirement-domain-shared-contract.md`
- 业务切片、依赖 DAG 与 `SLICE-*`：`references/splitting-dimensions.md`
- 业务顺序与当前优先闭环：`references/splitting-sequence.md`
- 正反例：`references/splitting-examples.md`
- 实施总览、周期、文件/符号与真实测试：`../implementation-planning-rules/SKILL.md`
- 前置验收：`../acceptance-criteria-rules/SKILL.md`
- 文档路径和落盘门禁：`../artifact-storage-rules/references/path-map.yaml`、`../artifact-delivery-gate-rules/references/plain-language-document-contract.md`
