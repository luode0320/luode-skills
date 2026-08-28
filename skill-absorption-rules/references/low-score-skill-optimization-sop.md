# 低分 skill 优化 SOP（low-score-skill-optimization-sop）

> 归属 owner：`skill-absorption-rules`。与 `score-inspection-workflow.md` 构成「巡检 → 优化 → 复评」完整闭环：巡检负责「批量打分发报告、识别短板」，本 SOP 负责「拿到低分名单后怎么逐 skill 优化」。
> 评分标准本身见 `darwin-rubric.md`（本文件不重复维度定义与计分公式）。
> 八轮实操验证（2026-08-25~26，7 个低分 skill：wsl-powershell 24.7→62.6 / z-data-crypto 26.9→63.6 / wsl-path-converter 27.4→68.9 / wsl-chrome-cdp 29.4→67.4 / vue-router-best-practices 30.9→66.6 / shell__skillhub 31.0→69.0 / vue-component-generator__skillhub 33.4→63.8，提升 +30.4 ~ +41.5）。

## 触发信号

- 评分巡检（`score-inspection-workflow.md`）产出自有类（`rules` / `other`）低分 skill。
- 用户点名："优化这个 skill（评分 XX 分）""继续优化低分 skill"。
- 用户说"按这个流程优化下一个低分 skill"。

## 八步闭环（串行，每步有退出点）

| 步 | 动作 | 关键产出 | 退出点 |
|---|---|---|---|
| 0 | 命中检查（skill-hit-check-rules） | 首条固定字段 + 闸门预告登记 | 字段不全不进入领域动作 |
| 1 | 基线核验 | 评分报告实锤 + 全资产读取（SKILL.md/脚本/references/meta）+ quick_validate 实测 | — |
| 2 | 市场检索 | 2-7 组关键词 × 每批 10 条；用户授权「安装验证后删除」时执行 | 0 候选是常态，直接进 3 |
| 3 | 本地能力对照 | 同域 skill 扫描 + 职责边界判定（互补/重叠/可交叉引用） | — |
| 4 | 三态裁决表 → 用户确认 | A 内容 / B 交叉引用 / C 市场吸收 / D 版本环境 分组 | 未确认不落盘 |
| 5 | 落盘 | 单一可编辑资产 + frontmatter 合规 + 环境自检 + 净增减预估 | — |
| 6 | 机器校验 | `quick_validate.py` → `Skill is valid!` + 引用链可达 | 不过则修复重验 |
| 7 | 独立复评 | 独立子代理 7 维打分（固定输出格式）+ 维度 8 本机实测 | — |
| 8 | 闭环修复 + 收口 | 本侧修正 + 复验 + 同域扫描 + 沉淀登记 | — |

## 短板类型学（诊断 → 修复模式，9 类）

| 短板（评分视角） | 实锤手法 | 修复模式 |
|---|---|---|
| 无 frontmatter / 违规键 | `quick_validate` 实测违规清单 | 合规化：顶层仅 `name`（hyphen-case）/`description`/`license`/`metadata`（+`allowed-tools`）；中文显示名收 `metadata.displayName`；description 带触发词、禁尖括号 |
| 内容有、路由无（reference/脚本充实，SKILL.md 是壳） | 全资产读取对照 | 把 reference/脚本消化成决策路由 + 内联速查（"问题-修复"对），决策表分级可从 reference frontmatter 机器提取 |
| 内容太薄无流程 | 行数 + 结构检查 | 补 4 步工作流（识别场景→查速查/选参数→执行→验收），每步带输入/输出 |
| 混入无关内容（变现/宣传） | 语义检查 | 直接删除 |
| 宣称与实现不符（列选项脚本不解析） | 逐参数实测（`--api/--typescript/--scss` 传了等于没传） | 脚本兑现宣称（能力矩阵逐项对齐实测），不收缩宣称 |
| 隐性失实（依赖未装 / 数据源不可达，宣称"开箱即用/无 key"） | 依赖 import 实测 + 数据源真实调用（DNS→私有网段 + TLS 失败 = 域名级不可达判据） | 去框架依赖 + 数据源诚实声明 + `--check` 探测命令（降级文案声明为预期行为），不换源重写 |
| 依赖远程规范 / 外部仓库（拉取失败或未安装则整体不可用） | WebFetch 实测拉取 + 本机路径/import 检查（openclaw-quant 未装、vercel 规范可拉取均为实锤） | 本地兜底（规范快照落盘 `local-*.md` 双通道）+ 前置检查步骤 + 显式降级路径（未安装时转咨询模式，不伪造远程能力）+ 删宣传性冗余（Roadmap/Cost/Support） |
| 脚本断链（声明不存在 / 裸相对路径） | 实测执行 | 脚本内置 `SCRIPT_DIR` 自定位 + 双调用方式（cd 相对 / 任意 cwd 绝对），不是删声明 |
| 内容空洞未接数据源 | 执行输出检查 | 接真实数据源（引用不复制防漂移） |

## 市场检索规律（防重复浪费）

- 八轮累计 28+ 组关键词 0 个有效候选（命中多为科研/视频/电商等无关项）。
- 低分 skill 的解药多数在仓库内部：同域 `rules` skill、官方内置命令（如 `wslpath`）、成熟 reference。
- 用户授权「安装验证后删除」无对象可执行是常态，直接记录结论进入下一步，不反复检索。

## 验证纪律（复评侧）

- 独立子代理 7 维（禁止"自己改自己评"）+ 固定输出格式：`<skill>|<D1>|<D2>|<D3>|<D4>|<D5>|<D6>|<D7>|<总分>|<短板一句话>`。
- 维度 8 本机实测三类场景：正常 / 边界 / 失败路径（失败路径验证"不编造结果"红线）。
- 机器核对：决策表分级 vs reference frontmatter 逐项一致（可获维度 8 一致性证据）。
- 棘轮：新分严格高于基线才保留；涨幅 <1 分自动早停。
- 闭环修复「本侧修正」原则：不实声明在谁侧引入就改谁侧表述，不跨 skill 修改成熟资产。
- 断言笔误要区分「测试脚本错误 vs 产物 bug」：先复现产物再下结论（实测曾把测试断言期望值误写为 `handleClose`，产物实为 `handleClick`，断言失败是测试脚本错误非产物 bug）。
- 复评发现的确定性小问题（断链 / 表述精化 / 格式瑕疵）在同轮顺手修复 + quick_validate 复验（实测两例：z-data-crypto 轮 frontmatter `icon` 断链修复、wsl-path-converter 轮 UNC 行为表述从单一输出精化为"两次实测不同"）。

## 已知实操坑

- description 含尖括号（如 `<script setup>`）→ 校验器拒绝（`Description cannot contain angle brackets`），改文字表述。
- `sed -i` 仅 GNU 语法与 macOS 宣称矛盾 → 加平台分支（BSD 用 `sed -i ""`）。
- 连续大写 kebab-case（`MyAPIClient` → `my-api-client` 需先拆连续大写再拆普通边界）。
- Google Drive 同步占用导致并发 Edit 撞 `File has been modified since read` / EBUSY → 重读后重试。
- 多文件并发 Edit 首条易撞锁 → 串行编辑或失败重读重试。
- 从 Bash 调 PowerShell 可能被安全策略拦截 → 拆分为 bash 转义验证 + PowerShell 工具命令体验证两组。

## 单轮收口清单

- [ ] `quick_validate` 复验 `Skill is valid!`
- [ ] 同域冗余扫描 4 项（重复段落 / 门控层叠 / 散落产物 / 引用链）PASS
- [ ] 知识库沉淀回读一致 + `knowledge_index.py check` 0 死链
- [ ] 工作日志追加 + 项目记忆三件套更新（PROJECT_HISTORY ≤ 20 条）
- [ ] `source-notes.md` + `workbuddy-absorption-map.md` 登记（含整理去重 / 同域扫描 / 净增体积）
- [ ] 未提交 git（无用户当前轮授权时）

## 与相关文件边界

- `darwin-rubric.md`：评分标准单一权威（维度 / 权重 / 公式），本 SOP 不重复。
- `score-inspection-workflow.md`：全量巡检流程（打分发报告），本 SOP 承接其「自有短板 → 优化」出口。
- `skill-audit-rules`：多 skill 职责重叠审计（只读）；优化中发现的体系级冗余（如"速查 vs 手册"双胞胎 skill）登记其审计建议，不在单轮内强制合并。
