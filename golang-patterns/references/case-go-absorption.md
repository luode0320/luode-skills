# Case Study：go v1.0.2 吸收（golang-patterns 陷阱清单）

> 供下次吸收对照：记录本次吸收的形态、裁决模式、体积账与坑。

## 背景

外部 skill `go`（skillhub v1.0.2）是纯陷阱清单型 skill：9 类陷阱概览 + 4 个 references，约 62 条原子陷阱。本地 golang-patterns 是「模式/最佳实践」型 skill，恰好缺「陷阱 checklist」这一互补形态。知识库此前已确认 golang-patterns 演进走方案 B（SKILL.md 精简 + references/ 承载细节），本次落点与该方案一致。

## 关键决策

1. **形态分离**：外部「Quick Reference 表 + 4 独立文件」目录结构不复制，合并为单一 `go-traps-checklist.md`（10 类，比源 9 类多拆「结构体与内存」）。
2. **版本语义修订**：外部 concurrency.md 的 loop variable trap（`go func(i int)`）在 Go 1.22+ 已无必要，原文未区分版本；吸收时注明「Go < 1.22 才需显式传参」，避免误导新版用户。
3. **语言清理**：原文残留西班牙语（usar、es copy、necesita），吸收时统一中文——外部 skill 内容质量参差，逐条人工核验不可省。
4. **三态裁决**：与本地已有规则重叠的（errors.Is/As、%w、strings.Builder、panic 保护、零值可用、预分配 slice 等）一律「保留本地」，checklist 只写本地缺失的 Go 专属细节，避免双写。
5. **职责边界**：通用错误处理原则归 `error-handling-rules`（跨语言），Go 专属机制（sentinel var、Unwrap、*MyError、log.Fatal）归 golang-patterns，两 skill 不互相复制。

## 体积账（防臃肿执行证据）

| 项 | 字节 |
| --- | --- |
| SKILL.md 原 → 新 | 6,842 → 8,236（+1,394，入口表 + description） |
| 新增 checklist | 10,251 |
| 目标 skill 净增 | +11,645 |
| 删除源 go__skillhub 目录 | −11,251 |
| **体系净变化** | **+394（≈持平）** |

结论：吸收 + 删除源后整个 skill 体系体积几乎不变，换取单一权威落点（消除双 Go skill 并存），符合「吸收即整理」要求。

## 棘轮评分

- 基线：55.8（吸收前 239 行无 references，P1/P2/P3 三个陷阱场景仅 P1 部分覆盖）
- 吸收后：84.3（独立子代理评分，3 场景全命中专属条目）
- 涨幅 28.5，远超 1 分早停阈值，保留。

## 经验沉淀（供下次吸收复用）

- 陷阱清单型外部 skill 与「模式/最佳实践」型本地 skill 是天然互补，优先落 references 而非正文。
- 外部 skill 的版本敏感内容（语言版本、API 变更）必须核验修订，不能原样照搬。
- 吸收前后记得统计「目标净增 vs 源删除」的体系级体积账，用数字证明防臃肿。
