# `6-review` 检查流水线

## 目的

本文件是 `6-review` 的**步骤口径**：每一步查什么、判什么、留下什么证据。步骤本身不手写，由 `scripts/static_owner_router.py` 的 `route_review_pipeline()` 从**已加载的来源映射**推导，因此"检查哪些 Owner"永远与 `references/static-owner-source-map.json` 保持一致，不需要人工同步。

- 步骤来源（数据）：`references/static-owner-source-map.json`（Owner → 规则来源文件）。
- 步骤顺序（方法）：`scripts/static_owner_router.py` 的 `REVIEW_STEPS` 九步表。
- 步骤触发（范围）：`route_owners(changed_files, signals)` 先算出本轮相关 Owner，流水线只保留命中的步骤与其命中的 Owner。
- 收口格式（记录）：`references/style-regression-contract.md`。

## 运行方式

```bash
python code-style-consistency-rules/scripts/static_owner_router.py \
  --changed src/service/user.go --changed src/components/UserForm.vue \
  --signal computed --root .
```

- `--changed` 可重复或逗号分隔；`--signal` 传上游**已确认**的语义信号；`--json` 输出结构化步骤。
- 来源映射校验失败时退出码为 `2`，并打印具体违例项；此时不得继续 `6-review`。
- 输出即 `6-review` 记录里"检查步骤"段落的正文，逐步检查后再逐项写证据。

## 九步口径

### STYLE-01

**静态格式与编码一致性**（覆盖维度2、维度5）

- 规则 Owner：`code-style-consistency-rules`、`windows-encoding-rules`
- 检查项：UTF-8 无 BOM、LF 换行、无尾随空白；Windows 脚本（`.ps1` / `.bat` / `.cmd`）与 `.gitattributes` / `.editorconfig` 的编码与换行口径；是否引入项目未使用的格式化风格。
- 判定：编码错误、BOM、尾随空白、CRLF 漂移、格式跳变 → `FIX_REQUIRED`。
- 证据：`STYLE-01：<文件> → <现象或行号> → <结论>`

### STYLE-02

**命名与符号引用一致**（覆盖维度3、维度4）

- 规则 Owner：`naming-rules`
- 检查项：新增符号命名是否与同层既有符号、领域术语一致；导入别名、包别名、方法名是否与项目既有约定一致；版本化目录内的导入别名是否与版本目录名对齐（禁止业务语义别名）；是否出现同义不同名。
- 判定：命名跳变、语义别名导入版本化包、同义不同名 → `FIX_REQUIRED`。
- 证据：`STYLE-02：<文件:符号> → <结论>`

### STYLE-03

**注释分层与定义位置**（覆盖维度3）

- 规则 Owner：`comment-rules`
- 检查项：函数 / 方法注释是否为唯一完整层（整体说明 + `[参数]` + `[返回]` + 最近修改时间含一句话说明）；字段、行内、结构体字面量、补丁位点是否只写一句话作用说明，未平摊完整格式；局部变量是否函数开头集中声明、包级变量与常量是否顶部集中；注释语言与颗粒度是否服从 `comment-rules`。
- 判定：把函数注释格式平摊到字段或行内、局部变量就地散落声明、注释语言漂移 → `FIX_REQUIRED`。
- 证据：`STYLE-03：<文件:符号> → <结论>`

### STYLE-04

**函数签名与参数结构**（覆盖维度6）

- 规则 Owner：`code-quality-rules`
- 检查项：参数顺序是否为上下文 → 必填 → 可选；含可选或扩展字段时是否已收敛为结构体（`XxxParams` / `XxxOptions`）；同源参数是否达到 ≥3 仍未收敛；是否用多行参数列表代替收敛。
- 判定：可选字段平铺成参数、同源参数 ≥3 未收、以多行签名代替收敛 → `FIX_REQUIRED`。
- 证据：`STYLE-04：<文件:函数> → <结论>`

### STYLE-05

**结构与落点（结构体角色 / 目录位置 / 依赖方向）**（覆盖维度1、维度7）

- 规则 Owner：`package-structure-rules`、`micro-business-architecture-rules`
- 检查项：结构体是否按角色落在规定位置（持久化模型 / 领域实体 / 接口 req-resp / 公共传输 / 内部临时结构），内部临时结构是否误进 `entity/` 或 `common/`；新增目录与文件落点是否在 Catalog 允许集合内；依赖方向是否越界（业务域互相导入、公共层依赖业务层）。
- 判定：落点越界、同一模型多处重复定义、依赖方向反转 → `FIX_REQUIRED`。
- 证据：`STYLE-05：<路径> → <结论>`

### STYLE-06

**公共复用与工具落点（纯转换函数 / 工具索引）**（覆盖维度8、维度9）

- 规则 Owner：`common-util-rules`
- 检查项：新增工具函数是否先检索既有实现、有无同语义重复封装；纯转换函数（确定性 / 无副作用 / 无 IO / 无项目依赖）是否落在根 `utils/<pkg>/`，需要项目依赖的是否落在 `common/util/<函数>.<ext>`；导出工具函数是否已在项目内公共工具索引登记（`doc/1-架构/3-模块职责.md` 的 `## 公共工具索引` 小节）。
- 判定：同语义重复封装、纯转换函数落在业务层、导出工具函数未登记索引 → `FIX_REQUIRED`。
- 证据：`STYLE-06：<文件:函数> → <结论>`

### STYLE-07

**接口契约与数据访问**（覆盖维度1）

- 规则 Owner：`api-contract-rules`、`database-query-rules`、`database-schema-rules`、`error-handling-rules`、`logging-trace-rules`、`time-util-rules`
- 检查项（按本轮命中的 Owner 取子集）：端点语义、请求形状、响应形状与契约是否一致；参数校验与暴露安全；SQL 与访问层边界、事务与锁；错误分类与处理路径是否吞错；日志字段与 trace 传播；时间与时区转换口径。
- 判定：契约与实现不一致、错误被吞、日志缺可反查稳定标识、时区口径漂移 → `FIX_REQUIRED`。
- 证据：`STYLE-07：<文件:符号> → <结论>`

### STYLE-08

**语言与框架特异写法**（覆盖维度2）

- 规则 Owner：`golang-patterns`、`vue-best-practices`、`vue-router-best-practices`、`vercel-react-best-practices`、`frontend-component-rules`、`frontend-ui-visual-rules`
- 检查项（按本轮命中的 Owner 取子集）：Go 的常量与枚举写法、字符串归一化是否必要、包别名；Vue 的组件数据流、响应式与路由守卫；React 的依赖数组、缓存与渲染边界；组件边界与 props / emits 契约；视觉层的布局、色彩与可访问性。
- 判定：违反对应语言或框架的既定写法 → `FIX_REQUIRED`。
- 证据：`STYLE-08：<文件:符号> → <结论>`

### STYLE-09

**测试资产与编码前契约**（覆盖维度5）

- 规则 Owner：`test-program-rules`、`code-generation-style-rules`
- 检查项：测试程序、fixture 与启动脚本是否落在项目根 `test/` 并按被测源码目录镜像（`doc/5-tests/` 只保存说明与证据）；本轮是否真的产出了编码前风格契约，并按其完成一致性检查。
- 判定：测试资产落在 `doc/`、编码前契约缺失却宣称一致性 → `FIX_REQUIRED`。
- 证据：`STYLE-09：<路径> → <结论>`

## 加载契约（强制）

来源映射必须通过以下断言后才允许进入流水线，任一不通过即失败关闭：

- `version` 必须为 `2`；`owners` 必须是数组，禁止 v1 的「对象 key = Owner 名」形态（同一 Owner 的多个位点会被 JSON 静默覆盖）。
- 文本层声明数与解析数必须一致（Owner 数、来源分组数双重对账），同一 Owner 名不得重复出现。
- `OWNER_NAMES` 与来源映射的 Owner 集合必须**完全一致**，任一方向漂移都失败关闭。
- 每组 `source_paths` 必须非空，且只允许仓库相对路径、必须位于该 Owner 目录下、禁止绝对路径与路径穿越、文件必须真实存在；`source_globs` 不得含空 glob。
- 流水线不得引用未登记 Owner，也不得让任何已登记 Owner 失去检查落点（九步必须覆盖全部 `OWNER_NAMES`）。
- **覆盖率必须完整**：Owner 目录下的规则 Markdown 必须全部登记为来源，否则该规则存在却没有检查落点；枚举口径与豁免名单见 `references/static-owner-routing-contract.md` 的覆盖率断言小节。
- 加载失败只允许「先修映射再重跑」，不得降级为手写步骤或跳过检查。

## 与相邻规则的边界

- `6-review` 的入口、结果取值、记录模板与负向边界：`references/style-regression-contract.md`。
- 共享路由的导出接口与变更约束：`references/static-owner-routing-contract.md`。
- 各步检查项的规则正文：以该步「规则 Owner」对应 skill 为准，本文件只做步骤编排与判定口径，不复制规则内容。

## 负向边界

- 本流水线只判断写法、位置、格式与既有习惯；不判断业务正确性、不重新验需求覆盖、不替代真实功能测试、不作发布放行或最终验收结论。
- 步骤为空（无变更）时不得伪造步骤或证据。
- 缺真实测试证据时，`6-review` 记录为 `FIX_REQUIRED`，不得用流水线输出冒充测试通过。
