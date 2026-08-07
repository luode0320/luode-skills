# 测试资产治理

## 双根结论

- 根 `test/` 是唯一活动测试代码根。测试程序、mock、stub、fake、fixture、helper 和数据构造均为活动测试资产；源码关联资产按被测源码路径镜像存放，只有跨源码复用资产才进入 `test/shared/`。
- `doc/5-tests/` 是唯一活动测试说明与证据根。时间戳目录内只保存 `README.md`、日志、报告、截图和非可执行运行产物，不得新增测试程序或 mock/stub/fake。
- 历史 `doc/5-tests/` 中已有可执行资产按指纹只读保留；首次修改、改名或新增时迁至根 `test/`，不批量迁移历史包。

## 位置与命名

- 单文件源码：`src/order/service.py -> test/src/order/service_test.py`。
- 目录级测试：`code-style-consistency-rules/ -> test/code-style-consistency-rules/static_owner_router_test.py`；任务 README 必须列出被测文件。
- Python 测试统一使用 `*_test.py`；禁止新增 `test_*.py`。
- 测试 Mock、stub、fake、fixture 和 helper 位于相同源码镜像目录；运行时 Mock 由根 `mock/` 独立管理，不归本域治理；只有跨源码复用时才进入 `test/shared/`。不能在生产源码、仓库根、`doc/5-tests/` 或 `*/tests/` 新增活动测试代码。
- Go 测试必须位于根 `test/` 的 ASCII 路径，以外部 `<target>_test` 包导入目标模块；源码目录禁止 `*_test.go`。白盒需求先补导出 seam，不保留同包例外。

## 说明与证据

- 每次真实测试在 `doc/5-tests/YYYY-MM-DD_HHmmss_<任务主题>/README.md` 记录测试目的、运行命令、样本、结果和证据路径。
- `evidence/` 存放脱敏日志和报告；`artifacts/` 存放非可执行运行产物。截图、报告和日志不得混入 `test/`。
- 测试代码的变更不因时间戳目录而重建；时间戳只用于说明和证据轮次。

## 历史与迁移

1. 读取历史 `doc/5-tests/` 时保持原文，不修改 README、日志、报告或可执行资产。
2. 需要维护历史可执行资产时，将其移动到对应 `test/<源码镜像>/`，改为 `*_test.<ext>`，并更新活动调用方和指纹清单。
3. 未迁移的历史资产必须与 `test/shared/legacy_doc5_tests_manifest.json` 一致；新增、改名或内容变化都失败关闭。
4. 迁移只覆盖当前任务直接相关资产，不把历史整理扩展为全仓批量搬运。

## 检查与通过标准

- 运行 `python -X utf8 -B -m unittest discover -s test/test-asset-governance -p "*_test.py" -v`，覆盖正确镜像、错误目录、旧 Python 命名、源码 Go 测试和历史指纹变化。
- 运行 `python -X utf8 -B test/run_python_tests.py`，只发现根 `test/` 下的 `*_test.py`。
- Go 项目运行 `go test ./test/...`；不扫描源码目录的 `*_test.go`。
- 通过：活动测试代码仅在根 `test/`，说明和证据仅在 `doc/5-tests/`，历史包没有被批量改写。
- 驳回：把新测试代码写入 `doc/5-tests/`、源码目录或 `*/tests/`，使用 `test_*.py`，或在无迁移记录的情况下修改历史可执行资产。
