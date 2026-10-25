---
schema_version: 1
doc_id: "REVIEW-20261025-01"
doc_type: style_regression
source_ids: []
status: accepted
version: v1.0
current_slice: "SLICE-FRONTEND-VISUAL-DEMO"
updated_at: "2026-10-25 18:50:00"
reader_level: business_general
writing_style: plain_chinese
appendix_policy: preserve_existing_or_one_terminal_appendix
complexity: L1
baseline_commit: 5e290834
template_version: v1
---

# 6-review 风格回归：前端视觉改动对比 Demo 规则落盘

结论：本轮规则资产落盘完成，`STYLE: PASS`。改动集中在两个前端 skill：新建一份权威细则，另两处各加 1 行入口。影响：后续修改已有界面的尺寸、间距、颜色、圆角、阴影、字体、布局、组件外观或动效时，必须先给新旧对比 demo，用户确认后才动生产代码。范围：只核对写法、位置、引用、编码与目录归位。非范围：不判断规则本身好不好用、不判断任何前端页面视觉质量。变化：新建 1 个 reference，修改 2 个 SKILL.md，连带刷新字典产物 2 个。完成标准：六维逐项有磁盘证据，发现项已修复或登记。

## 文档信息

- 来源任务：用户提出"前端改样式、改组件、调 CSS 不能只用文字说明，要给 HTML demo 对比新旧，用户判断更准确"，要求吸收进 skill 体系。
- 回归时间：2026-10-25；执行环境：本机 Git Bash + Windows。
- 图片资产决策：`N/A + 原因 + 证据`。原因：本轮只改规则文档，不产出图片。证据：`git status --porcelain` 无图片路径。
- 数据写入：`N/A`，理由：本轮未向任何数据库、缓存或消息队列写入数据。

## 六维交付残留自查

| 维度 | 结论 | 证据 |
|---|---|---|
| 维度 1 需求覆盖对账 | 通过 | 用户一项诉求拆为四条验收：① 规则要进 skill 体系（不新建独立目录）→ `frontend-design/references/visual-change-demo.md` 全文；② 必须"新旧对比"而非只说改成什么样 → 该文件「二、对比形态四级」`M1`-`M4`；③ 必须"给出 html demo"→ 同节与「六、产物纪律」第 2 档本地单文件 HTML + 可打开绝对路径；④ 必须"然后才继续"→「五、闸门语义」明确 demo 未确认前不得改生产代码。四条均有落点 |
| 维度 2 影响面 / 消费方对账 | 通过 | 本轮唯一契约面是"新增一个 reference 路径 + 两条入口引用"。全仓扫描 `grep -rn "visual-change-demo" --include=*.md --include=*.js .` 命中 4 处（权威文件自身 1、`frontend-design/SKILL.md` 1、`frontend-ui-visual-rules/SKILL.md` 1、字典索引 1），无其它 skill 消费该口径需同步。两条入口均为新增引用，未改名任何既有符号，不存在未处置调用方 |
| 维度 3 残留物清扫 | 通过 | `git status --porcelain` 只有 4 个修改 + 1 个新增，全部是本轮计划内文件，无临时脚本、无 debug 开关、无孤儿文件。本轮未启动任何服务或后台进程，无需进程清理。`.workbuddy/tmp/*.py`（7 个）经 `ls -la` 核实修改时间为 2026-08-23，属历史遗留非本轮产物，不处置 |
| 维度 4 文档与引用一致性 | 通过（曾发现 1 项并已修复） | 发现：`visual-change-demo.md` 原写 `design-review:visual-regression-review` 未标明其为宿主插件 skill，读者按仓库相对路径解析会误判为断链（实测 `ls -d design-review` 返回不存在）→ 已改为显式标注"宿主插件 skill，非本仓库目录"。其余引用双向核对：`frontend-design/SKILL.md:111` → 权威文件（存在）；`frontend-ui-visual-rules/SKILL.md:73` → `frontend-design/references/visual-change-demo.md`（存在）；权威文件引用的 `runtime-process-cleanup-rules`、`frontend-component-rules` 目录均实测存在 |
| 维度 5 口径一致性 | 通过 | 形态编号跨载体比对：权威文件定义 `M1`/`M2`/`M3`/`M4`，`frontend-design/SKILL.md` 引用 `M1`（1 次）与 `M4`（1 次），无未定义编号、无定义未使用。触发面措辞在 SKILL.md 与权威文件逐字相同（"尺寸、间距、颜色、圆角、阴影、字体、布局结构、组件外观或动效参数"全仓命中 1 处定义 + 1 处引用，无第二种表述）。字典计数核对：`references_total` 928 → 929，与实际新增 1 个 reference 一致；`implemented_total` 66 未变（本轮未新增 skill 目录） |
| 维度 6 验证有效性反审 | 通过（曾发现 1 项并已修复） | 反审发现：初跑 `quick_validate.py` 报 `UnicodeDecodeError: 'gbk' codec`，退出码 1，但报错点在脚本自身的 `read_text()` 默认编码，与本轮文件内容无关。若直接按退出码判失败会误判，若肉眼放过又会漏掉真实校验 → 处理方式为设置 `PYTHONUTF8=1` 重跑同一脚本（不改脚本），两次均返回 `Skill is valid!` 退出码 0。独立判据：另用 `file` 命令确认新文件为 `Unicode text, UTF-8 text`，用乱码替换符（U+FFFD）计数命令检查三文件均为 0 命中，与校验结果互证，未用本轮结论自证本轮验证。本轮无生产代码变更，故不适用真实运行测试，理由已在本文件与实施计划中双重记录 |

## 本轮发现项处置

| 发现项 | 处置 | 说明 |
|---|---|---|
| 权威文件把宿主插件 skill 写成疑似仓库相对路径 | 已修复 | 补注"宿主插件 skill，非本仓库目录"，避免读者判为断链 |
| `quick_validate.py` 在 Windows 默认 GBK 解码导致假失败 | 已规避（非本轮引入） | 改用 `PYTHONUTF8=1` 重跑，不改脚本；属 `.system/` 只读资产，不在本轮边界内 |
| `.workbuddy/tmp/` 下 7 个 2026-08-23 历史脚本 | 不处置 | 非本轮产物，修改时间早于本轮两个月，不影响本轮交付 |

## 第二轮增强：demo 必须继承原项目样式

用户追加要求：新旧对比 demo 不能自带一套外观，要与实际项目风格接近。原保真约束只有三条原则性要求（真实 token、真实组件、真实字体），缺可执行的落地路径，现扩充为：

| 新增内容 | 作用 |
|---|---|
| 样式来源优先级五档 | `<link>` 真实构建产物 CSS → `@import` token 源文件 → 挂进项目跑真实组件 → `M3` 真实页面截图 → `getComputedStyle` 抽取兜底；每档给出适用条件 |
| 复用真实 class 名与 DOM 结构 | 从真实页面复制片段，不改名、不简写、不重排 |
| 四条禁止 | 凭记忆写 token 名、肉眼估算色值、默认字体冒充、另起一套 class |
| before 版是校准基准 | before 必须与真实页面并排一致后才交付；before 偏了，after 的判断随之失效 |
| 字体与资源 404 检查 | 引入真实 CSS 后仍需确认字体、图标字体、背景图真的加载 |

同步在 `frontend-design/SKILL.md` 第 2 步闸门条补一句指引（`<link>` / `@import` / 真实 class + before 校准）。
**同域扫描**：`getComputedStyle` 在 `source-notes.md:130` 另有一处，为历史组件修复记录，与 demo 规则无关，不构成第二权威，**PASS**。


## 检查范围与非范围

- 范围：`frontend-design/references/visual-change-demo.md`（新建）、`frontend-design/SKILL.md`（第 2 步 +1 行）、`frontend-ui-visual-rules/SKILL.md`（暂停条件 +1 行），以及连带刷新的 `skill-dictionary/data.js` 与 `字典.md`。
- 非范围：`frontend-design/component-library/` 全部资产、`frontend-component-rules`、宿主 `design-review` 插件均未改动。
- 不判断：规则是否真能在实践中稳定触发（需后续场景实测）、任何前端页面的视觉质量、发布放行。

## 验证记录

| 验证项 | 命令 / 方式 | 结果 |
|---|---|---|
| 结构校验 frontend-design | `PYTHONUTF8=1 python .system/skill-creator/scripts/quick_validate.py frontend-design` | `Skill is valid!`，退出码 0 |
| 结构校验 frontend-ui-visual-rules | 同上，参数换 skill 名 | `Skill is valid!`，退出码 0 |
| 新文件编码 | `file frontend-design/references/visual-change-demo.md` | `Unicode text, UTF-8 text` |
| 三文件乱码自检 | 乱码替换符（U+FFFD）计数命令 | 全部 0 |
| 引用可达 | `test -f` + `grep -c "references/visual-change-demo.md"` | 权威文件存在；两个 SKILL.md 各 1 处引用 |
| 同域去重扫描 | `grep -rln "新旧对比\|visual-change-demo" --include=*.md .` | 命中 4 处，除权威文件外均为引用；`doubao-creative-video` 命中为视频叙事术语，与前端无关 |
| 字典刷新 | `PYTHONUTF8=1 python skill-dictionary/generate_dictionary.py` | 退出码 0；`references_total` 928→929 |
| 变更集核对 | `git status --porcelain` | 4 修改 + 1 新增，等于计划范围 |
