# 需求(story)

# 需求(story)字段说明
## 需求重要字段说明
|字段|说明|
|:----:|:----:|
| id | ID |
| name | 标题 |
| priority | 优先级 |
| priority_label | 优先级 |
| business_value | 业务价值 |
| status | 状态 |
| version | 版本 |
| module | 模块 |
| test_focus | 测试重点 |
| size | 规模 |
| owner | 处理人 |
| cc | 抄送人 |
| creator | 创建人 |
| developer | 开发人员 |
| begin | 预计开始 |
| due | 预计结束 |
| created | 创建时间 |
| modified | 最后修改时间 |
| completed | 完成时间 |
| iteration_id | 迭代 |
| effort | 预估工时 |
| effort_completed | 完成工时 |
| remain | 剩余工时 |
| exceed | 超出工时 |
| category_id | 需求分类 |
| workitem_type_id | 需求类别 |
| release_id | 发布计划 |
| source | 来源 |
| type | 类型 |
| bug_id | 关联的bugID |
| parent_id | 父需求 |
| children_id | 子需求 |
| ancestor_id | 祖先ID |
| description | 详细描述 |
| workspace_id | 项目ID |
| created_from | 创建来源 |
| step | 流程节点 |
| path | 需求位置（到根需求的直系父需求ID组成） |
| level | 需求层级（到根需求的直系父需求数量） |
| templated_id | 模板ID |
| feature | 特性 |
| label | 标签 |
| progress | 进度 |
| is_archived | 是否归档 |
| tech_risk | 技术风险 |
| business_value | 业务价值 |
| flows | 状态流转步骤快照 |
| secret_root_id | 需求保密根节点 |
| progress_manual | 进度（可忽略，已废弃） |
| priority_label | 自定义计划应用名称 |
| custom_field_* | 自定义字段参数，具体字段名通过接口 [获取需求自定义字段配置](/api-doc/API文档/api_reference/story/get_story_custom_fields_settings.html) 获取 |
| custom_plan_field_* | 自定义计划应用参数，具体字段名通过接口 [获取自定义计划应用](/api-doc/API文档/api_reference/iteration/get_plan_apps.html) 获取 |

## 需求优先级(priority)取值字段说明
为了兼容自定义优先级，`请使用 priority_label 字段`，详情参考：[如何兼容自定义优先级](/api-doc/API文档/subject/custom_priority/) 。

## 其他字段
status(状态)/ module(模块)/ iteration_id(迭代) 等字段可选值跟当前项目有关,属于动态可选值, 需要通过接口 [获取需求所有字段及候选值](get_story_fields_info.html)获取.
