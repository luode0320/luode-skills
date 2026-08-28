---
name: bash
description: "编写可靠的 Bash 脚本：引号与分词陷阱、[[ ]] 测试、子 shell 变量丢失、set -euo pipefail 错误处理、数组、参数展开、算术、trap 清理、调试（bash -x）。适用于写/改 bash 脚本、排查脚本变量丢失/引号报错/退出码不对、做健壮性审查场景。触发词：bash、bash 脚本、shell 脚本、sh 脚本、引号、变量展开、word splitting、set -e、pipefail、数组遍历、trap、bash -x、脚本报错、参数展开、环境变量。"
license: MIT
metadata:
  displayName: "Bash 脚本编写与调试"
  version: "1.1.0"
  author: "Clawhub Developer"
---

# Bash 脚本编写与调试

Bash 脚本正确性与健壮性手册。**先走「工作流」再查「知识区」**：写脚本、调试、健壮性审查各有固定流程；语法细节按主题索引文件深入。

## 工作流

### 脚本开发流程
1. **头部安全开关**（新脚本必加）：
   ```bash
   #!/usr/bin/env bash
   set -euo pipefail    # 出错即停 + 未定义变量报错 + 管道失败即失败
   ```
2. **引号纪律**：所有变量 `"$var"`；数组展开 `"${arr[@]}"`；命令替换 `"$(cmd)"`。
3. **变量与参数**：默认值 `${var:-default}`；未设置报错 `${var:?msg}`。
4. **错误处理**：`trap cleanup EXIT` 清理临时文件；可能失败且可容忍的命令放 `if`/`||` 里。
5. **测试**：`bash -n script.sh`（语法）+ 空输入/含空格输入/特殊字符输入各跑一次。

### 调试流程
1. 现象是"变量为空/计数丢了"：检查是否在**子 shell**（管道 `| while`、`( )`）里赋值 → 改用 `while read < file` 或进程替换 `< <(cmd)`。
2. 引号/分词报错：`bash -x script.sh` 跟踪展开；重点看未引号变量是否被拆分。
3. 退出码不对：`set -e` 在 `if`/`||`/`&&` 条件中不生效属正常；管道失败需 `set -o pipefail`。
4. 测试括号报错：一律用 `[[ ]]`（无分词、支持 `&&`/`||`/正则）。

### 健壮性审查清单
- 未引号变量/数组 → 全量检查
- 无 `set -euo pipefail` 的脚本 → 确认是否有意为之
- 临时文件未 trap 清理
- `read` 未加 `-r`（反斜杠被当转义）
- 用 `echo` 输出多变内容 → 改 `printf`
- `local` 未用导致变量泄漏到全局

## Quick Reference

| Topic | File |
|-------|------|
| Arrays and loops | `arrays.md` |
| Parameter expansion | `expansion.md` |
| Error handling patterns | `errors.md` |
| Testing and conditionals | `testing.md` |

## Quoting Traps

- Always quote variables—`"$var"` not `$var`, spaces break unquoted
- `"${arr[@]}"` preserves elements—`${arr[*]}` joins into single string
- Single quotes are literal—`'$var'` doesn't expand
- Quote command substitution—`"$(command)"` not `$(command)`

## Word Splitting and Globbing

- Unquoted `$var` splits on whitespace—`file="my file.txt"; cat $file` fails
- Unquoted `*` expands to files—quote or escape if literal: `"*"` or `\*`
- `set -f` disables globbing—or quote everything properly

## Test Brackets

- `[[ ]]` preferred over `[ ]`—no word splitting, supports `&&`, `||`, regex
- `[[ $var == pattern* ]]`—glob patterns without quotes on right side
- `[[ $var =~ regex ]]`—regex match, don't quote the regex
- `-z` is empty, `-n` is non-empty—`[[ -z "$var" ]]` tests if empty

## Subshell Traps

- Pipes create subshells—`cat file | while read; do ((count++)); done`—count lost
- Use `while read < file` or process substitution—`while read; do ...; done < <(command)`
- `( )` is subshell, `{ }` is same shell—variables in `( )` don't persist

## Exit Handling

- `set -e` exits on error—but not in `if`, `||`, `&&` conditions
- `set -u` errors on undefined vars—catches typos
- `set -o pipefail`—pipeline fails if any command fails, not just last
- `trap cleanup EXIT`—runs on any exit, even errors

## Arrays

- Declare: `arr=(one two three)`—or `arr=()` then `arr+=(item)`
- Length: `${#arr[@]}`—not `${#arr}`
- All elements: `"${arr[@]}"`—always quote
- Indices: `${!arr[@]}`—useful for sparse arrays

## Parameter Expansion

- Default value: `${var:-default}`—use default if unset/empty
- Assign default: `${var:=default}`—also assigns to var
- Error if unset: `${var:?error message}`—exits with message
- Substring: `${var:0:5}`—first 5 chars
- Remove prefix: `${var#pattern}`—`##` for greedy

## Arithmetic

- `$(( ))` for math—`result=$((a + b))`
- `(( ))` for conditions—`if (( count > 5 )); then`
- No `$` needed inside `$(( ))`—`$((count + 1))` not `$(($count + 1))`

## Common Mistakes

- `[ $var = "value" ]` fails if var empty—use `[ "$var" = "value" ]` or `[[ ]]`
- `if [ -f $file ]` with spaces—always quote: `if [[ -f "$file" ]]`
- `local` in functions—without it, variables are global
- `read` without `-r`—backslashes interpreted as escapes
- `echo` portability—use `printf` for reliable formatting

## 适用边界

**何时用**：编写/调试/审查 Bash 脚本（Linux/macOS/Git Bash）、排查引号/分词/子 shell/退出码问题。

**何时不用**：
- 通用 shell 语义与跨 shell 差异 → 转 `shell__skillhub`；
- PowerShell 脚本 → 转 `powershell__skillhub`、`windows-powershell-environment-rules`；
- Windows 路径/编码/系统集成 → 转 `windows-encoding-rules`；
- 与 AI 代理执行相关的 Bash 可靠性约束 → 转 `bash__skillhub` 上级规则（如 `execution-failure-learning-rules`）。

## 验收清单

- [ ] 头部已加 `set -euo pipefail`（或明确说明为什么不用）
- [ ] 所有变量/数组/命令替换均已加引号
- [ ] 无子 shell 变量丢失（管道内赋值已改用重定向/进程替换）
- [ ] 测试条件用 `[[ ]]`；`read` 带 `-r`
- [ ] 临时文件/资源有 `trap ... EXIT` 清理
- [ ] `bash -n` 通过；空值/空格/特殊字符输入实测正常
