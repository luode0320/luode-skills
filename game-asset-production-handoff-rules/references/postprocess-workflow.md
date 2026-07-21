# 后处理流程

当已经拿到原始 2D 素材图时，使用本流程把它整理成可继续接入 Godot 的结果。

## 目标

把原始图整理成这些可复用产物：

- 透明背景 Sprite Sheet
- 独立帧 PNG
- GIF 动画预览
- QA 元数据 JSON
- 切开的 prop pack 单图

## 适用场景

- 角色、怪物、Boss 的动作 sheet
- 投射物、命中特效、法术动画
- 图标或掉落物的多帧动画
- 规则网格的 prop pack

## 默认步骤

1. 如果原图是纯洋红背景，先做去背。
2. 按行列切出每格。
3. 跳过完全空白格。
4. 对非空帧做透明边缘裁切。
5. 按 `center` 或 `bottom` 重新对齐到统一画布。
6. 导出独立帧。
7. 拼回透明 Sprite Sheet。
8. 可选导出 GIF。
9. 写出 QA 元数据。

## 脚本入口

```powershell
python scripts\postprocess_sprite_sheet.py sprite `
  --input raw_sheet.png `
  --output-dir out\hero_run `
  --rows 2 `
  --cols 2 `
  --anchor bottom `
  --chroma-key ff00ff `
  --gif
```

Prop pack 切片：

```powershell
python scripts\postprocess_sprite_sheet.py prop-pack `
  --input raw_props.png `
  --output-dir out\props_small `
  --rows 3 `
  --cols 3 `
  --chroma-key ff00ff
```

## 参数建议

- 角色、怪物：`--anchor bottom`
- 投射物、法术、命中特效：`--anchor center`
- 需要预览时：加 `--gif`
- 原图不是洋红背景时：不要传 `--chroma-key`

## QA 关注点

重点检查 JSON 里的这些字段：

- `frame_count`
- `non_empty_frames`
- `max_content_width`
- `max_content_height`
- `edge_touch_frames`

如果 `edge_touch_frames` 非空，说明有帧贴边，通常意味着原始图构图过满、切格不合适，或需要回炉重新生成。
