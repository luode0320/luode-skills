# 完成标记编写规范

## 目标

完成标记是长任务循环的核心协议。当 worker 的输出中包含完成标记时，控制器才认为任务真正完成，停止循环。本文件定义完成标记的格式、要求和最佳实践。

## 完成标记格式

### 推荐格式

`<promise>...</promise>`（XML 包裹式）

```
当所有任务完成时，输出以下标记：
<promise>DONE</promise>
```

优势：
- 误匹配概率低，不会与代码中的普通字符串混淆
- XML 包裹式，可携带额外信息（如 `<promise token="123">DONE</promise>`）
- 与 easy-vibe 页面推荐的写法一致

### 简洁格式

`##LOOP_DONE##`

```
当所有任务完成时，输出：
##LOOP_DONE##
```

优势：
- 简洁，适合简短任务
- 双 # 包裹，不易误匹配

### 兼容格式

`COMPLETE`（纯文本）

```
当所有任务完成且测试通过时，输出：
COMPLETE
```

优势：
- 兼容 Ralph Wiggum 生态
- 简单直观

## 标记要求

### 必须满足

1. 唯一性：标记不会在代码、注释、日志或报错中意外出现
2. 稳定性：标记在整轮循环中不变，不随迭代次数变化
3. 可见性：标记必须出现在 worker 线程的最终输出中（final 通道）
4. 独立性：标记前后可以附带汇总信息，但标记本身必须完整且可正则匹配

### 推荐命名

- 大写下划线命名：TASK_DONE、REFACTOR_COMPLETE、MIGRATION_FINISHED
- 语义清晰：标记名应反映任务类型
- 长度适中：8-30 个字符

### 禁止行为

- 使用模糊词汇（done、ok、finish 单独出现）
- 使用代码中可能出现的字符串（TODO、FIXME、true、false）
- 标记包含换行符或特殊控制字符
- 标记依赖特定的上下文（如 "All tests passed" 可能出现在测试输出中）

## 在 Goal objective 中使用

### 基本写法

```
<objective>
# 任务：重构用户认证模块

1. 将身份验证逻辑从 monolith 中提取到独立服务
2. 所有测试通过
3. 文档更新完成

当所有工作完成且测试通过后，输出：<promise>DONE</promise>
</objective>
```

### 带参数写法

```
<objective --max-iterations 100 --checkpoint-interval 20>
# 任务：从 Jest 迁移到 Vitest

...
当所有测试文件迁移完成且新测试通过后，输出：<promise>VITEST_DONE</promise>
</objective>
```

### worker prompt 模板

```
# 任务描述

<goal_objective 的正文>

# 完成条件

当所有任务完成时，输出以下标记：
<promise>DONE</promise>

# 当前进度

第 <current_iteration> 轮 / 最多 <max_iterations> 轮
上一轮已完成的：<上一轮汇总>
本轮需要继续：<未完成部分>

# 停止条件

- 不要在输出标记前停止
- 如果遇到无法解决的问题，输出 <promise>BLOCKED</promise> 并说明原因
```
