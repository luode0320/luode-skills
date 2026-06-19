# 命令模板

## 通用模板

```powershell
wsl.exe -e bash -lc "cd '<WSL_PROJECT_PATH>' && <COMMAND>"
```

## 常见命令

### Node / pnpm / npm / yarn

```powershell
wsl.exe -e bash -lc "cd '<WSL_PROJECT_PATH>' && pnpm install"
wsl.exe -e bash -lc "cd '<WSL_PROJECT_PATH>' && pnpm test"
wsl.exe -e bash -lc "cd '<WSL_PROJECT_PATH>' && pnpm dev"
wsl.exe -e bash -lc "cd '<WSL_PROJECT_PATH>' && npm test"
wsl.exe -e bash -lc "cd '<WSL_PROJECT_PATH>' && yarn test"
```

### Python

```powershell
wsl.exe -e bash -lc "cd '<WSL_PROJECT_PATH>' && pytest"
wsl.exe -e bash -lc "cd '<WSL_PROJECT_PATH>' && python -m pytest"
wsl.exe -e bash -lc "cd '<WSL_PROJECT_PATH>' && python manage.py runserver"
```

### Go

```powershell
wsl.exe -e bash -lc "cd '<WSL_PROJECT_PATH>' && go test ./..."
wsl.exe -e bash -lc "cd '<WSL_PROJECT_PATH>' && go run ./cmd/server"
```

### Rust

```powershell
wsl.exe -e bash -lc "cd '<WSL_PROJECT_PATH>' && cargo test"
wsl.exe -e bash -lc "cd '<WSL_PROJECT_PATH>' && cargo run"
```

### Java / Gradle / Maven

```powershell
wsl.exe -e bash -lc "cd '<WSL_PROJECT_PATH>' && ./gradlew test"
wsl.exe -e bash -lc "cd '<WSL_PROJECT_PATH>' && ./gradlew bootRun"
wsl.exe -e bash -lc "cd '<WSL_PROJECT_PATH>' && mvn test"
```

## 需要登录 shell 的模板

当命令依赖 `nvm`、`sdkman`、`pyenv`、`asdf` 或 `.bashrc` / `.profile` 初始化时：

```powershell
wsl.exe -e bash -lic "cd '<WSL_PROJECT_PATH>' && <COMMAND>"
```

仅在确认需要时使用，避免把所有命令都升级为更重的交互式 shell。
