# 项目当前状态

## 当前任务

- 目标：为 `swag-openapi-maintainer-rules` 增加上游/第三方出站接口文档能力。
- 范围：B1 上游子目录契约、5 个 references 扩展、新增第三方发现规则、递归校验脚本、7 用例离线 fixture、字典刷新与项目记忆同步。
- 非范围：不改 `api-swagger-rules` / `api-request-rules` / `编码skill.md`，不联网抓取上游文档，不到真实业务项目生成第三方 swag，不接入自有上线测试基线，不推送远端。
- 状态：任务 1-4 已完成并真实验证，已完成本地提交，未推送远端。

## 已完成

- 契约冻结为 B1：每个 `swag/<vendor-slug>/` 独立维护 `openapi.yaml`、`.swag-manifest.yaml` 与单接口 YAML。
- 上游 manifest 固定使用 `source_type: upstream`、`upstream`、`base_url`、`coverage: partial`、`source_client_file`、`source_symbols` 与 `discovery_confidence`。
- 根目录自有接口与上游目录校验隔离；根 `openapi.yaml` 不聚合上游；manifest 文件字段必须是裸文件名。
- `validate_openapi_yaml.py` 已支持 `validate_swag_dir(scope)` 与 `validate_swag_tree`，陌生目录按 YAML 存在性产生 `tree_warnings`。
- 离线测试资产已落在 `doc/5-tests/2026-07-14_121425/`，中文说明目录只放 README，Python 资产位于 ASCII 镜像目录。
- 7/7 离线用例通过，覆盖正例、中文说明缺失、manifest 映射、路径逃逸、source_type 缺失、单目录兼容和陌生目录 warning。
- 实现自审已落盘至 `doc/6-审查/2026-07-14_122718_需求-swag第三方接口文档能力升级_实现自审.md`，结论通过。
- 当前改动总审查已落盘至 `doc/6-审查/2026-07-14_124241_需求-swag第三方接口文档能力升级_当前改动总审查.md`，结论通过且无 P0/P1 阻断。

## 本轮收口

- `python skill-dictionary/generate_dictionary.py` 已成功刷新 `skill-dictionary/data.js` 与根 `字典.md`。
- `PROJECT_MEMORY.md` 已回写上游 swag 稳定契约、人类阅读区和机器索引区；机器索引 YAML 解析通过。
- `git diff --check`、Python 编译、离线 7 用例和审查文档均已完成；提交后工作树已清空。

## 阻断

- 当前无影响原始目标的环境阻断。
- 本次执行中曾出现两项已修正的测试 fixture/边界问题：缺中文说明用例误断言根 `valid`，以及陌生目录含普通 YAML 时脚本未发 warning；修正后 7/7 通过。

## 验证

- `$env:PYTHONUTF8='1'; python doc/5-tests/2026-07-14_121425/swag-openapi-maintainer-rules/scripts/validate_openapi_yaml_third_party_test.py`：7/7 通过。
- 测试主程序通过 CLI 真实入口校验退出码、stdout JSON、root/third_party scope、裸文件名错误和 `tree_warnings`。
- `validate_swag_dir(swag_dir)` 与无上游 fixture 的旧根级结果逐键一致。
- `git diff --check`：通过。
- `python skill-dictionary/generate_dictionary.py`：84 个已实现 skill，0 个缺失计划项；swag description 与新增 reference 已刷新。
- `PROJECT_MEMORY.md` 机器索引抽取与 YAML 解析：通过。
- CodeGraph：已安装，当前仓库索引状态 up to date；未执行写入型重建。

## 交接点

- 当前已完成任务 4；最大边界已达到计划定义的字典/记忆更新、门禁复核和本地提交收口。
- 不执行远端推送或业务项目真实 swag 生成。
