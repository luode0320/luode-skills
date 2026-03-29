---
name: bug-assertion-diagnostic-rules
description: 当怀疑状态异常、顺序错误、数据污染、不变量被破坏，且需要通过程序断言、诊断性检查、快速失败或区间收缩来暴露问题位置时触发。负责断言进入条件、放置位置、Bug 根目录记录和删除收口要求；不要把诊断断言长期留作正式业务逻辑。
---

# Bug 断言诊断规则

只在已有明确怀疑点，需要用断言或诊断检查快速缩小 Bug 区间时使用这个 skill。
如果当前还不清楚要验证什么，请先转 `bug-runtime-debug-rules`；如果要设计正式参数校验，请转交相邻业务校验或错误处理规则。

## Skill 作用与适用场景

- 用快速失败和不变量检查尽快暴露异常区间。
- 约束断言适合放在哪里、检查什么、持续多久。
- 将断言方案、失败结果和清理状态统一收口到同一个 Bug 根目录。
- 帮助区分状态污染、顺序错误、分支误走和数据不一致。
- 防止把诊断断言混成正式业务规则。

## 自动触发信号

- 怀疑某个状态在运行途中被意外改写或污染。
- 怀疑调用顺序、生命周期或并发顺序错乱。
- 需要快速确认某个不变量是不是被破坏。
- 普通日志不足以收缩问题发生区间。
- 需要将本轮断言记录与同一 Bug 的日志记录统一保存在一个 Bug 根目录下。

## 进入后先做什么

1. 先定义要验证的状态、不变量或顺序假设。
2. 为当前 Bug 确认统一的根目录，具体路径、目录名和入口文件统一遵循 `artifact-storage-rules`。
3. 选择最能缩小区间的断言位置，而不是到处都加。
4. 明确断言失败后需要记录什么上下文。
5. 提前决定断言在问题定位或修改完成后如何删除，并同步记录删除结论。

## 默认执行流程

1. 默认先读 `references/assertion-entry-conditions.md`，先判断当前是否适合用断言诊断。
2. 再读 `../artifact-storage-rules/references/path-map.yaml` 与 `../artifact-storage-rules/references/update-policy.md`，确认 Bug 根目录、入口 `README.md` 和同一 Bug 持续复用同一根目录的策略。
3. 如需继续展开，再读 `references/assertion-placement.md`，需要决定断言放置位置和粒度。
4. 需要对照边界或正反例时，再读 `references/assertion-examples.md`，需要对照断言诊断样例。
5. 输出断言诊断方案、放置位置、Bug 根目录记录方案和失败后的处理口径，并更新到当前 Bug 根目录下的 `README.md`。
6. 断言结果应回流 `bug-runtime-debug-rules` 或 `bug-root-cause-rules` 固化定位结论；诊断代码进入测试和交付前必须经过 `cleanup-format-review-rules` 检查。

## 权责边界与不负责事项

- 只负责诊断性断言，不代替正式输入校验和业务校验。
- 不在高风险路径随意加入会改变业务行为的重断言。
- 不把所有怀疑点都写成断言，必须有明确假设。
- 诊断断言属于调试改动，问题定位或修改完成后必须删除。
- 如果后续确实需要正式保护逻辑，必须删除当前诊断断言，再按正式校验逻辑重新设计，不能直接保留当前断言。
- 不默认长期保留诊断断言。

## 需要暂停并确认的条件

- 断言目标不清，无法说明要验证什么不变量。
- 断言会显著改变业务流程或引发不可接受的副作用。
- 断言失败后缺少上下文，无法支撑定位。
- 团队打算把诊断断言直接作为正式规则上线，但没有重新审查。
- 当前 Bug 还没有建立统一的 Bug 根目录，导致断言记录和日志记录可能再次分散。

## 执行通过 / 驳回标准

- 通过：能够说明断言验证什么、为什么放在这里、失败后会暴露什么信息；相关记录统一落在当前 Bug 根目录下；问题定位或修改完成后这些诊断断言已删除。
- 驳回：断言只是为了碰碰运气，没有清晰假设，没有统一 Bug 根目录记录，或断言本身引入额外混乱。

## 执行结果归档要求

- 将断言目标、位置、失败结果和删除结论统一记录到 `artifact-storage-rules` 约定的当前 Bug 根目录中。
- 当前 Bug 根目录必须包含 `README.md`，至少写明问题现象、验证假设、断言位置、失败摘要、定位结论和清理状态。
- Bug 根目录、入口 `README.md` 和同一 Bug 根目录复用策略统一遵循 `../artifact-storage-rules/references/path-map.yaml` 与 `../artifact-storage-rules/references/update-policy.md`。
- 如果同一 Bug 有多轮断言诊断和日志诊断，统一放在同一个 Bug 根目录下，不再分散记录到其他目录。
- 如果后续需要补正式保护逻辑，应在删除当前诊断断言后，另行按正式校验规则重新设计。

## references 读取规则

- 默认先读 `references/assertion-entry-conditions.md`。
- 在定位当前 Bug 根目录、入口 `README.md` 或判断是否继续复用同一根目录时，先读 `../artifact-storage-rules/references/path-map.yaml` 与 `../artifact-storage-rules/references/update-policy.md`。
- 只有在 规划断言位置和失败上下文 时，再读 `references/assertion-placement.md`。
- 只有在 对照正反例或判断是否越界 时，再读 `references/assertion-examples.md`。
