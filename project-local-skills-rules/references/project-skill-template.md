# 项目子 Skill 模板

```md
---
name: <project-topic-skill-name>
description: 当<明确触发条件>时触发。负责<核心职责>；不要用它代替<边界外 skill>。
---

# <标题>

## Skill 作用与适用场景

- ...

## 自动触发信号

- ...

## 进入后先做什么

1. ...

## 默认执行流程

1. ...

## 权责边界与不负责事项

- ...

## 执行通过 / 驳回标准

- 通过：...
- 驳回：...
```

## 命名建议

- 统一前缀：`project-<项目slug>-`；统一后缀：`-rules`
- 示例：`project-ellipal-db-rules`、`project-goadmin-api-rules`
- 保持 ASCII 小写 + 连字符，便于跨平台工具处理与自动命中
- 落点：项目根目录 `skills/`（luode-skills 仓库以仓库根为 skill 资产库，直接落根）；命中由项目级 `AGENTS.md` / `CLAUDE.md` 显式引用，不依赖工具专属路径

## 质量标准（吸收自 skill-autosave）

- ✅ description 清晰描述触发场景（什么时候用、什么情况下命中）
- ✅ body 包含具体可执行步骤，不是泛泛而谈
- ✅ 包含踩过的坑和注意事项（报错、解法、边界）
- ✅ 代码 / 命令能直接复制执行
- ❌ 泛泛而谈的指导
- ❌ 只描述问题不给方案
- ❌ 过度冗长的解释

