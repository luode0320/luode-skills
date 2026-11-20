# 吸收裁决表（workbuddy-absorption-map）

本表登记本技能每一次外部吸收的裁决结果，供后续追溯、避免重复吸收，并作为「吸收即整理」的自检凭据。逐条来源细节与拒绝理由见 `references/SOURCES.md`。

---

## 一、第二轮吸收：novel-writing-ai-skill-pack-20（2026-11-14）

来源路径：`C:\Users\luode\Downloads\novel-writing-ai-skill-pack-20\skills`（20 个目录 / 20 份 SKILL.md，均为「开源项目 → 创作流程」模板化转写）。

净增减预估：**新增 2 份 reference、修改 4 份 reference + 1 份 SKILL.md；整理去重 6 处**（详见第三节）。

| 日期 | 来源 | 条目 | 本地现状 | 裁决 | agent 通用性 | 环境依赖 | 落点 | 整理去重 |
|---|---|---|---|---|---|---|---|---|
| 2026-11-14 | iLearn-Lab/NovelClaw（350★, MIT） | agent-novel-memory：三层记忆（硬事实 / 软倾向 / 临时计划）与每章前后的读写纪律 | `02a-bible-guide.md` 只有 bible 四件套与维护纪律，无「什么该进 bible」的判据 | 合并 | 通用 | N/A：纯方法论正文，不依赖环境变量、宿主配置或 hook | `references/02a-bible-guide.md` 第六节 + `SKILL.md` 记忆分层小节 | 与 `00-workflow.md` 闭环五步的分工写明：本文管「存什么」，工作流管「哪一步做」 |
| 2026-11-14 | andreafeccomandi/bibisco（762★, GPL-3.0） | bibisco-character-arc：错误信念、关系四格（需求/误解/利益冲突/情感债）、工具人三问 | `templates/character-card.md` 有「弧光」字段但只一层，无错误信念与工具人判据 | 合并 | 通用 | N/A：纯方法论正文 | `templates/character-card.md` 弧光四要素 + 人物关系四格表 + 工具人自查 | 弧光字段升级为四要素，原一句话「弧光」不再重复保留；关系四格与 C8 关系标签口径对齐 |
| 2026-11-14 | ydsgangge-ux/dramatica-flow（183★） | dramatica-causal-plot：伏笔三点制（埋设点 / 误导点 / 兑现点） | 本地伏笔只有 F 行单行登记 + C5 状态枚举，「误导」仅出现在悬疑红鲱鱼语境 | 合并 | 通用 | N/A：纯方法论正文 | `templates/plot-board.md` 误导点登记 | 三点写成 F 行下的缩进子项，不塞进 F 行本体——否则 `consistency_audit.py` 的 C5 正则失配 |
| 2026-11-14 | SillyTavern（31069★, AGPL-3.0） | sillytavern-character-roleplay：声线卡六字段、三种压力场景测对白、偏离回写 | `04-正文技法.md` 第五节只有三型声线表（理性/感性/焦虑），无固定字段与验收手段 | 合并 | 通用 | N/A：纯方法论正文 | `references/04-正文技法.md` 第五节 | 三型表保留为「快速分流」，六字段作为「写死清单」并行，不重复解释声线概念 |
| 2026-11-14 | inkle/ink（4871★, MIT）+ klembot/twinejs（2833★, GPL-3.0）+ KoboldAI-Client（3923★, AGPL-3.0） | 互动叙事三合一：knots/stitches 分层、节点表、选择四要素、回收节点、跑团状态维护 | 全库零命中：无互动叙事能力 | 合并（三卡合一份） | 通用 | N/A：纯方法论正文 | 新建 `references/11-互动叙事.md` | 三卡合并为一份 reference，避免三份互相重复「分支」「选择」「状态」三概念 |
| 2026-11-14 | Sigil（6889★, GPL-3.0）+ pandoc（GPL-2.0）+ typst（Apache-2.0） | ebook-polish-publish：转档前 10 项清理、Markdown→中间格式→EPUB/PDF、移动端实测 | 全库零命中「EPUB」「完稿」；`export_markdown.py` 只到 Markdown 整合稿 | 合并 | 通用 | pandoc / typst / Sigil 均为**可选**，本机实测全部缺失；缺失时只降级交付形态，不阻断 | 新建 `references/12-成稿转档与交付.md` | 转档工具链收敛为一张环境依赖表，命令不重复散落在正文各处 |
| 2026-11-14 | 12 张设计卡（ai-native-novel-pipeline、ai-story-long-output、book-os-context-system、chinese-webnovel-routine、kobold-local-fiction、local-rag-novel-ide、novelwriter-plain-text-draft、schema-card-novel-forge、single-binary-story-writer、story-quality-benchmark、storycraftr-outline-chapter、webnovel-market-disassembly） | 各卡的 4 步工作流与输出模板 | 本地 `03-大纲工程.md` 六层七步、`07-质量门禁.md` 16 维、`02b` C1–C11 + 32KB 扫描脚本、`platform/` 18 份均已更强 | 保留 | 通用 | N/A | 不落盘，逐卡理由登记于 `references/SOURCES.md` 7.2 | 拒绝整卡搬运，避免形成第二套流程权威 |
| 2026-11-14 | 全部 20 张卡 | 3 条逐字相同的边界声明 + description 重复的「时使用。」 | 本地创作立场由 `10-content-safety.md` 统一口径 | 拒绝 | 通用 | N/A | 不落盘 | 20 份同文声明合并成 0 份，消除 20 处门控层叠 |

---

## 二、第一轮吸收（历史，2026-11-07）

7 个已安装写作 skill 与 MuMuAINovel 项目的合并，完整裁决见 `references/SOURCES.md` 第一至六节，此处不重复登记。

---

## 三、同域冗余扫描（2026-11-14）

扫描范围：`xiaoshuo/` 全目录（`SKILL.md`、`references/` 22+2 份、`references/genres/` 8 份、`references/platform/` 18 份、`templates/` 18 份、`scripts/` 11 份）。

| 检查项 | 发现 | 处理 |
|---|---|---|
| 重复段落 | 新增的「记忆分层」与 `00-workflow.md` 的闭环五步存在概念邻近；「声线六字段」与三型表存在概念重叠 | 均按「一个概念一个权威」处理：记忆分层判据只在 `02a` 第六节展开，工作流只保留指向；三型表保留快速分流用途、六字段为写死清单，判据只写一次 |
| 门控概念层叠 | 20 张卡各带 3 条相同边界声明；两张互动叙事卡各带一遍「变量只记状态」 | 边界声明全部拒绝；互动叙事三卡合并为一份 reference，变量纪律只写一次 |
| 散落产物 | 无新增脚本、无临时文件、无 `(1)` 副本 | 无 |
| 引用链 | `SKILL.md` 新增 2 条路由指向 `11-互动叙事.md`、`12-成稿转档与交付.md`；两份新 reference 均只被 `SKILL.md` 引用，内部无互引需求 | 断链 0；孤儿 0（两份新文件都在路由表内） |
| 权威冲突 | `12-成稿转档与交付.md` 的清理项与 `07-质量门禁.md` 交稿前清单局部邻近 | 分工写明：`07` 管「正文质量是否达标」，`12` 管「格式是否可转档」；`12` 开头声明「转档工具原样放大格式问题，先清稿再转档」 |

结论：**PASS**。发现概念邻近 3 处，均已收敛为单一权威 + 指向，无重复正文。

---

## 四、环境依赖登记

| 依赖 | 归属 | 必需性 | 自检能力 |
|---|---|---|---|
| Python 3（标准库） | `scripts/` 全部 11 个脚本 | 必需 | 脚本纯标准库、确定性、可复跑；`--help` 可自检 |
| pandoc | `12-成稿转档与交付.md` 第四节 | 可选 | 缺失时降级为「交付 Markdown 整合稿 + 附转档命令」 |
| typst | `12-成稿转档与交付.md` 第四节 | 可选 | 同上 |
| Sigil | `12-成稿转档与交付.md` 第五节 | 可选 | 缺失时按清单人工核对 EPUB 内部结构 |

本技能不依赖任何宿主专属路径、环境变量或 hook。

---

## 五、源删除记录

| 项 | 内容 |
|---|---|
| 删除对象 | `C:\Users\luode\Downloads\novel-writing-ai-skill-pack-20`（顶层 3 份 md/json + `skills\` 20 个目录） |
| 删除前规模 | 23 个文件 / 47,934 bytes；21 个目录 |
| 承接核对 | 20 份 SKILL.md 全文已在裁决前逐份读取并按 7.1 / 7.2 裁决（8 张合并、12 张保留现状）；`sources.json` 的 slug / repo / stars / license / focus 全量转录到 `references/SOURCES.md` 7.5；`README.md` 的 5 组推荐组合转录到 7.5 组合表 |
| 未落盘 | `README.md`（5,036 bytes，安装指引与目录清单，信息已入 7.5）、`product-copy-cn.md`（2,190 bytes，中文售卖文案，无方法论）、`sources.json`（16,799 bytes，字段已转录） |
| 删除后核验 | `Test-Path` 返回 **False**，实测已不存在 |

---

## 六、八维评分（2026-11-14，打分人：独立子 agent，未参与编写）

| 维度 | 权重 | 得分 | 理由 |
|---|---|---|---|
| 1 Frontmatter 质量 | 8 | 8 | description 覆盖全链路与触发词；`_zh`/`_en` 三份语义重复 |
| 2 工作流清晰度 | 15 | 7 | 六阶段 + 闭环五步清晰；`00-workflow.md` 四处断链（已修） |
| 3 边界条件覆盖 | 10 | 8 | 三条红线、6 行格式红线表、C1–C11 误报边界、WARN 需人工确认 |
| 4 检查点设计 | 7 | 5 | 主流程自动闭环，无「关键决策前停下等确认」机制 |
| 5 指令具体性 | 15 | 8 | 裸标签 ≤30%、单段 ≤5 行、对话占比 30–45%、前 300 字出钩子等硬数字 |
| 6 资源整合度 | 5 | 7 | 11 脚本 10 个跑通，闭环成立；评分时有 4+1 处断链与 `data_diagnosis.py` 崩栈 |
| 7 整体架构 | 15 | 7 | 分层合理有溯源；8 份文件挤在 `09` 前缀下语义各异 |
| 8 实测表现 | 25 | 8 | 实跑脚本均正常产出，可验证性显著强于纯文本自检 |

**总分 74.4 / 100**。短板 gap：实测表现 5.0、工作流清晰度 4.5、整体架构 4.5。

## 七、评分后补强（2026-11-14）

| 项 | 内容 | 涉及文件 |
|---|---|---|
| 修断链（评分第 1 项） | `planning-guide.md` → `03-大纲工程.md`；`writing-guide.md` → `04-正文技法.md`；`consistency-rules.md` → `02b-consistency-rules.md`；`de-ai-flavor.md` → `06-去AI味.md` | `references/00-workflow.md` |
| 修示例路径失真 | 原文写 `examples/sanguo-demo/`，实际 `examples/` 是平铺文件（前缀 `bible-*` / `ms-第N章_*` / `deai-*`）；改为按前缀改名归位的说明 | `references/00-workflow.md` |
| 修脚本崩栈 | `data_diagnosis.py` 的 `ask_interactive()` 在无终端/管道下 `input()` 抛 `EOFError` 直接 traceback；包 `try/except (EOFError, KeyboardInterrupt)` 并打印中断提示，由既有 `main()` 空数据分支收口。实测空 stdin 不再 traceback，`--input` 与 `--json` 正常 | `scripts/data_diagnosis.py` |
| 清理散落产物 | 删除 `scripts/__pycache__`（2 个 pyc）与 `skill-dictionary/__pycache__`（1 个 pyc） | 目录清理 |
| 全量 BOM 复扫 | 两 skill 所有 `*.md/*.py/*.yaml` 均无 BOM | — |

## 八、第二轮复评（2026-11-14，打分人：另一个独立子 agent，未参与编写与首轮评分）

| 维度 | 权重 | 首评 | 复评 | 复评理由 |
|---|---|---|---|---|
| 1 Frontmatter 质量 | 8 | 8 | 8 | description 三段语义重复，未因补强而改善（也不该靠补强改善） |
| 2 工作流清晰度 | 15 | 7 | 8 | `00-workflow.md` 四处断链已修，示例路径改为可执行的归位说明 |
| 3 边界条件覆盖 | 10 | 8 | 9 | 新增「第七节 三个脚本各管一段」明确了口径冲突的裁决顺序 |
| 4 检查点设计 | 7 | 5 | 7 | 交稿前清单从 9 条扩到 10 条并改成可判定项（脚本退出码 / 分数阈值） |
| 5 指令具体性 | 15 | 8 | 9 | 三条命令的 CLI 签名实测校正（`check_prose.py` 只吃单文件） |
| 6 资源整合度 | 5 | 7 | 6 | 复评扣分点：`templates/` 6 份、`web-search-protocol.md`、`genres/` 8 份从 SKILL.md BFS 不可达 |
| 7 整体架构 | 15 | 7 | 8 | 新增两节 reference 但未打破原有分层 |
| 8 实测表现 | 25 | 8 | 8 | 11 脚本 `--help` 全 0；但复评发现两脚本结论互相矛盾且 examples 不自洽 |

**总分 80.8 / 100**（首评 74.4，+6.4）。短板 gap：实测表现 5.0 ＞ 工作流清晰度 3.0 ＝ 整体架构 3.0 ＞ 检查点 2.1。

**复评指出的两条最该补**：① `check_prose.py` 对 `examples/` 内章节判 EXIT=1（中文冒号 3 处、破折号 2 处）而 `tomato_audit.py` 判 90.2/100「殿堂级可交付」，两者矛盾；② `scripts/export_markdown.py:148` 印不存在的 `monthly_evolution.py`。

## 九、复评后补强（2026-11-14）

| 项 | 问题 | 改法 | 涉及文件 |
|---|---|---|---|
| 示例不自洽（最该补 ①） | 5 份正文稿件含中文冒号/破折号，`check_prose.py` 全判 EXIT=1，与 `tomato_audit.py` 的「殿堂级」结论冲突 | 逐句改掉硬禁令：`ms-第1章` 3 处冒号+2 处破折号、`ms-第2章` 3 冒号+2 破折号、`ms-第3章` 1 冒号、`deai-after-第1章` 2 冒号。改后这 4 份全部 EXIT=0；`deai-before-*` 保留冒号/破折号作反例（EXIT=1 属设计如此，已在 `deai-README.md` 注明） | `examples/ms-第1章_穰县醒.md`、`examples/ms-第2章_智退追兵.md`、`examples/ms-第3章_北望许昌.md`、`examples/deai-after-第1章_穰县醒_定稿.md` |
| 幽灵脚本名（最该补 ②） | `export_markdown.py` 的交付说明模板印 `python scripts/monthly_evolution.py --check`，该脚本不存在 | 改为 `python scripts/search_matrix.py --wave 1` + 指向 `references/platform/web-search-protocol.md` | `scripts/export_markdown.py:148` |
| 破折号三重计数（新发现） | `tomato_audit.py` 的 `dash_count = text.count("——") + text.count("—")` 把每个 `——` 算 3 次（`——` 命中 1 次 + `—` 命中 2 次），实测 `甲乙——丙丁—戊` 计 4 而实际 2 处，导致阈值判定系统性偏严 | 改为 `len(re.findall(r"—+", text))`，连续破折号算一处 | `scripts/tomato_audit.py:186` |
| 评分口径冲突（结构性） | 第五节量化门禁写「破折号 ≤12 处/章」，第六节成稿硬禁令写「不用破折号」，两处对同一项给出不同强度 | 第五节加注说明「本节是体检扣分线，第六节是交付硬线，冲突以第六节为准」 | `references/06-去AI味.md` |
| 质量清单口径错配 | `07-质量门禁.md` 交稿前清单写「跑过 `tomato_audit.py` 且 P0 清零」，但 `tomato_audit.py` 只输出分数与扣分项、**不产生 P0/P1/P2 分级** | 清单改为「`consistency_audit.py` ERROR 清零 / `check_prose.py` 退出码 0 / `tomato_audit.py` 综合分 ≥90」；新增第八节「三个脚本各管一段，不许互相代替」 | `references/07-质量门禁.md` |
| 示例 README 命令不可跑 | `sanguo-README.md` 与 `deai-README.md` 里的 `examples/sanguo-demo/` 路径不存在，且用 bash 语法而本机是 PowerShell | 改为可直接粘贴的 PowerShell 归位脚本（把平铺示例复制成 `bible/` + `manuscript/` 两棵树），并新增「前缀 → 归位路径」映射表；标注「整个 `examples/` 直接当 `--ms` 会多出十几条 C11 WARN」 | `examples/sanguo-README.md`、`examples/deai-README.md` |
| 脚本内旧名残留 | `consistency_audit.py` 三处印 `references/de-ai-flavor.md`（文件已改名） | 全部改为 `references/06-去AI味.md`（L581 / L606 / L638） | `scripts/consistency_audit.py` |
| 实测验证 | 按 `sanguo-README.md` §2 命令逐行执行 → `consistency_audit.py` 输出 **ERROR 0 / WARN 3**（3 条全 C5 伏笔未回收），与文档声称一致；按 `deai-README.md` 命令执行 → before **ERROR 0 / WARN 7**、after **ERROR 0 / WARN 0**；5 份稿件 `check_prose.py` 复跑 4 通过 1 故意失败；两脚本 `py_compile` 通过；临时目录全部清理（`Test-Path` False） | — | — |
