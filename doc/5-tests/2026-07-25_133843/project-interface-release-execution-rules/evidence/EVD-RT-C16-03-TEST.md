# EVD-RT-C16-03-TEST

- 完整测试：24/24 PASS。
- 正向：WS sequence 升序、event_id 唯一、SSE 与 HTTP correlation 相等。
- 负向：跨协议捕获值不一致稳定抛出 `ScenarioAssertionError`。
