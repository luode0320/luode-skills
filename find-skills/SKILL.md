---
name: find-skills
description: 当用户提出“我该怎么做 X”“帮我找一个做 X 的 skill”“有没有能做这个的 skill”这类问题，或表达想扩展能力的诉求时，帮助用户发现并安装可用的 agent skill。凡是用户在寻找可能以可安装 skill 形式存在的能力时，都应使用此 skill。
---

# 查找 Skills

这个 skill 用来帮助你从开放的 agent skills 生态中发现并安装合适的 skill。

## 何时使用本 Skill

当用户出现以下诉求时使用本 skill：

- 提出“我该怎么做 X”，而 X 很可能是已有 skill 已覆盖的常见任务
- 直接说“帮我找一个做 X 的 skill”或“有没有做 X 的 skill”
- 问“你能不能做 X”，而 X 属于某种专业化能力
- 明确表达希望扩展 agent 能力
- 想搜索工具、模板或工作流
- 提到希望在某个具体领域获得帮助，例如设计、测试、部署等

## 什么是 Skills CLI？

Skills CLI（`npx skills`）是开放式 agent skills 生态的包管理工具。Skill 是模块化能力包，用于通过专业知识、工作流和工具来扩展 agent 的能力。

**核心命令：**

- `npx skills find [query]` - 按关键词或交互方式搜索 skill
- `npx skills add <package>` - 从 GitHub 或其它来源安装 skill
- `npx skills check` - 检查 skill 更新
- `npx skills update` - 更新所有已安装的 skill

**浏览 skills：** https://skills.sh/

## 如何帮助用户查找 Skills

### 第一步：理解用户真正需要什么

当用户提出需求时，先识别：

1. 所属领域，例如 React、测试、设计、部署
2. 具体任务，例如写测试、做动画、评审 PR
3. 这是否是一个足够常见、很可能已经存在 skill 的任务

### 第二步：先检查排行榜

在运行 CLI 搜索之前，先查看 [skills.sh 排行榜](https://skills.sh/)，确认这个领域是否已经有知名 skill。排行榜按总安装量排序，优先呈现更流行、经更多用户验证的选项。

例如，Web 开发方向的热门 skill 包括：
- `vercel-labs/agent-skills` - React、Next.js、Web 设计（每个都有 100K+ 安装量）
- `anthropics/skills` - 前端设计、文档处理（100K+ 安装量）

### 第三步：搜索 Skills

如果排行榜里没有覆盖用户需求，再运行查找命令：

```bash
npx skills find [query]
```

例如：

- 用户问“如何让我的 React 应用更快？” -> `npx skills find react performance`
- 用户问“你能帮我做 PR 评审吗？” -> `npx skills find pr review`
- 用户说“我需要生成 changelog” -> `npx skills find changelog`

### 第四步：推荐前先验证质量

**不要只凭搜索结果就直接推荐某个 skill。** 始终验证以下内容：

1. **安装量**：优先选择安装量在 1K 以上的 skill，低于 100 的要谨慎。
2. **来源信誉**：`vercel-labs`、`anthropics`、`microsoft` 这类官方或知名来源，通常比未知作者更可靠。
3. **GitHub Stars**：检查来源仓库。若 skill 所在仓库少于 100 stars，需要保持怀疑态度。

### 第五步：向用户展示可选项

找到相关 skill 后，向用户展示时应包含：

1. Skill 名称，以及它能做什么
2. 安装量和来源
3. 可执行的安装命令
4. 在 skills.sh 上查看更多信息的链接

示例回复：

```text
I found a skill that might help! The "react-best-practices" skill provides
React and Next.js performance optimization guidelines from Vercel Engineering.
(185K installs)

To install it:
npx skills add vercel-labs/agent-skills@react-best-practices

Learn more: https://skills.sh/vercel-labs/agent-skills/react-best-practices
```

### 第六步：提供安装帮助

如果用户希望继续，你可以直接帮用户安装：

```bash
npx skills add <owner/repo@skill> -g -y
```

其中 `-g` 表示全局安装（用户级），`-y` 表示跳过确认提示。

## 常见 Skill 分类

搜索时，可以优先考虑这些常见类别：

| Category        | Example Queries                          |
| --------------- | ---------------------------------------- |
| Web Development | react, nextjs, typescript, css, tailwind |
| Testing         | testing, jest, playwright, e2e           |
| DevOps          | deploy, docker, kubernetes, ci-cd        |
| Documentation   | docs, readme, changelog, api-docs        |
| Code Quality    | review, lint, refactor, best-practices   |
| Design          | ui, ux, design-system, accessibility     |
| Productivity    | workflow, automation, git                |

## 高效搜索建议

1. **使用更具体的关键词**：例如 `"react testing"` 会比只搜 `"testing"` 更有效。
2. **尝试同义词或替代表达**：如果 `"deploy"` 没结果，可以试 `"deployment"` 或 `"ci-cd"`。
3. **优先查看热门来源**：很多 skill 都来自 `vercel-labs/agent-skills` 或 `ComposioHQ/awesome-claude-skills`。

## 当没有找到合适的 Skill 时

如果没有找到相关 skill：

1. 明确告知用户当前没有找到现成 skill
2. 说明你仍然可以直接依靠通用能力帮助完成任务
3. 如果这是高频需求，建议用户通过 `npx skills init` 创建自己的 skill

示例：

```text
I searched for skills related to "xyz" but didn't find any matches.
I can still help you with this task directly! Would you like me to proceed?

If this is something you do often, you could create your own skill:
npx skills init my-xyz-skill
```
