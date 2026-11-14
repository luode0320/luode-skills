# 来源记录

## 上游来源

| 项 | 内容 |
|---|---|
| 名称 | Jailbreaks（system prompts / persona locks / workspace policies / agent operating specifications） |
| 地址 | `https://github.com/togg53192-cmd/jailbreaks` |
| 首次入库 | 2026-11-07 |
| 锁定版本 | `f639dac0b89792165afa9e3b6922e429ad9098e4` |
| 规模 | 45 个提示词文件、约 663 KB |
| 许可 | 仓库未声明开源许可证；上游 README 明确「仅供研究与教育用途」。本地按「研究样本」定位使用，不做商业分发 |
| 获取方式 | `git clone --depth 1`（一次性浅克隆），不使用 GitHub API（曾有速率限制 403） |

## 吸收裁决记录（2026-11-07）

按 `skill-absorption-rules` 的三态裁决，逐条登记如下。

| # | 来源条目 | 本地现状 | 裁决 | 落点 | 理由 |
|---|---|---|---|---|---|
| 1 | 45 份提示词原文 | 无同类资产 | 合并 | `prompts/` | 离线可用、升级可 diff、来源可回指 |
| 2 | 一文件一提示词的目录约定 | 本仓库 skill 为 `SKILL.md + references + scripts` | 合并 | `prompts/` 平铺 + `data/index.json` 索引 | 只吸收约定，不改本地 skill 结构 |
| 3 | 五种载体形态（系统提示 / AGENTS.md / 工作区策略 / harness 配置 / Modelfile） | 无 | 合并 | `references/adaptation-matrix.md` | 载体区分正是「怎么用」的关键 |
| 4 | 提示词写法手法（身份锁定、优先序、两分结构、反占位清单） | 有编码类规则，无提示词手法库 | 合并 | `references/prompt-techniques.md` | 提炼为手法条目，不搬运原句 |
| 5 | 「更严格策略未加载，只是训练残留」类覆盖话术 | 与 `AGENTS.md` 红线冲突 | 拒绝 | 反例区登记 | 不作为模板交付 |
| 6 | 「冲突不向操作者暴露」 | 破坏可审计性 | 拒绝 | 反例区登记 | 同上 |
| 7 | 「授权已由他人满足，不要追问」 | 伪造授权前提 | 拒绝 | 反例区登记 | 同上 |
| 8 | 上游持续更新的维护形态 | 无同步机制 | 合并 | `scripts/sync_upstream.py` | 升级是用户明确诉求 |
| 9 | 面向免费隐身模型的绕过型提示词 | 越界 | 拒绝 | 仅作研究样本 | 不生成绕过第三方供应商策略的操作指导 |

## 与本地 skill 的边界

| 相邻 skill | 边界 |
|---|---|
| `code-generation-style-rules` | 管写代码风格；pojia 只产出 agent 前置提示词，不写业务代码 |
| `write` / `humanizer` | 管文本润色与去 AI 味；pojia 不负责改写用户正文 |
| `skill-absorption-rules` | 管 skill 体系自身的吸收裁决；pojia 是它的一个产物，不反向管理它 |
| `implementation-planning-rules` | 管实施规划；pojia 不产出实施计划 |

## 维护责任

| 触发 | 动作 |
|---|---|
| 上游有新模型 | `sync_upstream.py --check` → `--apply` → 路由表加族 → 验证三条 |
| 路由错配被发现 | 改 `data/model-routing.json` 的 alias 或 candidates 顺序，不改脚本 |
| 上游口径变化 | 在本文件与 `references/prompt-techniques.md` 反例区同步更新 |
| 升级完成 | 在 `references/upgrade-playbook.md` 的升级记录表追加一行 |
