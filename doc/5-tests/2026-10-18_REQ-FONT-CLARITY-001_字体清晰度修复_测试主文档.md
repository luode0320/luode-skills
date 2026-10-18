---
schema_version: 1
doc_id: TEST-FONT-CLARITY-001
doc_type: test_main
template_version: 1
source_ids:
  - SRC-FONT-CLARITY-001
version: 1
current_slice: 全部四个最小任务
updated_at: 2026-10-18
status: accepted
unresolved_decisions: 0
reader_level: business_general
writing_style: plain_chinese
appendix_policy: preserve_existing_or_one_terminal_appendix
---

# 测试主文档：组件库文字清晰度修复

结论：四项最小任务全部通过真实测试与全量回归；影响：后台所有页面与 752 张组件示例卡；范围：噪点层、字重轴、字号行高、全量守卫；非范围：接口与数据库测试（本轮不涉及）；变化：文字边缘更锐利、字重层次可辨；完成标准：全部守卫 PASS 且构建成功；术语说明：`dpr` 指设备像素比；验证状态：已执行并通过。

## 1. 测试环境

| 项 | 取值 |
| --- | --- |
| 运行方式 | 本地 Vite 开发服务（`npm run dev`） |
| 端口 | 5196–5202 独立端口，执行后按 PID 终止 |
| 浏览器 | Playwright Chromium（HeadlessChrome 149） |
| 视口 | 1600×1000，`device_scale_factor=1` |
| 登录方式 | mock 接口 `POST /api/auth/login`，captcha 固定 `1024` |
| 操作系统 | Windows 10.0.19045 |

## 2. 测试结果总表

| 任务 | 测试内容 | 结果 | 证据 |
| --- | --- | --- | --- |
| `TASK-01` | 噪点层开/关正文像素对照 | 通过 | 逐字节相同，自噪声对照 0% |
| `TASK-02` | 五档字重字形差异 | 通过 | 5 种字形，宽度 300.45→305.66 递增 |
| `TASK-03` | 非整数字号收敛 | 通过 | 9.13% → 0.46% |
| `TASK-03` | 布局回归（5 个代表页） | 通过 | 零溢出、零空白卡 |
| `TASK-04` | `FIDELITY` | 通过 | `PASS (263 local / 139 upstream-tracked)` |
| `TASK-04` | `FONT_OVERRIDES` | 通过 | `PASS (82 selectors, 5 size groups)` |
| `TASK-04` | `DEMO_VISIBILITY` | 通过 | `PASS (101 页 752 卡)` |
| `TASK-04` | `DEMO_GUIDES` | 通过 | `PASS (101 页 752 卡)` |
| `TASK-04` | `vue-tsc --noEmit` | 通过 | 退出码 0 |
| `TASK-04` | `npm run test:unit` | 通过 | 21/21 |
| `TASK-04` | `npm run build` | 通过 | 4.13s |
| `TASK-04` | 测试污染扫描 | 通过 | `POLLUTION: PASS` |

## 3. 详细证据

### 3.1 噪点层让位（TASK-01）

方法：同一页面连续截图，仅切换 `.grain-layer{display:none}`；同时做同条件两次截图作为自噪声对照，并关闭动画排除补间残留。

结果：

| 页面 | 噪点开/关差异 | 判定 |
| --- | --- | --- |
| `/gallery/general/button` | 逐字节相同（0%） | 通过 |
| `/gallery/layout/divider` | 逐字节相同（0%） | 通过 |
| `/gallery/display/table` | 逐字节相同（0%） | 通过 |

计算样式佐证：`grainZ = -1`、`appZ = 0`、`stageBg = rgba(0, 0, 0, 0)`。

首轮曾出现 0.02% 差异（最大 117 灰阶），经自噪声对照确认为入场动画残留，非回归；关闭动画后复测为 0%。

### 3.2 字重轴解锁（TASK-02）

方法：每个字重创建独立元素（28px、文本「组件示例文字 ABC 123」），只截元素自身盒子取 MD5。

| 字重 | 像素哈希 | 元素宽度 |
| --- | --- | --- |
| 400 | `5e97477a` | 300.45 |
| 500 | `afb717ef` | 302.67 |
| 560 | `c87d0697` | 303.59 |
| 620 | `ab489335` | 304.48 |
| 700 | `d901130a` | 305.66 |

五档哈希互异，且宽度随字重单调递增——这是可变字体轴真实生效的独立佐证。`document.fonts` 中 `PearlSans` 状态为 `loaded`，权重声明 `100 900`。

对照：改动前同样测法只有 3 种字形（500 与 560 相同、620 与 700 相同）。

### 3.3 字号行高整数化（TASK-03）

方法：遍历 6 个代表页全部可见文本节点，读取 `fontSize` 与 `lineHeight`。

结果：非整数字号字符占比由 **9.13%** 降至 **0.46%**。剩余为 `em` 派生值（12.8px、17.92px）与 SVG 缩放，不属于字号声明范围。

本地扩展层 17 个文件非整数字号已全部清零；冻结层 82 处由 `build_font_overrides.py` 自动派生覆盖。

### 3.4 布局回归

5 个代表页（button / divider / display-table / modal / locate）全部零溢出、零空白卡。

### 3.5 全量守卫

- `FIDELITY: PASS (263 local / 139 upstream-tracked; upstream 577079e9a347)` —— 冻结面未被触碰
- `FONT_OVERRIDES: PASS (82 selectors, 5 size groups)` —— 派生块与冻结源同步
- `DEMO_VISIBILITY: PASS (扫描 101 页 752 张示例卡，组件全部在卡内可见)`
- `DEMO_GUIDES: PASS (扫描 101 页 752 张示例卡，每格提示均对应本格示例)`

### 3.6 构建与类型

- `npx vue-tsc --noEmit`：退出码 0
- `npm run test:unit`：21 通过、0 失败
- `npm run build`：`✓ built in 4.13s`

### 3.7 测试污染扫描

`POLLUTION: PASS`，4 条命中均为既有登记豁免（`task_plan_projection.py` 三处、`session-regression.py` 一处），本轮未新增。

## 4. 未覆盖说明

| 项 | 原因 |
| --- | --- |
| 接口测试 | 本轮不涉及 HTTP 接口 |
| 数据库测试 | 本轮不涉及数据库 |
| 多浏览器 | 仅在 Chromium 验证；Firefox / Safari 的 `local()` 行为未测 |
| 高 dpi 视口 | 仅在 `dpr=1` 验证；`dpr=2` 下非整数问题本就不可见，未单独回归 |

## 5. 清理与回滚

- 全部探针在独立端口启动服务，执行后按端口查 PID 终止并确认端口释放。
- 临时脚本与截图目录已删除。
- 代码回滚方式：删除 `overrides.css` 中新增的三个规则块即可；本地扩展层的字号改动可逐文件还原。

图片资产决策：N/A + 原因：本测试以命令输出、像素哈希与守卫文本为证据，无需视觉资产归档 + 证据：第 2、3 节全部结论均由哈希与退出码判定。
