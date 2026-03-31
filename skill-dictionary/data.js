window.SKILL_DICTIONARY = {
  "generated_at": "2026-03-31 23:59:49",
  "repo_root": "C:\\Users\\Administrator\\.codex\\skills",
  "plan_doc": "编码skill.md",
  "plan_doc_name": "编码skill.md",
  "summary": {
    "planned_total": 57,
    "implemented_total": 57,
    "planned_missing": 0,
    "seed_total": 5,
    "doc_total": 2,
    "references_total": 199,
    "agents_total": 59
  },
  "downloaded_seeds": {
    "path": "downloaded-seeds",
    "exists": false,
    "entry_count": 0,
    "entries": []
  },
  "domains": [
    {
      "id": "orchestration",
      "label": "总控层",
      "description": "流程分流、冲突裁决、阶段阻断与全局基础约定",
      "order": 1,
      "implemented_count": 4,
      "planned_count": 0,
      "seed_count": 0,
      "total_count": 4,
      "items": [
        {
          "id": "team-development-rules",
          "name": "team-development-rules",
          "title": "团队研发总控规则",
          "status": "implemented",
          "status_label": "已实现",
          "domain_id": "orchestration",
          "domain_label": "总控层",
          "domain_description": "流程分流、冲突裁决、阶段阻断与全局基础约定",
          "domain_order": 1,
          "item_order": 1,
          "auto_trigger": "当任务阶段不明确、领域边界不清、多个 skill 同时触发、流程需要暂停/重启/继续/终止，或需要先判断应该进入历史回忆、需求、Bug、编码、测试还是交付处理时触发。负责阶段分析、路由分流、冲突裁决和流程阻断；不要在单一明确的 SQL、API、配置、测试、评审等任务中触发。",
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
            "重点看是否只做分流、阻断或全局基础约定，没有越权覆盖单域 skill。"
          ]
        },
        {
          "id": "artifact-storage-rules",
          "name": "artifact-storage-rules",
          "title": "研发产物存储规则",
          "status": "implemented",
          "status_label": "已实现",
          "domain_id": "orchestration",
          "domain_label": "总控层",
          "domain_description": "流程分流、冲突裁决、阶段阻断与全局基础约定",
          "domain_order": 1,
          "item_order": 2,
          "auto_trigger": "当需要定义、调整或解释项目中 `ment/`、`bug/`、`test/`、`doc/` 以及根目录 `项目设计.md` 等研发产物根目录、主入口文件、命名模板、同任务复用策略或跨域文档引用关系时自动触发。负责提供全局唯一的目录与命名单一真相源，并为需求、Bug、测试、记忆、项目设计和交付类 skill 提供统一引用基准；不要用它代替需求分析、Bug 定位、测试执行、生产代码存放决策或流程分流。",
          "core_responsibility": "作为跨域统一约定 skill，提供目录、命名和复用策略的单一真相源，供需求、Bug、测试、记忆、项目设计和交付类 skill 统一引用。",
          "skill_path": "artifact-storage-rules/SKILL.md",
          "directory_path": "artifact-storage-rules",
          "directory": "artifact-storage-rules",
          "sections": [
            "Skill 作用与适用场景",
            "测试目录复用优先级（写死边界）",
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
            "artifact-storage-rules/references/naming-templates.md",
            "artifact-storage-rules/references/path-map.yaml",
            "artifact-storage-rules/references/root-directories.md",
            "artifact-storage-rules/references/skill-integration.md",
            "artifact-storage-rules/references/update-policy.md"
          ],
          "agents": [
            "artifact-storage-rules/agents/openai.yaml"
          ],
          "has_license": false,
          "focus_points": [
            "优先检查 description 是否具体到触发信号，而不是只写抽象用途。",
            "检查 references 是否足以承接复杂场景，避免 SKILL.md 过厚或过空。",
            "重点看是否只做分流、阻断或全局基础约定，没有越权覆盖单域 skill。"
          ]
        },
        {
          "id": "project-design-doc-rules",
          "name": "project-design-doc-rules",
          "title": "项目设计文档规则",
          "status": "implemented",
          "status_label": "已实现",
          "domain_id": "orchestration",
          "domain_label": "总控层",
          "domain_description": "流程分流、冲突裁决、阶段阻断与全局基础约定",
          "domain_order": 1,
          "item_order": 3,
          "auto_trigger": "当用户要求分析整个项目、梳理项目架构/模块/目录/主链路、检查根目录 `项目设计.md` 及同类设计文档是否偏移、同步更新项目设计文档，或在完成全项目分析后为缺失项目补建根目录 `项目设计.md` 时自动触发。负责把根目录项目设计类文档作为弱参考源读取，按“代码与当前文档优先、设计文档低优先级”原则校验偏移，并统一同步到根目录 `项目设计.md`；不要用它代替 recent-context-bootstrap-rules 的轻量预热、artifact-storage-rules 的路径命名总规则、project-timeline-rules 的长期时间线，或 package-structure-rules / code-placement-review-rules 的代码归位判断。",
          "core_responsibility": "负责把根目录项目设计类文档当作弱参考源读取，按代码与当前文档优先原则判断偏移，并统一同步或补建根目录 `项目设计.md`。",
          "skill_path": "project-design-doc-rules/SKILL.md",
          "directory_path": "project-design-doc-rules",
          "directory": "project-design-doc-rules",
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
            "project-design-doc-rules/references/design-template.md",
            "project-design-doc-rules/references/discovery-and-priority.md",
            "project-design-doc-rules/references/sync-policy.md"
          ],
          "agents": [
            "project-design-doc-rules/agents/openai.yaml"
          ],
          "has_license": false,
          "focus_points": [
            "优先检查 description 是否具体到触发信号，而不是只写抽象用途。",
            "检查 references 是否足以承接复杂场景，避免 SKILL.md 过厚或过空。",
            "重点看是否只做分流、阻断或全局基础约定，没有越权覆盖单域 skill。"
          ]
        },
        {
          "id": "skill-evolution-rules",
          "name": "skill-evolution-rules",
          "title": "Skill 演进规则",
          "status": "implemented",
          "status_label": "已实现",
          "domain_id": "orchestration",
          "domain_label": "总控层",
          "domain_description": "流程分流、冲突裁决、阶段阻断与全局基础约定",
          "domain_order": 1,
          "item_order": 4,
          "auto_trigger": "当研发任务已经进入需求、Bug、编码、审查、测试或交付主流程，且当前已命中的 skill 在执行中暴露出触发不准、规则缺失、边界不清、references 不足、归档约定缺失或无法覆盖当前高频场景，继续推进只能依赖临时口头补充时触发。负责判断这是业务问题还是 skill 问题，明确应补哪个现有 skill、是否需要新增相邻 skill、给出最小完善建议，并在必要时先暂停当前任务；待 skill 更新并重新加载后，再回到原任务继续执行。不要用它代替需求补齐、Bug 定位或具体代码实现。",
          "core_responsibility": "负责判断这是业务问题还是 skill 问题，明确应补哪个现有 skill、是否需要新增相邻 skill、给出最小完善建议，并在必要时先暂停当前任务，待 skill 更新并重新加载后再继续。",
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
            "skill-evolution-rules/references/evolution-decision-matrix.md",
            "skill-evolution-rules/references/gap-signals.md",
            "skill-evolution-rules/references/improvement-output-template.md",
            "skill-evolution-rules/references/resume-workflow.md"
          ],
          "agents": [
            "skill-evolution-rules/agents/openai.yaml"
          ],
          "has_license": false,
          "focus_points": [
            "优先检查 description 是否具体到触发信号，而不是只写抽象用途。",
            "检查 references 是否足以承接复杂场景，避免 SKILL.md 过厚或过空。",
            "重点看是否只做分流、阻断或全局基础约定，没有越权覆盖单域 skill。"
          ]
        }
      ]
    },
    {
      "id": "memory",
      "label": "记忆域",
      "description": "新会话近期预热、跨会话历史检索、项目演进回顾、长期上下文补全",
      "order": 2,
      "implemented_count": 3,
      "planned_count": 0,
      "seed_count": 0,
      "total_count": 3,
      "items": [
        {
          "id": "recent-context-bootstrap-rules",
          "name": "recent-context-bootstrap-rules",
          "title": "新会话上下文预热规则",
          "status": "implemented",
          "status_label": "已实现",
          "domain_id": "memory",
          "domain_label": "记忆域",
          "domain_description": "新会话近期预热、跨会话历史检索、项目演进回顾、长期上下文补全",
          "domain_order": 2,
          "item_order": 1,
          "auto_trigger": "当当前会话刚开始、缺少历史上下文、用户直接提出与当前项目相关的需求、Bug、编码、测试或交付问题时自动触发。负责优先从 `artifact-storage-rules` 约定的近 3 天需求、测试、Bug、文档根目录和 git 提交中提取最近活动；如果当前任务涉及整项目分析、架构梳理或模块总览，也可额外读取根目录 `项目设计.md` 及其同类设计文档作为弱参考源，但不把它当成最新事实；如果部分目录不存在，则只使用存在的目录和 git 信息；不要把它代替 history-recall-rules 的深度历史回忆、project-timeline-rules 的长期时间线、project-design-doc-rules 的设计文档同步，或当前主域本身的分析执行。",
          "core_responsibility": "负责优先从 `artifact-storage-rules` 约定目录和最近 Git 提交中压缩前置上下文；如果当前任务涉及整项目分析，可额外弱读取根目录项目设计类文档，再把任务转交真正主域。",
          "skill_path": "recent-context-bootstrap-rules/SKILL.md",
          "directory_path": "recent-context-bootstrap-rules",
          "directory": "recent-context-bootstrap-rules",
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
            "recent-context-bootstrap-rules/references/bootstrap-sources.md",
            "recent-context-bootstrap-rules/references/boundary-rules.md",
            "recent-context-bootstrap-rules/references/output-format.md"
          ],
          "agents": [
            "recent-context-bootstrap-rules/agents/openai.yaml"
          ],
          "has_license": false,
          "focus_points": [
            "优先检查 description 是否具体到触发信号，而不是只写抽象用途。",
            "检查 references 是否足以承接复杂场景，避免 SKILL.md 过厚或过空。",
            "重点看它是否只补近期或历史上下文，不越权代替当前需求、Bug、编码或交付判断。"
          ]
        },
        {
          "id": "history-recall-rules",
          "name": "history-recall-rules",
          "title": "历史回忆规则",
          "status": "implemented",
          "status_label": "已实现",
          "domain_id": "memory",
          "domain_label": "记忆域",
          "domain_description": "新会话近期预热、跨会话历史检索、项目演进回顾、长期上下文补全",
          "domain_order": 2,
          "item_order": 2,
          "auto_trigger": "当用户明确询问“上次怎么做的”“之前有没有修过/做过/讨论过”“以前类似需求/类似 Bug/类似接口/类似表结构是怎么处理的”，或当前任务明显依赖过去会话结论时自动触发。负责优先从持久记忆后端检索历史方案、历史修复和历史决策；如果没有真实记忆后端，则降级为基于 `artifact-storage-rules` 约定目录、Git 和本地文档的历史回溯；不要把它代替 recent-context-bootstrap-rules 的新会话最近 3 天上下文预热，也不要用它代替当前需求澄清、当前 Bug 定位或当前实现验证。",
          "core_responsibility": "负责检索跨会话历史、历史方案和历史修复记录，补回长期上下文。",
          "skill_path": "history-recall-rules/SKILL.md",
          "directory_path": "history-recall-rules",
          "directory": "history-recall-rules",
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
            "history-recall-rules/references/backend-boundary.md",
            "history-recall-rules/references/local-fallback-recall.md",
            "history-recall-rules/references/persistent-search-workflow.md",
            "history-recall-rules/references/source-notes.md"
          ],
          "agents": [
            "history-recall-rules/agents/openai.yaml"
          ],
          "has_license": false,
          "focus_points": [
            "优先检查 description 是否具体到触发信号，而不是只写抽象用途。",
            "检查 references 是否足以承接复杂场景，避免 SKILL.md 过厚或过空。",
            "重点看它是否只补近期或历史上下文，不越权代替当前需求、Bug、编码或交付判断。"
          ]
        },
        {
          "id": "project-timeline-rules",
          "name": "project-timeline-rules",
          "title": "项目时间线规则",
          "status": "implemented",
          "status_label": "已实现",
          "domain_id": "memory",
          "domain_label": "记忆域",
          "domain_description": "新会话近期预热、跨会话历史检索、项目演进回顾、长期上下文补全",
          "domain_order": 2,
          "item_order": 3,
          "auto_trigger": "当用户要求生成项目开发历程、阶段总结、技术演进、关键决策回顾、项目时间线报告、完整历史分析或“这个项目一路是怎么走过来的”时自动触发。负责基于持久记忆后端或本地历史材料，按时间顺序组织项目演进、关键阶段、重大问题和技术决策；不要用它代替当前一次交付摘要、当前需求验收或当前 Bug 修复说明。",
          "core_responsibility": "负责按项目维度组织长期历史、输出时间线和演进报告。",
          "skill_path": "project-timeline-rules/SKILL.md",
          "directory_path": "project-timeline-rules",
          "directory": "project-timeline-rules",
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
            "project-timeline-rules/references/backend-timeline-workflow.md",
            "project-timeline-rules/references/local-material-timeline.md",
            "project-timeline-rules/references/source-notes.md",
            "project-timeline-rules/references/timeline-scope-boundary.md"
          ],
          "agents": [
            "project-timeline-rules/agents/openai.yaml"
          ],
          "has_license": false,
          "focus_points": [
            "优先检查 description 是否具体到触发信号，而不是只写抽象用途。",
            "检查 references 是否足以承接复杂场景，避免 SKILL.md 过厚或过空。",
            "重点看它是否只补近期或历史上下文，不越权代替当前需求、Bug、编码或交付判断。"
          ]
        }
      ]
    },
    {
      "id": "requirement",
      "label": "需求域",
      "description": "需求澄清、缺口识别、边界确认、验收前置",
      "order": 3,
      "implemented_count": 7,
      "planned_count": 0,
      "seed_count": 0,
      "total_count": 7,
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
          "domain_order": 3,
          "item_order": 1,
          "auto_trigger": "当用户提出新需求、新功能、新页面、新接口、新模块，且任务刚进入研发阶段、尚未进入实现或 Bug 定位时触发。支持从需求 URL、零散资料、物料和补充说明中整理需求，先结合当前项目上下文逐步澄清目标、约束和成功标准，对存在多个合理方向的需求先收敛方案，再补齐到可进入后续代码开发的程度，并将结果沉淀到 `artifact-storage-rules` 约定的需求文档根目录；它同时定义需求域统一文档入口，同一需求后续只能持续更新由 `artifact-storage-rules` 约定的同一份需求主文档；不要用它代替需求缺口、边界、拆分、变更或验收标准类 skill。",
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
          "domain_order": 3,
          "item_order": 2,
          "auto_trigger": "当需求描述不完整、缺少前提、缺少字段、缺少流程、缺少业务规则、缺少依赖条件、缺少成功标准、存在多种合理解释或关键方案尚未收敛时触发。负责识别需求缺口并在信息不足时阻断盲目编码推进，同时将缺口分析结果持续更新到 `requirement-intake-rules` 约定、且路径与命名由 `artifact-storage-rules` 统一定义的同一份需求主文档中；不要用它代替需求边界判断、需求变更判断或验收标准细化 skill。",
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
          "domain_order": 3,
          "item_order": 3,
          "auto_trigger": "当需求边界不清、影响范围不明、兼容性不明确、是否允许改旧逻辑不清楚，或需要区分当前需求、历史问题、需求变更和验收偏差时触发。负责明确改动边界和影响面，并将边界结论持续更新到 `requirement-intake-rules` 约定、且路径与命名由 `artifact-storage-rules` 统一定义的同一份需求主文档中；不要用它代替需求缺口识别或 Bug 根因定位 skill。",
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
          "domain_order": 3,
          "item_order": 4,
          "auto_trigger": "当需求较大、涉及多个模块、多个接口、多个页面、多个步骤、多个角色协作，或一次性覆盖多个独立子系统、多个产品子域、多个相对独立主线，无法作为单一实现单元稳定推进时触发。负责拆出任务边界、实施顺序和最小闭环，并将拆分结果持续更新到 `requirement-intake-rules` 约定、且路径与命名由 `artifact-storage-rules` 统一定义的同一份需求主文档中；不要用它代替需求接入、边界确认或项目排期管理。",
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
          "id": "implementation-plan-rules",
          "name": "implementation-plan-rules",
          "title": "实施计划拆解规则",
          "status": "implemented",
          "status_label": "已实现",
          "domain_id": "requirement",
          "domain_label": "需求域",
          "domain_description": "需求澄清、缺口识别、边界确认、验收前置",
          "domain_order": 3,
          "item_order": 5,
          "auto_trigger": "当需求、边界和验收标准已基本稳定，且正式编码前仍需要先把当前优先闭环的文件落点、模块职责、任务顺序、验证步骤和阶段收口拆清时触发。负责把已确认需求或已拆分出的当前优先子项转成可执行实施计划，并将计划单独保存到 `artifact-storage-rules` 约定的实施计划文档中；不要用它代替需求拆分、验收标准编写、实际编码或测试执行。",
          "core_responsibility": "把已确认需求转成可执行实施计划。",
          "skill_path": "implementation-plan-rules/SKILL.md",
          "directory_path": "implementation-plan-rules",
          "directory": "implementation-plan-rules",
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
            "implementation-plan-rules/references/plan-boundaries-and-examples.md",
            "implementation-plan-rules/references/plan-entry-checklist.md",
            "implementation-plan-rules/references/plan-review-checklist.md",
            "implementation-plan-rules/references/plan-structure-template.md",
            "implementation-plan-rules/references/source-notes.md",
            "implementation-plan-rules/references/task-granularity-and-order.md"
          ],
          "agents": [
            "implementation-plan-rules/agents/openai.yaml"
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
          "domain_order": 3,
          "item_order": 6,
          "auto_trigger": "当编码过程中需求被补充、修正、插入新条件、改变优先级、调整默认值或交付物形态时触发。负责识别变更类型、重算影响范围和决定是否需要回退前序结论，并将变更结果持续更新到 `requirement-intake-rules` 约定、且路径与命名由 `artifact-storage-rules` 统一定义的同一份需求主文档中；不要把历史缺陷误当成需求变更。",
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
          "domain_order": 3,
          "item_order": 7,
          "auto_trigger": "当任务准备进入实现前确认，或交付前需要把“做到什么算完成”写成可验证、可测试、可复核的标准时触发。负责细化成功条件、异常条件、边界条件和不在范围项，并将验收标准单独保存到 `artifact-storage-rules` 约定的验收文档中；不要用它代替功能验证或回归验证。",
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
      "order": 4,
      "implemented_count": 10,
      "planned_count": 0,
      "seed_count": 0,
      "total_count": 10,
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
          "domain_order": 4,
          "item_order": 1,
          "auto_trigger": "当用户描述报错、异常行为、结果不符、线上问题、偶发问题、接口异常、页面异常、数据错误或性能异常时触发。负责把 Bug 描述标准化，整理现象、影响范围、环境条件、期望结果和实际结果，并统一建立符合 `artifact-storage-rules` 约定的 Bug 根目录记录；不要用它代替根因定位、运行时调试或修复方案制定 skill。",
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
          "domain_order": 4,
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
          "domain_order": 4,
          "item_order": 3,
          "auto_trigger": "当问题需要构造步骤、确定触发条件、判断是否稳定发生、确认出现频率或复现环境时触发。负责输出复现路径、稳定性判断、符合 `artifact-storage-rules` 约定的 Bug 根目录记录和无法复现时的结论处理；不要用它代替根因分析。",
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
          "domain_order": 4,
          "item_order": 4,
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
          "domain_order": 4,
          "item_order": 5,
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
          "domain_order": 4,
          "item_order": 6,
          "auto_trigger": "当定位 Bug 需要临时增加 debug 日志、关键变量输出、关键分支日志、上下游输入输出日志或时间线日志来补充运行时证据时触发。负责日志落点、日志粒度、Bug 根目录记录、可回收性和清理要求；临时诊断日志也必须使用项目日志框架且不得使用控制台打印；不要把临时诊断日志混成正式日志策略。",
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
          "domain_order": 4,
          "item_order": 7,
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
          "domain_order": 4,
          "item_order": 8,
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
          "domain_order": 4,
          "item_order": 9,
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
          "domain_order": 4,
          "item_order": 10,
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
      "order": 5,
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
          "domain_order": 5,
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
          "domain_order": 5,
          "item_order": 2,
          "auto_trigger": "当新增或修改业务代码、工具代码、服务代码、脚本代码或 Bug 修复逻辑时触发。负责约束函数结构、逻辑顺序、复杂度和可维护性，并在功能不变前提下优先让最近改动代码表达更清楚、更直接；当单文件达到 500 行及以上且仍持续新增功能时，必须触发拆分评估；结构调整落地后必须联动 `code-comment-rules` 完成改动位点注释补齐；Go 接入第三方 API 时默认使用结构体解析响应，禁止长期使用 map + key 硬编码解析；不要用它代替最小改动、风格一致性、注释规则或代码归位规则。",
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
            "需要避免",
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
          "domain_order": 5,
          "item_order": 3,
          "auto_trigger": "当新增或修改任意代码文件、脚本文件、配置型代码或测试代码时触发。负责跟随项目现有写法，避免局部风格跳变和个人偏好入侵；不要用它代替最小改动、可读性、注释规范或代码归位规则。",
          "core_responsibility": "跟随项目现有风格，不引入风格跳变。",
          "skill_path": "code-style-consistency-rules/SKILL.md",
          "directory_path": "code-style-consistency-rules",
          "directory": "code-style-consistency-rules",
          "sections": [
            "Skill 作用与适用场景",
            "Go 路由风格约定",
            "Go 局部变量声明风格约定",
            "Go 函数签名风格约定",
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
          "domain_order": 5,
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
          "domain_order": 5,
          "item_order": 5,
          "auto_trigger": "当新增或修改代码注释、步骤说明、复杂逻辑解释、临时诊断说明或测试说明，且团队要求注释必须使用中文（除标准协议字段/第三方固定错误原文外）时触发。负责中文注释的语言选择、表达方式和禁忌；不要把它代替注释位置与颗粒度规则。",
          "core_responsibility": "统一中文表达习惯和注释语气。",
          "skill_path": "chinese-comment-rules/SKILL.md",
          "directory_path": "chinese-comment-rules",
          "directory": "chinese-comment-rules",
          "sections": [
            "Skill 作用与适用场景",
            "强制规则：注释语言",
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
          "domain_order": 5,
          "item_order": 6,
          "auto_trigger": "当新增或修改任意代码，或需要判断代码是否应该加注释、注释放在哪里、写到什么颗粒度、如何与实现同步维护时触发。负责注释必要性、位置选择、颗粒度控制、步骤注释、字段注释、函数方法参数返回注释、函数方法修改时间标注和过期注释治理；必须对本轮改动位点执行注释补齐检查；每个函数方法的修改都必须补充最近修改时间（北京时间：yyyy-MM-DD HH:mm:ss），并补充 `[参数]` / `[返回]` 简单注释；Swagger/OpenAPI 接口文档注解/注释不由本 skill 兜底，应转交 api-swagger-rules；不要把它代替中文语言表达规则。",
          "core_responsibility": "统一注释层级和颗粒度，并拦截改动位点漏注释。",
          "skill_path": "code-comment-rules/SKILL.md",
          "directory_path": "code-comment-rules",
          "directory": "code-comment-rules",
          "sections": [
            "Skill 作用与适用场景",
            "强制门禁：改动位点注释补齐",
            "强制规则：步骤注释位置",
            "强制规则：注释语言",
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
      "order": 6,
      "implemented_count": 13,
      "planned_count": 0,
      "seed_count": 0,
      "total_count": 13,
      "items": [
        {
          "id": "package-structure-rules",
          "name": "package-structure-rules",
          "title": "包结构与分层规则",
          "status": "implemented",
          "status_label": "已实现",
          "domain_id": "location",
          "domain_label": "代码位点域",
          "domain_description": "按改动位置叠加触发的实现规则",
          "domain_order": 6,
          "item_order": 1,
          "auto_trigger": "用于判断新增或修改包、目录、模块、`main.go` 启动入口、`internal` 私有代码、`utils` / `common` / `global` / `middleware` / `crontask` / `async` 等支撑目录，以及 `router` / `controller` / `service` / `repository` / `model` / `entity` 等业务目录的落点、职责和依赖方向。适用于 Go、Java、Node/Python 项目的结构决策，尤其适合判断单二进制 Go 服务中哪些代码必须留在 `internal/`，以及哪些入口层目录必须保持根级；`utils` / `common` / `global` / `middleware` 根目录默认只放子包子目录，`internal/service` 也默认先拆业务子目录再落实现文件；Go 场景下请求/响应/第三方结果等结构体默认落在 `internal/entity`，不应散落在 `internal/service` 实现文件；当单文件达到 500 行及以上且仍在扩展时，需评估按功能拆文件并在必要时拆子目录/子包；不要用它代替工具实现、接口设计或代码审查类 skill。",
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
          "domain_order": 6,
          "item_order": 2,
          "auto_trigger": "当新增或修改工具类、通用方法、公共组件、工具函数、通用常量或复用代码时触发。负责统一公共工具代码的判定标准、存放位置、调用方式和边界；`utils` / `common` / `global` / `middleware` 这类通用包根目录应先按职责拆子目录，再在子目录放实现文件，避免循环依赖和命名冲突；不要用它代替业务逻辑抽象、包结构规则或具体实现细则。",
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
          "domain_order": 6,
          "item_order": 3,
          "auto_trigger": "当新增或修改表、字段、索引、唯一约束、外键、迁移脚本、DDL、实体结构、schema 定义时自动触发。负责统一数据库结构变更、迁移安全、兼容性和回滚边界；数据库的字段必须要定义数据类型、默认值、是否需要索引、字段 CHARSET=utf8mb4、ENGINE=InnoDB、注释说明等写清楚，不要遗漏；所有金额相关的要强制使用字符串，避免任何出现精度问题的情况；所有表必须包含 created_at 和 updated_at 字段，由数据库自动管理；必须冗余一个毫秒级时间戳的创建时间，避免数据库的时区问题影响不同的时间格式；所有表必须包含逻辑删除字段，1 的状态标识删除，不是 1 代表正常非删除状态，默认 0=非删除；否则会导致自动创建表出现不可控的因素；避免把查询实现、事务控制和业务逻辑混进结构变更；不要用它代替 database-query-rules、项目配置约束或发布回滚流程。",
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
          "domain_order": 6,
          "item_order": 4,
          "auto_trigger": "当新增或修改 SQL、Repository、DAO、Mapper、QueryBuilder、事务、锁、批量 CRUD、分页查询时自动触发。负责统一数据库访问实现、查询性能、事务与锁边界，避免把 schema 设计、缓存策略和业务逻辑混进数据访问层；不要用它代替 database-schema-rules、缓存策略约束或业务规则本身。",
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
          "domain_order": 6,
          "item_order": 5,
          "auto_trigger": "当新增或修改 controller、router、路由声明、HTTP 方法、接口路径命名、接口入口职责或超时入口边界时触发。负责统一接口入口设计、路径命名和强制使用 POST 方法，并约束 Go 路由注册代码块写法；必须以 package-structure-rules 为基准，不使用 handler 包名；若本次改动影响 Swagger/OpenAPI 的路径、tag、摘要或文档分组，应与 api-swagger-rules 同步生效；不要用它代替请求参数、响应结构或错误处理规则。",
          "core_responsibility": "统一接口入口设计。",
          "skill_path": "api-endpoint-rules/SKILL.md",
          "directory_path": "api-endpoint-rules",
          "directory": "api-endpoint-rules",
          "sections": [
            "Skill 作用与适用场景",
            "强制规则：Go 路由注册写法（internal/router）",
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
          "domain_order": 6,
          "item_order": 6,
          "auto_trigger": "当新增或修改请求参数、DTO、body 结构、参数校验或请求模型时触发。负责统一请求结构、参数表达和基础校验边界；必须以 api-endpoint-rules 为基准，只使用 POST 请求，所有参数通过 JSON body 传递；若本次改动影响 Swagger/OpenAPI 请求模型、字段说明或示例，应与 api-swagger-rules 同步生效；不要用它代替接口入口设计、响应结构或业务规则本身。",
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
          "domain_order": 6,
          "item_order": 7,
          "auto_trigger": "当新增或修改返回体、响应包装器、分页结构、错误响应结构、兼容字段、版本字段或统一响应模型时触发。负责统一响应格式和兼容策略；成功响应和错误响应都必须包含状态码、状态、消息、数据四个字段；若本次改动影响 Swagger/OpenAPI 成功响应、错误响应或分页文档，应与 api-swagger-rules 同步生效；不要用它代替错误处理流程、异常分类或接口入口职责规则。",
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
          "id": "api-swagger-rules",
          "name": "api-swagger-rules",
          "title": "Swagger / OpenAPI 规则",
          "status": "implemented",
          "status_label": "已实现",
          "domain_id": "location",
          "domain_label": "代码位点域",
          "domain_description": "按改动位置叠加触发的实现规则",
          "domain_order": 6,
          "item_order": 8,
          "auto_trigger": "当新增或修改后端 HTTP API、Swagger/OpenAPI 框架接入、接口文档注解/注释、Swagger 调试入口、接口分组标签、文档暴露路径或 Swagger 环境开关时触发。负责统一 Swagger/OpenAPI 框架选型边界、接口文档最小必填项、请求/响应同步、调试可用性和暴露安全规则；对存在 HTTP API 且需要联调/调试的后端项目，默认要求使用统一的 Swagger/OpenAPI 方案；不要用它代替 api-endpoint-rules、api-request-rules、api-response-rules、普通业务注释规则或功能验证。",
          "core_responsibility": "统一 Swagger/OpenAPI 接入、接口文档同步和调试入口暴露规则。",
          "skill_path": "api-swagger-rules/SKILL.md",
          "directory_path": "api-swagger-rules",
          "directory": "api-swagger-rules",
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
            "api-swagger-rules/references/baseline-and-scope.md",
            "api-swagger-rules/references/exposure-and-security.md",
            "api-swagger-rules/references/sync-and-annotation-rules.md"
          ],
          "agents": [
            "api-swagger-rules/agents/openai.yaml"
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
          "domain_order": 6,
          "item_order": 9,
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
          "domain_order": 6,
          "item_order": 10,
          "auto_trigger": "当新增或修改日志、logger、trace、span、审计日志、脱敏字段、排障字段、日志配置文件或链路透传逻辑时触发。负责统一日志与链路追踪规则，后端日志必须使用项目日志框架且不得使用控制台打印，并通过配置文件管理日志参数；日志初始化必须在 LoadConfig 之后且仅初始化一次，禁止空配置预初始化；不要用它代替错误处理、响应结构或长期监控告警策略。",
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
            "logging-trace-rules/references/backend-framework-and-config.md",
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
          "id": "frontend-design",
          "name": "frontend-design",
          "title": "frontend-design",
          "status": "implemented",
          "status_label": "已实现",
          "domain_id": "location",
          "domain_label": "代码位点域",
          "domain_description": "按改动位置叠加触发的实现规则",
          "domain_order": 6,
          "item_order": 11,
          "auto_trigger": "创建具有鲜明风格、达到生产级质量的高品质前端界面。当用户要求构建 Web 组件、页面或前端应用时使用这个 skill。它会生成有创意、打磨精细的代码，并避免出现千篇一律的 AI 模板化审美。",
          "core_responsibility": "生成具有鲜明风格、生产级质量的前端界面，并在与内部前端规则冲突时优先作为主导 skill。",
          "skill_path": "frontend-design/SKILL.md",
          "directory_path": "frontend-design",
          "directory": "frontend-design",
          "sections": [
            "设计思考",
            "前端审美指导"
          ],
          "references": [],
          "agents": [],
          "has_license": false,
          "focus_points": [
            "优先检查 description 是否具体到触发信号，而不是只写抽象用途。",
            "检查 references 是否足以承接复杂场景，避免 SKILL.md 过厚或过空。",
            "重点看主位点与横切位点是否可并行叠加，而不是互相覆盖。",
            "当前没有 references，可考虑补最小示例或边界文档以降低后续维护成本。"
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
          "domain_order": 6,
          "item_order": 12,
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
          "domain_order": 6,
          "item_order": 13,
          "auto_trigger": "当新增或修改前端页面、页面布局、主题样式、配色、字体、图标、卡片、弹窗、表单、表格、图表、导航、空状态、动画、响应式样式、暗黑模式、设计 token、Tailwind 类名、CSS/SCSS/LESS、`.tsx`/`.jsx`/`.vue`/`.html` 中影响界面视觉和交互体验的代码时自动触发，尤其适用于首页、营销页、品牌展示页、数据面板和需要明确设计方向的前端界面。负责页面视觉方向、信息层级、交互反馈、可访问性、响应式适配和交付前 UI 自审；内置合并后的 UI/UX 设计种子数据与搜索脚本，可在风格不明时辅助定方向；不要用它代替纯组件工程拆分、状态管理、接口接线或后端规则。",
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
            "frontend-ui-visual-rules/references/aesthetic-direction-rules.md",
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
          "has_license": true,
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
      "order": 7,
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
          "domain_order": 7,
          "item_order": 1,
          "auto_trigger": "当功能代码已经完成、准备进入测试前验证时触发。负责检查实现是否符合可读性优先、单一职责、命名语义化、注释完整、错误处理明确、日志可追溯、依赖使用审慎、魔法值治理、冗余逻辑清理和编码规范等实现质量要求，并在功能不变前提下检查最近改动代码是否还存在可直接收口的表达层冗余；必须核验本轮改动是否完成 `code-comment-rules` 的改动位点注释补齐；必须识别 500 行及以上且持续膨胀的文件并要求拆分或给出拆分方案；Go 场景下还需在实现自审阶段扫描 `test/` 外 `*_test.go` 禁放问题，以及本轮改动是否把业务实现直接落在 `internal/service/*.go` 根目录文件，是否把请求/响应/第三方结果结构体散落在 `internal/service` 实现文件，是否在函数/方法内使用 `var (...)` 分组声明局部变量，是否把多参数函数签名直接写成多行参数列表，是否把第三方 API 响应长期用 `map[string]any` + key 硬编码解析；若本轮改动涉及后端 HTTP API，还必须检查 Swagger/OpenAPI 是否同步更新；不要用它代替语法检查、格式化执行、目录归位审查或功能验证规则。",
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
          "domain_order": 7,
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
          "domain_order": 7,
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
          "domain_order": 7,
          "item_order": 4,
          "auto_trigger": "当新增文件、移动文件、扩展模块、跨层调用、工具类落点或目录归属可能不合理时，在进入测试前触发。负责检查代码存放位置、模块归属、层级边界和依赖方向是否合理；Go 项目中还需检查 `*_test.go` 是否误落在 `test/` 之外，并检查 `internal/service` 是否散落请求/响应等结构体定义；对 500 行及以上且持续膨胀的文件需追加拆分审查；不要用它代替编码前的包结构决策规则。",
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
      "description": "策略、资源、功能验证、浏览器联动与回归",
      "order": 8,
      "implemented_count": 8,
      "planned_count": 0,
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
          "domain_description": "策略、资源、功能验证、浏览器联动与回归",
          "domain_order": 8,
          "item_order": 1,
          "auto_trigger": "当准备进入测试阶段，需要确定测什么、先测什么、测到什么程度、哪些路径必须覆盖、哪些风险只能记录待补测时触发。负责测试优先级、测试类型组合、覆盖范围和资源收口；必须以 `artifact-storage-rules` 与 `test-location-rules` 为基准，把策略摘要统一记录到中央约定的测试任务主说明 `README.md` 中，并在需要拆成多轮独立测试时给出多个时间戳根目录方案；不要用它代替具体测试资源管理或验证执行 skill。",
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
          "domain_description": "策略、资源、功能验证、浏览器联动与回归",
          "domain_order": 8,
          "item_order": 2,
          "auto_trigger": "当新增或修改测试目录、测试文件、测试脚本、验证程序、fixture、mock 数据、测试说明文档落点时触发。负责在 `artifact-storage-rules` 的统一约定下管理测试资源根目录、时间戳任务根目录、中文说明目录、真实代码路径镜像目录和禁止散落规则；尤其要避免把中文路径放进会被 Go 工具链编译的测试包目录，并强制 Go 源码目录禁止落地 `*_test.go`（白盒诉求必须通过可外部测试 seam 解决）。不要用它代替 test-naming-rules、test-program-rules、test-doc-rules、code-placement-review-rules 或功能验证规则。",
          "core_responsibility": "统一测试资源位置。",
          "skill_path": "test-location-rules/SKILL.md",
          "directory_path": "test-location-rules",
          "directory": "test-location-rules",
          "sections": [
            "铁律：所有测试资产必须统一在 `artifact-storage-rules` 定义的测试根目录下",
            "Go 冲突决策分支：白盒同包诉求与禁放规则",
            "新基线：时间戳根目录 + 中文说明目录 + 真实代码路径镜像",
            "硬阻断规则：新测试任务必须使用当天时间戳目录",
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
          "domain_description": "策略、资源、功能验证、浏览器联动与回归",
          "domain_order": 8,
          "item_order": 3,
          "auto_trigger": "当创建或修改测试时间戳根目录、中文说明目录、测试文件、测试脚本、测试数据目录、fixture 目录、mock 目录时触发。负责统一测试目录与文件命名规范，保证名称可读、可检索、与业务目标一致；必须以 `artifact-storage-rules` 与 `test-location-rules` 为基础，遵循中央约定的时间戳根目录、中文说明目录和真实代码路径镜像目录命名规则；尤其要避免中文进入会被 Go 工具链编译的路径。不要用它代替 test-location-rules、test-program-rules、test-doc-rules 或功能验证规则。",
          "core_responsibility": "统一测试目录和文件命名。",
          "skill_path": "test-naming-rules/SKILL.md",
          "directory_path": "test-naming-rules",
          "directory": "test-naming-rules",
          "sections": [
            "命名一致性硬规则（时间戳目录）",
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
          "domain_description": "策略、资源、功能验证、浏览器联动与回归",
          "domain_order": 8,
          "item_order": 4,
          "auto_trigger": "当新增或修改测试程序、模拟程序、验证脚本、数据构造脚本、测试辅助代码时触发。负责统一测试程序职责拆分、辅助代码边界和长期保留策略；必须以 `artifact-storage-rules` 与 `test-location-rules` 为基准，把真实测试代码、脚本、mock、fixture 和执行产物统一落在中央约定的测试时间戳根目录下的 ASCII 真实代码路径镜像目录中，并避免中文进入会被 Go 工具链编译的路径；测试脚本执行时必须向控制台输出关键过程日志，便于观察执行进度与定位失败步骤；Go 场景下白盒/黑盒/集成测试都遵循同一落点规则，源码目录禁止 `*_test.go`，白盒诉求通过 seam 解决；第三方 API 文档缺失响应模型时，必须先用测试脚本探测真实响应，再反推结构体定义；不要用它代替 test-location-rules、test-naming-rules、test-doc-rules、bug-runtime-debug-rules 或功能验证规则。",
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
          "domain_description": "策略、资源、功能验证、浏览器联动与回归",
          "domain_order": 8,
          "item_order": 5,
          "auto_trigger": "当新增或修改测试 README、验证说明、测试报告、覆盖说明、测试执行记录时触发。负责统一测试文档的最小结构、记录字段、主文档入口和归档方式；必须以 `artifact-storage-rules` 与 `test-location-rules` 为基准，使用中央约定的测试任务主说明 `README.md` 作为中文主说明入口，并把额外文档放到同一时间戳根目录下的 ASCII 真实代码路径镜像目录中；不要用它代替 test-location-rules、test-program-rules、functional-validation-rules 或 test-regression-rules。",
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
          "id": "agent-browser",
          "name": "agent-browser",
          "title": "使用 agent-browser 进行浏览器自动化",
          "status": "implemented",
          "status_label": "已实现",
          "domain_id": "test",
          "domain_label": "测试域",
          "domain_description": "策略、资源、功能验证、浏览器联动与回归",
          "domain_order": 8,
          "item_order": 6,
          "auto_trigger": "面向 AI 代理的浏览器自动化 CLI。当用户需要与网站交互时使用，包括打开页面、填写表单、点击按钮、截图、提取数据、测试 Web 应用，或执行任何浏览器自动化任务。典型触发语句包括“打开一个网站”“填写表单”“点击按钮”“截个图”“抓取页面数据”“测试这个 Web 应用”“登录某个网站”“自动化浏览器操作”，以及任何需要通过程序控制浏览器完成的任务。",
          "core_responsibility": "统一浏览器自动化测试与页面交互执行。",
          "skill_path": "agent-browser/SKILL.md",
          "directory_path": "agent-browser",
          "directory": "agent-browser",
          "sections": [
            "核心工作流",
            "命令链式执行",
            "处理认证",
            "常用命令",
            "Streaming",
            "Batch 批量执行",
            "常见模式",
            "安全",
            "Diff（验证变化）",
            "超时与慢页面",
            "JavaScript 对话框（alert / confirm / prompt）",
            "Session 管理与清理",
            "Ref 生命周期（重要）",
            "带标注的截图（Vision 模式）",
            "语义定位器（Refs 的替代方案）",
            "JavaScript 求值（eval）",
            "配置文件",
            "深入文档",
            "浏览器引擎选择",
            "观测面板（Observability Dashboard）",
            "可直接使用的模板"
          ],
          "references": [
            "agent-browser/references/authentication.md",
            "agent-browser/references/commands.md",
            "agent-browser/references/profiling.md",
            "agent-browser/references/proxy-support.md",
            "agent-browser/references/session-management.md",
            "agent-browser/references/snapshot-refs.md",
            "agent-browser/references/video-recording.md"
          ],
          "agents": [],
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
          "domain_description": "策略、资源、功能验证、浏览器联动与回归",
          "domain_order": 8,
          "item_order": 7,
          "auto_trigger": "当需要验证新功能、修改后的功能、接口行为、页面交互、输入输出结果是否满足当前需求、当前变更和验收标准时触发。负责界定本次功能验证范围、验证步骤、通过驳回标准和结论留痕；必须以 `artifact-storage-rules` 与 `test-location-rules` 为基准，把功能验证结论写回中央约定的测试任务主说明 `README.md`，并把详细执行证据放到同一时间戳根目录下的 ASCII 真实代码路径镜像目录中；不要用它代替 test-strategy-rules、test-location-rules 或 test-regression-rules。",
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
          "domain_description": "策略、资源、功能验证、浏览器联动与回归",
          "domain_order": 8,
          "item_order": 8,
          "auto_trigger": "当 Bug 修复、原有功能迭代、公共模块修改、共享逻辑调整、接口兼容性变化后准备执行测试时触发。负责判定回归范围、选择回归用例、验证兼容性影响并输出回归结论；必须以 `artifact-storage-rules` 与 `test-location-rules` 为基准，把回归结论统一写回中央约定的测试任务主说明 `README.md`，并把详细回归案例、执行证据和补充说明放到同一时间戳根目录下的 ASCII 真实代码路径镜像目录中；不要用它代替 functional-validation-rules、test-strategy-rules 或测试资源管理类规则。",
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
        }
      ]
    },
    {
      "id": "delivery",
      "label": "交付域",
      "description": "Git 协作与交付说明",
      "order": 9,
      "implemented_count": 2,
      "planned_count": 0,
      "seed_count": 0,
      "total_count": 2,
      "items": [
        {
          "id": "git-collaboration-rules",
          "name": "git-collaboration-rules",
          "title": "Git 协作规则",
          "status": "implemented",
          "status_label": "已实现",
          "domain_id": "delivery",
          "domain_label": "交付域",
          "domain_description": "Git 协作与交付说明",
          "domain_order": 9,
          "item_order": 1,
          "auto_trigger": "当准备整理提交、拆提交粒度、同步分支、处理协作变更、准备 PR 或合并前收口时触发。负责提交粒度、提交说明、分支同步、协作边界和 PR 整理；提交代码时必须分析未提交的代码，如果可以分成不同的业务修改，就用多次不同的 git 提交；git 提交消息必须遵循 feat/fix 等格式，并且在 Windows/PowerShell 下提交说明必须使用真实换行（禁止把 `\\n` 当文本）；git 提交前必须先在项目根目录 README.md 追加本次改动日志，格式为时间 + 提交标题，且 README.md 改动日志必须保持按时间正序排列；Go 项目提交前还必须扫描 `test/` 外 `*_test.go` 并阻断违规提交，同时阻断本次提交中直接落在 `internal/service/*.go` 根目录的业务实现文件；不要把它代替代码评审或发布上线规则。",
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
            "重点看 Git 协作与交付说明是否已分层收口，并且不越界替代测试或发布流程。"
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
          "domain_description": "Git 协作与交付说明",
          "domain_order": 9,
          "item_order": 2,
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
            "重点看 Git 协作与交付说明是否已分层收口，并且不越界替代测试或发布流程。"
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
      "seed_count": 5,
      "total_count": 5,
      "items": [
        {
          "id": "\"doc\"",
          "name": "\"doc\"",
          "title": "DOCX Skill",
          "status": "seed",
          "status_label": "扩展种子",
          "domain_id": "seed",
          "domain_label": "扩展种子",
          "domain_description": "已入库但未并入主规划的参考 skill",
          "domain_order": 10,
          "item_order": 1,
          "auto_trigger": "\"Use when the task involves reading, creating, or editing `.docx` documents, especially when formatting or layout fidelity matters; prefer `python-docx` plus the bundled `scripts/render_docx.py` for visual checks.\"",
          "core_responsibility": "当前已在仓库中，但尚未并入主规划域表。",
          "skill_path": "doc/SKILL.md",
          "directory_path": "doc",
          "directory": "doc",
          "sections": [
            "When to use",
            "Workflow",
            "Temp and output conventions",
            "Dependencies (install if missing)",
            "Environment",
            "Rendering commands",
            "Quality expectations",
            "Final checks"
          ],
          "references": [],
          "agents": [
            "doc/agents/openai.yaml"
          ],
          "has_license": true,
          "focus_points": [
            "先决定它是并入主规划、保持外部种子，还是拆成多个更窄的内部 skill。",
            "如果准备纳入体系，先补上与主规划域的映射关系和落位说明。",
            "重点看这个种子是否真的能落入主规划，还是保持独立参考更合适。"
          ]
        },
        {
          "id": "\"pdf\"",
          "name": "\"pdf\"",
          "title": "PDF Skill",
          "status": "seed",
          "status_label": "扩展种子",
          "domain_id": "seed",
          "domain_label": "扩展种子",
          "domain_description": "已入库但未并入主规划的参考 skill",
          "domain_order": 10,
          "item_order": 2,
          "auto_trigger": "\"Use when tasks involve reading, creating, or reviewing PDF files where rendering and layout matter; prefer visual checks by rendering pages (Poppler) and use Python tools such as `reportlab`, `pdfplumber`, and `pypdf` for generation and extraction.\"",
          "core_responsibility": "当前已在仓库中，但尚未并入主规划域表。",
          "skill_path": "pdf/SKILL.md",
          "directory_path": "pdf",
          "directory": "pdf",
          "sections": [
            "When to use",
            "Workflow",
            "Temp and output conventions",
            "Dependencies (install if missing)",
            "Environment",
            "Rendering command",
            "Quality expectations",
            "Final checks"
          ],
          "references": [],
          "agents": [
            "pdf/agents/openai.yaml"
          ],
          "has_license": true,
          "focus_points": [
            "先决定它是并入主规划、保持外部种子，还是拆成多个更窄的内部 skill。",
            "如果准备纳入体系，先补上与主规划域的映射关系和落位说明。",
            "重点看这个种子是否真的能落入主规划，还是保持独立参考更合适。"
          ]
        },
        {
          "id": "\"spreadsheet\"",
          "name": "\"spreadsheet\"",
          "title": "Spreadsheet Skill",
          "status": "seed",
          "status_label": "扩展种子",
          "domain_id": "seed",
          "domain_label": "扩展种子",
          "domain_description": "已入库但未并入主规划的参考 skill",
          "domain_order": 10,
          "item_order": 3,
          "auto_trigger": "\"Use when tasks involve creating, editing, analyzing, or formatting spreadsheets (`.xlsx`, `.csv`, `.tsv`) with formula-aware workflows, cached recalculation, and visual review.\"",
          "core_responsibility": "当前已在仓库中，但尚未并入主规划域表。",
          "skill_path": "spreadsheet/SKILL.md",
          "directory_path": "spreadsheet",
          "directory": "spreadsheet",
          "sections": [
            "When to use",
            "Workflow",
            "Temp and output conventions",
            "Primary tooling",
            "Recalculation and visual review",
            "Rendering and visual checks",
            "Dependencies (install if missing)",
            "Environment",
            "Examples",
            "Formula requirements",
            "Citation requirements",
            "Formatting requirements (existing formatted spreadsheets)",
            "Formatting requirements (new or unstyled spreadsheets)",
            "Color conventions (if no style guidance)",
            "Finance-specific requirements",
            "Investment banking layouts"
          ],
          "references": [
            "spreadsheet/references/examples/openpyxl/create_basic_spreadsheet.py",
            "spreadsheet/references/examples/openpyxl/create_spreadsheet_with_styling.py",
            "spreadsheet/references/examples/openpyxl/read_existing_spreadsheet.py",
            "spreadsheet/references/examples/openpyxl/styling_spreadsheet.py"
          ],
          "agents": [
            "spreadsheet/agents/openai.yaml"
          ],
          "has_license": true,
          "focus_points": [
            "先决定它是并入主规划、保持外部种子，还是拆成多个更窄的内部 skill。",
            "如果准备纳入体系，先补上与主规划域的映射关系和落位说明。",
            "重点看这个种子是否真的能落入主规划，还是保持独立参考更合适。"
          ]
        },
        {
          "id": "find-skills",
          "name": "find-skills",
          "title": "查找 Skills",
          "status": "seed",
          "status_label": "扩展种子",
          "domain_id": "seed",
          "domain_label": "扩展种子",
          "domain_description": "已入库但未并入主规划的参考 skill",
          "domain_order": 10,
          "item_order": 4,
          "auto_trigger": "当用户提出“我该怎么做 X”“帮我找一个做 X 的 skill”“有没有能做这个的 skill”这类问题，或表达想扩展能力的诉求时，帮助用户发现并安装可用的 agent skill。凡是用户在寻找可能以可安装 skill 形式存在的能力时，都应使用此 skill。",
          "core_responsibility": "当前已在仓库中，但尚未并入主规划域表。",
          "skill_path": "find-skills/SKILL.md",
          "directory_path": "find-skills",
          "directory": "find-skills",
          "sections": [
            "何时使用本 Skill",
            "什么是 Skills CLI？",
            "如何帮助用户查找 Skills",
            "常见 Skill 分类",
            "高效搜索建议",
            "当没有找到合适的 Skill 时"
          ],
          "references": [],
          "agents": [],
          "has_license": false,
          "focus_points": [
            "先决定它是并入主规划、保持外部种子，还是拆成多个更窄的内部 skill。",
            "如果准备纳入体系，先补上与主规划域的映射关系和落位说明。",
            "重点看这个种子是否真的能落入主规划，还是保持独立参考更合适。"
          ]
        },
        {
          "id": "skill-compliance-gate-rules",
          "name": "skill-compliance-gate-rules",
          "title": "Skill 执行完整性闸门规则",
          "status": "seed",
          "status_label": "扩展种子",
          "domain_id": "seed",
          "domain_label": "扩展种子",
          "domain_description": "已入库但未并入主规划的参考 skill",
          "domain_order": 10,
          "item_order": 5,
          "auto_trigger": "当任务已经进入编码、审查、测试或交付收口阶段，且本轮已触发一个或多个 skill，但存在“只执行了部分规则、未执行规则没有明确后续动作”的风险时触发。负责在最终回复前进行一次 skill 执行完整性闸门检查，并在固定格式中输出合并后的下一步建议：主任务建议优先，skill 补齐建议次优先。不要用它代替需求澄清、Bug 定位、功能实现或测试执行本身。",
          "core_responsibility": "当前已在仓库中，但尚未并入主规划域表。",
          "skill_path": "skill-compliance-gate-rules/SKILL.md",
          "directory_path": "skill-compliance-gate-rules",
          "directory": "skill-compliance-gate-rules",
          "sections": [
            "Skill 作用与适用场景",
            "自动触发信号",
            "进入后先做什么",
            "默认执行流程",
            "提交前闸门检查（internal/router）",
            "输出要求（简化版）",
            "阻断判定与处理",
            "权责边界与不负责事项",
            "执行通过 / 驳回标准",
            "references 读取规则",
            "回到主流程的重启点"
          ],
          "references": [
            "skill-compliance-gate-rules/references/applicability-and-gap-check.md",
            "skill-compliance-gate-rules/references/next-step-suggestion-template.md"
          ],
          "agents": [
            "skill-compliance-gate-rules/agents/openai.yaml"
          ],
          "has_license": false,
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
      "domain_description": "流程分流、冲突裁决、阶段阻断与全局基础约定",
      "domain_order": 1,
      "item_order": 1,
      "auto_trigger": "当任务阶段不明确、领域边界不清、多个 skill 同时触发、流程需要暂停/重启/继续/终止，或需要先判断应该进入历史回忆、需求、Bug、编码、测试还是交付处理时触发。负责阶段分析、路由分流、冲突裁决和流程阻断；不要在单一明确的 SQL、API、配置、测试、评审等任务中触发。",
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
        "重点看是否只做分流、阻断或全局基础约定，没有越权覆盖单域 skill。"
      ]
    },
    {
      "id": "artifact-storage-rules",
      "name": "artifact-storage-rules",
      "title": "研发产物存储规则",
      "status": "implemented",
      "status_label": "已实现",
      "domain_id": "orchestration",
      "domain_label": "总控层",
      "domain_description": "流程分流、冲突裁决、阶段阻断与全局基础约定",
      "domain_order": 1,
      "item_order": 2,
      "auto_trigger": "当需要定义、调整或解释项目中 `ment/`、`bug/`、`test/`、`doc/` 以及根目录 `项目设计.md` 等研发产物根目录、主入口文件、命名模板、同任务复用策略或跨域文档引用关系时自动触发。负责提供全局唯一的目录与命名单一真相源，并为需求、Bug、测试、记忆、项目设计和交付类 skill 提供统一引用基准；不要用它代替需求分析、Bug 定位、测试执行、生产代码存放决策或流程分流。",
      "core_responsibility": "作为跨域统一约定 skill，提供目录、命名和复用策略的单一真相源，供需求、Bug、测试、记忆、项目设计和交付类 skill 统一引用。",
      "skill_path": "artifact-storage-rules/SKILL.md",
      "directory_path": "artifact-storage-rules",
      "directory": "artifact-storage-rules",
      "sections": [
        "Skill 作用与适用场景",
        "测试目录复用优先级（写死边界）",
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
        "artifact-storage-rules/references/naming-templates.md",
        "artifact-storage-rules/references/path-map.yaml",
        "artifact-storage-rules/references/root-directories.md",
        "artifact-storage-rules/references/skill-integration.md",
        "artifact-storage-rules/references/update-policy.md"
      ],
      "agents": [
        "artifact-storage-rules/agents/openai.yaml"
      ],
      "has_license": false,
      "focus_points": [
        "优先检查 description 是否具体到触发信号，而不是只写抽象用途。",
        "检查 references 是否足以承接复杂场景，避免 SKILL.md 过厚或过空。",
        "重点看是否只做分流、阻断或全局基础约定，没有越权覆盖单域 skill。"
      ]
    },
    {
      "id": "project-design-doc-rules",
      "name": "project-design-doc-rules",
      "title": "项目设计文档规则",
      "status": "implemented",
      "status_label": "已实现",
      "domain_id": "orchestration",
      "domain_label": "总控层",
      "domain_description": "流程分流、冲突裁决、阶段阻断与全局基础约定",
      "domain_order": 1,
      "item_order": 3,
      "auto_trigger": "当用户要求分析整个项目、梳理项目架构/模块/目录/主链路、检查根目录 `项目设计.md` 及同类设计文档是否偏移、同步更新项目设计文档，或在完成全项目分析后为缺失项目补建根目录 `项目设计.md` 时自动触发。负责把根目录项目设计类文档作为弱参考源读取，按“代码与当前文档优先、设计文档低优先级”原则校验偏移，并统一同步到根目录 `项目设计.md`；不要用它代替 recent-context-bootstrap-rules 的轻量预热、artifact-storage-rules 的路径命名总规则、project-timeline-rules 的长期时间线，或 package-structure-rules / code-placement-review-rules 的代码归位判断。",
      "core_responsibility": "负责把根目录项目设计类文档当作弱参考源读取，按代码与当前文档优先原则判断偏移，并统一同步或补建根目录 `项目设计.md`。",
      "skill_path": "project-design-doc-rules/SKILL.md",
      "directory_path": "project-design-doc-rules",
      "directory": "project-design-doc-rules",
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
        "project-design-doc-rules/references/design-template.md",
        "project-design-doc-rules/references/discovery-and-priority.md",
        "project-design-doc-rules/references/sync-policy.md"
      ],
      "agents": [
        "project-design-doc-rules/agents/openai.yaml"
      ],
      "has_license": false,
      "focus_points": [
        "优先检查 description 是否具体到触发信号，而不是只写抽象用途。",
        "检查 references 是否足以承接复杂场景，避免 SKILL.md 过厚或过空。",
        "重点看是否只做分流、阻断或全局基础约定，没有越权覆盖单域 skill。"
      ]
    },
    {
      "id": "skill-evolution-rules",
      "name": "skill-evolution-rules",
      "title": "Skill 演进规则",
      "status": "implemented",
      "status_label": "已实现",
      "domain_id": "orchestration",
      "domain_label": "总控层",
      "domain_description": "流程分流、冲突裁决、阶段阻断与全局基础约定",
      "domain_order": 1,
      "item_order": 4,
      "auto_trigger": "当研发任务已经进入需求、Bug、编码、审查、测试或交付主流程，且当前已命中的 skill 在执行中暴露出触发不准、规则缺失、边界不清、references 不足、归档约定缺失或无法覆盖当前高频场景，继续推进只能依赖临时口头补充时触发。负责判断这是业务问题还是 skill 问题，明确应补哪个现有 skill、是否需要新增相邻 skill、给出最小完善建议，并在必要时先暂停当前任务；待 skill 更新并重新加载后，再回到原任务继续执行。不要用它代替需求补齐、Bug 定位或具体代码实现。",
      "core_responsibility": "负责判断这是业务问题还是 skill 问题，明确应补哪个现有 skill、是否需要新增相邻 skill、给出最小完善建议，并在必要时先暂停当前任务，待 skill 更新并重新加载后再继续。",
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
        "skill-evolution-rules/references/evolution-decision-matrix.md",
        "skill-evolution-rules/references/gap-signals.md",
        "skill-evolution-rules/references/improvement-output-template.md",
        "skill-evolution-rules/references/resume-workflow.md"
      ],
      "agents": [
        "skill-evolution-rules/agents/openai.yaml"
      ],
      "has_license": false,
      "focus_points": [
        "优先检查 description 是否具体到触发信号，而不是只写抽象用途。",
        "检查 references 是否足以承接复杂场景，避免 SKILL.md 过厚或过空。",
        "重点看是否只做分流、阻断或全局基础约定，没有越权覆盖单域 skill。"
      ]
    },
    {
      "id": "recent-context-bootstrap-rules",
      "name": "recent-context-bootstrap-rules",
      "title": "新会话上下文预热规则",
      "status": "implemented",
      "status_label": "已实现",
      "domain_id": "memory",
      "domain_label": "记忆域",
      "domain_description": "新会话近期预热、跨会话历史检索、项目演进回顾、长期上下文补全",
      "domain_order": 2,
      "item_order": 1,
      "auto_trigger": "当当前会话刚开始、缺少历史上下文、用户直接提出与当前项目相关的需求、Bug、编码、测试或交付问题时自动触发。负责优先从 `artifact-storage-rules` 约定的近 3 天需求、测试、Bug、文档根目录和 git 提交中提取最近活动；如果当前任务涉及整项目分析、架构梳理或模块总览，也可额外读取根目录 `项目设计.md` 及其同类设计文档作为弱参考源，但不把它当成最新事实；如果部分目录不存在，则只使用存在的目录和 git 信息；不要把它代替 history-recall-rules 的深度历史回忆、project-timeline-rules 的长期时间线、project-design-doc-rules 的设计文档同步，或当前主域本身的分析执行。",
      "core_responsibility": "负责优先从 `artifact-storage-rules` 约定目录和最近 Git 提交中压缩前置上下文；如果当前任务涉及整项目分析，可额外弱读取根目录项目设计类文档，再把任务转交真正主域。",
      "skill_path": "recent-context-bootstrap-rules/SKILL.md",
      "directory_path": "recent-context-bootstrap-rules",
      "directory": "recent-context-bootstrap-rules",
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
        "recent-context-bootstrap-rules/references/bootstrap-sources.md",
        "recent-context-bootstrap-rules/references/boundary-rules.md",
        "recent-context-bootstrap-rules/references/output-format.md"
      ],
      "agents": [
        "recent-context-bootstrap-rules/agents/openai.yaml"
      ],
      "has_license": false,
      "focus_points": [
        "优先检查 description 是否具体到触发信号，而不是只写抽象用途。",
        "检查 references 是否足以承接复杂场景，避免 SKILL.md 过厚或过空。",
        "重点看它是否只补近期或历史上下文，不越权代替当前需求、Bug、编码或交付判断。"
      ]
    },
    {
      "id": "history-recall-rules",
      "name": "history-recall-rules",
      "title": "历史回忆规则",
      "status": "implemented",
      "status_label": "已实现",
      "domain_id": "memory",
      "domain_label": "记忆域",
      "domain_description": "新会话近期预热、跨会话历史检索、项目演进回顾、长期上下文补全",
      "domain_order": 2,
      "item_order": 2,
      "auto_trigger": "当用户明确询问“上次怎么做的”“之前有没有修过/做过/讨论过”“以前类似需求/类似 Bug/类似接口/类似表结构是怎么处理的”，或当前任务明显依赖过去会话结论时自动触发。负责优先从持久记忆后端检索历史方案、历史修复和历史决策；如果没有真实记忆后端，则降级为基于 `artifact-storage-rules` 约定目录、Git 和本地文档的历史回溯；不要把它代替 recent-context-bootstrap-rules 的新会话最近 3 天上下文预热，也不要用它代替当前需求澄清、当前 Bug 定位或当前实现验证。",
      "core_responsibility": "负责检索跨会话历史、历史方案和历史修复记录，补回长期上下文。",
      "skill_path": "history-recall-rules/SKILL.md",
      "directory_path": "history-recall-rules",
      "directory": "history-recall-rules",
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
        "history-recall-rules/references/backend-boundary.md",
        "history-recall-rules/references/local-fallback-recall.md",
        "history-recall-rules/references/persistent-search-workflow.md",
        "history-recall-rules/references/source-notes.md"
      ],
      "agents": [
        "history-recall-rules/agents/openai.yaml"
      ],
      "has_license": false,
      "focus_points": [
        "优先检查 description 是否具体到触发信号，而不是只写抽象用途。",
        "检查 references 是否足以承接复杂场景，避免 SKILL.md 过厚或过空。",
        "重点看它是否只补近期或历史上下文，不越权代替当前需求、Bug、编码或交付判断。"
      ]
    },
    {
      "id": "project-timeline-rules",
      "name": "project-timeline-rules",
      "title": "项目时间线规则",
      "status": "implemented",
      "status_label": "已实现",
      "domain_id": "memory",
      "domain_label": "记忆域",
      "domain_description": "新会话近期预热、跨会话历史检索、项目演进回顾、长期上下文补全",
      "domain_order": 2,
      "item_order": 3,
      "auto_trigger": "当用户要求生成项目开发历程、阶段总结、技术演进、关键决策回顾、项目时间线报告、完整历史分析或“这个项目一路是怎么走过来的”时自动触发。负责基于持久记忆后端或本地历史材料，按时间顺序组织项目演进、关键阶段、重大问题和技术决策；不要用它代替当前一次交付摘要、当前需求验收或当前 Bug 修复说明。",
      "core_responsibility": "负责按项目维度组织长期历史、输出时间线和演进报告。",
      "skill_path": "project-timeline-rules/SKILL.md",
      "directory_path": "project-timeline-rules",
      "directory": "project-timeline-rules",
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
        "project-timeline-rules/references/backend-timeline-workflow.md",
        "project-timeline-rules/references/local-material-timeline.md",
        "project-timeline-rules/references/source-notes.md",
        "project-timeline-rules/references/timeline-scope-boundary.md"
      ],
      "agents": [
        "project-timeline-rules/agents/openai.yaml"
      ],
      "has_license": false,
      "focus_points": [
        "优先检查 description 是否具体到触发信号，而不是只写抽象用途。",
        "检查 references 是否足以承接复杂场景，避免 SKILL.md 过厚或过空。",
        "重点看它是否只补近期或历史上下文，不越权代替当前需求、Bug、编码或交付判断。"
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
      "domain_order": 3,
      "item_order": 1,
      "auto_trigger": "当用户提出新需求、新功能、新页面、新接口、新模块，且任务刚进入研发阶段、尚未进入实现或 Bug 定位时触发。支持从需求 URL、零散资料、物料和补充说明中整理需求，先结合当前项目上下文逐步澄清目标、约束和成功标准，对存在多个合理方向的需求先收敛方案，再补齐到可进入后续代码开发的程度，并将结果沉淀到 `artifact-storage-rules` 约定的需求文档根目录；它同时定义需求域统一文档入口，同一需求后续只能持续更新由 `artifact-storage-rules` 约定的同一份需求主文档；不要用它代替需求缺口、边界、拆分、变更或验收标准类 skill。",
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
      "domain_order": 3,
      "item_order": 2,
      "auto_trigger": "当需求描述不完整、缺少前提、缺少字段、缺少流程、缺少业务规则、缺少依赖条件、缺少成功标准、存在多种合理解释或关键方案尚未收敛时触发。负责识别需求缺口并在信息不足时阻断盲目编码推进，同时将缺口分析结果持续更新到 `requirement-intake-rules` 约定、且路径与命名由 `artifact-storage-rules` 统一定义的同一份需求主文档中；不要用它代替需求边界判断、需求变更判断或验收标准细化 skill。",
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
      "domain_order": 3,
      "item_order": 3,
      "auto_trigger": "当需求边界不清、影响范围不明、兼容性不明确、是否允许改旧逻辑不清楚，或需要区分当前需求、历史问题、需求变更和验收偏差时触发。负责明确改动边界和影响面，并将边界结论持续更新到 `requirement-intake-rules` 约定、且路径与命名由 `artifact-storage-rules` 统一定义的同一份需求主文档中；不要用它代替需求缺口识别或 Bug 根因定位 skill。",
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
      "domain_order": 3,
      "item_order": 4,
      "auto_trigger": "当需求较大、涉及多个模块、多个接口、多个页面、多个步骤、多个角色协作，或一次性覆盖多个独立子系统、多个产品子域、多个相对独立主线，无法作为单一实现单元稳定推进时触发。负责拆出任务边界、实施顺序和最小闭环，并将拆分结果持续更新到 `requirement-intake-rules` 约定、且路径与命名由 `artifact-storage-rules` 统一定义的同一份需求主文档中；不要用它代替需求接入、边界确认或项目排期管理。",
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
      "id": "implementation-plan-rules",
      "name": "implementation-plan-rules",
      "title": "实施计划拆解规则",
      "status": "implemented",
      "status_label": "已实现",
      "domain_id": "requirement",
      "domain_label": "需求域",
      "domain_description": "需求澄清、缺口识别、边界确认、验收前置",
      "domain_order": 3,
      "item_order": 5,
      "auto_trigger": "当需求、边界和验收标准已基本稳定，且正式编码前仍需要先把当前优先闭环的文件落点、模块职责、任务顺序、验证步骤和阶段收口拆清时触发。负责把已确认需求或已拆分出的当前优先子项转成可执行实施计划，并将计划单独保存到 `artifact-storage-rules` 约定的实施计划文档中；不要用它代替需求拆分、验收标准编写、实际编码或测试执行。",
      "core_responsibility": "把已确认需求转成可执行实施计划。",
      "skill_path": "implementation-plan-rules/SKILL.md",
      "directory_path": "implementation-plan-rules",
      "directory": "implementation-plan-rules",
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
        "implementation-plan-rules/references/plan-boundaries-and-examples.md",
        "implementation-plan-rules/references/plan-entry-checklist.md",
        "implementation-plan-rules/references/plan-review-checklist.md",
        "implementation-plan-rules/references/plan-structure-template.md",
        "implementation-plan-rules/references/source-notes.md",
        "implementation-plan-rules/references/task-granularity-and-order.md"
      ],
      "agents": [
        "implementation-plan-rules/agents/openai.yaml"
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
      "domain_order": 3,
      "item_order": 6,
      "auto_trigger": "当编码过程中需求被补充、修正、插入新条件、改变优先级、调整默认值或交付物形态时触发。负责识别变更类型、重算影响范围和决定是否需要回退前序结论，并将变更结果持续更新到 `requirement-intake-rules` 约定、且路径与命名由 `artifact-storage-rules` 统一定义的同一份需求主文档中；不要把历史缺陷误当成需求变更。",
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
      "domain_order": 3,
      "item_order": 7,
      "auto_trigger": "当任务准备进入实现前确认，或交付前需要把“做到什么算完成”写成可验证、可测试、可复核的标准时触发。负责细化成功条件、异常条件、边界条件和不在范围项，并将验收标准单独保存到 `artifact-storage-rules` 约定的验收文档中；不要用它代替功能验证或回归验证。",
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
      "domain_order": 4,
      "item_order": 1,
      "auto_trigger": "当用户描述报错、异常行为、结果不符、线上问题、偶发问题、接口异常、页面异常、数据错误或性能异常时触发。负责把 Bug 描述标准化，整理现象、影响范围、环境条件、期望结果和实际结果，并统一建立符合 `artifact-storage-rules` 约定的 Bug 根目录记录；不要用它代替根因定位、运行时调试或修复方案制定 skill。",
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
      "domain_order": 4,
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
      "domain_order": 4,
      "item_order": 3,
      "auto_trigger": "当问题需要构造步骤、确定触发条件、判断是否稳定发生、确认出现频率或复现环境时触发。负责输出复现路径、稳定性判断、符合 `artifact-storage-rules` 约定的 Bug 根目录记录和无法复现时的结论处理；不要用它代替根因分析。",
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
      "domain_order": 4,
      "item_order": 4,
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
      "domain_order": 4,
      "item_order": 5,
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
      "domain_order": 4,
      "item_order": 6,
      "auto_trigger": "当定位 Bug 需要临时增加 debug 日志、关键变量输出、关键分支日志、上下游输入输出日志或时间线日志来补充运行时证据时触发。负责日志落点、日志粒度、Bug 根目录记录、可回收性和清理要求；临时诊断日志也必须使用项目日志框架且不得使用控制台打印；不要把临时诊断日志混成正式日志策略。",
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
      "domain_order": 4,
      "item_order": 7,
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
      "domain_order": 4,
      "item_order": 8,
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
      "domain_order": 4,
      "item_order": 9,
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
      "domain_order": 4,
      "item_order": 10,
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
      "id": "code-minimal-change-rules",
      "name": "code-minimal-change-rules",
      "title": "最小改动编码规则",
      "status": "implemented",
      "status_label": "已实现",
      "domain_id": "baseline",
      "domain_label": "编码基线域",
      "domain_description": "开始编码即并行生效的基础质量规则",
      "domain_order": 5,
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
      "domain_order": 5,
      "item_order": 2,
      "auto_trigger": "当新增或修改业务代码、工具代码、服务代码、脚本代码或 Bug 修复逻辑时触发。负责约束函数结构、逻辑顺序、复杂度和可维护性，并在功能不变前提下优先让最近改动代码表达更清楚、更直接；当单文件达到 500 行及以上且仍持续新增功能时，必须触发拆分评估；结构调整落地后必须联动 `code-comment-rules` 完成改动位点注释补齐；Go 接入第三方 API 时默认使用结构体解析响应，禁止长期使用 map + key 硬编码解析；不要用它代替最小改动、风格一致性、注释规则或代码归位规则。",
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
        "需要避免",
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
      "domain_order": 5,
      "item_order": 3,
      "auto_trigger": "当新增或修改任意代码文件、脚本文件、配置型代码或测试代码时触发。负责跟随项目现有写法，避免局部风格跳变和个人偏好入侵；不要用它代替最小改动、可读性、注释规范或代码归位规则。",
      "core_responsibility": "跟随项目现有风格，不引入风格跳变。",
      "skill_path": "code-style-consistency-rules/SKILL.md",
      "directory_path": "code-style-consistency-rules",
      "directory": "code-style-consistency-rules",
      "sections": [
        "Skill 作用与适用场景",
        "Go 路由风格约定",
        "Go 局部变量声明风格约定",
        "Go 函数签名风格约定",
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
      "domain_order": 5,
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
      "domain_order": 5,
      "item_order": 5,
      "auto_trigger": "当新增或修改代码注释、步骤说明、复杂逻辑解释、临时诊断说明或测试说明，且团队要求注释必须使用中文（除标准协议字段/第三方固定错误原文外）时触发。负责中文注释的语言选择、表达方式和禁忌；不要把它代替注释位置与颗粒度规则。",
      "core_responsibility": "统一中文表达习惯和注释语气。",
      "skill_path": "chinese-comment-rules/SKILL.md",
      "directory_path": "chinese-comment-rules",
      "directory": "chinese-comment-rules",
      "sections": [
        "Skill 作用与适用场景",
        "强制规则：注释语言",
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
      "domain_order": 5,
      "item_order": 6,
      "auto_trigger": "当新增或修改任意代码，或需要判断代码是否应该加注释、注释放在哪里、写到什么颗粒度、如何与实现同步维护时触发。负责注释必要性、位置选择、颗粒度控制、步骤注释、字段注释、函数方法参数返回注释、函数方法修改时间标注和过期注释治理；必须对本轮改动位点执行注释补齐检查；每个函数方法的修改都必须补充最近修改时间（北京时间：yyyy-MM-DD HH:mm:ss），并补充 `[参数]` / `[返回]` 简单注释；Swagger/OpenAPI 接口文档注解/注释不由本 skill 兜底，应转交 api-swagger-rules；不要把它代替中文语言表达规则。",
      "core_responsibility": "统一注释层级和颗粒度，并拦截改动位点漏注释。",
      "skill_path": "code-comment-rules/SKILL.md",
      "directory_path": "code-comment-rules",
      "directory": "code-comment-rules",
      "sections": [
        "Skill 作用与适用场景",
        "强制门禁：改动位点注释补齐",
        "强制规则：步骤注释位置",
        "强制规则：注释语言",
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
      "domain_order": 6,
      "item_order": 1,
      "auto_trigger": "用于判断新增或修改包、目录、模块、`main.go` 启动入口、`internal` 私有代码、`utils` / `common` / `global` / `middleware` / `crontask` / `async` 等支撑目录，以及 `router` / `controller` / `service` / `repository` / `model` / `entity` 等业务目录的落点、职责和依赖方向。适用于 Go、Java、Node/Python 项目的结构决策，尤其适合判断单二进制 Go 服务中哪些代码必须留在 `internal/`，以及哪些入口层目录必须保持根级；`utils` / `common` / `global` / `middleware` 根目录默认只放子包子目录，`internal/service` 也默认先拆业务子目录再落实现文件；Go 场景下请求/响应/第三方结果等结构体默认落在 `internal/entity`，不应散落在 `internal/service` 实现文件；当单文件达到 500 行及以上且仍在扩展时，需评估按功能拆文件并在必要时拆子目录/子包；不要用它代替工具实现、接口设计或代码审查类 skill。",
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
      "domain_order": 6,
      "item_order": 2,
      "auto_trigger": "当新增或修改工具类、通用方法、公共组件、工具函数、通用常量或复用代码时触发。负责统一公共工具代码的判定标准、存放位置、调用方式和边界；`utils` / `common` / `global` / `middleware` 这类通用包根目录应先按职责拆子目录，再在子目录放实现文件，避免循环依赖和命名冲突；不要用它代替业务逻辑抽象、包结构规则或具体实现细则。",
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
      "domain_order": 6,
      "item_order": 3,
      "auto_trigger": "当新增或修改表、字段、索引、唯一约束、外键、迁移脚本、DDL、实体结构、schema 定义时自动触发。负责统一数据库结构变更、迁移安全、兼容性和回滚边界；数据库的字段必须要定义数据类型、默认值、是否需要索引、字段 CHARSET=utf8mb4、ENGINE=InnoDB、注释说明等写清楚，不要遗漏；所有金额相关的要强制使用字符串，避免任何出现精度问题的情况；所有表必须包含 created_at 和 updated_at 字段，由数据库自动管理；必须冗余一个毫秒级时间戳的创建时间，避免数据库的时区问题影响不同的时间格式；所有表必须包含逻辑删除字段，1 的状态标识删除，不是 1 代表正常非删除状态，默认 0=非删除；否则会导致自动创建表出现不可控的因素；避免把查询实现、事务控制和业务逻辑混进结构变更；不要用它代替 database-query-rules、项目配置约束或发布回滚流程。",
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
      "domain_order": 6,
      "item_order": 4,
      "auto_trigger": "当新增或修改 SQL、Repository、DAO、Mapper、QueryBuilder、事务、锁、批量 CRUD、分页查询时自动触发。负责统一数据库访问实现、查询性能、事务与锁边界，避免把 schema 设计、缓存策略和业务逻辑混进数据访问层；不要用它代替 database-schema-rules、缓存策略约束或业务规则本身。",
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
      "domain_order": 6,
      "item_order": 5,
      "auto_trigger": "当新增或修改 controller、router、路由声明、HTTP 方法、接口路径命名、接口入口职责或超时入口边界时触发。负责统一接口入口设计、路径命名和强制使用 POST 方法，并约束 Go 路由注册代码块写法；必须以 package-structure-rules 为基准，不使用 handler 包名；若本次改动影响 Swagger/OpenAPI 的路径、tag、摘要或文档分组，应与 api-swagger-rules 同步生效；不要用它代替请求参数、响应结构或错误处理规则。",
      "core_responsibility": "统一接口入口设计。",
      "skill_path": "api-endpoint-rules/SKILL.md",
      "directory_path": "api-endpoint-rules",
      "directory": "api-endpoint-rules",
      "sections": [
        "Skill 作用与适用场景",
        "强制规则：Go 路由注册写法（internal/router）",
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
      "domain_order": 6,
      "item_order": 6,
      "auto_trigger": "当新增或修改请求参数、DTO、body 结构、参数校验或请求模型时触发。负责统一请求结构、参数表达和基础校验边界；必须以 api-endpoint-rules 为基准，只使用 POST 请求，所有参数通过 JSON body 传递；若本次改动影响 Swagger/OpenAPI 请求模型、字段说明或示例，应与 api-swagger-rules 同步生效；不要用它代替接口入口设计、响应结构或业务规则本身。",
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
      "domain_order": 6,
      "item_order": 7,
      "auto_trigger": "当新增或修改返回体、响应包装器、分页结构、错误响应结构、兼容字段、版本字段或统一响应模型时触发。负责统一响应格式和兼容策略；成功响应和错误响应都必须包含状态码、状态、消息、数据四个字段；若本次改动影响 Swagger/OpenAPI 成功响应、错误响应或分页文档，应与 api-swagger-rules 同步生效；不要用它代替错误处理流程、异常分类或接口入口职责规则。",
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
      "id": "api-swagger-rules",
      "name": "api-swagger-rules",
      "title": "Swagger / OpenAPI 规则",
      "status": "implemented",
      "status_label": "已实现",
      "domain_id": "location",
      "domain_label": "代码位点域",
      "domain_description": "按改动位置叠加触发的实现规则",
      "domain_order": 6,
      "item_order": 8,
      "auto_trigger": "当新增或修改后端 HTTP API、Swagger/OpenAPI 框架接入、接口文档注解/注释、Swagger 调试入口、接口分组标签、文档暴露路径或 Swagger 环境开关时触发。负责统一 Swagger/OpenAPI 框架选型边界、接口文档最小必填项、请求/响应同步、调试可用性和暴露安全规则；对存在 HTTP API 且需要联调/调试的后端项目，默认要求使用统一的 Swagger/OpenAPI 方案；不要用它代替 api-endpoint-rules、api-request-rules、api-response-rules、普通业务注释规则或功能验证。",
      "core_responsibility": "统一 Swagger/OpenAPI 接入、接口文档同步和调试入口暴露规则。",
      "skill_path": "api-swagger-rules/SKILL.md",
      "directory_path": "api-swagger-rules",
      "directory": "api-swagger-rules",
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
        "api-swagger-rules/references/baseline-and-scope.md",
        "api-swagger-rules/references/exposure-and-security.md",
        "api-swagger-rules/references/sync-and-annotation-rules.md"
      ],
      "agents": [
        "api-swagger-rules/agents/openai.yaml"
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
      "domain_order": 6,
      "item_order": 9,
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
      "domain_order": 6,
      "item_order": 10,
      "auto_trigger": "当新增或修改日志、logger、trace、span、审计日志、脱敏字段、排障字段、日志配置文件或链路透传逻辑时触发。负责统一日志与链路追踪规则，后端日志必须使用项目日志框架且不得使用控制台打印，并通过配置文件管理日志参数；日志初始化必须在 LoadConfig 之后且仅初始化一次，禁止空配置预初始化；不要用它代替错误处理、响应结构或长期监控告警策略。",
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
        "logging-trace-rules/references/backend-framework-and-config.md",
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
      "id": "frontend-design",
      "name": "frontend-design",
      "title": "frontend-design",
      "status": "implemented",
      "status_label": "已实现",
      "domain_id": "location",
      "domain_label": "代码位点域",
      "domain_description": "按改动位置叠加触发的实现规则",
      "domain_order": 6,
      "item_order": 11,
      "auto_trigger": "创建具有鲜明风格、达到生产级质量的高品质前端界面。当用户要求构建 Web 组件、页面或前端应用时使用这个 skill。它会生成有创意、打磨精细的代码，并避免出现千篇一律的 AI 模板化审美。",
      "core_responsibility": "生成具有鲜明风格、生产级质量的前端界面，并在与内部前端规则冲突时优先作为主导 skill。",
      "skill_path": "frontend-design/SKILL.md",
      "directory_path": "frontend-design",
      "directory": "frontend-design",
      "sections": [
        "设计思考",
        "前端审美指导"
      ],
      "references": [],
      "agents": [],
      "has_license": false,
      "focus_points": [
        "优先检查 description 是否具体到触发信号，而不是只写抽象用途。",
        "检查 references 是否足以承接复杂场景，避免 SKILL.md 过厚或过空。",
        "重点看主位点与横切位点是否可并行叠加，而不是互相覆盖。",
        "当前没有 references，可考虑补最小示例或边界文档以降低后续维护成本。"
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
      "domain_order": 6,
      "item_order": 12,
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
      "domain_order": 6,
      "item_order": 13,
      "auto_trigger": "当新增或修改前端页面、页面布局、主题样式、配色、字体、图标、卡片、弹窗、表单、表格、图表、导航、空状态、动画、响应式样式、暗黑模式、设计 token、Tailwind 类名、CSS/SCSS/LESS、`.tsx`/`.jsx`/`.vue`/`.html` 中影响界面视觉和交互体验的代码时自动触发，尤其适用于首页、营销页、品牌展示页、数据面板和需要明确设计方向的前端界面。负责页面视觉方向、信息层级、交互反馈、可访问性、响应式适配和交付前 UI 自审；内置合并后的 UI/UX 设计种子数据与搜索脚本，可在风格不明时辅助定方向；不要用它代替纯组件工程拆分、状态管理、接口接线或后端规则。",
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
        "frontend-ui-visual-rules/references/aesthetic-direction-rules.md",
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
      "has_license": true,
      "focus_points": [
        "优先检查 description 是否具体到触发信号，而不是只写抽象用途。",
        "检查 references 是否足以承接复杂场景，避免 SKILL.md 过厚或过空。",
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
      "domain_order": 7,
      "item_order": 1,
      "auto_trigger": "当功能代码已经完成、准备进入测试前验证时触发。负责检查实现是否符合可读性优先、单一职责、命名语义化、注释完整、错误处理明确、日志可追溯、依赖使用审慎、魔法值治理、冗余逻辑清理和编码规范等实现质量要求，并在功能不变前提下检查最近改动代码是否还存在可直接收口的表达层冗余；必须核验本轮改动是否完成 `code-comment-rules` 的改动位点注释补齐；必须识别 500 行及以上且持续膨胀的文件并要求拆分或给出拆分方案；Go 场景下还需在实现自审阶段扫描 `test/` 外 `*_test.go` 禁放问题，以及本轮改动是否把业务实现直接落在 `internal/service/*.go` 根目录文件，是否把请求/响应/第三方结果结构体散落在 `internal/service` 实现文件，是否在函数/方法内使用 `var (...)` 分组声明局部变量，是否把多参数函数签名直接写成多行参数列表，是否把第三方 API 响应长期用 `map[string]any` + key 硬编码解析；若本轮改动涉及后端 HTTP API，还必须检查 Swagger/OpenAPI 是否同步更新；不要用它代替语法检查、格式化执行、目录归位审查或功能验证规则。",
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
      "domain_order": 7,
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
      "domain_order": 7,
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
      "domain_order": 7,
      "item_order": 4,
      "auto_trigger": "当新增文件、移动文件、扩展模块、跨层调用、工具类落点或目录归属可能不合理时，在进入测试前触发。负责检查代码存放位置、模块归属、层级边界和依赖方向是否合理；Go 项目中还需检查 `*_test.go` 是否误落在 `test/` 之外，并检查 `internal/service` 是否散落请求/响应等结构体定义；对 500 行及以上且持续膨胀的文件需追加拆分审查；不要用它代替编码前的包结构决策规则。",
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
      "domain_description": "策略、资源、功能验证、浏览器联动与回归",
      "domain_order": 8,
      "item_order": 1,
      "auto_trigger": "当准备进入测试阶段，需要确定测什么、先测什么、测到什么程度、哪些路径必须覆盖、哪些风险只能记录待补测时触发。负责测试优先级、测试类型组合、覆盖范围和资源收口；必须以 `artifact-storage-rules` 与 `test-location-rules` 为基准，把策略摘要统一记录到中央约定的测试任务主说明 `README.md` 中，并在需要拆成多轮独立测试时给出多个时间戳根目录方案；不要用它代替具体测试资源管理或验证执行 skill。",
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
      "domain_description": "策略、资源、功能验证、浏览器联动与回归",
      "domain_order": 8,
      "item_order": 2,
      "auto_trigger": "当新增或修改测试目录、测试文件、测试脚本、验证程序、fixture、mock 数据、测试说明文档落点时触发。负责在 `artifact-storage-rules` 的统一约定下管理测试资源根目录、时间戳任务根目录、中文说明目录、真实代码路径镜像目录和禁止散落规则；尤其要避免把中文路径放进会被 Go 工具链编译的测试包目录，并强制 Go 源码目录禁止落地 `*_test.go`（白盒诉求必须通过可外部测试 seam 解决）。不要用它代替 test-naming-rules、test-program-rules、test-doc-rules、code-placement-review-rules 或功能验证规则。",
      "core_responsibility": "统一测试资源位置。",
      "skill_path": "test-location-rules/SKILL.md",
      "directory_path": "test-location-rules",
      "directory": "test-location-rules",
      "sections": [
        "铁律：所有测试资产必须统一在 `artifact-storage-rules` 定义的测试根目录下",
        "Go 冲突决策分支：白盒同包诉求与禁放规则",
        "新基线：时间戳根目录 + 中文说明目录 + 真实代码路径镜像",
        "硬阻断规则：新测试任务必须使用当天时间戳目录",
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
      "domain_description": "策略、资源、功能验证、浏览器联动与回归",
      "domain_order": 8,
      "item_order": 3,
      "auto_trigger": "当创建或修改测试时间戳根目录、中文说明目录、测试文件、测试脚本、测试数据目录、fixture 目录、mock 目录时触发。负责统一测试目录与文件命名规范，保证名称可读、可检索、与业务目标一致；必须以 `artifact-storage-rules` 与 `test-location-rules` 为基础，遵循中央约定的时间戳根目录、中文说明目录和真实代码路径镜像目录命名规则；尤其要避免中文进入会被 Go 工具链编译的路径。不要用它代替 test-location-rules、test-program-rules、test-doc-rules 或功能验证规则。",
      "core_responsibility": "统一测试目录和文件命名。",
      "skill_path": "test-naming-rules/SKILL.md",
      "directory_path": "test-naming-rules",
      "directory": "test-naming-rules",
      "sections": [
        "命名一致性硬规则（时间戳目录）",
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
      "domain_description": "策略、资源、功能验证、浏览器联动与回归",
      "domain_order": 8,
      "item_order": 4,
      "auto_trigger": "当新增或修改测试程序、模拟程序、验证脚本、数据构造脚本、测试辅助代码时触发。负责统一测试程序职责拆分、辅助代码边界和长期保留策略；必须以 `artifact-storage-rules` 与 `test-location-rules` 为基准，把真实测试代码、脚本、mock、fixture 和执行产物统一落在中央约定的测试时间戳根目录下的 ASCII 真实代码路径镜像目录中，并避免中文进入会被 Go 工具链编译的路径；测试脚本执行时必须向控制台输出关键过程日志，便于观察执行进度与定位失败步骤；Go 场景下白盒/黑盒/集成测试都遵循同一落点规则，源码目录禁止 `*_test.go`，白盒诉求通过 seam 解决；第三方 API 文档缺失响应模型时，必须先用测试脚本探测真实响应，再反推结构体定义；不要用它代替 test-location-rules、test-naming-rules、test-doc-rules、bug-runtime-debug-rules 或功能验证规则。",
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
      "domain_description": "策略、资源、功能验证、浏览器联动与回归",
      "domain_order": 8,
      "item_order": 5,
      "auto_trigger": "当新增或修改测试 README、验证说明、测试报告、覆盖说明、测试执行记录时触发。负责统一测试文档的最小结构、记录字段、主文档入口和归档方式；必须以 `artifact-storage-rules` 与 `test-location-rules` 为基准，使用中央约定的测试任务主说明 `README.md` 作为中文主说明入口，并把额外文档放到同一时间戳根目录下的 ASCII 真实代码路径镜像目录中；不要用它代替 test-location-rules、test-program-rules、functional-validation-rules 或 test-regression-rules。",
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
      "id": "agent-browser",
      "name": "agent-browser",
      "title": "使用 agent-browser 进行浏览器自动化",
      "status": "implemented",
      "status_label": "已实现",
      "domain_id": "test",
      "domain_label": "测试域",
      "domain_description": "策略、资源、功能验证、浏览器联动与回归",
      "domain_order": 8,
      "item_order": 6,
      "auto_trigger": "面向 AI 代理的浏览器自动化 CLI。当用户需要与网站交互时使用，包括打开页面、填写表单、点击按钮、截图、提取数据、测试 Web 应用，或执行任何浏览器自动化任务。典型触发语句包括“打开一个网站”“填写表单”“点击按钮”“截个图”“抓取页面数据”“测试这个 Web 应用”“登录某个网站”“自动化浏览器操作”，以及任何需要通过程序控制浏览器完成的任务。",
      "core_responsibility": "统一浏览器自动化测试与页面交互执行。",
      "skill_path": "agent-browser/SKILL.md",
      "directory_path": "agent-browser",
      "directory": "agent-browser",
      "sections": [
        "核心工作流",
        "命令链式执行",
        "处理认证",
        "常用命令",
        "Streaming",
        "Batch 批量执行",
        "常见模式",
        "安全",
        "Diff（验证变化）",
        "超时与慢页面",
        "JavaScript 对话框（alert / confirm / prompt）",
        "Session 管理与清理",
        "Ref 生命周期（重要）",
        "带标注的截图（Vision 模式）",
        "语义定位器（Refs 的替代方案）",
        "JavaScript 求值（eval）",
        "配置文件",
        "深入文档",
        "浏览器引擎选择",
        "观测面板（Observability Dashboard）",
        "可直接使用的模板"
      ],
      "references": [
        "agent-browser/references/authentication.md",
        "agent-browser/references/commands.md",
        "agent-browser/references/profiling.md",
        "agent-browser/references/proxy-support.md",
        "agent-browser/references/session-management.md",
        "agent-browser/references/snapshot-refs.md",
        "agent-browser/references/video-recording.md"
      ],
      "agents": [],
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
      "domain_description": "策略、资源、功能验证、浏览器联动与回归",
      "domain_order": 8,
      "item_order": 7,
      "auto_trigger": "当需要验证新功能、修改后的功能、接口行为、页面交互、输入输出结果是否满足当前需求、当前变更和验收标准时触发。负责界定本次功能验证范围、验证步骤、通过驳回标准和结论留痕；必须以 `artifact-storage-rules` 与 `test-location-rules` 为基准，把功能验证结论写回中央约定的测试任务主说明 `README.md`，并把详细执行证据放到同一时间戳根目录下的 ASCII 真实代码路径镜像目录中；不要用它代替 test-strategy-rules、test-location-rules 或 test-regression-rules。",
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
      "domain_description": "策略、资源、功能验证、浏览器联动与回归",
      "domain_order": 8,
      "item_order": 8,
      "auto_trigger": "当 Bug 修复、原有功能迭代、公共模块修改、共享逻辑调整、接口兼容性变化后准备执行测试时触发。负责判定回归范围、选择回归用例、验证兼容性影响并输出回归结论；必须以 `artifact-storage-rules` 与 `test-location-rules` 为基准，把回归结论统一写回中央约定的测试任务主说明 `README.md`，并把详细回归案例、执行证据和补充说明放到同一时间戳根目录下的 ASCII 真实代码路径镜像目录中；不要用它代替 functional-validation-rules、test-strategy-rules 或测试资源管理类规则。",
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
      "id": "git-collaboration-rules",
      "name": "git-collaboration-rules",
      "title": "Git 协作规则",
      "status": "implemented",
      "status_label": "已实现",
      "domain_id": "delivery",
      "domain_label": "交付域",
      "domain_description": "Git 协作与交付说明",
      "domain_order": 9,
      "item_order": 1,
      "auto_trigger": "当准备整理提交、拆提交粒度、同步分支、处理协作变更、准备 PR 或合并前收口时触发。负责提交粒度、提交说明、分支同步、协作边界和 PR 整理；提交代码时必须分析未提交的代码，如果可以分成不同的业务修改，就用多次不同的 git 提交；git 提交消息必须遵循 feat/fix 等格式，并且在 Windows/PowerShell 下提交说明必须使用真实换行（禁止把 `\\n` 当文本）；git 提交前必须先在项目根目录 README.md 追加本次改动日志，格式为时间 + 提交标题，且 README.md 改动日志必须保持按时间正序排列；Go 项目提交前还必须扫描 `test/` 外 `*_test.go` 并阻断违规提交，同时阻断本次提交中直接落在 `internal/service/*.go` 根目录的业务实现文件；不要把它代替代码评审或发布上线规则。",
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
        "重点看 Git 协作与交付说明是否已分层收口，并且不越界替代测试或发布流程。"
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
      "domain_description": "Git 协作与交付说明",
      "domain_order": 9,
      "item_order": 2,
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
        "重点看 Git 协作与交付说明是否已分层收口，并且不越界替代测试或发布流程。"
      ]
    },
    {
      "id": "\"doc\"",
      "name": "\"doc\"",
      "title": "DOCX Skill",
      "status": "seed",
      "status_label": "扩展种子",
      "domain_id": "seed",
      "domain_label": "扩展种子",
      "domain_description": "已入库但未并入主规划的参考 skill",
      "domain_order": 10,
      "item_order": 1,
      "auto_trigger": "\"Use when the task involves reading, creating, or editing `.docx` documents, especially when formatting or layout fidelity matters; prefer `python-docx` plus the bundled `scripts/render_docx.py` for visual checks.\"",
      "core_responsibility": "当前已在仓库中，但尚未并入主规划域表。",
      "skill_path": "doc/SKILL.md",
      "directory_path": "doc",
      "directory": "doc",
      "sections": [
        "When to use",
        "Workflow",
        "Temp and output conventions",
        "Dependencies (install if missing)",
        "Environment",
        "Rendering commands",
        "Quality expectations",
        "Final checks"
      ],
      "references": [],
      "agents": [
        "doc/agents/openai.yaml"
      ],
      "has_license": true,
      "focus_points": [
        "先决定它是并入主规划、保持外部种子，还是拆成多个更窄的内部 skill。",
        "如果准备纳入体系，先补上与主规划域的映射关系和落位说明。",
        "重点看这个种子是否真的能落入主规划，还是保持独立参考更合适。"
      ]
    },
    {
      "id": "\"pdf\"",
      "name": "\"pdf\"",
      "title": "PDF Skill",
      "status": "seed",
      "status_label": "扩展种子",
      "domain_id": "seed",
      "domain_label": "扩展种子",
      "domain_description": "已入库但未并入主规划的参考 skill",
      "domain_order": 10,
      "item_order": 2,
      "auto_trigger": "\"Use when tasks involve reading, creating, or reviewing PDF files where rendering and layout matter; prefer visual checks by rendering pages (Poppler) and use Python tools such as `reportlab`, `pdfplumber`, and `pypdf` for generation and extraction.\"",
      "core_responsibility": "当前已在仓库中，但尚未并入主规划域表。",
      "skill_path": "pdf/SKILL.md",
      "directory_path": "pdf",
      "directory": "pdf",
      "sections": [
        "When to use",
        "Workflow",
        "Temp and output conventions",
        "Dependencies (install if missing)",
        "Environment",
        "Rendering command",
        "Quality expectations",
        "Final checks"
      ],
      "references": [],
      "agents": [
        "pdf/agents/openai.yaml"
      ],
      "has_license": true,
      "focus_points": [
        "先决定它是并入主规划、保持外部种子，还是拆成多个更窄的内部 skill。",
        "如果准备纳入体系，先补上与主规划域的映射关系和落位说明。",
        "重点看这个种子是否真的能落入主规划，还是保持独立参考更合适。"
      ]
    },
    {
      "id": "\"spreadsheet\"",
      "name": "\"spreadsheet\"",
      "title": "Spreadsheet Skill",
      "status": "seed",
      "status_label": "扩展种子",
      "domain_id": "seed",
      "domain_label": "扩展种子",
      "domain_description": "已入库但未并入主规划的参考 skill",
      "domain_order": 10,
      "item_order": 3,
      "auto_trigger": "\"Use when tasks involve creating, editing, analyzing, or formatting spreadsheets (`.xlsx`, `.csv`, `.tsv`) with formula-aware workflows, cached recalculation, and visual review.\"",
      "core_responsibility": "当前已在仓库中，但尚未并入主规划域表。",
      "skill_path": "spreadsheet/SKILL.md",
      "directory_path": "spreadsheet",
      "directory": "spreadsheet",
      "sections": [
        "When to use",
        "Workflow",
        "Temp and output conventions",
        "Primary tooling",
        "Recalculation and visual review",
        "Rendering and visual checks",
        "Dependencies (install if missing)",
        "Environment",
        "Examples",
        "Formula requirements",
        "Citation requirements",
        "Formatting requirements (existing formatted spreadsheets)",
        "Formatting requirements (new or unstyled spreadsheets)",
        "Color conventions (if no style guidance)",
        "Finance-specific requirements",
        "Investment banking layouts"
      ],
      "references": [
        "spreadsheet/references/examples/openpyxl/create_basic_spreadsheet.py",
        "spreadsheet/references/examples/openpyxl/create_spreadsheet_with_styling.py",
        "spreadsheet/references/examples/openpyxl/read_existing_spreadsheet.py",
        "spreadsheet/references/examples/openpyxl/styling_spreadsheet.py"
      ],
      "agents": [
        "spreadsheet/agents/openai.yaml"
      ],
      "has_license": true,
      "focus_points": [
        "先决定它是并入主规划、保持外部种子，还是拆成多个更窄的内部 skill。",
        "如果准备纳入体系，先补上与主规划域的映射关系和落位说明。",
        "重点看这个种子是否真的能落入主规划，还是保持独立参考更合适。"
      ]
    },
    {
      "id": "find-skills",
      "name": "find-skills",
      "title": "查找 Skills",
      "status": "seed",
      "status_label": "扩展种子",
      "domain_id": "seed",
      "domain_label": "扩展种子",
      "domain_description": "已入库但未并入主规划的参考 skill",
      "domain_order": 10,
      "item_order": 4,
      "auto_trigger": "当用户提出“我该怎么做 X”“帮我找一个做 X 的 skill”“有没有能做这个的 skill”这类问题，或表达想扩展能力的诉求时，帮助用户发现并安装可用的 agent skill。凡是用户在寻找可能以可安装 skill 形式存在的能力时，都应使用此 skill。",
      "core_responsibility": "当前已在仓库中，但尚未并入主规划域表。",
      "skill_path": "find-skills/SKILL.md",
      "directory_path": "find-skills",
      "directory": "find-skills",
      "sections": [
        "何时使用本 Skill",
        "什么是 Skills CLI？",
        "如何帮助用户查找 Skills",
        "常见 Skill 分类",
        "高效搜索建议",
        "当没有找到合适的 Skill 时"
      ],
      "references": [],
      "agents": [],
      "has_license": false,
      "focus_points": [
        "先决定它是并入主规划、保持外部种子，还是拆成多个更窄的内部 skill。",
        "如果准备纳入体系，先补上与主规划域的映射关系和落位说明。",
        "重点看这个种子是否真的能落入主规划，还是保持独立参考更合适。"
      ]
    },
    {
      "id": "skill-compliance-gate-rules",
      "name": "skill-compliance-gate-rules",
      "title": "Skill 执行完整性闸门规则",
      "status": "seed",
      "status_label": "扩展种子",
      "domain_id": "seed",
      "domain_label": "扩展种子",
      "domain_description": "已入库但未并入主规划的参考 skill",
      "domain_order": 10,
      "item_order": 5,
      "auto_trigger": "当任务已经进入编码、审查、测试或交付收口阶段，且本轮已触发一个或多个 skill，但存在“只执行了部分规则、未执行规则没有明确后续动作”的风险时触发。负责在最终回复前进行一次 skill 执行完整性闸门检查，并在固定格式中输出合并后的下一步建议：主任务建议优先，skill 补齐建议次优先。不要用它代替需求澄清、Bug 定位、功能实现或测试执行本身。",
      "core_responsibility": "当前已在仓库中，但尚未并入主规划域表。",
      "skill_path": "skill-compliance-gate-rules/SKILL.md",
      "directory_path": "skill-compliance-gate-rules",
      "directory": "skill-compliance-gate-rules",
      "sections": [
        "Skill 作用与适用场景",
        "自动触发信号",
        "进入后先做什么",
        "默认执行流程",
        "提交前闸门检查（internal/router）",
        "输出要求（简化版）",
        "阻断判定与处理",
        "权责边界与不负责事项",
        "执行通过 / 驳回标准",
        "references 读取规则",
        "回到主流程的重启点"
      ],
      "references": [
        "skill-compliance-gate-rules/references/applicability-and-gap-check.md",
        "skill-compliance-gate-rules/references/next-step-suggestion-template.md"
      ],
      "agents": [
        "skill-compliance-gate-rules/agents/openai.yaml"
      ],
      "has_license": false,
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
    },
    {
      "id": "doc:README",
      "name": "README",
      "file_name": "README.md",
      "title": "luode-skills",
      "kind": "其他文档",
      "path": "README.md",
      "is_plan_doc": false
    }
  ],
  "recommendations": [
    "57 个规划 skill 已全部独立落地，后续优化优先检查 description 命中率、相邻 skill 边界和 references 的信息密度。",
    "当前规划同时包含 `frontend-component-rules` 与 `frontend-ui-visual-rules`，建议前者聚焦组件工程与状态边界，后者聚焦页面视觉与交互体验，避免触发歧义。",
    "可以开始按域做第二轮巡检：先审触发 description 是否足够具体，再审 references 是否过厚、过空或与相邻 skill 重叠。"
  ]
};
