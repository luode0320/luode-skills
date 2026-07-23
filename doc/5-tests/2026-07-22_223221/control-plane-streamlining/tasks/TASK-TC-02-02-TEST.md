# TASK-TC-02-02 真实测试证据

## 测试目标

验证“验证入口、Git 当前轮和计划 Owner 边界”已经按冻结写集实现，自动触发、用户习惯、安全、授权、停止、回滚和输出协议未被弱化。

## 输入与范围

- 实现范围：trigger fixtures 与专项 validator
- 测试环境：`local` 仓库文件与本地 Python/Bash 工具；未连接 test、staging 或 production。
- 样本来源：本任务 manifest、trigger fixtures、迁移后 Skill 资产和真实子代理生命周期记录。

## 执行与断言

- 主要证据：`doc/5-tests/2026-07-22_223221/control-plane-streamlining/evidence/trigger-result.json`
- 通过标准：trigger 返回 valid=true，历史轮 Git 不继承，明确单域不被阶段路由抢占。
- 失败预期：任一目标文件缺失、旧入口仍被活跃消费者引用、触发正负样本失败、生命周期数量不一致或机器校验非零时，本任务必须停止并保持/恢复为 HOLD。

## 清理与回滚

- 临时测试目录已清理，仓库只保留正式测试证据。
- 回滚定位使用 manifest 中冻结的 `baseline_commit`、source tree hash 和 `rollback_locator`；不通过时只回滚当前候选。

## 测试结论

**PASS**：trigger 返回 valid=true，历史轮 Git 不继承，明确单域不被阶段路由抢占。
