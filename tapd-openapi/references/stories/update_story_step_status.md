# 说明
完成进行中的节点


# url
`${TAPD_API_ENDPOINT}/stories/update_story_step_status`

# 支持格式
JSON/XML（默认JSON格式）

#  HTTP请求方式
POST

# 请求数限制
每次只允许更新一条数据

# 请求参数
|字段名|必选|  类型及范围  |     说明     |
|:----:|:----:|:-------:|:----------:|
| story_id | `是` | integer |    需求ID    |
| workspace_id | `是` | integer |    项目ID    |
| step | `是` | string  | 取值必须为当前进行中的节点  |

# 调用示例及返回结果
## 完成需求1010104801871430407的工作流节点，返回需求更新后的数据
### curl 使用 Basic Auth 鉴权调用示例
`curl -u 'api_user:api_password' -d 'story_id=1010104801871430407&step=step_10555_1&workspace_id=10104801' '${TAPD_API_ENDPOINT}/stories/update_story_step_status'`

### curl 使用 OAuth Access Token 鉴权调用示例
`curl -H 'Authorization: Bearer ACCESS_TOKEN' -d 'story_id=1010104801871430407&step=step_10555_1&workspace_id=10104801' '${TAPD_API_ENDPOINT}/stories/update_story_step_status'`

### 返回结果
```JSON
{
    "status": 1,
    "data": {
        "Story": {
            "id": "1010104801871430407",
            "workitem_type_id": "1010104801000022091",
            "name": "aatt",
            "description": null,
            "workspace_id": "10104801",
            "creator": "v_xuanfang",
            "created": "2022-01-07 15:21:15",
            "modified": "2022-01-11 16:57:11",
            "status": "develop",
            "owner": "",
            "cc": "",
            "begin": null,
            "due": null,
            "size": null,
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
            "path": "1010104801870636009:1010104801871430407:",
            "parent_id": "1010104801870636009",
            "children_id": "|",
            "ancestor_id": "1010104801870636009",
            "business_value": null,
            "effort": "0",
            "effort_completed": "4",
            "exceed": "10",
            "remain": "6",
            "release_id": "0",
            "confidential": "N",
            "templated_id": null,
            "custom_field_one": "",
            "custom_field_two": "",
            "custom_field_three": "",
            "custom_field_four": "",
            "custom_field_five": "",
            "custom_field_six": "",
            "custom_field_seven": "",
            "custom_field_eight": "",
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
            "custom_field_200": ""
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

## 需求优先级(priority)取值字段说明
|取值|字面值|
|:----:|:----:|
| 4 | High |
| 3 | Middle |
| 2 | Low |
| 1 | Nice To Have |
