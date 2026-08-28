---
name: github-pages-auto-deploy
description: "配置 GitHub Pages 自动部署：GitHub Actions 工作流、自定义域名（CNAME）、HTTPS、CDN 与预览环境。当用户需要把静态网站（个人博客、项目文档、作品集、官网）自动部署到 GitHub Pages、配置自定义域名或排查 Pages 部署失败时触发。触发词：GitHub Pages、自动部署、静态网站部署、gh-pages、部署网站、自定义域名、pages 部署、deploy to github pages。"
license: MIT
metadata:
  displayName: "GitHub Pages 自动部署"
  version: "1.1.0"
  homepage: "https://api.skillhub.cn/sendwealth/github-pages-auto-deploy"
  tags: [github-pages, deploy, static-site, github-actions, custom-domain]
allowed-tools: Bash, Read, Write
---

# GitHub Pages 自动部署

配置静态网站自动部署到 GitHub Pages：推送代码 → Actions 自动构建 → 上线，支持自定义域名与 HTTPS。

## 适用边界

- **做**：生成 deploy-pages.yml 工作流、配置 GitHub Pages 源为 Actions、自定义域名（CNAME + DNS）、HTTPS 启用、预览环境、部署后健康检查。
- **不做（转交）**：
  - 其它平台部署（Vercel/Netlify/CloudStudio）→ 对应部署 skill（如 `cloudstudio-deploy`）
  - GitHub 仓库/PR/认证操作 → `github`（GitHub CLI）
  - 静态站点生成（Hugo/Jekyll/Next 构建）→ 先在本项目构建出静态产物再部署

## 工作流（5 步）

### 第 1 步：确认站点结构与产物目录

- **输入**：本地站点目录（如 `website/` 或构建产物目录）。
- **动作**：确认静态文件存在（index.html 等）；区分「纯静态目录」与「需构建的框架项目」（框架项目先确认构建命令与产物目录）。
- **输出**：站点类型 + 部署目录结论。

### 第 2 步：生成工作流文件（检查点）

- **输入**：第 1 步结论。
- **动作**：创建 `.github/workflows/deploy-pages.yml`（模板见下），按实际目录与分支调整 `path` 与 `branches`。
- **检查点【必确认】**：目标分支（master/main）、部署目录、是否含自定义域名三项与用户确认后再落盘；分支受保护时说明需要 PR 或临时放开。
- **输出**：deploy-pages.yml。

### 第 3 步：启用 Pages 并推送

- **输入**：确认后的工作流文件。
- **动作**：仓库 Settings → Pages → Source 选 GitHub Actions；推送代码触发部署。
- **检查点【必确认】**：推送/部署涉及写仓库历史与远端，执行前必须获得用户当轮明确授权（遵循仓库 Git 规则）。
- **输出**：触发记录 + 部署 URL。

### 第 4 步：配置自定义域名（可选）

- **输入**：用户拥有的域名。
- **动作**：`website/` 下创建 `CNAME` 文件；域名服务商加 CNAME 记录（名称 `@` 或 `www`，值 `yourusername.github.io`）；Settings → Pages → Enforce HTTPS 等证书生成。
- **输出**：DNS 配置清单 + 生效检查点（DNS 传播最长 48h）。

### 第 5 步：验证与监控

- **输入**：部署完成后的 URL。
- **动作**：健康检查（`curl -f <url>`）、必要时接 Lighthouse CI；确认页面与资源可达。
- **输出**：验证结论（可访问 / 失败原因）。

## 工作流模板（deploy-pages.yml）

```yaml
name: Deploy Website to GitHub Pages

on:
  push:
    branches: [ master ]
    paths:
      - 'website/**'
      - '.github/workflows/deploy-pages.yml'

permissions:
  contents: read
  pages: write
  id-token: write

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4
      - name: Setup Pages
        uses: actions/configure-pages@v4
      - name: Upload artifact
        uses: actions/upload-pages-artifact@v3
        with:
          path: 'website'
      - name: Deploy to GitHub Pages
        uses: actions/deploy-pages@v4
```

自定义域名：`website/CNAME` 写入 `yourdomain.com`；预览环境可加 `deploy-preview` job（`if: github.event_name == 'pull_request'`，`rossjrw/pr-preview-action`）。

## 边界条件与异常处理

- **部署失败**：先查 Actions 日志 → 确认 Pages 已启用（Source=GitHub Actions）→ 验证 `path` 与产物目录一致 → 确认权限（`pages: write`、`id-token: write`）。
- **域名无法访问**：检查 DNS 记录与 CNAME 文件是否在部署目录内 → 等待传播（最多 48h）→ 确认 HTTPS 已启用。
- **HTTPS 证书错误**：等待证书生成（几分钟）→ 检查域名解析 → 确认 DNS 指向 `yourusername.github.io`。
- **分支保护**：目标分支受保护时，不强行 push；改为走 PR 合并触发或与用户确认调整策略。
- **构建型站点**：先在本地/CI 构建出静态产物，工作流中构建步骤产物路径与 `upload-pages-artifact` 的 `path` 一致，避免空目录部署。

## 成本说明

- GitHub Pages / CDN / HTTPS：免费；自定义域名：域名注册费（约 ¥50-100/年）。

## 退出机制

用户输入「结束」→ 停止，回复「部署配置完成。」；工作流落盘、推送、DNS 变更等对外/写仓库动作前必须先经用户确认。

## 约束

- 工作流 YAML 与 GitHub Pages 官方 Actions 用法保持一致，使用 `actions/checkout@v4`、`actions/configure-pages@v4`、`actions/upload-pages-artifact@v3`、`actions/deploy-pages@v4` 版本组合。
- 推送/部署写仓库历史与远端，遵守仓库 Git 规则，未获当轮授权不执行。
- 域名/DNS 变更影响线上访问，变更前与用户确认，变更后给出验证步骤。
