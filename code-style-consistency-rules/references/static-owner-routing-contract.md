# 共享静态 Owner 路由契约

## 目的

`static_owner_router.py` 是静态 Owner 路由的唯一来源。`6-review` 使用它筛选代码风格相关 Owner，持续代码质量监督可复用完整 Owner 集合；两个消费者不得复制 Owner 常量或条件路由。

## 导出接口

- `OWNER_NAMES`：允许静态路由的完整 Owner 集合。
- `BASE_OWNER_NAMES`：所有非空代码改动都需要的基础 Owner，顺序固定。
- `route_owners(changed_files, signals=())`：按仓库相对路径与已确认信号返回去重后的稳定 Owner 顺序。
- `owner_source_map_path(repository_root)`：返回 `code-style-consistency-rules/references/static-owner-source-map.json` 的绝对路径。
- `load_owner_source_map(repository_root=".")`：加载并校验来源映射，返回 `{owner: {"sites": [...], "source_paths": [...]}}`；违例抛出 `OwnerSourceMapError`。
- `owner_source_paths(repository_root, owner)`：返回单个 Owner 的去重来源路径元组。
- `route_review_pipeline(changed_files, signals=(), repository_root=".")`：由已加载的来源映射推导 `6-review` 的有序检查步骤。
- `render_review_pipeline(pipeline)`：把步骤渲染为可粘贴进 `6-review` 记录的 Markdown 清单。
- `REVIEW_STEPS`、`SOURCE_MAP_VERSION`、`OwnerSourceMapError`：流水线九步表、映射版本与加载异常。
- `iter_rule_reference_files(repository_root, owner)`：按统一口径枚举某 Owner 目录下应当登记的规则 Markdown 文件。
- `RULE_REFERENCE_SUFFIX`、`NON_RULE_FILE_NAMES`、`NON_RULE_FILE_PATTERN`、`NON_RULE_DIR_NAMES`：覆盖率断言的枚举口径与豁免名单。

## 路由边界

- 路径只按文件后缀、完整路径段和完整 token 判断，避免任意子串误触发。
- `signals` 必须是上游已经确认的语义信号；本模块不从代码内容推断业务含义。
- 空文件列表返回空列表；同一 Owner 只返回一次，并保持基础 Owner 及条件 Owner 的固定顺序。
- 本契约只负责静态规则归属，不执行规则、不判断业务正确性、不判断测试充分性，也不作发布放行结论。

## 来源映射

来源映射为 `version: 2` 的**有序数组**结构：

```json
{
  "version": 2,
  "owners": [
    { "owner": "<owner>", "sites": [ { "source_paths": [], "source_globs": [], "consumption": "static-only" } ] }
  ]
}
```

- 一个 Owner 的 `sites` 可以有多组，用于承载该 Owner 在不同关注点上的规则来源；**禁止**把它压平为单列表，也**禁止**退回 v1 的「对象 key = Owner 名」形态——同一 Owner 以重复 key 出现时，JSON 会静默覆盖前一块（实测 v1 为 28 块、解析后仅剩 22 块，丢失 6 块）。
- `source_paths`：必须非空，且只允许仓库相对路径；必须位于该 Owner 目录下，拒绝绝对路径、路径穿越、跨 Owner 路径与缺失文件。
- `source_globs`：不得包含空 glob；当前全部为空数组，表示来源为精确文件清单。
- `consumption`：必填，声明该组来源的消费方式。

加载时必须通过的一致性断言：

- 文本层 Owner 声明数与解析数一致、来源分组数一致；同一 Owner 名不得重复。
- 来源映射的 Owner 集合与 `OWNER_NAMES` **完全一致**，任一方向漂移都失败关闭。
- 流水线（`REVIEW_STEPS`）引用的 Owner 必须已登记，且九步必须覆盖全部已登记 Owner。
- **覆盖率断言**：Owner 目录下的规则 Markdown 必须全部登记。`iter_rule_reference_files()` 是唯一枚举口径，漏登记即失败关闭，避免规则文件存在却没有 6-review 检查落点。

覆盖率断言的枚举口径与豁免：

- 枚举范围限 Markdown（`RULE_REFERENCE_SUFFIX`）；脚本与配置由各自的登记位点单独负责，不在本断言范围。
- 豁免目录 `NON_RULE_DIR_NAMES`：`templates`、`data`、`assets`、`scripts`、`__pycache__`、`.workbuddy`。豁免只是「不要求登记」，已登记的文件不受影响。
- 豁免文件 `NON_RULE_FILE_NAMES`：`source-notes.md`、`workbuddy-absorption-map.md`，以及仓库治理文件（`README.md`、`LICENSE.md`、`SYNC.md`、`AGENTS.md`、`CLAUDE.md`、`CHANGELOG.md`）。这些是溯源登记或吸收映射，不承载判定口径，不进入 6-review 来源投影。
- 豁免模式 `NON_RULE_FILE_PATTERN`：`case-<topic>-absorption.md`，属吸收案例记录而非规则。

调整豁免名单等同于调整规则边界，必须在同一轮同步本契约、测试与 `source-notes.md`。

## 变更约束

- 新增或删除 Owner 时，必须在同一轮内同步 `OWNER_NAMES`、来源映射、`REVIEW_STEPS` 与测试，再同步消费者。
- 新增 Owner 的规则来源文件后，必须在同一轮内同步该 Owner 的 `sites`；覆盖率断言会直接拦下漏登记，不需要靠人工盘点发现。
- 新增规则文件却无法确定归属分组时，追加到该 Owner 的归集 site；不要新建只为容纳单个文件的 site。
- 禁止在消费者目录复制本契约的 Owner 列表、条件信号或来源映射。
- 仅允许 UTF-8 文本和 JSON；不得全仓格式化或引入业务代码依赖。
