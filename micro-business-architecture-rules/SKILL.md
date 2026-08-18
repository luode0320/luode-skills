---
name: micro-business-architecture-rules
description: 当新建项目 / 新会话首轮检测到新或空仓库（缺业务代码骨架），或用户提出「微业务 / 伪微服务 / 按业务分目录包 / 业务隔离 / 业务互不关联 / 业务版本化 / 新业务开新包 / 一个项目一个服务的伪微服务」等诉求，或项目已存在微业务标记时自动触发。负责守护单项目单服务中的业务垂直切分、版本化目录隔离和跨业务导入隔离：业务域直连源码根，业务相关逻辑通过 `router/<v?>/`、`controller/<v?>/`、`entity/<v?>/`、`service/<v?>/` 四类版本化目录完全隔离（包名用 `v?router`、`v?controller`、`v?entity`、`v?service` 别名引用），业务域之间禁止直接导入对方任何目录；提供幂等脚手架、标记与确定性校验，并以 CodeGraph 导入节点作为审查证据。具体目录、引用边界由 `package-structure-rules` 唯一拥有；不要用它代替需求分析、实施规划、分层落点或实际编码。
---

# 微业务架构规则

## 目标

- 把微业务（伪微服务）的业务域隔离固化为可自动命中、可校验、可交接的规则。
- 让每个业务域自包含，调用方不能直接读取或引用其他业务域的私有代码、实体或状态。
- 用版本目录隔离业务演进，多版本并存对外，不引入网络 RPC、HTTP、消息队列或独立部署。

## 核心理念

- 微业务仍是一个项目、一个服务进程；切分目标是降低业务上下文和依赖耦合，不是创建真实微服务。
- 每个业务域直连源码根 `<source-root>/<domain>/`；业务相关逻辑通过 `router/<v?>/`、`controller/<v?>/`、`entity/<v?>/`、`service/<v?>/` 四类版本化目录完全隔离，其余为跨版本通用业务逻辑。
- 业务域之间禁止直接导入对方任何目录；跨域共享结构仅走根 `common/` 与 `global/` 非业务运行引用。

## 自动触发信号

- 用户提出微业务、伪微服务、业务隔离、业务版本化、按业务拆目录包或业务互不关联。
- 新会话首轮检测到新或空业务项目，或项目已有微业务标记。
- 用户要求新增业务域、创建版本目录、校验业务隔离或审查跨业务导入。

## 进入后先做什么

1. 明确当前对象是业务项目，不是 `luode-skills` 规则仓库本身。
2. 新会话首轮先联动 `project-rule-file-bootstrap-rules`，再依 `trigger-and-marker.md` 判断引导或守护模式。
3. 需要目录或引用边界时先查询 `package-structure-rules`；本 Skill 不复制其目录 Owner 职责。
4. 需要隔离检查时读取 `isolation-and-communication.md`，使用 `micro_business.py check` 做确定性门禁，并在审查时用 CodeGraph 导入节点复核证据。

## 核心原则

1. **业务垂直切分**：每个业务域是自包含目录包，私有实现只在本域中演进。
2. **域间禁止直连**：业务域 A 不得导入业务域 B 的任何目录（无 `rpc/` 例外）；跨域共享结构仅走根 `common/` 与 `global/` 非业务运行引用。
3. **版本化目录隔离**：业务相关逻辑通过 `router/<v?>/`、`controller/<v?>/`、`entity/<v?>/`、`service/<v?>/` 四类目录各自内嵌版本隔离，`v1` 起递增；版本命名 `v[0-9]+`，包名用 `v?router`、`v?controller`、`v?entity`、`v?service` 别名引用。
4. **版本并存对外**：域级单文件 `init.<ext>` 全量注册本域所有版本路由，`/v1`、`/v2` 前缀区分；旧版本不因新版本诞生而下线。
5. **允许的公共例外**：根 `common/request`、`response`、`constant`、`error`、`validation` 和仅含非业务运行引用的 `global/` 可直接使用；`global/` 禁止承载业务实体、业务状态、业务列表或可变业务缓存。

## 与相邻 Skill 的边界

- `package-structure-rules`：唯一拥有 `<source-root>/<domain>/` 目录树（含 `router/<v?>/`、`controller/<v?>/`、`entity/<v?>/`、`service/<v?>/` 版本化目录）、目录查询、初始化、渲染和严格检查规则。
- `codegraph-analysis-rules`：拥有导入节点、调用链和影响面检索；本 Skill 只把其结果作为跨域隔离审查证据。
- `code-readability-rules`：拥有一般抽象取舍；本规则的版本目录边界是已冻结的跨域隔离边界，不要求额外接口、注册或依赖注入层。
- `artifact-storage-rules`：拥有研发文档产物路径；本 Skill 不另建测试或文档目录。
- `architecture-doc-rules`：业务域与版本目录关系可按需摘要回写项目架构文档。

## 执行入口

- 触发、标记和守护：`references/trigger-and-marker.md`。
- 业务域目录与按需脚手架：`references/directory-layout.md`、`scripts/micro_business.py scaffold <domain>`。
- 隔离与 CodeGraph 审查：`references/isolation-and-communication.md`、`scripts/micro_business.py check`。
- 业务域 README 与全局索引：`references/md-convention.md`。

## 通过标准

- `micro_business.py check` 稳定拒绝任何跨业务域直接 import。
- CodeGraph 可定位每一种跨域违规导入，作为真实测试与 `6-review` 的追溯证据。
- 业务域通过版本化目录（`router/<v?>/`、`controller/<v?>/`、`entity/<v?>/`、`service/<v?>/`）隔离业务演进，`init.<ext>` 全量注册版本路由。
- 不创建真实网络通信、数据库迁移、业务仓库迁移或 Git 历史写入。
