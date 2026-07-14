---
reader_level: business_general
writing_style: plain_chinese
appendix_policy: preserve_existing_or_one_terminal_appendix
review_acceptance_gates:
  - stage: functional_validation
    applicability: applicable
    reason: 本轮需要验证校验脚本的新输入输出和异常分支。
    basis: 实施计划第 9 节七个离线用例。
    required_by_source: true
    required_now: true
    completed_validation:
      - 7/7 离线 fixture 用例
    substitute_validation: []
    manual_follow_up: N/A
    pass_standard: 七个用例按预期退出码、JSON、scope 和 warning 通过。
  - stage: third_party
    applicability: not_applicable
    reason: 本轮只验证离线 fixture，不调用真实第三方服务。
    basis: 计划明确禁止联网抓取和真实业务项目生成。
    required_by_source: false
    required_now: false
    completed_validation: []
    substitute_validation:
      - 本地离线 fixture
    manual_follow_up: N/A
    pass_standard: N/A
---

# 第三方 swag 校验升级验证

结论：7 个离线用例全部通过；影响：确认根目录与上游子目录可以隔离校验；范围：脚本输入输出、异常分支、兼容和告警；非范围：真实业务项目、真实第三方服务和上线基线；变化：校验命令支持一层上游目录；完成标准：7/7 用例按预期通过；术语说明：上游目录指本项目主动调用的外部或内部服务文档子目录；验证状态：已完成本地真实运行验证。

## 测试目标

验证 `validate_openapi_yaml.py` 能在一次命令中校验自有 `swag/` 根目录和一层 `swag/<vendor-slug>/` 上游服务子目录，同时保持没有上游子目录的旧项目行为兼容。

## 真实测试资产

- 测试主程序：`doc/5-tests/2026-07-14_121425/swag-openapi-maintainer-rules/scripts/validate_openapi_yaml_third_party_test.py`
- fixture 构造器：`doc/5-tests/2026-07-14_121425/swag-openapi-maintainer-rules/scripts/fixtures_builder.py`
- 运行时 fixture：`D:\tmp\swag-tree-*`，测试结束自动删除。

## 运行方式

在仓库根目录执行：

```powershell
$env:PYTHONUTF8='1'
python doc/5-tests/2026-07-14_121425/swag-openapi-maintainer-rules/scripts/validate_openapi_yaml_third_party_test.py
```

测试完全离线，不连接数据库、缓存、消息队列、HTTP/RPC 上游或业务项目，不包含真实密钥。

## 覆盖用例与通过标准

1. 正例：自有接口和 `moonpay` 上游目录均通过。
2. 上游字段缺中文说明：只报告上游 scope，根 scope 仍通过。
3. 上游 manifest 文件映射不匹配：退出码为 1 且命中映射错误。
4. 裸文件名/路径逃逸保护：根或上游 manifest 的文件路径被拒绝。
5. 上游 manifest 缺 `source_type`：退出码为 1 且命中字段错误。
6. 无上游子目录兼容：旧根级校验结果逐键一致，新增 `third_party: []`。
7. 陌生子目录：进入 `tree_warnings`，不影响根 scope 通过。

所有用例均须符合预期退出码和错误范围，测试结束输出通过汇总并清理临时 fixture。

## 本轮执行结论

- 执行环境：Windows 本地离线 Python + PyYAML，设置 `PYTHONUTF8=1`；未连接任何外部服务。
- 验证方式：真实运行验证，测试主程序通过 subprocess 调用被测 CLI，并解析 stdout JSON 与 stderr 过程日志。
- 执行命令：`$env:PYTHONUTF8='1'; python doc/5-tests/2026-07-14_121425/swag-openapi-maintainer-rules/scripts/validate_openapi_yaml_third_party_test.py`
- 结果：7/7 用例通过；正例退出 0，五类反例按预期退出 1，单目录兼容和陌生目录 warning 按预期通过。
- 清理：每个 fixture 使用 `TemporaryDirectory` 创建于 `D:\tmp`，测试结束自动清理；未留下测试数据。
- 未通过项：无。
