---
name: package-structure-rules
description: 当新增或修改包、目录、模块、分层结构、包名定义、文件归属或跨层引用关系时触发。负责统一代码包定义、目录分层、包职责、模块边界和依赖方向，尤其适用于 Go、Java、Node/Python 项目的结构决策；不要用它代替工具实现、接口规则或代码审查类 skill。
---

# 包结构与分层规则

只在判断“代码该落在哪一层、哪个目录、允许依赖谁”时使用这个 skill。
如果当前问题是工具函数内部怎么写、接口怎么设计、SQL 怎么写，转交对应的小 skill。

## Skill 作用与适用场景

- 决定新增代码应进入哪个包、目录或模块。
- 约束分层职责，避免目录失控和职责混杂。
- 限制跨层依赖方向，防止反向依赖和循环依赖。
- 在不同语言栈下，给出可落地的目录与包名建议。

## 自动触发信号

- 新增目录、包、模块或分层结构。
- 新增文件时不确定应放在哪一层。
- 修改包名定义、模块归属或跨层依赖关系。
- 新建公共目录、基础层、适配层或通用模块。
- 需要判断 `routes`、`controller`、`service`、`repository`、`model`、`middleware`、`config`、`constants`、`utils` 等目录职责。

## 进入后先做什么

1. 先识别当前项目语言或技术栈。
2. 再判断当前改动是入口层、业务层、数据访问层、配置层还是公共支撑层。
3. 判断是否已有稳定目录可复用，而不是先新建目录。
4. 最后确认该层允许依赖谁，不允许依赖谁。

## 默认执行流程

1. 默认先读 `references/structure-general.md`，确认分层、职责和依赖方向的通用规则。
2. 如果项目是 Go，再读 `references/go-package-layout.md`。
3. 如果项目是 Java，再读 `references/java-layer-layout.md`。
4. 如果项目是 Node 或 Python，再读 `references/node-python-module-layout.md`。
5. 输出目录归属、包职责、依赖方向和是否允许新增目录的结论。

## 权责边界与不负责事项

- 只负责代码该落在哪一层、哪个目录、是否允许跨层依赖。
- 不替代 `common-util-rules` 规定工具函数的内部实现和复用策略。
- 不替代 `api-endpoint-rules`、`database-query-rules` 等功能位点 skill 的实现细则。
- 不替代 `code-placement-review-rules` 做编码完成后的审查收口；这里是编码阶段的前置结构判断。

## 需要暂停并确认的条件

- 当前项目里已经存在多套冲突的目录分层，无法判断应跟随哪一套。
- 当前改动需要引入新的基础目录，但其职责仍说不清。
- 为了放置一个文件，打算新增过于宽泛的目录，如 `common`、`misc`、`helper`，但没有稳定边界。
- 结构调整会影响大量跨层依赖，已超出本次任务的最小必要范围。

## 执行通过 / 驳回标准

- 通过：能明确给出代码落点、目录职责、允许依赖方向和不允许跨层访问的边界。
- 驳回：目录命名含糊、职责交叉、依赖方向混乱，或把本应归属现有层的代码随意塞进新目录。

## 执行结果归档要求

- 如果本次新增了目录、调整了分层或决定了一套新的依赖方向，将结论记录到 `analysis/` 或 `review/`。
- 归档内容至少包含语言栈、目录结论、职责说明、依赖方向和暂不处理的结构问题。
- 如果只是沿用现有清晰结构且无争议，可以不单独归档。

## references 读取规则

- 默认先读 `references/structure-general.md`。
- 按语言二选一或三选一继续读：
  - Go: `references/go-package-layout.md`
  - Java: `references/java-layer-layout.md`
  - Node/Python: `references/node-python-module-layout.md`
- 不要一次性加载全部语言文件，只读当前技术栈对应的那一份。
