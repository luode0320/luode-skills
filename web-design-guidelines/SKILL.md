---
name: web-design-guidelines
description: 用于审查 UI 代码是否符合 Web Interface Guidelines。适用于“帮我审查 UI”“检查可访问性”“设计审计”“UX 评审”“按最佳实践检查网站”等请求。
metadata:
  author: vercel
  version: "1.0.0"
  argument-hint: <file-or-pattern>
---

# Web 界面规范审查

用于检查目标文件是否符合 Web Interface Guidelines。

## 工作方式

1. 从下方源地址拉取最新规范
2. 读取指定文件（若未提供则向用户询问文件或匹配模式）
3. 按拉取到的完整规则逐条审查
4. 以精简的 `file:line` 格式输出问题

## 规范来源

每次审查前都要拉取最新规则：

```
https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md
```

使用 WebFetch 获取最新规则。返回内容包含完整规则与输出格式要求。

## 使用方式

当用户提供文件路径或匹配模式时：
1. 从上述地址拉取最新规范
2. 读取目标文件
3. 应用拉取到的全部规则
4. 按规范要求的格式输出审查结果

如果用户未提供文件，先询问要审查哪些文件。
