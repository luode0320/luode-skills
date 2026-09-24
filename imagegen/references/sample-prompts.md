# Sample prompts (copy/paste)

These prompt recipes are shared across both top-level modes of the skill:
- 内置出图工具（default）
- CLI fallback（AI Hive，`scripts/imagegen.py`），用于显式 CLI/API/模型参数控制

Use these as starting points. They are intentionally complete prompt recipes, not the default amount of augmentation to add to every user request.

When adapting a user's prompt:
- keep user-provided requirements
- only add detail according to the specificity policy in `SKILL.md`
- do not treat every example below as permission to invent extra story elements

The labeled lines are prompt scaffolding, not a closed schema. `Asset type` and `Input images` are prompt-only scaffolding; the CLI does not expose them as dedicated flags.

Execution details such as explicit CLI flags, model params, output formats, and local output paths depend on mode. Use the built-in tool by default, including simple transparent-image requests. For transparent images, prompt for a flat chroma-key background and remove it locally with `python "<skill-dir>/scripts/remove_chroma_key.py"` (`<skill-dir>` = 本 SKILL.md 所在目录); only apply CLI-specific controls when the user explicitly opts into fallback mode.

CLI 通道说明（AI Hive）:
- CLI fallback 固定模型 `public_model_gpt_image_2`（生成与编辑一体）。
- 模型参数用 `--param key=value` 透传；分辨率/格式等支持范围以平台实时 imageConfig 为准。
- 默认路由 `COST_FIRST`；任务提交后只查原 taskId，避免重复扣费。
- 透明底默认纯色背景 + 本地去底；CLI 通道不支持原生透明时不承诺透明结果。

For prompting principles (structure, specificity, invariants, iteration), see `references/prompting.md`.

## Generate

### photorealistic-natural
```
Use case: photorealistic-natural
Primary request: candid photo of an elderly sailor on a small fishing boat adjusting a net
Scene/backdrop: coastal water with soft haze
Subject: weathered skin with wrinkles and sun texture
Style/medium: photorealistic candid photo
Composition/framing: medium close-up, eye-level
Lighting/mood: soft coastal daylight, shallow depth of field, subtle film grain
Materials/textures: real skin texture, worn fabric, salt-worn wood
Constraints: natural color balance; no heavy retouching; no glamorization; no watermark
Avoid: studio polish; staged look
```

### product-mockup
```
Use case: product-mockup
Primary request: premium product photo of a matte black shampoo bottle with a minimal label
Scene/backdrop: clean studio gradient from light gray to white
Subject: single bottle centered with subtle reflection
Style/medium: premium product photography
Composition/framing: centered, slight three-quarter angle, generous padding
Lighting/mood: softbox lighting, clean highlights, controlled shadows
Materials/textures: matte plastic, crisp label printing
Constraints: no logos or trademarks; no watermark
```

### ui-mockup
```
Use case: ui-mockup
Primary request: mobile app home screen for a local farmers market with vendors and daily specials
Asset type: mobile app screen
Style/medium: realistic product UI, not concept art
Composition/framing: clean vertical mobile layout with clear hierarchy
Constraints: practical layout, clear typography, no logos or trademarks, no watermark
```

### infographic-diagram
```
Use case: infographic-diagram
Primary request: detailed infographic of an automatic coffee machine flow
Scene/backdrop: clean, light neutral background
Subject: bean hopper -> grinder -> brew group -> boiler -> water tank -> drip tray
Style/medium: clean vector-like infographic with clear callouts and arrows
Composition/framing: vertical poster layout, top-to-bottom flow
Text (verbatim): "Bean Hopper", "Grinder", "Brew Group", "Boiler", "Water Tank", "Drip Tray"
Constraints: clear labels, strong contrast, no logos or trademarks, no watermark
```

### scientific-educational
```
Use case: scientific-educational
Primary request: biology diagram titled "Cellular Respiration at a Glance" for high school students
Scene/backdrop: clean white classroom handout background
Subject: glucose turns into energy inside a cell; include glycolysis, Krebs cycle, and electron transport chain
Style/medium: flat scientific diagram with consistent icons, arrows, and readable labels
Composition/framing: landscape slide-style layout with clear hierarchy and generous whitespace
Text (verbatim): "Cellular Respiration at a Glance", "Glucose", "Pyruvate", "ATP", "NADH", "FADH2", "CO2", "O2", "H2O"
Constraints: scientifically plausible; avoid tiny text; no extra decoration; no watermark
```

### logo-brand
```
Use case: logo-brand
Primary request: original logo for "Field & Flour", a local bakery
Style/medium: vector logo mark; flat colors; minimal
Composition/framing: single centered logo on a plain background with generous padding
Constraints: strong silhouette, balanced negative space; original design only; no gradients unless essential; no trademarks; no watermark
```

### illustration-story
```
Use case: illustration-story
Primary request: 4-panel comic about a pet left alone at home
Scene/backdrop: cozy living room across panels
Subject: pet reacting to the owner leaving, then relaxing, then returning to a composed pose
Style/medium: comic illustration with clear panels
Composition/framing: 4 equal-sized vertical panels, readable actions per panel
Constraints: no text; no logos or trademarks; no watermark
```

### stylized-concept
```
Use case: stylized-concept
Primary request: cavernous hangar interior with tall support beams and drifting fog
Scene/backdrop: industrial hangar interior, deep scale, light haze
Subject: compact shuttle parked near the center
Style/medium: cinematic concept art, industrial realism
Composition/framing: wide-angle, low-angle
Lighting/mood: volumetric light rays cutting through fog
Constraints: no logos or trademarks; no watermark
```

### ads-marketing
```
Use case: ads-marketing
Primary request: campaign image for a streetwear brand called Thread
Subject: group of friends hanging out together in a stylish urban setting
Style/medium: polished youth streetwear campaign photography
Composition/framing: vertical ad layout with natural poses and integrated headline space
Lighting/mood: contemporary, energetic, tasteful
Text (verbatim): "Yours to Create."
Constraints: render the tagline exactly once; clean legible typography; no extra text; no watermarks; no unrelated logos
```

### productivity-visual
```
Use case: productivity-visual
Primary request: one pitch-deck slide titled "Market Opportunity"
Asset type: fundraising slide image
Style/medium: clean modern deck slide, white background, crisp sans-serif typography
Subject: TAM/SAM/SOM concentric-circle diagram plus a small growth bar chart from 2021 to 2026
Composition/framing: 16:9 landscape slide, clear data hierarchy, polished spacing
Text (verbatim): "Market Opportunity", "TAM: $42B", "SAM: $8.7B", "SOM: $340M", "AGI Research, 2024", "Internal analysis"
Constraints: readable labels, no clip art, no stock photography, no decorative clutter, no watermark
```

### historical-scene
```
Use case: historical-scene
Primary request: outdoor crowd scene in Bethel, New York on August 16, 1969
Scene/backdrop: open field with period-appropriate staging
Subject: crowd in period-accurate clothing, authentic environment
Style/medium: photorealistic photo
Composition/framing: wide shot, eye-level
Constraints: period-accurate details; no modern objects; no logos or trademarks; no watermark
```

## Asset type templates (taxonomy-aligned)

### Website assets template
```
Use case: <photorealistic-natural|stylized-concept|product-mockup|infographic-diagram|ui-mockup>
Asset type: <hero image / section illustration / blog header>
Primary request: <short description>
Scene/backdrop: <environment or abstract backdrop>
Subject: <main subject>
Style/medium: <photo/illustration/3D>
Composition/framing: <wide/centered; note usable negative space only if needed>
Lighting/mood: <soft/bright/neutral>
Color palette: <brand colors or neutral>
Constraints: <no text; no logos; no watermark; leave room for UI if needed>
```

### Website assets example: minimal hero background
```
Use case: stylized-concept
Asset type: landing page hero background
Primary request: minimal abstract background with a soft gradient and subtle texture
Style/medium: matte illustration / soft-rendered abstract background
Composition/framing: wide composition with usable negative space for page copy
Lighting/mood: gentle studio glow
Color palette: restrained neutral palette
Constraints: no text; no logos; no watermark
```

### Website assets example: feature section illustration
```
Use case: stylized-concept
Asset type: feature section illustration
Primary request: simple abstract shapes suggesting connection and flow
Scene/backdrop: subtle light-gray backdrop with faint texture
Style/medium: flat illustration; soft shadows; restrained contrast
Composition/framing: centered cluster; open margins for UI
Color palette: muted neutral palette
Constraints: no text; no logos; no watermark
```

### Website assets example: blog header image
```
Use case: photorealistic-natural
Asset type: blog header image
Primary request: overhead desk scene with notebook, pen, and coffee cup
Scene/backdrop: warm wooden tabletop
Style/medium: photorealistic photo
Composition/framing: wide crop with clean room for page copy
Lighting/mood: soft morning light
Constraints: no text; no logos; no watermark
```

### Game assets template
```
Use case: stylized-concept
Asset type: <game environment concept art / game character concept / game UI icon / tileable game texture>
Primary request: <biome/scene/character/icon/material>
Scene/backdrop: <location + set dressing> (if applicable)
Subject: <main focal element(s)>
Style/medium: <realistic/stylized>; <concept art / character render / UI icon / texture>
Composition/framing: <wide/establishing/top-down>; <camera angle>; <focal point placement>
Lighting/mood: <time of day>; <mood>; <volumetric/fog/etc>
Constraints: no logos or trademarks; no watermark
```

### Game assets example: environment concept art
```
Use case: stylized-concept
Asset type: game environment concept art
Primary request: cavernous hangar interior with tall support beams and drifting fog
Scene/backdrop: industrial hangar interior, deep scale, light haze
Subject: compact shuttle parked near the center
Style/medium: cinematic concept art, industrial realism
Composition/framing: wide-angle, low-angle
Lighting/mood: volumetric light rays cutting through fog
Constraints: no logos or trademarks; no watermark
```

### Game assets example: character concept
```
Use case: stylized-concept
Asset type: game character concept
Primary request: desert scout character with layered travel gear
Subject: long coat, satchel, practical travel clothing
Style/medium: character render; stylized realism
Composition/framing: neutral hero pose on a simple backdrop
Constraints: no logos or trademarks; no watermark
```

### Game assets example: UI icon
```
Use case: stylized-concept
Asset type: game UI icon
Primary request: round shield icon with a subtle rune pattern
Style/medium: painted game UI icon
Composition/framing: centered icon; generous padding; clear silhouette
Constraints: no text; no background scene elements; no logos or trademarks; no watermark
```

### Game assets example: tileable texture
```
Use case: stylized-concept
Asset type: tileable game texture
Primary request: worn sandstone blocks
Style/medium: seamless tileable texture; PBR-ish look
Scene/backdrop: neutral lighting reference only
Constraints: seamless edges; no obvious focal elements; no text; no logos or trademarks; no watermark
```

### Wireframe template
```
Use case: ui-mockup
Asset type: website wireframe
Primary request: <page or flow to sketch>
Style/medium: low-fi grayscale wireframe
Composition/framing: <landscape or portrait to match expected device>
Subject: <sections in order; grid/columns; key labels>
Constraints: no color; no logos; no real photos; no watermark
```

### Wireframe example: homepage (desktop)
```
Use case: ui-mockup
Asset type: website wireframe
Primary request: SaaS homepage layout with clear hierarchy
Style/medium: low-fi grayscale wireframe
Subject: top nav; hero with headline and CTA; three feature cards; testimonial strip; pricing preview; footer
Composition/framing: landscape desktop layout
Constraints: label major blocks; no color; no logos; no real photos; no watermark
```

### Wireframe example: pricing page
```
Use case: ui-mockup
Asset type: website wireframe
Primary request: pricing page layout with comparison table
Style/medium: low-fi grayscale wireframe
Subject: header; plan toggle; 3 pricing cards; comparison table; FAQ accordion; footer
Composition/framing: desktop or tablet layout
Constraints: label key areas; no color; no logos; no real photos; no watermark
```

### Wireframe example: mobile onboarding flow
```
Use case: ui-mockup
Asset type: mobile onboarding wireframe
Primary request: three-screen mobile onboarding flow
Style/medium: low-fi grayscale wireframe
Subject: screen 1 headline and CTA; screen 2 feature bullets; screen 3 form fields and CTA
Composition/framing: portrait mobile layout
Constraints: label screens and blocks; no color; no logos; no real photos; no watermark
```

### Logo template
```
Use case: logo-brand
Asset type: logo concept
Primary request: <brand idea or symbol concept>
Style/medium: vector logo mark; flat colors; minimal
Composition/framing: centered mark; clear silhouette; generous margin
Color palette: <1-2 colors; high contrast>
Text (verbatim): "<exact name>" (only if needed)
Constraints: no gradients; no mockups; no 3D; no watermark
```

### Logo example: abstract symbol mark
```
Use case: logo-brand
Asset type: logo concept
Primary request: geometric leaf symbol suggesting sustainability and growth
Style/medium: vector logo mark; flat colors; minimal
Composition/framing: centered mark; clear silhouette
Color palette: deep green and off-white
Constraints: no text unless requested; no gradients; no mockups; no 3D; no watermark
```

### Logo example: monogram mark
```
Use case: logo-brand
Asset type: logo concept
Primary request: interlocking monogram of the letters "AV"
Style/medium: vector logo mark; flat colors; minimal
Composition/framing: centered mark; balanced spacing
Color palette: black on white
Constraints: no gradients; no mockups; no 3D; no watermark
```

### Logo example: wordmark
```
Use case: logo-brand
Asset type: logo concept
Primary request: clean wordmark for a modern studio
Style/medium: vector wordmark; flat colors; minimal
Text (verbatim): "Studio North"
Composition/framing: centered text; even letter spacing
Constraints: no gradients; no mockups; no 3D; no watermark
```

## Edit

### text-localization
```
Use case: text-localization
Input images: Image 1: original infographic
Primary request: replace "Bean Hopper", "Grinder", "Brew Group", "Boiler", "Water Tank", and "Drip Tray" with "Tolva", "Molino", "Grupo de infusión", "Caldera", "Depósito de agua", and "Bandeja de goteo"
Constraints: change only the text; preserve layout, typography, spacing, and hierarchy; no extra words; do not alter logos or imagery
```

### identity-preserve
```
Use case: identity-preserve
Input images: Image 1: person photo; Image 2..N: clothing references
Primary request: replace only the clothing with the provided garments
Constraints: preserve face, body shape, pose, hair, expression, and identity; match lighting and shadows; keep the background unchanged; no accessories or text
```

### precise-object-edit
```
Use case: precise-object-edit
Input images: Image 1: room photo
Primary request: replace only the white chairs with wooden chairs
Constraints: preserve camera angle, room lighting, floor shadows, and surrounding objects; keep all other aspects unchanged
```

### lighting-weather
```
Use case: lighting-weather
Input images: Image 1: original photo
Primary request: make it look like a winter evening with gentle snowfall
Constraints: preserve subject identity, geometry, camera angle, and composition; change only lighting, atmosphere, and weather
```

### background-extraction
```
Use case: background-extraction
Input images: Image 1: product photo
Primary request: isolate the product on a clean transparent background
Scene/backdrop: perfectly flat solid #00ff00 chroma-key background for local background removal
Constraints: background must be one uniform color with no shadows, gradients, texture, reflections, floor plane, or lighting variation; crisp silhouette; generous padding; no halos or fringing; preserve label text exactly; no restyling; do not use #00ff00 anywhere in the subject
```

Post-process note: after generation, run `python "<skill-dir>/scripts/remove_chroma_key.py" --input <source> --out <final.png> --auto-key border --soft-matte --transparent-threshold 12 --opaque-threshold 220 --despill` (`<skill-dir>` = 本 SKILL.md 所在目录), then validate the alpha result before shipping. The CLI channel does not support native transparency; do not promise transparent output for complex subjects.

### style-transfer
```
Use case: style-transfer
Input images: Image 1: style reference
Primary request: apply Image 1's visual style to a man riding a motorcycle on a plain white backdrop
Constraints: preserve palette, texture, and brushwork; no extra elements
```

### compositing
```
Use case: compositing
Input images: Image 1: base scene; Image 2: subject to insert
Primary request: place the subject from Image 2 next to the person in Image 1
Constraints: match lighting, perspective, and scale; keep the base framing unchanged; no extra elements
```

### character consistency workflow
```
Use case: identity-preserve
Input images: Image 1: previous character anchor illustration
Primary request: continue the story with the same character in a new scene and action
Scene/backdrop: snowy forest after a winter storm
Subject: same young forest hero gently helping a frightened squirrel out of a fallen tree
Style/medium: same children's book watercolor illustration style as Image 1
Constraints: do not redesign the character; preserve facial features, proportions, outfit, color palette, and personality; no text; no watermark
```

### sketch-to-render
```
Use case: sketch-to-render
Input images: Image 1: drawing
Primary request: turn the drawing into a photorealistic image
Constraints: preserve layout, proportions, and perspective; choose realistic materials and lighting; do not add new elements or text
```


## 现代 2D 高清微立体游戏资产实战模板（反像素系列）

以下模板均严格遵循反像素（Anti-Pixel Art）红线，适用于现代商业级 2D 游戏素材生成：

### 1. 植物塔防防御塔 / 英雄角色（Hero / Tower Unit）
```text
Use case: modern-2d-game-unit
Asset type: In-game character sprite (Tower Defense Unit)
Primary request: An iconic cute peashooter plant turret character sprite, ready for battle
Scene/backdrop: Solid flat vibrant magenta chroma-key background (#FF00FF), completely clean and empty
Subject: Modern stylized peashooter plant with glossy big dark eyes, sleek tubular muzzle, vibrant green leaf collar and curved stem
Style/medium: Modern 2D high-definition stylized vector art, polished digital cartoon game asset
Composition/framing: Centered full-body hero view, occupying 75% of canvas, perfectly framed with generous margin
Lighting/mood: Crisp studio lighting, gentle 2.5D bevel edge highlights, soft ambient occlusion
Color palette: Rich vivid emerald and lime greens, sunny yellow inner muzzle, glossy dark pupils with bright white specular reflections
Materials/textures: Smooth organic plant surface with subtle subsurface scattering feel, clean vector contours
Constraints: Centered single character; no ground shadow, no floor plane, no background gradient, no particle noise
Avoid: pixel art, pixelated, 8-bit, 16-bit, retro sprite, mosaic, dithering, low resolution, aliasing, jagged lines, photo, photorealistic, noise, 3d render artifacts, blurry edges
`

### 2. 敌方怪物 / Boss 单位（Enemy / Boss Sprite）
```text
Use case: modern-2d-game-monster
Asset type: In-game enemy monster sprite
Primary request: A menacing but stylized cartoon zombie invader with humorous armored elements
Scene/backdrop: Solid flat neon green chroma-key background (#00FF00), completely uniform and clean
Subject: Cartoon zombie warrior with a dented metallic bucket helmet and patchwork ragged suit, expressive dynamic pose
Style/medium: Modern 2D high-resolution stylized digital cartoon art, clean vector contours
Composition/framing: Centered three-quarter view, full body from head to toe, ample padding around edges
Lighting/mood: High-contrast character rim light, smooth gradient shadows, playful sinister mood
Color palette: Cool desaturated grey-purple skin, weathered brass and steel metal, muted dark brown cloth
Materials/textures: Smooth stylized surfaces, dented metal highlights, crisp outlines
Constraints: Isolated single subject; no cast shadows on floor, no background debris
Avoid: pixel art, pixelated, 8-bit, 16-bit, retro, mosaic, dithered, low resolution, aliasing, photo, photorealistic, noise, 3d render artifacts
`

### 3. 地图地砖 / 地形块（Isometric / Top-Down Tileset Block）
```text
Use case: modern-2d-tileset
Asset type: Top-down seamless map tile or isometric terrain block
Primary request: A stylized vibrant grass terrain tile with rich dirt side cross-section
Scene/backdrop: Neutral solid light grey (#E0E0E0) isolated background
Subject: Single modular terrain block, lush stylized cartoon grass tufts on top, rich layered earth soil beneath
Style/medium: Modern 2D stylized cartoon game art, clean vector illustration
Composition/framing: Centered orthographic or top-down view, precise geometric modular edges for grid alignment
Lighting/mood: Bright cheerful directional sunlit highlights, soft ground-contact ambient occlusion
Color palette: Fresh spring greens, warm chocolate brown soil, subtle golden pebble accents
Materials/textures: Stylized chunky grass clumps, smooth soil texture, polished outlines
Constraints: Perfectly modular tile, seamless edge compatibility, no perspective distortion outside the specified angle
Avoid: pixel art, pixelated, 8-bit, 16-bit, retro, mosaic, dithering, photorealistic, grunge noise, blurry
`

### 4. 技能特效 / 弹道粒子（VFX & Projectile Sprite）
```text
Use case: modern-2d-vfx
Asset type: Skill VFX projectile or impact burst
Primary request: A blazing plasma energy pea projectile flying horizontally with stylized motion trail
Scene/backdrop: Pitch black background (#000000) or solid flat chroma-key magenta (#FF00FF)
Subject: Glowing stylized plasma sphere surrounded by dynamic energy rings and smooth swooshing speed trails
Style/medium: Modern 2D digital vector VFX, stylized anime/arcade hit effect
Composition/framing: Centered horizontal flight orientation, clear directionality from left to right
Lighting/mood: Intense inner core glow (hyper-bright white-cyan), vibrant outer energy aura (neon electric green)
Color palette: Neon lime green, electric cyan, core pure white
Materials/textures: Smooth luminous plasma, clean gradient transparency falloff, sharp outer shockwave rings
Constraints: Crisp stylized shapes, no grainy noise, no dirty dithered alpha
Avoid: pixel art, pixelated, 8-bit, retro sprite, mosaic, dithering, low resolution, photo smoke, realistic fire, noise
`
