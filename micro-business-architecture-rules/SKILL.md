---
name: micro-business-architecture-rules
description: 当新建项目 / 新会话首轮检测到新或空仓库（缺业务代码骨架），或用户提出「微业务 / 伪微服务 / 按业务分目录包 / 业务隔离 / 业务互不关联 / RPC 通信 / 新业务开新包 / 一个项目一个服务的伪微服务」等诉求，或项目已存在微业务标记时自动触发。负责守护单项目单服务中的业务垂直切分和跨业务导入隔离：调用方只能导入目标业务域 `rpc/` 的 JSON 字符串公开函数，禁止导入目标业务私有层；提供幂等脚手架、标记与确定性校验，并以 CodeGraph 导入节点作为审查证据。具体目录、JSON 响应语义和引用边界由 `package-structure-rules` 唯一拥有；不要用它代替需求分析、实施规划、分层落点或实际编码。
---

# 微业务架构规则

## 目标

- 把微业务（伪微服务）的业务域隔离固化为可自动命中、可校验、可交接的规则。
- 让每个业务包自包含，调用方不能直接读取或引用其他业务域的私有代码、实体或状态。
- 用进程内 JSON 字符串 RPC 模拟服务接口边界，不引入网络 RPC、HTTP、消息队列或独立部署。

## 核心理念

- 微业务仍是一个项目、一个服务进程；切分目标是降低业务上下文和依赖耦合，不是创建真实微服务。
- 每个业务放在自己的 `business/<domain>/`；跨域仅导入目标域 `rpc/` 的公开函数，输入与输出都是 JSON 字符串。
- 被调用域在自身 `rpc/` 内解析请求、调用本域私有服务、序列化统一响应；调用方不会获得目标域实体、仓储模型或语言异常。

## 自动触发信号

- 用户提出微业务、伪微服务、业务隔离、跨业务通信、JSON RPC、按业务拆目录包或业务互不关联。
- 新会话首轮检测到新或空业务项目，或项目已有微业务标记。
- 用户要求新增业务包、创建业务域 RPC、校验业务隔离或审查跨业务导入。

## 进入后先做什么

1. 明确当前对象是业务项目，不是 `luode-skills` 规则仓库本身。
2. 新会话首轮先联动 `project-rule-file-bootstrap-rules`，再依 `trigger-and-marker.md` 判断引导或守护模式。
3. 需要目录、JSON 响应或引用边界时先查询 `package-structure-rules`；本 Skill 不复制其目录 Owner 职责。
4. 需要隔离检查时读取 `isolation-and-communication.md`，使用 `micro_business.py check` 做确定性门禁，并在审查时用 CodeGraph 导入节点复核证据。

## 核心原则

1. **业务垂直切分**：每个业务域是自包含目录包，私有实现只在本域中演进。
2. **跨域最小导入**：业务域 A 只能导入业务域 B 的 `rpc/`；`api/`、`service/`、`entity/`、`base/`、`constant/`、`init/`、`corntask/`、`util/` 均为目标域私有层。
3. **JSON 通信契约**：公开 RPC 函数接收 JSON 字符串，返回 JSON 字符串；返回值遵循根 `common/response.Response` 的 `code`、`status`、`message`、`data` 语义。
4. **失败不跨域抛出**：解析、校验与业务失败均序列化为统一响应，不能把目标域异常、实体或仓储模型泄漏给调用方。
5. **按需公开**：没有真实跨业务调用者时不创建 `rpc/`；新业务仅在需要时显式启用该目录。
6. **允许的公共例外**：根 `common/request`、`response`、`constant`、`error`、`validation` 和仅含非业务运行引用的 `global/` 可直接使用；`global/` 禁止承载业务实体、业务状态、业务列表或可变业务缓存。

## 与相邻 Skill 的边界

- `package-structure-rules`：唯一拥有 `business/<domain>/rpc/`、JSON 响应语义、目录查询、初始化、渲染和严格检查规则。
- `codegraph-analysis-rules`：拥有导入节点、调用链和影响面检索；本 Skill 只把其结果作为跨域隔离审查证据。
- `code-readability-rules`：拥有一般抽象取舍；本规则的 `rpc/` 是已冻结的跨域通信边界，不要求额外接口、注册或依赖注入层。
- `artifact-storage-rules`：拥有研发文档产物路径；本 Skill 不另建测试或文档目录。
- `architecture-doc-rules`：业务域与 RPC 关系可按需摘要回写项目架构文档。

## 执行入口

- 触发、标记和守护：`references/trigger-and-marker.md`。
- 业务域目录与按需脚手架：`references/directory-layout.md`、`scripts/micro_business.py scaffold <domain> --with-rpc`。
- 隔离、JSON 通信与 CodeGraph 审查：`references/isolation-and-communication.md`、`scripts/micro_business.py check`。
- 业务包 README 与全局索引：`references/md-convention.md`。

## 通过标准

- `micro_business.py check` 只接受跨业务到目标 `rpc/` 的精确导入，并稳定拒绝目标域任何私有层导入。
- CodeGraph 可定位合规 RPC 导入和每一种私有层违规导入，作为审查与验收证据。
- 业务域 RPC 函数仅传递 JSON 字符串，统一响应可解析为 `code`、`status`、`message`、`data`。
- 不创建真实网络通信、数据库迁移、业务仓库迁移或 Git 历史写入。
