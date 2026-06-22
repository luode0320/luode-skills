# 命令模板

## 执行前：挂载检查三步流程

```powershell
# 第一步：检查 bind mount 是否就绪
wsl.exe -e bash -lc "mountpoint -q /home/luode/d/luode/ellipal_admin && echo 'mounted' || echo 'not_mounted'"

# 第二步（未挂载时）：执行 bind mount
# 需要 root 密码时，停止自动执行，通知用户手动完成
wsl.exe -e bash -lc "mkdir -p /home/luode/d/luode/ellipal_admin && sudo mount --bind /mnt/d/luode/ellipal_admin /home/luode/d/luode/ellipal_admin"

# 若需要持久化（写入 fstab）
wsl.exe -e bash -lc "grep -v '/mnt/d/luode/ellipal_admin' /etc/fstab | sudo tee /etc/fstab && echo '/mnt/d/luode/ellipal_admin    /home/luode/d/luode/ellipal_admin    none    bind    0 0' | sudo tee -a /etc/fstab && mkdir -p /home/luode/d/luode/ellipal_admin && sudo mount -a"

# 第三步：挂载成功后执行项目命令（使用用户工作路径）
```

---

## 通用模板

```powershell
wsl.exe -e bash -lc "cd '/home/luode/d/luode/<project>' && <COMMAND>"
```

---

## Go 项目（团队主要技术栈）

```powershell
# 构建
wsl.exe -e bash -lc "cd '/home/luode/d/luode/ellipal_admin' && go build ./..."

# 测试（全量）
wsl.exe -e bash -lc "cd '/home/luode/d/luode/ellipal_admin' && go test ./..."

# 测试（指定包）
wsl.exe -e bash -lc "cd '/home/luode/d/luode/ellipal_admin' && go test ./internal/..."

# 启动服务
wsl.exe -e bash -lc "cd '/home/luode/d/luode/ellipal_admin' && go run ./cmd/server"

# 启动 dlv 调试器（供 VSCode 远程 attach）
wsl.exe -e bash -lc "cd '/home/luode/d/luode/ellipal_admin' && dlv dap --listen=:2345 --headless=true --log"

# 格式化
wsl.exe -e bash -lc "cd '/home/luode/d/luode/ellipal_admin' && gofmt -w . && goimports -w ."

# 依赖下载
wsl.exe -e bash -lc "cd '/home/luode/d/luode/ellipal_admin' && go mod download"
```

---

## Node / pnpm / npm

```powershell
wsl.exe -e bash -lc "cd '/home/luode/d/luode/<project>' && pnpm install"
wsl.exe -e bash -lc "cd '/home/luode/d/luode/<project>' && pnpm test"
wsl.exe -e bash -lc "cd '/home/luode/d/luode/<project>' && pnpm dev"
```

---

## Python

```powershell
wsl.exe -e bash -lc "cd '/home/luode/d/luode/<project>' && pytest"
wsl.exe -e bash -lc "cd '/home/luode/d/luode/<project>' && python manage.py runserver"
```

---

## 需要登录 shell 的模板

当命令依赖 `nvm`、`asdf`、`pyenv` 或 `.bashrc` 初始化时使用 `-lic`：

```powershell
wsl.exe -e bash -lic "cd '/home/luode/d/luode/<project>' && <COMMAND>"
```

仅在确认需要时使用，默认优先 `-lc`。
