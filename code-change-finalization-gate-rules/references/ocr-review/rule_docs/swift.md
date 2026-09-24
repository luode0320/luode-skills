#### Swift 代码质量
- 使用可选值时未安全解包
- 强引用循环（使用 `weak` 或 `unowned` 打破引用循环）
- 类型推断过度导致可读性差

#### 安全
- 使用 `NSKeyedUnarchiver` 解档不受信数据
- 注入风险：SQLite 查询拼接、WebView 中执行 JavaScript
- 敏感信息存储在 UserDefaults 等不安全位置

#### 并发
- 在主线程执行耗时操作
- Actor 隔离使用不当导致数据竞争

#### 性能
- 值类型与引用类型的选择不当
- 不必要的动态调度（可使用 `final` 优化）
- Force Unwrap（`!`）在非确定非空路径上
