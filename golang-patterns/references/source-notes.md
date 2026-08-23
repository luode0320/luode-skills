# golang-patterns 来源记录（source-notes）

## 2026-08-22 外部吸收：go v1.0.2（skillhub 市场）

- **来源**：skillhub 市场 `go` skill v1.0.2（slug: go，ownerId: kn73vp5rarc3b14rc7wjcw8f8580t5d1，publishedAt: 2026-02-15 前后）
- **本地安装路径**：`~/.workbuddy/skills/go__skillhub/`（已随本次吸收删除）
- **内容**：SKILL.md（九类陷阱概览）+ 4 个 references（concurrency.md / interfaces.md / collections.md / errors.md），共约 62 条原子陷阱
- **落点**：新增 `references/go-traps-checklist.md`（10 类陷阱清单，中文）；SKILL.md 新增「陷阱速查」入口表并扩展 description 触发词
- **修订**：循环变量捕获陷阱按 Go 1.22 语义修正；原文西班牙语残留全部译为中文；与本地已有规则重复的条目（errors.Is/As、%w、strings.Builder、panic 保护等）未重复写入
- **裁决与体积账**：见 `workbuddy-absorption-map.md`（2026-08-22 行）
- **案例**：见 `references/case-go-absorption.md`
