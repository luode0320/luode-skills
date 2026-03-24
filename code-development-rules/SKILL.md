---
name: code-development-rules
description: Enforce the team's code development workflow and coding standards for requirement clarification, ambiguity handling, minimal-change implementation, Chinese comments, semantic naming, constant extraction, error handling, and logging. Use when Codex is asked to generate, modify, refactor, or review code under these custom rules, or when the user asks to follow team-specific coding standards.
---

# 代码开发规则

## 概览

在生成、修改、重构或评审代码前，先按本 skill 约束需求澄清、实现方式和输出质量。
开始实现前先读取 `references/coding-rules.md`。

## 执行流程

### 1. 先澄清再动手

- 提炼业务场景、输入输出、边界条件、技术栈与依赖约束。
- 只要需求、BUG 边界、数据结构、接口契约或文档存在关键不明确项，就暂停执行。
- 使用“待确认项 + 可选方案 + 推荐方案”的方式向用户确认，不直接盲写代码。

### 2. 优先最小化改动

- 优先复用项目已有组件、工具类、服务与约定。
- 优先通过新增代码扩展能力，避免无必要的大范围重构。
- 修改前先识别是否需要抽离常量、枚举、配置、状态码与文案键。

### 3. 按规范实现

- 将核心逻辑拆为单一职责的方法；单个函数通常不超过 50 行。
- 使用语义化命名，避免无意义缩写。
- 新增文件默认使用 UTF-8；注释默认使用中文，重点说明“为什么这样做”。
- 在复杂代码块中使用 `1.`、`2.`、`3.` 这类步骤标记辅助阅读。
- 错误消息默认使用英文；日志优先使用中文，并包含模块、操作、对象或业务上下文。
- 清理未使用变量、导入、空分支、重复判断和明显冗余逻辑。

### 4. 完成后自检

- 核对边界条件、接口契约、错误处理、日志可追溯性、命名和常量抽离情况。
- 若因为信息缺失而做了假设，明确列出假设，不要伪装成已确认事实。
- 若无法在当前信息下安全继续，实现应停在澄清阶段。

## 输出约定

在需要用户确认时，优先使用以下结构：

1. `待确认项`
2. `可选方案`
3. `推荐方案`
4. `确认后实施范围`

## 参考资料

- 详细规则：`references/coding-rules.md`
