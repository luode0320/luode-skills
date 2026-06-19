# 团队推荐目录与工作流

## 目标

为“Windows 编辑、WSL 运行”的团队提供一套顺手但不强制的推荐流程。

## 推荐目录

推荐把项目真实文件放在 Windows 盘符目录，例如：

- `F:\code\project-a`
- `F:\code\project-b`

对应的 WSL 路径分别是：

- `/mnt/f/code/project-a`
- `/mnt/f/code/project-b`

## 推荐协作方式

- Windows 侧：
  - Codex 桌面端编辑真实文件
  - 资源管理器直接打开真实盘符路径
  - Windows 工具直接查看日志、图片、文档等产物
- WSL 侧：
  - 安装依赖
  - 启动项目
  - 跑测试
  - 跑构建
  - 运行开发脚本

## 推荐 VS Code 用法

二选一即可：

1. 直接打开 Windows 目录，例如 `F:\code\project-a`
2. 用 WSL Remote 打开 `/mnt/f/code/project-a`

两者都可行，但命令执行仍推荐落在 WSL 中。

## 推荐快捷挂载

如果团队希望在 WSL home 目录里有更好记的入口，可创建 bind mount：

### 映射整个 F 盘

```bash
mkdir -p /home/luode/work/f
sudo mount --bind /mnt/f /home/luode/work/f
```

### 映射 F:\\code

```bash
mkdir -p /home/luode/work/code
sudo mount --bind /mnt/f/code /home/luode/work/code
```

## 推荐持久化

### 映射整个 F 盘

```bash
sudo mkdir -p /home/luode/work/f
echo '/mnt/f /home/luode/work/f none bind 0 0' | sudo tee -a /etc/fstab
sudo mount -a
```

### 映射 F:\\code

```bash
sudo mkdir -p /home/luode/work/code
echo '/mnt/f/code /home/luode/work/code none bind 0 0' | sudo tee -a /etc/fstab
sudo mount -a
```

## 推荐注意事项

- bind mount 主要是给 WSL 内部使用的快捷入口
- Windows 侧访问真实文件时，仍推荐直接打开 `F:\...`
- 不要把 `\\wsl.localhost\Ubuntu\home\luode\work\f` 当成 `F:\` 的稳定替代入口
- `\\wsl.localhost` 更适合访问 WSL 自己的 Linux 文件，而不是“Windows 盘映射进 WSL 后再反向给 Windows 打开”的路径
