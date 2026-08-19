# knowledge-flow 吸收裁决表

> 归属 owner：`skill-absorption-rules` 流程登记。本表记录 knowledge-flow 吸收外部 skill 精华的完整裁决，供后续吸收对照。

## 2026-08-19: knowledge-spider v2.0.0（skillhub）

- 来源：`knowledge-spider`（skillhub 安装，本地路径 `~/.workbuddy/skills/knowledge-spider__skillhub/`）
- 试用方式：临时 data_dir 实测 `memory_store / kb_query / kb_stats / recognize_intent / kb_context / memory_forget` 全部核心动作
- 吸收后源已删除：`~/.workbuddy/skills/knowledge-spider__skillhub/` 整目录

| 外部精华 | 本地现状 | 裁决 | 落点 / 理由 | 整理去重 |
| --- | --- | --- | --- | --- |
| 自然语言自动分类信号词表（偏好/任务/重要/事实，中英正则） | knowledge-flow 有 7 固定主题目录，但无「从内容自动判性质」辅助清单 | 合并 | capture-retrieve-distill.md 新增「信息性质自动识别（写入辅助）」节：信号词 → 信息性质 → confidence/时效提示 | 与「沉淀触发硬信号」口径对齐，避免重复判定机制；新增约 20 行 |
| 上下文注入格式（分类 emoji + 日期 + 截断限长） | 本地有「检索优先」原则，但无注入格式规范 | 合并 | capture-retrieve-distill.md 检索流程后新增「检索结果注入对话」节：格式/排序/截断/台账一致/状态过滤 | 与「引用台账」入表门槛共用规则，不重复定义 |
| SQLite 存储 + usage_log 表 | 本地红线：Markdown 文件 + Google Drive 同步（knowledge-layout.md 固定根目录） | 拒绝 | 机制形态不迁移：二进制库不利于同步/检索/人类可读 | N/A |
| LIKE 搜索 + Jaccard 相似度 + 多维排序 | knowledge_index.py 六字段结构化全库检索（100% 覆盖） | 保留本地 | 本地更强（结构字段 > 全文 LIKE） | N/A |
| 访问计数（access_count/last_accessed） | 无此概念 | 拒绝 | 文件系统下维护成本高、收益低，与索引自动重建机制冲突 | N/A |
| 删除确认 / 分级处置 | conflict-staleness.md 分级处置（改状态/归档/删除 + 接替关系） | 保留本地 | 本地更强（有接替关系与 check 校验） | N/A |
| 统计（kb_stats） | knowledge_index.py stats 命令 | 保留本地 | 本地已有 | N/A |
| 四类意图识别路由（store/query/delete/stats） | 本地「选择性默认判定」机制（检索/沉淀/不适用） | 拒绝 | 外部实现有实测误判 bug（store 正则抢占 query/delete），且与本地触发机制重叠 | N/A |
| 存储前去重 | 三态判定 + 查同主题（capture-retrieve-distill.md） | 保留本地 | 本地更强；外部 SKILL.md 宣称有去重但代码未实现（空宣称，见案例沉淀） | N/A |

**净增预估与实际**：预估新增 1 个 reference 内 2 小节约 +60 行；实际新增 40 行（检索注入 10 行 + 信息性质识别 30 行），SKILL.md 未膨胀（引用链原本已覆盖 capture-retrieve-distill.md），零新增目录。
**分数变化**：基线 84.7 → 吸收后 86.2（+1.5 分，独立子 agent 评分，棘轮通过）。
**案例沉淀**：`references/case-knowledge-spider-absorption.md`。

## 2026-08-19 补充：重复安装再次清理

- 23:10 用户再次安装 knowledge-spider v2.0.0（用户级 + 工作区两份），要求再吸收。
- 校验：与已吸收版本 SKILL.md / index.py md5 完全一致（`50f352bd` / `3f7ba527`），无增量价值，不重复吸收。
- 处置：用户确认后删除两份重复源（用户级 `C:\Users\luode\.workbuddy\skills\knowledge-spider__skillhub` + 工作区 `D:\谷歌云盘\luode-skills\knowledge-spider__skillhub`）。
- 登记：本次为重复安装清理，无新裁决条目；吸收成果（capture-retrieve-distill.md 两节 + 登记文件）双位置均完好。
