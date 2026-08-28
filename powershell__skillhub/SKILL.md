---
name: "powershell"
description: "PowerShell 脚本编写与调试陷阱规避：输出行为（非预期输出/return 语义）、数组与标量陷阱、比较运算符、字符串插值、管道处理、错误处理（ErrorActionPreference/try-catch）、常见反模式、跨平台兼容（pwsh vs Windows PowerShell）。适用于编写或审查 PowerShell 脚本、排查脚本输出异常/数组处理错误/比较失效场景。触发词：powershell、pwsh、ps1、power shell 脚本、脚本输出不对、return 没生效、数组为空、比较运算符、-eq、管道 foreach、错误处理、ErrorActionPreference、try catch、ps 跨平台、powershell 报错。"
license: MIT
metadata:
  displayName: "PowerShell 脚本陷阱与调试"
  version: "1.1.0"
  author: "Clawhub Developer"
---

# PowerShell 脚本陷阱与调试

以**编写-调试视角**组织的 PowerShell 反模式手册：每条陷阱按「症状 → 根因 → 正确写法 → 验证」四步闭环，覆盖输出、数组、比较、字符串、管道、错误处理、反模式与跨平台 8 个主题。写脚本前先对照「验收清单」，出问题按「陷阱速查表」定位。

## 使用流程

1. **编写**：对照 §1-§8 的「正确写法」写主体逻辑，优先使用完整 cmdlet 名与显式类型。
2. **调试**：现象 → 「陷阱速查表」定位章节 → 读「症状/根因」确认 → 按「正确写法」修改。
3. **验证**：每处修改后跑一次脚本（或对应最小复现片段），确认输出/行为符合预期。
4. **收尾**：对照「验收清单」逐项自查后交付。

## 陷阱速查表

| 现象 | 章节 | 最常见根因 |
|---|---|---|
| 函数/脚本多输出不该输出的内容 | [§1 输出行为](#1-输出行为) | 未捕获表达式也进了输出流 |
| 数组只有一个元素时处理异常 | [§2 数组与标量](#2-数组与标量) | 单元素被解包为标量 |
| `==` / `>` 比较不生效 | [§3 比较与条件](#3-比较与条件) | 用了 C 风格运算符 |
| 变量没展开 / 多行字符串难写 | [§4 字符串与插值](#4-字符串与插值) | 引号类型与子表达式用法错 |
| foreach 语句不消费管道 | [§5 管道处理](#5-管道处理) | 混淆 `foreach` 与 `ForEach-Object` |
| try/catch 没捕获到错误 | [§6 错误处理](#6-错误处理) | 非终止错误未转 Stop |
| 脚本换台机器就崩 | [§8 跨平台兼容](#8-跨平台兼容) | 用了平台专属别名/路径写法 |

---

## 1. 输出行为

**症状**：函数返回了多余的 `Write-Output` 之外的内容；`return $x` 之后还有额外输出。

**根因**：PowerShell 中**一切未被捕获的表达式都会进输出流**——`return` 不阻止此前表达式的输出，`Write-Host` 之外的 `"字符串"` 本身也是输出。

**正确写法**
```powershell
function Get-User {
    $u = Get-ADUser -Identity $args[0]   # 这行没有赋值捕获 → 会输出！
    return $u.Name
}
# 改为：
function Get-User {
    $u = Get-ADUser -Identity $args[0] | Out-Null   # 显式丢弃
    return $u.Name
}
```
- 抑制输出：`$null = ...` 或 `[void](...)`。
- `Write-Host` 仅用于屏幕显示，**不进入管道**——需要返回值给下游时不要用它。

**验证**：`Get-User xxx` 只输出预期字段；用 `@(Get-User xxx).Count` 确认输出元素数符合预期。

## 2. 数组与标量

**症状**：`$arr.Count` 在结果只有一项时报错或返回 1；空结果判断失效。

**根因**：单元素结果被解包为**标量**（没有 `.Count` 语义），空结果返回 `$null` 而非空数组。

**正确写法**
```powershell
# 强制数组：单元素也有 .Count / 可遍历
$items = @(Get-Item .)
# 空判断：不要用 if ($items)，用 Count 明确
if ($items.Count -gt 0) { ... }
# 循环中避免 +=（每次创建新数组，慢）：用 ArrayList
$list = [System.Collections.ArrayList]::new()
[void]$list.Add($item)
# 返回数组不被解包
return ,$items
```
- `,` 是数组包装运算符：`,$item` 把单元素包成数组。

**验证**：单元素与多元素两种输入下 `$items.Count` 均正确；万次循环的 `+=` 改为 ArrayList 后耗时显著下降。

## 3. 比较与条件

**症状**：`if ($a == $b)` 永远不成立；`if ($a > 5)` 报错或行为诡异。

**根因**：PowerShell 用 `-eq/-ne/-gt/-lt` 而非 `==/!=/>/<`；`=` 是赋值不是比较。

**正确写法**
```powershell
if ($a -eq $b) { }            # 相等
if ($a -like "*abc*") { }     # 通配符
if ($a -match "^\d+$") { }    # 正则
if ($arr -contains $item) { } # 数组成员判断（等价 -in 反向）
if ($null -eq $var) { }       # $null 放左侧，避免数组比较陷阱
# 大小写敏感：-ceq / -cmatch
```
- 默认**不区分大小写**；需要严格匹配用 `-c` 前缀系列。

**验证**：用 `-eq` 重写后条件分支按预期进入；`$null -eq $var` 对数组与标量均稳定。

## 4. 字符串与插值

**症状**：`"$name.Count"` 输出为空；多行文本拼接到崩溃。

**根因**：双引号才插值，单引号字面量；复杂表达式插值需要 `$( )` 子表达式。

**正确写法**
```powershell
$name = "world"
"Hello $name"                    # Hello world
'$name'                          # 字面 $name（不展开）
"Count: $($arr.Count)"           # 属性/方法用子表达式
@"                                # 双引号 here-string：插值
Line1 $name
Line2
"@
@'
$name 保持字面
'@
"a`nb"                           # `n 换行、`t 制表符
```
**验证**：复杂插值一律 `$()` 包裹后输出正确；here-string 闭标签 `"@`/`'@` 顶格书写（前无空格）。

## 5. 管道处理

**症状**：`$x | foreach { ... }` 之后 `$x` 没变化；`foreach` 语句接管道报错。

**根因**：`foreach` 是语句（遍历已存在的集合），**不消费管道**；管道里要用 `ForEach-Object`（`$_` 为当前对象）。

**正确写法**
```powershell
Get-Service | ForEach-Object { $_.Status }          # 管道逐对象处理
Get-Service -PipelineVariable svc | Where-Object { $svc.Status -eq 'Running' }  # 中间对象
# 变量赋值结果也是管道流：$out = Get-Service | Select Name
```
- 管道**逐个对象流式处理**：`Write-Host` 在管道内逐项打印是正常现象。

**验证**：管道链输出符合预期；`ForEach-Object` 与 `foreach` 按场景正确选用。

## 6. 错误处理

**症状**：`try { Remove-Item x } catch { ... }` 的 catch 从未执行。

**根因**：PowerShell 多数命令抛**非终止错误**，`try/catch` 只捕获**终止错误**。

**正确写法**
```powershell
$ErrorActionPreference = 'Stop'          # 全局默认转终止
try {
    Remove-Item "x" -ErrorAction Stop    # 或单命令转终止
} catch {
    Write-Error "删除失败: $_"
}
# 判断原生命令成败
if ($LASTEXITCODE -ne 0) { ... }         # 外部程序
if (-not $?) { ... }                     # 上一条 cmdlet 是否成功
```
- 常用 `$ErrorActionPreference`：`Stop` / `Continue` / `SilentlyContinue`。

**验证**：制造一次失败（删除不存在的文件），确认 catch 分支执行；外部命令按 `$LASTEXITCODE` 判断。

## 7. 常见反模式

| 反模式 | 正确做法 |
|---|---|
| `if($x){`（`{` 前无空格） | `if ($x) {` 保持空格，可读且避免解析歧义 |
| 条件里用 `=` 赋值 | 比较用 `-eq` |
| `return $arr` 数组被解包 | `return ,$arr` |
| `Get-Content` 逐行处理却当单串 | 需整串用 `-Raw` |
| 假设 `Select-Object` 是引用 | 它创建**新对象**，属性是拷贝，改原对象无效 |
| 依赖 `ls`/`cat` 等别名 | 用完整 cmdlet 名（`Get-ChildItem`/`Get-Content`） |

**验证**：逐条对照反模式表审查自己的脚本，全部命中「正确做法」列。

## 8. 跨平台兼容

**症状**：脚本在 Linux 上跑 `powershell` 不存在；路径分隔符/环境变量写法报错。

**根因**：`powershell` 是 Windows PowerShell 5.1，`pwsh` 才是 PowerShell 7+；平台差异未处理。

**正确写法**
```powershell
# 路径拼接用 Join-Path（自动处理分隔符）
$cfg = Join-Path $env:APPDATA "app/config.json"
# 环境变量 $env:VAR 全平台通用
# 别用平台专属别名；换行用 `n 不要硬编码 \r\n
```
- 元数据要求：脚本头部标注 `pwsh` 依赖（本 skill 的 metadata 已声明 `requires.bins: pwsh`）。

**验证**：在 Linux/macOS 上以 `pwsh` 运行通过；`Join-Path` 生成的路径在目标平台可直接访问。

---

## 适用边界

**何时用**：编写/审查 PowerShell 脚本、定位输出/数组/比较/管道/错误处理类陷阱、做跨平台脚本移植。

**何时不用**：
- Windows 专属环境变量、路径编码、注册表等系统集成细节 → 转 `windows-powershell-environment-rules`、`windows-encoding-rules`；
- WSL 环境下的 PowerShell 桥接 → 转 `wsl-powershell__skillhub`；
- 通用 shell 脚本（Bash）语义 → 转 `bash__skillhub`、`shell__skillhub`；
- 交互式终端自动化（非脚本语义）→ 转 `browser-session-automation-rules` 等同级自动化类 skill。

## 验收清单

- [ ] 函数/脚本无意外输出（多余表达式已 `Out-Null` / `$null =` 抑制）
- [ ] 数组操作使用 `@()` 强制数组 / `ArrayList`，无 `+=` 大循环
- [ ] 所有比较使用 `-eq/-ne/-gt/-lt` 系列，`$null` 放左侧
- [ ] 插值用 `$( )` 包裹属性/方法；here-string 闭标签顶格
- [ ] 管道用 `ForEach-Object`，语句用 `foreach`，未混用
- [ ] 错误处理已 `-ErrorAction Stop` 或设置 `$ErrorActionPreference`
- [ ] 路径用 `Join-Path`、无平台专属别名，`pwsh` 可运行
