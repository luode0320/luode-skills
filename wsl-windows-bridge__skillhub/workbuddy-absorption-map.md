# workbuddy-absorption-map

本文件登记 `wsl-windows-bridge` 的吸收/调整裁决历史（外部吸收 + 内部更新）。

## 2026-08-26 内部更新：Windows 宿主侧工作流吸收

| 来源 | 条目 | 本地现状 | 裁决 | 落点 | 整理去重 |
| --- | --- | --- | --- | --- | --- |
| 知识库 `开发环境/agent在Windows项目在WSL的编译启动调试经验.md`（2026-08-26 实测沉淀） | 双路线原则（读写留 Windows / 执行进 WSL 或 Temp 副本） | AGENTS.md 内联 + wsl-shell-reliability 仅覆盖 shell 选择 | 合并 | SKILL.md「Windows 宿主侧工作流」节 + `references/windows-host-side-workflow.md` | N/A（新 reference，无存量可清） |
| 同上 | go.mod RLock → Temp 副本；重同步覆盖坑；陈旧文件坑 | 无 | 合并 | 同上（配方 1） | N/A |
| 同上 | 128xx 端口段被 svchost 接管 → 18080 | 无 | 合并 | 同上（配方 2） | N/A |
| 同上 | 验证码 dev 放行、登录失败 HTTP 恒 200 | 无 | 合并 | 同上（配方 3） | N/A |
| 同上 | Bash 调 PowerShell 拦截、Windows Python /tmp 路径坑 | 无 | 合并 | 同上（配方 4） | N/A |
| 同上 | apifox 遥测弹窗 | `apifox-cli` SKILL.md 61-77 行已详细覆盖 | 保留本地（本地更强） | 引用 `apifox-cli` | **收敛 1 处**：reference 初稿含重复细节 → 改为「权威源引用」，删除重复段落 |
| 同上 | 两套 $HOME 凭据不共享 | 本 skill Common Scenarios 已有 win-path/win-copy 流程 | 保留本地 | 交叉引用，不复制 | N/A |
| 同上 | 空间不支持 WSL/UNC、回复路径口径 | 用户级 MEMORY + AGENTS.md 已有 | 保留本地 | 未写入 | N/A |

- 环境依赖登记：`APIFOX_CLI_TELEMETRY=0`（用户级环境变量，详见 apifox-cli）、端口 18080（本机约定）。reference 附「环境依赖」表。
- 同域冗余扫描：范围 = wsl-windows-bridge / wsl-shell-reliability / windows-encoding-rules / apifox-cli / wsl-powershell / wsl-path-converter。发现 1 处重复（apifox 遥测，与 apifox-cli 61-77 行），已收敛为引用；无门控层叠；无散落产物；引用链可达。**PASS**。
- 结构校验：`quick_validate.py` 基线报 `compatibility` 违规键 → 本次一并合规化（移入 metadata）→ 修改后 `Skill is valid!` EXIT=0。
- 净增体积：+1 reference（约 3.2KB）+ SKILL.md +1 节/-1 行 frontmatter 调整。

## 2026-10-08 执行中 gap 回补：Bash 工具成对反斜杠减半提醒

| 来源 | 条目 | 本地现状 | 裁决 | 落点 | 整理去重 | 环境依赖 | agent 通用性 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 知识库执行案例 `20-Knowledge/execution-failure-cases/wsl-windows-bridge/20260930-204809-exec-case-bash-tool-halves-double-backslash.md`（candidate，occurrences 3） | agent 在 Windows 宿主经 Bash 工具执行时，命令文本里的成对反斜杠在进 shell 前被减半，单引号与 `<<'EOF'` 挡不住；单个反斜杠、文件写入工具落盘的内容不受影响；正则字符类因此静默漏检或报语法错误，Python 的反斜杠字面量变成未闭合字符串 | 「免桥直读要点」第 3 步推荐 quoted heredoc，只覆盖 agent 在 WSL 内；反向拓扑工作流没有这条提醒；陷阱清单在文件级限定 WSL 内 | 合并 | `references/windows-host-side-workflow.md` 配方 5「现象」、触发信号 1 条（含 Python 3.9 及以下的报错文字）、引言补一句配方 5 不受「项目在 WSL」限定；SKILL.md 第 3 步后加拓扑限定指针 | 规则正文只写配方 5（单一权威），SKILL.md 只留指针；陷阱清单不改，由配方 5「范围」条覆盖 | N/A：只改写法 | 通用：实测宿主为 Claude Code 桌面版 + Git Bash，其他宿主未验证；文件写入工具与 `chr(92)` 不依赖宿主，`cygpath` 只在 Git Bash / MSYS2 / Cygwin 里有 |
| 同上 | 替代写法（按用途选）：原样写正文或必须保留字面反斜杠的脚本，用文件写入工具写成文件；内联 Python 用 `chr(92)` 构造反斜杠，匹配前 `.replace(chr(92), '/')`；传给 Windows 程序的路径写 `C:/Users/...`，`/d/...` 只作 Git Bash 命令参数，需要反斜杠形式时用 `cygpath -w` 运行时生成；不写四个去凑数；扫描结论带已知命中项作对照组 | 无 | 合并 | 配方 5「做法」分用途子项；SKILL.md 指针句先给原样写正文的做法，再给内联脚本写法 | N/A：新增 | N/A：`cygpath` 随 Git Bash 提供，WSL 内对应 `wslpath -w` | 通用 |
| 同上 | 主题列表登记 | 「Windows 宿主侧工作流」一节的主题列表缺这一项 | 合并 | SKILL.md 该节主题列表补「Bash 工具成对反斜杠减半（与项目位置无关）」 | N/A | N/A | 通用 |

- 环境依赖登记：0 项（不新增环境变量、配置、hook 或依赖；证据路径用知识库裸相对路径），无需附带自检能力。
- 同域冗余扫描：范围 = 全仓检索 quoted heredoc、成对反斜杠与反斜杠减半相关表述，重点核对本 skill（含 `references/wsl-windows-comm-pitfalls.md`）、`wsl-shell-reliability`、`windows-encoding-rules`、`wsl-powershell`、`windows-powershell-environment-rules`、`knowledge-flow` 的 `references/wsl-access.md`。重复描述 0 处；已有拓扑限定、无需改 3 处（`wsl-access.md` 限定 WSL 并分流、`wsl-powershell`、`docker-direct-deploy` 的 CI 执行）；无门控层叠；无散落产物（替代写法实测的临时文件已删除，回读确认不存在）；引用链可达。**PASS**。
- 范围外发现（另开任务，本轮不改）：git 提交后校验在 Windows 宿主可能假通过（`git-collaboration-rules/references/branch-and-commit.md`）；其他 skill 的 heredoc、写入与转义写法缺 Windows 宿主指针（`wsl-service-deploy`、`browser-session-automation-rules`、`windows-encoding-rules`、`wsl-shell-reliability`）；多处规则文档疑似误写成对反斜杠。
- 替代写法实测（2026-10-08，Claude Code 桌面版 + Git Bash）：文件写入工具写入两个反斜杠，落盘仍为两个（`5c 5c`）；`chr(92)*2` 得两个；`.replace(chr(92), '/')` 得正斜杠路径；`cygpath -w` 输出反斜杠形式路径；命令文本中单个反斜杠不变。减半现象本身未在本轮复现（本轮约束禁止在命令文本写成对反斜杠），证据引用上述案例的四组复现。折叠后的形态用单个反斜杠直接实测：`[\/]` 对混合文本只命中正斜杠行（退出码 0），对只含反斜杠的文本零命中（退出码 1）；`[/\]` 在 rg 报正则解析错误（退出码 2），在 Python 抛 `re.error`；`print('\')` 报 `SyntaxError: unterminated string literal`；Windows Python 把 `/d/foo` 解析成 `D:\d\foo`。临时目录已删除并回读确认。
- 独立评分（只读子代理，未参与修改；改前按 HEAD，改后按工作树）：8 维改前 → 改后依次为 7→7、7→7、6→7、4→4、8→9、9→9、7→8、4→8，加权总分 61.9 → 75.9（+14.0）；只看维度 1–7 也从 51.9 升到 55.9（+4.0），棘轮通过，保留。维度 8 按场景推演打分（B1–B3 改前通过 1/3、改后 3/3），没有实跑测试 prompt，属暂定分。评分针对下一条修正之前的版本；修正后受子代理批次门禁限制，未再独立复评。
- 评分问题处置：与本 skill 相关的 8 项中，修正 5 项：`/d/...` 区分使用场合；按用途给出做法优先级；删去「任何宿主都无副作用」；退出码表述补全成立条件；补 Python 3.9 及以下的报错文字。部分修正 1 项：参考页引言补配方 5 的适用范围，SKILL.md「Windows 宿主侧工作流」的 `##` 标题仍写「项目在 WSL」。保留 2 项：description 没有减半触发词，和上面的标题一样要重跑字典才能改，而 `data.js`、`字典.md` 正被其他会话修改；陷阱清单第 120 行没有回指配方 5，但该文件第 3 行已限定 WSL 内，Windows 宿主入口由 SKILL.md 第 64、170 行覆盖。
- 结构校验：`quick_validate.py wsl-windows-bridge__skillhub` 输出 `Skill is valid!`，EXIT=0，评分问题修正后重跑结果相同；description 与 `##` 标题未改，未重跑字典。
- 净增体积：SKILL.md 9,365 → 9,824 字节（+459）；`references/windows-host-side-workflow.md` 4,270 → 6,657（+2,387）；`references/source-notes.md` 680 → 1,779（+1,099）；本文件追加本节。整理：没有同义重复可并，净增全部是新增提醒；SKILL.md 只加指针，规则正文单一权威在参考页。
