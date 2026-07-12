# project-agents-bootstrap 当前渠道图像配置测试

## 测试目的

验证 `project-agents-bootstrap` 与 `imagegen` 使用 Codex 当前 `model_provider` 对应的 OpenAI-compatible 配置，且不再注入固定的 OpenAI 默认 URL。测试只使用临时 local fixture，不读取 test、staging 或 prod 配置，不执行外部图像 API 请求。

## 测试对象与真实资产

- 生产解析器：`imagegen/scripts/bootstrap_imagegen_env.py`
- 生产 CLI 桥接：`imagegen/scripts/image_gen.py`
- 生产模板：`project-agents-bootstrap/SKILL.md`、`project-agents-bootstrap/scripts/bootstrap_agents.sh`
- 真实测试程序：`doc/5-tests/2026-07-12_171805/project-agents-image-channel/imagegen/test_bootstrap_imagegen_env.py`

## 路径与命名结论

- 时间戳根目录 `2026-07-12_171805` 由当前运行时生成，符合 `yyyy-MM-DD_HHmmss`。
- 中文说明目录 `project-agents-image-channel` 只承载本 README。
- Python 测试资产放在 ASCII 的 `imagegen/` 真实代码路径镜像目录，避免中文目录进入可执行路径。
- 未复用历史时间戳目录；本轮为当前需求独立测试资产迁移，旧的业务代码侧测试目录不再保留测试文件。

## 执行方式

```powershell
python -X utf8 -m unittest discover -s doc/5-tests/2026-07-12_171805/project-agents-image-channel -p "test_*.py" -v
```

执行前置条件：本机 Python 3.11+，仓库处于 local 测试上下文；无需真实 API key、网络访问或第三方依赖。

## 覆盖范围

- custom active provider 的 `base_url` 解析。
- 旧顶层 `base_url` 的兼容读取。
- `codex-auth:active_provider_api_key` 与 `codex-config:active_provider_base_url` 项目 token。
- `IMAGEGEN_*` 优先于旧 `OPENAI_*` 环境变量。
- 缺失 provider 时不注入 `https://api.openai.com/v1`。
- 生成模板使用 provider-neutral token 与 `gpt-image-2`。

## 验证结论

- 真实测试资产迁移后执行结果：7/7 PASS。
- 测试输出不包含 fixture key 原值作为诊断信息。
- 未覆盖非 OpenAI-compatible 协议的真实请求；该场景按实现契约返回 unavailable，不在本地测试中发起网络调用。
