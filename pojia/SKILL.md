---
name: pojia
description: 当需要按「当前使用的模型」取用 / 改造前置提示词、人格锁定、工作区策略或 AGENTS.md 时触发；用户说「破甲 / pojia」「拉一份 XX 的系统提示」「这个模型该用哪份提示词」「把这份提示词改成 AGENTS.md / 工作区策略」「上游有没有更新」「升级 pojia 语料」都走这里。本 skill 是外部提示词语料库的唯一 Owner：内置 45 份上游 jailbreaks 快照 + 模型路由表，按模型名解析到对应提示词（未命中依次降级到厂商兜底与通用兜底），并可用 sync_upstream.py 从上游项目增量升级。只做语料检索、取原文与载体改造，不生成绕过第三方供应商安全策略的操作指导。
---

# 破甲（pojia）：模型前置提示词路由与语料工坊

用于「给定一个模型，我要它对应的前置提示词」这类任务：可能是指定某个模型要一份系统提示，也可能是想知道现在这份语料里有没有覆盖我正在用的模型，或者要把某份提示词改造成本仓库/自有 agent 能直接吃下的形态。

## 三步用法

### 第一步：确定模型与载体

先问清楚两件事，缺一个就先按项目现状推、推不出再问：

| 维度 | 取值 | 说明 |
|---|---|---|
| 模型 | 任意模型名 | 如 `claude-opus`、`Opus 4.6`、`GLM-5.3`、`deepseek-v4.1`。允许只给厂商名 |
| 载体 | `system_prompt` / `agents_md` / `workspace_policy` / `harness_config` / `ollama_modelfile`（另有 `persona_lock` / `conversation_persona` / `register_block` / `runtime_variant`） | 决定最终交付形态，见 `references/adaptation-matrix.md` |

不确定模型名的写法没关系，路由是模糊匹配的：全等 → 包含 → 厂商前缀 → 通用兜底。

### 第二步：路由并取原文

**脚本路径必须在 skill 基目录下解析**：本 skill 的资源块会给出 `Base directory`（如 `~/.dsh/skills/pojia`），
而会话工作目录通常是别的项目根，直接敲 `python scripts/resolve_prompt.py` 会报「找不到文件」。
先把基目录记为变量再调用：

```bash
SKILL_DIR="<本 skill 资源块给出的 Base directory>"
python "$SKILL_DIR/scripts/resolve_prompt.py" --model "Opus 4.6"        # 单次解析（精确匹配）
python "$SKILL_DIR/scripts/resolve_prompt.py" --model "某新模型" --fallback  # 未覆盖时显式授权用通用兜底
python "$SKILL_DIR/scripts/resolve_prompt.py" --model "glm-5.3" --kind agents_md
python "$SKILL_DIR/scripts/resolve_prompt.py" --list                     # 看全部族与候选
python "$SKILL_DIR/scripts/query_index.py" --vendor zhipu                # 按厂商浏览语料
python "$SKILL_DIR/scripts/query_index.py" --kind agents_md              # 按载体浏览语料
```

拿到 `FILE:` 指向的绝对路径后，**直接读那个文件**，把原文交给用户或进入改造。不要凭记忆复述提示词内容。

### 第三步：按载体改造

路由只解决「取哪一份」，把外部提示词变成能用的东西靠 `references/adaptation-matrix.md`：五种载体各自的落点、注入位置、改造步骤与验收点。

## 铁律

1. **路由先于记忆**：任何「这个模型用什么提示词」的判断，必须先跑 `resolve_prompt.py` 拿到真实文件路径，不允许凭印象指定。路由表是唯一权威（`data/model-routing.json`）。
2. **原文优先**：用户要「原文 / 完整提示词」时，直接给 `prompts/` 里的文件内容，不做摘要替代、不做删减。要摘要时明确标注是摘要。
3. **未命中必须先阻断、再降级，不准静默塞一份无关提示词**：
   - 默认行为是 **`NO_MATCH`**：退出码 1，不返回任何文件，只给出三步处置建议与候选兜底文件。宁可说「没覆盖」，也不给错的。
   - 第 1 级：用户确认可以先用通用提示词 → 加 `--fallback`，走通用兜底族（`Unified.md` → `hy4-agents.md` → `deepseek-4-1.md` 取第一份存在的），并打印 `DEGRADED`。
   - 第 2 级：用户希望「按这个模型定制」而语料里确实没有 → 主动提议升级：`python scripts/sync_upstream.py --check` 看上游有没有新模型，有就 `--apply` 拉下来；上游也没有，就用通用兜底 + `references/adaptation-matrix.md` 按目标模型的厂商风格改造。
   - 注意 `--fallback` 是**显式授权**语义，不是静默默认：不加它时看到 `NO_MATCH` 属于正常结果，不是故障。
4. **升级前先探测，不盲目拉取**：`--check` 是只读探测（`git ls-remote` 比对锁定 sha），`--apply` 才落盘。上游是活仓库，任何升级都要在 `references/upgrade-playbook.md` 登记一行。
5. **边界**：本 skill 提供的是**提示词语料与改造方法**。不生成绕过第三方供应商安全策略、伪造授权、定向攻击真实目标的指导；引用上游中「覆盖既有策略」一类写法时，只作为**研究样本**并标注为反例，不作为可执行模板交付。

## 新增 / 升级模型的三条路径

| 场景 | 动作 |
|---|---|
| 上游已有该模型 | `sync_upstream.py --apply` 拉取 → 在 `data/model-routing.json` 加族与别名 → `build_index.py` 重建 → `resolve_prompt.py --verify` |
| 上游没有，但同厂商有 | 把新模型写进同厂商已有族的 `aliases`，共享该族候选链 |
| 上游完全没有该厂商 | 走通用兜底族，按 `adaptation-matrix.md` 用目标模型的厂商风格就地改造，并把结论写进 `references/upgrade-playbook.md` 的「本地自建」区 |

## 脚本

| 脚本 | 用途 | 关键参数 |
|---|---|---|
| `scripts/resolve_prompt.py` | 模型 → 提示词文件（主入口） | `--model` `--kind` `--fallback` `--json` `--list` `--verify` |
| `scripts/query_index.py` | 按厂商 / 载体 / 族 / 手法 / 关键词检索 | `--vendor` `--kind` `--family` `--technique` `--keyword`（默认搜正文，`--meta-only` 只搜文件名与摘要）`--stats` |
| `scripts/build_index.py` | 扫描 `prompts/` 重建 `data/index.json` | `--check` 校验路由表候选是否齐全 |
| `scripts/sync_upstream.py` | 与上游仓库增量同步 | `--check` 只探测 / `--apply` 落盘并重建索引 |

四个脚本都是纯标准库、UTF-8 输出、无第三方依赖，Windows / Linux 双平台实测可用；`sync_upstream.py` 的临时克隆目录用完即删并回读确认，且文件哈希按 LF 规范化计算——同一份快照在两个平台得出的差异清单一致。

## References

- `references/adaptation-matrix.md`：五种载体的落点与改造步骤（改造任务必读）。
- `references/prompt-techniques.md`：从素材提炼的提示词写法手法与反例区。
- `references/upgrade-playbook.md`：升级与人工登记的完整流程。
- `references/source-notes.md`：上游坐标、版本锚点与裁决记录。

## 环境自检

```bash
SKILL_DIR="<本 skill 资源块给出的 Base directory>"
python "$SKILL_DIR/scripts/build_index.py" --check      # 路由表候选是否齐全
python "$SKILL_DIR/scripts/resolve_prompt.py" --verify  # 族覆盖与文件一致性
```

两条都输出 `PASS` 才算环境就绪；退出码非 0 说明路由表指向了不存在的文件，先跑 `sync_upstream.py --apply` 补齐。
