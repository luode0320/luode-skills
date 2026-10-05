---
name: app-internal-screenshot-rules
description: 需要给运行中的应用（Godot、游戏客户端、Electron、自绘 GUI、OpenGL/Vulkan/DirectX 窗口）截图取证，且担心桌面全屏抓取串到其它应用、依赖前台窗口、或抓到黑屏/陈旧帧时触发。典型信号：要「选定调试的项目截图」、截图会串味、要不动系统鼠标地驱动 GUI、要可重复的窗口画面证据。负责用应用自身的渲染/UI 通道（如 Godot 视口纹理 get_image、浏览器 CDP Page.captureScreenshot、Electron capturePage）取像素，天然只含目标应用自己；不负责浏览器页面内容理解，也不负责窗口级消息投递（那是 window-scoped-capture 的职责）。
---

# 应用内自渲染截图（选定目标应用，不串到其它窗口）

## 适用与不适用

- 适用：任何自身可控渲染的应用（Godot、自研游戏、Electron、Flutter 桌面、Qt 自绘、带调试协议的自绘窗口）。
- 关键判据：应用能输出自己的画面像素（视口纹理 / CDP / 应用自带截图 API），且需要确保证据只包含目标应用。
- 不适用：只能通过操作系统层面拿画面的普通第三方窗口。那类场景用 `window-scoped-capture` 的 `PrintWindow`，并接受它「GPU 窗口可能返回陈旧帧」的已知限制。

## 为什么优先用应用内截图

桌面截图 API（`CopyFromScreen`、`PrintWindow`、`BitBlt`）在本机实测有三类硬伤：

| 失败模式 | 现象 | 后果 |
|---|---|---|
| 全屏抓取串味 | 抓到的是当前前台窗口（可能是别的应用或编辑器） | 证据与目标应用无关，误判 |
| 依赖前台 | 目标不在前台就抓不到 | 不可重复、需抢焦点 |
| 黑屏 / 陈旧帧 | GPU 加速窗口返回黑图或动作之前的一帧 | 把「操作没生效」当成「功能坏了」 |

应用内截图直接从目标应用自己的渲染通道取像素，上述三问题天然消失：只含目标应用、与前台无关、帧内容就是应用当前真实一帧。

## 通用做法

- 应用提供截图 API 就用它：浏览器用 CDP `Page.captureScreenshot`，Electron 用 `win.webContents.capturePage()`。
- 自绘/游戏引擎用「渲染结果纹理」取图：Godot 用 `get_viewport().get_texture().get_image()`，其它引擎用各自的 backbuffer / framebuffer readback。
- 关键约束：**先等一帧渲染完成再取像素**（Godot 用 `await RenderingServer.frame_post_draw`），否则会取到未绘制的空白。
- 无头/离屏环境不渲染画面，必须**显式失败**，禁止输出空白图冒充「证据」。

## Godot 落地参考（本机已验证）

```gdscript
# 取当前视口渲染结果并落盘，只含本项目窗口
await RenderingServer.frame_post_draw
var img: Image = get_tree().root.get_texture().get_image()
img.save_png("res://output/debug_shots/shot_%d.png" % Time.get_ticks_msec())
```

- 无头环境判定：`DisplayServer.has_feature(DisplayServer.FEATURE_MOUSE)` 为假即无头，直接返回失败。
- 与 `window-scoped-capture` 的分工：优先用应用内截图；只有应用完全不提供画面通道、且必须拿操作系统层画面时，才回退窗口级/屏幕级抓取。

## 执行通过 / 驳回标准

- 通过：截图内容确认来自目标应用自身；不依赖前台、不移动系统光标、不干扰其它应用；无头环境明确失败；画面与动作形成「动作 -> 变化」可重复证据链。
- 驳回：用全屏截图冒充目标应用证据；把无头空图当成成功；单凭一张可能陈旧的截图就断言某功能失效（须用应用状态或调试通道交叉验证）。
