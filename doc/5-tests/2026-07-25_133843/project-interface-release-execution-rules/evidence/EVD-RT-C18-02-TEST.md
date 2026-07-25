# EVD-RT-C18-02-TEST

## 真实测试

- C18-02/C17 组合专项：`13/13 PASS`。
- 当前外部场景全量回归：`37/37 PASS`。
- 编译检查：通过。
- 缺包、版本不匹配、非 local 和完整 runtime 样本均已验证。

## 环境边界

测试依赖安装在 WSL `/tmp/luode-skills-release-test-env` 临时环境，未写入仓库依赖或被测项目依赖；doctor 的 `network_access` 固定为 `not_attempted`。
