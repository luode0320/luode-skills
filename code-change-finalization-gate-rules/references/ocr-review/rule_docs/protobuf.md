#### Protobuf 定义正确性
- 字段编号冲突或重用
- 破坏向后兼容性的字段号/类型变更
- 缺少必要的 package 声明

#### 编码规范
- 字段命名不符合 Protobuf 风格（snake_case）
- 消息命名规范（PascalCase）
- 枚举值必须有零值

#### 性能
- 使用过多的 optional 字段或 oneof
- 深层次嵌套的 message 结构
