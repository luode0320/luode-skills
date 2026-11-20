# 升级手册

本文件是 pojia 语料的升级登记簿与操作口径。每次升级必须在这里留一行，保证「这份语料是什么时候、从哪个版本、改了什么」可追溯。

## 版本锚点

| 项 | 值 |
|---|---|
| 上游仓库 | `https://github.com/togg53192-cmd/jailbreaks` |
| 锚点方式 | 锁定 commit sha（**不锁分支名**，上游是活仓库，分支会漂） |
| 锚点存储 | `data/sources.json` 的 `upstream.locked_sha` |
| 同步时间 | `data/sources.json` 的 `upstream.locked_at` / `last_checked_at` |
| 初版锚点 | `f639dac0b89792165afa9e3b6922e429ad9098e4`（2026-11-07，45 个文件 / 663,633 字节） |

## 标准升级流程

### 第一步：探测

```bash
python scripts/sync_upstream.py --check
```

只读探测：`git ls-remote` 取上游 HEAD 与锁定 sha 比对。

- 输出 `UP_TO_DATE` → 无更新，结束。
- 输出差异清单 → 进入第二步。

差异清单的四类语义：

| 标记 | 含义 | 处置 |
|---|---|---|
| `+ 文件` | 上游新增 | 通常直接收入，然后在路由表登记 |
| `~ 文件` | 上游已修改 | 逐份看 diff，判断是排版修正还是内容口径变化 |
| `- 文件` | 上游已删除 | **本地快照默认保留**，需人工裁决是否废弃 |
| 未列出 | 内容一致 | 无需动作 |

### 第二步：落盘

```bash
python scripts/sync_upstream.py --apply
```

落盘动作：复制新增与变更文件 → 更新 `data/sources.json` → 自动重建 `data/index.json` → 删除临时克隆目录并回读确认。

### 第三步：登记路由

新文件不会自动进路由表。按「新增 / 升级模型的三条路径」（见 SKILL.md）在 `data/model-routing.json` 加族或别名：

- 新模型、新厂商 → 新增一个 family，写 `id` / `label` / `vendor` / `priority` / `aliases` / `candidates` / `note`；
- 已有厂商的新版本 → 加进同厂商族的 `aliases`，并把新文件插到 `candidates` 前面（候选链按顺序取第一份存在的文件）；
- 无关文件（空文件、纯说明） → 记进 `ignored_files` 并写明理由。

### 第四步：验证

```bash
python scripts/build_index.py          # 重建索引
python scripts/build_index.py --check  # 路由表候选是否齐全
python scripts/resolve_prompt.py --verify  # 族覆盖与文件一致性
```

三条都要 PASS 才能收口。`--check` 或 `--verify` 非 0 退出说明路由表指向了不存在的文件。

### 第五步：登记

在本文件「升级记录」表追加一行，字段固定：日期 / from-sha → to-sha / 新增 / 修改 / 删除 / 人工标注（新增或调整的路由族数）/ 备注。

## 升级裁决口径

| 情形 | 裁决 |
|---|---|
| 上游新增某模型提示词，且能进现有厂商族 | 收，加别名 |
| 上游新增某模型提示词，厂商全新 | 收，新增 family |
| 上游修改文件，属排版 / 措辞微调 | 收 |
| 上游修改，属「覆盖既有策略」类话术加强 | 收（保留研究样本），但在 `references/prompt-techniques.md` 反例区同步登记 |
| 上游删除文件 | 本地快照保留，路由表把该文件从 `candidates` 移除即可，不物理删除 |
| 上游文件名或目录结构调整 | 本地命名由 `sync_upstream.py` 的 `collect_upstream` 规则派生，会表现为「一删一增」；同 `sha256` 的项按重命名处理，路由表跟着改名 |

## 本地自建区

上游没有、但本地按目标模型厂商风格自行改造产出的提示词，登记在这里而不是 `prompts/`——`prompts/` 与上游严格 1:1，任何自建文件放进去都会在下次同步时被识别为「上游已删除」。

| 日期 | 目标模型 | 基线文件 | 改造要点 | 落点 |
|---|---|---|---|---|
| 暂无 | - | - | - | - |

## 升级记录

| 日期 | 版本变化 | 新增 | 修改 | 删除 | 人工标注 | 备注 |
|---|---|---|---|---|---|---|
| 2026-11-07 | 首次入库（无锁定 → `f639dac`） | 45 | 0 | 0 | 32 个路由族 | 45 文件 / 663,633 字节；2 组重复内容；1 个空文件 `qwen-preferences.md` 记入 ignored |
| 2026-11-07 | 五次实测后修复（版本未变） | 0 | 0 | 0 | 0 | 修一处**跨平台缺陷**：45 份快照在 Windows 侧是 CRLF、上游是 LF（git autocrlf 所致），而 `hash_file` 直接哈希原始字节，导致同一份数据在 Linux/WSL 侧把 44/45 全判为 CHANGED、Windows 侧判 0 变更。修法：① `hash_file` 与落盘统一规范化行尾为 LF；② 存量 45 份快照一次性转 LF 并重算 `sources.json` 哈希表。验证：两侧同时跑 `--check` 均为 `ADDED=0 CHANGED=0 REMOVED=0 UNCHANGED=45` |
| 2026-11-07 | 四次实测后修复（版本未变） | 0 | 0 | 0 | 0 | 修三处：① **SKILL.md 的脚本调用路径不可用**——文档写 `python scripts/xxx.py`，但会话工作目录是仓库根，照抄直接「找不到文件」；改为先取资源块给出的 Base directory 再拼路径，并实测照抄可用；② `index.json` / `sources.json` 原用 `write_text` 非原子写，写一半被并发读会拿到残缺 JSON，改为临时文件 + `os.replace` 原子替换；③ 并发压力验证：4 路并发 resolve 4/4 通过、8 路并发建索引后 JSON 仍有效、40 次读写竞态零失败 |
| 2026-11-07 | 三次实测后修复（版本未变） | 0 | 0 | 0 | 0 | 修三处：① `--keyword` 原来只搜文件名与摘要，搜 `reverse shell` / `keylogger` 全落空，改为默认搜正文（惰性读取 + 单次查询内缓存，119ms vs 基线 103ms）并新增 `--meta-only` 保留快速模式；② 路由表 JSON 损坏时抛裸 traceback，改为带行号列号与修复指引的 `SystemExit`；③ 四个脚本只 reconfiguered stdout，`SystemExit` 中文报错走 stderr 在 GBK 控制台（chcp 936）乱码，统一补 stderr |
| 2026-11-07 | 二次实测后修复（版本未变） | 0 | 0 | 0 | 0 | 修两处：① `--fallback` 原为死参数（两个分支代码相同，唯一效果是让警告消失），改为严格模式 `NO_MATCH` 阻断 + 显式 `--fallback` 才兜底；② `--apply` 零变更时不再重写 `sources.json` / 重建索引，文件指纹恢复稳定；③ 阻断输出超长模型名截断 |
| 2026-11-07 | 会话内实测后修复（版本未变） | 0 | 0 | 0 | 0 | 修三处：① `--kind` 载体偏好改读 `index.json` 的真实 kind，不再用文件名子串匹配；② 手法判据剔除裸词 `persona`，`persona_lock` 从 29 条噪音收敛到 2 条；③ 补 `ds4.1` / `ds-v4.1` 别名 |
