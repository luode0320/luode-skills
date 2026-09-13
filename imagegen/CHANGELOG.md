# Changelog

## 2.0.0（2026-09-05）

- **吸收合并**：删除独立 `gpt-image-2` skill（marketplace），其 AI Hive CLI 通道（`scripts/imagegen.py`，固定 `public_model_gpt_image_2`）迁入本 skill 作为唯一 CLI fallback 通道；脚本内 `SKILL_CONFIG` 归属改为 `imagegen`。
- **去 Codex 化（agent 通用）**：删除 `codex-network.md`、`local-entrypoints.md`、`agents/openai.yaml`、`run_imagegen.ps1/.sh`、`bootstrap_imagegen_env.py`；SKILL.md 与 references 清除 `$CODEX_HOME`、`~/.codex`、`config.toml`、`gpt-image-1.5` 等痕迹；删除 OpenAI 通道 `image_gen.py`。
- **瘦身**：SKILL.md 21,050B → 10,788B（-49%）；references 7 → 5（`cli.md`+`image-api.md` 合并为 AI Hive 语义的 `cli.md`）；scripts 5 → 2。
- **规则简化**：透明底去掉"询问切 gpt-image-1.5"确认链，收敛为纯色背景 + 本地去底 + 能力说明；强阻断规则压缩为核心红线；error-casebook 旧 OpenAI 案例标 `superseded`，AI Hive 案例骨架待积累。
- 保留：`prompting.md`、`sample-prompts.md`（清路径痕迹）、`remove_chroma_key.py`（纯本地算法）、LICENSE、assets。

## 1.x（历史，Codex 生态移植版）

- 早期版本为 Codex 生态 imagegen 移植（OpenAI 通道），本次已整体切换。
