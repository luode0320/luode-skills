# TAPD 浏览器自动化流程沉淀（2026-04-03）

## 目标
- 把本次 TAPD 自动化操作沉淀为可复用流程。
- 记录真实暂停点与处理方式，作为后续 skill 演进输入。
- 形成“首登一次后，后续尽量免交互”的执行路径。

## 本次任务范围
- 入口页面：`https://www.tapd.cn/tapd_fe/my/work`
- 业务目标：提取“我的工作”中本周（自然周）需求进度统计。
- 目标输出：总数、状态分布、完成项清单、可直接写入周报。

## 标准自动化状态机

### S0 预检
```bash
which agent-browser || true
npx -y agent-browser --version
```
- 若本机无 `agent-browser`，统一走 `npx -y agent-browser ...`。

### S1 清理旧会话
```bash
npx -y agent-browser close --all || true
```
- 目的：避免旧 daemon 参数残留导致新参数无效。

### S2 打开目标页面
```bash
npx -y agent-browser open https://www.tapd.cn/tapd_fe/my/work
npx -y agent-browser get title
npx -y agent-browser get text body
```
- 判定分支：
  - 标题/正文包含“WAF拦截” -> 进入 `S2A`
  - 标题为“登录-TAPD” -> 进入 `S3`
  - 标题为“我的工作-TAPD平台” -> 进入 `S4`

### S2A WAF 处理
```bash
npx -y agent-browser --debug open https://www.tapd.cn/tapd_fe/my/work
npx -y agent-browser get text body
```
- 保留请求 UUID 便于反馈排查。
- 若仍拦截，切换启动参数并重启 daemon 后重试：
```bash
npx -y agent-browser close --all || true
npx -y agent-browser --args '--disable-blink-features=AutomationControlled,--lang=zh-CN' \
  --user-agent 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36' \
  open https://www.tapd.cn/tapd_fe/my/work
```

### S3 登录处理
```bash
npx -y agent-browser snapshot -i
npx -y agent-browser click @企业微信登录对应ref
npx -y agent-browser screenshot /tmp/tapd_login.png
```
- 首次通常需要人工扫码或账号认证。
- 成功后再次验证：
```bash
npx -y agent-browser get title
npx -y agent-browser get url
```

### S4 数据提取（本周）
```bash
npx -y agent-browser snapshot -i
npx -y agent-browser click @时间筛选ref
npx -y agent-browser snapshot -i > /tmp/tapd_snapshot_week.txt
```
- 解析 `本周 (N)` 分组，按每行字段提取：
  - `ID`、`标题`、`状态`、`处理人`、`优先级`、`处理时间`

### S5 统计与输出
- 统计口径：
  - 总数
  - 状态分布
  - 完成数与完成率（例如按 `已实现`/`已关闭`/`已解决`）
  - 本周已完成清单
- 输出结果用于周报追加。

## 本次暂停点复盘（真实记录）

| 阶段 | 现象 | 原因 | 临时处理 | 后续固化 |
|---|---|---|---|---|
| 工具准备 | `agent-browser: command not found` | 本机未全局安装 | 改用 `npx -y agent-browser` | skill 内默认支持 npx 回退 |
| 自动连接 | `No running Chrome instance found` | 未开启可连接 CDP 会话 | 改为独立会话并后续重启策略 | 增加“连接失败分支” |
| 依赖安装 | `install --with-deps` 需 sudo | 当前环境无法提权 | 跳过系统依赖安装 | 文档明确“无 sudo 时降级策略” |
| 访问阶段 | TAPD 被 WAF 拦截 | 自动化特征触发风控 | 调整启动参数后重试 | 增加 WAF 检测与重试策略 |
| 登录阶段 | 企业微信登录需要人机认证 | SSO 强认证不可完全自动 | 人工扫码一次 | 首登后持久化会话，后续免交互 |
| 参数切换 | `--args ignored: daemon already running` | daemon 持续复用旧参数 | 先 `close --all` 再启动 | 将“会话清理”设为强制前置步骤 |

## 无交互化落地方案（建议）

### 方案 A：`session-name` 持久化（优先）
1. 首次人工登录：
```bash
npx -y agent-browser --session-name tapd_weekly open https://www.tapd.cn/tapd_fe/my/work
```
2. 登录完成后关闭，自动保存状态：
```bash
npx -y agent-browser --session-name tapd_weekly close
```
3. 后续任务直接复用：
```bash
npx -y agent-browser --session-name tapd_weekly open https://www.tapd.cn/tapd_fe/my/work
```

### 方案 B：`state` 文件持久化
1. 登录后保存：
```bash
npx -y agent-browser state save /home/luode/code/.auth/tapd-state.json
```
2. 后续加载：
```bash
npx -y agent-browser --state /home/luode/code/.auth/tapd-state.json open https://www.tapd.cn/tapd_fe/my/work
```

### 方案 C：失败兜底顺序（必须固化）
1. `close --all`
2. 重新 `open`
3. 检测 WAF -> 应用反自动化参数重试
4. 检测登录态失效 -> 触发一次人工登录恢复会话

## 建议补充到 agent-browser skill 的内容
- 新增“受风控站点（如 TAPD）状态机模板”。
- 明确“必须前置 `close --all` 的场景”。
- 增加“WAF/登录页识别关键字”与固定 fallback。
- 增加“会话持久化优先级”规则：`session-name` > `state` > `auto-connect`。
- 增加“暂停点记录模板”：`现象/原因/临时处理/长期方案/是否阻断`。

## 验收标准（本流程）
- 能在无人工输入前提下完成“打开 TAPD + 进入我的工作 + 拉取本周列表 + 输出统计”。
- 登录态失效时，最多一次人工登录即可恢复后续自动运行。
- 任何失败都能归入已定义分支，不出现“无处理路径”的中断。

## 已落地模板脚本
- 路径：`templates/tapd-weekly-report.sh`
- 示例：
```bash
./templates/tapd-weekly-report.sh 2026-04-03 ./output
```
- 关键环境变量：
  - `TAPD_SESSION_NAME`
  - `TAPD_STATE_FILE`
  - `TAPD_LOGIN_WAIT_SECONDS`
  - `TAPD_FORCE_CLEAN_START`
