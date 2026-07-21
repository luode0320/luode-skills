# TASK-SPLIT-05-01 原子化映射证据

- 测试：`TEST-SPLIT-017`（`python -X utf8 validate_skill_split.py --mode mapping --mapping mapping/agent-browser.yaml`）。
- 映射产物：`doc/5-tests/2026-07-17_155229/skill-split-validation/mapping/agent-browser.yaml`，37 条 `R-AB-001`~`R-AB-037` 规则 + 5 条 `shared_resources`，共 42 条目，`owner`/`migration_action` 覆盖率 100%。
- 基线指纹（只读核对，未改动）：`agent-browser/SKILL.md`：36,228B，MD5 `59917697eefafef9221d4484cb1d5225`（远超 24,000B hard_warning，是本次拆分体积治理的最优先目标）；11 个 `references/*.md`（合计约 53KB）；4 个 `templates/*.sh`（合计约 14.7KB），逐文件字节数与 MD5 见本轮 `Get-ChildItem | Get-FileHash` 命令行输出。
- 拆分结论：`group_a = browser-session-automation-rules`（核心工作流、认证、session、快照/交互、批量执行、截图清理、eval、4 个业务模板，共 28 条 group_a）；`group_b = browser-advanced-testing-rules`（网络 HAR、diff、录制/profiling、代理、多 session 观测面板，共 6 条 group_b）；3 条 split/split_rewrite（description、"常用命令"网络/diff 子集拆分、"可视化浏览器调试"小节 highlight/inspect 归核心与 record/profiler 归高级、"深入文档"引用表拆分）；5 条 shared_duplicate（安全边界、配置文件优先级、引擎选择、项目联调路由、失败案例册）。
- 关键决策：`references/commands.md`（11,191B 完整命令参考）判定为 `group_a` 整份迁移的主参考，`group_b` 不复制该文件，只通过章节锚点交叉引用其网络/HAR/diff 小节，避免同一份参考被两组同时持有导致后续维护双写。
- 命令与结果：`python -X utf8 validate_skill_split.py --mode mapping --mapping mapping/agent-browser.yaml` → 退出码 0，`[通过] mapping：原子化映射 42 条目全部有 owner 与 migration_action，覆盖率 100%`。
- 结论：PASS。旧 skill 文件保持冻结基线，未做任何改动。