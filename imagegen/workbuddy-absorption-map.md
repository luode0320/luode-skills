# Absorption map（吸收裁决登记）

| 日期 | 来源 | 条目 | 本地现状 | 裁决 | agent 通用性 | 落点 | 整理去重 |
|---|---|---|---|---|---|---|---|
| 2026-09-05 | gpt-image-2 (marketplace skill_2087496107183259648, AI Hive GPT Image 2) | AI Hive CLI 通道（generate/task/upload/init，固定 public_model_gpt_image_2，COST_FIRST） | imagegen 原 CLI 为 OpenAI 生态（image_gen.py），无真实可用 key | 合并 | 通用（仅依赖 requests + sk-api-*） | scripts/imagegen.py 迁入；SKILL.md「CLI fallback 通道」节 | 旧 OpenAI 通道 5 文件全删；references 7→5 |
| 2026-09-05 | 同上 | CLI 参数速查表 | 无对应表 | 合并 | 通用 | SKILL.md 参数表 + references/cli.md | cli.md 承接 image-api.md 职责 |
| 2026-09-05 | 同上 | 提示词结构/图片文字/参考图角色/电商场景 | prompting.md/sample-prompts.md 已覆盖且更强 | 保留本地 | — | 不吸收 | prompting.md/sample-prompts.md 清 CODEX_HOME 路径痕迹 |
| 2026-09-05 | 同上 | 产品化文档形态（FAQ/子命令大全） | 形态非规则精华 | 拒绝（形态） | — | 不吸收 | 仅借鉴 FAQ 写法入 cli.md |

**同域冗余扫描（2026-09-05）**：扫描范围 imagegen + 图片生成同域（.system/imagegen 官方快照、buddy-image-processing、2D 素材设计/生产 skill）。发现：SKILL.md 内 `<skill-dir>` 路径写法与 prompting/sample-prompts 统一一致；gpt-image-2 独立目录删除后无散落产物；引用链可达。清理 0 处残留冗余。结论 PASS。

**官方快照清理（2026-09-05 收尾）**：`.system/imagegen`（WorkBuddy 官方 8/10 快照，旧版 SKILL.md 24KB）已按用户指令删除，仓库根 `imagegen/`（重构版 10.8KB）成为图片生成域唯一入口。`.system/` 下其余官方快照（openai-docs、plugin-creator、review-agent、skill-creator、skill-installer）保留不受影响。注：若宿主启动时自动重建 `.system` 快照，需在宿主侧确认官方快照管理策略。
