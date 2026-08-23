# 来源记录（source-notes）

## 2026-08-22 — 外部吸收：ssh-remote-skill

- **来源类型**：外部 skill（skillhub 本地安装源）
- **来源标识**：`ssh-remote-skill` v1.0.0（npm 包名 `ssh-remote`，依赖 `ssh2 ^1.15.0`）
- **可回指地址**：源 `skill.json` 声明 `repository: https://github.com/YOUR_USERNAME/ssh-remote-skill`（占位地址，原作者未填真实仓库）；本地安装目录用户级 `C:\Users\luode\.workbuddy\skills\ssh-remote-sanitized__skillhub\` 与工作区 `D:\谷歌云盘\luode-skills\ssh-remote-sanitized__skillhub\`（两份内容一致，吸收后已删除）
- **吸收动机**：获得 SSH 远程运维能力骨架；按用户诉求改造凭证管理为「密码首连→密钥认证常驻」
- **落点**：`ssh-server-ops-rules`（新建）
  - `SKILL.md` — 触发条件、能力清单、凭证模型、日常使用规则、安全规则
  - `references/credential-guide.md` — 凭证引导流程、servers.json schema、常见错误
  - `scripts/push_pubkey.js` — 密码首连推公钥脚本（Node + ssh2）
  - `references/workbuddy-absorption-map.md` — 吸收裁决表
  - `references/case-ssh-server-ops-absorption.md` — 案例沉淀
- **保留的原子规则**：功能矩阵、触发词体系、批量执行、常用命令模板
- **拒绝的原子规则**：Node 连接池复用（改用系统 ssh）、8 模块完整 Node 实现（只保留推钥脚本）、配置明文存密码（改为密钥认证 + 用后即弃）
- **用户决策（2026-08-22 确认）**：规则型 + Node(ssh2) 脚本；配置存 `C:\Users\luode\.ssh\servers.json`；密码用后即弃不落盘
