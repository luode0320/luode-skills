# Source notes（来源与调整记录）

## 2026-09-05：imagegen 吸收 gpt-image-2（AI Hive 通道）+ 去 Codex 化重构

- **来源类型**：内部更新 + 外部吸收（本地安装源模式）
- **外部源**：`gpt-image-2` skill（marketplace，skillId `skill_2087496107183259648`，v1.0.0，AI Hive OpenAPI 裸接口包装，固定 `public_model_gpt_image_2`）。吸收完成后本地安装目录已删除。
- **用户诉求**：图片生成规则"不好"——Codex 专属内容多、通道混乱不实用、规则过严/过时、太臃肿；要求合并后 imagegen 保持单一权威入口。
- **吸收条目**：
  1. AI Hive CLI 通道（generate/task/upload/init + `--param`/`--routing`/`--batch`）→ `scripts/imagegen.py`（SKILL_CONFIG 归属改为 imagegen）
  2. CLI 参数速查 → 精简入 SKILL.md「CLI fallback 通道」节 + `references/cli.md`
  3. 提示词结构/图片文字/参考图角色/电商场景 → `保留本地`（prompting.md 已有且更强，不重复吸收）
  4. 产品化文档形态 → `拒绝`（形态非规则精华）
- **内部更新（逐文件去留）**：
  - SKILL.md：重写，21,050B → 10,788B
  - `references/cli.md`：改写为 AI Hive 语义（承接 image-api.md 职责，后者删除）
  - `references/error-casebook.md`：精简为 AI Hive 语义，旧 OpenAI 案例标 superseded
  - `references/prompting.md` / `sample-prompts.md`：清除 Codex 路径与 gpt-image-1.5 痕迹
  - 删除：`codex-network.md`、`local-entrypoints.md`、`image-api.md`、`image_gen.py`、`bootstrap_imagegen_env.py`、`run_imagegen.ps1/.sh`、`agents/openai.yaml`
  - 保留：`remove_chroma_key.py`、`prompting.md`、`sample-prompts.md`、`config.example.json`、LICENSE、assets
- **环境依赖登记**：AI Hive CLI 需 Python3 + requests、`sk-api-*` API Key（`~/.ai-hive/config.json` 0600 / `AI_HIVE_API_KEY` / `--api-key`）、外网；去底需 Pillow。SKILL.md 已含「环境自检」小节。
- **agent 通用性**：产物不再依赖任何单一 agent 宿主（内置出图工具按宿主名称描述）。
