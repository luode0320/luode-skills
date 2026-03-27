# 测试目录落点样例

## 正例

- 后端接口集成测试放在 `tests/api/order-create/`，同目录下再区分 `cases/`、`fixtures/`、`README.md`。
- 前端项目采用就近测试约定时，组件测试放在 `src/components/UserCard/__tests__/`。
- 共享 mock 服务或共享测试辅助工具放在 `tests/shared/` 或项目既有公共测试目录。
- Go 项目的样例数据放在模块旁边的 `testdata/`，前提是项目本身就采用这种结构。

## 反例

- 把 `create-order-test.js` 直接放在仓库根目录。
- 把接口返回样例 JSON 放进 `src/controllers/`、`app/services/` 之类的生产目录。
- 把验证脚本命名成临时文件后长期留在 `scripts/` 或 `tmp/` 中。
- 把测试说明写到 `docs/`，但目录里没有对应测试代码和测试数据，导致说明与资产脱节。

## 判定示例

- 如果当前仓库统一使用 `tests/` 管理测试资源，就不要再新增 `qa/`、`verify/`、`tmp-test/` 等平行目录。
- 如果当前仓库统一使用模块内 `__tests__/`，就不要把局部单测强行挪到项目根目录。
- 如果当前测试资产只服务一个需求任务，应优先在该任务测试目录聚合，不要拆散到多个无关公共目录。
