# 平台能力矩阵

本表只描述通用准入条件。平台名称不是 capability；adapter 必须用真实 API/CLI 或受管进程接口证明能力，并以当前版本和 local 配置验证。

| 组件类型 | 常见故障 | 最低能力 | 可选高阶能力 | 无能力时的边界 |
| --- | --- | --- | --- | --- |
| MCP transport/server | timeout、EOF、连接 reset、协议不可用 | L1 probe | L2 reconnect、L3 server reload、L4 managed restart、L5 resume | 只能诊断并人工重连；不能猜测 server 进程或启动参数 |
| AI 编码/代理插件 | 插件 host 卡死、能力消失、版本不兼容 | L1 probe | L3 隔离 reload、L4 受管 host restart、L5 task resume | 不能把安装/启用动作当运行期恢复；无生命周期 API 则 manual_handoff |
| 浏览器自动化会话 | profile 断开、页面会话失效、浏览器进程退出 | L1 probe | L2 rebind、L3 profile/session reload、L4 受管浏览器 restart、L5 checkpoint resume | 不能清除认证数据或对所有 profile 执行 close-all |
| 外部工具/本地服务 | 子进程退出、端口不可用、响应格式异常 | L1 probe | L2 reconnect、L4 指定实例 restart | 只能操作当前任务拥有的实例；不能按模糊名称杀进程 |
| 智能体宿主 | 主进程崩溃、宿主 API 不可用、上下文丢失 | L1 probe | L4 host restart、L5 startup resume | 没有启动续接 hook 时最多报告 restarted，不得承诺任务继续 |

## 注册准入

1. adapter 先声明 `capabilities`、组件作用域、授权、side effects、fingerprint 和回滚策略。
2. 使用 local fixture 注入 timeout、EOF、断连和进程重启，验证 `probe -> action -> wait_ready -> original_success_criterion`。
3. 只有测试通过的等级才能注册；声明 L5 必须同时提供 checkpoint 和 resume，并在新进程启动后验证 token 与任务指纹。
4. 平台版本、配置来源或 API 变化时降级为 L0/L1，重新验证后才能恢复等级。

## 结果含义

- `reconnected`/`reloaded`/`restarted` 表示工具链恢复，不表示原任务已继续。
- `resumed` 只表示检查点续接且原成功标准通过。
- `manual_handoff` 表示需要人工/上层 agent 决策，`blocked` 表示规则拒绝继续；两者都不可重试循环。
