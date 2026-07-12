# EVD-TASK-RT-C09-01-TEST

## 真实测试

命令：`python -m unittest discover -s doc/5-tests/2026-07-12_191712/project-release-test-rules/tests -p 'test_contract_asset_sync.py' -v`

结果：4/4 PASS，覆盖完整三方、全部缺失、非法 YAML、非 local 路径和 strict pipeline 报告透传。

回归命令：`python -m unittest discover -s doc/5-tests/2026-07-12_191712/project-release-test-rules/tests -p 'test_c08_e2e_artifacts.py' -v`

结果：1/1 PASS；既有 local HTTP fixture、baseline replay 和历史非 strict 行为保持通过。
