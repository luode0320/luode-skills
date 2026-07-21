# TASK-SPLIT-02-03 脚本幂等对照证据

- 测试：`TEST-SPLIT-006`（bash 语法检查）、`TEST-SPLIT-007`（首次/重复运行等价性）。
- 命令：`& 'C:\Program Files\Git\bin\bash.exe' -n project-agents-bootstrap/scripts/bootstrap_agents.sh` → 退出码 0。
- 命令：在空 fixture `cases/bootstrap/first` 上运行 `bootstrap_agents.sh --target both` → 生成 7 个文件；复制为 `cases/bootstrap/second` 后重复运行同一命令 → 退出码 0，无新增追加。
- 对照结果（SHA-256 逐文件比对，`first` vs `second`）：

| 文件 | 字节数 | 哈希一致 |
|---|---:|:---:|
| `.editorconfig` | 231 | 是 |
| `.gitattributes` | 168 | 是 |
| `AGENTS.md` | 37287 | 是 |
| `CLAUDE.md` | 37287 | 是 |
| `PROJECT_CURRENT.md` | 360 | 是 |
| `PROJECT_HISTORY.md` | 183 | 是 |
| `PROJECT_MEMORY.md` | 466 | 是 |

- 结论：脚本未修改、`sync_section` 幂等 upsert 生效，规则文件 owner（`project-rule-file-bootstrap-rules`）与记忆文件 owner（`project-memory-file-bootstrap-rules`）共用同一脚本不产生双写或重复追加。
- 清理：`cases/bootstrap/first`、`cases/bootstrap/second` 两个临时 fixture 目录在验证完成后删除，只保留本证据文件。
