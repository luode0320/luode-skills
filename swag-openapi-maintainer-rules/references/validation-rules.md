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
9. `$ref` 无并列字段。
10. `git diff --check` 通过。

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
