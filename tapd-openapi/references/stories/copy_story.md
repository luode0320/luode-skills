# 说明
复制需求，返回新建需求的数据


# url
`${TAPD_API_ENDPOINT}/stories/copy_story`

# 支持格式
JSON/XML（默认JSON格式）

#  HTTP 请求方式
POST

# 请求数限制
- 一次复制一条需求
- 同步复制支持的字段：name(标题)、 status(状态)、 description(详细描述)、 attachment(附件)、begin_due(预计开始结束时间)、 module(模块)、 feature(特性)、 priority(优先级)、 owner(处理人)、 developer(开发人员)、 business_value(业务价值)、 size(规模)、 effort(Estimated effort)、 cc(抄送人)、 test_focus(测试重点)、 version(版本)、 label(标签)、 tech_risk(技术风险)、 iteration_id(迭代)、 comments(评论)、 custom_field::字段中文名

# 请求参数
|字段名|必选|类型及范围|说明|
|:----:|:----:|:----:|:----:|
| workspace_id | `是` | integer | 源项目ID |
| src_story_id |  `是`  | integer | 源需求ID |
| dst_workspace_id |  `是`  | integer | 目标项目ID |
| sync_fields |  否 | string | 需要同步的字段。多写使用 , 分隔 |
| dst_workitem_type_id | 否 | integer | 目标需求类别ID |
| new_creator |  否  | string | 新需求创建人 |
| new_status |  否  | string | 新需求状态 |

# 调用示例及返回结果
## 复制需求到另外项目
### curl 使用 Basic Auth 鉴权调用示例
`curl -u 'api_user:api_password' -d 'workspace_id=10104801&src_story_id=1010104801854843773&dst_workspace_id=755' '${TAPD_API_ENDPOINT}/stories/copy_story'`

### curl 使用 OAuth Access Token 鉴权调用示例
`curl -H 'Authorization: Bearer ACCESS_TOKEN' -d 'workspace_id=10104801&src_story_id=1010104801854843773&dst_workspace_id=755' '${TAPD_API_ENDPOINT}/stories/copy_story'`

### 返回结果
```json
{
    "status": 1,
    "data": {
        "Story": {
            "id": "1000000755854845111",
            "workitem_type_id": "1000000755000000003",
            "name": "bbbbbbbb",
            "description": "<p><b><span style=\"color: #ff0000;\">作为</span></b>&nbsp;</p>\n<div>&nbsp;\n<div>\n<div><b><span style=\"color: #ff0000;\">我希望</span></b>&nbsp;</div>\n<div></div>\n<div><b><span style=\"color: #ff0000;\">以便</span></b> ADFADFADF</div>\n<div></div>\n<div>【验收标准】</div>\n<div>1、</div>\n<div>2、</div>\n<div>3、</div>\n<div>ADFADFDFDAADFFADS</div>\n</div>\n</div>",
            "workspace_id": "755",
            "creator": "anyechen",
            "created": "2020-12-09 17:00:09",
            "modified": "2020-12-09 17:00:10",
            "status": "planning",
            "owner": "",
            "cc": "",
            "begin": null,
            "due": null,
            "size": "0",
            "priority": "",
            "developer": "",
            "iteration_id": "0",
            "test_focus": "",
            "type": "",
            "source": "",
            "module": "",
            "version": "",
            "completed": null,
            "category_id": "-1",
            "path": "1000000755854845111",
            "parent_id": "0",
            "children_id": "|",
            "ancestor_id": "1000000755854845111",
            "business_value": null,
            "effort": "0",
            "effort_completed": "0",
            "exceed": "0",
            "remain": "0",
            "release_id": "0",
            "custom_field_one": null,
            "custom_field_two": null,
            "custom_field_three": null,
            "custom_field_four": null,
            "custom_field_five": null,
            "custom_field_six": null,
            "custom_field_seven": null,
            "custom_field_eight": null,
            "custom_field_9": "",
            "custom_field_10": "",
            "custom_field_11": "",
            "custom_field_12": "",
            "custom_field_13": "",
            "custom_field_14": "",
            "custom_field_15": "",
            "custom_field_16": "",
            "custom_field_17": "",
            "custom_field_18": "",
            "custom_field_19": "",
            "custom_field_20": "",
            "custom_field_21": "",
            "custom_field_22": "",
            "custom_field_23": "",
            "custom_field_24": "",
            "custom_field_25": "",
            "custom_field_26": "",
            "custom_field_27": "",
            "custom_field_28": "",
            "custom_field_29": "",
            "custom_field_30": "",
            "custom_field_31": "",
            "custom_field_32": "",
            "custom_field_33": "",
            "custom_field_34": "",
            "custom_field_35": "",
            "custom_field_36": "",
            "custom_field_37": "",
            "custom_field_38": "",
            "custom_field_39": "",
            "custom_field_40": "",
            "custom_field_41": "",
            "custom_field_42": "",
            "custom_field_43": "",
            "custom_field_44": "",
            "custom_field_45": "",
            "custom_field_46": "",
            "custom_field_47": "",
            "custom_field_48": "",
            "custom_field_49": "",
            "custom_field_50": "",
            "custom_field_51": "",
            "custom_field_52": "",
            "custom_field_53": "",
            "custom_field_54": "",
            "custom_field_55": "",
            "custom_field_56": "",
            "custom_field_57": "",
            "custom_field_58": "",
            "custom_field_59": "",
            "custom_field_60": "",
            "custom_field_61": "",
            "custom_field_62": "",
            "custom_field_63": "",
            "custom_field_64": "",
            "custom_field_65": "",
            "custom_field_66": "",
            "custom_field_67": "",
            "custom_field_68": "",
            "custom_field_69": "",
            "custom_field_70": "",
            "custom_field_71": "",
            "custom_field_72": "",
            "custom_field_73": "",
            "custom_field_74": "",
            "custom_field_75": "",
            "custom_field_76": "",
            "custom_field_77": "",
            "custom_field_78": "",
            "custom_field_79": "",
            "custom_field_80": "",
            "custom_field_81": "",
            "custom_field_82": "",
            "custom_field_83": "",
            "custom_field_84": "",
            "custom_field_85": "",
            "custom_field_86": "",
            "custom_field_87": "",
            "custom_field_88": "",
            "custom_field_89": "",
            "custom_field_90": "",
            "custom_field_91": "",
            "custom_field_92": "",
            "custom_field_93": "",
            "custom_field_94": "",
            "custom_field_95": "",
            "custom_field_96": "",
            "custom_field_97": "",
            "custom_field_98": "",
            "custom_field_99": "",
            "custom_field_100": ""
        }
    },
    "info": "success"
}
```

## 同步复制需求到另外项目，同时设置状态、详细字段为同步字段
### curl 使用 Basic Auth 鉴权调用示例
`curl -u 'api_user:api_password' -d 'workspace_id=10104801&src_story_id=1010104801854843773&dst_workspace_id=755&sync_fields=description,status,owner' '${TAPD_API_ENDPOINT}/stories/copy_story'`

### curl 使用 OAuth Access Token 鉴权调用示例
`curl -H 'Authorization: Bearer ACCESS_TOKEN' -d 'workspace_id=10104801&src_story_id=1010104801854843773&dst_workspace_id=755&sync_fields=description,status,owner' '${TAPD_API_ENDPOINT}/stories/copy_story'`

### 返回结果
```json
{
    "status": 1,
    "data": {
        "Story": {
            "id": "1000000755854845109",
            "workitem_type_id": "1000000755000000003",
            "name": "bbbbbbbb",
            "description": "<p><b><span style=\"color: #ff0000;\">作为</span></b>&nbsp;</p>\n<div>&nbsp;\n<div>\n<div><b><span style=\"color: #ff0000;\">我希望</span></b>&nbsp;</div>\n<div></div>\n<div><b><span style=\"color: #ff0000;\">以便</span></b> ADFADFADF</div>\n<div></div>\n<div>【验收标准】</div>\n<div>1、</div>\n<div>2、</div>\n<div>3、</div>\n<div>ADFADFDFDAADFFADS</div>\n</div>\n</div>",
            "workspace_id": "755",
            "creator": "anyechen",
            "created": "2020-12-09 16:49:47",
            "modified": "2020-12-09 16:49:47",
            "status": "planning",
            "owner": "",
            "cc": "",
            "begin": null,
            "due": null,
            "size": "0",
            "priority": "",
            "developer": "",
            "iteration_id": "0",
            "test_focus": "",
            "type": "",
            "source": "",
            "module": "",
            "version": "",
            "completed": null,
            "category_id": "-1",
            "path": "1000000755854845109",
            "parent_id": "0",
            "children_id": "|",
            "ancestor_id": "1000000755854845109",
            "business_value": null,
            "effort": "0",
            "effort_completed": "0",
            "exceed": "0",
            "remain": "0",
            "release_id": "0",
            "custom_field_one": null,
            "custom_field_two": null,
            "custom_field_three": null,
            "custom_field_four": null,
            "custom_field_five": null,
            "custom_field_six": null,
            "custom_field_seven": null,
            "custom_field_eight": null,
            "custom_field_9": "",
            "custom_field_10": "",
            "custom_field_11": "",
            "custom_field_12": "",
            "custom_field_13": "",
            "custom_field_14": "",
            "custom_field_15": "",
            "custom_field_16": "",
            "custom_field_17": "",
            "custom_field_18": "",
            "custom_field_19": "",
            "custom_field_20": "",
            "custom_field_21": "",
            "custom_field_22": "",
            "custom_field_23": "",
            "custom_field_24": "",
            "custom_field_25": "",
            "custom_field_26": "",
            "custom_field_27": "",
            "custom_field_28": "",
            "custom_field_29": "",
            "custom_field_30": "",
            "custom_field_31": "",
            "custom_field_32": "",
            "custom_field_33": "",
            "custom_field_34": "",
            "custom_field_35": "",
            "custom_field_36": "",
            "custom_field_37": "",
            "custom_field_38": "",
            "custom_field_39": "",
            "custom_field_40": "",
            "custom_field_41": "",
            "custom_field_42": "",
            "custom_field_43": "",
            "custom_field_44": "",
            "custom_field_45": "",
            "custom_field_46": "",
            "custom_field_47": "",
            "custom_field_48": "",
            "custom_field_49": "",
            "custom_field_50": "",
            "custom_field_51": "",
            "custom_field_52": "",
            "custom_field_53": "",
            "custom_field_54": "",
            "custom_field_55": "",
            "custom_field_56": "",
            "custom_field_57": "",
            "custom_field_58": "",
            "custom_field_59": "",
            "custom_field_60": "",
            "custom_field_61": "",
            "custom_field_62": "",
            "custom_field_63": "",
            "custom_field_64": "",
            "custom_field_65": "",
            "custom_field_66": "",
            "custom_field_67": "",
            "custom_field_68": "",
            "custom_field_69": "",
            "custom_field_70": "",
            "custom_field_71": "",
            "custom_field_72": "",
            "custom_field_73": "",
            "custom_field_74": "",
            "custom_field_75": "",
            "custom_field_76": "",
            "custom_field_77": "",
            "custom_field_78": "",
            "custom_field_79": "",
            "custom_field_80": "",
            "custom_field_81": "",
            "custom_field_82": "",
            "custom_field_83": "",
            "custom_field_84": "",
            "custom_field_85": "",
            "custom_field_86": "",
            "custom_field_87": "",
            "custom_field_88": "",
            "custom_field_89": "",
            "custom_field_90": "",
            "custom_field_91": "",
            "custom_field_92": "",
            "custom_field_93": "",
            "custom_field_94": "",
            "custom_field_95": "",
            "custom_field_96": "",
            "custom_field_97": "",
            "custom_field_98": "",
            "custom_field_99": "",
            "custom_field_100": ""
        }
    },
    "info": "success"
}
```

# 需求字段说明
## 需求重要字段说明
|字段|说明|
|:----:|:----:|
| id | ID |
| name | 标题 |
| priority | 优先级 |
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
| lastmodify | 最后修改人 |
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
| release_id | 发布计划 |
| source | 来源 |
| type | 类型 |
| parent_id | 父需求 |
| children_id | 子需求 |
| description | 详细描述 |
| workspace_id | 项目ID |
| workitem_type_id | 需求类别 |

## 需求优先级(priority)取值字段说明
|取值|字面值|
|:----:|:----:|
| 4 | High |
| 3 | Middle |
| 2 | Low |
| 1 | Nice To Have |

需求字段说明，请参考：[需求字段说明](/api-doc/API文档/api_reference/story/story.md)
