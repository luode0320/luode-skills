# 计数锚点 Schema

## 目标

定义项目记忆三文件（`PROJECT_MEMORY.md` / `PROJECT_STYLE.md` / `PROJECT_HISTORY.md`）的"使用次数"计数锚点结构、字段约束和扩展边界。统一采用**机器索引区模式**：文件底部固定标题 + yaml fenced block，不散落进人类阅读区条目。

## 通用约束

1. 计数锚点区必须位于**文件底部**，与 `PROJECT_MEMORY.md` 既有"机器索引区必须位于底部"规则一致。
2. 计数锚点全部为**可选字段**：老文件/老条目缺失时按 0/null 处理，不报错、不强制全量迁移。
3. 锚点 key 必须**稳定且可回指**：能通过 key 定位到对应的人类阅读区条目或事件。
4. 条目标题被重写时，同步更新锚点 key；缺失锚点由收口闸门提示回补。
5. 计数块标题与 yaml 结构必须幂等，重复写入不得产生重复区块。
6. 写入的值必须是**合法 YAML 标量**，见下节；判据是解析器读得出，不是 `grep` 找得到。

## 0. 写入约束：中文技术内容的 yaml 裸标量（强制）

> 教训来源（2026-08-25）：某项目机器索引区因 3 处反引号开头的 `定义:` 值与 2 处 `- *_test.go` 列表项，**整块 yaml 长期解析失败**，16 个实体一个都读不到；而两个读取脚本当时都 `except yaml.YAMLError: return {}`，扫描结果显示 `candidates: []`、退出码 0，与「确实没有候选」完全无法区分，缺陷因此潜伏至今。

记忆文件里写的是中文技术描述，极易踩到 YAML plain scalar 的保留字符：

| 写法 | 后果 | 正确写法 |
|---|---|---|
| ``定义: `NEXCHANGE` 和 ...`` | `found character '\`' that cannot start any token` | ``定义: "`NEXCHANGE` 和 ..."`` |
| `- *_test.go` | `*` 被当成 alias 引用，找不到锚点即报错 | `- "*_test.go"` |
| `摘要: 结论: 通过` | 值内 `: `（冒号+空格）被解析成嵌套映射 | `摘要: "结论: 通过"` |
| `名称: 状态 #1 分支` | 值内 ` #`（空格+井号）被当成行内注释 | `名称: "状态 #1 分支"` |

规则：

1. 值的**首字符**属于 `` ` * & ! % @ { } [ ] , # ? | > `` 时，用双引号包裹整个值。`{}`、`[]` 等完整配平的 flow collection 除外。
2. 值内部出现 `: ` 或 ` #` 时，用双引号包裹整个值。
3. 已用 `"` 或 `'` 完整包裹的值就是正确写法，不要重复处理。
4. 双引号内的反引号、`$`、`*`、单引号都无需转义；只有值本身含双引号时才需转义。
5. 落盘后跑 `scripts/check_memory_anchors.py` 确认 `ok=true`——**文本写进去了不等于解析器读得出来**。

## 1. PROJECT_MEMORY.md — 扩展现有机器索引区

### `usage_tracking` 顶层键

在机器索引区 yaml 顶层新增（放在 `extensions` 之前），`version` 保持 1 向后兼容：

```yaml
usage_tracking:
  schema_version: 1
  counted_files: [PROJECT_MEMORY.md, PROJECT_STYLE.md, PROJECT_HISTORY.md]
  policy_ref: memory-usage-tracking-rules/references/usage-tracking-policy.md
```

### `entities[]` 可选字段

每实体追加 4 个可选字段（缺省即 0/null）：

```yaml
- entity_id: rule.apifox-test-separate-db
  name: Apifox 测试分离库规则
  type: 规则
  # ...既有字段不变...
  usage_count: 0
  usage_days: 0
  last_used_at: null
  absorbed_to: null
```

| 字段 | 类型 | 含义 |
|---|---|---|
| `usage_count` | `int` | 累计实际引用次数（同会话同实体只 +1） |
| `usage_days` | `int` | 累计引用天数（当天首次引用时 +1；用于"跨 ≥ 2 个日期"判定） |
| `last_used_at` | `YYYY-MM-DD` | 最近一次实际引用日期（与内容修订时间无关） |
| `absorbed_to` | `string` | 已吸收到的项目 skill 目录名（如 `project-luode-skills-memory-usage`）；非空即冻结计数，不再进吸收候选 |

约束：`usage_count` / `usage_days` / `last_used_at` 联动更新；`absorbed_to` 写入后，该实体不再参与 `scan_absorption_candidates.py` 候选输出，后续引用走 skill，除非该 skill 被删除回退。

## 2. PROJECT_STYLE.md — 新增计数锚点区

文件底部（`变更记录` 之后）新增：

```md
## 计数锚点区

```yaml
version: 1
anchors:
  - title: 中文优先表达
    usage_count: 0
    usage_days: 0
    last_used_at: null
    absorbed_to: null
```
```

- 锚点 key `title` 必须与人类阅读区 `### 标题` **完全一致**（去除 `### ` 前缀）。
- 每个 `### 条目` 应有且仅有一个锚点；新增条目时同步补锚点，删除条目时删除锚点。
- 标题含 Markdown 代码符号（反引号等）时，yaml 值用双引号包裹。

## 3. PROJECT_HISTORY.md — 新增计数锚点区

文件底部新增 `## 计数锚点区`，锚点 key 用事件条目 `- YYYY-MM-DD：` 后的**核心主题短语**（约前 12 字符，可前缀匹配）：

```yaml
version: 1
anchors:
  - title: 异步任务宿主任务列表桥接
    usage_count: 0
    usage_days: 0
    last_used_at: null
    absorbed_to: null
```

- **裁剪一致性（强制）**：事件被裁剪时，对应锚点**随事件一起删除**，不保留 retired 标记。理由：HISTORY 只保留最近 20 条窗口，被裁剪即已过窗口、失去"当前高频候选"价值；审计留痕写在当日日志而非文件内。
- 事件条目重写时同步更新锚点 title（保持前缀匹配语义）。
- HISTORY 计数仅作主题热度**弱信号**：吸收候选以 MEMORY/STYLE 为主；同一主题在 HISTORY 反复出现（`usage_days ≥ 2` 且次数 ≥ 3）可作为候选辅助证据，但不能单独触发吸收。

## 脚本解析契约

- `scripts/check_memory_anchors.py`：**结构健康检查，是另两个脚本的前置**。检查 yaml 可解析性（C1）、非法裸标量（C2）、schema 一致性（C3：`counted_files` 三项 + `policy_ref` + 四个计数字段）、锚点与条目一一对应（C4）、锚点区位于文件底部（C5）。`--list-missing` 输出待回补锚点清单。退出码 0=健康 / 1=有问题 / 2=读取异常。
- `scripts/usage_ledger_validate.py`：输入三文件路径 + claims JSON，校验锚点存在性/可定位性 + 会话内去重。
- `scripts/scan_absorption_candidates.py`：读三文件计数块，输出候选清单（usage_count / dates / absorbed_to / suggested_skill_name / dedup_hint）。
- 三脚本均为**只读**；计数写盘由 AI 编辑记忆文件完成，不脚本化写盘（三文件结构不同、回写含状态标记，AI 编辑更稳）。
- **解析失败不得静默**：后两个脚本的 yaml 解析失败一律抛 `AnchorParseError` 并以退出码 2 报错，禁止 `except: return {}` 退化成空结果——否则「解析失败」与「无数据」不可区分（2026-08-25 修）。
