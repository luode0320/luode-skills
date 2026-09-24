# Open Code Review 规则吸收实施计划

## 总目标

将阿里巴巴 Open Code Review 的 50+ 种语言审查规则全部吸收进 `code-change-finalization-gate-rules`，
在每轮代码收口时自动触发行级审查，用户无感知。零额外依赖，复用当前对话模型能力。

## 实施步骤

### Step 1: 编写批量下载脚本
- 从 GitHub API 批量拉取 OCR 所有 `rule_docs/*.md` 文件和 `system_rules.json`
- 保存到本地暂存目录

### Step 2: 翻译并生成所有规则文件
- 每个规则文件翻译为中文，保持原始分类结构
- 写入 `references/ocr-review/rule_docs/`

### Step 3: 创建路径映射文档 rule-path-map.md
- 用中文描述文件扩展名 ↔ 规则文件的映射关系

### Step 4: 创建审查工作流文档 review-workflow.md
- 定义 agent 行级审查的标准步骤

### Step 5: 修改 SKILL.md
- 在收口流程嵌入 OCR 审查步骤
- 更新阻断判定逻辑

### Step 6: 测试验证

## 关键设计决策

| 决策项 | 选择 |
|--------|------|
| Skill 形态 | 嵌入 code-change-finalization-gate-rules |
| 语言范围 | 全部 50+ 语言 |
| 规则语言 | 全部翻译为中文 |
| 审查执行 | 当前 Agent 自行审查 |
| 映射文件 | 中文文档 |
| 独立入口 | 不创建，仅嵌入收口 gate |
| 阻断条件 | Critical 级别问题阻断 |
