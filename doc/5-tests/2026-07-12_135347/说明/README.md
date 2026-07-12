# Windows PowerShell 环境 Skill 测试

- 来源：`windows-powershell-environment-rules`
- 时间戳根目录：`2026-07-12_135347`
- 真实测试资产：`windows-powershell-environment-rules/scripts/`
- 环境：Windows local 用户环境；不连接数据库、缓存、消息队列或非 local 服务。
- 覆盖：Audit、PowerShell 7 profile、Windows Terminal JSONC 配置、幂等重跑、rollback、工具实际版本探针。
- 通过标准：脚本退出码为 0；固定 profile GUID 只有一项；重复运行不增加 profile；rollback 恢复原始 JSONC 语义；所有命令版本探针可解析。
