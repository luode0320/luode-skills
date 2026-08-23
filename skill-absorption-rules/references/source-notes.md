# 来源记录（source-notes）

> 归属 owner：`skill-absorption-rules`。追加每次吸收的来源与落点，可回指原始仓库 / 市场 / 版本。

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
