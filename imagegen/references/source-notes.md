# Source notes（来源与调整记录）

## 2026-10-19：统一生图配置目录为 `~/.imagegen/`

- **来源类型**：内部更新（用户指令）
- **用户诉求**：生图配置统一放在用户目录下的 `.imagegen/`，把该目录作为唯一的生图配置目录。
- **改动落点**：
  1. `scripts/imagegen.py`：配置常量改为 `~/.imagegen/config.json`，删除 `~/.ai-hive/config.json` 回退分支；`init` 写入统一配置并合并保留已有字段。
  2. `SKILL.md`：新增「统一配置目录（唯一写入源）」小节，配置加载优先级、环境自检与凭据口径改为统一目录。
  3. `references/cli.md`、`references/error-casebook.md`、`CHANGELOG.md`：同步路径口径。
- **边界**：仅统一配置位置，不改变配置字段结构、模型优先级、多 Key 池与环境变量覆盖语义。

## 2026-10-05：新增「生成后符合度自检铁律」（内部更新通道）

- **来源类型**：内部更新（用户指令）
- **用户诉求**：生图 skill 要检查，不是生成就算完成，生成后必须检查是否符合提示词要求，不符合就继续重新修改生成新图。
- **gap 诊断**：原 `SKILL.md` 工作流第 5 步只有"出图后检查：主体、风格、构图、文本准确性、约束是否满足"，既没要求逐条给出符合度结论，也没有"不符合则重做"的闭环，执行时容易以"已生成"替代"已达标"。
- **落点与裁决**：
  1. `SKILL.md` 核心规则新增【生成后符合度自检铁律】：逐条给出 `符合 / 不符合 / 无法判定`，存在"不符合"则不得交付、须定向修改后重新生成新图（版本递增不覆盖），连续 3 轮不达标停止自动重试并交回用户。
  2. `SKILL.md` 工作流第 5/6/7 步重写为「自检硬闸门 → 不符合即重做 → 最终汇报附自检结论」。
  3. `references/prompting.md` 新增「生成后符合度自检」节，给出逐条验收清单（10 个维度）与判定处置口径；SKILL.md 只引用，不复制清单，避免双权威。
- **同域冗余扫描**：全仓 grep 相关关键词仅命中 `imagegen/SKILL.md:95` 这一处原句，无兄弟 skill 重复定义；本次已把该句升级为完整闭环，未新增交叉冗余。
- **环境依赖**：N/A（纯规则文本，无环境变量 / 配置 / 依赖安装）。
- **agent 通用性**：通用（仅约束生图流程行为，不绑定任何单一 agent 宿主）。

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
- **环境依赖登记**：AI Hive CLI 需 Python3 + requests、`sk-api-*` API Key（统一配置 `~/.imagegen/config.json` 0600 / `AI_HIVE_API_KEY` / `--api-key`）、外网；去底需 Pillow。SKILL.md 已含「环境自检」小节。
- **agent 通用性**：产物不再依赖任何单一 agent 宿主（内置出图工具按宿主名称描述）。
