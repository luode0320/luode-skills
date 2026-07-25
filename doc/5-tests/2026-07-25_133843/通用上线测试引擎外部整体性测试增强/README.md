# 通用上线测试引擎外部整体性测试增强

结论：本轮消费者场景整体性测试已完成，真实 HTTP、SSE、RFC 6455 WebSocket 和 Socket.IO 对外行为以及 oracle、清理、兼容迁移、双轨门禁和隔离工具环境全部通过。影响：上线放行依据从逐接口结果升级为完整消费者流程。范围：`REQ-RT-20260712-001` 的 `CYCLE-RT-13..18`。非范围：gRPC、MQ、性能、压力、安全扫描和浏览器 UI。变化：新增 `external-scenario/1.0` 和场景硬门禁。完成标准：新测试、历史回归、文档校验、字典、审查和最终验收全部通过。验证状态：PASS。

## 测试目的

验证前端或其他系统通过公开 HTTP、SSE、WebSocket 和 Socket.IO 接口获取的数据、事件顺序、跨步骤值和最终状态一致，且测试写入可清理、证据可脱敏、非 local 来源会被阻断。

## 环境与依赖

- 配置来源：仅 local。
- 服务：随机回环端口上的 HTTP、SSE、RFC 6455 和 Socket.IO fixture。
- Python：隔离环境 `/tmp/luode-skills-release-test-env`，不修改被测项目依赖。
- 测试数据：临时目录和临时命名空间，结束后由 fixture 与 cleanup 清理。

## 真实资产

- 测试代码：`doc/5-tests/2026-07-25_133843/project-interface-release-execution-rules/tests/`。
- 逐任务证据：`doc/5-tests/2026-07-25_133843/project-interface-release-execution-rules/evidence/`。
- 实现代码：`project-interface-release-execution-rules/scripts/release_test_engine/`。

## 执行方式

```bash
wsl.exe --cd /mnt/f/luode-skills /tmp/luode-skills-release-test-env/bin/python -X utf8 -m unittest discover -s "doc/5-tests/2026-07-25_133843/project-interface-release-execution-rules/tests" -p "test_*.py" -v
```

历史回归继续执行 `doc/5-tests/2026-07-12_180240/project-release-test-rules/tests/` 和 `doc/5-tests/2026-07-12_191712/project-release-test-rules/tests/`，不得修改历史期望。

## 覆盖范围

| 优先级 | 覆盖对象 | 主要失败样本 |
| --- | --- | --- |
| P0 | 场景契约、HTTP JSON、跨协议值和硬门禁 | 类型错误、跨接口不一致、覆盖不足、清理失败 |
| P1 | form、multipart、下载、SSE、WebSocket、Socket.IO | 媒体类型错误、断流、乱序、重复、ack 错误 |
| P2 | 兼容迁移、工具环境和触发规则 | 旧 PASS 晋级、依赖缺失、非 local 配置 |

## 目录复用说明

复用原因：本轮连续完成同一来源对象 `REQ-RT-20260712-001` 的 `CYCLE-RT-13..18`，测试代码、fixture 和逐任务证据在同一时间戳根目录累积；新建时间戳会割裂同一轮追踪链。

## 验证结论

| 验证项 | 结果 | 说明 |
| --- | --- | --- |
| 最终代码基线连续三轮 | PASS | 42/42、42/42、42/42 |
| 文档收口后复验 | PASS | 42/42 |
| 历史兼容 | PASS | 27/27、37/37 |
| Skill 与字典 | PASS | quick validate 与生成器通过 |
| strict 工程文档 | PASS | requirement、acceptance、overview、C13-C18、master |
| 总审查与最终验收 | PASS | 无残留 P0/P1，最终状态 accepted |

所有 `FAIL/BLOCKED/PENDING`、残留进程/端口/数据、非 local 来源或依赖污染继续禁止自动放行；当前归档结果未命中这些阻断条件。
