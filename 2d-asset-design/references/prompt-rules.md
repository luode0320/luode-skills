# 提示词规则

当需要手写 2D 素材生成提示词时，用这个文件。

## 全局约束

默认写清楚：

- 纯色背景
- 无文字
- 无标签
- 无 UI
- 无水印
- 精确格数
- 无边框
- 无格线
- 同一资产身份 across frames
- 相近体量和边界

如果需要洋红去背流程，明确要求 `#FF00FF` 纯色背景。

## 风格规则

- `clean_hd`：清晰非像素、低噪点、商业感更强
- `pixel_inspired`：现代像素感，但不走重颗粒
- `retro_pixel`：仅当用户明确要求复古像素
- `project-native`：跟项目现有风格保持一致
- `map_style`：跟当前地图风格保持一致

除非用户明确要求，否则不要主动写成 16-bit、retro JRPG、chunky pixel-art。

## 项目风格一致性提示词规则

当输出用于已有游戏项目时，提示词必须包含项目视觉基线。
不要只写“高质量”“商业级”“像某某参考”，必须明确它如何继续属于当前项目。

必须写清：

- Match the existing project art direction / 匹配项目现有美术方向
- Same top-down camera angle / 相同俯视或 3/4 镜头
- Same outline language / 相同描边逻辑
- Same color system and accent color / 相同配色系统和焦点色
- Same material rendering style / 相同材质表达方式
- Same shadow and glow logic / 相同阴影和发光规则
- Same detail density / 相同细节密度

如果已经写了 image spec，提示词必须直接继承 image spec 里的项目视觉基线、允许差异、参考差距和通过条件，不要重新发明一套更松的说明。

必须避免：

- different asset pack style
- inconsistent camera angle
- different rendering style
- photorealistic element in stylized game
- web icon style inside game asset
- unrelated palette
- mismatched outline weight
- pasted sticker look

## 商业级素材提示词规则

当目标是 `Tier 2` 或 `Tier 3`，提示词必须写出“美术完成度”而不是只写资产类别。

必须包含：

- hand-drawn line art rhythm / 手绘线稿节奏
- varied outline weight / 非均匀描边粗细
- appealing silhouette / 好看的外轮廓
- rich negative shapes / 清晰负形
- asymmetrical organic structure / 非对称有姿态的结构
- layered material planes / 材质层级
- grounded contact shadow / 对应主体落点的接地影
- 1-3 focal details / 1-3 个视觉焦点

如果是从 image spec 生成提示词，提示词必须保留以下字段语义：

- asset type
- use case
- project visual baseline
- reference gap
- allowed differences
- style constraints
- composition / framing
- materials / textures
- lighting / mood
- quality tier
- pass criteria
- avoid

禁止出现或必须规避：

- simple geometric icon
- flat vector clipart
- symmetrical sticker
- uniform outline weight
- random glowing dots
- pillow-shaded blob
- low-effort prop pack
- placeholder art

如果是树木、变异植物、发光树，应明确：

- 3-5 irregular canopy masses, not circles
- visible trunk and branching structure
- one dominant branch/stem direction
- crystal/fruit/glow elements with physical sockets
- roots and shadow aligned with contact points

如果是建筑、路障、残骸，应明确：

- readable load-bearing structure
- roof/wall/support/base layers
- damaged edges, rivets, straps, cracks or worn metal
- top plane and side plane value separation
- no single polygon slab with dots

## 参考规则

当存在参考图或参考素材包时：

- 明确哪些保留：镜头、轮廓逻辑、色块、材质语言、风格节奏
- 明确哪些变化：身份、动作、世界观、体量、功能细节
- 明确它是视觉方向，不是复制目标

## 布局 guide 规则

做 prop pack、tileset-like atlas、固定格子 sheet 时，可以先生成布局 guide。

提示词里要写清：

- 只把它当作行列、间距、居中、安全边距参考
- 不要真正画出 guide 线框、标记、编号、边框

## 容纳与留白规则

对所有需要稳定切帧的素材，优先写明：

- 主体完整落在格内
- 四周保留安全边距
- 武器、尾迹、烟、火花不越界

## 本体与 FX 分离

对主角、精英怪、Boss：

- 本体动作优先只保留本体与贴身武器动作
- 大范围刀光、枪焰、投射物、爆炸、长拖尾默认独立生成

## 通用骨架

```text
为一款 2D 游戏创建一个原创 <资产类型>。
资产类型：<asset type>。
用途：<use case>。
主要诉求：<primary request>。
项目视觉基线：<project visual baseline>。
参考来源：<reference sources>。
参考差距：<reference gap>。
允许差异：<allowed differences>。
风格约束：<style constraints>。
用途：<玩法职责>。
视角：<俯视 / 侧视 / 3/4>。
风格：<clean_hd / pixel_inspired / project-native>。
构图：<composition / framing>。
材质：<materials / textures>。
光照：<lighting / mood>。
质量阶梯：<quality tier>。
通过条件：<pass criteria>。
项目风格基线：<镜头、描边、配色、材质、阴影、发光、细节密度>。
风格一致性：必须匹配项目已有素材，不能像来自另一个素材包；只允许为玩法识别做受控差异。
轮廓：<轮廓语言>。
配色：<配色方向>。
质量：目标 <Tier 2 / Tier 3>，必须具备好看的外轮廓、手绘线稿节奏、非均匀描边、清晰负形、材质层级、接地阴影和 1-3 个视觉焦点。
输出：准确的 <rows>x<cols> 网格。
禁止项：<avoid>。
背景：纯平 #FF00FF。
不要文字、标签、UI、水印、边框、格线。
不要简单几何图标、均匀描边贴纸、随机发光点、占位图或 prop pack 小装饰感。
每格中的主体必须保持同一身份、相近体量、完整落在格内并保留安全边距。
```
