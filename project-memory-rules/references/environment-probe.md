# 项目环境探测清单（吸收自 java-story-develop）

> 归属 owner：`project-memory-rules`。本文件是项目环境探测的标准清单与记忆固化格式，不产生独立自动触发入口。吸收来源：`java-story-develop__skillhub`（LobeHub 安装包）。吸收原则：只吸收「环境探测维度 + 探测方式 + 记忆固化格式」的语言无关精华，本地已有的「记忆优先读取、冲突检测、四件套职责边界」保留本地且不与本文件冲突。

## 适用场景

- 新项目 / 新会话首轮，`PROJECT_CURRENT.md`、`PROJECT_MEMORY.md` 未命中项目环境信息时执行。
- 用户明确否认记忆中的环境信息（版本变更、框架替换、前端新增）时重新执行完整探测。
- 探测结果按本节格式固化进 `PROJECT_MEMORY.md`，后续会话优先复用记忆、不重复探测。

## 探测维度与方式（Go / Java / 前端通用）

只读取真实配置文件，禁止凭印象或假设填充；探测结果必须能回指到具体文件与字段。

| 维度 | Go 项目 | Java 项目 | 前端项目 |
|------|---------|-----------|----------|
| 语言运行时版本 | `go.mod` 首行 `go 1.x` | `pom.xml` 的 `<java.version>` 或 `maven-compiler-plugin` source/target | `package.json` 的 `engines.node`（如有） |
| Web 框架 | `go.mod` 中 gin / echo / fiber / chi | `pom.xml` 的 `spring-boot-starter-parent`（Boot 版本）、`spring-cloud-*` | Vue 3 / React / Angular（`package.json` dependencies） |
| ORM / 数据访问 | `go.mod` 中 gorm / sqlx / ent / xorm | `mybatis-spring-boot-*` / `mybatis-plus-*` / `spring-boot-starter-data-jpa` | 请求层 axios / fetch / TanStack Query |
| 业务基础框架 | 项目自有 starter / 基础库 | continew-starter / jeecg-boot / 自定义 starter | 组件库（Arco / Element / Ant Design）+ 状态库（Pinia / Redux） |
| 工具库 | 项目自有 util / 常用依赖 | Lombok / Hutool / Guava / 项目自有 util | lodash / dayjs / 项目自有 utils |
| 数据库类型 | 配置文件（.yaml / .env / docker-compose）中 driver | `pom.xml` + 配置文件的 mysql / postgresql / oracle | — |
| 构建工具 | Makefile / go build / taskfile | Maven / Gradle | vite / webpack / next build |
| 测试框架 | testing / testify / ginkgo | JUnit4 / JUnit5 / Spock + Mockito | Vitest / Jest / Playwright |

## 探测命令示例

```bash
# Go 项目
head -5 go.mod                                    # go 版本 + module 名
grep -E 'gin|echo|fiber|gorm|sqlx' go.mod         # Web 框架 / ORM

# Java 项目
grep -A2 '<parent>' pom.xml | head -5             # Spring Boot 版本
grep '<java.version>' pom.xml                     # JDK 版本
grep -E 'mybatis|mybatis-plus|jpa' pom.xml        # ORM 框架

# 前端项目
grep -E '"vue"|"react"|"@angular' package.json    # 框架
grep -E '"vite"|"webpack"|"next"' package.json    # 构建工具
```

## 记忆固化格式

探测完成后写入 `PROJECT_MEMORY.md` 机器索引区（按 `memory-index-schema.md` 的实体规则），并同步人类阅读区一行摘要：

```
项目名称：{projectName}
技术栈：Go {version} + {webFramework} + {orm} + {businessFramework}
工具库：{toolkit}
数据库：{databaseType}
前端技术栈：{frontendStack}（如有）
构建工具：{buildTool}
测试框架：{testFramework}
项目路径：{projectRoot}
最后探测：{date}
```

- 环境信息属于稳定长期事实，写入 `PROJECT_MEMORY.md`；不写入 `PROJECT_CURRENT.md`（那是当前状态，不是稳定环境）。
- 后续会话命中环境记忆时，仅向用户确认「环境信息是否仍然准确」，用户否认才重新探测。
- 探测中发现的环境变更（如升级框架版本）按 `memory-conflict-and-staleness.md` 更新旧实体，不叠加新实体。

## 红线（与本地规则一致）

- 只允许使用 `local` 配置连接数据库 / 服务确认结构，禁止回退 test / staging / prod。
- 禁止把探测失败当作「无此技术栈」写入记忆；探测不到时应标记「未探测到，待确认」而不是默认值。
- 探测结果不是执行授权：连接生产、写入数据、执行迁移等仍按对应 skill 的授权边界处理。
