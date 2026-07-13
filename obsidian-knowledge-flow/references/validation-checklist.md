# 验证清单

创建、更新或前向测试本 skill 时使用这份清单。

## Skill 资产验证

- `SKILL.md` 的 YAML frontmatter 只包含 `name` 和 `description`。
- `description` 覆盖选择性默认判断、Windows/WSL bridge、固定根目录 `D:\obsidian_data`、`知识库/` 工作区、会话开始检索、总结阶段捕获/沉淀、Obsidian、vault、Markdown 知识库、CLI、本地笔记库和知识库检索等触发场景。
- `SKILL.md` 直接链接所有 references，references 只保持一层深度。
- `agents/openai.yaml` 字符串均已加引号，且 `default_prompt` 提到 `$obsidian-knowledge-flow`。
- 不新增 README、安装指南、changelog 或无关辅助文档。

## 选择性默认验证

0. 项目本地四件套启动：
   - 输入：临时项目目录缺少 `PROJECT_CURRENT.md`、`PROJECT_MEMORY.md`、`PROJECT_HISTORY.md`。
   - 预期：先创建三个 UTF-8 文件，读取 current 后读取 memory；普通启动不读取 history。
   - 追加场景：已有 history 内容时重复初始化不得覆盖；current 超过 51,200 字节时阻断。

1. 普通仓库任务：
   - 输入：一次不依赖历史知识、也没有可复用沉淀价值的普通文档或实现任务。
    - 预期：输出 `Obsidian:不适用`，不调用 bridge，不读取 vault。
2. 历史知识问题：
   - 输入：用户询问“上次怎么定的”“之前 Obsidian 里有没有记录”。
    - 预期：输出 `Obsidian:检索`，通过 bridge `search` / `search-context` 检索，并用 bridge `read` 读取匹配笔记。
3. 收口沉淀：
   - 输入：阶段收口时形成可复用规则、流程、事实或调试经验。
    - 预期：输出 `Obsidian:沉淀`，先通过 bridge 检索已有承接笔记，再决定 `create` 或 `append`。
4. bridge / vault 不可用：
    - 输入：本应检索或沉淀，但 bridge doctor 失败、vault 未注册或根目录不一致。
   - 预期：输出 `Obsidian:阻断`，说明恢复动作，不用直接文件系统读写作为 fallback。

## bridge 前置验证

在样例 vault 功能测试前先验证：

1. Windows / WSL bridge doctor：
   - 预期：Windows 使用 direct transport，WSL 使用 Windows interop；二者均返回 `ok=true`、`verified=true`。
2. bridge doctor 失败：
   - 预期：按稳定错误码阻断，不继续读写 vault；WSL 缺少原生 `obsidian` 但 interop 可用时不得阻断。
3. 默认根目录不存在：
   - Windows 预期固定 `D:\obsidian_data`。
   - 预期：由 bridge doctor 校验；若 bridge 无法唯一解析该 vault，阻断并提示用户在 Obsidian 中打开/注册一次。
4. `D:\obsidian_data` 下的 `知识库/` 目录不存在：
   - 预期：只允许在固定根目录内补齐，不得改用其它路径。
5. 多个/零个固定根匹配、nested root 或路径越界：
   - 预期：返回 `VAULT_ROOT_AMBIGUOUS`、`VAULT_NOT_REGISTERED`、`LEGACY_NESTED_VAULT_MODEL` 或 `PATH_OUTSIDE_KNOWLEDGE`，不写入。
6. 应用不可达、interop、PowerShell 或 timeout 失败：
   - 预期：只按 bridge 的有限恢复策略执行，仍失败时返回稳定错误码；不杀用户进程、不无限重试。
7. 10KB 中文正文、多行表格或 Mermaid：
    - 预期：bridge/adapter 分块写入，最终 readback 保持完整 UTF-8 内容。
8. 有限恢复与重试边界：
    - 预期：应用不可达时最多隐藏启动一次、等待 15 秒并重试一次；`attempts` 不超过 3。参数、路径、interop、selector、timeout 和 readback 错误不得无变化重试。

## 样例 Vault 功能测试

创建或使用一次性本地样例 vault 做验证。不要直接在生产 vault 上测试。

1. 会话开始检索：
   - 输入：用户用别名询问之前的决策。
    - 预期：通过 bridge 扩展别名检索，读取匹配笔记，并引用笔记路径。
2. 总结阶段捕获：
   - 输入：一段会话包含一个稳定决策、一个来源链接和一个反复出现的项目实体。
    - 预期：通过 bridge 创建或更新一篇会话笔记、一篇知识笔记、一篇来源笔记和一篇实体笔记，并补齐 backlinks/readback。
3. 沉淀：
   - 输入：一篇会话笔记同时包含稳定事实和不确定事实。
   - 预期：稳定事实被提升；不确定事实留在会话笔记或 `知识库/00-Inbox/`。
4. 冲突：
   - 输入：一条新笔记与旧的活跃笔记矛盾，且没有权威证据。
   - 预期：笔记标记为 `conflicted`，同时保留两种说法。
5. 敏感数据：
   - 输入：会话包含 API key。
   - 预期：不保存原值；只产生脱敏占位或不产出笔记。
6. 可读组件：
   - 输入：一段长期流程或决策对比。
   - 预期：笔记正文可使用表格、列表、Obsidian callout 或 Mermaid；仍保持纯 Markdown 可读。
7. 全量 vault 沉淀：
    - 输入：一个受控 source root 与 bridge doctor 已验证的固定目标 vault。
   - 预期：先统计源 Markdown 总数；每个顶层分类生成逐篇沉淀笔记；全量总览汇总所有批次；逐篇表格数据行数等于来源 Markdown 数；总和等于源总数；敏感主题只保存脱敏后的通用线索。

## 仓库验证

在 skill 仓库中修改本 skill 后：

- 对 skill 目录运行 skill creator 校验器。
- 当 `description` 或 `##` 标题变化时，运行仓库 skill 字典生成脚本。
- 检查 `git diff`，确认生成的字典文件由脚本刷新，不是手工修改。
- 同时确认项目本地四件套与 vault 分层：项目 Markdown 使用标准文件工具，vault 检索和沉淀只能使用公开 bridge。

## 跨宿主证据映射

| 能力 | 自动化或实机测试 |
| --- | --- |
| doctor、固定 root 和唯一 selector | TEST-OBS-001/011 |
| Windows/WSL transport 与 interop | TEST-OBS-003/007 |
| create、append、路径与 readback | TEST-OBS-004/008/013 |
| 应用自动启动 | TEST-OBS-006 |
| Unicode 10KB 分块 | TEST-OBS-010 |
| distill、INDEX、脱敏和路由 | TEST-OBS-014/015 |
| references bridge-only、禁止词与 TEST 映射扫描 | TEST-OBS-016 |
