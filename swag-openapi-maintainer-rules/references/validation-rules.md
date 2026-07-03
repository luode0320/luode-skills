# 校验规则

本文件定义 `swag-openapi-maintainer-rules` 收口前必须完成的校验。

## 必跑校验

1. YAML 可解析。
2. OpenAPI / Swagger 版本合法。
3. `swag/openapi.yaml` 存在。
4. `.swag-manifest.yaml` 存在。
5. 总 YAML operation 数 = manifest 当前接口数。
6. 单接口 YAML 数 = manifest 当前接口数。
7. 每个 manifest 文件存在。
8. 每个单接口 YAML 是完整 OpenAPI / Swagger 文档。
9. 单接口 YAML 的 operation 默认不含 `tags`，避免导入 Apifox 时自动新增父目录。
10. 单接口文件名符合“路径名 + 中文简要说明”规则，且中文简介后缀已去掉 `1.`、`11.`、`（1）` 等数字前缀与无业务意义特殊符号；若回退纯路径文件名，manifest 必须显式标记 `summary_source: unresolved`。
11. manifest 中的 `file`、`summary`、`summary_source` 与实际单接口文件一致。
12. 头部、请求参数、响应字段中文说明完整。
13. `$ref` 无并列字段。
14. `git diff --check` 通过。

## 推荐命令

```bash
python swag-openapi-maintainer-rules/scripts/validate_openapi_yaml.py --swag-dir swag
git diff --check
```

Windows 下如果必须使用 PowerShell，应先设置 UTF-8：

```powershell
[Console]::InputEncoding=[System.Text.UTF8Encoding]::new($false)
[Console]::OutputEncoding=[System.Text.UTF8Encoding]::new($false)
$env:PYTHONUTF8='1'
python swag-openapi-maintainer-rules/scripts/validate_openapi_yaml.py --swag-dir swag
```

## 验收口径

- 生成逻辑可以由 agent 第一版手工读取代码并生成，但校验必须脚本化。
- 校验脚本不负责从业务代码扫描路由；路由扫描结果以 `.swag-manifest.yaml` 为校验基准。
- 如果 manifest 与当前扫描接口数不一致，必须先重新生成 manifest 后再校验。
- 若单接口 YAML 带 `tags`、文件名不符合新规则、中文简介后缀仍带数字前缀 / 序号噪音、manifest 映射缺 `summary_source`，或字段中文说明缺失，视为 skill 未通过，不得以“可导入”代替“规则合格”。
