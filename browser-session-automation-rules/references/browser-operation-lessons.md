# 浏览器操作经验手册

这份手册用于沉淀“能跑通”和“能稳定复现”的实战经验，优先于理想化命令示例。

## 1. 页面状态三分法（先判断再操作）

每次 `open` 后立即执行：

```bash
agent-browser get title
agent-browser get text body
```

按结果分流：
- 业务页：继续自动化
- 登录页：走登录分支（优先复用 session/state）
- WAF/风控页：走反风控分支

不要在未判定状态时直接 `snapshot -> click`，否则大量失败都变成“未知原因”。

## 2. 启动参数切换的硬规则

当要调整 `--args`、`--user-agent`、profile 等启动参数时，必须先清理旧会话：

```bash
agent-browser close --all || true
```

原因：旧 daemon 可能复用已有参数，导致新参数未真正生效。

## 3. Ref 生命周期硬规则

以下动作后旧 ref 一律视为失效：
- 导航跳转
- 表单提交
- 弹窗/抽屉切换
- 异步局部刷新

固定收口：

```bash
agent-browser wait --load networkidle
agent-browser snapshot -i
```

## 4. 风控/WAF 兜底模板

当页面命中风控关键字（如“WAF”“请求已中断”）：

```bash
agent-browser close --all || true
agent-browser --args '--disable-blink-features=AutomationControlled,--lang=zh-CN' \
  --user-agent 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36' \
  open <url>
agent-browser wait --load networkidle || true
agent-browser get title
agent-browser get text body
```

## 5. 登录与状态复用优先级

优先级：
1. `--session-name`
2. `--state <file>`
3. `--auto-connect`

建议：首次人工登录后，固定复用同一 `session-name`，避免重复登录和重复风控触发。

## 6. 证据留存最小集

每次关键步骤至少输出 4 类证据：
- 当前 URL：`agent-browser get url`
- 当前标题：`agent-browser get title`
- 结构快照：`agent-browser snapshot -i`
- 页面截图：`agent-browser screenshot <path>`

失败回报必须包含“最后一次证据”，避免只回“失败”。

## 7. 稳定执行清单（可直接复用）

1. 预检：`agent-browser --version`
2. 清会话（可选）：`agent-browser close --all || true`
3. 打开页面：`open`
4. 判定状态：`get title` + `get text body`
5. 分支处理：业务/登录/WAF
6. 交互：`snapshot -i` -> `click/fill/...`
7. 每次页面变化后：`wait --load networkidle` + `snapshot -i`
8. 结果校验：`get text` / `diff snapshot`
9. 收尾：`close` 或保留具名 session

## 8. 回传格式建议

建议固定返回：
- 当前阶段（S0/S1/S2...）
- 执行命令（可省略敏感参数）
- 结果摘要
- 下一步动作
- 失败证据路径（若失败）

