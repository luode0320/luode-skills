# Changelog

## 2.4.0（2026-10-19）

- **修正媒体交付通道优先级**：原规则把 `data:` URI 内联列为可用备选，并假设"主流 Electron CSP 包含 `data:`"。实测 Qoder CN 的聊天 Markdown 净化器在协议层就把 `data:`、`file:` 列入黑名单，与 CSP 无关，该假设不成立。
- **新增三档降级链**：宿主专用可视化 / 媒体通道（Qoder 用 `present_visualization`）→ 实测放行的 `data:` 内联 → 宿主本地资源协议；前一档真实成功才停。
- **补充宿主实证与止损规则**：记录 Qoder CN `harden()` 的 `blockedProtocols` 与 `src` 白名单证据；明确看到 `[Image blocked: ...]` 时不得靠缩小图片或换 base64 写法重试，应直接切第一档通道。
- **区分"提交成功"与"已渲染"**：`present_visualization` 返回成功只代表片段通过校验并保存快照，不代表客户端已渲染；交付话术不得越级断言"已展示"。
- **新增案例 IMG-007**：`references/error-casebook.md` 记录"图片已生成落盘但聊天渲染被拦截"的根因、脱敏复现输入与验证方式。

## 2.3.0（2026-10-19）

- **统一生图配置目录**：所有生图配置固定存放于 `~/.imagegen/`，主配置为 `~/.imagegen/config.json`；不再使用 `~/.ai-hive/config.json`。
- **CLI fallback 对齐**：`scripts/imagegen.py` 只从统一配置读取，删除 `~/.ai-hive/` 回退分支；`init` 写入统一配置并保留已有 `api_keys`、`model`、`model_priority` 等字段，避免覆盖多 Key 池。
- **文档同步**：`SKILL.md`、`references/cli.md`、`references/error-casebook.md` 的配置路径与凭据口径统一改为 `~/.imagegen/config.json`。

## 2.2.0（2026-10-05）

- **新增「生成后符合度自检铁律」**：明确"出图不等于任务完成"。每次生成或编辑后，必须对照用户原始提示词与本轮约束逐条给出 `符合 / 不符合 / 无法判定` 的验收结论；只要存在任何"不符合"项就不得交付，必须按不符合项定向修改提示词并重新生成新图（版本号递增、不覆盖旧版），直到全部要求符合才允许交付与汇报。
- **不符合即重做闭环**：`SKILL.md` 工作流第 5/6/7 步重写为「自检硬闸门 → 不符合即重做 → 最终汇报附自检结论」；连续 3 轮仍不达标时停止自动重试，改为向用户报告差距、已尝试修改与候选方向。
- **操作细则下沉**：`references/prompting.md` 新增「生成后符合度自检」节，提供 10 维度逐条验收清单（主体与数量 / 风格与媒介 / 构图与取景 / 颜色与配色 / 尺寸与比例 / 画面内文字 / 禁止项 / 透明底与色度键 / 参考图角色 / 输入图不可变项）与判定处置口径；SKILL.md 只引用不复制，避免双权威。

## 2.1.0（2026-09-24）

- **新一代模型升级**：新增支持 `gpt-image-2.5-sunburst`、`gpt-image-2.5-flare` 和 `gpt-image-2` 模型族。
- **画质模型优先**：建立模型梯队原则，将默认出图主力提升为画质最高、光影细节与大场景氛围最强的 `gpt-image-2.5-sunburst`；同时支持 `gpt-image-2.5-flare`（极速与金属高光版）。
- **多 API Key 密钥池与并发容灾**：
  - 配置文件 `~/.imagegen/config.json` 与环境变量支持 `api_keys: [...]` 数组。
  - 脚本内置 `ApiKeyPool`，支持多任务轮询派发与并发负载均衡。
  - 针对 429 限流错误与瞬态异常，自动执行 Key 故障转移（Failover）与指数退避重试。
- **配置解析优化**：以 `~/.imagegen/config.json` 作为核心单一真理源，解决 Windows 下守护进程缓存导致的环境变量影子覆盖问题。

## 2.0.0（2026-09-05）

- **吸收合并**：删除独立 `gpt-image-2` skill（marketplace），其 AI Hive CLI 通道（`scripts/imagegen.py`，固定 `public_model_gpt_image_2`）迁入本 skill 作为唯一 CLI fallback 通道；脚本内 `SKILL_CONFIG` 归属改为 `imagegen`。
- **去 Codex 化（agent 通用）**：删除 `codex-network.md`、`local-entrypoints.md`、`agents/openai.yaml`、`run_imagegen.ps1/.sh`、`bootstrap_imagegen_env.py`；SKILL.md 与 references 清除 `$CODEX_HOME`、`~/.codex`、`config.toml`、`gpt-image-1.5` 等痕迹；删除 OpenAI 通道 `image_gen.py`。
- **瘦身**：SKILL.md 21,050B → 10,788B（-49%）；references 7 → 5（`cli.md`+`image-api.md` 合并为 AI Hive 语义的 `cli.md`）；scripts 5 → 2。
- **规则简化**：透明底去掉"询问切 gpt-image-1.5"确认链，收敛为纯色背景 + 本地去底 + 能力说明；强阻断规则压缩为核心红线；error-casebook 旧 OpenAI 案例标 `superseded`，AI Hive 案例骨架待积累。
- 保留：`prompting.md`、`sample-prompts.md`（清路径痕迹）、`remove_chroma_key.py`（纯本地算法）、LICENSE、assets。

## 1.x（历史，Codex 生态移植版）

- 早期版本为 Codex 生态 imagegen 移植（OpenAI 通道），本次已整体切换。
