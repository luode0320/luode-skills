# Go 陷阱速查清单

> 本文件是 golang-patterns 的陷阱清单（checklist），与 SKILL.md 正文互补：正文承载「推荐写法/模式」，本文件只承载「容易踩的坑、会导致线上事故或难排查 bug 的写法」。
> 来源：吸收自 skillhub 市场 `go` skill v1.0.2（2026-08-22 吸收），已修订 Go 1.22 循环变量语义、统一中文表达、删除与本地已有规则重复的条目（errors.Is/As、%w 包装、strings.Builder、panic 保护等见 SKILL.md 正文）。

## 1. Goroutine 与并发

- goroutine 阻塞在无 sender/receiver 的 channel 上 = 永久泄漏；泄漏的 goroutine 只累积内存、永不回收。启动 goroutine 前先想清退出条件。
- **无法从外部杀死 goroutine**，只能靠 context 取消或 channel close 协作退出；写 `go func()` 时必须保证循环体内检查 `ctx.Done()` 或接收方最终会 close。
- `for range ch` 会一直循环直到 channel 被 close——sender 必须负责 `close(ch)`，否则接收 goroutine 泄漏。
- context 取消不会自动停止 goroutine：`context.WithCancel` 之后必须真正在 goroutine 里 `select` 或检查 `ctx.Done()`，否则取消是空操作。
- 循环变量捕获（Go 1.22 之前）：`go func() { fmt.Println(i) }()` 在循环内捕获的是同一个变量，全部 goroutine 读到最终值；Go 1.22+ 的 `for range` 每次迭代已是新变量、不再有此问题。若项目仍兼容 Go < 1.22，必须显式传参：`go func(i int) { ... }(i)`。
- 原子读 + 原子写 ≠ 原子读-改-写：需要 `counter.AddInt64(1)` 这类原子操作，不要用「先 Load 再 Store」拼凑。
- `atomic.Value` 的 Store 必须始终存同一种具体类型，混存不同类型会 panic。
- 生产代码不要留 `context.TODO()`——它没有取消能力，上线前必须替换为真实 context。
- context value 用自定义类型作 key（`type ctxKey string`），不要用裸 string 作 key，类型错了会静默变成 nil。

## 2. Channel

- 向 nil channel 发送永久阻塞，从 nil channel 接收也永久阻塞；`var ch chan int` 未 make 就使用是经典死锁来源。
- 向已 close 的 channel 发送会 panic；重复 close 同一个 channel 也会 panic。
- **只有 sender 应该 close channel**——receiver 负责 close 会导致 sender panic。
- 无缓冲 channel 是同步点：send 会阻塞直到有 receiver。不是"异步队列"。
- 带缓冲 channel 满了 send 照样阻塞；buffer size 1 不等于异步，容量要按预期负载设计。
- `select` 多个 case 同时 ready 时**随机**选择一个，不是先写的先执行；不要依赖 case 顺序。
- 空 `select {}` 永久阻塞（可用于阻塞 main），`default` 分支让 select 变成非阻塞——注意别写出空转 busy loop。
- 把 nil channel 放进 select 会被忽略，可用于「临时禁用某个 case」。

## 3. Defer

- defer 参数**立即求值**：`defer log(time.Now())` 记下的是 defer 语句执行时刻，不是函数返回时刻；需要延迟取值就包一层闭包 `defer func() { log(time.Now()) }()`。
- defer 在循环里会累积到函数结束才执行，循环量大时堆积资源；需要每轮释放的逻辑放函数内子块或抽成函数。
- defer 在 panic 时也会执行（适合清理），但 `recover()` 只在 deferred 函数内有效，且只能恢复**当前 goroutine** 的 panic。
- 命名返回值可在 defer 里修改：`defer func() { err = wrap(err) }()` 是给错误补上下文的常见写法。
- defer 按 LIFO 执行：最后 defer 的最先运行；`defer mu.Unlock()` 要写在 `Lock()` 之后紧邻的位置，不要在两者之间插入可能提前 return 的逻辑。
- lock/unlock 必须在同一个函数内成对出现；不要把已加锁的 mutex 传给其他函数，也不要复制含 mutex 的 struct（复制的是未上锁的副本）。

## 4. 接口与类型系统

- **nil 具体值放进接口 ≠ nil 接口**：`var p *MyType = nil; var i any = p` 之后 `i != nil` 为 true。接口为 nil 当且仅当 type 和 value **同时**为 nil。返回 nil 指针作为接口返回值的函数，调用方 `if err == nil` 判断会失效（典型错误处理坑）。
- 类型断言不用 comma-ok 会 panic：`s := i.(string)` 在类型不符时崩溃；一律写 `s, ok := i.(string)`。
- 接口满足是隐式的：方法签名漂移不会产生编译错误，改方法时对照接口声明检查。
- 指针接收者的方法集：`*T` 拥有全部方法，值 `T` 没有指针接收者方法；把值类型传入要求接口的地方可能编译失败或行为意外。
- 空接口 `any` 接受一切但丢失类型安全；能避免就避免，需要时配合类型断言/type switch。
- 断言到接口检查的是方法集而非底层类型；type switch 不能直接匹配泛型类型参数，需要时用 reflect。
- 嵌入 nil 指针会「暴露」一堆调用即 panic 的方法——嵌入前确认被嵌入值非 nil。
- 遮蔽嵌入方法（shadowing）是静默的，没有覆盖警告；改名时容易无意遮蔽父方法。
- 嵌入指向接口的指针几乎总是错误设计。
- 接口方法超过 10 个 = 几乎没人能实现，拆成小接口组合。
- 返回接口会隐藏具体类型的方法，调用方需要断言才能用——返回具体类型，入参用接口。

## 5. 错误处理（Go 专属机制）

- 哨兵错误必须定义一次：`var ErrNotFound = errors.New("not found")`；在函数里每次 `errors.New()` 都是新实例，`==` 永远不相等。
- 哨兵错误被 `%w` 包装后 `==` 比较失效，必须用 `errors.Is(err, ErrNotFound)` 沿链判断。
- `errors.As(err, &target)` 需要传**指向目标类型的指针**（`&target` 本身得是指针变量的地址）。
- 自定义错误类型用指针接收者：`type MyError struct{...}; func (e *MyError) Error() string`，错误值应为 `*MyError` 而非 `MyError`（否则 `errors.As` 无法匹配）。
- 实现 `Unwrap() error` 才能让 `errors.Is/As` 穿透你的自定义包装；忘了实现链条就断。
- 函数返回值 `val, err := f()`：`err != nil` 时 `val` 可能仍有效（如部分读取），按文档语义处理，不要默认丢弃或默认可用。
- `log.Fatal` 内部调用 `os.Exit(1)`，**defer 不会执行**、缓冲不刷新；需要清理时用 `log.Print` + `return` 或显式清理后再退出。
- panic 只会崩当前 goroutine 所在程序；goroutine 内的 panic 要就地 recover（见 SKILL.md 正文 panic 保护规则），不要指望外层兜底。

## 6. Slice

- 切片是底层数组的引用：`b := a[1:3]` 不复制数据，修改 b 会影响 a。
- `append` 可能重新分配也可能原地追加，**永远不要假设容量**；需要保证独立就显式复制。
- 大 slice 切片出小片段后，底层大数组仍被引用、无法回收——提取小片段用 `append([]T{}, big[1:3]...)` 或 `copy`。
- `copy(dst, src)` 复制 min(两长度) 个元素，不会扩展 dst；先 `make` 足够容量。
- nil slice（`var s []int`）与 empty slice（`s := []int{}`）不同：nil slice 可安全 append/len 为 0，但 JSON 序列化结果不同（nil→null，empty→[]）。
- `clear(s)` 只把元素归零/置空并**保持长度**，不是清空；要清空用 `s = s[:0]`。
- 切片传给函数共享内存，函数内的修改对调用方可见——不期望被改就传副本。

## 7. Map

- 读 nil map 返回零值（不报错），**写 nil map 会 panic**；`var m map[string]int` 未 make 就写入是崩溃来源。
- 迭代顺序随机，不要依赖遍历顺序；需要有序就显式排序 key。
- map 并发读写不安全，会直接 panic（concurrent map writes）；需要并发访问用 `sync.Map` 或加锁。
- `&m[key]` 不允许编译——map 元素不可寻址，要修改就整体赋值或存指针。
- 迭代中 delete 是安全的，但**新增**元素可能被跳过或重复访问。

## 8. String

- string 是不可变字节序列，每次拼接产生新分配；循环里 `s += x` 是 O(n²)，用 `strings.Builder`（见 SKILL.md 正文）。
- `range` 字符串迭代的是 rune 不是字节，多字节字符（中文）会让索引跳变；按字节遍历用 `s[i]`。
- `len(s)` 返回**字节数**不是字符数，字符数用 `utf8.RuneCountInString(s)`。
- 字符串比较是逐字节比较，不是 Unicode 规范化比较；同义字（如 NFC/NFD）比较不相等。
- 子串 `s[1:3]` 共享底层内存，大字符串取小片段会撑住整块内存；需要独立用小片段就 `strings.Clone` 或复制。
- `string(65)` 得到的是字节 65 对应的字符 "A"，不是 "65"；十进制转换用 `strconv.Itoa(65)`。

## 9. 结构体与内存

- 结构体字段按对齐 padding，字段顺序影响内存大小；热路径大结构体按「大字段在前/同类相邻」排布可减少 padding。
- 复制带 mutex 的 struct 会复制未上锁的副本（vet 会报 copylocks）；含锁/原子字段的类型一律传指针。
- embedding 不是继承：被提升的方法可能被遮蔽（shadowing），且没有「override 警告」。
- 导出字段首字母大写，小写字段在包外不可见——序列化（json/yaml）只认导出字段。

## 10. 构建与工具链

- 未使用的 import 直接编译失败；只为副作用导入用 `_ "package/path"`。
- `init()` 执行顺序按依赖关系而非文件顺序，多个 init 的先后不易直觉判断；不要在 init 里做需要确定顺序的工作（见 SKILL.md 正文「避免包级可变状态」）。
- `go:embed` 路径相对**源文件所在目录**，不是工作目录；跨目录嵌入要写相对路径并注意通配符行为。
- 交叉编译 `GOOS=linux GOARCH=amd64 go build` 很容易，但必须在目标平台真实跑过（尤其 CGO 依赖）。

---

## 使用建议

- 编码/评审 Go 代码时，把本清单当「上线前检查表」逐类过一遍，重点看 1（goroutine 泄漏）、4（nil interface）、5（错误链）三类——这三类是线上事故和难排查 bug 的高发区。
- 与 SKILL.md 正文配合：正文讲「怎么写对」，本清单讲「哪里会写错」；两者冲突时以正文规则为准。
