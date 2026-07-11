# Imagegen 错误案例库

本文件只保存已经复现、已经解决并完成本地验证的生图错误。它服务于 `imagegen/SKILL.md` 的持续迭代规则，不替代当前代码、官方 API 文档或用户当前指令。

- **Owner Skill**：`imagegen`
- **统一路由**：`prevent`（调用前命中 `active`）、`recover`（失败后诊断和复验）、`learn`（验证后写入 `candidate`）
- **案例归属**：每条案例只能由一个 owner Skill 维护；跨领域经验使用引用，不复制正文。
- **字段映射**：本文件的中文字段与元 Skill 案例模板一一对应：`案例 ID=id`、`状态=status`、`失败阶段=mode`、`类型=category`、`环境/版本=environment/tool_or_model`、`错误特征=error_signature`、`最小复现输入=minimal_input`、`根因=root_cause`、`解决方案=solution`、`验证=verification`、`适用边界=scope`、`禁止动作=avoid`、`授权=authorization`、`来源=source`、`发生次数/首次观察/最后验证=occurrences/first_observed/last_verified`、`替代关系=replaces`。

## 使用与维护规则

- 先按错误类型、模型、调用模式和根因匹配案例，再执行解决方案；案例不匹配时不要强行套用。
- 解决方案必须用同一输入和同一成功标准通过本地 `--dry-run`、`check` 或等价验证，才允许写入 `candidate`；仅退出码为 0 不算验证完成。
- `active` 是唯一可在 `prevent` 中自动执行的状态；`candidate` 只表示已验证但待晋级的候选，`conflicted` 表示与现有方案或 owner 归属冲突，`stale` 表示暂不推荐但仍保留历史价值，`superseded` 表示已被新方案替代，`rejected` 表示未通过复用或安全门禁。
- `active` 晋级必须满足：根因确认、同输入复验、唯一 owner、脱敏、去重和可复用边界明确，并且有至少两次独立复现或确定性的官方/代码证据；同时需要当前任务的 skill 维护授权。
- 同一错误优先更新原案例；新方案与现有 `active` 冲突时先保留为 `candidate`，验证并获授权后再将旧条目标为 `superseded`，无法证明优于旧方案的候选标为 `rejected`。
- 记录时只保留最小可复现参数摘要。禁止写入 API key、token、密码、完整 prompt、输入图片内容、完整响应体和未经脱敏的本机路径。
- 每次新增或更新案例都要补充来源和最后验证时间；无法回溯来源的案例不得进入 `active`。

## 案例字段

新增或更新案例使用以下统一字段；历史条目保留原有事实，下一次维护时按此模板补齐：

- `案例 ID`：稳定且唯一，例如 `IMG-001`
- `状态`：`candidate`、`active`、`conflicted`、`stale`、`superseded` 或 `rejected`
- `类型`：`参数`、`环境`、`鉴权`、`网络/限流`、`模型能力` 或 `输出校验`
- `失败阶段`：`prevent`、`recover` 或 `learn`
- `环境/版本`：运行侧、入口脚本版本和模型版本摘要
- `适用模型`：明确模型和调用模式
- `错误特征`：可脱敏、可检索的错误摘要
- `最小复现输入`：不含私有 prompt 或输入图片的最小参数摘要
- `根因`：由代码、文档或复现结果支持的判断
- `解决方案`：可执行步骤和禁止动作
- `验证`：使用同一输入和成功标准的本地验证命令或明确结果
- `适用边界`：何时适用，何时转交相邻 Skill
- `授权`：候选回写和 active 晋级所依据的当前任务授权
- `发生次数`、`首次观察`、`最后验证`：演进审计信息
- `替代关系`：替代或被替代的案例 ID；无则写 `无`
- `用户确认`：是否需要换模型、换路径或其他显式确认
- `来源`：代码或参考文档路径

案例写入前必须完成根因、复验、脱敏、去重和唯一 owner 检查；未满足时只保留当轮诊断，不写入案例库。

## 已验证案例

### IMG-001：gpt-image-2 尺寸约束失败

- `案例 ID`：`IMG-001`
- `失败阶段`：`recover`
- `状态`：`active`
- `类型`：`参数`
- `适用模型`：CLI fallback，`gpt-image-2`
- `环境/版本`：CLI fallback，当前入口脚本及 `gpt-image-2` 参数校验
- `错误特征`：指定尺寸的边长不是 16 的倍数、超过 3840px、长宽比超过 3:1，或总像素不在允许范围内。
- `最小复现输入`：`generate --dry-run` 搭配一个不满足尺寸约束的 `size`
- `根因`：`gpt-image-2` 使用受约束的自定义尺寸，脚本会在发起 API 请求前执行模型专属校验。
- `解决方案`：优先改用 `auto`；需要固定尺寸时同时满足最大边、16px 倍数、3:1 比例和总像素约束。不要为了绕过校验静默切换旧模型。
- `验证`：使用 `generate --dry-run` 分别验证一个合法尺寸和一个非法尺寸，非法输入必须在本地被拒绝。
- `用户确认`：仅当改用其他模型会改变能力或输出契约时需要确认。
- `适用边界`：只处理本地尺寸校验；鉴权、网络和输出内容问题转交对应案例。
- `禁止动作`：不要为了绕过校验静默切换旧模型或修改脚本约束。
- `授权`：历史已验证案例；后续状态变更遵循当前任务 skill 维护授权。
- `发生次数`：1
- `首次观察`：2026-07-12
- `替代关系`：无
- `来源`：`scripts/image_gen.py` 的 gpt-image-2 尺寸校验；`references/image-api.md` 的尺寸约束。
- `最后验证`：2026-07-12

### IMG-002：gpt-image-2 不接受透明背景参数

- `案例 ID`：`IMG-002`
- `失败阶段`：`recover`
- `状态`：`active`
- `类型`：`模型能力`
- `适用模型`：CLI fallback，`gpt-image-2`
- `环境/版本`：CLI fallback，`gpt-image-2` 模型参数校验
- `错误特征`：调用中使用 `background=transparent`，被本地模型校验拒绝。
- `最小复现输入`：`generate --dry-run --background transparent`
- `根因`：`gpt-image-2` 不支持 Image API 的 `background=transparent`；当前默认透明流程是纯色抠图背景加本地去底。
- `解决方案`：默认使用 built-in 或 CLI `gpt-image-2` 生成纯色背景，再运行 `remove_chroma_key.py` 并校验 alpha。只有用户明确需要真透明、复杂主体不适合抠图，或本地校验失败时，才请求确认是否改用 `gpt-image-1.5`。
- `验证`：`generate --dry-run --background transparent` 必须被拒绝；纯色背景方案必须通过 alpha 校验。
- `用户确认`：切换到 `gpt-image-1.5 --background transparent --output-format png` 前必须确认。
- `适用边界`：只处理透明参数能力差异；本地抠图边缘问题转交输出校验路径。
- `禁止动作`：不得未经确认静默切换模型或把程序绘图当作 fallback。
- `授权`：历史已验证案例；后续状态变更遵循当前任务 skill 维护授权。
- `发生次数`：1
- `首次观察`：2026-07-12
- `替代关系`：无
- `来源`：`SKILL.md` 透明底规则；`scripts/image_gen.py` 的透明参数校验；`references/image-api.md`。
- `最后验证`：2026-07-12

### IMG-003：gpt-image-2 错传 input_fidelity

- `案例 ID`：`IMG-003`
- `失败阶段`：`recover`
- `状态`：`active`
- `类型`：`参数`
- `适用模型`：CLI fallback 编辑，`gpt-image-2`
- `环境/版本`：CLI fallback 编辑参数校验
- `错误特征`：编辑命令显式传入 `input_fidelity`，或把该参数当作 gpt-image-2 的通用参数。
- `最小复现输入`：`edit --dry-run --input-fidelity high`
- `根因`：`gpt-image-2` 对图像输入固定使用高保真，不支持设置 `input_fidelity`。
- `解决方案`：删除该参数；保留模型默认高保真行为。只有使用支持该参数的旧模型时，才按对应模型文档设置。
- `验证`：使用本地示例输入执行 `edit --dry-run --input-fidelity high`，确认 gpt-image-2 被拒绝；删除参数后 dry-run 通过。
- `用户确认`：改用旧模型时需要说明能力变化并确认。
- `适用边界`：只处理模型参数契约；输入图不可读或输出校验失败转交对应路径。
- `禁止动作`：不要通过自建 wrapper 强行注入被模型拒绝的参数。
- `授权`：历史已验证案例；后续状态变更遵循当前任务 skill 维护授权。
- `发生次数`：1
- `首次观察`：2026-07-12
- `替代关系`：无
- `来源`：`scripts/image_gen.py` 的模型专属参数校验；`references/cli.md` 与 `references/image-api.md`。
- `最后验证`：2026-07-12

### IMG-004：CLI 依赖缺失

- `案例 ID`：`IMG-004`
- `失败阶段`：`recover`
- `状态`：`active`
- `类型`：`环境`
- `适用模型`：CLI fallback
- `环境/版本`：系统入口脚本 `check`，本地 Python 依赖
- `错误特征`：`check` 报告 `openai` 或 `PIL` 无法导入，或真实调用在依赖导入阶段失败。
- `最小复现输入`：运行系统入口的 `check` 子命令
- `根因`：CLI fallback 依赖本地 Python 包和入口脚本环境；这不是模型调用失败。
- `解决方案`：先运行系统入口 `check`；只缺 `openai` / `PIL` 时补齐本地依赖，再重复 `check`。不要另写一次性 SDK wrapper，也不要把程序绘图当作 fallback。
- `验证`：Windows 使用 `scripts/run_imagegen.ps1 -Action check`，Linux/macOS 使用 `scripts/run_imagegen.sh check`；dry-run 中出现的 `OPENAI_API_KEY is not set` warning 不等于真实鉴权失败，输出不得包含密钥原值。
- `用户确认`：安装依赖属于当前本地环境操作；若仍无可用鉴权或通道，必须报告 blocked。
- `适用边界`：只处理本地依赖；鉴权来源不可用转交 IMG-005。
- `禁止动作`：不要另写一次性 SDK wrapper，也不要用程序绘图冒充真实生图。
- `授权`：历史已验证案例；后续状态变更遵循当前任务 skill 维护授权。
- `发生次数`：1
- `首次观察`：2026-07-12
- `替代关系`：无
- `来源`：`SKILL.md` CLI fallback 验证流程；`scripts/run_imagegen.ps1`；`scripts/run_imagegen.sh`。
- `最后验证`：2026-07-12

### IMG-005：CLI 无可用图像通道

- `案例 ID`：`IMG-005`
- `失败阶段`：`recover`
- `状态`：`active`
- `类型`：`鉴权`
- `适用模型`：CLI fallback
- `环境/版本`：当前进程、项目规则文件和 Codex local 配置链路
- `错误特征`：`check` 在当前进程、项目规则文件和 Codex local 配置中都找不到可用图像通道。
- `最小复现输入`：运行 `check` 并读取来源摘要，不输出密钥原值
- `根因`：CLI fallback 需要可用的鉴权和 base URL；built-in 路径与 CLI 配置链路不同。
- `解决方案`：按 skill 规定顺序检查当前进程环境变量、项目 `AGENTS.md` / `CLAUDE.md` 图像配置和 Codex local 配置；缺少 key 时只提示配置位置，不输出或回写 secret。确认两条生图路径都不可用后，明确标记尚未生成最终图片。
- `验证`：运行 `check`，确认只输出来源和可用性摘要，不输出 key、token 或完整连接串。
- `用户确认`：不能通过该案例自动切换到其他模型或外部服务。
- `适用边界`：只处理鉴权和通道可用性；依赖导入错误转交 IMG-004。
- `禁止动作`：不得输出或回写 key、token、连接串原值，也不得切到 test/prod 通道。
- `授权`：历史已验证案例；后续状态变更遵循当前任务 skill 维护授权。
- `发生次数`：1
- `首次观察`：2026-07-12
- `替代关系`：无
- `来源`：`SKILL.md` 环境与强阻断规则；`references/local-entrypoints.md`。
- `最后验证`：2026-07-12

### IMG-006：限流或瞬态网络错误

- `案例 ID`：`IMG-006`
- `失败阶段`：`recover`
- `状态`：`active`
- `类型`：`网络/限流`
- `适用模型`：CLI fallback，`generate-batch`
- `环境/版本`：CLI fallback 批量生成重试逻辑
- `错误特征`：HTTP 429、rate limit、timeout、connection reset 等瞬态错误。
- `最小复现输入`：批量生成请求触发可识别的瞬态错误分类
- `根因`：上游限流或短暂网络故障，不代表 prompt、模型参数或鉴权配置错误。
- `解决方案`：只对已识别的限流和瞬态网络错误按 `retry-after` 或指数退避重试；`generate-batch` 默认最多 3 次尝试，必要时降低并发。当前单图 `generate` / `edit` 路径不自动重试，参数错误、鉴权错误和其他非瞬态错误不得自动重试，也不得无限重试。
- `验证`：检查重试日志是否包含尝试次数和退避时间，并确认超过最大次数后任务明确失败；不得用真实线上故障作为本地验证前提。
- `用户确认`：改变模型或生图路径不属于本案例的自动解决方案，需要单独确认。
- `适用边界`：只适用于已识别的限流或瞬态网络失败；参数、鉴权和模型能力错误不得套用。
- `禁止动作`：单图路径不得无限重试，也不得把真实线上故障作为本地验证前提。
- `授权`：历史已验证案例；后续状态变更遵循当前任务 skill 维护授权。
- `发生次数`：1
- `首次观察`：2026-07-12
- `替代关系`：无
- `来源`：`scripts/image_gen.py` 的瞬态错误识别与重试逻辑；`references/cli.md` 的 batch 参数说明。
- `最后验证`：2026-07-12

## 回写检查清单

新增或更新案例前，必须确认：

1. 错误已复现，且根因有代码、文档或运行证据支持。
2. 解决方案已通过本地验证，未把静态猜测写成 `active`。
3. 错误摘要、命令和路径已脱敏，未包含凭据或用户私有内容。
4. 已按案例 ID、错误特征和适用模型去重，并更新来源与最后验证时间。
5. 已记录唯一 owner、失败阶段、最小复现输入、适用边界和禁止动作。
6. `candidate` 与现有 `active` 冲突时先标为 `conflicted`，未直接覆盖；状态变更和 `active` 晋级有当前任务授权。
