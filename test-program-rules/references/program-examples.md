# 测试程序正反例

## 正例

- `test/internal/service/history_client_test.go` 只保留场景编排和断言，把稳定重复的数据构造抽到同目录 helper。
- `test/internal/service/history_client_mock.json` 与主测试代码同在 `internal/service` 的 ASCII 源码镜像目录；若 mock 由可执行程序提供，也继续放在该目录，不迁入 `doc/5-tests/`。
- `doc/5-tests/2026-08-01_120000_历史客户端查询/README.md` 只说明目标、运行方式、被测文件和证据路径，不承载脚本。
- 白盒需求先补 seam，再将外部包用例放入根 `test/`，不在源码目录新增同包 `*_test.go`。
- 第三方 API 响应不明时，在根 `test/` 放探测脚本，执行后将脱敏响应留存到 `doc/5-tests/` 的 `evidence/`。

## 反例

- 在 `doc/5-tests/` 中文目录直接放 `history_client_test.go`、mock、stub、fake 或其它可执行模拟程序。
- 一个脚本同时做环境切换、构造数据、发请求、验结果、导报告和清理资源。
- 为了测试方便，把假实现和测试常量直接写进生产 `service` 或 `utils`。
- 把 Go 测试包目录命名成中文，或在源码目录新增 `internal/service/order_service_test.go`。
- 第三方 API 响应结构不明时，在生产代码中直接使用 `map[string]any` 加硬编码 key 解析。
