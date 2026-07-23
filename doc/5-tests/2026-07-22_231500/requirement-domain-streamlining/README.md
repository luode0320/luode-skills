# 需求域 Skill 精简专项验证

- RUN_TS：`2026-07-22_231500`
- 基线：`76ee419d59396d919fea04ed55ea373ddeb8cb26`
- 阶段：`baseline`、`trigger`、`consumer`、`reference`、`post-cleanup`。
- 验证器只真实扫描磁盘；`doc/` 中的历史、manifest、fixture 和证据不作为活跃消费者。
- 失败时对应候选保持 `HOLD`，不执行 Git 写历史。
