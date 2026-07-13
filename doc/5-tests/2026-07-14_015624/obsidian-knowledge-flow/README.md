# Obsidian 执行失败持续学习测试

本目录验证 `obsidian-knowledge-flow` 的执行失败正反例契约、追加式状态事件、精确 scope 检索、脱敏、local-only 边界和 bridge-only 写入规则。

测试只使用仓库内 UTF-8 规则文件、内存 `FakeBridge` 和临时 fixture，不启动 Obsidian，不读写真实 vault，也不连接 test、staging 或 production 环境。

运行入口：

```powershell
python -m unittest discover -s doc/5-tests/2026-07-14_015624/obsidian-knowledge-flow -p "test_*.py" -v
```

真实 vault 的 `doctor`、`create`、`append` 和 readback 仍需在 `D:\obsidian_data` 注册且 CLI 可用后单独验证；bridge 未注册时必须保持 `Obsidian:阻断`，不得使用文件系统 fallback。
