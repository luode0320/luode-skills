# Skills 培训文档

## 1. Skill 是什么

Skill 可以理解成“给 Codex 的专项作业手册”。

它不是模型参数微调，也不是插件市场里的二进制扩展，而是一组结构化文件，用来告诉代理：

- 这个 skill 解决什么问题。
- 在什么场景下应该触发。
- 具体应该遵循什么流程、规则和约束。
- 需要时去读哪些参考资料、脚本或模板。

一个 skill 的本质，是把团队经验、业务规则和固定工作流沉淀成可复用的上下文资产。

## 2. 什么时候值得写一个 skill

当下面任意一种情况反复出现时，就值得把它做成 skill：

- 团队有稳定的编码规范、评审规则、接口约定或业务术语。
- 每次做类似任务都要重新解释一遍流程和边界。
- 某些工作有固定步骤，直接交给代理时容易遗漏关键检查点。
- 某类任务依赖项目私有知识，例如目录约定、表结构、错误码、日志规范。
- 同一类问题每次都要重复贴长提示词，维护成本高，且输出不稳定。

## 3. Skill 的标准结构

一个最小可用的 skill 目录通常长这样：

```text
my-skill/
├── SKILL.md
├── agents/
│   └── openai.yaml
├── references/
│   └── xxx.md
├── scripts/
│   └── xxx.py
└── assets/
    └── ...
```

各目录职责如下：

- `SKILL.md`
  这是 skill 的核心文件，必须存在。
- `agents/openai.yaml`
  给工具 UI 用的展示信息，例如显示名、简介、默认提示语。
- `references/`
  放详细规则、业务文档、接口说明、约束清单等按需加载资料。
- `scripts/`
  放可执行脚本，用于需要稳定复用的操作。
- `assets/`
  放模板、示例工程、图标、字体等输出资产。

## 4. 写一个新 skill 的推荐流程

### 第一步：先定义它解决什么问题

写 skill 前，不要先写文件，先写这三个问题的答案：

1. 这个 skill 解决哪一类高频问题？
2. 什么样的用户请求应该触发它？
3. 它要把哪些团队规则变成稳定行为？

如果这三点说不清，skill 很容易写成一份冗长但触发不准的说明书。

### 第二步：先设计触发描述，再写正文

`SKILL.md` 顶部的 YAML frontmatter 最关键，尤其是 `description`。

原因是：

- 工具首先靠 `name` 和 `description` 判断这个 skill 何时应被使用。
- “什么时候用”必须写进 `description`，不要只写在正文里。
- 正文是在 skill 被触发之后才可能被读取。

一个合格的 `description` 至少要包含两类信息：

- 它做什么。
- 什么时候用它。

### 第三步：正文只写流程，不要把所有细节塞进去

推荐做法是：

- `SKILL.md` 只保留核心执行流程、决策点、引用入口。
- 详细规范放进 `references/`。
- 稳定重复的操作做成 `scripts/`。

这样做的好处是：

- 减少上下文长度。
- 后续更新某一块规则时不需要重写整份 skill。
- 不同任务只加载所需内容。

### 第四步：准备好示例和验证方式

一个 skill 写完后，至少要能回答下面两个问题：

1. 用户会怎么触发它？
2. 代理使用后，输出和行为会有哪些明显变化？

如果没有这两个验证点，skill 很难持续优化。

## 5. 在当前环境里创建一个新 skill

当前环境已经自带了 `skill-creator`，可直接用它的初始化脚本创建骨架。

初始化命令示例：

```powershell
python -X utf8 'C:\Users\Administrator\.codex\skills\.system\skill-creator\scripts\init_skill.py' `
  code-development-rules `
  --path 'E:\luode-skills' `
  --resources references `
  --interface display_name='Code Development Rules' `
  --interface short_description='Clarify requirements first and enforce team coding rules.' `
  --interface default_prompt='Use $code-development-rules to clarify requirements first and then implement the smallest safe code change.'
```

初始化后，重点编辑这几个地方：

- `SKILL.md`：写触发说明、执行流程、引用路径。
- `references/*.md`：写详细规则、模板、术语表。
- `agents/openai.yaml`：调整显示名、简介和默认提示词。

## 6. 怎么安装到 Codex

Codex 通常会从下面这个目录发现自定义 skill：

- 如果设置了 `CODEX_HOME`：`$CODEX_HOME/skills`
- 如果没有设置：`$HOME/.codex/skills`

PowerShell 安装示例：

```powershell
$skillName = 'code-development-rules'
$source = "E:\luode-skills\$skillName"
$targetRoot = if ($env:CODEX_HOME) {
  Join-Path $env:CODEX_HOME 'skills'
} else {
  Join-Path $HOME '.codex\skills'
}
$target = Join-Path $targetRoot $skillName

New-Item -ItemType Directory -Force -Path $targetRoot | Out-Null
if (Test-Path $target) {
  Remove-Item -Recurse -Force $target
}
Copy-Item -Recurse -Force $source $target
```

安装完成后，建议新开一个会话再使用，这样 skill 发现最稳定。

## 7. 怎么触发我们写的 skill

最稳妥的方式有两种：

- 显式调用：在提示词里写 `$code-development-rules`
- 隐式触发：让 `description` 足够准确，使工具知道在“按团队编码规范生成/修改代码”时该加载它

推荐显式调用示例：

```text
Use $code-development-rules to review this requirement, list clarification questions first, and only implement after the constraints are clear.
```

## 8. 怎么更新和优化 skill

建议把 skill 当成“团队规则产品”来维护，而不是写完就不动的静态文档。

### 更新触发条件

当你发现 skill 触发不准时，优先修改：

- `SKILL.md` 的 `description`
- `agents/openai.yaml` 的 `default_prompt`

因为很多问题不是规则不够，而是触发入口不够清晰。

### 更新规则内容

当你发现代理的行为仍不稳定时，优先修改：

- `references/` 下的规则文档
- `SKILL.md` 中的执行流程

推荐更新方式：

1. 收集一次真实失败案例。
2. 找出是“触发问题”还是“执行问题”。
3. 只修改对应那一层内容。
4. 再用相似请求回归测试。

### 什么时候加 scripts

如果某个操作一再重复，且输出必须稳定一致，就不要一直写成长文本说明，应改为脚本。

典型适合写成脚本的场景：

- 固定格式文件生成。
- 特定目录扫描和校验。
- 统一代码片段转换。
- 文档模板填充。

## 9. Skill 验证方式

写完后至少做两类验证：

### 结构校验

```powershell
python -X utf8 'C:\Users\Administrator\.codex\skills\.system\skill-creator\scripts\quick_validate.py' `
  'E:\luode-skills\code-development-rules'
```

如规则文档包含中文，Windows 下建议统一使用 python -X utf8 运行校验脚本。

### 行为验证

找 2 到 3 个真实请求测试：

- 一个需求描述完整的场景。
- 一个需求描述不完整的场景。
- 一个涉及边界条件、错误处理和日志约束的场景。

看代理是否真的会：

- 先澄清再实现。
- 在不明确时暂停。
- 维持最小化改动。
- 按规则输出注释、日志和错误处理。

## 10. 示例 skill：代码开发规则

这份培训文档同时配套了一个示例 skill：

- 路径：`E:\luode-skills\code-development-rules`
- 核心文件：`SKILL.md`
- 详细规则：`references/coding-rules.md`

这个 skill 解决的问题是：

- 让代理在写代码前先补全问题和边界。
- 当需求不清楚时，先停下来提问，而不是直接盲写。
- 在改代码时遵循最小变更原则。
- 统一注释、命名、常量、错误处理和日志输出习惯。

## 11. 什么时候用一个 skill，什么时候拆多个 skill

判断原则不要看“规则条数多少”，而要看“触发场景是否一致”。

更适合使用一个主 skill 的情况：

- 这些规则本质上属于同一套工作方式，会在同一类任务里一起生效。
- 用户在使用时，希望显式调用一次就让代理整体遵守，而不是手动拼多个 skill。
- 多组规则之间没有明显冲突，只是主题不同，例如沟通、编码、测试、交付。
- 规则共享同一触发入口，例如“按团队研发规范完成任务”。

更适合拆成多个 skill 的情况：

- 触发场景明显不同，例如“写业务代码”和“生成数据库迁移脚本”是两类不同工作。
- 所需工具、依赖、目录结构或外部系统完全不同。
- 某部分规则只在少数任务里才会用到，长期塞进主 skill 会造成上下文噪音。
- 不同 skill 的维护人、更新频率或审批边界明显不同。

简单判断法：

1. 如果用户一句话就能自然调用全部规则，优先一个主 skill。
2. 如果用户必须先判断“现在属于哪种任务类型”，再决定加载哪套规则，优先拆多个 skill。
3. 如果只是规则很多，但它们始终围绕同一研发流程，优先一个 skill，细节拆到 `references/`。

## 12. 对你这组规则的建议：一个主 skill，更合适

你给出的 23 条规则虽然覆盖了沟通、编码、测试、Git 和交付，但它们本质上都在约束同一个对象：

- 让代理按你们团队的研发协作方式完成任务。

因此我不建议把它们拆成多个彼此独立的 skill。原因有三点：

1. 这些规则在一次真实开发任务里通常会连续生效，而不是只命中其中一部分。
2. 如果拆成多个 skill，实际使用时很容易漏掉测试规则、交付规则或 Git 上下文规则。
3. 这套规则最适合做成“一个主 skill + 多个 references 主题文档”的结构，既统一入口，又便于后续维护。

## 13. 新的完整示例 skill：团队研发规则

这次补充了一套更完整的主 skill：

- 路径：`E:\luode-skills\team-development-rules`
- 核心文件：`SKILL.md`
- 沟通与澄清：`references/01-communication-and-clarification.md`
- 编码与变更：`references/02-coding-and-change-rules.md`
- 测试与验证：`references/03-testing-and-validation.md`
- 仓库协作与交付：`references/04-repo-and-delivery-rules.md`
- 方法修改保护：`references/05-method-change-guard.md`

这套结构的特点是：

- 对外只有一个显式调用入口：`$team-development-rules`
- 对内按主题拆细节，避免 `SKILL.md` 过长
- 后续新增团队规则时，可以优先往 `references/` 扩展，而不是直接把主文件写得越来越臃肿

如果你们要直接把这套完整规则安装到 Codex，安装脚本里的 `$skillName` 替换为 `team-development-rules` 即可。

推荐显式调用示例：

```text
Use $team-development-rules to read the latest commit first if available, clarify missing requirements, implement the smallest safe change, and complete testing before delivery.
```

## 14. 什么时候应该新建另一个 skill

未来如果出现下面这些情况，就应该新建另一个 skill，而不是继续往 `team-development-rules` 里堆：

- 某组规则只服务于特定技术域，例如“前端视觉设计规范”“数据库迁移规范”“OpenAI API 接入规范”。
- 某类任务需要独立脚本、模板、外部工具或私有文档。
- 某部分规则已经形成独立工作流，例如“PR 评论处理”“上线发布检查”“事故复盘报告生成”。
- 新规则的触发语义已经不再是“通用研发规则”，而是明确指向某个专门场景。

## 15. 早期简单示例 skill 的设计要点

之所以把你的规则做成 `SKILL.md + references/coding-rules.md` 两层结构，是因为这样更适合后续维护：

- `SKILL.md` 负责告诉代理“何时触发、按什么流程执行”。
- `references/coding-rules.md` 负责保存详细规则条目和确认模板。

后续如果你们要扩展更多团队规则，可以继续往 `references/` 里拆：

- `references/api-contract.md`
- `references/db-rules.md`
- `references/review-checklist.md`

这样不会把主 skill 写得越来越臃肿。

## 16. 常见坑

- 只写“规则是什么”，不写“什么时候触发”。
- 把所有内容都塞进 `SKILL.md`，导致正文过长、维护困难。
- 规则写得太抽象，没有明确的暂停条件和输出模板。
- 只靠自然语言要求代理遵守规范，不沉淀成 skill。
- 更新后不做回归验证，导致旧问题反复出现。

## 17. 团队推荐落地方式

如果你们打算把这套东西真正用于团队协作，建议这样做：

1. 先维护一个 Git 仓库，专门存放团队 skill。
2. 每个 skill 单独一个目录，避免规则混杂。
3. 先从一个高频场景开始，例如“代码开发规则”。
4. 每次出现失败案例，都补到 `references/` 或 `SKILL.md`。
5. 定期把稳定版本复制到 Codex 的 `skills` 目录中。

这套方式的本质，是把“每次重新解释一次要求”升级成“长期维护一份可复用规则资产”。
