# 来源记录（source-notes）

> 本文件登记 `crypto-quant-analysis` 历次外部吸收的来源与落点。

## 2026-09-07 · 量化策略回测师（wm-backtest）策略迭代方法论吸收

- **外部来源**：WorkBuddy 市场 skill `wm-backtest`（个人开发者，v0.3.25，slug `wm-backtest`），本地安装源 `~/.workbuddy/skills/wm-backtest__skillhub/`。
- **描述**：量化策略回测师，把自然语言里的选股池或交易想法收成可跑的回测任务，输出结果解读与归因。
- **吸收通道**：外部吸收。
- **裁决摘要**：合并 5 条精华（策略迭代方法论/结果归因框架/一次只改一类纪律/关键分支打点/自然语言→回测工作流），拒绝 6 条（平台私有 API、ConfigOverride、阶段 XS 引擎、计费系统、8 个 reference 文件等全部为平台专属，不迁移）。
- **同域扫描**：范围 = crypto-quant-analysis（吸收目标）、crypto-price（价格查询）、quant-analyst（量化交易系统）、swap-tokens、cryptocurrency-data-api。发现 0 处重复段落（策略迭代方法论/归因框架均为本地缺失能力，同域 4 skill 零命中）。0 处门控层叠。0 处散落产物。**PASS**。
- **落点**：新增 `references/strategy-iteration-methodology.md`（~6.8KB）；修改 `SKILL.md`（策略回测 scope 增强、新增「策略迭代工作流」节、Q5 FAQ 更新）。
- **来源可回指**：本地安装源已删除；市场元数据见 `_skillhub_meta.json`（slug: `wm-backtest`, version: 0.3.25）。