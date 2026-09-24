# Prompting best practices

These prompting principles are shared by both top-level modes of the skill:
- 内置出图工具（default，宿主不同名称不同）
- CLI fallback（AI Hive，`scripts/imagegen.py`）

This file is about prompt structure, specificity, and iteration. Fallback-only execution controls such as `quality`, `input_fidelity`, masks, output format, and output paths live in the fallback docs.

## Contents
- [Structure](#structure)
- [Specificity policy](#specificity-policy)
- [Allowed and disallowed augmentation](#allowed-and-disallowed-augmentation)
- [Composition and layout](#composition-and-layout)
- [Constraints and invariants](#constraints-and-invariants)
- [Text in images](#text-in-images)
- [Input images and references](#input-images-and-references)
- [Iterate deliberately](#iterate-deliberately)
- [Transparent images](#transparent-images)
- [Fallback-only execution controls](#fallback-only-execution-controls)
- [Use-case tips](#use-case-tips)
- [Where to find copy/paste recipes](#where-to-find-copypaste-recipes)
- [Use-case taxonomy](#use-case-taxonomy)
- [共享 prompt 模板](#共享-prompt-模板)
- [Prompt 最佳实践](#prompt-最佳实践)

## Structure
- Use a consistent order: scene/backdrop -> subject -> key details -> constraints -> output intent.
- Include intended use (ad, UI mock, infographic) to set the level of polish.
- For complex requests, use short labeled lines instead of one long paragraph.

## Specificity policy
- If the user prompt is already specific and detailed, normalize it into a clean spec without adding creative requirements.
- If the prompt is generic, you may add tasteful detail when it materially improves the output.
- Treat examples in `sample-prompts.md` as fully-authored recipes, not as the default amount of augmentation to add to every request.
- For photorealism, include `photorealistic` directly when that is the goal, plus concrete real-world texture such as pores, wrinkles, fabric wear, material grain, or imperfect everyday detail.

## Allowed and disallowed augmentation

Allowed augmentation for generic prompts:
- composition and framing cues
- intended-use or polish-level hints
- practical layout guidance
- reasonable scene concreteness that supports the request

Do not add:
- extra characters, props, or objects that are not implied
- brand palettes, slogans, or story beats that are not implied
- arbitrary side-specific placement unless the surrounding layout supports it

## Composition and layout
- Specify framing and viewpoint (close-up, wide, top-down) and placement only when it materially helps.
- Call out negative space if the asset clearly needs room for UI or copy.
- Avoid making left/right layout decisions unless the user or surrounding layout supports them.
- For people, describe body framing, scale, gaze, and object interactions when they matter (`full body visible`, `looking down at the book`, `hands naturally gripping the handlebars`).

## Constraints and invariants
- State what must not change (`keep background unchanged`).
- For edits, say `change only X; keep Y unchanged` and repeat invariants on every iteration to reduce drift.

## Text in images
- Put literal text in quotes or ALL CAPS and specify typography (font style, size, color, placement).
- Spell uncommon words letter-by-letter if accuracy matters.
- For in-image copy, require verbatim rendering and no extra characters.
- 图片内含小字、密集信息图、多字体排版、图例坐标轴时，要求逐字渲染并提分辨率/正式参数出图（CLI 参数以平台实时 imageConfig 为准）。

## Input images and references
- Do not assume that every provided image is an edit target.
- Label each image by index and role (`Image 1: edit target`, `Image 2: style reference`).
- If the user provides images for style, composition, or mood guidance and does not ask to modify them, treat the request as generation with references.
- If the user asks to preserve an existing image while changing specific parts, treat the request as an edit.
- For compositing, describe how the images interact (`place the subject from Image 2 into Image 1`).

## Iterate deliberately
- Start with a clean base prompt, then make small single-change edits.
- Re-specify critical constraints when you iterate.
- Prefer one targeted follow-up at a time over rewriting the whole prompt.

## Transparent images
- 优先用内置出图工具处理透明底请求；主体明显复杂到不适合抠图时，说明限制并与用户对齐处理方式，不擅自承诺透明结果。
- Prompt 要求铺满单一纯色抠图背景，通常 `#00ff00`；主体为绿色时用 `#ff00ff`，避免用主体中出现的颜色。
- 明确禁止背景出现阴影、渐变、地面、反射、纹理与光照变化。
- 要求主体边缘清晰、留足边距、主体内部不使用 key 色。
- 生成后用本地脚本去底：`python "<skill-dir>/scripts/remove_chroma_key.py" --input <source> --out <final.png> --auto-key border --soft-matte --transparent-threshold 12 --opaque-threshold 220 --despill`（`<skill-dir>` = 本 SKILL.md 所在目录），并在交付前校验 alpha。
- 边缘抗锯齿用 soft matte + despill；纯硬边像素/精确取色场景才用仅 tolerance 的去除。

## Fallback-only execution controls
- CLI 专属执行控制（模型参数、输出格式与路径等）不混入内置工具语义；用户明确走 CLI 时读 `references/cli.md`。
- CLI fallback 固定模型 `public_model_gpt_image_2`，模型参数用 `--param key=value` 透传；支持范围以平台实时 `imageConfig` 为准。
- 草稿优先低成本（低分辨率、`--batch 1`、`COST_FIRST` 路由）；正式图按需求提分辨率与参数。
- 任务提交后只查原 `taskId`，不重复提交避免重复扣费。

## Use-case tips
Generate:
- photorealistic-natural: Prompt as if a real photo is captured in the moment; use photography language (lens, lighting, framing); call for real texture; avoid over-stylized polish unless requested.
- product-mockup: Describe the product/packaging and materials; ensure clean silhouette and label clarity; if in-image text is needed, require verbatim rendering and specify typography.
- ui-mockup: Describe the target fidelity first (shippable mockup or low-fi wireframe), then focus on layout, hierarchy, and practical UI elements; avoid concept-art language.
- infographic-diagram: Define the audience and layout flow; label parts explicitly; require verbatim text; prefer higher quality in CLI mode for dense labels.
- logo-brand: Keep it simple and scalable; ask for a strong silhouette and balanced negative space; avoid decorative flourishes unless requested.
- ads-marketing: Write like a creative brief; include brand positioning, audience, desired vibe, scene, and exact tagline if text must appear.
- productivity-visual: Name the exact artifact (slide, chart, workflow diagram), define the canvas and hierarchy, provide real labels/data, and ask for readable typography and polished spacing.
- scientific-educational: Define audience, lesson objective, required labels, scientific constraints, arrows, and scan-friendly whitespace.
- illustration-story: Define panels or scene beats; keep each action concrete.
- stylized-concept: Specify style cues, material finish, and rendering approach (3D, painterly, clay) without inventing new story elements.
- historical-scene: State the location/date and required period accuracy; constrain clothing, props, and environment to match the era.

Edit:
- text-localization: Change only the text; preserve layout, typography, spacing, and hierarchy; no extra words or reflow unless needed.
- identity-preserve: Lock identity (face, body, pose, hair, expression); change only the specified elements; match lighting and shadows.
- precise-object-edit: Specify exactly what to remove/replace; preserve surrounding texture and lighting; keep everything else unchanged.
- lighting-weather: Change only environmental conditions (light, shadows, atmosphere, precipitation); keep geometry, framing, and subject identity.
- background-extraction: For simple opaque subjects, request a clean cutout on a perfectly flat chroma-key background; crisp silhouette; generous padding; no shadows; no halos; preserve label text exactly; no restyling. 复杂主体需要真透明时，说明通道不支持原生透明，回到内置工具或与用户对齐处理方式。
- style-transfer: Specify style cues to preserve (palette, texture, brushwork) and what must change; add `no extra elements` to prevent drift.
- compositing: Reference inputs by index; specify what moves where; match lighting, perspective, and scale; keep the base framing unchanged.
- sketch-to-render: Preserve layout, proportions, and perspective; choose materials and lighting that support the supplied sketch without adding new elements.

## Where to find copy/paste recipes
For copy/paste prompt specs (examples only), see `references/sample-prompts.md`. This file focuses on principles, specificity, and iteration patterns.

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

- `references/sample-prompts.md`


## 现代 2D 高清微立体游戏资产规范（默认非像素生图铁律）

本规范沉淀自游戏素材生产实战经验与用户实测验收，专门应对 2D 游戏资产生成中容易意外退化为低清、粗糙或像素风格的问题：

### 1. 风格定位与特征公式
- **权威风格定位**：**现代 2D 高清微立体手绘矢量卡通风格（Modern 2D High-Definition Stylized Vector/Cartoon Art）**。
- **画面特质**：
  - 极具工业质感的高精度平滑连续轮廓线（polished smooth continuous outlines, clean vector edges）。
  - 细腻柔和的体积光影与微立体倒角遮蔽（gentle volumetric 2.5D bevel shading, soft ambient occlusion）。
  - 鲜明饱满的渐变色彩层次（vibrant rich gradient tones），彻底杜绝脏色与死黑。
  - 晶莹灵动的局部高光与反光（glossy highlights, vibrant eye reflection）。

### 2. 默认非像素机制与负向词库（Default Anti-Pixel Rule）
- **默认全局生效**：凡是处理 2D 游戏资产（角色、怪物、英雄、NPC、Boss、地图地砖、场景组件、技能特效、道具、UI 图标、Sprite 精灵图）的生图或改图请求，**全链路默认强制装配黄金反像素负向词库**与现代高清手绘矢量风格，无须用户反复强调。
- **豁免条件（仅显式指定像素时放行）**：只有当用户在 Prompt 或参数中**显式要求“像素风 / pixel art / 8-bit / 16-bit / 点阵 / 复古像素”**，或指定 `--allow-pixel` 时，系统才豁免该反像素过滤规则。
- **黄金反像素负向词库清单**：
```text
Avoid: pixel art, pixelated, 8-bit, 16-bit, retro sprite, mosaic, dithering, low resolution, aliasing, jagged lines, photo, photorealistic, noise, 3d render artifacts, blurry edges, compression artifacts, dirty textures, sketch lines
```

### 3. 抠图与色度键规范（Chroma-Key Background）
- 生成单体游戏素材（角色、怪物、塔、道具）时，主体必须完整居中，四边留白，背景强制指定纯平色度键背景（Solid Flat Chroma-Key Background）。
- **背景色选取铁律**：
  - 绿色/蓝绿色系主体（如植物、毒液、森林角色）：强制指定纯洋红 `#FF00FF`。
  - 暖色/红黄色系主体（如火炎、机甲、熔岩角色）：强制指定纯荧光绿 `#00FF00`。
  - 严禁产生渐变背景、投影、反光地面或半透明粒子与背景混合，确保下游 `remove_chroma_key.py` 能一键 100% 纯净去底。

### 4. 运行环境与网络鲁棒性
- 在 Windows 宿主环境下，调用外部中转或第三方 API 若遇到网络连接重置（`ConnectionResetError(10054)`）或 SSL 握手超时，优先在 WSL（Windows Subsystem for Linux）环境下运行生图命令，保证网络链路畅通与高效响应。
