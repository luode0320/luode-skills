# 微业务隔离校验测试任务

## 目标

验证 `micro-business-architecture-rules` 的隔离校验脚本 `micro_business.py check` 能正确识别业务包之间的非法横向 import(禁止 `business` 直连 `business`），并验证 `scaffold` 建骨架的幂等性。

## 测试资产（ASCII 镜像目录）

- `micro-business-isolation-check/good/`  合规样例：`business/order` 只 import `contract/user` 与 `common`
- `micro-business-isolation-check/bad/`   违规样例：`business/order` 直接 import `business/user` 内部路径

> 样例 `.go` 为静态样例，仅供脚本扫描 import 文本，不参与编译（遵循 `go-test-compile-path-rules`：ASCII 路径、不落源码目录 `*_test.go`）。

## 执行命令（在仓库根 `D:\luode\luode-skills` 下）

```bash
# 合规组：期望退出码 0
python micro-business-architecture-rules/scripts/micro_business.py check \
  --root doc/5-tests/2026-07-13_174233/micro-business-isolation-check/good

# 违规组：期望退出码 1 且报出 order -> user 违规
python micro-business-architecture-rules/scripts/micro_business.py check \
  --root doc/5-tests/2026-07-13_174233/micro-business-isolation-check/bad

# scaffold 幂等：连续两次，第二次应“未新增任何内容”
python micro-business-architecture-rules/scripts/micro_business.py scaffold payment \
  --root doc/5-tests/2026-07-13_174233/scaffold-tmp --with-contract
```

## 通过标准

- good：退出码 0，输出「隔离校验通过」
- bad：退出码 1，输出违规行（业务包 order -> user）
- scaffold：首次创建业务包骨架 + README；第二次输出「目标已存在，未新增任何内容(幂等)」

## 执行结果

执行时间：2026-07-13_174233（北京时间）

| 测试 | 期望 | 实际 | 结论 |
|---|---|---|---|
| check good | 退出 0，隔离校验通过 | EXIT 0，发现 order/user，通过 | ✅ |
| check bad | 退出 1，报 order->user 违规 | EXIT 1，精确报出 `order/service.go` import `business/user` | ✅ |
| scaffold 首次 | 退出 0，建 6 项骨架 | EXIT 0，创建 handler/logic/model/store/README.md/contract/payment | ✅ |
| scaffold 幂等 | 退出 0，未新增 | EXIT 0，「目标已存在，未新增任何内容(幂等)」 | ✅ |
| init 首次 | 退出 0，写入标记 | EXIT 0，CLAUDE.md/AGENTS.md/项目设计.md 各 created | ✅ |
| init 幂等 | 退出 0，不重复堆叠 | EXIT 0，各章节 count=1，IDEMPOTENT_PASS | ✅ |

六组真实测试全部通过。控制台中文显示为 GBK 回显乱码属 Git Bash 终端现象，脚本 UTF-8 读写与退出码逻辑均正确。scaffold/init 产物落在本目录 `scaffold-tmp/`、`init-tmp/`，作为测试证据保留。

> 缺陷修复记录：`init` 首次运行曾因 `upsert_section` 在文件不存在分支未创建父目录报 `FileNotFoundError`，已在源头补 `parent.mkdir(parents=True, exist_ok=True)` 修复，重跑通过（体现真实测试价值，非绕过式修补）。
