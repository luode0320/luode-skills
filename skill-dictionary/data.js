window.SKILL_DICTIONARY = {
  "generated_at": "2026-03-28 22:10:55",
  "repo_root": "E:\\luode-skills",
  "plan_doc": "编码skill.md",
  "plan_doc_name": "编码skill.md",
  "summary": {
    "planned_total": 56,
    "implemented_total": 47,
    "planned_missing": 9,
    "seed_total": 0,
    "doc_total": 3,
    "references_total": 152,
    "agents_total": 47
  },
  "downloaded_seeds": {
    "path": "downloaded-seeds",
    "exists": true,
    "entry_count": 0,
    "entries": []
  },
  "domains": [
    {
      "id": "orchestration",
      "label": "总控层",
      "description": "流程分流、冲突裁决、阶段阻断",
      "order": 1,
      "implemented_count": 1,
      "planned_count": 0,
      "seed_count": 0,
      "total_count": 1,
      "items": [
        {
          "id": "team-development-rules",
          "name": "team-development-rules",
          "title": "团队研发总控规则",
          "status": "implemented",
          "status_label": "已实现",
          "domain_id": "orchestration",
          "domain_label": "总控层",
          "domain_description": "流程分流、冲突裁决、阶段阻断",
          "domain_order": 1,
          "item_order": 1,
          "auto_trigger": "当任务阶段不明确、领域边界不清、多个 skill 同时触发、流程需要暂停/重启/继续/终止，或用户明确要求按团队完整研发流程处理时触发。负责阶段分析、路由分流、冲突裁决和流程阻断；不要在单一明确的 SQL、API、配置、测试、评审等任务中触发。",
          "core_responsibility": "作为弱触发协调层，负责阶段分析、路由分流、冲突裁决和中断管控，不承载数据库、API、错误处理等细节规则，也不替代小 skill 执行。",
          "skill_path": "team-development-rules/SKILL.md",
          "directory_path": "team-development-rules",
          "directory": "team-development-rules",
          "sections": [
            "Skill 作用与适用场景",
            "自动触发信号",
            "进入后先做什么",
            "默认执行流程",
            "权责边界与不负责事项",
            "需要暂停并确认的条件",
            "执行通过 / 驳回标准",
            "执行结果归档要求",
            "references 读取规则"
          ],
          "references": [
            "team-development-rules/references/05-method-change-guard.md",
            "team-development-rules/references/conflict-examples.md",
            "team-development-rules/references/routing-rules.md",
            "team-development-rules/references/stage-blockers.md"
          ],
          "agents": [
            "team-development-rules/agents/openai.yaml"
          ],
          "has_license": false,
          "focus_points": [
            "优先检查 description 是否具体到触发信号，而不是只写抽象用途。",
            "检查 references 是否足以承接复杂场景，避免 SKILL.md 过厚或过空。",
            "重点看是否只做分流和阻断，没有越权覆盖单域 skill。"
          ]
        }
      ]
    },
    {
      "id": "requirement",
      "label": "需求域",
      "description": "需求澄清、缺口识别、边界确认、验收前置",
      "order": 2,
      "implemented_count": 6,
      "planned_count": 0,
      "seed_count": 0,
      "total_count": 6,
      "items": [
        {
          "id": "requirement-intake-rules",
          "name": "requirement-intake-rules",
          "title": "需求接入规则",
          "status": "implemented",
          "status_label": "已实现",
          "domain_id": "requirement",
          "domain_label": "需求域",
          "domain_description": "需求澄清、缺口识别、边界确认、验收前置",
          "domain_order": 2,
          "item_order": 1,
          "auto_trigger": "当用户提出新需求、新功能、新页面、新接口、新模块，且任务刚进入研发阶段、尚未进入实现或 Bug 定位时触发。支持从需求 URL、零散资料、物料和补充说明中整理需求，补齐到可进入后续代码开发的程度，并将结果沉淀到 `ment/` 目录；它同时定义需求域统一文档入口，同一需求后续只能持续更新这一份文档；不要用它代替需求缺口、边界、拆分、变更或验收标准类 skill。",
          "core_responsibility": "先理解目标、背景、上下游和输入输出。",
          "skill_path": "requirement-intake-rules/SKILL.md",
          "directory_path": "requirement-intake-rules",
          "directory": "requirement-intake-rules",
          "sections": [
            "Skill 作用与适用场景",
            "自动触发信号",
            "进入后先做什么",
            "默认执行流程",
            "权责边界与不负责事项",
            "需要暂停并确认的条件",
            "执行通过 / 驳回标准",
            "执行结果归档要求",
            "references 读取规则"
          ],
          "references": [
            "requirement-intake-rules/references/intake-boundaries-and-examples.md",
            "requirement-intake-rules/references/intake-checklist.md",
            "requirement-intake-rules/references/requirement-structure-template.md"
          ],
          "agents": [
            "requirement-intake-rules/agents/openai.yaml"
          ],
          "has_license": false,
          "focus_points": [
            "优先检查 description 是否具体到触发信号，而不是只写抽象用途。",
            "检查 references 是否足以承接复杂场景，避免 SKILL.md 过厚或过空。",
            "重点看是否能区分需求缺口、边界变化、验收偏差和历史 Bug。"
          ]
        },
        {
          "id": "requirement-gap-rules",
          "name": "requirement-gap-rules",
          "title": "需求缺口识别规则",
          "status": "implemented",
          "status_label": "已实现",
          "domain_id": "requirement",
          "domain_label": "需求域",
          "domain_description": "需求澄清、缺口识别、边界确认、验收前置",
          "domain_order": 2,
          "item_order": 2,
          "auto_trigger": "当需求描述不完整、缺少前提、缺少字段、缺少流程、缺少业务规则、缺少依赖条件或缺少验收信息时触发。负责识别需求缺口并在信息不足时阻断盲目编码推进，同时将缺口分析结果持续更新到 `requirement-intake-rules` 约定的同一个 `ment/` 需求文档中；不要用它代替需求边界判断、需求变更判断或验收标准细化 skill。",
          "core_responsibility": "识别缺失信息并暂停盲目实现。",
          "skill_path": "requirement-gap-rules/SKILL.md",
          "directory_path": "requirement-gap-rules",
          "directory": "requirement-gap-rules",
          "sections": [
            "Skill 作用与适用场景",
            "自动触发信号",
            "进入后先做什么",
            "默认执行流程",
            "权责边界与不负责事项",
            "需要暂停并确认的条件",
            "执行通过 / 驳回标准",
            "执行结果归档要求",
            "references 读取规则"
          ],
          "references": [
            "requirement-gap-rules/references/missing-info-checklist.md",
            "requirement-gap-rules/references/pause-triggers.md",
            "requirement-gap-rules/references/requirement-gap-examples.md"
          ],
          "agents": [
            "requirement-gap-rules/agents/openai.yaml"
          ],
          "has_license": false,
          "focus_points": [
            "优先检查 description 是否具体到触发信号，而不是只写抽象用途。",
            "检查 references 是否足以承接复杂场景，避免 SKILL.md 过厚或过空。",
            "重点看是否能区分需求缺口、边界变化、验收偏差和历史 Bug。"
          ]
        },
        {
          "id": "requirement-boundary-rules",
          "name": "requirement-boundary-rules",
          "title": "需求边界判定规则",
          "status": "implemented",
          "status_label": "已实现",
          "domain_id": "requirement",
          "domain_label": "需求域",
          "domain_description": "需求澄清、缺口识别、边界确认、验收前置",
          "domain_order": 2,
          "item_order": 3,
          "auto_trigger": "当需求边界不清、影响范围不明、兼容性不明确、是否允许改旧逻辑不清楚，或需要区分当前需求、历史问题、需求变更和验收偏差时触发。负责明确改动边界和影响面，并将边界结论持续更新到 `requirement-intake-rules` 约定的同一个 `ment/` 需求文档中；不要用它代替需求缺口识别或 Bug 根因定位 skill。",
          "core_responsibility": "明确改动边界和影响面。",
          "skill_path": "requirement-boundary-rules/SKILL.md",
          "directory_path": "requirement-boundary-rules",
          "directory": "requirement-boundary-rules",
          "sections": [
            "Skill 作用与适用场景",
            "自动触发信号",
            "进入后先做什么",
            "默认执行流程",
            "权责边界与不负责事项",
            "需要暂停并确认的条件",
            "执行通过 / 驳回标准",
            "执行结果归档要求",
            "references 读取规则"
          ],
          "references": [
            "requirement-boundary-rules/references/acceptance-routing-examples.md",
            "requirement-boundary-rules/references/boundary-checklist.md",
            "requirement-boundary-rules/references/history-vs-change.md"
          ],
          "agents": [
            "requirement-boundary-rules/agents/openai.yaml"
          ],
          "has_license": false,
          "focus_points": [
            "优先检查 description 是否具体到触发信号，而不是只写抽象用途。",
            "检查 references 是否足以承接复杂场景，避免 SKILL.md 过厚或过空。",
            "重点看是否能区分需求缺口、边界变化、验收偏差和历史 Bug。"
          ]
        },
        {
          "id": "requirement-splitting-rules",
          "name": "requirement-splitting-rules",
          "title": "需求拆分规则",
          "status": "implemented",
          "status_label": "已实现",
          "domain_id": "requirement",
          "domain_label": "需求域",
          "domain_description": "需求澄清、缺口识别、边界确认、验收前置",
          "domain_order": 2,
          "item_order": 4,
          "auto_trigger": "当需求较大、涉及多个模块、多个接口、多个页面、多个步骤或多个角色协作，无法作为单一实现单元稳定推进时触发。负责拆出任务边界、实施顺序和最小闭环，并将拆分结果持续更新到 `requirement-intake-rules` 约定的同一个 `ment/` 需求文档中；不要用它代替需求接入、边界确认或项目排期管理。",
          "core_responsibility": "负责任务拆分、模块拆分和实施顺序。",
          "skill_path": "requirement-splitting-rules/SKILL.md",
          "directory_path": "requirement-splitting-rules",
          "directory": "requirement-splitting-rules",
          "sections": [
            "Skill 作用与适用场景",
            "自动触发信号",
            "进入后先做什么",
            "默认执行流程",
            "权责边界与不负责事项",
            "需要暂停并确认的条件",
            "执行通过 / 驳回标准",
            "执行结果归档要求",
            "references 读取规则"
          ],
          "references": [
            "requirement-splitting-rules/references/splitting-dimensions.md",
            "requirement-splitting-rules/references/splitting-examples.md",
            "requirement-splitting-rules/references/splitting-sequence.md"
          ],
          "agents": [
            "requirement-splitting-rules/agents/openai.yaml"
          ],
          "has_license": false,
          "focus_points": [
            "优先检查 description 是否具体到触发信号，而不是只写抽象用途。",
            "检查 references 是否足以承接复杂场景，避免 SKILL.md 过厚或过空。",
            "重点看是否能区分需求缺口、边界变化、验收偏差和历史 Bug。"
          ]
        },
        {
          "id": "requirement-change-rules",
          "name": "requirement-change-rules",
          "title": "需求变更确认规则",
          "status": "implemented",
          "status_label": "已实现",
          "domain_id": "requirement",
          "domain_label": "需求域",
          "domain_description": "需求澄清、缺口识别、边界确认、验收前置",
          "domain_order": 2,
          "item_order": 5,
          "auto_trigger": "当编码过程中需求被补充、修正、插入新条件、改变优先级、调整默认值或交付物形态时触发。负责识别变更类型、重算影响范围和决定是否需要回退前序结论，并将变更结果持续更新到 `requirement-intake-rules` 约定的同一个 `ment/` 需求文档中；不要把历史缺陷误当成需求变更。",
          "core_responsibility": "重新确认变更范围和影响。",
          "skill_path": "requirement-change-rules/SKILL.md",
          "directory_path": "requirement-change-rules",
          "directory": "requirement-change-rules",
          "sections": [
            "Skill 作用与适用场景",
            "自动触发信号",
            "进入后先做什么",
            "默认执行流程",
            "权责边界与不负责事项",
            "需要暂停并确认的条件",
            "执行通过 / 驳回标准",
            "执行结果归档要求",
            "references 读取规则"
          ],
          "references": [
            "requirement-change-rules/references/change-classification.md",
            "requirement-change-rules/references/change-decision-examples.md",
            "requirement-change-rules/references/impact-recheck.md"
          ],
          "agents": [
            "requirement-change-rules/agents/openai.yaml"
          ],
          "has_license": false,
          "focus_points": [
            "优先检查 description 是否具体到触发信号，而不是只写抽象用途。",
            "检查 references 是否足以承接复杂场景，避免 SKILL.md 过厚或过空。",
            "重点看是否能区分需求缺口、边界变化、验收偏差和历史 Bug。"
          ]
        },
        {
          "id": "acceptance-criteria-rules",
          "name": "acceptance-criteria-rules",
          "title": "验收标准细化规则",
          "status": "implemented",
          "status_label": "已实现",
          "domain_id": "requirement",
          "domain_label": "需求域",
          "domain_description": "需求澄清、缺口识别、边界确认、验收前置",
          "domain_order": 2,
          "item_order": 6,
          "auto_trigger": "当任务准备进入实现前确认，或交付前需要把“做到什么算完成”写成可验证、可测试、可复核的标准时触发。负责细化成功条件、异常条件、边界条件和不在范围项，并将验收标准单独保存到 `ment/` 下的验收文档中；不要用它代替功能验证或回归验证。",
          "core_responsibility": "补齐可验证、可测试的验收标准。",
          "skill_path": "acceptance-criteria-rules/SKILL.md",
          "directory_path": "acceptance-criteria-rules",
          "directory": "acceptance-criteria-rules",
          "sections": [
            "Skill 作用与适用场景",
            "自动触发信号",
            "进入后先做什么",
            "默认执行流程",
            "权责边界与不负责事项",
            "需要暂停并确认的条件",
            "执行通过 / 驳回标准",
            "执行结果归档要求",
            "references 读取规则"
          ],
          "references": [
            "acceptance-criteria-rules/references/acceptance-boundaries.md",
            "acceptance-criteria-rules/references/acceptance-template.md",
            "acceptance-criteria-rules/references/testable-criteria-checklist.md"
          ],
          "agents": [
            "acceptance-criteria-rules/agents/openai.yaml"
          ],
          "has_license": false,
          "focus_points": [
            "优先检查 description 是否具体到触发信号，而不是只写抽象用途。",
            "检查 references 是否足以承接复杂场景，避免 SKILL.md 过厚或过空。",
            "重点看是否能区分需求缺口、边界变化、验收偏差和历史 Bug。"
          ]
        }
      ]
    },
    {
      "id": "bug",
      "label": "Bug 域",
      "description": "问题录入、定位、运行时诊断、修复建议",
      "order": 3,
      "implemented_count": 10,
      "planned_count": 1,
      "seed_count": 0,
      "total_count": 11,
      "items": [
        {
          "id": "bug-intake-rules",
          "name": "bug-intake-rules",
          "title": "Bug 问题录入规则",
          "status": "implemented",
          "status_label": "已实现",
          "domain_id": "bug",
          "domain_label": "Bug 域",
          "domain_description": "问题录入、定位、运行时诊断、修复建议",
          "domain_order": 3,
          "item_order": 1,
          "auto_trigger": "当用户描述报错、异常行为、结果不符、线上问题、偶发问题、接口异常、页面异常、数据错误或性能异常时触发。负责把 Bug 描述标准化，整理现象、影响范围、环境条件、期望结果和实际结果，并统一建立 Bug 根目录记录；不要用它代替根因定位、运行时调试或修复方案制定 skill。",
          "core_responsibility": "把问题描述标准化。",
          "skill_path": "bug-intake-rules/SKILL.md",
          "directory_path": "bug-intake-rules",
          "directory": "bug-intake-rules",
          "sections": [
            "Skill 作用与适用场景",
            "自动触发信号",
            "进入后先做什么",
            "默认执行流程",
            "权责边界与不负责事项",
            "需要暂停并确认的条件",
            "执行通过 / 驳回标准",
            "执行结果归档要求",
            "references 读取规则"
          ],
          "references": [
            "bug-intake-rules/references/bug-description-template.md",
            "bug-intake-rules/references/intake-examples.md",
            "bug-intake-rules/references/minimum-intake-fields.md"
          ],
          "agents": [
            "bug-intake-rules/agents/openai.yaml"
          ],
          "has_license": false,
          "focus_points": [
            "优先检查 description 是否具体到触发信号，而不是只写抽象用途。",
            "检查 references 是否足以承接复杂场景，避免 SKILL.md 过厚或过空。",
            "重点看静态定位与运行时诊断的切换条件是否清楚。"
          ]
        },
        {
          "id": "bug-gap-rules",
          "name": "bug-gap-rules",
          "title": "Bug 缺口识别规则",
          "status": "implemented",
          "status_label": "已实现",
          "domain_id": "bug",
          "domain_label": "Bug 域",
          "domain_description": "问题录入、定位、运行时诊断、修复建议",
          "domain_order": 3,
          "item_order": 2,
          "auto_trigger": "当 Bug 描述缺少复现条件、环境信息、输入数据、报错日志、影响范围或关键时间线，导致后续复现与定位无法可靠推进时触发。负责识别缺失项、区分阻断级与非阻断级缺口，并统一记录到 Bug 根目录，阻止盲目进入定位。",
          "core_responsibility": "补齐定位所需基础信息。",
          "skill_path": "bug-gap-rules/SKILL.md",
          "directory_path": "bug-gap-rules",
          "directory": "bug-gap-rules",
          "sections": [
            "Skill 作用与适用场景",
            "自动触发信号",
            "进入后先做什么",
            "默认执行流程",
            "权责边界与不负责事项",
            "需要暂停并确认的条件",
            "执行通过 / 驳回标准",
            "执行结果归档要求",
            "references 读取规则"
          ],
          "references": [
            "bug-gap-rules/references/blocking-signals.md",
            "bug-gap-rules/references/gap-checklist.md",
            "bug-gap-rules/references/gap-examples.md"
          ],
          "agents": [
            "bug-gap-rules/agents/openai.yaml"
          ],
          "has_license": false,
          "focus_points": [
            "优先检查 description 是否具体到触发信号，而不是只写抽象用途。",
            "检查 references 是否足以承接复杂场景，避免 SKILL.md 过厚或过空。",
            "重点看静态定位与运行时诊断的切换条件是否清楚。"
          ]
        },
        {
          "id": "bug-reproduction-rules",
          "name": "bug-reproduction-rules",
          "title": "Bug 复现规则",
          "status": "implemented",
          "status_label": "已实现",
          "domain_id": "bug",
          "domain_label": "Bug 域",
          "domain_description": "问题录入、定位、运行时诊断、修复建议",
          "domain_order": 3,
          "item_order": 3,
          "auto_trigger": "当问题需要构造步骤、确定触发条件、判断是否稳定发生、确认出现频率或复现环境时触发。负责输出复现路径、稳定性判断、Bug 根目录记录和无法复现时的结论处理；不要用它代替根因分析。",
          "core_responsibility": "输出复现步骤和复现结论。",
          "skill_path": "bug-reproduction-rules/SKILL.md",
          "directory_path": "bug-reproduction-rules",
          "directory": "bug-reproduction-rules",
          "sections": [
            "Skill 作用与适用场景",
            "自动触发信号",
            "进入后先做什么",
            "默认执行流程",
            "权责边界与不负责事项",
            "需要暂停并确认的条件",
            "执行通过 / 驳回标准",
            "执行结果归档要求",
            "references 读取规则"
          ],
          "references": [
            "bug-reproduction-rules/references/reproduction-examples.md",
            "bug-reproduction-rules/references/reproduction-template.md",
            "bug-reproduction-rules/references/stability-checks.md"
          ],
          "agents": [
            "bug-reproduction-rules/agents/openai.yaml"
          ],
          "has_license": false,
          "focus_points": [
            "优先检查 description 是否具体到触发信号，而不是只写抽象用途。",
            "检查 references 是否足以承接复杂场景，避免 SKILL.md 过厚或过空。",
            "重点看静态定位与运行时诊断的切换条件是否清楚。"
          ]
        },
        {
          "id": "bug-scoping-rules",
          "name": "bug-scoping-rules",
          "title": "bug-scoping-rules",
          "status": "planned",
          "status_label": "规划中",
          "domain_id": "bug",
          "domain_label": "Bug 域",
          "domain_description": "问题录入、定位、运行时诊断、修复建议",
          "domain_order": 3,
          "item_order": 4,
          "auto_trigger": "当需要判断问题属于哪个模块、哪个业务链路、哪个服务、哪个页面、哪个接口、哪个数据流时自动触发。",
          "core_responsibility": "明确问题归属和影响范围。",
          "skill_path": "",
          "directory_path": "",
          "directory": "",
          "sections": [],
          "references": [],
          "agents": [],
          "has_license": false,
          "focus_points": [
            "先补齐触发 description、邻接边界和最小 references，再决定是否正式建目录。",
            "优先确认它与同域相邻 skill 的拆分边界，避免新建后职责重叠。",
            "重点看静态定位与运行时诊断的切换条件是否清楚。"
          ]
        },
        {
          "id": "bug-root-cause-rules",
          "name": "bug-root-cause-rules",
          "title": "Bug 根因定位规则",
          "status": "implemented",
          "status_label": "已实现",
          "domain_id": "bug",
          "domain_label": "Bug 域",
          "domain_description": "问题录入、定位、运行时诊断、修复建议",
          "domain_order": 3,
          "item_order": 5,
          "auto_trigger": "当开始分析代码、追调用链、看现有日志、查 trace、结合上下游行为定位 Bug 根因时触发。负责通过静态证据收敛根因、统一记录到 Bug 根目录并区分实现问题与设计问题；不要用它代替运行时调试或修复方案制定 skill。",
          "core_responsibility": "找出根因并区分实现问题与设计问题。",
          "skill_path": "bug-root-cause-rules/SKILL.md",
          "directory_path": "bug-root-cause-rules",
          "directory": "bug-root-cause-rules",
          "sections": [
            "Skill 作用与适用场景",
            "自动触发信号",
            "进入后先做什么",
            "默认执行流程",
            "权责边界与不负责事项",
            "需要暂停并确认的条件",
            "执行通过 / 驳回标准",
            "执行结果归档要求",
            "references 读取规则"
          ],
          "references": [
            "bug-root-cause-rules/references/root-cause-evidence.md",
            "bug-root-cause-rules/references/static-analysis-path.md",
            "bug-root-cause-rules/references/when-to-stop-static-analysis.md"
          ],
          "agents": [
            "bug-root-cause-rules/agents/openai.yaml"
          ],
          "has_license": false,
          "focus_points": [
            "优先检查 description 是否具体到触发信号，而不是只写抽象用途。",
            "检查 references 是否足以承接复杂场景，避免 SKILL.md 过厚或过空。",
            "重点看静态定位与运行时诊断的切换条件是否清楚。"
          ]
        },
        {
          "id": "bug-runtime-debug-rules",
          "name": "bug-runtime-debug-rules",
          "title": "Bug 运行时诊断规则",
          "status": "implemented",
          "status_label": "已实现",
          "domain_id": "bug",
          "domain_label": "Bug 域",
          "domain_description": "问题录入、定位、运行时诊断、修复建议",
          "domain_order": 3,
          "item_order": 6,
          "auto_trigger": "当仅靠静态分析不能稳定定位 Bug，且需要在运行过程中通过断点、单步执行、变量观察、调用栈观察、条件命中判断、debug 日志或运行时证据来缩小问题范围时触发。负责运行时诊断进入条件、观察方式、退出条件和证据回流；不要把它当成默认第一选择。",
          "core_responsibility": "通过运行时调试缩小问题范围并定位异常位置。",
          "skill_path": "bug-runtime-debug-rules/SKILL.md",
          "directory_path": "bug-runtime-debug-rules",
          "directory": "bug-runtime-debug-rules",
          "sections": [
            "Skill 作用与适用场景",
            "自动触发信号",
            "进入后先做什么",
            "默认执行流程",
            "权责边界与不负责事项",
            "需要暂停并确认的条件",
            "执行通过 / 驳回标准",
            "执行结果归档要求",
            "references 读取规则"
          ],
          "references": [
            "bug-runtime-debug-rules/references/runtime-entry-conditions.md",
            "bug-runtime-debug-rules/references/runtime-exit-and-handoff.md",
            "bug-runtime-debug-rules/references/runtime-observation-methods.md"
          ],
          "agents": [
            "bug-runtime-debug-rules/agents/openai.yaml"
          ],
          "has_license": false,
          "focus_points": [
            "优先检查 description 是否具体到触发信号，而不是只写抽象用途。",
            "检查 references 是否足以承接复杂场景，避免 SKILL.md 过厚或过空。",
            "重点看静态定位与运行时诊断的切换条件是否清楚。"
          ]
        },
        {
          "id": "bug-debug-log-rules",
          "name": "bug-debug-log-rules",
          "title": "Bug 调试日志规则",
          "status": "implemented",
          "status_label": "已实现",
          "domain_id": "bug",
          "domain_label": "Bug 域",
          "domain_description": "问题录入、定位、运行时诊断、修复建议",
          "domain_order": 3,
          "item_order": 7,
          "auto_trigger": "当定位 Bug 需要临时增加 debug 日志、关键变量输出、关键分支日志、上下游输入输出日志或时间线日志来补充运行时证据时触发。负责日志落点、日志粒度、Bug 根目录记录、可回收性和清理要求；不要把临时诊断日志混成正式日志策略。",
          "core_responsibility": "通过可回收的临时日志补充运行期证据。",
          "skill_path": "bug-debug-log-rules/SKILL.md",
          "directory_path": "bug-debug-log-rules",
          "directory": "bug-debug-log-rules",
          "sections": [
            "Skill 作用与适用场景",
            "自动触发信号",
            "进入后先做什么",
            "默认执行流程",
            "权责边界与不负责事项",
            "需要暂停并确认的条件",
            "执行通过 / 驳回标准",
            "执行结果归档要求",
            "references 读取规则"
          ],
          "references": [
            "bug-debug-log-rules/references/debug-log-cleanup.md",
            "bug-debug-log-rules/references/debug-log-examples.md",
            "bug-debug-log-rules/references/debug-log-placement.md"
          ],
          "agents": [
            "bug-debug-log-rules/agents/openai.yaml"
          ],
          "has_license": false,
          "focus_points": [
            "优先检查 description 是否具体到触发信号，而不是只写抽象用途。",
            "检查 references 是否足以承接复杂场景，避免 SKILL.md 过厚或过空。",
            "重点看静态定位与运行时诊断的切换条件是否清楚。"
          ]
        },
        {
          "id": "bug-assertion-diagnostic-rules",
          "name": "bug-assertion-diagnostic-rules",
          "title": "Bug 断言诊断规则",
          "status": "implemented",
          "status_label": "已实现",
          "domain_id": "bug",
          "domain_label": "Bug 域",
          "domain_description": "问题录入、定位、运行时诊断、修复建议",
          "domain_order": 3,
          "item_order": 8,
          "auto_trigger": "当怀疑状态异常、顺序错误、数据污染、不变量被破坏，且需要通过程序断言、诊断性检查、快速失败或区间收缩来暴露问题位置时触发。负责断言进入条件、放置位置、Bug 根目录记录和删除收口要求；不要把诊断断言长期留作正式业务逻辑。",
          "core_responsibility": "用断言和诊断检查缩小 bug 发生区间。",
          "skill_path": "bug-assertion-diagnostic-rules/SKILL.md",
          "directory_path": "bug-assertion-diagnostic-rules",
          "directory": "bug-assertion-diagnostic-rules",
          "sections": [
            "Skill 作用与适用场景",
            "自动触发信号",
            "进入后先做什么",
            "默认执行流程",
            "权责边界与不负责事项",
            "需要暂停并确认的条件",
            "执行通过 / 驳回标准",
            "执行结果归档要求",
            "references 读取规则"
          ],
          "references": [
            "bug-assertion-diagnostic-rules/references/assertion-entry-conditions.md",
            "bug-assertion-diagnostic-rules/references/assertion-examples.md",
            "bug-assertion-diagnostic-rules/references/assertion-placement.md"
          ],
          "agents": [
            "bug-assertion-diagnostic-rules/agents/openai.yaml"
          ],
          "has_license": false,
          "focus_points": [
            "优先检查 description 是否具体到触发信号，而不是只写抽象用途。",
            "检查 references 是否足以承接复杂场景，避免 SKILL.md 过厚或过空。",
            "重点看静态定位与运行时诊断的切换条件是否清楚。"
          ]
        },
        {
          "id": "bug-fix-proposal-rules",
          "name": "bug-fix-proposal-rules",
          "title": "Bug 修复建议规则",
          "status": "implemented",
          "status_label": "已实现",
          "domain_id": "bug",
          "domain_label": "Bug 域",
          "domain_description": "问题录入、定位、运行时诊断、修复建议",
          "domain_order": 3,
          "item_order": 9,
          "auto_trigger": "当问题已定位，需要形成修改建议、风险评估、备选方案并判断是否应等待用户确认时触发。负责把 Bug 域稳定交接到编码域，并统一记录到 Bug 根目录；不要用它代替根因定位或直接实施编码修复。",
          "core_responsibility": "先给修改建议，再决定是否实施。",
          "skill_path": "bug-fix-proposal-rules/SKILL.md",
          "directory_path": "bug-fix-proposal-rules",
          "directory": "bug-fix-proposal-rules",
          "sections": [
            "Skill 作用与适用场景",
            "自动触发信号",
            "进入后先做什么",
            "默认执行流程",
            "权责边界与不负责事项",
            "需要暂停并确认的条件",
            "执行通过 / 驳回标准",
            "执行结果归档要求",
            "references 读取规则"
          ],
          "references": [
            "bug-fix-proposal-rules/references/confirm-before-coding.md",
            "bug-fix-proposal-rules/references/fix-proposal-template.md",
            "bug-fix-proposal-rules/references/risk-assessment-checklist.md"
          ],
          "agents": [
            "bug-fix-proposal-rules/agents/openai.yaml"
          ],
          "has_license": false,
          "focus_points": [
            "优先检查 description 是否具体到触发信号，而不是只写抽象用途。",
            "检查 references 是否足以承接复杂场景，避免 SKILL.md 过厚或过空。",
            "重点看静态定位与运行时诊断的切换条件是否清楚。"
          ]
        },
        {
          "id": "bug-regression-risk-rules",
          "name": "bug-regression-risk-rules",
          "title": "Bug 回归风险规则",
          "status": "implemented",
          "status_label": "已实现",
          "domain_id": "bug",
          "domain_label": "Bug 域",
          "domain_description": "问题录入、定位、运行时诊断、修复建议",
          "domain_order": 3,
          "item_order": 10,
          "auto_trigger": "当 Bug 修复可能影响公共方法、共享模块、已有接口、数据库行为、缓存行为、兼容性或其他历史能力时触发。负责识别回归风险点、风险等级、验证优先级并统一记录到 Bug 根目录；不要把它代替实际回归测试。",
          "core_responsibility": "识别回归风险。",
          "skill_path": "bug-regression-risk-rules/SKILL.md",
          "directory_path": "bug-regression-risk-rules",
          "directory": "bug-regression-risk-rules",
          "sections": [
            "Skill 作用与适用场景",
            "自动触发信号",
            "进入后先做什么",
            "默认执行流程",
            "权责边界与不负责事项",
            "需要暂停并确认的条件",
            "执行通过 / 驳回标准",
            "执行结果归档要求",
            "references 读取规则"
          ],
          "references": [
            "bug-regression-risk-rules/references/risk-dimensions.md",
            "bug-regression-risk-rules/references/risk-examples.md",
            "bug-regression-risk-rules/references/risk-ranking-and-scope.md"
          ],
          "agents": [
            "bug-regression-risk-rules/agents/openai.yaml"
          ],
          "has_license": false,
          "focus_points": [
            "优先检查 description 是否具体到触发信号，而不是只写抽象用途。",
            "检查 references 是否足以承接复杂场景，避免 SKILL.md 过厚或过空。",
            "重点看静态定位与运行时诊断的切换条件是否清楚。"
          ]
        },
        {
          "id": "bug-validation-rules",
          "name": "bug-validation-rules",
          "title": "Bug 修复验证规则",
          "status": "implemented",
          "status_label": "已实现",
          "domain_id": "bug",
          "domain_label": "Bug 域",
          "domain_description": "问题录入、定位、运行时诊断、修复建议",
          "domain_order": 3,
          "item_order": 11,
          "auto_trigger": "当 Bug 修复后需要验证是否真的修好、是否引入副作用、是否需要补测试样例、是否已经满足关闭条件时触发。负责修复后验证闭环、Bug 根目录结论记录和未覆盖说明；不要把它代替功能实现验证或全量回归策略。",
          "core_responsibility": "负责修复后的验证闭环。",
          "skill_path": "bug-validation-rules/SKILL.md",
          "directory_path": "bug-validation-rules",
          "directory": "bug-validation-rules",
          "sections": [
            "Skill 作用与适用场景",
            "自动触发信号",
            "进入后先做什么",
            "默认执行流程",
            "权责边界与不负责事项",
            "需要暂停并确认的条件",
            "执行通过 / 驳回标准",
            "执行结果归档要求",
            "references 读取规则"
          ],
          "references": [
            "bug-validation-rules/references/validation-boundaries.md",
            "bug-validation-rules/references/validation-checklist.md",
            "bug-validation-rules/references/validation-template.md"
          ],
          "agents": [
            "bug-validation-rules/agents/openai.yaml"
          ],
          "has_license": false,
          "focus_points": [
            "优先检查 description 是否具体到触发信号，而不是只写抽象用途。",
            "检查 references 是否足以承接复杂场景，避免 SKILL.md 过厚或过空。",
            "重点看静态定位与运行时诊断的切换条件是否清楚。"
          ]
        }
      ]
    },
    {
      "id": "baseline",
      "label": "编码基线域",
      "description": "开始编码即并行生效的基础质量规则",
      "order": 4,
      "implemented_count": 6,
      "planned_count": 0,
      "seed_count": 0,
      "total_count": 6,
      "items": [
        {
          "id": "code-minimal-change-rules",
          "name": "code-minimal-change-rules",
          "title": "最小改动编码规则",
          "status": "implemented",
          "status_label": "已实现",
          "domain_id": "baseline",
          "domain_label": "编码基线域",
          "domain_description": "开始编码即并行生效的基础质量规则",
          "domain_order": 4,
          "item_order": 1,
          "auto_trigger": "当新增或修改代码、调整功能、修复 Bug、补测试支撑代码或整理实现细节时触发。负责约束改动范围、删除无关修改并保持变更聚焦；不要用它代替可读性、风格一致性、代码归位或测试规范等相邻 skill。",
          "core_responsibility": "严控代码变更范围，杜绝无关修改、冗余改动和过度优化，保证每次变更聚焦单一目标，降低回归风险和排查难度。",
          "skill_path": "code-minimal-change-rules/SKILL.md",
          "directory_path": "code-minimal-change-rules",
          "directory": "code-minimal-change-rules",
          "sections": [
            "Skill 作用与适用场景",
            "自动触发信号",
            "进入后先做什么",
            "默认执行流程",
            "权责边界与不负责事项",
            "需要暂停并确认的条件",
            "执行通过 / 驳回标准",
            "执行结果归档要求",
            "references 读取规则"
          ],
          "references": [
            "code-minimal-change-rules/references/minimal-change-boundaries.md",
            "code-minimal-change-rules/references/minimal-change-examples.md",
            "code-minimal-change-rules/references/minimal-change-general.md"
          ],
          "agents": [
            "code-minimal-change-rules/agents/openai.yaml"
          ],
          "has_license": false,
          "focus_points": [
            "优先检查 description 是否具体到触发信号，而不是只写抽象用途。",
            "检查 references 是否足以承接复杂场景，避免 SKILL.md 过厚或过空。",
            "重点看它是否能并行生效，并且不抢位点域或审查域职责。"
          ]
        },
        {
          "id": "code-readability-rules",
          "name": "code-readability-rules",
          "title": "代码可读性规则",
          "status": "implemented",
          "status_label": "已实现",
          "domain_id": "baseline",
          "domain_label": "编码基线域",
          "domain_description": "开始编码即并行生效的基础质量规则",
          "domain_order": 4,
          "item_order": 2,
          "auto_trigger": "当新增或修改业务代码、工具代码、服务代码、脚本代码或 Bug 修复逻辑时触发。负责约束函数结构、逻辑顺序、复杂度和可维护性；不要用它代替最小改动、风格一致性、注释规则或代码归位规则。",
          "core_responsibility": "保证函数结构清晰、逻辑顺序自然、复杂度可控。",
          "skill_path": "code-readability-rules/SKILL.md",
          "directory_path": "code-readability-rules",
          "directory": "code-readability-rules",
          "sections": [
            "Skill 作用与适用场景",
            "自动触发信号",
            "进入后先做什么",
            "默认执行流程",
            "权责边界与不负责事项",
            "需要暂停并确认的条件",
            "执行通过 / 驳回标准",
            "执行结果归档要求",
            "references 读取规则"
          ],
          "references": [
            "code-readability-rules/references/function-structure-rules.md",
            "code-readability-rules/references/readability-examples.md",
            "code-readability-rules/references/readability-general.md"
          ],
          "agents": [
            "code-readability-rules/agents/openai.yaml"
          ],
          "has_license": false,
          "focus_points": [
            "优先检查 description 是否具体到触发信号，而不是只写抽象用途。",
            "检查 references 是否足以承接复杂场景，避免 SKILL.md 过厚或过空。",
            "重点看它是否能并行生效，并且不抢位点域或审查域职责。"
          ]
        },
        {
          "id": "code-style-consistency-rules",
          "name": "code-style-consistency-rules",
          "title": "代码风格一致性规则",
          "status": "implemented",
          "status_label": "已实现",
          "domain_id": "baseline",
          "domain_label": "编码基线域",
          "domain_description": "开始编码即并行生效的基础质量规则",
          "domain_order": 4,
          "item_order": 3,
          "auto_trigger": "当新增或修改任意代码文件、脚本文件、配置型代码或测试代码时触发。负责跟随项目现有写法，避免局部风格跳变和个人偏好入侵；不要用它代替最小改动、可读性、注释规范或代码归位规则。",
          "core_responsibility": "跟随项目现有风格，不引入风格跳变。",
          "skill_path": "code-style-consistency-rules/SKILL.md",
          "directory_path": "code-style-consistency-rules",
          "directory": "code-style-consistency-rules",
          "sections": [
            "Skill 作用与适用场景",
            "自动触发信号",
            "进入后先做什么",
            "默认执行流程",
            "权责边界与不负责事项",
            "需要暂停并确认的条件",
            "执行通过 / 驳回标准",
            "执行结果归档要求",
            "references 读取规则"
          ],
          "references": [
            "code-style-consistency-rules/references/consistency-examples.md",
            "code-style-consistency-rules/references/local-convention-detection.md",
            "code-style-consistency-rules/references/style-baseline.md"
          ],
          "agents": [
            "code-style-consistency-rules/agents/openai.yaml"
          ],
          "has_license": false,
          "focus_points": [
            "优先检查 description 是否具体到触发信号，而不是只写抽象用途。",
            "检查 references 是否足以承接复杂场景，避免 SKILL.md 过厚或过空。",
            "重点看它是否能并行生效，并且不抢位点域或审查域职责。"
          ]
        },
        {
          "id": "naming-rules",
          "name": "naming-rules",
          "title": "命名规则",
          "status": "implemented",
          "status_label": "已实现",
          "domain_id": "baseline",
          "domain_label": "编码基线域",
          "domain_description": "开始编码即并行生效的基础质量规则",
          "domain_order": 4,
          "item_order": 4,
          "auto_trigger": "当新增或修改变量、函数、类、模块、接口、字段、事件、任务名、测试名或配置项命名时触发。负责统一业务术语、语义粒度、缩写边界、默认驼峰命名风格和命名一致性；不要把它代替代码可读性或风格格式规则。",
          "core_responsibility": "保证命名语义化。",
          "skill_path": "naming-rules/SKILL.md",
          "directory_path": "naming-rules",
          "directory": "naming-rules",
          "sections": [
            "Skill 作用与适用场景",
            "自动触发信号",
            "进入后先做什么",
            "默认执行流程",
            "权责边界与不负责事项",
            "需要暂停并确认的条件",
            "执行通过 / 驳回标准",
            "执行结果归档要求",
            "references 读取规则"
          ],
          "references": [
            "naming-rules/references/domain-term-alignment.md",
            "naming-rules/references/naming-examples.md",
            "naming-rules/references/naming-principles.md"
          ],
          "agents": [
            "naming-rules/agents/openai.yaml"
          ],
          "has_license": false,
          "focus_points": [
            "优先检查 description 是否具体到触发信号，而不是只写抽象用途。",
            "检查 references 是否足以承接复杂场景，避免 SKILL.md 过厚或过空。",
            "重点看它是否能并行生效，并且不抢位点域或审查域职责。"
          ]
        },
        {
          "id": "chinese-comment-rules",
          "name": "chinese-comment-rules",
          "title": "中文注释规则",
          "status": "implemented",
          "status_label": "已实现",
          "domain_id": "baseline",
          "domain_label": "编码基线域",
          "domain_description": "开始编码即并行生效的基础质量规则",
          "domain_order": 4,
          "item_order": 5,
          "auto_trigger": "当新增或修改代码注释、步骤说明、复杂逻辑解释、临时诊断说明或测试说明，且团队要求默认使用中文表述时触发。负责中文注释的语言选择、表达方式和禁忌；不要把它代替注释位置与颗粒度规则。",
          "core_responsibility": "统一中文表达习惯和注释语气。",
          "skill_path": "chinese-comment-rules/SKILL.md",
          "directory_path": "chinese-comment-rules",
          "directory": "chinese-comment-rules",
          "sections": [
            "Skill 作用与适用场景",
            "自动触发信号",
            "进入后先做什么",
            "默认执行流程",
            "权责边界与不负责事项",
            "需要暂停并确认的条件",
            "执行通过 / 驳回标准",
            "执行结果归档要求",
            "references 读取规则"
          ],
          "references": [
            "chinese-comment-rules/references/chinese-comment-patterns.md",
            "chinese-comment-rules/references/comment-examples.md",
            "chinese-comment-rules/references/comment-language-boundary.md"
          ],
          "agents": [
            "chinese-comment-rules/agents/openai.yaml"
          ],
          "has_license": false,
          "focus_points": [
            "优先检查 description 是否具体到触发信号，而不是只写抽象用途。",
            "检查 references 是否足以承接复杂场景，避免 SKILL.md 过厚或过空。",
            "重点看它是否能并行生效，并且不抢位点域或审查域职责。"
          ]
        },
        {
          "id": "code-comment-rules",
          "name": "code-comment-rules",
          "title": "代码注释规则",
          "status": "implemented",
          "status_label": "已实现",
          "domain_id": "baseline",
          "domain_label": "编码基线域",
          "domain_description": "开始编码即并行生效的基础质量规则",
          "domain_order": 4,
          "item_order": 6,
          "auto_trigger": "当需要判断代码是否应该加注释、注释放在哪里、写到什么颗粒度、如何与实现同步维护时触发。负责注释必要性、位置选择、颗粒度控制、步骤注释、字段注释、函数方法修改时间标注和过期注释治理；每个函数方法的修改都必须补充最近修改时间（北京时间：yyyy-MM-DD HH:mm:ss）；不要把它代替中文语言表达规则。",
          "core_responsibility": "统一注释层级和颗粒度。",
          "skill_path": "code-comment-rules/SKILL.md",
          "directory_path": "code-comment-rules",
          "directory": "code-comment-rules",
          "sections": [
            "Skill 作用与适用场景",
            "自动触发信号",
            "进入后先做什么",
            "默认执行流程",
            "权责边界与不负责事项",
            "需要暂停并确认的条件",
            "执行通过 / 驳回标准",
            "执行结果归档要求",
            "references 读取规则"
          ],
          "references": [
            "code-comment-rules/references/comment-examples.md",
            "code-comment-rules/references/comment-granularity.md",
            "code-comment-rules/references/comment-placement.md"
          ],
          "agents": [
            "code-comment-rules/agents/openai.yaml"
          ],
          "has_license": false,
          "focus_points": [
            "优先检查 description 是否具体到触发信号，而不是只写抽象用途。",
            "检查 references 是否足以承接复杂场景，避免 SKILL.md 过厚或过空。",
            "重点看它是否能并行生效，并且不抢位点域或审查域职责。"
          ]
        }
      ]
    },
    {
      "id": "location",
      "label": "代码位点域",
      "description": "按改动位置叠加触发的实现规则",
      "order": 5,
      "implemented_count": 11,
      "planned_count": 4,
      "seed_count": 0,
      "total_count": 15,
      "items": [
        {
          "id": "config-change-rules",
          "name": "config-change-rules",
          "title": "config-change-rules",
          "status": "planned",
          "status_label": "规划中",
          "domain_id": "location",
          "domain_label": "代码位点域",
          "domain_description": "按改动位置叠加触发的实现规则",
          "domain_order": 5,
          "item_order": 1,
          "auto_trigger": "当新增或修改 `.env`、`.env.example`、`application.yml`、`application.yaml`、`settings.py`、`config.ts`、`appsettings.json`、`values.yaml`、环境变量读取、默认值、配置注入、配置分层、特性开关、密钥占位时自动触发。",
          "core_responsibility": "统一配置、密钥和默认值策略。",
          "skill_path": "",
          "directory_path": "",
          "directory": "",
          "sections": [],
          "references": [],
          "agents": [],
          "has_license": false,
          "focus_points": [
            "先补齐触发 description、邻接边界和最小 references，再决定是否正式建目录。",
            "优先确认它与同域相邻 skill 的拆分边界，避免新建后职责重叠。",
            "重点看主位点与横切位点是否可并行叠加，而不是互相覆盖。"
          ]
        },
        {
          "id": "package-structure-rules",
          "name": "package-structure-rules",
          "title": "包结构与分层规则",
          "status": "implemented",
          "status_label": "已实现",
          "domain_id": "location",
          "domain_label": "代码位点域",
          "domain_description": "按改动位置叠加触发的实现规则",
          "domain_order": 5,
          "item_order": 2,
          "auto_trigger": "用于判断新增或修改包、目录、模块、`main.go` 启动入口、`internal` 私有代码、`utils` / `common` / `global` / `middleware` / `crontask` / `async` 等支撑目录，以及 `router` / `controller` / `service` / `repository` / `model` 等业务目录的落点、职责和依赖方向。适用于 Go、Java、Node/Python 项目的结构决策，尤其适合判断单二进制 Go 服务中哪些代码必须留在 `internal/`，以及哪些入口层目录必须保持根级；不要用它代替工具实现、接口设计或代码审查类 skill。",
          "core_responsibility": "统一代码包定义、目录分层、包名职责、模块边界和依赖方向，尤其约束 Go 等语言中的 `routes`、`services`、`utils`、`models`、`repositories`、`middleware`、`constants`、`config`、`controller` 等包结构，避免目录失控和职责混乱。",
          "skill_path": "package-structure-rules/SKILL.md",
          "directory_path": "package-structure-rules",
          "directory": "package-structure-rules",
          "sections": [
            "Skill 作用与适用场景",
            "自动触发信号",
            "进入后先做什么",
            "默认执行流程",
            "权责边界与不负责事项",
            "需要暂停并确认的条件",
            "执行通过 / 驳回标准",
            "执行结果归档要求",
            "references 读取规则"
          ],
          "references": [
            "package-structure-rules/references/go-package-layout.md",
            "package-structure-rules/references/java-layer-layout.md",
            "package-structure-rules/references/node-python-module-layout.md",
            "package-structure-rules/references/structure-general.md"
          ],
          "agents": [
            "package-structure-rules/agents/openai.yaml"
          ],
          "has_license": false,
          "focus_points": [
            "优先检查 description 是否具体到触发信号，而不是只写抽象用途。",
            "检查 references 是否足以承接复杂场景，避免 SKILL.md 过厚或过空。",
            "重点看主位点与横切位点是否可并行叠加，而不是互相覆盖。"
          ]
        },
        {
          "id": "common-util-rules",
          "name": "common-util-rules",
          "title": "公共工具规则",
          "status": "implemented",
          "status_label": "已实现",
          "domain_id": "location",
          "domain_label": "代码位点域",
          "domain_description": "按改动位置叠加触发的实现规则",
          "domain_order": 5,
          "item_order": 3,
          "auto_trigger": "当新增或修改工具类、通用方法、公共组件、工具函数、通用常量或复用代码时触发。负责统一公共工具代码的判定标准、存放位置、调用方式和边界；不要用它代替业务逻辑抽象、包结构规则或具体实现细则。",
          "core_responsibility": "统一通用工具代码的编写规范、复用标准、存放位置和调用方式，避免重复造轮子，保证公共代码的通用性、稳定性和可维护性。",
          "skill_path": "common-util-rules/SKILL.md",
          "directory_path": "common-util-rules",
          "directory": "common-util-rules",
          "sections": [
            "Skill 作用与适用场景",
            "自动触发信号",
            "进入后先做什么",
            "默认执行流程",
            "权责边界与不负责事项",
            "需要暂停并确认的条件",
            "执行通过 / 驳回标准",
            "执行结果归档要求",
            "references 读取规则"
          ],
          "references": [
            "common-util-rules/references/util-examples.md",
            "common-util-rules/references/util-placement.md",
            "common-util-rules/references/util-qualification.md"
          ],
          "agents": [
            "common-util-rules/agents/openai.yaml"
          ],
          "has_license": false,
          "focus_points": [
            "优先检查 description 是否具体到触发信号，而不是只写抽象用途。",
            "检查 references 是否足以承接复杂场景，避免 SKILL.md 过厚或过空。",
            "重点看主位点与横切位点是否可并行叠加，而不是互相覆盖。"
          ]
        },
        {
          "id": "database-schema-rules",
          "name": "database-schema-rules",
          "title": "数据库结构规则",
          "status": "implemented",
          "status_label": "已实现",
          "domain_id": "location",
          "domain_label": "代码位点域",
          "domain_description": "按改动位置叠加触发的实现规则",
          "domain_order": 5,
          "item_order": 4,
          "auto_trigger": "当新增或修改表、字段、索引、唯一约束、外键、迁移脚本、DDL、实体结构、schema 定义时自动触发。负责统一数据库结构变更、迁移安全、兼容性和回滚边界；数据库的字段必须要定义数据类型、默认值、是否需要索引、字段 CHARSET=utf8mb4、ENGINE=InnoDB、注释说明等写清楚，不要遗漏；所有金额相关的要强制使用字符串，避免任何出现精度问题的情况；所有表必须包含 created_at 和 updated_at 字段，由数据库自动管理；必须冗余一个毫秒级时间戳的创建时间，避免数据库的时区问题影响不同的时间格式；所有表必须包含逻辑删除字段，1 的状态标识删除，不是 1 代表正常非删除状态，默认 0=非删除；否则会导致自动创建表出现不可控的因素；避免把查询实现、事务控制和业务逻辑混进结构变更；不要用它代替 database-query-rules、config-change-rules 或发布回滚规则。",
          "core_responsibility": "统一表结构变更、迁移安全和回滚策略。",
          "skill_path": "database-schema-rules/SKILL.md",
          "directory_path": "database-schema-rules",
          "directory": "database-schema-rules",
          "sections": [
            "Skill 作用与适用场景",
            "自动触发信号",
            "进入后先做什么",
            "默认执行流程",
            "权责边界与不负责事项",
            "需要暂停并确认的条件",
            "执行通过 / 驳回标准",
            "执行结果归档要求",
            "references 读取规则"
          ],
          "references": [
            "database-schema-rules/references/migration-safety-and-rollback.md",
            "database-schema-rules/references/schema-boundaries.md",
            "database-schema-rules/references/schema-examples.md"
          ],
          "agents": [
            "database-schema-rules/agents/openai.yaml"
          ],
          "has_license": false,
          "focus_points": [
            "优先检查 description 是否具体到触发信号，而不是只写抽象用途。",
            "检查 references 是否足以承接复杂场景，避免 SKILL.md 过厚或过空。",
            "重点看主位点与横切位点是否可并行叠加，而不是互相覆盖。"
          ]
        },
        {
          "id": "database-query-rules",
          "name": "database-query-rules",
          "title": "数据库访问规则",
          "status": "implemented",
          "status_label": "已实现",
          "domain_id": "location",
          "domain_label": "代码位点域",
          "domain_description": "按改动位置叠加触发的实现规则",
          "domain_order": 5,
          "item_order": 5,
          "auto_trigger": "当新增或修改 SQL、Repository、DAO、Mapper、QueryBuilder、事务、锁、批量 CRUD、分页查询时自动触发。负责统一数据库访问实现、查询性能、事务与锁边界，避免把 schema 设计、缓存策略和业务逻辑混进数据访问层；不要用它代替 database-schema-rules、performance-caching-rules 或业务规则本身。",
          "core_responsibility": "统一数据库访问和查询性能规则。",
          "skill_path": "database-query-rules/SKILL.md",
          "directory_path": "database-query-rules",
          "directory": "database-query-rules",
          "sections": [
            "Skill 作用与适用场景",
            "自动触发信号",
            "进入后先做什么",
            "默认执行流程",
            "权责边界与不负责事项",
            "需要暂停并确认的条件",
            "执行通过 / 驳回标准",
            "执行结果归档要求",
            "references 读取规则"
          ],
          "references": [
            "database-query-rules/references/access-layer-boundaries.md",
            "database-query-rules/references/query-performance-examples.md",
            "database-query-rules/references/transactions-locks-and-batch.md"
          ],
          "agents": [
            "database-query-rules/agents/openai.yaml"
          ],
          "has_license": false,
          "focus_points": [
            "优先检查 description 是否具体到触发信号，而不是只写抽象用途。",
            "检查 references 是否足以承接复杂场景，避免 SKILL.md 过厚或过空。",
            "重点看主位点与横切位点是否可并行叠加，而不是互相覆盖。"
          ]
        },
        {
          "id": "api-endpoint-rules",
          "name": "api-endpoint-rules",
          "title": "接口入口规则",
          "status": "implemented",
          "status_label": "已实现",
          "domain_id": "location",
          "domain_label": "代码位点域",
          "domain_description": "按改动位置叠加触发的实现规则",
          "domain_order": 5,
          "item_order": 6,
          "auto_trigger": "当新增或修改 controller、router、路由声明、HTTP 方法、接口路径命名、接口入口职责或超时入口边界时触发。负责统一接口入口设计、路径命名和强制使用 POST 方法；必须以 package-structure-rules 为基准，不使用 handler 包名；不要用它代替请求参数、响应结构或错误处理规则。",
          "core_responsibility": "统一接口入口设计。",
          "skill_path": "api-endpoint-rules/SKILL.md",
          "directory_path": "api-endpoint-rules",
          "directory": "api-endpoint-rules",
          "sections": [
            "Skill 作用与适用场景",
            "自动触发信号",
            "进入后先做什么",
            "默认执行流程",
            "权责边界与不负责事项",
            "需要暂停并确认的条件",
            "执行通过 / 驳回标准",
            "执行结果归档要求",
            "references 读取规则"
          ],
          "references": [
            "api-endpoint-rules/references/endpoint-examples.md",
            "api-endpoint-rules/references/endpoint-responsibility.md",
            "api-endpoint-rules/references/path-and-method-semantics.md"
          ],
          "agents": [
            "api-endpoint-rules/agents/openai.yaml"
          ],
          "has_license": false,
          "focus_points": [
            "优先检查 description 是否具体到触发信号，而不是只写抽象用途。",
            "检查 references 是否足以承接复杂场景，避免 SKILL.md 过厚或过空。",
            "重点看主位点与横切位点是否可并行叠加，而不是互相覆盖。"
          ]
        },
        {
          "id": "api-request-rules",
          "name": "api-request-rules",
          "title": "接口请求规则",
          "status": "implemented",
          "status_label": "已实现",
          "domain_id": "location",
          "domain_label": "代码位点域",
          "domain_description": "按改动位置叠加触发的实现规则",
          "domain_order": 5,
          "item_order": 7,
          "auto_trigger": "当新增或修改请求参数、DTO、body 结构、参数校验或请求模型时触发。负责统一请求结构、参数表达和基础校验边界；必须以 api-endpoint-rules 为基准，只使用 POST 请求，所有参数通过 JSON body 传递；不要用它代替接口入口设计、响应结构或业务规则本身。",
          "core_responsibility": "统一请求模型和校验规则。",
          "skill_path": "api-request-rules/SKILL.md",
          "directory_path": "api-request-rules",
          "directory": "api-request-rules",
          "sections": [
            "Skill 作用与适用场景",
            "自动触发信号",
            "进入后先做什么",
            "默认执行流程",
            "权责边界与不负责事项",
            "需要暂停并确认的条件",
            "执行通过 / 驳回标准",
            "执行结果归档要求",
            "references 读取规则"
          ],
          "references": [
            "api-request-rules/references/parameter-validation-rules.md",
            "api-request-rules/references/request-examples.md",
            "api-request-rules/references/request-shape-boundaries.md"
          ],
          "agents": [
            "api-request-rules/agents/openai.yaml"
          ],
          "has_license": false,
          "focus_points": [
            "优先检查 description 是否具体到触发信号，而不是只写抽象用途。",
            "检查 references 是否足以承接复杂场景，避免 SKILL.md 过厚或过空。",
            "重点看主位点与横切位点是否可并行叠加，而不是互相覆盖。"
          ]
        },
        {
          "id": "api-response-rules",
          "name": "api-response-rules",
          "title": "接口响应规则",
          "status": "implemented",
          "status_label": "已实现",
          "domain_id": "location",
          "domain_label": "代码位点域",
          "domain_description": "按改动位置叠加触发的实现规则",
          "domain_order": 5,
          "item_order": 8,
          "auto_trigger": "当新增或修改返回体、响应包装器、分页结构、错误响应结构、兼容字段、版本字段或统一响应模型时触发。负责统一响应格式和兼容策略；成功响应和错误响应都必须包含状态码、状态、消息、数据四个字段；不要用它代替错误处理流程、异常分类或接口入口职责规则。",
          "core_responsibility": "统一响应格式和兼容策略。",
          "skill_path": "api-response-rules/SKILL.md",
          "directory_path": "api-response-rules",
          "directory": "api-response-rules",
          "sections": [
            "Skill 作用与适用场景",
            "自动触发信号",
            "进入后先做什么",
            "默认执行流程",
            "权责边界与不负责事项",
            "需要暂停并确认的条件",
            "执行通过 / 驳回标准",
            "执行结果归档要求",
            "references 读取规则"
          ],
          "references": [
            "api-response-rules/references/response-examples.md",
            "api-response-rules/references/response-shape-baseline.md",
            "api-response-rules/references/response-variants.md"
          ],
          "agents": [
            "api-response-rules/agents/openai.yaml"
          ],
          "has_license": false,
          "focus_points": [
            "优先检查 description 是否具体到触发信号，而不是只写抽象用途。",
            "检查 references 是否足以承接复杂场景，避免 SKILL.md 过厚或过空。",
            "重点看主位点与横切位点是否可并行叠加，而不是互相覆盖。"
          ]
        },
        {
          "id": "request-header-rules",
          "name": "request-header-rules",
          "title": "request-header-rules",
          "status": "planned",
          "status_label": "规划中",
          "domain_id": "location",
          "domain_label": "代码位点域",
          "domain_description": "按改动位置叠加触发的实现规则",
          "domain_order": 5,
          "item_order": 9,
          "auto_trigger": "当新增或修改认证头、`trace-id`、`span-id`、租户头、幂等键、客户端上下文头、`X-Forwarded-*` 逻辑时自动触发。",
          "core_responsibility": "统一请求头约定和透传规则。",
          "skill_path": "",
          "directory_path": "",
          "directory": "",
          "sections": [],
          "references": [],
          "agents": [],
          "has_license": false,
          "focus_points": [
            "先补齐触发 description、邻接边界和最小 references，再决定是否正式建目录。",
            "优先确认它与同域相邻 skill 的拆分边界，避免新建后职责重叠。",
            "重点看主位点与横切位点是否可并行叠加，而不是互相覆盖。"
          ]
        },
        {
          "id": "error-handling-rules",
          "name": "error-handling-rules",
          "title": "错误处理规则",
          "status": "implemented",
          "status_label": "已实现",
          "domain_id": "location",
          "domain_label": "代码位点域",
          "domain_description": "按改动位置叠加触发的实现规则",
          "domain_order": 5,
          "item_order": 10,
          "auto_trigger": "当新增或修改异常类、全局异常处理、错误中间件、try/catch、错误映射、重试、超时、降级或 fallback 时触发。负责统一错误处理模型和处理路径；不要用它代替错误响应结构、日志链路或接口入口设计规则。",
          "core_responsibility": "统一错误处理模型。",
          "skill_path": "error-handling-rules/SKILL.md",
          "directory_path": "error-handling-rules",
          "directory": "error-handling-rules",
          "sections": [
            "Skill 作用与适用场景",
            "自动触发信号",
            "进入后先做什么",
            "默认执行流程",
            "权责边界与不负责事项",
            "需要暂停并确认的条件",
            "执行通过 / 驳回标准",
            "执行结果归档要求",
            "references 读取规则"
          ],
          "references": [
            "error-handling-rules/references/error-classification.md",
            "error-handling-rules/references/handling-paths.md",
            "error-handling-rules/references/resilience-boundaries.md"
          ],
          "agents": [
            "error-handling-rules/agents/openai.yaml"
          ],
          "has_license": false,
          "focus_points": [
            "优先检查 description 是否具体到触发信号，而不是只写抽象用途。",
            "检查 references 是否足以承接复杂场景，避免 SKILL.md 过厚或过空。",
            "重点看主位点与横切位点是否可并行叠加，而不是互相覆盖。"
          ]
        },
        {
          "id": "logging-trace-rules",
          "name": "logging-trace-rules",
          "title": "日志与追踪规则",
          "status": "implemented",
          "status_label": "已实现",
          "domain_id": "location",
          "domain_label": "代码位点域",
          "domain_description": "按改动位置叠加触发的实现规则",
          "domain_order": 5,
          "item_order": 11,
          "auto_trigger": "当新增或修改日志、logger、trace、span、审计日志、脱敏字段、排障字段或链路透传逻辑时触发。负责统一日志与链路追踪规则；不要用它代替错误处理、响应结构或长期监控告警策略。",
          "core_responsibility": "统一日志和链路追踪规则。",
          "skill_path": "logging-trace-rules/SKILL.md",
          "directory_path": "logging-trace-rules",
          "directory": "logging-trace-rules",
          "sections": [
            "Skill 作用与适用场景",
            "自动触发信号",
            "进入后先做什么",
            "默认执行流程",
            "权责边界与不负责事项",
            "需要暂停并确认的条件",
            "执行通过 / 驳回标准",
            "执行结果归档要求",
            "references 读取规则"
          ],
          "references": [
            "logging-trace-rules/references/log-types-and-fields.md",
            "logging-trace-rules/references/logging-examples.md",
            "logging-trace-rules/references/trace-propagation.md"
          ],
          "agents": [
            "logging-trace-rules/agents/openai.yaml"
          ],
          "has_license": false,
          "focus_points": [
            "优先检查 description 是否具体到触发信号，而不是只写抽象用途。",
            "检查 references 是否足以承接复杂场景，避免 SKILL.md 过厚或过空。",
            "重点看主位点与横切位点是否可并行叠加，而不是互相覆盖。"
          ]
        },
        {
          "id": "auth-security-rules",
          "name": "auth-security-rules",
          "title": "auth-security-rules",
          "status": "planned",
          "status_label": "规划中",
          "domain_id": "location",
          "domain_label": "代码位点域",
          "domain_description": "按改动位置叠加触发的实现规则",
          "domain_order": 5,
          "item_order": 12,
          "auto_trigger": "当新增或修改认证、鉴权、登录、登出、会话、JWT、对象级授权、输入校验、敏感信息处理、上传下载安全、外部请求安全时自动触发。",
          "core_responsibility": "统一安全实现的默认基线。",
          "skill_path": "",
          "directory_path": "",
          "directory": "",
          "sections": [],
          "references": [],
          "agents": [],
          "has_license": false,
          "focus_points": [
            "先补齐触发 description、邻接边界和最小 references，再决定是否正式建目录。",
            "优先确认它与同域相邻 skill 的拆分边界，避免新建后职责重叠。",
            "重点看主位点与横切位点是否可并行叠加，而不是互相覆盖。"
          ]
        },
        {
          "id": "frontend-component-rules",
          "name": "frontend-component-rules",
          "title": "前端组件工程规则",
          "status": "implemented",
          "status_label": "已实现",
          "domain_id": "location",
          "domain_label": "代码位点域",
          "domain_description": "按改动位置叠加触发的实现规则",
          "domain_order": 5,
          "item_order": 13,
          "auto_trigger": "当新增或修改 React、Vue、前端组件拆分、组件目录归属、props 设计、emits 设计、slots 设计、状态归属、事件上抛、组合方式、hooks、composables、复用边界、受控/非受控切换、渲染副作用或客户端展示逻辑时自动触发。负责组件边界、状态边界、接口契约、组合复用和渲染可维护性；不要用它代替页面视觉、配色、排版、响应式和 UI 风格规则。",
          "core_responsibility": "统一前端组件工程、状态边界和页面内组合规则。",
          "skill_path": "frontend-component-rules/SKILL.md",
          "directory_path": "frontend-component-rules",
          "directory": "frontend-component-rules",
          "sections": [
            "Skill 作用与适用场景",
            "自动触发信号",
            "进入后先做什么",
            "默认执行流程",
            "权责边界与不负责事项",
            "需要暂停并确认的条件",
            "执行通过 / 驳回标准",
            "执行结果归档要求",
            "references 读取规则"
          ],
          "references": [
            "frontend-component-rules/references/component-boundary-rules.md",
            "frontend-component-rules/references/component-review-checklist.md",
            "frontend-component-rules/references/composition-reuse-rules.md",
            "frontend-component-rules/references/props-events-contract-rules.md",
            "frontend-component-rules/references/render-side-effect-rules.md",
            "frontend-component-rules/references/state-ownership-rules.md"
          ],
          "agents": [
            "frontend-component-rules/agents/openai.yaml"
          ],
          "has_license": false,
          "focus_points": [
            "优先检查 description 是否具体到触发信号，而不是只写抽象用途。",
            "检查 references 是否足以承接复杂场景，避免 SKILL.md 过厚或过空。",
            "重点看主位点与横切位点是否可并行叠加，而不是互相覆盖。"
          ]
        },
        {
          "id": "frontend-ui-visual-rules",
          "name": "frontend-ui-visual-rules",
          "title": "前端 UI 视觉规则",
          "status": "implemented",
          "status_label": "已实现",
          "domain_id": "location",
          "domain_label": "代码位点域",
          "domain_description": "按改动位置叠加触发的实现规则",
          "domain_order": 5,
          "item_order": 14,
          "auto_trigger": "当新增或修改前端页面、页面布局、主题样式、配色、字体、图标、卡片、弹窗、表单、表格、图表、导航、空状态、动画、响应式样式、暗黑模式、设计 token、Tailwind 类名、CSS/SCSS/LESS、`.tsx`/`.jsx`/`.vue`/`.html` 中影响界面视觉和交互体验的代码时自动触发。负责页面视觉方向、信息层级、交互反馈、可访问性、响应式适配和交付前 UI 自审；内置合并后的 UI/UX 设计种子数据与搜索脚本，可在风格不明时辅助定方向；不要用它代替纯组件工程拆分、状态管理、接口接线或后端规则。",
          "core_responsibility": "统一页面视觉方向、信息层级、交互反馈、响应式适配、可访问性和交付前 UI 自审。",
          "skill_path": "frontend-ui-visual-rules/SKILL.md",
          "directory_path": "frontend-ui-visual-rules",
          "directory": "frontend-ui-visual-rules",
          "sections": [
            "Skill 作用与适用场景",
            "自动触发信号",
            "进入后先做什么",
            "默认执行流程",
            "权责边界与不负责事项",
            "需要暂停并确认的条件",
            "执行通过 / 驳回标准",
            "执行结果归档要求",
            "references 读取规则"
          ],
          "references": [
            "frontend-ui-visual-rules/references/color-typography-icon-rules.md",
            "frontend-ui-visual-rules/references/design-search-workflow.md",
            "frontend-ui-visual-rules/references/forms-nav-data-display-rules.md",
            "frontend-ui-visual-rules/references/interaction-accessibility-rules.md",
            "frontend-ui-visual-rules/references/layout-responsive-rules.md",
            "frontend-ui-visual-rules/references/page-style-and-scenario.md",
            "frontend-ui-visual-rules/references/seed-source-notes.md",
            "frontend-ui-visual-rules/references/ui-delivery-checklist.md",
            "frontend-ui-visual-rules/references/ui-priority-model.md"
          ],
          "agents": [
            "frontend-ui-visual-rules/agents/openai.yaml"
          ],
          "has_license": false,
          "focus_points": [
            "优先检查 description 是否具体到触发信号，而不是只写抽象用途。",
            "检查 references 是否足以承接复杂场景，避免 SKILL.md 过厚或过空。",
            "重点看主位点与横切位点是否可并行叠加，而不是互相覆盖。"
          ]
        },
        {
          "id": "performance-caching-rules",
          "name": "performance-caching-rules",
          "title": "performance-caching-rules",
          "status": "planned",
          "status_label": "规划中",
          "domain_id": "location",
          "domain_label": "代码位点域",
          "domain_description": "按改动位置叠加触发的实现规则",
          "domain_order": 5,
          "item_order": 15,
          "auto_trigger": "当新增或修改 SQL 性能、接口耗时、缓存读取写入、缓存 key、缓存失效、前端渲染热点、大列表、图表、虚拟滚动时自动触发。",
          "core_responsibility": "统一性能和缓存规则。",
          "skill_path": "",
          "directory_path": "",
          "directory": "",
          "sections": [],
          "references": [],
          "agents": [],
          "has_license": false,
          "focus_points": [
            "先补齐触发 description、邻接边界和最小 references，再决定是否正式建目录。",
            "优先确认它与同域相邻 skill 的拆分边界，避免新建后职责重叠。",
            "重点看主位点与横切位点是否可并行叠加，而不是互相覆盖。"
          ]
        }
      ]
    },
    {
      "id": "review",
      "label": "编码审查域",
      "description": "测试前的静态自审、语法检查、清理归位",
      "order": 6,
      "implemented_count": 4,
      "planned_count": 0,
      "seed_count": 0,
      "total_count": 4,
      "items": [
        {
          "id": "implementation-review-rules",
          "name": "implementation-review-rules",
          "title": "实现自审规则",
          "status": "implemented",
          "status_label": "已实现",
          "domain_id": "review",
          "domain_label": "编码审查域",
          "domain_description": "测试前的静态自审、语法检查、清理归位",
          "domain_order": 6,
          "item_order": 1,
          "auto_trigger": "当功能代码已经完成、准备进入测试前验证时触发。负责检查实现是否符合可读性优先、单一职责、命名语义化、注释完整、错误处理明确、日志可追溯、依赖使用审慎、魔法值治理、冗余逻辑清理和编码规范等实现质量要求；不要用它代替语法检查、格式化执行、目录归位审查或功能验证规则。",
          "core_responsibility": "对刚完成的实现做一次测试前规范自审。",
          "skill_path": "implementation-review-rules/SKILL.md",
          "directory_path": "implementation-review-rules",
          "directory": "implementation-review-rules",
          "sections": [
            "Skill 作用与适用场景",
            "自动触发信号",
            "进入后先做什么",
            "核心自审要求",
            "默认执行流程",
            "权责边界与不负责事项",
            "需要暂停并确认的条件",
            "执行通过 / 驳回标准",
            "执行结果归档要求",
            "references 读取规则"
          ],
          "references": [
            "implementation-review-rules/references/review-boundaries.md",
            "implementation-review-rules/references/review-examples.md",
            "implementation-review-rules/references/review-scope.md"
          ],
          "agents": [
            "implementation-review-rules/agents/openai.yaml"
          ],
          "has_license": false,
          "focus_points": [
            "优先检查 description 是否具体到触发信号，而不是只写抽象用途。",
            "检查 references 是否足以承接复杂场景，避免 SKILL.md 过厚或过空。",
            "重点看它是否只处理静态质量问题，不越界替代测试。"
          ]
        },
        {
          "id": "syntax-check-review-rules",
          "name": "syntax-check-review-rules",
          "title": "语法校验规则",
          "status": "implemented",
          "status_label": "已实现",
          "domain_id": "review",
          "domain_label": "编码审查域",
          "domain_description": "测试前的静态自审、语法检查、清理归位",
          "domain_order": 6,
          "item_order": 2,
          "auto_trigger": "当新增或修改代码后准备进入测试前验证，且需要确认语法、类型、依赖引用、构建基础是否正确时触发。负责检查语法错误、引用缺失、类型问题和明显构建失败风险；不要用它代替实现自审、格式清理或功能测试规则。",
          "core_responsibility": "检查语法错误、引用缺失、类型问题和明显构建失败风险。",
          "skill_path": "syntax-check-review-rules/SKILL.md",
          "directory_path": "syntax-check-review-rules",
          "directory": "syntax-check-review-rules",
          "sections": [
            "Skill 作用与适用场景",
            "自动触发信号",
            "进入后先做什么",
            "默认执行流程",
            "权责边界与不负责事项",
            "需要暂停并确认的条件",
            "执行通过 / 驳回标准",
            "执行结果归档要求",
            "references 读取规则"
          ],
          "references": [
            "syntax-check-review-rules/references/check-examples.md",
            "syntax-check-review-rules/references/check-scope.md",
            "syntax-check-review-rules/references/type-and-reference-risks.md"
          ],
          "agents": [
            "syntax-check-review-rules/agents/openai.yaml"
          ],
          "has_license": false,
          "focus_points": [
            "优先检查 description 是否具体到触发信号，而不是只写抽象用途。",
            "检查 references 是否足以承接复杂场景，避免 SKILL.md 过厚或过空。",
            "重点看它是否只处理静态质量问题，不越界替代测试。"
          ]
        },
        {
          "id": "cleanup-format-review-rules",
          "name": "cleanup-format-review-rules",
          "title": "清理格式审查规则",
          "status": "implemented",
          "status_label": "已实现",
          "domain_id": "review",
          "domain_label": "编码审查域",
          "domain_description": "测试前的静态自审、语法检查、清理归位",
          "domain_order": 6,
          "item_order": 3,
          "auto_trigger": "当新增或修改代码后准备进入测试前验证，且存在未使用导入、未使用变量、未使用方法引用、调试残留、临时代码、死代码、多余换行或格式不一致风险时触发。负责清理代码噪音并统一基础格式；不要用它代替功能性修改或实现重构。",
          "core_responsibility": "清理代码噪音并统一基础格式。",
          "skill_path": "cleanup-format-review-rules/SKILL.md",
          "directory_path": "cleanup-format-review-rules",
          "directory": "cleanup-format-review-rules",
          "sections": [
            "Skill 作用与适用场景",
            "自动触发信号",
            "进入后先做什么",
            "默认执行流程",
            "权责边界与不负责事项",
            "需要暂停并确认的条件",
            "执行通过 / 驳回标准",
            "执行结果归档要求",
            "references 读取规则"
          ],
          "references": [
            "cleanup-format-review-rules/references/cleanup-examples.md",
            "cleanup-format-review-rules/references/cleanup-scope.md",
            "cleanup-format-review-rules/references/debug-artifact-rules.md"
          ],
          "agents": [
            "cleanup-format-review-rules/agents/openai.yaml"
          ],
          "has_license": false,
          "focus_points": [
            "优先检查 description 是否具体到触发信号，而不是只写抽象用途。",
            "检查 references 是否足以承接复杂场景，避免 SKILL.md 过厚或过空。",
            "重点看它是否只处理静态质量问题，不越界替代测试。"
          ]
        },
        {
          "id": "code-placement-review-rules",
          "name": "code-placement-review-rules",
          "title": "代码归位审查规则",
          "status": "implemented",
          "status_label": "已实现",
          "domain_id": "review",
          "domain_label": "编码审查域",
          "domain_description": "测试前的静态自审、语法检查、清理归位",
          "domain_order": 6,
          "item_order": 4,
          "auto_trigger": "当新增文件、移动文件、扩展模块、跨层调用、工具类落点或目录归属可能不合理时，在进入测试前触发。负责检查代码存放位置、模块归属、层级边界和依赖方向是否合理；不要用它代替编码前的包结构决策规则。",
          "core_responsibility": "检查代码存放位置、模块归属、层级边界和依赖方向是否合理。",
          "skill_path": "code-placement-review-rules/SKILL.md",
          "directory_path": "code-placement-review-rules",
          "directory": "code-placement-review-rules",
          "sections": [
            "Skill 作用与适用场景",
            "自动触发信号",
            "进入后先做什么",
            "默认执行流程",
            "权责边界与不负责事项",
            "需要暂停并确认的条件",
            "执行通过 / 驳回标准",
            "执行结果归档要求",
            "references 读取规则"
          ],
          "references": [
            "code-placement-review-rules/references/dependency-direction.md",
            "code-placement-review-rules/references/placement-checklist.md",
            "code-placement-review-rules/references/placement-examples.md"
          ],
          "agents": [
            "code-placement-review-rules/agents/openai.yaml"
          ],
          "has_license": false,
          "focus_points": [
            "优先检查 description 是否具体到触发信号，而不是只写抽象用途。",
            "检查 references 是否足以承接复杂场景，避免 SKILL.md 过厚或过空。",
            "重点看它是否只处理静态质量问题，不越界替代测试。"
          ]
        }
      ]
    },
    {
      "id": "test",
      "label": "测试域",
      "description": "策略、资源、功能验证、联调、回归",
      "order": 7,
      "implemented_count": 7,
      "planned_count": 1,
      "seed_count": 0,
      "total_count": 8,
      "items": [
        {
          "id": "test-strategy-rules",
          "name": "test-strategy-rules",
          "title": "测试策略规则",
          "status": "implemented",
          "status_label": "已实现",
          "domain_id": "test",
          "domain_label": "测试域",
          "domain_description": "策略、资源、功能验证、联调、回归",
          "domain_order": 7,
          "item_order": 1,
          "auto_trigger": "当准备进入测试阶段，需要确定测什么、先测什么、测到什么程度、哪些路径必须覆盖、哪些风险只能记录待补测时触发。负责测试优先级、测试类型组合、覆盖范围和资源收口；必须以 `test-location-rules` 为基准，把策略摘要统一记录到 `test/yyyy-MM-DD_HHmmss/测试任务中文简介/README.md`，并在需要拆成多轮独立测试时给出多个时间戳根目录方案；不要用它代替具体测试资源管理或验证执行 skill。",
          "core_responsibility": "决定测试层级和覆盖重点。",
          "skill_path": "test-strategy-rules/SKILL.md",
          "directory_path": "test-strategy-rules",
          "directory": "test-strategy-rules",
          "sections": [
            "Skill 作用与适用场景",
            "自动触发信号",
            "进入后先做什么",
            "默认执行流程",
            "权责边界与不负责事项",
            "需要暂停并确认的条件",
            "执行通过 / 驳回标准",
            "执行结果归档要求",
            "references 读取规则"
          ],
          "references": [
            "test-strategy-rules/references/priority-model.md",
            "test-strategy-rules/references/strategy-dimensions.md",
            "test-strategy-rules/references/strategy-template.md"
          ],
          "agents": [
            "test-strategy-rules/agents/openai.yaml"
          ],
          "has_license": false,
          "focus_points": [
            "优先检查 description 是否具体到触发信号，而不是只写抽象用途。",
            "检查 references 是否足以承接复杂场景，避免 SKILL.md 过厚或过空。",
            "重点看测试策略、资源、功能验证、联调、回归是否已经拆开。"
          ]
        },
        {
          "id": "test-location-rules",
          "name": "test-location-rules",
          "title": "测试目录落点规则",
          "status": "implemented",
          "status_label": "已实现",
          "domain_id": "test",
          "domain_label": "测试域",
          "domain_description": "策略、资源、功能验证、联调、回归",
          "domain_order": 7,
          "item_order": 2,
          "auto_trigger": "当新增或修改测试目录、测试文件、测试脚本、验证程序、fixture、mock 数据、测试说明文档落点时触发。负责统一测试资源根目录、时间戳任务根目录、中文说明目录、真实代码路径镜像目录和禁止散落规则；尤其要避免把中文路径放进会被 Go 工具链编译的测试包目录。不要用它代替 test-naming-rules、test-program-rules、test-doc-rules、code-placement-review-rules 或功能验证规则。",
          "core_responsibility": "统一测试资源位置。",
          "skill_path": "test-location-rules/SKILL.md",
          "directory_path": "test-location-rules",
          "directory": "test-location-rules",
          "sections": [
            "铁律：所有测试资产必须统一在 test/ 目录下",
            "新基线：时间戳根目录 + 中文说明目录 + 真实代码路径镜像",
            "Skill 作用与适用场景",
            "自动触发信号",
            "进入后先做什么",
            "默认执行流程",
            "权责边界与不负责事项",
            "需要暂停并确认的条件",
            "执行通过 / 驳回标准",
            "执行结果归档要求",
            "references 读取规则"
          ],
          "references": [
            "test-location-rules/references/forbidden-scattered-assets.md",
            "test-location-rules/references/location-examples.md",
            "test-location-rules/references/test-root-and-task-folders.md"
          ],
          "agents": [
            "test-location-rules/agents/openai.yaml"
          ],
          "has_license": false,
          "focus_points": [
            "优先检查 description 是否具体到触发信号，而不是只写抽象用途。",
            "检查 references 是否足以承接复杂场景，避免 SKILL.md 过厚或过空。",
            "重点看测试策略、资源、功能验证、联调、回归是否已经拆开。"
          ]
        },
        {
          "id": "test-naming-rules",
          "name": "test-naming-rules",
          "title": "测试命名规则",
          "status": "implemented",
          "status_label": "已实现",
          "domain_id": "test",
          "domain_label": "测试域",
          "domain_description": "策略、资源、功能验证、联调、回归",
          "domain_order": 7,
          "item_order": 3,
          "auto_trigger": "当创建或修改测试时间戳根目录、中文说明目录、测试文件、测试脚本、测试数据目录、fixture 目录、mock 目录时触发。负责统一测试目录与文件命名规范，保证名称可读、可检索、与业务目标一致；必须以 test-location-rules 为基础，遵循 `test/yyyy-MM-DD_HHmmss/` 时间戳根目录、中文说明目录和真实代码路径镜像目录的命名规则；尤其要避免中文进入会被 Go 工具链编译的路径。不要用它代替 test-location-rules、test-program-rules、test-doc-rules 或功能验证规则。",
          "core_responsibility": "统一测试目录和文件命名。",
          "skill_path": "test-naming-rules/SKILL.md",
          "directory_path": "test-naming-rules",
          "directory": "test-naming-rules",
          "sections": [
            "Skill 作用与适用场景",
            "自动触发信号",
            "进入后先做什么",
            "默认执行流程",
            "权责边界与不负责事项",
            "需要暂停并确认的条件",
            "执行通过 / 驳回标准",
            "执行结果归档要求",
            "references 读取规则"
          ],
          "references": [
            "test-naming-rules/references/naming-baseline.md",
            "test-naming-rules/references/naming-boundaries.md",
            "test-naming-rules/references/naming-examples.md"
          ],
          "agents": [
            "test-naming-rules/agents/openai.yaml"
          ],
          "has_license": false,
          "focus_points": [
            "优先检查 description 是否具体到触发信号，而不是只写抽象用途。",
            "检查 references 是否足以承接复杂场景，避免 SKILL.md 过厚或过空。",
            "重点看测试策略、资源、功能验证、联调、回归是否已经拆开。"
          ]
        },
        {
          "id": "test-program-rules",
          "name": "test-program-rules",
          "title": "测试程序规则",
          "status": "implemented",
          "status_label": "已实现",
          "domain_id": "test",
          "domain_label": "测试域",
          "domain_description": "策略、资源、功能验证、联调、回归",
          "domain_order": 7,
          "item_order": 4,
          "auto_trigger": "当新增或修改测试程序、模拟程序、验证脚本、数据构造脚本、测试辅助代码时触发。负责统一测试程序职责拆分、辅助代码边界和长期保留策略；必须以 `test-location-rules` 为基准，把真实测试代码、脚本、mock、fixture 和执行产物统一落在 `test/yyyy-MM-DD_HHmmss/<ASCII 真实代码路径镜像>/` 下，并避免中文进入会被 Go 工具链编译的路径；不要用它代替 test-location-rules、test-naming-rules、test-doc-rules、bug-runtime-debug-rules 或功能验证规则。",
          "core_responsibility": "统一测试程序和辅助脚本位置。",
          "skill_path": "test-program-rules/SKILL.md",
          "directory_path": "test-program-rules",
          "directory": "test-program-rules",
          "sections": [
            "Skill 作用与适用场景",
            "自动触发信号",
            "进入后先做什么",
            "默认执行流程",
            "权责边界与不负责事项",
            "需要暂停并确认的条件",
            "执行通过 / 驳回标准",
            "执行结果归档要求",
            "references 读取规则"
          ],
          "references": [
            "test-program-rules/references/program-boundaries.md",
            "test-program-rules/references/program-examples.md",
            "test-program-rules/references/program-types-and-splitting.md"
          ],
          "agents": [
            "test-program-rules/agents/openai.yaml"
          ],
          "has_license": false,
          "focus_points": [
            "优先检查 description 是否具体到触发信号，而不是只写抽象用途。",
            "检查 references 是否足以承接复杂场景，避免 SKILL.md 过厚或过空。",
            "重点看测试策略、资源、功能验证、联调、回归是否已经拆开。"
          ]
        },
        {
          "id": "test-doc-rules",
          "name": "test-doc-rules",
          "title": "测试文档规则",
          "status": "implemented",
          "status_label": "已实现",
          "domain_id": "test",
          "domain_label": "测试域",
          "domain_description": "策略、资源、功能验证、联调、回归",
          "domain_order": 7,
          "item_order": 5,
          "auto_trigger": "当新增或修改测试 README、验证说明、测试报告、覆盖说明、测试执行记录时触发。负责统一测试文档的最小结构、记录字段、主文档入口和归档方式；必须以 `test-location-rules` 为基准，使用 `test/yyyy-MM-DD_HHmmss/测试任务中文简介/README.md` 作为中文主说明入口，并把额外文档放到同一时间戳根目录下的 ASCII 真实代码路径镜像目录中；不要用它代替 test-location-rules、test-program-rules、functional-validation-rules 或 test-regression-rules。",
          "core_responsibility": "统一测试说明文档结构。",
          "skill_path": "test-doc-rules/SKILL.md",
          "directory_path": "test-doc-rules",
          "directory": "test-doc-rules",
          "sections": [
            "Skill 作用与适用场景",
            "自动触发信号",
            "进入后先做什么",
            "默认执行流程",
            "权责边界与不负责事项",
            "需要暂停并确认的条件",
            "执行通过 / 驳回标准",
            "执行结果归档要求",
            "references 读取规则"
          ],
          "references": [
            "test-doc-rules/references/doc-boundaries.md",
            "test-doc-rules/references/doc-examples.md",
            "test-doc-rules/references/doc-minimums.md"
          ],
          "agents": [
            "test-doc-rules/agents/openai.yaml"
          ],
          "has_license": false,
          "focus_points": [
            "优先检查 description 是否具体到触发信号，而不是只写抽象用途。",
            "检查 references 是否足以承接复杂场景，避免 SKILL.md 过厚或过空。",
            "重点看测试策略、资源、功能验证、联调、回归是否已经拆开。"
          ]
        },
        {
          "id": "functional-validation-rules",
          "name": "functional-validation-rules",
          "title": "功能验证规则",
          "status": "implemented",
          "status_label": "已实现",
          "domain_id": "test",
          "domain_label": "测试域",
          "domain_description": "策略、资源、功能验证、联调、回归",
          "domain_order": 7,
          "item_order": 6,
          "auto_trigger": "当需要验证新功能、修改后的功能、接口行为、页面交互、输入输出结果是否满足当前需求、当前变更和验收标准时触发。负责界定本次功能验证范围、验证步骤、通过驳回标准和结论留痕；必须以 `test-location-rules` 为基准，把功能验证结论写回 `test/yyyy-MM-DD_HHmmss/测试任务中文简介/README.md`，并把详细执行证据放到同一时间戳根目录下的 ASCII 真实代码路径镜像目录中；不要用它代替 test-strategy-rules、test-location-rules、integration-debugging-rules 或 test-regression-rules。",
          "core_responsibility": "负责当前需求对应的功能正确性验证。",
          "skill_path": "functional-validation-rules/SKILL.md",
          "directory_path": "functional-validation-rules",
          "directory": "functional-validation-rules",
          "sections": [
            "Skill 作用与适用场景",
            "自动触发信号",
            "进入后先做什么",
            "默认执行流程",
            "权责边界与不负责事项",
            "需要暂停并确认的条件",
            "执行通过 / 驳回标准",
            "执行结果归档要求",
            "references 读取规则"
          ],
          "references": [
            "functional-validation-rules/references/validation-boundaries.md",
            "functional-validation-rules/references/validation-scope.md",
            "functional-validation-rules/references/validation-template-and-examples.md"
          ],
          "agents": [
            "functional-validation-rules/agents/openai.yaml"
          ],
          "has_license": false,
          "focus_points": [
            "优先检查 description 是否具体到触发信号，而不是只写抽象用途。",
            "检查 references 是否足以承接复杂场景，避免 SKILL.md 过厚或过空。",
            "重点看测试策略、资源、功能验证、联调、回归是否已经拆开。"
          ]
        },
        {
          "id": "test-regression-rules",
          "name": "test-regression-rules",
          "title": "回归验证规则",
          "status": "implemented",
          "status_label": "已实现",
          "domain_id": "test",
          "domain_label": "测试域",
          "domain_description": "策略、资源、功能验证、联调、回归",
          "domain_order": 7,
          "item_order": 7,
          "auto_trigger": "当 Bug 修复、原有功能迭代、公共模块修改、共享逻辑调整、接口兼容性变化后准备执行测试时触发。负责判定回归范围、选择回归用例、验证兼容性影响并输出回归结论；必须以 `test-location-rules` 为基准，把回归结论统一写回 `test/yyyy-MM-DD_HHmmss/测试任务中文简介/README.md`，并把详细回归案例、执行证据和补充说明放到同一时间戳根目录下的 ASCII 真实代码路径镜像目录中；不要用它代替 functional-validation-rules、test-strategy-rules、integration-debugging-rules 或测试资源管理类规则。",
          "core_responsibility": "明确回归测试的范围、用例选取、验证要点，针对改动点关联的功能、上下游链路做全覆盖验证，防止修复旧 Bug 引入新问题，保障功能兼容性。",
          "skill_path": "test-regression-rules/SKILL.md",
          "directory_path": "test-regression-rules",
          "directory": "test-regression-rules",
          "sections": [
            "Skill 作用与适用场景",
            "自动触发信号",
            "进入后先做什么",
            "默认执行流程",
            "权责边界与不负责事项",
            "需要暂停并确认的条件",
            "执行通过 / 驳回标准",
            "执行结果归档要求",
            "references 读取规则"
          ],
          "references": [
            "test-regression-rules/references/regression-boundaries.md",
            "test-regression-rules/references/regression-scope-selection.md",
            "test-regression-rules/references/regression-template-and-examples.md"
          ],
          "agents": [
            "test-regression-rules/agents/openai.yaml"
          ],
          "has_license": false,
          "focus_points": [
            "优先检查 description 是否具体到触发信号，而不是只写抽象用途。",
            "检查 references 是否足以承接复杂场景，避免 SKILL.md 过厚或过空。",
            "重点看测试策略、资源、功能验证、联调、回归是否已经拆开。"
          ]
        },
        {
          "id": "integration-debugging-rules",
          "name": "integration-debugging-rules",
          "title": "integration-debugging-rules",
          "status": "planned",
          "status_label": "规划中",
          "domain_id": "test",
          "domain_label": "测试域",
          "domain_description": "策略、资源、功能验证、联调、回归",
          "domain_order": 7,
          "item_order": 8,
          "auto_trigger": "当联调、排查接口不通、字段不一致、环境差异、trace 断链、测试环境问题时自动触发。",
          "core_responsibility": "统一联调和排障证据记录。",
          "skill_path": "",
          "directory_path": "",
          "directory": "",
          "sections": [],
          "references": [],
          "agents": [],
          "has_license": false,
          "focus_points": [
            "先补齐触发 description、邻接边界和最小 references，再决定是否正式建目录。",
            "优先确认它与同域相邻 skill 的拆分边界，避免新建后职责重叠。",
            "重点看测试策略、资源、功能验证、联调、回归是否已经拆开。"
          ]
        }
      ]
    },
    {
      "id": "delivery",
      "label": "交付域",
      "description": "Git 协作、评审、发布与交付说明",
      "order": 8,
      "implemented_count": 2,
      "planned_count": 2,
      "seed_count": 0,
      "total_count": 4,
      "items": [
        {
          "id": "release-rollout-rules",
          "name": "release-rollout-rules",
          "title": "release-rollout-rules",
          "status": "planned",
          "status_label": "规划中",
          "domain_id": "delivery",
          "domain_label": "交付域",
          "domain_description": "Git 协作、评审、发布与交付说明",
          "domain_order": 8,
          "item_order": 1,
          "auto_trigger": "当新增或修改发布脚本、发布检查、灰度策略、观察窗口、上线 checklist、回滚条件时自动触发。",
          "core_responsibility": "管理上线和回滚规则。",
          "skill_path": "",
          "directory_path": "",
          "directory": "",
          "sections": [],
          "references": [],
          "agents": [],
          "has_license": false,
          "focus_points": [
            "先补齐触发 description、邻接边界和最小 references，再决定是否正式建目录。",
            "优先确认它与同域相邻 skill 的拆分边界，避免新建后职责重叠。",
            "重点看 Git 协作、评审、发布、交付说明是否已分层收口。"
          ]
        },
        {
          "id": "code-review-rules",
          "name": "code-review-rules",
          "title": "code-review-rules",
          "status": "planned",
          "status_label": "规划中",
          "domain_id": "delivery",
          "domain_label": "交付域",
          "domain_description": "Git 协作、评审、发布与交付说明",
          "domain_order": 8,
          "item_order": 2,
          "auto_trigger": "当任务是 PR 评审、他人代码评审、检查 diff、风险扫描、测试遗漏检查或交付前复查时自动触发。",
          "core_responsibility": "统一评审重点和输出方式，不替代编码完成后的自审。",
          "skill_path": "",
          "directory_path": "",
          "directory": "",
          "sections": [],
          "references": [],
          "agents": [],
          "has_license": false,
          "focus_points": [
            "先补齐触发 description、邻接边界和最小 references，再决定是否正式建目录。",
            "优先确认它与同域相邻 skill 的拆分边界，避免新建后职责重叠。",
            "重点看 Git 协作、评审、发布、交付说明是否已分层收口。"
          ]
        },
        {
          "id": "git-collaboration-rules",
          "name": "git-collaboration-rules",
          "title": "Git 协作规则",
          "status": "implemented",
          "status_label": "已实现",
          "domain_id": "delivery",
          "domain_label": "交付域",
          "domain_description": "Git 协作、评审、发布与交付说明",
          "domain_order": 8,
          "item_order": 3,
          "auto_trigger": "当准备整理提交、拆提交粒度、同步分支、处理协作变更、准备 PR 或合并前收口时触发。负责提交粒度、提交说明、分支同步、协作边界和 PR 整理；提交代码时必须分析未提交的代码，如果可以分成不同的业务修改，就用多次不同的 git 提交；git 提交消息必须遵循 feat/fix 等格式；不要把它代替代码评审或发布上线规则。",
          "core_responsibility": "统一 Git 协作规则。",
          "skill_path": "git-collaboration-rules/SKILL.md",
          "directory_path": "git-collaboration-rules",
          "directory": "git-collaboration-rules",
          "sections": [
            "Skill 作用与适用场景",
            "自动触发信号",
            "进入后先做什么",
            "默认执行流程",
            "权责边界与不负责事项",
            "需要暂停并确认的条件",
            "执行通过 / 驳回标准",
            "执行结果归档要求",
            "references 读取规则"
          ],
          "references": [
            "git-collaboration-rules/references/branch-and-commit.md",
            "git-collaboration-rules/references/collaboration-examples.md",
            "git-collaboration-rules/references/sync-and-pr-scope.md"
          ],
          "agents": [
            "git-collaboration-rules/agents/openai.yaml"
          ],
          "has_license": false,
          "focus_points": [
            "优先检查 description 是否具体到触发信号，而不是只写抽象用途。",
            "检查 references 是否足以承接复杂场景，避免 SKILL.md 过厚或过空。",
            "重点看 Git 协作、评审、发布、交付说明是否已分层收口。"
          ]
        },
        {
          "id": "delivery-summary-rules",
          "name": "delivery-summary-rules",
          "title": "交付总结规则",
          "status": "implemented",
          "status_label": "已实现",
          "domain_id": "delivery",
          "domain_label": "交付域",
          "domain_description": "Git 协作、评审、发布与交付说明",
          "domain_order": 8,
          "item_order": 4,
          "auto_trigger": "当开发人员提出“请帮我生成交付文档”“发布文档”“发布总结文档”“准备上线总结文档”等请求，需要输出一份可交接、可发布、可复盘的总结文档时触发。负责交付说明结构、Git 提交范围汇总、验证摘要、风险说明、保存位置和后续建议；必须先得到用户确认是否开始发布总结，不要把它代替发布动作或代码评审。",
          "core_responsibility": "统一交付文档结构。",
          "skill_path": "delivery-summary-rules/SKILL.md",
          "directory_path": "delivery-summary-rules",
          "directory": "delivery-summary-rules",
          "sections": [
            "Skill 作用与适用场景",
            "自动触发信号",
            "进入后先做什么",
            "默认执行流程",
            "权责边界与不负责事项",
            "需要暂停并确认的条件",
            "执行通过 / 驳回标准",
            "执行结果归档要求",
            "references 读取规则"
          ],
          "references": [
            "delivery-summary-rules/references/delivery-examples.md",
            "delivery-summary-rules/references/delivery-risk-and-debt.md",
            "delivery-summary-rules/references/delivery-template.md"
          ],
          "agents": [
            "delivery-summary-rules/agents/openai.yaml"
          ],
          "has_license": false,
          "focus_points": [
            "优先检查 description 是否具体到触发信号，而不是只写抽象用途。",
            "检查 references 是否足以承接复杂场景，避免 SKILL.md 过厚或过空。",
            "重点看 Git 协作、评审、发布、交付说明是否已分层收口。"
          ]
        }
      ]
    },
    {
      "id": "evolution",
      "label": "体系维护域",
      "description": "维护 skill 体系自身的拆分、迁移与演进",
      "order": 9,
      "implemented_count": 0,
      "planned_count": 1,
      "seed_count": 0,
      "total_count": 1,
      "items": [
        {
          "id": "skill-evolution-rules",
          "name": "skill-evolution-rules",
          "title": "skill-evolution-rules",
          "status": "planned",
          "status_label": "规划中",
          "domain_id": "evolution",
          "domain_label": "体系维护域",
          "domain_description": "维护 skill 体系自身的拆分、迁移与演进",
          "domain_order": 9,
          "item_order": 1,
          "auto_trigger": "当新增、修改、拆分、合并团队内部 skill，或发现某类规则应当迁移到其他 skill 中时自动触发。",
          "core_responsibility": "维护 skill 体系自身的拆分和演进规则。",
          "skill_path": "",
          "directory_path": "",
          "directory": "",
          "sections": [],
          "references": [],
          "agents": [],
          "has_license": false,
          "focus_points": [
            "先补齐触发 description、邻接边界和最小 references，再决定是否正式建目录。",
            "优先确认它与同域相邻 skill 的拆分边界，避免新建后职责重叠。",
            "重点看新增、合并、迁移和退休 skill 的门槛是否足够明确。"
          ]
        }
      ]
    },
    {
      "id": "seed",
      "label": "扩展种子",
      "description": "已入库但未并入主规划的参考 skill",
      "order": 10,
      "implemented_count": 0,
      "planned_count": 0,
      "seed_count": 0,
      "total_count": 0,
      "items": []
    }
  ],
  "items": [
    {
      "id": "team-development-rules",
      "name": "team-development-rules",
      "title": "团队研发总控规则",
      "status": "implemented",
      "status_label": "已实现",
      "domain_id": "orchestration",
      "domain_label": "总控层",
      "domain_description": "流程分流、冲突裁决、阶段阻断",
      "domain_order": 1,
      "item_order": 1,
      "auto_trigger": "当任务阶段不明确、领域边界不清、多个 skill 同时触发、流程需要暂停/重启/继续/终止，或用户明确要求按团队完整研发流程处理时触发。负责阶段分析、路由分流、冲突裁决和流程阻断；不要在单一明确的 SQL、API、配置、测试、评审等任务中触发。",
      "core_responsibility": "作为弱触发协调层，负责阶段分析、路由分流、冲突裁决和中断管控，不承载数据库、API、错误处理等细节规则，也不替代小 skill 执行。",
      "skill_path": "team-development-rules/SKILL.md",
      "directory_path": "team-development-rules",
      "directory": "team-development-rules",
      "sections": [
        "Skill 作用与适用场景",
        "自动触发信号",
        "进入后先做什么",
        "默认执行流程",
        "权责边界与不负责事项",
        "需要暂停并确认的条件",
        "执行通过 / 驳回标准",
        "执行结果归档要求",
        "references 读取规则"
      ],
      "references": [
        "team-development-rules/references/05-method-change-guard.md",
        "team-development-rules/references/conflict-examples.md",
        "team-development-rules/references/routing-rules.md",
        "team-development-rules/references/stage-blockers.md"
      ],
      "agents": [
        "team-development-rules/agents/openai.yaml"
      ],
      "has_license": false,
      "focus_points": [
        "优先检查 description 是否具体到触发信号，而不是只写抽象用途。",
        "检查 references 是否足以承接复杂场景，避免 SKILL.md 过厚或过空。",
        "重点看是否只做分流和阻断，没有越权覆盖单域 skill。"
      ]
    },
    {
      "id": "requirement-intake-rules",
      "name": "requirement-intake-rules",
      "title": "需求接入规则",
      "status": "implemented",
      "status_label": "已实现",
      "domain_id": "requirement",
      "domain_label": "需求域",
      "domain_description": "需求澄清、缺口识别、边界确认、验收前置",
      "domain_order": 2,
      "item_order": 1,
      "auto_trigger": "当用户提出新需求、新功能、新页面、新接口、新模块，且任务刚进入研发阶段、尚未进入实现或 Bug 定位时触发。支持从需求 URL、零散资料、物料和补充说明中整理需求，补齐到可进入后续代码开发的程度，并将结果沉淀到 `ment/` 目录；它同时定义需求域统一文档入口，同一需求后续只能持续更新这一份文档；不要用它代替需求缺口、边界、拆分、变更或验收标准类 skill。",
      "core_responsibility": "先理解目标、背景、上下游和输入输出。",
      "skill_path": "requirement-intake-rules/SKILL.md",
      "directory_path": "requirement-intake-rules",
      "directory": "requirement-intake-rules",
      "sections": [
        "Skill 作用与适用场景",
        "自动触发信号",
        "进入后先做什么",
        "默认执行流程",
        "权责边界与不负责事项",
        "需要暂停并确认的条件",
        "执行通过 / 驳回标准",
        "执行结果归档要求",
        "references 读取规则"
      ],
      "references": [
        "requirement-intake-rules/references/intake-boundaries-and-examples.md",
        "requirement-intake-rules/references/intake-checklist.md",
        "requirement-intake-rules/references/requirement-structure-template.md"
      ],
      "agents": [
        "requirement-intake-rules/agents/openai.yaml"
      ],
      "has_license": false,
      "focus_points": [
        "优先检查 description 是否具体到触发信号，而不是只写抽象用途。",
        "检查 references 是否足以承接复杂场景，避免 SKILL.md 过厚或过空。",
        "重点看是否能区分需求缺口、边界变化、验收偏差和历史 Bug。"
      ]
    },
    {
      "id": "requirement-gap-rules",
      "name": "requirement-gap-rules",
      "title": "需求缺口识别规则",
      "status": "implemented",
      "status_label": "已实现",
      "domain_id": "requirement",
      "domain_label": "需求域",
      "domain_description": "需求澄清、缺口识别、边界确认、验收前置",
      "domain_order": 2,
      "item_order": 2,
      "auto_trigger": "当需求描述不完整、缺少前提、缺少字段、缺少流程、缺少业务规则、缺少依赖条件或缺少验收信息时触发。负责识别需求缺口并在信息不足时阻断盲目编码推进，同时将缺口分析结果持续更新到 `requirement-intake-rules` 约定的同一个 `ment/` 需求文档中；不要用它代替需求边界判断、需求变更判断或验收标准细化 skill。",
      "core_responsibility": "识别缺失信息并暂停盲目实现。",
      "skill_path": "requirement-gap-rules/SKILL.md",
      "directory_path": "requirement-gap-rules",
      "directory": "requirement-gap-rules",
      "sections": [
        "Skill 作用与适用场景",
        "自动触发信号",
        "进入后先做什么",
        "默认执行流程",
        "权责边界与不负责事项",
        "需要暂停并确认的条件",
        "执行通过 / 驳回标准",
        "执行结果归档要求",
        "references 读取规则"
      ],
      "references": [
        "requirement-gap-rules/references/missing-info-checklist.md",
        "requirement-gap-rules/references/pause-triggers.md",
        "requirement-gap-rules/references/requirement-gap-examples.md"
      ],
      "agents": [
        "requirement-gap-rules/agents/openai.yaml"
      ],
      "has_license": false,
      "focus_points": [
        "优先检查 description 是否具体到触发信号，而不是只写抽象用途。",
        "检查 references 是否足以承接复杂场景，避免 SKILL.md 过厚或过空。",
        "重点看是否能区分需求缺口、边界变化、验收偏差和历史 Bug。"
      ]
    },
    {
      "id": "requirement-boundary-rules",
      "name": "requirement-boundary-rules",
      "title": "需求边界判定规则",
      "status": "implemented",
      "status_label": "已实现",
      "domain_id": "requirement",
      "domain_label": "需求域",
      "domain_description": "需求澄清、缺口识别、边界确认、验收前置",
      "domain_order": 2,
      "item_order": 3,
      "auto_trigger": "当需求边界不清、影响范围不明、兼容性不明确、是否允许改旧逻辑不清楚，或需要区分当前需求、历史问题、需求变更和验收偏差时触发。负责明确改动边界和影响面，并将边界结论持续更新到 `requirement-intake-rules` 约定的同一个 `ment/` 需求文档中；不要用它代替需求缺口识别或 Bug 根因定位 skill。",
      "core_responsibility": "明确改动边界和影响面。",
      "skill_path": "requirement-boundary-rules/SKILL.md",
      "directory_path": "requirement-boundary-rules",
      "directory": "requirement-boundary-rules",
      "sections": [
        "Skill 作用与适用场景",
        "自动触发信号",
        "进入后先做什么",
        "默认执行流程",
        "权责边界与不负责事项",
        "需要暂停并确认的条件",
        "执行通过 / 驳回标准",
        "执行结果归档要求",
        "references 读取规则"
      ],
      "references": [
        "requirement-boundary-rules/references/acceptance-routing-examples.md",
        "requirement-boundary-rules/references/boundary-checklist.md",
        "requirement-boundary-rules/references/history-vs-change.md"
      ],
      "agents": [
        "requirement-boundary-rules/agents/openai.yaml"
      ],
      "has_license": false,
      "focus_points": [
        "优先检查 description 是否具体到触发信号，而不是只写抽象用途。",
        "检查 references 是否足以承接复杂场景，避免 SKILL.md 过厚或过空。",
        "重点看是否能区分需求缺口、边界变化、验收偏差和历史 Bug。"
      ]
    },
    {
      "id": "requirement-splitting-rules",
      "name": "requirement-splitting-rules",
      "title": "需求拆分规则",
      "status": "implemented",
      "status_label": "已实现",
      "domain_id": "requirement",
      "domain_label": "需求域",
      "domain_description": "需求澄清、缺口识别、边界确认、验收前置",
      "domain_order": 2,
      "item_order": 4,
      "auto_trigger": "当需求较大、涉及多个模块、多个接口、多个页面、多个步骤或多个角色协作，无法作为单一实现单元稳定推进时触发。负责拆出任务边界、实施顺序和最小闭环，并将拆分结果持续更新到 `requirement-intake-rules` 约定的同一个 `ment/` 需求文档中；不要用它代替需求接入、边界确认或项目排期管理。",
      "core_responsibility": "负责任务拆分、模块拆分和实施顺序。",
      "skill_path": "requirement-splitting-rules/SKILL.md",
      "directory_path": "requirement-splitting-rules",
      "directory": "requirement-splitting-rules",
      "sections": [
        "Skill 作用与适用场景",
        "自动触发信号",
        "进入后先做什么",
        "默认执行流程",
        "权责边界与不负责事项",
        "需要暂停并确认的条件",
        "执行通过 / 驳回标准",
        "执行结果归档要求",
        "references 读取规则"
      ],
      "references": [
        "requirement-splitting-rules/references/splitting-dimensions.md",
        "requirement-splitting-rules/references/splitting-examples.md",
        "requirement-splitting-rules/references/splitting-sequence.md"
      ],
      "agents": [
        "requirement-splitting-rules/agents/openai.yaml"
      ],
      "has_license": false,
      "focus_points": [
        "优先检查 description 是否具体到触发信号，而不是只写抽象用途。",
        "检查 references 是否足以承接复杂场景，避免 SKILL.md 过厚或过空。",
        "重点看是否能区分需求缺口、边界变化、验收偏差和历史 Bug。"
      ]
    },
    {
      "id": "requirement-change-rules",
      "name": "requirement-change-rules",
      "title": "需求变更确认规则",
      "status": "implemented",
      "status_label": "已实现",
      "domain_id": "requirement",
      "domain_label": "需求域",
      "domain_description": "需求澄清、缺口识别、边界确认、验收前置",
      "domain_order": 2,
      "item_order": 5,
      "auto_trigger": "当编码过程中需求被补充、修正、插入新条件、改变优先级、调整默认值或交付物形态时触发。负责识别变更类型、重算影响范围和决定是否需要回退前序结论，并将变更结果持续更新到 `requirement-intake-rules` 约定的同一个 `ment/` 需求文档中；不要把历史缺陷误当成需求变更。",
      "core_responsibility": "重新确认变更范围和影响。",
      "skill_path": "requirement-change-rules/SKILL.md",
      "directory_path": "requirement-change-rules",
      "directory": "requirement-change-rules",
      "sections": [
        "Skill 作用与适用场景",
        "自动触发信号",
        "进入后先做什么",
        "默认执行流程",
        "权责边界与不负责事项",
        "需要暂停并确认的条件",
        "执行通过 / 驳回标准",
        "执行结果归档要求",
        "references 读取规则"
      ],
      "references": [
        "requirement-change-rules/references/change-classification.md",
        "requirement-change-rules/references/change-decision-examples.md",
        "requirement-change-rules/references/impact-recheck.md"
      ],
      "agents": [
        "requirement-change-rules/agents/openai.yaml"
      ],
      "has_license": false,
      "focus_points": [
        "优先检查 description 是否具体到触发信号，而不是只写抽象用途。",
        "检查 references 是否足以承接复杂场景，避免 SKILL.md 过厚或过空。",
        "重点看是否能区分需求缺口、边界变化、验收偏差和历史 Bug。"
      ]
    },
    {
      "id": "acceptance-criteria-rules",
      "name": "acceptance-criteria-rules",
      "title": "验收标准细化规则",
      "status": "implemented",
      "status_label": "已实现",
      "domain_id": "requirement",
      "domain_label": "需求域",
      "domain_description": "需求澄清、缺口识别、边界确认、验收前置",
      "domain_order": 2,
      "item_order": 6,
      "auto_trigger": "当任务准备进入实现前确认，或交付前需要把“做到什么算完成”写成可验证、可测试、可复核的标准时触发。负责细化成功条件、异常条件、边界条件和不在范围项，并将验收标准单独保存到 `ment/` 下的验收文档中；不要用它代替功能验证或回归验证。",
      "core_responsibility": "补齐可验证、可测试的验收标准。",
      "skill_path": "acceptance-criteria-rules/SKILL.md",
      "directory_path": "acceptance-criteria-rules",
      "directory": "acceptance-criteria-rules",
      "sections": [
        "Skill 作用与适用场景",
        "自动触发信号",
        "进入后先做什么",
        "默认执行流程",
        "权责边界与不负责事项",
        "需要暂停并确认的条件",
        "执行通过 / 驳回标准",
        "执行结果归档要求",
        "references 读取规则"
      ],
      "references": [
        "acceptance-criteria-rules/references/acceptance-boundaries.md",
        "acceptance-criteria-rules/references/acceptance-template.md",
        "acceptance-criteria-rules/references/testable-criteria-checklist.md"
      ],
      "agents": [
        "acceptance-criteria-rules/agents/openai.yaml"
      ],
      "has_license": false,
      "focus_points": [
        "优先检查 description 是否具体到触发信号，而不是只写抽象用途。",
        "检查 references 是否足以承接复杂场景，避免 SKILL.md 过厚或过空。",
        "重点看是否能区分需求缺口、边界变化、验收偏差和历史 Bug。"
      ]
    },
    {
      "id": "bug-intake-rules",
      "name": "bug-intake-rules",
      "title": "Bug 问题录入规则",
      "status": "implemented",
      "status_label": "已实现",
      "domain_id": "bug",
      "domain_label": "Bug 域",
      "domain_description": "问题录入、定位、运行时诊断、修复建议",
      "domain_order": 3,
      "item_order": 1,
      "auto_trigger": "当用户描述报错、异常行为、结果不符、线上问题、偶发问题、接口异常、页面异常、数据错误或性能异常时触发。负责把 Bug 描述标准化，整理现象、影响范围、环境条件、期望结果和实际结果，并统一建立 Bug 根目录记录；不要用它代替根因定位、运行时调试或修复方案制定 skill。",
      "core_responsibility": "把问题描述标准化。",
      "skill_path": "bug-intake-rules/SKILL.md",
      "directory_path": "bug-intake-rules",
      "directory": "bug-intake-rules",
      "sections": [
        "Skill 作用与适用场景",
        "自动触发信号",
        "进入后先做什么",
        "默认执行流程",
        "权责边界与不负责事项",
        "需要暂停并确认的条件",
        "执行通过 / 驳回标准",
        "执行结果归档要求",
        "references 读取规则"
      ],
      "references": [
        "bug-intake-rules/references/bug-description-template.md",
        "bug-intake-rules/references/intake-examples.md",
        "bug-intake-rules/references/minimum-intake-fields.md"
      ],
      "agents": [
        "bug-intake-rules/agents/openai.yaml"
      ],
      "has_license": false,
      "focus_points": [
        "优先检查 description 是否具体到触发信号，而不是只写抽象用途。",
        "检查 references 是否足以承接复杂场景，避免 SKILL.md 过厚或过空。",
        "重点看静态定位与运行时诊断的切换条件是否清楚。"
      ]
    },
    {
      "id": "bug-gap-rules",
      "name": "bug-gap-rules",
      "title": "Bug 缺口识别规则",
      "status": "implemented",
      "status_label": "已实现",
      "domain_id": "bug",
      "domain_label": "Bug 域",
      "domain_description": "问题录入、定位、运行时诊断、修复建议",
      "domain_order": 3,
      "item_order": 2,
      "auto_trigger": "当 Bug 描述缺少复现条件、环境信息、输入数据、报错日志、影响范围或关键时间线，导致后续复现与定位无法可靠推进时触发。负责识别缺失项、区分阻断级与非阻断级缺口，并统一记录到 Bug 根目录，阻止盲目进入定位。",
      "core_responsibility": "补齐定位所需基础信息。",
      "skill_path": "bug-gap-rules/SKILL.md",
      "directory_path": "bug-gap-rules",
      "directory": "bug-gap-rules",
      "sections": [
        "Skill 作用与适用场景",
        "自动触发信号",
        "进入后先做什么",
        "默认执行流程",
        "权责边界与不负责事项",
        "需要暂停并确认的条件",
        "执行通过 / 驳回标准",
        "执行结果归档要求",
        "references 读取规则"
      ],
      "references": [
        "bug-gap-rules/references/blocking-signals.md",
        "bug-gap-rules/references/gap-checklist.md",
        "bug-gap-rules/references/gap-examples.md"
      ],
      "agents": [
        "bug-gap-rules/agents/openai.yaml"
      ],
      "has_license": false,
      "focus_points": [
        "优先检查 description 是否具体到触发信号，而不是只写抽象用途。",
        "检查 references 是否足以承接复杂场景，避免 SKILL.md 过厚或过空。",
        "重点看静态定位与运行时诊断的切换条件是否清楚。"
      ]
    },
    {
      "id": "bug-reproduction-rules",
      "name": "bug-reproduction-rules",
      "title": "Bug 复现规则",
      "status": "implemented",
      "status_label": "已实现",
      "domain_id": "bug",
      "domain_label": "Bug 域",
      "domain_description": "问题录入、定位、运行时诊断、修复建议",
      "domain_order": 3,
      "item_order": 3,
      "auto_trigger": "当问题需要构造步骤、确定触发条件、判断是否稳定发生、确认出现频率或复现环境时触发。负责输出复现路径、稳定性判断、Bug 根目录记录和无法复现时的结论处理；不要用它代替根因分析。",
      "core_responsibility": "输出复现步骤和复现结论。",
      "skill_path": "bug-reproduction-rules/SKILL.md",
      "directory_path": "bug-reproduction-rules",
      "directory": "bug-reproduction-rules",
      "sections": [
        "Skill 作用与适用场景",
        "自动触发信号",
        "进入后先做什么",
        "默认执行流程",
        "权责边界与不负责事项",
        "需要暂停并确认的条件",
        "执行通过 / 驳回标准",
        "执行结果归档要求",
        "references 读取规则"
      ],
      "references": [
        "bug-reproduction-rules/references/reproduction-examples.md",
        "bug-reproduction-rules/references/reproduction-template.md",
        "bug-reproduction-rules/references/stability-checks.md"
      ],
      "agents": [
        "bug-reproduction-rules/agents/openai.yaml"
      ],
      "has_license": false,
      "focus_points": [
        "优先检查 description 是否具体到触发信号，而不是只写抽象用途。",
        "检查 references 是否足以承接复杂场景，避免 SKILL.md 过厚或过空。",
        "重点看静态定位与运行时诊断的切换条件是否清楚。"
      ]
    },
    {
      "id": "bug-root-cause-rules",
      "name": "bug-root-cause-rules",
      "title": "Bug 根因定位规则",
      "status": "implemented",
      "status_label": "已实现",
      "domain_id": "bug",
      "domain_label": "Bug 域",
      "domain_description": "问题录入、定位、运行时诊断、修复建议",
      "domain_order": 3,
      "item_order": 5,
      "auto_trigger": "当开始分析代码、追调用链、看现有日志、查 trace、结合上下游行为定位 Bug 根因时触发。负责通过静态证据收敛根因、统一记录到 Bug 根目录并区分实现问题与设计问题；不要用它代替运行时调试或修复方案制定 skill。",
      "core_responsibility": "找出根因并区分实现问题与设计问题。",
      "skill_path": "bug-root-cause-rules/SKILL.md",
      "directory_path": "bug-root-cause-rules",
      "directory": "bug-root-cause-rules",
      "sections": [
        "Skill 作用与适用场景",
        "自动触发信号",
        "进入后先做什么",
        "默认执行流程",
        "权责边界与不负责事项",
        "需要暂停并确认的条件",
        "执行通过 / 驳回标准",
        "执行结果归档要求",
        "references 读取规则"
      ],
      "references": [
        "bug-root-cause-rules/references/root-cause-evidence.md",
        "bug-root-cause-rules/references/static-analysis-path.md",
        "bug-root-cause-rules/references/when-to-stop-static-analysis.md"
      ],
      "agents": [
        "bug-root-cause-rules/agents/openai.yaml"
      ],
      "has_license": false,
      "focus_points": [
        "优先检查 description 是否具体到触发信号，而不是只写抽象用途。",
        "检查 references 是否足以承接复杂场景，避免 SKILL.md 过厚或过空。",
        "重点看静态定位与运行时诊断的切换条件是否清楚。"
      ]
    },
    {
      "id": "bug-runtime-debug-rules",
      "name": "bug-runtime-debug-rules",
      "title": "Bug 运行时诊断规则",
      "status": "implemented",
      "status_label": "已实现",
      "domain_id": "bug",
      "domain_label": "Bug 域",
      "domain_description": "问题录入、定位、运行时诊断、修复建议",
      "domain_order": 3,
      "item_order": 6,
      "auto_trigger": "当仅靠静态分析不能稳定定位 Bug，且需要在运行过程中通过断点、单步执行、变量观察、调用栈观察、条件命中判断、debug 日志或运行时证据来缩小问题范围时触发。负责运行时诊断进入条件、观察方式、退出条件和证据回流；不要把它当成默认第一选择。",
      "core_responsibility": "通过运行时调试缩小问题范围并定位异常位置。",
      "skill_path": "bug-runtime-debug-rules/SKILL.md",
      "directory_path": "bug-runtime-debug-rules",
      "directory": "bug-runtime-debug-rules",
      "sections": [
        "Skill 作用与适用场景",
        "自动触发信号",
        "进入后先做什么",
        "默认执行流程",
        "权责边界与不负责事项",
        "需要暂停并确认的条件",
        "执行通过 / 驳回标准",
        "执行结果归档要求",
        "references 读取规则"
      ],
      "references": [
        "bug-runtime-debug-rules/references/runtime-entry-conditions.md",
        "bug-runtime-debug-rules/references/runtime-exit-and-handoff.md",
        "bug-runtime-debug-rules/references/runtime-observation-methods.md"
      ],
      "agents": [
        "bug-runtime-debug-rules/agents/openai.yaml"
      ],
      "has_license": false,
      "focus_points": [
        "优先检查 description 是否具体到触发信号，而不是只写抽象用途。",
        "检查 references 是否足以承接复杂场景，避免 SKILL.md 过厚或过空。",
        "重点看静态定位与运行时诊断的切换条件是否清楚。"
      ]
    },
    {
      "id": "bug-debug-log-rules",
      "name": "bug-debug-log-rules",
      "title": "Bug 调试日志规则",
      "status": "implemented",
      "status_label": "已实现",
      "domain_id": "bug",
      "domain_label": "Bug 域",
      "domain_description": "问题录入、定位、运行时诊断、修复建议",
      "domain_order": 3,
      "item_order": 7,
      "auto_trigger": "当定位 Bug 需要临时增加 debug 日志、关键变量输出、关键分支日志、上下游输入输出日志或时间线日志来补充运行时证据时触发。负责日志落点、日志粒度、Bug 根目录记录、可回收性和清理要求；不要把临时诊断日志混成正式日志策略。",
      "core_responsibility": "通过可回收的临时日志补充运行期证据。",
      "skill_path": "bug-debug-log-rules/SKILL.md",
      "directory_path": "bug-debug-log-rules",
      "directory": "bug-debug-log-rules",
      "sections": [
        "Skill 作用与适用场景",
        "自动触发信号",
        "进入后先做什么",
        "默认执行流程",
        "权责边界与不负责事项",
        "需要暂停并确认的条件",
        "执行通过 / 驳回标准",
        "执行结果归档要求",
        "references 读取规则"
      ],
      "references": [
        "bug-debug-log-rules/references/debug-log-cleanup.md",
        "bug-debug-log-rules/references/debug-log-examples.md",
        "bug-debug-log-rules/references/debug-log-placement.md"
      ],
      "agents": [
        "bug-debug-log-rules/agents/openai.yaml"
      ],
      "has_license": false,
      "focus_points": [
        "优先检查 description 是否具体到触发信号，而不是只写抽象用途。",
        "检查 references 是否足以承接复杂场景，避免 SKILL.md 过厚或过空。",
        "重点看静态定位与运行时诊断的切换条件是否清楚。"
      ]
    },
    {
      "id": "bug-assertion-diagnostic-rules",
      "name": "bug-assertion-diagnostic-rules",
      "title": "Bug 断言诊断规则",
      "status": "implemented",
      "status_label": "已实现",
      "domain_id": "bug",
      "domain_label": "Bug 域",
      "domain_description": "问题录入、定位、运行时诊断、修复建议",
      "domain_order": 3,
      "item_order": 8,
      "auto_trigger": "当怀疑状态异常、顺序错误、数据污染、不变量被破坏，且需要通过程序断言、诊断性检查、快速失败或区间收缩来暴露问题位置时触发。负责断言进入条件、放置位置、Bug 根目录记录和删除收口要求；不要把诊断断言长期留作正式业务逻辑。",
      "core_responsibility": "用断言和诊断检查缩小 bug 发生区间。",
      "skill_path": "bug-assertion-diagnostic-rules/SKILL.md",
      "directory_path": "bug-assertion-diagnostic-rules",
      "directory": "bug-assertion-diagnostic-rules",
      "sections": [
        "Skill 作用与适用场景",
        "自动触发信号",
        "进入后先做什么",
        "默认执行流程",
        "权责边界与不负责事项",
        "需要暂停并确认的条件",
        "执行通过 / 驳回标准",
        "执行结果归档要求",
        "references 读取规则"
      ],
      "references": [
        "bug-assertion-diagnostic-rules/references/assertion-entry-conditions.md",
        "bug-assertion-diagnostic-rules/references/assertion-examples.md",
        "bug-assertion-diagnostic-rules/references/assertion-placement.md"
      ],
      "agents": [
        "bug-assertion-diagnostic-rules/agents/openai.yaml"
      ],
      "has_license": false,
      "focus_points": [
        "优先检查 description 是否具体到触发信号，而不是只写抽象用途。",
        "检查 references 是否足以承接复杂场景，避免 SKILL.md 过厚或过空。",
        "重点看静态定位与运行时诊断的切换条件是否清楚。"
      ]
    },
    {
      "id": "bug-fix-proposal-rules",
      "name": "bug-fix-proposal-rules",
      "title": "Bug 修复建议规则",
      "status": "implemented",
      "status_label": "已实现",
      "domain_id": "bug",
      "domain_label": "Bug 域",
      "domain_description": "问题录入、定位、运行时诊断、修复建议",
      "domain_order": 3,
      "item_order": 9,
      "auto_trigger": "当问题已定位，需要形成修改建议、风险评估、备选方案并判断是否应等待用户确认时触发。负责把 Bug 域稳定交接到编码域，并统一记录到 Bug 根目录；不要用它代替根因定位或直接实施编码修复。",
      "core_responsibility": "先给修改建议，再决定是否实施。",
      "skill_path": "bug-fix-proposal-rules/SKILL.md",
      "directory_path": "bug-fix-proposal-rules",
      "directory": "bug-fix-proposal-rules",
      "sections": [
        "Skill 作用与适用场景",
        "自动触发信号",
        "进入后先做什么",
        "默认执行流程",
        "权责边界与不负责事项",
        "需要暂停并确认的条件",
        "执行通过 / 驳回标准",
        "执行结果归档要求",
        "references 读取规则"
      ],
      "references": [
        "bug-fix-proposal-rules/references/confirm-before-coding.md",
        "bug-fix-proposal-rules/references/fix-proposal-template.md",
        "bug-fix-proposal-rules/references/risk-assessment-checklist.md"
      ],
      "agents": [
        "bug-fix-proposal-rules/agents/openai.yaml"
      ],
      "has_license": false,
      "focus_points": [
        "优先检查 description 是否具体到触发信号，而不是只写抽象用途。",
        "检查 references 是否足以承接复杂场景，避免 SKILL.md 过厚或过空。",
        "重点看静态定位与运行时诊断的切换条件是否清楚。"
      ]
    },
    {
      "id": "bug-regression-risk-rules",
      "name": "bug-regression-risk-rules",
      "title": "Bug 回归风险规则",
      "status": "implemented",
      "status_label": "已实现",
      "domain_id": "bug",
      "domain_label": "Bug 域",
      "domain_description": "问题录入、定位、运行时诊断、修复建议",
      "domain_order": 3,
      "item_order": 10,
      "auto_trigger": "当 Bug 修复可能影响公共方法、共享模块、已有接口、数据库行为、缓存行为、兼容性或其他历史能力时触发。负责识别回归风险点、风险等级、验证优先级并统一记录到 Bug 根目录；不要把它代替实际回归测试。",
      "core_responsibility": "识别回归风险。",
      "skill_path": "bug-regression-risk-rules/SKILL.md",
      "directory_path": "bug-regression-risk-rules",
      "directory": "bug-regression-risk-rules",
      "sections": [
        "Skill 作用与适用场景",
        "自动触发信号",
        "进入后先做什么",
        "默认执行流程",
        "权责边界与不负责事项",
        "需要暂停并确认的条件",
        "执行通过 / 驳回标准",
        "执行结果归档要求",
        "references 读取规则"
      ],
      "references": [
        "bug-regression-risk-rules/references/risk-dimensions.md",
        "bug-regression-risk-rules/references/risk-examples.md",
        "bug-regression-risk-rules/references/risk-ranking-and-scope.md"
      ],
      "agents": [
        "bug-regression-risk-rules/agents/openai.yaml"
      ],
      "has_license": false,
      "focus_points": [
        "优先检查 description 是否具体到触发信号，而不是只写抽象用途。",
        "检查 references 是否足以承接复杂场景，避免 SKILL.md 过厚或过空。",
        "重点看静态定位与运行时诊断的切换条件是否清楚。"
      ]
    },
    {
      "id": "bug-validation-rules",
      "name": "bug-validation-rules",
      "title": "Bug 修复验证规则",
      "status": "implemented",
      "status_label": "已实现",
      "domain_id": "bug",
      "domain_label": "Bug 域",
      "domain_description": "问题录入、定位、运行时诊断、修复建议",
      "domain_order": 3,
      "item_order": 11,
      "auto_trigger": "当 Bug 修复后需要验证是否真的修好、是否引入副作用、是否需要补测试样例、是否已经满足关闭条件时触发。负责修复后验证闭环、Bug 根目录结论记录和未覆盖说明；不要把它代替功能实现验证或全量回归策略。",
      "core_responsibility": "负责修复后的验证闭环。",
      "skill_path": "bug-validation-rules/SKILL.md",
      "directory_path": "bug-validation-rules",
      "directory": "bug-validation-rules",
      "sections": [
        "Skill 作用与适用场景",
        "自动触发信号",
        "进入后先做什么",
        "默认执行流程",
        "权责边界与不负责事项",
        "需要暂停并确认的条件",
        "执行通过 / 驳回标准",
        "执行结果归档要求",
        "references 读取规则"
      ],
      "references": [
        "bug-validation-rules/references/validation-boundaries.md",
        "bug-validation-rules/references/validation-checklist.md",
        "bug-validation-rules/references/validation-template.md"
      ],
      "agents": [
        "bug-validation-rules/agents/openai.yaml"
      ],
      "has_license": false,
      "focus_points": [
        "优先检查 description 是否具体到触发信号，而不是只写抽象用途。",
        "检查 references 是否足以承接复杂场景，避免 SKILL.md 过厚或过空。",
        "重点看静态定位与运行时诊断的切换条件是否清楚。"
      ]
    },
    {
      "id": "bug-scoping-rules",
      "name": "bug-scoping-rules",
      "title": "bug-scoping-rules",
      "status": "planned",
      "status_label": "规划中",
      "domain_id": "bug",
      "domain_label": "Bug 域",
      "domain_description": "问题录入、定位、运行时诊断、修复建议",
      "domain_order": 3,
      "item_order": 4,
      "auto_trigger": "当需要判断问题属于哪个模块、哪个业务链路、哪个服务、哪个页面、哪个接口、哪个数据流时自动触发。",
      "core_responsibility": "明确问题归属和影响范围。",
      "skill_path": "",
      "directory_path": "",
      "directory": "",
      "sections": [],
      "references": [],
      "agents": [],
      "has_license": false,
      "focus_points": [
        "先补齐触发 description、邻接边界和最小 references，再决定是否正式建目录。",
        "优先确认它与同域相邻 skill 的拆分边界，避免新建后职责重叠。",
        "重点看静态定位与运行时诊断的切换条件是否清楚。"
      ]
    },
    {
      "id": "code-minimal-change-rules",
      "name": "code-minimal-change-rules",
      "title": "最小改动编码规则",
      "status": "implemented",
      "status_label": "已实现",
      "domain_id": "baseline",
      "domain_label": "编码基线域",
      "domain_description": "开始编码即并行生效的基础质量规则",
      "domain_order": 4,
      "item_order": 1,
      "auto_trigger": "当新增或修改代码、调整功能、修复 Bug、补测试支撑代码或整理实现细节时触发。负责约束改动范围、删除无关修改并保持变更聚焦；不要用它代替可读性、风格一致性、代码归位或测试规范等相邻 skill。",
      "core_responsibility": "严控代码变更范围，杜绝无关修改、冗余改动和过度优化，保证每次变更聚焦单一目标，降低回归风险和排查难度。",
      "skill_path": "code-minimal-change-rules/SKILL.md",
      "directory_path": "code-minimal-change-rules",
      "directory": "code-minimal-change-rules",
      "sections": [
        "Skill 作用与适用场景",
        "自动触发信号",
        "进入后先做什么",
        "默认执行流程",
        "权责边界与不负责事项",
        "需要暂停并确认的条件",
        "执行通过 / 驳回标准",
        "执行结果归档要求",
        "references 读取规则"
      ],
      "references": [
        "code-minimal-change-rules/references/minimal-change-boundaries.md",
        "code-minimal-change-rules/references/minimal-change-examples.md",
        "code-minimal-change-rules/references/minimal-change-general.md"
      ],
      "agents": [
        "code-minimal-change-rules/agents/openai.yaml"
      ],
      "has_license": false,
      "focus_points": [
        "优先检查 description 是否具体到触发信号，而不是只写抽象用途。",
        "检查 references 是否足以承接复杂场景，避免 SKILL.md 过厚或过空。",
        "重点看它是否能并行生效，并且不抢位点域或审查域职责。"
      ]
    },
    {
      "id": "code-readability-rules",
      "name": "code-readability-rules",
      "title": "代码可读性规则",
      "status": "implemented",
      "status_label": "已实现",
      "domain_id": "baseline",
      "domain_label": "编码基线域",
      "domain_description": "开始编码即并行生效的基础质量规则",
      "domain_order": 4,
      "item_order": 2,
      "auto_trigger": "当新增或修改业务代码、工具代码、服务代码、脚本代码或 Bug 修复逻辑时触发。负责约束函数结构、逻辑顺序、复杂度和可维护性；不要用它代替最小改动、风格一致性、注释规则或代码归位规则。",
      "core_responsibility": "保证函数结构清晰、逻辑顺序自然、复杂度可控。",
      "skill_path": "code-readability-rules/SKILL.md",
      "directory_path": "code-readability-rules",
      "directory": "code-readability-rules",
      "sections": [
        "Skill 作用与适用场景",
        "自动触发信号",
        "进入后先做什么",
        "默认执行流程",
        "权责边界与不负责事项",
        "需要暂停并确认的条件",
        "执行通过 / 驳回标准",
        "执行结果归档要求",
        "references 读取规则"
      ],
      "references": [
        "code-readability-rules/references/function-structure-rules.md",
        "code-readability-rules/references/readability-examples.md",
        "code-readability-rules/references/readability-general.md"
      ],
      "agents": [
        "code-readability-rules/agents/openai.yaml"
      ],
      "has_license": false,
      "focus_points": [
        "优先检查 description 是否具体到触发信号，而不是只写抽象用途。",
        "检查 references 是否足以承接复杂场景，避免 SKILL.md 过厚或过空。",
        "重点看它是否能并行生效，并且不抢位点域或审查域职责。"
      ]
    },
    {
      "id": "code-style-consistency-rules",
      "name": "code-style-consistency-rules",
      "title": "代码风格一致性规则",
      "status": "implemented",
      "status_label": "已实现",
      "domain_id": "baseline",
      "domain_label": "编码基线域",
      "domain_description": "开始编码即并行生效的基础质量规则",
      "domain_order": 4,
      "item_order": 3,
      "auto_trigger": "当新增或修改任意代码文件、脚本文件、配置型代码或测试代码时触发。负责跟随项目现有写法，避免局部风格跳变和个人偏好入侵；不要用它代替最小改动、可读性、注释规范或代码归位规则。",
      "core_responsibility": "跟随项目现有风格，不引入风格跳变。",
      "skill_path": "code-style-consistency-rules/SKILL.md",
      "directory_path": "code-style-consistency-rules",
      "directory": "code-style-consistency-rules",
      "sections": [
        "Skill 作用与适用场景",
        "自动触发信号",
        "进入后先做什么",
        "默认执行流程",
        "权责边界与不负责事项",
        "需要暂停并确认的条件",
        "执行通过 / 驳回标准",
        "执行结果归档要求",
        "references 读取规则"
      ],
      "references": [
        "code-style-consistency-rules/references/consistency-examples.md",
        "code-style-consistency-rules/references/local-convention-detection.md",
        "code-style-consistency-rules/references/style-baseline.md"
      ],
      "agents": [
        "code-style-consistency-rules/agents/openai.yaml"
      ],
      "has_license": false,
      "focus_points": [
        "优先检查 description 是否具体到触发信号，而不是只写抽象用途。",
        "检查 references 是否足以承接复杂场景，避免 SKILL.md 过厚或过空。",
        "重点看它是否能并行生效，并且不抢位点域或审查域职责。"
      ]
    },
    {
      "id": "naming-rules",
      "name": "naming-rules",
      "title": "命名规则",
      "status": "implemented",
      "status_label": "已实现",
      "domain_id": "baseline",
      "domain_label": "编码基线域",
      "domain_description": "开始编码即并行生效的基础质量规则",
      "domain_order": 4,
      "item_order": 4,
      "auto_trigger": "当新增或修改变量、函数、类、模块、接口、字段、事件、任务名、测试名或配置项命名时触发。负责统一业务术语、语义粒度、缩写边界、默认驼峰命名风格和命名一致性；不要把它代替代码可读性或风格格式规则。",
      "core_responsibility": "保证命名语义化。",
      "skill_path": "naming-rules/SKILL.md",
      "directory_path": "naming-rules",
      "directory": "naming-rules",
      "sections": [
        "Skill 作用与适用场景",
        "自动触发信号",
        "进入后先做什么",
        "默认执行流程",
        "权责边界与不负责事项",
        "需要暂停并确认的条件",
        "执行通过 / 驳回标准",
        "执行结果归档要求",
        "references 读取规则"
      ],
      "references": [
        "naming-rules/references/domain-term-alignment.md",
        "naming-rules/references/naming-examples.md",
        "naming-rules/references/naming-principles.md"
      ],
      "agents": [
        "naming-rules/agents/openai.yaml"
      ],
      "has_license": false,
      "focus_points": [
        "优先检查 description 是否具体到触发信号，而不是只写抽象用途。",
        "检查 references 是否足以承接复杂场景，避免 SKILL.md 过厚或过空。",
        "重点看它是否能并行生效，并且不抢位点域或审查域职责。"
      ]
    },
    {
      "id": "chinese-comment-rules",
      "name": "chinese-comment-rules",
      "title": "中文注释规则",
      "status": "implemented",
      "status_label": "已实现",
      "domain_id": "baseline",
      "domain_label": "编码基线域",
      "domain_description": "开始编码即并行生效的基础质量规则",
      "domain_order": 4,
      "item_order": 5,
      "auto_trigger": "当新增或修改代码注释、步骤说明、复杂逻辑解释、临时诊断说明或测试说明，且团队要求默认使用中文表述时触发。负责中文注释的语言选择、表达方式和禁忌；不要把它代替注释位置与颗粒度规则。",
      "core_responsibility": "统一中文表达习惯和注释语气。",
      "skill_path": "chinese-comment-rules/SKILL.md",
      "directory_path": "chinese-comment-rules",
      "directory": "chinese-comment-rules",
      "sections": [
        "Skill 作用与适用场景",
        "自动触发信号",
        "进入后先做什么",
        "默认执行流程",
        "权责边界与不负责事项",
        "需要暂停并确认的条件",
        "执行通过 / 驳回标准",
        "执行结果归档要求",
        "references 读取规则"
      ],
      "references": [
        "chinese-comment-rules/references/chinese-comment-patterns.md",
        "chinese-comment-rules/references/comment-examples.md",
        "chinese-comment-rules/references/comment-language-boundary.md"
      ],
      "agents": [
        "chinese-comment-rules/agents/openai.yaml"
      ],
      "has_license": false,
      "focus_points": [
        "优先检查 description 是否具体到触发信号，而不是只写抽象用途。",
        "检查 references 是否足以承接复杂场景，避免 SKILL.md 过厚或过空。",
        "重点看它是否能并行生效，并且不抢位点域或审查域职责。"
      ]
    },
    {
      "id": "code-comment-rules",
      "name": "code-comment-rules",
      "title": "代码注释规则",
      "status": "implemented",
      "status_label": "已实现",
      "domain_id": "baseline",
      "domain_label": "编码基线域",
      "domain_description": "开始编码即并行生效的基础质量规则",
      "domain_order": 4,
      "item_order": 6,
      "auto_trigger": "当需要判断代码是否应该加注释、注释放在哪里、写到什么颗粒度、如何与实现同步维护时触发。负责注释必要性、位置选择、颗粒度控制、步骤注释、字段注释、函数方法修改时间标注和过期注释治理；每个函数方法的修改都必须补充最近修改时间（北京时间：yyyy-MM-DD HH:mm:ss）；不要把它代替中文语言表达规则。",
      "core_responsibility": "统一注释层级和颗粒度。",
      "skill_path": "code-comment-rules/SKILL.md",
      "directory_path": "code-comment-rules",
      "directory": "code-comment-rules",
      "sections": [
        "Skill 作用与适用场景",
        "自动触发信号",
        "进入后先做什么",
        "默认执行流程",
        "权责边界与不负责事项",
        "需要暂停并确认的条件",
        "执行通过 / 驳回标准",
        "执行结果归档要求",
        "references 读取规则"
      ],
      "references": [
        "code-comment-rules/references/comment-examples.md",
        "code-comment-rules/references/comment-granularity.md",
        "code-comment-rules/references/comment-placement.md"
      ],
      "agents": [
        "code-comment-rules/agents/openai.yaml"
      ],
      "has_license": false,
      "focus_points": [
        "优先检查 description 是否具体到触发信号，而不是只写抽象用途。",
        "检查 references 是否足以承接复杂场景，避免 SKILL.md 过厚或过空。",
        "重点看它是否能并行生效，并且不抢位点域或审查域职责。"
      ]
    },
    {
      "id": "package-structure-rules",
      "name": "package-structure-rules",
      "title": "包结构与分层规则",
      "status": "implemented",
      "status_label": "已实现",
      "domain_id": "location",
      "domain_label": "代码位点域",
      "domain_description": "按改动位置叠加触发的实现规则",
      "domain_order": 5,
      "item_order": 2,
      "auto_trigger": "用于判断新增或修改包、目录、模块、`main.go` 启动入口、`internal` 私有代码、`utils` / `common` / `global` / `middleware` / `crontask` / `async` 等支撑目录，以及 `router` / `controller` / `service` / `repository` / `model` 等业务目录的落点、职责和依赖方向。适用于 Go、Java、Node/Python 项目的结构决策，尤其适合判断单二进制 Go 服务中哪些代码必须留在 `internal/`，以及哪些入口层目录必须保持根级；不要用它代替工具实现、接口设计或代码审查类 skill。",
      "core_responsibility": "统一代码包定义、目录分层、包名职责、模块边界和依赖方向，尤其约束 Go 等语言中的 `routes`、`services`、`utils`、`models`、`repositories`、`middleware`、`constants`、`config`、`controller` 等包结构，避免目录失控和职责混乱。",
      "skill_path": "package-structure-rules/SKILL.md",
      "directory_path": "package-structure-rules",
      "directory": "package-structure-rules",
      "sections": [
        "Skill 作用与适用场景",
        "自动触发信号",
        "进入后先做什么",
        "默认执行流程",
        "权责边界与不负责事项",
        "需要暂停并确认的条件",
        "执行通过 / 驳回标准",
        "执行结果归档要求",
        "references 读取规则"
      ],
      "references": [
        "package-structure-rules/references/go-package-layout.md",
        "package-structure-rules/references/java-layer-layout.md",
        "package-structure-rules/references/node-python-module-layout.md",
        "package-structure-rules/references/structure-general.md"
      ],
      "agents": [
        "package-structure-rules/agents/openai.yaml"
      ],
      "has_license": false,
      "focus_points": [
        "优先检查 description 是否具体到触发信号，而不是只写抽象用途。",
        "检查 references 是否足以承接复杂场景，避免 SKILL.md 过厚或过空。",
        "重点看主位点与横切位点是否可并行叠加，而不是互相覆盖。"
      ]
    },
    {
      "id": "common-util-rules",
      "name": "common-util-rules",
      "title": "公共工具规则",
      "status": "implemented",
      "status_label": "已实现",
      "domain_id": "location",
      "domain_label": "代码位点域",
      "domain_description": "按改动位置叠加触发的实现规则",
      "domain_order": 5,
      "item_order": 3,
      "auto_trigger": "当新增或修改工具类、通用方法、公共组件、工具函数、通用常量或复用代码时触发。负责统一公共工具代码的判定标准、存放位置、调用方式和边界；不要用它代替业务逻辑抽象、包结构规则或具体实现细则。",
      "core_responsibility": "统一通用工具代码的编写规范、复用标准、存放位置和调用方式，避免重复造轮子，保证公共代码的通用性、稳定性和可维护性。",
      "skill_path": "common-util-rules/SKILL.md",
      "directory_path": "common-util-rules",
      "directory": "common-util-rules",
      "sections": [
        "Skill 作用与适用场景",
        "自动触发信号",
        "进入后先做什么",
        "默认执行流程",
        "权责边界与不负责事项",
        "需要暂停并确认的条件",
        "执行通过 / 驳回标准",
        "执行结果归档要求",
        "references 读取规则"
      ],
      "references": [
        "common-util-rules/references/util-examples.md",
        "common-util-rules/references/util-placement.md",
        "common-util-rules/references/util-qualification.md"
      ],
      "agents": [
        "common-util-rules/agents/openai.yaml"
      ],
      "has_license": false,
      "focus_points": [
        "优先检查 description 是否具体到触发信号，而不是只写抽象用途。",
        "检查 references 是否足以承接复杂场景，避免 SKILL.md 过厚或过空。",
        "重点看主位点与横切位点是否可并行叠加，而不是互相覆盖。"
      ]
    },
    {
      "id": "database-schema-rules",
      "name": "database-schema-rules",
      "title": "数据库结构规则",
      "status": "implemented",
      "status_label": "已实现",
      "domain_id": "location",
      "domain_label": "代码位点域",
      "domain_description": "按改动位置叠加触发的实现规则",
      "domain_order": 5,
      "item_order": 4,
      "auto_trigger": "当新增或修改表、字段、索引、唯一约束、外键、迁移脚本、DDL、实体结构、schema 定义时自动触发。负责统一数据库结构变更、迁移安全、兼容性和回滚边界；数据库的字段必须要定义数据类型、默认值、是否需要索引、字段 CHARSET=utf8mb4、ENGINE=InnoDB、注释说明等写清楚，不要遗漏；所有金额相关的要强制使用字符串，避免任何出现精度问题的情况；所有表必须包含 created_at 和 updated_at 字段，由数据库自动管理；必须冗余一个毫秒级时间戳的创建时间，避免数据库的时区问题影响不同的时间格式；所有表必须包含逻辑删除字段，1 的状态标识删除，不是 1 代表正常非删除状态，默认 0=非删除；否则会导致自动创建表出现不可控的因素；避免把查询实现、事务控制和业务逻辑混进结构变更；不要用它代替 database-query-rules、config-change-rules 或发布回滚规则。",
      "core_responsibility": "统一表结构变更、迁移安全和回滚策略。",
      "skill_path": "database-schema-rules/SKILL.md",
      "directory_path": "database-schema-rules",
      "directory": "database-schema-rules",
      "sections": [
        "Skill 作用与适用场景",
        "自动触发信号",
        "进入后先做什么",
        "默认执行流程",
        "权责边界与不负责事项",
        "需要暂停并确认的条件",
        "执行通过 / 驳回标准",
        "执行结果归档要求",
        "references 读取规则"
      ],
      "references": [
        "database-schema-rules/references/migration-safety-and-rollback.md",
        "database-schema-rules/references/schema-boundaries.md",
        "database-schema-rules/references/schema-examples.md"
      ],
      "agents": [
        "database-schema-rules/agents/openai.yaml"
      ],
      "has_license": false,
      "focus_points": [
        "优先检查 description 是否具体到触发信号，而不是只写抽象用途。",
        "检查 references 是否足以承接复杂场景，避免 SKILL.md 过厚或过空。",
        "重点看主位点与横切位点是否可并行叠加，而不是互相覆盖。"
      ]
    },
    {
      "id": "database-query-rules",
      "name": "database-query-rules",
      "title": "数据库访问规则",
      "status": "implemented",
      "status_label": "已实现",
      "domain_id": "location",
      "domain_label": "代码位点域",
      "domain_description": "按改动位置叠加触发的实现规则",
      "domain_order": 5,
      "item_order": 5,
      "auto_trigger": "当新增或修改 SQL、Repository、DAO、Mapper、QueryBuilder、事务、锁、批量 CRUD、分页查询时自动触发。负责统一数据库访问实现、查询性能、事务与锁边界，避免把 schema 设计、缓存策略和业务逻辑混进数据访问层；不要用它代替 database-schema-rules、performance-caching-rules 或业务规则本身。",
      "core_responsibility": "统一数据库访问和查询性能规则。",
      "skill_path": "database-query-rules/SKILL.md",
      "directory_path": "database-query-rules",
      "directory": "database-query-rules",
      "sections": [
        "Skill 作用与适用场景",
        "自动触发信号",
        "进入后先做什么",
        "默认执行流程",
        "权责边界与不负责事项",
        "需要暂停并确认的条件",
        "执行通过 / 驳回标准",
        "执行结果归档要求",
        "references 读取规则"
      ],
      "references": [
        "database-query-rules/references/access-layer-boundaries.md",
        "database-query-rules/references/query-performance-examples.md",
        "database-query-rules/references/transactions-locks-and-batch.md"
      ],
      "agents": [
        "database-query-rules/agents/openai.yaml"
      ],
      "has_license": false,
      "focus_points": [
        "优先检查 description 是否具体到触发信号，而不是只写抽象用途。",
        "检查 references 是否足以承接复杂场景，避免 SKILL.md 过厚或过空。",
        "重点看主位点与横切位点是否可并行叠加，而不是互相覆盖。"
      ]
    },
    {
      "id": "api-endpoint-rules",
      "name": "api-endpoint-rules",
      "title": "接口入口规则",
      "status": "implemented",
      "status_label": "已实现",
      "domain_id": "location",
      "domain_label": "代码位点域",
      "domain_description": "按改动位置叠加触发的实现规则",
      "domain_order": 5,
      "item_order": 6,
      "auto_trigger": "当新增或修改 controller、router、路由声明、HTTP 方法、接口路径命名、接口入口职责或超时入口边界时触发。负责统一接口入口设计、路径命名和强制使用 POST 方法；必须以 package-structure-rules 为基准，不使用 handler 包名；不要用它代替请求参数、响应结构或错误处理规则。",
      "core_responsibility": "统一接口入口设计。",
      "skill_path": "api-endpoint-rules/SKILL.md",
      "directory_path": "api-endpoint-rules",
      "directory": "api-endpoint-rules",
      "sections": [
        "Skill 作用与适用场景",
        "自动触发信号",
        "进入后先做什么",
        "默认执行流程",
        "权责边界与不负责事项",
        "需要暂停并确认的条件",
        "执行通过 / 驳回标准",
        "执行结果归档要求",
        "references 读取规则"
      ],
      "references": [
        "api-endpoint-rules/references/endpoint-examples.md",
        "api-endpoint-rules/references/endpoint-responsibility.md",
        "api-endpoint-rules/references/path-and-method-semantics.md"
      ],
      "agents": [
        "api-endpoint-rules/agents/openai.yaml"
      ],
      "has_license": false,
      "focus_points": [
        "优先检查 description 是否具体到触发信号，而不是只写抽象用途。",
        "检查 references 是否足以承接复杂场景，避免 SKILL.md 过厚或过空。",
        "重点看主位点与横切位点是否可并行叠加，而不是互相覆盖。"
      ]
    },
    {
      "id": "api-request-rules",
      "name": "api-request-rules",
      "title": "接口请求规则",
      "status": "implemented",
      "status_label": "已实现",
      "domain_id": "location",
      "domain_label": "代码位点域",
      "domain_description": "按改动位置叠加触发的实现规则",
      "domain_order": 5,
      "item_order": 7,
      "auto_trigger": "当新增或修改请求参数、DTO、body 结构、参数校验或请求模型时触发。负责统一请求结构、参数表达和基础校验边界；必须以 api-endpoint-rules 为基准，只使用 POST 请求，所有参数通过 JSON body 传递；不要用它代替接口入口设计、响应结构或业务规则本身。",
      "core_responsibility": "统一请求模型和校验规则。",
      "skill_path": "api-request-rules/SKILL.md",
      "directory_path": "api-request-rules",
      "directory": "api-request-rules",
      "sections": [
        "Skill 作用与适用场景",
        "自动触发信号",
        "进入后先做什么",
        "默认执行流程",
        "权责边界与不负责事项",
        "需要暂停并确认的条件",
        "执行通过 / 驳回标准",
        "执行结果归档要求",
        "references 读取规则"
      ],
      "references": [
        "api-request-rules/references/parameter-validation-rules.md",
        "api-request-rules/references/request-examples.md",
        "api-request-rules/references/request-shape-boundaries.md"
      ],
      "agents": [
        "api-request-rules/agents/openai.yaml"
      ],
      "has_license": false,
      "focus_points": [
        "优先检查 description 是否具体到触发信号，而不是只写抽象用途。",
        "检查 references 是否足以承接复杂场景，避免 SKILL.md 过厚或过空。",
        "重点看主位点与横切位点是否可并行叠加，而不是互相覆盖。"
      ]
    },
    {
      "id": "api-response-rules",
      "name": "api-response-rules",
      "title": "接口响应规则",
      "status": "implemented",
      "status_label": "已实现",
      "domain_id": "location",
      "domain_label": "代码位点域",
      "domain_description": "按改动位置叠加触发的实现规则",
      "domain_order": 5,
      "item_order": 8,
      "auto_trigger": "当新增或修改返回体、响应包装器、分页结构、错误响应结构、兼容字段、版本字段或统一响应模型时触发。负责统一响应格式和兼容策略；成功响应和错误响应都必须包含状态码、状态、消息、数据四个字段；不要用它代替错误处理流程、异常分类或接口入口职责规则。",
      "core_responsibility": "统一响应格式和兼容策略。",
      "skill_path": "api-response-rules/SKILL.md",
      "directory_path": "api-response-rules",
      "directory": "api-response-rules",
      "sections": [
        "Skill 作用与适用场景",
        "自动触发信号",
        "进入后先做什么",
        "默认执行流程",
        "权责边界与不负责事项",
        "需要暂停并确认的条件",
        "执行通过 / 驳回标准",
        "执行结果归档要求",
        "references 读取规则"
      ],
      "references": [
        "api-response-rules/references/response-examples.md",
        "api-response-rules/references/response-shape-baseline.md",
        "api-response-rules/references/response-variants.md"
      ],
      "agents": [
        "api-response-rules/agents/openai.yaml"
      ],
      "has_license": false,
      "focus_points": [
        "优先检查 description 是否具体到触发信号，而不是只写抽象用途。",
        "检查 references 是否足以承接复杂场景，避免 SKILL.md 过厚或过空。",
        "重点看主位点与横切位点是否可并行叠加，而不是互相覆盖。"
      ]
    },
    {
      "id": "error-handling-rules",
      "name": "error-handling-rules",
      "title": "错误处理规则",
      "status": "implemented",
      "status_label": "已实现",
      "domain_id": "location",
      "domain_label": "代码位点域",
      "domain_description": "按改动位置叠加触发的实现规则",
      "domain_order": 5,
      "item_order": 10,
      "auto_trigger": "当新增或修改异常类、全局异常处理、错误中间件、try/catch、错误映射、重试、超时、降级或 fallback 时触发。负责统一错误处理模型和处理路径；不要用它代替错误响应结构、日志链路或接口入口设计规则。",
      "core_responsibility": "统一错误处理模型。",
      "skill_path": "error-handling-rules/SKILL.md",
      "directory_path": "error-handling-rules",
      "directory": "error-handling-rules",
      "sections": [
        "Skill 作用与适用场景",
        "自动触发信号",
        "进入后先做什么",
        "默认执行流程",
        "权责边界与不负责事项",
        "需要暂停并确认的条件",
        "执行通过 / 驳回标准",
        "执行结果归档要求",
        "references 读取规则"
      ],
      "references": [
        "error-handling-rules/references/error-classification.md",
        "error-handling-rules/references/handling-paths.md",
        "error-handling-rules/references/resilience-boundaries.md"
      ],
      "agents": [
        "error-handling-rules/agents/openai.yaml"
      ],
      "has_license": false,
      "focus_points": [
        "优先检查 description 是否具体到触发信号，而不是只写抽象用途。",
        "检查 references 是否足以承接复杂场景，避免 SKILL.md 过厚或过空。",
        "重点看主位点与横切位点是否可并行叠加，而不是互相覆盖。"
      ]
    },
    {
      "id": "logging-trace-rules",
      "name": "logging-trace-rules",
      "title": "日志与追踪规则",
      "status": "implemented",
      "status_label": "已实现",
      "domain_id": "location",
      "domain_label": "代码位点域",
      "domain_description": "按改动位置叠加触发的实现规则",
      "domain_order": 5,
      "item_order": 11,
      "auto_trigger": "当新增或修改日志、logger、trace、span、审计日志、脱敏字段、排障字段或链路透传逻辑时触发。负责统一日志与链路追踪规则；不要用它代替错误处理、响应结构或长期监控告警策略。",
      "core_responsibility": "统一日志和链路追踪规则。",
      "skill_path": "logging-trace-rules/SKILL.md",
      "directory_path": "logging-trace-rules",
      "directory": "logging-trace-rules",
      "sections": [
        "Skill 作用与适用场景",
        "自动触发信号",
        "进入后先做什么",
        "默认执行流程",
        "权责边界与不负责事项",
        "需要暂停并确认的条件",
        "执行通过 / 驳回标准",
        "执行结果归档要求",
        "references 读取规则"
      ],
      "references": [
        "logging-trace-rules/references/log-types-and-fields.md",
        "logging-trace-rules/references/logging-examples.md",
        "logging-trace-rules/references/trace-propagation.md"
      ],
      "agents": [
        "logging-trace-rules/agents/openai.yaml"
      ],
      "has_license": false,
      "focus_points": [
        "优先检查 description 是否具体到触发信号，而不是只写抽象用途。",
        "检查 references 是否足以承接复杂场景，避免 SKILL.md 过厚或过空。",
        "重点看主位点与横切位点是否可并行叠加，而不是互相覆盖。"
      ]
    },
    {
      "id": "frontend-component-rules",
      "name": "frontend-component-rules",
      "title": "前端组件工程规则",
      "status": "implemented",
      "status_label": "已实现",
      "domain_id": "location",
      "domain_label": "代码位点域",
      "domain_description": "按改动位置叠加触发的实现规则",
      "domain_order": 5,
      "item_order": 13,
      "auto_trigger": "当新增或修改 React、Vue、前端组件拆分、组件目录归属、props 设计、emits 设计、slots 设计、状态归属、事件上抛、组合方式、hooks、composables、复用边界、受控/非受控切换、渲染副作用或客户端展示逻辑时自动触发。负责组件边界、状态边界、接口契约、组合复用和渲染可维护性；不要用它代替页面视觉、配色、排版、响应式和 UI 风格规则。",
      "core_responsibility": "统一前端组件工程、状态边界和页面内组合规则。",
      "skill_path": "frontend-component-rules/SKILL.md",
      "directory_path": "frontend-component-rules",
      "directory": "frontend-component-rules",
      "sections": [
        "Skill 作用与适用场景",
        "自动触发信号",
        "进入后先做什么",
        "默认执行流程",
        "权责边界与不负责事项",
        "需要暂停并确认的条件",
        "执行通过 / 驳回标准",
        "执行结果归档要求",
        "references 读取规则"
      ],
      "references": [
        "frontend-component-rules/references/component-boundary-rules.md",
        "frontend-component-rules/references/component-review-checklist.md",
        "frontend-component-rules/references/composition-reuse-rules.md",
        "frontend-component-rules/references/props-events-contract-rules.md",
        "frontend-component-rules/references/render-side-effect-rules.md",
        "frontend-component-rules/references/state-ownership-rules.md"
      ],
      "agents": [
        "frontend-component-rules/agents/openai.yaml"
      ],
      "has_license": false,
      "focus_points": [
        "优先检查 description 是否具体到触发信号，而不是只写抽象用途。",
        "检查 references 是否足以承接复杂场景，避免 SKILL.md 过厚或过空。",
        "重点看主位点与横切位点是否可并行叠加，而不是互相覆盖。"
      ]
    },
    {
      "id": "frontend-ui-visual-rules",
      "name": "frontend-ui-visual-rules",
      "title": "前端 UI 视觉规则",
      "status": "implemented",
      "status_label": "已实现",
      "domain_id": "location",
      "domain_label": "代码位点域",
      "domain_description": "按改动位置叠加触发的实现规则",
      "domain_order": 5,
      "item_order": 14,
      "auto_trigger": "当新增或修改前端页面、页面布局、主题样式、配色、字体、图标、卡片、弹窗、表单、表格、图表、导航、空状态、动画、响应式样式、暗黑模式、设计 token、Tailwind 类名、CSS/SCSS/LESS、`.tsx`/`.jsx`/`.vue`/`.html` 中影响界面视觉和交互体验的代码时自动触发。负责页面视觉方向、信息层级、交互反馈、可访问性、响应式适配和交付前 UI 自审；内置合并后的 UI/UX 设计种子数据与搜索脚本，可在风格不明时辅助定方向；不要用它代替纯组件工程拆分、状态管理、接口接线或后端规则。",
      "core_responsibility": "统一页面视觉方向、信息层级、交互反馈、响应式适配、可访问性和交付前 UI 自审。",
      "skill_path": "frontend-ui-visual-rules/SKILL.md",
      "directory_path": "frontend-ui-visual-rules",
      "directory": "frontend-ui-visual-rules",
      "sections": [
        "Skill 作用与适用场景",
        "自动触发信号",
        "进入后先做什么",
        "默认执行流程",
        "权责边界与不负责事项",
        "需要暂停并确认的条件",
        "执行通过 / 驳回标准",
        "执行结果归档要求",
        "references 读取规则"
      ],
      "references": [
        "frontend-ui-visual-rules/references/color-typography-icon-rules.md",
        "frontend-ui-visual-rules/references/design-search-workflow.md",
        "frontend-ui-visual-rules/references/forms-nav-data-display-rules.md",
        "frontend-ui-visual-rules/references/interaction-accessibility-rules.md",
        "frontend-ui-visual-rules/references/layout-responsive-rules.md",
        "frontend-ui-visual-rules/references/page-style-and-scenario.md",
        "frontend-ui-visual-rules/references/seed-source-notes.md",
        "frontend-ui-visual-rules/references/ui-delivery-checklist.md",
        "frontend-ui-visual-rules/references/ui-priority-model.md"
      ],
      "agents": [
        "frontend-ui-visual-rules/agents/openai.yaml"
      ],
      "has_license": false,
      "focus_points": [
        "优先检查 description 是否具体到触发信号，而不是只写抽象用途。",
        "检查 references 是否足以承接复杂场景，避免 SKILL.md 过厚或过空。",
        "重点看主位点与横切位点是否可并行叠加，而不是互相覆盖。"
      ]
    },
    {
      "id": "config-change-rules",
      "name": "config-change-rules",
      "title": "config-change-rules",
      "status": "planned",
      "status_label": "规划中",
      "domain_id": "location",
      "domain_label": "代码位点域",
      "domain_description": "按改动位置叠加触发的实现规则",
      "domain_order": 5,
      "item_order": 1,
      "auto_trigger": "当新增或修改 `.env`、`.env.example`、`application.yml`、`application.yaml`、`settings.py`、`config.ts`、`appsettings.json`、`values.yaml`、环境变量读取、默认值、配置注入、配置分层、特性开关、密钥占位时自动触发。",
      "core_responsibility": "统一配置、密钥和默认值策略。",
      "skill_path": "",
      "directory_path": "",
      "directory": "",
      "sections": [],
      "references": [],
      "agents": [],
      "has_license": false,
      "focus_points": [
        "先补齐触发 description、邻接边界和最小 references，再决定是否正式建目录。",
        "优先确认它与同域相邻 skill 的拆分边界，避免新建后职责重叠。",
        "重点看主位点与横切位点是否可并行叠加，而不是互相覆盖。"
      ]
    },
    {
      "id": "request-header-rules",
      "name": "request-header-rules",
      "title": "request-header-rules",
      "status": "planned",
      "status_label": "规划中",
      "domain_id": "location",
      "domain_label": "代码位点域",
      "domain_description": "按改动位置叠加触发的实现规则",
      "domain_order": 5,
      "item_order": 9,
      "auto_trigger": "当新增或修改认证头、`trace-id`、`span-id`、租户头、幂等键、客户端上下文头、`X-Forwarded-*` 逻辑时自动触发。",
      "core_responsibility": "统一请求头约定和透传规则。",
      "skill_path": "",
      "directory_path": "",
      "directory": "",
      "sections": [],
      "references": [],
      "agents": [],
      "has_license": false,
      "focus_points": [
        "先补齐触发 description、邻接边界和最小 references，再决定是否正式建目录。",
        "优先确认它与同域相邻 skill 的拆分边界，避免新建后职责重叠。",
        "重点看主位点与横切位点是否可并行叠加，而不是互相覆盖。"
      ]
    },
    {
      "id": "auth-security-rules",
      "name": "auth-security-rules",
      "title": "auth-security-rules",
      "status": "planned",
      "status_label": "规划中",
      "domain_id": "location",
      "domain_label": "代码位点域",
      "domain_description": "按改动位置叠加触发的实现规则",
      "domain_order": 5,
      "item_order": 12,
      "auto_trigger": "当新增或修改认证、鉴权、登录、登出、会话、JWT、对象级授权、输入校验、敏感信息处理、上传下载安全、外部请求安全时自动触发。",
      "core_responsibility": "统一安全实现的默认基线。",
      "skill_path": "",
      "directory_path": "",
      "directory": "",
      "sections": [],
      "references": [],
      "agents": [],
      "has_license": false,
      "focus_points": [
        "先补齐触发 description、邻接边界和最小 references，再决定是否正式建目录。",
        "优先确认它与同域相邻 skill 的拆分边界，避免新建后职责重叠。",
        "重点看主位点与横切位点是否可并行叠加，而不是互相覆盖。"
      ]
    },
    {
      "id": "performance-caching-rules",
      "name": "performance-caching-rules",
      "title": "performance-caching-rules",
      "status": "planned",
      "status_label": "规划中",
      "domain_id": "location",
      "domain_label": "代码位点域",
      "domain_description": "按改动位置叠加触发的实现规则",
      "domain_order": 5,
      "item_order": 15,
      "auto_trigger": "当新增或修改 SQL 性能、接口耗时、缓存读取写入、缓存 key、缓存失效、前端渲染热点、大列表、图表、虚拟滚动时自动触发。",
      "core_responsibility": "统一性能和缓存规则。",
      "skill_path": "",
      "directory_path": "",
      "directory": "",
      "sections": [],
      "references": [],
      "agents": [],
      "has_license": false,
      "focus_points": [
        "先补齐触发 description、邻接边界和最小 references，再决定是否正式建目录。",
        "优先确认它与同域相邻 skill 的拆分边界，避免新建后职责重叠。",
        "重点看主位点与横切位点是否可并行叠加，而不是互相覆盖。"
      ]
    },
    {
      "id": "implementation-review-rules",
      "name": "implementation-review-rules",
      "title": "实现自审规则",
      "status": "implemented",
      "status_label": "已实现",
      "domain_id": "review",
      "domain_label": "编码审查域",
      "domain_description": "测试前的静态自审、语法检查、清理归位",
      "domain_order": 6,
      "item_order": 1,
      "auto_trigger": "当功能代码已经完成、准备进入测试前验证时触发。负责检查实现是否符合可读性优先、单一职责、命名语义化、注释完整、错误处理明确、日志可追溯、依赖使用审慎、魔法值治理、冗余逻辑清理和编码规范等实现质量要求；不要用它代替语法检查、格式化执行、目录归位审查或功能验证规则。",
      "core_responsibility": "对刚完成的实现做一次测试前规范自审。",
      "skill_path": "implementation-review-rules/SKILL.md",
      "directory_path": "implementation-review-rules",
      "directory": "implementation-review-rules",
      "sections": [
        "Skill 作用与适用场景",
        "自动触发信号",
        "进入后先做什么",
        "核心自审要求",
        "默认执行流程",
        "权责边界与不负责事项",
        "需要暂停并确认的条件",
        "执行通过 / 驳回标准",
        "执行结果归档要求",
        "references 读取规则"
      ],
      "references": [
        "implementation-review-rules/references/review-boundaries.md",
        "implementation-review-rules/references/review-examples.md",
        "implementation-review-rules/references/review-scope.md"
      ],
      "agents": [
        "implementation-review-rules/agents/openai.yaml"
      ],
      "has_license": false,
      "focus_points": [
        "优先检查 description 是否具体到触发信号，而不是只写抽象用途。",
        "检查 references 是否足以承接复杂场景，避免 SKILL.md 过厚或过空。",
        "重点看它是否只处理静态质量问题，不越界替代测试。"
      ]
    },
    {
      "id": "syntax-check-review-rules",
      "name": "syntax-check-review-rules",
      "title": "语法校验规则",
      "status": "implemented",
      "status_label": "已实现",
      "domain_id": "review",
      "domain_label": "编码审查域",
      "domain_description": "测试前的静态自审、语法检查、清理归位",
      "domain_order": 6,
      "item_order": 2,
      "auto_trigger": "当新增或修改代码后准备进入测试前验证，且需要确认语法、类型、依赖引用、构建基础是否正确时触发。负责检查语法错误、引用缺失、类型问题和明显构建失败风险；不要用它代替实现自审、格式清理或功能测试规则。",
      "core_responsibility": "检查语法错误、引用缺失、类型问题和明显构建失败风险。",
      "skill_path": "syntax-check-review-rules/SKILL.md",
      "directory_path": "syntax-check-review-rules",
      "directory": "syntax-check-review-rules",
      "sections": [
        "Skill 作用与适用场景",
        "自动触发信号",
        "进入后先做什么",
        "默认执行流程",
        "权责边界与不负责事项",
        "需要暂停并确认的条件",
        "执行通过 / 驳回标准",
        "执行结果归档要求",
        "references 读取规则"
      ],
      "references": [
        "syntax-check-review-rules/references/check-examples.md",
        "syntax-check-review-rules/references/check-scope.md",
        "syntax-check-review-rules/references/type-and-reference-risks.md"
      ],
      "agents": [
        "syntax-check-review-rules/agents/openai.yaml"
      ],
      "has_license": false,
      "focus_points": [
        "优先检查 description 是否具体到触发信号，而不是只写抽象用途。",
        "检查 references 是否足以承接复杂场景，避免 SKILL.md 过厚或过空。",
        "重点看它是否只处理静态质量问题，不越界替代测试。"
      ]
    },
    {
      "id": "cleanup-format-review-rules",
      "name": "cleanup-format-review-rules",
      "title": "清理格式审查规则",
      "status": "implemented",
      "status_label": "已实现",
      "domain_id": "review",
      "domain_label": "编码审查域",
      "domain_description": "测试前的静态自审、语法检查、清理归位",
      "domain_order": 6,
      "item_order": 3,
      "auto_trigger": "当新增或修改代码后准备进入测试前验证，且存在未使用导入、未使用变量、未使用方法引用、调试残留、临时代码、死代码、多余换行或格式不一致风险时触发。负责清理代码噪音并统一基础格式；不要用它代替功能性修改或实现重构。",
      "core_responsibility": "清理代码噪音并统一基础格式。",
      "skill_path": "cleanup-format-review-rules/SKILL.md",
      "directory_path": "cleanup-format-review-rules",
      "directory": "cleanup-format-review-rules",
      "sections": [
        "Skill 作用与适用场景",
        "自动触发信号",
        "进入后先做什么",
        "默认执行流程",
        "权责边界与不负责事项",
        "需要暂停并确认的条件",
        "执行通过 / 驳回标准",
        "执行结果归档要求",
        "references 读取规则"
      ],
      "references": [
        "cleanup-format-review-rules/references/cleanup-examples.md",
        "cleanup-format-review-rules/references/cleanup-scope.md",
        "cleanup-format-review-rules/references/debug-artifact-rules.md"
      ],
      "agents": [
        "cleanup-format-review-rules/agents/openai.yaml"
      ],
      "has_license": false,
      "focus_points": [
        "优先检查 description 是否具体到触发信号，而不是只写抽象用途。",
        "检查 references 是否足以承接复杂场景，避免 SKILL.md 过厚或过空。",
        "重点看它是否只处理静态质量问题，不越界替代测试。"
      ]
    },
    {
      "id": "code-placement-review-rules",
      "name": "code-placement-review-rules",
      "title": "代码归位审查规则",
      "status": "implemented",
      "status_label": "已实现",
      "domain_id": "review",
      "domain_label": "编码审查域",
      "domain_description": "测试前的静态自审、语法检查、清理归位",
      "domain_order": 6,
      "item_order": 4,
      "auto_trigger": "当新增文件、移动文件、扩展模块、跨层调用、工具类落点或目录归属可能不合理时，在进入测试前触发。负责检查代码存放位置、模块归属、层级边界和依赖方向是否合理；不要用它代替编码前的包结构决策规则。",
      "core_responsibility": "检查代码存放位置、模块归属、层级边界和依赖方向是否合理。",
      "skill_path": "code-placement-review-rules/SKILL.md",
      "directory_path": "code-placement-review-rules",
      "directory": "code-placement-review-rules",
      "sections": [
        "Skill 作用与适用场景",
        "自动触发信号",
        "进入后先做什么",
        "默认执行流程",
        "权责边界与不负责事项",
        "需要暂停并确认的条件",
        "执行通过 / 驳回标准",
        "执行结果归档要求",
        "references 读取规则"
      ],
      "references": [
        "code-placement-review-rules/references/dependency-direction.md",
        "code-placement-review-rules/references/placement-checklist.md",
        "code-placement-review-rules/references/placement-examples.md"
      ],
      "agents": [
        "code-placement-review-rules/agents/openai.yaml"
      ],
      "has_license": false,
      "focus_points": [
        "优先检查 description 是否具体到触发信号，而不是只写抽象用途。",
        "检查 references 是否足以承接复杂场景，避免 SKILL.md 过厚或过空。",
        "重点看它是否只处理静态质量问题，不越界替代测试。"
      ]
    },
    {
      "id": "test-strategy-rules",
      "name": "test-strategy-rules",
      "title": "测试策略规则",
      "status": "implemented",
      "status_label": "已实现",
      "domain_id": "test",
      "domain_label": "测试域",
      "domain_description": "策略、资源、功能验证、联调、回归",
      "domain_order": 7,
      "item_order": 1,
      "auto_trigger": "当准备进入测试阶段，需要确定测什么、先测什么、测到什么程度、哪些路径必须覆盖、哪些风险只能记录待补测时触发。负责测试优先级、测试类型组合、覆盖范围和资源收口；必须以 `test-location-rules` 为基准，把策略摘要统一记录到 `test/yyyy-MM-DD_HHmmss/测试任务中文简介/README.md`，并在需要拆成多轮独立测试时给出多个时间戳根目录方案；不要用它代替具体测试资源管理或验证执行 skill。",
      "core_responsibility": "决定测试层级和覆盖重点。",
      "skill_path": "test-strategy-rules/SKILL.md",
      "directory_path": "test-strategy-rules",
      "directory": "test-strategy-rules",
      "sections": [
        "Skill 作用与适用场景",
        "自动触发信号",
        "进入后先做什么",
        "默认执行流程",
        "权责边界与不负责事项",
        "需要暂停并确认的条件",
        "执行通过 / 驳回标准",
        "执行结果归档要求",
        "references 读取规则"
      ],
      "references": [
        "test-strategy-rules/references/priority-model.md",
        "test-strategy-rules/references/strategy-dimensions.md",
        "test-strategy-rules/references/strategy-template.md"
      ],
      "agents": [
        "test-strategy-rules/agents/openai.yaml"
      ],
      "has_license": false,
      "focus_points": [
        "优先检查 description 是否具体到触发信号，而不是只写抽象用途。",
        "检查 references 是否足以承接复杂场景，避免 SKILL.md 过厚或过空。",
        "重点看测试策略、资源、功能验证、联调、回归是否已经拆开。"
      ]
    },
    {
      "id": "test-location-rules",
      "name": "test-location-rules",
      "title": "测试目录落点规则",
      "status": "implemented",
      "status_label": "已实现",
      "domain_id": "test",
      "domain_label": "测试域",
      "domain_description": "策略、资源、功能验证、联调、回归",
      "domain_order": 7,
      "item_order": 2,
      "auto_trigger": "当新增或修改测试目录、测试文件、测试脚本、验证程序、fixture、mock 数据、测试说明文档落点时触发。负责统一测试资源根目录、时间戳任务根目录、中文说明目录、真实代码路径镜像目录和禁止散落规则；尤其要避免把中文路径放进会被 Go 工具链编译的测试包目录。不要用它代替 test-naming-rules、test-program-rules、test-doc-rules、code-placement-review-rules 或功能验证规则。",
      "core_responsibility": "统一测试资源位置。",
      "skill_path": "test-location-rules/SKILL.md",
      "directory_path": "test-location-rules",
      "directory": "test-location-rules",
      "sections": [
        "铁律：所有测试资产必须统一在 test/ 目录下",
        "新基线：时间戳根目录 + 中文说明目录 + 真实代码路径镜像",
        "Skill 作用与适用场景",
        "自动触发信号",
        "进入后先做什么",
        "默认执行流程",
        "权责边界与不负责事项",
        "需要暂停并确认的条件",
        "执行通过 / 驳回标准",
        "执行结果归档要求",
        "references 读取规则"
      ],
      "references": [
        "test-location-rules/references/forbidden-scattered-assets.md",
        "test-location-rules/references/location-examples.md",
        "test-location-rules/references/test-root-and-task-folders.md"
      ],
      "agents": [
        "test-location-rules/agents/openai.yaml"
      ],
      "has_license": false,
      "focus_points": [
        "优先检查 description 是否具体到触发信号，而不是只写抽象用途。",
        "检查 references 是否足以承接复杂场景，避免 SKILL.md 过厚或过空。",
        "重点看测试策略、资源、功能验证、联调、回归是否已经拆开。"
      ]
    },
    {
      "id": "test-naming-rules",
      "name": "test-naming-rules",
      "title": "测试命名规则",
      "status": "implemented",
      "status_label": "已实现",
      "domain_id": "test",
      "domain_label": "测试域",
      "domain_description": "策略、资源、功能验证、联调、回归",
      "domain_order": 7,
      "item_order": 3,
      "auto_trigger": "当创建或修改测试时间戳根目录、中文说明目录、测试文件、测试脚本、测试数据目录、fixture 目录、mock 目录时触发。负责统一测试目录与文件命名规范，保证名称可读、可检索、与业务目标一致；必须以 test-location-rules 为基础，遵循 `test/yyyy-MM-DD_HHmmss/` 时间戳根目录、中文说明目录和真实代码路径镜像目录的命名规则；尤其要避免中文进入会被 Go 工具链编译的路径。不要用它代替 test-location-rules、test-program-rules、test-doc-rules 或功能验证规则。",
      "core_responsibility": "统一测试目录和文件命名。",
      "skill_path": "test-naming-rules/SKILL.md",
      "directory_path": "test-naming-rules",
      "directory": "test-naming-rules",
      "sections": [
        "Skill 作用与适用场景",
        "自动触发信号",
        "进入后先做什么",
        "默认执行流程",
        "权责边界与不负责事项",
        "需要暂停并确认的条件",
        "执行通过 / 驳回标准",
        "执行结果归档要求",
        "references 读取规则"
      ],
      "references": [
        "test-naming-rules/references/naming-baseline.md",
        "test-naming-rules/references/naming-boundaries.md",
        "test-naming-rules/references/naming-examples.md"
      ],
      "agents": [
        "test-naming-rules/agents/openai.yaml"
      ],
      "has_license": false,
      "focus_points": [
        "优先检查 description 是否具体到触发信号，而不是只写抽象用途。",
        "检查 references 是否足以承接复杂场景，避免 SKILL.md 过厚或过空。",
        "重点看测试策略、资源、功能验证、联调、回归是否已经拆开。"
      ]
    },
    {
      "id": "test-program-rules",
      "name": "test-program-rules",
      "title": "测试程序规则",
      "status": "implemented",
      "status_label": "已实现",
      "domain_id": "test",
      "domain_label": "测试域",
      "domain_description": "策略、资源、功能验证、联调、回归",
      "domain_order": 7,
      "item_order": 4,
      "auto_trigger": "当新增或修改测试程序、模拟程序、验证脚本、数据构造脚本、测试辅助代码时触发。负责统一测试程序职责拆分、辅助代码边界和长期保留策略；必须以 `test-location-rules` 为基准，把真实测试代码、脚本、mock、fixture 和执行产物统一落在 `test/yyyy-MM-DD_HHmmss/<ASCII 真实代码路径镜像>/` 下，并避免中文进入会被 Go 工具链编译的路径；不要用它代替 test-location-rules、test-naming-rules、test-doc-rules、bug-runtime-debug-rules 或功能验证规则。",
      "core_responsibility": "统一测试程序和辅助脚本位置。",
      "skill_path": "test-program-rules/SKILL.md",
      "directory_path": "test-program-rules",
      "directory": "test-program-rules",
      "sections": [
        "Skill 作用与适用场景",
        "自动触发信号",
        "进入后先做什么",
        "默认执行流程",
        "权责边界与不负责事项",
        "需要暂停并确认的条件",
        "执行通过 / 驳回标准",
        "执行结果归档要求",
        "references 读取规则"
      ],
      "references": [
        "test-program-rules/references/program-boundaries.md",
        "test-program-rules/references/program-examples.md",
        "test-program-rules/references/program-types-and-splitting.md"
      ],
      "agents": [
        "test-program-rules/agents/openai.yaml"
      ],
      "has_license": false,
      "focus_points": [
        "优先检查 description 是否具体到触发信号，而不是只写抽象用途。",
        "检查 references 是否足以承接复杂场景，避免 SKILL.md 过厚或过空。",
        "重点看测试策略、资源、功能验证、联调、回归是否已经拆开。"
      ]
    },
    {
      "id": "test-doc-rules",
      "name": "test-doc-rules",
      "title": "测试文档规则",
      "status": "implemented",
      "status_label": "已实现",
      "domain_id": "test",
      "domain_label": "测试域",
      "domain_description": "策略、资源、功能验证、联调、回归",
      "domain_order": 7,
      "item_order": 5,
      "auto_trigger": "当新增或修改测试 README、验证说明、测试报告、覆盖说明、测试执行记录时触发。负责统一测试文档的最小结构、记录字段、主文档入口和归档方式；必须以 `test-location-rules` 为基准，使用 `test/yyyy-MM-DD_HHmmss/测试任务中文简介/README.md` 作为中文主说明入口，并把额外文档放到同一时间戳根目录下的 ASCII 真实代码路径镜像目录中；不要用它代替 test-location-rules、test-program-rules、functional-validation-rules 或 test-regression-rules。",
      "core_responsibility": "统一测试说明文档结构。",
      "skill_path": "test-doc-rules/SKILL.md",
      "directory_path": "test-doc-rules",
      "directory": "test-doc-rules",
      "sections": [
        "Skill 作用与适用场景",
        "自动触发信号",
        "进入后先做什么",
        "默认执行流程",
        "权责边界与不负责事项",
        "需要暂停并确认的条件",
        "执行通过 / 驳回标准",
        "执行结果归档要求",
        "references 读取规则"
      ],
      "references": [
        "test-doc-rules/references/doc-boundaries.md",
        "test-doc-rules/references/doc-examples.md",
        "test-doc-rules/references/doc-minimums.md"
      ],
      "agents": [
        "test-doc-rules/agents/openai.yaml"
      ],
      "has_license": false,
      "focus_points": [
        "优先检查 description 是否具体到触发信号，而不是只写抽象用途。",
        "检查 references 是否足以承接复杂场景，避免 SKILL.md 过厚或过空。",
        "重点看测试策略、资源、功能验证、联调、回归是否已经拆开。"
      ]
    },
    {
      "id": "functional-validation-rules",
      "name": "functional-validation-rules",
      "title": "功能验证规则",
      "status": "implemented",
      "status_label": "已实现",
      "domain_id": "test",
      "domain_label": "测试域",
      "domain_description": "策略、资源、功能验证、联调、回归",
      "domain_order": 7,
      "item_order": 6,
      "auto_trigger": "当需要验证新功能、修改后的功能、接口行为、页面交互、输入输出结果是否满足当前需求、当前变更和验收标准时触发。负责界定本次功能验证范围、验证步骤、通过驳回标准和结论留痕；必须以 `test-location-rules` 为基准，把功能验证结论写回 `test/yyyy-MM-DD_HHmmss/测试任务中文简介/README.md`，并把详细执行证据放到同一时间戳根目录下的 ASCII 真实代码路径镜像目录中；不要用它代替 test-strategy-rules、test-location-rules、integration-debugging-rules 或 test-regression-rules。",
      "core_responsibility": "负责当前需求对应的功能正确性验证。",
      "skill_path": "functional-validation-rules/SKILL.md",
      "directory_path": "functional-validation-rules",
      "directory": "functional-validation-rules",
      "sections": [
        "Skill 作用与适用场景",
        "自动触发信号",
        "进入后先做什么",
        "默认执行流程",
        "权责边界与不负责事项",
        "需要暂停并确认的条件",
        "执行通过 / 驳回标准",
        "执行结果归档要求",
        "references 读取规则"
      ],
      "references": [
        "functional-validation-rules/references/validation-boundaries.md",
        "functional-validation-rules/references/validation-scope.md",
        "functional-validation-rules/references/validation-template-and-examples.md"
      ],
      "agents": [
        "functional-validation-rules/agents/openai.yaml"
      ],
      "has_license": false,
      "focus_points": [
        "优先检查 description 是否具体到触发信号，而不是只写抽象用途。",
        "检查 references 是否足以承接复杂场景，避免 SKILL.md 过厚或过空。",
        "重点看测试策略、资源、功能验证、联调、回归是否已经拆开。"
      ]
    },
    {
      "id": "test-regression-rules",
      "name": "test-regression-rules",
      "title": "回归验证规则",
      "status": "implemented",
      "status_label": "已实现",
      "domain_id": "test",
      "domain_label": "测试域",
      "domain_description": "策略、资源、功能验证、联调、回归",
      "domain_order": 7,
      "item_order": 7,
      "auto_trigger": "当 Bug 修复、原有功能迭代、公共模块修改、共享逻辑调整、接口兼容性变化后准备执行测试时触发。负责判定回归范围、选择回归用例、验证兼容性影响并输出回归结论；必须以 `test-location-rules` 为基准，把回归结论统一写回 `test/yyyy-MM-DD_HHmmss/测试任务中文简介/README.md`，并把详细回归案例、执行证据和补充说明放到同一时间戳根目录下的 ASCII 真实代码路径镜像目录中；不要用它代替 functional-validation-rules、test-strategy-rules、integration-debugging-rules 或测试资源管理类规则。",
      "core_responsibility": "明确回归测试的范围、用例选取、验证要点，针对改动点关联的功能、上下游链路做全覆盖验证，防止修复旧 Bug 引入新问题，保障功能兼容性。",
      "skill_path": "test-regression-rules/SKILL.md",
      "directory_path": "test-regression-rules",
      "directory": "test-regression-rules",
      "sections": [
        "Skill 作用与适用场景",
        "自动触发信号",
        "进入后先做什么",
        "默认执行流程",
        "权责边界与不负责事项",
        "需要暂停并确认的条件",
        "执行通过 / 驳回标准",
        "执行结果归档要求",
        "references 读取规则"
      ],
      "references": [
        "test-regression-rules/references/regression-boundaries.md",
        "test-regression-rules/references/regression-scope-selection.md",
        "test-regression-rules/references/regression-template-and-examples.md"
      ],
      "agents": [
        "test-regression-rules/agents/openai.yaml"
      ],
      "has_license": false,
      "focus_points": [
        "优先检查 description 是否具体到触发信号，而不是只写抽象用途。",
        "检查 references 是否足以承接复杂场景，避免 SKILL.md 过厚或过空。",
        "重点看测试策略、资源、功能验证、联调、回归是否已经拆开。"
      ]
    },
    {
      "id": "integration-debugging-rules",
      "name": "integration-debugging-rules",
      "title": "integration-debugging-rules",
      "status": "planned",
      "status_label": "规划中",
      "domain_id": "test",
      "domain_label": "测试域",
      "domain_description": "策略、资源、功能验证、联调、回归",
      "domain_order": 7,
      "item_order": 8,
      "auto_trigger": "当联调、排查接口不通、字段不一致、环境差异、trace 断链、测试环境问题时自动触发。",
      "core_responsibility": "统一联调和排障证据记录。",
      "skill_path": "",
      "directory_path": "",
      "directory": "",
      "sections": [],
      "references": [],
      "agents": [],
      "has_license": false,
      "focus_points": [
        "先补齐触发 description、邻接边界和最小 references，再决定是否正式建目录。",
        "优先确认它与同域相邻 skill 的拆分边界，避免新建后职责重叠。",
        "重点看测试策略、资源、功能验证、联调、回归是否已经拆开。"
      ]
    },
    {
      "id": "git-collaboration-rules",
      "name": "git-collaboration-rules",
      "title": "Git 协作规则",
      "status": "implemented",
      "status_label": "已实现",
      "domain_id": "delivery",
      "domain_label": "交付域",
      "domain_description": "Git 协作、评审、发布与交付说明",
      "domain_order": 8,
      "item_order": 3,
      "auto_trigger": "当准备整理提交、拆提交粒度、同步分支、处理协作变更、准备 PR 或合并前收口时触发。负责提交粒度、提交说明、分支同步、协作边界和 PR 整理；提交代码时必须分析未提交的代码，如果可以分成不同的业务修改，就用多次不同的 git 提交；git 提交消息必须遵循 feat/fix 等格式；不要把它代替代码评审或发布上线规则。",
      "core_responsibility": "统一 Git 协作规则。",
      "skill_path": "git-collaboration-rules/SKILL.md",
      "directory_path": "git-collaboration-rules",
      "directory": "git-collaboration-rules",
      "sections": [
        "Skill 作用与适用场景",
        "自动触发信号",
        "进入后先做什么",
        "默认执行流程",
        "权责边界与不负责事项",
        "需要暂停并确认的条件",
        "执行通过 / 驳回标准",
        "执行结果归档要求",
        "references 读取规则"
      ],
      "references": [
        "git-collaboration-rules/references/branch-and-commit.md",
        "git-collaboration-rules/references/collaboration-examples.md",
        "git-collaboration-rules/references/sync-and-pr-scope.md"
      ],
      "agents": [
        "git-collaboration-rules/agents/openai.yaml"
      ],
      "has_license": false,
      "focus_points": [
        "优先检查 description 是否具体到触发信号，而不是只写抽象用途。",
        "检查 references 是否足以承接复杂场景，避免 SKILL.md 过厚或过空。",
        "重点看 Git 协作、评审、发布、交付说明是否已分层收口。"
      ]
    },
    {
      "id": "delivery-summary-rules",
      "name": "delivery-summary-rules",
      "title": "交付总结规则",
      "status": "implemented",
      "status_label": "已实现",
      "domain_id": "delivery",
      "domain_label": "交付域",
      "domain_description": "Git 协作、评审、发布与交付说明",
      "domain_order": 8,
      "item_order": 4,
      "auto_trigger": "当开发人员提出“请帮我生成交付文档”“发布文档”“发布总结文档”“准备上线总结文档”等请求，需要输出一份可交接、可发布、可复盘的总结文档时触发。负责交付说明结构、Git 提交范围汇总、验证摘要、风险说明、保存位置和后续建议；必须先得到用户确认是否开始发布总结，不要把它代替发布动作或代码评审。",
      "core_responsibility": "统一交付文档结构。",
      "skill_path": "delivery-summary-rules/SKILL.md",
      "directory_path": "delivery-summary-rules",
      "directory": "delivery-summary-rules",
      "sections": [
        "Skill 作用与适用场景",
        "自动触发信号",
        "进入后先做什么",
        "默认执行流程",
        "权责边界与不负责事项",
        "需要暂停并确认的条件",
        "执行通过 / 驳回标准",
        "执行结果归档要求",
        "references 读取规则"
      ],
      "references": [
        "delivery-summary-rules/references/delivery-examples.md",
        "delivery-summary-rules/references/delivery-risk-and-debt.md",
        "delivery-summary-rules/references/delivery-template.md"
      ],
      "agents": [
        "delivery-summary-rules/agents/openai.yaml"
      ],
      "has_license": false,
      "focus_points": [
        "优先检查 description 是否具体到触发信号，而不是只写抽象用途。",
        "检查 references 是否足以承接复杂场景，避免 SKILL.md 过厚或过空。",
        "重点看 Git 协作、评审、发布、交付说明是否已分层收口。"
      ]
    },
    {
      "id": "release-rollout-rules",
      "name": "release-rollout-rules",
      "title": "release-rollout-rules",
      "status": "planned",
      "status_label": "规划中",
      "domain_id": "delivery",
      "domain_label": "交付域",
      "domain_description": "Git 协作、评审、发布与交付说明",
      "domain_order": 8,
      "item_order": 1,
      "auto_trigger": "当新增或修改发布脚本、发布检查、灰度策略、观察窗口、上线 checklist、回滚条件时自动触发。",
      "core_responsibility": "管理上线和回滚规则。",
      "skill_path": "",
      "directory_path": "",
      "directory": "",
      "sections": [],
      "references": [],
      "agents": [],
      "has_license": false,
      "focus_points": [
        "先补齐触发 description、邻接边界和最小 references，再决定是否正式建目录。",
        "优先确认它与同域相邻 skill 的拆分边界，避免新建后职责重叠。",
        "重点看 Git 协作、评审、发布、交付说明是否已分层收口。"
      ]
    },
    {
      "id": "code-review-rules",
      "name": "code-review-rules",
      "title": "code-review-rules",
      "status": "planned",
      "status_label": "规划中",
      "domain_id": "delivery",
      "domain_label": "交付域",
      "domain_description": "Git 协作、评审、发布与交付说明",
      "domain_order": 8,
      "item_order": 2,
      "auto_trigger": "当任务是 PR 评审、他人代码评审、检查 diff、风险扫描、测试遗漏检查或交付前复查时自动触发。",
      "core_responsibility": "统一评审重点和输出方式，不替代编码完成后的自审。",
      "skill_path": "",
      "directory_path": "",
      "directory": "",
      "sections": [],
      "references": [],
      "agents": [],
      "has_license": false,
      "focus_points": [
        "先补齐触发 description、邻接边界和最小 references，再决定是否正式建目录。",
        "优先确认它与同域相邻 skill 的拆分边界，避免新建后职责重叠。",
        "重点看 Git 协作、评审、发布、交付说明是否已分层收口。"
      ]
    },
    {
      "id": "skill-evolution-rules",
      "name": "skill-evolution-rules",
      "title": "skill-evolution-rules",
      "status": "planned",
      "status_label": "规划中",
      "domain_id": "evolution",
      "domain_label": "体系维护域",
      "domain_description": "维护 skill 体系自身的拆分、迁移与演进",
      "domain_order": 9,
      "item_order": 1,
      "auto_trigger": "当新增、修改、拆分、合并团队内部 skill，或发现某类规则应当迁移到其他 skill 中时自动触发。",
      "core_responsibility": "维护 skill 体系自身的拆分和演进规则。",
      "skill_path": "",
      "directory_path": "",
      "directory": "",
      "sections": [],
      "references": [],
      "agents": [],
      "has_license": false,
      "focus_points": [
        "先补齐触发 description、邻接边界和最小 references，再决定是否正式建目录。",
        "优先确认它与同域相邻 skill 的拆分边界，避免新建后职责重叠。",
        "重点看新增、合并、迁移和退休 skill 的门槛是否足够明确。"
      ]
    }
  ],
  "docs": [
    {
      "id": "doc:编码skill",
      "name": "编码skill",
      "file_name": "编码skill.md",
      "title": "编码 Skill 体系整体计划（审查稿）",
      "kind": "总规划",
      "path": "编码skill.md",
      "is_plan_doc": true
    },
    {
      "id": "doc:完成习惯调整",
      "name": "完成习惯调整",
      "file_name": "完成习惯调整.md",
      "title": "package-structure-rules [√]",
      "kind": "其他文档",
      "path": "完成习惯调整.md",
      "is_plan_doc": false
    },
    {
      "id": "doc:未调整",
      "name": "未调整",
      "file_name": "未调整.md",
      "title": "未调整的 Skill 列表",
      "kind": "其他文档",
      "path": "未调整.md",
      "is_plan_doc": false
    }
  ],
  "recommendations": [
    "Bug 域还缺 1 个环节，尤其是复现、范围界定、诊断日志和修复后验证，建议补完整闭环。",
    "测试域缺 1 个、交付域缺 2 个，建议先补 `test-strategy-rules` 和交付域三件套。",
    "当前规划同时包含 `frontend-component-rules` 与 `frontend-ui-visual-rules`，建议前者聚焦组件工程与状态边界，后者聚焦页面视觉与交互体验，避免触发歧义。"
  ]
};
