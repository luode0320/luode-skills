# 说明
更新需求，返回需求更新后的数据


# url
`${TAPD_API_ENDPOINT}/stories`

# 支持格式
JSON/XML（默认JSON格式）

#  HTTP请求方式
POST

# 请求数限制
每次只允许更新一条数据

# 请求参数
|字段名|必选|类型及范围|说明|
|:----:|:----:|:----:|:----:|
| id | `是` | integer | ID |
| workspace_id | `是` | integer | 项目ID |
| name | 否 | string | 标题 |
| priority | 否 | string | 优先级。为了兼容自定义优先级，`请使用 priority_label 字段`，详情参考：[如何兼容自定义优先级](/api-doc/API文档/subject/custom_priority/) |
| priority_label | 否 | string | 优先级。推荐使用这个字段 |
| business_value | 否 | integer | 业务价值 |
| status | 否 | string | 状态。需求当前使用并行工作流时，将按状态重置来更新节点，进行中节点变更参考[节点完成接口](/api-doc/API文档/api_reference/story/update_story_step_status.html)  |
| v_status | 否 | string | 状态(支持传入中文状态名称) |
| version | 否 | string | 版本 |
| module | 否 | string | 模块 |
| test_focus | 否 | string | 测试重点 |
| size | 否 | integer | 规模 |
| owner | 否 | string | 处理人 |
| current_user | 否 | string | 变更人 |
| cc | 否 | string | 抄送人 |
| developer | 否 | string | 开发人员 |
| begin | 否 | date | 预计开始 |
| due | 否 | date | 预计结束 |
| iteration_id | 否 | string | 迭代ID |
| effort | 否 | string | 预估工时 |
| effort_completed | 否 | string | 完成工时 |
| remain | 否 | float | 剩余工时 |
| exceed | 否 | float | 超出工时 |
| category_id | 否 | integer | 需求分类 |
| release_id | 否 | integer | 发布计划 |
| source | 否 | string | 来源 |
| type | 否 | string | 类型 |
| description | 否 | string | 详细描述 |
| is_auto_close_task | 否 | integer | 需求流转到结束状态时，是否自动关闭关联的任务。为 1 时会自动关闭；默认取 0，不关闭 |
| label | 否 | string |     标签，标签不存在时将自动创建，多个以英文坚线分格      |
| cus_{$自定义字段别名} | 否 | string |     自定义字段值，参数名会由后台自动转义为custom_field_*，如：cus_这是一个自定义字段的名称 |
| custom_field_* | 否 | string或者integer | 自定义字段参数，具体字段名通过接口 [获取需求自定义字段配置](/api-doc/API文档/api_reference/story/get_story_custom_fields_settings.html) 获取 |
| custom_plan_field_* | 否 | string或者integer | 自定义计划应用参数，具体字段名通过接口 [获取自定义计划应用](/api-doc/API文档/api_reference/iteration/get_plan_apps.html) 获取 |

# 调用示例及返回结果
## 更新需求 1010104801125341253 的优先级为高，处理人为 anyechen
### curl 使用 Basic Auth 鉴权调用示例
`curl -u 'api_user:api_password' -d 'id=1010104801125341253&priority=高&owner=anyechen;&workspace_id=10104801' '${TAPD_API_ENDPOINT}/stories'`

### curl 使用 OAuth Access Token 鉴权调用示例
`curl -H 'Authorization: Bearer ACCESS_TOKEN' -d 'id=1010104801125341253&priority=高&owner=anyechen;&workspace_id=10104801' '${TAPD_API_ENDPOINT}/stories'`

### 返回结果
```JSON
{
    "status": 1,
    "data": {
        "Story": {
            "id": "1010104801125341253",
            "workitem_type_id": "1010104801000022091",
            "name": "1frxxx - txt",
            "description": "<p>666111</p>",
            "workspace_id": "10104801",
            "creator": "anyechen",
            "created": "2025-06-27 12:22:31",
            "modified": "2025-07-08 14:51:25",
            "status": "planning",
            "step": "",
            "owner": "anyechen;",
            "cc": "",
            "begin": null,
            "due": null,
            "size": null,
            "priority": "高",
            "developer": "",
            "iteration_id": "1010104801001103985",
            "test_focus": "111",
            "type": "功能需求",
            "source": "",
            "module": "",
            "version": "",
            "completed": null,
            "category_id": "-1",
            "path": "1010104801125341252::1010104801125341253:",
            "parent_id": "1010104801125341252",
            "children_id": "|",
            "ancestor_id": "1010104801125341252",
            "level": "1",
            "business_value": null,
            "effort": null,
            "effort_completed": "0",
            "exceed": "0",
            "remain": "0",
            "release_id": "0",
            "bug_id": null,
            "templated_id": "1010104801000090889",
            "created_from": null,
            "feature": "",
            "label": "",
            "progress": "0",
            "is_archived": "0",
            "tech_risk": null,
            "flows": null,
            "custom_field_one": "",
            "custom_field_two": "",
            "custom_field_three": "",
            "custom_field_four": "",
            "custom_field_five": "",
            "custom_field_six": "",
            "custom_field_seven": "",
            "custom_field_eight": "",
            "secret_root_id": "0",
            "progress_manual": "0",
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
            "custom_field_48": "2",
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
            "custom_field_100": "",
            "custom_field_101": "",
            "custom_field_102": "",
            "custom_field_103": "",
            "custom_field_104": "",
            "custom_field_105": "",
            "custom_field_106": "",
            "custom_field_107": "",
            "custom_field_108": "",
            "custom_field_109": "",
            "custom_field_110": "",
            "custom_field_111": "",
            "custom_field_112": "",
            "custom_field_113": "",
            "custom_field_114": "",
            "custom_field_115": "",
            "custom_field_116": "",
            "custom_field_117": "",
            "custom_field_118": "",
            "custom_field_119": "",
            "custom_field_120": "",
            "custom_field_121": "",
            "custom_field_122": "",
            "custom_field_123": "",
            "custom_field_124": "",
            "custom_field_125": "",
            "custom_field_126": "",
            "custom_field_127": "",
            "custom_field_128": "",
            "custom_field_129": "",
            "custom_field_130": "",
            "custom_field_131": "",
            "custom_field_132": "",
            "custom_field_133": "",
            "custom_field_134": "",
            "custom_field_135": "",
            "custom_field_136": "",
            "custom_field_137": "",
            "custom_field_138": "",
            "custom_field_139": "",
            "custom_field_140": "",
            "custom_field_141": "",
            "custom_field_142": "",
            "custom_field_143": "",
            "custom_field_144": "",
            "custom_field_145": "",
            "custom_field_146": "",
            "custom_field_147": "",
            "custom_field_148": "",
            "custom_field_149": "",
            "custom_field_150": "",
            "custom_field_151": "",
            "custom_field_152": "",
            "custom_field_153": "",
            "custom_field_154": "",
            "custom_field_155": "",
            "custom_field_156": "",
            "custom_field_157": "",
            "custom_field_158": "",
            "custom_field_159": "",
            "custom_field_160": "",
            "custom_field_161": "",
            "custom_field_162": "",
            "custom_field_163": "",
            "custom_field_164": "",
            "custom_field_165": "",
            "custom_field_166": "",
            "custom_field_167": "",
            "custom_field_168": "",
            "custom_field_169": "",
            "custom_field_170": "",
            "custom_field_171": "",
            "custom_field_172": "",
            "custom_field_173": "",
            "custom_field_174": "",
            "custom_field_175": "",
            "custom_field_176": "",
            "custom_field_177": "",
            "custom_field_178": "",
            "custom_field_179": "",
            "custom_field_180": "",
            "custom_field_181": "",
            "custom_field_182": "",
            "custom_field_183": "",
            "custom_field_184": "",
            "custom_field_185": "",
            "custom_field_186": "",
            "custom_field_187": "",
            "custom_field_188": "",
            "custom_field_189": "",
            "custom_field_190": "",
            "custom_field_191": "",
            "custom_field_192": "",
            "custom_field_193": "",
            "custom_field_194": "",
            "custom_field_195": "",
            "custom_field_196": "",
            "custom_field_197": "",
            "custom_field_198": "",
            "custom_field_199": "",
            "custom_field_200": "",
            "custom_plan_field_1": "0",
            "custom_plan_field_2": "0",
            "custom_plan_field_3": "0",
            "custom_plan_field_4": "0",
            "custom_plan_field_5": "0",
            "custom_plan_field_6": "0",
            "custom_plan_field_7": "0",
            "custom_plan_field_8": "0",
            "custom_plan_field_9": "0",
            "custom_plan_field_10": "0",
            "priority_label": "高"
        }
    },
    "info": "success"
}
```

# 需求字段说明
需求字段说明，请参考：[需求字段说明](/api-doc/API文档/api_reference/story/story.md)
