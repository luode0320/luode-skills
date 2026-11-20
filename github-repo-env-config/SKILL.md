---
name: github-repo-env-config
description: >-
  GitHub 仓库环境配置（仓库级 Actions Secret 四要素 + 部署流水线对齐）。
  当用户说"配置 github 仓库环境配置""配一下仓库的 Actions Secret""部署凭据/远端凭据配一下"
  "换服务器了，改一下 IP/端口""REMOTE_HOST / REMOTE_PORT / REMOTE_USER / REMOTE_PASSWORD",
  或工作流报错指向 secrets 未配置、ssh/scp 连接超时、端口不对时触发。
  固定契约：远端部署统一使用四个仓库级 Secret —— REMOTE_HOST（主机）、REMOTE_PORT（SSH 端口）、
  REMOTE_USER（登录用户）、REMOTE_PASSWORD（登录密码），并同步把所有 `.github/workflows`
  中的 host/port/username/password 改为 `secrets.*` 直连、清掉 workflow 内明文默认值。
  包含无 gh CLI 时的 libsodium sealed box 写入通道、机器校验脚本与端口连通性实测。
  发版链路（bump/发布/资产）见 `github-release-pipeline`，本 skill 只管"连得上、连得对"。

---

# GitHub 仓库环境配置（四要素 Secret + 工作流对齐）

> 适用前提：部署形态是「GitHub Actions → scp/ssh 到一台远端主机」。
> 本 skill 只回答两件事：**凭据放哪**（仓库级 Actions Secret）、**工作流怎么引用**（`secrets.*` 直连）。
> 不含项目特定事实（仓库名、主机地址、目录、容器名），全部用占位符。

## 0. 固定契约（不要自创字段名）

远端部署的四个连接要素，**名称固定、粒度固定、层级固定**：

| Secret 名称 | 含义 | 示例值 | 敏感度 | 缺失/空值后果 |
|---|---|---|---|---|
| `REMOTE_HOST` | 目标主机 IP 或域名 | `203.0.113.10` | 中（拓扑信息） | 连接失败，无回落 |
| `REMOTE_PORT` | 目标主机 SSH 端口 | `18998`（非 22 时必须显式配） | 低 | **静默回落 22** → 连接超时，最难排查 |
| `REMOTE_USER` | SSH 登录用户 | `root` | 低 | 鉴权失败（Permission denied） |
| `REMOTE_PASSWORD` | SSH 登录密码 | `***` | **高** | 鉴权失败 |

铁律：

1. **层级必须是仓库级（Repository secrets），不是环境级（Environment secrets）**。除非工作流显式声明了 `environment:`，环境级 secret 在无环境的 job 中不可见。
2. **四个都要配**，不要"敏感的两个放 secret、不敏感的三个写 env"。半吊子状态会让后来者以为还有明文分支可退。
3. **workflow 里不得出现任何明文默认值**（`REMOTE_PORT: 22`、`REMOTE_USER: root` 一律删除）。
4. 相邻凭据不混淆：`REGISTRY_USERNAME` / `REGISTRY_PASSWORD`（镜像仓库）是另一组，不在本契约内；`passphrase`（私钥口令）与 `password`（登录密码）是两个不同的 action 入参。

## 1. 识别口径（触发即执行，不必追问）

命中任一即按本 skill 全流程走：

- 用户给出主机/端口/账号/密码中的任意组合，且语境是"部署到服务器"。
- 用户说"配置一下 github 仓库的环境 / Actions Secret / 部署凭据"（**不需要点名四个字段，默认就是这四个**）。
- 工作流日志出现 `ssh: connect to host ... port 22: Connection timed out`、`Permission denied`、`dial tcp ... i/o timeout`，且流水线依赖 `secrets.REMOTE_*`。
- 服务器换了 IP/端口，需要同步流水线。

仅在下列情况才需要向用户确认：给不出仓库（无法从 `git remote -v` 解析 owner/repo）、或同一账号下多个仓库都可能命中而用户未指明。

## 2. 执行流程（顺序不可颠倒）

### Step 1 定位仓库与层级

```bash
git remote -v                 # 取 owner/repo
git rev-parse --abbrev-ref HEAD
```

同时确认是否存在环境级配置（决定 secret 放哪一层）：

```bash
curl -s -H "Authorization: Bearer $TOKEN" \
  "https://api.github.com/repos/<owner>/<repo>/environments"
```
`total_count: 0` → 全部放仓库级。若工作流 job 里写了 `environment: xxx`，则该 job **优先** 读环境级 secret，需在环境层也配一份或改为仓库级引用。

### Step 2 盘点现状（值不可读，只能看元数据）

```bash
curl -s -H "Authorization: Bearer $TOKEN" -H "Accept: application/vnd.github+json" \
  "https://api.github.com/repos/<owner>/<repo>/actions/secrets"
```

输出 `name` + `updated_at`。判断要点：

- **GitHub 不允许读回 secret 值**，所以"是否已配"只能靠 `name` 是否存在、"是否刚更新"只能靠 `updated_at` 是否刷新到当前时间。**不要声称已验证值正确**。
- `updated_at` 是很久以前的时间戳，说明该 secret 是历史遗留，换主机/换密码后很可能已失效——必须在收口时显式提示用户。

### Step 3 写入 Secret

**通道 A：有 `gh` CLI（首选，最省事）**

```bash
gh secret set REMOTE_HOST --repo <owner>/<repo> --body "<host>"
gh secret set REMOTE_PORT --repo <owner>/<repo> --body "<port>"
gh secret set REMOTE_USER --repo <owner>/<repo> --body "<user>"
gh secret set REMOTE_PASSWORD --repo <owner>/<repo> --body "<password>"
```

**通道 B：无 `gh`（本机默认无），用 libsodium sealed box**

用本 skill 自带脚本，参数化、secret 值不走命令行历史：

```bash
python -m pip install pynacl --target "$TEMP/wb_pynacl" -q
PYTHONPATH="$TEMP/wb_pynacl" python <skill>/scripts/set_repo_secret.py \
  <owner>/<repo> REMOTE_HOST "<host>" --token-file "<pat 路径>"
```

一次配四个用批处理模式（值从 JSON 或 env 文件读，避免逐条手敲）：

```bash
PYTHONPATH="$TEMP/wb_pynacl" python <skill>/scripts/set_repo_secret.py \
  <owner>/<repo> --json-file ./repo-env.json --token-file "<pat 路径>"
```

写入成功判据：`GET /actions/secrets` 中该项 `updated_at` 已刷新为当前时间（秒级）。

### Step 4 对齐 `.github/workflows`

原则：**`steps.<id>.with` 里直连 `secrets.*`，不经 `env` 中转。**

```yaml
      - name: 上传产物
        uses: appleboy/scp-action@master
        with:
          host: ${{ secrets.REMOTE_HOST }}
          username: ${{ secrets.REMOTE_USER }}
          password: ${{ secrets.REMOTE_PASSWORD }}
          port: ${{ secrets.REMOTE_PORT }}
```

```diff
     env:
       PROJECT_SLUG: <slug>
-      # 留空时默认复用 ...
-      REMOTE_USER: root
-      REMOTE_PORT: 22
+      # 远端 host/port/user/password 四要素统一由仓库级 Actions Secret 提供，
+      # 仓库内不保留明文默认值：REMOTE_HOST / REMOTE_PORT / REMOTE_USER / REMOTE_PASSWORD。
```

为什么不用 `env` 中转：`jobs.<job_id>.env` 对 `secrets` 上下文的支持不如 `steps.*.with` 明确，`env: REMOTE_PORT: ${{ secrets.REMOTE_PORT }}` 属于灰色地带；直连零歧义，也少一层排障面。

**必须逐个引用点改完**，常见漏改位置：

| 位置 | 形态 |
|---|---|
| 上传/部署 action | `appleboy/scp-action`、`appleboy/ssh-action`、`rsync` action、`docker context` |
| 裸命令脚本 | `run:` 里的 `ssh -p $PORT`、`scp -P $PORT`（**ssh 是小写 `-p`，scp 是大写 `-P`**） |
| 复合 action | 自定义 `action.yml` 内的 `inputs.port` 默认值 |
| 文档 | README / 部署说明里粘贴过的主机与端口 |

同一文件多处替换用 `replace_all`，**一次一个 Edit 调用、串行执行**（同文件并行 Edit 会静默互相覆盖）。

### Step 5 机器校验（不可用口头说明替代）

```bash
python <skill>/scripts/validate_workflow_secrets.py .github/workflows \
  --required REMOTE_HOST,REMOTE_PORT,REMOTE_USER,REMOTE_PASSWORD
```

脚本做三件事：YAML 可解析；`job.env` 内无这四个明文键；每个含 `host:` 的步骤四项均为 `secrets.*` 表达式。任一失败即视为未完成。

### Step 6 实证连通性（区分"配置对"与"服务器通"）

配置正确 ≠ 服务可达。用 TCP + banner 实测，能提前把"端口写错"和"密码错"分开：

```python
import socket
for host, port in [("<host>", <port>), ("<host>", 22)]:
    s = socket.socket(); s.settimeout(6)
    try:
        s.connect((host, port))
        s.settimeout(3)
        print(host, port, "OK banner=", s.recv(64))
    except Exception as e:
        print(host, port, "FAIL", type(e).__name__, e)
    finally:
        s.close()
```

判读：返回 `SSH-2.0-OpenSSH_x.y` 才算端口确实指向 SSH 服务；22 端口能连上但无 banner，通常是防火墙静默丢包（DROP），正好反证非默认端口配置是必要的。

### Step 7 收口

- 说明**工作流改动是否已提交**。禁止自动 commit/push，需用户逐次明确授权。
- 明确告知：**secret 值不可回读**，本次验证依据是 `updated_at` 刷新 + 端口连通性，**未覆盖密码正确性**。
- 追加项目工作记忆：本次四要素取值来源、端口实测结论、遗留的旧 `updated_at` 项。

## 3. 陷阱速查表

| 现象 | 根因 | 对策 |
|---|---|---|
| `AttributeError: module 'nacl' has no attribute 'public'` | 只 `import nacl.bindings`，子模块未加载 | 脚本内**显式** `import nacl.public` |
| `ModuleNotFoundError: nacl` | 系统无 pynacl，且不愿污染全局 | `pip install pynacl --target <tmp>` + `PYTHONPATH=<tmp>` |
| secret 更新成功但流水线仍连 22 | `REMOTE_PORT` 为空/未建，action 回落默认值 | 建齐四个；**该 secret 只能改值不能删** |
| `PUT` 返回 404 | 仓库名/owner 拼错，或 PAT 无该仓库权限 | 先 `git remote -v` 校准；Classic PAT 需 `repo` scope |
| 环境级 secret 不生效 | job 未声明 `environment:` | 改配仓库级，或补 `environment:` 声明 |
| 改完仍连旧主机 | 只改了 env、漏改某些 action 的 `host:` | 跑 Step 5 校验脚本，按引用点清单逐个核 |
| 批量替换后部分引用未生效 | 同文件并行 Edit 互相覆盖 | 一次一个 Edit，`replace_all` 处理同类行，逐条验证 |
| 凭据错 vs 网络错分不清 | 两者都表现为超时/拒绝 | 先 banner 实测端口，再单独验密码 |
| 401/403 或 TLS `UNEXPECTED_EOF` 抓 API | curl/urllib 通道不稳定、代理误报 | 换 PowerShell `Invoke-RestMethod` + `SecurityProtocol=3072`（见 `github-release-pipeline`） |

## 4. 幂等与重复执行

- Secret 写入用 `PUT` 覆盖，天然幂等；重复执行只是刷新 `updated_at`，无副作用。
- 工作流对齐是幂等文本替换；重复执行应产生零 diff，可据此判断上次是否真的落盘。
- 换项目复用时**只需换 `<owner>/<repo>` 与四个取值**，脚本与校验流程不变。

## 5. 边界（不做的事）

- 不负责发版链（bump / dispatch / 资产下载 / 二进制验证）→ `github-release-pipeline`。
- 不负责 commit/push 规范与冲突处理 → `git-collaboration-rules`。
- 不保管密码明文：不在回复、日志、commit message 中回显 `REMOTE_PASSWORD`；不在仓库内落 `.env`。
- 建议但不当场执行：root 直连改为专用部署用户 + 私钥（`REMOTE_PRIVATE_KEY`），届时需同步把 `password:` 换成 `key:`。

## 6. 变更记录

- 2026-11-07：从 `web-start-vue` 实际配置中抽象（REMOTE_HOST/REMOTE_PORT/REMOTE_USER 迁入仓库级 Secret，端口 18998），补齐无 gh CLI 的 sealed box 通道、机器校验脚本与端口 banner 实测方法。
