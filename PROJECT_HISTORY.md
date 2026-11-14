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

### 2026-10-31 浮层入场改为「优化版缩放」：用户实测推翻规范推断（同日第二十七笔，未提交）

- 当前状态: 内容面板入场回到**从锚点缩放**，并修掉上游 `modal` 分支的三个缺陷。全守卫 PASS。
- 用户反馈: 「A 缩放是最好的，丝滑，还可以更好吗？」——**推翻了上一笔的判断**。
- 判断反转（必须记住的教训）:
  - 上一笔我按 Material 规范（对话框 `scale 0.86` / 菜单 fade + slide）把下拉改成位移，理由是缩放会让文字重栅格化、背景模糊跟着缩放。
  - 但实测观感相反：**缩放有「从触发器长出来」的来源感，位移只是「滑进来」，缺来源**。
  - 结论：规范是通用参考，**实际观感优先**。技术缺陷应该被修掉，而不是用换语法来回避。
- 三项修复（`morph.ts` 自己实现，参数可控）:
  1. **长尾**：`expo.out` 46ms 就到 0.944、之后 150ms 只再走 0.05。换 `glide`（`power4.out`），时长 380 → **280ms**。
  2. **文字重栅格化**：入场挂 `will-change: transform, opacity` 提升合成层，`onComplete` 立即 `clearProps` 清理（实测 310ms 后回到 `auto`）。
  3. **原点不准**：上游按面板几何算 `transformOrigin`，轴心可能落在中部像「从肚子鼓起来」。固定为**顶边中心**（面板在视口上半则底边）。
- 实测: scale `0.914 → 0.955 → 0.98 → 0.992 → 1`，**209ms 到位**（原版 262ms 才到 0.995）。
- 对比工具: `frontend-design/references/overlay-motion-compare.html` 已改为三栏——A 原版缩放 / **A+ 优化缩放（现在）** / B 位移对照，带真实 `backdrop-filter` 材质。
- 顺带记录一个被证伪的假设: 之前怀疑「掉帧 / 背景模糊重算」导致卡顿，实测 rAF 稳定 16.7ms、零超 20ms 帧，**主线程没压力**；首帧宽度也单调递增无跳变。观感问题来自曲线与栅格化。
- 验证: `vue-tsc rc=0`；`OVERLAY_MOTION: PASS`；`FIDELITY: PASS`；`DEMO_HEALTH` 双主题 101 页 763 卡零命中。
- 交接点: 无阻断。若还需更「贴手」，可试 A+ 的时长再压到 0.24s，或 scale 收到 0.9。

### 2026-10-31 浮层入场改位移：定位「不丝滑」的真因（同日第二十六笔，未提交）

- 当前状态: 内容面板入场从「锚点缩放」改为「位移 12px + 淡入」；小气泡仍走 `pop`。全守卫 PASS。
- 用户反馈: 「弹出窗口还是不够丝滑，有一叠卡顿感，为什么？」
- 排查（三个假设逐个证伪/证实）:
  1. **掉帧？否**。实测 rAF 平均 16.7ms、最大 16.8ms、超 20ms 帧 **0**；关掉 `backdrop-filter` 后数据相同。
  2. **首帧跳变？否**。逐帧记录面板宽度单调递增 `221.9 → 256.6`，无「先大后小」。
  3. **真因：语法用错 + 材质冲突**。`.m-float` 带 `backdrop-filter: blur(28px)`，对它做 `scale` 会让浏览器每帧按新尺寸重采样背景并重算高斯模糊——**透过面板看到的卡片也在缩放**；同时面板内文字被重新栅格化，动画中发虚。叠加 `expo` 曲线长尾（262ms 时 scale 仍停在 0.995），观感就是「一叠卡顿」。
- 规范依据: Material 把对话框（从中心升起）用 `scale 0.86`，**菜单用 fade + slide**。下拉紧贴触发器，属于后者。上一笔把 dialog 的语法套到了 menu 上。
- 修复: `overlayMenuEnter` 自己实现位移入场（`y 12 → 0` + 淡入，0.26s `--ease-reveal`），**完全不缩放**；方向按面板落在视口上半/下半决定；退场只淡出 0.14s。小气泡仍调上游 `pop`。
- 实测新入场: scale **恒为 1**；`y 7.9 → 3.3 → 1.3 → 0.4 → 0.1 → 0`；opacity `0.35 → 0.73 → 0.89 → 0.96 → 1`；**216ms 完全落定**（此前 262ms 还停在 0.995）。
- 对比 demo: `frontend-design/references/overlay-motion-compare.html` —— 三栏并排（A 缩放 / B 位移 12px / C 位移 8px 更快），**带真实 `backdrop-filter` 材质**，否则看不出差别。已实测可运行、零报错。
- 验证: `vue-tsc rc=0`；`OVERLAY_MOTION: PASS`；`FIDELITY: PASS`；`DEMO_HEALTH` 双主题 101 页 763 卡零命中；`A11Y_WIRING` / `KEYBOARD_VERIFY` PASS。
- 交接点: 无阻断。若用户觉得 12px 仍偏弱，C 方案（8px + 0.20s）已在 demo 里备好。

### 2026-10-31 浮层入场全量统一 + 经验沉淀（同日第二十五笔，未提交）

- 当前状态: 22 个浮层全部接入统一入口，按「面板内有无可操作项」自动分派形态；新增 `OVERLAY_MOTION` 守卫；规则沉淀进 `PROJECT_MEMORY.md`。全守卫 PASS。
- 用户要求: 「都统一，吸收为项目经验」。
- 统一做法（关键设计决定）:
  - **不是把所有浮层都改成同一个参数**——Tooltip 这类几十像素的纯文字提示从 0.86 放大会像「弹」。
  - 改成**统一规则、分层表现**：`overlayMenuEnter` 按面板里有没有可操作项（`button` / `[role=menuitem]` / `[role=option]` / `[role=treeitem]` / `input` 等）分派，有则 `modal`（14% 形变），纯文字则 `pop`（轻量淡入）。
  - 判据用「可操作性」而非宽度：下拉菜单可能只有 160px、确认气泡反而更宽，按尺寸分会判反。
- 接入范围: 全库 22 个浮层，包括此前的 `BackTop` `HelpTip` `Popconfirm` `Tooltip` `Trigger` 与冻结层的 `Select` `HoverCard` `Topbar`。全库已无裸 `overlayEnter(..., 'pop')` 调用。
- 实测分派: Dropdown/Cascader/DatePicker/Select 起始 `0.86`；Popconfirm 起始 `0.86`（有确认按钮）；Tooltip 起始 `0.986`（纯文字）。**判据正确**。
- 冻结面: `Select` `HoverCard` `Topbar` 三个文件登记进 `LOCAL_MANAGED`，校验打印 4 条 `OVERRIDE`（含 package-lock）。
- 新增守卫: `scripts/check_overlay_motion.py`（`OVERLAY_MOTION`）——组件里直写 `overlayEnter(..., 'pop')` 即 FAIL，防止绕过统一入口。双向验证通过，已接入 `_sweep.sh` 第 41 项。
- 经验沉淀（写进 `PROJECT_MEMORY.md` 新章节「组件库动效：形变语言与浮层入场规则」）:
  1. 缓动与形变是两件事，不要互相冒充。
  2. 形变起点必须是「无」而非「小」（0.6→1 只是弹一下，0→1 才是长出来）。
  3. 入场力度按体量分档（列表错位 / 单件上浮 / 色块 0.9 起 / 小气泡淡入）。
  4. 展开必须双向，一端有动效一端瞬删比都没有更僵硬。
  5. `animation-fill-mode` 用 `backwards` 不用 `both`（后者会压掉 hover 位移且不报错）。
  6. 浮层形态按可操作性分派，不按类型、不按尺寸。
  7. 冻结面破例要登记、写明代价与回退；非必须不扩清单。
- 验证: `vue-tsc rc=0`；`OVERLAY_MOTION: PASS`；`FIDELITY: PASS (274 local)`；`DEMO_HEALTH` 双主题 101 页 763 卡零命中；`A11Y_WIRING: PASS`。
- 交接点: 无阻断。`LOCAL_MANAGED` 现有 3 个 `src` 文件，是本次的代价，后续非必须不再扩。

### 2026-10-31 Select 解冻：登记为本地受管例外（同日第二十四笔，未提交）

- 当前状态: `Select` 入场改为锚点展开，文件登记进 `LOCAL_MANAGED`；冻结面 PASS 且例外被显式打印。双主题健康、无障碍、键盘全 PASS。
- 用户授权: 「允许」（针对上一笔提出的「要统一得先解冻 `ui/Select.vue`」）。
- 改动: `ui/Select.vue` 两处——Transition 的 `@enter`/`@leave` 换成 `overlayMenuEnter`/`overlayMenuLeave`，import 来源换成 `@/composables/morph`。
- 实测: scale `0.86 → 0.92 → 0.965 → 0.991 → 1`，**14% 幅度**，与 Dropdown / Cascader / DatePicker 一致。
- 冻结面处理（关键）:
  - 直接改会让 `verify_fidelity.py` 报 `DRIFTED: src/components/ui/Select.vue` → `FIDELITY: FAIL`（已实测确认守卫有效）。
  - 登记进 `fidelity_upstream.py` 的 `LOCAL_MANAGED` 后转为 `OVERRIDE: src/components/ui/Select.vue (local-managed, declared)`，`FIDELITY: PASS`。
  - **代价写在代码注释里**：该文件从此不再与上游比对，上游修 bug 或改交互本地不会告警；回退方式是删掉那行并恢复原 Transition 属性。非必须不要再往清单加 `src` 文件。
- 仍受限: `Topbar`（`layout/`）、`HoverCard`（`ui/`）保持 `pop`；`Trigger` 是通用基件保持原样。这三个使用频率低，暂不破例。
- 验证: `vue-tsc rc=0`；`FIDELITY: PASS (274 local)`；`DEMO_HEALTH` 双主题 101 页 763 卡零命中；`A11Y_WIRING: PASS`；`KEYBOARD_VERIFY: PASS`。
- 交接点: 无阻断。浮层入场现覆盖 17 个组件，小气泡类刻意保留轻量形态。

### 2026-10-31 浮层入场统一：25 个弹出层从「几乎无动画」改为锚点展开（同日第二十三笔，未提交）

- 当前状态: 16 个菜单类浮层改走 `modal` 入场形态；4 个小气泡按设计保留 `pop`；3 个冻结组件受限于上游无法改。双主题健康、示例可见性、冻结面全 PASS。
- 用户要求: 「检查其他会弹出子层级的组件，是否也有同样问题，一起修复」。
- 排查结论:
  - **30 个组件用 `overlayEnter`**（有入场），只有 4 个裸 `v-if`：`MenuNode`（上一笔已修）、`Notification` / `Tree` / `Upload`（不是浮层）。
  - 但 **25 个走 `pop` 分支**，参数是 `y -6 + scale 0.98`。实测下拉 scale 只从 **0.986 → 1**，**幅度 1.4%**，肉眼等同于无动画，只剩淡入。**这就是「僵硬」的真因，与菜单同源。**
- 修复: `morph.ts` 增 `overlayMenuEnter` / `overlayMenuLeave`（语义包装，内部走 `'modal'` 分支——从锚点 `scale .86` 展开，退场 `.94`）。组件只改 `@enter` / `@leave` 与 import。
- 实测（真实指针点击）:
  | 组件 | scale 曲线 | 幅度 |
  |---|---|---|
  | Dropdown | `0.86 → 0.884 → 0.944 → 0.984 → 1` | 14% |
  | Cascader | `0.87 → 0.93 → 0.966 → 0.991 → 1` | 13% |
  | DatePicker | `0.86 → 0.908 → 0.965 → 0.99 → 1` | 14% |
- 改动范围（16 个，全在 `extend/` 可写层）: Dropdown / DropdownButton / DropdownSubmenu / Cascader / ColorPicker / DatePicker / MonthPicker / QuarterPicker / RangePicker / WeekPicker / YearPicker / TimePicker / AutoComplete / Mention / TreeSelect / OverflowList，外加内容气泡 Popover。
- 刻意保留: `Tooltip` `HelpTip` `Popconfirm` `BackTop` 走 `pop`——小气泡缩放会显得「弹」，不能一刀切。
- 无法改: `Select`（`ui/`）、`Topbar`（`layout/`）、`HoverCard`（`ui/`）在冻结面；`Trigger` 是通用基件，保持原样。
- 关键认知: **`motion.ts` 逐字节冻结，缝隙只允许追加精确行**，改不了 `pop` 分支的 `0.98`。所以只能在调用侧换形态——这也是为什么加了语义包装而不是直接写 `'modal'`（第三个参数描述入场形态，不代表组件是弹窗）。
- 验证: `vue-tsc rc=0`；`DEMO_HEALTH` 双主题 101 页 763 卡零命中；`DEMO_VISIBILITY` PASS；`FIDELITY: PASS (274 local)`。
- 交接点: 无阻断。`Select` 若要一并改，需先解冻 `ui/Select.vue` 或与上游同步该改动。

### 2026-10-31 菜单展开收起改为双向高度形变（同日第二十二笔，未提交）

- 当前状态: `MenuNode` 子菜单从「只有展开有动效」改为**双向高度形变**；箭头状态改绑 `subOpen`。双主题健康、无障碍接线、键盘验证全 PASS。
- 用户指出: 截图中「监控中心」的展开收起「太僵硬，一点动画效果都没有」。
- 根因: 上一轮做的是「子项逐条落下」，但那只覆盖**展开**；收起仍是 `v-if` 直接卸载，元素瞬间消失。一端有动效一端没有，反而比全都没有更显突兀。
- 修复:
  1. `<Transition :css="false" @enter="onSubEnter" @leave="onSubLeave">` 包住 `<ul v-if="subOpen">`。
  2. `@enter`：`height: 0 → auto` + `opacity 0 → 1`，0.24s `--ease-swap`。
  3. `@leave`：`height → 0` + `opacity → 0`，0.18s `--ease-exit`，`onComplete: done`。
  4. `.x-menu-sub` 加 `overflow: hidden` 裁切；撤掉原来的 `menu-unfold` 逐行落下（与高度形变叠加会乱）。
  5. 箭头 `:class="{ 'is-open': subOpen }"`（原绑 `expanded`，浮层态下永远不转）。
- 实测:
  - 内联展开：高度 `0 → 7 → 34 → 71 → 72px`，opacity `0 → 1`；收起 `72 → 68 → 53 → 0`。
  - 浮层展开：高度 `14 → 67 → 86`，opacity `0.17 → 0.78 → 1`。
  - 箭头：收起 `transform: none` → 展开 `matrix(-1,0,0,-1)`（180°）→ 收起还原。
- 差点踩的坑: `onEnter` / `onLeave` **在 MenuNode 里已被悬停逻辑占用**（`@pointerenter` / `@pointerleave`），直接用同名会把悬停展开覆盖掉。TypeScript 的 `Duplicate function implementation` 拦下了这次覆盖，改名为 `onSubEnter` / `onSubLeave`。
- 验证: `vue-tsc rc=0`；`A11Y_WIRING: PASS`；`KEYBOARD_VERIFY: PASS`；`DEMO_HEALTH` 双主题 101 页 763 卡零命中。
- 交接点: 无阻断。

### 2026-10-31 示例层视觉一致性：栅格占位块成材 + 新增守卫（同日第二十一笔，未提交）

- 当前状态: `GridRow` 示例的两个裸色块改为库内槽材质；新增 `DEMO_STYLE` 守卫并入批跑（第 52 项）。双主题健康、内容留白全 PASS。
- 用户指出: 截图显示 `GridRow` 示例里两个「半宽列」是**纯色矩形**，与整屏玻璃/面板语言明显不一致。
- 根因: 示例层直接拼内联样式 —— `style: 'padding:8px;background:var(--blue-soft)'`，**没有圆角、没有描边、没有材质、字号也没走令牌**，所以看着像调试占位块。而且 `--blue-soft` / `--lime-soft` 是语义色（accent / success），在栅格示例里没有任何语义，纯装饰性上色。
- 修复: 改用库内 `.m-groove` 材质（`border 1px + groove 底 + 内阴影`）+ `border-radius: var(--r-sm)` + `font-size: var(--fs-sm)` + 居中。实测 `radius 12px / border 1px / fs 13px / text-align center`，8 个 GridRow 示例一次修复。
- 全量排查: 运行时扫 101 页示例卡的内联视觉样式，命中 29 种，**除 GridRow 外全部合理** —— 头像是按名字派生色（内容色）、取色器色块是内容、时间线节点用 `var(--red)` 令牌、图标用 `var(--ink-soft)`。**没有第二处裸色块。**
- 新增守卫: `scripts/check_demo_style.py`（`DEMO_STYLE`）。判据：示例层内联 style 里出现 `background` 但缺 `border-radius` / `border` / 材质类 → 失败。已做双向验证（当前 PASS；旧写法能被命中）。已接入 `_sweep.sh`。
- 规则沉淀: `LOCAL-GUIDE` 新增「示例内容本身也要成材」一节，含正反例与边界（示例图片 SVG 色值、取色器色值属内容，不算违规）。
- 副产物: 期间发现 dev server 已挂（`curl` 返回 000），重启后守卫恢复；浏览器类守卫依赖它存活，挂掉时表现为导航超时而不是判据失败。
- 验证: `DEMO_HEALTH` 双主题 101 页 763 卡零命中；`CONTENT_PADDING` PASS（763 卡无文本贴边）；`DEMO_STYLE` PASS。
- 交接点: 无阻断。

### 2026-10-31 全组件复检：修掉一个静默功能回归（同日第二十笔，未提交）

- 当前状态: 31 项守卫全 PASS；发现并修复一处**由我自己上一笔引入的回归**——卡片悬停上浮失效。工作树未提交。
- 复检目标: 用户「再次遍历检查一下所有组件」。重点是查上一轮批量加动画带来的副作用，而不是重跑一遍守卫。
- 发现的真问题: **`animation-fill-mode: both` 会永久占用属性**。入场动画末帧是 `transform: none`，而 CSS 动画在层叠里优先于普通声明 → `.x-card:hover { transform: translateY(-2px) }` 被压掉，悬停上浮直接失效。页面上只表现为「不浮了」，不报错、守卫也抓不到。
- 修复: 5 处入场动画的 `both` → `backwards`（只在开始前补首帧，结束即释放）。复测：静止 `none`、悬停 `matrix(1,0,0,1,0,-2)`，上浮恢复；`animationName` 仍为 `morph-enter`，入场未被削弱。
- 同源排查: 逐个检查被加动画的 10 个类（`.x-card` `.panel` `.spec-plate` `.tag` `.x-badge` `.delta-pill` `.quick-link` `.bento-grid` `.share-list` `.activity`）是否还有 hover/active 位移 —— **只有卡片一处**，其余无位移，未受影响。
- 验证: 全量批跑 **31 项零失败**（含 `MOTION_OVERRIDES: PASS (53 重定时 + 26 补建)`、`DEMO_HEALTH` 双主题 101 页 763 卡零命中、`FIDELITY: PASS`、`vue-tsc rc=0`）。
- 教训（已写进计划与记忆）: 给元素加完入场动画后，**必须复测它原有的 hover/active 位移还在不在**（悬停前后 `getComputedStyle(el).transform` 是否变化）。只看「动画播得对」会漏掉这类静默回归。
- 交接点: 无阻断。

### 2026-10-31 形变通用语式三：单件容器 + 纯色块（同日第十九笔，未提交）

- 当前状态: 补齐最后两类。双主题健康、动效语言全 PASS。
- 新增两条:
  1. **单件容器上浮**（`.x-card` `.panel` `.spec-plate`）：6px 上浮 + 淡入，**不做错位**——它们不是列表，整页一起落位才是正确读法。实测 `opacity 0.89→0.96→1`。
  2. **纯色块落定**（`.tag` `.x-badge` `.delta-pill`）：出现时 `scale .9 → 1`，0.2s `--ease-settle`，末尾轻微过冲读作「贴上去了」。**不从 0 起**——色块体量小，从 0 长出来像闪。实测 `scale 0.98→1.01→1`。
- 至此形变覆盖（去重）: 7 个专门实现 + 12 个列表入场 + 5 类选中行 + 3 类单件容器 + 3 类纯色块 + 26 个浮层自带 ≈ **35 个组件**。
- 验证: `DEMO_HEALTH` 双主题 101 页 763 卡零命中；`MOTION_LANGUAGE: PASS`。
- 交接点: 无阻断。形变语言到此覆盖了「列表 / 单件 / 色块 / 选中 / 完成 / 浮层」六类场景，剩余未覆盖的是纯装饰性组件（Divider / Space / Grid 等，本身没有状态）。

### 2026-10-31 形变通用语式二：选中强调条（同日第十八笔，未提交）

- 当前状态: 新增「选中强调条从中心长出」（`scaleY 0→1`，0.22s `--ease-swap`），覆盖 5 类选中行。双主题健康、动效语言全 PASS。
- 覆盖: `.x-menu-item` `.select-option` `.x-cas-option` `.tree-row` `.x-tree-row` → 菜单 / 下拉 / 级联 / 业务树 / 组件树。
- 实测: 菜单切换选中项时强调条 `scaleY 0 → 0.19 → 0.7 → 1`；树行 `.x-tree-row.is-selected` 实测 2.5px 蓝条、`translateY(-50%)` + `scaleY 1`。
- 踩坑（重要）: **`.tree-row` 与 `.x-tree-row` 是两套类名**——前者属冻结的 DeptTree / PermissionTree，后者属可写的 TreeNode / TreeSelect。只写一个会漏掉一半，第一版就是这样漏的。
- 纠正上一笔的判断: 浮层类**本来就带入场形变**，不是「改不了」。`overlayEnter` 里 drawer 用共享元素 ghost 从被点的行长成抽屉、modal 从触发点 `scale .86→1`、pop 是 `y -6 + scale .98`（克制但存在）。冻结的是参数微调，不是能力缺失。
- 验证: `DEMO_HEALTH` 双主题 101 页 763 卡零命中；`MOTION_LANGUAGE: PASS`。
- 交接点: 无阻断。形变现覆盖约 25 个组件（7 个专门实现 + 12 个列表入场 + 5 类选中行 + 浮层自带）。

### 2026-10-31 形变通用语式：列表入场（同日第十七笔，未提交）

- 当前状态: 用户反馈「希望更多组件有形变」。逐组件改只有 7 个，改成**一条通用语式覆盖一批**：`overrides.css` 新增 `morph-enter` 关键帧 + 8 组列表容器选择器。形变覆盖从 7 个组件扩到约 20 个。
- 做法:
  - `@keyframes morph-enter`：`opacity 0→1` + `translateY(6px)→0`，0.26s `--ease-reveal`。
  - 容器选择器：`.table tbody tr`、`.x-datalist .x-datalist-row`、`.x-timeline .x-timeline-item`、`.activity-list > .activity`、`.share-list > li`、`.x-desc .x-desc-item`、`.bento-grid > *`、`.quick-link`。
  - 错位：前 8 条各差 26ms，第 8 条起封顶 104ms（长列表不该滚出一波浪）。
- 覆盖组件: `DataTable` `ListPage` `PermissionMatrix` `GeneratorPipeline` `DataList` `Timeline` `TimelineItem` `ActivityList` `ShareList` `Descriptions` `BentoGrid` `ShortcutGrid`。
- 边界: 只对「一条一条进来」的容器生效。卡片、面板这类单件**不加**——不是列表，逐条落下没有语义；加了会变成「整页都在动」。
- 验证: 实测表格行起点 opacity 0.93 / 0.86 / 0.72（延迟不同，逐条落下成立）；`DEMO_HEALTH` 双主题 101 页 763 卡零命中。
- 交接点: 无阻断。要再扩只有两条路：①给冻结的 `overlayEnter` 开缝隙（26 个浮层组件的入场）；②给组件新增选中标记元素（8 个选中类）。

### 2026-10-31 形变全量扫描 + 收口（同日第十六笔，未提交）

- 当前状态: 154 个组件全部扫过并分类；本轮新增 `MenuNode` 子菜单展开。形变覆盖 **7 个组件**（含此前 6 个）。双主题健康、动效语言、冻结面全 PASS。
- 扫描结论（154 个组件）:
  | 分类 | 数量 |
  |---|---|
  | 已有形变 | 12 |
  | 有形式变但受现实限制 | 43 |
  | **状态只换色（无形变机会）** | **99** |
- 43 个「有形式变但没做」的四类原因（已写进计划文档）:
  1. **浮层入场编排在冻结的 `motion.ts`**（26 个）：Dropdown / Popover / Tooltip / Popconfirm / HelpTip / AutoComplete / Cascader / 日期时间族 / Mention / TreeSelect / OverflowList + 冻结的 CommandPalette / Drawer / HoverCard / Modal / Select。要做必须先给 `overlayEnter` 开缝隙或本地重写。
  2. **选中态没有「标记元素」，只有行高亮**（8 个）：Anchor / Calendar / ImagePreviewGroup / StyledScrollbar / TickRing / Sidebar 等。要做得先新增标记元素，属重新设计。
  3. **图标挂载即存在 / 无收拢载体**（5 个）：Alert / Notification / Result / LinkText / GeneratorPipeline。加入场动效会让一屏提示条同时晃。
  4. **增删宿主冻结或只是换图**（4 个）：Image / ImagePreview / ImagePreviewGroup / Topbar，以及 Upload（进度条 `v-if` 卸载）。
- 本轮新增: `MenuNode` 子菜单展开 24ms 错位（实测 `opacity 0 → 0.86 → 0.98 → 1`），与 `Tree` 同一套语式。
- 验证: `vue-tsc rc=0`；`DEMO_HEALTH` 双主题 101 页 763 卡零命中；`MOTION_LANGUAGE: PASS`；`FIDELITY: PASS (274 local)`。
- 交接点: 无阻断。形变已到自然边界——再做要么改冻结的 `motion.ts`（浮层入场），要么给组件新增标记元素（重新设计），二者都不属于「补动效」。

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
