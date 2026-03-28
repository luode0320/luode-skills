# 内置设计搜索工作流

本 skill 已合并外部 `ui-ux-pro-max-skill` 的核心 `data/` 与 `scripts/`。
当内部规则不足以决定风格时，可以直接在当前 skill 内运行搜索脚本。

## 什么时候用

- 新页面没有现成视觉方向
- 只有一句“做得更专业、更像产品”但缺少具体风格
- 想快速补产品类型、配色、字体、落地页结构或 UX 细则
- 要对照某个技术栈的界面最佳实践

## 推荐顺序

1. 先用 `--design-system` 拿整套方向
2. 再按具体疑问继续查 `--domain`
3. 如果需要栈相关建议，再查 `--stack`
4. 最终仍以当前项目现有设计系统和本 skill 的约束为准

## 常用命令

```bash
python scripts/search.py "saas dashboard minimal modern" --design-system -f markdown
python scripts/search.py "fintech trust stable" --domain color
python scripts/search.py "hero social proof conversion" --domain landing
python scripts/search.py "animation accessibility loading" --domain ux
python scripts/search.py "rerender memo list" --stack react
```

## 常见查询域

- `product`：产品类型与风格方向
- `style`：视觉风格与效果
- `color`：配色方案
- `typography`：字体搭配
- `landing`：落地页结构
- `chart`：图表建议
- `ux`：交互、无障碍、体验规范
- `icons`：图标方向
- `react`：React / Next.js 体验与性能建议
- `web`：Web / App 界面可用性建议
- `google-fonts`：字体搜索

## 使用边界

- 搜索结果只作为风格参考，不等于必须原样落地
- 如果搜索结果和现有品牌、设计系统冲突，以项目现有规范为准
- 不要因为查到了更多风格就把一个页面做成混搭
