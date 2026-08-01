# 共享静态 Owner 路由契约

## 目的

`static_owner_router.py` 是静态 Owner 路由的唯一来源。`6-review` 使用它筛选代码风格相关 Owner，持续代码质量监督可复用完整 Owner 集合；两个消费者不得复制 Owner 常量或条件路由。

## 导出接口

- `OWNER_NAMES`：允许静态路由的完整 Owner 集合。
- `BASE_OWNER_NAMES`：所有非空代码改动都需要的基础 Owner，顺序固定。
- `route_owners(changed_files, signals=())`：按仓库相对路径与已确认信号返回去重后的稳定 Owner 顺序。
- `owner_source_map_path(repository_root)`：返回 `code-style-consistency-rules/references/static-owner-source-map.json` 的绝对路径。

## 路由边界

- 路径只按文件后缀、完整路径段和完整 token 判断，避免任意子串误触发。
- `signals` 必须是上游已经确认的语义信号；本模块不从代码内容推断业务含义。
- 空文件列表返回空列表；同一 Owner 只返回一次，并保持基础 Owner 及条件 Owner 的固定顺序。
- 本契约只负责静态规则归属，不执行规则、不判断业务正确性、不判断测试充分性，也不作发布放行结论。

## 来源映射

`static-owner-source-map.json` 中的 `source_paths` 与 `source_globs` 必须使用仓库相对路径，并且路径必须位于对应 Owner 目录下。消费者读取来源时应拒绝绝对路径、路径穿越、跨 Owner 路径、缺失文件和空 glob。

## 变更约束

- 新增 Owner 前先更新本模块、来源映射和测试，再同步消费者。
- 禁止在消费者目录复制本契约的 Owner 列表、条件信号或来源映射。
- 仅允许 UTF-8 文本和 JSON；不得全仓格式化或引入业务代码依赖。
