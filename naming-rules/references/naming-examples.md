# 命名样例

## 更优

- `orderRefundStatus` 明显优于 `status2`。
- `buildInvoicePayload` 明显优于 `handleData`。
- `buildInvoicePayload` 明显优于 `build_invoice_payload`，前提是它属于内部代码标识符而不是外部协议字段。
- `RefundOrderRequest` 明显优于 `refund_order_request`，前提是它是类型名而不是数据库表或外部消息结构名。

## 较差

- 一个名字同时承担动作和对象含义。
- 同一概念在不同文件里叫 `user`、`member`、`account` 却没有区分说明。
- 同一概念在不同位置混用 `orderRefundStatus`、`order_refund_status`、`order-refund-status`，却没有语言生态或外部协议上的理由。
