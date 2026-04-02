# 命名与产出

## 1. 命名原则

新 skill 名称必须根据该新 skill 自己的 `description` 命名，而不是沿用旧 skill 名字做机械裁剪。

命名时固定抓两类信息：

1. 主触发对象：当什么对象、位点或场景变化时触发。
2. 主职责焦点：这个新 skill 主要负责什么，不负责什么。

命名约束：

- 使用最稳定、最可区分的触发对象与职责焦点。
- 保持 `kebab-case`，仅使用小写字母、数字和连字符。
- 统一以 `-rules` 结尾，且整体长度尽量控制在 64 个字符以内。
- 名称必须能脱离旧 skill 上下文被理解。

## 2. 命名步骤

1. 先写出新 skill 的完整 `description`。
2. 从 `description` 中提取主触发对象。
3. 再提取主职责焦点。
4. 按 `<trigger-object>-<focus>-rules` 生成候选名称。
5. 若有多个候选，优先选择与 `description` 语义最贴近、且最不依赖旧 skill 上下文的名称。

## 3. 命名反例

以下名称应直接回退重命名：

- 只是沿用旧 skill 前缀再硬拼一个后缀。
- `common-rules`、`misc-rules`、`other-rules` 这类过宽名称。
- 看名字像 A，`description` 实际是 B。
- 多个新 skill 名称高度近似，只能靠旧 skill 上下文才能分清。

## 4. 命名示例

示例一：

- 新 skill `description`：当新增或修改测试目录、测试文件、测试脚本落点时触发。负责统一测试基础落点规则；不要用它代替验证程序、fixture、mock 或测试说明文档落点规则。
- 推荐名称：`test-location-core-rules`

示例二：

- 新 skill `description`：当新增或修改验证程序、fixture、mock 数据落点时触发。负责统一测试支撑资源落点规则；不要用它代替测试目录、测试文件或测试脚本落点规则。
- 推荐名称：`test-support-location-rules`

示例三：

- 新 skill `description`：当旧 skill 拆分完成、准备删除旧 skill 前触发。负责核对删除前承接关系与删除条件；不要用它代替覆盖映射校验本身。
- 推荐名称：`skill-retirement-check-rules`

## 5. 新 skill 产出要求

每个新 skill 至少要完成以下产出：

- 独立的 `SKILL.md`
- 已同步的 `agents/openai.yaml`
- 按需迁移后的 `references/`
- 按需迁移后的 `scripts/` 与 `assets/`
- 明确的边界声明、通过标准与阻断条件

整轮拆分任务还必须额外产出：

- 原规则到新 skill 的覆盖映射表
- 特例规则迁移说明
- 旧 skill 删除前承接检查结论
- 旧 skill 删除动作及引用清理结果

## 6. 交付完成判定

只有当以下条件同时满足时，才算真正完成拆分：

- 新 skill 都能独立触发、独立执行、独立解释职责。
- 名称与 `description` 一一对应，不依赖旧 skill 名称补语义。
- 原规则、特例规则和资源迁移都有明确落点。
- 覆盖映射表与删除前承接检查均已完成。
- 旧 skill 已删除，且删除后不再依赖旧 skill 命中入口。
