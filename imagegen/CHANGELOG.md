# Changelog

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
