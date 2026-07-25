# EVD-RT-C14-02-TEST

- 命令：`python -X utf8 -m unittest discover -s doc/5-tests/2026-07-25_133843/project-interface-release-execution-rules/tests -p test_*.py -v`
- 环境：隔离工具环境、随机回环端口、local 配置来源。
- 结果：完整 C13+C14 测试集 10/10 PASS；C14-02 新增 2/2 PASS。
- 正向：状态码、媒体类型、下载文件名、响应头长度、实际长度和 SHA-256 全部一致。
- 负向：HTTP 200 但预期摘要错误时，场景稳定返回 `FAIL/SCENARIO_ASSERTION_FAILED`。
- 清理：响应流关闭，服务线程和随机端口在测试结束时回收。
