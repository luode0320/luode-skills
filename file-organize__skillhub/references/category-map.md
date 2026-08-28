# 文件分类规则表（category-map）

> 本文件是分类规则的权威定义源；SKILL.md 内联速查表引用本文件，新增/调整分类只改这里。

## 默认分类表

| 类别 | 子文件夹名 | 扩展名 |
|------|-----------|--------|
| 文档 | 文档 | .pdf, .docx, .doc, .md, .txt, .pptx, .ppt, .xlsx, .xls |
| 图片 | 图片 | .png, .jpg, .jpeg, .gif, .bmp, .svg, .webp, .ico |
| 压缩包 | 压缩包 | .zip, .rar, .7z, .tar, .gz, .mrpack |
| 安装程序 | 安装程序 | .exe, .msi, .msu |
| DLL文件 | DLL文件 | .dll |
| 代码 | 代码 | .java, .py, .js, .ts, .html, .css, .json, .xml, .yaml, .yml, .c, .cpp, .h, .go, .rs |
| 日志 | 日志 | .log |
| Minecraft | Minecraft | .litematic, .schematic |
| 其他 | 其他 | 以上未覆盖的扩展名 |

## 自定义规则约定

- 用户自定义规则优先级高于默认表；自定义时保留「类别 → 子文件夹名 → 扩展名列表」三元组结构。
- 扩展名一律小写匹配（`.PDF` 等同 `.pdf`）。
- 无扩展名文件归「其他」并单独列出（不猜测类型）。

## 维护记录

- 2026-08-26：初始版本（从 SKILL.md 内联表迁移，作为分类规则权威源）。
