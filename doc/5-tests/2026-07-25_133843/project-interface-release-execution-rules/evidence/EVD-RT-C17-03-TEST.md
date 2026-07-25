# EVD-RT-C17-03-TEST

## 真实测试

- C17-03 专项：`8/8 PASS`。
- 当前外部场景全量回归：`32/32 PASS`。
- `generate_release_test_plan.py release-run --help`：通过，展示三种 gate mode 和窗口参数。
- `py_compile`：门禁、CLI、场景 runner、兼容入口和 C17 测试通过。
- `git diff --check`：通过。

## 必测失败样本

窗口不足、窗口含 FAIL、硬切后 legacy 回退和非 local 资产路径均已覆盖或固定阻断。
