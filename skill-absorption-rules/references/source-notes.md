# 来源记录（source-notes）

> 归属 owner：`skill-absorption-rules`。追加每次吸收的来源与落点，可回指原始仓库 / 市场 / 版本。

## 2026-08-26：内部调整——测试进程生命周期强制收口

- **来源名称**：无外部源（内部更新通道）；调整诉求 = "测试任务结束后必须强制关闭测试启动的进程，禁止遗留后台；用户需要时自行启动"。
- **获取方式**：内部调整（经验事实源为本次 ellipal_admin 合作方新字段同步任务的真实链路测试——12801 被测服务在测试收口后仍留后台，用户指出应强制关闭，非外部 skill 源）。
- **吸收落点**：
  - `test-strategy-rules/SKILL.md`（修改）：新增《测试进程生命周期（强制）》节，作为测试域进程生命周期的单一权威来源（测试收口必关 / 核验可证 / 不替用户保留 / 残留清理 / 联调衔接）。
  - `functional-validation-rules/SKILL.md`（修改）：联调节第 6 条补引用指针指向权威节。
  - `browser-advanced-testing-rules/SKILL.md`（修改）：联调节第 6 条补引用指针指向权威节。
- **裁决表**：`workbuddy-absorption-map.md`（2026-08-26 内部更新条目）。
- **环境依赖登记**：N/A（纯规则文本）。
- **源清理**：N/A（内部更新通道，无外部源可删）。

## 2026-08-26：内部调整——低分 skill 优化 SOP 固化（八轮经验总结）

- **来源名称**：无外部源（内部更新通道）；调整诉求 = "八轮低分 skill 优化（7 个 skill：24.7~33.4 → 62.6~69.0）的实操经验总结成标准流程，后续评分巡检中的低分 skill 都按此流程优化；经验吸收进本 skill"。
- **获取方式**：内部调整（经验事实源为知识库笔记《Windows-WSL命令失败恢复与Skill持续迭代.md》八轮完整记录 + 本项目 8 轮会话实操，非外部 skill 源）。
- **吸收落点**：
  - `skill-absorption-rules/references/low-score-skill-optimization-sop.md`（新建，6306B）：触发信号 / 八步闭环表 / 短板类型学 7 类映射 / 市场检索规律 / 验证纪律 / 实操坑 / 单轮收口清单 / 与 darwin-rubric、score-inspection-workflow、skill-audit-rules 边界。
  - `skill-absorption-rules/SKILL.md`（修改）：自动触发信号补 1 条（"总结多轮实操经验成标准流程"）+ references 读取规则补 1 条（低分 skill 优化闭环读 SOP）。
  - `skill-absorption-rules/references/score-inspection-workflow.md`（修改）：短板识别节自有 rules/other 出口补指向 SOP 的衔接句。
- **裁决表**：`workbuddy-absorption-map.md`（2026-08-26 内部更新条目）。
- **环境依赖登记**：N/A（纯规则文本）。
- **源清理**：N/A（内部更新通道，无外部源可删）。

## 2026-08-24：内部调整——8 维评分体系巡检工作流固化

- **来源名称**：无外部源（内部更新通道）；调整诉求 = "把「用 darwin-rubric 8 维给全仓库 skill 打分 + 生成 skill-8维评分报告.html」的实操经验固化为可复用流程，后续快速打分更新报告"。
- **获取方式**：内部调整（本次实操经验来自 2026-08-24 全量巡检打分，非外部 skill 源）。
- **吸收落点**：
  - `skill-absorption-rules/references/score-inspection-workflow.md`（新建）：体系评分巡检完整流程（触发信号 / 范围四分类 / 并行子代理分批打分 / 固定输出格式 / 短板识别 / 报告固定文件与结构约定）。
  - `skill-absorption-rules/SKILL.md`（修改）：references 读取规则补 1 条（体系评分巡检读 score-inspection-workflow.md）。
  - `skill-absorption-rules/references/darwin-rubric.md`（修改）：第 60 行「体系巡检」处补指向 score-inspection-workflow.md 的引用。
- **裁决表**：`workbuddy-absorption-map.md`（2026-08-24 内部更新条目）。
- **环境依赖登记**：N/A（纯规则文本）。
- **源清理**：N/A（内部更新通道，无外部源可删）。

## 2026-08-23：skill-merger（技能合并器）

- **来源名称**：技能合并器（mimo-skill-merger）
- **获取方式**：skillhub 安装源（用户级 + 工作区 junction 同一物理目录，`mimo-skill-merger__skillhub`，version 1.3.0，MIT-0，homepage qqyougitcom/mimo-skill-merger）
- **来源描述**：多技能合并工具——吸收型/融合型/编排型三策略 + 冲突处理（触发词双列）+ 变更对比模板 + 反合理化表。吸收目标为 skill-absorption-rules 自身，补齐「内部更新通道」的多技能合并执行细则（本地此前仅有触发信号"把这两个 skill 合并"，无策略框架）。
- **原始文件**：`SKILL.md`（74 行）+ `references/details.md`（24 行）+ `skill-card.md`
- **吸收落点**：
  - `skill-absorption-rules/references/merge-strategies.md`（新建）：三策略 + 冲突处理 + 变更对比模板 + 反合理化表 + 同域边界。
  - `skill-absorption-rules/SKILL.md`（修改）：三通道表格内部更新通道行 + references 读取规则。
- **裁决表**：`workbuddy-absorption-map.md`（2026-08-23 skill-merger 条目）。
- **环境依赖登记**：N/A（纯规则文本）。
- **源清理**：吸收完成后删除本地安装源 `mimo-skill-merger__skillhub`（junction 双路径验证均不存在）。

## 2026-08-23：qa-bug-root-cause-analysis（缺陷根因分析）

- **来源名称**：缺陷根因分析（qa-bug-root-cause-analysis）
- **获取方式**：skillhub 安装源（用户级 + 工作区 junction 同一物理目录，`qa-bug-root-cause-analysis__skillhub`，version 1.7.0）
- **来源描述**：QA Test Skills 技能集（49 个之一，作者 Kokxi/qa-test-skills）——从症状出发，用症状分类映射、现象速查表、排查顺序、根因分层等方法系统化定位缺陷根源。⚠️ 源 skill 声明"完整工作流体验需安装全套 12 步工作流"，本次仅吸收根因分析精华到本地 Bug 域。
- **原始文件**：`SKILL.md`（328 行）
- **吸收落点**：
  - `bug-root-cause-rules/references/symptom-rootcause-map.md`（新建）：五类症状→根因方向映射 + 现象速查表 + 排查顺序 + 根因分层 + 脱敏注意事项。
  - `bug-root-cause-rules/SKILL.md`（修改）：默认执行流程第 3 步 + references 读取规则登记。
  - `bug-root-cause-rules/references/root-cause-catalog.md`（修改）：顶部症状层入口衔接。
- **裁决表**：`workbuddy-absorption-map.md`（2026-08-23 qa-bug-root-cause-analysis 条目）。
- **环境依赖登记**：N/A（纯规则文本）。
- **源清理**：吸收完成后删除本地安装源 `qa-bug-root-cause-analysis__skillhub`（junction 双路径验证均不存在）。

## 2026-08-23：browser-use API + guide 合并吸收

- **来源名称**：Browser Use API（browser-use-api）+ browser-use AI浏览器自动化（browser-use-guide）
- **获取方式**：skillhub 安装源（仓库根 + 用户级 junction 同一物理目录，`browser-use-api__skillhub` / `browser-use-guide__skillhub`，均 1.0.0）
- **来源描述**：browser-use.com 云端浏览器自动化的操作层资料——REST API v2 端点与 shell 助手（API 版）+ 完整指南含开源库/CLI/OpenClaw/云端对比（guide 版）。用户决策：合并为 `browser-use-cloud-rules` 的 REST 操作通道，凭据统一存 `~/.browser-use/.env`，定位为"项目程序操作公网（https 域名）浏览器"。
- **原始文件**：`browser-use-api__skillhub/SKILL.md`（99 行）+ `scripts/browser-use.sh`（88 行）；`browser-use-guide__skillhub/SKILL.md`（380 行）
- **吸收落点**：
  - `browser-use-cloud-rules/references/api-operations.md`（新建）：REST v2 端点/状态机/curl/Python 集成/模型定价/边界。
  - `browser-use-cloud-rules/scripts/browser-use.sh`（新建）：`~/.browser-use/.env` 密钥 + `--check/--balance`。
  - `browser-use-cloud-rules/scripts/.env.example`（新建）：密钥模板。
  - `browser-use-cloud-rules/SKILL.md`（修改）：触发扩展、凭据策略、REST 通道、环境自检、References。
  - `browser-use-cloud-rules/references/routing-and-safety.md`（修改）：MCP 凭据来源口径。
- **裁决表**：`workbuddy-absorption-map.md`（2026-08-23 browser-use 条目）。
- **环境依赖登记**：`workbuddy-env-manifest.md` 第 9 项（`~/.browser-use/.env`）。
- **源清理**：吸收完成后删除本地安装源 `browser-use-api__skillhub` 与 `browser-use-guide__skillhub`（仓库根 + 用户级 junction 双路径各删一份）。

## 2026-08-23：内部调整——环境依赖吸收（跨机器自愈）

- **来源名称**：无外部源（内部更新通道）；调整诉求 = "吸收 skill 时同步吸收环境配置 / hook / 依赖，换电脑缺失自动检测并自动补齐"。
- **获取方式**：内部调整（平台配置事实来源于 WorkBuddy 官方文档 env-vars + 本机现网部署，非外部 skill 源）。
- **吸收落点**：
  - `skill-absorption-rules/SKILL.md`（修改）：环境依赖吸收升级（设计内核 + 默认流程第 4 步 + 收口说明 + 通过/驳回标准 + references 读取规则 3 条）。
  - `skill-absorption-rules/references/workbuddy-env-manifest.md`（新建）：8 项 WorkBuddy 平台配置单一权威清单（autoCompactEnabled / hooks.Stop×2 / 4 个环境变量 / 2 个 hook 文件）。
  - `skill-absorption-rules/references/env-dependency-absorption.md`（新建）：五类环境依赖吸收指引（环境变量 / 宿主配置 / hook·插件·MCP / 依赖安装 / 路径引用）。
  - `skill-absorption-rules/scripts/env-bootstrap-check.py`（新建）：跨机器 `--check / --dry-run / --fix` 三模式自愈脚本。
  - `skill-absorption-rules/assets/hooks/summary-check.py`、`ralph-stop.py`（新建）：用户级现网 hook 资产副本（md5 一致）。
- **裁决表**：`workbuddy-absorption-map.md`（2026-08-23 条目）。
- **源清理**：N/A（内部更新通道，无外部源可删）。

## 2026-08-22：调试（debugging）

- **来源名称**：调试（Systematic bug diagnosis and resolution）
- **获取方式**：marketplace 安装源（仓库根 + 用户级 junction 同一物理目录，`debugging-skillhub__skillhub`）
- **来源描述**：通用系统化调试方法论——reproduce → isolate → diagnose → fix → verify 五步工作流 + 6 条最佳实践 + 5 类边界场景（Heisenbug / 环境特定 / 第三方库 / runtime / 损坏状态）+ 跨语言工具参考表。
- **原始文件**：`SKILL.md`（194 行）
- **吸收落点**：
  - `bug-root-cause-rules/references/root-cause-catalog.md`（新建）：常见根因类别清单（输入假设/并发状态/缓存过期/运算符优先级/缺失 await/依赖版本/无界内存容器）+ 第三方库/runtime/数据损坏三类边界场景 + 区分根因与症状。
  - `bug-root-cause-rules/references/static-analysis-path.md`（修改）：补堆栈阅读纪律 + 先查最近变更 + 二分隔离/stub 排除三节。
  - `bug-intake-rules/references/runtime-diagnostics-bug-runtime-debug-rules-runtime-observation-methods.md`（修改）：补 Heisenbug 场景节 + 跨语言工具参考表。
  - `bug-reproduction-rules/references/stability-checks.md`（修改）：补环境特定 Bug 匹配复现节。
- **裁决表**：`workbuddy-absorption-map.md`（2026-08-22 条目）。
- **源清理**：吸收完成后删除本地安装源 `debugging-skillhub__skillhub`（仓库根目录）。

## 2026-08-22：diagnose

- **来源名称**：diagnose（Disciplined diagnosis loop）
- **获取方式**：marketplace 安装源（仓库根 + 用户级 junction 同一物理目录）
- **来源描述**：系统化调试六阶段闭环——反馈回路（reproduce → minimise → hypothesise → instrument → fix → regression-test），核心是「反馈回路优先」元方法论。
- **原始文件**：`SKILL.md`（125 行）+ `_skillhub_meta.json`
- **吸收落点**：
  - `bug-reproduction-rules/references/feedback-loop.md`（新建）：反馈回路核心 + 10 种构建方式 + 迭代三问 + 非确定性复现率 + 无法构建回路处理 + 复现三确认 + 性能回归测量。
  - `bug-root-cause-rules/references/hypothesis-ranking.md`（新建）：3-5 排序假设 + 可证伪预测 + 给用户看。
  - `bug-intake-rules/references/runtime-diagnostics-bug-debug-log-rules-debug-log-placement.md`（修改）：补调试日志唯一前缀标签机制。
  - `test-regression-rules/references/correct-seam.md`（新建）：正确接缝定义 + 无接缝即发现 + 修复前失败测试 + 重跑原始场景 + 收尾清单。
  - `bug-validation-rules/references/post-mortem.md`（新建）：修复后复盘「什么能阻止这个 Bug」。
- **裁决表**：`workbuddy-absorption-map.md`（2026-08-22 条目）。
- **源清理**：吸收完成后删除本地安装源 `diagnose`（仓库根目录）。

## 2026-08-19：java-story-develop__skillhub

- **来源名称**：java-story-develop（Java Story Develop）
- **获取方式**：LobeHub Skill 安装包，本地安装（工作区 + 用户级 `java-story-develop__skillhub` 目录）
- **来源描述**：项目环境秒级感知 + 全栈双端通吃，SIMPLE/QUICK/FULL 三种工作模式，主动记忆、角色互搏、异常恢复、11 项编码准则、文档沉淀与复盘检查。
- **原始文件**：`SKILL.md`（1153 行）+ `references/coding-standards.md`（11 节编码规范）+ `references/templates/`（1-Requirement / 2-Analysis / 3-Design / S-Simple / context.json）+ `references/examples/`
- **吸收落点**：
  - `project-memory-rules/references/environment-probe.md`（新建）：环境探测清单 + 记忆固化格式。
  - `requirement-intake-rules/references/workload-mode-routing.md`（新建）：SIMPLE/QUICK/FULL 三档规模分档路由。
  - `requirement-intake-rules/references/adversarial-gap-interview.md`（追加）：设计阶段双角色自检小节。
  - `skill-absorption-rules/SKILL.md`（修改）：固化「本地安装源吸收」流程（读取本地原文 → 吸收 → 删除源）。
- **裁决表**：`workbuddy-absorption-map.md`（2026-08-19 条目）。
- **源清理**：吸收完成后删除本地安装 `java-story-develop__skillhub`（工作区 + 用户级）。

## 2026-08-25 · 内部调整：记忆计数锚点链路「从写得进去到读得出来」

- **通道**：内部更新 + 执行中 gap 回补（无外部源，无需源清理）。
- **调整诉求**：用户要求把某存量项目首次启用计数锚点时暴露的问题，吸收进规则 md 同步 skill 与脚本，使下次更新规则 md 时同类问题被同步处理。
- **来源事实**：该项目 `PROJECT_MEMORY.md` 机器索引区 yaml 长期整块解析失败（3 处反引号开头裸标量 + 2 处 `- *_test.go`），16 个实体一个读不到；两个读取脚本 `except: return {}` 静默降级，扫描仍报 `candidates: []` 且退出码 0。
- **裁决**：7 条原子条目全部「合并」，0 条保留现状，0 条拒绝。
- **吸收落点**：
  - `memory-usage-tracking-rules/scripts/check_memory_anchors.py`（新建）：C1~C5 五项结构健康检查，`--list-missing` 出回补清单。
  - `memory-usage-tracking-rules/scripts/{usage_ledger_validate,scan_absorption_candidates}.py`（修改）：解析失败改抛 `AnchorParseError` + 退出码 2，不再静默返回空。
  - `memory-usage-tracking-rules/SKILL.md`（修改）：计数回写两级前置校验 + 新增「存量项目锚点回补（强制）」。
  - `memory-usage-tracking-rules/references/usage-anchor-schema.md`（修改）：新增第 0 节「写入约束：中文技术内容的 yaml 裸标量」+ 脚本解析契约补第三个脚本与「解析失败不得静默」。
  - `project-rule-file-bootstrap-rules/scripts/bootstrap_agents.sh`（修改）：三处 `counted_files` 模板补全 + 「键在但内容不全」`[WARN]`。
  - `project-rule-file-bootstrap-rules/SKILL.md`（修改）：Schema 变更强制检查新增「解析器判据」与「存量项目回补」，统一执行步骤新增 4.1 锚点健康检查（每次都跑）。
  - `project-memory-rules/SKILL.md` + `references/memory-index-schema.md`（修改）：计数字段 3→4 补 `usage_days`，`counted_files` 副本补全。
  - `project-rule-file-bootstrap-rules/references/项目记忆模板/四件套模板.md`（修改）：模板副本补全。
- **整理去重**：删除 2 处 `except: return {}` 静默降级；`counted_files` 的 5 份字面副本从「各自维护」收敛为「schema 为权威 + `check_memory_anchors.py` 校验副本」，不新增第 6 份。净增 1 个脚本。
- **同域冗余扫描**：范围 memory-usage-tracking / project-rule-file-bootstrap / project-memory / project-style；重复段落 0、门控层叠 0、散落产物 0（fixture 已清理）、引用链 18 处一致无断链。**PASS**。
- **验证**：新脚本正向 `ok=true`（16/26/20）+ 双 fixture 负向覆盖 C1~C5；坏样本下两读取脚本退出码 2；真实自举三路径全通过；三脚本回归与基线一致。
- **裁决表**：本条即裁决登记（目标 skill 无 `workbuddy-absorption-map.md`，不为单次内部调整新建该文件，避免散落产物）。

## 2026-08-26 · 内部调整：全量 8 维评分巡检第二轮（157 → 158 skill，报告刷新）

- **通道**：内部更新（评分巡检报告刷新，无外部源，无需源清理）。
- **调整诉求**：用户要求「对所有 skill 再打分一次，更新打分的 html」——第二轮全量评分巡检。
- **执行**：6 个独立子代理并行分批打分（每批约 26 个，darwin-rubric 静态 7 维，维度 8 未实测）；当前 158 个含新增 log-analysis-rules，无删除；总分由脚本按权重 W=[8,15,10,7,15,5,15] 复算，不以子代理手算为准。
- **结果**：总平均 60.6（上轮 54.4，+6.2）；rules 63.4（83）、other 58.3（25）、skillhub 57.3（48）、market 55.3（2）；中位数 60.9；最低 self-ent-tech-database-design__skillhub 36.9，最高 imagegen 74.3。
- **产物**：`skill-8维评分报告.html` 覆盖更新（D 数组 158 行 + 副标题/按钮数字同步）。
- **验证**：Python 独立复算 158 行/分类计数/平均分/最低最高/中位数全部一致；维度界 1-10 全通过；旧数字无残留。

## 2026-08-26 · 内部调整：低分 skill 批量优化第十一轮（9 个，A+B+D 裁决）

- **通道**：内部更新（用户点名 9 个低分 skill 按顺序逐个优化，默认 A+B+D 组裁决，无外部源、无市场吸收）。
- **调整诉求**：用户列出评分报告最低 9 个 skill（36.9-49.2），要求「按照顺序，一个一个 skill 优化他们，直到这些都优化完成，默认都是 A+B+D」。
- **执行**：逐 skill 八步闭环（基线核验→实测→落盘→quick_validate→统一独立复评）。清单：self-ent-tech-database-design（36.9→63.3，frontmatter 空键致 YAML 解析失败 + 缺触发词/资源）、goal（37.7→62.8，纯命令入口补流程边界）、golang（46.0→66.1，脚本 12 处 case 顶层误用 local 全命令写入损坏 + 宣称构建工具实为日志工具）、frontend-design（46.7→61.2，补 5 步流程 + 2 确认检查点 + 删 comment-rules 三连重复）、tg（48.6→66.5，发送强制确认闸门 + 异常处理）、file-organize（48.7→67.5，补个人文件操作安全红线 + 分批移动 + 新建 references/category-map.md 资源）、skill_2054901716814716928（48.8→63.3，frontmatter 8 违规键合规化 + 删营销签名 + 补流程检查点）、cryptocurrency-data-api（49.0→66.1，工具表去重 + 修 search_schools 复制残留 + 补错误处理）、ip（49.2→64.6，脚本路径断链修复 + ip.py 去 requests 改标准库 + name 合规化）。
- **结果**：9 个全部提升（+14.5 ~ +26.4）；`skill-8维评分报告.html` 对应 9 行更新，总平均 60.6→61.7；新最低 pdf 50.1（原最低 self-ent-tech 36.9 出列）。
- **验证**：9×quick_validate `Skill is valid!`；golang 脚本 12 命令实测 Saved 全通过 + export 非法格式 exit=1；ip.py 无 key/缺参/非法 JSON/假 key 联网 4 分支实测通过；Node+Python 双端校验 158 行/总平均 61.7/分类计数（skillhub 48/rules 83/other 25/market 2）一致。
- **产物**：9 个 SKILL.md 重构 + 2 个脚本修复（golang script.sh、ip ip.py）+ 1 个新 reference（file-organize references/category-map.md）。
