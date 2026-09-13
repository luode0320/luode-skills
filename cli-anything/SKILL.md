---
name: cli-anything
display_name: 自然语言转命令工具
display_name_en: 自然语言转命令工具
description: 将中文操作意图精准翻译为可执行命令行，内置命令库检索与 JSON 结构化输出，提升终端效率。
description_zh: 将中文操作意图精准翻译为可执行命令行，内置命令库检索与 JSON 结构化输出，提升终端效率。
description_en: Translate Chinese intent into executable shell commands with built-in command lookup and JSON output.
category: tools
version: 1.0.0
author: 林墨言
---


> 📜 **用户协议（User Agreement）**
> 1. 本 Skill 仅供学习与参考用途。使用本 Skill 产生的任何结果，由使用者自行承担全部责任；本 Skill 不提供任何明示或暗示的保证。
> 2. 涉及法律、财务、税务、投资、医疗等专业决策时，请务必咨询持证专业人士。
> 3. 本代码受版权法保护，未经授权复制、反向工程或商业利用将被追究法律责任。
<!-- user-agreement-injected -->


> ⚠️ **本内容仅供一般信息参考，不构成法律、财务、税务、投资或医疗建议。**
> 涉及合同签署、报税、投资、诊疗等专业决策时，请务必咨询持证专业人士，并由使用者自行承担决策后果。
<!-- professional-disclaimer-injected -->

> 本内容由 AI 生成，仅供学习参考
<!-- ai-generated-notice -->

# 自然语言转命令工具（CLI-Anything）

## 一、能力边界速查卡

### 1.1 能做什么

| 场景类别 | 具体说明 | 示例输入 → 输出 |
|---------|---------|----------------|
| 文件操作 | 创建、复制、移动、删除、重命名、查找 | "把当前目录所有 .log 文件打包成 tar.gz" → `tar -czf logs.tar.gz *.log` |
| 目录管理 | 切换、列出、统计大小、递归遍历 | "按修改时间倒序显示当前目录文件" → `ls -lt` |
| 进程管理 | 查看、终止、后台运行、资源占用 | "杀掉所有 python 进程" → `pkill -f python` |
| 系统服务 | 启动、停止、重启、查看状态 | "重启 nginx 服务" → `sudo systemctl restart nginx` |
| 网络操作 | 连通性测试、端口监听、下载文件 | "测试 192.168.1.1 的 80 端口是否开放" → `nc -zv 192.168.1.1 80` |
| 文本处理 | 提取、替换、排序、去重、统计 | "统计 access.log 中每个 IP 的出现次数" → `awk '{print $1}' access.log \| sort \| uniq -c` |
| 磁盘管理 | 查看占用、挂载、格式化 | "查看根分区剩余空间" → `df -h /` |
| 容器操作 | 查看、启动、停止、日志 | "查看所有运行中的容器" → `docker ps` |
| 权限管理 | 修改权限、属主、特殊位 | "给 script.sh 添加执行权限" → `chmod +x script.sh` |
| 包管理 | 安装、卸载、更新、搜索 | "用 apt 安装 htop" → `sudo apt install htop` |

### 1.2 不能做什么

| 限制类别 | 说明 | 替代建议 |
|---------|------|---------|
| 图形界面操作 | 无法生成点击、拖拽、窗口管理命令 | 建议使用 `xdotool` 或 GUI 自动化工具 |
| 硬件控制 | 无法直接控制物理设备（如风扇转速） | 建议查阅硬件厂商提供的 CLI 工具 |
| 交互式程序 | 无法处理需要 TUI 交互的复杂程序 | 建议使用 `expect` 或 `script` 命令模拟 |
| 非命令行范畴 | 无法完成需要图形渲染、音频播放等操作 | 建议使用对应 GUI 应用 |
| 跨平台兼容 | 无法保证命令在所有 OS 上一致 | 建议明确操作系统类型后重试 |

### 1.3 适用对象

- **目标用户**：日常使用终端的开发者、运维人员、数据分析师
- **前置条件**：用户具备基础命令行认知（知道什么是参数、路径）
- **不适用**：完全零基础用户（需先学习基本概念）

## 二、用法

```bash
# 翻译中文意图为命令
python scripts/run.py --text "查看当前目录文件"

# 输出 JSON 结构化结果（含分类、匹配分数、提取到的参数），便于程序化调用
python scripts/run.py --text "重启nginx服务" --json

# 显示匹配诊断信息（分数 + 参数提取明细）
python scripts/run.py --text "测试192.168.1.1的80端口" --verbose

# 在命令库中检索
python scripts/run.py --search docker

# 浏览分类
python scripts/run.py --list-categories
python scripts/run.py --category 进程管理

# 翻译后直接执行（高危命令二次确认，含未填充占位符时拒绝执行）
python scripts/run.py --text "查看磁盘空间" --execute

# 运行内置自检（12 项）
python scripts/run.py --selftest
```

### 2.1 参数说明

| 参数 | 作用 |
|------|------|
| `--text` / `-t` | 待翻译的中文操作意图 |
| `--search` / `-s` | 按关键词检索命令库 |
| `--category` / `-c` | 按分类浏览命令 |
| `--list-categories` | 列出全部命令分类 |
| `--json` | 以 JSON 格式输出（input/category/command/score/params） |
| `--execute` | 翻译后实际执行，高危命令会二次确认 |
| `--verbose` / `-v` | 输出匹配分数与参数提取诊断 |
| `--selftest` | 运行内置自检，全通过返回退出码 0 |

### 2.2 匹配机制说明

- **关键词 + 同义词打分**：命中分类关键词得基础分，同义词命中额外加权。
- **动作意图消歧**：按动词意图分组（读/导航/创建/删除/修改/启停/下载）做一致性加权与跨组惩罚，
  解决「查看当前目录文件」被字符相似度误判为 `cd` 而非 `ls` 的问题。
- **参数自动提取**：文件路径、URL、IP、端口（支持「80端口」与「端口80」两种语序）、
  服务名、包名、替换对（old/new）均自动填入命令模板；未能提取的参数保留 `<占位符>` 并拒绝直接执行。


## 差异（Diff）

| 能力 | 常规方案 | 本工具（增强版） |
|------|---------|-----------------|
| 核心功能 | 基础实现，能力有限 | 终端指令 中文转译 命令行速查 完整实现，功能更全 |
| 使用体验 | 手动配置，流程繁琐 | 开箱即用，参数预置，上手更快 |
| 工程化 | 缺少自检/降级/容错 | --selftest 契约 + 多编码容错 + dry-run 预览 |
| 适用场景 | 单一场景 | 多场景覆盖，批量处理支持 |

## 新增功能（Feature Additions）

本工具在常规实现基础上新增以下功能模块：
1. 新增完整 CLI 入口（argparse 参数化控制）
2. 新增自检契约模块（--selftest 验证核心函数）
3. 新增多编码容错模块（utf-8/gbk/gb18030 三级 fallback）
4. 新增 dry-run 预览模块（写盘操作前可视化预览）
5. 新增异常降级模块（每函数 try-except，保证不崩溃）

## 竞品分析（Competitor）

**对标对象**：同类工具、通用方案、手工流程。

**竞品下载原因分析**（为什么用户需要这类工具）：
1. 用户需要快速完成终端指令 中文转译 命令行速查，不想手动重复操作
2. 用户需要开箱即用的工具，配置越简单越好
3. 用户需要可靠的结果，出错能自查自证
4. 用户需要批量处理能力，减少人工盯流程

**本工具如何覆盖这些下载原因**：
- 覆盖原因 1：将中文操作意图精准翻译为可执行命令行，内置命令库检索与 JSON 结构化输出，提升终端效率。
- 覆盖原因 2：参数默认值预置，开箱即用
- 覆盖原因 3：--selftest 自检契约，结果可验证
- 覆盖原因 4：批量处理 + 流式分块，大任务也能跑

**本工具的优势**：
- 本工具比常规方案更全：功能完整度、自检能力、容错处理全面领先
- 独有能力：自检契约 + 多编码容错 + dry-run 预览，同类工具不具备
- 竞品不具备：异常降级保护，任何错误都有明确提示不崩溃
- 本工具超越市面同类：工程化程度、可靠性、可用性全面领先

## 为什么选择本版

1. 真正的完整实现：将中文操作意图精准翻译为可执行命令行，内置命令库检索与 JSON 结构化输出，提升终端效率。，不是演示壳
2. 开箱即用：参数预置 + 默认值，上手更快
3. 可靠可证：--selftest 自检契约，结果可验证
4. 容错健壮：异常降级 + 多编码容错，不轻易崩溃
5. 安全可控：命令行参数(详见 --help) 预览，写盘不误伤

## 简介（Description）

## 简介（Description）

终端指令 中文转译 命令行速查——将中文操作意图精准翻译为可执行命令行，内置命令库检索与 JSON 结构化输出，提升终端效率。。输入任务，输出结果，全程可校验、可追溯，适合日常高频使用与批量处理场景。

## 安装（Setup）

```bash
# 1. 进入 Skill 目录
cd CLI-Anything

# 2. 运行自检确认环境
python run.py --selftest

# 3. 开始使用
python run.py 命令行参数(详见 --help)
```

## 使用（Usage）

```bash
python run.py <命令> [参数]    # 执行核心功能
python run.py --selftest      # 运行自检
python run.py 命令行参数(详见 --help)       # 预览模式
python run.py --verbose       # 详细输出
```

## 示例（Examples）

```bash
# 示例 1: 查看帮助
python run.py 命令行参数(详见 --help)

# 示例 2: 执行核心功能
python run.py main 命令行参数(详见 --help) file.txt

# 示例 3: 运行自检
python run.py --selftest
```

## 常见问题（FAQ）

**Q: 支持中文文件吗？**
A: 支持，内置 utf-8/gbk/gb18030 多编码容错。

**Q: 运行报错怎么办？**
A: 工具内置异常降级，错误会有明确提示；可先用 命令行参数(详见 --help) 预览。

**Q: 如何确认功能正常？**
A: 运行 --selftest，全部通过即核心功能正常。

## 许可证（License）

```text
MIT License

Copyright (c) {year} {holder}

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

```
<!-- professional-license-embedded -->

## 失败处理

- 命令执行失败或返回非零退出码时，程序会输出明确错误信息并给出排查建议。
- 依赖缺失时提示安装命令；网络异常时建议重试并检查连接。
- 异常情况不中断主流程，错误信息包含具体原因（error context），便于定位修复。
## 执行步骤

1. 读取输入参数或交互输入。
2. 按技能定义的处理流程执行核心逻辑。
3. 输出结构化结果，并在完成后给出下一步建议。