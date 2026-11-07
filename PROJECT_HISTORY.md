# 项目历史事件

> 本文件追加关键历史事件并只保留最近 20 条（按日期倒序、新事件置顶、追加后自动裁剪）；普通启动默认不读取，只有历史追问、当前状态不足或真实卡点时才窄检索。

## 事件
- 2026-10-31：**Skill 体系中等重构：流程链 16 环压到 5 环，元规则全部删除，六条安全红线保留并加守卫**。用户判断「skill 执行流程太长，很多 agent 本身已经支持了」，只读盘点证实：194 个 skill 的 description 常驻合计 62,318 字符、`AGENTS.md` 62,059 字节、普通「改一个 Go 函数」串行经 16 环强制 + 3 环条件、延迟 gate 登记 9 强制 + 8 条件，且历史线是累积型膨胀（4 月 67 个 SKILL.md → 10 月 197 个，8 月合并 17 个目录后顶层 `*-rules` 仅从 90 降到 89）。按用户四项决策执行中等重构：删除 10 个 skill 目录（含 `task-plan-rehydration-rules` 的 v5 投影 registry 与 `summary-check` Stop hook、`memory-usage-tracking-rules` 的 `usage_count`/`absorbed_to` 吸收机制），合并合规收口组与上下文组，`skill-hit-check-rules` 115 → 29 行且不再产出打卡字段，`test-strategy-rules` 385 → 83 行、`reasoning-summary-structure-rules` 382 → 104 行（细节移入 12 个新 reference）。关键决策：① 元规则全部删除而不降级——打卡字段存在一天，模型就会为它分配注意力，降级方案必然回流；② 六条安全红线的锚点原文逐字保留，删规则时把红线一起带走比流程链过长严重得多；③ 发现 RED-2 测试污染红线此前只存在于 `AGENTS.md` 手写章节、自举脚本无对应常量，重新自举会让整节被覆盖消失——与 2026-10-29「提交即推送」静默丢失同类，已补成 `BODY_TEST_POLLUTION` 受管章节；④ 新增守卫必须同时断言「`AGENTS.md` 里有」与「自举脚本里有」，只校验前者发现不了下次自举会冲掉红线。验证：`meta_rule_purge_test.py` 7/7 PASS；`bootstrap_agents_test.py` 3/3 PASS（54.806s）；`cmp AGENTS.md CLAUDE.md` rc=0（各 29,931 字节）；`scan_test_pollution.py --diff-only` 输出 `POLLUTION: PASS`；`generate_dictionary.py --check` rc=0；连续两次自举字节不变。规模：`AGENTS.md` 62,059 → 29,931 字节，活跃 description 62,318 → 35,425 字符，活跃 SKILL.md 28,329 → 15,518 行，强制串行 16 → 5 环。遗留：全库行数 26,357 超判据口径，差额全来自 60 个不改造的第三方种子。本轮改动未提交。
- 2026-10-29：**自举脚本恢复「提交即推送」按仓库归属注入，并同步四份规则文件的受管章节**。用户要求「吸收经验并根据 git 提交 skill 的规则，所有文件提交 git」。开工复核发现 `project-rule-file-bootstrap-rules/scripts/bootstrap_agents.sh` 当前版本的 `sync_agents_file()` 直接使用通用 `BODY_NO_AUTO_COMMIT`，而历史提交 `76975c58` 曾实现过「仅归属仓库注入项目级推送默认值」的条件注入——该能力在某次改写中丢失，导致本仓库重新自举时会丢失推送默认值。修复方式：新增 `BODY_NO_AUTO_COMMIT_PROJECT_EXTRA` 正文常量与 `resolve_no_auto_commit_body()` 解析函数，按 `basename "$REPO_DIR"` 判定归属仓库后再在收尾条款前插入项目专属授权；配套新增回归测试 `test_commit_implies_push_extra_is_scoped_to_owner_repo`，对 `luode-skills` 与 `some-other-project` 两个仓库名做双向断言。关键教训：① 受管章节的正文常量与注入逻辑必须同源同测，只改正文不补归属判定会让授权边界静默失效，而 `grep -c` 只能证明文本在、不能证明注入条件正确；② 判定必须用仓库 slug 而非路径前缀，`basename` 对临时目录与真实仓库给出一致结果；③ 子目录规则文件同样走同一解析函数，`proactive-agent__skillhub/assets/AGENTS.md` 与 `vercel-react-best-practices/AGENTS.md` 因此同步获得该条款，符合「同一规则全仓一份权威正文」的口径；④ 历史提交是这类「能力被回归掉」的唯一可靠线索，规则文件漂移排查应先 `git log -S` 定位实现是否曾经存在。验证：`bash -n` 语法检查 PASS；`python test/project-rule-file-bootstrap-rules/bootstrap_agents_test.py -v` 3 项全通过（含归属仓库双向断言与子目录跳过标记幂等用例），耗时 55.177s；`scan_test_pollution.py --diff-only` 输出 `POLLUTION: PASS`。
- 2026-10-27：**imagegen 模型清单收敛为唯一 gpt-image-2**。用户要求「生图的 skill，把模型限制在 gpt-image-2，删除 gpt-image-2.5-flare、gpt-image-2.5-sunburst」。本轮只改模型名与默认值，不动通道结构。落点：`SKILL.md` description / 模型章节 / CLI 描述 / 配置兜底 / 核心规则、`references/config.example.json` 三处模型字段、`scripts/image_gen.py` 的 `DEFAULT_MODEL`、`scripts/imagegen.py` 的解析兜底与 `SKILL_CONFIG`、`CHANGELOG.md` 2.5.0。关键教训：① 改 skill 默认值不等于改本机生效值——同名的 `IMAGEGEN_MODEL`、`PROJECT_IMAGE_MODEL` 用户级环境变量优先级高于脚本常量，`~/.imagegen/config.json` 又高于环境变量，验证时若不隔离这三层会误判「改动没生效」；② Windows 用户级环境变量只对新建进程生效，当前 shell 仍读旧值，必须用新进程复验；③ 旧模型名在 `.pyc` 缓存里仍有残留，但 `__pycache__` 未被 Git 跟踪，用 `git ls-files` 确认后不必处理；④ `--model` 参数层按用户明确选择保持宽松（只改默认值，不加白名单），此边界须在文档中写清以免误认为已锁死。验证：两个脚本 `py_compile` 通过；示例配置 JSON 解析正常；清除环境变量后在隔离 HOME 下 `_resolve_default_model()` 返回 `gpt-image-2`，再在新进程复验仍为 `gpt-image-2`；`quick_validate.py` 返回 `Skill is valid!`；`POLLUTION: PASS`；字典旧模型计数 0。仓外同步：`~/.imagegen/config.json` 与两个用户级环境变量已按用户确认改为 `gpt-image-2`，配置改前备份 `config.json.bak.20261027`。
- 2026-10-25：**前端视觉改动对比 Demo 规则吸收并全量提交收口（Git 收口）**。用户要求「吸收经验并根据 git 提交 skill 的规则，所有文件提交 git」。本轮业务目标单一：把「改样式/改组件/调 CSS 必须先给新旧对比 demo」沉淀为 skill 规则。落点裁决结论是补进既有 skill 而非新建独立目录——`frontend-design` 已是前端 UI/组件/样式改动的主路径，另两处只留单句引用，避免双权威日后各自漂移。新增 `frontend-design/references/visual-change-demo.md` 为唯一权威细则（触发面与四类免触发面、对比形态四级 `M1`-`M4`、可判定性硬约束、保真五档样式来源、闸门语义、产物纪律）；`frontend-design/SKILL.md` 第 2 步追加 1 行闸门条、`frontend-ui-visual-rules/SKILL.md` 暂停条件追加 1 行引用。关键教训：① demo 必须长在项目自己的样式上（`<link>` 真实构建产物 CSS → `@import` token → 挂项目跑真实组件 → `M3` 截图 → `getComputedStyle` 兜底），手搓近似样式会让「演示通过、落地不符」比不出 demo 更糟；② before 版是校准基准，before 偏了 after 的判断随之失效；③ `quick_validate.py` 在 Windows 默认 GBK 解码读 UTF-8 中文 SKILL.md 会假失败，须 `PYTHONUTF8=1` 重跑同一脚本而非改脚本；④ 字典生成器每次写入新时间戳，`data.js` 与 `字典.md` 的 `generated_at` 必然变化，核对计数应比对 `references_total` 等结构字段而非整文件哈希。验证：两个 skill `quick_validate.py` 均 `Skill is valid!` 退出码 0；三文件 UTF-8 且乱码替换符 0 命中；`references_total` 928→929 与实际新增 1 个 reference 一致；6-review 六维自查 PASS。本仓库根仅 `package.json` 且无 `build` 脚本，编译闸门按规则判 `N/A`。
- 2026-10-22：**索引漂移识别与全量提交收口（Git 收口）**。用户要求「吸收经验并根据 git 提交 skill 的规则，所有文件提交 git」。开工盘点发现索引树等于 2026-10-15 提交 `3a9aa97e`，392 条「已暂存删除」中 365 条与 HEAD 完全一致、其余仅差 CRLF/LF，证实索引被整体回退而非文件删除；用混合 `git reset` 恢复后真实变更从 576 项收敛为 106 项。按业务拆成 8 笔提交：提交索引漂移判据、Markdown 文档规则与 PPTX 种子、生图配置统一、TAPD 路由收敛、任务投影单会话唯一、design 组件库定位、系统 skill 同步、规则记忆与字典收口。关键教训：① 批量假删除必须先查「文件是否还在磁盘 + 内容是否等于 HEAD + write-tree 是否等于历史提交树」，直接提交会吞掉期间的提交；② 恢复只能用混合 reset，`checkout`/`restore`/`rm` 会真的删掉完好文件；③ 外部种子（pptx 的 W3C XSD 与上游脚本）用 `.gitattributes` 的 `-whitespace` 保留原始字节；④ 测试 runner 需把测试文件所在目录加入 `sys.path` 才能导入同目录 fixture；⑤ 文档宣称的组件数必须与守卫实测对齐（本轮 151→152）。验证：git 规则 12 项、任务投影 87 项测试全绿，`POLLUTION: PASS`，每笔提交 pre/post gate 均 PASS；全量 476 项中 6 错 2 失败的存量问题在 HEAD 基线同样存在，本轮新增 2 项失败已归因为既有测试路径缺陷。

- 2026-10-19：**规则吸收与全量提交收口（Git 收口）**。用户要求「吸收经验并根据 git 提交 skill 的规则，所有文件提交 git」。工作树 110 项、451 条文件级改动按业务目标拆成 9 笔提交：组件库与示例守卫体系（355 文件，含 152 组件、运行时守卫脚本、Arco 真相源、需求/Bug/测试/6-review 与截图证据）、生图并发与媒体内联展示、计划可行性探针 `FEAS-*`（L1 只读 / L2 隔离真实）、浏览器路由判据（登录需求不再回退 Chrome Plugin）、测试污染 P4 豁免通道、任务投影单条容错、C 盘清理实测坑、扩展种子（豆包视频创作 / rea）、规则入口与残留自查维度校验。关键教训：① `git diff --cached --check` 会把「行尾多余空格」与「EOF 多空行」当阻断，七处来自历史文档与新增脚本的空白问题需先修再提交；② 字典生成器每次写入 `generated_at` 时间戳，md5 必然变化，确定性校验必须先剥离时间戳；③ 根目录 `.npm-cache` 是 npm run dev 的日志残留，与历史处置一致直接删除而非提交；④ 组件库 `node_modules` / `dist` / `.npm-cache` 由子目录 `.gitignore` 自行排除，实际入库 264 文件、16.3MB，不需要在根 `.gitignore` 重复登记。验证：两套改动测试 87 项全绿（`task_plan_projection_test.py` 87 OK、`scan_test_pollution_test.py` 正负用例通过）、`POLLUTION: PASS`、Python 语法编译 0 错误、每笔提交 pre/post gate 均 PASS。
- 2026-10-18：**组件示例全量遍历排查与事件接线守卫（Goal 收口）**。用户 Goal「继续检查所有组件示例，遍历检查每一个组件和示例，修复 bug」。在既有守卫覆盖的可见性/逐格提示/留白/边角/投影之外，逐组件逐示例遍历 101 页 749 卡，查出 11 个真实缺陷 + 1 个上游冻结面缺陷。最重的是系统性缺陷：示例层 `use-live-props.ts` 只按样本已有键建 `update:<键>` 回写，从未消费组件其余声明事件，导致 341 条可点事件（Alert 关闭、Popconfirm 确认、Form 提交、Typography 复制、Tabs 关闭、Topbar 五入口等）发出后无人接收，按钮点了没反应。修复：新增 `build_demo_events.mjs` 从 `defineEmits` 派生事件表，`use-live-props.ts` 按表给全部声明事件接上节流提示（8 类非手势事件豁免）；变体生成器改深度感知枚举识别（修 `Array<联合>` 误当标量、嵌套联合误取），示例 752→749；修 `TreeSelect` 类型声明、`Comment` 头像裂图、`Image` 放大控件可访问名+空格、`Spin` 浅色遮罩对比度、`CollapseItem` 无父级本地开合、`Typography` 复用 `@/utils/clipboard` 并让复制失败可见；`check_help_tip_interaction.py` 作用域收窄到 `.g-cell-body`（旧版命中卡片头自带图标而常年报红）；删残留 `.npm-cache`。新增 2 条运行时守卫 `check_demo_health.py`（九判据双主题）与 `check_demo_event_wiring.py`（vnode 子树遍历对账），均按 diamond 拆同级模块并内置阳性对照。关键教训：① 弹层组件走 Teleport、收起时整棵子树不渲染，接线判定必须从 `body.__vueParentComponent.subTree` 遍历 vnode 而非扫 DOM，否则 8 个组件 48 处误报缺口；② `el._vei` 在本构建恒空不可用，改读 `el.__vnode.props` 的 `on*` 键；③ 对比度判据必须逐层 alpha 合成到不透明底，跳过半透明祖先会把 Spin 的 1.46 读成 1.07，遇渐变/图片背景要返回 `measurable=false` 跳过（RelationGraph 深盘浅字否则误报）；④ 事件名 `row-click` 对应 `onRowClick`，不归一会全量误报；⑤ GSAP 空目标告警属上游 `motion.ts` 冻结面缺陷，只登记 `KNOWN_CONSOLE_ALLOW` 写明上游修法与移除条件，不在本地打补丁。验证：双主题 `DEMO_HEALTH: PASS`（749 卡九判据零命中）、`EVENT_WIRING: PASS`（341 条全接豁免 43）、两守卫 `SELFTEST: PASS`（阳性对照+扫描根覆盖 20→21）、真实点击取证 7 类反馈文案、剪贴板授权/未授权双上下文对照；其余 15 条守卫全 PASS、`vue-tsc` 0、单测 21/21、`vite build` 6.10s、`POLLUTION: PASS`；Bug/测试/6-review 三份文档机器校验 PASS。6-review 阶段发现两条新守卫超 200 行基准（379/251），已按 diamond 拆分并用 `inspect.getsource` 证明判据字节未改写。改动停在已改动未提交状态。
- 2026-10-18：**组件库文字清晰度修复（需求收口）**。用户反馈「文字字体的像素很低，有些模糊」，并要求看修改前后对比再决定是否实施。诊断出三个根因：① 全屏噪点层以 `fixed + z-index 200` 压在正文之上，开/关噪点层正文区 100% 像素有差异、最大 8 灰阶；② 字体栈前 5 项为 macOS 专属，Windows 上全部空转，165 处字重声明中 96 处非标准档位被静默吸附（400/500/560/620/700 只渲染出 3 种字形）；③ 非整数字号与非整数行高落在半像素栅格。关键教训：只把噪点层 `z-index` 降到 0 无效——0 与 auto 同层，仍按 DOM 顺序画在内容之后，首轮「修改后」截图其实未生效，靠开/关像素对照仍为 100% 才发现；正确做法是给 `#app` 建层叠上下文、噪点层降到 -1、`.stage` 让开背景。交付：`overrides.css` 新增噪点层级、`@font-face` 用 `local()` 解锁 100-900 连续字重轴（不打包 17MB 系统字体）、平台字体栈、受管字号派生块；本地扩展层 17 个文件非整数字号清零；新增 `scripts/build_font_overrides.py`（从冻结源自动派生 82 个选择器的整数化覆盖块，含 `--check` 同步守卫）并登记进 SKILL.md 与 LOCAL-GUIDE.md。验证：噪点层开/关正文逐字节相同（自噪声对照 0%）；五档字重五种字形且宽度 300.45→305.66 单调递增；非整数字号 9.13%→0.46%；`FIDELITY`/`FONT_OVERRIDES`/`DEMO_VISIBILITY(752)`/`DEMO_GUIDES(752)`/`POLLUTION` 全 PASS；`vue-tsc` 0、单测 21/21、`vite build` 4.13s；四份文档机器校验 PASS；`FONT_OVERRIDES` 阳性对照篡改后退 1、还原后退 0。改动停在已改动未提交状态。
- 2026-10-18：**组件示例文字提示与逐格说明（需求收口）**。用户提出「文字提示 / 悬停文字说明与图标式帮助；我们希望所有组件都加一个文字提示的组件提示说明」，并补充「每一个组件示例的提示一个都是对应这次示例的说明」。侦察确认：`references/component-catalog.json` 已有 135/152 条说明，但 17 条为空且全部位于 139 个上游冻结文件（`ui/`、`layout/`、`Icon.vue`，源码无头部注释不可改），该索引又在 `src` 编译范围外不能直接 import。交付：新增 `src/data/component-guides.ts`（152 条中文说明，单一数据源）；新增 `views/gallery/demo-guides.ts` 按该格 props 覆盖项拼出「组件说明 + 本格示例」；`entries.ts` 新增 `diff` 字段透出本格覆盖项；`DemoCell.vue` 卡头挂既有 `HelpTip`；新增守卫 `check_demo_guides.py` 并登记进两份指南。关键决策：说明放 `src/data/` 而非跨目录读 `references/`；17 条冻结面说明写入数据源而不改源码；每格差异按覆盖项推导，不逐格手写 752 句；复用 `HelpTip` 不另造组件。验证：`DEMO_GUIDES: PASS`（101 页 752 卡，四类缺口均为 0）；两条阳性对照分别精确报出「非基础示例却写默认形态」与「缺少提示图标」；真实鼠标悬停三格文案各不相同；其余守卫全 PASS、`vue-tsc` 0、单测 21/21、`vite build` 4.50s；需求与 6-review 机器校验 PASS。改动停在已改动未提交状态。
- 2026-10-18：**组件示例卡不可见与出卡修复、示例可见性守卫（Goal 收口）**。用户截图圈出 `/gallery/navigation/locate` 的四个 `BackTop` 示例卡全部空白，要求检查所有组件并完善。全量体检 101 页 / 750 张示例卡后命中 6 处：4 处 `BackTop` 出卡（按钮按 `position: fixed` 参照视口，飘到浏览器右下角）、1 处 `TabPane` 空白（`active: false` 由 `v-show` 隐藏整块）、1 处纵向 `Divider` 塌缩（靠 `align-self: stretch` 撑高，单独挂载只剩 1em 的 13px 短线）。修复：`BackTop.vue` 新增 `container` 属性与根锚点 `div.x-backtop-anchor`（`absolute; inset: 0`），父元素自动补 `relative`，`hostReady` 驱动 `anchorStyle` 改为 computed；示例层新增 `DemoFrame` 并排外框（`entries.ts` 透传、`Gallery.vue` 渲染、指纹纳入 `frame`），纵向 `Divider` 由三组带外框的策展示例接管并剔除生成器派生项；`TabPane` 移除空白示例、补三组可见差异。新增长期守卫 `check_demo_visibility.py` 并登记进 `SKILL.md` 与 `LOCAL-GUIDE.md`。关键教训：出卡判据遍历内容区全部元素时，`inset: 0` 的定位包装层会盖住真正飘出去的浮层，首版阳性对照因此仍报 PASS；改为排除「恰好铺满内容区的定位包装层」后，阳性对照精确报出 4 处 `BackTop all-outside`。验证：`DEMO_VISIBILITY: PASS`（101 页 752 卡）、`CONTENT_PADDING`/`CORNER_OCCLUSION`/`FIDELITY`/`POLLUTION`/`CATEGORIES`/`DEMO_VARIANTS(752)`/`CATALOG(152)` 全 PASS、`vue-tsc` 0、单测 21/21；三视口竖线均 1×72、无溢出；Bug 与 6-review 机器校验 PASS。改动停在已改动未提交状态。
- 2026-10-18：**菜单选项文字贴边修复与内容留白守卫判据升级（Bug 收口）**。用户三张截图指出菜单选项「文字末尾和整个选项的边缘太靠近了，几乎一键贴边」，要求修复并检查全部组件。根因是 `MenuNode.vue` 的 `.x-menu-item` 左内边距由行内缩进按层级给出，样式块从未声明 `padding-right`：纵向模式按钮撑满容器掩盖了遗漏，横向模式按钮收窄到内容宽度后文字末尾直接落到选中底色块右边缘（实测 `padding: 10px / 0px`、`padR=0`）。修复为补 `padding-right: 10px`，与 `TreeNode.vue`、`TreeSelect.vue` 既有写法同值。守卫 `check_content_padding.py` 判据升级：旧版整体豁免交互控件导致该类缺陷完全扫不到，改为纳入 `button` / `menuitem` / `option` / `tab`；判据只取左右两向、阈值 4px，并新增三类语义豁免（无可见边界的纯文字按钮与布局 div、圆形容器、自身可滚动容器）。验证：`CONTENT_PADDING: PASS`（750 张卡）；阳性对照移除 `padding-right` 后精确报出 1 处 `x-menu-item.is-active > SPAN.x-menu-label`（`r:0`），恢复后 PASS；`FIDELITY`、`POLLUTION`、`CATEGORIES`、`DEMO_VARIANTS`、`CATALOG` 全 PASS，`vue-tsc` 0、单测 21/21；横向选项 `padR` 由 0 变为 10，浮层子项 49/53。判据校准过程：纳入控件后底部方向误报小控件、纯文字按钮假阳性 60 余处、圆形头像误报，逐项收敛后为 0。改动停在已改动未提交状态。
- 2026-10-17：**Panel 内容贴边修复与内容留白守卫（Bug 收口）**。用户截图指出 `/gallery/layout/container` 的面板正文文字贴到边框外沿，要求修复并检查全部组件。根因是上游 `Panel.vue` 把 `<slot />` 直接挂在根 `<section>` 下，从未使用 `components.css` 已定义的 `.panel-body` 包裹层，`.panel-body { padding: 0 20px 20px }` 成了死样式，正文左右与底部实测留白均为 0。因 `Panel.vue` 在 139 文件冻结面内，修复落在本地覆盖层 `src/styles/overrides.css`：对 `.panel > :not(.panel-head)` 补左右 20px、首末子元素补上下 20px。新增守卫 `frontend-design/scripts/check_content_padding.py`，路由从分类真相源派生 101 个示例页，用 Range 取文本字形矩形与容器边框内沿比对，左右或底部贴边即 FAIL。验证：`CONTENT_PADDING: PASS`（750 张卡）；阳性对照移除覆盖层规则后精确报出 4 处 `panel > P` 贴边，恢复后 PASS；`FIDELITY`、`POLLUTION`、`SHADOW_CLIP`、`CORNER_OCCLUSION`、`CATEGORIES`、`DEMO_VARIANTS`、`CATALOG` 全 PASS，`vue-tsc` 0、单测 21/21。判据踩坑：首版路由写死二级路径扫到 0 张卡仍报 PASS；把 `.workspace` 写进排除面使阳性对照整页失效；取四边最小值会让顶部对齐掩盖左右贴边。改动停在已改动未提交状态。
- 2026-10-17：**组件库双击启动脚本（收口）**。用户要求「组件库写一个 bat 的启动脚本，我们可以点击启动」。新增 `frontend-design/component-library/启动组件库.bat`：切到自身目录、检查 Node（缺失时打印安装地址并 `pause`）、依赖缺失才 `npm install`、随后 `npm run dev`，异常退出保留窗口。关键坑一：cmd.exe 按字节偏移逐行读批处理，在文件内 `chcp 65001` 切代码页后，含中文的行会被从中间截断并当作命令执行，实测报 `'口，端口随进程退出释放。' is not recognized`——解法是 bat 保持纯 ASCII，中文提示移入 `scripts/launch-message.mjs` 由 Node 输出（六种提示：welcome/prepare/start/exit/no-node/install-failed）。关键坑二：给 `README.md` 加说明后 `FIDELITY: FAIL (drifted=1)`，因它属 139 个上游冻结文件，改动只能写进 `LOCAL-GUIDE.md`。关键坑三：根目录 `.gitattributes` 的 `*.bat eol=crlf` 不生效，组件库自带 `* text=auto eol=lf` 会覆盖子目录属性，CRLF 例外必须写进组件库那一份。验证：真实运行 `HTTP=200`、Playwright 打开 `/login` 标题「登录 · 通用后台管理系统」、结束进程后 `HTTP=000` 且 5173 无监听、最小 PATH 模拟无 Node 退出码 1、`FIDELITY: PASS`（261 本地 / 139 上游）+2 SEAM、`POLLUTION: PASS`、`INVENTORY: PASS`、`CATALOG: PASS(152)`、`vue-tsc` 0、6-review 文档机器校验 PASS。改动停在未提交状态。
- 2026-10-17：**图标式气泡帮助组件 HelpTip（需求收口）**。用户指出组件库缺少「有一个图标，鼠标移上去就弹出悬浮说明功能/字段/业务」的形态并附问号与信息圆环截图。侦察确认：`extend/Tooltip.vue` 只有纯文字气泡、触发区由调用方提供；`ui/HoverCard.vue` 是富内容名片；`ui/IconButton.vue` 只有浏览器原生 `title`；图标表只有 `info` 没有问号。故在本地扩展层新增 `extend/HelpTip.vue`：图标按钮 + 悬停/聚焦浮层，`Teleport` 到 `body` 并 `position: fixed` 以避开示例卡滚动容器裁切，定位按触发区与浮层实测尺寸计算、超出视口自动翻面并夹边 8px，动效复用 `overlayEnter/overlayLeave`、材质复用 `.m-float`、层级复用 `floatingLayerFor`。关键取舍：`src/data/icons.ts` 与七层样式都在 139 文件冻结面内，问号图标只能内联进组件、橙色令牌不得新增，故 help 态用 `--ink-muted`、info 态用 `--blue`；落 `extend/` 而非全冻结的 `ui/`；归入既有 `display/tooltip` 而非新开子分组。过程中修掉三处自身问题：首版 213 行超 200 行基线（按同目录单行函数注释收敛到 193 行）、点击区固定 24px 会让 `size=44` 图标溢出（改为 `max(24, size + 9)`）、指针移出后仍聚焦按钮上的说明被错误收起（本地标记与 DOM 真实焦点长期不一致，改为直接比对 `document.activeElement`，`dismiss()` 先 `blur()`）。验证：新增交互守卫 `scripts/check_help_tip_interaction.py`（161 行）沿 `offsetParent` 祖先链检查裁剪容器，输出 `HELP_TIP: PASS`（悬停/聚焦/Esc/焦点保持/指针穿透/视口夹取/ARIA 关联/长文 260px 上限）；`CATEGORIES(152)`、`DEMO_VARIANTS(750 组, 4.93)`、`ADMIN_COVERAGE(152/152)`、`CATALOG(152)`、`INVENTORY/PARITY/COMPONENT_PARITY/SHADOW_CLIP/CORNER_OCCLUSION/FIDELITY/POLLUTION` 全 PASS；`vue-tsc` 退出码 0、单测 21/21、`vite build` 4.18s；需求、测试、6-review 三份文档机器校验均 PASS。改动停在未提交状态。
- 2026-10-17：**组件边角方角缺口修复与边角一致性守卫（Goal 收口）**。用户截图指出「组件的边角会多出来一点和组件风格不一致的透明边角」，要求修复并全量排查。根因不是透明度：应用外壳有 10px 深色描边与 38px 圆角，导航轨 `.rail` 作为直角子元素带半透明玻璃底、从内边距左上角铺满，把圆角内侧的描边盖掉，角部露出浅色方角；`overflow: clip` 只裁外接矩形不裁圆角弧，对子元素无效。逐行取色证实 y=304–307 四行完全无深色描边，两次截图一致。修复写在本地覆盖层 `overrides.css`：≥821px 时给 `.app-frame > .rail` 补 28px 左上/左下内弧圆角（28 = 外弧 38 − 描边 10），修复后同四行恢复为 397/396/395/395，2 倍密度 45 度剖面连续。新增运行时守卫 `scripts/check_corner_occlusion.py`，两条判据（粗描边内弧被直角子元素盖住 / 有背景圆角父级下方角子元素外露，父级 `overflow: hidden/clip` 时跳过），全量 112 个菜单页 PASS；两条阳性对照均真实转 FAIL。过程中废弃了两版静态源码守卫（解析不到 `.m-rail` 组合类），并修正 `overflow` 裁剪与 1px 顶线两处误报。验证：`CORNER_OCCLUSION`/`CATEGORIES`/`DEMO_VARIANTS`/`ADMIN_COVERAGE`/`SHADOW_CLIP`/`FIDELITY`/`POLLUTION` 全 PASS、`vue-tsc` 零报错、单测 21/21、`vite build` 4.14s；Bug 主文档与 6-review 机器校验均 `valid: true / PASS`。改动停在未提交状态。
- 2026-10-17：**组件菜单单一概念拆分、示例页三列大卡与示例扩容（Goal 收口）**。用户要求菜单不要「xx与xx」并列（点名「标识与头像」拆成两个菜单）、组件像素更高、示例更多、卡片更大、一行 3 格。重写 `component-categories.{basic,data,extended}.ts` 为 10 父分类 / 101 单一概念子分组；`Gallery.vue` 栅格改固定 3 列（断点 1360/820，按「三列每卡不低于 300px」反推，实测 1320px 三列仅 297px 比两列更小）、画布最小高 200；`DemoCell.vue` 字号与内容区上限上调；`entries.ts` 画布默认 160→240；派生器补反向布尔与三档数值、弹层专属宽度档；策展补真实差异并修复 `curated-inputs.ts` 重复对象键（后段静默覆盖前段）与 `SpecPlate`/`MenuStarMap` 同值变体。示例 579→738 组、平均 3.83→4.89。曾试在冻结的 `src/router/index.ts` 加旧地址重定向，`FIDELITY` 立刻报 `DRIFTED`，已完整撤回（缝隙只允许新增声明行后逐字节相等）。验证：`CATEGORIES/DEMO_VARIANTS/ADMIN_COVERAGE/CATALOG/SHADOW_CLIP/FIDELITY/POLLUTION` 全 PASS、`vue-tsc` 零报错、单测 21/21、`vite build` 成功；浏览器实测 1920/1440/1360 三列 497/337/310px，1359/1180 两列 474/397px，8 页抽样渲染异常 0、空页 0。改动停在未提交状态。
- 2026-10-17：**组件示例边角阴影块修复与投影留白守卫（用户 Goal 收口）**。用户报「为什么有一些边角阴影块，组件细节没做好」并附截图。根因是柔影延展量超过容器留白后被 `overflow: clip` 的裁切边（落在 padding 外沿）硬切成方形暗块，共三个落点：外壳 `.app-frame` 带 `0 24px 70px` 大外阴影（四向需 11/35/59/35）而上游 `.stage` 只留 8px；示例卡内容区 `.g-cell-body` 无留白承接卡内组件柔影（需 5/25/47/25）；登录页 `.login-canvas` 同量级外阴影而上游 `.login` 只留 14px。上游七层样式与 `main.ts` 属 139 文件逐字节冻结面，修复只能走受控通道：新增本地覆盖层 `src/styles/overrides.css`（留白 14/36/62/36 与登录同值，只在 `min-width: 821px / 961px` 生效以保持窄屏上游贴边形态）+ `main.ts` 追加一行引入并登记进 `fidelity_upstream.py` 的 `SANCTIONED_SEAMS`（剥离声明行后仍须逐字节等于上游）；`.g-cell-body` 取 `26/26/48/26` 并把 `max-height` 由 420 抬到 494 以保持内容可视高度不变；留白变化必须同步修正由旧值写死的 `.app-frame` 高度与 `.login-canvas` 最小高度公式。新增静态守卫 `scripts/check_shadow_clipping.mjs` + `scripts/shadow_clip_measure.mjs`（裁决入口 102 行 / 测量模块 170 行），判据当场从源码解析全部非内阴影层四向延展并与三落点留白逐维比较，阳性对照要求留白清零后 3 落点 × 4 方向共 12 条全部报缺。取证教训三条：① 首版判据取「每层四向最小值」，20px 留白对着 47px 投影照样 PASS，属空判定；② 亮度聚类像素判据把中文字形与主色按钮误读成暗块，像素统计不能当缺陷判据；③ iframe 扫描漏注入登录态会把 `cells: 0` 误读成通过，跨 realm 不能直接调父窗口函数。磁盘级变异自证：下方留白改 10px 立即 `FAIL` 点名 `.stage.bottom 需 59px 只有 10px`，按字节还原后校验和一致、复跑 `PASS`。真实浏览器 39 页 579 格全量复核（空页 0）：卡片/外壳/登录三级容器裁切 0、页面无横向溢出；探针早期报的 `shell/frame` 与 Segmented 滑块 6 处经「最近裁切祖先」定位证实为口径错误（AppShell 示例自带内层 `.stage` 已覆盖、Segmented 滑块包含块不裁切）。滚动条 A/B 单变量对照显示净增 3 横 1 竖，换来卡内柔影零裁切。组件自有圆角/滚动容器（`x-card` 圆角 `--r-lg`、`x-image` 圆角 `--r-sm`、`x-tabs` 横向滚动、热力格、关系图画布）裁切内部 0.04–0.05 极淡投影属既定造型，与被报的深色方块不同类，逐条登记为未覆盖说明。验证：`SHADOW_CLIP/FIDELITY(+SEAM)/GUARD_SELFTEST/INVENTORY/PARITY/CATALOG/CATEGORIES/DEMO_VARIANTS/ADMIN_COVERAGE/POLLUTION: PASS`、`vue-tsc` 退出码 0、单测 21/21、`vite build` 成功；Bug 主文档 `doc/4-bugs/2026-10-17_084300_组件示例边角阴影块.md` 与 `doc/6-review/2026-10-17_093600_组件示例边角阴影块修复_6-review.md` 均机器校验 PASS。工作树未提交（无当轮 Git 授权）。
- 2026-10-17：**组件库菜单二级化 + 一组件多示例可用性收口（用户 Goal 收口）**。把组件库导航从 10 个一级分类细化为「父分类 → 子组件分类」两级共 39 个可点示例页；151 个组件补齐到 579 组示例（平均 3.83 组），并用浏览器逐格渲染签名加输入值扫描清除「属性写了不同值但渲染完全一样」的伪变体（Form 插槽硬编码空值、Countdown 停表未给剩余量、Swimlane 样本不足两条泳道、DataTable 无选中项时改 rowKey、StyledScrollbar 双轴受溢出门控、Rate allowClear 属行为差异）。示例卡片由裁切改为限高滚动，39 页在五档宽度 195 组测量的裁切与横向溢出全为 0。修复 `extend/TreeSelect.vue` 的真实缺陷：收起态下选中二级节点时触发区退化为占位符，原因是按可见行列表查节点而该列表剔除折叠子行，改为在完整数据树递归查找。后台根地址默认落到组件库第一个示例页。详见 `doc/5-tests/2026-10-17_044000_REQ-PEARL-ADMIN-GALLERY-001_组件菜单二级化与示例可用性_测试主文档.md`。
- 2026-10-16：**组件库后台化收口（用户 Goal）**。151 个组件全部在管理后台可达并提供可操作示例，独立 showcase 入口可逆退役，新增覆盖率守卫四模块与本地页面登记处，上游登记表开出 2 行声明式缝隙。
- 2026-10-15：**Arco 组件粒度对齐补齐 21 个组件，组件总数 126 → 147（用户 Goal 收口）**。延续上一条 Goal，把对齐口径从「品类目录」下沉到「组件粒度」——上一条只对平 74 个品类目录，但 Arco 实际对外导出 131 个组件名，只对目录会把 `RangePicker`/`InputSearch`/`CheckboxGroup`/`CardMeta` 这类子组件整体漏掉，属「看着齐全、实则遗漏」。做法：① 从同一份 `npm pack @arco-design/web-vue@2.58.0` 的 `es/index.js` 导出清单派生 `references/arco-components.json`（131 条 = 74 顶层 + 57 子组件）与 `references/arco-component-parity.json`（逐条标 `kind`: covered / merged / gap）；② 新增 `scripts/check_arco_component_parity.py` 五重校验——`COVERAGE_GAP` 未清零 / `STALE_GAP` 标 gap 却已实现 / `DANGLING` 标 covered 但文件缺失 / `PHANTOM_COMPONENT` 登记了 Arco 没有的 / `MISSING_COMPONENT` Arco 有但漏登，前两者用于推进、后三者防止清单自己长歪；③ `src/components/extend/` 新增 21 个文件——日期族 5、浮层预览族 5、输入容器族 5、卡片树族 5，外加递归单元 `TreeNode`（非 Arco 导出，随 `Tree` 落地），extend 层累计 78 个。语义纠错：上轮按「`SubMenu` 缺口」建成的文件实为悬停下拉面板，而 Arco 的 `SubMenu` 是 Menu 的行内子项、已被 `MenuNode.children` 递归覆盖（标 merged 正确），真正缺口是 `Dsubmenu`；核对 `Menu.vue`/`MenuNode.vue` 确认递归存在且全仓无引用后改名 `DropdownSubmenu.vue` 并登记到 `Dsubmenu`，避免一个错名文件同时污染两个语义。核对页适配：`ImagePreview`/`ImagePreviewGroup` 受控键是 `visible` 而非 `open`，`Showcase.vue` 弹层识别与 `bindOf()` 扩展为同时认两种受控键（`visible` 走 `update:visible` 回写）；新增 21 组 demo 样本，含 `TREE_DATA`（`label` 契约，与 `TreeSelect` 的 `title` 契约不同不能互相顶替）。验证：核对页浏览器实测 147/147 全部「已挂载」、0 空白卡片、0 渲染异常（`NeuralNet` canvas / `Mention` textarea / `Skeleton` 骨架三张无文本卡片经 DOM 核查属预期）；`COMPONENT_PARITY: PASS (131 全覆盖; covered:98 merged:33)`、`PARITY: PASS (74)`、`INVENTORY: PASS (123)`、`FIDELITY: PASS (239 本地/139 上游)`、`GUARD_SELFTEST: PASS`、`CATALOG: PASS (147)`、`POLLUTION: PASS`、单测 21/21、`vue-tsc + vite build` 成功。临时产物（`.xverify-*.mjs`、`/tmp/arcoaudit`）已清理；工作树未提交（无当轮 Git 授权）。

## 交接档案（自 PROJECT_CURRENT 迁入）

> 由 `context-recovery-rules/scripts/archive_project_current.py` 自动迁入，新条目置顶、只保留最近 20 条。当前交接点仍以 `PROJECT_CURRENT.md` 为准。

### 2026-10-31 形变升级全部执行完成（同日第十五笔，未提交）

- 当前状态: 计划里的四个批次已按序执行完毕，**6 个组件落地形变**，4 处按理由跳过。双主题健康、动效语言、冻结面、示例契约全 PASS。工作树未提交。
- 本轮目标: 用户「继续执行，把所有形变的升级计划都按照顺序完成」。
- 落地清单（全部逐帧实测）:
  | 组件 | 语式 | 实测 |
  |---|---|---|
  | `Radio` | 落定 + 生长 | 环 `1→0.89→1`，点 `0→0.26→0.86→1.09→1` |
  | `Rate` | 落定 | 被点的星 `0.96→0.86→0.98→1.01→1` |
  | `Steps` | 描线 | 勾常驻，`dashoffset 20→3.1→-1.9→0`，数字 `opacity 1→0` |
  | `InputTag` | 收拢 | 宽度 `87→85→72→22→移除`，标签数 9→8 |
  | `Tree` | 展开 | 子行 `opacity 0→0.35→0.83→1`，`translateY -5→0`，26ms 错位 |
  | `Progress`（上一笔） | 收拢+描线 | 条收拢成圆 → 描环 → 画勾 → 回弹 |
- 跳过 4 处（写进计划文档，附理由）:
  - `Checkbox`：`settlePop` 挂在常驻包裹 span 上，本来就正常。
  - `Segmented` / `Tabs`：已有滑块 `x + width` 位移，再叠按压是噪声。
  - `Upload`：进度条 `v-if="uploading"`，状态一变整条卸载，没有收拢余地，要做得先重构列表行。
  - `Alert` / `Notification`：图标由 `showIcon` 驱动、挂载即存在，加入场动效会让一屏提示条同时晃。
  - `Dropdown` / `Popover` / `Drawer`：入场编排在冻结的 `motion.ts` 的 `overlayEnter` 里。
- 新增能力: `morph.ts` 增 `collapseOut`（宽度+内边距收到 0，退场用 `EASE.exit`）。这是少数**允许动宽高**的地方——收拢本来就是宽度变没，用 `scaleX` 会把文字压扁，比动宽高更假。
- 两个实现坑（都已记入 LOCAL-GUIDE / 记忆）:
  1. **`watch` 默认在渲染前触发**，对 `v-if` 元素做进场动效必然拿到 null。`Radio` 原来的 `settlePop(dot.value)` 就是这样静默失效的，实测圆点 scale 恒为 1，注释里的「落定弹入」从未生效。
  2. **GSAP 与 CSS `transition: transform` 打架**：GSAP 每帧写 inline 值会被过渡再插值一次，动作变软。`morph.ts` 在动效期间临时置 `transition: none`，结束恢复。
- 验证: `vue-tsc rc=0`；`DEMO_HEALTH` 双主题 101 页 763 卡零命中；`MOTION_LANGUAGE: PASS`；`FIDELITY: PASS (274 local)`；`DEMO_VARIANTS: PASS (763 组)`。
- 交接点: 无阻断。若要把跳过项做掉：`Upload` 需重构列表行让进度条常驻；`Dropdown`/`Popover` 需给 `overlayEnter` 开缝隙或改为本地实现。

### 2026-10-31 形变升级批次 1：Radio / Rate 落定（同日第十四笔，未提交）

- 当前状态: 批次 1 落地 `morph.ts` + 改 `Radio`、`Rate`；顺带修掉 Radio 一处**从未生效的死代码**。双主题健康、动效语言、冻结面全 PASS。工作树未提交。
- 交付:
  1. `src/composables/morph.ts`（新增）：形变语式落点，三个原语 `growIn`（0→1 长出，带过冲）、`pressSettle`（1→0.88→1 按压）、`morphSelect`（环按压 + 点生长，60ms 错位）。与 `motion.ts` 分工：那边管曲线，这边管几何动作。
  2. `extend/Radio.vue`：选中改为 `morphSelect(box, dot)`。外环按压 + 圆点从 0 长出。
  3. `extend/Rate.vue`：点击时被点的星 `pressSettle(el, 0.86)`，从「整排一起变色」变成「按下的那颗有反馈」。
- 修掉的死代码（本轮最有价值的发现）:
  `Radio` 原本是 `watch(checked, () => settlePop(dot.value))`，但 `dot` 是 `v-if="checked"`，而 `watch` 默认**在渲染前触发**——那一刻 `dot` 还是 `null`，`settlePop(null)` 静默返回。**实测真组件圆点 scale 恒为 1**，源码注释写的「勾上时一次落定弹入」从未生效过。修法：`await nextTick()` 再取元素。
- 实测（逐帧）:
  - `Radio` 圆点 `0 → 0.26 → 0.86 → 1.09 → 1`；外环 `0.97 → 0.89 → 0.99 → 1.01 → 1`。
  - `Rate` 星标 `0.96 → 0.86 → 0.98 → 1.01 → 1`。
- 计划内的两处跳过（有理由，不是漏做）:
  - `Checkbox`：它的 `settlePop` 挂在**常驻包裹 span** 上，本来就正常，不需要改。
  - `Segmented` / `Tabs`：已有滑块 `x + width` 位移，再叠按压属于噪声。
- 一个必须记住的实现细节: `morph.ts` 会在动效期间**临时关掉元素自身的 `transition: transform`**。GSAP 每帧写 inline 值会被 CSS 再插值一次，不关的话动作变软变慢（`Rate` 星标正是这种情况）。
- 验证: `vue-tsc rc=0`；`DEMO_HEALTH` 双主题 101 页 763 卡零命中；`MOTION_LANGUAGE: PASS`；`FIDELITY: PASS (274 local)`。
- 交接点: 无阻断。下一步：批次 2 描线（`Steps` / `Upload` / `Alert`），前置动作是把 `v-if` 图标改常驻 + `dashoffset` 控显隐。

### 2026-10-31 形变语言全量升级计划（同日第十三笔，未提交）

- 当前状态: 计划已成文 `frontend-design/references/morph-upgrade-plan.md`；未实施。本轮不写代码，只出方案与可行性数据。
- 本轮目标: 用户「全部设计一下形变，给出新的升级计划」。
- 盘点数据（全库扫描，非估计）:
  | 指标 | 数量 |
  |---|---|
  | 组件总数 | 154 |
  | 有状态规则 | 46 |
  | 状态里出现几何属性 | 42 |
  | 用 `<Icon v-if>`（描线障碍） | 26 |
  | 可写层 / 冻结层 | 95 / 59 |
  | 42 个候选里落在可写层的 | **42（全部）** |
- 计划要点:
  1. **四类形变语式**：收拢 Collapse（宽高→圆/0）、描线 Draw（`stroke-dashoffset`）、落定 Settle（`scale` 过冲）、展开 Unfold（0↔1）。三拍组合即 `playCrystallize`。
  2. **三步适配判定**：状态是否改形状 → 两态元素是否都在 DOM → 是否可写层。
  3. **四个批次**：①落定（Radio/Rate/Segmented/Tabs/Checkbox，零 DOM 改动）②描线（Steps/Upload/Alert，需把 `v-if` 图标改常驻）③收拢（Upload 完成、InputTag 删除）④展开（Tree 子节点 stagger、Dropdown/Popover 从触发点展开）。
  4. **明确不做**：`Tag` 关闭（组件本身没有关闭按钮也没有 `Transition`，做形变要改调用方用法）、约 112 个纯换色组件、图形类（会干扰读图）。
- 关键结论: 形变改造**不受冻结面限制**（42 个候选全在可写层），真正的瓶颈是 26 个组件的 `v-if` 让描线没有起点。
- 验证: 本笔无代码改动；`ARCHIVE: PASS`。
- 交接点: 无阻断。建议从批次 1 开始——纯 `transform`、零 DOM 改动，先把三拍语式固化成 `morph.ts` 再动 DOM。

### 2026-10-31 形变语言开篇：Progress 完成态三拍形变（同日第十二笔，未提交）

- 当前状态: `Progress`（line 型 + 100% + success）从「染绿」改为**收拢成圆 → 描环 → 画勾 → 回弹**；新增 2 格示例；双主题健康、动效语言、冻结面全 PASS。工作树未提交。
- 本轮起因: 用户指出「登录的动效是按钮由一个形状变成另一个形状，而不是底色的变化」。**这个批评成立**——前面十几轮做的是缓动语言（颜色/位置变化的曲线），不是形变语言（形状本身改变）。
- 关键区分（已写进 LOCAL-GUIDE）:
  | | 缓动 | 形变 |
  |---|---|---|
  | 变什么 | 颜色 / 位置 | 形状本身 |
  | 载体 | `timing-function` | 宽高、圆角、`scale`、`stroke-dashoffset` |
  | 观感 | 变顺，不细看看不出 | 一眼看到「变形了」 |
- 交付:
  1. `extend/Progress.vue`：成功态不再染绿，改为渲染 34px 徽标，进场时复用 `playCrystallize` 播三拍。
  2. 触发条件收紧：`type='line' && status='success' && percent >= 100`。单给 status 不给 percent 不变形——「62% 打对勾」语义矛盾。
  3. 示例：`CURATED_DISPLAY.Progress` 加「走完落定」「失败态」两格，并保留 `status=success`（62%）做反例。
- 逐帧实测（状态翻转触发）: 宽度 258 → 164 → **34**（0.42s）；圆环 `dashoffset` 126 → 14 → 0；对勾 24 → **-1（back 过冲）** → 0；1.4s 内全部落定，控制台零错误。
- 形变可行性盘点（为「所有组件都试形变」做准备）: 全库扫描状态规则里的几何属性，只有 **19 条规则**涉及 `width/height/border-radius/transform/translate/rotate`，集中在 Card、Carousel 圆点、Collapse/MenuNode/Tree 箭头、Rate 星标、Steps、Anchor、开关滑块、组织节点、矩阵勾选、色板、关系图节点。**其余组件状态只换色，加形变等于重新设计状态表达，不是补过渡。**
- 两个硬门槛（决定「能不能做形变」）:
  1. **两态都要在 DOM 里**。复选框的勾是 `<Icon v-if>`，未选中时 SVG 不在，描线没有起点——要做得先让图标常驻 + `dashoffset` 控显隐，需改 DOM，而 `ui/` 冻结。
  2. **几何得真的在变**。只换色的状态谈不上形变。
- 验证: `DEMO_HEALTH` 双主题 101 页 763 卡零命中；`MOTION_LANGUAGE: PASS`；`FIDELITY: PASS`；`vue-tsc rc=0`；`DEMO_VARIANTS: PASS (763 组)`。
- 交接点: 无阻断。下一步：按 19 条几何状态清单逐个评估——先挑「两态都在 DOM 且几何真在变」的（Tree 箭头、MenuNode 箭头、Carousel 圆点、开关轨道填充已具备），冻结面的先用覆盖层或缝隙解决 DOM 限制。

### 2026-10-31 动效语言第三阶段：图形类先做两个（同日第十一笔，未提交）

- 当前状态: 图形类补建先做 2 处验证方向；`--audit` 修掉重复计数；补建总数 24 → 26。双主题健康守卫零命中、冻结面 PASS。工作树未提交。
- 本轮起因: 用户「接着做图形类那批，先挑 2 个做出来给你看效果」。
- 做了什么:
  1. **关系图节点** `.rg-node .rg-body`：悬停时描边与投影加强，之前是一下跳出来。实测 `transitionDuration 0.18s | border-color, box-shadow`。
  2. **权限矩阵行** `.mx-row .mx-label`：悬停时行底色浮起。慢放 10 倍取到中间帧插值色（`rgb(251,252,252)` → `oklab(…)` → `color(srgb 0.941 0.959 0.982)`），证明是渐变而不是跳变。
- 两个判断修正（都推翻了我上一轮的说法）:
  1. **图形类里没有「交互硬跳」的存量**。上一轮说「图形类占一半」是松判据的产物：`.heat-cell` 与 `.org-node` 本来就有 `transition`（只是缓动是默认 `ease`，属于重定时范畴，第一轮已处理）；`.heat-cell::after` / `.org-node.is-root` 等是变体类，挂载即确定，补过渡只会在首屏闪一下。
  2. **`--audit` 之前重复计数**：没排除已补的 24 条，报 55；修掉后真实待评估是 **34**，其中约一半是已带基础类过渡的 `.btn-*` / `.icon-btn` / `.pill-btn`（不能再补，shorthand 会整条重置）。
- 机制新增: `EXTRA_RULES`（图形类按「元素 + 属性」写死一条规则，不走选择器匹配）。理由：图形类的基选择器带变体类（`.rg-node.is-item`），按选择器匹配会漏，且每个变体要单列。
- 图形类要避开的两类: ① 渐变驱动（`.bar-col` 改的是 `background: linear-gradient`，`background-color` 过渡不了）；② 变体类（`.is-risky` / `.is-root`，不是状态）。
- 验证: `MOTION_OVERRIDES: PASS (53 重定时 + 26 补建)`；`DEMO_HEALTH` 双主题 101 页 762 卡零命中；`FIDELITY: PASS (273 local / 139 upstream)`。
- 交接点: 无阻断。下一步：按 `--audit` 的 34 条逐条过——先剔掉 `.btn-*` / `.icon-btn` / `.pill-btn` 这批「已继承」的，剩下的再判断值不值得补。

### 2026-10-31 动效语言第二阶段：补建（原无过渡的地方）（同日第十笔，未提交）

- 当前状态: 检出「状态会变但从未有 transition」的硬跳 97 处，已补 10 处，剩 68 个选择器待评估；生成器新增补建段与 `--audit` 审计；双主题健康守卫零命中。工作树未提交。
- 本轮起因: 用户指出「很多组件没有这个动效语言，为什么不改」。核对后确认这是**两件不同的事**：上一轮做的是「重定时」（把已有过渡的默认 `ease` 换成令牌，53 条规则 / 96 段），**没有做「补建」**（给从来没有过渡的地方新增声明）。154 个组件里 106 个 scoped 样式一条 `transition` 都没有。
- 判据（运行时可测，不靠肉眼）: 某条状态规则（`:hover` / `.is-*`）声明了可视属性，而元素 `transition-duration` 全为 0s → 硬跳。全量扫描 101 页得到 **78 个选择器**（去画廊自身外壳）。
- 本轮交付:
  1. `motion_language.py` 新增 `split_selectors` / `visual_props` / `transition_for`；可视属性表补 `translate` / `rotate` / `scale`（开关滑块用的是独立 `translate`，不算 `transform`）。
  2. `build_motion_overrides.py` 新增补建段与 `--audit`；生成受「自动审计 + 人工确认名单 `CURATED_BASES`」双重约束，属性仍机械读取。
  3. 已补 **24 处**：复选框（方块 border/background/shadow）、开关（滑块 translate 0.22s 对称曲线）、树折叠箭头、输入框清除、输入壳聚焦、表头可排序、表格行操作格、看板菜单项、设置导航、导航预览、筛选芯片、图例开关、范围单选、命令面板图标、快捷入口箭头、权限矩阵勾选、色板、追踪面包屑、问答输入、预览文件名。
- 判据纠偏（本轮最重要的一条）:
  - 第一版用 `\.is-[a-z]` 一把抓，把 **变体**（`.is-info` / `.is-success` / `.is-bordered` / `.is-sm` / `.is-disabled`）也算成硬跳。变体在挂载时就确定，给它加过渡只会在首屏闪一下，是伪需求。收紧到只认真交互态（`.is-on` / `.is-active` / `.is-selected` / `.is-open` / `:hover` / `:focus`）后，候选从 **97 → 55**，因此「78/68/59」那组数字是松判据下的，不可与收紧后的口径混用。
  - 曲线分派也不能看选择器名：`.table th.is-sortable` 里的 `is-sortable` 是**能力标记**（可排序 ≠ 状态切换），按 `is-` 判交接会误用对称曲线。现在只看属性。
- 三条必须守住的约束（都已写进 LOCAL-GUIDE）:
  1. **非法选择器不能落盘**——自动派生会产出 `.heat:has()` / `.page:not()` 这类空参形态，写进样式表会让浏览器从它开始丢弃后续规则。加 `selector_is_valid()` 兜底。
  2. **别给已有过渡的元素补 shorthand**——`.btn-primary:not(:disabled)` 同时带着已有过渡的 `.btn`，补一条会整条重置。生成器跳过。
  3. **逗号分组要拆开**——`.checkbox.is-on .checkbox-box, .checkbox.is-partial .checkbox-box` 整串匹配不上基选择器，属性被静默漏掉（这就是第一版只补到 `border-color` 的原因）。
- 验证: `MOTION_OVERRIDES: PASS (53 重定时 + 24 补建)`；抽查实测非 0（复选框方块 0.18s×3、开关滑块 0.22s `translate`）；`DEMO_HEALTH` 双主题 101 页 762 卡零命中。
- 已知遗留:
  - 剩 **55 个基选择器**未评估（收紧判据后的口径）。其中图形类（`.rg-node .rg-body::before`、`.heat-cell::after`、`.org-*`、`.bar-*`）占一半，补过渡可能改图形结构，要逐个判断；另一半是数据展示与预览缩略图，动与不动属设计取舍。
  - `.switch .switch-track` 没补：它靠 `--fill` 自定义属性驱动渐变，要 `@property` 注册才能过渡，属于另一个机制。
- 交接点: 无阻断。下一步：按 `--audit` 清单逐组评估剩余 55 个——图形类单独一批、需要逐个看补完是否真的更好；数据展示类若判定「该动」再补。

### 2026-10-31 侧栏多层级折叠菜单重设计（同日第九笔，未提交）

- 当前状态: 画廊侧栏从「父子平铺」改为可折叠分组，13 个分类默认只展开当前所在那一个；冻结面仍逐字节相等（新增第 5 条缝隙）；全量批跑见验证段。工作树未提交。
- 本轮目标: 用户截图指出左侧菜单「父子平铺不符合想法」，希望「点父级收起、展开子项」。
- 约束（决定了方案形态）: `components/layout/Sidebar.vue` 逐字节冻结，分类数据来自服务端 `navGroups`（只改数据层无效），模板结构无法扩展。
- 交付:
  1. `src/views/gallery/GalleryNav.vue`（新增）：可折叠分组导航。分类头是 `<button>`（`aria-expanded` + 条目数 + 旋转 chevron），折叠用 `grid-template-rows: 0fr ↔ 1fr`，收起态加 `inert` 防止 Tab 进入被裁项。
  2. `Sidebar.vue` 追加 2 行缝隙（import + `<GalleryNav />`），已登记 `SANCTIONED_SEAMS` → `SEAM: Sidebar.vue (+2 行)`。
  3. `overrides.css`：`.rail-nav:has(.gn) > .nav-group` 隐藏上游平铺分组与滑动块。用 `:has` 而不是运行时给父级加类，不给冻结组件留 DOM 副作用。
- 交互规则:
  - 默认只展开当前路由所在分类（全展开等于回到平铺长列表，折叠失去意义）；用户点过之后按他的选择持久化到 `scaffold.galleryNav.open`。
  - 路由变化自动展开目标分类；**收起的分组若含当前页，标题与计数转主色**，避免「导航丢了」。
- 踩坑（都已写进 LOCAL-GUIDE）:
  1. **示例卡里的 AppShell 会连带挂上本组件**——它是同一个冻结侧栏的样本。不加 `.g-cell` 判断时，演示卡里一次多出 4 套导航，`DEMO_HEALTH` 报 **816 条 `zeroIcon`**（双主题各 816）。真侧栏收起后实测 0 条。
  2. **`.nav-thumb` 会双重内缩**：上游 `left/right:12px` 是相对 `.rail-nav` 内边距算的，`.gn-list` 已在同样内边距里，再套一次 → 项目 207px、玻璃块只有 183px。`.gn-list .nav-thumb { left:0; right:0 }` 修正。
  3. **分类头不能用 `--ink-faint`**：3.1:1 达不到正文 AA，改用 `--ink-soft`；计数守 12px 下限，不靠压小 + 降透明度做层级。
- 验证: `vue-tsc rc=0`；`FIDELITY: PASS (273 local / 139 upstream)` 且 5 条缝隙全部识别；`DEMO_HEALTH` 浅色与暗色各 101 页 762 卡零命中；实测量测：真侧栏 13 组、示例卡内 `.gn` = 0、收起后 112 个图标零塌缩、玻璃块与项目行完全对齐（均 58→265）。
- 设计稿: Ardot `侧栏多层级折叠菜单 · 重设计`（fileId 742524501352325），左侧现状、右侧重设计，含收起态主色提示说明。
- 交接点: 无阻断。下一步候选：①分组顺序与计数来自服务端，若后端分组变化需要复核默认展开项的兜底；②折叠状态目前是「多开」，若用户觉得列表仍偏长可改成手风琴（同时只开一个）。
- 已验证的边界: **侧栏整体收成图标模式时不接管**——分组头只剩条目数和箭头（实测一列「6 / 8 / 23」），比上游的图标列表更糟，所以 `ready` 里带 `!railCollapsed`，该模式交还上游（实测 `.gn-head` 0 个、上游分组 `display: block`）。

### 2026-10-31 动效慢放验收 + 上下文文档自动归档（同日第八笔，未提交）

- 当前状态: 6 场景慢放实测完成；`PROJECT_CURRENT.md` 归档已脚本化并写成自动规则，历史小节已迁出。工作树未提交。
- 本轮目标: ①补齐计划里唯一未闭环的「手感验收」；②用户指出「历史小节该自动迁移，不需要用户提醒」。
- 一、慢放验收（`frontend-design/scripts/_compare_motion.py` 新增）
  - 做法：`transition-duration` 放大 10 倍做真慢放，逐帧采样计算值；同一交互跑两遍（旧 `ease` / 新语态），进度按起终点颜色连线投影归一，**只比形状不比速度**。
  - 结果：`按钮悬停` +45pt、`复选框选中` +43pt、`选项卡切换` +43pt、`日期格选中` +44pt、`级联选项选中` +43pt、`图标按钮悬停` +42pt（均为 25% 时长处的起步差距）。
  - 结论：**在四分之一时长处，旧曲线只走到约 38%，新曲线已到约 80%**；一半时长新曲线 95%+，旧曲线还在 75% 爬。六场景高度一致，映射规则在整个库上是同一条语言。
  - 工具的两个前提：①`nth` 选的是**第一个未处于目标状态的实例**——演示卡里第一个组件往往本来就选中，直接加状态类等于没加（前两轮只测出 2 个就是这原因）；②颜色变化过小或「起手 10% 时长内就 >92%」的样本丢弃，后者说明该属性没走过渡，量出来是假曲线（`.tree-row` 因此剔除）。
- 二、上下文文档自动归档
  - 新增 `context-recovery-rules/scripts/archive_project_current.py`：只搬 `## YYYY-MM-DD` 日期小节，逐字迁进 `PROJECT_HISTORY.md` 的「交接档案」区（`###` 降级、新条目置顶、保留最近 20 条），非日期小节（如「最近 5 个同项目会话」）原地不动。默认只打印计划，`--apply` 执行，`--check` 是闸门（日期小节 > 3 且字节 > 40,000 即退出 1）。
  - **规则已写进自举常量**（`bootstrap_agents.sh` 的 `BODY_SKILL_AUTO`）并同步到 `AGENTS.md` / `CLAUDE.md`：归档是收口时的自动动作，不需要用户提醒。三处内容一致，`cmp AGENTS.md CLAUDE.md` rc=0（各 30,019 字节）。
  - 本次已执行：`PROJECT_CURRENT.md` 44,374 → **13,174 字节**（14 → 3 个日期小节），11 个小节迁入 `PROJECT_HISTORY.md` 交接档案区；核对无内容丢失，`## 事件` 区 20 条原样保留。
- 已知遗留:
  - 慢放只覆盖 6 个可见色变场景。`树行`因颜色变化过小、`表格行`/`输入壳`/`分段控件`因该页无悬停入口未纳入——**未被测到不等于没升级**，它们同样吃第 2 批的覆盖块，只是缺少可量化样本。
  - 映射表本身未经审美复核：数据只能证明「起手更快」，证明不了「这个快得恰到好处」。
- 交接点: 无阻断。下一步候选：①按审美判断微调映射表（例如退场是否再快一档）；②把时长收敛成独立批次（目前 12 种散值只做了令牌定义）。

### 2026-10-31 动效语言升级：180 段默认 ease 全部收敛（同日第七笔，未提交）

- 当前状态: 计划里的 4 个批次全部落地；批跑 **31 项零失败**；`vue-tsc rc=0`；可写层与冻结层的默认 `ease` 清零。工作树未提交。
- 本轮目标: 用户先要「动效语言升级计划」，随后「按照计划执行」——把浏览器默认 `ease` 统一到登录页那套曲线。
- 执行结果:
  | 批次 | 范围 | 结果 |
  |---|---|---|
  | 1 | 可写层 `extend` + `workspace` | 29 文件 / 84 段改写为令牌，残留 **0** |
  | 2 | 冻结层 `src/styles/*.css` | 生成器派生 **53 条规则 / 96 段**，`MOTION_OVERRIDES: PASS` |
  | 3 | keyframes 14 段 | 仅 **4 段**需改（2 入场→`reveal`、2 呼吸→`swap`），7 段 spinner/倒计时保持 `linear` |
  | 4 | 守卫 | `MOTION_LANGUAGE: PASS`，已入 `_sweep.sh` |
- 新增件:
  1. `scripts/motion_language.py`：共享判定（拆段 / 属性优先分派 / 退场 ×0.8）。生成器与守卫共用，避免「生成按一套、校验按另一套」。
  2. `scripts/build_motion_overrides.py`：从冻结样式机械派生覆盖块，含 `--check` 与 `--selftest`（断言多属性分派、`@media` 复刻、`linear`/`premium` 排除、`reduced-motion` 排除、`keyframes` 排除）。
  3. `scripts/check_motion_language.py`：三条判据——可写层零默认 `ease`、冻结层默认 `ease` 必须被覆盖块接住、动画必须有具名曲线或覆盖。
  4. `scripts/_apply_motion_language.py`：批次 1 的一次性改写工具（带 dry-run，保留原有 `property <easing> <duration>` 笔法与换行符）。
- 执行中发现并修正的三处偏差（都写进了计划文档）:
  1. **统计高估**：第一版正则要求缓动在行尾，把既有 `property <easing> <duration>` 写法整段漏判，得出「225 段默认 ease / 11 段 premium」。用括号感知的拆分器重算是 **180 / 56**。
  2. **漏了一个样式文件**：`layout.css` 有 9 段过渡，最初没登记。现已改成「目录里出现未登记的 `.css` 直接 FAIL」，防再漏。
  3. **删除手写重定时清单**：`overrides.css` 原本手写 12 个选择器的重定时，与生成块重复。现在只留生成块一份来源；其中给 `.segmented button` / `.x-tabs-tab` 手写的 `swap` 按「属性优先」改判 `reveal`——真正的交接是滑动的 `.x-tabs-thumb`（`glide`）。
- 验证:
  - 计算值实测：`.btn` / `.icon-btn` / `.checkbox-box` / `.switch-track` / `.x-date-cell` 均为 `cubic-bezier(0.16, 1, 0.3, 1)`；`.skeleton` 的 `pulse` 为 `cubic-bezier(0.455, 0.03, 0.515, 0.955)`。
  - 批跑 31 项全 PASS：静态 19 + 渲染 12，含 `MOTION_OVERRIDES(53)` / `MOTION_LANGUAGE` / `DEMO_HEALTH` 双主题 762 卡 / `CRYSTALLIZE_VERIFY` / `KEYBOARD_VERIFY`。
- 已知遗留:
  - **手感本身没有机器验收**。守卫只证明「没有默认 ease」，证明不了「这条曲线选得对」。计划里的慢放抽查（6 个代表组件）仍未做，下一步应当人工过一遍。
  - 时长仍是 12 种散值，只做了令牌定义、未做收敛，退场 ×0.8 目前也只作用于批次 1 的改写。
  - `PROJECT_CURRENT.md` 已 4.3 万字节 / 15 个小节，接近 51,200 上限，历史小节该迁往 `PROJECT_HISTORY.md` 了。
- 交接点: 无阻断。下一步候选：①按计划第 6 节做慢放抽查并据此微调映射表；②把时长收敛成独立批次。

### 2026-10-31 动效审计 + 确认落定动效沉淀（同日第六笔，未提交）

- 当前状态: 组件数 153 → 154（新增 `ConfirmButton`），示例 750 → 762；`overrides.css` 新增「动效校准层」；落定动效抽成 `crystallize.ts` + `ConfirmButton.vue`。工作树未提交。
- 本轮目标: 用户带登录页两张截图——「再次检查每个组件的细腻程度、动画的流畅度，看看有没有需要优化的」+「把这个风格延续到其他组件的组件中」。
- 动效审计（量化，不是感觉）:
  1. **两套动效语言并存**。216 段 `transition` 里 **154 段用浏览器默认 `ease`**，只有 11 段用了 `--ease-premium`；而 `motion.ts` 的 `EASE` 是专门设计的五条曲线（expo/power4/power2/back）。默认 `ease` 起步钝、收尾也钝，没有能量语态。**登录那个动画之所以高级，不是形变更花哨，而是它拿到了真曲线**——这是本轮最重要的结论。
  2. 时长没有令牌，12 种散值（.12s～.5s）；同一语义的 hover 在不同组件上是 .15s / .2s / .25s。
  3. `transition: all` **0 处**（这点很干净，无需处理）。
  4. GSAP 侧布局属性动画只有 **4 处 / 约 94 处**：`Login.vue` 与 `crystallize.ts` 的宽度收拢（同源）、`motion.ts` 的 FLIP ghost（width/height 是共用元素转场的必要手段）。其余全是 transform/opacity，合成器友好。
  5. `base.css` 有全局 `*` 的 reduced-motion 兜底（`animation-duration: .01ms !important`），13 个组件额外遵守 `motionSkipped()`。降级链完整。
- 本轮交付:
  1. `overrides.css`「动效校准层」：五条 `--ease-*`（与 `EASE` 一一对应，取标准 cubic-bezier 近似）+ 四档 `--dur-*`；对用户会碰到的原语（btn / icon-btn / tag / nav-item / menu-item / input-shell / card / x-tabs-tab / segmented / perm-chip / user-chip / cmd-trigger）重新定时。进度条、跑马灯、骨架屏这类 **linear 语义**的排除在外。
  2. `src/composables/crystallize.ts`（新增）：`playCrystallize()` 把登录页三拍抽成可复用件——收拢 0.42s `swap` → 描环 0.5s `reveal`（提前 0.08s 交接）→ 画勾 0.32s `settle`（再压 0.22s 起笔，笔顺感就靠这个错位）→ 回弹 1 → 1.06 → 1。`motionSkipped()` 时直接给终态。
  3. `src/components/extend/ConfirmButton.vue`（新增）：`variant`/`size` 与 `Button` 同名同值，换用只改标签名。**受控**（传 `status`）与**自驱**（不传则点一下自己走完 pending→落定→复位）两种模式。
  4. 登记链：分类 `general>button`、组件说明、基础样本、slot 文案 + catalog → variants → events 三连。
  5. `scripts/_verify_crystallize.py`（新增）：逐帧采集宽度、两笔 `stroke-dashoffset`、回弹缩放，已并入 `_sweep.sh`。
  6. `LOCAL-GUIDE` 新增「动效（能量语态与确认落定）」整章；`references/component-checklist.md` 补动效检查项与两条已知坑。
- 关键决策:
  - **不新建曲线体系**，只把 CSS 侧拉回 `motion.ts` 已有的五条语态。新增令牌与 `EASE` 一一对应，`cubic-bezier` 取 GSAP 曲线的标准近似（`power2.in` = `.55,.085,.68,.53`，`power2.inOut` = `.455,.03,.515,.955`——我第一版写错了，靠复核 easings 标准值改回）。
  - **形变改内层圆而不是按钮宽度**：按钮盒子不动，内层 `.cx-orb` 从满宽收到 36px 正圆，布局不位移，工具栏里也能用。
  - **环与勾取圆的 88%**：按登录页 46px 圆 0.87 的比例换算到 36px 按钮高度，环会贴住蓝底边只剩 1.3px；88% 留出约 2.4px 呼吸，且比例不随尺寸漂移。
  - **自驱复位必须等动画真正结束**：固定 1800ms 会在慢帧机器上把最后那下回弹剪掉，而回弹正是确认感的来源。改成 `playCrystallize()` 的 Promise resolve 后再排 900ms。
- 守卫抓到的两个真缺陷（本轮修复）:
  1. `DEMO_HEALTH` 浅色 FAIL `lowContrast`：error 态把 `--red-text` 直接压在主色实底上，**红字铺蓝 1.01:1**。改为 `--red-soft` 底 + `--red-text` 字（与 `.btn-text.is-danger` 同一套语言）。
  2. `DEMO_HEALTH` 暗色 FAIL `noName`：落定后按钮里只剩图形，`aria-label` 挂在内层圆上，读屏读不到按钮名。改为挂到按钮本体。
- 验证（真实逐帧，不是看终态）:
  - `CRYSTALLIZE_VERIFY: PASS`——宽度 258 → 36 有 8 档以上中间值（是渐变不是跳变）、圆环 19 档 126→0、对勾 11 档 24→0 且**晚于圆环 284ms 起笔**、回弹 51 帧、收拢后宽高比 1.00、动画结束两笔 dashoffset 均归零、自驱能复位回可点击态。
  - `DEMO_HEALTH` 浅色 + 暗色各 101 页 762 卡零命中。
  - 全量批跑 **28 项零失败**（静态 16 + 渲染 12）；`vue-tsc rc=0`。
- 已知遗留:
  - 落定圆只有 36px（跟随按钮高度）。若某处需要更饱满的确认徽标，得让按钮高度长到 44px 并同步动画高度，目前没做。
  - `ConfirmButton` 的 `block` 默认 `true`：窄按钮上看不出「收拢」，需要形变的场景必须给足宽度。
  - 上一笔的 4 处硬编码蓝仍在。
- 交接点: 无阻断。下一步候选：①把 `crystallize.ts` 用到非按钮场景（结果页出现、行内保存）；②`--dur-*` 令牌目前只在 `overrides.css` 里定义，组件自身 scoped 样式仍写裸时长，可逐步迁。

### 2026-10-31 两个审计件转正为守卫 + 新增组件检查清单（同日第五笔，未提交）

- 当前状态: 守卫家族 22 → 24，批跑条目 26 → 27（新增 `CONTRACTS` / `A11Y_WIRING` 各带 `--selftest`，渲染段补入 `verify_keyboard`）；**静态 16 项 + 渲染 11 项全 PASS**，`vue-tsc rc=0`。工作树未提交。
- 本轮目标: 用户「都做」——① 把三种键盘模式抽成新增组件时的检查清单；② 两个审计件补阳性对照后转正为守卫。
- 本轮交付:
  1. `scripts/check_component_contracts.py`（由 `_audit_contracts.py` 改写）：`audit_source(label, raw)` 纯函数供真扫描与自证共用；`--selftest` 断言「死 prop / 只在默认值出现的 prop / 死 emit」三类必报、正常组件零误报。
  2. `scripts/check_a11y_wiring.py`（由 `_audit_wiring.py` 改写）：同结构；`--selftest` 断言两类缺口各报 1 项、七类豁免零上抛。新增 `class_tokens()` 归一 `:class="[...]"` 写法。
  3. 删除 `scripts/_audit_contracts.py`、`scripts/_audit_wiring.py`（被取代）。
  4. `references/component-checklist.md`（新增）：形态选型表（combobox / roving tabindex / 列表项 / 纯展示）→ 契约 → 样式 → 示例 → 无障碍 → 收口命令 → 已知的坑。规则正文仍归 `LOCAL-GUIDE`，清单只给操作序列。
  5. `LOCAL-GUIDE`：守卫清单补两条；「交互无障碍」节把审计件改成守卫名并加清单入口。
- 关键决策:
  - **审计件转守卫必须改退出码**：审计件是「只报不拦」恒 `rc=0`，放进批跑等于永远绿。两个守卫改为「有命中即 `rc=1`」。
  - **自证用合成样本，不注入真实组件**。仓库既有守卫多用「改真实文件再还原」，那是为了顺带验证文件发现链路；本守卫已有「扫到 <100 个组件即 FAIL」兜底，合成样本足以证明判据，且失败时不会留下半改的源码。
  - `a11y_wiring` 的 class 归一：`:class="['input-shell', ...]"` 直接按空格切会切出 `['input-shell',` 这种带符号 token，豁免表匹配不上就全量误报；显式剥离 `[ ] ' ,` 后才正确。
- 验证:
  - 静态 16 项全 PASS：`FIDELITY` / `GUARD_SELFTEST` / `INVENTORY(123/14/8)` / `CONTRACTS_SELFTEST` / `CONTRACTS(153)` / `CATEGORIES` / `PARITY(74)` / `COMPONENT_PARITY(131)` / `CATALOG(153)` / `DEMO_VARIANTS(750)` / `DEMO_EVENTS(122)` / `A11Y_WIRING_SELFTEST` / `A11Y_WIRING(153)` / `FONT_OVERRIDES(198,5)` / `ACCENT_PALETTES(5×2)` / `CONTRAST(14+10)` / `ADMIN_COVERAGE(153/153)`。
  - 渲染 11 项全 PASS：`SHADOW_CLIP` / `KEYBOARD_VERIFY` / `CORNER_OCCLUSION(112 页)` / `CONTENT_PADDING(750 卡)` / `DEMO_VISIBILITY(101 页 750 卡)` / `DEMO_GUIDES(101 页 750 卡)` / `EVENT_WIRING(341 条已接)` / `DEMO_HEALTH` 浅色与暗色各 101 页 750 卡零命中 / `HELP_TIP`。
- 踩坑（已写进 `_sweep.sh` 注释）:
  - **渲染类守卫不能与其它 Playwright 任务并发**。并发时 CPU 抢占导致 `wait_for_selector(".g-cell")` 30s 超时，报出假的「空页」失败；本次 `EVENT_WIRING` 与 `DEMO_HEALTH(light)` 就是这么假挂的，单独复跑即 PASS。
  - 批跑脚本运行中不能编辑：bash 按字节偏移读脚本，改行数会让它从半截继续执行。
- 交接点: 无阻断。下一步候选：①把 `KEYBOARD_VERIFY` 扩展到全部三种键盘模式（目前只覆盖 Steps 与 Cascader，roving tabindex 尚无浏览器实测）；②`component-checklist.md` 里的收口命令若与批跑条目再次分叉，考虑让清单直接引用 `_sweep.sh` 的分组。

### 2026-10-31 组件与示例全量遍历：死契约 / 接线 / 键盘可达性（同日第四笔，未提交）

- 当前状态: 22 个守卫全 PASS（上一笔遗留的 `CATALOG: STALE` 已查清并转绿），`vue-tsc rc=0`；组件侧修 3 处、审计工具新增 3 个。工作树未提交。
- 本轮目标: 用户「继续遍历检查所有组件和组件示例，修复，优化」。做法是把「遍历」变成可复跑的检查，而不是靠肉眼挨个看。
- 遍历手段:
  1. `scripts/_sweep.sh` 一次跑完 22 个守卫，输出每条 rc / 耗时 / 末行结论。
  2. `scripts/_audit_contracts.py`（新增）：死契约（声明了从不使用的 props / emits）。
  3. `scripts/_audit_wiring.py`（新增）：未声明就派发的事件 + 绑了 `@click` 却键盘到不了的元素。
  4. `scripts/_verify_keyboard.py`（新增）：浏览器里实测键盘操作，而不是只看代码里有没有 `keydown`。
- 遍历结果（153 个组件 / 750 张示例卡）:
  - 死契约 **0**（619 props、124 emits 全部在用）；未声明事件 **0**；图标按钮缺可读名 **0**（唯一命中是 `Button.vue` 自身，文字来自插槽，正常）。
  - 硬编码色只有 `ColorPicker` 与 `AppearanceSettings` 两处，均属必要：前者色板本身就是十六进制，后者是主题缩略图，**必须**脱离当前主题取色，否则深色下三张卡糊成黑白两团。
  - 可点击无键盘 **34 → 0**。其中真实缺口 2 个，其余是登记在案的豁免（combobox / tree 选项、微型动作、遮罩、触发器包装层）。
- 本轮修复:
  1. `extend/Steps.vue`：可点步骤此前只有 `@click`，键盘完全到不了。补 `tabindex`（仅在 `clickable && i <= current` 时给）与 Enter/Space 激活，并加 `:focus-visible` 焦点环（实测 `2px solid`）。**不换成 `role="button"`**——换了等于 `<ol>` 不再有列表项，`aria-current="step"` 也失去上下文。
  2. `extend/Cascader.vue`：菜单能开但里面一步都走不动。按 combobox 模式补完整键位——焦点留在触发器、`aria-activedescendant` 指向当前项、上下移动跳过 `disabled`、左右进退列、`Home/End` 到首末、Esc 收起并还焦点；`aria-activedescendant` 的 id 只在菜单打开时存在，同页多实例不会撞。焦点态用内描边（`.is-focus`）与选中态（底色 + 主色）分开，两者叠加仍分得清。
  3. `extend/Trigger.vue`：`disabled` 此前只拦开合，读屏读不出禁用。补 `aria-disabled` / `data-disabled`，并加 watch——运行中置为禁用会立即收起已打开的浮层，否则浮层挂着一个失效的触发区只能靠点外部关闭。外观不接管，留给调用方按 `[data-disabled]` 处理。
- 关键发现:
  - **`CATALOG: STALE` 不是漂移**。备份后重新生成并逐组件比对指纹，差异只有 `AppearanceSettings` 的 `props`——即上一笔加的 `sections` 没重跑生成。确认后重建，`CATALOG: PASS (153)`。
  - **审计工具本身最容易漏报**：死契约扫描若不去掉 `withDefaults` 的默认值对象，只在默认值里回过一次名的 prop 会被算成「已使用」；接线扫描若没遮蔽 `defineEmits` 声明块，每个事件都会把自己数成一次使用。两处都补了遮蔽，并用阳性对照验证（样本 3 项全中、正常样本 0 命中）。
- 验证:
  - `_verify_keyboard: PASS`——Steps 12 个步骤里 8 个可聚焦、Enter 把当前步从「部门审批」切到「提交申请」；Cascader Enter 开菜单 → `aria-activedescendant=x-cas-opt-1-0` → ArrowDown 到 `-1-1` → ArrowLeft 退回层级 0 → ArrowRight 进入层级 1 → Esc 关闭且焦点回到触发器。
  - `DEMO_HEALTH` 浅色 + 暗色各扫 101 页 750 卡，九类判据零命中；`CONTENT_PADDING` / `DEMO_VISIBILITY` / `DEMO_GUIDES` / `EVENT_WIRING` / `CORNER_OCCLUSION` / `HELP_TIP` 全 PASS。
  - 静态 12 项全 PASS：`FIDELITY(270 local)` / `INVENTORY(8 层)` / `CATEGORIES(153)` / `PARITY(74)` / `COMPONENT_PARITY(131)` / `CATALOG(153)` / `DEMO_VARIANTS(750)` / `DEMO_EVENTS(122)` / `FONT_OVERRIDES(198,5)` / `ACCENT_PALETTES(5×2)` / `CONTRAST(14+10)` / `ADMIN_COVERAGE(153/153)`。
- 已知遗留:
  - `.input-clear`、`x-tag-x`、`x-tabs-close`、`x-tree-arrow` 这类微型动作不占 Tab 位（与 Arco 一致），已在 `LOCAL-GUIDE` 写成明确豁免；要改就 11 个组件一起改。
  - `Dropdown` / `Popover` / `Popconfirm` / `Trigger` 的触发器包装层没有 `role`，可访问元素由插槽内容提供；若要给整个组件补 `aria-haspopup`，得先约定「插槽里必须是可聚焦元素」。
  - 上一笔的 4 处硬编码蓝（`instruments.css`、`pages.css`、`components.css`）仍未处理。
- 交接点: 无阻断。下一步候选：①把 `LOCAL-GUIDE` 的无障碍三模式抽成新增组件时的检查清单模板；②`_audit_contracts.py` / `_audit_wiring.py` 目前是审计件（`_` 前缀、不进 `_sweep.sh`），若想常态化，需先补阳性对照再转正为守卫。

### 2026-10-31 外观设置重做：字号入口可见化 + 主题控件改版 + 顶部栏入口重绘（同日第三笔，未提交）

- 当前状态: 面板重做已落盘，17 个守卫全 PASS，生产构建 rc=0（4.66s）；**工作树 87 个文件未提交**（含更早遗留的 16 个组件档位扩展改动，非本笔产物）。dev server 已停，5173 已释放。
- 本轮目标: 用户带截图反馈两点 —— ①「没看到可以切换和调整字体的」；②「切换主题的这个按钮也很难看，需要重新设计」。截图 1 圈的是顶部栏 `contrast` 入口按钮，截图 2 圈的是「外观设置」里的主题分段控件。
- 根因（都不是审美问题）:
  1. 字号面板 `AppearanceExtPanel` 是独立弹窗，只在 gallery 里可达；真实入口「外观设置」（`AppearanceDialog`）里只有主题与密度。**入口分裂**才是「找不到字号」的原因。
  2. 主题控件是三个纯文字分段项，460px 弹窗里塞不下 `浅色/深色/跟随系统`，只能换行左对齐，且看不出选中后长什么样。
  3. 顶部栏按钮用的是 stroke-only 的 `contrast` 字形：空心圆 + 一条竖线，17px 下读不出「深浅对比」，又没有控件边界，夹在胶囊搜索框和头像之间像装饰件。
- 本轮交付:
  1. `src/components/workspace/AppearanceSettings.vue`（新增）：外观设置**正文**，主题 / 主色 / 字号 / 表格密度四区合一。主题改为三张带缩略图的预览卡（半填充选中环 + 角标），主色为 5 个色点（挂 `data-accent` 自取色，深浅自动跟随），字号行带实时示例与 px 数值。
  2. `src/components/layout/AppearanceDialog.vue`：冻结文件，仅追加 2 行缝隙（`import` + `<AppearanceSettings />`），已登记 `SANCTIONED_SEAMS`；原 `.pref-list` 由 `overrides.css` 的 `.modal-body:has(> .apx) > .pref-list{display:none}` 隐藏。
  3. `overrides.css`：新增顶部栏入口按钮重绘——掩码补画半实心对比圆（跟随文字色），套用搜索框同款胶囊材质与 34px 高。上游 `<svg>` 保留在 DOM、只把描边设透明（`display:none` 会触发「零尺寸图标」判据）。
  4. `build_font_overrides.py`：紧凑档 `caption` 11px → 12px，三档统一守住「辅助字号 ≥12px」。重新生成 198 条覆盖。
  5. `AppearanceExtPanel.vue` 下线（重复入口），登记点同步：`workspace/index.ts`、分类 data、`demo-props`、`component-guides`，三份生成物按序重跑。
- 关键决策:
  - **正文与外壳分离**：冻结的对话框只保留外壳（标题 / 完成按钮 / 关闭），正文整块归本地组件。这样既不改上游一个字节，也不再出现「两个外观弹窗」。
  - **不做任意色相**：主色仍是 5 套预置、由守卫矩阵证明达标；自定义入口保留 `data-accent="custom"` + 同元素注入。
  - **紧凑档不再压最小字号**：12px 是验收条件本身，紧凑档的收紧只体现在 body（13px）。
- 验证（真实交互 + 渲染守卫）:
  - e2e：进页 `accent=blue` → 点「青碧」`dataset.accent=teal` → 点「宽松」按钮实测 `font-size: 15px`、示例行显示 `15 / 13px` → 刷新后 `dark/teal/large` 全部保持，控制台零错误。
  - `DEMO_HEALTH: PASS`（浅色 + 暗色两个主题各扫 101 页 748 卡，九类判据零命中）；`DEMO_VISIBILITY` / `DEMO_GUIDES` / `EVENT_WIRING` / `CONTENT_PADDING` / `ADMIN_COVERAGE(153/153)` 全 PASS。
  - `FIDELITY: PASS (270 local)`，`SEAM: AppearanceDialog.vue (+2 行)`；`INVENTORY(8 层)` / `CATEGORIES(153)` / `CATALOG` / `DEMO_EVENTS` / `PARITY(74)` / `FONT_OVERRIDES(198,5)` / `ACCENT_PALETTES(5×2)` / `CONTRAST(14 字色 + 10 色板)` 全 PASS。
- 已知遗留:
  - 对话框标题与「完成」按钮仍是上游形态，未品牌化；要合并成一体需上游升级或多开缝隙深度侵入，不建议。
  - 用户下拉菜单里的「外观设置」项仍用 `contrast` 小图标（菜单项，视觉权重低，未改）。
  - 主题卡方向键切换（同日后续已补：主题卡与主色点均接 `onRadioKey`，roving tabindex + 方向键带焦点，本条遗留已关闭）。
  - 上一笔的 4 处硬编码蓝（`instruments.css` 矩阵悬停、`pages.css` 登录渐变、`components.css` 复选框投影）仍在，换非蓝色板时会露出旧蓝。
- 交接点: 无阻断。下一步候选：①把 `AppearanceSettings` 抽成业务系统可直接引用的公开出口（连同 `appearance-ext` 一起写进 README）；②补主题卡方向键与 `aria-activedescendant`；③处理上述 4 处硬编码蓝。

### 2026-10-31 珍珠玻璃组件库：UI 评审 + 字号标度 + 主色色板 + 字色 AA（未提交）

- 当前状态: 五项改造全部落盘、14 个守卫全 PASS、生产构建 rc=0；**工作树 86 个文件未提交**（其中 16 个是更早遗留的组件档位扩展改动，非本轮产物）。本条即本轮交接点。
- 本轮目标（用户诉求演进）: ①评审珍珠玻璃并给可落地优化；②13px「好看但不实用、只能当美术品」→ 基准提到 14px 且字号可单点调整；③组件库要有通用的「字体调节 + 主题色切换」，使用方系统可覆盖，色板可随时新增。
- 本轮交付:
  1. `frontend-design/scripts/check_contrast.py`（新增）：字色令牌 + 主色色板双矩阵判定，含 `--selftest` 双向阳性对照。
  2. `build_font_overrides.py` 重写：由「非整数字号整数化」升级为「字号标度化」，10–15px 的 21 种散值归并为 5 档（caption 12 / sm 13 / body 14 / lg 15 / title 16），生成 198 条覆盖；支持 `data-font-scale` 三档（compact 12–15 / regular 12–16 / large 13–17，三档 caption 均不低于 12px），每档显式整数不用 `calc`。
  3. `build_accent_palette.py` + `references/accent-palettes.json`（新增）：一个种子色派生 12 令牌 × 5 套 × 2 主题，种子色不达标时沿 HSL 明度自动修正；同时产出 `src/data/accent-palettes.generated.ts` 供前端渲染色板。
  4. `src/utils/controlSize.ts` + 单测（新增）：档位 → 四变量映射，只出 `var()` 引用不写像素数字。
  5. `src/composables/appearance-ext.ts` + `src/components/workspace/AppearanceExtPanel.vue`（新增）：主色与字号两个维度的引擎与面板，`ADMIN_COVERAGE` 153/153 可达。
  6. `overrides.css`：字色四档整改、`.faint` 等 16 处小字用法迁移、`.btn-primary` 改读 `--blue-solid`、标签高度 22→24。
  7. `extend/` 110 处 scoped 字号并入标度（55 个文件）。
- 关键决策:
  - **冻结面比预期大**：`appearance.ts` / `AppearanceDialog.vue` / `AppShell.vue` 全属上游逐字节冻结，`LOCAL_MANAGED` 只收 `vite.config.ts` 与锁文件。外观扩展因此走「新增文件 + gallery 磁盘发现」，首屏防闪烁走 `index.html` seam（+3 行，已在 `fidelity_upstream.py` 的 `SANCTIONED_SEAMS` 登记，剥离后与上游逐字节相等）。
  - **主色拆 text / solid**：深底上当文字要 L≥0.206、当背景配白字要 L≤0.183，两区间不重叠；不拆时深色主题 5 套色板的按钮白字只有 2.09–3.20。
  - **扩展维度用独立存储键** `scaffold.appearance.ext`：上游 `appearance.ts` 用整对象回写 `scaffold.appearance`，共用键会被主题/密度切换冲掉。
  - **`--ink-faint` 退出文本档**：四档灰若全达 AA 会挤在 4.5–6 失去层次，改为「非文本档 3.14 + 文本只留 ink/muted/soft 三档」。
  - **字号基准 14 与解除 `BOUND-05`** 已作为 `DEC-04` 记录在 `doc/2-需求/2026-10-31_REQ-FONT-SCALE-001_字号标度与基准上调.md`，未改写旧需求正文。
- 验证: FIDELITY(270 local / 3 seam) · INVENTORY · CATEGORIES(153) · PARITY(74) · CATALOG(153) · DEMO_EVENTS · FONT_OVERRIDES(198, 5 组) · ACCENT_PALETTES(5×2) · CONTRAST(14 字色 + 10 色板) · ADMIN_COVERAGE(153/153) · DEMO_GUIDES(748 卡) · DEMO_VISIBILITY(748) · DEMO_HEALTH(九类零命中) · EVENT_WIRING(342 条) 全部 PASS；`npm run build` rc=0。真实交互实测：点青碧 → `data-accent=teal`、点宽松 → `.btn` 15px、刷新后两者保持；`/system/users` 两档字号下表格 `scrollWidth == clientWidth == 1040` 无溢出，手机号单元格宽 = 内容宽 = 117 未裁切。
- 已知遗留:
  - `extend/` 之外仍有 6 处 scoped 字号（`layout/` 2、`business/` 3、`ui/` 1），属冻结文件不可改。
  - 冻结样式里 4 处硬编码蓝色 rgba（`components.css` 复选框投影、`instruments.css` 矩阵悬停 ×2、`pages.css` 登录渐变）未跟随主色，换非蓝色板时这 4 处仍偏蓝。
  - 主题与密度绑死 `:root`，只能全局切换；主色与字号用不绑 root 的选择器，可局部嵌套。
- 交接点: 无阻断，可直接继续。下一步候选：①给那 4 处硬编码蓝补覆盖；②若要求明暗也支持局部嵌套，需把整套深色变量复制到覆盖层（多一份真相，需权衡）；③提交前按业务目标把 86 个文件拆成多笔。

### 2026-10-31 Skill 体系中等重构：流程链 16 环压到 5 环、元规则全部删除（未提交）

- 当前状态: 全部改动已在工作树落盘，**未提交**（无当轮 Git 授权）。`AGENTS.md` 62,059 → 29,931 字节，活跃 description 62,318 → 35,425 字符，活跃 SKILL.md 28,329 → 15,518 行；六条安全红线逐条保留并新增机器守卫。
- 本轮交付: ① 删除 10 个 skill 目录（`skill-audit-rules`、`team-development-rules`、`memory-usage-tracking-rules`、`task-plan-rehydration-rules`、`thread-title-rules`（含 `mcp/` 3400+ 文件）、`code-context-resync-rules`、`context-compression-rules`、`recent-context-bootstrap-rules`、`project-rule-file-bootstrap-rules`、`skill-execution-compliance-gate-rules`）；② 合并 3 组：合规收口组并入 `code-change-finalization-gate-rules`、上下文组并入新 `context-recovery-rules`、`project-memory-rules` 瘦身至 50 行；③ `skill-hit-check-rules` 115 → 29 行，`deferred-gate-registry.md` 17 → 18 行时机表；④ `test-strategy-rules` 385 → 83 行 + 8 个新 reference，`reasoning-summary-structure-rules` 382 → 104 行 + 4 个新 reference；⑤ 14 个领域 skill 的 Markdown 路由块三行并一行；⑥ 36 个活跃 skill 的 description 压缩；⑦ 删 `summary-check` Stop hook 与 `usage_count`/`absorbed_to`/v5 registry 机制；⑧ 新增 `test/skill-hit-check-rules/meta_rule_purge_test.py`（7 项断言）；⑨ 新增 `doc/5-tests/2026-10-31_skill体系中重构_链路走查与规模验证_测试主文档.md`。
- 关键决策: ① 元规则「全部删除」而非降级——打卡字段存在一天，AI 就会为它花掉注意力，降级方案必然回流；② 六条安全红线不做任何压缩改写，`保留（红线）` 锚点原文逐字保留，因为删规则时把红线一起带走比流程链过长严重得多；③ RED-2 从手写章节补成 `BODY_TEST_POLLUTION` 受管章节——它此前只存在于 `AGENTS.md` 手写部分，重新自举会让整节被覆盖消失，与 2026-10-29「提交即推送」静默丢失属同一类缺口；④ 新增守卫同时断言「`AGENTS.md` 里有」与「自举脚本里有」，只校验前者无法发现下次自举会冲掉红线；⑤ `__skillhub` 第三方种子不在改造范围，故规模口径以自建活跃 skill 为准。
- 验证: `meta_rule_purge_test.py` 7/7 PASS；`bootstrap_agents_test.py` 3/3 PASS（54.806s）；`cmp AGENTS.md CLAUDE.md` rc=0（均 29,931 字节）；`scan_test_pollution.py --diff-only` 输出 `POLLUTION: PASS`；`generate_dictionary.py --check` rc=0；连续两次自举字节不变（幂等）；测试主文档 `--profile test` 校验 PASS。
- 已知遗留: 全库 SKILL.md 26,357 行超 24,000 判据口径，差额全部来自 60 个第三方种子（10,839 行）；全量 Python 测试 3 个存量失败（空 `skills/` 目录遮蔽、`.system` 部分 `openai.yaml` 的 CRLF、gitignore 目录内的 `test_*.py`）在 HEAD 基线上同样存在。

### 2026-10-29 自举脚本恢复「提交即推送」归属注入并全量提交收口（Git 收口）

- 当前状态: `bootstrap_agents.sh` 已恢复按仓库 slug 条件注入项目专属 Git 授权正文，四份规则文件的受管章节同步刷新，回归测试 3 项全通过；本轮全部改动按三个业务目标分三笔提交并推送 `origin/main`（`3129f0b9` 生图模型收敛、`1a282ad9` 自举授权边界恢复、`9d81d7f0` 记忆计数与吸收冻结），工作树已清空。
- 本轮交付: ① 新增 `BODY_NO_AUTO_COMMIT_PROJECT_EXTRA` 正文常量与 `resolve_no_auto_commit_body()` 解析函数，按 `basename "$REPO_DIR"` 判定归属仓库后再在收尾条款前插入项目专属授权；② 配套回归测试 `test_commit_implies_push_extra_is_scoped_to_owner_repo`，对归属与非归属仓库双向断言；③ 根 `AGENTS.md` / `CLAUDE.md` 与两个子目录 `AGENTS.md` 的受管章节同步；④ 第一个业务目标（imagegen 模型收敛）另成一笔。
- 关键决策: ① 判定用仓库 slug 而非路径前缀——`basename` 对临时目录与真实仓库给出一致结果，回归测试可直接在 `TemporaryDirectory` 内覆盖两种仓库名；② 正文常量与注入逻辑必须同源同测，只改正文不补归属判定会让授权边界静默失效，而 `grep -c` 只能证明文本在、不能证明注入条件正确；③ 子目录规则文件走同一解析函数，保持「同一规则全仓一份权威正文」；④ 历史提交 `76975c58` 是这类「能力被回归掉」的唯一可靠线索，规则漂移排查先 `git log -S` 定位。
- 验证: `bash -n` 语法检查 PASS；`bootstrap_agents_test.py -v` 3 项全通过（55.177s）；`scan_test_pollution.py --diff-only` 输出 `POLLUTION: PASS`；`check_memory_anchors.py` 全绿（memory 58 实体、style 35/35、history 20/20）；`knowledge_index.py check` 全库 419 篇、死链 0、未挂载 0；`validate_engineering_docs.py --profile style_regression` PASS；`check_punctuation.py` ok；字典重跑 `implemented_total 66 / planned_missing 8 / seed_total 128`。仓库根 `package.json` 无 `build` 脚本，编译闸门按规则判 `N/A`。
- 知识库: 新增 `20-Knowledge/AI协作/默认值验证必须隔离配置优先级与进程缓存.md` 并挂载到 AI 协作 MOC；本轮另修复 11 篇存量笔记的 frontmatter、4 处死链与 5 处未挂载，全库合规检查从 12 处违规收敛为 0。巡检 `_index (1).json` 为 Google Drive 生成的 2026-10-19 陈旧索引副本（343 条 vs 现行 425 条），登记为同步冲突但不删除。
- 记忆计数: `rule.repo-commit-implies-push` 本轮实际引用升至 `usage_count 3 / usage_days 3`，达到吸收阈值；查重确认已被 `git-collaboration-rules` 完整覆盖（`SKILL.md` 行 29 + `references/current-turn-authorization.md` 项目级例外节），按「已覆盖则更新不新建」补入自举脚本归属注入的防漂移说明，并把 `absorbed_to` 写为 `git-collaboration-rules` 冻结计数，未新建重复 skill。

### 2026-10-27 imagegen 模型清单收敛为唯一 gpt-image-2（Git 收口）

- 当前状态: 仓库内 8 个文件已改（6 个 skill 资产 + 2 个字典产物）并新增 1 份 6-review 记录，已随本轮第一笔提交收口；本机 `~/.imagegen/config.json` 与两个用户级环境变量已按用户确认同步为 `gpt-image-2`。
- 本轮交付: ① `imagegen/SKILL.md` 的 description、模型章节、CLI 描述、配置兜底、核心规则统一为唯一 `gpt-image-2`；② `references/config.example.json` 三处模型字段收敛；③ `scripts/image_gen.py` 的 `DEFAULT_MODEL` 与函数注释；④ `scripts/imagegen.py` 的解析兜底与 `SKILL_CONFIG`；⑤ `CHANGELOG.md` 2.5.0；⑥ 吸收登记 `workbuddy-absorption-map.md` 与 `references/source-notes.md`；⑦ `doc/6-review/2026-10-27_imagegen模型收敛gpt-image-2_6-review.md` 并登记 README 索引；⑧ 字典刷新。
- 关键决策: ① 只改默认值，不加 `--model` 白名单——用户明确选择「只改默认值」，需在文档中写清该边界，避免被误读为参数层已锁死；② 历史文件（`CHANGELOG.md` 2.1.0、`source-notes.md` 旧条目、`workbuddy-absorption-map.md` 旧行）按只读保留，历史记录描述的是当时事实；③ `SKILL.md` 保留一条禁止条款列出两个历史模型名，用于阻断回退，属有意保留；④ `.system/imagegen` 官方快照不含被删模型，无需同步。
- 验证: 两脚本 `py_compile` 通过；示例配置 JSON 解析正常；隔离 HOME + 清除环境变量后 `_resolve_default_model()` 返回 `gpt-image-2`，新进程复验一致；`quick_validate.py` 返回 `Skill is valid!`；`POLLUTION: PASS`；5 个改动文件 UTF-8 无乱码、LF、无尾随空白；字典旧模型计数 0；6-review 六维自查 PASS。真实出图未执行（会消耗额度且用户未要求产出图片），已显式降级为静态验证。
- 已知遗留: `image_gen.py:39` `GPT_IMAGE_2_MODEL` 与 `image_gen.py:521` `_decode_and_write` 全仓无引用，属本轮之前的存量死代码，按最小改动原则未处置，登记为后续技术债候选。

### 2026-10-25 前端视觉改动对比 Demo 规则吸收与全量提交收口（Git 收口）

- 当前状态: 规则资产已落盘并已提交推送 `main`（提交 `d8600c2d`）；工作树改动为单一业务目标（前端视觉对比 demo 闸门），无索引漂移。
- 本轮交付: ① 新增 `frontend-design/references/visual-change-demo.md`（唯一权威细则：触发面与四类免触发面、对比形态 `M1`-`M4`、可判定性硬约束、保真五档样式来源、闸门语义、产物纪律）；② `frontend-design/SKILL.md` 第 2 步追加 1 行视觉改动对比闸门；③ `frontend-ui-visual-rules/SKILL.md` 暂停条件追加 1 行引用；④ `doc/6-review/` 新增 6-review 记录并登记 README 索引；⑤ 刷新 `skill-dictionary/data.js` 与 `字典.md`；⑥ 项目记忆与历史事件同步沉淀。
- 关键决策: ① 规则补进既有 `frontend-design` 而非新建独立 skill 目录——它已是前端 UI/组件/样式改动的主路径，另两处只留单句引用，避免双权威日后各自漂移；② demo 必须继承项目真实样式（五档来源：真实构建产物 CSS → token 源文件 → 挂项目跑真实组件 → `M3` 截图 → `getComputedStyle` 兜底），手搓近似样式会让「演示通过、落地不符」比不出 demo 更糟；③ before 版是校准基准，before 偏了 after 的判断随之失效；④ 免 demo 仅四类且必须写明依据。
- 验证: 两个 skill `quick_validate.py` 均 `Skill is valid!` 退出码 0（Windows 下需 `PYTHONUTF8=1`，脚本自身默认 GBK 解码会假失败）；三文件 UTF-8 且乱码替换符 0 命中；`references_total` 928→929 与实际新增 1 个 reference 一致；6-review 六维自查 PASS。仓库根仅 `package.json` 且无 `build` 脚本，编译闸门按规则判 `N/A`。
- 知识库: 细则已完整沉淀于 `20-Knowledge/AI协作/前端样式改动先出对比demo.md`，项目记忆只留一行结论加指针，避免两处各写一遍导致口径漂移。

### 2026-10-22 索引漂移识别与全量提交收口（Git 收口）

- 当前状态: 工作树已按业务拆成 8 笔提交并推送 `origin/main`；本轮新增的索引漂移判据已写入 `git-collaboration-rules/references/staged-review-and-evidence.md`「索引漂移前置核对」。
- 本轮交付: ① 索引被整体回退到 `3a9aa97e`（2026-10-15）的识别与恢复（392 条假删除 → 真实变更 106 项）；② Markdown 文档规则与 PPTX 外部种子；③ 生图配置统一目录；④ TAPD CLI 优先路由；⑤ 任务投影单会话唯一；⑥ design 组件库定位与 design+ 口径；⑦ `.system` 内置 skill 同步；⑧ 规则、记忆、字典与历史收口。
- 关键决策: ① 批量「已暂存删除」先按三重判据识别索引漂移，禁止直接提交（会静默吞掉期间提交）；② 恢复只用混合 `git reset`，禁止 `checkout`/`restore`/`rm`；③ pptx 外部种子用 `.gitattributes` 的 `pptx/** -whitespace` 保留上游字节；④ 组件数按 `CATEGORIES`/`CATALOG` 守卫实测校正为 152。
- 验证: git 规则 12 项、任务投影 87 项测试全绿；`POLLUTION: PASS`；每笔提交 pre/post gate 均 PASS；全量 476 项测试中 6 错 2 失败为 HEAD 基线同样存在的存量问题（本机 `~/.workbuddy` Python 软链失效、空 `skills/` 目录遮蔽、CRLF 存量）。

### 2026-10-16 珍珠玻璃组件库后台化：后台承载全部组件示例（Goal 收口）

- 当前状态: 151 个组件 **全部在管理后台可达并在后台内提供可操作示例**（覆盖率守卫 151/151），独立 `showcase.html` 入口已可逆退役、示例收敛为单轨。工作树未提交（无当轮 Git 授权）。
- 本轮交付: 新增 `src/views/gallery/`（示例页 + 单元格 + 磁盘发现入口 + 受控回写 + 四类样本）、`src/data/view-registry.ts`（本地页面登记处）、覆盖率守卫四模块（裁决入口 / 可达图访问器 / 引用边遍历 / 源码解析口径）；`mock/server.mjs` 改为直接 import 分类单一数据源生成 10 条组件库菜单；`src/composables/auth.ts` 开入 2 行声明式登记缝隙。
- 关键决策: ① 覆盖率不能靠改上游页面提高——139 个上游文件（含业务视图、路由、登记表）逐字节冻结且无冻结文件 import 本地模块，故新增本地后台路由页 + 单一登记缝隙；② 缝隙不按整文件豁免，改为「剥离声明行后必须等于上游字节」，缝隙外改动仍报 DRIFTED；③ 覆盖率判据要求「导入的本地名真被使用」，只 import 不渲染不计入，防批量导入刷满；④ 退役入口用临时目录搬移而非删除（本仓库配置 Git content filters，`git ls-files` 不能当还原兜底）。
- 行数基准返工: 首版守卫 250/270 行、可达图工厂函数 157 行越基准，已拆为 90/167/107/115 与 151/181 行、最大函数 23 行；示例样本 666 行单文件无损拆为四类；三个样本文件写出为 CRLF 已按组件库 `eol=lf` 策略归一。
- 验证: `ADMIN_COVERAGE: PASS(151/151)`、`CATEGORIES: PASS(10 类 151)`、`CATALOG: PASS(151)`、`FIDELITY: PASS(244 本地/139 上游)` + `SEAM`、`GUARD_SELFTEST: PASS`、`INVENTORY: PASS`、`COMPONENT_PARITY: PASS`、`PARITY: PASS(74)`、`POLLUTION: PASS`、`vue-tsc` 零报错、`vite build` 成功、单测 21/21；真实浏览器十分类挂载 11/8/16/33/31/12/6/20/8/6=151、空白卡片 0、渲染错误 0，输入回写 / 开关翻转 / 弹层开合 / 提示与确认宿主均真实状态迁移。证据见 `doc/5-tests/2026-10-16_193800_REQ-PEARL-ADMIN-GALLERY-001_组件库后台化_测试主文档.md` 与 `doc/6-review/2026-10-16_202200_珍珠玻璃组件库后台化_6-review.md`。
- 守卫变异自证: 收窄示例页发现面 → `FAIL(75/151)`；给登记缝隙文件追加未声明行 → `FIDELITY: FAIL drifted=1`；两者还原后恢复 PASS 且文件校验和回到注入前。
- 已知缺口: `ui/DataTable.vue` 无列排序（上游冻结 + 多页消费，需以需求立项）；上游 `motion.ts` 的 `revealPage` 无引用（冻结层，转评估）；画布类组件视觉只能前台取证（上游隐藏标签页停帧属预期）。
