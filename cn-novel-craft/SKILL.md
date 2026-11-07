---
name: cn-novel-craft
description: 中文长篇小说创作与质量管控一体方法论（合并版 v2.0）。融合 WorkBuddy open-novel-writing 的模块化工程流程 + novel-16d-review 的16维审核框架 + 本地长篇小说批量自动化（long-form novel batch automation）的量化门禁/去AI感/叙事结构/声线卡/钩子工程。覆盖 设定→大纲→章节spec→正文生成→量化门禁→16维审核→批量推进→插章重编号 的完整闭环。
description_zh: 中文长篇小说创作与质量管控一体方法论（合并版 v2.0）。融合 WorkBuddy open-novel-writing 的模块化工程流程 + novel-16d-review 的16维审核框架 + 本地长篇小说批量自动化（long-form novel batch automation）的量化门禁/去AI感/叙事结构/声线卡/钩子工程。覆盖 设定→大纲→章节spec→正文生成→量化门禁→16维审核→批量推进→插章重编号 的完整闭环。
description_en: An integrated methodology for writing and quality-controlling Chinese long-form web novels (network fiction). Merges WorkBuddy's modular writing pipeline with a 16-dimension review framework and machine-checkable quality gates (de-AI-ify 34 patterns, narrative structures, character voice cards, hook engineering, ban-word / em-dash / dialogue-tag checks, plus an insert-chapter renumbering workflow). Provides systematic diagnostics to significantly reduce AI-generated traces. For Chinese web-novel and long-fiction writers.
version: 2.0.0
category: creative
agent_created: true
tags: [novel, writing, quality-gate, de-ai-ify, review, batch]
license: MIT
visibility: public
display_name: 中文小说创作与质量管控
display_name_en: Chinese Novel Craft
author: 普通青年
---

# 中文小说创作与质量方法论（合并版 v2.0）

> 本技能是两套方法论的合并产物：
> - **WorkBuddy 固有所长**：模块化工程流程（设定/大纲/章节spec/正文/批量推进）、16维系统审核框架、分级红线机制。
> - **批量自动化所长（吸取）**：可机检的量化门禁（破折号/对话标签/情绪命名/ban词）、风格锚定卡、钩子工程、去AI感34模式+4大死亡气味、情绪行为外化、比喻三原则、7大真实人声、叙事结构库（Save the Cat/Story Circle/MRU）、角色声线卡、伏笔登记册、文件写入铁律4步。

---

## 一、创作流程（来自 open-novel-writing，工程骨架）

```
想法 → 设定(世界观/人物/势力/伏笔) → 大纲(起承转合/卷规划/高潮) → 章节spec(YAML) → 正文生成 → 量化门禁 → 16维审核 → 修订 → 批量推进
```
各模块可独立使用，也可串行。章节 spec 建议字段：
```yaml
chapter: 101
title: "章节标题"
summary: "200字内摘要"
before_state: {characters:[{name,state,location}], plot_hooks:[...]}
after_state:  {characters:[...], plot_advances:[...]}
must_happen: [...]
tension_curve: [{position:0,value:3,note:"铺垫"},{position:50,value:8,note:"高潮"}]
key_scenes: [...]
new_hooks: [...]
```

## 二、风格锚定卡（生成每批前必须输出 · 批量自动化所长）

```
### 风格锚定 ###
主角视角：[角色名]（第一人称"我"/第三人称）
本章起止：第X章至第X+2章
当前核心冲突：[本章核心矛盾]
五感重点：[至少3个]
禁用词检查：完整 ban/warn/limit 三级扫描
本章钩子类型：[危机/悬疑/反转/信息/情感/时间/选择/生存 中选1]
人物风格：[角色A]=[关键特征] / [角色B]=[关键特征]
情节结构：冲突→探索→转折→悬念（钩子）
### 锚定完毕 ###
```

## 三、10步量化门禁（每章生成后必执行 · 批量自动化所长，可机检）

```
1️⃣ 字数安检：常规章≥3000字
2️⃣ 破折号安检：≤12处/章（解释→冒号；转折→句号；补充→分号；强调→动作打断）
3️⃣ ban词扫描：零容忍（见下方 ban 词表）
4️⃣ warn词计数：≤3次/章
5️⃣ limit词计数：每种不超限
6️⃣ 钩子检测：必须存在且类型≥1种
7️⃣ 对话标签检测：裸标签"我说/他说"≤30%，≥70%替换为动作标签
8️⃣ 章末检测：非反问/非感叹/非平收("第X章完"不作末句)
9️⃣ 情绪命名检测："感到/觉得"≤2次/章
🔟 段落均匀度：长短句交替
```
ban 词示例（零容忍）：`不禁 / 与此同时 / 一股XX涌上心头 / 然而 / 内心深处 / 缓缓说道 / 命运的齿轮 / 宿命感 / 忍不住 / 下意识地 / 不由自主地`
warn 词（≤3次）：`深吸一口气 / 时间来到了 / 另一边 / 仿佛 / 似乎`

## 四、钩子工程（批量自动化所长）
1. 每章末尾必须有明确钩子；2. 连续3章不可用同一种钩子；3. 每5章内覆盖≥4种类型；4. 禁反问/感叹结尾；5. 禁平收。

## 五、去 AI 感（批量自动化所长 + novel-16d-review 维度13）

**12 种 AI 痕迹（生成后自检）**：
1. 段落均长→长短交替 2. 场景固定顺序→从声音/动作/对话切入 3. 过渡词"与此同时/另一边/时间来到了"→删
4. 情绪直接命名→用行为 5. 所有角色内心独白一个风格→差异化 6. 对话后必跟情绪标签→去掉80%
7. "不禁/忍不住/一股XX涌上心头"→删80% 8. 五感公式化"空气中弥漫着XX的味道"→改写
9. 比喻都"安全"→具体+意外+角色化 10. 过渡词堆砌→减 11. "不由自主/下意识"→减 12. 每章结尾都是反问/感叹→多样化

**4 大死亡气味**（出现即高危）：堆砌排比、三段式强行升华、空洞象征、AI 套话（"众所周知/不言而喻"）。

**情绪表达铁律**：`他感到紧张`→`他把烟点反了两次`；`她很害怕`→`她的指甲掐进了掌心`；`他很愤怒`→`他没说话，只是把杯子放到了桌上，声音很响`。

**比喻三原则**：具体（能想象画面）/ 意外（跨类别连接）/ 角色化（符合 POV 认知）。
**7 大真实人声**：不完整、重复、跑题、延迟、说错话、物理性(渴饿累痒)、当下(记忆碎片化)。

## 六、叙事结构库（批量自动化所长）
- **Save the Cat! 15 节拍**：开场画面1% → 催化剂10% → 中点50%(假胜利/假失败必含) → 一切失去75% → 暗夜灵魂75-80% → 终极对决80-99% → 终场99-100%。
- **Story Circle（章级）**：YOU→NEED→GO→SEARCH→FIND→PAY→RETURN→CHANGE。
- **网文节奏公式**：每3000字小爽点 | 每10000字中爽点 | 每30000-50000字大爽点 | 每章末必留钩子。
- **MRU 单元（刺激→反应）**：`[外部刺激]→[感觉0.1s]→[反射动作0.5s]→[理性思考1s]→[言语行动数秒]`。新手常错：跳过感觉/反射直接理性，不像真人。

## 七、角色声线卡 + 反派设计（批量自动化所长）
- **声线卡**：高频词 / 句式特征 / 比喻域 三维差异化。例：理性型=科学类比+长句分析；感性型=自然/地质类比+柔和长句；焦虑型=超短句+急促碎片化。
- **反派设计**：从自身视角行为合理；与主角共享同一 Wound；某个时刻让读者动摇"也许他们是对的？"。

## 八、伏笔登记册（批量自动化所长）
每完成一批(3章)更新：记录新伏笔、更新已有伏笔状态、检查待回收伏笔是否遗漏。

## 九、16 维审核框架（WorkBuddy 固有所长 · 批量自动化实践无此成体系维度）

### 宏观（灵魂与骨架）
| # | 维度 | 检查点 |
|---|------|--------|
| 1 | 核心创意与主题 | 一句话梗概清晰；主题贯穿；无说教；独创性 |
| 2 | 结构与节奏 | 开篇500字钩子；三幕清晰；高潮强度；悬念埋收；结尾质量 |
### 中观（血肉与张力）
| 3 | 人物塑造与弧光 | 立体度；弧线完整；配角工具化；反派动机；一致性 |
| 4 | 情节与冲突逻辑 | 因果非巧合；冲突升级；时间线/地理/设定自洽；支线收束 |
| 5 | 世界观与设定 | 规则自洽；信息自然渗透；考据严谨 |
### 微观（感官与笔触）
| 6 | 场景与描写 | 展示非告知；五感覆盖；转换自然；冗余/匮乏 |
| 7 | 对话 | 听感；功能性；标签不滥用；潜台词留白 |
| 8 | 语言与文笔 | 句式流畅；重复度；一致性；语病；标点 |
### 包装（投稿与市场）
| 9 | 书名与简介 | 记忆点；200字钩子+卖点；标签匹配 |
| 10 | 平台契合度 | 调性；敏感内容；篇幅 |
| 11 | 格式与体例 | 编号统一；排版；专名一致 |
| 12 | 情感力量与余味 | 高潮渲染；结尾余味；弃文风险点 |
### AI 专项（维度13-16）
| 13 | 祛除 AI 味 | 逻辑连词密度；句式多样性；心理总结泛滥；噪声注入改写（用第五节清单） |
| 14 | 逻辑黑洞与幻觉 | 情感因果断裂；物理/时间/空间错误；反向推演 |
| 15 | 原创性与融梗 | 高相似排查；设定内部污染 |
| 16 | AI 协作效能 | 关键高潮谁主笔；转折是否过度依赖AI建议（仅AI辅助创作时审） |

**输出**：`《书名》16维审核报告` = 总评(综合分/优势/问题) + 各维度评分表 + TOP5修改建议 + 优化版正文(标注[优化])。

## 十、分级红线（WorkBuddy 固有）
- **P0 绝对禁止**：明显AI词汇、感悟式结尾("他明白了")、感叹式结尾、上帝视角、抄袭级错误。
- **P1 建议避免**：套路化、流水账、抽象心理("他感到很")、排比句、代词连续开头。
- **P2 可选优化**：细节打磨、画面强化、节奏调整。

## 十一、文件写入铁律4步（批量自动化所长 · 防并发膨胀）
`read_file 全文 → 内存合并 → write_file 覆盖 → read_file 验证`。**严禁子代理并行修改同一文件**（会导致内容重复膨胀），被其他代理改过的文件由主代理直接 patch。

## 十二、批量推进（来自 open-novel-writing）
"推进N章"：循环[更新设定→章节spec→正文→量化门禁→16维审核→达标进下一章]，不通过则修订(≤2次)，仍不通过标记跳过。每章自动保存，可中断。

## 十三、插章与重编号工作流（吸收 novel-chapter-insert 所长）

用于给"第NNN章 标题"按序号编号的小说批量插入新章（扩写/放慢节奏/加情节）。核心难点：整块插入会破坏重编号、插错位置导致章号错位、插章破坏"仅主角知晓某秘密"类铁律。

**标准脚本模板（expand_actN.py）**
```python
# -*- coding: utf-8 -*-
import io, sys, re
SRC = r'...原文.txt'            # 作用于【原文】，不要直接改派生文件
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
# (before_num, 标题, 正文) — 新章插在 before_num 这一章【之前】
CH = [(256, '盟书初定', '　　正文段落，全角空格缩进。可多段。'),
      (258, '论功',     '　　第二段示例。')]
raw = open(SRC, encoding='gb18030').read()
lines = raw.split('\n')
chap_re = re.compile(r'^\s*第\s*0*([0-9]+)\s*章')
def find_chapter_line(num):
    for i, l in enumerate(lines):
        m = chap_re.match(l)
        if m and int(m.group(1)) == num: return i
    return None
# 关键：DESC 顺序插入，低号不扰动高号行位置
for before_num, title, body in sorted(CH, key=lambda x: x[0], reverse=True):
    idx = find_chapter_line(before_num)
    if idx is None: print('未找到第%d章，跳过' % before_num); continue
    # 关键：必须 .split('\n') 逐行插入，否则整章塌成一行导致重编号丢正文
    new_block = ('第%03d章 %s\n' % (before_num, title) + body).split('\n')
    for bl in new_block: lines.insert(idx, bl); idx += 1
# 整体顺序重编号（保留标题文字）
new_lines = []; cur = 0
for l in lines:
    m = chap_re.match(l)
    if m:
        cur += 1
        mm = re.match(r'^\s*第\s*0*([0-9]+)\s*章\s*(.*)$', l)
        title_part = mm.group(2).strip() if mm else ''
        new_lines.append('第%03d章 %s' % (cur, title_part))
    else:
        new_lines.append(l)
open(SRC, 'w', encoding='gb18030').write('\n'.join(new_lines))
print('插入章数:', len(CH), ' 总章数:', cur)
```

**必做步骤**：① 先备份原文 `cp 原文.txt 原文·扩写前备份.txt`；② 写 `expand_actN.py`，`before_num` 选目标段内现有章号；③ 运行 → 校验（见下）；④ 重跑派生（第一人称转换版 / 细纲 / 粗纲，粗纲的幕范围起止按内容锚点重新定位）。

**校验脚本（每次必跑）**：读取校验章号连续（`nums == list(range(1, nums[-1]+1))`）、无空章、无残留旧词（改名后应为 0）。

**铁律审计（"仅主角知 X"类约束）**：遍历每章正文，对每个配角专名检查——同一句（按 。！？\n 切分）内不得同时出现 配角名 与 秘密元素（如某秘籍来源词）。主角可在内心独白提及，配角绝不可说破；新章里把秘密来源写作"自家琢磨的心得/秘籍指的路"即可安全绕过。

**坑位清单**：① 整块插入塌行——务必 `body.split('\n')` 逐行 insert；② 升序插入错位——务必 DESC 顺序；③ 编码——源是 GBK，读/写均用 `gb18030`，脚本本身 UTF-8；④ 粗纲范围过期——每扩完一段按内容锚点（关键情节节点、势力更迭处）重定位；⑤ 插章卡时间线——若原文有分期改名设定（前期称A、后期称B），新章需对应时期用语。

**人物/派系改名（前置可选）**：全量改名按 old 长度降序逐词替换避免子串错替；书名号内或含关键词的行需 skip 保护（如"金戒指"≠"金手指"）。

---
**合并说明**：创作流程/16维审核/分级红线为 WorkBuddy 固有；量化门禁/风格锚定/钩子工程/去AI感/叙事结构/声线卡/伏笔登记/写入铁律为吸收 批量自动化所长。两者互补——前者解决"系统诊断"，后者解决"可机检硬指标"。（插章与重编号工作流见第十三节，吸收 novel-chapter-insert 所长。）
