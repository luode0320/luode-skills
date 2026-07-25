# EVD-RT-C14-02-IMPL

- 结论：完成下载响应头、实际字节长度和 SHA-256 消费者断言。
- 实现：复用 HTTP transport 的 `body_length`、`body_sha256` 和脱敏 `body_bytes` 输出。
- fixture：真实返回 `application/octet-stream`、`Content-Disposition` 和 `Content-Length`。
- 边界：不持久化原始下载内容，不新增依赖或动作类型。
