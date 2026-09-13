---
name: "imagegen"
description: "用于生成或编辑位图图片，例如插画、照片、纹理、精灵图、UI 图、概念图、透明底抠图等。当用户要“生图”“改图”“参考图出新图”“做图片素材”时使用；覆盖文生图、图生图、图片编辑、电商图、广告图、详情页、带货种草等图片场景。优先使用宿主内置出图工具；内置工具不可用或用户要求 CLI/API/模型参数控制时，使用本 skill 捆绑的 AI Hive CLI 通道（固定 public_model_gpt_image_2）验证后出图，不默认阻断。不要用于更适合直接修改 SVG、矢量资源或代码原生图形的任务。"
---

# Image Generation Skill（imagegen）

> 本目录（仓库根目录 `imagegen/`）是本仓库维护的权威版本，吸收 AI Hive GPT Image 2 CLI 通道后独立成稿；不依赖任何单一 agent 宿主。

用于为当前项目生成或编辑位图图像：网站素材、游戏素材、UI 预览图、产品图、线框图、Logo 探索图、照片风图像、信息图、角色动作帧等。

## 顶层模式

本 skill 只有两条真实出图路径，其余（程序绘制、脚本拼图、SVG/HTML/CSS/canvas 合成、占位图）一律不算出图：

1. **内置模式（默认优先）**：使用当前宿主提供的内置位图生成工具（不同宿主名称不同，如 WorkBuddy 的 ImageGen、Codex 的 `image_gen`）。零配置，普通生图、改图、简单透明底需求直接用它。
2. **CLI fallback 模式**：使用捆绑的 `scripts/imagegen.py`（AI Hive OpenAPI 通道，固定 `public_model_gpt_image_2`）。当内置工具在当前 turn 不可用且本地 CLI 环境验证通过时自动启用；用户显式要求 CLI/API/模型参数控制时也走这条路径。

判定优先级：内置可用 → 用内置；内置不可用 → 验证 CLI fallback 后出图；两条都不可用 → 明确标记 blocked（尚未生成最终图片），不伪造。

## 核心规则

- 只要用户请求语义属于生图相关，即使没说"请用 imagegen"，也必须自动触发本 skill。
- 两条真实路径都不可用时才允许 blocked；blocked 状态下不得假装图片已生成、不得输出"最终 PNG/WebP"，只能给出明确标注的中间产物（prompt 草稿、image brief、环境检查结果、修复步骤等）。
- 不允许因为"有脚本能画个差不多的图"就绕开真实生成链路，也不允许把设计草图、占位图说成已完成素材。
- 不要因为用户只是改尺寸、质量、输出路径就主动切 CLI；只有确实需要 CLI 控制或内置不可用时才切。
- 用户显式要求 CLI 时用捆绑的 `scripts/imagegen.py`，不要自建一次性 SDK 脚本。
- 不要静默降级通道或换模型；AI Hive 通道固定 `public_model_gpt_image_2`，如模型下线或要换其他模型，先查询实时模型列表并与用户确认。
- **不要修改** `scripts/imagegen.py` 的模型固定与通道逻辑；能力不够时先和用户对齐（改脚本内 `SKILL_CONFIG` 归属元数据除外）。

## 什么时候用 / 什么时候不用

- 用：生成全新图片、基于参考图生成新图、编辑现有图片、生成一批位图素材、透明底抠图。
- 不用：明显更适合直接改 SVG/矢量图标系统；更适合用 HTML/CSS/canvas 画的简单图形；已有可编辑原生源文件；用户明确要确定性的代码原生输出。

## 判定思路

1. **意图**：`generate`（无图或图仅作风格/构图参考）vs `edit`（保留原图主体、修改局部）。本地文件走内置 edit 时先把它读进上下文；需要文件路径控制、mask 等 CLI 专属参数时走 CLI。
2. **数量**：单资产多次调用即可；只有明确走 CLI 且需要大量不同 prompt 时才批量；`--batch` 只适合同一 prompt 的多个变体。
3. **批量策略**：内置路径一个资产/一种变体对应一次调用；CLI 路径的 `--batch N` 用于同一 prompt 出 N 张变体，不是多个不同资产。

## 工作流

1. 判定顶层模式（内置可用→内置；否则验证 CLI fallback）。
2. 判定 `generate` / `edit`，明确每张输入图角色：`reference image`（风格/构图参考）、`edit target`（修改目标）、`supporting input`（辅助输入）。
3. 判定结果用途：预览图（对话展示即可）还是项目正式资产（必须落盘）。
4. 一次性收集输入：prompt、文字要求、约束、禁止项、输入图；用户 prompt 很具体时只做结构化整理不乱加创意，比较泛时只补能明显提升质量的必要细节。
5. 出图后检查：主体、风格、构图、文本准确性、约束是否满足。
6. 迭代时一次只改一个重点；同一张图连续优化按 `v1`、`v2`、`v3` 递增命名，不覆盖旧版本。
7. 最终汇报：最终保存路径、最终 prompt 集、生图路径（内置 / CLI fallback）、使用的模型。

## 透明底规则

- 默认流程是"纯色抠图背景 + 本地去底"，不依赖模型原生透明通道：
  1. 生成铺满纯色背景（默认 `#00ff00`，绿色主体用 `#ff00ff`，避免与主体撞色）、无阴影/渐变/地面/反射的主体图。
  2. 用 `scripts/remove_chroma_key.py` 本地去底（仅依赖 Pillow）：

  ```bash
  python "<skill-dir>/scripts/remove_chroma_key.py" --input <source> --out <final.png> \
    --auto-key border --soft-matte --transparent-threshold 12 --opaque-threshold 220 --despill
  ```

  3. 校验 alpha 与边缘（无绿边/紫边），正式资产存入项目目录。
- `<skill-dir>` = 本 SKILL.md 所在目录（脚本路径解析规则见下）。
- 复杂透明主体（毛发、皮毛、羽毛、烟雾、玻璃、液体、半透明/反光材质、软阴影）本地抠图效果差，或用户明确要真透明时：说明当前通道不支持原生透明，回到内置工具尝试或与用户对齐处理方式，不擅自承诺透明结果。

## Prompt 增强

- 允许补：构图提示、预期用途、必要布局约束、合理的场景具体化。
- 禁止补：用户没提过的额外角色/物体、品牌文案、故事设定、没依据的左右位置要求。
- 图片内文字必须逐字出现时用引号包围，指定语言、大小写、换行、位置；交付前人工复核。
- 参考图角色要逐张说清（图 1 提供商品、图 2 提供材质、图 3 提供构图），不要让模型猜冲突关系。
- 详细技巧、use-case taxonomy、共享模板见 `references/prompting.md`；可直接复制的样例见 `references/sample-prompts.md`。

## 保存规则

- 内置模式生成文件默认落在宿主默认位置；不要依赖内置工具的目标路径参数，需要特定位置时先生成再移动/复制。
- 图片是当前项目正式资产时，统一存到项目根目录 `images/<YYYYMMDDHHMMSS>/`；同一批次的正式资产放同一时间戳目录。
- 保存优先级：用户指定路径 > 项目 `images/<YYYYMMDDHHMMSS>/` > 仅预览（留在默认位置即可）。
- 不要把项目实际依赖的图片只留在宿主默认目录。
- 同一张图多轮优化默认递增版本号（`hero-v1.png`、`hero-v2.png`…）；从无版本起步的第一版直接用 `v1`；用户明确要替换时才覆盖。

## CLI fallback 通道（AI Hive GPT Image 2）

> 本通道吸收自独立 gpt-image-2 skill（AI Hive OpenAPI 裸接口），迁移后由本 skill 统一承接；入口 `scripts/imagegen.py`。

**能力**：图片生成与编辑，固定模型 `public_model_gpt_image_2`；支持文生图、参考图生成（`--image`）、批量（`--batch`）、模型参数透传（`--param key=value`）。

**子命令速查**：

| 子命令 | 功能 | 关键参数 |
|---|---|---|
| `generate` | 生成或编辑图片（固定模型） | `--prompt`(必填)、`--image`(可多张)、`--batch`(默认1)、`--param key=value`、`--routing COST_FIRST/SPEED_FIRST/SUCCESS_FIRST`、`--output-dir`、`--no-download` |
| `task` | 查询生成任务 | `--task-id` |
| `upload` | 上传图片拿 mediaId | `--file` |
| `init` | 交互式配置 API Key | `--skill-name` |

**示例**：

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt "高级商业摄影风格的产品主视觉，主体清晰，材质真实，留出标题空间"
# 参考图 / 批量 / 仅提交不下载
python3 "$SKILL_PATH/scripts/imagegen.py" generate --prompt "..." --image ref1.png ref2.png --batch 4 --no-download
python3 "$SKILL_PATH/scripts/imagegen.py" task --task-id <taskId>
```

**参数与行为**：`--routing` 默认 `COST_FIRST`（实时读取价格）；输出默认 `~/Downloads/AiHive/`（可用 `--output-dir` 改）；模型支持的具体格式/尺寸/参数以脚本运行时查询的实时 `imageConfig` 为准；提交后只查询原任务 `taskId`，避免重复提交扣费。详细参考 `references/cli.md`。

## 环境自检（CLI fallback）

AI Hive CLI 通道环境依赖：

| 依赖 | 说明 |
|---|---|
| Python 3 + `requests` | 脚本唯一运行时依赖；缺 `requests` 时 `pip3 install requests` |
| API Key | 格式 `sk-api-*`。三种来源：`init` 子命令引导写入 `~/.ai-hive/config.json`（权限 0600）/ `AI_HIVE_API_KEY` 环境变量 / `--api-key` 参数 |
| 外网 | 需可达 AI Hive API（默认 base URL） |
| Pillow | 仅透明底去底 `remove_chroma_key.py` 需要 |

凭据口径：`AI_HIVE_API_KEY` 默认来源为 `~/.ai-hive/config.json`（由 `init` 子命令引导写入，权限 0600），`AI_HIVE_API_KEY` 环境变量与 `--api-key` 参数仅作运行时覆盖；agent 不得代填，禁止在过程性输出中回显凭据原值。

自检三步：① `python3 scripts/imagegen.py init` 配置 Key；② `models` 能力不存在时跑一次带 `--no-download` 的最简 `generate`，返回 `taskId` 即配置成功；③ 去底场景先确认 `import PIL` 可用。换机器/干净环境后按上表逐项恢复。

## 错误处理

出现非预期失败、退出码为 0 但结果不可信、参数被拒、鉴权失败、限流等，先按参数 / 环境 / 鉴权 / 网络限流 / 模型能力 / 输出校验分类，读取 `references/error-casebook.md` 匹配案例；同一失败假设最多无变化重试一次。禁止在输出中回显 API key、token 等凭据原值。

## 参考文件

- `references/prompting.md` — prompt 结构、specificity、use-case taxonomy、共享模板
- `references/sample-prompts.md` — 可直接复制的 prompt 样例
- `references/cli.md` — AI Hive CLI 通道完整参考（generate/task/upload/init 参数与模型说明）
- `references/error-casebook.md` — 已验证错误案例库（active/candidate 状态演进）
- `references/config.example.json` — API 配置示例
- `scripts/imagegen.py` — AI Hive CLI 通道（固定 `public_model_gpt_image_2`）
- `scripts/remove_chroma_key.py` — 透明底本地去底（纯 Pillow，通道无关）
- `workbuddy-absorption-map.md` / `references/source-notes.md` — 吸收登记（gpt-image-2 → imagegen）
