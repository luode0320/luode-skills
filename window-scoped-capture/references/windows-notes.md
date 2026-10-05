# Windows 平台细节与踩坑

## PowerShell 5.1 的 `.ps1` 编码陷阱（最高频坑）

- Windows PowerShell 5.1（`powershell.exe`）按**系统 ANSI 代码页**读取脚本文本，而 Windows PowerShell 7+（`pwsh`）与大多数编辑器按 UTF-8 读。
- 后果：UTF-8 编码的 `.ps1` 里只要出现中文（注释、字符串都算），脚本可能直接语法报错，且报错信息指向**别处**：
  - `Missing closing '}' in statement block or type definition.`
  - `The string is missing the terminator: ".`
  - `Unexpected token '...' in expression or statement.`
- 排查原则：**遇到 `.ps1` 里看不懂的语法错误，先怀疑编码，而不是逻辑**。把脚本转为纯 ASCII（英文注释与英文输出）通常立刻恢复。
- 生成脚本时不要用 shell 重定向写入中文；如果要嵌入中文数据，放到单独的 UTF-8 数据文件里由脚本读取，而不是写进 `.ps1`。

## `PrintWindow` 的行为差异

- `PrintWindow(hwnd, hdc, 0)`：整窗（含标题栏与边框），兼容性最好但画面含非客户区。
- `PrintWindow(hwnd, hdc, 2)`（`PW_CLIENTONLY`）：只取客户区，适合「只关心应用内容」的取证。
- 部分显卡驱动 / 远程桌面 / 硬件加速窗口下，`PrintWindow` 可能失败或只渲染出上半部分（其余为黑）。
  - 先退回 `flags = 0` 试一次；
  - 仍失败时可用 `PrintWindow` 取到全黑的事实本身作为证据，并改用应用自带的可编程调试通道（CLI / API / 调试协议）来替代视觉取证，而不是改用全屏截图。
- **静默返回陈旧帧（比全黑更危险）**：`PrintWindow` 在上述环境下还可能**成功返回一张旧画面**——调用不报错、图像尺寸正确、内容却停留在若干帧之前甚至动作开始之前。
  - 危险点：取证者会把「画面没变」误判成「动作没生效」，从而得出「点击无效 / 功能坏掉」的**错误根因**。
  - 判定方法：动作后连抓两张。若两张完全一致但应用自己报告状态已变，基本可判为陈旧帧。
  - 正确替代：当目标窗口**确实处于前台**时，用屏幕区域抓取（`BitBlt(SRCCOPY)` 按客户区在屏幕上的矩形）替代 `PrintWindow`；它取的是实时合成结果，不含其它应用。窗口被遮挡时该方法无效，此时必须退回应用自身的可编程通道，而不是信任 `PrintWindow` 的画面。
  - 收口要求：凡是依据截图得出「某操作无效」的结论，必须先用**独立通道**（应用日志、应用状态查询接口、应用自带调试协议）交叉验证，不得单凭 `PrintWindow` 画面下结论。

## 窗口枚举与过滤

- 用 `EnumWindows` + `GetWindowThreadProcessId` 把窗口归属到目标进程。
- 过滤三条：`IsWindowVisible` 为真、标题非空、客户区尺寸不小于一个阈值（例如 64x64）。否则会把隐藏的辅助窗口 / 消息窗口 / 0 尺寸工具窗一起选中。
- 同一进程可能有多个候选窗口时，取**客户区面积最大**的那个作为主窗口。

## 消息投递的坑

- `PostMessage` 是**异步**投递：投递后要 `Sleep` 一小段时间（80ms 量级）再取截图，否则截到动作前的画面。
- 点击要成对发：`WM_MOUSEMOVE` -> 小睡 -> `WM_LBUTTONDOWN` -> 小睡 -> `WM_LBUTTONUP`。只发 down 不发 up 会让控件停在按下态。
- 坐标打包规则：`LPARAM = (y << 16) | (x & 0xFFFF)`；注意 `y` 在高 16 位、`x` 在低 16 位。
- **已实证：Godot 4 的 Windows 导出程序不响应 `PostMessage` 鼠标消息**（`WM_MOUSEMOVE` / `WM_LBUTTONDOWN` / `WM_LBUTTONUP` 全部投递成功但界面无任何反应）。这类应用只认真实输入队列。
  - 先用 `PostMessage` 做「不抢前台」的按键 / 点击投递；若投递后界面无反应，**先怀疑通道，不要怀疑应用**。
  - 需要真实输入时，用 `SetForegroundWindow` + `SetCursorPos` + `mouse_event`：这要求目标窗口确实在前台，且**必须先用 `WindowFromPoint` / `GetAncestor(GA_ROOT)` 确认点击坐标处的最上层窗口就是目标窗口**，否则会点到坐标下方真正露出的其它窗口。
  - 若无法确认前台无干扰（用户在用电脑），退回应用自身的可编程通道，不要冒险全局注入。

## 键盘按键

- `WM_KEYDOWN` / `WM_KEYUP` 的 `wParam` 是**虚拟键码**（VK），例如 `F12 = 0x7B`、`Esc = 0x1B`、`Enter = 0x0D`、`Tab = 0x09`。
- 字符键的按键还需要区分「扫描码 / 扩展位」，简单场景优先用功能键与 Esc / Enter / Tab 这类稳定的 VK。
- 投递后同样要 `Sleep` 再截图。

## 收口

- 为取证启动的进程必须关闭；临时截图目录在确认不需要作为交付物后删除。
- 若截图本身属于交付物，保留到明确的证据目录，不要留在系统临时目录里。
