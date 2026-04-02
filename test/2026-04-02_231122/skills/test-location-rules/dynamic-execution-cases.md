# `test-location-rules` 动态样例验证

## 补充文档类型

- 动态落点样例与结构检查记录

## 对应的真实代码路径

- `test/2026-04-02_231122/`
- `test-task-root-layout-rules/`
- `test-scattered-asset-location-rules/`
- `go-test-compile-path-rules/`

## 补充目的

在当前测试时间戳根目录下实际创建一组“正确落点后的样例资产”，验证新 skill 集合不仅能在文档推演里说清规则，也能落成一套符合结构约束的真实路径。

## 动态执行样例

### 样例 1：新测试任务根布局的实际落点

- 创建路径：
  - `test/2026-04-02_231122/test-location-rules拆分对照验证/README.md`
  - `test/2026-04-02_231122/skills/test-location-rules/dynamic-artifacts/case-root-layout/internal/service/login_validation_entry.txt`
- 验证点：
  - 当前时间戳根目录只包含时间戳，不混中文。
  - 中文目录只承载 `README.md`。
  - 真实测试资产落在 ASCII 镜像路径下。
- 预期主承接 skill：
  - `test-task-root-layout-rules`

### 样例 2：散落资产迁移后的正确目标位置

- 创建路径：
  - `test/2026-04-02_231122/skills/test-location-rules/dynamic-artifacts/case-scattered-migration/internal/order/create_order_test.js`
  - `test/2026-04-02_231122/skills/test-location-rules/dynamic-artifacts/case-scattered-migration/internal/order/order_mock.json`
- 验证点：
  - 原本假设散落在仓库根目录或 `docs/` 的测试脚本与 mock，迁移后能归位到当前测试时间戳根目录的 ASCII 镜像路径。
  - 不需要再把这些文件放入中文说明目录。
- 预期主承接 skill：
  - `test-scattered-asset-location-rules`

### 样例 3：Go 白盒诉求的正确整改目标路径

- 创建路径：
  - `test/2026-04-02_231122/skills/test-location-rules/dynamic-artifacts/case-go-seam/internal/service/order_service_seam_plan.md`
- 验证点：
  - 相关整改材料位于 ASCII 路径。
  - 没有把 `_test.go` 放回源码目录。
  - 没有在 `test/` 根目录内部继续引入中文可编译路径。
- 预期主承接 skill：
  - `go-test-compile-path-rules`

## 结构检查结果

- 当前测试时间戳根目录下存在 1 个中文说明目录和 1 个 ASCII 证据目录，结构符合测试任务根布局要求。
- 中文说明目录当前仅包含 `README.md`，没有混入额外 markdown、脚本、mock 或附件。
- 动态样例资产全部位于 `skills/test-location-rules/...` 的 ASCII 路径中。
- 当前未发现“动态样例资产被误写入历史时间戳目录”或“被写进中文说明目录”的情况。

## 实际结果或观察结论

- 新 skill 集合给出的“正确目标位置”在文件系统层面可以实际落盘，且不会互相冲突。
- 目前没有出现“规则上说得通，但一旦落盘就会违反另一条规则”的结构冲突。
- 动态验证仍未覆盖自动触发引擎本身，但已经覆盖了真实落点目标路径是否自洽。

## 与主 README 的关联说明

- 本文件是 `test/2026-04-02_231122/test-location-rules拆分对照验证/README.md` 的第三轮补充证据文档。
