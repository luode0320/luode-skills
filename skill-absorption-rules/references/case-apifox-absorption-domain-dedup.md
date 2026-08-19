# Case Study：api-test-automation-pro 吸收后同域冗余残留与补救（2026-08-19/20）

> 归属 owner：`skill-absorption-rules`。本案例是「吸收后同域去重」条款（2026-08-20 补）的反面教材：棘轮评分通过 ≠ 无冗余残留；目标文件内整理 ≠ 同域去重。

## 一、事件时间线

| 时间 | 事件 |
|---|---|
| 2026-08-19 23:40 | 吸收 `api-test-automation-pro__skillhub`（v1.5.0，约 1 万行 + 18 references）到 apifox + test-strategy 双落点 |
| 2026-08-19 23:40 | 收口：8 维评分 92.1（基线 75.7，+16.4 棘轮通过）；净增 +24,898 字节；test-case-generation.md 压缩 -568 字节 |
| 2026-08-20 | 用户发起测试域复杂度检查 → 发现同域 3 处重复 + 门控层叠 + 散落产物（本次吸收未清理） |
| 2026-08-20 | 执行 P0+P1 收敛去重（6 处改动），冗余清除 |

## 二、残留的冗余（吸收时应发现而未发现）

1. **4 级样本矩阵逐字重复**：test-strategy-rules「写接口样本分布（4 级矩阵）」与 functional-validation-rules「写接口的功能验证样本（4 级矩阵）」几乎逐字相同（`historical_succeeded` / `historical_failed_lifecycle` / `historical_inflight` / `current_listing_available`、N≥5、`UNEXPECTED_FAIL=0`）。
2. **双根落点三处重复**：test-program / test-regression / functional-validation 三份 SKILL.md 各写了一遍几乎相同的「活动资产落点（强制）」（mock 镜像 + doc/5-tests 只留证据），真正权威在 test-strategy 的 test-asset-governance 路由。
3. **apifox 内部模块重叠**：test-case.md（CLI 操作层）与 test-case-generation.md（设计方法论层）Step 3 断言映射表重复。
4. **门控层叠**：apifox SKILL.md 并存「必须询问用户」与「三重门控」两套确认概念。
5. **散落产物**：skills 根目录 `release-test-plan.yaml`（219B 全 0 空模板，无引用）误放。

## 三、为什么吸收闭环没拦住

- 「吸收即整理」（8/19 版）只要求**目标文件内**与新增内容同义的段落整理——本次目标文件是 apifox 模块与 test-strategy，而冗余发生在**同域兄弟 skill**（functional-validation / test-program / test-regression），超出原规则的侦察范围。
- 棘轮评分（92.1）衡量的是吸收目标的质量提升，**不含同域冗余扫描**，因此"高分通过"与"同域冗余残留"可以同时成立。
- 收口说明只报了"净增体积与文件内整理"，未要求报同域扫描结论，冗余无登记、无问责。

## 四、补救动作（2026-08-20，P0+P1 收敛去重）

| 项 | 动作 | 收敛到 |
|---|---|---|
| 样本矩阵 | functional-validation 32 行重复正文 → 引用 + 3 条域专属补充 | test-strategy「测试样本分布优先（强制）」 |
| 双根落点 | 三份 SKILL.md「落点（强制）」→ 引用 | test-strategy-rules/references/test-asset-governance.md |
| apifox 断言映射 | test-case-generation Step 3 断言表 → 引用 | test-case.md「断言速查（16 种映射）」 |
| 门控层叠 | 「必须询问」+「三重门控」→ 合并 | apifox SKILL.md「门控与确认清单」 |
| 散落产物 | 删除 release-test-plan.yaml（Grep 复核无引用） | — |

净减约 5KB 重复正文（未提交，工作树含历史遗留改动）。

## 五、教训（已固化为规则）

1. **同域去重是吸收闭环的强制环节**：落盘后、评分前必须扫描本次吸收触达的同域 skill 集合（重复段落 / 门控层叠 / 散落产物 / 引用链四项），发现即可清理的冗余必须在同一闭环内清理，未清理不得收口。
2. **棘轮评分不能替代同域扫描**：评分看目标质量提升，扫描看体系冗余；两者互补，缺一不可。
3. **目标文件内整理 ≠ 同域去重**：吸收内容投放后与兄弟 skill 的交叉重复，只有圈定同域范围才能发现。
4. **收口说明必须报同域扫描结论**：扫描范围 / 发现 X 处 / 清理 Y 处 / PASS-FAIL，写入裁决表，形成可审计闭环。
