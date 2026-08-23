# 吸收裁决表（workbuddy-absorption-map）

> 本文件记录 ssh-server-ops-rules 的外部吸收裁决与整理去重动作，保证可追溯。

## 2026-08-22 吸收：ssh-remote-skill v1.0.0（外部吸收通道）

- **来源**：`ssh-remote-skill`（skillhub 本地安装，用户级 + 工作区各一份，MIT）
  - 仓库回指：`https://github.com/YOUR_USERNAME/ssh-remote-skill`（源 skill.json 声明，占位地址）
  - 本地安装路径：`C:\Users\luode\.workbuddy\skills\ssh-remote-sanitized__skillhub\`（用户级）
  - 工作区路径：`D:\谷歌云盘\luode-skills\ssh-remote-sanitized__skillhub\`（工作区）
- **吸收方向**：新建独立 skill `ssh-server-ops-rules`（规则型 + Node 推钥脚本）
- **用户核心调整诉求**：凭证管理改造——用户提供用户名/密码 → agent 自动生成 ed25519 密钥对 → 存 `C:\Users\luode\.ssh` → 密码首连推公钥 → 后续密钥认证；密码用后即弃不落盘

| # | 来源条目 | 裁决 | 落点 | 理由 |
| --- | --- | --- | --- | --- |
| 1 | 功能矩阵（连接/执行/上传/下载/监控/服务/日志/安全） | 合并 | SKILL.md 能力清单 | 保留骨架；安全检查并入服务管理，不单列 |
| 2 | servers.json 配置模型（含明文 password） | 合并+改造 | references/credential-guide.md | 去明文 password，改 keyPath + agent 自动生成密钥 |
| 3 | Node 连接池复用（ssh2 Map） | 拒绝 | — | 规则型 skill 用系统 ssh，会话复用由 SSH agent 承担 |
| 4 | ssh2 npm 依赖 + 全套 Node 实现（8 模块 js） | 拒绝 | — | 只保留「密码首连→推公钥」这一个必须脚本化的环节（scripts/push_pubkey.js） |
| 5 | 触发词体系（ssh 连接/执行/上传/下载/监控/服务/日志/安全） | 合并 | SKILL.md description | 扩展为语义触发 |
| 6 | 批量执行、常用命令参考 | 合并 | SKILL.md 日常使用规则 | 高频运维场景 |
| 7 | 快速配置指南（手动 ssh-keygen + ssh-copy-id） | 合并+改造 | references/credential-guide.md | 改造为 agent 自动执行（核心诉求） |

**整理去重**：
- 目标 skill 内：N/A（新建目录，无存量可整理）
- 同域扫描：范围 = `docker-direct-deploy` / `test-strategy-rules` / `ssh-remote-sanitized__skillhub`（源）；发现 0 处重复段落、0 处概念层叠、0 处散落产物；PASS
- 净增体积：新增 1 目录（SKILL.md 约 5KB + credential-guide.md 约 4KB + push_pubkey.js 约 5KB + 登记文件约 3KB），无删除项（源删除另计）

**源处理**：吸收确认后删除本地安装源（用户级 + 工作区两份），已删除。

**评分验证**：结构自评 8 维见 `case-ssh-server-ops-absorption.md`；真实场景验证 3 例（见同文件）。
