# Skill 集成方式

其他 skill 需要引用目录和命名规则时，优先引用本 skill，而不是重复写死模板。

## 推荐引用方式

- 需要知道根目录、入口文件或扫描范围时，优先读取 `../artifact-storage-rules/references/path-map.yaml`
- 需要知道各根目录职责时，读取 `../artifact-storage-rules/references/root-directories.md`
- 需要知道命名模板时，读取 `../artifact-storage-rules/references/naming-templates.md`
- 需要知道“更新原记录还是新建新记录”时，读取 `../artifact-storage-rules/references/update-policy.md`

## 其他 skill 的写法建议

- 可以写“路径、命名和复用策略统一遵循 `artifact-storage-rules`”。
- 可以写“如需具体模板，读取 `../artifact-storage-rules/references/path-map.yaml`”。
- 不建议在各自 `SKILL.md` 中重复维护完整的 `ment/`、`bug/`、`test/`、`doc/` 模板说明。

## 变更优先级

如果全局目录或命名约定调整，默认顺序如下：

1. 先改 `artifact-storage-rules/references/path-map.yaml`
2. 再改 `artifact-storage-rules` 其他说明文件
3. 最后只同步修改其他 skill 中少量必要的引用描述

不要反过来先修改其他 skill，再回头补中央规则。
