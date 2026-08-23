# golang-patterns 吸收裁决表（workbuddy-absorption-map）

> 归属 owner：`skill-absorption-rules`。每行必须可回指来源与落点，含「整理去重」列。

## 2026-08-22 吸收 go（skillhub 市场，v1.0.2）→ golang-patterns

| 外部来源 | 外部精华 | 本地现状 | 裁决 | 落点 / 理由 | 整理去重 |
| --- | --- | --- | --- | --- | --- |
| go v1.0.2（skillhub） | Goroutine 泄漏：无退出条件、for range 无人 close、ctx 取消不生效、无法外部 kill | 本地仅「select+ctx.Done() 兜底」（弱版） | 合并 | `references/go-traps-checklist.md` §1；SKILL.md 入口表 | 本地弱版规则保留在正文，checklist 不重复展开 |
| go v1.0.2（skillhub） | Channel 陷阱：nil/closed channel、仅 sender close、select 随机、empty select、无缓冲同步点 | 本地缺失 | 合并 | `references/go-traps-checklist.md` §2 | 无 |
| go v1.0.2（skillhub） | Defer 陷阱：立即求值、循环累积、LIFO、修改命名返回值、defer mu.Unlock | 本地缺失 | 合并 | `references/go-traps-checklist.md` §3 | 无 |
| go v1.0.2（skillhub） | nil interface（type+value 双 nil）、comma-ok、隐式实现、指针接收者方法集、嵌入陷阱 | 本地缺失 | 合并 | `references/go-traps-checklist.md` §4；SKILL.md 入口表 | 与正文「接口设计」互补：正文讲模式，checklist 讲陷阱 |
| go v1.0.2（skillhub） | 错误链 Go 专属：sentinel var、errors.New 每次新实例、*MyError、Unwrap、log.Fatal 跳过 defer | 本地仅 errors.Is/As、%w（已有且更强） | 部分合并 | 通用原则保留本地正文；Go 专属机制进 `references/go-traps-checklist.md` §5 | 与 `error-handling-rules`（通用错误处理）确认职责边界：Go 专属归本 skill，不复制通用原则 |
| go v1.0.2（skillhub） | Slice/Map/String 陷阱：共享底层数组、append 重分配、nil map 写 panic、len 字节数、string(65) 等 | 本地仅 strings.Builder、预分配 slice（已有） | 部分合并 | 本地已有的 strings.Builder、预分配 slice 保留正文；其余进 `references/go-traps-checklist.md` §6-8 | 无重复段落 |
| go v1.0.2（skillhub） | Struct/Build 陷阱：padding、复制含锁 struct、go:embed 相对路径、unused import | 本地零值可用、init 全局状态已有 | 部分合并 | 本地已有的零值/init 保留正文；其余进 `references/go-traps-checklist.md` §9-10 | 无 |
| go v1.0.2（skillhub） | 循环变量捕获陷阱（go func(i int)） | 本地缺失 | 合并（修订） | checklist §1 注明 Go 1.22+ 已修复，仅 <1.22 需要显式传参 | 修订原文过时语义，避免误导新版用户 |
| go v1.0.2（skillhub） | 西班牙语残留（usar、es copy、necesita） | — | 拒绝 | 不照搬，统一中文表达 | 无 |
| go v1.0.2（skillhub） | `go build -a` 强制重建缓存 | — | 拒绝 | 非高频陷阱，为吸收而吸收 | 无 |
| go v1.0.2（skillhub） | Quick Reference 表 + 4 独立 reference 目录结构 | — | 拒绝 | 不复制外部形态，合并为单一 checklist（10 类） | 单一权威落点 |

**净增/净减**：目标 skill 净增 11,645 字节（SKILL.md +1,394、checklist 10,251）；删除源目录 11,251 字节；体系净增 394 字节。
**同域冗余扫描**：范围 {golang-patterns, error-handling-rules, common-util-rules, code-quality-rules, code-generation-style-rules}；发现 0 处逐字重复；清理 0 处；PASS（Go 专属陷阱归 golang-patterns，通用错误原则归 error-handling-rules，职责边界已确认）。
**棘轮评分**：基线 55.8 → 吸收后 84.3（独立子代理评分，3 场景实测全命中），涨幅 28.5 分，保留。
**源删除**：`go__skillhub/`（用户级安装）已删除。
