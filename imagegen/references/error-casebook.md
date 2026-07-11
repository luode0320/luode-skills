# Imagegen 错误案例库

本文件只保存已经复现、已经解决并完成本地验证的生图错误。它服务于 `imagegen/SKILL.md` 的持续迭代规则，不替代当前代码、官方 API 文档或用户当前指令。

## 使用与维护规则

- 先按错误类型和模型匹配案例，再执行解决方案；案例不匹配时不要强行套用。
- 只有解决方案通过本地 `--dry-run`、`check` 或等价验证后，案例才可标记为 `active`。
- `candidate` 只表示当轮观察结果，不是可执行规则；未解决的错误不得写成 `active`。
- 同一错误优先更新原案例；解决方案被新规则替代时保留原条目并标记为 `superseded`。
- 记录时只保留最小可复现参数摘要。禁止写入 API key、token、密码、完整 prompt、输入图片内容、完整响应体和未经脱敏的本机路径。
- 每次新增或更新案例都要补充来源和最后验证时间；无法回溯来源的案例不得进入 `active`。

## 案例字段

每条案例使用以下字段：

- `状态`：`active`、`candidate` 或 `superseded`
- `类型`：`参数`、`环境`、`鉴权`、`网络/限流`、`模型能力` 或 `输出校验`
- `适用模型`：明确模型和调用模式
- `错误特征`：可脱敏、可检索的错误摘要
- `根因`：由代码、文档或复现结果支持的判断
- `解决方案`：可执行步骤和禁止动作
- `验证`：本地验证命令或明确的验证结果
- `用户确认`：是否需要换模型、换路径或其他显式确认
- `来源`：代码或参考文档路径
- `最后验证`：日期或版本标识

## 已验证案例

### IMG-001：gpt-image-2 尺寸约束失败

- `状态`：`active`
- `类型`：`参数`
- `适用模型`：CLI fallback，`gpt-image-2`
- `错误特征`：指定尺寸的边长不是 16 的倍数、超过 3840px、长宽比超过 3:1，或总像素不在允许范围内。
- `根因`：`gpt-image-2` 使用受约束的自定义尺寸，脚本会在发起 API 请求前执行模型专属校验。
- `解决方案`：优先改用 `auto`；需要固定尺寸时同时满足最大边、16px 倍数、3:1 比例和总像素约束。不要为了绕过校验静默切换旧模型。
- `验证`：使用 `generate --dry-run` 分别验证一个合法尺寸和一个非法尺寸，非法输入必须在本地被拒绝。
- `用户确认`：仅当改用其他模型会改变能力或输出契约时需要确认。
- `来源`：`scripts/image_gen.py` 的 gpt-image-2 尺寸校验；`references/image-api.md` 的尺寸约束。
- `最后验证`：2026-07-12

### IMG-002：gpt-image-2 不接受透明背景参数

- `状态`：`active`
- `类型`：`模型能力`
- `适用模型`：CLI fallback，`gpt-image-2`
- `错误特征`：调用中使用 `background=transparent`，被本地模型校验拒绝。
- `根因`：`gpt-image-2` 不支持 Image API 的 `background=transparent`；当前默认透明流程是纯色抠图背景加本地去底。
- `解决方案`：默认使用 built-in 或 CLI `gpt-image-2` 生成纯色背景，再运行 `remove_chroma_key.py` 并校验 alpha。只有用户明确需要真透明、复杂主体不适合抠图，或本地校验失败时，才请求确认是否改用 `gpt-image-1.5`。
- `验证`：`generate --dry-run --background transparent` 必须被拒绝；纯色背景方案必须通过 alpha 校验。
- `用户确认`：切换到 `gpt-image-1.5 --background transparent --output-format png` 前必须确认。
- `来源`：`SKILL.md` 透明底规则；`scripts/image_gen.py` 的透明参数校验；`references/image-api.md`。
- `最后验证`：2026-07-12

### IMG-003：gpt-image-2 错传 input_fidelity

- `状态`：`active`
- `类型`：`参数`
- `适用模型`：CLI fallback 编辑，`gpt-image-2`
- `错误特征`：编辑命令显式传入 `input_fidelity`，或把该参数当作 gpt-image-2 的通用参数。
- `根因`：`gpt-image-2` 对图像输入固定使用高保真，不支持设置 `input_fidelity`。
- `解决方案`：删除该参数；保留模型默认高保真行为。只有使用支持该参数的旧模型时，才按对应模型文档设置。
- `验证`：使用本地示例输入执行 `edit --dry-run --input-fidelity high`，确认 gpt-image-2 被拒绝；删除参数后 dry-run 通过。
- `用户确认`：改用旧模型时需要说明能力变化并确认。
- `来源`：`scripts/image_gen.py` 的模型专属参数校验；`references/cli.md` 与 `references/image-api.md`。
- `最后验证`：2026-07-12

### IMG-004：CLI 依赖缺失

- `状态`：`active`
- `类型`：`环境`
- `适用模型`：CLI fallback
- `错误特征`：`check` 报告 `openai` 或 `PIL` 无法导入，或真实调用在依赖导入阶段失败。
- `根因`：CLI fallback 依赖本地 Python 包和入口脚本环境；这不是模型调用失败。
- `解决方案`：先运行系统入口 `check`；只缺 `openai` / `PIL` 时补齐本地依赖，再重复 `check`。不要另写一次性 SDK wrapper，也不要把程序绘图当作 fallback。
- `验证`：Windows 使用 `scripts/run_imagegen.ps1 -Action check`，Linux/macOS 使用 `scripts/run_imagegen.sh check`；dry-run 中出现的 `OPENAI_API_KEY is not set` warning 不等于真实鉴权失败，输出不得包含密钥原值。
- `用户确认`：安装依赖属于当前本地环境操作；若仍无可用鉴权或通道，必须报告 blocked。
- `来源`：`SKILL.md` CLI fallback 验证流程；`scripts/run_imagegen.ps1`；`scripts/run_imagegen.sh`。
- `最后验证`：2026-07-12

### IMG-005：CLI 无可用图像通道

- `状态`：`active`
- `类型`：`鉴权`
- `适用模型`：CLI fallback
- `错误特征`：`check` 在当前进程、项目规则文件和 Codex local 配置中都找不到可用图像通道。
- `根因`：CLI fallback 需要可用的鉴权和 base URL；built-in 路径与 CLI 配置链路不同。
- `解决方案`：按 skill 规定顺序检查当前进程环境变量、项目 `AGENTS.md` / `CLAUDE.md` 图像配置和 Codex local 配置；缺少 key 时只提示配置位置，不输出或回写 secret。确认两条生图路径都不可用后，明确标记尚未生成最终图片。
- `验证`：运行 `check`，确认只输出来源和可用性摘要，不输出 key、token 或完整连接串。
- `用户确认`：不能通过该案例自动切换到其他模型或外部服务。
- `来源`：`SKILL.md` 环境与强阻断规则；`references/local-entrypoints.md`。
- `最后验证`：2026-07-12

### IMG-006：限流或瞬态网络错误

- `状态`：`active`
- `类型`：`网络/限流`
- `适用模型`：CLI fallback，`generate-batch`
- `错误特征`：HTTP 429、rate limit、timeout、connection reset 等瞬态错误。
- `根因`：上游限流或短暂网络故障，不代表 prompt、模型参数或鉴权配置错误。
- `解决方案`：只对已识别的限流和瞬态网络错误按 `retry-after` 或指数退避重试；`generate-batch` 默认最多 3 次尝试，必要时降低并发。当前单图 `generate` / `edit` 路径不自动重试，参数错误、鉴权错误和其他非瞬态错误不得自动重试，也不得无限重试。
- `验证`：检查重试日志是否包含尝试次数和退避时间，并确认超过最大次数后任务明确失败；不得用真实线上故障作为本地验证前提。
- `用户确认`：改变模型或生图路径不属于本案例的自动解决方案，需要单独确认。
- `来源`：`scripts/image_gen.py` 的瞬态错误识别与重试逻辑；`references/cli.md` 的 batch 参数说明。
- `最后验证`：2026-07-12

## 回写检查清单

新增或更新案例前，必须确认：

1. 错误已复现，且根因有代码、文档或运行证据支持。
2. 解决方案已通过本地验证，未把静态猜测写成 `active`。
3. 错误摘要、命令和路径已脱敏，未包含凭据或用户私有内容。
4. 已按案例 ID、错误特征和适用模型去重，并更新来源与最后验证时间。
