# `test-location-rules` 拆分对照案例

## 补充文档类型

- 场景对照验证明细

## 对应的真实代码路径

- `test-location-rules/`
- `test-task-root-layout-rules/`
- `test-scattered-asset-location-rules/`
- `go-test-compile-path-rules/`

## 补充目的

逐个场景核对旧 `test-location-rules` 与新 skill 集合的承接关系，判断是否存在功能丢失、弱化或边界歧义。

## 执行时间

- `2026-04-02 23:11:22`

## 执行人

- Codex

## 执行环境

- Windows PowerShell
- 本地静态文档对照

## 案例明细

### 场景 1：新建一轮测试任务目录

- 场景输入：
  - “我要为用户登录功能新建一轮测试任务，测试脚本、README、fixtures 应该怎么落目录？”
- 旧 skill 预期结论：
  - 命中 `test-location-rules`
  - 创建 `test/<当天时间戳>/`
  - 建中文说明目录，仅放 `README.md`
  - 真实测试资产放到 ASCII 镜像路径
- 新 skill 集合预期结论：
  - 主命中 `test-task-root-layout-rules`
  - 结论与旧 skill 等价
- 对照结果：
  - 一致
- 观察说明：
  - 根布局职责被完整拆到 `test-task-root-layout-rules`，没有再依赖旧 skill 才能说清结构

### 场景 2：今天是 2026-04-02，但想把新文件写进 2026-04-01 的旧测试目录

- 场景输入：
  - “我想直接复用昨天 `2026-04-01_101500` 的测试目录继续写新验证文件。”
- 旧 skill 预期结论：
  - 命中 `test-location-rules`
  - 必须中止并确认是否明确复用旧目录
  - 未获许可前禁止写新文件
- 新 skill 集合预期结论：
  - 主命中 `test-task-root-layout-rules`
  - 同样要求暂停确认，未获许可前禁止写入旧时间戳目录
- 对照结果：
  - 一致
- 观察说明：
  - 时间戳根目录与复用阻断没有丢失，仍由单一 skill 完整承接

### 场景 3：测试脚本和 mock 数据散落在根目录与 docs 目录

- 场景输入：
  - “仓库根目录有 `create-order-test.js`，`docs/` 里有 `order_mock.json`，应该怎么办？”
- 旧 skill 预期结论：
  - 命中 `test-location-rules`
  - 识别为散落测试资产
  - 迁回当前测试时间戳根目录，不允许继续留在根目录或 `docs/`
- 新 skill 集合预期结论：
  - 主命中 `test-scattered-asset-location-rules`
  - 若当前测试任务根目录尚未建立，先补 `test-task-root-layout-rules`
  - 再执行散落资产迁移
- 对照结果：
  - 一致
- 观察说明：
  - 新 skill 集合把“先有目标目录，再迁移散落资产”的顺序表达得更清晰，没有弱化约束

### 场景 4：Go 项目想在源码目录写白盒同包 `_test.go`，且测试包路径含中文

- 场景输入：
  - “我要在 `internal/service/order_service_test.go` 写白盒测试，测试目录里还想放中文路径，方便看。”
- 旧 skill 预期结论：
  - 命中 `test-location-rules`
  - 源码目录 `*_test.go` 禁放
  - 中文不能进入 Go 可编译路径
  - 白盒同包不是特例，应该先改 seam，再把测试资产放回 `test/<时间戳>/` 的 ASCII 镜像路径
- 新 skill 集合预期结论：
  - 主命中 `go-test-compile-path-rules`
  - 如测试任务根目录未建立，则先联动 `test-task-root-layout-rules`
  - 结论与旧 skill 等价
- 对照结果：
  - 一致
- 观察说明：
  - Go 特例规则现在被单独聚焦到 `go-test-compile-path-rules`，边界更清楚，未发现承接空洞

## 实际结果或观察结论

- 4 个场景均能从新 skill 集合中找到明确主承接者。
- 需要两个 skill 联动的场景，其先后关系也能说清楚，没有出现“大家都该管，但没人主负责”的空洞。
- 当前最主要的残余风险不在规则内容，而在未来系统级自动触发时的命中优先级实现。

## 与主 README 的关联说明

- 本文件是 `test/2026-04-02_231122/test-location-rules拆分对照验证/README.md` 的详细证据文档。
