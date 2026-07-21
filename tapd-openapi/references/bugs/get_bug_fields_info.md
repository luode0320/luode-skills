# 说明
返回缺陷所有字段及候选值(枚举值),即通常理解的字段的 "英文Key" 和 "中文值".


# url
`${TAPD_API_ENDPOINT}/bugs/get_fields_info`

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
| all_options | 否 | integer | 是否也返回已关闭的选项。all_options=1 则返回。默认是 0，不返回，与TAPD界面对齐 |  |

# 调用示例及返回结果
## 获取项目下的缺陷字段
### curl 使用 Basic Auth 鉴权调用示例
`curl -u 'api_user:api_password'  '${TAPD_API_ENDPOINT}/bugs/get_fields_info?workspace_id=10104801'`

### curl 使用 OAuth Access Token 鉴权调用示例
`curl -H 'Authorization: Bearer ACCESS_TOKEN'  '${TAPD_API_ENDPOINT}/bugs/get_fields_info?workspace_id=10104801'`

### 返回结果
```JSON
{
    "status": 1,
    "data": {
        "id": {
            "name": "id",
            "label": "ID",
            "options": [],
            "pure_options": [],
            "html_type": "input",
            "memo": ""
        },
        "title": {
            "name": "title",
            "label": "标题",
            "options": [],
            "pure_options": [],
            "html_type": "input",
            "memo": ""
        },
        "description": {
            "name": "description",
            "label": "详细描述",
            "options": [],
            "pure_options": [],
            "html_type": "rich_edit",
            "memo": ""
        },
        "module": {
            "name": "module",
            "label": "模块",
            "options": {
                "333": "333",
                "创建模块": "创建模块"
            },
            "pure_options": [],
            "html_type": "select",
            "memo": ""
        },
        "feature": {
            "name": "feature",
            "label": "特性",
            "options": {
                "tx1": "tx1"
            },
            "pure_options": [],
            "html_type": "select",
            "memo": ""
        },
        "reporter": {
            "name": "reporter",
            "label": "创建人",
            "options": [],
            "pure_options": [],
            "html_type": "user_chooser",
            "memo": ""
        },
        "deadline": {
            "name": "deadline",
            "label": "解决期限",
            "options": [],
            "pure_options": [],
            "html_type": "dateinput",
            "memo": ""
        },
        "created": {
            "name": "created",
            "label": "创建时间",
            "options": [],
            "pure_options": [],
            "html_type": "datetime",
            "memo": ""
        },
        "reopen_time": {
            "name": "reopen_time",
            "label": "重新打开时间",
            "options": [],
            "pure_options": [],
            "html_type": "datetime",
            "memo": ""
        },
        "closed": {
            "name": "closed",
            "label": "关闭时间",
            "options": [],
            "pure_options": [],
            "html_type": "datetime",
            "memo": ""
        },
        "modified": {
            "name": "modified",
            "label": "最后修改时间",
            "options": [],
            "pure_options": [],
            "html_type": "datetime",
            "memo": ""
        },
        "lastmodify": {
            "name": "lastmodify",
            "label": "最后修改人",
            "options": [],
            "pure_options": [],
            "html_type": "user_chooser",
            "memo": ""
        },
        "de": {
            "name": "de",
            "label": "开发人员",
            "options": [],
            "pure_options": [],
            "html_type": "user_chooser",
            "memo": ""
        },
        "te": {
            "name": "te",
            "label": "测试人员",
            "options": [],
            "pure_options": [],
            "html_type": "user_chooser",
            "memo": ""
        },
        "auditer": {
            "name": "auditer",
            "label": "审核人",
            "options": [],
            "pure_options": [],
            "html_type": "user_chooser",
            "memo": ""
        },
        "confirmer": {
            "name": "confirmer",
            "label": "验证人",
            "options": [],
            "pure_options": [],
            "html_type": "user_chooser",
            "memo": ""
        },
        "current_owner": {
            "name": "current_owner",
            "label": "处理人",
            "options": [],
            "pure_options": [],
            "html_type": "user_chooser",
            "memo": ""
        },
        "status": {
            "name": "status",
            "label": "状态",
            "options": {
                "new": "新",
                "in_progress": "接受/处理",
                "assigned": "已分配",
                "verified": "已验证",
                "postponed": "延期",
                "reopened": "重新打开",
                "resolved": "已解决",
                "rejected": "已拒绝",
                "closed": "已关闭x",
                "unconfirmed": "待确认的",
                "planning": "计划中",
                "feedback": "需要再次说明",
                "acknowledged": "已了解",
                "suspended": "挂起",
                "TM_audited": "TM审核",
                "PMM_audited": "PMM审核",
                "PM_audited": "PM审核",
                "QA_audited": "QA审核"
            },
            "pure_options": [],
            "html_type": "select",
            "memo": ""
        },
        "resolution": {
            "name": "resolution",
            "label": "解决方法",
            "options": {
                "ignore": "无需解决",
                "fixed": "已修改",
                "fix later": "延期解决",
                "failed to recur": "无法重现",
                "external reason": "外部原因",
                "duplicated": "重复",
                "intentional design": "设计如此",
                "unclear description ": "问题描述不准确",
                "feature change": "需求变更",
                "transferred to story": "已转需求",
                "hold": "挂起"
            },
            "pure_options": [],
            "html_type": "select",
            "memo": ""
        },
        "priority": {
            "name": "priority",
            "label": "优先级",
            "color_options": [
                {
                    "value": "urgent",
                    "label": "紧急",
                    "color": "#FF6770"
                },
                {
                    "value": "high",
                    "label": "高",
                    "color": "#FF6770"
                },
                {
                    "value": "medium",
                    "label": "中",
                    "color": "#28AB80"
                },
                {
                    "value": "low",
                    "label": "低",
                    "color": "#7C8597"
                },
                {
                    "value": "insignificant",
                    "label": "无关紧要",
                    "color": "#7C8597"
                }
            ],
            "pure_options": [],
            "html_type": "select",
            "memo": "",
            "options": {
                "urgent": "紧急",
                "high": "高",
                "medium": "中",
                "low": "低",
                "insignificant": "无关紧要"
            }
        },
        "severity": {
            "name": "severity",
            "label": "严重程度",
            "options": {
                "fatal": "致命",
                "serious": "严重",
                "normal": "一般",
                "prompt": "提示",
                "advice": "建议"
            },
            "pure_options": [],
            "html_type": "select",
            "memo": ""
        },
        "platform": {
            "name": "platform",
            "label": "软件平台",
            "options": {
                "PC": "PC",
                "其他": "其他"
            },
            "pure_options": [],
            "html_type": "select",
            "memo": ""
        },
        "os": {
            "name": "os",
            "label": "操作系统",
            "options": {
                "All": "All",
                "Windows XP": "Windows XP",
                "Windows 2000": "Windows 2000",
                "Windows NT": "Windows NT",
                "Linux": "Linux",
                "Unix": "Unix"
            },
            "pure_options": [],
            "html_type": "select",
            "memo": ""
        },
        "testmode": {
            "name": "testmode",
            "label": "测试方式",
            "options": {
                "手工测试": "手工测试",
                "自动化测试": "自动化测试"
            },
            "pure_options": [],
            "html_type": "select",
            "memo": ""
        },
        "testtype": {
            "name": "testtype",
            "label": "测试类型",
            "options": {
                "功能测试": "功能测试",
                "性能测试": "性能测试",
                "界面测试": "界面测试"
            },
            "pure_options": [],
            "html_type": "select",
            "memo": ""
        },
        "testphase": {
            "name": "testphase",
            "label": "测试阶段",
            "options": {
                "单元测试": "单元测试",
                "集成测试": "集成测试",
                "系统测试": "系统测试",
                "运营测试": "运营测试"
            },
            "pure_options": [],
            "html_type": "select",
            "memo": ""
        },
        "source": {
            "name": "source",
            "label": "缺陷根源",
            "options": {
                "需求": "需求",
                "设计": "设计",
                "编码": "编码",
                "其它": "其它"
            },
            "pure_options": [],
            "html_type": "select",
            "memo": ""
        },
        "frequency": {
            "name": "frequency",
            "label": "重现规律",
            "options": {
                "可重现": "可重现",
                "随机重现": "随机重现",
                "不可重现": "不可重现"
            },
            "pure_options": [],
            "html_type": "select",
            "memo": ""
        },
        "cc": {
            "name": "cc",
            "label": "抄送人",
            "options": [],
            "pure_options": [],
            "html_type": "mix_chooser",
            "memo": ""
        },
        "fixer": {
            "name": "fixer",
            "label": "修复人",
            "options": [],
            "pure_options": [],
            "html_type": "user_chooser",
            "memo": ""
        },
        "closer": {
            "name": "closer",
            "label": "关闭人",
            "options": [],
            "pure_options": [],
            "html_type": "user_chooser",
            "memo": ""
        },
        "participator": {
            "name": "participator",
            "label": "参与人",
            "options": [],
            "pure_options": [],
            "html_type": "user_chooser",
            "memo": ""
        },
        "version_report": {
            "name": "version_report",
            "label": "发现版本",
            "options": {
                "ver1.1": "ver1.1",
                "[v1.16.1]计费下单支付-支持渠道物品信息反查": "[v1.16.1]计费下单支付-支持渠道物品信息反查",
                "测试": "测试"
            },
            "pure_options": [],
            "html_type": "select",
            "memo": ""
        },
        "version_test": {
            "name": "version_test",
            "label": "验证版本",
            "options": {
                "ver1.1": "ver1.1",
                "[v1.16.1]计费下单支付-支持渠道物品信息反查": "[v1.16.1]计费下单支付-支持渠道物品信息反查",
                "测试": "测试"
            },
            "pure_options": [],
            "html_type": "select",
            "memo": ""
        },
        "version_fix": {
            "name": "version_fix",
            "label": "合入版本",
            "options": {
                "ver1.1": "ver1.1",
                "[v1.16.1]计费下单支付-支持渠道物品信息反查": "[v1.16.1]计费下单支付-支持渠道物品信息反查",
                "测试": "测试"
            },
            "pure_options": [],
            "html_type": "select",
            "memo": ""
        },
        "version_close": {
            "name": "version_close",
            "label": "关闭版本",
            "options": {
                "ver1.1": "ver1.1",
                "[v1.16.1]计费下单支付-支持渠道物品信息反查": "[v1.16.1]计费下单支付-支持渠道物品信息反查",
                "测试": "测试"
            },
            "pure_options": [],
            "html_type": "select",
            "memo": ""
        },
        "baseline_find": {
            "name": "baseline_find",
            "label": "发现基线",
            "options": [],
            "pure_options": [],
            "html_type": "select",
            "memo": ""
        },
        "baseline_join": {
            "name": "baseline_join",
            "label": "合入基线",
            "options": [],
            "pure_options": [],
            "html_type": "select",
            "memo": ""
        },
        "baseline_close": {
            "name": "baseline_close",
            "label": "关闭基线",
            "options": [],
            "pure_options": [],
            "html_type": "select",
            "memo": ""
        },
        "baseline_test": {
            "name": "baseline_test",
            "label": "验证基线",
            "options": [],
            "pure_options": [],
            "html_type": "select",
            "memo": ""
        },
        "originphase": {
            "name": "originphase",
            "label": "发现阶段",
            "options": {
                "需求阶段": "需求阶段",
                "架构阶段": "架构阶段",
                "设计阶段": "设计阶段",
                "编码阶段": "编码阶段",
                "测试阶段": "测试阶段",
                "上线阶段": "上线阶段"
            },
            "pure_options": [],
            "html_type": "select",
            "memo": ""
        },
        "sourcephase": {
            "name": "sourcephase",
            "label": "引入阶段",
            "options": {
                "需求阶段": "需求阶段",
                "架构阶段": "架构阶段",
                "设计阶段": "设计阶段",
                "编码阶段": "编码阶段",
                "测试阶段": "测试阶段",
                "集成阶段": "集成阶段"
            },
            "pure_options": [],
            "html_type": "select",
            "memo": ""
        },
        "bugtype": {
            "name": "bugtype",
            "label": "缺陷类型",
            "options": {
                "SQL注入": "SQL注入",
                "XSS": "XSS",
                "CSRF": "CSRF",
                "访问控制": "访问控制",
                "权限控制": "权限控制",
                "其它": "其它"
            },
            "pure_options": [],
            "html_type": "select",
            "memo": ""
        },
        "reject_time": {
            "name": "reject_time",
            "label": "拒绝时间",
            "options": [],
            "pure_options": [],
            "html_type": "datetime",
            "memo": ""
        },
        "in_progress_time": {
            "name": "in_progress_time",
            "label": "接受处理时间",
            "options": [],
            "pure_options": [],
            "html_type": "datetime",
            "memo": ""
        },
        "resolved": {
            "name": "resolved",
            "label": "解决时间",
            "options": [],
            "pure_options": [],
            "html_type": "datetime",
            "memo": ""
        },
        "verify_time": {
            "name": "verify_time",
            "label": "验证时间",
            "options": [],
            "pure_options": [],
            "html_type": "datetime",
            "memo": ""
        },
        "assigned_time": {
            "name": "assigned_time",
            "label": "分配时间",
            "options": [],
            "pure_options": [],
            "html_type": "datetime",
            "memo": ""
        },
        "iteration_id": {
            "name": "iteration_id",
            "label": "迭代",
            "options": {
                "1010104801001787437": "测试自定义字段",
                "1010104801001662155": "fromAPI",
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
            "pure_options": [
                {
                    "parent_id": "0",
                    "workspace_id": "10104801",
                    "sort": "120299600000",
                    "value": "1010104801001787437",
                    "label": "测试自定义字段",
                    "panel": 0
                },
                {
                    "parent_id": "0",
                    "workspace_id": "10104801",
                    "sort": "120299500000",
                    "value": "1010104801001662155",
                    "label": "fromAPI",
                    "panel": 0
                },
                {
                    "parent_id": "0",
                    "workspace_id": "10104801",
                    "sort": "120299400000",
                    "value": "1010104801001641399",
                    "label": "create by api",
                    "panel": 0
                },
                {
                    "parent_id": "0",
                    "workspace_id": "10104801",
                    "sort": "120299300000",
                    "value": "1010104801001641397",
                    "label": "页面新迭代",
                    "panel": 0
                },
                {
                    "parent_id": "0",
                    "workspace_id": "10104801",
                    "sort": "120299200000",
                    "value": "1010104801001595935",
                    "label": "锁定的迭代",
                    "panel": 0
                },
                {
                    "parent_id": "0",
                    "workspace_id": "10104801",
                    "sort": "117990900000",
                    "value": "1010104801001179909",
                    "label": "aaaassssss",
                    "panel": 0
                },
                {
                    "parent_id": "0",
                    "workspace_id": "10104801",
                    "sort": "120299100000",
                    "value": "1020419374001202991",
                    "label": "adra",
                    "panel": 0
                },
                {
                    "parent_id": "0",
                    "workspace_id": "10104801",
                    "sort": "117988700000",
                    "value": "1010104801001179887",
                    "label": "cjdd",
                    "panel": 0
                },
                {
                    "parent_id": "0",
                    "workspace_id": "10104801",
                    "sort": "110398500000",
                    "value": "1010104801001103985",
                    "label": "对对对",
                    "panel": 0
                },
                {
                    "parent_id": "0",
                    "workspace_id": "10104801",
                    "sort": "111222100000",
                    "value": "1010104801001112221",
                    "label": "myI",
                    "panel": 0
                },
                {
                    "parent_id": "0",
                    "workspace_id": "10104801",
                    "sort": "108091300000",
                    "value": "1010104801001080913",
                    "label": "【Word】191001常规发布",
                    "panel": 0
                },
                {
                    "parent_id": "0",
                    "workspace_id": "10104801",
                    "sort": "117106700000",
                    "value": "1010104801001171067",
                    "label": "oyctest20190911xxx1111",
                    "panel": 0
                },
                {
                    "parent_id": "0",
                    "workspace_id": "10104801",
                    "sort": "116980300000",
                    "value": "1010104801001169803",
                    "label": "oyctest20190911xxx1111",
                    "panel": 0
                },
                {
                    "parent_id": "0",
                    "workspace_id": "10104801",
                    "sort": "110596500000",
                    "value": "1010104801001105965",
                    "label": "oyctest20190911xxx1111",
                    "panel": 0
                },
                {
                    "parent_id": "0",
                    "workspace_id": "10104801",
                    "sort": "110519300000",
                    "value": "1010104801001105193",
                    "label": "oyctest20190911xxx1111",
                    "panel": 0
                },
                {
                    "parent_id": "0",
                    "workspace_id": "10104801",
                    "sort": "108201700000",
                    "value": "1010104801001082017",
                    "label": "日常发布",
                    "panel": 0
                },
                {
                    "parent_id": "0",
                    "workspace_id": "10104801",
                    "sort": "108201300000",
                    "value": "1010104801001082013",
                    "label": "日常发布",
                    "panel": 0
                },
                {
                    "parent_id": "0",
                    "workspace_id": "10104801",
                    "sort": "108189900000",
                    "value": "1010104801001081899",
                    "label": "oyctest20190917ABC2",
                    "panel": 0
                },
                {
                    "parent_id": "0",
                    "workspace_id": "10104801",
                    "sort": "108078300000",
                    "value": "1010104801001080783",
                    "label": "日常发布",
                    "panel": 0
                },
                {
                    "parent_id": "0",
                    "workspace_id": "10104801",
                    "sort": "112320700000",
                    "value": "1010104801001123207",
                    "label": "oyctest20190911",
                    "panel": 0
                },
                {
                    "parent_id": "0",
                    "workspace_id": "10104801",
                    "sort": "50768900000",
                    "value": "1010104801000507689",
                    "label": "i1",
                    "panel": 0
                },
                {
                    "parent_id": "0",
                    "workspace_id": "10104801",
                    "sort": "42318100000",
                    "value": "1010104801000423181",
                    "label": "迭代1",
                    "panel": 0
                },
                {
                    "parent_id": "0",
                    "workspace_id": "10104801",
                    "sort": "0",
                    "value": "1010104801001733159",
                    "label": "测试创建迭代2",
                    "panel": 0
                },
                {
                    "parent_id": "0",
                    "workspace_id": "10104801",
                    "sort": "0",
                    "value": "1010104801001628193",
                    "label": "API创建测试",
                    "panel": 0
                },
                {
                    "parent_id": "0",
                    "workspace_id": "10104801",
                    "sort": "0",
                    "value": "1010104801001628057",
                    "label": "测试创建迭代2",
                    "panel": 0
                },
                {
                    "parent_id": "0",
                    "workspace_id": "10104801",
                    "sort": "0",
                    "value": "1010104801001628055",
                    "label": "测试创建迭代",
                    "panel": 0
                }
            ],
            "html_type": "select",
            "lock_info": [],
            "memo": ""
        },
        "project_id": {
            "name": "project_id",
            "label": "所属项目",
            "options": {
                "10104801": "TAPD 乌云"
            },
            "pure_options": [],
            "html_type": "select",
            "memo": ""
        },
        "begin": {
            "name": "begin",
            "label": "预计开始",
            "options": [],
            "pure_options": [],
            "html_type": "dateinput",
            "memo": ""
        },
        "due": {
            "name": "due",
            "label": "预计结束",
            "options": [],
            "pure_options": [],
            "html_type": "dateinput",
            "memo": ""
        },
        "label": {
            "name": "label",
            "label": "标签",
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
            "pure_options": [],
            "html_type": "multi_select",
            "memo": ""
        },
        "size": {
            "name": "size",
            "label": "规模",
            "options": [],
            "pure_options": [],
            "html_type": "integer",
            "memo": ""
        },
        "effort": {
            "name": "effort",
            "label": "预估工时",
            "options": [],
            "pure_options": [],
            "html_type": "float",
            "memo": ""
        },
        "effort_completed": {
            "name": "effort_completed",
            "label": "完成工时",
            "options": [],
            "pure_options": [],
            "html_type": "float",
            "memo": ""
        },
        "remain": {
            "name": "remain",
            "label": "剩余工时",
            "options": [],
            "pure_options": [],
            "html_type": "float",
            "memo": ""
        },
        "exceed": {
            "name": "exceed",
            "label": "超出工时",
            "options": [],
            "pure_options": [],
            "html_type": "float",
            "memo": ""
        },
        "progress": {
            "name": "progress",
            "label": "进度",
            "options": [],
            "pure_options": [],
            "html_type": "input",
            "memo": ""
        },
        "estimate": {
            "name": "estimate",
            "label": "预计解决时间",
            "options": [],
            "pure_options": [],
            "html_type": "int",
            "memo": ""
        },
        "custom_field_four": {
            "name": "custom_field_four",
            "label": "文本的",
            "options": [],
            "pure_options": [],
            "html_type": "text",
            "memo": ""
        },
        "custom_field_one": {
            "name": "custom_field_one",
            "label": "测试下拉",
            "options": {
                "xxx": "xxx",
                "qqq": "qqq"
            },
            "pure_options": [],
            "html_type": "select",
            "memo": ""
        },
        "custom_field_two": {
            "name": "custom_field_two",
            "label": "测试字段",
            "options": [],
            "pure_options": [],
            "html_type": "text",
            "memo": ""
        },
        "custom_field_three": {
            "name": "custom_field_three",
            "label": "123",
            "options": [],
            "pure_options": [],
            "html_type": "text",
            "memo": ""
        },
        "custom_plan_field_1": {
            "name": "custom_plan_field_1",
            "label": "超级迭代",
            "options": {
                "1010104801001754573": "快速迭代1"
            },
            "pure_options": [
                {
                    "parent_id": "0",
                    "workspace_id": "10104801",
                    "sort": "120299600000",
                    "plan_app_id": "1010104801000000397",
                    "value": "1010104801001754573",
                    "label": "快速迭代1",
                    "panel": 0
                }
            ],
            "html_type": "select",
            "memo": ""
        },
        "custom_plan_field_2": {
            "name": "custom_plan_field_2",
            "label": "发布计划",
            "options": {
                "1010104801001934461": "v2test",
                "1010104801001934459": "test",
                "1010104801001934457": "发布",
                "1010104801001934455": "4324"
            },
            "pure_options": [
                {
                    "parent_id": "0",
                    "workspace_id": "10104801",
                    "sort": "120299700000",
                    "plan_app_id": "1010104801000085167",
                    "value": "1010104801001934461",
                    "label": "v2test",
                    "panel": 0
                },
                {
                    "parent_id": "0",
                    "workspace_id": "10104801",
                    "sort": "120299700000",
                    "plan_app_id": "1010104801000085167",
                    "value": "1010104801001934459",
                    "label": "test",
                    "panel": 0
                },
                {
                    "parent_id": "0",
                    "workspace_id": "10104801",
                    "sort": "120299700000",
                    "plan_app_id": "1010104801000085167",
                    "value": "1010104801001934457",
                    "label": "发布",
                    "panel": 0
                },
                {
                    "parent_id": "0",
                    "workspace_id": "10104801",
                    "sort": "120299700000",
                    "plan_app_id": "1010104801000085167",
                    "value": "1010104801001934455",
                    "label": "4324",
                    "panel": 0
                }
            ],
            "html_type": "select",
            "memo": ""
        },
        "priority_label": {
            "name": "priority_label",
            "label": "优先级",
            "color_options": [
                {
                    "value": "urgent",
                    "label": "紧急",
                    "color": "#FF6770"
                },
                {
                    "value": "high",
                    "label": "高",
                    "color": "#FF6770"
                },
                {
                    "value": "medium",
                    "label": "中",
                    "color": "#28AB80"
                },
                {
                    "value": "low",
                    "label": "低",
                    "color": "#7C8597"
                },
                {
                    "value": "insignificant",
                    "label": "无关紧要",
                    "color": "#7C8597"
                }
            ],
            "options": {
                "urgent": "紧急",
                "high": "高",
                "medium": "中",
                "low": "低",
                "insignificant": "无关紧要"
            },
            "pure_options": [],
            "html_type": "select",
            "memo": ""
        },
        "release_id": {
            "name": "release_id",
            "label": "发布计划",
            "options": {
                "1010104801000069739": "v2test",
                "1010104801000068721": "test",
                "1010104801000068405": "发布",
                "1010104801000058771": "4324"
            },
            "pure_options": [],
            "html_type": "select",
            "memo": ""
        }
    },
    "info": "success"
}
```
# 返回格式说明
| 字段 | 说明 |
|:----:|:----:|
| name | name |
| options | 候选值 |
| html_type | 类型 |
| label | 中文名称 |


# 返回候选值内容
|缺陷字段|说明|
|:----:|:----:|
| priority | 优先级 |
| severity | 严重程度 |
| status | 状态 枚举值 (可选值) |
| iteration_id | 迭代 枚举值 (可选值) |
| module | 模块 枚举值 (可选值) |
| release_id | 发布计划 枚举值 (可选值) |
| version_report | 发现版本 枚举值 (可选值) |
| version_test | 验证版本 枚举值 (可选值) |
| version_fix | 合入版本 枚举值 (可选值) |
| version_close | 关闭版本 枚举值 (可选值) |
| baseline_find | 发现基线 枚举值 (可选值) |
| baseline_join | 合入基线 枚举值 (可选值) |
| baseline_test | 验证基线 枚举值 (可选值)  |
| baseline_close | 关闭基线 枚举值 (可选值) |
| os | 操作系统 枚举值 (可选值) |
| platform | 软件平台 枚举值 (可选值) |
| testmode | 测试方式 枚举值 (可选值) |
| testphase | 测试阶段 枚举值 (可选值) |
| testtype | 测试类型 枚举值 (可选值) |
| source | 缺陷根源 枚举值 (可选值) |
| bugtype | 缺陷类型 枚举值 (可选值) |
| frequency | 重现规律 枚举值 (可选值) |
| originphase | 发现阶段 枚举值 (可选值) |
| sourcephase | 引入阶段 枚举值 (可选值)   |
| resolution | 解决方法 枚举值 (可选值) |
| custom_field_* | 解决方法 枚举值 (可选值) |


## 缺陷状态(status)可选值说明
status状态是支持每个项目单独配置的,所以状态(status)没有固定的中英文映射, 只能通过该接口获取.

## 缺陷优先级(priority)取值字段说明
为了兼容自定义优先级，`请使用 priority_label 字段`，详情参考：[如何兼容自定义优先级](/api-doc/API文档/subject/custom_priority/) 。


## 缺陷严重程度(severity)可选值说明
|取值|字面值|
|:----:|:----:|
| fatal | 致命 |
| serious | 严重 |
| normal | 一般 |
| prompt | 提示 |
| advice | 建议 |

## 缺陷解决方法(resolution)可选值说明
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
