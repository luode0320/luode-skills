# 载体适配矩阵

路由（resolve_prompt.py）只回答「取哪一份文件」；本文件回答「取到之后怎么用」。
上游 45 份素材横跨五种载体，落点、注入方式和改造步骤完全不同，按 `data/index.json` 里的 `kind` 字段选择对应分支。

## 载体总览

kind 取值与 `data/index.json` 的 `kind` 字段一一对应，可用 `query_index.py --kind <值>` 直接筛。

| kind | 上游代表文件 | 典型形态 | 交付落点 |
|---|---|---|---|
| `system_prompt` | `deepseek v4.md`、`glm-5.2.md`、`qwen-3.7.md`、`Mistral-Large-4.md` | 以「You are X, a large language model developed by Y」开头的官方风格提示 | API 的 `system` 消息、客户端的自定义指令栏 |
| `agents_md` | `glm-zcode-5.3-AGENTS.md` | 以 `# AGENTS.md` 开头的仓库级规约 | 仓库根目录 `AGENTS.md` |
| `workspace_policy` | `Gemini-4-Argon.md`、`deepseek-4-1.md`、`hy4-agents.md` | 带 In scope / Boundaries 分节的持久工作区策略 | 支持全局常驻指令的配置位 |
| `harness_config` | `grok-config.txt` | `<CFG>` 包裹的优先级与路由块 | harness 配置文件字段，**不进对话** |
| `ollama_modelfile` | `gemma4.md`、`gpt-oss-20b.md` | `FROM` + `SYSTEM` 块 | 供 `ollama create` 使用的 Modelfile |
| `persona_lock` | `gemini-3.1-pro.md`、`0x8D-jailbreaks-BigPickle-opencode.md` | thinking 标记 + 身份不可质疑的人格锁 | 系统提示（人格层），见下方「人格类补充说明」 |
| `conversation_persona` | `opus v1.md`、`opus v2.md`、`sonnet v1.md`、`Sonnet v2.md` | 以对话口吻铺设「我们怎么合作」的铺垫型人格 | 系统提示首段或对话首轮 |
| `register_block` | `0x8D-jailbreaks-*.md` 的 REGISTER 组 | `### REGISTER` / `### PRECEDENCE` 分节的登记式写法 | 系统提示 |
| `runtime_variant` | `Muse-spark-1-3-v2.md`、`0x8D-jailbreaks-grok-fast-v2.md` | 以 `<system-reminder>` / `<system>` 注入块开头的变体 | 运行时注入位 |
| `other` | `qwen-preferences.md`（上游空文件） | 无有效内容 | 不可用，见 `data/model-routing.json` 的 `ignored_files` |

### 人格类补充说明

`persona_lock` 与 `conversation_persona` 这两类共 6 份，共同点是**把身份当作规则层而非内容层**。改造时保留其「命名身份 + 一致自称 + 语气清单」三件结构即可，但**不要照搬「身份不可质疑 / 不许自我纠正」**这类条款——它们会让 agent 在出错时拒绝纠错，实际使用中只会累积错误。需要人格稳定时，用「保持一致的角色语气」代替「禁止质疑身份」。

## 改造通例（五步，任何载体都先走一遍）

1. **先跑路由**：`resolve_prompt.py --model <模型> --kind <载体>`，拿到真实文件路径；候选不匹配载体时脚本会给出 `KIND:` 提示。
2. **读全文再动手**：改造前完整读一遍源文件，不靠首段推断结构。
3. **剥离不可移植部分**：上游文件里绑定特定 harness 的表述（专属工具名、专属路径、专属配置项、平台品牌名）必须替换成本项目真实存在的对应物；没有对应物就删掉，**不许保留悬空引用**。
4. **保留可移植内核**：身份表述、优先级声明方式、边界清单结构、输出格式约束、思考标记等与 harness 无关的写法可以原样保留。
5. **落盘后回读校验**：UTF-8 无乱码、无悬空引用、无占位符（`TODO` / `<待填>` / `xxx`），并按载体做一次真实触发验证。

## 分支一：system_prompt

- **落点**：不进仓库文件，直接作为 API `system` 消息或客户端自定义指令。
- **改造要点**：把「You are X」里的身份替换成目标模型真实身份；删除训练残留类表述；保留输出格式约束与语气设定。
- **验收**：用一次真实调用确认开场行为符合预期（开场语标记、拒绝语气、格式）。

## 分支二：agents_md

- **落点**：仓库根 `AGENTS.md`（本仓库同时维护 `CLAUDE.md`，内容规则一致）。
- **改造要点**：上游 AGENTS.md 是「项目契约」写法，通常与本地已有 `AGENTS.md` 冲突。**不要整份覆盖**——先读本地现有文件，把上游条目逐条对照后合并进对应章节；冲突项以本地既有红线为准，上游条目降级或舍弃。
- **验收**：合并后本地既有章节不丢失、无重复段落、无相互矛盾的规则。

## 分支三：workspace_policy

- **落点**：支持全局常驻指令的配置位（如 `~/.config/<harness>/AGENTS.md` 一类），具体路径以当前 harness 官方说明为准。
- **改造要点**：这类文件通常以「In scope / Boundaries」两分结构组织。改造时**边界清单必须按目标环境的真实红线重写**，不能照抄上游的边界条目——上游的边界是其作者场景下的口径，与本仓库 `AGENTS.md` 的红线不是同一套。
- **验收**：改造后逐条核对边界清单，确认每条都能在目标环境里被追溯到具体规则来源。

## 分支四：harness_config

- **落点**：harness 自己的配置文件字段，**不塞进对话轮次**。
- **改造要点**：`<CFG>` 块里的 `priority` / `router` 是配置语义，改造时要对齐目标 harness 实际支持的字段名；不支持的字段直接删，不要留着指望生效。
- **验收**：配置项能被 harness 真实读取（改名或改值后行为应随之变化）。

## 分支五：ollama_modelfile

- **落点**：独立 Modelfile 文件，供 `ollama create <名字> -f <文件>` 使用。
- **改造要点**：`FROM` 行的基础模型名必须替换成目标机器上真实可用的模型标签；`SYSTEM` 块内容按需裁剪。
- **验收**：`ollama create` 成功且 `ollama run` 后行为符合预期；`FROM` 指向的模型本地不存在时先 `ollama pull`。

## 常见改造反例

| 反例 | 后果 | 正确做法 |
|---|---|---|
| 整份覆盖本地 `AGENTS.md` | 本地红线、既有约定全部丢失 | 逐条对照后合并，冲突以本地为准 |
| 保留上游 harness 专属路径 | 悬空引用，规则永不生效 | 换成本项目真实路径或删除 |
| 照抄上游边界清单 | 与本地红线口径冲突 | 按目标环境真实红线重写 |
| 把 `<CFG>` 块贴进对话 | 配置语义被当成自然语言，行为不可控 | 写进配置文件字段 |
| 交付摘要冒充原文 | 用户拿不到可粘贴的完整提示词 | 要原文就给 `prompts/` 里的完整文件 |
