---
schema_version: 1
template_version: 1
doc_id: "STYLE-TAPD-CLI-20261123"
doc_type: style_regression
source_ids: ["TASK-TAPD-CLI-ONLY"]
status: accepted
version: "v1.0"
current_slice: "SLICE-TAPD-CLI-ONLY"
updated_at: "2026-11-23 15:49:57"
reader_level: business_general
writing_style: plain_chinese
appendix_policy: preserve_existing_or_one_terminal_appendix
---

# TAPD 强制 CLI 去浏览器 6-review

结论：TAPD 操作规则已统一为强制使用命令行工具，浏览器入口从用户侧规则中移除。影响：后续查询、创建、评论、工时和状态流转都走同一套命令，规则里不再保留网页或截图作为备用做法。范围：TAPD 四个相关 skill、URL 路由规则、浏览器 skill 的 TAPD 入口、项目记忆与技能字典。非范围：本轮不执行业务写入，也不验证所有项目状态机都能由命令行完成。变化：删除了浏览器 TAPD 自动化参考和周报模板，补上命令行能力缺口时的停止口径。完成标准：受影响的 skill 结构校验通过，规则和字典口径一致，真实只读命令可用，风格检查为通过。术语说明：风格回归表示只检查写法、位置、格式和可读性，不判断业务流程是否正确。验证状态：结构和只读命令已验证，命令行未覆盖的业务写入留作后续验证。

## 文档信息

| 字段 | 内容 |
|---|---|
| 来源任务 | `TASK-TAPD-CLI-ONLY`，用户要求 TAPD 规则绝对禁止浏览器并强制使用 CLI |
| 风格结果 | `STYLE: PASS` |
| 检查对象 | TAPD 四个 skill 及其参考文件、URL 路由规则、浏览器 skill、项目记忆和技能字典 |
| 回归时间 | 2026-11-23 15:49:57 |
| 执行环境 | Windows 本机 Git Bash，Node.js 命令行工具 |

## 检查范围

- TAPD 查询、创建、更新、评论、工时和状态流转的规则口径。
- TAPD 链接的处理方式与浏览器 skill 中的 TAPD 专属入口。
- 规则文本中的路径、引用、编码、标点和目录归位。
- N/A + 原因 + 证据：不检查真实 TAPD 业务写入，本轮只做规则改造和只读命令验证，证据见 `TEST-TAPD-CLI-VALIDATION`。

## 真实测试前置证据

| 测试 | 证据 |
|---|---|
| `TEST-TAPD-CLI-VALIDATION` | `EVIDENCE-TAPD-CLI-VALIDATION`：七个受影响 skill 的结构校验全部通过，差异格式检查退出码为 0。 |
| `TEST-TAPD-CLI-READONLY` | `EVIDENCE-TAPD-CLI-READONLY`：用户信息与迭代列表两个只读命令返回真实数据，没有执行业务写入。 |

## 6-review 结论

STYLE: PASS

检查覆盖规则文本的格式、引用、标点和目录归位，以及文档结构与追踪字段。业务正确性和 TAPD 写入能力不在本次风格回归范围内。

## 检查清单

| 检查项 | 结果 | 证据 |
|---|---|---|
| 规则统一使用命令行入口 | PASS | `EVIDENCE-TAPD-CLI-VALIDATION` |
| 浏览器 TAPD 入口已清理 | PASS | 旧文件引用扫描无命中，浏览器 skill 只保留通用网页操作规则 |
| 格式、编码与标点 | PASS | 差异格式检查退出码 0，Markdown 标点校验通过 |
| 稳定 ID 与追踪字段 | PASS | `TASK-TAPD-CLI-ONLY`、`TEST-TAPD-CLI-VALIDATION`、`EVIDENCE-TAPD-CLI-VALIDATION` |

## 问题与修复

- 已修复：首版记录缺少新文档契约要求的元数据、白话摘要和规定章节，现已补齐并通过文档校验。
- 已修复：白话开场中的英文缩写与中文之间缺少空格、半角逗号混用，现已统一为全角标点和中西文空格。
- 已修复：浏览器 skill 继续保留 TAPD 自动化参考与周报模板，容易让执行者回到网页流程；两处入口已删除，历史内容可从 Git 历史恢复。
- 已知缺口：命令行没有查询工作流转换规则的能力，缺陷更新也未暴露部分字段参数；规则要求遇到这类情况报告缺口并停止，不转到浏览器或直接调用接口。

图片资产决策：N/A + 原因：本轮只修改 skill 规则与文档，不涉及界面、截图或视觉对比 + 证据：暂存差异仅包含 Markdown、JavaScript 字典数据和被删除的 Markdown 与 shell 模板，没有图片路径。

## 追踪附录

| 任务 | 测试 | 证据 |
|---|---|---|
| `TASK-TAPD-CLI-ONLY` | `TEST-TAPD-CLI-VALIDATION` | `EVIDENCE-TAPD-CLI-VALIDATION` |
| `TASK-TAPD-CLI-ONLY` | `TEST-TAPD-CLI-READONLY` | `EVIDENCE-TAPD-CLI-READONLY` |
