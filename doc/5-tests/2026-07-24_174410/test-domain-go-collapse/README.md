# 测试域 go 编译路径 skill 收编记录（CAND-SS-TEST-11）

## 结论
- 本轮把独立 skill `go-test-compile-path-rules` 收编（merge_retire）进 `test-program-rules` 的《Go 测试编译路径（强制）》承接节，并删除原 skill 目录。
- 该动作属于「测试域中度精简」当前任务周期的 T5 收口，不属于已冻结的 `MANIFEST-SS-20260721`（2026-07-21 六域治理）范围，因此不改动、不追加该冻结清单（其校验器硬锁 36 Skill / 11 退役，且已依赖被清理的 .tmp 清单而失效），改为在本目录独立记账，保持冻结产物不被污染。

## 影响与放行判定
- 保留硬阻断（语义等价迁移，无保护缺口）：Go 源码目录禁放 `*_test.go`、Go 可编译测试路径必须保持 ASCII、白盒同包诉求统一改 seam、散落资产转交 `test-strategy-rules 的 test-asset-governance 条件路由`。
- 外部引用已改指 `test-program-rules` 的《Go 测试编译路径（强制）》：`code-change-finalization-gate-rules/SKILL.md`、`skill-hit-check-rules/references/hit-checklist.md`、根 `编码skill.md`、`README.md`。
- 字典 `skill-dictionary/data.js` 与 `字典.md` 已在收口重生，自然移除 `go-test-compile-path-rules` 词条。

## 回滚
- 回滚基线提交：`8102ca95463e392e7dc534fa80e9d75876da3d56`（删除前 HEAD）。
- 从该提交可完整恢复被删目录 `go-test-compile-path-rules/`（3 个文件，哈希见 mapping/go-collapse-manifest.yaml）。

## 详细记账
- 机器可读记录见 `mapping/go-collapse-manifest.yaml`。
