# 前端项目位置规则

前端独立项目根的业务资产必须保留在自身 `config/`、`data/`、`src/`、`scripts/`、`deploy/`、`doc/` 中，不能提升至同仓工作区根。

- `src/app/` 负责启动和全局装配；`src/modules/<domain>/` 负责业务域；跨域复用的组件进入 `src/components/`。
- `src/api/` 是项目级传输基建，域内 API 调用进入 `src/modules/<domain>/api/`。
- `src/common/` 放项目级结构；业务域模型进入 `src/modules/<domain>/model/`。
- React 仅创建 `hooks/`，Vue 仅创建 `composables/`；`pages/` 与 `views/` 只选一套。
- `public/` 放原样公开文件，`src/assets/` 放参与打包的资源，两者不得重复同一资产。
