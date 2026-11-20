---
schema_version: 1
doc_id: "REVIEW-20261027-01"
doc_type: style_regression
source_ids: ["TASK-IMAGEGEN-MODEL-SINGLE"]
status: accepted
version: v1.0
current_slice: "SLICE-IMAGEGEN-MODEL-SINGLE"
updated_at: "2026-10-27 22:12:00"
reader_level: business_general
writing_style: plain_chinese
appendix_policy: preserve_existing_or_one_terminal_appendix
complexity: L1
baseline_commit: 59b85aa6
template_version: v1
---

# 6-review 风格回归：imagegen 模型清单收敛为 gpt-image-2

结论：本轮把 imagegen skill 的可用模型从三档收敛为单一 `gpt-image-2`，风格检查通过。影响：后续走 CLI fallback 通道时，默认使用 `gpt-image-2`，不再按画质或速度切换默认模型。范围：核对写法、位置、命名、注释、编码与目录归位。非范围：不判断模型画质是否满足业务预期、不做真实出图验证、不判定发布放行。变化：修改 5 个文件，连带刷新字典产物 2 个。完成标准：六维逐项有磁盘证据，发现项已登记处置。术语说明：风格回归指只检查写法与位置的检查。验证状态：静态验证通过，未做真实出图。

## 真实测试前置证据

- `TEST-IMAGEGEN-MODEL-SINGLE`：两个生图脚本 `py_compile` 通过；示例配置 JSON 解析通过；隔离 `HOME` 与相关环境变量后，真实 `_resolve_default_model()` 返回 `gpt-image-2`；新进程复验一致。
- `EVIDENCE-IMAGEGEN-MODEL-SINGLE`：无生产业务行为改动，真实出图未执行，因为用户未要求产出图片且出图会消耗额度；不以静态验证宣称生图功能可用。

## 文档信息

- 来源任务：用户要求"生图的 skill，把模型限制在 gpt-image-2，删除 gpt-image-2.5-flare、gpt-image-2.5-sunburst"。
- 回归时间：2026-10-27；执行环境：本机 Git Bash + Windows。
- 图片资产决策：`N/A + 原因 + 证据`。原因：本轮只改 skill 文档与脚本常量，不产出图片。证据：`git status --porcelain` 无图片路径。
- 数据写入：`N/A`，理由：本轮未向任何数据库、缓存或消息队列写入数据。本机 `~/.imagegen/config.json` 的模型字段经用户确认后修改，已留备份 `config.json.bak.20261027`。

## 六维交付残留自查

| 维度 | 结论 | 证据 |
|---|---|---|
| 维度 1 需求覆盖对账 | 通过 | 用户两项诉求逐项对账：① "模型限制在 gpt-image-2" → `SKILL.md` 模型章节改为唯一模型 + 禁止事项；`scripts/image_gen.py` 的 `DEFAULT_MODEL`、`scripts/imagegen.py` 的解析兜底与 `SKILL_CONFIG`、`references/config.example.json` 三处模型字段全部改为 `gpt-image-2`。② "删除 gpt-image-2.5-flare、gpt-image-2.5-sunburst" → 全仓 `grep -rn "sunburst\|flare"` 在 SKILL.md / config.example.json / scripts 下仅剩 SKILL.md:20 一条禁止条款（有意保留的禁令说明），运行期无任何引用 |
| 维度 2 影响面 / 消费方对账 | 通过 | 本轮契约面是"可用模型名集合"与"默认模型值"。消费方扫描：`scripts/image_gen.py`（`DEFAULT_MODEL`、`_resolve_default_model`）、`scripts/imagegen.py`（模型解析链、`SKILL_CONFIG`）、`references/config.example.json`、`SKILL.md` 四类载体全部同步；`skill-dictionary/data.js` 与 `字典.md` 由生成脚本重写，`grep -c "gpt-image-2.5-sunburst" data.js` 返回 0，说明字典已无旧模型残留。仓外消费方 `~/.imagegen/config.json` 与用户级环境变量 `IMAGEGEN_MODEL`、`PROJECT_IMAGE_MODEL` 属用户级配置，已按用户确认同步并留备份 |
| 维度 3 残留物清扫 | 通过 | `git status --porcelain` 只有 5 个修改 + 2 个字典产物，全部为本轮计划内文件，无临时脚本、无 debug 开关、无孤儿文件。`imagegen/scripts/__pycache__/` 下的 `.pyc` 含旧模型字符串，但 `git ls-files` 确认该目录未被跟踪，属本地缓存；本轮编译校验用 `-B` 参数运行，未再生成新缓存。本轮未启动服务或后台进程，无需进程清理 |
| 维度 4 文档与引用一致性 | 通过 | 交叉核对 `SKILL.md` 内多处模型表述：description、开篇说明、模型章节、CLI fallback 描述、配置加载兜底、示例配置、核心规则全部指向 `gpt-image-2`，无一处残留旧模型作为可用值。`CHANGELOG.md` 新增 2.5.0 条目并保留 2.1.0 历史记录（历史条目记录的是当时事实，按只读处理不改写）。`references/cli.md` 使用的是 AI Hive 通道固定 `public_model_gpt_image_2`，与本轮 OpenAI 兼容通道模型清单互不冲突，无需改动 |
| 维度 5 口径一致性 | 通过 | "唯一模型"措辞在 SKILL.md 出现 3 处（description 的"唯一模型 gpt-image-2"、模型章节的"只允许使用 gpt-image-2 一个模型"、核心规则的"模型固定使用 gpt-image-2"），语义一致无第二种表述。字典 `auto_trigger` 与 `SKILL.md` 的 description 逐字一致（由生成脚本从 SKILL.md 读取写入）。`references_total` 未变化（本轮未新增 reference 文件），`implemented_total` 66 未变（未新增 skill 目录） |
| 维度 6 验证有效性反审 | 通过（曾发现 1 项并已修复） | 反审发现：首次在临时 HOME 下验证 `_resolve_default_model()` 仍返回 `gpt-image-2.5-sunburst`，一度疑似改动未生效。查明原因是本机存在同名用户级环境变量 `IMAGEGEN_MODEL` / `PROJECT_IMAGE_MODEL` 且优先级高于脚本默认常量，属预期设计而非代码缺陷；用 `env -u` 清除两个变量后重跑，返回 `gpt-image-2`。随后在加载新用户级环境变量的新进程中复验，脚本实际解析结果仍为 `gpt-image-2`，双向互证。未用本轮结论自证本轮验证。本轮无生产业务代码变更（仅常量与文档），真实出图未执行，理由：出图会消耗额度且用户未要求产出图片，已在此显式降级为静态验证 |

## 问题与修复

本轮发现本机用户配置与环境变量仍指向旧默认值，已按用户确认同步为 `gpt-image-2`；文档契约缺口已补齐，未改变生图脚本既有行为边界。

## 检查清单

- 格式、命名、目录归位：通过。
- 注释、日志、可读性与复用：通过。
- 编码、引用链与生产代码测试污染扫描：通过。

## 本轮发现项处置

| 发现项 | 处置 | 说明 |
|---|---|---|
| 本机 `~/.imagegen/config.json` 的 `model` / `models` / `model_priority` 仍指向已删除模型 | 已修复（经用户确认） | 改为 `gpt-image-2`；改前备份为 `config.json.bak.20261027`；`api_key` / `api_keys` 原样保留 |
| 用户级环境变量 `IMAGEGEN_MODEL` / `PROJECT_IMAGE_MODEL` 仍为 `gpt-image-2.5-sunburst` | 已修复（经用户确认） | 通过 PowerShell `SetEnvironmentVariable(...,'User')` 改为 `gpt-image-2`；已回读确认 |
| 当前 shell 进程仍缓存旧环境变量 | 不处置 | Windows 用户级变量只对新建进程生效；已在新进程验证解析结果正确，无需干预当前 shell |
| `image_gen.py:39` `GPT_IMAGE_2_MODEL` 与 `image_gen.py:521` `_decode_and_write` 全仓无引用 | 不处置 | 两条均由污染扫描标为 `[ORPHAN]`，但 `git diff` 确认不在本轮改动范围，属存量代码；按最小改动原则不顺手删除，记录为后续技术债候选 |

## 检查范围

- 范围：`imagegen/SKILL.md`、`imagegen/CHANGELOG.md`、`imagegen/references/config.example.json`、`imagegen/scripts/image_gen.py`、`imagegen/scripts/imagegen.py`，以及连带刷新的 `skill-dictionary/data.js` 与 `字典.md`。
- 非范围：`imagegen/references/cli.md`（AI Hive 固定模型口径，与本轮无关）、`imagegen/references/error-casebook.md` 与 `source-notes.md`、`workbuddy-absorption-map.md`（历史记录文件，只读）、`.system/imagegen/` 官方快照（不含这两个模型名，无改动必要）。
- 不判断：`gpt-image-2` 的实际画质是否满足各类素材需求、真实出图链路是否通畅、发布放行。

## 6-review 结论

STYLE: PASS

六维交付残留自查与行级风格核对均无未处置问题。脚本默认值、示例配置和文档口径一致，命令行显式覆盖保持原契约，未将默认值收敛误写为参数白名单。结果仅覆盖写法与位置，不代表真实出图链路已验证。

## 验证记录

| 验证项 | 命令 / 方式 | 结果 |
|---|---|---|
| 脚本语法 | `python -X utf8 -B -c "py_compile.compile(...)"` × 2 | 两个脚本均 `OK`，退出码 0 |
| 示例配置 JSON | `json.load(open('imagegen/references/config.example.json'))` | 解析成功，`model` / `models` / `model_priority` 均为 `gpt-image-2` |
| 默认模型解析（干净环境） | `env -u IMAGEGEN_MODEL -u PROJECT_IMAGE_MODEL` + 临时 HOME | `_resolve_default_model()` 返回 `gpt-image-2` |
| 默认模型解析（新环境变量） | PowerShell 读取 User 级变量后启动 Python | 返回 `gpt-image-2`，与用户级配置一致 |
| skill 结构校验 | `PYTHONUTF8=1 python .system/skill-creator/scripts/quick_validate.py imagegen` | `Skill is valid!`，退出码 0 |
| 旧模型名残留扫描 | `grep -rn "sunburst\|flare"` 限定 SKILL.md / config.example.json / scripts | 仅剩 SKILL.md:20 禁止条款 1 处，其余为 `.pyc` 本地缓存 |
| 生产代码测试污染扫描 | `python test-strategy-rules/scripts/scan_test_pollution.py --root . --diff-only` | `POLLUTION: PASS`（2 条 ORPHAN 属存量代码，已登记不处置） |
| 编码与换行 | Python 逐文件 `read_bytes()` + U+FFFD 计数 | 5 个文件均 UTF-8、乱码 0、CRLF 0、尾随空白 0 |
| 字典刷新 | `PYTHONUTF8=1 python skill-dictionary/generate_dictionary.py` | 退出码 0；`data.js` 旧模型计数 0，新口径命中 2 处 |
| 变更集核对 | `git status --porcelain` | 5 修改 + 2 字典产物，等于计划范围 |
