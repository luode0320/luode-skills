# 说明
创建测试计划和需求关联关系


# url
`${TAPD_API_ENDPOINT}/test_plans/create_story_relation`

# 支持格式
JSON/XML（默认JSON格式）

# HTTP请求方式
POST

# 请求数限制
一次最多保存10条需求关联关系

# 请求参数
|字段名|必选|类型及范围|说明|特殊规则|
|:----:|:----:|:----:|:----:|:----:|
| plan_id |  `是` | integer | 测试计划ID | |
| workspace_id | `是` | integer | 项目ID |  |
| story_ids | `是` | integer | 要关联或解除关联的需求ID,最多不超过10条，多个需求ID之间用,分割 |  |
| creator| `是` | string | 创建人 |  |

# 调用示例及返回结果
## 创建测试计划和需求关联关系
### curl 使用 Basic Auth 鉴权调用示例
`curl -u 'api_user:api_password' -d 'plan_id=1010158231077224799&workspace_id=10158231&story_ids=123123123&creator=peter' '${TAPD_API_ENDPOINT}/test_plans/create_story_relation'`

### curl 使用 OAuth Access Token 鉴权调用示例
`curl -H 'Authorization: Bearer ACCESS_TOKEN'  -d 'plan_id=1010158231077224799&workspace_id=10158231&story_ids=123123123&creator=peter' '${TAPD_API_ENDPOINT}/test_plans/create_story_relation'`

### 返回结果
```JSON
{
    "status": 1,
    "data": [],
    "info": "create plan story relation success"
}
```
