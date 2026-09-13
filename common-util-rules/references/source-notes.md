# 来源记录（source-notes）

> 归属 owner：`common-util-rules`。登记本 skill 历次调整的来源与落点，与 `workbuddy-absorption-map.md` 配套。

## 2026-09-11：内部更新——纯转换工具函数落点 + 公共工具索引文档契约

- **调整类型**：内部更新通道。
- **调整诉求**：
  - ① 点名「纯转换工具函数」的落点判据——补齐用户九维清单第 8 维（纯转换工具函数的定义位置），把"可独立复制 → `utils/<pkg>`、需项目依赖 → `common/util`"的二分落到"纯"的硬判据上。
  - ② 补齐用户九维清单第 9 维（工具函数索引文档规范）——此前零基线，现有四层索引全是目录 / 类别级，无函数级索引。
- **触发场景**：用户提出 AI 辅助开发瓶颈已从逻辑正确性转向代码质量，九维清单中第 8、9 维在 `util-placement.md`（26 行）与 `util-qualification.md`（39 行）内均无承接；用户裁决口径为"约定项目内索引契约 + 纯转换单独点名"。
- **落点**：
  - 主定义：`common-util-rules/references/util-index-doc-contract.md`（新建）。
  - 落点判据：`common-util-rules/references/util-placement.md` 新增「纯转换工具函数的落点（点名判据）」小节。
  - 入口引用：`common-util-rules/SKILL.md` 复用红线 +1 条、默认执行流程 +1 步、references 读取规则 +1 条、description 补索引契约。
- **裁决依据**：见 `../workbuddy-absorption-map.md` 2026-09-11 段落。
- **未落盘内容**：无。
- **外部源**：无（内部更新通道）。
