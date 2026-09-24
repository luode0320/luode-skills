#### Astro 框架审查
- 组件 props 类型定义正确性
- Astro 特有语法（frontmatter、模板表达式）的正确使用
- Astro Island（客户端交互）的 hydration 策略合理性

#### 性能
- 不必要的客户端 JavaScript 加载（尽量使用 server-side rendering）
- 大量静态页面生成时的构建性能考虑
