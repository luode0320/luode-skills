# 测试程序正反例

## 正例

- `test/internal/service/history_client_test.go` 只保留场景编排和断言，把稳定重复的数据构造抽到同目录 helper。
- `test/internal/service/history_client_mock.json` 与主测试代码同在 `internal/service` 的 ASCII 源码镜像目录；若 mock 由可执行程序提供，也继续放在该目录，不迁入 `doc/5-tests/`。
- `doc/5-tests/2026-08-01_120000_历史客户端查询.md` 只说明目标、运行方式、被测文件和证据路径，不承载脚本。
- 白盒需求按三级替代出路降级后，将外部包用例放入根 `test/`，不在源码目录新增同包 `*_test.go`，也不为可测性改动生产代码。
- 测试所需的种子数据、固定样本和假依赖全部放在 `test/` 的源码镜像目录，由测试侧调用生产已导出的 API 落库。
- 第三方 API 响应不明时，在根 `test/` 放探测脚本，执行后将脱敏响应留存到 `doc/5-tests/` 测试主文档的证据小节。

## 反例

- 在 `doc/5-tests/` 中文目录直接放 `history_client_test.go`、mock、stub、fake 或其它可执行模拟程序。
- 一个脚本同时做环境切换、构造数据、发请求、验结果、导报告和清理资源。
- 为了测试方便，把假实现和测试常量直接写进生产 `service` 或 `utils`。
- 在生产 repository 上加一个只有 `test/` 调用的 `EnsureSeed()`，并把固定测试样本写成生产文件里的 `seedAddressBlacklist` 常量数组：前者命中引用面判据，后者命中级联污染，都必须迁到 `test/` 镜像目录。
- 把 Go 测试包目录命名成中文，或在源码目录新增 `internal/service/order_service_test.go`。
- 第三方 API 响应结构不明时，在生产代码中直接使用 `map[string]any` 加硬编码 key 解析。
