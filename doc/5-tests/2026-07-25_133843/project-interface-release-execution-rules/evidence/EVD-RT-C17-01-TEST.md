# EVD-RT-C17-01-TEST

## 真实测试

- `wsl.exe --cd /mnt/f/luode-skills /tmp/luode-skills-release-test-env/bin/python -X utf8 -m unittest discover -s "doc/5-tests/2026-07-25_133843/project-interface-release-execution-rules/tests" -p "test_dual_gate_migration.py" -v`：`3/3 PASS`。
- `wsl.exe --cd /mnt/f/luode-skills /tmp/luode-skills-release-test-env/bin/python -X utf8 -m unittest discover -s "doc/5-tests/2026-07-25_133843/project-interface-release-execution-rules/tests" -p "test_*.py"`：`27/27 PASS`。
- `wsl.exe --cd /mnt/f/luode-skills /tmp/luode-skills-release-test-env/bin/python -X utf8 -m py_compile project-interface-release-execution-rules/scripts/release_test_engine/report.py doc/5-tests/2026-07-25_133843/project-interface-release-execution-rules/tests/test_dual_gate_migration.py`：通过。
- `git diff --check`：通过。

## 覆盖样本

验证接口/场景独立归档、旧报告兼容、步骤字段、空场景 `not_configured`、错误场景状态、清理阻断、敏感值脱敏和证据清单相对路径。

## 环境

所有服务测试使用 local 随机回环端口；临时依赖仅安装到 WSL `/tmp/luode-skills-release-test-env`，未修改被测项目依赖。

