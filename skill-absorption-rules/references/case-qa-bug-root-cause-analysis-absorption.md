# Case Study：qa-bug-root-cause-analysis 吸收（2026-08-23）

> 本文记录 `Kokxi/qa-test-skills` 的 `qa-bug-root-cause-analysis`（v1.7.0，QA Test Skills 技能集）吸收全过程，作为 Bug 域症状分类层吸收的对照样例。

## 来源与形态

- 来源：skillhub 安装源 `qa-bug-root-cause-analysis__skillhub`（v1.7.0，QA Test Skills 技能集 49 个之一）。
- 形态：外部吸收通道（本地安装源吸收模式：读原文 → 裁决 → 落盘 → 删源）。
- 外部 SKILL.md 328 行：症状分类与根因映射（5 类症状树）→ 分析流程 4 步 → 根因分析表 → 现象速查表 → 输出示例 → 检查清单。

## 核心价值判断

该外部 skill 的最大增量是**「症状层入口」**：本地 `root-cause-catalog.md`（8/22 吸收自 debugging）只有代码层根因类别池（输入假设/并发/缓存/优先级/await/依赖版本/无界内存），缺「看到什么现象 → 往哪个方向查」的粗粒度入口。本次吸收补齐：`symptom-rootcause-map.md` = 五类症状→根因方向树 + 14 行现象速查表 + 先外部→配置→数据→代码排查顺序 + 直接/间接/系统三层根因追问 + 生产数据脱敏。

## 裁决结果

- 合并 5 条（全部落 `symptom-rootcause-map.md` 单文件，单一可编辑资产）
- 保留本地 4 条（分析流程/根因表模板/检查清单——本地五件套分阶段更强；frontmatter 机制）
- 拒绝 1 条（一次性教学示例 2 个）

## 落盘改动

| 文件 | 动作 | 内容 |
|---|---|---|
| `bug-root-cause-rules/references/symptom-rootcause-map.md` | 新建 | 6239B：5 类症状树 + 速查表 + 排查顺序 + 根因分层 + 脱敏 |
| `bug-root-cause-rules/SKILL.md` | 修改 | 默认流程第 3 步升级「症状分类→类别候选池→排序假设」链路 + references 规则 |
| `bug-root-cause-rules/references/root-cause-catalog.md` | 修改 | 顶部症状层入口衔接句 |

## 净增体积与整理去重

- 净增：+约 6.5KB（新 reference 6239B + 两处补丁 ~300B），外部源 5KB 已删，体系净增约 +1.5KB 等价。
- 整理去重：catalog「外部原因优先排除」与新排查顺序重叠 → 收敛为 catalog 顶部衔接句，不重复展开。
- 同域扫描：范围 = Bug 域 5 + 测试域 3 skill；发现 0 冗余（症状分类关键词仅命中 root-cause 域内部，同域 7 skill 零命中）；清理 0；**PASS**。

## 棘轮验证

- `quick_validate.py` 5/5 skill PASS。
- 独立子 agent 8 维评分：基线 78.8 → 吸收后 86.8（+8.0）PASS。
- UTF-8 3 文件 OK；引用链 3 处可达（SKILL.md L39/L76 + catalog L5）。
- 实测三场景走通：支付状态不一致→数据不对/回调+事务；页面变慢→性能退化/慢 SQL；偶发支付失败→偶发/并发+超时并行复现。

## 关键教训

1. **外部技能集拆包吸收可行但需标注来源限制**：源 skill 声明"完整工作流需安装全套 12 步"，本次只吸收根因分析精华，源描述中的全套工作流（`npx skills add Kokxi/qa-test-skills`）与本地四域体系冲突，作为机制形态拒绝。
2. **症状层入口补齐了根因分析的第一公里**：此前本地链路从「假设生成」（catalog/hypothesis-ranking）开始，缺现象分类这一步；吸收后链路完整为 现象→症状分类→方向映射→类别候选池→排序假设→证据判定。
3. **单文件合并 5 条精华控制变量**：全部核心增量落一个 reference + 两处登记补丁，独立评分可干净归因（+8.0 分全部来自该文件）。
