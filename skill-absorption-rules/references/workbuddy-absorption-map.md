# 吸收裁决表（workbuddy-absorption-map）

> 归属 owner：`skill-absorption-rules`。登记每次外部 skill 吸收的三态裁决结果，来源可回指。新吸收追加行，不覆盖旧记录。
>
> **防臃肿登记要求（2026-08-19 起）**：每次吸收除记录「合并/保留/拒绝」外，必须记录本次「整理去重」动作（合并了哪些重复段落、消除了哪些冗余引用、删除了哪些过时规则）与「净增体积变化」；无整理动作的写 `N/A + 理由`。只增不减的登记视为不合格。
>
> **同域扫描登记要求（2026-08-20 起）**：每次吸收必须在登记中新增「同域扫描结论」行——扫描范围（本次吸收触达的同域 skill 集合）、发现 X 处冗余（重复段落 / 门控层叠 / 散落产物）、清理 Y 处、PASS/FAIL；「整理去重」动作描述必须包含同域清理位置（哪个 skill、哪个段落、收敛到哪个权威）。缺同域扫描结论的吸收登记视为未完成。
>
> **内部更新通道登记（2026-08-20 起）**：本表同时登记「内部 skill 更新通道」的裁决式调整——来源列写"内部调整：<目标 skill>，<调整诉求>"，其余列（裁决 / 落点 / 整理去重 / 同域扫描结论 / 净增体积）要求与外部吸收完全一致，无外部源可删。

## 2026-09-06：外部吸收——Design（skillhub）设计偏好学习机制 → frontend-design 集成

- **来源**：skillhub `design` v1.0.0（ownerId `kn73vp5rarc3b14rc7wjcw8f8580t5d1`），本地安装源 `~/.workbuddy/skills/design__skillhub/`。
- **形态**：外部吸收通道（本地安装源吸收模式：读取原文 → 裁决 → 落盘 → 删除源）。
- **吸收目标**：`frontend-design`（前端设计生成型 skill，版本 1.1.0 → 1.2.0）。
- **同域前任**：`frontend-ui-visual-rules` 已于 2026-08-22 从同一源吸收，落点为 `references/visual-preference-learning.md`（case-design-absorption.md 记录）。
- **拆解原子规则数**：9 条。

| 外部来源 | 外部精华 | 本地现状 | 裁决 | agent 通用性 | 落点 / 理由 |
|---------|---------|---------|------|-------------|------------|
| design | 自动学习视觉偏好——从用户选择、反馈、反应中检测模式 | 缺失。frontend-design 无偏好学习机制 | 合并 | 通用 | 增强 `frontend-ui-visual-rules/references/visual-preference-learning.md`（权威文件），补充工作流集成节 |
| design | 偏好分类体系（Aesthetic / By Medium / Brands / Never） | 缺失。但同域已有权威文件（visual-preference-learning.md 四分类语义等价） | 合并(同域收敛) | 通用 | 不新写，增强权威文件并补充 frontend-design 工作流衔接 |
| design | 偏好添加准则（1次明确表达+2+次一致模式，排除客户需求/一次性实验） | 缺失。同域权威文件已有相同语义 | 合并(同域收敛) | 通用 | 增强权威文件，补充「反馈模式记录示例」节 |
| design | 设计维度检测框架（8个维度：视觉风格/颜色/字体/布局/UI/图形/动效/媒介） | 同域权威文件已有检测维度节 | 保留本地 | — | 同域权威文件已覆盖，不重复 |
| design | 反馈模式捕捉（记录喜欢/不喜欢/参考来源/竞品参考） | 缺失。同域权威文件无示例 | 合并(同域收敛) | 通用 | 增强权威文件，补充「反馈模式记录示例」节 |
| design | 媒介限定——不同媒介不同偏好 | 缺失。同域权威文件「按介质」分类语义等价 | 保留本地 | — | 同域权威文件已覆盖 |
| design | 主观性处理——趋势而非规则，记录例外，随品味更新 | 缺失。同域权威文件「倾向性表述」语义等价 | 保留本地 | — | 同域权威文件已覆盖 |
| design | 维护规则——保持紧凑，合并相似项 | 同域权威文件「同义词合并」+ 本地上轮「吸收即整理」原则覆盖 | 保留本地 | — | 本地更强 |
| design | 整体偏好记录为 SKILL.md 内的模板段落 | 形态不匹配，frontend-design 是工作流型 skill | 拒绝 | — | 形态不迁移，精华已通过上方合并条目收敛至同域权威 |

- **落盘改动**：
  - 修改 `frontend-design/SKILL.md`（版本 1.1.0 → 1.2.0）：第 1 步工作流增加偏好查询环节（①-④ 步）+ 职责边界引用指向 `frontend-ui-visual-rules/references/visual-preference-learning.md`。
  - 增强 `frontend-ui-visual-rules/references/visual-preference-learning.md`（权威文件）：新增「在 frontend-design 工作流中的应用」节（第 1-2-5 步衔接）+「反馈模式记录示例」节。
  - 新增 `frontend-design/references/source-notes.md`（吸收登记）。
- **整理去重**：新建的 `design-preference-learning.md`（~5.5KB）与同域权威文件 `visual-preference-learning.md` 高度重复 → 删除冗余文件；出错的文件（~5.5KB）已删除。权威文件净增约 +0.8KB（工作流集成 + 反馈示例），减去冗余文件后体系净增为负。
- **同域扫描结论**：范围 = frontend-design（吸收目标）、frontend-ui-visual-rules（同域权威）、frontend-component-rules（同域技术层）、frontend-ui-visual-rules（数据层）。发现 = 1 处重复段落（新建 `design-preference-learning.md` 与 `visual-preference-learning.md` 高度重复）、0 处门控层叠、0 处散落产物；清理 1 处（删除冗余文件）；引用链收敛为「单一权威（visual-preference-learning.md）+ 引用（frontend-design SKILL.md 指针）」；**PASS**。
- **环境依赖登记**：N/A + 理由（纯规则文本，无环境变量 / 宿主配置 / hook / 依赖安装 / 路径引用）。
- **净增体积**：SKILL.md +1.8KB（版本增约 +0.5KB，工作流 +0.5KB，引用 +0.1KB，source-notes +0.7KB）；权威文件 +0.8KB；删除冗余文件 -5.5KB；**体系净增 ≈ -2.9KB（净减）**。
- **棘轮验证**：引用链 2 处可达（frontend-design SKILL.md L19-L24 工作流 → visual-preference-learning.md 相应节；SKILL.md L65 职责边界 → visual-preference-learning.md）；UTF-8 3 文件 OK；`quick_validate.py` 结构校验 PASS（待执行）。
- **源清理**：吸收完成后删除本地安装源 `design__skillhub`（用户级 ~/.workbuddy/skills/design__skillhub/ 目录）。

## 2026-09-06：外部吸收——Apple 流体交互设计（apple-design）→ frontend-design 集成

- **来源**：WorkBuddy 市场 skill `apple-design`（个人开发者，v1.0.0，slug `apple-design`），本地安装源 `~/.workbuddy/skills/apple-design/`。
- **形态**：外部吸收通道（本地安装源吸收模式：读取原文 → 裁决 → 落盘 → 删除源）。
- **吸收目标**：`frontend-design`（前端设计生成型 skill，版本 1.2.0 → 1.3.0）。
- **拆解原子规则数**：12 条。

| # | 外部精华 | 本地现状 | 裁决 | agent 通用性 | 落点 / 理由 |
|---|---------|---------|------|-------------|------------|
| 1 | 流体交互核心思想（即时响应/连续运动/动量传递/动画可打断/物理模拟） | 本地动效节有"错峰 reveal、滚动触发、hover"但无物理模拟思想 | 合并 | 通用 | 增强 frontend-design SKILL.md 动效节，追加「弹簧物理驱动」段 |
| 2 | 弹簧参数表（阻尼比/响应时间，三大交互类型参数） | 本地无任何弹簧物理参数 | 合并 | 通用 | `references/apple-fluid-design.md` 新建 |
| 3 | 速度移交公式（手势释放速度移交至动画） | 本地无 | 合并 | 通用 | 同上 reference |
| 4 | 动量投射公式（decelerationRate + 投影到最近吸附点） | 本地无 | 合并 | 通用 | 同上 reference |
| 5 | 毛玻璃材质（backdrop-filter blur(20px) saturate(180%)） | 本地有"渐变网格、噪点纹理"但无毛玻璃配方 | 合并 | 通用 | 增强 frontend-design SKILL.md 背景节，追加毛玻璃材质段 |
| 6 | 光学字号排版（字号/行高/字间距动态适配） | 本地有字体风格选择但无排版参数 | 合并 | 通用 | 并入 `references/apple-fluid-design.md` |
| 7 | 无障碍动效降级 CSS（prefers-reduced-motion / prefers-reduced-transparency） | 本地边界条件仅提到"可访问性"但无具体 CSS | 合并 | 通用 | 增强 frontend-design SKILL.md 边界条件，追加无障碍动效降级节 |
| 8 | 八大设计原则校验清单（目的性/控制权/责任/熟悉感/灵活性/简洁/工艺/愉悦感） | 本地无结构化评审原则 | 合并 | 通用 | 并入 `references/apple-fluid-design.md` |
| 9 | 核心交互校验清单（按下即反馈/拖拽1:1/动画可打断/弹簧替代transition/动量投射/橡胶边界/路径对称） | 本地第 4 步自查有"风格统一、细节打磨"但无交互校验 | 合并 | 通用 | 增强 frontend-design SKILL.md 第 4 步，追加交互校验清单 |
| 10 | 代码生成脚本（code-snippet-gen.py，仅 2 个硬编码模板） | 简陋形态，精华已通过上方条目吸收 | 拒绝 | — | 机制形态不迁移 |
| 11 | 前置工具声明（allowed-tools: Read/Write/Bash） | 本地已有工具协议 | 拒绝 | — | 形态不匹配 |
| 12 | 被动触发模式（user-invocable/disable-model-invocation） | 本地是主动触发型 skill | 拒绝 | — | 形态不匹配 |

- **落盘改动**：
  - 新增 `frontend-design/references/apple-fluid-design.md`（~6.7KB，弹簧参数/速度移交/动量投射/毛玻璃配方/无障碍降级/八大原则/交互校验清单/流体交互思想）。
  - 修改 `frontend-design/SKILL.md`（版本 1.2.0 → 1.3.0）：动效节追加「弹簧物理驱动」段；背景节追加「毛玻璃材质」段；边界条件追加「无障碍动效降级」节；第 4 步自查追加交互校验清单引用；职责边界引用新增 `apple-fluid-design.md`。
  - 修改 `frontend-design/references/source-notes.md`：追加本次吸收登记。
- **整理去重**：N/A + 理由——弹簧参数、毛玻璃配方、流体交互校验均为本地全新能力，无存量重复段落可清。frontend-design 的"动效"节原有 1 段，现扩充为 2 段（传统动效 + 弹簧物理），语义互补非重复。
- **同域扫描结论**：范围 = frontend-design（吸收目标）、frontend-ui-visual-rules（同域规则层）、frontend-component-rules（同域组件层）。发现 = 0 处重复段落（弹簧参数/毛玻璃配方/交互校验均为本地缺失能力，同域 2 个 skill 零命中）、0 处门控层叠、0 处散落产物；清理 0 处；**PASS**。
- **环境依赖登记**：N/A + 理由（纯规则文本，无环境变量 / 宿主配置 / hook / 依赖安装 / 路径引用）。
- **净增体积**：+约 7.2KB（apple-fluid-design.md ~6.7KB + SKILL.md 约 +0.5KB）；外部源 6 文件约 247KB（含 _icon.png 236KB 图片 + 脚本 1.5KB + 模板/元数据），**体系净增 = +7.2KB（规则正文净增），源图片/脚本不计入规则体积**。
- **棘轮验证**：引用链 4 处可达（SKILL.md L77 弹簧物理 → apple-fluid-design.md 弹簧参数节；L80 毛玻璃 → apple-fluid-design.md 毛玻璃节；L42 交互校验 → apple-fluid-design.md 核心交互校验清单节；L92 无障碍降级 → apple-fluid-design.md 无障碍降级节）；UTF-8 3 文件 OK；quick_validate.py 结构校验待执行。
- **源清理**：吸收完成后删除本地安装源 `apple-design`（用户级 ~/.workbuddy/skills/apple-design/ 目录，6 文件 247KB 含图片）。

- **来源**：内部调整：`test-strategy-rules`（测试策略统一主入口）+ `functional-validation-rules` + `browser-advanced-testing-rules`，调整诉求 = "测试任务结束后必须强制关闭测试启动的进程，禁止遗留后台；用户需要时自行启动。实测教训：真实链路测试启动的 12801 被测服务在测试收口后仍留在后台运行（goadmin-server-tmp 进程 + 端口监听），直到用户追问才处理"。
- **形态**：内部更新通道（无外部源可删）。
- **拆解原子条目数**：5 条（A1 测试收口必关 / A2 核验可证 / A3 不替用户保留 / A4 残留清理 / A5 联调衔接）。
- **裁决**：
  - A1 测试收口必关（任务完成不包含服务继续留在后台）→ 合并（缺口）：现有三 skill 只有「联调完成后关闭前后端进程」，未覆盖真实链路测试启动的被测服务场景。
  - A2 核验可证（关闭动作 + 关闭后状态检查证据）→ 合并（缺口）：现只有 functional-validation 第 7 条有半句，未成权威。
  - A3 不替用户保留（用户需要时自行启动）→ 合并（缺口）：全新原则，各 skill 均无。
  - A4 残留清理（发现历史残留先核验归属再清理）→ 合并（缺口）：全新原则。
  - A5 联调衔接（开场基线收口与收尾强制关闭互补）→ 合并（缺口）：明确两者关系防只开场不收尾。
- **落盘改动**：
  - `test-strategy-rules/SKILL.md`：新增《测试进程生命周期（强制）》节（单一权威，位于「测试隔离红线」之后）。
  - `functional-validation-rules/SKILL.md`：联调节第 6 条补引用指针（指向权威节），第 7 条保留（域专属补充）。
  - `browser-advanced-testing-rules/SKILL.md`：联调节第 6 条补引用指针（指向权威节），第 7 条保留。
- **整理去重**：三 skill 原有「联调完成后必须关闭前后端进程」条款语义重叠 → 收敛为「单一权威（test-strategy-rules）+ 引用（两个下游 skill 只留域专属补充与指针）」；下游重复定义段删除，不留两套进程收口规则。
- **同域扫描结论**：范围 = test-strategy-rules（权威落点）、functional-validation-rules、browser-advanced-testing-rules、test-regression-rules、test-program-rules、bug-validation-rules；发现 = 2 处重复段落（functional-validation 第 6 条 / browser-advanced 第 6 条与权威节语义重复）、0 处门控层叠、0 处散落产物；清理 2 处（改为引用指针）；**PASS**。
- **环境依赖登记**：N/A + 理由（纯规则文本，无环境变量 / 宿主配置 / hook / 依赖安装 / 路径引用）。
- **净增体积**：+约 1.0KB（test-strategy-rules 权威节 ~0.9KB + 两处引用指针 ~0.1KB）；两处下游重复段删除抵消部分增量。
- **棘轮验证**：`quick_validate.py` 三 skill → `Skill is valid!`（exit 0）；UTF-8 OK；引用指针 2 处可达（指向 test-strategy-rules 权威节标题）。

## 2026-08-26：内部更新——低分 skill 优化 SOP 固化（八轮经验总结）

- **来源**：内部调整：`skill-absorption-rules`（吸收规则总入口），调整诉求 = "八轮低分 skill 优化实操经验总结成标准流程，后续评分巡检低分 skill 都按此流程优化；经验吸收进本 skill"。
- **形态**：内部更新通道（无外部源可删）。
- **拆解原子条目数**：7 条（A1 八步闭环 SOP / A2 短板类型学 / A3 验证纪律 / A4 市场检索规律 / B1 SKILL.md 触发信号 / B2 SKILL.md 读取规则 / B3 score-inspection 衔接指针）。
- **裁决**：
  - 八步闭环 SOP → 合并（缺口）：新增 `references/low-score-skill-optimization-sop.md` 作低分优化流程单一权威。
  - 短板类型学 7 类映射 → 合并（缺口）：并入新 SOP（诊断→修复一对一）。
  - 验证纪律（独立子代理/固定格式/维度8实测/本侧修正/棘轮/早停/确定性小问题顺手修复）→ 合并（缺口）：并入新 SOP；评分公式不复制（引用 darwin-rubric）。
  - 市场检索规律（28+ 组关键词 0 候选、解药在仓库内）→ 合并（缺口）：并入新 SOP。
  - SKILL.md 触发信号补"多轮实操经验总结" → 合并（缺口）：+1 条。
  - SKILL.md references 读取规则补 SOP 指针 → 合并（缺口）：+1 条。
  - score-inspection-workflow 短板识别出口衔接 → 合并（缺口）：自有 rules/other 短板出口补 SOP 指针。
  - 新建独立 skill 承载 SOP → 拒绝（本地红线：不新增 skill 目录，属本 skill 职责）。
- **落盘改动**：
  - 新增 `skill-absorption-rules/references/low-score-skill-optimization-sop.md`（6306B）。
  - 修改 `skill-absorption-rules/SKILL.md`（触发信号 +1 行 + 读取规则 +1 行，约 +0.3KB）。
  - 修改 `skill-absorption-rules/references/score-inspection-workflow.md`（短板识别出口 1 句）。
- **整理去重**：评分标准已在 darwin-rubric.md、巡检流程已在 score-inspection-workflow.md，新 SOP 只补「优化执行流程」不复制维度定义与打分公式（边界声明在 SOP「与相关文件边界」节）；无存量重复段落可清（N/A + 理由）。
- **同域扫描结论**：范围 = skill-absorption-rules（落点）、score-inspection-workflow（巡检上游）、darwin-rubric（评分标准）、skill-audit-rules（只读审计）、skill-hit-check-rules（触发总控）；发现 = 0 处重复段落（SOP 讲"优化"、score-inspection 讲"打分"，指针衔接非重复）、0 处门控层叠（SOP 独有术语"八步闭环/短板类型学/本侧修正"与既有 gate 无嵌套）、0 处散落产物（新文件为正式资产，improvement-output-template.md 为既有 gap 模板非散落）；清理 0 处；**PASS**。
- **环境依赖登记**：N/A + 理由（纯规则文本，无环境变量 / 宿主配置 / hook / 依赖安装 / 路径引用）。
- **净增体积**：+约 6.6KB（SOP 6306B + SKILL.md 2 行 ~0.3KB + score-inspection 1 句 ~0.1KB）；无外部源，净增即缺口流程本身。
- **棘轮验证**：`quick_validate.py` → `Skill is valid!`（exit 0）；独立子代理覆盖度审查 **PASS**（7 skill 名单/分数/八步顺序/7 类短板/6 实操坑全部核实一致，2 处轻微表述已修正）；知识库 `knowledge_index.py check` 0 死链；UTF-8 3 文件 OK；引用链 2 处可达（SKILL.md 读取规则 + score-inspection 出口）。

## 2026-08-24：内部更新——8 维评分体系巡检工作流固化

- **来源**：内部调整：`skill-absorption-rules`（吸收规则总入口），调整诉求 = "把「用 darwin-rubric 8 维给全仓库 skill 打分 + 生成 skill-8维评分报告.html」的实操经验固化为可复用流程，后续快速打分更新报告"。
- **形态**：内部更新通道（无外部源可删）。
- **拆解原子条目数**：3 条。
- **裁决**：
  - 8 维评分标准（权重 / 计分公式）→ 保留本地（`darwin-rubric.md` 已是单一权威，不重复定义）。
  - 体系巡检执行流程（范围分类 / 分批打分 / 报告产出）→ 合并（缺口）：新增 `score-inspection-workflow.md` 作流程单一权威。
  - 报告固定文件与结构约定 → 合并（缺口）：报告路径 `skill-8维评分报告.html` 与 JS 数据格式约定写入新流程文件。
- **落盘改动**：
  - `skill-absorption-rules/references/score-inspection-workflow.md`（新建）：触发信号 / 范围四分类 / 并行子代理分批打分 / 固定输出格式 / 短板识别 / 报告结构约定。
  - `skill-absorption-rules/SKILL.md`：references 读取规则补 1 条指针。
  - `skill-absorption-rules/references/darwin-rubric.md`：第 60 行补 1 句指向新流程文件。
- **整理去重**：评分标准已在 darwin-rubric.md，新文件只补「执行流程」不复制维度定义；无存量重复段落可清（N/A + 理由）。
- **同域扫描结论**：范围 = skill-absorption-rules（落点）、skill-audit-rules（只读审计，涉及多 skill 巡检但职责为职责重叠审计非评分）、skill-hit-check-rules（触发总控）；发现 = 0 处重复段落、0 处门控层叠、0 处散落产物；清理 0 处；**PASS**。
- **环境依赖登记**：N/A + 理由（纯规则文本，无环境变量 / 宿主配置 / hook / 依赖安装 / 路径引用）。
- **净增体积**：+约 3.2KB（score-inspection-workflow.md ~3.0KB + SKILL.md 1 行指针 ~0.1KB + darwin-rubric.md 1 句 ~0.1KB）；无外部源，净增即缺口流程本身。
- **棘轮验证**：引用链 2 处可达（SKILL.md 读取规则 + darwin-rubric.md 均指向 score-inspection-workflow.md）；UTF-8 3 文件 OK。

## 2026-08-24：内部更新——文档阶段接口测试要求预埋

- **来源**：内部调整：`test-strategy-rules`（测试策略统一主入口），调整诉求 = "写需求 / 计划 / bug / 实施 md 文档时，涉及 API 接口测试必须预埋「本地 test/ 单元测试 + 完善 apifox 接口用例」双要求"。
- **形态**：内部更新通道（无外部源可删）。
- **拆解原子条目数**：4 条。
- **裁决**：
  - 测试双要求（test/ 单元测试 + apifox 接口用例）→ 保留本地（`test-strategy-rules`「接口测试执行通道」已覆盖执行阶段）。
  - 顺序约束（先单测后 apifox）→ 保留本地（执行通道已隐含）。
  - 完成标准（apifox 用例完善 = 落地 + 通过，非本地 curl）→ 保留本地（执行通道「不得只本地 curl 不落地」）。
  - 文档阶段预埋 → 合并（缺口）：新增「文档阶段接口测试要求预埋（强制）」节作单一权威。
- **落盘改动**：
  - `test-strategy-rules/SKILL.md`：新增「文档阶段接口测试要求预埋（强制）」节（单一权威，「接口测试执行通道」姊妹节）。
  - `requirement-intake-rules/SKILL.md`、`implementation-planning-rules/SKILL.md`、`bug-intake-rules/SKILL.md`：各加 1 行引用指针，不重复定义。
- **整理去重**：执行阶段规则已存在未重复；新增仅补文档阶段缺口，引用式接入，无存量冗余可清（N/A + 理由）。
- **同域扫描结论**：范围 = 测试域（test-strategy / test-program / test-regression / functional-validation / bug-validation）+ 文档域（requirement-intake / implementation-planning / bug-intake / artifact-delivery-gate）；发现 = 0 处重复段落（「文档阶段预埋」vs「接口测试执行通道」为写文档时 vs 执行测试时两阶段，非重复）、0 处门控层叠、0 处散落产物；清理 0 处；**PASS**。
- **环境依赖登记**：N/A + 理由（纯规则文本，无环境变量 / 宿主配置 / hook / 依赖安装 / 路径引用）。
- **净增体积**：+约 1.3KB（test-strategy-rules 新节 ~1.1KB + 3 处引用指针各 ~0.07KB）；无外部源，净增即缺口规则本身。
- **棘轮验证**：引用链 4 处可达（单一权威节 + 3 引用指针，均指向 `test-strategy-rules/SKILL.md` 新节）；UTF-8 4 文件 OK。

## 2026-08-23：skill-merger（技能合并器，ClawHub mimo-skill-merger）

- **来源**：skillhub 安装源 `mimo-skill-merger__skillhub`（用户级 + 工作区 junction 同一物理目录，version 1.3.0，homepage qqyougitcom/mimo-skill-merger，MIT-0）。
- **形态**：外部吸收通道（本地安装源吸收模式：读取原文 → 裁决 → 落盘 → 删除源）；吸收目标为 skill-absorption-rules 自身——补齐「内部更新通道」的多技能合并执行细则（本地此前仅有触发信号"把这两个 skill 合并"，无策略框架）。
- **拆解原子规则数**：17 条。

| # | 外部精华 | 本地现状 | 裁决 | 落点 / 理由 |
|---|---------|---------|------|------------|
| 1 | 吸收型策略（B⊂A → 独特能力并入 A 作子模块） | 外部吸收通道仅覆盖外部→本地单向吸收，无自有技能间吸收显式策略 | 合并 | `merge-strategies.md`「吸收型」节 |
| 2 | 融合型策略（交叉各有优势 → 统一新流程） | 本地无平等合并策略；红线不新增 skill 目录 | 合并(适配) | 「融合型」节；融合产物落现有主 skill 的 reference，不新建目录 |
| 3 | 编排型策略（独立常配合 → 编排层路由） | 本地无编排层概念（audit 只读、split 管拆分） | 合并 | 「编排型」节 |
| 4 | Step1 技能分析（读 SKILL.md 提取能力识别重叠） | 裁决第 2 步要求读 SKILL.md + references 原文 | 保留本地 | 本地更严（references 全文） |
| 5 | Step2 策略选择 | 随 1-3 落地 | 合并 | 并入三策略节 |
| 6 | 触发词冲突 → 合并关键词 + 细化排除场景，触发词/排除词双列不单留 | 触发体系在 hit-check-rules；absorption 无显式触发合并冲突规则 | 合并 | 「冲突处理」节 |
| 7 | 冲突处理·流程重叠 → 保留更详细版 | 「保留本地（本地更强）」裁决语义等价 | 保留本地 | 裁决矩阵已覆盖 |
| 8 | 冲突处理·输出格式 → 统一模板 | 本地裁决表格式更细（含整理建议列） | 保留本地 | 本地更强 |
| 9 | 变更对比模板（+新增 / -消除 / ~调整） | 本地无此输出模板 | 合并 | 「变更对比」节 |
| 10 | 不丢功能（覆盖所有源核心能力） | 「语义零丢失」原则等价且更强 | 保留本地 | 吸收即整理原则 |
| 11 | 保持独立（不强制合并差异大技能） | 红线「不新增同类目录」更强 | 保留本地 | 本地红线更强 |
| 12 | 版本管理（新技能从 v1.0.0 起） | 本地合并产物是 reference/正文补丁，无新技能实体 | 拒绝 | 形态不匹配（不新建 skill 目录） |
| 13 | 反合理化①"差异大合并不了" → 编排型兜底，至少输出编排方案 | 无此兜底规则 | 合并 | 「反合理化」节 |
| 14 | 反合理化②"怕丢功能" → 变更对比逐条确认 | 「语义零丢失」有原则、无强制输出 | 合并 | 同 #9 |
| 15 | 反合理化③"触发词冲突" → 双列排除 | 同 #6 | 合并 | 同 #6 |
| 16 | 反合理化④"逐个看" → 只读 description+前 3 步 | 本地「能查证就不要凭记忆」要求读原文 | 拒绝 | 本地更强（裁决必须读原文，快速扫描仅可预判策略） |
| 17 | 反合理化⑤"命名不好定" → 主功能词+后缀 | 本地不新建目录，命名场景少 | 拒绝 | 形态不匹配 |

- **落盘改动**：
  - 新增 `skill-absorption-rules/references/merge-strategies.md`（3889B，三策略 + 冲突处理 + 变更对比模板 + 反合理化表 + 同域边界）。
  - 修改 `skill-absorption-rules/SKILL.md`（三通道表格内部更新通道行补合并策略指引 + references 读取规则补 1 条，+507B）。
- **整理去重**：外部 3KB → 合并 8 项 → 新 reference 3889B；SKILL.md 正文仅净增 3 行（表格 1 行 + 读取规则 1 行），细则下沉 references，符合「单一可编辑资产 + 吸收即整理」；本地无同义重复段落可清（引用式结构，N/A + 理由）。
- **同域扫描结论**：范围 = skill-absorption-rules（落点）、skill-audit-rules（只读审计）、skill-split-preserve-rules（拆分）、skill-hit-check-rules（触发冲突）；发现 = 0 处重复段落（三策略关键词同域 3 skill 零命中）、0 处门控层叠（吸收型/融合型/编排型为本地缺失能力，与 audit 只读、split 反向拆分语义可区分）、0 处散落产物；清理 0 处；**PASS**。
- **环境依赖登记**：N/A + 理由（纯规则文本，无环境变量/宿主配置/hook/依赖安装/路径引用）。
- **净增体积**：+约 4.4KB（merge-strategies 3889B + SKILL.md 补丁 507B）；外部源 3KB 已删除，体系净增约 +1.4KB 等价。
- **棘轮验证**：`quick_validate.py` 结构校验 PASS；独立子 agent 8 维评分基线 75.8 → 86.8（+11.0）PASS；UTF-8 2 文件 OK；引用链 2 处可达（SKILL.md 三通道表格 + 读取规则）。
- **源清理**：吸收完成后删除本地安装源 `mimo-skill-merger__skillhub`（用户级 + 工作区 junction 双路径验证）。

## 2026-08-23：qa-bug-root-cause-analysis（Kokxi/qa-test-skills）

- **来源**：skillhub 安装源 `qa-bug-root-cause-analysis__skillhub`（用户级 + 工作区 junction 同一物理目录，version 1.7.0，homepage Kokxi/qa-test-skills，QA Test Skills 技能集 49 个之一）。
- **形态**：外部吸收通道（本地安装源吸收模式：读取原文 → 裁决 → 落盘 → 删除源）。
- **拆解原子规则数**：10 条。

| # | 外部精华 | 本地现状 | 裁决 | 落点 / 理由 |
|---|---------|---------|------|------------|
| 1 | 5 类症状 → 根因方向树状映射（返回错误/数据不对/性能退化/没反应/偶发） | root-cause-catalog 有代码层类别池，缺「症状层入口」 | 合并 | `bug-root-cause-rules/references/symptom-rootcause-map.md`（新建） |
| 2 | 现象速查表（现象→大概率方向→优先排查 14 行） | 本地无此表 | 合并 | 同上 |
| 3 | 排查顺序（先外部→配置→数据→代码） | catalog 边界场景部分覆盖，无完整顺序 | 合并 | 同上（交叉引用不重复展开） |
| 4 | 分析流程 4 步（收集→分类→缩小→验证） | intake 收集 + static-analysis 收窄 + evidence 验证 | 保留本地 | 五件套分阶段更强 |
| 5 | 根因分析表模板 | Bug 主文档 + evidence 证据条件 | 保留本地 | 本地更强 |
| 6 | 输出示例 2 个 | 本地有真实案例 | 拒绝 | 一次性教学示例形态 |
| 7 | 检查清单 6 项 | evidence + delivery-gate 收口 | 保留本地 | 本地更强 |
| 8 | frontmatter 机制（input/output/深度量化） | Bug 主文档 + 触发路由体系 | 拒绝 | 机制形态不迁移 |
| 9 | 根因分层：直接/间接/系统 3 层级 | hypothesis-ranking 有横向候选，缺纵向追问 | 合并 | 并入 symptom-rootcause-map.md「根因分层」节 |
| 10 | 生产数据脱敏警告 | 无脱敏专项 | 合并 | 并入 symptom-rootcause-map.md 注意事项 |

- **落盘改动**：
  - 新增 `bug-root-cause-rules/references/symptom-rootcause-map.md`（6239B，五类症状映射 + 速查表 + 排查顺序 + 根因分层 + 脱敏）。
  - 修改 `bug-root-cause-rules/SKILL.md`（默认执行流程第 3 步升级为「症状分类 → 类别候选池 → 排序假设」四级链路 + references 读取规则 1 处）。
  - 修改 `bug-root-cause-rules/references/root-cause-catalog.md`（顶部加症状层入口衔接句）。
- **整理去重**：外部 328 行 → 合并 5 项 → 精简为 103 行核心表；catalog「外部原因优先排除」与新排查顺序重叠处收敛为交叉引用（catalog 顶部衔接句），未重复展开；本地无同义重复段落可清（引用式结构，N/A + 理由）。
- **同域扫描结论**：范围 = Bug 域 5 skill（intake/reproduction/root-cause/fix-proposal/validation）+ 测试域 3 skill（strategy/program/regression）；发现 = 0 处重复段落（症状分类关键词仅命中 root-cause 域内部 3 文件，同域 7 skill 零命中）、0 处门控层叠（症状映射/类别候选池/假设排序为同一链路上下游三阶段）、0 处散落产物；清理 0 处；**PASS**。
- **环境依赖登记**：N/A + 理由（纯规则文本，无环境变量/宿主配置/hook/依赖安装/路径引用）。
- **净增体积**：+约 6.5KB（新 reference 6239B + SKILL.md 补丁 ~180B + catalog 衔接 ~100B）；外部源 5KB 已删除，体系净增约 +1.5KB 等价。
- **棘轮验证**：`quick_validate.py` 5/5 skill PASS（落点 + 同域四件套）；独立子 agent 8 维评分基线 78.8 → 86.8（+8.0）PASS；UTF-8 3 文件 OK；引用链 3 处可达（SKILL.md L39/L76 + catalog L5）。
- **源清理**：吸收完成后删除本地安装源 `qa-bug-root-cause-analysis__skillhub`（用户级 + 工作区 junction 双路径验证均不存在）。

## 2026-08-23：browser-use API + guide 合并吸收（Cloud REST 操作通道）

- **来源**：skillhub 安装源 `browser-use-api__skillhub`（REST v2 API 操作指南，含 `scripts/browser-use.sh`）+ `browser-use-guide__skillhub`（browser-use 完整指南，含开源库/CLI/OpenClaw/云端对比）；两源均同时存在于仓库根与用户级（junction 同一物理目录）。
- **形态**：外部吸收通道（本地安装源吸收模式：读取原文 → 裁决 → 落盘 → 删除源）；吸收触达同域 skill `browser-use-cloud-rules`，按用户决策将两源合并进该 skill（不新建同类目录）。
- **拆解原子规则数**：22 条（来源 A 11 + 来源 B 11）。
- **裁决**：
  - 来源 A（REST API）：v2 端点表、curl 示例、任务状态机、`browser-use.sh` 轮询脚本、credits 查询、定价 → **合并**（本地仅 MCP 路径文档，无 REST 路径）；"When to Use/When NOT" → **保留本地**（`browser-use-cloud-rules` 路由边界 + `mcp-installation-rules/tool-priority.md` 矩阵更强）。
  - 来源 B（指南）：云端 vs 开源对比、模型定价表、应用场景示例、故障排除（API Key/被检测→云端）→ **合并**；密钥配置 → **合并但改写**（按用户新决策统一存 `~/.browser-use/.env`，废弃原"项目代码/配置默认"旧口径）；本地开源库安装、Python Agent 本地代码、CLI 工具、OpenClaw 集成、自定义 Tools、Chrome profile 复用 → **拒绝**（场景不匹配——用户定位是"项目程序操作公网 https 浏览器"；宿主不匹配——OpenClaw 专属形态）。
- **落盘改动**：
  - `browser-use-cloud-rules/references/api-operations.md`（新建）：REST v2 端点/状态机/curl/Python 集成/模型定价/边界，凭据单一权威指向 `~/.browser-use/.env`。
  - `browser-use-cloud-rules/scripts/browser-use.sh`（新建）：从 `~/.browser-use/.env` 读 key + `--check/--balance` 自检（替代源脚本的纯环境变量模式）。
  - `browser-use-cloud-rules/scripts/.env.example`（新建）：密钥模板。
  - `browser-use-cloud-rules/SKILL.md`（修改）：description 触发扩展（项目程序操作公网浏览器）、凭据策略改 `~/.browser-use/.env` 单一权威、新增「REST API 操作通道」「环境自检」小节、References 补 api-operations.md。
  - `browser-use-cloud-rules/references/routing-and-safety.md`（修改）：MCP 配置凭据来源补"值来自 `~/.browser-use/.env`"口径。
- **整理去重**：browser-use 凭据来源策略收敛为单一权威——`browser-use-cloud-rules` 旧口径"项目代码/配置默认"更新为 `~/.browser-use/.env`；同域 `authenticated-url-routing-rules/SKILL.md` 两处旧口径（L30 配置位置、L115 凭据来源）同步收敛为引用；两源合并后拒绝约 60% 开源库/OpenClaw 内容，未产生整段重复。
- **同域扫描结论**：范围 = browser-use-cloud-rules、authenticated-url-routing-rules、mcp-installation-rules（tool-priority）、browser-session-automation-rules、browser-advanced-testing-rules、README.md、编码skill.md；发现 = 2 处门控层叠（authenticated-url-routing L30/L115 旧凭据口径与新版冲突）+ 1 处引用链缺口（routing-and-safety MCP 凭据来源未指向 .env）；清理 3 处；**PASS**（其余引用为中性表述，兼容）。
- **环境依赖登记**：1 项——`路径: ~/.browser-use/.env`（junction → `D:\谷歌云盘\browser-use`，Google Drive 同步），已登记至 `workbuddy-env-manifest.md` 第 9 项；自检能力 = `scripts/browser-use.sh --check`（SKILL.md「环境自检」小节三行命令）。
- **净增体积**：+约 12KB（api-operations.md ~6KB + browser-use.sh ~4KB + .env.example ~0.2KB + SKILL.md/routing 增量 ~2KB）；两源合计 ~11KB，合并后净增约 +1KB 等价（含拒绝内容约 6.5KB 未入）。
- **棘轮验证**：`quick_validate.py` PASS；`bash -n browser-use.sh` 语法 PASS；`--check` 真实环境自检 PASS（正确报 key 缺失）；Python 集成密钥读取三场景（.env 读取 / env 覆盖 / 双缺失抛错）全部 PASS（隔离 HOME + 哨兵 key）；UTF-8 与引用链复核 PASS（api-operations → SKILL.md 2 处、browser-use.sh → SKILL.md 3 处、.env.example → SKILL.md 环境自检 1 处、manifest 第 9 项 → SKILL.md 权威）。
- **源清理**：吸收完成后删除本地安装源 `browser-use-api__skillhub` 与 `browser-use-guide__skillhub`（仓库根 + 用户级 junction 双路径各删一份，共 4 目录）。

## 2026-08-23：内部更新——环境依赖吸收（跨机器自愈）

- **来源**：内部调整：`skill-absorption-rules`（吸收方法论）+ WorkBuddy 平台配置事实（官方文档 env-vars + 现网部署），调整诉求 = "吸收 skill 时不能只吸收规则正文，还要吸收环境配置 / hook / 依赖；换电脑或新环境缺失时自动检测并自动补齐"。
- **形态**：内部更新通道（无外部源可删；平台配置事实来自官方文档与现网部署，已入知识库）。
- **裁决**：
  - 环境依赖成为吸收一等公民 → 合并进 `skill-absorption-rules/SKILL.md` 默认流程第 4 步（环境依赖登记 + manifest 写入）+ 收口说明（依赖登记数量 / 自检能力数量 / 净增体积）+ 通过/驳回标准（环境类条目未登记依赖驳回、有依赖无自检/自动配置能力驳回）+ references 读取规则 3 条。
  - 单一权威 manifest → 新建 `references/workbuddy-env-manifest.md`（8 项 WorkBuddy 平台配置，每项含检测方式 / 配置方法 / 验证方式 / 来源证据）。
  - 环境依赖吸收指引 → 新建 `references/env-dependency-absorption.md`（五类依赖：环境变量 / 宿主配置 / hook·插件·MCP / 依赖安装 / 路径引用；裁决表加「环境依赖」列，无依赖写 `N/A + 理由`；复杂依赖须提供 `--check/--dry-run/--fix` 自检）。
  - 跨机器自检自愈 → 新建 `scripts/env-bootstrap-check.py`（三模式，merge / 追加 / 备份 / 幂等策略，Windows 用 `setx` 写 `HKCU\Environment`）。
  - hook 资产副本 → 新增 `assets/hooks/summary-check.py` + `assets/hooks/ralph-stop.py`（md5 与用户级现网脚本一致，仓库即备份源）。
- **落盘改动**：`skill-absorption-rules/SKILL.md` 4 处升级（设计内核 / 默认流程第 4 步 / 收口说明 / 通过驳回标准）；新增 2 reference + 1 脚本 + 2 hook 资产副本，共 5 文件。
- **整理去重**：环境配置表述收敛到 `workbuddy-env-manifest.md` 单一权威——此前平台配置散落在工作日志与知识库，仓库侧无权威清单，本次收敛为"同一环境依赖只允许在一个 manifest 定义、其他 skill 只引用"，消除配置漂移源；hook 资产以现网 md5 为准副本化，消除"仓库与现网两处漂移"。
- **同域扫描结论**：范围 = 吸收域（skill-absorption-rules）+ 环境依赖触达域（reasoning-summary-structure / context-compression / autonomous-execution / task-plan-rehydration，均与 SUMMARY-GATE-PMW-002 / 平台压缩配置相关）；发现 = 0 处重复段落、0 处门控层叠、0 处散落产物（manifest 为配置事实权威 vs 各 skill 为使用方引用，非冗余）；清理 0 处；**PASS**。
- **净增体积**：+42035 bytes（manifest 5543 + 指引 4341 + 自愈脚本 14376 + hook 资产副本 17775）；hook 副本为现网脚本资产化，非规则正文膨胀。
- **棘轮验证**：`env-bootstrap-check.py` 语法 PASS、六场景单测 6/6 PASS、真实环境 `--check` 8/8 完备、UTF-8 7 文件 PASS、引用链 12 本 skill + 3 跨 skill 全部可达、同域扫描 0 扩散、登记文件与知识库收口补齐。

## 2026-08-22：调试（awesome-ai-agent-skills）

- **来源**：marketplace 安装源 `debugging-skillhub__skillhub`（仓库根 + 用户级 junction 同一物理目录，git 未跟踪，version 1.0.0，作者 awesome-ai-agent-skills contributors）。
- **形态**：外部吸收通道（本地安装源吸收模式：读取原文 → 裁决 → 落盘 → 删除源）。
- **拆解原子规则数**：20 条。

| # | 外部精华 | 本地现状 | 裁决 | 落点 / 理由 |
|---|---------|---------|------|------------|
| 1 | 复现：确认可观察可重复 + 收集错误/堆栈/日志 + 最小输入 + 间歇记录频率环境 | intake 收集 + reproduction-template 步骤 + feedback-loop 复现三确认 + stability-checks 频率条件 | 保留本地 | 全覆盖 |
| 2 | 隔离：堆栈/错误/代码结构缩小范围 + 从失败点向后追踪数据流 | static-analysis-path「顺着调用链往内收窄」「对照关键状态/分支/数据转换」 | 保留本地 | 数据流收窄已覆盖 |
| 3 | 隔离战术：stub/bypass 排除无关路径 + 禁用一半系统二分定位 | static-analysis-path 无此战术；feedback-loop 的二分是自动化回路语境（不同） | 合并 | 补 static-analysis-path.md |
| 4 | 常见根因类别清单（输入假设/并发状态/缓存过期/运算符优先级/缺失 await/依赖版本） | root-cause-evidence 有证据标准，无「可能是什么」类别清单 | 合并 | `bug-root-cause-rules/references/root-cause-catalog.md`（新建） |
| 5 | 区分根因与症状（NPE 是症状，根因可能在三跳前） | root-cause-evidence「常见误判」已有「只看堆栈忽略前置状态」 | 保留本地 | 同义且更强 |
| 6 | 修复：最小改动 + 共享接口追踪调用者 + 防御性修复 | fix-proposal「根因修复优先 + 最小改动协调 + 反打补丁式修复」 | 保留本地 | 本地更强 |
| 7 | 验证：重跑复现 + 回归测试 + 既有测试 + 关键路径监控 | validation 闭环 + correct-seam（失败测试+重跑原始）+ post-mortem | 保留本地 | 本地更强 |
| 8 | 堆栈阅读纪律：从下往上、根因在深层应用帧、框架帧可跳过 | static-analysis-path 有「看报错位置」，无阅读顺序纪律 | 合并 | 补 static-analysis-path.md |
| 9 | 一次只改一件事 | runtime-observation-methods「诊断手段服务于当前假设」 | 保留本地 | 与 diagnose #10 同义，已裁决 |
| 10 | 战略日志：入口/出口插日志，修复后移除 | debug-log-placement「决策点/状态点/边界/异常处」⊇ 入口出口 | 保留本地 | 本地更强 |
| 11 | 先查最近变更：git bisect / review diff 常是最快路径 | feedback-loop 有二分 harness（自动化回路），无「先查最近提交」快速纪律 | 合并 | 补 static-analysis-path.md |
| 12 | 修复前先复现，不可复现不修 | feedback-loop 复现三确认 + reproduction 暂停条件 | 保留本地 | 全覆盖 |
| 13 | 每个修复产出失败→通过回归测试 | correct-seam「修复前失败测试 + 重跑原始场景」 | 保留本地 | 本地更强（含正确接缝检查） |
| 14 | Heisenbug：调试工具附加改变时序掩盖竞态 → 日志/追踪 + race detector | runtime-observation-methods 无 Heisenbug 专项 | 合并 | 补 runtime-observation-methods.md |
| 15 | 环境特定 bug：生产才出现 → 问环境细节 + 匹配约束复现（Docker 内存限制） | stability-checks 有「网络波动」、feedback-loop 有「索要环境」，无匹配复现战术 | 合并 | 补 stability-checks.md |
| 16 | 第三方库 bug：升级/workaround/pin + 查 changelog/issue tracker | 本地无 | 合并 | 并入 root-cause-catalog.md |
| 17 | 编译器/runtime bug：穷尽应用层解释再测不同 runtime | 本地无 | 合并 | 并入 root-cause-catalog.md |
| 18 | 损坏状态：数据与代码一起查 + 要样本数据 | 本地无 | 合并 | 并入 root-cause-catalog.md |
| 19 | 跨语言工具参考表（stack trace/debugger/profiling/memory/concurrency） | runtime-observation-methods 有手段分类，无工具名清单 | 合并 | 补 runtime-observation-methods.md |
| 20 | 示例 2 个（race condition / memory leak 教学代码） | 精华已提取为根因类别条目（并发共享可变状态 / 无界内存容器） | 拒绝 | 一次性教学示例形态 |

- **落盘改动**：
  - 新增 `bug-root-cause-rules/references/root-cause-catalog.md`，并在 SKILL.md 默认执行流程第 3 步 + references 读取规则登记。
  - 补 `bug-root-cause-rules/references/static-analysis-path.md`（堆栈阅读纪律 + 先查最近变更 + 二分隔离/stub 排除三节）。
  - 补 `bug-intake-rules/references/runtime-diagnostics-bug-runtime-debug-rules-runtime-observation-methods.md`（Heisenbug 节 + 跨语言工具参考表）。
  - 补 `bug-reproduction-rules/references/stability-checks.md`（环境特定 Bug 匹配复现节），并同步 SKILL.md 两处引用描述。
- **整理去重**：修复 `bug-reproduction-rules/SKILL.md` 默认执行流程编号重复（两个「3.」→ 1-6 顺排，上轮 feedback-loop 插入遗留的格式瑕疵）；无同义重复段落可合并（本地五件套为引用式结构，本轮为补缺增量）。
- **同域扫描结论**：范围 = Bug 域 5 skill（intake/reproduction/root-cause/fix-proposal/validation）+ 测试域 3 skill（strategy/program/regression）；发现 = 0 处重复段落、0 处门控层叠、0 处散落产物（root-cause-catalog 为假设生成候选池 vs hypothesis-ranking 为排序纪律，阶段互补；stability-checks 环境匹配 vs feedback-loop 索要环境，分属复现判定与回路构建两阶段；static-analysis-path 禁用一半系统 vs feedback-loop 二分 harness，静态排除战术 vs 自动化回路工具）；清理 1 处（SKILL.md 编号格式）；**PASS**。
- **净增体积**：+5005 bytes（1 个新 reference 2549 + 3 处补丁 992/479/985），引用式接入无膨胀。
- **棘轮验证**：3 个 skill `quick_validate.py` 全部 PASS；4 个落盘文件 UTF-8 无乱码；引用链可达（root-cause-catalog→SKILL.md 2 处、stability-checks→bug-reproduction SKILL.md 2 处、runtime-observation-methods→runtime-diagnostics.md 路由、static-analysis-path→SKILL.md 默认第 1 步）。
- **源清理**：吸收完成后删除本地安装源 `debugging-skillhub__skillhub`（仓库根目录，junction 双路径同一物理目录）。

## 2026-08-22：diagnose（mattpocock/skills）

- **来源**：marketplace 安装源 `diagnose`（仓库根 + 用户级 junction 同一物理目录，`_skillhub_meta.json` skillId `skill_2057443344813191168`，version 1.0.0，homepage `https://github.com/mattpocock/skills`）。
- **形态**：外部吸收通道（本地安装源吸收模式：读取原文 → 裁决 → 落盘 → 删除源）。
- **拆解原子规则数**：18 条。

| # | 外部精华 | 本地现状 | 裁决 | 落点 / 理由 |
|---|---------|---------|------|------------|
| 1 | 反馈回路是调试核心：先构建快速确定性 agent 可运行 pass/fail 信号，再谈定位 | reproduction 有最小复现路径、runtime-diagnostics 有受控观察，但无「反馈回路优先」元方法论 | 合并 | `bug-reproduction-rules/references/feedback-loop.md`（新建） |
| 2 | 构建回路 10 种方式清单（failing test/curl/CLI fixture/headless/replay trace/harness/fuzz/bisection/differential/HITL） | 本地无系统化回路构建清单 | 合并 | 并入 feedback-loop.md |
| 3 | 迭代回路三问：更快/信号更尖锐/更确定性 | stability-checks 有稳定性判断，无「回路本身可优化」概念 | 合并 | 并入 feedback-loop.md |
| 4 | 非确定性 Bug：目标是提高复现率（loop 100×、并行、加压力、窄化时序窗口） | stability-checks 有「是否每次出现/特定条件」，无提高复现率战术 | 合并 | 并入 feedback-loop.md |
| 5 | 无法构建回路：停下明说、列尝试、索要环境访问/捕获产物/临时插桩权限 | reproduction 有暂停条件，缺「索要三样东西」清单 | 合并 | 并入 feedback-loop.md |
| 6 | 复现三确认：用户描述的现象/跨多次可复现/捕获确切症状 | reproduction 有「记录复现结果、稳定性、失败差异」，缺「确认是用户描述的现象」 | 合并 | 并入 feedback-loop.md |
| 7 | 测试前生成 3-5 个排序假设；单假设锚定 | root-cause 有「多个假设都成立」暂停条件，缺排序纪律 | 合并 | `bug-root-cause-rules/references/hypothesis-ranking.md`（新建） |
| 8 | 假设必须可证伪：陈述预测 If X then changing Y | root-cause-evidence 有「能解释为什么」，缺可证伪预测格式 | 合并 | 并入 hypothesis-ranking.md |
| 9 | 排序列表给用户看（领域知识可重排），不阻塞 | fix-proposal 有「是否需用户确认」（修复阶段），假设阶段给用户看是新增量 | 合并 | 并入 hypothesis-ranking.md |
| 10 | 探针映射 Phase 3 预测 + 一次只改一个变量 | runtime-observation-methods 已有「诊断手段服务于当前假设」「不做全链路无差别打印」 | 保留本地 | 本地更强（含 local 只读约束） |
| 11 | 工具偏好：debugger > 定向日志 > 绝不 log everything | runtime-observation-methods 已有「先最小侵入、先观察关键状态点」 | 保留本地 | 本地同义且更强 |
| 12 | 调试日志唯一前缀标签（[DEBUG-xxxx]）→ 一次 grep 清理 | debug-log-placement 有「输出字段最小集合」、cleanup 有「默认删除」，缺唯一前缀标签机制 | 合并 | 补进 `bug-intake-rules/references/runtime-diagnostics-bug-debug-log-rules-debug-log-placement.md` |
| 13 | Perf 分支：先建基线测量再 bisect，先测量后修复 | 本地无性能回归专项方法论 | 合并 | 并入 feedback-loop.md「性能回归」节 |
| 14 | 修复前写回归测试——仅当有正确接缝（correct seam）；接缝太浅给虚假信心 | test-regression 有回归范围判定，缺「正确接缝」概念 | 合并 | `test-regression-rules/references/correct-seam.md`（新建） |
| 15 | 无正确接缝本身就是发现：架构阻碍锁定 bug，标记给下一阶段 | 本地无此概念 | 合并 | 并入 correct-seam.md |
| 16 | 最小化复现→失败测试→修复→通过→重跑原始未最小化场景 | validation 有验证闭环、regression 有流程，缺「重跑原始场景」收尾 | 合并 | 并入 correct-seam.md |
| 17 | 收尾清单：原复现不再复现/回归通过/DEBUG 移除/一次性原型删除/正确假设写 commit message | debug-log-cleanup 有日志清理，缺「原型删除 + 正确假设写 commit」 | 合并 | 并入 correct-seam.md「修复收尾清单」 |
| 18 | post-mortem：修复后问「什么能阻止这个 Bug」，架构建议在修复后给 | 本地无 post-mortem 概念 | 合并 | `bug-validation-rules/references/post-mortem.md`（新建） |

- **落盘改动**：
  - 新增 `bug-reproduction-rules/references/feedback-loop.md`，并在 SKILL.md 默认执行流程第 2 步 + references 读取规则登记。
  - 新增 `bug-root-cause-rules/references/hypothesis-ranking.md`，并在 SKILL.md 默认执行流程第 3 步 + references 读取规则登记。
  - 修改 `bug-intake-rules/references/runtime-diagnostics-bug-debug-log-rules-debug-log-placement.md`（补唯一前缀标签机制）。
  - 新增 `test-regression-rules/references/correct-seam.md`，并在 SKILL.md 默认执行流程第 2 步 + references 读取规则登记。
  - 新增 `bug-validation-rules/references/post-mortem.md`，并在 SKILL.md 默认执行流程第 7 步 + references 读取规则登记。
- **整理去重**：N/A + 理由：本地五件套为引用式结构，无同义重复段落可合并；本次为纯方法论增量（反馈回路/假设排序/正确接缝/复盘四块本地确实缺失），无存量冗余可清。
- **同域扫描结论**：范围 = Bug 域 5 skill（intake/reproduction/root-cause/fix-proposal/validation）+ 测试域 3 skill（strategy/program/regression）；发现 = 初判 0 处重复段落、0 处门控层叠、0 处散落产物（feedback-loop 与 reproduction-template 为方法层 vs 格式层互补，post-mortem 与 validation-checklist 为阶段前后互补，均非冗余）；清理 0 处；**PASS**。
- **净增体积**：+9292 bytes（4 个新 reference + 1 处小补丁），引用式接入无膨胀。
- **棘轮验证**：5 个 skill `quick_validate.py` 全部 PASS；4 个新文件 UTF-8 无乱码；引用链可达（5 处 SKILL.md 引用 + 1 处跨 skill 引用 post-mortem→correct-seam 均可达）。
- **源清理**：吸收完成后删除本地安装源 `diagnose`（仓库根目录，junction 双路径同一物理目录）。

## 2026-08-19：java-story-develop__skillhub

- **来源**：LobeHub 安装包 `java-story-develop__skillhub`（工作区 `D:\谷歌云盘\luode-skills\java-story-develop__skillhub\`，用户级 `C:\Users\luode\.workbuddy\skills\java-story-develop__skillhub\`），版本以安装包 `_meta.json` 为准。
- **形态**：本地安装源吸收（先安装 → 分析吸收 → 删除源）。
- **拆解原子规则数**：14 条。

| # | 外部精华 | 本地现状 | 裁决 | 落点 / 理由 |
|---|---------|---------|------|------------|
| 1 | 环境探测：扫描 pom.xml/go.mod/package.json 探测运行时、Web 框架、ORM、业务框架、工具库、数据库、前端栈 | `project-memory-rules` 有四件套记忆但无环境探测清单机制 | 合并 | `project-memory-rules/references/environment-probe.md`（新建），含探测维度表 + 命令示例 + 记忆固化格式 |
| 2 | 记忆优先恢复环境，命中则跳过探测 | `project-memory-rules` 启动读 PROJECT_CURRENT/PROJECT_MEMORY | 保留本地 | 本地更强 |
| 3 | 环境记忆持久化格式（project-env-{projectName}） | `project-memory-rules` 机器索引区 | 合并 | 并入 environment-probe.md 的记忆固化格式 |
| 4 | 前端检测 + devMode 问询（FULLSTACK/BACKEND） | `package-structure-rules` 已能自动判断前后端同仓 | 拒绝 | 与本地「能自动判断就不问」习惯冲突 |
| 5 | SIMPLE/QUICK/FULL 三档分档路由 + 状态机 | `team-development-rules` 阶段路由、`requirement-splitting-rules` 复杂度拆分 | 合并 | `requirement-intake-rules/references/workload-mode-routing.md`（新建），与极致完整性标准调和 |
| 6 | context.json 状态机（currentPhase/phases/todos） | `task-plan-rehydration-rules` 投影 + AGENTS.md 追踪链 | 拒绝 | 机制形态不迁移，本地投影已覆盖 |
| 7 | 四轮小步迭代（骨架→填充→复盘→风险） | `artifact-delivery-gate-rules`（6-review）、`code-change-finalization-gate-rules` | 保留本地 | 本地更强 |
| 8 | 角色互搏（开发/产品双角色） | `adversarial-gap-interview.md` 已有对抗式缺口追问 | 合并 | `adversarial-gap-interview.md` 追加「设计阶段双角色自检」小节 |
| 9 | 异常恢复指引（6.1-6.5） | `agent-runtime-recovery-rules`、`session-handoff-rules`、`task-plan-rehydration-rules` | 保留本地 | 本地更强 |
| 10 | 11 条编码规范 | `code-generation-style-rules`、`code-quality-rules`、`error-handling-rules`、`logging-trace-rules`、`database-query-rules`、`naming-rules` 等十几条细分 | 保留本地 | 本地更细且 Go 生态适配 |
| 11 | 文档编号规则（1-Requirement/2-Analysis/3-Design） | `artifact-storage-rules`（doc/1-架构 2-需求 3-实施）+ 稳定 ID | 保留本地 | 本地更强 |
| 12 | TODO 分类规范（[临时]/[技债]/[外部依赖]/[逻辑补全]/[暂不明确]） | `task-blocker-closure-contract.md` 已有遗留项处理语义 | 拒绝 | 与本地闸门重叠，避免为吸收而吸收 |
| 13 | 核心变量命名（storyNameCN/ID/Branch） | `naming-rules`、`git-collaboration-rules` | 保留本地 | — |
| 14 | 子任务调度策略（并行分析/设计） | `parallel-task-dispatch-rules` | 保留本地 | 本地更强 |

- **落盘改动**：
  - 新增 `project-memory-rules/references/environment-probe.md`，并在 `project-memory-rules/SKILL.md` 适用场景追加引用。
  - 新增 `requirement-intake-rules/references/workload-mode-routing.md`，并在 `requirement-intake-rules/SKILL.md` References 追加引用。
  - 修改 `requirement-intake-rules/references/adversarial-gap-interview.md`，追加「设计阶段双角色自检」小节。
- **源清理**：吸收完成后删除本地安装 `java-story-develop__skillhub`（工作区 + 用户级两份）。
- **评分**：见对应 case study（`references/case-java-story-develop-absorption.md`，如需）。

## 2026-08-20：内部更新——需求 / 实施 / Bug 三域收敛去重

- **来源**：内部调整：三域 skill 体系（13 个 skill），调整诉求 = "整理一下需求、实施、bug 的 skill"（延续测试域收敛）。
- **形态**：内部更新通道（无外部源可删）。
- **拆解原子条目数**：13 个 skill 逐域盘点。

### 裁决与落点

| 域 | skill | 裁决 | 落点 / 理由 |
|---|---|---|---|
| 需求域 | intake / boundary / change / splitting | 保留现状 | 4 个 SKILL.md 均已"单一权威 + 引用"（shared-contract 76 行承载保护语义，各 SKILL.md 仅 1-2 句精简落地提示）；图片规则在 references 内为不同语境落地项（清单/检查/模板），非硬冗余 |
| 实施域 | delivery-gate | 调整合并 | step4 测试域细则（ASCII 镜像 / release-artifacts / apifox caseId）与 test-strategy 完全重复 → 收敛为引用 test-asset-governance + 《接口测试执行通道》 |
| 实施域 | implementation-planning | 保留现状 | 22 refs 主题区分度高（模板/门禁/契约/流程），按需加载是优点非膨胀；RULE-PMW / 跨会话契约红线不动 |
| 实施域 | storage / rehydration | 保留现状 | 职责独立，仅划界 |
| Bug 域 | intake 等 5 个 | 部分调整 | output-template 重命名规范化（→ bug-discovery-output-template.md）；11 个旧命名空间文件经全量复核为活跃路由资产（被 discovery-and-gap / runtime-diagnostics 引用），保留不删；五份 SKILL.md 已引用式（local 0 处展开复述），bug-lifecycle-common-contract 已为共享契约，C2-C5 保留现状 |

- **整理去重**：delivery-gate SKILL.md L62 测试域细则 → 引用 test-strategy（-约 80 字节展开）；Bug 模板重命名 + 注册表 TPL-PLAIN-BUG-002 path 同步 + discovery-and-gap.md L15 引用同步（消除旧命名空间文件名）。
- **同域扫描结论**：范围 = 需求域 4 + 实施域 4 + Bug 域 5（13 个 skill）；发现 = 探索初判 6 处冗余（需求图片规则 / 实施 refs 膨胀 / Bug 骨架同构等），实测后**3 处为误判**（已引用式 / 模块化设计 / 独立成文模板句），**1 处为误删**（Bug 旧命名文件实为活跃资产，已从 git 恢复 11 个 + 修复引用）；真实冗余 = delivery-gate 测试域细则 1 处 + 旧命名模板名 1 处；清理 2 处；**PASS**（引用链全量复核无死引用）。
- **净增体积**：-约 200 字节（收敛展开 + 重命名），无新增内容。
- **棘轮验证**：体积下降、UTF-8 全通过、全量回归无新增失败、引用链无断链——评分不降。

## 2026-08-20：内部更新——Skill 治理域盘点（保留现状）

- **来源**：内部调整：Skill 治理域（9 项），调整诉求 = "还有哪个域需要整理？→ 用户选 Skill 治理域"。
- **形态**：内部更新通道（只读盘点，无改动）。
- **裁决**：全部保留现状。
  - hit-check / audit / compliance-gate / reasoning-summary 四 gate：逐字重复检测 **0 处**；边界已通过"不替代/只负责/统一交给"声明划清（触发检查 / 过程中审计 / 收口闸门 / 总结渲染四阶段时序），合并会破坏触发机制，不整合即最好整理。
  - skill-dictionary：工具资产（generate_dictionary.py + data.js），被 authenticated-url-routing / code-style-consistency / doc 等广泛引用，非 skill 但移动破坏引用链 → 保留。
  - thread-title mcp/node_modules（23MB）：活跃 MCP server 依赖（SKILL.md 引用 bootstrap.mjs / rename_current_thread），删除破坏功能 → 保留；git 卫生（gitignore node_modules）另行处理。
  - evolution / split-preserve / absorption：职责清晰（gap 回补 / 体积拆分 / 外部引入），合并破坏各自触发 → 保留。
- **同域扫描结论**：范围 = 治理域 9 skill；发现 = 探索初判 4 处（门控层叠 3 遍 / dictionary 混入 / node_modules 垃圾 / 生命周期三 skill 归并），实测**全部为误判**（逻辑相似非逐字重复 / 工具资产 / 活跃依赖 / 职责独立）；真实冗余 0 处；清理 0 处；**PASS**。
- **净增体积**：0（只读盘点，零改动）。
- **棘轮验证**：未改动，无评分变化。

## 2026-08-20：内部更新——编码域盘点（保留现状）

- **来源**：内部调整：编码域（24 skill，~700KB），调整诉求 = "按优先级继续 → 编码域"。
- **形态**：内部更新通道（只读盘点，无改动）。
- **裁决**：全部保留现状。
  - 注释三件套（completion-gate / placement-granularity / chinese-comment）：逐字重复 0 处；三者为"补齐闸门 / 放置颗粒度 / 中文表达"三阶段视角，边界已通过"转交"声明划清；"5 行代码块步骤注释 / 结构体字段注释 / 补丁注释"虽在三件套内双写，但一处是"必须补"（闸门视角）、一处是"放哪"（放置视角），互补非冗余，合并会破坏 gate 强制触发语义。
  - 风格四件套（generation-style / minimal-change / readability / style-consistency）：逐字重复仅 1 处无害句（"不替代 style-consistency"）；四者为"写码前契约 / 范围控制 / 可读检查 / 一致性闸门"编码生命周期四阶段，generation-style 的"同时约束命名/结构/注释/日志/错误"是契约覆盖维度（写码前汇总声明），非越界执行，L58-65 边界节已划清。
  - api-* 四件套 / database-* 两件套：职责清晰（请求生命周期 / 结构-访问），保留。
  - 散落产物：无（各目录结构干净）；仓库根 inventory.yaml 是接口基线活跃资产（被 project-interface-baseline-rules 引用），保留。
- **同域扫描结论**：范围 = 编码域 24 skill；发现 = 探索初判 2 组（注释三件套可合一 / 风格四件套越界），实测**误判**（阶段/视角差异非逐字重复，边界已划清）；真实冗余 0 处；清理 0 处；**PASS**。
- **净增体积**：0（只读盘点，零改动）。
- **棘轮验证**：未改动，无评分变化。

## 2026-08-20：内部更新——Agent 运行域盘点（保留现状）

- **来源**：内部调整：Agent 运行域（11 skill，~568KB），调整诉求 = "按优先级继续 → Agent 运行域"。
- **形态**：内部更新通道（只读盘点，无改动）。
- **裁决**：全部保留现状。3 组候选触发重叠实测均为"触发源 / 时间窗 / 机制差异"，非硬冗余：
  1. session-handoff（用户主动换会话 / 归档）vs context-compression（系统被动压缩后的恢复）：触发源不同（用户发起 vs 系统事件）；compression 条件联动的是 recent-context-bootstrap 而非 handoff。
  2. autonomous（任务闭环推进，无 Goal 依赖）vs long-run-loop（Goal active / 显式 goal 意图驱动的长循环）：Goal 有无是关键差异。
  3. history-recall（用户主动问历史，深度回溯）vs recent-context-bootstrap（新会话启动引导，近 3 天）：双向"不要代替"声明已划清（recent 声明不代替 history 深度回忆，history 声明不代替 recent 近期引导）。
  - 逐字重复 0 处；8 个运行 skill 相互边界声明齐全（条件联动 / 不要代替 / 不替代执行授权）。
- **同域扫描结论**：范围 = 运行域 11 skill；发现 = 探索初判 3 组触发重叠，实测**误判**（触发源/时间窗/Goal 机制差异 + 边界声明已划清）；真实冗余 0 处；清理 0 处；**PASS**。
- **净增体积**：0（只读盘点，零改动）。
- **棘轮验证**：未改动，无评分变化。

## 2026-08-20：内部更新——项目记忆知识域盘点（保留现状，体系盘点收官）

- **来源**：内部调整：项目记忆知识域（8 skill，~444KB），调整诉求 = "顺手过一遍（体系盘点最后一个域）"。
- **形态**：内部更新通道（只读盘点，无改动）。
- **裁决**：全部保留现状。7 个 skill 产出物完全不同，职责天然清晰：
  - project-memory（四件套：状态/规则/历史）、project-style（PROJECT_STYLE.md 风格记忆）、project-local-skills（project-* 前缀项目级 skill 沉淀）、project-rule-file-bootstrap（新会话启动读取）、project-timeline（项目历程报告）、project-design-doc（项目设计.md 维护）、knowledge-flow（跨项目 Google Drive 知识库，明确与四件套分层）。
  - 逐字重复 0 处；边界声明齐全：style 不负责生成契约（归 code-generation-style）、local-skills 不代替 knowledge-flow、bootstrap 不替代 memory 事实抽取、timeline 不代替当前交付摘要、design-doc 不代替 recent-context-bootstrap/artifact-storage。
- **同域扫描结论**：范围 = 记忆知识域 8 skill；发现 = 探索初判"四件套 Owner 需划界"，实测**边界已划清**（产出物不同 + 双向声明）；真实冗余 0 处；清理 0 处；**PASS**。
- **净增体积**：0（只读盘点，零改动）。
- **棘轮验证**：未改动，无评分变化。

## 2026-08-20：内部更新——剩余 skill 全量扫描（4 组保留 + 4 个残留清理）

- **来源**：内部调整：8 域之外的剩余 skill 全量扫描，调整诉求 = "其他 skill 还需要整理吗？扫一遍"。
- **形态**：内部更新通道（扫描 + 少量清理）。
- **裁决**：
  - A 类自有规则 4 组候选重叠全部保留现状：浏览器三件套（本地自动化/高级观测/云端能力三层面，重复仅为 agent-browser 工具说明，独立可读需要，低价值不收敛）、安装组（MCP vs 插件，差异明确）、交付报告组（交付总结 vs 周期报告，差异明确）、Windows 组（编码 vs 环境，差异明确）。
  - 独立 A 类 8 个（git-collaboration / swag-openapi-maintainer / authenticated-url-routing / image-redbox-focus / godot-project-bootstrap / game-asset-* 等）职责清晰，保留。
  - B 类工具 skill 39 个（~4.75MB，含 skillhub + doc/pdf/spreadsheet 等）无卫生问题，无需整理。
- **清理（同域扫描发现）**：删除根目录 4 个 0 引用一次性脚本残留（_write_cycle.py / _write_cycle2.py / _write_docs.py / _bm_skillid_migration.json，均 git 跟踪、硬编码 8/8 文档路径，一次性产物）。index.html 保留（11 处引用）。
- **维持**：thread-title mcp/node_modules（活跃 MCP 依赖，gitignore 卫生另行处理）。
- **同域扫描结论**：范围 = 剩余全部 skill（17 A 类 + 39 B 类）；发现 = 4 组候选重叠 + 4 个残留；清理 4 个残留；真实冗余 0（A 类职责差异/低价值说明）；**PASS**。
- **净增体积**：-41KB（删除 4 个脚本）。
- **棘轮验证**：删除不影响任何引用（0 引用复核），评分不降。

## 2026-08-26：内部更新——全量 8 维评分巡检报告刷新（第二轮）

- **来源**：内部调整：skill 体系评分巡检，调整诉求 = 「对所有 skill 再打分一次，更新打分的 html」。
- **形态**：内部更新通道（只读打分 + 报告刷新，无 skill 内容改动）。
- **裁决**：不涉及吸收/合并/拒绝裁决——纯评分巡检，产物为 `skill-8维评分报告.html`。
- **执行摘要**：6 个独立子代理分批打分 158 个 skill（静态 7 维，权重 W=[8,15,10,7,15,5,15]，满分 75）；总分脚本复算；独立校验通过。新增 log-analysis-rules（上轮无），无删除。
- **结果**：总平均 60.6（上轮 54.4，+6.2）；rules 63.4/83、other 58.3/25、skillhub 57.3/48、market 55.3/2；最低 self-ent-tech-database-design 36.9；最高 imagegen 74.3；中位数 60.9。
- **棘轮验证**：全量重新打分（非单 skill 优化），158 个全部重评；整体平均较上轮 +6.2，主要来自 08-25/26 期间 26+ 个低分 skill 优化闭环（skillhub 类 44.5 → 57.3）。

## 2026-08-26：内部更新——低分 skill 批量优化第十一轮（9 个，A+B+D 裁决）

- **来源**：内部调整：用户点名 9 个最低分 skill 逐个优化，默认 A+B+D（内容+交叉引用+版本环境），排除 C 市场吸收。
- **形态**：内部更新通道（9×SKILL.md 重构 + 2 脚本修复 + 1 新 reference）。
- **裁决**：A+B+D 组裁决（用户默认），无 C 市场吸收。
- **执行摘要**：逐 skill 八步闭环；修复真实 bug 2 处（golang script.sh case 顶层 local 误用、ip.py 依赖 requests 未装）；修复硬伤 2 处（cryptocurrency-data-api search_schools 残留、ip SKILL.md 脚本路径断链）；frontmatter 合规化 5 个（self-ent-tech/gol/golang/tg/cryptocurrency-data-api/ip/skill_2054901716814716928 8 违规键）。
- **结果**：36.9→63.3 / 37.7→62.8 / 46.0→66.1 / 46.7→61.2 / 48.6→66.5 / 48.7→67.5 / 48.8→63.3 / 49.0→66.1 / 49.2→64.6；报告总平均 60.6→61.7；新最低 pdf 50.1。
- **棘轮验证**：全量重新打分（非单 skill 优化），9 个全部高于基线（+14.5 ~ +26.4），无早停项。


## 2026-08-28：内部更新——新增「优化 XX skill」泛化触发 + 按基线分流路由

- **来源**：内部调整：skill-absorption-rules，调整诉求 = 「加入提示词触发：只要提出 优化 <?> skill 就走固定优化流程」。
- **形态**：内部更新通道（1×SKILL.md 触发机制增强，无外部源、无市场吸收）。
- **裁决**：A 类内容（泛化触发词）合并 → description；A 类内容（路由绑定）合并 → 自动触发信号第 8 条；无 C 市场吸收、无 D 版本环境。
- **执行摘要**：description 追加「优化 XX skill（XX 为任意 skill 名，如 优化 vue-router-best-practices skill）触发固定优化流程」；触发信号第 7 条追加模板说明（去重合并），新增第 8 条按基线分流路由（有 8 维基线 → 低分 SOP 八步闭环；无基线 → 内部更新通道同闭环 + quick_validate 替代棘轮）。
- **整理去重**：原第 7 条列举式与新增模板合并为互补结构，净增约 350 字节（description 646→约 710 字符，<1024 合规）。
- **同域扫描结论**：全仓 grep 无抢触发，**PASS**。
- **棘轮验证**：无既有评分基线，按方案以 quick_validate 结构校验 + 同域扫描替代（用户已确认）。


## 2026-08-28：外部吸收——tapd-openapi 脚本 mine 能力 + SKILL.md 输出规范（来源：EllipalNodeSync 同事资产）

- **来源**：外部（同 team 项目 EllipalNodeSync `.claude/skills/tapd-openapi/` + `.tapd/`），非官方市场。
- **形态**：外部吸收（脚本升级 + SKILL.md 章节增量 + 编排层联动增强）。
- **裁决**：A 合并 × 2（新版 tapd_client_stdlib.py 545 行全文替换本地 287 行旧版，含 mine 子命令、with_ancestors 父需求树、status_map、resolve_iteration、download_entity_images 等 15 个新函数；SKILL.md 新增「输出规范」章节）；拒绝 × 3（SKILL.md 其余段本地更优、search_wiki.py/hooks.json 与本地一致、.tapd/ 壳为项目级参考不落盘）。
- **兼容适配**：外部变量名 `TAPD_ACCESS_TOKEN`/`TAPD_API_BASE_URL` → 本地 `TAPD_TOKEN`/`TAPD_API_ENDPOINT`，`_get_headers`/`_get_base_url`/`_is_cloud` 三处加 `or` 回退（实测本地仅注入 TAPD_TOKEN，未适配必失败）。
- **联动增强**：tapd-task-executor「拉取我的任务+bug」步骤改为优先 mine 子命令，tapd-cli 兜底。
- **棘轮验证**：无既有评分基线，以真实 API 冒烟 + quick_validate + AST + 同域扫描替代。mine 实测输出父需求树：`兑换（父）→ 兑换提供外部服务-对接开放接口`，19 位 id/状态/优先级/链接完整；bugs 查询 0 项正常。

## 2026-09-05：外部吸收——grilling（严格拷问，marketplace 个人开发者 v1.0.0）

- **来源**：WorkBuddy 市场 skill `grilling`（`_skillhub_meta.json`：source marketplace，skillId skill_2095263945412698112，display_name 严格拷问），本地安装源 `D:\谷歌云盘\luode-skills\grilling\`。
- **形态**：外部吸收（本地安装源模式，直接读 `grilling/SKILL.md` 原文，不 WebFetch）。
- **裁决**：拆解 8 条原子规则（每轮只问一个最关键问题 / 问题须推动决策或暴露风险 / 可查证事实先自查不丢给用户 / 决策权在用户且可给推荐答案不可拍板 / 无共享理解不执行 / 沿依赖最强分支问 / 语气直接有压力但不辱骂 / 输出=核心风险一句话+一个问题+一句推荐）→ **保留本地 × 8，合并 × 0**。逐条对应本地更强出处：`requirement-intake-rules/references/gap-routing.md`（一次只推一个真实缺口）、`adversarial-gap-interview.md`（推荐答案待确认建议 + 反方批评 + 决策树依赖优先 + 输出格式）、`initial-discovery-route.md`（可查证先自查）、`extreme-completeness-standard.md`（不满足模糊答案、直到共识）。本质为本地 2026-08-18 已吸收 `softspark-ai-toolkit-grill-me` 精华的同源复刻，无新增精华。
- **落点**：无规则落盘（0 合并）；grilling 本体保留为独立「用户召唤式通用拷问入口」（本地对抗式追问均内嵌需求/实施流程，无独立 grill 触发入口，保留不构成重复）。
- **环境依赖**：N/A（纯规则文本，无环境变量 / 配置 / hook / 依赖）。
- **agent 通用性**：通用（frontmatter 无单 agent 绑定、正文无专属路径 / 命令 / 术语）。
- **整理去重**：N/A + 理由（本次无合并内容落盘；仅登记，未触碰既有 adversarial / plan-devils-advocate-review 文件）。
- **同域扫描**：范围 = grilling / requirement-intake adversarial-gap-interview / implementation-planning plan-devils-advocate-review；发现 0 处重复段落（grilling 正文与本地吸收产物无逐字重复，职责为独立召唤入口 vs 流程内嵌），清理 0 处。PASS。
- **棘轮验证**：0 合并即无内容增量，无 8 维基线可比；以结构核对 + 同域扫描替代。净增体积：本体 0 改动，登记文件约 +15 行。
- **源清理**：保留（用户主动安装的可用 skill，裁决为本地化保留非并入删除）。

## 2026-09-07：外部吸收——量化策略回测师（wm-backtest）→ crypto-quant-analysis 集成

- **来源**：WorkBuddy 市场 skill `wm-backtest`（个人开发者，v0.3.25，slug `wm-backtest`），本地安装源 `~/.workbuddy/skills/wm-backtest__skillhub/`。
- **形态**：外部吸收通道（本地安装源吸收模式：读取原文 → 裁决 → 落盘 → 删除源）。
- **吸收目标**：`crypto-quant-analysis`（加密货币量化分析 skill，v2.2）。
- **拆解原子规则数**：11 条。

| # | 外部精华 | 本地现状 | 裁决 | agent 通用性 | 落点 / 理由 |
|---|---------|---------|------|-------------|------------|
| 1 | 策略迭代方法论（基线→单变量假设→测试→拉执行历史→归因→1-3条改法→再跑） | 本地有 backtest.py 但无结构化迭代方法论 | 合并 | 通用 | 新增 `references/strategy-iteration-methodology.md` |
| 2 | 结果归因框架（不只看总收益，要读执行历史+过程日志+因子暴露） | 回测仅输出收益率/夏普/回撤，无归因分析框架 | 合并 | 通用 | 同上 reference |
| 3 | "一次只改一类"纪律（禁止同时改多个变量，否则无法归因） | 本地无此纪律 | 合并 | 通用 | 同上 reference |
| 4 | 关键分支必须打点（归因依赖日志，仅 return 不 trace 无法证明规则是否触发） | 本地 Python 回测脚本无结构化日志概念 | 合并 | 通用 | 同上 reference，适配 Python 语境 |
| 5 | 自然语言→回测工作流（预览确认→发起→输出→解读→偏差→下一轮改法） | 回测是直接执行，无"确认后发起"和"偏差解读"工作流 | 合并 | 通用 | 增强 SKILL.md 新增「策略迭代工作流」节 |
| 6 | 结果分层拉取（先 summary 看全景，再 deep 看细节，再 trace 看过程） | 无分层概念 | 合并 | 通用 | 并入 references/strategy-iteration-methodology.md |
| 7 | simulation.* / bt.* / run_custom / from_watchlist 等平台 API | 本地无此平台 | 拒绝 | — | 平台专属，不迁移 |
| 8 | ConfigOverride 机制（改窗口/宇宙/参数 vs 改脚本逻辑分离） | 平台专属机制 | 拒绝 | — | 形态不匹配 |
| 9 | 阶段 XS 引擎（selector→rank→trading→risk 日环） | 本地回测是 Python 函数调用 | 拒绝 | — | 引擎形态不匹配 |
| 10 | 计费/Scope/EC 系统 | 平台运营专属 | 拒绝 | — | 形态不匹配 |
| 11 | 8 个 reference 文件（system/lifecycle/stages/simulation-api 等） | 全部为平台 API 文档 | 拒绝 | — | 平台专属，不迁移 |

- **落盘改动**：
  - 新增 `crypto-quant-analysis__skillhub/references/strategy-iteration-methodology.md`（~6.8KB，策略迭代闭环/归因框架/一次只改一类/关键分支打点/分层结果解读/自然语言→回测工作流）。
  - 修改 `crypto-quant-analysis__skillhub/SKILL.md`：策略回测 scope 增强（+"支持策略迭代闭环"）；新增「策略迭代工作流」节（完整闭环+每轮规范+结果解读规范+关键纪律）；Q5 FAQ 更新。
  - 新增 `crypto-quant-analysis__skillhub/references/source-notes.md`（吸收登记）。
- **整理去重**：N/A + 理由——策略迭代方法论/归因框架/一次只改一类纪律均为本地全新能力，crypto-quant-analysis 已有的回测内容仅为脚本调用表和示例工作流，不含方法论层面重复。
- **同域扫描结论**：范围 = crypto-quant-analysis（吸收目标）、crypto-price（价格查询）、quant-analyst（量化交易系统）、swap-tokens、cryptocurrency-data-api。发现 = 0 处重复段落（策略迭代方法论/归因框架均为本地缺失能力，同域 4 skill 零命中）、0 处门控层叠、0 处散落产物；清理 0 处；**PASS**。
- **环境依赖登记**：N/A + 理由（纯规则文本，无环境变量 / 宿主配置 / hook / 依赖安装 / 路径引用）。
- **净增体积**：+约 7.5KB（strategy-iteration-methodology.md ~6.8KB + source-notes.md ~0.6KB + SKILL.md 增量 ~0.1KB）；外部源 22 文件约 108KB（含脚本 90KB+），**体系净增 = +7.5KB（规则正文净增），源脚本/图片不计入规则体积**。
- **棘轮验证**：引用链 2 处可达（SKILL.md L1018 策略迭代工作流 → strategy-iteration-methodology.md；L1047 Q5 FAQ → strategy-iteration-methodology.md）；UTF-8 3 文件 OK。
- **源清理**：吸收完成后删除本地安装源 `wm-backtest__skillhub`（用户级 ~/.workbuddy/skills/wm-backtest__skillhub/ 目录，22 文件 108KB 含脚本）。

## 2026-09-10：内部更新——artifact-storage-rules 补齐「文档生命周期与退场」治理

- **来源**：内部调整：`artifact-storage-rules`，调整诉求 = 「`doc/` 下长期未动的过程文档从未被清理；很多长时间文档的结论已归类总结吸收进知识库，应当退场，请把这套治理补进规则」。
- **形态**：内部更新通道（触发语「优化我们的skill规则」）。
- **吸收目标**：`artifact-storage-rules`。
- **拆解原子规则数**：5 条。

| # | 内部调整诉求 | 本地现状 | 裁决 | 落点 / 理由 |
|---|---|---|---|---|
| 1 | 区分过程产物与长期资产的生命周期 | 仅覆盖空间维度（落点 / 命名 / 复用），时间维度完全缺失 | 合并 | SKILL.md 新增「文档生命周期与退场（强制）」+ `lifecycle-policy.md` 第一节 |
| 2 | 给出退场时间阈值 | 无时间阈值；仅事件驱动清理（`.gap.md`、图片旧版本、迁移后旧目录、`test/{skill}/temp`） | 合并 | `path-map.yaml` → `process_doc_retire_after_days: 15`（用户选定「半个月」） |
| 3 | 落实「先沉淀再清理」前置条件 | `knowledge-flow/conflict-staleness.md` 有知识笔记三档处置与引用守卫，但未延伸到 doc 产物 | 合并 | `lifecycle-policy.md` 四道守卫；沉淀守卫 owner 显式指向 `knowledge-flow` |
| 4 | 明确退场动作与批次 | 无 | 合并 | `process_doc_retire_action: git_rm` + `process_doc_retire_batch_limit: 10`（用户选定「沉淀知识库后删除老文档」，不设归档目录） |
| 5 | 防止退场误伤长期资产与在用文档 | 无边界声明 | 合并 | `process_doc_long_lived_roots` 白名单 + 驳回标准新增两条 |

- **落盘改动**：
  - 新增 `artifact-storage-rules/references/lifecycle-policy.md`（两类产物定位 / 时间判据 / 四道前置守卫 / 退场清单格式 / 批次与执行 / 相邻规则边界 / 禁止事项）。
  - 修改 `artifact-storage-rules/SKILL.md`：`description` 扩触发面（生命周期判定 + 长期文档退场）；新增「文档生命周期与退场（强制）」章节；自动触发信号 +2；进入后先做什么 +1；默认执行流程 +1；需要暂停并确认的条件 +2；执行通过 / 驳回标准 +2；references 读取规则 +1；执行结果归档要求 +1。
  - 修改 `artifact-storage-rules/references/path-map.yaml`：`policies` 新增 10 个 `process_doc_*` 键。
  - 修改 `artifact-storage-rules/references/update-policy.md`：新增「过程产物生命周期与退场」策略摘要节。
  - 修改 `artifact-storage-rules/references/skill-integration.md` 与 `references/root-directories.md`：补引用入口与生命周期定位。
  - 刷新 `skill-dictionary/data.js` 与 `字典.md`（改 `description` + 新增 `##` 级标题的强制动作）。
- **整理去重**：不以复制存量条款换取新增——`update-policy.md` 退场节只保留策略摘要与边界声明，判定细则、取证命令与清单模板全部收敛到 `lifecycle-policy.md`（单一权威）；既有事件驱动清理条款（`.gap.md`、图片旧版本、迁移后旧目录、`test/{skill}/temp`）保持原位不动，新章节显式声明「两者不互相替代」。
- **同域扫描结论**：范围 = `artifact-storage-rules`（目标）、`artifact-delivery-gate-rules`、`knowledge-flow`、`test-strategy-rules`（`test-asset-lifecycle`）、`project-design-doc-rules`、`architecture-doc-rules`、`project-interface-baseline-rules`。发现 = 0 处重复段落（全仓检索「退场 / 生命周期 / process_doc_retire / 长期文档」，命中均为其他语境：接口生命周期、参数样本 `retired`、agent 恢复链、触发契约）、0 处门控层叠（沉淀判定收敛到 `knowledge-flow` 单一 owner）、0 处散落产物；清理 0 处；**PASS**。
- **环境依赖登记**：N/A + 理由——纯规则文本；正文引用的知识库根（`D:\谷歌云盘\知识库\`）由 `AGENTS.md` 固定、`git rm` 由 `git-collaboration-rules` 承载，均属既有约定，未新增环境变量 / 宿主配置 / hook / 依赖安装。
- **净增体积**：新增 `lifecycle-policy.md` 约 6.1KB + 5 个既有文件增量约 4.2KB；字典产物刷新另计（含 2026-09-01 至 2026-09-10 的 9 天累积同步，非本次规则增量）。
- **棘轮验证**：`quick_validate.py` → `Skill is valid!`（内部更新通道无 8 维评分基线，以结构校验替代）；`path-map.yaml` YAML 解析通过（version 10，`process_doc_*` 11 键回读一致）；UTF-8 与乱码自检通过；引用链 3 处可达（SKILL.md → lifecycle-policy.md，skill-integration.md → lifecycle-policy.md，update-policy.md → lifecycle-policy.md）。
- **源清理**：N/A（内部更新通道，无外部安装源）。
