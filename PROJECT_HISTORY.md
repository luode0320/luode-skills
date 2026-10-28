# 项目历史事件

> 本文件追加关键历史事件并只保留最近 20 条（按日期倒序、新事件置顶、追加后自动裁剪）；普通启动默认不读取，只有历史追问、当前状态不足或真实卡点时才窄检索。

## 事件
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
- 2026-10-15：**Arco 品类对齐补齐 57 个组件，组件总数 69 → 126（用户 Goal 主体交付）**。用户 Goal 要求对标 `arco.design/vue` 的组件品类广度、用现有珍珠玻璃样式与 GSAP 动效「继续补充完善，不要遗漏」。做法：① 品类真相源改为可核验数据——`npm pack @arco-design/web-vue@2.58.0` 取 `es/` 目录清单（网页为 SPA，WebFetch 只能拿到分析脚本），落盘 `references/arco-parity.json` 共 74 品类（display 22 / feedback 12 / inputs 22 / layout 8 / navigation 10；初录 75 后剔除误录的 `segmented`——Arco Vue 2.58.0 的 `es/` 与 `es/index.js` 均无该组件，是 Ant Design 的品类）；② 新增 `scripts/check_arco_parity.py` 三重校验守卫（`STALE_GAP` 标 gap 却已实现 / `DANGLING` 标 covered 但文件缺失 / `COVERAGE_GAP` 未清零，另以 `references/arco-categories.json` 真实品类参照对账报 `PHANTOM_CATEGORY` 虚构条目与 `MISSING_CATEGORY` 漏登品类，两个方向均做变异自测），把「不要遗漏」变成机器可判定契约；③ 新增本地扩展层 `src/components/extend/` 共 57 个组件，因上游冻结面含全部七层样式与 `src/main.ts`，extend 一律自带 `<style scoped>` 且只引用 `tokens.css` 令牌、材质复用 `.m-*`、动效复用 `composables/motion.ts`；④ 并行 6 个 background subagent 按不重叠写集实现（display/feedback/inputs/layout/navigation 分组），主 agent 统一收口类型检查与守卫。真实缺陷修复：`Trigger` 动态方法名调用 `addEventListener` 使 TS 重载失配、`Popover` 模板 ref 与 setup 变量重名、`BackTop` 联合类型收窄失败、`Typography` 的 `delete` 保留字不能进模板表达式、`Upload` 局部函数遮蔽同名 prop、`Cascader` 自引用变量缺注解、`MenuNode` 缺必填 props 在核对页崩溃、`CollapseItem` 独立挂载时 `inject` 无兜底告警。验证：核对页浏览器实测 126/126 全部正常渲染、0 渲染异常、0 控制台告警；`PARITY: PASS (74 品类)`、`INVENTORY: PASS (123)`、`FIDELITY: PASS (215/139)`、`GUARD_SELFTEST: PASS`、`CATALOG: PASS (126)`、`POLLUTION: PASS`、单测 21/21、`vue-tsc + vite build` 成功。工作树未提交（无当轮 Git 授权）。

## 计数锚点区

> 本区由 `memory-usage-tracking-rules` 收口闸门维护：仅"实际引用"条目时 +1（用于决策/输出/代码）；同会话同条目只 +1；`usage_days` 当天首次引用时 +1。HISTORY 锚点 key 使用事件主题短语（可前缀匹配）；事件被裁剪时锚点随事件一起删除。

```yaml
version: 1
anchors:
  - title: "自举脚本恢复「提交即推送」按仓库归属注入"
    usage_count: 0
    usage_days: 0
    last_used_at: null
    absorbed_to: null
  - title: "imagegen 模型清单收敛为唯一 gpt-image-2"
    usage_count: 0
    usage_days: 0
    last_used_at: null
    absorbed_to: null
  - title: "前端视觉改动对比 Demo 规则吸收并全量提交收口（Git 收口）"
    usage_count: 0
    usage_days: 0
    last_used_at: null
    absorbed_to: null
  - title: "索引漂移识别与全量提交收口（Git 收口）"
    usage_count: 0
    usage_days: 0
    last_used_at: null
    absorbed_to: null
  - title: "规则吸收与全量提交收口（Git 收口）"
    usage_count: 0
    usage_days: 0
    last_used_at: null
    absorbed_to: null
  - title: "组件示例全量遍历排查与事件接线守卫（Goal 收口）"
    usage_count: 0
    usage_days: 0
    last_used_at: null
    absorbed_to: null
  - title: "组件库文字清晰度修复（需求收口）"
    usage_count: 0
    usage_days: 0
    last_used_at: null
    absorbed_to: null
  - title: "组件示例文字提示与逐格说明（需求收口）"
    usage_count: 0
    usage_days: 0
    last_used_at: null
    absorbed_to: null
  - title: "组件示例卡不可见与出卡修复、示例可见性守卫（Goal 收口）"
    usage_count: 0
    usage_days: 0
    last_used_at: null
    absorbed_to: null
  - title: "菜单选项文字贴边修复与内容留白守卫判据升级（Bug 收口）"
    usage_count: 0
    usage_days: 0
    last_used_at: null
    absorbed_to: null
  - title: "Panel 内容贴边修复与内容留白守卫（Bug 收口）"
    usage_count: 0
    usage_days: 0
    last_used_at: null
    absorbed_to: null
  - title: "组件库双击启动脚本（收口）"
    usage_count: 0
    usage_days: 0
    last_used_at: null
    absorbed_to: null
  - title: "图标式气泡帮助组件 HelpTip（需求收口）"
    usage_count: 0
    usage_days: 0
    last_used_at: null
    absorbed_to: null
  - title: "组件边角方角缺口修复与边角一致性守卫（Goal 收口）"
    usage_count: 0
    usage_days: 0
    last_used_at: null
    absorbed_to: null
  - title: "组件菜单单一概念拆分、示例页三列大卡与示例扩容（Goal 收口）"
    usage_count: 0
    usage_days: 0
    last_used_at: null
    absorbed_to: null
  - title: "组件示例边角阴影块修复与投影留白守卫（用户 Goal 收口）"
    usage_count: 0
    usage_days: 0
    last_used_at: null
    absorbed_to: null
  - title: "组件库菜单二级化 + 一组件多示例可用性收口（用户 Goal 收口）"
    usage_count: 0
    usage_days: 0
    last_used_at: null
    absorbed_to: null
  - title: "组件库后台化收口（用户 Goal）"
    usage_count: 0
    usage_days: 0
    last_used_at: null
    absorbed_to: null
  - title: "Arco 组件粒度对齐补齐 21 个组件，组件总数 126 → 147（用户 Goal 收口）"
    usage_count: 0
    usage_days: 0
    last_used_at: null
    absorbed_to: null
  - title: "Arco 品类对齐补齐 57 个组件，组件总数 69 → 126（用户 Goal 主体交付）"
    usage_count: 0
    usage_days: 0
    last_used_at: null
    absorbed_to: null
```
