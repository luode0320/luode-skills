# 来源记录（api-contract-rules）

> 归属 owner：`skill-absorption-rules`。记录本 skill 的调整来源与落点，外部源必须可回指。

## 2026-08-23：外部吸收 — api-design__skillhub

- **来源**：`api-design__skillhub`（本地安装源，origin: ECC；元数据见 `_skillhub_meta.json`）。
- **主题**：REST API design patterns（资源命名、状态码、分页、过滤、错误响应、版本化、限流）。
- **落点**：
  - `references/path-and-method-semantics.md` — kebab-case 多词资源命名、子资源层级表达（+2 行）
  - `references/response-variants.md` — HTTP 状态码语义补充、cursor 分页变体 + 选择矩阵、兼容字段与版本化策略、限流响应（净增约 45 行，含去重约 30 行）
- **删除**：吸收确认后删除源目录 `api-design__skillhub/`。
- **裁决明细**：见 `workbuddy-absorption-map.md`。
