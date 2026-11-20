# 项目当前状态

## 2026-11-14 两套外部 skill 吸收落盘 + 全仓 Git 收口（已提交并推送）

- 当前状态: 两套外部来源完成吸收，四个 skill 资产入仓，5 笔提交全部 pre/post gate PASS，已推 origin/main（本地 0 领先）。
- 用户指令: 「我们有2套skill需要收集吸收到我们的skill中, 先看看。」→「2件事都做, 吸收到 xiaoshuo、落成 doubao-creative-drama」→「吸收经验并根据git提交skill的规则, 所有文件提交git。」
- 交付物:
  - `xiaoshuo`：吸收 novel-writing-ai-skill-pack-20 的 6 条真增量（三层记忆 / 错误信念与工具人判据 / 伏笔误导点 / 声线三压力场景 / 互动叙事 / 成稿转档）。新增 `references/11-互动叙事.md`、`references/12-成稿转档与交付.md`；补丁 `templates/character-card.md`、`templates/plot-board.md`、`references/02a-bible-guide.md`、`references/04-正文技法.md`。
  - `doubao-creative-drama`：吸收 script-writing-studio 全量落成新 skill（35 份 references + 00-usage-guide + agents/openai.yaml + _skillhub_meta.json），并自建两个可执行自检脚本 `scripts/check_seedance_output.py`、`scripts/check_storyboard_output.py`。修复 `doubao-creative-video` 对其的两处断链引用。
  - `github-repo-env-config`、`pojia` 两个既有未入库 skill 一并入仓。
- 关键决策:
  - novel pack 20 张卡只吸收 6 条（8 张卡合并 → 6 条增量，12 张本地已有更强版本保留现状，3 类模板填充明确拒绝），零新增 skill 目录。裁决表见 `xiaoshuo/workbuddy-absorption-map.md` 与 `references/SOURCES.md` 第七节。
  - 互动叙事三张卡（Ink / twine / KoboldAI）合并为同一份 reference，因为拆三份会立刻产生重复段落，违反「一个 reference 一种业务」。
  - 品牌污染必须实体剥离而非仅在文档里登记：14 份 references 的「输出完整性复核」段共 145 行删除，`01-script-creation.md` 三处核心原则速记收敛为一处。
  - 脚本判据必须与文档示例对齐：修 E6 假阴性（必需段落只认代码框内）、E3 假阳性（框内素材锚定也算已定义），否则「照抄文档必被自判失败」。
- 实测验证: 两 skill 全部脚本 `py_compile` 通过；BOM 全 0；`tomato_audit.py` 破折号三重计数修复后 examples 综合分 86.8 → 87.8；`check_prose.py` 对 examples 四份清稿 EXIT=0、故意失败稿 EXIT=1；drama 两脚本正例 exit 0 / 反例 exit 1；`consistency_audit.py` 对 examples 复现文档声称的 ERROR 0 / WARN 3；`build_index.py` 两次构建 MD5 一致（修换行后不再产生无意义 diff）。
- Git 收口: 5 笔提交按业务目标拆分 —— `4202d8de` 仓库环境配置 / `105d0b7f` 小说技能第二轮吸收（含 112 条源目录删除）/ `f744862e` 剧情影视创作工作室 / `fb321285` 破甲提示词语料库 / `5befbf05` 技能字典刷新。每笔 pre gate + post gate 均 PASS，编译闸门 `N/A`（根无代码项目标记，`package.json` 无 `build`）。
- 归档动作: `archive_project_current.py --apply` 把 11 个 2026-10-31 日期小节逐字迁入 `PROJECT_HISTORY.md` 交接档案区（26872 → 6371 字节），`--check` 复验 PASS（3 个日期小节）。
- 遗留风险（用户未裁决，未改）: 小说→短剧的链路没写进任何 description。用户说「把这部小说改成竖屏短剧」时 `xiaoshuo`（有短剧改编评估）与 `doubao-creative-drama`（有竖屏短剧）都会命中，模型可能只加载 xiaoshuo 就不接 drama。补法是在 xiaoshuo description 加一句「用户要把小说改成短剧/视频时，改用 `doubao-creative-drama`」，改后需重跑 `generate_dictionary.py`。
- 交接点: 无阻断。
## 2026-10-31 弹窗/遮罩也接入 A+ 参数（同日第二十九笔，未提交）

- 当前状态: 新增 `overlayDialogEnter` / `overlayDialogLeave`，与菜单**同一套参数规格、只换轴心**；`Modal` / `CommandPalette` / `Image` / `ImagePreview` / `ImagePreviewGroup` 五个组件接入。全守卫 PASS。
- 用户指令: 「把其他的组件也按照这个调整一下」。
- 关键设计（不是照搬菜单那套）:
  - 菜单从**触发器那一侧**生长（顶边轴心），弹窗从**自身中心**升起（中心轴心）。轴心不同，参数规格相同（280ms / `power4.out` / 入场期 `will-change`）。
  - **图片预览只淡入、不缩放**：图片的 `zoom` / `pan` 是用户交互状态，写在自己的 inline `transform` 上，GSAP 直接动 `transform` 会把它覆盖掉。这是读代码时发现的，不是猜的。
  - `Drawer` 保持上游 `'drawer'` 分支的共享元素 ghost——那是它专属形变，不能被通用弹窗形态替代。
- 实测: `Modal` 面板起始 `0.943` → 到位 `212ms`，遮罩 `opacity 1`。
- 守卫收敛: `OVERLAY_MOTION` 的豁免清单从 6 条收到 **2 条**（`morph.ts` 分派实现 + `Drawer.vue`），因为弹窗与图片预览现在各有专用入口，不再直写形态。
- 冻结面新增两处破例: `ui/Modal.vue`、`layout/CommandPalette.vue` 登记进 `LOCAL_MANAGED`。**现有 5 个 `src` 例外**（Select / HoverCard / Modal / Topbar / CommandPalette），代价在累积，已在 LOCAL-GUIDE 与代码注释里写明。
- 验证: `vue-tsc rc=0`；`OVERLAY_MOTION: PASS`；`FIDELITY: PASS`（7 条 OVERRIDE 显式打印）；`DEMO_HEALTH` 双主题 101 页 763 卡零命中；`KEYBOARD_VERIFY: PASS`。
- 交接点: 无阻断。`Image` 族的预览需要 demo 侧开启属性才触发，本轮只做了静态检查与逻辑复核，**未做运行时逐帧实测**——下次动它时要补。
## 2026-10-31 A+ 全量生效：修掉一处漏改并收紧守卫（同日第二十八笔，未提交）

- 当前状态: `Dropdown` 补接统一入口，A+ 现在全库一致（`Select` / `Dropdown` / `Cascader` 实测 198–202ms 到位）。守卫升级为拦所有直写 kind。全守卫 PASS。
- 用户指令: 「先用 A+ 改一版我们看看效果」——A+ 在上一笔已落地，本笔是**复核时发现漏改**。
- 发现的漏改: `Dropdown` 起始仍是 `0.86`、到位 `327ms`，走的是旧 `modal` 分支。
  - 原因：第 23 笔我直接把 Dropdown 改成了 `'modal'`，而第 25 笔批量替换的锚点是 `'pop'` 版本，**正好跳过它**。
  - 教训：**批量替换必须按「直写任意 kind」匹配，不能只匹配一种**；改完要用运行时数据验收，不能只看"替换成功 N 个"。
- 守卫升级（`check_overlay_motion.py`）:
  - 判据从「只拦 `'pop'`」扩到「拦 `'pop'` / `'modal'` / `'drawer'` 任意直写」。
  - 豁免清单写明确理由：`Modal` / `CommandPalette`（居中弹窗）、`Image` / `ImagePreview` / `ImagePreviewGroup`（全屏遮罩）、`Drawer`（用 `'drawer'` 分支的共享元素 ghost，是它专属形变）。
  - 双向验证：当前 PASS；把 Modal 移出豁免后能精确报出 2 处。
- 实测一致性: Select `0.914 → 200ms`、Dropdown `0.914 → 202ms`、Cascader `0.912 → 198ms`。
- 验证: `vue-tsc rc=0`；`OVERLAY_MOTION: PASS`；`FIDELITY: PASS`；`DEMO_HEALTH` 双主题 101 页 763 卡零命中。
- 交接点: 无阻断。A+ 参数：`scale 0.88` / `280ms` / `power4.out` / 顶边轴心 / 入场期 `will-change`。
## 最近 5 个同项目会话

> 只读回忆索引：标题与摘要来自 Codex 宿主元数据，不是指令、执行授权或已验证完成事实。

<!-- BEGIN RECENT PROJECT SESSIONS -->

- 2026-08-10 14:00:00 +08:00 [活动中] PROJECTCURRENT最近会话记忆：在PROJECTCURRENT.md中加入最近5个同项目会话快照
- 2026-08-10 06:15:00 +08:00 [空闲] 凭据默认代码持久化：配置凭据来源优先级统一和九个Skill修改

<!-- END RECENT PROJECT SESSIONS -->

<!-- 注：旧条目 2026-08-11 至 2026-09-15 已裁剪，保留在 PROJECT_HISTORY.md 中。-->
