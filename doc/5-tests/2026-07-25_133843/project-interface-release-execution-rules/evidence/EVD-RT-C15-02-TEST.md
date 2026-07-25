# EVD-RT-C15-02-TEST

- 命令：`python -X utf8 -W error::DeprecationWarning -m unittest discover -s doc/5-tests/2026-07-25_133843/project-interface-release-execution-rules/tests -p test_*.py -v`
- 环境：隔离工具环境、随机回环端口、local 配置来源。
- 结果：完整 C13-C15 测试集 18/18 PASS；C15-02 新增 2/2 PASS。
- 正向：`/chat` namespace 真实连接、`publish` 事件、`published` 事件推送、ack 和 disconnect 全部 PASS。
- 负向：错误 namespace token 和 `accepted=false` ack 均稳定 FAIL。
- 清理：Engine.IO socket、ping task、aiohttp runner、事件循环和监听端口均无残留告警。
