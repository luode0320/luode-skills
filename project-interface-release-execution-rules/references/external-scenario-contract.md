# 外部消费者场景契约

> 唯一行为 owner：`project-interface-release-execution-rules`。本文件只承接 `external-scenario/1.0` 契约，不产生平行 Skill。

## 版本与目录结构

- 场景命名空间固定为 `external-scenario/1.0`，不得与接口 IR `2.0` 或旧结果迁移版本混用。
- `scenario-catalog.yaml` 根节点固定包含 `schema_version` 与 `scenarios` 映射。
- 每个场景必须完整声明 `scenario_id`、`risk`、`consumers`、`source_evidence`、`source_fingerprint`、`lifecycle`、`preconditions`、`steps`、`assertions`、`cleanup` 和 `verification`。
- `scenario_id` 必须与映射键相同；来源指纹由规范化来源证据计算，漂移时目录整体校验失败。

## 生命周期与晋级

- 生命周期固定为 `candidate -> verified -> stale/quarantined -> retired`。
- AI 或规则生成器只能生成 `candidate`，不能直接进入发布门禁。
- 晋级 `verified` 必须同时满足 `contract_valid`、`positive_passed`、`fault_detected`、`cleanup_passed`、`source_current` 五项全真，并且只能由 `promote_to_verified()` 生成 `external-verify/1.0` 晋级记录。
- `verification` 的 verified 形状固定为五项门槛、`verification_run_id`、`positive_result/fault_result/cleanup_result`、`source_fingerprint` 、`artifact_path/artifact_sha256` 以及 `method/candidate_fingerprint/verification_digest`；结果摘要只保留 run、场景、状态、失败分类和清理失败数，不携带原始报文。
- 候选指纹绑定场景身份、来源、步骤、断言和清理但排除 `lifecycle/verification`；验证摘要再绑定正向 PASS、故障注入 FAIL、cleanup PASS、来源指纹和 verification run，loader 必须从项目根回读 `.release-test-engine/verification-evidence/*.json`，校验文件 SHA-256 并重算两层摘要。
- 仅手写 `lifecycle: verified` 和五个布尔值、缺任一结构化运行摘要、缺 artifact root、文件缺失或摘要不符、篡改晋级后的步骤或复制失配摘要都必须阻断加载；candidate 仍可保存未完成的验证状态但不得进入门禁。
- `verified` 场景若包含非 `GET/HEAD/OPTIONS` HTTP 请求，必须声明非空顶层清理；空清理不能解释为成功。
- 来源漂移、验证门槛不完整、非 local 前置条件、未知字段或未知动作均阻断加载。

## 声明式动作与执行边界

- 主步骤动作只允许 `http.request`、`sse.expect`、`ws.connect/send/expect/close`、`socketio.connect/emit/expect/disconnect`、`state.probe` 和 `cleanup`。
- 场景与清理都禁止嵌入任意代码、shell、原始 SQL 或动态表达式。
- 捕获值必须使用 JSON Pointer；配置中的 `${capture.<name>}` 只能引用已经完成的结构化捕获。
- 默认场景串行；只有连续步骤显式声明同一 `parallel_group` 时并发，SSE 并行组必须在响应头就绪后才启动触发动作。

## 确定性 oracle

- 正确性优先使用外部状态码、响应 schema、类型、枚举、相等、包含、正则、数量、摘要、跨路径相等、事件关联、顺序、唯一性和最终一致性等待。
- 外部响应或事件失败时立即保持 FAIL/BLOCKED，`state.probe` 不得覆盖外部结论。
- `state.probe` 只能调用项目显式注册的只读 allowlist，配置来源必须为 local，禁止携带 SQL。
- 传输错误只允许持久化白名单协议错误码；主流程与 cleanup 的断言实际值、expected 值、URL、鉴权内容和敏感报文均不得进入失败原因。

## 安全、脱敏与清理

- 正式运行只接受 local 配置来源；`test/staging/pre/release/prod/production` 一律 BLOCKED。
- `token/access_token/refresh_token/password/secret/authorization/cookie/set-cookie/api-key` 等字段递归脱敏。
- 原始敏感报文只允许存在于内存或受控临时目录，正式产物只保存脱敏值、长度或摘要。
- 主流程 PASS、FAIL 或 BLOCKED 后都必须执行声明清理；清理失败立即升级为 `CLEANUP_FAILED`，并停止后续写场景。
