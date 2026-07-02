# swag-openapi 维护 skill 当前改动总审查

审查结论: 通过
审查范围: swag-openapi-maintainer-rules/SKILL.md；swag-openapi-maintainer-rules/references/；swag-openapi-maintainer-rules/scripts/validate_openapi_yaml.py；PROJECT_MEMORY.md；PROJECT_STYLE.md；skill-dictionary/data.js；字典.md
是否允许提交: 是
阻断问题: 无

## 审查摘要

- 本轮新增 `swag-openapi-maintainer-rules`，职责聚焦为维护项目全量 HTTP 接口 OpenAPI / Swagger YAML 资产。
- 新 skill 明确 `swag/` 为唯一正式输出目录，要求每个接口一个完整 YAML，同时维护 `swag/openapi.yaml` 和 `swag/.swag-manifest.yaml`。
- 新 skill 明确当前代码是唯一真相源，禁止凭历史记忆或旧文档补字段。
- 校验逻辑已脚本化，覆盖 YAML 解析、版本合法性、manifest 映射、operation 数、单接口文件数和 `$ref` sibling。

## 风险核对

- 未发现新 skill 与 `api-swagger-rules` 职责冲突：前者负责 `swag/` 资产生成和持续维护，后者负责 Swagger/OpenAPI 接入方案和调试入口规则。
- 未发现校验脚本写入业务项目文件；脚本只读校验 `--swag-dir`。
- 未发现对旧未提交改动的回退或覆盖。

## 验证证据

- `.system/skill-creator/scripts/quick_validate.py swag-openapi-maintainer-rules` 通过。
- `python -m py_compile swag-openapi-maintainer-rules/scripts/validate_openapi_yaml.py` 通过。
- 临时 `swag/` 目录 smoke test 通过，输出 `valid: true`。
- `skill-dictionary/generate_dictionary.py` 通过并刷新 `skill-dictionary/data.js` 与 `字典.md`。
- `git diff --check` 通过；仅有既有文件 CRLF 规范化提示。
