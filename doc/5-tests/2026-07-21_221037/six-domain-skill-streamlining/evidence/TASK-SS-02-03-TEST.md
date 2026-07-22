# EVD-SS-02-03-TEST：需求域 discovery 旧目录删除测试

结论：PASS；影响：`requirement-discovery-rules` 已在承接、消费者、资产、字典和 scoped post-delete 验证通过后真实删除；范围：单候选 pre-delete、物理删除、字典再生、资产 retired 标记和 scoped post-delete；非范围：其他 10 个退役候选的全局 pre-delete/post-delete；变化：验证器新增 `--only-source` 增量闸门和 post-delete retired asset 生命周期，避免把尚未迁移的其他候选混入当前候选结论；完成标准：当前候选无活跃旧引用、source 目录不存在、owner/route/字典和回滚定位均成立；验证状态：PASS。

## 执行环境

- 仓库根目录：`F:\luode-skills`
- 环境：local 文件系统、Python UTF-8、PowerShell 7。
- 外部连接：`N/A + 原因 + 证据`：只操作本地规则资产，不连接任何业务环境。

## 删除前真实测试

```powershell
pwsh -NoProfile -File "doc/5-tests/2026-07-21_221037/six-domain-skill-streamlining/run_domain_trigger_cases.ps1" -RepoRoot "F:\luode-skills" -Phase pre-delete -OnlySource "requirement-discovery-rules"
```

结果：退出码 `0`，`valid=true`、`errors=[]`。断言 source、target、route marker、manifest、资产、消费者和 discovery fixtures 均通过。

## 实际删除与 post-delete 真实测试

```powershell
python -B "skill-dictionary/generate_dictionary.py"
pwsh -NoProfile -File "doc/5-tests/2026-07-21_221037/six-domain-skill-streamlining/run_domain_trigger_cases.ps1" -RepoRoot "F:\luode-skills" -Phase post-delete -OnlySource "requirement-discovery-rules"
```

结果：

- 物理 source `requirement-discovery-rules/` 不存在。
- 字典再生返回 `implemented_total=87`、`planned_missing=1`，且 `skill-dictionary/data.js` 与 `字典.md` 不再包含旧入口。
- scoped post-delete 返回 `valid=true`、`errors=[]`、退出码 `0`。
- `domain-asset-inventory.json` 保留冻结文件记录并标记 `retired: true`，未把旧哈希伪装成当前磁盘资产。

## 执行失败恢复证据

首轮 post-delete 在验证器仍把 `delete_authorized=true` 当作 baseline-only 非法状态时返回非零；已修正验证器生命周期判断，随后以相同 candidate、相同 phase 和相同成功标准复验，返回退出码 `0`。该修复属于测试闸门实现修复，不改变 Skill 规则或删除授权边界。

## 清理与回滚

- 清理：测试使用 `python -B`；删除测试过程中的 `__pycache__`；不写 local 业务数据。
- 回滚：以 `baseline_commit: 548fe02a42b6572b75330fc8b8827b62a4218b5f` 恢复 `requirement-discovery-rules/`，恢复 owner refs、consumer index、manifest、asset inventory、字典生成物和验证器改动；不回滚已闭环周期。
- 停止：任何 post-delete 失败、字典仍残留旧入口、owner route 缺失或回滚定位失效时，停止后续候选删除。