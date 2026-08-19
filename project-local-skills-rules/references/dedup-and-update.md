# 查重与更新细则

> 吸收自外部 skill-autosave（查重/更新流程），路径适配 WorkBuddy 环境。

## 落点（junction 说明）

- 项目级 skill 统一写入用户级 `C:\Users\luode\.workbuddy\skills\`（即 `~/.workbuddy/skills/`）。
- 该目录是 junction，物理指向 `D:\谷歌云盘\luode-skills`（luode-skills 仓库）——**用户级即仓库，勿在项目根另建 `skill/` 目录**（非标准加载路径，不会被自动命中）。
- 命名：`project-<项目slug>-<topic>-rules`，ASCII 小写 + 连字符，`-rules` 后缀。示例：`project-ellipal-db-rules`、`project-goadmin-api-rules`。

## 查重步骤

1. 列出已有项目级 skill：
   ```bash
   ls ~/.workbuddy/skills/ | grep '^project-'
   ```
2. 与目标名（`project-<slug>-<topic>`）比较 name 与 description，判断是否覆盖同一场景：
   - 完全覆盖 → 走「更新」流程。
   - 部分重叠 → 优先并入已有 skill（新增小节），不新建。
   - 无重叠 → 走「创建」流程。
3. 与全局 skill 对照：项目专属差异点才沉淀，通用规则不重复抄写（交 `skill-evolution-rules` 体系侧回补）。

## 创建

```bash
python3 ~/.workbuddy/skills/.system/skill-creator/scripts/init_skill.py project-<slug>-<topic>-rules --path ~/.workbuddy/skills --resources references
```

- 生成 SKILL.md 骨架 + agents/openai.yaml；随后按 `project-skill-template.md` 填充正文。
- 生成 `display_name`、`short_description`、`default_prompt` 时用 `--interface key=value` 传入。
- 校验：`python3 ~/.workbuddy/skills/.system/skill-creator/scripts/quick_validate.py <skill目录>`。

## 更新（已有 skill）

评估是否补充：
- 新步骤 / 边缘情况（上次没覆盖的边界）。
- 过时命令或 API（版本变更适配）。
- 踩坑记录（新增报错与解法）。
- 直接改 `SKILL.md` 或对应 reference，改后跑 `quick_validate.py`。

## 更新后登记

- 每次创建/更新后，在目标 skill 的 `references/source-notes.md`（或本 skill 的登记文件）追加一行：日期、项目、主题、做了什么。
