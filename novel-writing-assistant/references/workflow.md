# 端到端工作流（workflow）

适用：从零开始写一本百万字小说，或接手半成品需要系统化。

## 闭环：建库 → 规划 → 写作 → 校验 → 修订

### 步骤 1 建库（单一事实源）
```
python scripts/build_bible.py --project ./my-novel
```
生成 `my-novel/bible/` 骨架：world-bible.md、characters/、timeline.md、plot-board.md。
随后填 `templates/` 下的模板（复制到 bible 目录后填写）：
- 世界规则 / 力量体系 / 地图 → `world-bible.md`
- 每个主要人物一张卡 → `characters/<name>.md`
- 大事年表 → `timeline.md`
- 伏笔 / 线头 / 回收 → `plot-board.md`

**原则**：bible 是唯一事实源。后续写作与校验都从这里取数。

> 📌 **不想从零搭？直接复制官方可运行示例**：
> `examples/sanguo-demo/` 是「建库 → 写 → 审计」的最小完整范例（含 bible 四件套 + 3 章正文 + README）。
> 复制该目录即可一键跑通审计，再改成你自己的故事。详见 `examples/sanguo-demo/README.md`。

### 步骤 2 规划（长弧拆解 + 字数预算）
- 读 `planning-guide.md`：把百万字拆为 卷 → 章 → 节拍；用三幕/英雄之旅/雪弗兰作通用结构参考。
- 跑预算：
```
python scripts/wordcount_budget.py --total 1000000 --volumes 5 --chapters-per-volume 60
```
输出每卷/每章字数上限，作为写作层的硬预算。

### 步骤 3 写作（双模式）
- 成稿模式：基于 bible 事实 + 本章预算，产出完整章节。
- 骨架模式：只出 节拍 / 场景卡 / 对话骨架，用户扩写。
- 约束见 `writing-guide.md`：从 bible 取事实、在场性检查、voice 一致、不超预算。

### 步骤 4 校验（确定性扫描）
每写完一批章节（建议每卷或每 10 章）：
```
python scripts/consistency_audit.py --bible ./my-novel/bible --ms ./my-novel/manuscript
```
读 `consistency-rules.md` 理解每条规则与误报边界，逐项处理报告。

### 步骤 4.5 去 AI 味二遍（首版去机械感）
首版草稿常有"机器痕迹"：破折号滥用、仿佛/似乎搭桥、段尾强行升华、无人称感受句等。
本步用 `consistency_audit.py` 的 **C11** 信号 + `de-ai-flavor.md` 改写范式做二遍去味：

1. 跑审计，看 `[C11/WARN]` 行，得到「章节 × 信号类型 × 次数」清单。
2. 照 `references/de-ai-flavor.md` 第 2 节对应范式逐章改写（八类信号都有 before/after）。
3. 重跑审计确认 C11 清零；改写后**必须重跑全量审计**，确保 C1–C10 仍 ERROR 0、伏笔状态未乱。

> 优先级：先修 C1–C10 逻辑硬伤，再处理 C11 文风信号。探测器只探雷，真正去味靠这遍改写。

### 步骤 5 修订（回写 bible）
校验发现的真矛盾，修正 manuscript **并同步回 bible**（保持单一事实源）。伏笔回收后在 plot-board 标记「已回收」。

## 频率建议
- 建库：一次性，后续增量维护。
- 规划：开局一次，重大转向时复评。
- 写作：日常。
- 校验：**每卷或每 10 章一次**（这是「稳定」的保证，不要等写完百万字再查）。

## 格式红线（建库即规避，否则对应规则失效）

| 位置 | 错误写法 | 正确写法 | 后果 |
|---|---|---|---|
| plot-board 伏笔 | `— 埋于：第1卷第3章 — 状态：待回收` | `— 埋于：第1卷 — 状态：待回收` | 加章号 → C5 解析失败漏报 |
| plot-board 状态 | `状态：部分回收` | `状态：待回收` / `已回收` | 不在枚举 → C5 不触发 |
| timeline 日期 | `公元 715 年` | `公元715年` / `建安五年` | 空格 → C2 年份匹配失败 |
| 人物卡标题 | `# 人物：陈默（规范名）` | `# 人物：陈默` | 括号 → 规范名解析错，C1 互标 |
| 人物卡别名 | `别名/曾用名：陈恪（前世…）` | `别名/曾用名：陈恪` | 长串 → 别名无效，变体误报 |
| 缺人物卡 | 文中有「陈实」却无 `characters/陈实.md` | 补卡 | 无卡 → 被误判为「陈默」变体 WARN |

> 红线已同步写入 `templates/` 各模板注释与 `examples/sanguo-demo/README.md`，复制模板即可规避。
