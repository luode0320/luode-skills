# EVD-RT-C17-02-TEST

## 真实测试

- `wsl.exe --cd /mnt/f/luode-skills bash -lc "/tmp/luode-skills-release-test-env/bin/python -X utf8 -m unittest discover -s 'doc/5-tests/2026-07-25_133843/project-interface-release-execution-rules/tests' -p 'test_dual_gate_migration.py' -v"`：`6/6 PASS`。
- 同一测试根目录全量执行：`30/30 PASS`。
- C17-02 CLI 集成样本使用随机回环端口，同一 local HTTP 服务同时承接 legacy 和 verified scenario 请求。
- `py_compile`：`gate.py`、`cli.py`、`report.py`、`scenario_runner.py` 和 C17 测试通过。

## 失败样本

覆盖缺口、场景 FAIL、清理 FAIL、状态不一致、非 local 场景资产和敏感字段均有断言或执行边界。
