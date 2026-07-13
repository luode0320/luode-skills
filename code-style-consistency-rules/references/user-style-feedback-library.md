# 全局用户风格反例库

本文件是**全局、跨项目、跨会话**的用户代码风格反例库，由 `code-style-consistency-rules` 唯一维护。
任何仓库写代码前都应加载本库，把其中 `active` 条目当作用户明确禁止的写法规避。

## 使用约定

- 条目格式见 `style-case-template.md`；只有 `active` 条目落盘于本文件。
- 写入前必须经用户确认（candidate→active），写入流程见 `style-feedback-workflow.md`。
- 命中同一去重键的重复反馈只更新出现次数与确认时间，不新增条目。
- 本库承载“用户跨项目通用风格偏好”；某个项目专属的一次性风格约定仍写入该项目根目录 `PROJECT_STYLE.md`，由 `project-style-rules` 维护。
- `code-generation-style-rules` 在写码前把本库 `active` 条目并入本轮风格契约的“禁用写法”。

## 反例条目

> 下面第一条为库结构示例条目，演示字段与代码块对照格式；后续用户确认的反例按 `style-case-template.md` 追加。

### STYLE-CASE-GO-001：错误处理禁止吞异常
- id: STYLE-CASE-GO-001
- status: active
- 语言/技术栈: Go
- 适用范围: 错误处理
- 去重键: go|错误处理|吞异常忽略error
- 来源: 库结构示例条目（2026-07-13）
- 反例（禁止这样写）:
  ```go
  data, _ := doSomething()   // 忽略 error
  ```
- 正例（应该这样写）:
  ```go
  data, err := doSomething()
  if err != nil {
      return fmt.Errorf("doSomething 失败: %w", err)
  }
  ```
- 规则一句话: Go 中禁止用 `_` 丢弃 error，必须显式判断并包装返回。
- 首次记录: 2026-07-13
- 确认时间: 2026-07-13
- 出现次数: 1

### STYLE-CASE-GO-002：常量枚举禁止使用 iota
- id: STYLE-CASE-GO-002
- status: active
- 语言/技术栈: Go
- 适用范围: 常量与枚举
- 去重键: go|常量枚举|iota
- 来源: 用户文字反馈（2026-07-13）
- 反例（禁止这样写）:
  ```go
  const (
      StatusInit = iota
      StatusRunning
      StatusDone
  )
  ```
- 正例（应该这样写）:
  ```go
  const (
      StatusInit    = 0
      StatusRunning = 1
      StatusDone    = 2
  )
  ```
- 规则一句话: Go 常量和枚举禁止使用 `iota`，必须显式写出每个常量值。
- 首次记录: 2026-07-13
- 确认时间: 2026-07-13
- 出现次数: 1

## 变更记录

- 2026-07-13：建立全局用户风格反例库，写入库结构示例条目 STYLE-CASE-GO-001。
- 2026-07-13：经周期01捕获流程演练，用户确认后写入 active 条目 STYLE-CASE-GO-002（禁用 iota）。
