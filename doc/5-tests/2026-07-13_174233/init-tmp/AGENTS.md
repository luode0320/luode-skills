# AGENTS

## 微业务架构约束

本项目采用微业务(伪微服务)架构, 由 `micro-business-architecture-rules` skill 守护。

- 不同业务放在 `internal/business/<域>/` 下, 各自自包含; 业务包之间禁止直接 import(横向零依赖)。
- 跨业务调用只经公共接口包 `internal/contract/<域>/` 以接口形式通信(依赖倒置)。
- 新业务新开目录包, 旧业务只在自己包内演进, 互不影响。
- 每个业务包必须有统一 README; 全局业务索引在 `internal/business/README.md`, 接口契约清单在 `internal/contract/README.md`。
- 新增业务用 `micro_business.py scaffold <业务名>`, 改动后用 `micro_business.py check` 校验隔离。
