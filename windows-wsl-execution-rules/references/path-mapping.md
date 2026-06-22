# 路径映射规则

## 团队路径三层结构

```
Windows 源码路径        D:\luode\ellipal_admin
      ↓ WSL 自动挂载
WSL 自动挂载路径        /mnt/d/luode/ellipal_admin
      ↓ bind mount
WSL 用户工作路径        /home/luode/d/luode/ellipal_admin   ← 所有命令在此执行
```

| Windows 路径 | WSL 自动挂载路径 | WSL 用户工作路径（实际使用） |
|-------------|----------------|--------------------------|
| `D:\luode\ellipal_admin` | `/mnt/d/luode/ellipal_admin` | `/home/luode/d/luode/ellipal_admin` |
| `D:\luode\<project>` | `/mnt/d/luode/<project>` | `/home/luode/d/luode/<project>` |

**项目命令统一使用用户工作路径，不直接使用 `/mnt/d/...`。**

## 路径换算步骤

### 第一步：Windows → WSL 自动挂载路径
1. 取出盘符并转小写（`D` → `d`）
2. 去掉 `:`
3. 将 `\` 替换为 `/`
4. 前缀 `/mnt/`
- 示例：`D:\luode\project` → `/mnt/d/luode/project`

### 第二步：WSL 自动挂载路径 → 用户工作路径（bind mount）
- 格式：`/home/<user>/d/<path-after-drive>`
- 示例：`/mnt/d/luode/project` → `/home/luode/d/luode/project`

## 挂载检查（执行命令前必须先确认）

```powershell
# 检查 bind mount 是否就绪
wsl.exe -e bash -lc "mountpoint -q /home/luode/d/luode/ellipal_admin && echo 'mounted' || echo 'not_mounted'"
```

未挂载时，执行 bind mount（需要 root 密码时暂停通知用户）：

```powershell
# 临时挂载（重启 WSL 后失效）
wsl.exe -e bash -lc "mkdir -p /home/luode/d/luode/ellipal_admin && sudo mount --bind /mnt/d/luode/ellipal_admin /home/luode/d/luode/ellipal_admin"

# 持久化挂载（写入 fstab，重启后自动生效）
wsl.exe -e bash -lc "grep -v '/mnt/d/luode/ellipal_admin' /etc/fstab | sudo tee /etc/fstab && echo '/mnt/d/luode/ellipal_admin    /home/luode/d/luode/ellipal_admin    none    bind    0 0' | sudo tee -a /etc/fstab && mkdir -p /home/luode/d/luode/ellipal_admin && sudo mount -a"
```

## 注意事项

- 如果路径中包含空格，进入 `bash -lc` 时要整体放进单引号。
- 如果路径位于 `\\wsl$\<distro>\...`，不要再按三层结构转换，直接使用对应 Linux 原生路径。
- WSL 自动挂载路径 `/mnt/d` 在 WSL 启动时由系统自动创建，通常不需要手动挂载；bind mount 到用户目录才需要手动操作。
