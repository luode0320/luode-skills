# 番茄殿堂作家（tomato-palace-master）

> WorkBuddy 平台技能 · **v2.0.0** · 知识截止 2026-09-11
> 番茄小说平台殿堂级网文创作与运营总引擎：从一句选题到百万字连载、再到数据诊断与短剧改编评估的完整流水线。

---

## 一、这是什么

「番茄殿堂作家」不是写作助手，而是**殿堂级作家分身 + 数据军师 + 改编评估师**。它把番茄平台的算法逻辑、留存机制、签约规则、福利档位、AI 治理红线，内化成一条可执行的生产流水线。

**五个天花板能力**：

| 能力 | 一句话 | 对标与超越点 |
|---|---|---|
| **黄金三章生死线引擎** | 把"开篇看天赋"变成可复现的工程 | 同类工具只给三章正文；本技能给**能过 8 万字三次评估的三章** + 开篇 100 分评分 + 十二类低留存自检 |
| **殿堂笔触（零 AI 味）** | 读三句就知道是人写的 | 60+ 条 AI 腔正则 + **AI 痕迹十大清单 + 五大标志 + 五大人味规则 + 情绪替换素材库**，逐句给替换清单与评分 |
| **算法对齐作战室** | 每份交付附"当前该做什么" | 六层流量池 + 各阶段及格线 + 断流红线，逐阶段给出考核指标与 7 天动作 |
| **数据回填诊断引擎**（V2 新增） | 把后台数据翻译成病因与处方 | 同类只会说"多更新"；本技能给出**阶段判定 → 未达标清单 → 病因排序 → 处方 → 7 天动作**，严守"先修最前端"铁律 |
| **短剧改编评估引擎**（V2 新增） | 选题阶段就判断值不值得拍 | 10 维改编评估卡（100 分制），对齐"664 部爆款短剧中 413 部来自番茄 IP"的产业事实 |

## 二、目录结构

```text
tomato-palace-master/
├── SKILL.md                      # 技能主文件（frontmatter + 五能力 + 五大协议 + 十阶段工作流）
├── README.md                     # 本文件
├── references/                   # 知识库（21 个文件 / 3871 行，AI 按需加载）
│   ├── platform-mechanics-2026.md      # 平台机制全解（流量池/三关制/五大数据/治理红线）
│   ├── monetization-welfare-2026.md    # 变现与福利全解（全勤/星火/完本/征文/版权）
│   ├── traffic-pool-and-diagnosis.md   # 流量漏斗 + 数据回填诊断 + 算法对齐卡
│   ├── opening-engineering-2026.md     # 开篇工程学（四窗口/12类低留存/8模型/100分表）
│   ├── golden-three-chapters.md        # 黄金三章工程学（章级配方）
│   ├── viral-tracks-2026.md            # 赛道雷达（趋势/蓝海/热门设定）
│   ├── genre-atlas-2026.md             # 全赛道图谱（男频14+女频9/标签流量量级）
│   ├── title-blurb-tags.md             # 书名简介标签公式库
│   ├── book-test-and-crisis-rescue.md  # 书测套餐 + 断流急救 + 切书决策
│   ├── long-form-architecture.md       # 百万字架构（伏笔台账/人设弧光/一致性）
│   ├── character-and-dialogue.md       # 人物塑造与对话工程
│   ├── plot-rhythm-and-hooks.md        # 节奏·钩子·爽点密度
│   ├── anti-ai-style.md                # 零 AI 味手册（含附编 V2 人味工作流）
│   ├── reader-persona-2026.md          # 读者画像与场景工程
│   ├── reader-psychology.md            # 读者心理与情绪引擎
│   ├── short-drama-adaptation.md       # 短剧/漫剧改编评估卡
│   ├── platform-matrix.md              # 多平台口径矩阵与转换器
│   ├── prompt-library.md               # 24 组可直接复用的提示词
│   ├── quality-rubric.md               # 100 分制质检卡（含 V2 附加维度）
│   ├── web-search-protocol.md          # 增强联网搜索协议
│   └── changelog.md                    # 变更日志 + 待核验项
├── scripts/                      # 确定性脚本（8 个，零依赖，仅标准库）
│   ├── opening_predict.py              # 开篇 100 分评分 + 十二类低留存检测
│   ├── tomato_audit.py                 # 稿件殿堂体检（AI 味评分 + 逐句替换清单）
│   ├── data_diagnosis.py               # 后台数据 → 阶段判定 → 病因 → 处方 → 7 天动作
│   ├── book_test_gen.py                # 书测 5 组素材套餐生成
│   ├── chapter_ops.py                  # 章节作战表生成与节奏校验
│   ├── search_matrix.py                # 三波次联网检索关键词矩阵
│   ├── monthly_evolution.py            # 时效检查/扫描/作业单/记录进化/版本递增/包自检
│   └── export_markdown.py              # Markdown 导出与交付整理
└── templates/                    # 输出模板（5 个）
    ├── novel-brief.md                  # 作品立项卡
    ├── outline.md                      # 分卷分章大纲
    ├── chapter.md                      # 章节正文
    ├── diagnosis-report.md             # 数据回填诊断报告
    └── book-test-package.md            # 书测素材套餐
```

## 三、使用示例

**① 从零写一本**
> 帮我写一本番茄的悬疑脑洞新书，主角是殡仪馆化妆师。

依次产出：赛道卡 → 立项卡 → 流量门面（书名 + 简介 + 标签）→ 黄金三章正文 → 开篇 100 分评分 → 前 30 章细纲 → 体检报告 → 算法对齐卡。

**② 只要开篇三章**
> 给我三章开篇，题材：穿越毒士 + 职场厚黑。

走 Craft 模式，直接产出可发布正文 + 开篇评分 + 十二类低留存自检（低留存命中项必须逐条修复，**≥85 分才交付**）。

**③ 诊断已有稿件**
> 我这本写到 12 万字，数据掉得厉害，帮我看看。

走 Rescue 模式：跑 `data_diagnosis.py` 做阶段判定与病因处方 → 跑 `tomato_audit.py` 与 `opening_predict.py` 定位内容问题 → 给 7 天补救清单 + 三条死命令自查。

**④ 首秀扑街想翻盘**
> 我 22 万字了，首秀数据很差，还有救吗？

走书测路径：`book_test_gen.py` 生成 5 组素材套餐 + 封面方向 + 简介骨架 + 操作禁忌；附切书决策模型（3 次评估机会未用尽前不轻言切书）。

**⑤ 选题能拍短剧吗**
> 我这个题材适合改成短剧吗？

走 Adapt 模式：10 维改编评估卡打分 + 改编方向判断（真人短剧 / AI 漫剧 / 双适配）+ 改造建议 + 预估集数。

**⑥ 检查资源库时效 / 月度进化**
> 检查时效 / 月度进化

```bash
python scripts/monthly_evolution.py --check
python scripts/monthly_evolution.py --worklist 进化作业单.md
# ……联网核验并更新 references 后……
python scripts/monthly_evolution.py --verify --note "本次变更摘要"
python scripts/monthly_evolution.py --bump-version minor
python scripts/monthly_evolution.py --selfcheck
```

## 四、脚本用法

```bash
# 开篇留存预测（100 分制 + 十二类低留存）
python scripts/opening_predict.py ./开篇 --json

# 稿件殿堂体检（AI 味评分 + 逐句替换清单）
python scripts/tomato_audit.py ./chapters --json --out 体检报告.json

# 数据回填诊断（后台数据 → 病因处方）
python scripts/data_diagnosis.py --input 后台数据.md --out 诊断报告.md

# 书测 5 组素材套餐
python scripts/book_test_gen.py --genre 古言 --hero 商户女 --twist 重生先知 \
    --conflict 退婚 --tag "重生,退婚,空间" --out 书测套餐.md

# 生成 30 章作战表 / 校验节奏
python scripts/chapter_ops.py --gen 30 --out 章节作战表.md
python scripts/chapter_ops.py --check 章节作战表.md

# 三波次联网检索关键词矩阵（按当期月份自动生成）
python scripts/search_matrix.py --out 检索清单.md

# 资源库时效检查 / 逐文件扫描 / 结构自检
python scripts/monthly_evolution.py --check
python scripts/monthly_evolution.py --scan
python scripts/monthly_evolution.py --selfcheck

# 导出整合稿 + 分章稿 + 交付说明（全部 Markdown）
python scripts/export_markdown.py --input ./chapters --out ./交付 --title 书名 --split
```

## 五、上传到 WorkBuddy 开放平台

1. 将本目录打包为 `tomato-palace-master.zip`（**zip 内顶层必须是单一项目目录 `tomato-palace-master/`**）；
2. 打开 open.workbuddy.cn → 登录 → 【技能】→ 创建技能 / 上传 zip；
3. 表单需**单独上传 512×512 技能图标**（图标不在 zip 内，平台不从 zip 读取）；
4. 平台解析确认 → 提交审核 → 审核通过后发布（实操约 7 个工作日）；
5. **版本递增**：任何改动重新上传前，必须先把 `SKILL.md` 的 `version` 递增，否则平台拒收；
6. **name 不可改**：`tomato-palace-master` 是平台唯一标识，上传后不可变更，改名只能新建。

## 六、时效与进化

- 资源库知识截止 **2026-09-11**，滞后 ≤30 天为新鲜；31–60 天建议核验；>60 天输出需标注「未联网校验」。
- **已配置每月 1 号 00:30 自动进化任务**：运行时效检查 → 按 7 大主题 / 21 组关键词联网核验 → 更新 references → 追加 changelog → 复验时效 → 版本递增 → 重新打包归位（历史版本不覆盖）。
- 平台规则、榜单数据、福利条款均在快速变动，**重要决策前请复核最新官方公告**。

## 七、输出格式

**所有生成的文字内容一律直接落盘为 Markdown（`.md`）文件**，可按需随时导出为 PDF / Word / HTML / TXT 等主流文档格式。

## 八、合规声明

- 本技能**不提供、不支持任何"绕过平台 AI 检测"的方法**；所有文字处理只做**真实提升质量**的改写（目标不是骗过检测，是达到手写水准）。
- 不生成抄袭、洗稿、未授权同人改编内容。
- 不承诺收入数字；所有福利金额表述为"公开信源整理，以作者后台实际结算为准"。
- 联网结论均标注来源与日期（【官方】/【实操】/【分歧】/【推断】四级），不把历史榜单表述为实时数据。
- 涉及短剧/版权话题时提示合同约束（独家原创首发是参与大部分征文与新增福利的前置条件；改编权授予范围需看清）。
