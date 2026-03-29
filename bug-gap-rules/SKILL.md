---
name: bug-gap-rules
description: 当 Bug 描述缺少复现条件、环境信息、输入数据、报错日志、影响范围或关键时间线，导致后续复现与定位无法可靠推进时触发。负责识别缺失项、区分阻断级与非阻断级缺口，并统一记录到 Bug 根目录，阻止盲目进入定位。
---

# Bug 缺口识别规则

只在 Bug 已经被提出来，但入口信息还不够支撑复现、归属或定位时使用这个 skill。
如果当前已经具备足够信息开始复现或定位，请转交 `bug-reproduction-rules` 或 `bug-root-cause-rules`。

## Skill 作用与适用场景

- 识别 Bug 入口中到底缺了哪些基础信息。
- 区分只是补充说明，还是已经阻断复现和定位推进。
- 输出明确的待补信息清单，避免边猜边调。
- 将缺口清单和阻断判断统一沉淀到当前 Bug 根目录。
- 把 Bug 入口和后续复现、定位步骤解耦。

## 自动触发信号

- 问题描述里只有“报错了”“不对了”，没有稳定场景和证据。
- 缺少环境、数据、日志、时间点、账号或触发前提。
- 团队对是否能直接进入复现或定位存在争议。
- 同一个 Bug 被多次转述后，入口信息明显失真。

## 进入后先做什么

1. 先区分当前已有信息和真正缺失的信息。
2. 为当前 Bug 确认统一的根目录，继续沿用 `artifact-storage-rules` 约定的当前 Bug 根目录。
3. 判断缺失项会影响复现、范围界定还是根因定位。
4. 把缺口按阻断级和非阻断级排序。
5. 输出待补信息列表和补齐优先级。

## 默认执行流程

1. 默认先读 `references/gap-checklist.md`，先检查 Bug 入口最少应包含哪些信息。
2. 再读 `../artifact-storage-rules/references/path-map.yaml` 与 `../artifact-storage-rules/references/update-policy.md`，确认 Bug 根目录、入口 `README.md` 和同一 Bug 持续复用同一根目录的策略。
3. 如需继续展开，再读 `references/blocking-signals.md`，需要判断哪些缺口会阻断推进。
4. 需要对照边界或正反例时，再读 `references/gap-examples.md`，需要对照缺口识别正反例。
5. 输出 Bug 缺口清单、阻断判断和补充优先级，并更新到当前 Bug 根目录下的 `README.md`。
6. 缺口补齐后再进入 `bug-reproduction-rules` 或 `bug-root-cause-rules`；若基础问题描述本身混乱，可回流 `bug-intake-rules`。

## 权责边界与不负责事项

- 只负责识别缺口，不替代 `bug-intake-rules` 的标准化录入职责。
- 不直接设计复现步骤，那属于 `bug-reproduction-rules`。
- 不提前猜根因，也不把缺口识别当成定位结果。
- 不因为轻微缺口就过度阻断所有后续动作。

## 需要暂停并确认的条件

- 连异常现象本身都无法准确描述。
- 缺失项已经阻断复现和定位，但来源方暂时无法补齐。
- 问题来源和环境版本互相矛盾，无法形成可信入口。
- 团队试图用猜测替代缺失信息继续推进。

## 执行通过 / 驳回标准

- 通过：能够明确列出缺失项、说明其影响，并判断哪些缺口必须先补齐、哪些可后续补充。
- 驳回：只是笼统地说“信息不够”，没有具体缺口列表、没有优先级，或直接绕过缺口继续定位。

## 执行结果归档要求

- 将缺口清单、阻断结论和补充优先级统一记录到 `artifact-storage-rules` 约定的当前 Bug 根目录中。
- 当前 Bug 根目录必须包含 `README.md`，至少写明当前已知信息、缺失项、影响面和下一步动作。
- Bug 根目录、入口 `README.md` 和同一 Bug 根目录复用策略统一遵循 `../artifact-storage-rules/references/path-map.yaml` 与 `../artifact-storage-rules/references/update-policy.md`。
- 如果缺口来自历史信息断裂，应保留来源说明，便于后续追溯，并继续沿用同一个 Bug 根目录。

## references 读取规则

- 默认先读 `references/gap-checklist.md`。
- 在定位当前 Bug 根目录、入口 `README.md` 或判断是否继续复用同一根目录时，先读 `../artifact-storage-rules/references/path-map.yaml` 与 `../artifact-storage-rules/references/update-policy.md`。
- 只有在 区分阻断级和非阻断级缺口 时，再读 `references/blocking-signals.md`。
- 只有在 需要对照样例或判断是否过度阻断 时，再读 `references/gap-examples.md`。
