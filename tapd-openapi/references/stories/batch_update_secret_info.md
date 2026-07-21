# 说明
批量修改需求的保密信息


# url
`${TAPD_API_ENDPOINT}/stories/batch_update_secret_info`

# 支持格式
JSON/XML（默认JSON格式）

#  HTTP请求方式
POST

# 请求数限制
当一次修改涉及20个及以上的需求时，会触发后台异步执行，不会立即生效。

# 请求参数
|字段名|必选|类型及范围|说明|
|:----:|:----:|:----:|:----:|
| workspace_id | `是` | integer | 项目ID |
| story_id_list | `是` | string | 所需修改的需求id列表, 用"\|"隔开多个 |
| secret_scope | `是` | string | 修改后的保密状态(public:设置为公开 \| secret:设置为保密) |
| allow_list | `是` | string | 保密白名单(支持填入用户nick和用户组id), 用";"隔开多个 |
| add_participant_fields | `是` | string | 是否将需求树的参与人动态纳入到保密范围内 (true:纳入\|false:不纳入) |
| operation_type | `否` | integer | 保密范围(上述allow_list)的操作模式(0:默认模式/覆盖模式, 用传入的新名单覆盖旧名单 \| 1:新增模式, 在旧名单基础上进行新增此次传入的名单 \| 2:删除模式, 从旧名单里删除此次传入的名单) |
| current_user | `是` | string | 执行此操作的用户的nick |


# 调用示例及返回结果
## 修改需求1010104801871430407和1010104801871430409的保密信息
### curl 使用 Basic Auth 鉴权调用示例
`curl -u 'api_user:api_password' -d 'workspace_id=10104801&story_id_list=1010104801871430407|1010104801871430409&secret_scope=secret&allow_list=xinweihe;1000000000000000002&add_participant_fields=false&operation_type=0&current_user=xinweihe' '${TAPD_API_ENDPOINT}/stories/batch_update_secret_info'`
### curl 使用 OAuth Access Token 鉴权调用示例
`curl -H 'Authorization: Bearer ACCESS_TOKEN' -d 'workspace_id=10104801&story_id_list=1010104801871430407|1010104801871430409&secret_scope=secret&allow_list=xinweihe;1000000000000000002&add_participant_fields=false&operation_type=0&current_user=xinweihe' '${TAPD_API_ENDPOINT}/stories/batch_update_secret_info'`

### 返回结果
```JSON
{
    "status": 1,
    "data": {
        "code": "succeed",
        "msg": "需求可访问人员设置成功"
    },
    "info": "success"
}
```
