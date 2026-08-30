# Case：吸收 `comprehensive-test-case-writer`（一源落两 skill）

> 吸收时间：2026-08-30｜通道：外部吸收（本地安装源 `functional-use-cases__skillhub`）｜目标 skill：`test-strategy-rules`（主）+ `apifox-cli__skillhub`（辅）
> 供下次吸收对照的典型性：**外部 skill 与本地已有能力高度重叠，主落点本地空白、辅落点本地更强**的裁决与"持平判定"。

## 一、这次踩到的判断点

1. **用户说的"测试 skill"不是一个 skill，是一个域**。用户原话"吸收到测试和 apifox 测试的 skill 中"，本地测试域有 5 个 skill（`test-strategy-rules` / `test-program-rules` / `test-regression-rules` / `functional-validation-rules` / `bug-validation-rules`）+ apifox。落点不能猜，必须先侦察再问。**侦察结论直接决定裁决表质量**：这次靠一轮 grep 就确认"测试域零黑盒方法、零质量维度定义"，而 apifox 侧已由 `test-case-from-requirement.md`（吸收自 skillmd test-cases）完全覆盖。

2. **同一个外部源，两个落点的裁决结果完全相反**。test-strategy-rules 侧 9 条中合并 6 条；apifox 侧 6 条中合并 1 条、拒绝 1 条、保留 4 条。**不要因为"用户点名了两个 skill"就在两侧平均用力**——平均用力必然导致强势侧被灌水、两套模板并存。

3. **本地已吸收过同源能力时，先查 absorption-map 再裁决**。apifox 的 `workbuddy-absorption-map.md` 里已记录 8/19 吸收 `api-test-automation-pro` 的 16 条裁决，其中第 10 条就是"自然语言→用例、测试点分析、6 大用例矩阵 → 已吸收"。**没有这一步，会把外部源当成新东西重复吸收一遍**。

## 二、裁决要点（可复用判据）

| 判据 | 应用 |
|------|------|
| 本地更强 → 保留本地，哪怕外部写得更"全" | 外部 7 字段模板 + P0-P3 vs 本地 12 字段 + 风险导向 P0-P2：拒绝外部，理由是**两套模板/两套优先级比少一个字段更贵** |
| 本地空白 → 合并，但只补方法定义不复制落地细节 | 黑盒五法只写"适用信号/取值要点/用例下限"，接口级落地统一指向 apifox 模块 |
| 领域专项（游戏）→ 条件化 + 去垂直品牌 | 去掉原神/星铁/米哈游语境，保留玩法/数值/联机/付费/本地化/更新兼容通用方法 |
| 新增门控与既有清单重叠 → 必须写分工声明 | 新增"四性"与 apifox Step 5 的 11 项覆盖验证层叠 → 加一句"接口级以 Step 5 为准，四性只做非接口场景与跨维度总判" |
| description 触发词必须覆盖 reference 里的条件化小节 | 第一版漏了"游戏"，实测"游戏抽卡保底怎么测"命中为空 → 补触发词后 6/6 通过 |

## 三、可复用的收口检查

写完不要只查编码和 frontmatter，**跑一遍"场景 prompt 命中 description 触发词"的轻量实测**：把 reference 里每个小节的代表性关键词拿出来，模拟用户 prompt 看是否命中。这次靠它抓到游戏专项触发不到的问题（脚本见收口说明中的 6 例）。

引用链要按**正文**查，不能只解析 frontmatter description：下游 skill 的引用通常写在 references 读取规则里，只查 description 会误判 FAIL。

## 四、净增与整理

- 新增：reference 1 个（9.4 KB）+ `test-strategy-rules/SKILL.md` +约 1.1 KB（含 description 触发词）+ `functional-validation-rules/SKILL.md` +0.6 KB + apifox 模块 +1.3 KB + 登记文件 3 个。
- 整理：`test-strategy-rules/SKILL.md` 末尾孤行归位；`functional-validation-rules/SKILL.md` "测试主文档、测试主文档"重复词去重；权威声明由"4 个 skill 直接引用"（引用链不可达）改为"统一以本节为准"。
- 同域扫描：6 个 skill 范围，发现 2 处（门控层叠风险 1、空引用声明 1），闭环内清理 2 处，PASS。

## 五、源处置（已闭环，2026-08-30 14:22）

- **删除前引用扫描**：`functional-use-cases` / `comprehensive-test-case-writer` 在 skills 目录中仅出现在登记文件、case study、reference 来源声明与工作日志（均为**来源记录性质的文本提及**，非路径依赖）；`inventory.yaml`、`_bm_skillid_migration.json`、`字典.md`、`README.md`、`index.html`、`skills拆分.md` 六份索引文件命中数均为 0 → 删除不会造成断链。
- **执行**：先 `cp -r` 备份到 `C:\Users\luode\.workbuddy\skill-archive\functional-use-cases__skillhub_20260830`（4 文件 / 15,287 字节），校验备份完整后再 `Remove-Item` 删除源目录。
- **环境坑（下次直接照做）**：本环境 PowerShell 安全策略**禁止 `Add-Type` 编译 .NET、禁止 COM 对象实例化**，因此 `Microsoft.VisualBasic.FileIO.FileSystem::DeleteDirectory(..., SendToRecycleBin)` 与 `Shell.Application.NameSpace(10).MoveHere()` 两条回收站路径**均不可用**；源 skill 删除只能走 `Remove-Item`，故**「先备份 + 校验备份完整再删」是强制前置**，不能省。
- **改进点**：下次吸收应在裁决表里就把"源删除时点 + 备份落点"写死，避免源与新落点并存期间的重复命中（本次并存约 11 小时）。
