# tapd-cli 实操陷阱

本文件只收录**实测踩过、且会导致静默错误结论**的坑。静默错误比报错危险——报错会停下，静默错误会让你拿着错数据往下走。

来源：2026-08-28 完成需求 1162459836001001627、2026-09-01 完成缺陷 1130399328001002897 的真实执行。

## 一、按人筛选：story 与 bug 的字段不一样

| 实体 | 正确字段 | 错误字段的表现 |
|---|---|---|
| `bug` | `current_owner=<中文名>` | — 正常生效 |
| `story` | `developer=<中文名>` | `current_owner=` **静默失效**，返回全项目需求且不报错 |

```bash
# 正确
tapd-cli bug   list workspaceid=<id> current_owner=罗德 status="<>closed" limit=50
tapd-cli story list workspaceid=<id> developer=罗德 limit=200
```

**为什么危险**：`story list ... current_owner=罗德` 会返回 100+ 条全项目需求且 `status:1 success`，看起来完全正常。若不校验返回条数是否合理、不抽查 `developer` 字段值，就会把别人的需求当成自己的领走。

**自检**：拉完后抽查几条的 `developer` / `current_owner` 字段是否真含目标用户名；条数异常多（接近项目总量）即判定过滤未生效。

## 二、`task` 实体通常是空的

本项目的活挂在 `story`（需求）和 `bug`（缺陷）上，`task` 实体查不到东西。**找活默认查 story + bug 两类**，不要只查 `task`。

## 三、状态过滤

```bash
status="<>closed"    # 排除已关闭
```

不加这个过滤，返回里会混大量 `closed` 项。另外 `status` 除了 `new`/`in_progress`/`resolved`/`closed`/`reopened` 这类标准值，还会出现项目自定义的 `status_1` ~ `status_5`，**不要假设状态集合是固定的**，按实际返回值处理。

## 四、模糊查询不可用，改本地过滤

`name="~关键词"` 语法**不生效**，返回空数组（不报错）。需要按关键词找单时，拉全量再本地过滤：

```bash
# 先看总量决定翻几页
tapd-cli story count workspaceid=<id>
# 再分页拉取，管道给 node/python 本地过滤
for p in 1 2 3 4; do
  tapd-cli story list workspaceid=<id> limit=200 page=$p fields="id,name,status,developer,created" \
    | node -e "<本地关键词过滤>"
done
```

`limit` 上限 200，`count` 子命令可先确认总量。

## 五、评论正文绝不能在 shell 里内联拼接

评论 `description` 是 Markdown，**直接在 shell 命令里拼正文会被破坏**：`---`（分隔线/表格分隔行）被当命令解析报 `-: command not found`，`|`（表格）被当管道，结果是内容**静默截断**后照常提交成功——返回 `ok: true`，但线上看到的是残缺评论。

`tapd-addcomment` 的 `add_comment.py` 本来提供了 `--description -` 从 stdin 读的路径，但**该脚本当前不可用**：第 344 行字典项 `"none_sdk_version": True` 后缺逗号，任何调用都直接 `SyntaxError`（2026-08-28 实测；属 skillhub 官方安装源，不要改它，改了会被更新覆盖）。

所以现阶段统一走 `tapd-cli comment add` + 读文件传参绕开 shell：

```python
import io, subprocess
desc = io.open('comment.md', encoding='utf-8').read()
subprocess.run(['node', '<skills>/tapd-cli/scripts/tapd-cli.cjs', 'comment', 'add',
                'workspaceid=<id>', 'entry-type=stories', 'entry-id=<19位id>',
                'author=<中文名>', 'description=' + desc],
               capture_output=True, text=True, encoding='utf-8')
```

提交后**核对回显正文的长度与结尾**，确认没被截断——CLI 会把实际写入的正文原样打印出来。

`entry-type` 需求用复数 `stories`，缺陷用 `bug`；Markdown 会自动转 HTML，格式细节与 @提及、回复评论的语义见 `tapd-addcomment`（文档可用，脚本不可用）。

建缺陷单同理走文件传参：

```bash
tapd-cli bug add workspaceid=<id> title=<标题> severity=normal priority=low \
  current_owner=<中文名> reporter=<中文名> description=<正文>
```

## 六、非交互 shell 里环境变量会缺失

在 WSL 里跑 CLI 报 `错误: 未设置环境变量 TAPD_API_ENDPOINT` 时，**不是 WSL 没配**——真源 `~/.tapd/env.sh` 两侧都有，是非交互 `bash -lc` 不加载 `~/.bashrc`（Ubuntu 默认 `.bashrc` 对非交互直接 return）。

两条出路，按场景选：

- TAPD 操作本来就不需要进 WSL，**直接在 Windows 侧（Git Bash）执行**最省事，用户级环境变量已注入
- 确需在 WSL 内执行时，命令前加 `source ~/.tapd/env.sh &&`

环境配置的完整事实（真源位置、注入层、更新流程、验证命令）以 `tapd-env-bootstrap` 为唯一权威，本节只记录这一个现象与判断方向，不重复定义配置。

## 七、用户名用中文昵称

`current_owner` / `developer` / `author` / `current_user` 全部用 TAPD 昵称（如 `罗德`），不是邮箱、不是登录名。用 `tapd-cli user info` 取 `data.nick`。

## 八、工时登记

收口时必须登记工时。三个易错点，都实测过。

**1. `entity_type` 用单数，与评论的复数不一样**

| 动作 | 参数 | 需求写法 |
|---|---|---|
| 评论 | `entry-type` | `stories`（复数）|
| 工时 | `entity_type` | `story`（单数）|

缺陷两处都是 `bug`，任务是 `task`。

**2. 必须先查再写——关单可能已自动生成占位记录**

同一 `entity_type + entity_id + spentdate + owner` 只允许存在一条记录，直接 `add` 会撞唯一约束。而**部分项目在需求置为 resolved 时会自动生成一条 `timespent=0` 的占位记录**，这是项目级配置差异，不能假设：

- 30399328 的 1001399 关单瞬间自动生成了 `timespent=0` 记录（`created` 与关单 `modified` 同一秒）
- 62459836 的 1001627 关单后查为 0 条

所以固定先查：

```bash
# 注意 entity_id 必须配 entity_type 一起传，只传 entity_id 会 422 param entity_type is required
tapd-cli timesheet list workspaceid=<id> entity_type=story entity_id=<19位id>
```

- 查到当天同 owner 的记录 → `timesheet update workspaceid=<id> id=<记录id> timespent=<小时> memo=<说明>`
- 没查到 → `timesheet add workspaceid=<id> entity_type=story entity_id=<19位id> timespent=<小时> owner=<中文名> spentdate=YYYY-MM-DD memo=<说明>`

**3. 单位是小时，0.5 为最小粒度**

团队实际记录里的取值是 0.5 / 1 / 1.5 / 2 / 3，没有出现过分钟或人天。`owner` 用中文昵称。

估算按**实际投入**，不按任务重要性，也不凑整到 8 小时。参考分档：

| 情形 | 参考值 |
|---|---|
| 只读核查 / 验证后关单，无代码改动 | 0.5 |
| 小改动（1~2 文件）含测试与报告 | 1 |
| 中等改动（3~5 文件）含真实测试闭环 | 2~3 |
| 跨模块、需搭环境或多轮验证返工 | 3 以上，按实际 |

`memo` 写清做了什么（改动点、验证方式），团队里写得细的记录可读性明显更好；留空虽被接受，但会让工时失去追溯价值。

## 九、更新状态

```bash
# 需求置为已实现
tapd-cli story update workspaceid=<id> id=<19位id> status=resolved current_user=<中文名>
```

返回体里会带更新后的完整 Story 对象，**核对 `status` 与 `modified` 字段确认真的改了**，不要只看 `status:1`（那是 API 调用成功标志，不是业务状态）。

### 缺陷不能直接置 resolved——工作流要求逐跳走，且中间跳有必填字段

需求可以一步 `status=resolved`，**缺陷不行**。缺陷受项目工作流约束，`new` 通常没有直达 `resolved` 的边，硬传会失败或静默不生效。

先拉工作流，筛出从当前状态出发的合法下一跳与必填字段（`Notnull=yes`）：

```bash
python <skills>/tapd-openapi/scripts/tapd_client_stdlib.py \
  get --endpoint workflows/all_transitions -p workspace_id=<id> -p system=bug
```

实测 30399328「研发内部需求」的缺陷工作流（2026-09-01，缺陷 1002897）：

| 起点 | 合法下一跳 | 该跳必填字段 |
|---|---|---|
| `new` | `new` / `in_progress` / `rejected` | 到 `in_progress` 必填 `de`（开发人员）、`effort`（预估工时）|
| `in_progress` | `in_progress` / `resolved` / `rejected` | 无 |
| `resolved` | `resolved` / `verified` / `reopened` / `closed` | 到 `verified` 必填 `te`（测试人员）|

所以 `new → resolved` 实际要走两跳：

```
POST bugs  status=in_progress  de=<中文名>  effort=<小时>
POST bugs  status=resolved
```

**每跳后回读实体核对再走下一跳**，缺陷额外核对 `resolved` 时间戳已写入：

```python
r = tc.request("GET", "bugs", params={"workspace_id": ws, "id": bug_id,
                                      "fields": "id,status,de,effort,resolved"})
```

**工作流是项目级配置，各项目不同**，上表只是一个实例，不能当通用常量套用——每次都读 `all_transitions`。

**终态止于 `resolved`**：`verified` / `closed` 代表测试已验证通过，属测试角色判定，自动化流程不越权置上。
