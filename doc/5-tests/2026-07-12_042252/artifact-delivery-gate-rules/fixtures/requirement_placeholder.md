---
schema_version: 1
doc_id: "REQ-FIXTURE-PLACEHOLDER-001"
doc_type: requirement
source_ids:
  - "SRC-FIXTURE-001"
status: draft
version: "v1.0"
current_slice: "N/A"
updated_at: "2026-07-12"
---

# 需求负例：占位词

## 文档信息

该 fixture 用于验证占位词会被阻断。

## 决策冻结

当前决策后续再补。

## 普通模型零决策执行契约

执行模型不得猜测。

## 需求来源与证据台账

| 来源 | 证据 |
| --- | --- |
| `SRC-FIXTURE-001` | fixture |

## 目标与非目标

范围已限定。

## 功能需求

行为已定义。

## 数据与外部契约

N/A；原因与证据：本 fixture 不涉及外部契约。

## 风险、假设、依赖与阻断

没有额外风险。

## 追踪矩阵

| 上游 | 下游 |
| --- | --- |
| `SRC-FIXTURE-001` | `REQ-FIXTURE-001` |

```mermaid
flowchart TD
    A["输入"] --> B["输出"]
```

```mermaid
sequenceDiagram
    participant A as 来源
    participant B as 执行模型
    A->>B: 交接
```
