---
name: docker-direct-deploy
description: >-
  生成"镜像直传服务器部署"的 GitHub Actions workflow（.github/workflows/*.yml）。
  在 CI 里用 docker buildx 把镜像导出为 tar 包，经 scp 上传到远程服务器，再用
  docker load + docker run 启动，全程不经过 Docker Hub（不 login / 不 push / 不 pull）。
  当用户要新建或修改 .github/workflows 下的部署 workflow，或提到"镜像直传"、
  "直接上传镜像到服务器"、"不经过 Docker Hub"、"上传 tar 部署"、"服务器用上传的
  镜像启动"、"自动构建部署到服务器"、"部署 workflow" 时触发；也用于把现有
  push/pull 模式部署改造成直传模式。触发后读取本 skill 与 assets 模板快速生成。
---

# 镜像直传部署 Workflow 生成

## 何时使用（触发条件）

- 用户要新建 `.github/workflows/` 下的部署 workflow（例如"给 XX 加个自动部署""创建构建部署流水线"）。
- 用户提到：镜像直传、直接上传镜像到服务器、不经过 Docker Hub、docker load、上传 tar 部署、服务器用上传的镜像启动、把现有 push/pull 部署改成直传。
- 用户引用了现有直传 workflow（如 new-api 的 `.github/workflows/docker-deploy.yml` 或桌面参考文件）要求照此生成。

如果用户只是问原理 / 对比，不要求生成文件，则只说明、不落盘。

## 生成步骤

1. 收集参数（见"参数清单"）。用户没给全时：
   - 能从仓库上下文推断的（项目名、默认分支、Dockerfile 位置、端口等）直接推断；
   - 无法推断的关键参数（镜像命名空间、远程服务器凭据 Secrets、SQL_DSN 等）向用户确认，不要猜。
2. 读取模板 `assets/direct-deploy-workflow.template.yml`，按参数替换占位符（`<PROJECT_SLUG>`、`<BRANCH>`、`<IMAGE_NAMESPACE>` 等）。
3. 写到 `.github/workflows/<PROJECT_SLUG>-deploy.yml`（文件名可按用户指定）。
4. 按"校验"章节做本地校验；通过后交付。
5. 提示用户：真实部署需在 GitHub 仓库配置 Secrets `REMOTE_HOST`、`REMOTE_PASSWORD`（SSH 用户 / 端口非默认时还需 `REMOTE_USER` / `REMOTE_PORT`），然后推送触发分支或手动触发 workflow。

## 参数清单

| 参数 | 说明 | 默认 / 推断 |
| --- | --- | --- |
| `PROJECT_SLUG` | 项目名；同时作为容器名、tar 名、builder 名、远程子目录基准 | 仓库名，必填 |
| `IMAGE_NAMESPACE` | 镜像命名空间 / 用户名，仅用于给本地 load 的镜像打标签，不推送 | 必填 |
| `BRANCH` | 触发分支 | 仓库默认分支（main / master） |
| `REMOTE_BASE_DIR` | 远程放置 tar 与数据目录的根路径 | `/usr/local/src` |
| `TARGET_OS` / `TARGET_ARCH` | 目标平台 | `linux` / `amd64` |
| `REMOTE_USER` / `REMOTE_PORT` | SSH 用户与端口 | `root` / `22` |
| `DOCKER_RUN_ARGS` | `docker run` 参数块（`--network` / `--restart` / `-e` / `-v` / `--add-host` 等） | 必填，按项目实际 |
| `DOCKER_RUN_CMD` | 镜像名之后的容器命令（ENTRYPOINT 尾参），无则空串 `""` | 空 |
| 挂载目录 | 需预创建的 data / logs 等目录 | 与 `DOCKER_RUN_ARGS` 里的 `-v` 对应 |
| 部署 Secrets | 仓库 Secrets 名 | `REMOTE_HOST` / `REMOTE_PASSWORD` |

## 硬规则（为什么）

- **不得出现 `docker login` / `docker push` / `docker pull`，也不得引用 `REGISTRY_PASSWORD` 之类注册表密码**：直传模式镜像不经过任何镜像仓库，服务器直接用上传的 tar 启动，出现即视为错误。
- 用 `docker buildx build --output "type=docker,dest=<slug>.tar"` 导出单平台 tar，配合 `docker/setup-qemu-action@v3` 支持跨架构（`TARGET_OS` / `TARGET_ARCH`）。
- 名称全部由 `PROJECT_SLUG` 派生（`IMAGE` / `IMAGE_TAR` / `BUILDER_NAME` / `APP_DIR` / `CONTAINER`），避免相似前缀重复维护；派生结果写入 `GITHUB_ENV` 供后续步骤与 SSH 脚本复用。
- `DOCKER_RUN_ARGS` 用块标量（`|`）+ 行尾反斜杠续行，保留原始 `docker run` 写法；SSH 脚本内用引号 heredoc（`<<'EOF'`）原样注入，再 `eval "docker run ..."` 拼接。**块内禁止写 `#` 注释**（会原样传给 `docker run`）。
- `DOCKER_RUN_CMD` 承载镜像名之后的尾参（如 `--log-dir /app/logs`），追加在 `"${IMAGE}"` 之后；无尾参时设空串，展开后为空、不影响命令。
- 部署脚本顺序固定：校验 tar 存在 → `mkdir -p` 预建挂载目录 → 打印旧镜像 hash → `rm` 旧容器 / 旧镜像 → `docker load` → 打印新镜像 hash → `docker run` → `docker ps` 校验 → 清理 tar。每步都为了"能看出远端是否真的切到新内容"。
- 触发分支、`concurrency`、`permissions` 按项目需要保留；默认 `permissions: contents: read`。
- 多 Dockerfile 时在 buildx build 里保留 `-f Dockerfile`；单 Dockerfile 可去掉。

## 校验

生成后本地校验（不连接任何服务器）：

- YAML 可解析：`python -c "import yaml; yaml.safe_load(open(r'.github/workflows/<file>',encoding='utf-8')); print('YAML_OK')"`
- 无 Docker Hub 残留：`grep -nE "docker (login|push|pull)|REGISTRY_PASSWORD|docker\.io|index\.docker" .github/workflows/<file>` 必须无匹配（退出码 1）
- 关键结构齐全：模板中的 setup-qemu / buildx / scp-action / ssh-action / `docker load` / `docker run` / `docker ps` 均存在
- 校验通过才交付；失败则修正后重跑。

## 模板

- 完整模板：`assets/direct-deploy-workflow.template.yml`（含全部步骤与中文注释，直接替换占位符即可用）。
- 参考实例：new-api 的 `.github/workflows/docker-deploy.yml`（本模板的来源，可直接对照）。
