---
name: skill-displayname-patcher
displayName: "Skill 显示标题中文规范化"
description: 当 WorkBuddy「我安装的」技能列表中英文显示标题混杂，或 builtin skill 被 workbuddySeedManaged 重新同步回英文时触发。负责扫描所有 skill 目录、识别缺中文 name 的 _skillhub_meta.json、给出简洁技术风的中文翻译并批量写入（不改 slug、不动 SKILL.md、不破坏调用），以及给 user 自建无 meta 的 skill 创建中文 _skillhub_meta.json。
---

# Skill 显示标题中文规范化

## 何时触发

- 用户反馈 WorkBuddy skill 列表「中英混杂」，希望统一显示为中文标题
- builtin skill 被 WorkBuddy 升级/重新同步回英文后再次需要补中文显示名
- 用户从市场新装了一批 skill，又出现显示名不一致
- 新创建了 user 自建 skill，需要中文显示名

## 真实机制（2026-08-20 实验确认，勿再走弯路）

WorkBuddy「我安装的」卡片标题**不是**来自 SKILL.md frontmatter 的 `displayName` 字段——该字段 WorkBuddy 不读，改了无效。

真实读取顺序（实测验证）：

| Skill 类型 | 目录特征 | 显示名来源 |
|---|---|---|
| marketplace 装 | `<name>__skillhub/` | `<name>__skillhub/_skillhub_meta.json` 的 `name` 字段 |
| user 自建（带 meta） | `<name>/_skillhub_meta.json` | 同上 |
| user 自建（无 meta） | 只有 SKILL.md + agents/ | **创建** `_skillhub_meta.json` 后 WorkBuddy 才会读（已验证） |
| builtin plugin | `plugins/cache/workbuddy-builtin/<plugin>/<version>/` | `.codebuddy-plugin/plugin.json` 的 `name` 字段（被托管，升级会回写） |

证据（实验链路）：
1. 改 `loop__skillhub/_skillhub_meta.json` 的 `name` 从 "Loop" → "Loop 循环测试"，重启后 UI 卡片标题变为 "Loop 循环测试" ✅
2. 给 user 自建 `code-change-finalization-gate-rules/` 新建 `_skillhub_meta.json`，重启后卡片标题变为中文 ✅
3. 反向证明：改 SKILL.md frontmatter 的 `displayName` 字段 → UI 无任何变化 ❌

## 不要做的事

- **不要修改 SKILL.md frontmatter 的 `displayName`**：WorkBuddy 不读，改了无效。
- **不要修改 `_skillhub_meta.json` 的 `slug`**：这是 invoke 用的标识，改成中文会破坏 `Skill xxx` 调用。
- **不要修改 `name` slug 字段**（SKILL.md 的 `name` 或 plugin.json 的 `name`）：同上，破调用。
- **不要给 builtin skill 做"持久化修正"**：`workbuddySeedManaged: true`，WorkBuddy 升级会回写。改完只保证当前会话生效，升级后重跑。

## 工作流程

### 1. 环境前置

工具脚本长期目录：

```
C:\Users\luode\.workbuddy\.displayname-patch-tool\
├── scan_skills.py        # 扫描 + 输出待补清单
├── patch_meta.py         # 批量改已有 _skillhub_meta.json 的 name 字段
├── create_meta.py        # 给 user 自建无 meta 的 skill 创建中文 meta
└── cleanup_skillmd.py    # 清理误注入到 SKILL.md 的 displayName(可选)
```

**注意**：`apply_patch.py` 已废弃（改 SKILL.md displayName 的旧脚本，机制证伪后弃用，勿再用）。

Python：

```
C:\Users\luode\.workbuddy\binaries\python\versions\3.13.12\python.exe
```

依赖：`pyyaml`（首次用前 `python -m pip install pyyaml`）。

### 2. 干跑（先看清单，再动手）

```bash
cd "/c/Users/luode/.workbuddy/.displayname-patch-tool"
"/c/Users/luode/.workbuddy/binaries/python/versions/3.13.12/python.exe" create_meta.py
```

输出所有待创建 meta 的 user 自建 skill 及建议中文名（含来源：openai.yaml / override map / SKILL.md H1）。

改已有 meta 的 name：

```bash
"/c/Users/luode/.workbuddy/binaries/python/versions/3.13.12/python.exe" patch_meta.py
```

（修改前先看代码里的 `HUB_NAME_OVERRIDES` / `USER_SELF_BUILT_OVERRIDES` 映射表。）

### 3. 真正写盘

```bash
"/c/Users/luode/.workbuddy/binaries/python/versions/3.13.12/python.exe" create_meta.py --apply
"/c/Users/luode/.workbuddy/binaries/python/versions/3.13.12/python.exe" patch_meta.py
```

### 4. 中文名来源优先级（create_meta.py 内实现）

1. `SLUG_TO_ZH_OVERRIDES` 映射（scan_skills.py 中维护，简洁技术风，最高优先）
2. `agents/openai.yaml` 的 `interface.display_name`（仅当含中文）
3. SKILL.md 的 H1 title（仅当含中文）
4. `agents/openai.yaml` 英文名保底
5. 目录名保底

新装一批 skill 后出现未翻译 slug 时，往 `SLUG_TO_ZH_OVERRIDES` 加一行：

```python
"my-new-skill": "我的新技能 中文名",
```

然后重跑。

## 已知陷阱

1. **`slug` / `name` 是调用关键字，必须保持 ASCII slug**。中文化只改 `_skillhub_meta.json.name` 显示字段。
2. **SKILL.md 的 `displayName` 完全无效**——这是最坑的弯路，已实测证伪。
3. **builtin plugin 被 WorkBuddy 自动托管**（`workbuddySeedManaged: true`）。覆盖前把本地覆盖当成"临时补丁"理解，不是源仓库改动。升级后重跑工具恢复。
4. **marketplace 装 skill 的 meta 文件是 `_skillhub_meta.json`**，改 name 后 UI 立即生效，但重新拉取新版会被覆盖。
5. **`github` / `TAPD` / `WSL Chrome CDP` 这类专有名或技术名**：保留原名是合理的，不强改。
6. **user 自建 skill 创建 meta 后 source 字段标 `user-self-built`**：防止后续误当 marketplace 资源处理。

## 收尾 / 验证

1. **重启 WorkBuddy** 让 plugin cache 重新加载 → 「我安装的」列表标题立刻变中文
2. 抽 3-5 个改过的目录 `cat _skillhub_meta.json` 看 name 行写入成功
3. 截图 diff 给用户确认

## 关联上下文

- 用户偏好：中文显示，简洁技术风（如 database-schema-rules → 数据库结构规则）
- 永久化工具位置：`~/.workbuddy/.displayname-patch-tool/`
- 2026-08-20 实测确认：WorkBuddy 只读 `_skillhub_meta.json.name` 作为标题
