---
name: codex-custom-models
description: 为 Codex Desktop（含 Windows CLI）维护 luode.vip 中转的自定义模型目录。触发场景：用户说"更新 codex 模型 / 给 codex desktop 加模型 / 模型切换 / 模型清单(models.json)更新了 / 把 luode 模型同步到 codex"。流程：读源清单 D:\谷歌云盘\workbuddy-model\models.json → 生成 Codex catalog（ModelsResponse/ModelInfo schema）→ 写 ~/.codex/model-catalog.json + 云盘镜像 → 校验（TOML 语法 + base_instructions 必填 + 引擎连通测试）→ 提醒重启 Codex Desktop。沉淀了完整机制与坑：model_catalog_json 顶层键、官方目录在 codex-rs/models-manager/models.json、wire_api 仅支持 responses、catalog 条目必须含 base_instructions 或 model_messages.instructions_template、引擎运行模式（runCodexInWindowsSubsystemForLinux 决定 WSL/Windows 原生）决定 model_catalog_json 路径写法（/mnt/c vs C:\，写错即 os error 2/"配置加载未成功"）、provider 认证会被 App 改写为 http_headers 内联 key（此时不需环境变量；若仍 env_key 则 WSL 引擎拿不到 Windows 用户环境变量报 Missing environment variable）。含生成模板脚本 scripts/generate_catalog.py。
---

# Codex Desktop 自定义模型目录（luode.vip 中转）

> 目标：让 Codex Desktop 的模型选择器列出并可切换 luode.vip 中转的全部模型（含非 OpenAI 的 glm/kimi/deepseek/qwen/doubao/hy4 等）。
> 本 skill 含**本机环境事实**（集中见文末"环境事实"段，未来路径变动只改该段）；代码/知识层为可迁移通用内容。

## 机制速览（避免重新考古）

- Codex 模型列表由 **active catalog** 驱动（源码 `codex-rs/models-manager`）；内置目录编译进二进制，无法直接改。
- config 顶层键 **`model_catalog_json`**（文件路径）注入自定义目录，供桌面与 CLI 共用。
- catalog 文件 schema = **`ModelsResponse`**：顶层 `{"models": [ <ModelInfo>... ]}`（与官方 `codex-rs/models-manager/models.json` 同构）。
- `ModelInfo` 大多数字段带 `serde(default)` 可省略，但**至少满足一条**：含 `base_instructions` 或 `model_messages.instructions_template`，否则加载报错 `model X is missing both base_instructions and model_messages.instructions_template`。
- `wire_api` 仅支持 `"responses"`；写 `"chat"` 会被直接拒绝加载。
- 第三方模型建议用中性 `base_instructions`（不要复制 GPT 的 `model_messages`，否则模型自认是 GPT）。

## 标准步骤

### 1. 读源清单
- 源 = `D:\谷歌云盘\workbuddy-model\models.json`（用户维护的真源，字段含 id/name/vendor/url/apiKey/supportsToolCall/maxInputTokens/reasoning.supportedEfforts）。
- 比对中转实际可用模型：`GET {base_url}/v1/models`（带 key）——catalog 只应含中转真实支持的 slug，防止选到 404 模型。

### 2. 生成 Codex catalog
- 运行 `scripts/generate_catalog.py`（默认读上述 models.json，输出 `~/.codex/model-catalog.json` 并镜像回云盘 `codex-model-catalog.json`）。
- 转换要点：
  - slug / display_name 用中转模型 id（与 `/v1/models` 一致）。
  - `context_window` / `max_context_window`：第三方按用户 models.json 的 `maxInputTokens`（通常 262144）；GPT 系（luna/sol/terra/astra）可用官方条目基底 + 用户要求的窗口（如 400000，见环境事实）。
  - `default_reasoning_level` = 用户 models.json `reasoning.defaultEffort`（当前 high）；`supported_reasoning_levels` 与用户 `supportedEfforts` 集合对齐（low/medium/high/xhigh/max）。
  - 能力标记（verbosity/websocket/reasoning summary/apply_patch 等）**以官方 gpt-5.6-luna 条目为基底**——它是 luode.vip 全链路实测兼容的配置；不要凭空捏造字段。
  - `visibility = "list"`（出现在 picker）、`supported_in_api = true`、`priority` 决定排序。
  - 4 个 GPT slug（gpt-6-astra / gpt-5.6-sol / gpt-5.6-terra / gpt-5.6-luna）官方条目可直接复用（从现 catalog 或官方 models.json 抽取）。

### 3. 写入配置
- 先判定引擎运行模式（**决定 catalog 路径写法，写错必 os error 2**）：
  ```bash
  grep runCodexInWindowsSubsystemForLinux ~/.codex/config.toml
  ```
  - `= true`（WSL 引擎）：路径必须 **WSL 视角** `/mnt/c/Users/luode/.codex/model-catalog.json`；
  - `= false`（Windows 原生引擎）：路径必须 **Windows 视角** `C:\\Users\\luode\\.codex\\model-catalog.json`。
- 确认 `~/.codex/config.toml` 顶层含（**路径按上面判定写，不要照抄**）：
  ```toml
  model_catalog_json = "<按引擎模式选定的路径>"
  ```
- 若该行缺失/被桌面 App 重写掉，追加即可（App 重写 config 时保留未知表，实测不丢）。
- **provider 认证由桌面 App UI 管理**：App 在 apikey 模式下会把 custom provider 的 key 改写为 `http_headers = { Authorization = "Bearer sk-..." }` 内联（此时**不需要** OPENAI_API_KEY 环境变量）；若 App 未改写、配置仍是 `env_key = "OPENAI_API_KEY"`，则 Windows/WSL 引擎都**只认该环境变量**且不回退 auth.json——此时必须保证进程环境里有它（WSL 引擎默认没有，见坑#9）。
- 全局窗口/压缩键（如 `model_context_window`、`model_auto_compact_token_limit`）是 override，会作用于所有模型，改模型窗口时注意同步。

### 4. 校验（不可跳步）
```bash
# a) 语法与结构
python -c "import tomllib; c=tomllib.load(open(r'C:\Users\luode\.codex\config.toml','rb')); print(c['model_catalog_json'])"
python -c "import json; d=json.load(open(r'C:\Users\luode\.codex\model-catalog.json',encoding='utf-8')); print('models:',len(d['models']))"
# b) 必填字段（缺 base_instructions/model_messages 会报错）
python -c "
import json; d=json.load(open(r'C:\Users\luode\.codex\model-catalog.json',encoding='utf-8'))
bad=[m['slug'] for m in d['models'] if not m.get('base_instructions') and not (m.get('model_messages') or {}).get('instructions_template')]
assert not bad, bad; print('instructions-ok')"
# c) WSL 引擎连通（模拟桌面引擎视角，最接近真实）
#    引擎二进制 ~/.codex/bin/wsl/<hash>/codex（hash 会变，动态取最新）
WSLCODEX=$(ls -d /mnt/c/Users/luode/.codex/bin/wsl/*/ 2>/dev/null | sort | tail -1)
wsl.exe -e bash -lc "export CODEX_HOME=/mnt/c/Users/luode/.codex; export OPENAI_API_KEY='<key>'; $WSLCODEX/codex exec --skip-git-repo-check --sandbox read-only --dangerously-bypass-approvals-and-sandbox -m glm-5.3 -c model_reasoning_effort=low 'Reply OK'"
```
- 抽测至少一个第三方模型（glm/deepseek 等）；返回正常即 catalog 被引擎正确加载。

### 5. 收尾
- 提醒用户**完全退出并重启 Codex Desktop**（旧引擎进程不重读 config，是"改了没生效"的第一嫌疑）。

## 已沉淀的坑（改动前先读）

1. **`wire_api = "chat"` 已被废弃**（codex 0.153.x 起）：config 加载直接报 `no longer supported`，必须 `"responses"`。luode.vip 支持 responses 端点。
2. **引擎运行模式有两种，且 App 设置可切换**（config 中 `runCodexInWindowsSubsystemForLinux`）：WSL 引擎（Linux 二进制 `~/.codex/bin/wsl/<hash>/codex`）与 Windows 原生引擎（`codex.exe`）。磁盘 config.toml 中**文件系统路径必须匹配当前引擎视角**：
   - WSL 模式：`/mnt/c/...`（写成 `C:\...` → 桌面报 `无法加载 config.toml / No such file or directory (os error 2)`）；
   - Windows 原生模式：`C:\...`（写成 `/mnt/c/...` → 同样 os error 2，表现为"配置加载未成功"）。
   - App 在两种模式间切换后**不会自动改写 model_catalog_json**——排查"配置加载未成功"先查该键路径与引擎模式是否匹配。
3. **provider 认证随 App UI 改写**：apikey 模式下 App 可能把 `env_key` 替换为 `http_headers.Authorization` 内联 key（此时不依赖任何环境变量，最省心）；若仍是 `env_key = "OPENAI_API_KEY"`，则**只认该环境变量、不回退 auth.json**，且 **WSL 引擎默认拿不到 Windows 用户环境变量**（需 WSLENV 白名单，App 白名单不含它）→ 报 `Missing environment variable: OPENAI_API_KEY`。此时要么改回 http_headers 内联（推荐，让 App UI 管理），要么在 WSL Linux 侧持久化该变量。
4. **model_catalog_json 按进程 CWD/原样解析**：不支持相对路径、不 join CODEX_HOME（实测从别的 cwd 传 `model-catalog.json` 失败）。
5. **catalog 条目必须含指令**：`base_instructions` 或 `model_messages.instructions_template` 至少其一（见标准步骤 2）。
6. **catalog 解析是 eager 的**：文件缺失/格式错会直接 fatal（CLI/引擎启动即崩），不会静默降级——改完务必跑校验步骤 4。
7. **桌面 App 会重写 config.toml**（读-改-写、保留未知表、把部分路径规范化为 /mnt/c 或 \\?\ 前缀），但**不会主动补** model_catalog_json——改动 config 前先 `cp config.toml config.toml.bak-$(date +%Y%m%d-%H%M%S)`。
8. 曾尝试 `C:\mnt\c` junction→`C:\` 让 Windows CLI 也能解析 `/mnt/c`，但 `C:\mnt\c` 是桌面 App 在用的插件镜像目录，**不可动**，已弃用该路线。
9. **Windows 用户环境变量不自动进 WSL**（仅 WSLENV 白名单变量随 `wsl.exe` 传入；App 注入引擎的白名单只有 CODEX_* / SKY_* / NODE_REPL_* 等）——任何"给 Windows setx 了变量但 WSL 引擎说缺失"的现象都是这个原因。
10. App 切换引擎模式后可能出现一次性引导 **"完成 Windows 设置 / setup_failed"**——这是 **Elevated sandbox 提权安装**（引擎调 `~/.codex/bin/<hash>/codex-windows-sandbox-setup.exe`，需 UAC 点"是"；该 exe 是 base64 payload 的 helper，**不能裸跑**）。重试多次仍 failed 的官方降级路径：config.toml 追加 `[windows]` 表 + `sandbox = "unelevated"`（RestrictedToken 受限令牌模式，**无需提权**；等价于引导页"继续受限访问"的持久化；键名拼写 kebab-case，出自源码 `WindowsSandboxModeToml`）。设置后引导不再要求提权。要完整 elevated 沙箱则需在引导页点"重试"并确认 UAC"是"。

## 环境事实（本机专属，改路径只动这段）

- 中转：`https://api.luode.vip/v1`（wire_api=responses，/v1/models 可列出真实支持模型）。
- API key：环境变量 `OPENAI_API_KEY`（用户级 setx 持久化）；也存在于 `~/.codex/auth.json`。
- 源清单：`D:\谷歌云盘\workbuddy-model\models.json`；生成脚本副本：`D:\谷歌云盘\workbuddy-model\gen_codex_catalog.py`；catalog 镜像：`D:\谷歌云盘\workbuddy-model\codex-model-catalog.json`。
- 生效配置：`~/.codex/config.toml`（键 model_catalog_json、model_provider=custom、model_context_window=400000、model_auto_compact_token_limit=200000、model_reasoning_effort=xhigh）。
- **引擎模式现状（2026-09-06 确认）**：`runCodexInWindowsSubsystemForLinux = false`（Windows 原生引擎），`model_catalog_json` 用 Windows 路径 `C:\Users\luode\.codex\model-catalog.json`；provider key 由 App 写为 `http_headers.Authorization` 内联，**不再依赖 OPENAI_API_KEY 环境变量**。若该开关被 App 切回 true，路径需同步改回 `/mnt/c/...`。
- **沙箱策略（用户已确认）**：用户默认给 Codex 全权限（`approval_policy=never` + `sandbox_mode=danger-full-access`），Windows 沙箱组件维持 `[windows] sandbox = "unelevated"`，**不追求 elevated 完整安装**——引导页 setup_failed 无需再处理。
- catalog：`~/.codex/model-catalog.json`。
- 桌面引擎：`~/.codex/bin/wsl/<hash>/codex`（Linux 二进制，hash 随版本变化）。
- 官方模型目录（基底来源，可选联网）：`codex-rs/models-manager/models.json` in github.com/openai/codex。
