package sample

import "fmt"

type RefundRequest struct {
    UserID  string // 用户 ID
    OrderID string // 订单 ID
    Reason  string // 退款原因
}

func BuildRefundPayload(req RefundRequest) map[string]any {
    payload := map[string]any{
        "userId":  req.UserID,
        "orderId": req.OrderID,
        "reason":  req.Reason,
    }

    // 查询订单
    order, err := queryOrder(req.OrderID)
    if err != nil {
        // third-party fixed error message: resource not found
        return map[string]any{
            "error": err.Error(),
        }
    }

    // 更新状态
    if order.Status == "paid" {
        payload["status"] = "refunding"
    } else {
        payload["status"] = "pending_review"
    }

    return payload
}

func queryOrder(orderID string) (*Order, error) {
    if orderID == "" {
        return nil, fmt.Errorf("orderID is required")
    }

    return &Order{
        Status: "paid",
    }, nil
}

type Order struct {
    Status string
}
