# 总控层 Skill 精简验证任务

结论：验证总控层 Skill 的规则零丢失、自动触发兼容、单向路由、资产归属和物理删除；影响：验证结果决定两个旧入口能否删除；范围：manifest、inventory、trigger fixtures、验证器与任务证据；非范围：N/A + 原因：不连接任何数据库、HTTP 或非 local 服务；变化：新增 baseline、trigger、post-delete 三阶段门禁；完成标准：三个阶段均返回 `valid=true`；术语说明：baseline 是变更前冻结，trigger 是路由契约，post-delete 是删除后全链路检查；验证状态：baseline 待执行。

## 文档信息

| 字段 | 内容 |
| --- | --- |
| 来源 | `SRC-CONTROL-PLANE-20260722-001` |
| 测试 ID | `TEST-TC-001` |
| 环境 | local 文件系统与本地 Python |
| 第三方连接 | N/A + 原因：无网络和外部服务依赖 |

## 完成标准

- baseline、trigger、post-delete 均通过。
- 两个退役目录删除后没有活跃消费者。
- 自动触发 aliases、保护语义和 references 均可定位。
- 字典 `planned_missing=0`。
