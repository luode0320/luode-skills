# 说明
使用并行工作流的需求，获取其节点信息


# url
`${TAPD_API_ENDPOINT}/stories/get_story_step_list`

# 支持格式
JSON/XML（默认JSON格式）

# HTTP请求方式
GET

# 请求数限制
获取指定需求的所有节点列表

# 请求参数
|     字段名      |必选|类型及范围|说明|特殊规则|
|:------------:|:----:|:----:|:----:|:----:|
|   story_id   | `是`  | integer | 需求ID | |
| workspace_id | `是` | integer | 项目ID |  |

# 调用示例及返回结果
## 获取项目下需求
### curl 使用 Basic Auth 鉴权调用示例
`curl -u 'api_user:api_password'  '${TAPD_API_ENDPOINT}/stories/get_story_step_list?workspace_id=70002667&story_id=1070002667006658827'`

### curl 使用 OAuth Access Token 鉴权调用示例
`curl -H 'Authorization: Bearer ACCESS_TOKEN'  '${TAPD_API_ENDPOINT}/stories?workspace_id=10158231/get_story_step_list?workspace_id=70002667&story_id=1070002667006658827'`

### 返回结果
```JSON
{
  "status": 1,
  "data": [
    {
      "WorkitemStepInfo": {
        "id": "1070002667000137213",
        "workspace_id": "70002667",
        "entity_type": "story",
        "workitem_id": "1070002667006658827",
        "step": "step_2970811_1",
        "status": "0",
        "owner": "",
        "begin": null,
        "due": null,
        "effort": "3",
        "iteration_id": "0",
        "begin_time": "2026-01-04 09:37:57",
        "complete_time": "2026-01-04 09:38:23",
        "time_cost": "26",
        "completer": "ocenhu"
      }
    }
  ],
  "info": "success"
}
```
## 字段说明
|字段|    说明    |
|:----:|:--------:|
| step |   节点原名   |
| status |   节点状态   |
| owner |  节点负责人   |
| begin |  节点预计开始  |
| due | 节点预计结束时间 |
| effort |  节点预估工时  |
| iteration_id |   节点迭代   |
| begin_time |   实际开始时间   |
| complete_time |  实际完成时间   |
| time_cost |   节点停留时长   |
| completer |   操作完成人   |
