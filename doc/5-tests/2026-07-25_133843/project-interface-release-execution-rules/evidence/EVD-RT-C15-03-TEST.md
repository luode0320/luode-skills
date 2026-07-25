# EVD-RT-C15-03-TEST

- 命令：`python -X utf8 -W error::DeprecationWarning -m unittest discover -s doc/5-tests/2026-07-25_133843/project-interface-release-execution-rules/tests -p test_*.py -v`
- 环境：隔离工具环境、随机回环端口、local 配置来源。
- 结果：完整 C13-C15 测试集 19/19 PASS；C15-03 新增 1/1 PASS。
- 正向：HTTP 返回 202、SSE 收到关联事件、HTTP GET 返回相同 correlation/state/value、DELETE 返回 deleted=1。
- 清理：跨协议对象、SSE 流、服务线程和端口全部回收。
