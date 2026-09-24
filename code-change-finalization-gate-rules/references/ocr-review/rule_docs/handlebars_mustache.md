#### Handlebars/Mustache 模板正确性
- 引用了未定义的变量或 helper
- 模板语法错误（缺少闭合标签、块参数错误等）
- 部分渲染语法使用不当（如 `{{>` 的上下文传递）

#### 安全
- XSS 风险：未正确转义的变量输出。Handlebars 默认 HTML 转义，但使用 triple-stash `{{{` 时需注意
- 在模板中直接使用用户提供的 partial 名称可能导致注入

#### 性能
- helper 中执行了过重的计算或异步操作
- 不必要的大型嵌套 partial 导致渲染缓慢
