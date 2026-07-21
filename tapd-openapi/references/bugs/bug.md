# 缺陷(bug)

# 缺陷(bug)字段说明
## 缺陷重要字段说明
|字段|说明|
|:----:|:----:|
| id | ID |
| title | 标题 |
| priority | 优先级 |
| priority_label | 优先级 |
| severity | 严重程度 |
| status | 状态 |
| iteration_id | 迭代 |
| module | 模块 |
| feature | 特性 |
| release_id | 发布计划 |
| version_report | 发现版本 |
| version_test | 验证版本 |
| version_fix | 合入版本 |
| version_close | 关闭版本 |
| baseline_find | 发现基线 |
| baseline_join | 合入基线 |
| baseline_test | 验证基线  |
| baseline_close | 关闭基线 |
| current_owner | 处理人 |
| cc | 抄送人 |
| reporter | 创建人 |
| participator | 参与人 |
| te | 测试人员 |
| de | 开发人员 |
| auditer | 审核人 |
| confirmer | 验证人 |
| fixer | 修复人 |
| closer | 关闭人 |
| lastmodify | 最后修改人 |
| size | 规模 |
| created | 创建时间 |
| in_progress_time | 接受处理时间  |
| resolved | 解决时间 |
| verify_time | 验证时间 |
| closed | 关闭时间 |
| reject_time | 拒绝时间 |
| modified | 最后修改时间 |
| begin | 预计开始 |
| due | 预计结束 |
| deadline | 解决期限 |
| os | 操作系统 |
| platform | 软件平台 |
| testmode | 测试方式 |
| testphase | 测试阶段 |
| testtype | 测试类型 |
| source | 缺陷根源 |
| bugtype | 缺陷类型 |
| issue_id | 问题ID |
| frequency | 重现规律 |
| originphase | 发现阶段 |
| sourcephase | 引入阶段   |
| resolution | 解决方法 |
| estimate | 预计解决时间 |
| description | 详细描述 |
| workspace_id | 项目ID |
| effort | 预估工时 |
| effort_completed | 完成工时 |
| remain | 剩余工时 |
| exceed | 超出工时 |


# 常用字段候选值映射
## 缺陷优先级(priority)字段说明
为了兼容自定义优先级，`请使用 priority_label 字段`，详情参考：[如何兼容自定义优先级](/api-doc/API文档/subject/custom_priority/) 。`下面取值将不再使用`。

|取值|字面值|
|:----:|:----:|
| urgent | 紧急 |
| high | 高 |
| medium | 中 |
| low | 低 |
| insignificant | 无关紧要 |

## 缺陷严重程度(severity)字段说明
|取值|字面值|
|:----:|:----:|
| fatal | 致命 |
| serious | 严重 |
| normal | 一般 |
| prompt | 提示 |
| advice | 建议 |

## 缺陷解决方法(resolution)字段说明
|取值|字面值|
|:----:|:----:|
| ignore | 无需解决 |
| fix | 延期解决 |
| failed | 无法重现 |
| external | 外部原因 |
| duplicated | 重复 |
| intentional | 设计如此 |
| unclear | 问题描述不准确 |
| hold | 挂起 |
| feature | 需求变更 |
| fixed | 已解决 |
| transferred to story | 已转需求 |


## 其他字段
status(状态)/ module(模块)/ iteration_id(迭代) 等字段可选值跟当前项目有关,属于动态可选值, 需要通过接口 [获取缺陷所有字段及候选值](get_bug_fields_info.html)获取.
