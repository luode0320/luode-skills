# EVD-RT-C14-03-TEST

- 命令：`python -X utf8 -m unittest discover -s doc/5-tests/2026-07-25_133843/project-interface-release-execution-rules/tests -p test_*.py -v`
- 环境：隔离工具环境、随机回环端口、local 配置来源。
- 结果：完整 C13+C14 测试集 13/13 PASS；C14-03 新增 3/3 PASS。
- 正向：首次订阅接收 `corr-1`；第二次订阅携带 `Last-Event-ID: 1` 并只接收 ID 2 的 `corr-2`。
- 负向：半包后断流稳定返回 `SSE_STREAM_INTERRUPTED`；错误关联稳定返回场景 FAIL。
- 清理：SSE 响应、线程池、fixture 服务线程和随机端口均在测试结束时回收。
