# `test-location-rules` 拆分对照验证

## 测试目的

验证旧 `test-location-rules` 保留为冻结基线时，新拆分的 skill 集合是否能够在首轮对照中完整承接原有规则，不出现明显丢失、弱化或边界漂移。

## 测试对象

- 旧 skill：
  - `test-location-rules`
- 新 skill 集合：
  - `test-task-root-layout-rules`
  - `test-scattered-asset-location-rules`
  - `go-test-compile-path-rules`

## 真实测试资产入口

- 详细案例与逐条对照：`test/2026-04-02_231122/skills/test-location-rules/comparison-cases.md`
- 第二轮边界与联动验证：`test/2026-04-02_231122/skills/test-location-rules/routing-edge-cases.md`
- 第三轮动态样例验证：`test/2026-04-02_231122/skills/test-location-rules/dynamic-execution-cases.md`
- 第四轮 GitHub 真实项目演练：`test/2026-04-02_231122/skills/test-location-rules/github-vt2geojson-real-drill.md`

## 执行前置条件

- 旧 `test-location-rules` 保持冻结，不继续新增规则。
- 三个新拆分 skill 已写入 `SKILL.md`、`agents/openai.yaml` 和 `references/`。
- 四个相关 skill 已通过 `python -X utf8 .system\skill-creator\scripts\quick_validate.py ...` 校验。

## 执行方式

- 本轮采用“静态场景对照验证”，不是运行外部自动触发引擎。
- 做法是为旧 skill 选取 4 个高代表性场景，分别比对：
  - 旧 skill 能否给出明确结论
  - 新 skill 集合是否能命中正确 skill，并得出等价结论
  - 是否存在规则空洞、边界重叠或承接歧义

## 依赖数据与环境

- 仓库路径：`C:\Users\Administrator\.codex\skills`
- 执行时间：`2026-04-02 23:11:22`
- 执行环境：Windows PowerShell，本地静态文档验证

## 覆盖范围

- 新测试任务根目录与布局规则
- 历史时间戳目录复用阻断
- 散落测试资产迁移规则
- Go 源码目录 `*_test.go` 禁放、ASCII 编译路径与白盒 seam 规则
- 非触发场景、跨 skill 联动顺序和 `test/` 根目录内的 Go 特例路径
- 动态落点样例的真实目录结构与资产归位路径
- GitHub 真实小项目中的遗留散落测试资产完整迁移演练

## 验证步骤摘要

1. 选取 4 个覆盖主职责与边界联动的代表性场景。
2. 用旧 `test-location-rules` 提取原结论。
3. 用新 skill 集合判断应该命中的 skill 和应得到的结论。
4. 比较两边是否一致，并记录差异、风险和残留未验证项。
5. 再执行第二轮“边界与联动验证”，确认新 skill 集合不会误触发、不会漏掉联动顺序，也不会在 `test/` 根目录内部漏掉 Go 路径问题。
6. 执行第三轮“动态样例验证”，实际创建一组正确目标路径，检查这些落点是否会与目录规则互相冲突。
7. 执行第四轮“GitHub 真实项目演练”，在外部小项目中实际迁移根目录散落测试资产并跑 `npm test` 对照基线副本。

## 实际结果

- 4 个场景均能从新 skill 集合中找到明确承接路径。
- 当前未发现“旧 skill 能处理，但新 skill 集合无法判断”的明显空洞。
- 当前未发现约束强度明显弱化的场景。
- 第二轮补充验证的 4 个边界场景也全部通过，对“非触发”“多 skill 联动”和“`test/` 根目录内 Go 特例”都未发现承接空洞。
- 第三轮动态样例验证已成功创建正确目标路径，未发现“规则之间互相打架导致真实落点不自洽”的结构冲突。
- 第四轮外部 GitHub 项目演练中，迁移后的 `npm test` 的 TAP 断言 `150/150` 全通过，且基线副本同样出现 `EXIT_CODE=1`，说明退出码问题不是本轮迁移回归。
- 需要补充说明的一点是：本轮已经从静态推演扩展到真实项目迁移演练，但仍未运行系统级自动触发链路测试。

## 未通过项 / 风险项

- 未执行真正的自动触发引擎级验证，因此“命中优先级”仍存在系统级残余风险。
- 已完成真实项目级迁移演练，但仍未执行自动触发实现层的优先级策略验证。
- 当前动态验证使用的是受控样例资产，不代表已经覆盖历史复杂遗留目录的全量迁移风险。
- 当前真实项目演练只覆盖了 Node 小项目，尚未补第二个外部 Go 项目样本。

## 详细证据路径

- `test/2026-04-02_231122/skills/test-location-rules/comparison-cases.md`
- `test/2026-04-02_231122/skills/test-location-rules/routing-edge-cases.md`
- `test/2026-04-02_231122/skills/test-location-rules/dynamic-execution-cases.md`
- `test/2026-04-02_231122/skills/test-location-rules/github-vt2geojson-real-drill.md`

## 结论

通过

## 下一步流转建议

1. 现在已经具备把旧 `test-location-rules` 从 `comparing` 推进到删除评估的证据基础。
2. 如果你还想再压一轮风险，可以再补一个 Go 外部小项目演练，专门覆盖真实 `_test.go` 与中文编译路径场景。
