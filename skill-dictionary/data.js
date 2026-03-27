window.SKILL_DICTIONARY = {
  "generated_at": "2026-03-27 11:37:04",
  "repo_root": "D:\\code\\luode-skills",
  "plan_doc": "编码skill.md",
  "plan_doc_name": "编码skill.md",
  "summary": {
    "planned_total": 55,
    "implemented_total": 35,
    "planned_missing": 20,
    "seed_total": 2,
    "doc_total": 1,
    "references_total": 117,
    "agents_total": 37
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
      "implemented_count": 2,
      "planned_count": 4,
      "seed_count": 0,
      "total_count": 6,
      "items": [
        {
          "id": "requirement-intake-rules",
          "name": "requirement-intake-rules",
          "title": "requirement-intake-rules",
          "status": "planned",
          "status_label": "规划中",
          "domain_id": "requirement",
          "domain_label": "需求域",
          "domain_description": "需求澄清、缺口识别、边界确认、验收前置",
          "domain_order": 2,
          "item_order": 1,
          "auto_trigger": "当用户提出新需求、新功能、新页面、新接口、新模块，且任务刚进入研发阶段时自动触发。",
          "core_responsibility": "先理解目标、背景、上下游和输入输出。",
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
          "auto_trigger": "当需求描述不完整、缺少前提、缺少字段、缺少流程、缺少业务规则、缺少依赖条件或缺少验收信息时触发。负责识别需求缺口并在信息不足时阻断盲目编码推进；不要用它代替需求边界判断、需求变更判断或验收标准细化 skill。",
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
          "auto_trigger": "当需求边界不清、影响范围不明、兼容性不明确、是否允许改旧逻辑不清楚，或需要区分当前需求、历史问题、需求变更和验收偏差时触发。负责明确改动边界和影响面；不要用它代替需求缺口识别或 Bug 根因定位 skill。",
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
          "title": "requirement-splitting-rules",
          "status": "planned",
          "status_label": "规划中",
          "domain_id": "requirement",
          "domain_label": "需求域",
          "domain_description": "需求澄清、缺口识别、边界确认、验收前置",
          "domain_order": 2,
          "item_order": 4,
          "auto_trigger": "当需求较大、涉及多个模块、多个接口、多个页面、多个步骤时自动触发。",
          "core_responsibility": "负责任务拆分、模块拆分和实施顺序。",
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
            "重点看是否能区分需求缺口、边界变化、验收偏差和历史 Bug。"
          ]
        },
        {
          "id": "requirement-change-rules",
          "name": "requirement-change-rules",
          "title": "requirement-change-rules",
          "status": "planned",
          "status_label": "规划中",
          "domain_id": "requirement",
          "domain_label": "需求域",
          "domain_description": "需求澄清、缺口识别、边界确认、验收前置",
          "domain_order": 2,
          "item_order": 5,
          "auto_trigger": "当编码过程中需求被补充、修正、插入新条件、改变优先级时自动触发。",
          "core_responsibility": "重新确认变更范围和影响。",
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
            "重点看是否能区分需求缺口、边界变化、验收偏差和历史 Bug。"
          ]
        },
        {
          "id": "acceptance-criteria-rules",
          "name": "acceptance-criteria-rules",
          "title": "acceptance-criteria-rules",
          "status": "planned",
          "status_label": "规划中",
          "domain_id": "requirement",
          "domain_label": "需求域",
          "domain_description": "需求澄清、缺口识别、边界确认、验收前置",
          "domain_order": 2,
          "item_order": 6,
          "auto_trigger": "当任务准备进入实现前确认，或交付前需要验收标准时自动触发。",
          "core_responsibility": "补齐可验证、可测试的验收标准。",
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
      "implemented_count": 4,
      "planned_count": 7,
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
          "auto_trigger": "当用户描述报错、异常行为、结果不符、线上问题、偶发问题、接口异常、页面异常、数据错误或性能异常时触发。负责把 Bug 描述标准化，整理现象、影响范围、环境条件、期望结果和实际结果；不要用它代替根因定位、运行时调试或修复方案制定 skill。",
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
          "title": "bug-gap-rules",
          "status": "planned",
          "status_label": "规划中",
          "domain_id": "bug",
          "domain_label": "Bug 域",
          "domain_description": "问题录入、定位、运行时诊断、修复建议",
          "domain_order": 3,
          "item_order": 2,
          "auto_trigger": "当 bug 描述缺少复现条件、环境信息、输入数据、报错日志、影响范围时自动触发。",
          "core_responsibility": "补齐定位所需基础信息。",
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
          "id": "bug-reproduction-rules",
          "name": "bug-reproduction-rules",
          "title": "bug-reproduction-rules",
          "status": "planned",
          "status_label": "规划中",
          "domain_id": "bug",
          "domain_label": "Bug 域",
          "domain_description": "问题录入、定位、运行时诊断、修复建议",
          "domain_order": 3,
          "item_order": 3,
          "auto_trigger": "当问题需要复现、构造步骤、确定触发条件、判断是否稳定发生时自动触发。",
          "core_responsibility": "输出复现步骤和复现结论。",
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
          "auto_trigger": "当开始分析代码、追调用链、看现有日志、查 trace、结合上下游行为定位 Bug 根因时触发。负责通过静态证据收敛根因并区分实现问题与设计问题；不要用它代替运行时调试或修复方案制定 skill。",
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
          "title": "bug-debug-log-rules",
          "status": "planned",
          "status_label": "规划中",
          "domain_id": "bug",
          "domain_label": "Bug 域",
          "domain_description": "问题录入、定位、运行时诊断、修复建议",
          "domain_order": 3,
          "item_order": 7,
          "auto_trigger": "当定位 bug 需要临时增加 debug 日志、关键变量输出、关键分支日志、上下游输入输出日志时自动触发。",
          "core_responsibility": "通过可回收的临时日志补充运行期证据。",
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
          "id": "bug-assertion-diagnostic-rules",
          "name": "bug-assertion-diagnostic-rules",
          "title": "bug-assertion-diagnostic-rules",
          "status": "planned",
          "status_label": "规划中",
          "domain_id": "bug",
          "domain_label": "Bug 域",
          "domain_description": "问题录入、定位、运行时诊断、修复建议",
          "domain_order": 3,
          "item_order": 8,
          "auto_trigger": "当怀疑状态异常、顺序错误、数据污染、不变量被破坏，且需要通过程序断言或诊断性检查快速暴露问题位置时自动触发。",
          "core_responsibility": "用断言和诊断检查缩小 bug 发生区间。",
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
          "auto_trigger": "当问题已定位，需要形成修改建议、风险评估、备选方案并判断是否应等待用户确认时触发。负责把 Bug 域稳定交接到编码域；不要用它代替根因定位或直接实施编码修复。",
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
          "title": "bug-regression-risk-rules",
          "status": "planned",
          "status_label": "规划中",
          "domain_id": "bug",
          "domain_label": "Bug 域",
          "domain_description": "问题录入、定位、运行时诊断、修复建议",
          "domain_order": 3,
          "item_order": 10,
          "auto_trigger": "当修复可能影响公共方法、共享模块、已有接口、数据库行为或兼容性时自动触发。",
          "core_responsibility": "识别回归风险。",
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
          "id": "bug-validation-rules",
          "name": "bug-validation-rules",
          "title": "bug-validation-rules",
          "status": "planned",
          "status_label": "规划中",
          "domain_id": "bug",
          "domain_label": "Bug 域",
          "domain_description": "问题录入、定位、运行时诊断、修复建议",
          "domain_order": 3,
          "item_order": 11,
          "auto_trigger": "当 bug 修复后需要验证是否修好、是否引入副作用、是否需要补回归测试时自动触发。",
          "core_responsibility": "负责修复后的验证闭环。",
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
        }
      ]
    },
    {
      "id": "baseline",
      "label": "编码基线域",
      "description": "开始编码即并行生效的基础质量规则",
      "order": 4,
      "implemented_count": 3,
      "planned_count": 3,
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
          "title": "naming-rules",
          "status": "planned",
          "status_label": "规划中",
          "domain_id": "baseline",
          "domain_label": "编码基线域",
          "domain_description": "开始编码即并行生效的基础质量规则",
          "domain_order": 4,
          "item_order": 4,
          "auto_trigger": "当新增或修改类名、函数名、变量名、常量名、DTO、实体、字段映射名时自动触发。",
          "core_responsibility": "保证命名语义化。",
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
            "重点看它是否能并行生效，并且不抢位点域或审查域职责。"
          ]
        },
        {
          "id": "chinese-comment-rules",
          "name": "chinese-comment-rules",
          "title": "chinese-comment-rules",
          "status": "planned",
          "status_label": "规划中",
          "domain_id": "baseline",
          "domain_label": "编码基线域",
          "domain_description": "开始编码即并行生效的基础质量规则",
          "domain_order": 4,
          "item_order": 5,
          "auto_trigger": "当新增或修改中文注释、业务说明、中文文档注释时自动触发。",
          "core_responsibility": "统一中文表达习惯和注释语气。",
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
            "重点看它是否能并行生效，并且不抢位点域或审查域职责。"
          ]
        },
        {
          "id": "code-comment-rules",
          "name": "code-comment-rules",
          "title": "code-comment-rules",
          "status": "planned",
          "status_label": "规划中",
          "domain_id": "baseline",
          "domain_label": "编码基线域",
          "domain_description": "开始编码即并行生效的基础质量规则",
          "domain_order": 4,
          "item_order": 6,
          "auto_trigger": "当新增或修改函数注释、类注释、模块注释、步骤注释、代码块注释时自动触发。",
          "core_responsibility": "统一注释层级和颗粒度。",
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
      "implemented_count": 13,
      "planned_count": 1,
      "seed_count": 0,
      "total_count": 14,
      "items": [
        {
          "id": "config-change-rules",
          "name": "config-change-rules",
          "title": "配置变更规则",
          "status": "implemented",
          "status_label": "已实现",
          "domain_id": "location",
          "domain_label": "代码位点域",
          "domain_description": "按改动位置叠加触发的实现规则",
          "domain_order": 5,
          "item_order": 1,
          "auto_trigger": "当新增或修改 `.env`、`.env.example`、`application.yml`、`application.yaml`、`settings.py`、`config.ts`、`appsettings.json`、`values.yaml`、环境变量读取、默认值、配置注入、配置分层、特性开关、密钥占位时自动触发。负责统一配置来源、分层、默认值、敏感配置和密钥占位规则，避免把业务逻辑、危险默认值和秘密暴露混进配置变更；不要用它代替 auth-security-rules、request-header-rules、deployment 或发布规则。",
          "core_responsibility": "统一配置、密钥和默认值策略。",
          "skill_path": "config-change-rules/SKILL.md",
          "directory_path": "config-change-rules",
          "directory": "config-change-rules",
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
            "config-change-rules/references/config-boundaries-and-examples.md",
            "config-change-rules/references/config-layering-and-sources.md",
            "config-change-rules/references/defaults-and-secrets.md"
          ],
          "agents": [
            "config-change-rules/agents/openai.yaml"
          ],
          "has_license": false,
          "focus_points": [
            "优先检查 description 是否具体到触发信号，而不是只写抽象用途。",
            "检查 references 是否足以承接复杂场景，避免 SKILL.md 过厚或过空。",
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
          "auto_trigger": "当新增或修改包、目录、模块、分层结构、包名定义、文件归属或跨层引用关系时触发。负责统一代码包定义、目录分层、包职责、模块边界和依赖方向，尤其适用于 Go、Java、Node/Python 项目的结构决策；不要用它代替工具实现、接口规则或代码审查类 skill。",
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
          "auto_trigger": "当新增或修改表、字段、索引、唯一约束、外键、迁移脚本、DDL、实体结构、schema 定义时自动触发。负责统一数据库结构变更、迁移安全、兼容性和回滚边界，避免把查询实现、事务控制和业务逻辑混进结构变更；不要用它代替 database-query-rules、config-change-rules 或发布回滚规则。",
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
          "auto_trigger": "当新增或修改 controller、router、handler、路由声明、HTTP 方法、接口 CRUD 路径命名、接口入口职责或超时入口边界时触发。负责统一接口入口设计、路径命名和 HTTP 方法语义；不要用它代替请求参数、响应结构或错误处理规则。",
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
          "auto_trigger": "当新增或修改请求参数、DTO、query 参数、path 参数、body 结构、参数校验或请求模型时触发。负责统一请求结构、参数表达和基础校验边界；不要用它代替接口入口设计、响应结构或业务规则本身。",
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
          "auto_trigger": "当新增或修改返回体、响应包装器、分页结构、错误响应结构、兼容字段、版本字段或统一响应模型时触发。负责统一响应格式和兼容策略；不要用它代替错误处理流程、异常分类或接口入口职责规则。",
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
          "title": "请求头规则",
          "status": "implemented",
          "status_label": "已实现",
          "domain_id": "location",
          "domain_label": "代码位点域",
          "domain_description": "按改动位置叠加触发的实现规则",
          "domain_order": 5,
          "item_order": 9,
          "auto_trigger": "当新增或修改认证头、trace-id、span-id、租户头、幂等键、客户端上下文头、X-Forwarded-* 逻辑时自动触发。负责统一请求头分类、来源可信度、透传边界和消费规则，避免把请求参数、日志字段和安全策略混进 Header 约定；不要用它代替 api-request-rules、logging-trace-rules 或 auth-security-rules。",
          "core_responsibility": "统一请求头约定和透传规则。",
          "skill_path": "request-header-rules/SKILL.md",
          "directory_path": "request-header-rules",
          "directory": "request-header-rules",
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
            "request-header-rules/references/header-boundaries-and-examples.md",
            "request-header-rules/references/header-categories-and-trust.md",
            "request-header-rules/references/propagation-and-forwarding.md"
          ],
          "agents": [
            "request-header-rules/agents/openai.yaml"
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
          "id": "auth-security-rules",
          "name": "auth-security-rules",
          "title": "认证与安全规则",
          "status": "implemented",
          "status_label": "已实现",
          "domain_id": "location",
          "domain_label": "代码位点域",
          "domain_description": "按改动位置叠加触发的实现规则",
          "domain_order": 5,
          "item_order": 12,
          "auto_trigger": "当新增或修改认证、鉴权、登录、登出、会话、JWT、对象级授权、输入校验、敏感信息处理、上传下载安全、外部请求安全时自动触发。负责统一安全实现的默认基线，覆盖身份校验、权限校验、输入处理、敏感信息和高风险入口控制；不要用它代替 request-header-rules、api-request-rules、error-handling-rules 或纯日志 trace 规则。",
          "core_responsibility": "统一安全实现的默认基线。",
          "skill_path": "auth-security-rules/SKILL.md",
          "directory_path": "auth-security-rules",
          "directory": "auth-security-rules",
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
            "auth-security-rules/references/framework-seed-selection.md",
            "auth-security-rules/references/security-baseline.md",
            "auth-security-rules/references/security-boundaries.md"
          ],
          "agents": [
            "auth-security-rules/agents/openai.yaml"
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
          "title": "frontend-component-rules",
          "status": "planned",
          "status_label": "规划中",
          "domain_id": "location",
          "domain_label": "代码位点域",
          "domain_description": "按改动位置叠加触发的实现规则",
          "domain_order": 5,
          "item_order": 13,
          "auto_trigger": "当新增或修改 React、Vue、前端组件、页面、表单、状态流、客户端数据展示逻辑时自动触发。",
          "core_responsibility": "统一前端组件和页面工程规则。",
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
          "title": "性能与缓存规则",
          "status": "implemented",
          "status_label": "已实现",
          "domain_id": "location",
          "domain_label": "代码位点域",
          "domain_description": "按改动位置叠加触发的实现规则",
          "domain_order": 5,
          "item_order": 14,
          "auto_trigger": "当新增或修改 SQL 性能、接口耗时、缓存读取写入、缓存 key、缓存失效、前端渲染热点、大列表、图表、虚拟滚动时自动触发。负责统一性能与缓存边界，区分必要优化与过度优化，避免把业务逻辑、schema 问题和缓存副作用伪装成性能改进；不要用它代替 database-query-rules、database-schema-rules 或前端组件结构规则。",
          "core_responsibility": "统一性能和缓存规则。",
          "skill_path": "performance-caching-rules/SKILL.md",
          "directory_path": "performance-caching-rules",
          "directory": "performance-caching-rules",
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
            "performance-caching-rules/references/cache-strategy-rules.md",
            "performance-caching-rules/references/performance-boundaries.md",
            "performance-caching-rules/references/performance-examples.md"
          ],
          "agents": [
            "performance-caching-rules/agents/openai.yaml"
          ],
          "has_license": false,
          "focus_points": [
            "优先检查 description 是否具体到触发信号，而不是只写抽象用途。",
            "检查 references 是否足以承接复杂场景，避免 SKILL.md 过厚或过空。",
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
          "auto_trigger": "当功能代码已经完成、准备进入测试前验证时触发。负责检查实现是否符合编码规范、命名规范、注释规范、风格一致性和最小改动原则；不要用它代替语法检查、格式清理或代码归位审查规则。",
          "core_responsibility": "对刚完成的实现做一次测试前规范自审。",
          "skill_path": "implementation-review-rules/SKILL.md",
          "directory_path": "implementation-review-rules",
          "directory": "implementation-review-rules",
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
          "title": "test-strategy-rules",
          "status": "planned",
          "status_label": "规划中",
          "domain_id": "test",
          "domain_label": "测试域",
          "domain_description": "策略、资源、功能验证、联调、回归",
          "domain_order": 7,
          "item_order": 1,
          "auto_trigger": "当功能实现和编码审查完成后，开始补测试、写验证脚本、做回归检查时自动触发。",
          "core_responsibility": "决定测试层级和覆盖重点。",
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
          "auto_trigger": "当新增或修改测试目录、测试文件、测试脚本、验证程序、fixture、mock 数据、测试说明文档落点时触发。负责统一测试资源根目录、任务目录和禁止散落规则；不要用它代替 test-naming-rules、test-program-rules、test-doc-rules、code-placement-review-rules 或功能验证规则。",
          "core_responsibility": "统一测试资源位置。",
          "skill_path": "test-location-rules/SKILL.md",
          "directory_path": "test-location-rules",
          "directory": "test-location-rules",
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
          "auto_trigger": "当创建或修改测试任务目录、测试文件、测试脚本、测试数据目录、fixture 目录、mock 目录时触发。负责统一测试目录与文件命名规范，保证名称可读、可检索、与业务目标一致；不要用它代替 test-location-rules、test-program-rules、test-doc-rules 或功能验证规则。",
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
          "auto_trigger": "当新增或修改测试程序、模拟程序、验证脚本、数据构造脚本、测试辅助代码时触发。负责统一测试程序职责划分、脚手架结构、辅助代码边界和复用方式，避免临时验证代码混入正式业务目录；不要用它代替 test-location-rules、test-naming-rules、test-doc-rules、bug-runtime-debug-rules 或功能验证规则。",
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
          "auto_trigger": "当新增或修改测试 README、验证说明、测试报告、覆盖说明、测试执行记录时触发。负责统一测试文档的最小结构、记录字段、归档方式和通过驳回标准，保证测试资产可追溯；不要用它代替 test-location-rules、test-program-rules、functional-validation-rules 或 test-regression-rules。",
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
          "auto_trigger": "当需要验证新功能、修改后的功能、接口行为、页面交互、输入输出结果是否满足当前需求、当前变更和验收标准时触发。负责界定本次功能验证范围、验证步骤、通过驳回标准和结论留痕；不要用它代替 test-strategy-rules、test-location-rules、integration-debugging-rules 或 test-regression-rules。",
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
          "auto_trigger": "当 Bug 修复、原有功能迭代、公共模块修改、共享逻辑调整、接口兼容性变化后准备执行测试时触发。负责判定回归范围、选择回归用例、验证兼容性影响并输出回归结论；不要用它代替 functional-validation-rules、test-strategy-rules、integration-debugging-rules 或测试资源管理类规则。",
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
          "title": "联调排障规则",
          "status": "implemented",
          "status_label": "已实现",
          "domain_id": "test",
          "domain_label": "测试域",
          "domain_description": "策略、资源、功能验证、联调、回归",
          "domain_order": 7,
          "item_order": 8,
          "auto_trigger": "当联调、排查接口不通、字段不一致、环境差异、trace 断链、测试环境问题时自动触发。负责统一跨系统联调、环境差异排查、链路证据记录和问题分流规则，避免把单点功能错误或单模块运行时 Bug 诊断误归到联调层；不要用它代替 functional-validation-rules、bug-runtime-debug-rules、request-header-rules 或 logging-trace-rules。",
          "core_responsibility": "统一联调和排障证据记录。",
          "skill_path": "integration-debugging-rules/SKILL.md",
          "directory_path": "integration-debugging-rules",
          "directory": "integration-debugging-rules",
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
            "integration-debugging-rules/references/env-diff-and-chain-diagnostics.md",
            "integration-debugging-rules/references/integration-boundaries-and-handoff.md",
            "integration-debugging-rules/references/integration-scope-and-evidence.md"
          ],
          "agents": [
            "integration-debugging-rules/agents/openai.yaml"
          ],
          "has_license": false,
          "focus_points": [
            "优先检查 description 是否具体到触发信号，而不是只写抽象用途。",
            "检查 references 是否足以承接复杂场景，避免 SKILL.md 过厚或过空。",
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
      "implemented_count": 0,
      "planned_count": 4,
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
          "title": "git-collaboration-rules",
          "status": "planned",
          "status_label": "规划中",
          "domain_id": "delivery",
          "domain_label": "交付域",
          "domain_description": "Git 协作、评审、发布与交付说明",
          "domain_order": 8,
          "item_order": 3,
          "auto_trigger": "当创建提交、整理提交说明、准备 PR、合并前检查时自动触发。",
          "core_responsibility": "统一 Git 协作规则。",
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
          "id": "delivery-summary-rules",
          "name": "delivery-summary-rules",
          "title": "delivery-summary-rules",
          "status": "planned",
          "status_label": "规划中",
          "domain_id": "delivery",
          "domain_label": "交付域",
          "domain_description": "Git 协作、评审、发布与交付说明",
          "domain_order": 8,
          "item_order": 4,
          "auto_trigger": "当准备交付说明、变更说明、影响范围说明、风险说明时自动触发。",
          "core_responsibility": "统一交付文档结构。",
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
        }
      ]
    },
    {
      "id": "evolution",
      "label": "体系维护域",
      "description": "维护 skill 体系自身的拆分、迁移与演进",
      "order": 9,
      "implemented_count": 1,
      "planned_count": 0,
      "seed_count": 0,
      "total_count": 1,
      "items": [
        {
          "id": "skill-evolution-rules",
          "name": "skill-evolution-rules",
          "title": "Skill 体系演进规则",
          "status": "implemented",
          "status_label": "已实现",
          "domain_id": "evolution",
          "domain_label": "体系维护域",
          "domain_description": "维护 skill 体系自身的拆分、迁移与演进",
          "domain_order": 9,
          "item_order": 1,
          "auto_trigger": "当新增、修改、拆分、合并、迁移或退休团队内部 skill，或发现现有 skill 边界失衡、触发描述失真、references 结构失控时触发。负责维护 skill 体系自身的拆分与演进规则；不要用它代替业务 skill 编写业务细则。",
          "core_responsibility": "维护 skill 体系自身的拆分和演进规则。",
          "skill_path": "skill-evolution-rules/SKILL.md",
          "directory_path": "skill-evolution-rules",
          "directory": "skill-evolution-rules",
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
            "skill-evolution-rules/references/evolution-patterns.md",
            "skill-evolution-rules/references/migration-checklist.md",
            "skill-evolution-rules/references/split-merge-boundaries.md"
          ],
          "agents": [
            "skill-evolution-rules/agents/openai.yaml"
          ],
          "has_license": false,
          "focus_points": [
            "优先检查 description 是否具体到触发信号，而不是只写抽象用途。",
            "检查 references 是否足以承接复杂场景，避免 SKILL.md 过厚或过空。",
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
      "seed_count": 2,
      "total_count": 2,
      "items": [
        {
          "id": "frontend-skill",
          "name": "frontend-skill",
          "title": "前端界面设计种子 Skill",
          "status": "seed",
          "status_label": "扩展种子",
          "domain_id": "seed",
          "domain_label": "扩展种子",
          "domain_description": "已入库但未并入主规划的参考 skill",
          "domain_order": 10,
          "item_order": 1,
          "auto_trigger": "当任务要求产出有明显视觉表达的落地页、网站、应用界面、原型、演示页或游戏 UI 时使用。这个 skill 强调克制的版式、清晰的信息层级、统一的内容结构和有节制的动效，避免通用卡片堆砌、品牌感弱和界面噪音。",
          "core_responsibility": "当前已在仓库中，但尚未并入主规划域表。",
          "skill_path": "frontend-skill/SKILL.md",
          "directory_path": "frontend-skill",
          "directory": "frontend-skill",
          "sections": [
            "工作模型",
            "默认做法",
            "落地页",
            "应用界面",
            "图片使用",
            "文案",
            "产品型页面文案",
            "动效",
            "硬规则",
            "常见失败",
            "自检问题"
          ],
          "references": [],
          "agents": [
            "frontend-skill/agents/openai.yaml"
          ],
          "has_license": true,
          "focus_points": [
            "先决定它是并入主规划、保持外部种子，还是拆成多个更窄的内部 skill。",
            "如果准备纳入体系，先补上与主规划域的映射关系和落位说明。",
            "重点看这个种子是否真的能落入主规划，还是保持独立参考更合适。"
          ]
        },
        {
          "id": "security-best-practices",
          "name": "security-best-practices",
          "title": "安全最佳实践种子 Skill",
          "status": "seed",
          "status_label": "扩展种子",
          "domain_id": "seed",
          "domain_label": "扩展种子",
          "domain_description": "已入库但未并入主规划的参考 skill",
          "domain_order": 10,
          "item_order": 2,
          "auto_trigger": "当用户明确要求安全最佳实践建议、安全评审、安全报告，或需要生成安全默认代码时使用。适用于 python、javascript/typescript、go 相关项目；不要在普通调试、通用代码评审或非安全任务中触发。",
          "core_responsibility": "当前已在仓库中，但尚未并入主规划域表。",
          "skill_path": "security-best-practices/SKILL.md",
          "directory_path": "security-best-practices",
          "directory": "security-best-practices",
          "sections": [
            "概览",
            "使用流程",
            "参考文件选择规则",
            "工作模式",
            "报告要求",
            "修复原则",
            "通用安全原则"
          ],
          "references": [
            "security-best-practices/references/golang-general-backend-security.md",
            "security-best-practices/references/javascript-express-web-server-security.md",
            "security-best-practices/references/javascript-general-web-frontend-security.md",
            "security-best-practices/references/javascript-jquery-web-frontend-security.md",
            "security-best-practices/references/javascript-typescript-nextjs-web-server-security.md",
            "security-best-practices/references/javascript-typescript-react-web-frontend-security.md",
            "security-best-practices/references/javascript-typescript-vue-web-frontend-security.md",
            "security-best-practices/references/python-django-web-server-security.md",
            "security-best-practices/references/python-fastapi-web-server-security.md",
            "security-best-practices/references/python-flask-web-server-security.md"
          ],
          "agents": [
            "security-best-practices/agents/openai.yaml"
          ],
          "has_license": true,
          "focus_points": [
            "先决定它是并入主规划、保持外部种子，还是拆成多个更窄的内部 skill。",
            "如果准备纳入体系，先补上与主规划域的映射关系和落位说明。",
            "重点看这个种子是否真的能落入主规划，还是保持独立参考更合适。"
          ]
        }
      ]
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
      "auto_trigger": "当需求描述不完整、缺少前提、缺少字段、缺少流程、缺少业务规则、缺少依赖条件或缺少验收信息时触发。负责识别需求缺口并在信息不足时阻断盲目编码推进；不要用它代替需求边界判断、需求变更判断或验收标准细化 skill。",
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
      "auto_trigger": "当需求边界不清、影响范围不明、兼容性不明确、是否允许改旧逻辑不清楚，或需要区分当前需求、历史问题、需求变更和验收偏差时触发。负责明确改动边界和影响面；不要用它代替需求缺口识别或 Bug 根因定位 skill。",
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
      "id": "requirement-intake-rules",
      "name": "requirement-intake-rules",
      "title": "requirement-intake-rules",
      "status": "planned",
      "status_label": "规划中",
      "domain_id": "requirement",
      "domain_label": "需求域",
      "domain_description": "需求澄清、缺口识别、边界确认、验收前置",
      "domain_order": 2,
      "item_order": 1,
      "auto_trigger": "当用户提出新需求、新功能、新页面、新接口、新模块，且任务刚进入研发阶段时自动触发。",
      "core_responsibility": "先理解目标、背景、上下游和输入输出。",
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
        "重点看是否能区分需求缺口、边界变化、验收偏差和历史 Bug。"
      ]
    },
    {
      "id": "requirement-splitting-rules",
      "name": "requirement-splitting-rules",
      "title": "requirement-splitting-rules",
      "status": "planned",
      "status_label": "规划中",
      "domain_id": "requirement",
      "domain_label": "需求域",
      "domain_description": "需求澄清、缺口识别、边界确认、验收前置",
      "domain_order": 2,
      "item_order": 4,
      "auto_trigger": "当需求较大、涉及多个模块、多个接口、多个页面、多个步骤时自动触发。",
      "core_responsibility": "负责任务拆分、模块拆分和实施顺序。",
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
        "重点看是否能区分需求缺口、边界变化、验收偏差和历史 Bug。"
      ]
    },
    {
      "id": "requirement-change-rules",
      "name": "requirement-change-rules",
      "title": "requirement-change-rules",
      "status": "planned",
      "status_label": "规划中",
      "domain_id": "requirement",
      "domain_label": "需求域",
      "domain_description": "需求澄清、缺口识别、边界确认、验收前置",
      "domain_order": 2,
      "item_order": 5,
      "auto_trigger": "当编码过程中需求被补充、修正、插入新条件、改变优先级时自动触发。",
      "core_responsibility": "重新确认变更范围和影响。",
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
        "重点看是否能区分需求缺口、边界变化、验收偏差和历史 Bug。"
      ]
    },
    {
      "id": "acceptance-criteria-rules",
      "name": "acceptance-criteria-rules",
      "title": "acceptance-criteria-rules",
      "status": "planned",
      "status_label": "规划中",
      "domain_id": "requirement",
      "domain_label": "需求域",
      "domain_description": "需求澄清、缺口识别、边界确认、验收前置",
      "domain_order": 2,
      "item_order": 6,
      "auto_trigger": "当任务准备进入实现前确认，或交付前需要验收标准时自动触发。",
      "core_responsibility": "补齐可验证、可测试的验收标准。",
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
      "auto_trigger": "当用户描述报错、异常行为、结果不符、线上问题、偶发问题、接口异常、页面异常、数据错误或性能异常时触发。负责把 Bug 描述标准化，整理现象、影响范围、环境条件、期望结果和实际结果；不要用它代替根因定位、运行时调试或修复方案制定 skill。",
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
      "auto_trigger": "当开始分析代码、追调用链、看现有日志、查 trace、结合上下游行为定位 Bug 根因时触发。负责通过静态证据收敛根因并区分实现问题与设计问题；不要用它代替运行时调试或修复方案制定 skill。",
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
      "auto_trigger": "当问题已定位，需要形成修改建议、风险评估、备选方案并判断是否应等待用户确认时触发。负责把 Bug 域稳定交接到编码域；不要用它代替根因定位或直接实施编码修复。",
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
      "id": "bug-gap-rules",
      "name": "bug-gap-rules",
      "title": "bug-gap-rules",
      "status": "planned",
      "status_label": "规划中",
      "domain_id": "bug",
      "domain_label": "Bug 域",
      "domain_description": "问题录入、定位、运行时诊断、修复建议",
      "domain_order": 3,
      "item_order": 2,
      "auto_trigger": "当 bug 描述缺少复现条件、环境信息、输入数据、报错日志、影响范围时自动触发。",
      "core_responsibility": "补齐定位所需基础信息。",
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
      "id": "bug-reproduction-rules",
      "name": "bug-reproduction-rules",
      "title": "bug-reproduction-rules",
      "status": "planned",
      "status_label": "规划中",
      "domain_id": "bug",
      "domain_label": "Bug 域",
      "domain_description": "问题录入、定位、运行时诊断、修复建议",
      "domain_order": 3,
      "item_order": 3,
      "auto_trigger": "当问题需要复现、构造步骤、确定触发条件、判断是否稳定发生时自动触发。",
      "core_responsibility": "输出复现步骤和复现结论。",
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
      "id": "bug-debug-log-rules",
      "name": "bug-debug-log-rules",
      "title": "bug-debug-log-rules",
      "status": "planned",
      "status_label": "规划中",
      "domain_id": "bug",
      "domain_label": "Bug 域",
      "domain_description": "问题录入、定位、运行时诊断、修复建议",
      "domain_order": 3,
      "item_order": 7,
      "auto_trigger": "当定位 bug 需要临时增加 debug 日志、关键变量输出、关键分支日志、上下游输入输出日志时自动触发。",
      "core_responsibility": "通过可回收的临时日志补充运行期证据。",
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
      "id": "bug-assertion-diagnostic-rules",
      "name": "bug-assertion-diagnostic-rules",
      "title": "bug-assertion-diagnostic-rules",
      "status": "planned",
      "status_label": "规划中",
      "domain_id": "bug",
      "domain_label": "Bug 域",
      "domain_description": "问题录入、定位、运行时诊断、修复建议",
      "domain_order": 3,
      "item_order": 8,
      "auto_trigger": "当怀疑状态异常、顺序错误、数据污染、不变量被破坏，且需要通过程序断言或诊断性检查快速暴露问题位置时自动触发。",
      "core_responsibility": "用断言和诊断检查缩小 bug 发生区间。",
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
      "id": "bug-regression-risk-rules",
      "name": "bug-regression-risk-rules",
      "title": "bug-regression-risk-rules",
      "status": "planned",
      "status_label": "规划中",
      "domain_id": "bug",
      "domain_label": "Bug 域",
      "domain_description": "问题录入、定位、运行时诊断、修复建议",
      "domain_order": 3,
      "item_order": 10,
      "auto_trigger": "当修复可能影响公共方法、共享模块、已有接口、数据库行为或兼容性时自动触发。",
      "core_responsibility": "识别回归风险。",
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
      "id": "bug-validation-rules",
      "name": "bug-validation-rules",
      "title": "bug-validation-rules",
      "status": "planned",
      "status_label": "规划中",
      "domain_id": "bug",
      "domain_label": "Bug 域",
      "domain_description": "问题录入、定位、运行时诊断、修复建议",
      "domain_order": 3,
      "item_order": 11,
      "auto_trigger": "当 bug 修复后需要验证是否修好、是否引入副作用、是否需要补回归测试时自动触发。",
      "core_responsibility": "负责修复后的验证闭环。",
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
      "title": "naming-rules",
      "status": "planned",
      "status_label": "规划中",
      "domain_id": "baseline",
      "domain_label": "编码基线域",
      "domain_description": "开始编码即并行生效的基础质量规则",
      "domain_order": 4,
      "item_order": 4,
      "auto_trigger": "当新增或修改类名、函数名、变量名、常量名、DTO、实体、字段映射名时自动触发。",
      "core_responsibility": "保证命名语义化。",
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
        "重点看它是否能并行生效，并且不抢位点域或审查域职责。"
      ]
    },
    {
      "id": "chinese-comment-rules",
      "name": "chinese-comment-rules",
      "title": "chinese-comment-rules",
      "status": "planned",
      "status_label": "规划中",
      "domain_id": "baseline",
      "domain_label": "编码基线域",
      "domain_description": "开始编码即并行生效的基础质量规则",
      "domain_order": 4,
      "item_order": 5,
      "auto_trigger": "当新增或修改中文注释、业务说明、中文文档注释时自动触发。",
      "core_responsibility": "统一中文表达习惯和注释语气。",
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
        "重点看它是否能并行生效，并且不抢位点域或审查域职责。"
      ]
    },
    {
      "id": "code-comment-rules",
      "name": "code-comment-rules",
      "title": "code-comment-rules",
      "status": "planned",
      "status_label": "规划中",
      "domain_id": "baseline",
      "domain_label": "编码基线域",
      "domain_description": "开始编码即并行生效的基础质量规则",
      "domain_order": 4,
      "item_order": 6,
      "auto_trigger": "当新增或修改函数注释、类注释、模块注释、步骤注释、代码块注释时自动触发。",
      "core_responsibility": "统一注释层级和颗粒度。",
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
        "重点看它是否能并行生效，并且不抢位点域或审查域职责。"
      ]
    },
    {
      "id": "config-change-rules",
      "name": "config-change-rules",
      "title": "配置变更规则",
      "status": "implemented",
      "status_label": "已实现",
      "domain_id": "location",
      "domain_label": "代码位点域",
      "domain_description": "按改动位置叠加触发的实现规则",
      "domain_order": 5,
      "item_order": 1,
      "auto_trigger": "当新增或修改 `.env`、`.env.example`、`application.yml`、`application.yaml`、`settings.py`、`config.ts`、`appsettings.json`、`values.yaml`、环境变量读取、默认值、配置注入、配置分层、特性开关、密钥占位时自动触发。负责统一配置来源、分层、默认值、敏感配置和密钥占位规则，避免把业务逻辑、危险默认值和秘密暴露混进配置变更；不要用它代替 auth-security-rules、request-header-rules、deployment 或发布规则。",
      "core_responsibility": "统一配置、密钥和默认值策略。",
      "skill_path": "config-change-rules/SKILL.md",
      "directory_path": "config-change-rules",
      "directory": "config-change-rules",
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
        "config-change-rules/references/config-boundaries-and-examples.md",
        "config-change-rules/references/config-layering-and-sources.md",
        "config-change-rules/references/defaults-and-secrets.md"
      ],
      "agents": [
        "config-change-rules/agents/openai.yaml"
      ],
      "has_license": false,
      "focus_points": [
        "优先检查 description 是否具体到触发信号，而不是只写抽象用途。",
        "检查 references 是否足以承接复杂场景，避免 SKILL.md 过厚或过空。",
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
      "auto_trigger": "当新增或修改包、目录、模块、分层结构、包名定义、文件归属或跨层引用关系时触发。负责统一代码包定义、目录分层、包职责、模块边界和依赖方向，尤其适用于 Go、Java、Node/Python 项目的结构决策；不要用它代替工具实现、接口规则或代码审查类 skill。",
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
      "auto_trigger": "当新增或修改表、字段、索引、唯一约束、外键、迁移脚本、DDL、实体结构、schema 定义时自动触发。负责统一数据库结构变更、迁移安全、兼容性和回滚边界，避免把查询实现、事务控制和业务逻辑混进结构变更；不要用它代替 database-query-rules、config-change-rules 或发布回滚规则。",
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
      "auto_trigger": "当新增或修改 controller、router、handler、路由声明、HTTP 方法、接口 CRUD 路径命名、接口入口职责或超时入口边界时触发。负责统一接口入口设计、路径命名和 HTTP 方法语义；不要用它代替请求参数、响应结构或错误处理规则。",
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
      "auto_trigger": "当新增或修改请求参数、DTO、query 参数、path 参数、body 结构、参数校验或请求模型时触发。负责统一请求结构、参数表达和基础校验边界；不要用它代替接口入口设计、响应结构或业务规则本身。",
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
      "auto_trigger": "当新增或修改返回体、响应包装器、分页结构、错误响应结构、兼容字段、版本字段或统一响应模型时触发。负责统一响应格式和兼容策略；不要用它代替错误处理流程、异常分类或接口入口职责规则。",
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
      "title": "请求头规则",
      "status": "implemented",
      "status_label": "已实现",
      "domain_id": "location",
      "domain_label": "代码位点域",
      "domain_description": "按改动位置叠加触发的实现规则",
      "domain_order": 5,
      "item_order": 9,
      "auto_trigger": "当新增或修改认证头、trace-id、span-id、租户头、幂等键、客户端上下文头、X-Forwarded-* 逻辑时自动触发。负责统一请求头分类、来源可信度、透传边界和消费规则，避免把请求参数、日志字段和安全策略混进 Header 约定；不要用它代替 api-request-rules、logging-trace-rules 或 auth-security-rules。",
      "core_responsibility": "统一请求头约定和透传规则。",
      "skill_path": "request-header-rules/SKILL.md",
      "directory_path": "request-header-rules",
      "directory": "request-header-rules",
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
        "request-header-rules/references/header-boundaries-and-examples.md",
        "request-header-rules/references/header-categories-and-trust.md",
        "request-header-rules/references/propagation-and-forwarding.md"
      ],
      "agents": [
        "request-header-rules/agents/openai.yaml"
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
      "id": "auth-security-rules",
      "name": "auth-security-rules",
      "title": "认证与安全规则",
      "status": "implemented",
      "status_label": "已实现",
      "domain_id": "location",
      "domain_label": "代码位点域",
      "domain_description": "按改动位置叠加触发的实现规则",
      "domain_order": 5,
      "item_order": 12,
      "auto_trigger": "当新增或修改认证、鉴权、登录、登出、会话、JWT、对象级授权、输入校验、敏感信息处理、上传下载安全、外部请求安全时自动触发。负责统一安全实现的默认基线，覆盖身份校验、权限校验、输入处理、敏感信息和高风险入口控制；不要用它代替 request-header-rules、api-request-rules、error-handling-rules 或纯日志 trace 规则。",
      "core_responsibility": "统一安全实现的默认基线。",
      "skill_path": "auth-security-rules/SKILL.md",
      "directory_path": "auth-security-rules",
      "directory": "auth-security-rules",
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
        "auth-security-rules/references/framework-seed-selection.md",
        "auth-security-rules/references/security-baseline.md",
        "auth-security-rules/references/security-boundaries.md"
      ],
      "agents": [
        "auth-security-rules/agents/openai.yaml"
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
      "title": "性能与缓存规则",
      "status": "implemented",
      "status_label": "已实现",
      "domain_id": "location",
      "domain_label": "代码位点域",
      "domain_description": "按改动位置叠加触发的实现规则",
      "domain_order": 5,
      "item_order": 14,
      "auto_trigger": "当新增或修改 SQL 性能、接口耗时、缓存读取写入、缓存 key、缓存失效、前端渲染热点、大列表、图表、虚拟滚动时自动触发。负责统一性能与缓存边界，区分必要优化与过度优化，避免把业务逻辑、schema 问题和缓存副作用伪装成性能改进；不要用它代替 database-query-rules、database-schema-rules 或前端组件结构规则。",
      "core_responsibility": "统一性能和缓存规则。",
      "skill_path": "performance-caching-rules/SKILL.md",
      "directory_path": "performance-caching-rules",
      "directory": "performance-caching-rules",
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
        "performance-caching-rules/references/cache-strategy-rules.md",
        "performance-caching-rules/references/performance-boundaries.md",
        "performance-caching-rules/references/performance-examples.md"
      ],
      "agents": [
        "performance-caching-rules/agents/openai.yaml"
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
      "title": "frontend-component-rules",
      "status": "planned",
      "status_label": "规划中",
      "domain_id": "location",
      "domain_label": "代码位点域",
      "domain_description": "按改动位置叠加触发的实现规则",
      "domain_order": 5,
      "item_order": 13,
      "auto_trigger": "当新增或修改 React、Vue、前端组件、页面、表单、状态流、客户端数据展示逻辑时自动触发。",
      "core_responsibility": "统一前端组件和页面工程规则。",
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
      "auto_trigger": "当功能代码已经完成、准备进入测试前验证时触发。负责检查实现是否符合编码规范、命名规范、注释规范、风格一致性和最小改动原则；不要用它代替语法检查、格式清理或代码归位审查规则。",
      "core_responsibility": "对刚完成的实现做一次测试前规范自审。",
      "skill_path": "implementation-review-rules/SKILL.md",
      "directory_path": "implementation-review-rules",
      "directory": "implementation-review-rules",
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
      "auto_trigger": "当新增或修改测试目录、测试文件、测试脚本、验证程序、fixture、mock 数据、测试说明文档落点时触发。负责统一测试资源根目录、任务目录和禁止散落规则；不要用它代替 test-naming-rules、test-program-rules、test-doc-rules、code-placement-review-rules 或功能验证规则。",
      "core_responsibility": "统一测试资源位置。",
      "skill_path": "test-location-rules/SKILL.md",
      "directory_path": "test-location-rules",
      "directory": "test-location-rules",
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
      "auto_trigger": "当创建或修改测试任务目录、测试文件、测试脚本、测试数据目录、fixture 目录、mock 目录时触发。负责统一测试目录与文件命名规范，保证名称可读、可检索、与业务目标一致；不要用它代替 test-location-rules、test-program-rules、test-doc-rules 或功能验证规则。",
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
      "auto_trigger": "当新增或修改测试程序、模拟程序、验证脚本、数据构造脚本、测试辅助代码时触发。负责统一测试程序职责划分、脚手架结构、辅助代码边界和复用方式，避免临时验证代码混入正式业务目录；不要用它代替 test-location-rules、test-naming-rules、test-doc-rules、bug-runtime-debug-rules 或功能验证规则。",
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
      "auto_trigger": "当新增或修改测试 README、验证说明、测试报告、覆盖说明、测试执行记录时触发。负责统一测试文档的最小结构、记录字段、归档方式和通过驳回标准，保证测试资产可追溯；不要用它代替 test-location-rules、test-program-rules、functional-validation-rules 或 test-regression-rules。",
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
      "auto_trigger": "当需要验证新功能、修改后的功能、接口行为、页面交互、输入输出结果是否满足当前需求、当前变更和验收标准时触发。负责界定本次功能验证范围、验证步骤、通过驳回标准和结论留痕；不要用它代替 test-strategy-rules、test-location-rules、integration-debugging-rules 或 test-regression-rules。",
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
      "auto_trigger": "当 Bug 修复、原有功能迭代、公共模块修改、共享逻辑调整、接口兼容性变化后准备执行测试时触发。负责判定回归范围、选择回归用例、验证兼容性影响并输出回归结论；不要用它代替 functional-validation-rules、test-strategy-rules、integration-debugging-rules 或测试资源管理类规则。",
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
      "title": "联调排障规则",
      "status": "implemented",
      "status_label": "已实现",
      "domain_id": "test",
      "domain_label": "测试域",
      "domain_description": "策略、资源、功能验证、联调、回归",
      "domain_order": 7,
      "item_order": 8,
      "auto_trigger": "当联调、排查接口不通、字段不一致、环境差异、trace 断链、测试环境问题时自动触发。负责统一跨系统联调、环境差异排查、链路证据记录和问题分流规则，避免把单点功能错误或单模块运行时 Bug 诊断误归到联调层；不要用它代替 functional-validation-rules、bug-runtime-debug-rules、request-header-rules 或 logging-trace-rules。",
      "core_responsibility": "统一联调和排障证据记录。",
      "skill_path": "integration-debugging-rules/SKILL.md",
      "directory_path": "integration-debugging-rules",
      "directory": "integration-debugging-rules",
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
        "integration-debugging-rules/references/env-diff-and-chain-diagnostics.md",
        "integration-debugging-rules/references/integration-boundaries-and-handoff.md",
        "integration-debugging-rules/references/integration-scope-and-evidence.md"
      ],
      "agents": [
        "integration-debugging-rules/agents/openai.yaml"
      ],
      "has_license": false,
      "focus_points": [
        "优先检查 description 是否具体到触发信号，而不是只写抽象用途。",
        "检查 references 是否足以承接复杂场景，避免 SKILL.md 过厚或过空。",
        "重点看测试策略、资源、功能验证、联调、回归是否已经拆开。"
      ]
    },
    {
      "id": "test-strategy-rules",
      "name": "test-strategy-rules",
      "title": "test-strategy-rules",
      "status": "planned",
      "status_label": "规划中",
      "domain_id": "test",
      "domain_label": "测试域",
      "domain_description": "策略、资源、功能验证、联调、回归",
      "domain_order": 7,
      "item_order": 1,
      "auto_trigger": "当功能实现和编码审查完成后，开始补测试、写验证脚本、做回归检查时自动触发。",
      "core_responsibility": "决定测试层级和覆盖重点。",
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
      "title": "git-collaboration-rules",
      "status": "planned",
      "status_label": "规划中",
      "domain_id": "delivery",
      "domain_label": "交付域",
      "domain_description": "Git 协作、评审、发布与交付说明",
      "domain_order": 8,
      "item_order": 3,
      "auto_trigger": "当创建提交、整理提交说明、准备 PR、合并前检查时自动触发。",
      "core_responsibility": "统一 Git 协作规则。",
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
      "id": "delivery-summary-rules",
      "name": "delivery-summary-rules",
      "title": "delivery-summary-rules",
      "status": "planned",
      "status_label": "规划中",
      "domain_id": "delivery",
      "domain_label": "交付域",
      "domain_description": "Git 协作、评审、发布与交付说明",
      "domain_order": 8,
      "item_order": 4,
      "auto_trigger": "当准备交付说明、变更说明、影响范围说明、风险说明时自动触发。",
      "core_responsibility": "统一交付文档结构。",
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
      "title": "Skill 体系演进规则",
      "status": "implemented",
      "status_label": "已实现",
      "domain_id": "evolution",
      "domain_label": "体系维护域",
      "domain_description": "维护 skill 体系自身的拆分、迁移与演进",
      "domain_order": 9,
      "item_order": 1,
      "auto_trigger": "当新增、修改、拆分、合并、迁移或退休团队内部 skill，或发现现有 skill 边界失衡、触发描述失真、references 结构失控时触发。负责维护 skill 体系自身的拆分与演进规则；不要用它代替业务 skill 编写业务细则。",
      "core_responsibility": "维护 skill 体系自身的拆分和演进规则。",
      "skill_path": "skill-evolution-rules/SKILL.md",
      "directory_path": "skill-evolution-rules",
      "directory": "skill-evolution-rules",
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
        "skill-evolution-rules/references/evolution-patterns.md",
        "skill-evolution-rules/references/migration-checklist.md",
        "skill-evolution-rules/references/split-merge-boundaries.md"
      ],
      "agents": [
        "skill-evolution-rules/agents/openai.yaml"
      ],
      "has_license": false,
      "focus_points": [
        "优先检查 description 是否具体到触发信号，而不是只写抽象用途。",
        "检查 references 是否足以承接复杂场景，避免 SKILL.md 过厚或过空。",
        "重点看新增、合并、迁移和退休 skill 的门槛是否足够明确。"
      ]
    },
    {
      "id": "frontend-skill",
      "name": "frontend-skill",
      "title": "前端界面设计种子 Skill",
      "status": "seed",
      "status_label": "扩展种子",
      "domain_id": "seed",
      "domain_label": "扩展种子",
      "domain_description": "已入库但未并入主规划的参考 skill",
      "domain_order": 10,
      "item_order": 1,
      "auto_trigger": "当任务要求产出有明显视觉表达的落地页、网站、应用界面、原型、演示页或游戏 UI 时使用。这个 skill 强调克制的版式、清晰的信息层级、统一的内容结构和有节制的动效，避免通用卡片堆砌、品牌感弱和界面噪音。",
      "core_responsibility": "当前已在仓库中，但尚未并入主规划域表。",
      "skill_path": "frontend-skill/SKILL.md",
      "directory_path": "frontend-skill",
      "directory": "frontend-skill",
      "sections": [
        "工作模型",
        "默认做法",
        "落地页",
        "应用界面",
        "图片使用",
        "文案",
        "产品型页面文案",
        "动效",
        "硬规则",
        "常见失败",
        "自检问题"
      ],
      "references": [],
      "agents": [
        "frontend-skill/agents/openai.yaml"
      ],
      "has_license": true,
      "focus_points": [
        "先决定它是并入主规划、保持外部种子，还是拆成多个更窄的内部 skill。",
        "如果准备纳入体系，先补上与主规划域的映射关系和落位说明。",
        "重点看这个种子是否真的能落入主规划，还是保持独立参考更合适。"
      ]
    },
    {
      "id": "security-best-practices",
      "name": "security-best-practices",
      "title": "安全最佳实践种子 Skill",
      "status": "seed",
      "status_label": "扩展种子",
      "domain_id": "seed",
      "domain_label": "扩展种子",
      "domain_description": "已入库但未并入主规划的参考 skill",
      "domain_order": 10,
      "item_order": 2,
      "auto_trigger": "当用户明确要求安全最佳实践建议、安全评审、安全报告，或需要生成安全默认代码时使用。适用于 python、javascript/typescript、go 相关项目；不要在普通调试、通用代码评审或非安全任务中触发。",
      "core_responsibility": "当前已在仓库中，但尚未并入主规划域表。",
      "skill_path": "security-best-practices/SKILL.md",
      "directory_path": "security-best-practices",
      "directory": "security-best-practices",
      "sections": [
        "概览",
        "使用流程",
        "参考文件选择规则",
        "工作模式",
        "报告要求",
        "修复原则",
        "通用安全原则"
      ],
      "references": [
        "security-best-practices/references/golang-general-backend-security.md",
        "security-best-practices/references/javascript-express-web-server-security.md",
        "security-best-practices/references/javascript-general-web-frontend-security.md",
        "security-best-practices/references/javascript-jquery-web-frontend-security.md",
        "security-best-practices/references/javascript-typescript-nextjs-web-server-security.md",
        "security-best-practices/references/javascript-typescript-react-web-frontend-security.md",
        "security-best-practices/references/javascript-typescript-vue-web-frontend-security.md",
        "security-best-practices/references/python-django-web-server-security.md",
        "security-best-practices/references/python-fastapi-web-server-security.md",
        "security-best-practices/references/python-flask-web-server-security.md"
      ],
      "agents": [
        "security-best-practices/agents/openai.yaml"
      ],
      "has_license": true,
      "focus_points": [
        "先决定它是并入主规划、保持外部种子，还是拆成多个更窄的内部 skill。",
        "如果准备纳入体系，先补上与主规划域的映射关系和落位说明。",
        "重点看这个种子是否真的能落入主规划，还是保持独立参考更合适。"
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
    }
  ],
  "recommendations": [
    "优先补齐需求域缺口，目前仍缺 4 个规划 skill，后续需求澄清和验收会继续压在总控层。",
    "Bug 域还缺 7 个环节，尤其是复现、范围界定、诊断日志和修复后验证，建议补完整闭环。",
    "测试域缺 1 个、交付域缺 4 个，建议先补 `test-strategy-rules` 和交付域三件套。",
    "把 `frontend-skill` 明确映射到规划中的 `frontend-component-rules`，避免前端规则长期处于体系外。",
    "评估 `security-best-practices` 与 `auth-security-rules` 的关系，决定保留为独立种子还是拆分吸收。"
  ]
};
