# code-style-consistency-rules 来源记录

## 2026-09-11

- 内部调整：`code-style-consistency-rules`，调整诉求「把来源映射（owners）的加载真正纳入 `6-review` 流水线，并让规则文件的登记完整性在加载期自证」。
- 触发来源：用户会话——AI 辅助开发瓶颈已从逻辑正确性转向代码质量；用户明确要求「把 owners 的加载也纳入流水线」，即不接受只做最小修补（数组化 + 断言），而要求检查步骤由**已加载的来源映射**派生，从编排层根治。
- 结构性缺陷一（静默覆盖）：来源映射原为 v1「对象 key = Owner 名」形态，28 个位点被 JSON 静默覆盖为 22 个，丢失 6 个（`api-contract-rules` ×3、`comment-rules` ×2、`code-quality-rules` ×1）。迁移为 `version: 2` 的有序数组后，28 个位点全部保留；迁移脚本已删除，迁移前备份 `owner-map-v1.bak.json`。
- 结构性缺陷二（规则文件漏登记）：对账发现 35 个 Markdown 未登记，其中 18 个是承载判定口径的规则文件，会导致这些规则**存在却没有 6-review 检查落点**。按语义分组补登记 18 条（`code-quality-rules` 按最小改动组 / 函数可读性组分别归位，其余进单一归集组），登记来源由 217 条增至 235 条。
- 落点：`scripts/static_owner_router.py`（新增 `SOURCE_MAP_VERSION`、`OWNER_KEY_PATTERN`、`SITE_KEY_PATTERN`、`OwnerSourceMapError`、`_read_source_map_text()`、`_assert_text_matches_parsed()`、`_assert_site_paths()`、`load_owner_source_map()`、`owner_source_paths()`、`iter_rule_reference_files()`、`_assert_rule_file_coverage()`、`REVIEW_STEPS`、`route_review_pipeline()`、`render_review_pipeline()`、`_main()` 命令行）、`references/static-owner-source-map.json`（v1→v2 + 补登记）、`references/style-review-pipeline.md`（新建，九步流水线与判定口径）、`references/static-owner-routing-contract.md`、`references/style-regression-contract.md`、`SKILL.md`、`test/code-style-consistency-rules/static_owner_router_test.py`（7→20 例）。
- 覆盖率断言口径：`iter_rule_reference_files()` 是唯一枚举入口，只枚举 Markdown；豁免目录 `NON_RULE_DIR_NAMES`（`templates`/`data`/`assets`/`scripts`/`__pycache__`/`.workbuddy`）、豁免文件 `NON_RULE_FILE_NAMES`（`source-notes.md`、`workbuddy-absorption-map.md` 及仓库治理文件）、豁免模式 `NON_RULE_FILE_PATTERN`（`case-*-absorption.md`）。豁免名单与 v1 的实测损失明细已写入 `references/static-owner-routing-contract.md`。
- 关联修复（`test-program-rules`）：`references/mock-factory-pattern.md`、`references/runtime-mock-pattern.md` 两个运行时 Mock 规则文档（8880B / 7332B）此前在 skill 内**零引用**，既不在正文引用区也不在读取规则中；已补 `references 读取规则` 条目恢复可达性；同时修掉 `description` 中重复出现的「运行时 Mock……」整句，以及「进入后先做什么」列表重复的编号 `7.`（顺延为 8、9）。
- 验证：`test/code-style-consistency-rules/static_owner_router_test.py` 20 例全通过；命令行 `--changed` / `--json` 端到端可用；覆盖率断言在补登记前精确拦下 18 条、补登记后通过。
