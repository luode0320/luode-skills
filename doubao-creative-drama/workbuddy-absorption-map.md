# 吸收裁决表：script-writing-studio → doubao-creative-drama

| 日期 | 来源 | 条目 | 本地现状 | 裁决 | agent 通用性 | 环境依赖 | 落点 | 整理去重 |
|---|---|---|---|---|---|---|---|---|
| 2026-11-14 | `script-writing-studio`（本地安装源 `C:\Users\luode\Downloads\script-writing-studio`） | 35 份 references 全量方法论（01 项目开发 / 01b 剧本写作 / 02 剧本医生 / 03 台词专家 / 04 AI 分镜 / 04b 运镜动作 / 05 资产库 / 06 Seedance 适配 / 07 后期声音） | 本地无剧情影视创作 skill；`doubao-creative-video/SKILL.md` L3 与 L148 已声明存在 `doubao-creative-drama`，但该 skill 实际不存在（断链） | 合并 | 通用，无 agent 专属路径 | N/A：全部为提示词与方法论正文，不依赖环境变量、宿主配置或 hook | 新建 skill `doubao-creative-drama/references/` 35 份 | 跳过 24 份 `(1)` 重复副本（逐字节相同）；`使用手册.md` 未整份搬运，按去重后抽成 `references/00-usage-guide.md`；21 份文件剥离 UTF-8 BOM 与同仓 `doubao-creative-video` / `xiaoshuo` 的「无 BOM」约定对齐 |
| 2026-11-14 | 同上 | 源 `SKILL.md` 262 行 | 无 | 合并 | 通用 | N/A | 新写 `doubao-creative-drama/SKILL.md` | 删除工作方法第 8 条「最终回复最后一行追加固定收束文案」；常用调用语前缀统一改为 `doubao-creative-drama`；新增「与其他 skill 的边界」段解决与 `doubao-creative-video` 的职责重叠 |
| 2026-11-14 | 同上 | 源 L206-210 固定收束品牌文案（原创声明 + 官方微信 + 官网域名） | 无 | 拒绝 | — | N/A | 不落盘 | 连带剥离 14 份 references 各 1 处「输出完整性复核」小节，共删除 145 行 |
| 2026-11-14 | 同上 | `01-script-creation.md` 的「核心原则速记」三处重复（开头 1/3、中部 2/3、结尾 3/3） | 无 | 合并 | 通用 | N/A | `references/01-script-creation.md` L42 + L603 引用块 | 三处收敛为一处唯一权威清单，保留中部独有第 6 条「不捏造」并入开头清单，中部改为指针、结尾整段删除 |
| 2026-11-14 | 同上 | `使用手册.md` 527 行（功能更新清单 / 调用方式 / 推荐流程 / 平台节奏档案 / 05→04→06 链路说明 / 常用调用语 12 组 / 材料清单 / 术语速查 / 维护说明） | 无 | 合并 | 通用 | N/A | `references/00-usage-guide.md` | 整份 28.1KB 精简为 5.8KB 入口速查；删掉与 `SKILL.md` 重复的推荐流程、平台节奏档案、阶段交接、05/04/06 机制解释与版本更新史，只保留"从哪开始 / 要什么材料 / 术语表 / 调用语"四段有效增量 |
| 2026-11-14 | 同上 | `agents/openai.yaml` | 无 | 合并 | 通用（宿主可选入口描述，不构成单 agent 绑定） | N/A | `doubao-creative-drama/agents/openai.yaml` | `display_name` 改为「短剧剧本创作工作室」以与 `doubao-creative-video` 区分；`default_prompt` 改用 `doubao-creative-drama` 口径 |

## 同域冗余扫描（2026-11-14）

扫描范围：`doubao-creative-drama`（新落盘）、`doubao-creative-video`（同域兄弟 skill）、`video-summary`（相邻链路）。

发现与清理：

1. **职责边界重叠**：`doubao-creative-video` 的 description 与 L148 已声明"短剧/剧情影视转 `doubao-creative-drama`"，新 skill 反向补齐对应声明，两边形成双向引用，无重复正文。
2. **重复段落**：`使用手册.md` 的推荐流程、平台节奏档案、阶段交接模板、05/04/06 机制说明与 `SKILL.md` 完全重叠，已按"单一权威 + 引用"收敛，仅 `SKILL.md` 保留机制正文，`00-usage-guide.md` 只保留面向用户的入口信息。
3. **门控层叠**：源 skill 的三处「核心原则速记」属同一门控重复播报，已收敛为一处。
4. **散落产物**：24 份 `(1)` 副本与临时脚本 `_strip_brand.py` 未留存；`使用手册.md` 与源 `SKILL.md` 未在目标目录留副本。
5. **引用链**：35 份 references 被引用 34 个文件名，断链 0；`07-post-music-sound-design.md` 仅由 `SKILL.md` 引用，属正常叶子模块。

结论：**PASS**。冗余已收敛，未引入与 `doubao-creative-video` 重复的工作流正文。

## 已删除源

- `C:\Users\luode\Downloads\script-writing-studio`（62 个文件 / 1,172,984 bytes，含 `SKILL.md`、`使用手册.md`、`agents\openai.yaml`、35 份 references 与 24 份 `(1)` 副本）—— 删除前逐文件核对：38 份非重复文件全部已在目标目录承接；14 份缺行文件的差额均等于品牌段剥离行数（10 或 11 行），无内容丢失。删除后 `Test-Path` 返回 `False`，实测已不存在。

## 落盘核验（删除前执行）

| 项 | 结果 |
|---|---|
| 源非重复文件数 | 38（1 份 SKILL.md + 1 份使用手册 + 1 份 openai.yaml + 35 份 references） |
| 目标承接 | 38/38 全部有对应文件 |
| 内容行数比对 | 24 份一致或更多；14 份减少 5–18 行，减少量逐份等于该文件被剥离的品牌段行数 |
| BOM 对齐 | 21 份剥离 BOM 后与同仓 `doubao-creative-video` / `xiaoshuo` 的「无 BOM」约定一致 |

## 八维评分（2026-11-14，打分人：独立子 agent，未参与编写）

| 维度 | 权重 | 得分 | 理由 |
|---|---|---|---|
| 1 Frontmatter 质量 | 8 | 9 | 363 字符；description 含做什么+何时用+触发词+改走 `doubao-creative-video` 的边界 |
| 2 工作流清晰度 | 15 | 9 | 9 行模块路由表 + 二级路由声明 + 3 套推荐流程，每阶段交接含下一步所需材料 |
| 3 边界条件覆盖 | 10 | 8 | 启动检查、冲突停止进入 06、字数超限拆段、材料不足先出暂定 |
| 4 检查点设计 | 7 | 8 | 01b 有 3 集一批的暂停-继续协议、用户反馈必暂停、A/B/C 模板选择确认 |
| 5 指令具体性 | 15 | 9 | 1900/2000 字硬上限、单组 ≤9 图、11 必填字段、镜头轨格式带对错示范 |
| 6 资源整合度 | 5 | 7 | references 全部可达、断链 0；评分时无 scripts（已补两个脚本，见下） |
| 7 整体架构 | 15 | 8 | 三层清晰；`04-core-workflow.md` 85KB、`06-core-format.md` 77KB 偏大 |
| 8 实测表现 | 25 | 7 | 评分时无实测记录 |

**总分 80.8 / 100**。短板 gap：实测表现 7.5、整体架构 3.0、边界条件 2.0。评分建议的「新建 scripts/ 把 06 §4 / 04 §9 自检清单变可跑脚本」已在本轮落实。

## 评分后补强（2026-11-14）

| 项 | 内容 | 涉及文件 |
|---|---|---|
| 新增可执行资产 | `scripts/check_seedance_output.py`：E0 无代码框 / E1 超 2000 字 / E2 代码框内平台参数 / E3 引用未定义编号 / E4 管理话术 / E5 图片参考超 9 张 / E6 缺 C 模板必需段落；W1 超 1900 字 / W2 代码框内 BGM / W3 否定式话术 / W4 镜头轨非五段 / W5 定义未使用编号。纯标准库，`--json` 可批处理 | `scripts/check_seedance_output.py`；`references/06-seedance2-adapter.md` §8；`SKILL.md`「脚本自检」 |
| 新增可执行资产 | `scripts/check_storyboard_output.py`：E1 缺 11 必填字段 / E2 有对白但台词与语气为空 / E3 下一段衔接为空 / E4 限制只写单向 / E5 未找到分镜；W1 运镜未写摄影机行为 / W2 光影只写空话 / W3 衔接写管理话术 / W4 正文出现硬时间码 | `scripts/check_storyboard_output.py`；`references/04-ai-video-storyboard.md` §9；`SKILL.md`「脚本自检」 |
| 实测验证 | 两脚本 `py_compile` 通过；good/bad/无输入三类样例全部跑通，退出码 0/1 符合预期（06：正常样例 PASS，错误样例命中 E3/E4 + W2/W4/W5；04：正常样例 PASS，错误样例命中 E2/E3/E4 + W1/W2/W4，缺字段样例命中 E1，无分镜样例命中 E5） | 临时测试脚本已删除，`scripts/__pycache__` 已清理 |

## 第二轮复评（2026-11-14，打分人：另一个独立子 agent，未参与编写与首轮评分）

| 维度 | 权重 | 首评 | 复评 | 复评理由 |
|---|---|---|---|---|
| 1 Frontmatter 质量 | 8 | 9 | 9 | description 覆盖全部业务线并写清改走 video 的边界，无需改动 |
| 2 工作流清晰度 | 15 | 9 | 9 | 9 行路由 + 二级路由 + 三套推荐流程，复评未发现断层 |
| 3 边界条件覆盖 | 10 | 8 | 8 | 边界清晰，但 06 的 `素材：` 写法与脚本判据冲突（见下） |
| 4 检查点设计 | 7 | 8 | 8 | 01b 三集一批暂停协议、A/B/C 模式确认仍在 |
| 5 指令具体性 | 15 | 9 | 9 | 1900/2000、9 图、11 字段、镜头轨五段格式均有硬数字 |
| 6 资源整合度 | 5 | 7 | 8 | 两脚本已接入 04 §9 与 06 §8 的自检节，引用链 41/41 全可达 |
| 7 整体架构 | 15 | 8 | 8 | 三层清晰；`04-core-workflow.md` 85KB / `06-core-format.md` 77KB 仍偏大 |
| 8 实测表现 | 25 | 7 | 8 | 两脚本零参退出码 2、带 `--file` 正常；但 E6 存在假阴性（见下） |

**总分 83.8 / 100**（首评 80.8，+3.0）。短板 gap：实测表现 5.0 ＞ 整体架构 3.0 ＞ 边界条件 2.0。

**复评指出的两条最该补**：① `check_seedance_output.py` 的 E6 假阴性——`check_blocks(text)` 只对全文做 `if name not in text`，段落写到代码框外仍判 PASS（实测样例 `seed_e6_falseneg.md`）；② `06-seedance2-adapter.md` 的 `素材：` 写法（L156「素材：林深参考 @图片2」，定义在代码框外）与脚本「编号必须在框外定义」判据冲突，导致照抄文档必被自判失败。

## 复评后补强（2026-11-14）

| 项 | 问题 | 改法 | 涉及文件 |
|---|---|---|---|
| E6 假阴性（最该补 ①） | `check_blocks(text)` 查全文，段落写到代码框外等于没交付却判 PASS | 签名改为 `check_blocks(code)`，判据改为 `missing = [name for name in REQUIRED_BLOCKS if name not in code]`；`run_checks` 调用点同步改为 `issues.extend(check_blocks(code))` | `scripts/check_seedance_output.py` |
| E3 假阳性（最该补 ②） | 旧判据要求编号「在代码框外」定义，但 C 模板把 `素材锚定` 写在框内，导致规范写法被误判 E3 | 新增 `split_shot_section(code)` 定位镜头轨区间；`used` 只取镜头轨内编号；`defined` 改为「框外素材段 + 框内镜头轨之前的定义」都算已定义 | `scripts/check_seedance_output.py` |
| docstring 与实现不一致 | 检查项清单漏列 `E0` 与 `W5` | 补齐两行说明 | `scripts/check_seedance_output.py` |
| 实测验证（三类样例） | — | ①全框内规范样例（素材锚定在代码框内）→ 221 字、ERROR 0 / WARN 0、PASS、exit 0；②段落全写框外 → ERROR 1（E6 命中七个必需段全缺）+ WARN 1（W5）、exit 1；③镜头轨引用 `@图5` 无定义 → ERROR 2（E3 + E6）、exit 1。另 `py_compile` 通过，`scripts/__pycache__` 与临时样例目录均已清理 | — |
