# 说明
获取需求所有字段及候选值，返回符合查询条件的所有需求字段及候选值。
部分字段为静态候选值，建议参考下方 “可选值说明”部分。其余动态字段（如：status(状态)/iteration_id(迭代)/categories(需求分类)），需要通过该接口获取对应的候选值（中英文映射）。


# url
`${TAPD_API_ENDPOINT}/stories/get_fields_info`

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
`curl -u 'api_user:api_password'  '${TAPD_API_ENDPOINT}/stories/get_fields_info?workspace_id=10104801'`

### curl 使用 OAuth Access Token 鉴权调用示例
`curl -H 'Authorization: Bearer ACCESS_TOKEN'  '${TAPD_API_ENDPOINT}/stories/get_fields_info?workspace_id=10104801'`

### 返回结果
```JSON
{
    "status": 1,
    "data": {
        "id": {
            "name": "id",
            "options": [],
            "html_type": "input",
            "label": "ID",
            "pure_options": [],
            "readonly": 0
        },
        "name": {
            "name": "name",
            "options": [],
            "html_type": "input",
            "label": "标题",
            "pure_options": [],
            "readonly": 0
        },
        "status": {
            "name": "status",
            "options": {
                "planning": "规划中",
                "developing": "实现中",
                "resolved": "已实现",
                "rejected": "已拒绝",
                "status_1": "其他状态1",
                "status_3": "已完成",
                "status_5": "new",
                "status_6": "aaaeb",
                "status_9": "需求终止",
                "status_10": "待规划",
                "status_11": "已评审",
                "status_12": "已排期",
                "status_13": "待排期",
                "status_14": "开发中",
                "status_15": "待测试",
                "status_16": "测试中",
                "status_17": "待验收",
                "status_18": "待发布",
                "status_19": "发布中",
                "status_20": "已发布",
                "status_21": "需求暂停2333",
                "status_22": "未开始",
                "status_23": "进行中"
            },
            "html_type": "select",
            "label": "状态",
            "pure_options": [],
            "readonly": 0
        },
        "description": {
            "name": "description",
            "options": [],
            "html_type": "rich_edit",
            "label": "详细描述",
            "pure_options": [],
            "readonly": 0
        },
        "owner": {
            "name": "owner",
            "options": [],
            "html_type": "single_user_chooser",
            "label": "处理人",
            "pure_options": [],
            "readonly": 0,
            "user_options": []
        },
        "creator": {
            "name": "creator",
            "options": [],
            "html_type": "user_chooser",
            "label": "创建人",
            "pure_options": [],
            "readonly": 0
        },
        "created": {
            "name": "created",
            "options": [],
            "html_type": "datetime",
            "label": "创建时间",
            "pure_options": [],
            "readonly": 0
        },
        "iteration_id": {
            "name": "iteration_id",
            "options": {
                "1010104801001662155": "fromAPI",
                "1010104801001787437": "测试自定义字段",
                "1010104801001641399": "create by api",
                "1010104801001641397": "页面新迭代",
                "1010104801001595935": "锁定的迭代",
                "1010104801001179909": "aaaassssss",
                "1020419374001202991": "adra",
                "1010104801001179887": "cjdd",
                "1010104801001103985": "对对对",
                "1010104801001112221": "myI",
                "1010104801001080913": "【Word】191001常规发布",
                "1010104801001171067": "oyctest20190911xxx1111",
                "1010104801001169803": "oyctest20190911xxx1111",
                "1010104801001105965": "oyctest20190911xxx1111",
                "1010104801001105193": "oyctest20190911xxx1111",
                "1010104801001082017": "日常发布",
                "1010104801001082013": "日常发布",
                "1010104801001081899": "oyctest20190917ABC2",
                "1010104801001080783": "日常发布",
                "1010104801001123207": "oyctest20190911",
                "1010104801000507689": "i1",
                "1010104801000423181": "迭代1",
                "1010104801001733159": "测试创建迭代2",
                "1010104801001628193": "API创建测试",
                "1010104801001628057": "测试创建迭代2",
                "1010104801001628055": "测试创建迭代"
            },
            "html_type": "select",
            "label": "迭代",
            "pure_options": [
                {
                    "parent_id": "0",
                    "workspace_id": "10104801",
                    "sort": "120299500000",
                    "workitem_type_id": "1010104801000321043",
                    "plan_app_id": "0",
                    "value": "1010104801001662155",
                    "label": "fromAPI",
                    "panel": 0
                },
                {
                    "parent_id": "0",
                    "workspace_id": "10104801",
                    "sort": "120299600000",
                    "workitem_type_id": "1010104801000321043",
                    "plan_app_id": "0",
                    "value": "1010104801001787437",
                    "label": "测试自定义字段",
                    "panel": 0
                },
                {
                    "parent_id": "0",
                    "workspace_id": "10104801",
                    "sort": "120299400000",
                    "workitem_type_id": "1010104801000321043",
                    "plan_app_id": "0",
                    "value": "1010104801001641399",
                    "label": "create by api",
                    "panel": 0
                },
                {
                    "parent_id": "0",
                    "workspace_id": "10104801",
                    "sort": "120299300000",
                    "workitem_type_id": "1010104801000321043",
                    "plan_app_id": "0",
                    "value": "1010104801001641397",
                    "label": "页面新迭代",
                    "panel": 0
                },
                {
                    "parent_id": "0",
                    "workspace_id": "10104801",
                    "sort": "120299200000",
                    "workitem_type_id": "1010104801000321043",
                    "plan_app_id": "0",
                    "value": "1010104801001595935",
                    "label": "锁定的迭代",
                    "panel": 0
                },
                {
                    "parent_id": "0",
                    "workspace_id": "10104801",
                    "sort": "117990900000",
                    "workitem_type_id": "1010104801000321043",
                    "plan_app_id": "0",
                    "value": "1010104801001179909",
                    "label": "aaaassssss",
                    "panel": 0
                },
                {
                    "parent_id": "0",
                    "workspace_id": "10104801",
                    "sort": "120299100000",
                    "workitem_type_id": "1010104801000321043",
                    "plan_app_id": "0",
                    "value": "1020419374001202991",
                    "label": "adra",
                    "panel": 0
                },
                {
                    "parent_id": "0",
                    "workspace_id": "10104801",
                    "sort": "117988700000",
                    "workitem_type_id": "1010104801000321043",
                    "plan_app_id": "0",
                    "value": "1010104801001179887",
                    "label": "cjdd",
                    "panel": 0
                },
                {
                    "parent_id": "0",
                    "workspace_id": "10104801",
                    "sort": "110398500000",
                    "workitem_type_id": "1010104801000321043",
                    "plan_app_id": "0",
                    "value": "1010104801001103985",
                    "label": "对对对",
                    "panel": 0
                },
                {
                    "parent_id": "0",
                    "workspace_id": "10104801",
                    "sort": "111222100000",
                    "workitem_type_id": "1010104801000321043",
                    "plan_app_id": "0",
                    "value": "1010104801001112221",
                    "label": "myI",
                    "panel": 0
                },
                {
                    "parent_id": "0",
                    "workspace_id": "10104801",
                    "sort": "108091300000",
                    "workitem_type_id": "1010104801000321043",
                    "plan_app_id": "0",
                    "value": "1010104801001080913",
                    "label": "【Word】191001常规发布",
                    "panel": 0
                },
                {
                    "parent_id": "0",
                    "workspace_id": "10104801",
                    "sort": "117106700000",
                    "workitem_type_id": "1010104801000321043",
                    "plan_app_id": "0",
                    "value": "1010104801001171067",
                    "label": "oyctest20190911xxx1111",
                    "panel": 0
                },
                {
                    "parent_id": "0",
                    "workspace_id": "10104801",
                    "sort": "116980300000",
                    "workitem_type_id": "1010104801000321043",
                    "plan_app_id": "0",
                    "value": "1010104801001169803",
                    "label": "oyctest20190911xxx1111",
                    "panel": 0
                },
                {
                    "parent_id": "0",
                    "workspace_id": "10104801",
                    "sort": "110596500000",
                    "workitem_type_id": "1010104801000321043",
                    "plan_app_id": "0",
                    "value": "1010104801001105965",
                    "label": "oyctest20190911xxx1111",
                    "panel": 0
                },
                {
                    "parent_id": "0",
                    "workspace_id": "10104801",
                    "sort": "110519300000",
                    "workitem_type_id": "1010104801000321043",
                    "plan_app_id": "0",
                    "value": "1010104801001105193",
                    "label": "oyctest20190911xxx1111",
                    "panel": 0
                },
                {
                    "parent_id": "0",
                    "workspace_id": "10104801",
                    "sort": "108201700000",
                    "workitem_type_id": "1010104801000321043",
                    "plan_app_id": "0",
                    "value": "1010104801001082017",
                    "label": "日常发布",
                    "panel": 0
                },
                {
                    "parent_id": "0",
                    "workspace_id": "10104801",
                    "sort": "108201300000",
                    "workitem_type_id": "1010104801000321043",
                    "plan_app_id": "0",
                    "value": "1010104801001082013",
                    "label": "日常发布",
                    "panel": 0
                },
                {
                    "parent_id": "0",
                    "workspace_id": "10104801",
                    "sort": "108189900000",
                    "workitem_type_id": "1010104801000321043",
                    "plan_app_id": "0",
                    "value": "1010104801001081899",
                    "label": "oyctest20190917ABC2",
                    "panel": 0
                },
                {
                    "parent_id": "0",
                    "workspace_id": "10104801",
                    "sort": "108078300000",
                    "workitem_type_id": "1010104801000321043",
                    "plan_app_id": "0",
                    "value": "1010104801001080783",
                    "label": "日常发布",
                    "panel": 0
                },
                {
                    "parent_id": "0",
                    "workspace_id": "10104801",
                    "sort": "112320700000",
                    "workitem_type_id": "1010104801000321043",
                    "plan_app_id": "0",
                    "value": "1010104801001123207",
                    "label": "oyctest20190911",
                    "panel": 0
                },
                {
                    "parent_id": "0",
                    "workspace_id": "10104801",
                    "sort": "50768900000",
                    "workitem_type_id": "1010104801000321043",
                    "plan_app_id": "0",
                    "value": "1010104801000507689",
                    "label": "i1",
                    "panel": 0
                },
                {
                    "parent_id": "0",
                    "workspace_id": "10104801",
                    "sort": "42318100000",
                    "workitem_type_id": "1010104801000321043",
                    "plan_app_id": "0",
                    "value": "1010104801000423181",
                    "label": "迭代1",
                    "panel": 0
                },
                {
                    "parent_id": "0",
                    "workspace_id": "10104801",
                    "sort": "0",
                    "workitem_type_id": "1010104801000321043",
                    "plan_app_id": "0",
                    "value": "1010104801001733159",
                    "label": "测试创建迭代2",
                    "panel": 0
                },
                {
                    "parent_id": "0",
                    "workspace_id": "10104801",
                    "sort": "0",
                    "workitem_type_id": "1010104801000321043",
                    "plan_app_id": "0",
                    "value": "1010104801001628193",
                    "label": "API创建测试",
                    "panel": 0
                },
                {
                    "parent_id": "0",
                    "workspace_id": "10104801",
                    "sort": "0",
                    "workitem_type_id": "1010104801000321043",
                    "plan_app_id": "0",
                    "value": "1010104801001628057",
                    "label": "测试创建迭代2",
                    "panel": 0
                },
                {
                    "parent_id": "0",
                    "workspace_id": "10104801",
                    "sort": "0",
                    "workitem_type_id": "1010104801000321043",
                    "plan_app_id": "0",
                    "value": "1010104801001628055",
                    "label": "测试创建迭代",
                    "panel": 0
                }
            ],
            "readonly": 0
        },
        "effort": {
            "name": "effort",
            "options": [],
            "html_type": "float",
            "label": "预估工时",
            "pure_options": [],
            "readonly": 0
        },
        "effort_completed": {
            "name": "effort_completed",
            "options": [],
            "html_type": "float",
            "label": "完成工时",
            "pure_options": [],
            "readonly": 0
        },
        "remain": {
            "name": "remain",
            "options": [],
            "html_type": "float",
            "label": "剩余工时",
            "pure_options": [],
            "readonly": 0
        },
        "exceed": {
            "name": "exceed",
            "options": [],
            "html_type": "float",
            "label": "超出工时",
            "pure_options": [],
            "readonly": 0
        },
        "progress": {
            "name": "progress",
            "options": [],
            "html_type": "input",
            "label": "进度",
            "pure_options": [],
            "readonly": 0
        },
        "modified": {
            "name": "modified",
            "options": [],
            "html_type": "datetime",
            "label": "最后修改时间",
            "pure_options": [],
            "readonly": 0
        },
        "priority": {
            "name": "priority",
            "html_type": "select",
            "label": "优先级",
            "pure_options": [],
            "readonly": 0,
            "color_options": [
                {
                    "value": "紧急",
                    "color": "#FF6770",
                    "label": "紧急"
                },
                {
                    "value": "高",
                    "color": "#FAA23B",
                    "label": "高"
                },
                {
                    "value": "中",
                    "color": "#F7C100",
                    "label": "中"
                },
                {
                    "value": "低",
                    "color": "#0D68FF",
                    "label": "低"
                },
                {
                    "value": "锦上添花",
                    "color": "#28AB80",
                    "label": "锦上添花"
                }
            ],
            "options": {
                "紧急": "紧急",
                "高": "高",
                "中": "中",
                "低": "低",
                "锦上添花": "锦上添花"
            }
        },
        "cc": {
            "name": "cc",
            "options": [],
            "html_type": "mix_chooser",
            "label": "抄送人",
            "pure_options": [],
            "readonly": 0
        },
        "begin": {
            "name": "begin",
            "options": [],
            "html_type": "dateinput",
            "label": "预计开始",
            "pure_options": [],
            "readonly": 0
        },
        "due": {
            "name": "due",
            "options": [],
            "html_type": "dateinput",
            "label": "预计结束",
            "pure_options": [],
            "readonly": 0
        },
        "source": {
            "name": "source",
            "options": {
                "产品规划": "产品规划",
                "用户反馈": "用户反馈",
                "总办": "总办",
                "其他": "其他",
                "CE平台": "CE平台"
            },
            "html_type": "select",
            "label": "需求来源",
            "pure_options": [],
            "readonly": 0
        },
        "workitem_type_id": {
            "name": "workitem_type_id",
            "options": {
                "1010104801000078307": "技术需求aaa",
                "1010104801000314545": "测试类别",
                "1010104801000022091": "需求",
                "1010104801000323559": "智研需求",
                "1010104801000626412": "任务aa"
            },
            "html_type": "select",
            "label": "需求类别",
            "pure_options": [],
            "readonly": 0
        },
        "type": {
            "name": "type",
            "options": {
                "功能需求": "功能需求",
                "体验优化需求": "体验优化需求",
                "技术需求": "技术需求",
                "其他": "其他",
                "产品需求": "产品需求",
                "运营需求": "运营需求",
                "算法类需求": "算法类需求",
                "售前需求": "售前需求",
                "其它": "其它",
                "业务需求": "业务需求"
            },
            "html_type": "select",
            "label": "需求类型",
            "pure_options": [],
            "readonly": 0
        },
        "children_id": {
            "name": "children_id",
            "options": [],
            "html_type": "input",
            "label": "子需求",
            "pure_options": [],
            "readonly": 0
        },
        "workspace_id": {
            "name": "workspace_id",
            "options": {
                "10104801": "TAPD 乌云",
                "70148636": "发布计划升级"
            },
            "html_type": "select",
            "label": "所属项目",
            "pure_options": [],
            "readonly": 0
        },
        "completed": {
            "name": "completed",
            "options": [],
            "html_type": "datetime",
            "label": "完成时间",
            "pure_options": [],
            "readonly": 0
        },
        "parent_id": {
            "name": "parent_id",
            "options": [],
            "html_type": "input",
            "label": "父需求",
            "pure_options": [],
            "readonly": 0
        },
        "business_value": {
            "name": "business_value",
            "options": [],
            "html_type": "integer",
            "label": "业务价值",
            "pure_options": [],
            "readonly": 0
        },
        "tech_risk": {
            "name": "tech_risk",
            "options": [],
            "html_type": "integer",
            "label": "技术风险",
            "pure_options": [],
            "readonly": 0
        },
        "has_attachment": {
            "name": "has_attachment",
            "options": {
                "1": "-不为空-",
                "0": "-空-"
            },
            "html_type": "checkbox",
            "label": "附件",
            "pure_options": [],
            "readonly": 0
        },
        "size": {
            "name": "size",
            "options": [],
            "html_type": "integer",
            "label": "规模",
            "pure_options": [],
            "readonly": 0
        },
        "feature": {
            "name": "feature",
            "options": {
                "tx1": "tx1"
            },
            "html_type": "select",
            "label": "特性",
            "pure_options": [],
            "readonly": 0
        },
        "test_focus": {
            "name": "test_focus",
            "options": [],
            "html_type": "textarea",
            "label": "测试重点",
            "pure_options": [],
            "readonly": 0
        },
        "developer": {
            "name": "developer",
            "options": [],
            "html_type": "user_chooser",
            "label": "开发人员",
            "pure_options": [],
            "readonly": 0,
            "user_options": []
        },
        "category_id": {
            "name": "category_id",
            "options": {
                "1010104801000037409": "abc",
                "1010104801000037411": "adfadxx",
                "1010104801001049673": "test",
                "1010104801001179311": "ttt",
                "1010104801001228145": "wd",
                "1010104801002646384": "test222",
                "-1": "未分类"
            },
            "html_type": "select",
            "label": "分类",
            "pure_options": [
                {
                    "name": "abc",
                    "id": "1010104801000037409",
                    "parent_id": "0",
                    "workspace_id": "10104801",
                    "sorting": "2",
                    "label": "abc",
                    "value": "1010104801000037409"
                },
                {
                    "name": "adfadxx",
                    "id": "1010104801000037411",
                    "parent_id": "0",
                    "workspace_id": "10104801",
                    "sorting": "1",
                    "label": "adfadxx",
                    "value": "1010104801000037411"
                },
                {
                    "name": "test",
                    "id": "1010104801001049673",
                    "parent_id": "1010104801000037411",
                    "workspace_id": "10104801",
                    "sorting": "0",
                    "label": "test",
                    "value": "1010104801001049673"
                },
                {
                    "name": "ttt",
                    "id": "1010104801001179311",
                    "parent_id": "1010104801000037111",
                    "workspace_id": "10104801",
                    "sorting": "0",
                    "label": "ttt",
                    "value": "1010104801001179311"
                },
                {
                    "name": "wd",
                    "id": "1010104801001228145",
                    "parent_id": "1010104801001179311",
                    "workspace_id": "10104801",
                    "sorting": "3",
                    "label": "wd",
                    "value": "1010104801001228145"
                },
                {
                    "name": "test222",
                    "id": "1010104801002646384",
                    "parent_id": "0",
                    "workspace_id": "10104801",
                    "sorting": "0",
                    "label": "test222",
                    "value": "1010104801002646384"
                }
            ],
            "readonly": 0
        },
        "module": {
            "name": "module",
            "options": {
                "333": "333",
                "创建模块": "创建模块"
            },
            "html_type": "select",
            "label": "模块",
            "pure_options": [],
            "readonly": 0
        },
        "version": {
            "name": "version",
            "options": {
                "ver1.1": "ver1.1",
                "[v1.16.1]计费下单支付-支持渠道物品信息反查": "[v1.16.1]计费下单支付-支持渠道物品信息反查"
            },
            "html_type": "select",
            "label": "版本",
            "pure_options": [],
            "readonly": 0
        },
        "label": {
            "name": "label",
            "options": {
                "三方依赖": "三方依赖",
                "待讨论": "待讨论",
                "提高优先级": "提高优先级",
                "管理层关注": "管理层关注",
                "紧急需求": "紧急需求",
                "非常棒": "非常棒",
                "阻塞": "阻塞",
                "开发受阻": "开发受阻",
                "有风险": "有风险",
                "等待设计走查": "等待设计走查",
                "方案已沟通": "方案已沟通",
                "等待转测": "等待转测"
            },
            "html_type": "multi_select",
            "label": "标签",
            "pure_options": [],
            "readonly": 0
        },
        "custom_field_50": {
            "name": "custom_field_50",
            "options": [],
            "html_type": "text",
            "label": "客户联系方式",
            "pure_options": [],
            "readonly": 0,
            "memo": "提供客户联系方式： QQ号+手机号+UIN"
        },
        "custom_field_49": {
            "name": "custom_field_49",
            "options": [],
            "html_type": "text",
            "label": "反馈量（一线）",
            "pure_options": [],
            "readonly": 0,
            "memo": ""
        },
        "custom_field_48": {
            "name": "custom_field_48",
            "options": {
                "1": "1",
                "2": "2",
                "3": "3"
            },
            "html_type": "select",
            "label": "产品分类",
            "pure_options": [],
            "readonly": 0,
            "enable_color": 0,
            "color_options": [],
            "memo": ""
        },
        "custom_field_one": {
            "name": "custom_field_one",
            "options": [],
            "html_type": "dateinput",
            "label": "atime",
            "pure_options": [],
            "readonly": 0,
            "memo": ""
        },
        "custom_field_three": {
            "name": "custom_field_three",
            "options": [],
            "html_type": "float",
            "label": "进度情况",
            "pure_options": [],
            "readonly": 0,
            "memo": ""
        },
        "custom_field_four": {
            "name": "custom_field_four",
            "options": [
                {
                    "name": "联动一级",
                    "children": [
                        {
                            "name": "联动一级子",
                            "children": [
                                {
                                    "name": "联动一级子子"
                                },
                                {
                                    "name": "联动一级子子1"
                                },
                                {
                                    "name": "联动一级子子2"
                                }
                            ]
                        },
                        {
                            "name": "联动一级a"
                        }
                    ]
                },
                {
                    "name": "联动二级",
                    "children": [
                        {
                            "name": "联动二级子"
                        },
                        {
                            "name": "联动二级a"
                        }
                    ]
                }
            ],
            "html_type": "cascade_checkbox",
            "label": "联动层级多选项目",
            "pure_options": [],
            "readonly": 0,
            "memo": ""
        },
        "custom_field_five": {
            "name": "custom_field_five",
            "options": [],
            "html_type": "text",
            "label": "^^^3###$%Q@\"'",
            "pure_options": [],
            "readonly": 0,
            "memo": "dafads"
        },
        "custom_field_six": {
            "name": "custom_field_six",
            "options": [],
            "html_type": "text",
            "label": "123",
            "pure_options": [],
            "readonly": 0,
            "memo": ""
        },
        "custom_field_seven": {
            "name": "custom_field_seven",
            "options": {
                "aa": "aa",
                "bb": "bb",
                "cc": "cc",
                "dd": "dd"
            },
            "html_type": "select",
            "label": "下拉测试",
            "pure_options": [],
            "readonly": 0,
            "enable_color": 0,
            "color_options": [
                {
                    "label": "aa",
                    "value": "aa",
                    "color": "transparent"
                },
                {
                    "label": "bb",
                    "value": "bb",
                    "color": "transparent"
                },
                {
                    "label": "cc",
                    "value": "cc",
                    "color": "transparent"
                },
                {
                    "label": "dd",
                    "value": "dd",
                    "color": "transparent"
                }
            ],
            "memo": ""
        },
        "custom_field_eight": {
            "name": "custom_field_eight",
            "options": [],
            "html_type": "user_chooser",
            "label": "测试人名",
            "pure_options": [],
            "readonly": 0,
            "user_options": [],
            "memo": ""
        },
        "custom_field_9": {
            "name": "custom_field_9",
            "options": [],
            "html_type": "dateinput",
            "label": "计划上线日期",
            "pure_options": [],
            "readonly": 0,
            "memo": ""
        },
        "custom_field_10": {
            "name": "custom_field_10",
            "options": [],
            "html_type": "datetime",
            "label": "实际开始",
            "pure_options": [],
            "readonly": 0,
            "memo": ""
        },
        "custom_field_11": {
            "name": "custom_field_11",
            "options": [],
            "html_type": "datetime",
            "label": "实际结束",
            "pure_options": [],
            "readonly": 0,
            "memo": ""
        },
        "custom_field_12": {
            "name": "custom_field_12",
            "options": [],
            "html_type": "text",
            "label": "排序",
            "pure_options": [],
            "readonly": 0,
            "memo": "推荐用于辅助优先级排序，或按约定定义排序"
        },
        "custom_field_13": {
            "name": "custom_field_13",
            "options": [],
            "html_type": "user_chooser",
            "label": "需求提出人",
            "pure_options": [],
            "readonly": 0,
            "user_options": [],
            "memo": "默认等于创建人"
        },
        "custom_field_14": {
            "name": "custom_field_14",
            "options": [],
            "html_type": "user_chooser",
            "label": "测试人员",
            "pure_options": [],
            "readonly": 0,
            "user_options": [],
            "memo": ""
        },
        "custom_field_15": {
            "name": "custom_field_15",
            "options": {
                "是": "是",
                "否": "否"
            },
            "html_type": "radio",
            "label": "是否免测",
            "pure_options": [],
            "readonly": 0,
            "memo": ""
        },
        "custom_field_16": {
            "name": "custom_field_16",
            "options": {
                "是": "是",
                "否": "否"
            },
            "html_type": "radio",
            "label": "是否紧急需求",
            "pure_options": [],
            "readonly": 0,
            "memo": ""
        },
        "custom_field_18": {
            "name": "custom_field_18",
            "options": [],
            "html_type": "text",
            "label": "API创建",
            "pure_options": [],
            "readonly": 0,
            "memo": ""
        },
        "custom_field_19": {
            "name": "custom_field_19",
            "options": [],
            "html_type": "file",
            "label": "附件测试",
            "pure_options": [],
            "readonly": 0,
            "memo": ""
        },
        "custom_field_17": {
            "name": "custom_field_17",
            "options": [
                {
                    "name": "a1",
                    "children": [
                        {
                            "name": "a11"
                        },
                        {
                            "name": "a12",
                            "children": [
                                {
                                    "name": "a123"
                                }
                            ]
                        }
                    ]
                },
                {
                    "name": "a2"
                },
                {
                    "name": "a3"
                }
            ],
            "html_type": "cascade_radio",
            "label": "联动字段测试",
            "pure_options": [],
            "readonly": 0,
            "memo": ""
        },
        "custom_plan_field_1": {
            "name": "custom_plan_field_1",
            "options": {
                "1010104801001754573": "快速迭代1"
            },
            "html_type": "select",
            "label": "超级迭代",
            "pure_options": [
                {
                    "parent_id": "0",
                    "workspace_id": "10104801",
                    "sort": "120299600000",
                    "workitem_type_id": "1010104801000289247",
                    "plan_app_id": "1010104801000000397",
                    "value": "1010104801001754573",
                    "label": "快速迭代1",
                    "panel": 0
                }
            ],
            "readonly": 0
        },
        "custom_plan_field_2": {
            "name": "custom_plan_field_2",
            "options": {
                "1010104801001934461": "v2test12",
                "1010104801001934457": "发布",
                "1010104801001934455": "4324"
            },
            "html_type": "select",
            "label": "发布计划",
            "pure_options": [
                {
                    "parent_id": "0",
                    "workspace_id": "10104801",
                    "sort": "120299700000",
                    "workitem_type_id": "1010104801000445327",
                    "plan_app_id": "1010104801000085167",
                    "value": "1010104801001934461",
                    "label": "v2test12",
                    "panel": 0
                },
                {
                    "parent_id": "0",
                    "workspace_id": "10104801",
                    "sort": "120299700000",
                    "workitem_type_id": "1010104801000445327",
                    "plan_app_id": "1010104801000085167",
                    "value": "1010104801001934457",
                    "label": "发布",
                    "panel": 0
                },
                {
                    "parent_id": "0",
                    "workspace_id": "10104801",
                    "sort": "120299700000",
                    "workitem_type_id": "1010104801000445327",
                    "plan_app_id": "1010104801000085167",
                    "value": "1010104801001934455",
                    "label": "4324",
                    "panel": 0
                }
            ],
            "readonly": 0
        },
        "custom_plan_field_3": {
            "name": "custom_plan_field_3",
            "options": {
                "1010104801002112931": "123"
            },
            "html_type": "select",
            "label": "ABC计划",
            "pure_options": [
                {
                    "parent_id": "0",
                    "workspace_id": "10104801",
                    "sort": "120299700000",
                    "workitem_type_id": "1010104801000497881",
                    "plan_app_id": "1010104801000106675",
                    "value": "1010104801002112931",
                    "label": "123",
                    "panel": 0
                }
            ],
            "readonly": 0
        },
        "priority_label": {
            "name": "priority_label",
            "options": {
                "紧急": "紧急",
                "高": "高",
                "中": "中",
                "低": "低",
                "锦上添花": "锦上添花"
            },
            "html_type": "select",
            "label": "优先级",
            "pure_options": [],
            "readonly": 0,
            "color_options": [
                {
                    "value": "紧急",
                    "color": "#FF6770",
                    "label": "紧急"
                },
                {
                    "value": "高",
                    "color": "#FAA23B",
                    "label": "高"
                },
                {
                    "value": "中",
                    "color": "#F7C100",
                    "label": "中"
                },
                {
                    "value": "低",
                    "color": "#0D68FF",
                    "label": "低"
                },
                {
                    "value": "锦上添花",
                    "color": "#28AB80",
                    "label": "锦上添花"
                }
            ]
        },
        "release_id": {
            "name": "release_id",
            "options": {
                "1010104801000069739": "v2test12",
                "1010104801000068405": "发布",
                "1010104801000058771": "4324"
            },
            "html_type": "select",
            "label": "发布计划",
            "pure_options": [],
            "readonly": 0
        }
    },
    "info": "success"
}
```

# 返回说明
### 格式说明
| 字段 | 说明 |
|:----:|:----:|
| name | name |
| options | 候选值 |
| html_type | 类型 |
| label | 中文名称 |

### 返回字段说明
|字段|说明|
|:----:|:----:|
| id | ID |
| name | 标题 |
| priority | 优先级 |
| business_value | 业务价值 |
| status | 状态|
| version | 版本 |
| module | 模块 |
| feature | 特性 |
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
| iteration_id | 迭代ID |
| templated_id | 模板ID |
| effort | 预估工时 |
| effort_completed | 完成工时 |
| remain | 剩余工时 |
| exceed | 超出工时 |
| category_id | 需求分类(取 -1 时，为未分类) |
| release_id | 发布计划 |
| is_archived | 是否归档 |
| source | 来源 |
| type | 类型 |
| parent_id | 父需求 |
| children_id | 子需求 |
| description | 详细描述 |
| workspace_id | 项目ID |
| workitem_type_id | 需求类别 |
| confidential | 是否保密 |
| created_from | 需求创建来源（为空时代表web创建） |
| level | 层级 |
| bug_id | 缺陷ID（当缺陷转需求时才会有值） |

## 需求优先级(priority)取值字段说明
为了兼容自定义优先级，`请使用 priority_label 字段`，详情参考：[如何兼容自定义优先级](/api-doc/API文档/subject/custom_priority/) 。
