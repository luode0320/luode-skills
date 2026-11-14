# 来源与裁决记录（SOURCES）

本技能由 7 个已安装写作 skill 与 MuMuAINovel 项目合并而成。本文件是完整的裁决台账，供后续追溯与再吸收对照。

合并日期：2026-11-07
裁决依据：`skill-absorption-rules` 三态裁决矩阵 + `merge-strategies.md` 融合型策略

---

## 一、来源清单

| # | 来源 | 版本 | 体积 | 形态 | 裁决 |
|---|---|---|---|---|---|
| 1 | cn-novel-craft | 2.0.0 | 53 KB | skill | 合并（主力承接） |
| 2 | novel-writing-assistant | 1.7.2 | 150 KB | skill | 合并（唯一硬资产） |
| 3 | novel-outline | 1.0.0 | 8.6 KB | skill | 合并（大纲权威） |
| 4 | conflict-max-web-fiction | 1.0.0 | 8.4 KB | skill | 合并（续写分支权威） |
| 5 | human-writing | 1.0.0 | 81 KB | skill | 合并（拆两半） |
| 6 | tomato-palace-master | 2.0.0 | 384 KB | skill | 降级保留 |
| 7 | story-import | 4.0.0 | 3.6 KB | skill | 合并（被上游超越） |
| 8 | MuMuAINovel | v1.5.8 | 应用 | Docker 应用 | 部分吸收 |

---

## 二、逐项裁决表

### 2.1 cn-novel-craft → 合并（主力承接）

| 外部精华 | 本地现状 | 裁决 | 落点 |
|---|---|---|---|
| 10 步量化门禁（字数/破折号/ban词/对话标签/钩子/情绪命名） | 本地小说域为空 | 合并 | `06-去AI味.md` 第五节 |
| 16 维审核框架 | 空 | 合并 | `07-质量门禁.md` 第二节 |
| 分级红线 P0/P1/P2 | 空 | 合并 | `07-质量门禁.md` 第一节 |
| 章节 spec YAML 结构 | 空 | 合并 | `07-质量门禁.md` 第四节 |
| 风格锚定卡 | 空 | 合并 | `07-质量门禁.md` 第五节 |
| 叙事结构库（Save the Cat / Story Circle / MRU） | 空 | 合并 | `03-大纲工程.md` 第五节 + `04-正文技法.md` 第二节 |
| 角色声线卡 | 空 | 合并 | `04-正文技法.md` 第五节 |
| 伏笔登记册 | 与 nwa C5 重复 | 合并（去重） | 合并进 `02-设定与一致性.md` 第四节 |
| 文件写入铁律 4 步 | 空 | 合并 | `07-质量门禁.md` 第六节 |
| 插章重编号 Python 工作流 | 空 | 合并 | `05a`/`05b` 续写与同人 第五节（坑位清单） |

### 2.2 novel-writing-assistant → 合并（唯一硬资产）

| 外部精华 | 本地现状 | 裁决 | 落点 |
|---|---|---|---|
| bible 四件套（world-bible / characters / timeline / plot-board） | 空 | 合并 | `02-设定与一致性.md` 第一节 + `references/02a-bible-guide.md` 原样保留 |
| C1–C10 确定性校验 + 误报边界 | 空 | 合并 | `references/02b-consistency-rules.md` 原样保留 |
| C11 AI 味探测 | 与 cn-craft 量化门禁重叠 | 合并（收敛） | `06-去AI味.md` 第七节（探测→改写→复跑） |
| `consistency_audit.py`（32 KB） | 无脚本 | 合并 | `scripts/` 原样迁入 |
| `build_bible.py` / `wordcount_budget.py` | 无 | 合并 | `scripts/` 原样迁入 |
| 7 个类型深度模板（仙侠/科幻/言情/悬疑/历史/奇幻/游戏） | 空 | 合并 | `references/genres/` + `templates/` 原样保留 |
| bible 模板 12 份 | 空 | 合并 | `templates/` 原样保留 |
| 三国示例（建库→写→审计闭环） | 空 | 合并 | `examples/` 原样保留 |
| 输出契约 B1–B5（不拟人/不编造标准/以 bible 为准/不越权代决策；原"不违规"项已废止） | 空 | 合并 | `SKILL.md` 三条质量红线 + `10-content-safety.md`（2026-11 改版为零拦截创作尺度立场：版权忽略、内容不设限） |

### 2.3 novel-outline → 合并（大纲权威）

| 外部精华 | 本地现状 | 裁决 | 落点 |
|---|---|---|---|
| 六层大纲模型 | 空 | 合并 | `03-大纲工程.md` 第一节 |
| 七步作业 + 每步判据模板 | 空 | 合并 | `03-大纲工程.md` 第二节 |
| 读者承诺类型六分类 | 空 | 合并 | `03-大纲工程.md` 第 1 步 |
| 升级路径四选一 | 空 | 合并 | `03-大纲工程.md` 第 3 步 |
| 钩子＝问题＋选择（否定环境信号） | tomato 有钩子但无此判据 | **合并**（本地无同义判据） | `03-大纲工程.md` 第 7 步 |
| 双份交付（人读版 + AI 辅助生成版） | 空 | 合并 | `03-大纲工程.md` 第七节 |

### 2.4 conflict-max-web-fiction → 合并（续写分支权威）

| 外部精华 | 本地现状 | 裁决 | 落点 |
|---|---|---|---|
| 冲突核四问 | 空 | 合并 | `04-正文技法.md` 第一节 |
| 场景五步因果链 | 空 | 合并 | `04-正文技法.md` 第一节 |
| 情绪五段（刺激—反应—克制—选择—余波） | cn-craft 有情绪外化但无完整链路 | 合并 | `04-正文技法.md` 第二节 |
| 四类冲突叠加（事件/关系/价值/内心） | 空 | 合并 | `04-正文技法.md` 第一节 |
| 五分支路由（完整短篇/连载章节/续写/局部改写/大纲） | 空 | 合并 | `05a`/`05b` 续写与同人 第一节 |
| **续写：承接最后一个有效状态、匹配视角时态声音** | 空 | **合并（关键）** | `05a`/`05b` 续写与同人 第三节 |
| 局部改写：只重写指定范围，不扩展成整章 | 空 | 合并 | `05a`/`05b` 续写与同人 第四节 |
| 题材适配四类（言情/复仇/悬疑/玄幻） | nwa genres 更细 | 保留本地（nwa 更强） | `references/genres/` |

### 2.5 human-writing → 合并（拆两半）

| 外部精华 | 本地现状 | 裁决 | 落点 |
|---|---|---|---|
| 材料论（虚构/现实/混合三分） | 空 | 合并 | `09-活人感文风.md` 第二节 |
| 说话位置五问 | 空 | 合并 | `09-活人感文风.md` 第三节 |
| 现代白话散文默认写法 13 条 | 空 | 合并 | `09-活人感文风.md` 第四节 |
| 论坛服装警告（假细节越具体 AI 味越重） | 空 | 合并 | `09-活人感文风.md` 第五节 |
| 成稿硬禁令（冒号/破折号/翻案句） | 空 | 合并 | `06-去AI味.md` 第六节 |
| 规则冲突优先级五级 | 空 | 合并 | `09-活人感文风.md` 第六节 |
| `check_prose.py` | 无脚本 | 合并 | `scripts/` 原样迁入 |
| 非虚构四份（forum-prose/reality/formats/revision） | 空 | 合并 | `references/09-*.md` 原样保留 |
| 「不创建作者画像/个人规则库」 | 空 | 合并 | `09-活人感文风.md` 第九节 |

### 2.6 tomato-palace-master → 降级保留

| 外部精华 | 本地现状 | 裁决 | 落点 |
|---|---|---|---|
| 开篇工程四窗口 | 空 | 合并 | `08-平台运营.md` 第四节 + `platform/opening-engineering-2026.md` |
| 黄金三章工程 | 空 | 合并 | `platform/golden-three-chapters.md` |
| 六层流量池与考核指标 | 空 | 合并 | `platform/traffic-pool-and-diagnosis.md` |
| 数据诊断（先修最前端） | 空 | 合并 | `08-平台运营.md` 第三节 + `data_diagnosis.py` |
| 书测套餐 / 断流急救 / 切书模型 | 空 | 合并 | `platform/book-test-and-crisis-rescue.md` + `book_test_gen.py` |
| 短剧改编 10 维评估 | 空 | 合并 | `platform/short-drama-adaptation.md` |
| 书名简介标签 | 空 | 合并 | `platform/title-blurb-tags.md` |
| 平台机制 / 福利变现 / 读者画像 | 空 | 合并 | `platform/` 全套保留 |
| 8 个脚本 | 无 | 合并 | `scripts/`（7 个迁入，`monthly_evolution.py` 拒绝） |

### 2.7 story-import → 合并（被上游超越）

| 外部精华 | 本地现状 | 裁决 | 落点 |
|---|---|---|---|
| 4 步导入流程 | 空 | 合并（但被 MuMuAINovel 6 阶段超越） | `01-导入与拆解.md` 第一节 |
| 质量检查三条 | 空 | 合并 | `01-导入与拆解.md` 第一节 |

### 2.8 MuMuAINovel → 部分吸收

| 外部精华 | 本地现状 | 裁决 | 落点 |
|---|---|---|---|
| `story-long-analyze` 6 阶段拆书管道 | story-import 只有 4 步骨架 | **合并（关键）** | `01-导入与拆解.md` 第二节 |
| 深度拆解目录树 | 空 | 合并 | `01-导入与拆解.md` 第二节 |
| 分块策略（按章数三档） | 空 | 合并 | `01-导入与拆解.md` 第二节 |
| 阶段 3 质量门控（置信度/覆盖率/重叠率） | 空 | 合并 | `01-导入与拆解.md` 第二节 |
| `story-deslop` 6 Gate | cn-craft 有 ban 词但无 Gate 结构 | 合并 | `06-去AI味.md` 第三节 |
| 真人写作基准对照表 | 空 | 合并 | `06-去AI味.md` 第二节 |
| 应用本体（FastAPI + React + PostgreSQL） | 不适用 | **拒绝** | 是应用不是 skill，无法作为技能资产 |
| `skill_loader.py` / 前端 / Docker 配置 | 不适用 | **拒绝** | 宿主专属实现 |

---

## 三、明确拒绝清单

| 拒绝项 | 来源 | 理由 |
|---|---|---|
| 「殿堂作家」人格设定与信条话术 | tomato | 人格外壳，非方法论；与「不拟人」输出契约冲突 |
| 「挑战输出上限」「永远给更强的那一版」 | tomato | 增量压力话术，会诱导无节制膨胀 |
| 每月 1 号 00:30 自动进化定时任务 | tomato | 宿主专属机制，且属环境依赖，不可迁移 |
| A/B/C/D 四级情报标注体系 | tomato | 与本地证据标注口径不同，合并会造成双轨 |
| `monthly_evolution.py` | tomato | 依赖上述定时任务机制，脱离即失效 |
| 上游 changelog 文档（14.6 KB） | tomato | 上游版本流水，对使用者无价值 |
| 上游 anti-ai-style 文档（18.7 KB） | tomato | 与收敛后的 `06-去AI味.md` 重复度过高，仅保留「四大死亡气味」 |
| `workbuddy.json` / `_skillhub_meta.json` / `_icon.*` / `LICENSE` | 全部 7 个 | 平台打包元数据，非能力内容 |
| `agents/openai.yaml` | human-writing | 单 agent 专属配置，违反 agent 通用性原则 |
| README / VERSION / SOURCE-ATTRIBUTION | 各源 | 元信息，已在本文件统一登记 |

---

## 四、去重账本

| 重复内容 | 原出现次数 | 收敛后位置 |
|---|---|---|
| AI 味检测与改写 | **5**（human-writing revision、nwa de-ai-flavor、cn-craft 第五节、tomato anti-ai-style、mumu story-deslop） | `06-去AI味.md` 单一权威 |
| 大纲 / 分卷 / 章纲 | 3（novel-outline、tomato long-form、cn-craft 流程） | `03-大纲工程.md` |
| 人设一致性 | 3（nwa bible、cn-craft 人物、tomato character） | `02-设定与一致性.md` |
| 冲突 / 情绪 / 节奏 | 2（conflict-max、tomato plot-rhythm） | `04-正文技法.md` |
| 伏笔管理 | 3（nwa C5、cn-craft 登记册、tomato 伏笔台账） | `02-设定与一致性.md` 第四节 |
| 开篇工程 | 2（tomato 内部两处重复） | `platform/golden-three-chapters.md` + `08` 第四节 |
| 平台规则 | 2（tomato 内部重复） | `platform/` |

---

## 五、净增体积

| 项 | 数值 |
|---|---|
| 7 个源 skill 总体积 | 约 690 KB（含图标 500 KB） |
| 纯文本部分 | 约 190 KB |
| 合并后本技能 | 约 330 KB（其中平台运营 references 约 200 KB 为按需加载） |
| 主流程必需部分 | 约 130 KB |
| 净变化 | 纯文本 **减少约 30%**，且消除了 5 处重复 |

---

## 六、已知缺口（合并时未解决）

| 缺口 | 说明 | 建议 |
|---|---|---|
| 同人 canon 自动化抽取 | `05a`/`05b` 续写与同人 的 canon 六类是人工流程，无脚本 | 后续可基于 `consistency_audit.py` 扩展 |
| 声线卡自动比对 | 靠人工混读验收，无量化指标 | 可考虑加一个句长/词频统计小脚本 |
| 平台数据时效 | 资源库截止 2026-09-11，会过期 | 用 `search_matrix.py` 定期联网校验 |
| 异世界/无限流等新兴赛道 | 类型模板只覆盖 7 类 | 按 `genres/` 的模式新增 |

---

## 七、第二轮吸收：novel-writing-ai-skill-pack-20（2026-11-14）

来源：`novel-writing-ai-skill-pack-20` 的 20 张设计卡（每卡单份 SKILL.md，1069–1423 bytes），全部为「公开开源项目 → 创作流程」的模板化转写，同一骨架：frontmatter / 来源项目 + GitHub 链接 + Star 数 + 许可证 / 适用场景 / 4 步工作流 / 输出 / 3 条逐字相同的边界声明。

模板共性缺陷（不作为吸收内容）：description 结尾重复一次「时使用。」；20 份的 3 条边界声明逐字相同，属模板填充而非卡特有内容。

裁决口径：**只吸收本地没有的具体判据**。整张卡的工作流若本地已有更完整版本，裁决为「保留现状」，不搬运。

### 7.1 合并（8 张卡 → 6 条增量）

| # | 来源卡 | 上游项目（Star / 许可） | 唯一真增量 | 落点 |
|---|---|---|---|---|
| 1 | agent-novel-memory | iLearn-Lab/NovelClaw（350★ / MIT） | 记忆三层分法：硬事实 / 软倾向 / 临时计划，及各层「每章前读什么、每章后写什么」 | `02a-bible-guide.md` 第六节 + `SKILL.md` 记忆分层小节 |
| 2 | bibisco-character-arc | andreafeccomandi/bibisco（762★ / GPL-3.0） | 弧光四要素中的**错误信念**；关系四格（需求/误解/利益冲突/情感债）；**工具人三问自查** | `templates/character-card.md` 弧光四要素 + 人物关系四格表 + 工具人自查 |
| 3 | dramatica-causal-plot | ydsgangge-ux/dramatica-flow（183★） | 伏笔**三点制**（埋设点 / 误导点 / 兑现点）与「误导点必须解释得通但错了」 | `templates/plot-board.md` 误导点登记 |
| 4 | sillytavern-character-roleplay | SillyTavern（31069★ / AGPL-3.0） | 声线卡固定六字段；**三种压力场景测对白**（利益冲突 / 亲密关系 / 信息隐瞒）；偏离回写判断 | `04-正文技法.md` 第五节 |
| 5 | ink-dialogue-scripting | inkle/ink（4871★ / MIT） | knots/stitches 脚本分层；变量只记影响后续文本的状态；路径可达性测试 | `11-互动叙事.md` 第五、六、七节 |
| 6 | twine-branching-plot | klembot/twinejs（2833★ / GPL-3.0） | 先主干后分叉；每个选择必须改变四样之一；回收节点控分支爆炸；节点表导出格式 | `11-互动叙事.md` 第二、三、四节 |
| 7 | koboldai-adventure-mode | KoboldAI-Client（3923★ / AGPL-3.0） | 跑团冒险模式：开局三样 + 每轮三件套 + 状态表 + 保留后果不硬重置 | `11-互动叙事.md` 第八节 |
| 8 | ebook-polish-publish | Sigil（6889★ / GPL-3.0）+ pandoc（GPL-2.0）+ typst（Apache-2.0） | 转档前 10 项清理 + Markdown→中间格式→EPUB/PDF 路线 + 移动端实测验收 | `12-成稿转档与交付.md` 全篇 |

第 5、6、7 三张卡合并为同一份 reference：三者都是互动叙事，拆成三份会立刻产生重复段落（本地已有「一个 reference 一种业务」的组织原则）。

### 7.2 保留现状（12 张卡，本地已有更强版本）

| # | 来源卡 | 本地已有 | 裁决理由 |
|---|---|---|---|
| 9 | ai-native-novel-pipeline | `03-大纲工程.md` 六层 + 七步作业（含「核心承诺」模板「一个【什么人】，因为【什么事】，必须【做到什么】，否则【失去什么】」） | 该卡的「一句话核心承诺」= 本地卖点模板；项目圣经 = `02a`；分章纲 = 本地 L6 层 |
| 10 | ai-story-long-output | `04-正文技法.md` 场景因果链五步；`06-去AI味.md` 全套去套话 | 卡的「拆场景/人物/冲突/氛围」粒度粗于本地冲突核四空 |
| 11 | book-os-context-system | `02a-bible-guide.md` 四件套 + `templates/` 18 份 | 卡的固定目录（brief/characters/world/plot…）本地已覆盖且字段更细 |
| 12 | chinese-webnovel-routine | `08-平台运营.md` + `platform/` 18 份（含 `golden-three-chapters.md`、`opening-engineering-2026.md`） | 卡的「前三章三展示」「3-5 章小兑现」本地有成体系的窗口工程与节奏密度 |
| 13 | kobold-local-fiction | `02a` 第六节（最小上下文纪律）+ `00-workflow.md` | 「跑偏先压缩上下文」已随记忆分层落盘 |
| 14 | local-rag-novel-ide | `02b-consistency-rules.md` C1–C11 + `consistency_audit.py`（32KB 确定性扫描） | 卡的「写完做一致性检查」本地已脚本化，判据更硬 |
| 15 | novelwriter-plain-text-draft | `04-正文技法.md` 章节 spec YAML + `templates/chapter.md` | 卡的「章首写目标/视角/时间/地点」已含在章节模板 |
| 16 | schema-card-novel-forge | `templates/` 18 份卡片模板 | 卡的卡片分类（角色/地点/势力/事件/伏笔/章节）本地已按类型拆分 |
| 17 | single-binary-story-writer | `03-大纲工程.md` 七步作业 + 章纲 | 卡的「12-30 章大纲 + 逐章输入全局设定」= 本地 L5/L6 分层作业 |
| 18 | story-quality-benchmark | `07-质量门禁.md` 16 维审核框架 | 卡的六维评分是本地 16 维的子集 |
| 19 | storycraftr-outline-chapter | `03-大纲工程.md` 七步作业第一步（定卖点）与三套叙事结构 | 卡的「先问 7 个问题」等价于本地立项问询，且本地有评分卡 |
| 20 | webnovel-market-disassembly | `01-导入与拆解.md` 拆文报告 + `08-平台运营.md` 对标 | 卡的「5-10 个对标作品拆解」= 本地拆书管道，本地还带可复用结论模板 |

### 7.3 明确拒绝

| 内容 | 理由 |
|---|---|
| 20 份逐字相同的 3 条边界声明 | 模板填充，无卡特有信息；本地创作立场由 `10-content-safety.md` 统一口径，重复声明会形成门控层叠 |
| description 结尾重复的「时使用。」 | 上游模板缺陷 |
| 整卡 4 步工作流原样搬运 | 本地主流程六阶段已覆盖，搬运会造成第二套流程权威 |

### 7.4 本轮净增与整理

| 项 | 数值 |
|---|---|
| 新增 reference | 2 份（`11-互动叙事.md`、`12-成稿转档与交付.md`） |
| 修改文件 | 4 份（`templates/character-card.md`、`templates/plot-board.md`、`02a-bible-guide.md`、`04-正文技法.md`）+ `SKILL.md` |
| 净增体积 | 约 +13.5 KB（12 号 reference 约 7 KB、11 号约 6.5 KB 为新增；4 份修改文件合计 +约 6 KB） |
| 转档工具依赖 | pandoc / typst / Sigil 均为可选，本机实测全部缺失，已在 `12-成稿转档与交付.md` 第七节登记为降级路径 |
### 7.5 全量来源索引（20 张卡，删除源目录前留档）

上游 sources.json 的机器可读字段（slug / repo / stars / license / focus）在删除安装源前完整留档于此，供日后复核许可与上游演进：

| 来源卡 | 上游仓库 | Star | 许可 | 聚焦 |
|---|---|---|---|---|
| `webnovel-market-disassembly` | worldwonderer/oh-story-claudecode | 4525 | MIT | 网文榜单、爆款结构、题材卖点拆解 |
| `ai-native-novel-pipeline` | ExplosiveCoderflome/AI-Novel-Writing-Assistant | 2092 | NOASSERTION | 从一句灵感到长篇小说的端到端流程 |
| `schema-card-novel-forge` | RhythmicWave/NovelForge | 1040 | AGPL-3.0 | 卡片化创作、结构化 JSON、上下文引用 |
| `chinese-webnovel-routine` | Tomsawyerhu/Chinese-WebNovel-Skill | 517 | NOASSERTION | 中文网文人设、金手指、爽点、节奏 |
| `local-rag-novel-ide` | heider-x/vela | 476 | GPL-3.0 | 本地模型、RAG、隐私优先、长篇一致性 |
| `agent-novel-memory` | iLearn-Lab/NovelClaw | 350 | MIT | 动态记忆、章节规划、长篇连贯 |
| `dramatica-causal-plot` | ydsgangge-ux/dramatica-flow | 183 | NOASSERTION | Dramatica 理论、多线叙事、伏笔追踪 |
| `storycraftr-outline-chapter` | raestrada/storycraftr | 151 | MIT | 故事概念、世界观、章节生成 |
| `book-os-context-system` | forsonny/book-os | 54 | MIT | 小说项目操作系统、上下文文件夹 |
| `single-binary-story-writer` | Nigh/show-me-the-story | 389 | MIT | OpenAI 兼容 API、outline 到逐章写作 |
| `story-quality-benchmark` | EQ-bench/creative-writing-bench | 121 | NOASSERTION | 创意写作评测、文本质量对比 |
| `ai-story-long-output` | datacrystals/AIStoryWriter | 257 | AGPL-3.0 | 长输出、连贯故事、用户提示扩写 |
| `sillytavern-character-roleplay` | SillyTavern/SillyTavern | 31069 | AGPL-3.0 | 角色卡、对话、人设一致性测试 |
| `kobold-local-fiction` | LostRuins/koboldcpp | 11212 | AGPL-3.0 | GGUF 本地模型、KoboldAI UI、零安装续写 |
| `koboldai-adventure-mode` | KoboldAI/KoboldAI-Client | 3923 | AGPL-3.0 | 冒险模式、交互式故事、AI Dungeon 类流程 |
| `novelwriter-plain-text-draft` | vkbo/novelWriter | 3028 | GPL-3.0 | 小说专用纯文本编辑、章节组织 |
| `bibisco-character-arc` | andreafeccomandi/bibisco | 762 | GPL-3.0 | 人物、地点、叙事线、小说结构 |
| `twine-branching-plot` | klembot/twinejs | 2833 | GPL-3.0 | 非线性故事、节点、选择分支 |
| `ink-dialogue-scripting` | inkle/ink | 4871 | MIT | 互动叙事脚本、变量、条件对白 |
| `ebook-polish-publish` | Sigil-Ebook/Sigil + jgm/pandoc + typst/typst | 6889 | GPL-3.0 / GPL-2.0 / Apache-2.0 | 电子书整理、EPUB、Markdown 转换、排版 |

上游 README 给出的 5 组推荐组合（可作为「一个任务该串哪几张卡」的参照）：

| 场景 | 上游推荐组合 | 本地对应 |
|---|---|---|
| 网文开篇 | webnovel-market-disassembly + chinese-webnovel-routine + bibisco-character-arc | `01-导入与拆解.md` + `08-平台运营.md` + `templates/character-card.md` |
| 长篇连载 | ai-native-novel-pipeline + agent-novel-memory + schema-card-novel-forge | `03-大纲工程.md` + `02a-bible-guide.md` 第六节 + `templates/` |
| 世界观设定库 | book-os-context-system + local-rag-novel-ide + schema-card-novel-forge | `02a-bible-guide.md` + `02b-consistency-rules.md` |
| 互动小说 | twine-branching-plot + ink-dialogue-scripting + koboldai-adventure-mode | `11-互动叙事.md`（三者已合并） |
| 完稿交付 | novelwriter-plain-text-draft + story-quality-benchmark + ebook-polish-publish | `07-质量门禁.md` + `12-成稿转档与交付.md` |

**未落盘的源文件**（营销与索引性质，不含创作方法论）：
- README.md（5,036 bytes）：20 张卡的合集说明与安装指引。
- product-copy-cn.md（2,190 bytes）：合集的中文售卖文案。
- sources.json（16,799 bytes）：上述上游字段，内容已全量转录到本节表格。
