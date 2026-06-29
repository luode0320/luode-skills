# Bug 域路由与让路判断

## 对外心智模型

Bug 域统一使用“现象录入 + 主动侦察 + 条件闸门 + 定位收敛”：

- Bug 域入口：`Intake（现象标准化） -> Discovery（主动侦察取证）`
- 条件步骤：`Gap（侦察后仍缺的阻断项） / Reproduction（复现）`
- 定位收敛：`Root Cause（静态定位） / Runtime Debug（运行时诊断）`
- 下游移交：`Fix Proposal -> 编码修复 -> Regression Risk -> Validation`

其中：

- `discovery` 负责主动看代码、查日志、只读连本地库比数据、理解截图，找有证据的根因候选。
- `intake` 负责把现象标准化并建立唯一 Bug 根目录入口。
- `gap` 只处理侦察后仍无法通过查代码 / 查数据解决、且会阻断定位的缺口。

## 内部默认顺序

1. `bug-intake-rules`：用户报障后先标准化现象、影响范围、期望与实际结果，建立 Bug 根目录。
2. `bug-discovery-rules`：现象清楚后，主动侦察代码、日志、本地数据与截图，形成有证据的根因候选。
3. `bug-gap-rules`：只处理侦察后仍缺、且阻断定位的信息，向用户提最少追问。
4. `bug-reproduction-rules`：在需要稳定复现路径时构造复现步骤与稳定性结论。
5. `bug-root-cause-rules`：用静态证据收敛最终根因，区分实现问题与设计问题。
6. `bug-runtime-debug-rules`：静态无法收敛、怀疑时序 / 并发 / 状态时，进入运行时诊断。
7. 根因确认后移交 `bug-fix-proposal-rules` 及后续修复、回归、验证。

## 让路与回流判断

- 用户只给一句话 / 截图：先 `intake` 标准化，再立即 `discovery` 主动侦察。
- `intake` 后准备向用户大量追问复现条件 / 日志：先让路给 `discovery`，能自己查到的不追问。
- `gap` 中“可主动查到的缺口”回流 `discovery`；只有查不到的才作为缺口阻断。
- `discovery` 已形成有证据的根因候选：转 `root-cause` 收敛，或转 `reproduction` 构造复现。
- `discovery` 怀疑时序 / 并发 / 运行期状态且静态不可收敛：转 `runtime-debug`。
- `discovery` 侦察后仍缺关键业务上下文：提最多 3 个拍板问题，再决定是否进 `gap`。

## 合并判断

不建议把 `discovery` 与 `intake` / `gap` / `root-cause` 合并：

- `intake` 是现象入口与根目录建立，不负责主动找证据。
- `discovery` 是主动取证与根因候选，不负责最终静态定位结论。
- `gap` 是缺口阻断，不应覆盖可通过侦察解决的问题。
- `root-cause` 是静态定位收敛，前提是已有足够证据，不负责从零主动取证。

## 与需求域的对称关系

- 需求域：`requirement-discovery-rules` 在追问前主动侦察资料 -> `requirement-intake-rules` 成文。
- Bug 域：`bug-intake-rules` 先记录现象 -> `bug-discovery-rules` 在追问前主动侦察证据。
- 两者共享“先侦察、再追问；只读优先、证据优先、可复用线索回写长期记忆”的原则。
