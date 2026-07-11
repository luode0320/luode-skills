---
name: "imagegen"
description: "用于生成或编辑位图图片，例如插画、照片、纹理、精灵图、UI 图、概念图、动作帧、透明底抠图等。当用户要“生图”“改图”“参考图出新图”“做 sprite / mockup / 位图素材”时使用。优先使用内置 `image_gen` 工具；如果当前 turn 没有内置工具，就在本地 imagegen 环境可验证时自动切换到捆绑的 CLI 流程，而不是默认阻断。不要用于更适合直接修改 SVG、矢量资源或代码原生图形的任务。"
---

# Image Generation Skill

> 本目录是本仓库维护的 `imagegen` 权威版本；`.system/imagegen/` 是官方分发的只读参考快照，不应被当作生效版本重复触发。如两者同时出现在 skill 扫描结果中，以本目录（仓库根目录 `imagegen/`）为准。

用于为当前项目生成或编辑位图图像，例如网站素材、游戏素材、UI 预览图、产品图、线框图、Logo 探索图、照片风图像、信息图、角色动作帧等。

## 顶层模式

本 skill 只有两种顶层模式：

- **默认内置模式（优先）**：使用内置 `image_gen` 工具做普通生图、改图和简单透明底需求。不依赖 `OPENAI_API_KEY`。
- **CLI fallback 模式**：使用 `scripts/image_gen.py` 以及系统入口脚本 `scripts/run_imagegen.ps1` / `scripts/run_imagegen.sh`。当内置工具在当前 turn 不可用且本地 imagegen 环境验证通过时自动启用；用户显式要求 CLI/API/模型控制时也走这条路径。

CLI fallback 暴露三个子命令：

- `generate`
- `edit`
- `generate-batch`

## 脚本路径解析规则（新增）

本 skill 引用的所有 `scripts/*` 路径均相对于**当前 SKILL.md 所在目录**（下称 `<skill-dir>`），不是固定的 `~/.codex/skills/imagegen/`：

- 若当前运行环境是 Codex 且本 skill 是从 `$CODEX_HOME/skills/imagegen`（默认 `~/.codex/skills/imagegen`）加载的，`<skill-dir>` 就是该路径，与历史行为一致。
- 若当前运行环境是 Claude Code，或本 skill 从其他位置（如本仓库路径、`.claude/skills/imagegen`）加载，`<skill-dir>` 必须解析为"本 SKILL.md 实际所在目录"，不得假设 `~/.codex/...`。
- 判定方法：优先使用当前 agent 运行时暴露的"当前技能目录/当前文件路径"能力；若不可用，退化为在候选路径列表中按存在性探测（当前工作目录下的 `imagegen/`、仓库内 `skill/imagegen/`、`~/.codex/skills/imagegen/`、`~/.claude/skills/imagegen/` 等），第一个存在 `scripts/run_imagegen.*` 的目录即为 `<skill-dir>`。

## 核心规则

- 普通生图和改图优先使用内置 `image_gen`。
- 只要用户请求语义属于生图相关，对话中即使没有出现“请用 imagegen / 用 image_gen / 用 CLI”这类显式措辞，也必须自动触发本 skill。
- 不要因为用户只是想改尺寸、质量、输出路径，就主动切到 CLI。
- 如果当前 turn 没有可用的内置 `image_gen`，不要立刻阻断；先验证本地 CLI fallback。
- 这里的 CLI fallback 仅指“通过 `imagegen` 自带脚本入口去调用真实图像生成/编辑 API”，绝不允许退化为程序绘制、脚本拼图、SVG/HTML/CSS/canvas/Pillow 几何合成、占位图生成或其他非真实模型出图方式。
- CLI fallback 优先使用系统入口脚本，而不是自己现写一层 runner：
  - Windows：`scripts/run_imagegen.ps1`
  - Linux/macOS：`scripts/run_imagegen.sh`
- CLI fallback 验证时，优先先跑 `check`，确认：
  - auth 来源
  - base URL 来源
  - `openai` 导入是否正常
  - `PIL` 导入是否正常
  - dry-run 是否成功
- 如果验证失败只是因为缺少 `openai` 或 `PIL`，在环境允许时先安装缺失依赖，再重跑验证。
- 如果 CLI fallback 验证通过，直接继续出图，不需要再等用户额外提示“请用 imagegen”。
- 只有在这两条路都不可用时才阻断：
  - 内置 `image_gen`
  - 已验证通过的 CLI fallback
- 不允许因为“有脚本能画个差不多的图”就绕开本 skill 的真实图像生成链路。
- 不要静默从 built-in `image_gen` 或 CLI `gpt-image-2` 降级到 `gpt-image-1.5`。这类路径变化默认要向用户确认，除非用户已经明确要求 `gpt-image-1.5`、`scripts/image_gen.py` 或 CLI fallback。
- 如果用户要的是真透明、复杂透明对象，或本地抠图失败，再询问是否切到 `gpt-image-1.5 --background transparent --output-format png`。
- 用户只是提到 “batch” 不代表必须走 CLI；只有确实需要 CLI 控制，或 built-in 不可用时，才切 CLI。
- 用户显式要求 CLI 时，使用捆绑的 `scripts/image_gen.py` / 系统入口脚本，不要自建一次性 SDK 脚本。
- **不要修改** `scripts/image_gen.py`。如果脚本能力不够，先和用户对齐。
- 当用户希望把 imagegen 配成以后都能复用的本地入口时，读取 `references/local-entrypoints.md`。

## 错误案例持续迭代

每次生图调用前后都由 `execution-failure-learning-rules` 路由本 skill 的 `prevent`、`recover`、`learn` 三种模式：

1. `prevent`：调用前先按模型、调用模式、参数和环境匹配 `active` 案例；精确命中时先应用已验证的修复，模糊命中不得套用。`candidate`、`conflicted`、`stale`、`superseded` 和 `rejected` 只供诊断和历史追踪，不能直接驱动调用。
2. `recover`：出现非预期失败、产物校验失败或退出码为 0 但结果不可信时，先按参数、环境、鉴权、网络/限流、模型能力和输出校验分类，再读取 `references/error-casebook.md`。同一失败假设最多无变化重试一次；第二次仍失败必须改变诊断维度或执行路径。
3. 只执行案例中已经验证过的解决方案；涉及换模型、改变生图路径、真实透明回退或修改脚本时，继续遵守本 skill 的用户确认规则。
4. 解决后必须用同一输入和同一成功标准，通过不依赖真实 API 的 `--dry-run`、`check` 或等价本地验证复核；仅退出码为 0 不算复验通过。
5. `learn`：已复现、已解决且已复验的错误脱敏后自动写入本 skill 案例库的 `candidate`；当前任务拥有 skill 维护授权且满足晋级门禁时，才可转为 `active`。未解决或未验证错误只能作为当轮诊断结果。
6. 回写前按案例 ID、错误特征、适用模型和根因去重；同根因合并，不追加平行答案。新方案取代旧方案时，只有新方案完成同输入复验并获得授权后，才把旧案例转为 `superseded`；与现有方案边界不兼容的候选先标为 `conflicted`，不得覆盖现有 `active`。
7. 案例中禁止写入 API key、token、密码、完整鉴权响应、用户私有 prompt、输入图片内容和未经脱敏的本机路径；只保留足以复现问题的最小参数摘要。

案例字段、状态和首批 `gpt-image-2` 错误示例统一见 `references/error-casebook.md`。该案例库是经验参考，不得覆盖当前代码、官方参数约束或用户当前明确要求。

## 强阻断规则

- 只要这是明确的位图图片任务，例如插画、照片、sprite、动作帧、纹理、概念图、UI 图、mockup、透明底抠图，就必须尝试真实的位图生成路径。
- 如果 built-in 不可用，必须先尝试验证 CLI fallback，再决定是否阻断。
- 只有满足以下全部条件时，才允许把任务判定为 blocked：
  - built-in `image_gen` 不可用
  - CLI fallback 验证失败，或无法鉴权
  - 没有已确认可用的其他模型/路径 fallback
- 在没有可用出图路径之前，不得：
  - 假装图片已经生成
  - 输出“最终 PNG / WebP / JPG”
  - 用 SVG / HTML / CSS / canvas 占位图冒充位图成品
  - 用 Pillow、脚本拼接、程序绘制、几何组合、布局导出、后处理合成结果冒充“imagegen 已生图”
  - 把设计草图、文字方案、占位图说成已完成素材
- 在 blocked 状态下，可以提供明确标注的中间产物，例如：
  - prompt 草稿
  - image brief
  - 动作规划
  - 布局规格
  - 环境检查结果
  - 依赖修复步骤
  - fallback 说明
- blocked 状态下给出的所有内容都必须明确标注为“尚未生成最终图片”。

## 内置模式保存规则

- built-in 模式下，默认生成文件会落到 `$CODEX_HOME/*`。
- 不要把 OS temp 当成默认 built-in 输出位置。
- 不要依赖 built-in 工具的目标路径参数行为；需要特定位置时，先生成，再移动/复制。
- 只要图片是当前项目的正式资产，默认统一存到项目根目录下的 `images/<YYYYMMDDHHMMSS>/` 子目录。
- `<YYYYMMDDHHMMSS>` 目录表示本次生成批次时间；同一批次的相关正式资产应放在同一个时间戳目录里。
- 保存优先级：
  1. 用户指定了目标路径：移动或复制到该路径
  2. 图片是当前项目要用的：移动或复制进项目 `images/<YYYYMMDDHHMMSS>/`
  3. 图片只是预览：可以只在对话里展示，底层文件保留在默认位置
- 不要把项目实际依赖的图片只留在 `$CODEX_HOME/*`。
- 同一张图的多轮优化、微调、返修，默认沿用同一基础名并做版本号递增，例如 `hero-v1.png`、`hero-v2.png`、`hero-v3.png`。
- 除非用户明确要替换原文件，否则不要覆盖旧版本；从无版本文件起步时，第一版也直接用 `v1`。

## 什么时候用

- 生成全新图片
- 基于一张或多张参考图生成新图
- 编辑现有图片
- 生成一批位图素材

## 什么时候不要用

- 明显更适合直接改 SVG / 矢量图标系统
- 更适合直接用 HTML / CSS / canvas 画出来的简单图形
- 已有源文件是更合适的原生可编辑格式
- 用户明确想要确定性的代码原生输出，而不是 AI 位图

## 判定思路

先判断两个维度：

1. **意图**：这是 `generate` 还是 `edit`
2. **执行方式**：这是单个资产，还是多个资产/变体

### 意图判定

- 用户想保留原图主体、修改局部：按 `edit`
- 用户给图只是做风格/构图/角色参考：按 `generate`
- 用户没有给图：按 `generate`

### built-in edit 语义

- built-in edit 只适合编辑当前对话上下文里可见的图片
- 如果用户要编辑的是本地文件，且仍打算走 built-in，先用 `view_image` 把图读入上下文
- 如果任务明确需要文件路径控制、mask 或其他 CLI 专属参数，再走 CLI

### 批量策略

- built-in 路径：一个资产/一种变体，对应一次 built-in 调用
- CLI 路径：只有明确走 CLI 且需要很多不同 prompt 时，才用 `generate-batch`
- `n` 只适合同一 prompt 的多个变体，不适合多个不同资产

## 工作流

1. 判定顶层模式：
   - built-in 可用：优先 built-in
   - built-in 不可用：立刻尝试 CLI fallback
   - 只有当需要 `gpt-image-1.5` 真透明或其他明显降级/换路时，才询问用户确认
2. 判定是 `generate` 还是 `edit`
3. 判定结果是预览图还是项目正式资产
4. 判定是单图、多次调用，还是 CLI `generate-batch`
5. 一次性收集输入：prompt、文字要求、约束、禁止项、输入图
6. 明确每张输入图的角色：
   - reference image
   - edit target
   - supporting input
7. 如果 edit target 是本地文件且你还打算走 built-in，先 `view_image`
8. 如果用户要的是照片、插画、sprite、banner、动作帧或其他位图产物，必须走真实图像路径，不要用代码占位
9. 按用户 prompt 具体程度做轻量增强：
   - 已经很具体：只规范化，不乱加创意
   - 比较泛：只补能明显提升质量的必要细节
10. built-in 可用时，先用 built-in `image_gen`
11. built-in 不可用时，先验证 CLI fallback
12. CLI fallback 验证命令（`<skill-dir>` 含义见"脚本路径解析规则"）：
    - Windows：`powershell -ExecutionPolicy Bypass -File "<skill-dir>\scripts\run_imagegen.ps1" -Action check`（Codex 默认安装下 `<skill-dir>` 通常是 `$env:USERPROFILE\.codex\skills\imagegen`）
    - Linux/macOS：`bash "<skill-dir>/scripts/run_imagegen.sh" check`（Codex 默认安装下 `<skill-dir>` 通常是 `$HOME/.codex/skills/imagegen`）
13. 如果只缺 `openai` / `PIL`，在环境允许时补依赖后重试验证
14. CLI 验证通过后，用系统入口脚本继续生成/编辑，不要另写 wrapper
15. 透明底需求：
    - built-in 可用：先用 built-in + 纯色抠图背景，再本地去底
    - built-in 不可用但 CLI 已验证：用 CLI `gpt-image-2` + 纯色抠图背景，再本地去底
    - 只有切 `gpt-image-1.5 --background transparent` 时才问用户
16. 检查结果：主体、风格、构图、文本准确性、约束是否满足
17. 需要迭代时，一次只改一个重点
18. 预览图可以直接在对话里展示
19. 项目正式资产必须存进项目 `images/<YYYYMMDDHHMMSS>/`
20. 多资产任务默认把每个正式结果都落盘
21. 同一张图的连续优化结果必须做 `v1`、`v2`、`v3` 递增，不要覆盖前一版
22. 用户显式要求 CLI/API/模型控制时，再细读 `references/cli.md` 和 `references/image-api.md`
23. 最终必须汇报：
    - 最终保存路径
    - 最终 prompt 或 prompt 集
    - 执行路径：
      - `生图路径: built-in image_gen`
      - `生图路径: CLI fallback`
      - `生图状态: 无可用的 built-in 或已验证 CLI 生图链路，本次未完成最终生图`
    - 本次实际使用的模型或通道：
      - `生图模型: gpt-image-2`
      - `生图模型: gpt-image-1.5`
      - 若走 built-in 且当前环境拿不到精确底层模型名，也必须明确写出 `生图模型: built-in image_gen（底层精确模型名当前环境未暴露）`
23. 用户要长期复用的本地入口时，读取 `references/local-entrypoints.md`

## 透明底规则

透明底请求优先仍然是“纯色背景 + 本地抠图”，不是默认直接上 `gpt-image-1.5`。

如果 built-in 可用，优先 built-in。  
如果 built-in 不可用但 CLI 已验证通过，就用 CLI `gpt-image-2` 走同样的纯色抠图流程。

### 默认步骤

1. 生成纯色抠图背景的图片：
   - built-in 可用：用 built-in
   - built-in 不可用：用已验证的 CLI `gpt-image-2`
2. 选择不容易和主体撞色的 key color：
   - 默认 `#00ff00`
   - 绿色主体用 `#ff00ff`
   - 蓝色主体避免 `#0000ff`
3. 把生成结果放到工作区或 `tmp/imagegen/`
   - built-in 路径：从 `$CODEX_HOME/generated_images/...` 挪出来
   - CLI 路径：直接输出到工作区目标文件
4. 用本地脚本去背景（`<skill-dir>` 含义见"脚本路径解析规则"；Codex 默认安装下 `<skill-dir>` 通常是 `${CODEX_HOME:-$HOME/.codex}/skills/imagegen`）：

```bash
python "<skill-dir>/scripts/remove_chroma_key.py" \
  --input <source> \
  --out <final.png> \
  --auto-key border \
  --soft-matte \
  --transparent-threshold 12 \
  --opaque-threshold 220 \
  --despill
```

5. 校验 alpha 是否正常、边缘是否有明显绿边/紫边
6. 如果是项目正式资产，把透明图存进项目目录

### 透明底 prompt 规范

```text
Create the requested subject on a perfectly flat solid #00ff00 chroma-key background for background removal.
The background must be one uniform color with no shadows, gradients, texture, reflections, floor plane, or lighting variation.
Keep the subject fully separated from the background with crisp edges and generous padding.
Do not use #00ff00 anywhere in the subject.
No cast shadow, no contact shadow, no reflection, no watermark, and no text unless explicitly requested.
```

### 什么时候要询问是否切 `gpt-image-1.5`

- 用户明确要 true/native transparency
- 本地抠图校验失败
- 主体太复杂，不适合纯色抠图，例如：
  - hair
  - fur
  - feathers
  - smoke
  - glass
  - liquids
  - translucent materials
  - reflective objects
  - soft shadows

确认文案可用：

```text
This likely needs true native transparency. The default path uses a chroma-key background plus local removal, but true transparency requires the CLI fallback with gpt-image-1.5 because gpt-image-2 does not support background=transparent. Should I proceed with that CLI fallback?
```

## Prompt 增强

把用户输入整理成更稳定的生产型 prompt，但不要无脑加戏。

### 具体程度策略

- 用户已经很具体：只做结构化整理
- 用户比较泛：只补能明显提升结果的必要信息

允许补充：

- 构图提示
- 预期用途
- 必要的布局约束
- 合理的场景具体化

不要补充：

- 用户没提过的额外角色/物体
- 用户没要求的品牌、文案、故事设定
- 没依据的左右位置要求

## Use-case taxonomy

下面这些 slug 保持英文，不要擅自翻译或改名：

### Generate

- `photorealistic-natural`
- `product-mockup`
- `ui-mockup`
- `infographic-diagram`
- `scientific-educational`
- `ads-marketing`
- `productivity-visual`
- `logo-brand`
- `illustration-story`
- `stylized-concept`
- `historical-scene`

### Edit

- `text-localization`
- `identity-preserve`
- `precise-object-edit`
- `lighting-weather`
- `background-extraction`
- `style-transfer`
- `compositing`
- `sketch-to-render`

## 共享 prompt 模板

```text
Use case: <taxonomy slug>
Asset type: <where the asset will be used>
Primary request: <user's main prompt>
Input images: <Image 1: role; Image 2: role> (optional)
Scene/backdrop: <environment>
Subject: <main subject>
Style/medium: <photo/illustration/3D/etc>
Composition/framing: <wide/close/top-down; placement>
Lighting/mood: <lighting + mood>
Color palette: <palette notes>
Materials/textures: <surface details>
Text (verbatim): "<exact text>"
Constraints: <must keep/must avoid>
Avoid: <negative constraints>
```

说明：

- `Asset type` 和 `Input images` 是 prompt 结构，不是 CLI 独立参数
- `Scene/backdrop` 指画面背景，不等于 CLI 的 `background` 参数
- `Quality`、`input_fidelity`、mask、输出格式、输出路径这类是 CLI 执行参数，不要混进 built-in 工具参数语义里

## Prompt 最佳实践

- prompt 顺序优先按：场景 -> 主体 -> 细节 -> 约束
- 写清楚用途，帮助模型进入正确质量模式
- 文本内容要逐字明确
- 多图输入时，按图片编号说明各自用途
- edit 任务要反复强调 invariants
- 每轮迭代只改一个重点
- prompt 已经很具体时，不要过度扩写

更多共享原则看：

- `references/prompting.md`
- `references/sample-prompts.md`

## `gpt-image-2` 指南

CLI fallback 默认模型是 `gpt-image-2`。

- 新的 CLI 工作流默认优先 `gpt-image-2`
- 只有 true transparency 等特殊需求才考虑 `gpt-image-1.5`
- `gpt-image-2` 不支持 `background=transparent`
- `gpt-image-2` 不需要设置 `input_fidelity`
- `quality` 可用：
  - `low`
  - `medium`
  - `high`
  - `auto`
- 草稿优先：
  - `1024x1024`
  - `quality low`
- 正式图按需求提升尺寸和质量

常用尺寸：

- `1024x1024`
- `1536x1024`
- `1024x1536`
- `2048x2048`
- `2048x1152`
- `3840x2160`
- `2160x3840`
- `auto`

## CLI fallback 专属约定

### 临时与输出目录

- 临时文件放 `tmp/imagegen/`
- 正式输出放项目根目录 `images/<YYYYMMDDHHMMSS>/`
- 同一批次共用同一个时间戳目录；不要把同批正式结果散落到多个目录
- 同一张图的版本文件名用稳定基础名加 `-v<number>`，例如 `landing-hero-v1.png`
- 文件名尽量稳定、可读

### 依赖

优先使用 `uv`，但当前环境没有 `uv` 时，也可以使用当前 Python 环境的包管理器。

```bash
uv pip install openai
uv pip install pillow
```

### 环境

- 真实 API 调用需要可用的图像通道
- built-in 路径不需要向用户索要 `OPENAI_API_KEY`
- CLI fallback 优先桥接：
  1. 当前进程环境变量
  2. 项目规则文件（`AGENTS.md` / `CLAUDE.md`）回退配置
  3. 项目规则文件（`AGENTS.md` / `CLAUDE.md`）图像配置
  4. `~/.codex/auth.json` + `~/.codex/config.toml`（仅 Codex 环境存在该机制）
  5. Claude Code 环境：当前版本暂无已确认的等价全局密钥配置文件（不假设存在 `~/.claude/auth.json` 等路径）；若前 3 级都未命中，必须明确提示用户在项目规则文件（`CLAUDE.md`）或本机环境变量中补充声明，不得静默尝试读取未经确认存在的 Claude Code 配置文件
- 当 built-in 不可用且任务适合 CLI fallback 时，先做这套恢复流程，再决定是否 blocked：
  1. 跑系统 `check`
  2. 如果 `openai` 或 `PIL` 缺失，先补依赖
  3. 再跑一次 `check`
  4. 如果 env / 项目规则文件（`AGENTS.md` / `CLAUDE.md`）/ AI local config 都无法提供图像通道，再明确报 unavailable
  5. 验证成功后立刻继续出图，不要再等用户额外提示

如果缺少 key，提示用户：

1. 去 OpenAI 平台创建 API key
2. 在本地系统环境变量中设置 `OPENAI_API_KEY`
3. 如有需要，继续指导用户按系统/终端配置

## 参考文件

- `references/prompting.md`
- `references/sample-prompts.md`
- `references/cli.md`
- `references/image-api.md`
- `references/codex-network.md`（仅适用于 Codex CLI 的网络/沙箱审批配置；Claude Code 环境下没有等价的 `approval_policy`/`sandbox_mode` 概念，网络访问由宿主环境而非 skill 层配置控制，遇到网络受限问题应提示用户检查当前 Claude Code 会话的网络权限设置，不要尝试套用 Codex 的 TOML 配置项）
- `references/local-entrypoints.md`
- `references/error-casebook.md`
- `scripts/image_gen.py`
- `scripts/bootstrap_imagegen_env.py`
- `scripts/run_imagegen.ps1`
- `scripts/run_imagegen.sh`
- `<skill-dir>/scripts/remove_chroma_key.py`（Codex 默认 `$CODEX_HOME/skills/imagegen/scripts/remove_chroma_key.py`；`<skill-dir>` 含义见"脚本路径解析规则"）
