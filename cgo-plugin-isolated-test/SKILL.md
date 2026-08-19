---
name: cgo-plugin-isolated-test
description: 在无 C 工具链的 Windows 环境(或任何 CGO_ENABLED=0 环境)下,验证 c-shared Go 插件包(cgo)的逻辑与单元测试。当插件包含 import "C" 的 main.go 导致 go build/go vet/go test 报 undefined 符号或 IgnoredGoFiles 时使用。
agent_created: true
---

# cgo 插件包隔离测试

## 触发场景

- 本地 Windows 无 gcc/mingw(检查:`where gcc` 无结果),插件包含 `import "C"`(c-shared 构建),`CGO_ENABLED=0` 时:
  - `go vet` 报 `undefined: storedAuth` 等符号(main.go 被 IgnoredGoFiles 排除,但它定义的符号被其他文件引用)
  - `go test` 编译失败
- 需要验证不依赖 cgo 的纯逻辑(调度、缓存、路由、配置解析等)

## 首选:cgo-shim-build.py(自动化 shim)

cpa-plugin 仓库已沉淀一键脚本 `scripts/cgo-shim-build.py`,自动完成:复制插件目录
到临时区 → 剥离 main.go 的 cgo preamble 并替换 C.* 引用为 Go 桩 → 追加 shim
类型/函数到文件末尾 → `CGO_ENABLED=0 go build/vet/test`。用法:

```bash
python scripts/cgo-shim-build.py workbuddy            # 全量 build+vet+test
python scripts/cgo-shim-build.py <dir> --no-test --keep   # 跳过 test / 失败保留临时目录
```

脚本内置两条**真实 cgo 构建前置校验**(shim 本身会掩盖这两类错误,CI 才暴露,
2026-08-19 两次踩坑后加入):
- cgo preamble 必须含 `extern int cliproxyPluginCall` / `cliproxyPluginFree` /
  `cliproxyPluginShutdown` 三件套(缺失 → `could not determine what
  C.cliproxyPluginCall refers to`);
- 包内必须存在 `func main()`(`-buildmode=c-shared` 硬性要求,缺失 →
  `function main is undeclared in the main package`;workbuddy/qoderwork 都有
  空 main,新插件别漏)。

## 核心方法:隔离目录 + shim

1. **确认依赖图**:grep 被测试文件的引用符号,确定哪些定义在 cgo 文件(main.go/host_bridge.go)或重依赖文件(cache.go/billing.go/management.go)。

2. **组装隔离目录**:
   ```bash
   mkdir -p <repo>/.test-tmp/<name>   # 建在仓库内,gitignore 需含 .test* 或用完删除
   cp <非cgo源文件> <go.mod> <go.sum> <测试文件> <repo>/.test-tmp/<name>/
   ```

3. **写 shim.go**(`package main`):提供 cgo 文件缺失的最小符号。例如:
   - `const providerName`
   - `envelope`/`okEnvelope`/`errorEnvelope`(若被测代码走 RPC envelope)
   - 被测代码引用的业务类型最小版(只含被测路径用到的字段,如 `creditsSummary{TotalRemain,TotalUsed,TotalSize,Packages}`)
   - 工具函数(如 `isCreditsExhausted`)按真实实现精简复制

4. **写 helpers_test.go**:把原仓库 `*_test.go` 里共用的 helper(`mustMarshal`、`parsePickResponse` 等)在隔离目录补一份(它们定义在被排除的测试文件中)。

5. **跑测试**:
   ```bash
   cd <repo>/.test-tmp/<name> && go mod tidy && go test -v ./...
   ```
   基于 go.mod 锁定的 SDK 版本编译——顺带验证了与线上依赖版本的兼容性。

6. **清理**:`rm -rf <repo>/.test-tmp`(shim 是测试专用,永不入库)。

## 关键坑

- **正则灾难性回溯(DOTALL + 嵌套 `.*`)**:shim 重写 main.go 时
  `(?://.*\n)*` 在 `re.DOTALL` 下对 31KB 文件 2^N 分支爆炸 → python 100% CPU
  死循环(表现像"构建卡死",实际 go 没跑到)。必须用类否定 `(?://[^\n]*\n)*`
  (单行锚定,线性)。任何 DOTALL 正则里的重复组都要警惕。
- **config_yaml 是 base64 传输**:宿主 RPC 层 `ConfigYAML []byte` 经
  encoding/json 序列化为 base64;插件端 `[]byte` 字段反序列化自动 base64 解码。
  测试模拟必须 `json.Marshal(map{"config_yaml": []byte(yaml)})`,直接传字符串会
  "illegal base64 data" 且被 `err == nil` 吞掉、配置静默失效。
- **O_APPEND 句柄不能 Truncate(Windows)**:`os.OpenFile(path, O_APPEND|...)`
  后 `f.Truncate(0)` 报 access denied(FILE_APPEND_DATA ≠ WRITE_DATA)。轮转
  用独立 `os.Truncate(path, 0)` 再开 O_APPEND。
- **零值配置触发 NewTicker(0) panic**:`usagestats.Open(Config{...})` 不补
  默认值,测试必须显式传 FlushInterval/RetentionDays 等,否则
  `time.NewTicker(0)` panic。
- **shim 块放文件末尾**:Go 要求所有 import 在声明之前,shim 的
  type/func 声明必须追加在 import 块之后(不能插在 package main 和 import 之间)。
- **`go test -race` 在无 C 编译器时不可用**(`-race requires cgo`);并发正确性靠锁审查 + 正常测试。
- **gofmt 对 CRLF 文件报 diff 是正常的**:仓库 Windows 下通常是 CRLF,`gofmt -l` 会列出所有仓库旧文件;只需确认自己**新写的文件**不在列表里(`gofmt -l session_auth.go` 无输出 = OK)。
- **语法检查不依赖编译**:`gofmt -e <file>` 可对含 cgo 的文件做纯语法校验。
- **SDK 字段兼容性**:隔离测试用 go.mod 锁定的版本编译,若被测代码用了新 SDK 字段(如 `SchedulerOptions.Headers/Metadata`),直接 `go doc github.com/.../pluginapi.SchedulerOptions` 确认该版本有该字段。
- **git 凭据 helper 卡死**:`credential.helper=helper-selector` 会导致 git push 静默挂起。解决:GIT_ASKPASS 脚本必须放在 **Windows 路径**(Git for Windows 的 git.exe 不认 POSIX `/tmp`),例如 `C:\Users\luode\.github\git-askpass.sh`,内容 `echo "$(cat /c/Users/luode/.github/token | tr -d '\r\n')"`,执行 `GIT_TERMINAL_PROMPT=0 GIT_ASKPASS='C:\...' git -c credential.helper= push origin main`,用完删除脚本。

## 验证清单

- [ ] 隔离目录 `go test ./...` 全绿
- [ ] `gofmt -e` 所有修改文件无语法错误
- [ ] 新文件 `gofmt -l` 不出现(格式干净)
- [ ] 隔离目录已删除
- [ ] 真实 cgo 编译留给 CI(GitHub Actions 有完整 CGO 环境)
