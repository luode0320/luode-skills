# 说明
返回需求所有字段的中英文


# url
`${TAPD_API_ENDPOINT}/stories/get_fields_lable`

# 支持格式
JSON/XML（默认JSON格式）

# HTTP请求方式
GET

# 请求数限制
默认返回所有数据

# 请求参数
|字段名|必选|类型及范围|说明|特殊规则|
|:----:|:----:|:----:|:----:|:----:|
| workspace_id | `是` | integer | 项目ID |  |

# 调用示例及返回结果
## 获取项目下的需求字段
### curl 使用 Basic Auth 鉴权调用示例
`curl -u 'api_user:api_password'  '${TAPD_API_ENDPOINT}/stories/get_fields_lable?workspace_id=10104801'`

### curl 使用 OAuth Access Token 鉴权调用示例
`curl -H 'Authorization: Bearer ACCESS_TOKEN'  '${TAPD_API_ENDPOINT}/stories/get_fields_lable?workspace_id=10104801'`

### 返回结果
```JSON
{
    "status": 1,
    "data": {
        "id": "ID",
        "name": "标题",
        "label": "标签",
        "priority": "优先级",
        "business_value": "业务价值",
        "status": "状态",
        "version": "版本",
        "module": "模块",
        "test_focus": "测试重点",
        "size": "规模",
        "custom_plan_field_1": "超级迭代",
        "custom_plan_field_2": "发布计划",
        "custom_plan_field_3": "ABC计划",
        "owner": "处理人",
        "cc": "抄送人",
        "creator": "创建人",
        "developer": "开发人员",
        "begin": "预计开始",
        "due": "预计结束",
        "created": "创建时间",
        "modified": "最后修改时间",
        "completed": "完成时间",
        "iteration_id": "迭代",
        "feature": "特性",
        "effort": "预估工时",
        "effort_completed": "完成工时",
        "remain": "剩余工时",
        "exceed": "超出工时",
        "progress": "进度",
        "category_id": "分类",
        "workitem_type_id": "需求类别",
        "parent_id": "父需求",
        "children_id": "子需求",
        "source": "需求来源",
        "type": "需求类型",
        "tech_risk": "技术风险",
        "workspace_id": "所属项目",
        "custom_field_50": "客户联系方式",
        "custom_field_49": "反馈量（一线）",
        "custom_field_48": "产品分类",
        "custom_field_one": "atime",
        "custom_field_three": "进度情况",
        "custom_field_four": "联动层级多选项目",
        "custom_field_five": "^^^3###$%Q@\"'",
        "custom_field_six": "123",
        "custom_field_seven": "下拉测试",
        "custom_field_eight": "测试人名",
        "custom_field_9": "计划上线日期",
        "custom_field_10": "实际开始",
        "custom_field_11": "实际结束",
        "custom_field_12": "排序",
        "custom_field_13": "需求提出人",
        "custom_field_14": "测试人员",
        "custom_field_15": "是否免测",
        "custom_field_16": "是否紧急需求",
        "custom_field_18": "API创建",
        "custom_field_19": "附件测试",
        "custom_field_17": "联动字段测试",
        "description": "详细描述",
        "priority_label": "优先级",
        "release_id": "发布计划"
    },
    "info": "success"
}
```
