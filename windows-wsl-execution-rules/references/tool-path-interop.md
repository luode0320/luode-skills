# WSL 内命令误用 Windows 版工具排查

## 根因

WSL 默认在 `/etc/wsl.conf` 的 `[interop]` 段开启 `appendWindowsPath=true`，会把 Windows 的 `%PATH%` 追加到 WSL 的 `$PATH` 末尾。如果 WSL 内没有原生安装某个命令行工具（比如没装 Linux 版 `ripgrep`），命令解析会 fallthrough 到 `/mnt/c/...` 挂载点下找到的 Windows 版 `.exe`。执行这种跨 interop 的 Windows 二进制时，可能因 DrvFs 挂载权限模式（`fmask`/`metadata` 选项）、文件只读标记或安全软件拦截等原因报 `permission denied`。

参考：[Advanced settings configuration in WSL](https://learn.microsoft.com/en-us/windows/wsl/wsl-config)、[File permissions for WSL](https://learn.microsoft.com/en-us/windows/wsl/file-permissions)

## 一次性自检

新会话第一次在某个 WSL 项目里执行命令时，可以顺手做一次自检，提前发现哪些常用工具还是 Windows 版，而不是等报错了再排查。这是一次性建议，不需要在每条命令前重复执行：

```bash
command -v rg fd fzf 2>/dev/null
```

按项目实际用到的工具调整这份清单。

## 识别方法

怀疑某次命令行为异常时，用 `command -v <tool>`（或 `type <tool>`）确认工具的实际路径：

```bash
command -v rg
# /usr/bin/rg 或 /usr/local/bin/rg → WSL 原生版，正常
# /mnt/c/... 下的路径          → 这是 Windows 版，可能是问题根源
```

## 常见症状

- 执行报 `permission denied`，且不像常规 Linux 权限问题（文件本身权限正常）
- 命令行为、参数格式、输出格式跟预期的 Linux 版不一致
- 路径分隔符、换行符出现异常

## 修复优先级

1. **优先在 WSL 内原生安装该工具**，装完后同名命令会自动优先命中原生版：
   ```bash
   sudo apt install ripgrep   # rg
   sudo apt install fd-find   # fd
   sudo apt install fzf       # fzf
   ```
2. 原生安装不可行或还没装好时，先用 WSL 自带的等价工具替代（`grep -r`、`find`、`python3` 等），不要在 Windows 版工具上反复重试。
3. 只有用户明确要求时，才考虑修改 `/etc/wsl.conf`（关闭 `appendWindowsPath`）或调整 `automount` 的 `fmask`/`dmask`。这会影响整个 WSL 发行版的所有项目和会话，不作为默认排查手段。

## 常见工具对照表

| 工具 | WSL 原生安装 |
|---|---|
| rg（ripgrep） | `sudo apt install ripgrep` |
| fd | `sudo apt install fd-find` |
| fzf | `sudo apt install fzf` |
