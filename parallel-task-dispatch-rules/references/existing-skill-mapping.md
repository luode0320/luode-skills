# 现有 Skill 并行映射表

## 可并行

- `format-review-rules`
  - 做什么：检查代码格式、缩进、空行和基础排版是否需要修正。
  - 建议：可并行，属于只读审查镜像；可和 `cleanup-format-review-rules` 的执行线程并发预审，再由主线程统一收口。
- `comment-review-rules`
  - 做什么：检查函数、方法、字段和补丁位点注释是否缺失或不合格。
  - 建议：可并行，属于只读审查镜像；可和 `comment-completion-gate-rules` / `comment-placement-granularity-rules` 的执行线程并发预审。
- `code-style-review-rules`
  - 做什么：检查局部代码风格、写法一致性和团队约定是否偏离。
  - 建议：可并行，属于只读审查镜像；可和 `code-style-consistency-rules` 的执行线程并发预审。
- `code-readability-review-rules`
  - 做什么：检查函数结构、表达顺序和局部可读性是否需要改进。
  - 建议：可并行，属于只读审查镜像；可和 `code-readability-rules` 的执行线程并发预审。
- `cleanup-format-review-rules`
  - 做什么：清理格式噪音、对齐缩进、统一空行和基础排版。
  - 建议：可并行，只要每个线程拥有不重叠的文件集。
- `comment-completion-gate-rules`
  - 做什么：补齐函数、方法、字段、补丁位点相关注释。
  - 建议：可并行，只要每个线程拥有不重叠的文件集。
- `comment-placement-granularity-rules`
  - 做什么：判断注释该补在哪里、补多细、哪些位点必须补。
  - 建议：可并行，当注释补充发生在不同文件或不同模块时。
- `syntax-check-review-rules`
  - 做什么：检查语法、类型、引用、基础编译是否正确。
  - 建议：可并行，当检查范围能按 package、模块或目录拆开时。
- `functional-validation-rules`
  - 做什么：验证功能行为、交互结果和输出是否满足需求。
  - 建议：可并行，当验证目标是独立模块或独立场景时。
- `implementation-review-rules`
  - 做什么：检查实现是否符合可读性、命名、结构、收口质量要求。
  - 建议：可并行，只要 review 范围不重叠且已指定统一收口线程。
- `implementation-review-mirror-rules`
  - 做什么：只读镜像检查实现自审是否满足实现收口要求。
  - 建议：可并行，属于只读审查镜像；可和 `implementation-review-rules` 的执行线程并发预审。
- `code-style-consistency-rules`
  - 做什么：统一代码风格、局部写法和团队约定。
  - 建议：可并行，只要每个线程处理的文件集不重叠。
- `code-readability-rules`
  - 做什么：提升函数结构、表达顺序和局部可读性。
  - 建议：可并行，只要受影响模块彼此独立。
- `skill-audit-rules`
  - 做什么：并发审计主任务是否漏触发 skill，以及已触发 skill 是否还有未执行完的规则。
  - 建议：可并行，只读审计，不改代码、不写文件，适合和主线程同时跑；只看当前轮次和主线程已声明 skill，不靠历史记忆。
- `code-placement-review-rules`
  - 做什么：审查代码落点、目录归属、层级边界和依赖方向是否合理。
  - 建议：可并行，只要每个线程检查的文件集不重叠。
- `code-placement-mirror-rules`
  - 做什么：只读镜像检查代码落点、目录归属和依赖方向是否满足归位要求。
  - 建议：可并行，属于只读审查镜像；可和 `code-placement-review-rules` 的执行线程并发预审。
- `code-review-automation-rules`
  - 做什么：自动审查当前分支提交，输出致命/严重/中等/建议问题。
  - 建议：可并行，只读审查，适合和实现线程同时跑。
- `bug-regression-risk-rules`
  - 做什么：审查 Bug 修复可能带来的回归风险、兼容性风险和验证优先级。
  - 建议：可并行，只读审查，适合和修复线程并发跑。
- `bug-regression-risk-mirror-rules`
  - 做什么：只读镜像检查 Bug 修复的回归风险和验证优先级是否满足风险识别要求。
  - 建议：可并行，属于只读审查镜像；可和 `bug-regression-risk-rules` 的执行线程并发预审。

## 条件并行

- `test-regression-rules`
  - 做什么：判断修复或改动后需要补哪些回归测试。
  - 建议：条件并行，仅在回归覆盖范围能按模块或服务稳定拆分时。
- `subagent-dispatch-rules`
  - 做什么：判断是否需要派发子代理，并定义子任务边界。
  - 建议：条件并行，它是分发器，不是执行器；应与本 skill 配合使用。
- `acceptance-criteria-rules`
  - 做什么：把“做到什么算完成”写成可验证、可测试、可复核的标准。
  - 建议：条件并行，它更适合作为前置门槛，而不是和实现同线程混跑。

## 必须串行

- `bug-root-cause-rules`
  - 做什么：定位 bug 根因、调用链和影响面。
  - 建议：必须串行，在根因和影响范围明确前不要拆并行。
- `bug-gap-rules`
  - 做什么：识别 Bug 描述中缺少的复现条件、环境信息、日志和影响范围。
  - 建议：必须串行，它负责先补齐信息缺口，再进入后续分析。
- `bug-fix-proposal-rules`
  - 做什么：形成修复方案、评估风险和备选路径。
  - 建议：必须串行，当修复方案会改同一条代码路径或共享抽象时。
- `requirement-gap-rules`
  - 做什么：识别需求描述里的缺口、歧义和未收敛项。
  - 建议：必须串行，它负责先把需求补完整，再进入后续工作。
- `requirement-boundary-rules`
  - 做什么：定义需求边界、范围、排除项和优先级。
  - 建议：必须串行，它负责为下游工作定边界。
- `api-endpoint-rules`
  - 做什么：约束 HTTP 接口、路由、方法和入口职责。
  - 建议：必须串行，接口未冻结前不要并行展开下游实现。
- `database-schema-rules`
  - 做什么：定义或修改数据库表、字段、索引和迁移顺序。
  - 建议：必须串行，schema 归属和迁移顺序未冻结前不要并行。
- `skill-compliance-gate-rules`
  - 做什么：在最终收口前检查已命中 skill 是否完整执行，补齐下一步建议。
  - 建议：必须串行，它是最终收口闸门，不适合并行跑。

## 分发建议

- review、cleanup、注释补充这类工作，只有在文件归属明确后才并行。
- 只读 review skill 可以并行检查同一批文件；真正的代码修改、注释补写、格式修正仍要按文件写入串行。
- 同一文件内的代码修改和注释修改必须串行，不能拆成多个线程同时写。
- 先做根因、契约定义、schema 决策，再分发下游任务。
- 如果两个候选 skill 都要修改同一个文件，直接收回为一个串行线程。
