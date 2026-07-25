# EVD-RT-C14-01-TEST

- 命令：`/home/luode/.cache/luode-skills/release-test-engine/bin/python -X utf8 -m unittest test_scenario_contract.py test_http_external_scenarios.py -v`
- 环境：WSL、随机回环端口、local 配置来源、隔离工具环境。
- 首次结果：form 与 multipart 因 URL 内捕获值未展开而稳定失败；同时发现错误响应资源告警。
- 修复：增加受限占位符替换并显式关闭 `HTTPError` 响应流。
- 同输入复验：8/8 PASS；C13 回归 5/5 PASS；C14-01 新样本 3/3 PASS。
- 失败样本：错误媒体类型返回 415，场景结果为 `FAIL/SCENARIO_ASSERTION_FAILED`。
- 清理：两个正向场景均执行 HTTP DELETE，fixture 记录为空；服务线程和端口在测试结束时回收。
