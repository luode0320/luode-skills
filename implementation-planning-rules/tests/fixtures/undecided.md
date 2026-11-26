# 计划：为示例模块补测试（含未决反例，期望 BLOCKED）

当前计划最终方案：补测试文件，落点 tests/test_demo.py。

## agent 对当前问题的理解

- 目标：补一个测试。
- 本轮范围：tests/test_demo.py。
- 不在范围：生产代码。

## 来源落盘

需求主文档见 docs/requirement-demo.md（已存在）。

## 范围与边界

- 范围：仅补测试。
- 归属：测试域。
- 兼容性：不改生产行为。

## 完成条件

- AC-1：运行 pytest tests/test_demo.py，通过标准 exit=0。

## 决策

- 是否同时补 fixture：待确认。

## 反方批判

结论：维持当前方案。
