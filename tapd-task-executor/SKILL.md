---
name: tapd-task-executor
description: 寻找并执行当前用户的 TAPD 任务与缺陷。拉取当前用户名下未完成任务和 bug，逐个分析描述是否清楚、是否可实现/可修复，将可执行项定位到当前会话项目并自行实现与修复；若无任何可执行项，列出 3 条优先级最高的任务/bug 注明缺口等待完善。当用户表达主动领取工作意图时自动触发，典型说法：找 tapd 的任务做、找任务做、找 bug 做、看看 TAPD 有什么活、有没有任务可以做、有什么活可以干。依赖 tapd-openapi / tapd-cli / tapd-addcomment 复用其 API 与评论能力，执行前遵守 tapd-openapi 的环境预检，TAPD_TOKEN 未配置时阻断并按 tapd-env-bootstrap 核对环境。
allowed-tools: Bash,Read,Write,Edit,Glob,Grep
---

# TAPD 任务执行

自动领取并完成当前用户的 TAPD 任务/缺陷：找活 → 分析 → 分流 → 执行/兜底。

## 触发与依赖

- 触发：用户表达主动领取 TAPD 工作的意图（见 frontmatter description），无需 tapd.cn 链接。
- 依赖（复用，不重复实现）：
  - `tapd-env-bootstrap`：环境预检（TAPD_TOKEN / TAPD_API_ENDPOINT / TAPD_WORKSPACE_IDS）
  - `tapd-cli` / `tapd-openapi`：拉取任务与 bug、更新状态
  - `tapd-addcomment`：执行结果评论回写

## 执行流程

### 1. 环境预检

按 `tapd-env-bootstrap` 核对 `TAPD_TOKEN` 已注入且非空（只判断有无，禁止回显 Token 明文）。缺失 → 阻断并输出配置指引。`TAPD_WORKSPACE_IDS` 为空 → 提示但不阻断。

### 2. 确定当前用户

- 优先取环境变量 `TAPD_USER_NAME` 或 `CURRENT_USER_NICK`；
- 否则调用 `tapd-cli user info` 取当前登录用户 nick。

### 3. 拉取我的任务 + bug

遍历 `TAPD_WORKSPACE_IDS`（逗号分隔），对每个 workspace_id 执行：

- **优先** `tapd-openapi/scripts/tapd_client_stdlib.py mine`（一条命令同时拉我名下的需求+缺陷，含当前迭代定位、状态过滤、优先级排序、父需求树）：
  ```bash
  python <skills>/tapd-openapi/scripts/tapd_client_stdlib.py mine --workspace-id <id> --iteration current --status active
  # 只看缺陷加 --bugs；只看需求加 --storys；状态 all 不过滤
  ```
  mine 输出为表格（含 19 位 id、状态、优先级、owner、标题、详情链接），直接解析为候选清单。
- **兜底**（mine 不可用或需精确字段时）——**按人筛选的字段两个实体不一样，用错会静默返回全项目数据**：

  ```bash
  tapd-cli bug   list workspaceid=<id> current_owner=<用户> status="<>closed" limit=50
  tapd-cli story list workspaceid=<id> developer=<用户> limit=200
  ```

  story 用 `current_owner` 不报错但过滤失效；`task` 实体通常为空，找活默认查 story + bug。详见 `references/cli-field-pitfalls.md`。

汇总候选清单：id、标题、描述、优先级/严重度、状态、链接（`$TAPD_SITE_URL/tapd_fe/<workspace_id>/<story|bug>/detail/<entity_id>`）。

拉完先抽查几条的 `developer` / `current_owner` 是否真含目标用户名——条数接近项目总量即说明过滤没生效。

### 4. 归项目过滤（只筛当前会话项目）

- 目标 = 当前会话工作区项目（如 luode-skills、ellipal_admin）。
- 判定：标题/描述中出现当前项目名、仓库名、模块名特征词，或可解析出明确项目标识 → 归入；否则忽略（不进兜底清单）。
- 无法判定归属 → 忽略并记录原因。
- 跨项目任务一律不写（红线，见下）。

### 5. 描述清楚度 + 可实现性分析

按 `references/task-analysis-criteria.md` 判定表逐条评估，输出四类：

- **可执行**：描述清楚（目标/范围/输入输出/验收，或复现步骤/预期实际）且可实现（代码可达、依赖可获取、无外部权限依赖、可本地验证）
- **疑似已完成**：查证确认功能已在仓库内落地，只是 TAPD 状态没同步
- **待完善**：仓库内查无痕迹且关键信息缺失 → 记录缺口
- **忽略**：描述基本为空或纯转发

**只有标题的老单必须先回仓库查现状再定性**：描述为空、无评论、创建日期较早的单，很可能早已实现只是没人回来改状态。直接判「待完善」会丢掉一个能立刻关掉的单，直接判「待执行」会重复造轮子。按标题里的名词在仓库搜实现与前端定义，再比对创建日期附近的提交记录。

### 6. 执行 / 兜底

可执行清单非空 → 逐条闭环：

1. **领取**：任务更新 `status=progressing`；缺陷按工作流置处理中（先读 `workflows/all_transitions` 拿合法下一跳与必填字段，方法同下方第 4 步；确实读不到映射时才退回「仅评论说明开始处理」，不凭猜测硬改状态）
2. **实现**：按宿主仓库 AGENTS.md 与既有规则闭环（需求接入/实施拆解/编码/真实测试/验证，按需联动 requirement-intake-rules、implementation-planning-rules、bug-root-cause-rules 等）
3. **回写**：评论执行摘要，**按「TAPD 回写三件套」小节的分节骨架写，禁止平铺一整段**；正文写进文件再读文件传参，提交后核对回显字符数。（`tapd-addcomment` 的脚本当前有语法错误不可用，见 `references/cli-field-pitfalls.md`。）
4. **收口（状态自动流转到 resolved）**：不自动 git commit，但**需求与缺陷的终态都自动流转，不再交人工**。

   需求：`tapd-cli story update workspaceid=<id> id=<19位id> status=resolved current_user=<用户>`。

   缺陷：**不能假设 `new` 能直达 `resolved`**——多数项目工作流要求逐跳走，且中间跳有必填字段。先读工作流再按最短合法路径逐跳流转：

   ```bash
   # 1) 拉全部流转，筛出从当前状态出发的合法下一跳与必填字段（Notnull=yes）
   python <skills>/tapd-openapi/scripts/tapd_client_stdlib.py \
     get --endpoint workflows/all_transitions -p workspace_id=<id> -p system=bug
   # 2) 逐跳 POST bugs，带上该跳的必填字段
   #    实测 ellipal「研发内部需求」：new -> in_progress（必填 de、effort）-> resolved
   ```

   **每跳后必须回读实体核对 `status` 真的变了再走下一跳**——`status:1` 只是 API 调用成功，不是业务状态；缺陷额外核对 `resolved` 时间戳已写入。任一跳回读不符即停止并报告，不继续往下跳、不谎报已关单。

   **终态止于 `resolved`，不自动流转到 `verified` / `closed`**：那两个状态代表测试已验证通过，是测试角色的判定，开发侧自动置上等于自己给自己验收。`resolved` 的语义是「开发已修复，待验证」，这正是本流程能负责的边界。
5. **登记工时（强制）**：改完终态必须填工时，不填不算收口。先查再写——同一实体同一天同一人只能有一条记录，且**部分项目关单时会自动生成 `timespent=0` 占位记录**（项目级差异，不能假设）：

   ```bash
   tapd-cli timesheet list workspaceid=<id> entity_type=story entity_id=<19位id>
   # 查到 → timesheet update workspaceid=<id> id=<记录id> timespent=<小时> memo=<说明>
   # 没查到 → timesheet add workspaceid=<id> entity_type=story entity_id=<19位id> \
   #            timespent=<小时> owner=<中文名> spentdate=YYYY-MM-DD memo=<说明>
   ```

   单位小时、0.5 为最小粒度，按**实际投入**估不按任务重要性估：只读核查关单 0.5、小改动含测试 1、中等改动含测试闭环 2~3、跨模块或多轮返工 3 以上。`entity_type` 用单数（与评论的复数 `entry-type=stories` 不同）。详见 `references/cli-field-pitfalls.md`。

6. **交付给用户时必须给可点链接，不能只给裸 id**：格式 `$TAPD_SITE_URL/tapd_fe/<workspace_id>/<story|bug>/detail/<19位id>`。新建的单还要一并说明**所在项目**与**是否属于某个迭代**——多 workspace 场景下用户默认只看主项目，`iteration_id=0` 的单不进迭代看板，只给 id 会导致用户根本找不到（2026-08-28 真实发生过）。

**疑似已完成**清单非空 → 先向用户确认需求字面目标的边界（例如「加到流水」是指展示列，还是要能按它筛选/聚合——边界不同工作量差一个数量级，这是用户的决定），确认后补跑真实验证出报告，再按上述 3~6 走完回写评论、改状态、登记工时与交付链接。**不要凭代码印象直接关单**；工时按补验证的实际投入填，不因「代码早就写好了」而省略。

验证过程中发现顺带缺陷时**停下来问用户**（修 / 记为遗留 / 另开缺陷单），不擅自扩大改动范围。

可执行与疑似已完成清单都为空 → **兜底**：从待完善清单按「缺陷优先、严重度/优先级、创建时间早者优先」排序，列 3 条高优先级任务/bug，逐条注明缺什么信息、由谁完善。

### 7. 改动找不到对应单时

手上已有改动但不确定挂哪个单时，**先证明真的没有**再问用户：拉全量需求与缺陷（`count` 确认总量 → 分页 `limit=200` → 本地关键词过滤，模糊查询语法不可用），两个 workspace 都扫。

确认无对应单后，把「建单 / 不建单」交给用户决定，不擅自建单。判断素材给足：这批改动是什么性质、有没有影响线上行为的策略变更、当前有哪些留痕（commit message、测试报告）。安全策略类变更零留痕的风险要明说。

## TAPD 回写三件套（强制）

单子做完了，TAPD 上必须留下三样东西，**缺任何一样都不算收口**：

| # | 动作 | 判定「真的做到了」的依据 |
|---|---|---|
| 1 | **评论**执行摘要 | 回显正文字符数与本地一致（防静默截断） |
| 2 | **工时**登记 | 回读记录的 `timespent` / `modified` 已变 |
| 3 | **状态**流转 | 回读实体 `status` 已变，缺陷额外看 `resolved` 时间戳 |

三者都不能只看接口返回的 `status:1`——那只是调用成功，不是业务生效。

### 1. 评论必须分节，禁止平铺一整段

一大段连续文字没人读得下去，关键信息（验证结果、遗留风险、代码是否已提交）会被埋掉。**用小标题分节 + 列表 + 表格**，让人扫一眼就能定位。

按下面的骨架写，没有的节直接省略，不要留空节：

```markdown
## 结论
一句话说清做了什么、当前处于什么状态。

## 根因
缺陷才写。现象 → 定位 → 为什么会这样。
若核查结果与原始描述不符，**在这里显式指出出入**，不要默默按自己的理解改。

## 修复方案 / 实现方案
改了什么、为什么这么改。有被否决的替代方案就写清否决理由。

## 验证方式与结果
用表格，一行一个检查项：

| 检查项 | 期望 | 实测 |
|---|---|---|
| ... | ... | ... |

## 验证边界
**如实写没验什么、为什么不验。** 不写这节会让人默认「全验过了」。

## 遗留风险
没有就写「无」，不要省略这节。

## 代码状态
已提交 / 已改动未提交，二选一写死。
```

硬要求：

- **正文写进文件再读文件传参**，绝不在 shell 里内联拼接——Markdown 的 `---` 会被当命令、`|` 会被当管道，内容**静默截断后照常提交成功**（返回 ok，线上是残缺评论）
- 提交后**核对回显正文的字符数与结尾**，与本地一致才算数
- 结论与事实不符时补发更正评论，不留错误留痕（例如先写了「交人工」后又自动流转了）
- 敏感信息脱敏；Token 一律不回显

### 2. 工时：先查后写，更新优先于新增

同一实体 + 同一天 + 同一人**只允许一条记录**，直接 `add` 会撞唯一约束；部分项目关单时还会自动生成 `timespent=0` 占位记录。所以**固定先 list 再决定 update 还是 add**。

**同一天内**二次投入同一个单（例如同日换个会话补验证、返工重跑），走 **update 把工时累加上去**，不要新增第二条，`memo` 把两次做的事合并写清；**跨天**的二次投入才是新增一条（`spentdate` 不同，不冲突）。

按**实际投入**估，不按任务重要性估。分档与字段细节见 `references/cli-field-pitfalls.md`。

### 3. 状态：读工作流、逐跳走、每跳回读

不要假设能一步到终态。方法见上方第 6 节第 4 步，终态止于 `resolved`。

## 红线（强制）

- 只处理能归到当前会话项目的任务/缺陷；其他项目代码只读，不产生任何写入（AGENTS.md 跨项目红线，用户口头授权也不放行）。
- TAPD Token 禁止回显；评论/描述中的敏感信息脱敏。
- 不自动 git commit / push（此条不因状态可自动流转而放宽，两者互不相干）。
- 状态流转**可自动执行**，但只走到开发侧终态 `resolved`；`verified` / `closed` 属测试验收判定，不自动置。每跳后回读核对业务状态，回读不符即停止并如实报告。
- 单条任务实现必须走真实测试与验证，禁止只改代码不验证。
- 回写三件套（评论 / 工时 / 状态）缺一不算收口；评论必须分节，禁止平铺一整段。

## 参考

- `references/task-analysis-criteria.md`：描述清楚度与可实现性判定标准、疑似已完成分流、优先级排序规则
- `references/cli-field-pitfalls.md`：tapd-cli 实测踩过的静默失效陷阱（按人筛选字段、状态过滤、模糊查询、评论传参、环境变量位置、状态更新核对）
