# CLI reference（`scripts/imagegen.py` — AI Hive 通道）

> 仅供 CLI fallback 模式使用。当内置出图工具不可用、或用户显式要求 CLI/API/模型参数控制时读取本文件。
> 本文件承接旧版 `image-api.md` 的职责（通道参数与模型说明），2026-09-05 合并改写为 AI Hive 语义。

## 本 CLI 做什么

- `generate`：从 prompt 生成新图，或带参考图/编辑要求出图（固定模型 `public_model_gpt_image_2`）
- `task`：查询生成任务状态并下载结果
- `upload`：上传图片获取 `mediaId`
- `init`：交互式初始化 API Key（写 `~/.ai-hive/config.json`，权限 0600）

真实 API 调用需要**外网** + 已配置的 AI Hive API Key（`sk-api-*`）。

## 快速开始

```bash
# 首次配置（浏览器引导拿 Key）
python3 "$SKILL_PATH/scripts/imagegen.py" init --skill-name imagegen

# 最简验证（--no-download 只提交不下载，返回 taskId 即成功）
python3 "$SKILL_PATH/scripts/imagegen.py" generate --prompt "test" --no-download
```

## generate 参数

| 参数 | 说明 | 默认 |
|---|---|---|
| `--prompt` | 图片描述或编辑要求 | 必填 |
| `--image` | 参考图片路径，可多张 | — |
| `--batch` | 同一 prompt 生成数量 | `1` |
| `--param key=value` | 模型参数透传，可多个 | — |
| `--routing` | `COST_FIRST` / `SPEED_FIRST` / `SUCCESS_FIRST` | `COST_FIRST` |
| `--output-dir` | 输出目录 | `~/Downloads/AiHive/` |
| `--no-download` | 只提交任务、不等待下载 | 关 |
| `--api-key` / `--base-url` / `--verbose` | 覆盖配置 / 详细日志 | — |

编辑语义：`--image` 传修改目标，prompt 里写"保留 X 不变，只改 Y"，并逐张说明参考图角色；多次迭代时重复 invariants 防止漂移。

## 模型与参数语义

- 固定模型：`public_model_gpt_image_2`（图片生成与编辑一体，参考图数量规则以实时能力为准）。
- **实时配置为准**：支持的分辨率、格式、尺寸枚举、参数 key 随平台 `imageConfig` 变化，不要在文档里写死；任务前可用一次 `--no-download` 或错误返回确认当前支持范围。
- 草稿优先低成本：小分辨率 + `--batch 1` + `COST_FIRST` 路由；正式图再按需求提分辨率/批量。
- 路由建议：默认 `COST_FIRST`；赶时间用 `SPEED_FIRST`；重要任务要求稳定可用用 `SUCCESS_FIRST`。
- `--param` 只透传模型支持的 key；传错会在任务响应中报 InvalidParameter，按实时 `imageConfig` 修正。

## 任务与计费

- 任务提交后返回 `taskId`；下载失败/超时用 `task --task-id <id>` 只查原任务，不要重新提交（避免重复扣费）。
- 价格以脚本运行时查询的实时销售价与扣费为准。
- 批量前先确认实时费用；`--no-download` 可先试成本。

## 输出与落盘

- 临时/调试文件放 `tmp/imagegen/`，正式资产按 SKILL.md「保存规则」落项目 `images/<YYYYMMDDHHMMSS>/`。
- 同一张图多轮返修用 `-v1/-v2` 版本名，不覆盖旧版。
- CLI 结果文件为 PNG/JPEG/WebP 或平台实时支持格式。

## Guardrails

- 直接用捆绑 CLI（`python3 scripts/imagegen.py ...`），不要自建一次性 wrapper。
- 不修改脚本的模型固定与通道逻辑；脚本能力不够先与用户对齐。
- 不静默把本通道替换成其他模型/平台；模型下线时查 `models` 实时列表并与用户确认。
- 透明底请求默认走"纯色背景 + `scripts/remove_chroma_key.py` 本地去底"（见 SKILL.md），本通道不支持时不要承诺原生透明。

## 常见问题

- 提示缺图片：该请求要求参考图，补 `--image`。
- 提示模型不存在：平台模型下线/更名，查实时模型列表或 `--base-url` 是否正确。
- 提示 401：检查 API Key（`init` 重配或 `--api-key`）。
- 提示 InvalidParameter：按实时 `imageConfig` 修正 `--param`/尺寸/数量。
- 任务一直 pending：保留 `taskId` 稍后 `task --task-id` 查询。
