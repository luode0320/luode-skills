---
name: python
description: "编写可靠 Python 代码：规避可变默认参数、is/== 陷阱、迭代中修改列表、GIL 与并发、循环导入、浮点精度、编码问题等常见坑。主题索引覆盖类型、集合、函数、类、并发、导入、测试。适用于编写/审查 Python 代码、排查运行时诡异行为（变量共享、列表跳过元素、UnboundLocalError）、编写测试场景。触发词：python、python3、py 脚本、python 报错、可变默认参数、列表迭代修改、循环导入、GIL、asyncio、UnboundLocalError、pytest、类型提示、python 编码、python 陷阱。"
license: MIT
metadata:
  displayName: "Python 可靠编码"
  version: "1.1.0"
  author: "Clawhub Developer"
---

# Python 可靠编码

面向「写出不出错 Python」的实战手册：7 个主题陷阱索引 + 13 条关键规则 + 调试速查。写代码前扫一眼关键规则，出问题时按「调试速查表」定位主题文件。

## 使用流程

1. **编写前**：扫读「关键规则」13 条（覆盖 80% 高频坑）。
2. **编写中**：按主题查索引文件（类型/集合/函数/类/并发/导入/测试）取细节。
3. **调试时**：现象 → 「调试速查表」定位主题 → 读对应规则 → 修正。
4. **收尾**：对照「验收清单」自查后交付。

## 主题索引

| 主题 | 文件 | 覆盖内容 |
|---|---|---|
| 类型 | `types.md` | 动态类型、type hints、`is` vs `==`、浮点、`None` 判断 |
| 集合 | `collections.md` | list/dict/set 陷阱、推导式、迭代中修改 |
| 函数 | `functions.md` | args/kwargs、闭包、装饰器、生成器 |
| 类 | `classes.md` | 继承、`__init__`/`__new__`、描述符、元类、可变类属性 |
| 并发 | `concurrency.md` | GIL、threading、asyncio、multiprocessing |
| 导入 | `imports.md` | 循环导入、包结构、`__init__.py` |
| 测试 | `testing.md` | pytest、mock、fixture |

## 调试速查表

| 现象 | 定位 |
|---|---|
| 函数多次调用结果互相污染 / 默认参数是共享列表 | `types.md` 可变默认参数 |
| `a == b` 成立但 `a is b` 不成立 | `types.md` is vs == |
| 浮点金额对不上（0.1+0.2≠0.3） | `types.md` 浮点 → 用 `decimal.Decimal` |
| 遍历 list 时删元素跳过了下一项 | `collections.md` 迭代中修改 → 遍历副本 |
| 给外层变量赋值报 UnboundLocalError | `functions.md` → `nonlocal`/`global` |
| 多线程跑不满 CPU / 并发结果不对 | `concurrency.md` GIL → CPU 密集用 multiprocessing |
| import 报循环错误 / 模块半初始化 | `imports.md` → 函数内延迟导入 |
| `with open()` 忘关导致句柄泄漏 | 关键规则 → 一律 `with` |
| 读写文件中文乱码 | 关键规则 → 显式 `encoding='utf-8'` |

## 关键规则

- `def f(items=[])` 共享同一列表——用 `items=None` 再 `items = items or []`
- `is` 查身份、`==` 查值——`"a" * 100 is "a" * 100` 可能为 False
- 迭代中修改 list 会跳过元素——遍历副本：`for x in list(items):`
- GIL 阻止 Python 线程真并行——CPU 密集用 multiprocessing
- 裸 `except:` 会吞掉 `SystemExit` 和 `KeyboardInterrupt`——用 `except Exception:`
- 给外层作用域变量赋值报 `UnboundLocalError`——用 `nonlocal` 或 `global`
- `open()` 不用上下文管理器会泄漏句柄——一律 `with open():`
- 循环导入静默失败或部分初始化——函数内导入打断环
- `0.1 + 0.2 != 0.3`——金额用 `decimal.Decimal`
- 生成器一次耗尽——不能复用，重建或用 `itertools.tee`
- 类属性带可变对象会跨实例共享——在 `__init__` 里定义
- `__init__` 不是构造器——`__new__` 创建实例，`__init__` 初始化
- 默认编码随平台——读写文件显式 `encoding='utf-8'`

## 适用边界

**何时用**：编写/审查 Python 代码、排查上述运行时陷阱、设计测试用例。

**何时不用**：
- Python 项目工程结构/目录规范 → 转 `package-structure-rules`；
- 测试程序/模拟程序/数据构造脚本规则 → 转 `test-program-rules`；
- 代码风格与注释规则 → 转 `code-generation-style-rules`、`comment-rules`；
- 数据库/爬虫/框架专属写法 → 转对应领域 skill（`database-query-rules`、`api-contract-rules` 等）。

## 验收清单

- [ ] 无可变默认参数（`def f(x=[])` 类写法）
- [ ] 相等判断用 `==`（身份判断才用 `is`，`None` 判断用 `is None`）
- [ ] 无迭代中修改集合；生成器未被复用
- [ ] 文件操作全部 `with` 上下文管理器且指定 `encoding='utf-8'`
- [ ] 异常捕获用 `except Exception:`（无裸 except）
- [ ] 金额/精度敏感计算用 `decimal`，浮点比较用 `math.isclose()`
