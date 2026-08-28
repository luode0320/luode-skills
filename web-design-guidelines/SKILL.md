---
name: web-design-guidelines
description: "审查 UI 代码是否符合 Web Interface Guidelines（Vercel 规范）：无障碍、焦点状态、表单、动画、排版、内容处理、图片、性能、导航与状态、触摸交互、安全区、深色模式、本地化、水合安全、文案。适用于“帮我审查 UI”“检查可访问性”“设计审计”“UX 评审”“按最佳实践检查网站”“审查组件代码”等请求。触发词：审查 UI、UI 审查、可访问性检查、a11y、设计审计、UX 评审、界面规范、web interface guidelines、无障碍、焦点状态、aria-label、反模式检查。"
license: MIT
metadata:
  displayName: "Web 界面规范审查"
  version: "1.1.0"
  author: "vercel"
---

# Web 界面规范审查

用于检查目标文件是否符合 Web Interface Guidelines。**远程优先、本地兜底**：优先拉取最新规范，拉取失败时使用内置本地规范副本（`local-guidelines.md`），保证离线/网络异常环境下审查能力不缺失。

## 工作流程

1. **尝试拉取远程规范**（最新版）：
   `https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md`
2. **失败降级**：拉取失败（网络/超时/404）时，读取本地兜底 `local-guidelines.md`（完整规范快照），并在输出开头注明「使用本地规范副本」。
3. **读取目标文件**：未提供文件时先询问用户文件或匹配模式。
4. **逐条审查**：按规范 15 类规则 + 反模式清单逐条核对。
5. **输出**：按 `file:line` 格式分组输出（见「输出格式」），结论精炼、无开场白。

## 审查重点（15 类）

无障碍 · 焦点状态 · 表单 · 动画 · 排版 · 内容处理 · 图片 · 性能 · 导航与状态 · 触摸与交互 · 安全区与布局 · 深色模式与主题 · 本地化 · 水合安全 · 文案

每类要点与反模式完整清单见 `local-guidelines.md`（或远程最新版）。

## 输出格式

```text
## src/Button.tsx

src/Button.tsx:42 - icon button missing aria-label
src/Button.tsx:18 - input lacks label
src/Button.tsx:55 - animation missing prefers-reduced-motion

## src/Card.tsx

✓ pass
```

- 按文件分组；`file:line`（VS Code 可点击）
- 只给问题+位置，修复不显然时补充一句说明

## 适用边界

**何时用**：审查 UI/组件代码的规范符合性、可访问性、UX 反模式。

**何时不用**：
- 从零设计 UI 视觉风格 → 转 `frontend-design`；
- 前端视觉/主题/配色/字体规范 → 转 `frontend-ui-visual-rules`；
- React/Vue 组件开发本身 → 转 `frontend-component-rules`、`vue__skillhub`；
- 浏览器端实际交互验证 → 转 `browser-session-automation-rules`、`browser-advanced-testing-rules`。

## 验收清单

- [ ] 已尝试拉取远程规范（网络异常时已降级到本地兜底并注明）
- [ ] 目标文件已按 15 类规则 + 反模式清单逐条核对
- [ ] 输出按 `file:line` 分组，无开场白、无冗长解释
- [ ] 反模式项（transition: all、outline-none、div onClick 等）已单独标记
- [ ] 无问题文件标注 `✓ pass`
