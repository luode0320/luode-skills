---
name: "imagegen"
description: "用于生成或编辑位图图片，例如插画、照片、纹理、精灵图、UI 图、概念图、透明底抠图等。当用户要“生图”“改图”“参考图出新图”“做图片素材”时使用；覆盖文生图、图生图、图片编辑、电商图、广告图、详情页、带货种草等图片场景。优先使用宿主内置出图工具；内置工具不可用或用户要求 CLI/API/模型参数控制时，使用本 skill 捆绑的双模 CLI 通道（优先 gpt-image-2.5-sunburst，支持多Key并发池与OpenAI/AI Hive兼容端点）出图。不要用于更适合直接修改 SVG、矢量资源或代码原生图形的任务。"
---

# Image Generation Skill（imagegen）

> 本目录（仓库根目录 `imagegen/`）是本仓库维护的权威版本，吸收新一代 GPT Image 模型族（`gpt-image-2.5-sunburst` / `gpt-image-2.5-flare` / `gpt-image-2`）、OpenAI 兼容端点、多 Key 并发密钥池与 AI Hive CLI 通道后独立成稿；不依赖任何单一 agent 宿主。

用于为当前项目生成或编辑位图图像：网站素材、游戏素材、UI 预览图、产品图、线框图、Logo 探索图、照片风图像、信息图、角色动作帧等。

## 模型梯队与优先级原则

新版生图通道支持三大主力模型，执行生图时默认遵循以下优先级与选型阶梯：

1. **`gpt-image-2.5-sunburst`（【默认主力】最高画质 / 丁达尔漫射与微距细节之王）**：
   - **画质特质**：大场景大气散射（Sunburst 阳光漫射效果）、体积雾、多层次远近景深、超微结构雕刻（极细齿轮、羽翼纹理、苔藓纤维）表现最为惊艳。
   - **耗时**：单张约 90 秒。
   - **选型建议**：**全链路默认主力模型**。优先用于最终正式素材交付、游戏概念图、高精原画与商业级插画。
2. **`gpt-image-2.5-flare`（高动态反光 / 极速增强版）**：
   - **画质特质**：镜面高光、边缘眩光（Flare 效应）、强烈金属质感反光，出图干净利落。
   - **耗时**：单张约 39 秒（速度最快）。
   - **选型建议**：适合潮玩道具、工业产品渲染、机甲/科幻风格、对出图时效敏感的多轮快速迭代预览。
3. **`gpt-image-2`（标准基准款）**：
   - **画质特质**：色彩自然均衡，标准写实光影。
   - **耗时**：单张约 45 秒。
   - **选型建议**：作为兼容兜底或基准测试使用。

## 顶层模式

本 skill 只有两条真实出图路径，其余（程序绘制、脚本拼图、SVG/HTML/CSS/canvas 合成、占位图）一律不算出图：

1. **内置模式（默认优先）**：使用当前宿主提供的内置位图生成工具（不同宿主名称不同，如 WorkBuddy 的 ImageGen、Codex 的 `image_gen`）。零配置，普通生图、改图、简单透明底需求直接用它。
2. **CLI fallback 模式**：使用捆绑的 `scripts/imagegen.py` 或 `scripts/image_gen.py`。支持 OpenAI 兼容接口（如 `https://api.luode.vip/v1` 等中转平台）与 AI Hive OpenAPI 接口。默认使用 `gpt-image-2.5-sunburst`，支持多 Key 轮换与限流故障切换。当内置工具不可用、需要一次并发生成多张不同图、或需要参数控制时走本路径。

判定优先级：内置可用 → 用内置；内置不可用 → 验证 CLI fallback 后出图；两条都不可用 → 明确标记 blocked（尚未生成最终图片），不伪造。

## 全局用户配置体系与多 Key 并发池

为了让开发机上所有项目（前后端、独立脚本、不同工作区）无需重复配置即可调用这套 API，本 skill 建立了分层解析与容灾机制：

### 1. 统一配置目录（唯一写入源）

- **配置目录固定为 `~/.imagegen/`**，Windows 即 `C:\Users\<用户名>\.imagegen\`。所有生图配置只放这里，不再使用 `~/.ai-hive/` 等其它目录。
- **主配置固定为 `~/.imagegen/config.json`**：`base_url`、`model`、`model_priority`、`api_key`、`api_keys` 等全部字段都写在这一份文件里；多条通道（OpenAI 兼容端点、AI Hive 端点）共用同一份配置，不按通道分文件。
- **`imagegen.py init` 写入该文件**，并在覆盖前保留已有的 `api_keys`、`model`、`model_priority` 等字段，不会把多 Key 池冲掉。
- **未配置时**：提示用户自行创建或运行 `init`；agent 不得代填 Key，也不得回显 Key 原值。

### 2. 配置加载优先级
1. **CLI 运行时入参**（最高优先级）：`--model`、`--api-key`、`--base-url`
2. **专用环境变量覆盖**：`IMAGEGEN_MODEL`、`IMAGEGEN_BASE_URL`、`IMAGEGEN_API_KEYS`
3. **统一配置文件（核心单一真理源）**：`~/.imagegen/config.json`（跨所有项目通用，优先读取避免 Windows 进程环境变量缓存漂移）
4. **Windows 用户级注册表环境变量**：`PROJECT_IMAGE_MODEL`、`PROJECT_IMAGE_BASE_URL`、`PROJECT_IMAGE_OPENAI_API_KEY`
5. **系统默认兜底**：模型 `gpt-image-2.5-sunburst`

> 仅运行时覆盖可走环境变量；任何需要长期保存的配置一律写回 `~/.imagegen/config.json`。

### 3. 多 Key 并发密钥池架构（Multi-Key Pool）
- **配置文件结构 (`~/.imagegen/config.json`)**：
  ```json
  {
    "base_url": "https://api.luode.vip/v1",
    "model": "gpt-image-2.5-sunburst",
    "model_priority": ["gpt-image-2.5-sunburst", "gpt-image-2.5-flare", "gpt-image-2"],
    "api_key": "sk-primary...",
    "api_keys": [
      "sk-account-1...",
      "sk-account-2...",
      "sk-account-3..."
    ]
  }
  ```
- **并发与限流应对**：
  - **默认并发批量**：`scripts/image_gen.py generate-batch` 使用 asyncio + Semaphore 真并发，默认 5 路、上限 25 路；多张不同 prompt 一次性提交，不再逐张串行等待。本机单 Key 实测：3 张串行 78.3s → 并发 3 路 33.1s（约 2.4×）；5 张并发 5 路 36.5s，全程无 429。
  - **Round-Robin 负载均衡**：并发请求按 Key 队列轮询派发，多 Key 时突破单个 Key 的 QPS/并发上限；单 Key 场景下并发仍有效，只是共享同一条限流额度。
  - **429 自动降级与切换（Rate-Limit Failover）**：当某个 Key 遇到限流（HTTP 429）或配额不足时，捕获异常后自动切换至密钥池中的下一个可用 Key 并执行指数退避重试，无须中断生成任务；单 Key 时同 Key 退避重试，`--max-attempts` 默认 3。
  - **失败隔离**：单个 job 失败不会中断其它 job；只有显式加 `--fail-fast` 才在首个失败时中止全部。
  - **串行开关**：`--concurrency 1` 恢复串行；仅在持续限流、配额冲突或需要可复现顺序时使用。

## 核心规则

- 只要用户请求语义属于生图相关，即使没说"请用 imagegen"，也必须自动触发本 skill。
- 两条真实路径都不可用时才允许 blocked；blocked 状态下不得假装图片已生成、不得输出"最终 PNG/WebP"，只能给出明确标注的中间产物（prompt 草稿、image brief、环境检查结果、修复步骤等）。
- 不允许因为"有脚本能画个差不多的图"就绕开真实生成链路，也不允许把设计草图、占位图说成已完成素材。
- 不要因为用户只是改尺寸、质量、输出路径就主动切 CLI；只有确实需要 CLI 控制或内置不可用时才切。
- 用户显式要求 CLI 时用捆绑的 `scripts/imagegen.py`，不要自建一次性 SDK 脚本。
- 模型选型默认使用 `gpt-image-2.5-sunburst`（画质最高）；用户指定速度优先时切 `gpt-image-2.5-flare`。
- **【生成后符合度自检铁律（Post-Generation Compliance Self-Check）】**：**出图不等于任务完成**。每次生成或编辑后，必须拿用户原始提示词与本轮约束逐条比对，对每一条要求给出 `符合 / 不符合 / 无法判定` 的验收结论；只要存在任何**不符合**项，就**不得交付**，必须按不符合项定向修改提示词并**重新生成新图**（版本号递增、不覆盖旧版），直到全部要求符合才允许进入保存与汇报。连续 3 轮仍未达标时停止自动重试，改为向用户说明差距、已尝试的修改与候选方向，不得把"生成成功但不符合提示词"的图当成完成结果。
- **【游戏素材默认非像素铁律（Default Anti-Pixel Rule for Game Assets）】**：凡是处理 2D 游戏资产（角色、怪物、英雄、NPC、Boss、地图地砖、场景组件、技能特效、道具、UI 图标、Sprite 精灵图）的生图或改图请求，**除非用户显式要求“像素风 / pixel art / 8-bit / 16-bit / 点阵 / 复古像素”**，否则**一律默认采用现代 2D 高清微立体手绘矢量卡通风格（Modern 2D High-Definition Stylized Vector Cartoon Art）**，且底层必须默认自动注入黄金反像素负向词库（`pixel art, pixelated, 8-bit, 16-bit, retro sprite, mosaic, dithering, low resolution, aliasing, jagged lines, photo, photorealistic, noise, 3d render artifacts, blurry edges, compression artifacts, dirty textures, sketch lines`）。严禁在用户未显式要求像素时默认生成像素画或粗糙点阵图。

## 什么时候用 / 什么时候不用

- 用：生成全新图片、基于参考图生成新图、编辑现有图片、生成一批位图素材、透明底抠图。
- 不用：明显更适合直接改 SVG/矢量图标系统；更适合用 HTML/CSS/canvas 画的简单图形；已有可编辑原生源文件；用户明确要确定性的代码原生输出。

## 判定思路

1. **意图**：`generate`（无图或图仅作风格/构图参考）vs `edit`（保留原图主体、修改局部）。本地文件走内置 edit 时先把它读进上下文；需要文件路径控制、mask 等 CLI 专属参数时走 CLI。
2. **数量**：默认并发。需要多张**不同**图时，走 CLI 的 `generate-batch` 一次提交，默认 `--concurrency 5`（已于本机单 Key 实测 5 路并发稳定、无 429）；内置通道实测并列调用仍会排队串行，因此多图不走内置。`--batch N` 仍然只表示同一 prompt 出 N 张变体，与"多个不同 prompt 并发"是两件事。
3. **批量策略**：
   - **多张不同内容（默认并发）**：写一份 JSONL（每行一个 `{"prompt": "...", "out": "name.png"}`），用 `generate-batch --input jobs.jsonl --out-dir <dir>` 一次跑完；默认并发 5，上限 25。
   - **同一 prompt 多张变体**：用 `--n N`（生成接口的 `n` 参数）或 AI Hive 通道的 `--batch N`。
   - **内置通道**：内置工具没有批量 API；实测同一轮并列发起 3 次内置生图仍是依次执行（完成时间戳间隔约 11s），不构成真并发。多张不同图且数量 ≥ 2 时，默认切 CLI `generate-batch`。
   - **降级为串行**：`--concurrency 1`。仅在并发出现持续 429、配额冲突或显式要求可复现顺序时使用。

## 工作流

1. 判定顶层模式（内置可用→内置；否则验证 CLI fallback）。
2. 判定 `generate` / `edit`，明确每张输入图角色：`reference image`（风格/构图参考）、`edit target`（修改目标）、`supporting input`（辅助输入）。
3. 判定结果用途：预览图（对话展示即可）还是项目正式资产（必须落盘）。
4. 一次性收集输入：prompt、文字要求、约束、禁止项、输入图；用户 prompt 很具体时只做结构化整理不乱加创意，比较泛时只补能明显提升质量的必要细节。
4.1 **多图并发预判（数量 ≥ 2 且内容不同时）**：先把每张图拆成独立 job（主体 + 该图独有约束 + 输出文件名），一次性写入 JSONL 并走 `generate-batch`；不要为了"安全"退回逐张串行，也不要指望内置通道并列调用来并发。只有单张需求或明确要求串行时才逐次调用。
5. **出图后符合度自检（硬闸门，不得跳过）**：把用户提示词与本轮约束拆成可逐条打勾的验收清单，至少覆盖主体与数量、风格/媒介、构图与取景、颜色与配色、尺寸与比例、画面内文字是否逐字准确、禁止项（`Avoid:` 负向词）是否守住、透明底或色度键要求、参考图角色是否被正确遵守；逐项给出 `符合 / 不符合 / 无法判定`，并把清单作为交付证据随结论一起给出。详细清单与判定口径见 `references/prompting.md`。
6. **不符合即重做（不得以"已生成"代替"已达标"）**：任一验收项为 `不符合` 时不得交付，须按不符合项做**定向修改**（已符合项保持不变，并在新 prompt 中复述关键约束防漂移），重新生成新图；同一资产多轮优化按 `v1`、`v2`、`v3` 递增命名，禁止覆盖旧版本，多问题时一次只改一个重点。连续 3 轮仍不达标 → 停止重试，向用户报告差距、已尝试修改与候选方向。
7. **交付必须先展示再给路径（硬闸门）**：生图成功后，用户可见的交付必须让图片本身出现在回复中，路径只作为补充信息。
   - 宿主支持图片渲染时（Qoder Desktop、ChatGPT、Claude 等聊天界面），必须把图片以可渲染形式嵌入最终回复，而不是只写"已保存到 `<路径>`"。
   - **嵌入通道按以下优先级逐个尝试，前一档真实成功才停**：
     1. **宿主专用可视化 / 媒体通道**：Qoder Desktop 用 `present_visualization`（提交内嵌 base64 的 HTML 片段）；其他宿主若有自己的原生媒体工具（如 Doubao 的 `present_files`）优先用它。这条通道与聊天 Markdown 渲染分离，是目前唯一已知能绕开 Qoder CN 净化器的路径。
     2. **`data:` URI 内联**：`![alt](data:image/jpeg;base64,...)`。**只有在该宿主已实测确认放行时才用**；不能凭"主流 Electron CSP 含 `data:`"臆测可用。
     3. **宿主已注册的本地资源协议**。
   - **Qoder CN 实证（2026-10-19，客户端 `resources/app.asar` 确认）**：聊天 Markdown 净化器 `harden()` 的 `blockedProtocols` 固定包含 `data:`、`file:`、`javascript:`、`vbscript:`；净化 schema 的 `src` 白名单只有 `http`、`https`。因此 `data:` 图片会被替换成纯文本 `[Image blocked: <alt>]`，`file:///` 与盘符绝对路径同样不可用。**Qoder CN 上必须走 `present_visualization`，不要用 `data:` 内联。**
   - **拦截无法靠"换写法"绕过**：这不是 CSP、图片体积或 base64 长度问题，压缩到多小都会被拦。看到 `[Image blocked: ...]` 直接切第 1 档通道，不要反复重试内联。
   - 大图必须先压缩：`present_visualization` 的 HTML 片段须控制在 1 MB 以内；`data:` 内联建议宽度 ≤ 800px、JPEG quality 60-75。原图始终完整落盘，回复里同时给出原图路径。
   - **所有通道都失败时**：明确写"当前环境不支持内联渲染"并给出原图绝对路径，不得伪造已展示，也不得把"我已经贴了 base64"当成已渲染。
   - **"工具返回成功"≠"用户已看见"**：`present_visualization` 返回成功只证明片段通过校验并保存为快照，**不证明客户端真的渲染出来了**。交付时只能说"已提交可视化通道"，不得断言"已展示"；若用户反馈看不到，按通道不可用处理并回退到路径交付，不要重复提交同一片段。
8. 最终汇报：展示结果（**实际用了哪一档通道**、该通道是否经真实返回确认成功；若走降档必须写明原因）、最终保存路径、最终 prompt 集、生图路径（内置 / CLI fallback）、使用的模型，以及本轮符合度自检结论。

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
- **落盘与展示是两个独立交付项**：落盘保证资产可复用，展示保证用户当场看得见；两者都要做，不得用其中一个替代另一个。

## CLI fallback 通道（AI Hive GPT Image 2）

> 本通道吸收自独立 gpt-image-2 skill（AI Hive OpenAPI 裸接口），迁移后由本 skill 统一承接；入口 `scripts/imagegen.py`。

**能力**：图片生成与编辑，固定模型 `public_model_gpt_image_2`；支持文生图、参考图生成（`--image`）、批量（`--batch`）、模型参数透传（`--param key=value`）。

## 并发批量通道（OpenAI 兼容端点，默认多图路径）

入口 `scripts/image_gen.py`，子命令 `generate-batch`。多张**不同**图默认走这里。

**JSONL 输入**（每行一个 job，可省略 `fields`）：

```jsonl
{"prompt": "红色陶瓷马克杯，纯白背景", "out": "mug.png"}
{"prompt": "黄色橡皮鸭，纯白背景", "out": "duck.png"}
```

**命令**：

```bash
python3 "$SKILL_PATH/scripts/image_gen.py" generate-batch \
  --input jobs.jsonl --out-dir images/20261019120000 \
  --concurrency 5 --max-attempts 3 \
  --size 1024x1024 --quality medium --output-format png
```

**关键参数**：

| 参数 | 默认 | 说明 |
|---|---|---|
| `--concurrency` | 5 | 并发上限 1–25；`1` 即串行基线 |
| `--max-attempts` | 3 | 单 job 限流/瞬态错误的最大尝试次数，失败自动切 Key + 指数退避 |
| `--fail-fast` | 关闭 | 默认单 job 失败不影响其它 job；开启后首个失败即中止全部 |
| `--out-dir` | 必填 | 批量模式强制要求，产物按 `序号-slug.png` 命名 |
| `--size` / `--quality` / `--output-format` | `auto` / `medium` / `png` | 作用于全部 job，也可在单行 job 内覆盖 |

**已验证事实（2026-10-19，本机单 Key，`api.luode.vip`）**：

| 场景 | 结果 |
|---|---|
| 3 张串行（`--concurrency 1`） | 29.2s + 23.8s + 25.3s = 78.3s |
| 3 张并发（`--concurrency 3`） | 33.1s，无 429 |
| 5 张并发（`--concurrency 5`） | 36.5s，无 429 |

单 Key 下并发同样有效，只是共享同一条限流额度；配多 Key 时 `ApiKeyPool` 轮询进一步分摊。串行只作为限流兜底，不再是默认。

**子命令速查（AI Hive 通道）**：

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
| API Key | 格式 `sk-api-*`。三种来源：`init` 子命令引导写入统一配置 `~/.imagegen/config.json`（权限 0600）/ `AI_HIVE_API_KEY` 环境变量 / `--api-key` 参数 |
| 外网 | 需可达 AI Hive API（默认 base URL） |
| Pillow | 仅透明底去底 `remove_chroma_key.py` 需要 |

凭据口径：API Key 默认来源为统一配置 `~/.imagegen/config.json`（由 `init` 子命令引导写入，权限 0600），`AI_HIVE_API_KEY`、`IMAGEGEN_API_KEY` 等环境变量与 `--api-key` 参数仅作运行时覆盖；agent 不得代填，禁止在过程性输出中回显凭据原值。

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
