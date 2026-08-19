# workbuddy-absorption-map（吸收裁决登记表）

> 归属 owner：`apifox`。登记外部 skill 精华吸收裁决，每行含"整理去重"列。追加式维护，不覆盖历史。

## 本次吸收：api-test-automation-pro__skillhub（API测试自动化专家版 v1.5.0）

- 吸收时间：2026-08-19
- 来源：本地安装 `api-test-automation-pro__skillhub`（用户级 + 工作区双副本，MIT）
- 吸收方式：补缺式吸收（用户已确认：拒绝脚本层、吸收后删源、apifox 为主 + test-strategy-rules 策略引用）
- 裁决摘要：合并 9 条 / 保留本地 7 条 / 拒绝 4 条

| # | 外部精华 | 本地现状（吸收前） | 裁决 | 落点 | 整理去重 |
|---|---------|-------------------|------|------|----------|
| 1 | 契约测试方法论（Schema 校验/变化检测） | test-case-generation 仅"结构断言"简单映射 | 合并 | 新建 `modules/test-contract.md` | test-case-generation 原"契约测试（映射到 apifox）"小节压缩为引用 |
| 2 | 性能测试 4 类型 + P50-P99 指标 + 预热渐进加压 | 同上仅"重复执行+响应时间断言" | 合并 | 新建 `modules/test-performance.md` | test-case-generation 原"性能测试（映射到 apifox）"小节压缩为引用 |
| 3 | YAML 批量定义方法论（when/loop/parallel/hooks） | 本地无 YAML 定义能力 | 合并 | 新建 `modules/test-yaml-definition.md` | 无重复；无 apifox 映射语法标注"仅设计参考"防跑偏 |
| 4 | 五层健康评分（功能30/性能20/安全20/稳定15/契约15） | 本地无健康评分 | 合并 | 新建 `modules/test-health-score.md` | 无重复；数据缺口按 0 计并明示 |
| 5 | 四层诊断（网络/请求/业务/性能→根因→建议） | testing-pitfalls 有 31 条陷阱但无分层诊断 | 合并 | `testing-pitfalls.md` 追加第七节 | 与"运行失败时"排查用法衔接，统一到使用方式第 2 条 |
| 6 | 8 类异常 Fallback 策略表 | 本地无系统化 Fallback 表 | 合并 | `testing-pitfalls.md` 追加第八节 | 与"常见恢复"表归类去重 |
| 7 | 三重门控（设计/执行/报告） | SKILL.md 已有"必须询问用户"但非阶段门控 | 合并 | `SKILL.md` 核心共享规则追加 | 与"必须询问用户"清单归类（事项确认 vs 阶段确认） |
| 8 | Top20 必检项 + 用例类型级 P0/P1/P2 | test-selection-policy 有接口级 P0/P1/P2 | 合并 | `testing-pitfalls.md` 追加第十/十一节 | 与 test-selection-policy 接口级分级显式区分声明 |
| 9 | 9 类安全 payload 分类 + 断言顺序 + 16 种断言速查 | 鉴权安全陷阱仅 4 条；断言规则 4 行 | 合并 | `testing-pitfalls.md` 第九节 + `test-case.md` 断言顺序/速查 | 与第四节"鉴权与安全陷阱"合并去重（用例层 vs 漏洞类层） |
| 10 | 自然语言→用例、测试点分析、6 大用例矩阵 | test-case-generation 已吸收 | 保留本地 | — | N/A（已覆盖） |
| 11 | 陷阱库 140 条全量 | 本地 31 条 apifox 场景化 | 保留本地（抽条） | `testing-pitfalls.md` 第十二节抽取 8 条 | 只抽本地未覆盖高价值条目（幂等/弱网/分布式），不全量搬 |
| 12 | Mock/多格式报告/GraphQL | apifox 内置能力 | 保留本地 | — | N/A（已覆盖） |
| 13 | Spring Doc 解析 | swag-openapi-maintainer-rules 已覆盖 | 保留本地 | — | N/A（已覆盖） |
| 14 | 22 个 Python 脚本（约 1 万行） | 红线：接口测试必须 apifox 落地 | 拒绝 | — | N/A（拒绝原因：脚本层与 apifox 落地红线冲突，记入 source-notes） |
| 15 | README 缺失 5 references（security_checks 等） | 均为脚本层专属文档 | 拒绝 | — | N/A（精华从 README/SKILL.md 可读描述吸收） |
| 16 | HTTP 全表参考 | troubleshooting/test-case 已覆盖场景 | 拒绝 | — | N/A（低频冗余） |

**净增减预估**：新增 4 模块（16,520 字节）+ 强化 3 模块 + SKILL.md；整理去重约 6 处（test-case-generation 压缩 -568 字节、pitfalls 归类去重、SKILL.md 门控归类）。

**棘轮验证**：darwin 8 维评分 吸收前约 75.7 → 吸收后 92.1（独立子 agent 评分，2026-08-19）；实测 3/3 路由命中；保留。

**源处置**：吸收确认后删除源 skill 双副本（用户级 `C:\Users\luode\.workbuddy\skills\api-test-automation-pro__skillhub\` + 工作区 `D:\谷歌云盘\luode-skills\api-test-automation-pro__skillhub\`），详见 source-notes。
