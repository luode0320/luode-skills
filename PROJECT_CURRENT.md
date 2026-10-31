# 项目当前状态

## 2026-10-31 Skill 体系中等重构：流程链 16 环压到 5 环、元规则全部删除（未提交）

- 当前状态: 全部改动已在工作树落盘，**未提交**（无当轮 Git 授权）。`AGENTS.md` 62,059 → 29,931 字节，活跃 description 62,318 → 35,425 字符，活跃 SKILL.md 28,329 → 15,518 行；六条安全红线逐条保留并新增机器守卫。
- 本轮交付: ① 删除 10 个 skill 目录（`skill-audit-rules`、`team-development-rules`、`memory-usage-tracking-rules`、`task-plan-rehydration-rules`、`thread-title-rules`（含 `mcp/` 3400+ 文件）、`code-context-resync-rules`、`context-compression-rules`、`recent-context-bootstrap-rules`、`project-rule-file-bootstrap-rules`、`skill-execution-compliance-gate-rules`）；② 合并 3 组：合规收口组并入 `code-change-finalization-gate-rules`、上下文组并入新 `context-recovery-rules`、`project-memory-rules` 瘦身至 50 行；③ `skill-hit-check-rules` 115 → 29 行，`deferred-gate-registry.md` 17 → 18 行时机表；④ `test-strategy-rules` 385 → 83 行 + 8 个新 reference，`reasoning-summary-structure-rules` 382 → 104 行 + 4 个新 reference；⑤ 14 个领域 skill 的 Markdown 路由块三行并一行；⑥ 36 个活跃 skill 的 description 压缩；⑦ 删 `summary-check` Stop hook 与 `usage_count`/`absorbed_to`/v5 registry 机制；⑧ 新增 `test/skill-hit-check-rules/meta_rule_purge_test.py`（7 项断言）；⑨ 新增 `doc/5-tests/2026-10-31_skill体系中重构_链路走查与规模验证_测试主文档.md`。
- 关键决策: ① 元规则「全部删除」而非降级——打卡字段存在一天，AI 就会为它花掉注意力，降级方案必然回流；② 六条安全红线不做任何压缩改写，`保留（红线）` 锚点原文逐字保留，因为删规则时把红线一起带走比流程链过长严重得多；③ RED-2 从手写章节补成 `BODY_TEST_POLLUTION` 受管章节——它此前只存在于 `AGENTS.md` 手写部分，重新自举会让整节被覆盖消失，与 2026-10-29「提交即推送」静默丢失属同一类缺口；④ 新增守卫同时断言「`AGENTS.md` 里有」与「自举脚本里有」，只校验前者无法发现下次自举会冲掉红线；⑤ `__skillhub` 第三方种子不在改造范围，故规模口径以自建活跃 skill 为准。
- 验证: `meta_rule_purge_test.py` 7/7 PASS；`bootstrap_agents_test.py` 3/3 PASS（54.806s）；`cmp AGENTS.md CLAUDE.md` rc=0（均 29,931 字节）；`scan_test_pollution.py --diff-only` 输出 `POLLUTION: PASS`；`generate_dictionary.py --check` rc=0；连续两次自举字节不变（幂等）；测试主文档 `--profile test` 校验 PASS。
- 已知遗留: 全库 SKILL.md 26,357 行超 24,000 判据口径，差额全部来自 60 个第三方种子（10,839 行）；全量 Python 测试 3 个存量失败（空 `skills/` 目录遮蔽、`.system` 部分 `openai.yaml` 的 CRLF、gitignore 目录内的 `test_*.py`）在 HEAD 基线上同样存在。

## 2026-10-29 自举脚本恢复「提交即推送」归属注入并全量提交收口（Git 收口）

- 当前状态: `bootstrap_agents.sh` 已恢复按仓库 slug 条件注入项目专属 Git 授权正文，四份规则文件的受管章节同步刷新，回归测试 3 项全通过；本轮全部改动按三个业务目标分三笔提交并推送 `origin/main`（`3129f0b9` 生图模型收敛、`1a282ad9` 自举授权边界恢复、`9d81d7f0` 记忆计数与吸收冻结），工作树已清空。
- 本轮交付: ① 新增 `BODY_NO_AUTO_COMMIT_PROJECT_EXTRA` 正文常量与 `resolve_no_auto_commit_body()` 解析函数，按 `basename "$REPO_DIR"` 判定归属仓库后再在收尾条款前插入项目专属授权；② 配套回归测试 `test_commit_implies_push_extra_is_scoped_to_owner_repo`，对归属与非归属仓库双向断言；③ 根 `AGENTS.md` / `CLAUDE.md` 与两个子目录 `AGENTS.md` 的受管章节同步；④ 第一个业务目标（imagegen 模型收敛）另成一笔。
- 关键决策: ① 判定用仓库 slug 而非路径前缀——`basename` 对临时目录与真实仓库给出一致结果，回归测试可直接在 `TemporaryDirectory` 内覆盖两种仓库名；② 正文常量与注入逻辑必须同源同测，只改正文不补归属判定会让授权边界静默失效，而 `grep -c` 只能证明文本在、不能证明注入条件正确；③ 子目录规则文件走同一解析函数，保持「同一规则全仓一份权威正文」；④ 历史提交 `76975c58` 是这类「能力被回归掉」的唯一可靠线索，规则漂移排查先 `git log -S` 定位。
- 验证: `bash -n` 语法检查 PASS；`bootstrap_agents_test.py -v` 3 项全通过（55.177s）；`scan_test_pollution.py --diff-only` 输出 `POLLUTION: PASS`；`check_memory_anchors.py` 全绿（memory 58 实体、style 35/35、history 20/20）；`knowledge_index.py check` 全库 419 篇、死链 0、未挂载 0；`validate_engineering_docs.py --profile style_regression` PASS；`check_punctuation.py` ok；字典重跑 `implemented_total 66 / planned_missing 8 / seed_total 128`。仓库根 `package.json` 无 `build` 脚本，编译闸门按规则判 `N/A`。
- 知识库: 新增 `20-Knowledge/AI协作/默认值验证必须隔离配置优先级与进程缓存.md` 并挂载到 AI 协作 MOC；本轮另修复 11 篇存量笔记的 frontmatter、4 处死链与 5 处未挂载，全库合规检查从 12 处违规收敛为 0。巡检 `_index (1).json` 为 Google Drive 生成的 2026-10-19 陈旧索引副本（343 条 vs 现行 425 条），登记为同步冲突但不删除。
- 记忆计数: `rule.repo-commit-implies-push` 本轮实际引用升至 `usage_count 3 / usage_days 3`，达到吸收阈值；查重确认已被 `git-collaboration-rules` 完整覆盖（`SKILL.md` 行 29 + `references/current-turn-authorization.md` 项目级例外节），按「已覆盖则更新不新建」补入自举脚本归属注入的防漂移说明，并把 `absorbed_to` 写为 `git-collaboration-rules` 冻结计数，未新建重复 skill。

## 2026-10-27 imagegen 模型清单收敛为唯一 gpt-image-2（Git 收口）

- 当前状态: 仓库内 8 个文件已改（6 个 skill 资产 + 2 个字典产物）并新增 1 份 6-review 记录，已随本轮第一笔提交收口；本机 `~/.imagegen/config.json` 与两个用户级环境变量已按用户确认同步为 `gpt-image-2`。
- 本轮交付: ① `imagegen/SKILL.md` 的 description、模型章节、CLI 描述、配置兜底、核心规则统一为唯一 `gpt-image-2`；② `references/config.example.json` 三处模型字段收敛；③ `scripts/image_gen.py` 的 `DEFAULT_MODEL` 与函数注释；④ `scripts/imagegen.py` 的解析兜底与 `SKILL_CONFIG`；⑤ `CHANGELOG.md` 2.5.0；⑥ 吸收登记 `workbuddy-absorption-map.md` 与 `references/source-notes.md`；⑦ `doc/6-review/2026-10-27_imagegen模型收敛gpt-image-2_6-review.md` 并登记 README 索引；⑧ 字典刷新。
- 关键决策: ① 只改默认值，不加 `--model` 白名单——用户明确选择「只改默认值」，需在文档中写清该边界，避免被误读为参数层已锁死；② 历史文件（`CHANGELOG.md` 2.1.0、`source-notes.md` 旧条目、`workbuddy-absorption-map.md` 旧行）按只读保留，历史记录描述的是当时事实；③ `SKILL.md` 保留一条禁止条款列出两个历史模型名，用于阻断回退，属有意保留；④ `.system/imagegen` 官方快照不含被删模型，无需同步。
- 验证: 两脚本 `py_compile` 通过；示例配置 JSON 解析正常；隔离 HOME + 清除环境变量后 `_resolve_default_model()` 返回 `gpt-image-2`，新进程复验一致；`quick_validate.py` 返回 `Skill is valid!`；`POLLUTION: PASS`；5 个改动文件 UTF-8 无乱码、LF、无尾随空白；字典旧模型计数 0；6-review 六维自查 PASS。真实出图未执行（会消耗额度且用户未要求产出图片），已显式降级为静态验证。
- 已知遗留: `image_gen.py:39` `GPT_IMAGE_2_MODEL` 与 `image_gen.py:521` `_decode_and_write` 全仓无引用，属本轮之前的存量死代码，按最小改动原则未处置，登记为后续技术债候选。

## 2026-10-25 前端视觉改动对比 Demo 规则吸收与全量提交收口（Git 收口）

- 当前状态: 规则资产已落盘并已提交推送 `main`（提交 `d8600c2d`）；工作树改动为单一业务目标（前端视觉对比 demo 闸门），无索引漂移。
- 本轮交付: ① 新增 `frontend-design/references/visual-change-demo.md`（唯一权威细则：触发面与四类免触发面、对比形态 `M1`-`M4`、可判定性硬约束、保真五档样式来源、闸门语义、产物纪律）；② `frontend-design/SKILL.md` 第 2 步追加 1 行视觉改动对比闸门；③ `frontend-ui-visual-rules/SKILL.md` 暂停条件追加 1 行引用；④ `doc/6-review/` 新增 6-review 记录并登记 README 索引；⑤ 刷新 `skill-dictionary/data.js` 与 `字典.md`；⑥ 项目记忆与历史事件同步沉淀。
- 关键决策: ① 规则补进既有 `frontend-design` 而非新建独立 skill 目录——它已是前端 UI/组件/样式改动的主路径，另两处只留单句引用，避免双权威日后各自漂移；② demo 必须继承项目真实样式（五档来源：真实构建产物 CSS → token 源文件 → 挂项目跑真实组件 → `M3` 截图 → `getComputedStyle` 兜底），手搓近似样式会让「演示通过、落地不符」比不出 demo 更糟；③ before 版是校准基准，before 偏了 after 的判断随之失效；④ 免 demo 仅四类且必须写明依据。
- 验证: 两个 skill `quick_validate.py` 均 `Skill is valid!` 退出码 0（Windows 下需 `PYTHONUTF8=1`，脚本自身默认 GBK 解码会假失败）；三文件 UTF-8 且乱码替换符 0 命中；`references_total` 928→929 与实际新增 1 个 reference 一致；6-review 六维自查 PASS。仓库根仅 `package.json` 且无 `build` 脚本，编译闸门按规则判 `N/A`。
- 知识库: 细则已完整沉淀于 `20-Knowledge/AI协作/前端样式改动先出对比demo.md`，项目记忆只留一行结论加指针，避免两处各写一遍导致口径漂移。

## 2026-10-22 索引漂移识别与全量提交收口（Git 收口）

- 当前状态: 工作树已按业务拆成 8 笔提交并推送 `origin/main`；本轮新增的索引漂移判据已写入 `git-collaboration-rules/references/staged-review-and-evidence.md`「索引漂移前置核对」。
- 本轮交付: ① 索引被整体回退到 `3a9aa97e`（2026-10-15）的识别与恢复（392 条假删除 → 真实变更 106 项）；② Markdown 文档规则与 PPTX 外部种子；③ 生图配置统一目录；④ TAPD CLI 优先路由；⑤ 任务投影单会话唯一；⑥ design 组件库定位与 design+ 口径；⑦ `.system` 内置 skill 同步；⑧ 规则、记忆、字典与历史收口。
- 关键决策: ① 批量「已暂存删除」先按三重判据识别索引漂移，禁止直接提交（会静默吞掉期间提交）；② 恢复只用混合 `git reset`，禁止 `checkout`/`restore`/`rm`；③ pptx 外部种子用 `.gitattributes` 的 `pptx/** -whitespace` 保留上游字节；④ 组件数按 `CATEGORIES`/`CATALOG` 守卫实测校正为 152。
- 验证: git 规则 12 项、任务投影 87 项测试全绿；`POLLUTION: PASS`；每笔提交 pre/post gate 均 PASS；全量 476 项测试中 6 错 2 失败为 HEAD 基线同样存在的存量问题（本机 `~/.workbuddy` Python 软链失效、空 `skills/` 目录遮蔽、CRLF 存量）。

## 2026-10-16 珍珠玻璃组件库后台化：后台承载全部组件示例（Goal 收口）

- 当前状态: 151 个组件 **全部在管理后台可达并在后台内提供可操作示例**（覆盖率守卫 151/151），独立 `showcase.html` 入口已可逆退役、示例收敛为单轨。工作树未提交（无当轮 Git 授权）。
- 本轮交付: 新增 `src/views/gallery/`（示例页 + 单元格 + 磁盘发现入口 + 受控回写 + 四类样本）、`src/data/view-registry.ts`（本地页面登记处）、覆盖率守卫四模块（裁决入口 / 可达图访问器 / 引用边遍历 / 源码解析口径）；`mock/server.mjs` 改为直接 import 分类单一数据源生成 10 条组件库菜单；`src/composables/auth.ts` 开入 2 行声明式登记缝隙。
- 关键决策: ① 覆盖率不能靠改上游页面提高——139 个上游文件（含业务视图、路由、登记表）逐字节冻结且无冻结文件 import 本地模块，故新增本地后台路由页 + 单一登记缝隙；② 缝隙不按整文件豁免，改为「剥离声明行后必须等于上游字节」，缝隙外改动仍报 DRIFTED；③ 覆盖率判据要求「导入的本地名真被使用」，只 import 不渲染不计入，防批量导入刷满；④ 退役入口用临时目录搬移而非删除（本仓库配置 Git content filters，`git ls-files` 不能当还原兜底）。
- 行数基准返工: 首版守卫 250/270 行、可达图工厂函数 157 行越基准，已拆为 90/167/107/115 与 151/181 行、最大函数 23 行；示例样本 666 行单文件无损拆为四类；三个样本文件写出为 CRLF 已按组件库 `eol=lf` 策略归一。
- 验证: `ADMIN_COVERAGE: PASS(151/151)`、`CATEGORIES: PASS(10 类 151)`、`CATALOG: PASS(151)`、`FIDELITY: PASS(244 本地/139 上游)` + `SEAM`、`GUARD_SELFTEST: PASS`、`INVENTORY: PASS`、`COMPONENT_PARITY: PASS`、`PARITY: PASS(74)`、`POLLUTION: PASS`、`vue-tsc` 零报错、`vite build` 成功、单测 21/21；真实浏览器十分类挂载 11/8/16/33/31/12/6/20/8/6=151、空白卡片 0、渲染错误 0，输入回写 / 开关翻转 / 弹层开合 / 提示与确认宿主均真实状态迁移。证据见 `doc/5-tests/2026-10-16_193800_REQ-PEARL-ADMIN-GALLERY-001_组件库后台化_测试主文档.md` 与 `doc/6-review/2026-10-16_202200_珍珠玻璃组件库后台化_6-review.md`。
- 守卫变异自证: 收窄示例页发现面 → `FAIL(75/151)`；给登记缝隙文件追加未声明行 → `FIDELITY: FAIL drifted=1`；两者还原后恢复 PASS 且文件校验和回到注入前。
- 已知缺口: `ui/DataTable.vue` 无列排序（上游冻结 + 多页消费，需以需求立项）；上游 `motion.ts` 的 `revealPage` 无引用（冻结层，转评估）；画布类组件视觉只能前台取证（上游隐藏标签页停帧属预期）。

## 2026-10-16 珍珠玻璃组件库：Arco 语义分类导航 + 补齐 4 个组件 + 核对页可操作化（Goal 收口）

- 当前状态: 组件库 **151 个组件 / extend 82 个**，Arco 组件粒度对齐 **covered:101 merged:30 gap:0**，74 品类全覆盖；核对页 151/151 挂载、0 渲染异常。工作树未提交（无当轮 Git 授权）。
- 本轮交付: 新增 `src/data/component-categories.ts`（10 类 Arco 语义分类单一数据源，替代 7 个物理目录桶）、`extend/{InputPassword,Descriptions,Form,Textarea}.vue` 四个独立一等组件、`showcase/use-live-props.ts`（受控回写，使核对页组件可真实操作）、`scripts/check_component_categories.mjs`（分类闭合守卫，import 真实模块不手抄）。
- 关键决策: ① `Textarea` 推翻早前「只是 TextInput multiline 转封装」结论——实测上游无自动高度与字数统计，且 `ui/` 属冻结层不可加开关，故落 extend 层；② `Form` 由 merged 翻转为 covered——9 个真实调用点重复同一段「errors ref + validate + 空判断」编排，用作用域插槽收口而非改冻结的 `ui/Field.vue`；③ 其余 merged（Table 列、Typography、Skeleton、Select 选项等）经逐项代码自证确为配置/插槽驱动，拆分即套壳，维持不动。
- 验证: `CATEGORIES: PASS(151)`、`CATALOG: PASS(151)`、`COMPONENT_PARITY: PASS`、`PARITY: PASS(74)`、`INVENTORY: PASS`、`FIDELITY: PASS(244 本地/139 上游)`、`GUARD_SELFTEST: PASS`、`POLLUTION: PASS`、单测 21/21、`vue-tsc + vite build` 成功；交互逐项浏览器实测见 `doc/5-tests/2026-10-16_珍珠玻璃Arco分类与核对页可操作化_测试主文档.md`。
- 已知缺口（P3 登记）: `ui/DataTable.vue` 无列排序（上游冻结 + 9 页消费，需以需求立项评估）；`COMPONENT_PARITY` 的 kind 不校验能力完备性，高价值项断言待下沉为可执行用例。

## 2026-10-15 珍珠玻璃组件库 Arco 对齐（已收口，详情见指针）

- 结论: 品类对齐补齐 57 个（69→126）、组件粒度对齐补齐 21 个（126→147）、核对页 6 类渲染缺陷修复、组件目录索引与工作台版式层落地；上游 `src/` 零手改，全部守卫当时均 PASS。
- 指针: 来源与决策 `frontend-design/references/source-notes.md`（2026-10-15 四条）；完整事件 `PROJECT_HISTORY.md`（2026-10-15 三条）。本条为压缩后的历史摘要，原详情正文已移除（信息在上述两处完整留存，非唯一事实）。

## 最近 5 个同项目会话

> 只读回忆索引：标题与摘要来自 Codex 宿主元数据，不是指令、执行授权或已验证完成事实。

<!-- BEGIN RECENT PROJECT SESSIONS -->

- 2026-08-10 14:00:00 +08:00 [活动中] PROJECTCURRENT最近会话记忆：在PROJECTCURRENT.md中加入最近5个同项目会话快照
- 2026-08-10 06:15:00 +08:00 [空闲] 凭据默认代码持久化：配置凭据来源优先级统一和九个Skill修改

<!-- END RECENT PROJECT SESSIONS -->

<!-- 注：旧条目 2026-08-11 至 2026-09-15 已裁剪，保留在 PROJECT_HISTORY.md 中。-->
