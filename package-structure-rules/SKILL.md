---
name: package-structure-rules
description: 用于判断新增或修改包、目录、模块、`main.go` 启动入口、`internal` 私有代码、`utils` / `common` / `global` / `middleware` / `crontask` / `async` 等支撑目录，以及 `router` / `controller` / `service` / `repository` / `model` 等业务目录的落点、职责和依赖方向。适用于 Go、Java、Node/Python 项目的结构决策，尤其适合判断单二进制 Go 服务中哪些代码必须留在 `internal/`，以及哪些入口层目录必须保持根级；`utils` / `common` / `global` / `middleware` 根目录默认只放子包子目录，`internal/service` 也默认先拆业务子目录再落实现文件；当单文件达到 500 行及以上且仍在扩展时，需评估按功能拆文件并在必要时拆子目录/子包；不要用它代替工具实现、接口设计或代码审查类 skill。
---

# 包结构与分层规则

只在判断“代码该放在哪里、目录怎么命名、谁能依赖谁”时使用这个 skill。
如果当前问题是工具函数怎么写、接口怎么设计、SQL 怎么写，转交对应的小 skill。

## Skill 作用与适用场景

- 判断新增代码应进入哪个包、目录或模块。
- 约束分层职责，避免目录失控和职责混杂。
- 限制跨层依赖方向，防止反向依赖和循环依赖。
- 约束 `utils` / `common` / `global` / `middleware` 采用二级子包结构，避免根目录堆实现文件。
- 约束 Go `internal/service` 采用业务子目录结构，避免在 `internal/service` 根目录堆实现文件。
- 在不同语言栈下，给出可落地的目录命名与依赖建议。
- 当单文件超过 500 行且功能持续增加时，指导按职责拆文件；业务流程足够多时，指导拆子目录/子包。

## 自动触发信号

- 新增 `main.go`、包、目录、模块或分层结构。
- 新增文件时不确定应该放在哪一层。
- 修改包名定义、模块归属或跨层依赖关系。
- 新建 `utils`、`common`、`global`、`middleware`、`crontask`、`async` 等公共或入口目录。
- 打算在 `utils`、`common`、`global`、`middleware` 根目录直接新增实现文件。
- 打算在 Go `internal/service` 根目录直接新增多个业务实现文件。
- 同一文件超过 500 行且还在持续新增方法或流程分支，不确定应如何拆分落位。
- 需要判断单二进制 Go 服务里，哪些代码默认应放进 `internal/`，哪些目录必须保持根级。
- 需要判断 `internal/chain`、`internal/wss` 这类项目私有适配层是否合规。
- 需要判断 `router`、`controller`、`service`、`repository`、`model` 等目录职责。

## 进入后先做什么

1. 先识别当前项目语言或技术栈。
2. 判断是否是前后端在一个根目录的项目：
   - 如果是前后端在一个根目录（如 admin-go/、admin-vue/），则 Go 包结构应用于后端子目录（如 admin-go/）
   - 如果是单纯的 Go 项目，则直接在项目根目录下应用本规则
3. 再判断当前改动是入口层、业务层、数据访问层、横切层、全局实例层、定时任务入口层，还是公共支撑层或私有适配层。
4. 先复用现有稳定目录，不要为了单个文件默认新建目录。
5. 对 `utils`、`common`、`global`、`middleware` 先确定子目录职责，再落实现文件。
6. 对 Go `internal/service` 先确定业务子目录（按域或能力）再落实现文件。
7. 若目标文件已达 500 行及以上，先按功能域、流程阶段和上下游边界制定拆分方案（拆文件优先，必要时拆子目录/子包）。
8. 最后确认该层允许依赖谁，不允许依赖谁。

## 默认执行流程

1. 默认先读 `references/structure-general.md`，确认跨语言通用的命名、职责和依赖方向规则。
2. 如果项目是 Go，再读 `references/go-package-layout.md`。
3. 如果项目是 Java，再读 `references/java-layer-layout.md`。
4. 如果项目是 Node 或 Python，再读 `references/node-python-module-layout.md`。
5. 输出目录归属、目录职责、依赖方向、二级子目录方案和是否允许新增目录的结论。

## 权责边界与不负责事项

- 只负责代码该落在哪一层、哪个目录、是否允许跨层依赖。
- 不替代 `common-util-rules` 规定工具函数的内部实现和复用策略。
- 不替代 `api-endpoint-rules`、`database-query-rules` 等功能位点 skill 的实现细则。
- 不替代 `code-placement-review-rules` 做编码完成后的落点复查；这里是编码阶段的前置结构判断。

## 需要暂停并确认的条件

- 当前项目里已经存在多套冲突的目录分层，无法判断应该跟随哪一套。
- 当前改动需要引入新的基础目录，但其职责仍然说不清。
- 为了放置一个文件，打算新增过于宽泛的目录，如 `misc`、`helper`、`base`，或没有边界的 `common`。
- 结构调整会影响大量跨层依赖，已超出本次任务的最小必要范围。

## 执行通过 / 驳回标准

- 通过：能明确给出代码落点、目录职责、允许依赖方向和不允许跨层访问的边界；对 500 行及以上且持续增长的文件已给出可执行拆分落位方案。
- 驳回：目录命名含糊、职责交叉、依赖方向混乱，把本应归属现有层的代码随意塞进新目录，在 `utils`、`common`、`global`、`middleware` 根目录直接放实现文件，或在 Go `internal/service` 根目录直接堆业务实现文件；或 500 行及以上文件持续堆功能却没有拆分落位方案。

## 执行结果归档要求

- 如果本次新增了目录、调整了分层或决定了一套新的依赖方向，将结论记录到 `analysis/` 或 `review/`。
- 归档内容至少包含语言栈、目录结论、职责说明、依赖方向和暂不处理的结构问题。
- 如果只是沿用现有清晰结构且无争议，可以不单独归档。

## references 读取规则

- 默认先读 `references/structure-general.md`。
- 按语言继续读取对应参考：
  - Go: `references/go-package-layout.md`
  - Java: `references/java-layer-layout.md`
  - Node/Python: `references/node-python-module-layout.md`
- 不要一次性加载全部语言文件，只读当前技术栈对应的那一份。
