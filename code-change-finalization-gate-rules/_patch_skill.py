import re

with open(r'D:\谷歌云盘\luode-skills\code-change-finalization-gate-rules\SKILL.md', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update description
content = content.replace('负责校验注释链', '负责 OCR 代码审查（基于阿里巴巴 Open Code Review 规则）、注释链校验')

# 2. Add OCR entry under Skill 作用与适用场景
old2 = '## Skill 作用与适用场景\n\n- 代码或测试新增/修改后，在最终回复前自动触发并核验专项收口。'
new2 = old2 + '\n- 每次收口时自动触发 OCR 代码审查：读取 `references/ocr-review/review-workflow.md`，按 `rule-path-map.md` 匹配文件类型，加载对应 `rule_docs/` 规则进行行级审查。Critical 级别问题阻断收口。'
content = content.replace(old2, new2)

# 3. Add OCR step after step 2 in default workflow
old3 = '2. 执行测试目录一致性检查；涉及 `internal/router` 时执行 router 专项检查。\n3. 涉及生产代码改动时'
new3 = '2. 执行测试目录一致性检查；涉及 `internal/router` 时执行 router 专项检查。\n2.5 **OCR 代码审查**：读取 `references/ocr-review/review-workflow.md`，对本次改动运行自动审查。依次执行：\n   - 获取改动文件列表 → 查 `rule-path-map.md` 匹配规则 → 加载对应 `rule_docs/` 规则 → 逐文件行级审查 → 输出 `OCR 审查:PASS/ISSUES`\n3. 涉及生产代码改动时'
content = content.replace(old3, new3)

# 4. Add OCR blocking condition
old4 = '属于阻断级：\n\n- Go 测试资产'
new4 = '属于阻断级：\n\n- **OCR 审查发现 Critical 级别问题且未修复** → 阻断级（除非用户明确要求不修复）。High/Medium 级别为非阻断级，在最终回复中提示。\n- Go 测试资产'
content = content.replace(old4, new4)

# 5. Add OCR reference reading
old5 = '不再维护本 skill 私有的 next-step 模板。'
new5 = old5 + '\n- OCR 审查工作流统一读取 `references/ocr-review/review-workflow.md`，路径映射读取 `references/ocr-review/rule-path-map.md`，各语言规则读取 `references/ocr-review/rule_docs/{语言}.md`。\n- OCR 相关的 `rule_docs/` 文件是阿里巴巴 Open Code Review 项目的翻译版吸收。如需更新，从 `https://github.com/alibaba/open-code-review` 同步。'
content = content.replace(old5, new5)

# 6. Add OCR output
old6 = '本 skill 不复制。'
new6 = old6 + '\n- OCR 审查结果按 `OCR 审查:CRITICAL/ISSUES/PASS` 标记，Critical 问题清单随阻断证据输出，High/Medium 作为提示信息。'
content = content.replace(old6, new6)

with open(r'D:\谷歌云盘\luode-skills\code-change-finalization-gate-rules\SKILL.md', 'w', encoding='utf-8') as f:
    f.write(content)

print('SKILL.md updated successfully')
