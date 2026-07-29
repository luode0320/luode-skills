# 跨语言结构总则

代码位置以 `placement-catalog.yaml` 为唯一机器事实源；三类完整目录树见 `project-layout-v2.md`。同仓根只拥有工作区资产，独立后端与独立前端分别拥有自己的业务目录。

后端根级 `database/`、`utils/`、`common/`、`global/`、`crontask/`、`async/`、`middleware/` 不进入语言源码根。其中根 `utils/` 只包含可独立复制的工具包子目录，不得直接存放文件，也不得依赖项目其他包。源码根只保留 `router/`、`controller/`、`util/`、`business/<domain>/`；源码根 `util/` 直接存放可依赖项目其他包的高关联工具函数，禁止建立子目录。业务域 `business/<domain>/util/` 仍是域私有辅助能力；跨域通信仅允许目标域 `business/<domain>/rpc/` 的公开函数，入参与返回值均为 JSON 字符串。禁止后端项目根 `util/` 工具包目录、根 `contract/`、根 `protocol/`、项目级 `schema/` 和 `infrastructure/`。

目录新增、迁移或职责调整后，必须更新项目真实目录树 `doc/1-架构/2-目录树.md`。
