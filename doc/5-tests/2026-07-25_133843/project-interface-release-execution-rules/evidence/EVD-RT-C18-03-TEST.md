# EVD-RT-C18-03-TEST

## 真实测试

- 修复后最终代码基线连续三轮：`57/57 PASS`，unittest 内部分别耗时 13.500 秒、14.543 秒、17.855 秒。
- 文档、字典和静态门禁稳定后的最终收口复验：`57/57 PASS`，unittest 内部耗时 14.686 秒。
- 历史兼容回归：`27/27 PASS`（2.135 秒）、`37/37 PASS`（3.181 秒）。执行前确认旧 Owner 路径 `ABSENT`，创建指向唯一 Owner 的临时符号链接并核对解析目标，执行后在 `finally` 删除并再次确认 `ABSENT`。
- 当前新增模块和测试 `compileall`：PASS；兼容入口 `py_compile`：PASS。
- 函数元数据审计缺口：0；长函数及嵌套长块编号注释缺口：0。

## Skill 与文档门禁

- `quick_validate.py project-interface-release-execution-rules`：`Skill is valid!`。
- `skill-dictionary/generate_dictionary.py`：PASS，生成 `data.js` 与 `字典.md`。
- strict validator：requirement、acceptance、implementation_overview、implementation_cycle（C13-C18）和 implementation_master 全部 PASS。
- `git diff --check`：PASS；既有 CRLF/LF 提示不构成错误且未进行全文件行尾转换。

## 失败样本

错误类型/枚举、跨接口值不一致、SSE 断流、WebSocket 丢失/乱序/重复、Socket.IO ack 错误、来源漂移、非 local、敏感字段、探针越权和清理失败均稳定返回预期 FAIL/BLOCKED/PENDING，不会伪造 PASS。新增负向样本还覆盖直接、父级及输出目录内文件 symlink 越界、数字敏感值泄漏、短敏感值验证受限、新旧场景迁移脱敏、canonical 根级 README、最终 SHA-256、manifest 门禁回流，以及真实子进程 `BLOCKED/3`、`PENDING/4` 和长敏感原值不进入输出。
