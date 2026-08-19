# 环境与 Mock — environment / variables / mock / database-connection

> 本模块覆盖环境配置、变量管理、Mock 规则及数据库连接。已从 SKILL.md 继承：写入标准流程、分支参数规则。

## 何时加载

- 创建/更新/查询/删除环境
- 管理环境变量、全局变量
- 配置 Mock 规则/期望/智能 Mock
- 配置数据库连接

## 命令入口

```bash
apifox environment --help
apifox variables --help
apifox mock --help
apifox database-connection --help
```

具体参数以当前 CLI help 为准。

## 环境管理

```bash
# 列出项目环境
apifox environment list --project <projectId>

# 获取环境详情
apifox environment get <environmentId> --project <projectId>
```

- 创建/更新前先通过 `cli-schema get` 获取结构定义
- 敏感变量（token、密码等）不要在回复中展示

## Mock 配置

Mock 是独立于环境的功能，需要在接口层级配置 Mock 规则或期望。

- 先确认接口已有响应定义，再配置 Mock
- Mock 未配置可能导致接口测试返回 404 或异常响应
- 区分：接口测试失败 ≠ 接口定义未保存，也可能是 Mock/环境未配置

## 运行环境建议

- 运行测试时建议显式带 `--environment`
- CI 场景 token 通过 secret 注入，不要写入仓库

## 被测服务本地启动（强制）

接口级测试（功能验证/回归/Bug 验证/上线门禁的接口部分）默认以本地服务为被测对象：

- 测试前必须先确认被测服务已在本地启动且端口可访问（`curl http://localhost:<port>/health` 或等价可达检查）
- apifox environment 的 baseUrl 指向本地服务：`http://localhost:<port>`；环境名约定使用 `local` / `localhost`
- 禁止新建指向 `test` / `prod` / `staging` / `pre` / `release` 的 environment，禁止把 baseUrl 指向非 local 服务（判定标准是配置归属，与 `test-strategy-rules` 的本地环境红线一致）
- 运行测试显式带 `--environment <localhost环境Id>`，避免默认环境漂移
- 数据构造仍从 local 数据库取真实样本（来源优先级见 `modules/test-data-and-judgement.md`），不得连非 local 服务取数

## 不可违反规则

1. 敏感变量不要出现在最终回复中
2. 运行测试建议显式指定 `--environment`，避免默认环境变化
3. 不要在未确认环境的情况下执行有副作用的操作
4. 接口级测试 environment 只允许指向 local（localhost），禁止指向非 local 服务
