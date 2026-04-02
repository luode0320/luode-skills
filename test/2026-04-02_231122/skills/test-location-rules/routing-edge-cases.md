# `test-location-rules` 第二轮边界与联动验证

## 补充文档类型

- 边界场景与联动顺序验证

## 对应的真实代码路径

- `test-location-rules/`
- `test-task-root-layout-rules/`
- `test-scattered-asset-location-rules/`
- `go-test-compile-path-rules/`

## 补充目的

验证新拆分 skill 集合在“非触发场景”“多 skill 联动顺序”“`test/` 根目录内部的 Go 特例路径”等更容易打架的边界上，是否仍能与旧 `test-location-rules` 对齐。

## 具体步骤、案例或证据

### 案例 5：只修改现有测试任务 README 内容，不改落点

- 场景输入：
  - “我只是在现有 `test/2026-04-02_231122/某任务/README.md` 里补一段测试结论，不移动目录也不新建文件。”
- 旧 skill 预期结论：
  - 不属于“测试说明文档落点变化”，旧 `test-location-rules` 不应主命中。
  - 应更偏向 `test-doc-rules` / `functional-validation-rules`。
- 新 skill 集合预期结论：
  - 三个新 skill 都不应主命中。
  - 仍应由 `test-doc-rules` / `functional-validation-rules` 处理内容更新。
- 对照结果：
  - 一致
- 观察说明：
  - 新 skill 集合没有因为“出现 README”而误触发，边界比旧 skill 更清楚。

### 案例 6：仓库还没有 test 根目录，但已经散落了测试资产和 Go 白盒测试文件

- 场景输入：
  - “当前仓库没有 `test/`，但根目录已有 `create-order-test.js`，`docs/` 里有 `order_mock.json`，`internal/service/order_service_test.go` 也已经出现了。”
- 旧 skill 预期结论：
  - 命中 `test-location-rules`
  - 先建立中央测试根目录和时间戳目录
  - 再迁移散落资产
  - 同时处理 Go 源码目录 `_test.go` 和 seam
- 新 skill 集合预期结论：
  - 第一步主命中 `test-task-root-layout-rules`
  - 第二步 `test-scattered-asset-location-rules` 迁移根目录和 `docs/` 散落资产
  - 第三步 `go-test-compile-path-rules` 处理源码目录 `_test.go` 和 seam
- 对照结果：
  - 一致
- 观察说明：
  - 新 skill 集合把旧 skill 的“大一统流程”拆成了清晰的先后顺序，没有丢掉任何步骤。

### 案例 7：测试文件已经位于 test 根目录下，但镜像路径里混入中文

- 场景输入：
  - “测试文件放在 `test/2026-04-02_231122/登录验证/internal/中文/service/login_test.go`，已经在 `test/` 下了，这样可不可以？”
- 旧 skill 预期结论：
  - 仍然不可以
  - 因为中文进入了 Go 可编译测试路径
- 新 skill 集合预期结论：
  - 主命中 `go-test-compile-path-rules`
  - 即使已位于 `test/` 根目录，也仍要清理中文可编译路径
- 对照结果：
  - 一致
- 观察说明：
  - 新 skill 没把“已经在 test 根目录”误判成“已经合规”，Go 特例承接正常。

### 案例 8：同一需求下要做第二个独立验证波次

- 场景输入：
  - “今天已经有一轮 `2026-04-02_231122` 的验证，现在还要再做一轮完全独立的导出功能验证，能不能继续往同一时间戳目录里堆？”
- 旧 skill 预期结论：
  - 不建议继续堆
  - 多轮独立验证应拆成新的时间戳根目录
- 新 skill 集合预期结论：
  - 主命中 `test-task-root-layout-rules`
  - 明确要求第二个独立验证波次新建新的时间戳根目录
- 对照结果：
  - 一致
- 观察说明：
  - 新 skill 集合保留了“独立波次建新根目录”的拆分原则，没有出现“同需求就默认全塞一个根目录”的退化。

## 实际结果或观察结论

- 第二轮 4 个边界案例全部通过。
- 当前未发现新 skill 集合在“非触发场景”上误抢职责。
- 当前未发现新 skill 集合在“先建根目录，再迁移散落资产，再处理 Go 特例”的联动顺序上出现歧义。
- 当前未发现“已经在 `test/` 根目录里就默认全都合规”的错误放宽。

## 与主 README 的关联说明

- 本文件是 `test/2026-04-02_231122/test-location-rules拆分对照验证/README.md` 的第二轮补充证据文档。
