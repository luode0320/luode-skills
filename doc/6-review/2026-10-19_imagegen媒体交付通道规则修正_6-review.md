---
schema_version: 1
doc_id: "REVIEW-20261019-04"
doc_type: style_regression
source_ids: []
status: accepted
version: v1.0
current_slice: "SLICE-IMAGEGEN-MEDIA-DELIVERY"
updated_at: "2026-10-19 22:55:00"
reader_level: business_general
writing_style: plain_chinese
appendix_policy: preserve_existing_or_one_terminal_appendix
complexity: L1
baseline_commit: 252f4e0f
template_version: v1
---

# 6-review 风格回归：imagegen 媒体交付通道规则修正

结论：本轮写法回归通过，`STYLE: PASS`。真实运行验证已完成（同一张图两次经 `present_visualization` 提交并返回成功快照；Qoder CN 客户端常量经 asar 二次复验）。本轮改动集中在 `imagegen` 的规则资产：重写工作流的交付通道优先级、新增一条客户端实证案例、同步变更日志。影响：后续所有生图交付在 Qoder 环境不再走 `data:` 内联，改为可视化通道。范围：只核对写法、位置、注释、编码、行数基准与目录归位。非范围：不判断生图模型质量与业务正确性。变化：修改 3 个文档文件（SKILL.md / CHANGELOG.md / error-casebook.md）。完成标准：六维逐项有磁盘证据，发现项已修复或登记。验证状态：结论来自真实命令输出、客户端 asar 复验与真实工具调用返回。

## 文档信息

- 来源任务：用户要求修正 imagegen 交付通道规则，并排查 `ffa5907c-03d0-4b72-9e85-021a1dfb41ad` 会话的生图不渲染问题。
- 回归时间：2026-10-19；执行环境：本机 Git Bash + Qoder CN 客户端。
- 图片资产决策：`N/A + 原因 + 证据`。原因：本轮只改规则文档，不产出新图。证据：`git diff --stat -- imagegen/` 只含 md/json/py 文档与脚本，无图片路径。
- 数据写入：`N/A`，理由：本轮未向任何数据库、缓存或消息队列写入数据。

## 六维交付残留自查

| 维度 | 结论 | 证据 |
|---|---|---|
| 维度 1 需求覆盖对账 | 通过 | 用户两项诉求均有落点：「修 skill 文档」→ `imagegen/SKILL.md:115-126`（三档通道优先级 + Qoder CN 禁用 `data:` + 拦截不可绕过 + 工具成功≠已渲染 + 全部失败兜底）；「排查 ffa5907c 渲染问题」→ 该会话转录第 419 行确认为同形态 `data:image` 内联，与原会话同根因，结论已写入 `imagegen/references/error-casebook.md` 的 `IMG-007`。本条六维审查本身落盘于本文件 |
| 维度 2 影响面 / 消费方对账 | 通过 | 交付规则是 skill 内部执行约定，不构成对外的数据结构/签名/配置键契约面。全仓扫描 `grep -rn "present_visualization" --include="*.md" .` 在 `imagegen/` 之外命中 0，说明无其它 skill 消费该口径需同步；`grep -rln "data:image/jpeg;base64"` 仅 `imagegen/SKILL.md` 定义内联交付规则，无跨 skill 重复权威。`present_files` 已核实为 Doubao 宿主工具（`doubao-creative-video/SKILL.md:21`），本宿主不提供，文案已改为「若宿主有原生媒体工具」的条件表述 |
| 维度 3 残留物清扫 | 部分遗留 | 本轮自建临时物已清理：`images/20261019221717/_viz_thumb.jpg`、`_viz2.jpg`、`_ffa_check.jpg` 均已在生成后删除；`git status --porcelain imagegen/` 无新增未跟踪文件。**遗留**：`images/20261019222901/inline.txt`（37,731 B，内容为 data URI）与 `imagegen-config-verify-v2-thumb.b64`（37,708 B）为 `ffa5907c` 会话产生的中间物，未被 git 跟踪、未被 `.gitignore` 覆盖；因属其它会话产物，本轮不擅自删除，登记为 P3 显式遗留，后续由用户或该会话清理 |
| 维度 4 文档与引用一致性 | 通过 | SKILL.md 内引用的 8 个资产全部存在：`references/cli.md`、`references/error-casebook.md`、`references/prompting.md`、`references/sample-prompts.md`、`references/source-notes.md`、`scripts/image_gen.py`、`scripts/imagegen.py`、`scripts/remove_chroma_key.py`；`error-casebook.md` 在 `imagegen/SKILL.md:243`（失败分流）与 `:250`（参考文件清单）双向可达；新增 `IMG-007` 被 `CHANGELOG.md` 2.4.0 条目引用 |
| 维度 5 口径一致性 | 通过（曾发现 2 项并已修复） | 发现 1：CHANGELOG 原写「三档降级链」但 SKILL.md 未标注档位序号 → 已在 SKILL.md 以 `1./2./3.` 编号对齐。发现 2：案例库 `验证` 字段原以「工具返回成功快照」作为展示成功证据，与 SKILL.md 新增的「工具成功≠用户已看见」自相矛盾 → 已改写为显式声明该证据不证明渲染，并要求用户侧确认。其余口径核对：`blockedProtocols` 四值（`javascript:` / `data:` / `file:` / `vbscript:`）在 SKILL.md:121 与 error-casebook.md:62 两处逐字一致；`1 MB` 限制在 SKILL.md:123 与 error-casebook.md:64 一致，且来源为本轮真实收到的工具报错原文「check the path, HTML fragment format and 1 MB size limit」 |
| 维度 6 验证有效性反审 | 通过（曾发现 1 项并已修复） | 反审发现：把 `present_visualization` 的返回成功当作「已渲染」是假阳性——工具语义只保证片段通过校验并保存快照。已在 `SKILL.md:126` 与 `error-casebook.md:64` 双处显式修正，并要求交付话术降级为「已提交可视化通道」。独立判据：`blockedProtocols` 与 `protocols.src` 白名单不是从本轮文档自证，而是二次回读客户端 `app.asar` 二进制原文复核（命中 `blockedProtocols=new Set(["javascript:","data:","file:","vbscript:"])` 与 `protocols:{...,src:["http","https"]}`）。未用 build/lint/静态搜索顶替真实运行：两次 `present_visualization` 均为真实工具调用且有返回 |

## 本轮发现项处置

| 发现项 | 处置 | 说明 |
|---|---|---|
| 案例库「验证」字段以工具返回值自证渲染成功 | 已修复 | 改写为「该证据不证明客户端已渲染，需用户侧确认」 |
| 案例库 `IMG-007` 缺 `环境/版本`、`发生次数`、`用户确认` 三个必填字段 | 已修复 | 按案例库字段规范补齐（`发生次数`：2，两个独立会话） |
| CHANGELOG「三档」与 SKILL.md 无编号对应 | 已修复 | SKILL.md 改为显式 `1./2./3.` 编号 |
| `present_files` 表述可能误导为通用工具 | 已修复 | 改为「其他宿主若有自己的原生媒体工具（如 Doubao 的 `present_files`）」，并附宿主归属出处 |
| `images/20261019222901/inline.txt` 与 `.thumb.b64` 残留 | 登记为显式遗留（P3） | 属 `ffa5907c` 会话产物，未被 git 跟踪、未被忽略；不影响本轮结论。原因：跨会话产物不擅自删除。影响：仓库内多两个 37 KB 中间文件。后续入口：用户确认后删除，或由该会话自行清理 |

## 检查范围与非范围

- 范围：`imagegen/SKILL.md`、`imagegen/CHANGELOG.md`、`imagegen/references/error-casebook.md` 三个文件的本轮改动，以及它们与全仓其它 skill 的引用关系。
- 非范围：`imagegen/scripts/imagegen.py`、`references/cli.md`、`config.example.json`、`source-notes.md` 的改动来自另一会话（统一配置目录与并发批量），本轮只读未改，不纳入本次风格判定。
- 不判断：生图模型出图质量、业务需求覆盖、发布放行。

## 验证记录

| 验证项 | 命令 / 方式 | 结果 |
|---|---|---|
| 改动文件编码 | 逐文件 `read_bytes().decode('utf-8')` | 3 文件均 UTF-8 OK |
| 工作流步骤编号 | 正则提取 `## 工作流` 到 `## 透明底规则` 间的步骤号 | `1,2,3,4,5,6,7,8` 连续 |
| SKILL.md 资产引用可达 | 提取 `references/*.md` 与 `scripts/*.py` 后逐个 `[ -e ]` | 8/8 OK，无 MISSING |
| 客户端常量复验 | 回读 `app.asar` 原始字节检索 `blockedProtocols=new Set` 与 `protocols:{cite:` | 两处均命中，与本轮文档表述一致 |
| 真实通道验证 | `present_visualization` 两次调用（老虎图、ffa5907c 原图） | 均返回成功快照；按维度 6 修正后的口径，该结果只记为「片段已保存」，不记为「用户已看见」 |
