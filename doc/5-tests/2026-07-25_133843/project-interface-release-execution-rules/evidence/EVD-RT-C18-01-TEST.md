# EVD-RT-C18-01-TEST

## 真实测试

- C18-01/C17 组合专项：`10/10 PASS`。
- 当前外部场景全量回归：`34/34 PASS`。
- `external-migrate --help`：通过。
- `py_compile`：迁移模块、兼容 CLI 和 C17 测试通过。

## 样本

覆盖旧接口结果列表、旧 PASS 降级、输入不覆盖、新输出弃用标记和现有 release-run 参数兼容。

