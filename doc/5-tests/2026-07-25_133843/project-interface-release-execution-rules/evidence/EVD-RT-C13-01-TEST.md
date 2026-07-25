# C13-01 真实测试证据

- 环境：WSL 隔离工具虚拟环境；随机 `127.0.0.1` 回环端口。
- 命令：`python -X utf8 -m unittest .../test_scenario_contract.py -v`。
- 结果：5 项通过；真实 HTTP 状态、JSON 值捕获、错误状态码断言、候选阻断和来源漂移均符合预期。
- 清理：HTTP 服务关闭、端口释放、线程已 join。
