---
schema_version: 1
doc_id: "TEST-RSR-CIT-README-001"
doc_type: "test"
source_ids: ["REQ-RSR-OBS-CITATION-001", "CYCLE-RSR-21-001"]
status: accepted
version: "v1.0"
current_slice: "CYCLE-21 总结知识引用清单"
updated_at: "2026-08-04"
template_version: 1
reader_level: business_general
writing_style: plain_chinese
appendix_policy: preserve_existing_or_one_terminal_appendix
---

# CYCLE-21 总结知识引用清单 测试证据

结论：本周期四项真实测试全部通过，其中规则契约测试 20 项全绿、字典刷新退出码为零、两份研发文档完整性校验通过、知识库实机验证成功读取与写入各一次。影响：证明「知识引用」小节的规则文本已落到位，且引用条目能来自真实知识库调用。范围：规则契约测试、字典生成脚本、文档完整性校验器与知识库桥接实机验证。非范围：根测试目录的全量启动器，它在本周期开始前就已存在既有故障，本轮不修。变化：新增一个契约测试文件，共 20 个用例，覆盖台账、顺序、禁令、模板、样例与编码六组。完成标准：四项测试均有可复核的执行结论，且既有失败项已被证明与本轮无关。术语说明：`契约测试` 指用可执行断言检查规则文本是否写到位的测试；`readback` 指写入笔记后再读回一次以证明确实写进去了。验证状态：全部通过，无受限项。

## 文档信息

| 项目 | 内容 |
|---|---|
| 文档编号 | `TEST-RSR-CIT-README-001` |
| 所属需求 | `REQ-RSR-OBS-CITATION-001` |
| 所属周期 | `CYCLE-RSR-21-001` |
| 覆盖任务 | `T21-01` 至 `T21-05` |
| 执行环境 | Windows Git Bash + 仓库自带 Python 3.11，无数据库、缓存或外部服务 |
| 关联风格回归 | `STYLE-RSR-OBS-CITATION-001` |

## 图片资产决策

图片资产决策：N/A + 原因：本次真实测试只产生命令行文本输出与 JSON 返回，不包含界面、截图或视觉验收对象 + 证据：`doc/data/images/` 下无本任务图片引用。

## 测试资产落点

| 资产 | 路径 | 说明 |
|---|---|---|
| 规则契约测试 | `test/reasoning-summary-structure-rules/obsidian_citation_contract_test.py` | 唯一新增可执行测试，按被测 Skill 名镜像到根 `test/` |
| 本目录 | `doc/5-tests/2026-08-04_202349_总结知识引用清单/` | 只保存本 README 与执行结论，不含任何可执行资产 |

## 执行结论

| 测试 ID | 入口 | 结果 | 关键数字 |
|---|---|---|---|
| `TEST-RSR-CIT-DOC` | 文档完整性校验器 requirement 与 implementation_cycle 两档 | 通过 | 两档均 `valid=True`、`error_codes=[]` |
| `TEST-RSR-CIT-001` | `python -X utf8 -m unittest discover -s test/reasoning-summary-structure-rules -p "*_test.py"` | 通过 | `Ran 20 tests` 全绿，0 failed |
| `TEST-RSR-CIT-002` | `python skill-dictionary/generate_dictionary.py` | 通过 | 退出码 0；`implemented_total 69`、`planned_missing 2`、`seed_total 34`；两个生成物已更新且含新口径 |
| `TEST-RSR-CIT-003` | 知识库桥接自检、检索、读取与创建 | 通过 | `doctor ok=true`、`read` 与 `create` 均 `verified=true`、`attempts=1` |

## 通过标准

| 项目 | 内容 |
|---|---|
| 契约测试 | 20 个用例全部通过，0 failed、0 error |
| 字典刷新 | 脚本退出码 0，两个生成物已更新且含新引用清单口径 |
| 文档校验 | requirement、implementation_cycle、test、style_regression 四档均 `valid=True` |
| 实机验证 | 桥接自检、读取与创建三类调用均返回 `verified=true` |
| 环境阻断 | N/A + 原因：本次测试不需要数据库、缓存或外部服务 + 证据：契约测试只读仓库内文本，实机验证只使用本地知识库 |
| 既有失败项 | 必须被证明与本轮无关，否则不得判定通过 |

## 契约测试用例分组

| 组 | 用例数 | 覆盖内容 |
|---|---|---|
| 台账组 | 6 | 六字段定义、立即登记、未读取不得入表、禁用 CLI 回显、会话内事实边界、技能入口 |
| 顺序组 | 6 | 知识引用在改动点之后、阻断收口仍最后、末尾按台账分流、自检可回指要求、条件判定与通过驳回标准、小节图标登记 |
| 禁令组 | 2 | 八条旧口径在七份规则文件中均已移除、结果区不再承载 Obsidian 摘要行 |
| 模板组 | 3 | 模板两张表固定表头、结构要求含新固定顺序、条件规则第 5 节为知识引用 |
| 样例组 | 2 | 正例含引用小节且位于改动点之后、反例覆盖「未读取却列入引用」 |
| 编码组 | 1 | 七份规则文件均为可解码 UTF-8 且无 NUL 字节 |

## 实机验证细节

| 步骤 | 命令 | 返回 |
|---|---|---|
| 自检 | `doctor --json` | `ok=true`、`vault_root=D:\obsidian_data`、`vault_selector=obsidian_data`、`verified=true`、CLI 版本 1.13.4（安装版 1.12.7） |
| 检索 | `search --query "obsidian cli"` 等三次 | 命中路径回显中文乱码，印证笔记名必须取自本地 path 字符串 |
| 读取 | `read --path "知识库/INDEX.md"` | `verified=true`；frontmatter 含 `title` 与 `status: active`，证明状态列可从 frontmatter 取值 |
| 写入 | `create --path "知识库/20-Knowledge/obsidian-cli/官方CLI回显编码限制.md"` | `ok=true`、`verified=true`、`attempts=1` |

实机验证只覆盖「台账非空时输出引用小节」这一条分支。「台账为空时整节省略」在本轮无法实机构造，改由契约测试的条件判定与模板结构断言锁定，不宣称已实机验证。

## 既有失败项说明

根测试启动器 `test/run_python_tests.py` 与另外两个既有测试文件在本周期开始前就已失败，与本轮改动无关，已通过回退到干净基线复跑证明：

| 项目 | 现象 | 基线复跑结论 |
|---|---|---|
| `test/run_python_tests.py` | 在既有目录 `test/artifact-delivery-gate-rules` 上抛 `ImportError: Start directory is not importable` | 移除本轮新增测试目录后仍失败，故障点为既有目录 |
| `test/artifact-delivery-gate-rules/validate_engineering_docs_test.py` | 1 failure + 1 error，failure 原因为历史 fixture 指向 `../7-验收/` 的链接已失效 | 干净基线复跑同样 `FAILED (failures=1, errors=1)` |
| `test/test-asset-governance/asset_location_test.py` | 1 failure，原因为 `doc/5-tests/` 历史可执行资产指纹与基线清单不一致 | 干净基线复跑同样 `FAILED (failures=1)`；本轮未改动 `doc/5-tests/` 下任何可执行资产 |

逐文件运行根 `test/` 全部测试的结果为 14 个文件通过、2 个文件失败，两个失败项即上表后两项。

## 清理与提交状态

| 项目 | 内容 |
|---|---|
| 临时文件 | 实机验证与基线复核使用的临时文件已全部删除，`D:\tmp` 下无残留 |
| 知识库写入 | 新增一篇知识笔记，属于本轮真实沉淀，保留在知识库内 |
| 工作树 | 停在已改动未提交状态，本轮未执行任何写入版本历史的动作 |
