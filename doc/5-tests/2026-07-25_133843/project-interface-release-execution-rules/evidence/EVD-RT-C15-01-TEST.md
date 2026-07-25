# EVD-RT-C15-01-TEST

- 命令：`python -X utf8 -W error::DeprecationWarning -m unittest discover -s doc/5-tests/2026-07-25_133843/project-interface-release-execution-rules/tests -p test_*.py -v`
- 环境：隔离工具环境、随机回环端口、local 配置来源。
- 首次结果：鉴权失败的 1008 关闭异常从发送动作逃出，形成 unittest ERROR。
- 修复：在 transport 边界读取正式 `rcvd.code` 并转换为稳定场景失败；同输入复验通过且无弃用告警。
- 结果：完整测试集 16/16 PASS；C15-01 新增 3/3 PASS。
- 负向：鉴权失败、消息缺失、乱序和重复均由真实 WebSocket 网络帧稳定识别。
- 清理：场景失败与成功均关闭客户端连接，服务线程和端口在类级清理中回收。
