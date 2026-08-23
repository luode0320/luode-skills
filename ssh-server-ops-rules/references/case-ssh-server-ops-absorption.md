# Case Study：ssh-remote-skill → ssh-server-ops-rules 吸收

> 供下次吸收对照的完整案例，记录裁决、改造、验证与体积变化。

## 1. 背景

用户要求吸收 `ssh-remote-skill`（skillhub 安装源）为独立新 skill，核心调整诉求是**凭证管理**：
用户提供远程服务器用户名/密码 → agent 连接后自行生成公钥/密钥对 → 数据默认保存
`C:\Users\luode\.ssh` → 供后续持续使用（免密）。

## 2. 关键决策（用户确认）

| 决策点 | 选择 | 理由 |
| --- | --- | --- |
| 实现形态 | 规则型 SKILL.md + Node(ssh2) 推钥脚本 | 延续源技术栈；只有「密码首连」必须脚本化 |
| 配置落点 | `C:\Users\luode\.ssh\servers.json` | 与密钥同目录，跨项目全局可用 |
| 密码处置 | 用后即弃，不落盘 | 与「生成密钥替代密码」初衷一致，安全优先 |

## 3. 改造亮点

- **凭证引导自动化**：把源 skill 的「手动 ssh-keygen + ssh-copy-id」改造为 agent 全自动流程
  （检查密钥 → 生成 ed25519 → 脚本密码首连推公钥 → 验证 → 配置落盘）。
- **幂等推钥**：`push_pubkey.js` 先 grep 检查 authorized_keys 是否已有该公钥，已有则跳过。
- **Windows 适配**：生成密钥后立即 `icacls` 收紧权限，规避 OpenSSH `UNPROTECTED PRIVATE KEY FILE`。
- **安全红线**：密码只走 `SSH_PASSWORD` 环境变量/进程内存；`servers.json` 无 password 字段；
  敏感文件禁止进 Git。

## 4. 净增体积与整理去重

| 项 | 数值 |
| --- | --- |
| 新增目录 | `ssh-server-ops-rules/`（5 个文件：SKILL.md、credential-guide.md、push_pubkey.js、workbuddy-absorption-map.md、source-notes.md + 本案例） |
| 新增体积 | 约 17KB |
| 目标 skill 内整理 | N/A（新建目录无存量） |
| 同域扫描 | docker-direct-deploy / test-strategy-rules / 源 skill；0 重复、0 层叠、0 散落；PASS |
| 删除 | 源 skill 两份（用户级 + 工作区），约 40KB 清理 |

## 5. 8 维结构自评（新 skill 无吸收前基线，以达标为准）

| 维度 | 评分 | 说明 |
| --- | --- | --- |
| 触发清晰度 | 8/10 | description 含明确触发词与语义场景 |
| 流程可执行性 | 9/10 | 首次接入 5 步 + 日常命令模板，零决策执行 |
| 边界与负向 | 8/10 | 含"只解释不落盘"边界；高危命令确认规则 |
| 安全合规 | 9/10 | 密码用后即弃、权限收紧、禁入 Git |
| 引用完整性 | 9/10 | References 全部可达 |
| 体积控制 | 9/10 | 拒绝 8 模块 Node 实现，只保留最小脚本 |
| 平台适配 | 8/10 | Windows 路径/权限专项，Linux/macOS 说明 |
| 可维护性 | 8/10 | 单一权威 + 登记文件齐备 |
| **合计** | **68/80** | 达标保留 |

## 6. 真实场景验证（3 例）

| 场景 | 预期 | 验证方式 |
| --- | --- | --- |
| 「给服务器配免密，root@192.168.1.100，密码 xxx」 | 生成密钥 → 推公钥 → servers.json 落盘 | 规则路径走通（语法校验 + 脚本参数校验已通过；真实服务器接入留待用户实测） |
| 「ssh 执行 api uptime」 | 从 servers.json 取 api 条目 → `ssh -i <keyPath>` 执行 | 命令模板正确 |
| 重复接入同一服务器 | 复用已有密钥、跳过公钥追加 | push_pubkey.js 幂等逻辑（grep 检查） |

> 注：真实服务器接入验证受限于当前无可用测试服务器，脚本已通过 `node --check` 语法校验与 `require('ssh2')` 加载验证；建议用户首次接入真实服务器时按本 skill 流程走一遍，若有问题回填到 credential-guide.md 常见错误表。
