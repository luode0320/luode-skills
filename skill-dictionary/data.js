window.SKILL_DICTIONARY = {
  "generated_at": "2026-07-08 11:00:54",
  "repo_root": "D:\\luode\\luode-skills",
  "plan_doc": "编码skill.md",
  "plan_doc_name": "编码skill.md",
  "summary": {
    "planned_total": 83,
    "implemented_total": 83,
    "planned_missing": 0,
    "seed_total": 24,
    "doc_total": 8,
    "references_total": 341,
    "agents_total": 90
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
      "implemented_count": 18,
      "planned_count": 0,
      "seed_count": 0,
      "total_count": 18,
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
          "auto_trigger": "当需要定义、调整或解释项目中 `doc/1-架构/`、`doc/2-需求/`、`doc/3-实施/`、`doc/4-bugs/`、`doc/5-tests/`、`doc/6-审查/`、`doc/7-验收/`、`doc/`、`skill/` 以及根目录 `项目设计.md` 等研发产物根目录、主入口文件、命名模板、同任务复用策略或跨域文档引用关系时自动触发。负责提供全局唯一的目录与命名单一真相源，并为需求、实施、验收、Bug、测试、审查、记忆、项目设计和交付类 skill 提供统一引用基准；不要用它代替需求分析、Bug 定位、测试执行、生产代码存放决策或流程分流。",
          "core_responsibility": "作为跨域统一约定 skill，提供目录、命名和复用策略的单一真相源，供需求、实施、验收、Bug、测试、记忆、项目设计和交付类 skill 统一引用。",
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
          "auto_trigger": "当用户要求分析整个项目、梳理项目架构/模块/目录/主链路、检查根目录 `项目设计.md` 及同类设计文档是否偏移、同步更新项目设计文档，或在完成全项目分析后为缺失项目补建根目录 `项目设计.md` 时自动触发。负责把根目录项目设计类文档作为弱参考源读取，按“代码与当前文档优先、设计文档低优先级”原则校验偏移，并统一同步到根目录 `项目设计.md`；不要用它代替 recent-context-bootstrap-rules 的轻量预热、artifact-storage-rules 的路径命名总规则、project-timeline-rules 的长期时间线，或 package-structure-rules / implementation-review-rules 的测试前归位判断。",
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
          "id": "architecture-doc-rules",
          "name": "architecture-doc-rules",
          "title": "架构文档规则",
          "status": "implemented",
          "status_label": "已实现",
          "domain_id": "orchestration",
          "domain_label": "总控层",
          "domain_description": "流程分流、冲突裁决、阶段阻断与全局基础约定",
          "domain_order": 1,
          "item_order": 4,
          "auto_trigger": "当需要创建、更新、审查或解释 `doc/1-架构/` 下的长期架构文档时自动触发，适用于总架构、目录树、目录职责、模块职责、主要业务/功能设计架构、模块关系、关键链路、运行时设计和架构专题说明；负责维护 `1-总架构.md`、`2-目录树.md`、`3-模块职责.md`、`4-主要业务链路.md` 四个有序中文主入口，并支持从序号 5 开始更新或追加“序号-业务链路-中文业务名称.md”文档。同时区分专题架构文档与根目录 `项目设计.md` 的分层关系，并确保路径、命名和复用策略服从 `artifact-storage-rules`。不要用它代替 project-design-doc-rules 的根目录项目总览同步、implementation-planning-rules 的当前需求实施计划、package-structure-rules 的生产代码目录归位或 codegraph-analysis-rules 的源码图谱探索。",
          "core_responsibility": "负责维护 `1-4` 四个有序中文主入口；业务链路从 `5` 开始依次下推，同一链路保留编号更新，新链路使用最大编号加一，并区分它与根目录 `项目设计.md` 的总览分层关系。",
          "skill_path": "architecture-doc-rules/SKILL.md",
          "directory_path": "architecture-doc-rules",
          "directory": "architecture-doc-rules",
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
            "architecture-doc-rules/references/architecture-doc-template.md",
            "architecture-doc-rules/references/architecture-topic-examples.md",
            "architecture-doc-rules/references/layering-with-project-design.md",
            "architecture-doc-rules/references/update-policy.md"
          ],
          "agents": [],
          "has_license": false,
          "focus_points": [
            "优先检查 description 是否具体到触发信号，而不是只写抽象用途。",
            "检查 references 是否足以承接复杂场景，避免 SKILL.md 过厚或过空。",
            "重点看是否只做分流、阻断或全局基础约定，没有越权覆盖单域 skill。"
          ]
        },
        {
          "id": "project-local-skills-rules",
          "name": "project-local-skills-rules",
          "title": "项目专属 Skill 沉淀规则",
          "status": "implemented",
          "status_label": "已实现",
          "domain_id": "orchestration",
          "domain_label": "总控层",
          "domain_description": "流程分流、冲突裁决、阶段阻断与全局基础约定",
          "domain_order": 1,
          "item_order": 5,
          "auto_trigger": "当用户要求“分析项目”并明确希望总结该项目专属编码规则/实践为 skill，或要求沉淀项目私有 skill 清单时自动触发。负责把项目专属能力拆成多个独立 skill 并统一写入项目根目录 `skill/`，用于后续上下文预热和编码阶段优先命中；不要用它代替通用体系 skill 的执行，也不要代替 `artifact-storage-rules` 的全局路径裁决。",
          "core_responsibility": "负责把项目专属规则拆成多个独立 skill，并统一落到项目根目录 `skill/`，供后续预热和编码阶段优先命中。",
          "skill_path": "project-local-skills-rules/SKILL.md",
          "directory_path": "project-local-skills-rules",
          "directory": "project-local-skills-rules",
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
            "project-local-skills-rules/references/priority-and-roadmap.md",
            "project-local-skills-rules/references/project-skill-template.md",
            "project-local-skills-rules/references/scope-and-splitting.md"
          ],
          "agents": [
            "project-local-skills-rules/agents/openai.yaml"
          ],
          "has_license": false,
          "focus_points": [
            "优先检查 description 是否具体到触发信号，而不是只写抽象用途。",
            "检查 references 是否足以承接复杂场景，避免 SKILL.md 过厚或过空。",
            "重点看是否只做分流、阻断或全局基础约定，没有越权覆盖单域 skill。"
          ]
        },
        {
          "id": "mcp-installation-rules",
          "name": "mcp-installation-rules",
          "title": "MCP 安装判定规则",
          "status": "implemented",
          "status_label": "已实现",
          "domain_id": "orchestration",
          "domain_label": "总控层",
          "domain_description": "流程分流、冲突裁决、阶段阻断与全局基础约定",
          "domain_order": 1,
          "item_order": 6,
          "auto_trigger": "当用户要求分析项目、检查当前项目是否需要安装 MCP、判断浏览器或 Godot 编辑器应优先由哪个工具接管，或任务即将涉及前端页面验证、浏览器联动、Godot 编辑器操控且需要先根据项目结构决定是否安装 Chrome DevTools MCP 或 Godot AI MCP 时自动触发。对“谷歌浏览器 MCP / Google Chrome MCP / Chrome MCP / Chrome DevTools for agents”统一按官方当前名称 `Chrome DevTools MCP` 处理。负责识别前端项目与 Godot 项目标记，给出 MCP 安装结论、优先级、Codex 配置补齐规则和后续工具让路规则；若已具备对应 MCP，应优先使用它们控制浏览器或 Godot 编辑器，再在缺失或不可用时回退到其他本地工具。此外，任何代码仓库默认推荐 CodeGraph（代码探索默认入口）与 codebase-memory-mcp（架构分析补充）这组代码图谱 MCP，安装与配置以官方仓库为准。",
          "core_responsibility": "负责识别前端项目与 Godot 项目标记，给出 MCP 安装结论、安装流程、优先级和后续工具让路规则，并将“谷歌浏览器 MCP / Google Chrome MCP / Chrome DevTools for agents”等称呼统一归一到 Chrome DevTools MCP；若项目级 Codex `config.toml` 缺少目标 MCP 配置，则默认补齐。",
          "skill_path": "mcp-installation-rules/SKILL.md",
          "directory_path": "mcp-installation-rules",
          "directory": "mcp-installation-rules",
          "sections": [
            "Skill 作用与适用场景",
            "自动触发信号",
            "进入后先做什么",
            "默认执行流程",
            "代码图谱 MCP（CodeGraph + codebase-memory-mcp）",
            "平台判定与 Claude Code MCP 配置分支（新增）",
            "Chrome DevTools MCP 安装流程（本节专属 Codex CLI 环境）",
            "适用安装结论模板",
            "默认优先级",
            "与相邻 skill 的边界",
            "需要暂停并确认的条件",
            "执行通过 / 驳回标准",
            "references 读取规则"
          ],
          "references": [
            "mcp-installation-rules/references/config-bootstrap.md",
            "mcp-installation-rules/references/current-sources.md",
            "mcp-installation-rules/references/project-signals.md",
            "mcp-installation-rules/references/tool-priority.md"
          ],
          "agents": [
            "mcp-installation-rules/agents/openai.yaml"
          ],
          "has_license": false,
          "focus_points": [
            "优先检查 description 是否具体到触发信号，而不是只写抽象用途。",
            "检查 references 是否足以承接复杂场景，避免 SKILL.md 过厚或过空。",
            "重点看是否只做分流、阻断或全局基础约定，没有越权覆盖单域 skill。"
          ]
        },
        {
          "id": "godot-project-bootstrap-rules",
          "name": "godot-project-bootstrap-rules",
          "title": "Godot 项目自举规则",
          "status": "implemented",
          "status_label": "已实现",
          "domain_id": "orchestration",
          "domain_label": "总控层",
          "domain_description": "流程分流、冲突裁决、阶段阻断与全局基础约定",
          "domain_order": 1,
          "item_order": 7,
          "auto_trigger": "当仓库命中 `project.godot`、`.gd`、`.tscn`、`addons/`、`export_presets.cfg` 等 Godot 项目标记，且需要自动补齐项目级规则文件（`AGENTS.md` / `CLAUDE.md`）、Godot AI MCP 配置、图像生成配置模板或检查 Godot 开发环境是否可直接进入执行时强制自动触发。负责把 Godot 项目的环境准备、自举补齐、图像通道模板和只差人工配置的缺口一次性收口。",
          "core_responsibility": "负责把 Godot 项目的环境准备、自举补齐、图像通道模板和只差人工配置的缺口一次性收口，并联动 `project-agents-bootstrap`、`mcp-installation-rules` 与 `imagegen`。",
          "skill_path": "godot-project-bootstrap-rules/SKILL.md",
          "directory_path": "godot-project-bootstrap-rules",
          "directory": "godot-project-bootstrap-rules",
          "sections": [
            "目标",
            "自动触发信号",
            "进入后先做什么",
            "默认执行流程",
            "图像配置硬规则",
            "输出要求",
            "与相邻 skill 的边界",
            "通过标准"
          ],
          "references": [],
          "agents": [
            "godot-project-bootstrap-rules/agents/openai.yaml"
          ],
          "has_license": false,
          "focus_points": [
            "优先检查 description 是否具体到触发信号，而不是只写抽象用途。",
            "检查 references 是否足以承接复杂场景，避免 SKILL.md 过厚或过空。",
            "重点看是否只做分流、阻断或全局基础约定，没有越权覆盖单域 skill。",
            "当前没有 references，可考虑补最小示例或边界文档以降低后续维护成本。"
          ]
        },
        {
          "id": "codegraph-analysis-rules",
          "name": "codegraph-analysis-rules",
          "title": "CodeGraph 分析规则",
          "status": "implemented",
          "status_label": "已实现",
          "domain_id": "orchestration",
          "domain_label": "总控层",
          "domain_description": "流程分流、冲突裁决、阶段阻断与全局基础约定",
          "domain_order": 1,
          "item_order": 8,
          "auto_trigger": "当需要分析代码库结构、符号关系、调用链、被调用方、影响面、重构范围或跨文件根因时自动触发。任何仓库都默认先尝试由 CodeGraph 支撑；若未安装 `codegraph`，必须从 `colbymchenry/codegraph` 强制下载并安装；若 `.codegraph/` 未初始化，则先自动初始化再用；若安装或初始化失败、当前环境不支持，则直接回退到 `rg`、`find`、`read` 等本地手段。不要把它代替项目设计、需求澄清、编码实现或测试验证主流程。",
          "core_responsibility": "负责优先提醒使用 CodeGraph 做图谱探索；未初始化时先自动初始化，失败后回退到 `rg`、`find`、`read` 等本地手段。",
          "skill_path": "codegraph-analysis-rules/SKILL.md",
          "directory_path": "codegraph-analysis-rules",
          "directory": "codegraph-analysis-rules",
          "sections": [
            "Skill 作用与适用场景",
            "自动触发信号",
            "进入后先做什么",
            "默认优先级",
            "CodeGraph 初始化规则",
            "与相邻 skill 的边界",
            "需要暂停并确认的条件",
            "执行通过 / 驳回标准"
          ],
          "references": [],
          "agents": [
            "codegraph-analysis-rules/agents/openai.yaml"
          ],
          "has_license": false,
          "focus_points": [
            "优先检查 description 是否具体到触发信号，而不是只写抽象用途。",
            "检查 references 是否足以承接复杂场景，避免 SKILL.md 过厚或过空。",
            "重点看是否只做分流、阻断或全局基础约定，没有越权覆盖单域 skill。",
            "当前没有 references，可考虑补最小示例或边界文档以降低后续维护成本。"
          ]
        },
        {
          "id": "project-agents-bootstrap",
          "name": "project-agents-bootstrap",
          "title": "项目 AGENTS.md 自举与补齐 Skill",
          "status": "implemented",
          "status_label": "已实现",
          "domain_id": "orchestration",
          "domain_label": "总控层",
          "domain_description": "流程分流、冲突裁决、阶段阻断与全局基础约定",
          "domain_order": 1,
          "item_order": 9,
          "auto_trigger": "若当前 AI 为 Claude Code，目标规则文件为 `CLAUDE.md`；若为 Codex，目标规则文件为 `AGENTS.md`；新会话第一轮默认自动触发（不依赖用户意图）；也可被”创建、补齐或更新 AGENTS.md / CLAUDE.md / 补充仓库级规则”等显式请求触发。负责在项目根目录强制检测 AGENTS.md / CLAUDE.md：不存在则必须创建最小可用模板，存在则对受管章节执行增量补齐与幂等 upsert，既保留用户已有规则，也持续同步最新仓库规则；同时确保包含代码生成风格入口规则、注释类任务流程、跨平台 UTF-8 文件写入约束、按平台能力矩阵执行的会话动态重命名规则，以及”上下文压缩后必须重新读取项目根目录规则文件再继续主任务”的硬规则。若仓库命中 Godot 项目标记，还必须额外补齐 Godot 工具接管与图像生成配置模板，并明确规则文件里不能存真实密钥；图像生成配置必须同步主通道与回退规则，且回退规则必须写成 `回退规则：回退配置` 的层级结构，并在其下声明 `api` / `baseurl`；若仓库需要长期记忆与长期风格，两者都要同步引入 `project-memory-rules`、`project-style-rules` 和 `code-generation-style-rules` 的仓库级入口口径，并确保其最低命中要求写入仓库级规则。当用户给出“根据 skill 补充更新 md / 根据规则更新 md / 按 skill 更新项目 md / 更新这几个 md”等聚合指令时，本 skill 作为统一入口，一次性编排项目根目录 `AGENTS.md`、`CLAUDE.md`、`PROJECT_MEMORY.md`、`PROJECT_STYLE.md` 四个核心 md 的“检测→缺失则创建→已存在则增量补齐”；其中 `PROJECT_MEMORY.md` 必须继续保持为唯一长期记忆主文件，但内部补齐为“人类阅读区 + 底部机器索引区”的单文件双区结构，且不得新增 `PROJECT_MEMORY_INDEX.yaml`。",
          "core_responsibility": "负责为项目补齐或同步仓库级规则文件，并把基础硬规则、自举模板和关键白名单口径统一收口。",
          "skill_path": "project-agents-bootstrap/SKILL.md",
          "directory_path": "project-agents-bootstrap",
          "directory": "project-agents-bootstrap",
          "sections": [
            "AI 环境检测与规则文件约定",
            "目标",
            "仓库级总控规则",
            "触发条件",
            "会话动态重命名规则",
            "统一 md 补齐编排（根据 skill 补充更新 md）",
            "执行步骤",
            "脚本用法",
            "最小模板（缺失时使用）",
            "适用范围",
            "Skill 强制自动触发规则（最高优先级）",
            "严禁脑补工具调用与结果（最高优先级，强制）",
            "严禁自动提交 Git（最高优先级，强制）",
            "Skill 命中强制规则",
            "代码生成风格入口规则",
            "会话动态重命名规则",
            "注释任务强制流程",
            "上下文压缩续做规则",
            "文件编码与写入规则",
            "变更最小化",
            "本地连接调试测试红线（最高优先级，强制）",
            "依赖与工具复用优先规则",
            "输出格式规则",
            "Windows / WSL 执行规则",
            "CodeGraph 强制准备规则",
            "代码库探索规则",
            "插件检测安装规则",
            "边界"
          ],
          "references": [],
          "agents": [],
          "has_license": false,
          "focus_points": [
            "优先检查 description 是否具体到触发信号，而不是只写抽象用途。",
            "检查 references 是否足以承接复杂场景，避免 SKILL.md 过厚或过空。",
            "重点看是否只做分流、阻断或全局基础约定，没有越权覆盖单域 skill。",
            "当前没有 references，可考虑补最小示例或边界文档以降低后续维护成本。"
          ]
        },
        {
          "id": "thread-title-rules",
          "name": "thread-title-rules",
          "title": "会话标题规则",
          "status": "implemented",
          "status_label": "已实现",
          "domain_id": "orchestration",
          "domain_label": "总控层",
          "domain_description": "流程分流、冲突裁决、阶段阻断与全局基础约定",
          "domain_order": 1,
          "item_order": 10,
          "auto_trigger": "【强制自动触发】当当前会话收到明确提问、需求、Bug、实施、审查、测试、提交、规则更新或其他可命名请求，或进入 goal 创建 / goal 恢复 / 上下文压缩续做 / 长任务阶段切换等过程节点，且可稳定归纳出中文任务主题时触发。负责自动生成 8-24 字中文简要标题，并按平台能力矩阵调用真实线程重命名工具重命名当前会话：Codex 使用 `set_thread_title`，Claude Code 仅在存在真实改名工具时执行，Claude Desktop 默认视为无真实自动改名工具并显式跳过；不等待用户显式要求，也不等到最终总结。问题过于闲聊、主题过散、标题已准确、工具不可用或用户明确禁止时不改名。不要用它代替需求分析、Bug 定位、实施规划、测试验证或提交动作。",
          "core_responsibility": "负责生成 8-24 字中文简要标题，并按平台能力矩阵调用当前环境真实线程重命名工具更新当前会话标题；Codex 优先使用 `set_thread_title`，Claude Code 仅在存在真实改名工具时执行，Claude Desktop 默认显式跳过。",
          "skill_path": "thread-title-rules/SKILL.md",
          "directory_path": "thread-title-rules",
          "directory": "thread-title-rules",
          "sections": [
            "目标",
            "自动触发条件",
            "跳过条件",
            "标题生成规则",
            "平台能力矩阵",
            "执行流程",
            "工具与证据约束",
            "通过标准"
          ],
          "references": [],
          "agents": [
            "thread-title-rules/agents/openai.yaml"
          ],
          "has_license": false,
          "focus_points": [
            "优先检查 description 是否具体到触发信号，而不是只写抽象用途。",
            "检查 references 是否足以承接复杂场景，避免 SKILL.md 过厚或过空。",
            "重点看是否只做分流、阻断或全局基础约定，没有越权覆盖单域 skill。",
            "当前没有 references，可考虑补最小示例或边界文档以降低后续维护成本。"
          ]
        },
        {
          "id": "parallel-task-dispatch-rules",
          "name": "parallel-task-dispatch-rules",
          "title": "并行任务分发规则",
          "status": "implemented",
          "status_label": "已实现",
          "domain_id": "orchestration",
          "domain_label": "总控层",
          "domain_description": "流程分流、冲突裁决、阶段阻断与全局基础约定",
          "domain_order": 1,
          "item_order": 11,
          "auto_trigger": "【强制自动触发】当研发、分析、侦察、审查、测试或文档任务进入实质执行前触发，不限于固定 skill 映射；主 agent 必须自主判断当前目标是否存在可由子 agent 并行推进的独立问题、证据来源、文件集、模块边界或职责边界。负责判断当前工作应并行、条件并行还是串行推进，并给出线程拆分、文件归属、收口合并与回退条件；若判定为可并行或条件并行且无阻断，必须联动 `subagent-dispatch-rules` 做真实启动判定。本仓库完全授权模式视为满足工具显式授权条件；只要环境支持、写集不冲突且风险可控，就应发起真实子线程 / 子代理并行执行。适用于项目分析、代码库侦察、需求完善侦察、Bug 分诊与证据收集、代码规范检查、注释补充、格式清理、lint 修复、测试补充、文档更新等可独立推进的任务；审查类 skill 只要能只读或按独立文件集检查，默认优先并行；单一根因裁决、接口边界冻结、数据库 schema 变更等必须先串行定边界，但其旁路证据收集可在边界清晰时条件并行。",
          "core_responsibility": "负责判断当前工作应并行、条件并行还是串行推进；若允许并行且无阻断，继续联动 `subagent-dispatch-rules` 发起真实子线程，并输出并行技能与文件归属。",
          "skill_path": "parallel-task-dispatch-rules/SKILL.md",
          "directory_path": "parallel-task-dispatch-rules",
          "directory": "parallel-task-dispatch-rules",
          "sections": [
            "目标",
            "核心判定规则",
            "典型分类",
            "分发流程",
            "输出要求",
            "与 subagent-dispatch-rules 的联动闸门",
            "执行通过 / 驳回标准",
            "references 读取规则"
          ],
          "references": [
            "parallel-task-dispatch-rules/references/existing-skill-mapping.md",
            "parallel-task-dispatch-rules/references/task-classification.md",
            "parallel-task-dispatch-rules/references/thread-template.md"
          ],
          "agents": [
            "parallel-task-dispatch-rules/agents/openai.yaml"
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
          "item_order": 12,
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
          "id": "skill-hit-check-rules",
          "name": "skill-hit-check-rules",
          "title": "Skill 命中检查规则（最小闭环版）",
          "status": "implemented",
          "status_label": "已实现",
          "domain_id": "orchestration",
          "domain_label": "总控层",
          "domain_description": "流程分流、冲突裁决、阶段阻断与全局基础约定",
          "domain_order": 1,
          "item_order": 13,
          "auto_trigger": "【强制总控】每轮用户新消息（含新会话第一条）都必须先做命中检查并在首条中间进度输出。凡涉及 Git 协作动作（含显式关键词与隐式语义，如“提交git/帮我提交/commit一下/推送代码/看下状态”），必须联动命中 git-collaboration-rules。凡处理本仓库任务，最低还必须联动命中 `parallel-task-dispatch-rules`，并执行 Obsidian 知识流选择性默认判断，输出 `Obsidian:<检索/沉淀/不适用/阻断>`；当判断为 `检索` 或 `沉淀` 时必须同时命中 `obsidian-knowledge-flow`。首条中间进度最小必填包含 `命中检查`、`命中技能`，若本轮命中 `parallel-task-dispatch-rules` 还必须追加 `并行技能`。",
          "core_responsibility": "在每轮开始前强制执行命中检查并显式回报命中列表，避免静默漏触发。",
          "skill_path": "skill-hit-check-rules/SKILL.md",
          "directory_path": "skill-hit-check-rules",
          "directory": "skill-hit-check-rules",
          "sections": [
            "-1.4 极简硬闸门（强制）",
            "-1.5 违规处理（强制）",
            "-1. 触发确认（强制）",
            "-1.0 新会话首轮保障（强制）",
            "-1.1 Git 意图识别（强制）",
            "-1.1.1 Git 仅限当前轮次（新增，强制）",
            "-1.2 Git 判定优先级（强制）",
            "-1.3 新会话首轮联动（强制）",
            "0. 首条消息格式（强制）",
            "1. 最小流程",
            "1.1 首条闸门（强制阻断）",
            "2. Git 联动闸门（强制）",
            "2.3 Skill 资产改动联动闸门（强制）",
            "3. 通过标准",
            "4. 执行文件"
          ],
          "references": [
            "skill-hit-check-rules/references/hit-checklist.md",
            "skill-hit-check-rules/references/output-format.md"
          ],
          "agents": [
            "skill-hit-check-rules/agents/openai.yaml"
          ],
          "has_license": false,
          "focus_points": [
            "优先检查 description 是否具体到触发信号，而不是只写抽象用途。",
            "检查 references 是否足以承接复杂场景，避免 SKILL.md 过厚或过空。",
            "重点看是否只做分流、阻断或全局基础约定，没有越权覆盖单域 skill。"
          ]
        },
        {
          "id": "code-snippet-location-rules",
          "name": "code-snippet-location-rules",
          "title": "代码片段位置定位规则",
          "status": "implemented",
          "status_label": "已实现",
          "domain_id": "orchestration",
          "domain_label": "总控层",
          "domain_description": "流程分流、冲突裁决、阶段阻断与全局基础约定",
          "domain_order": 1,
          "item_order": 14,
          "auto_trigger": "当用户只粘贴一段代码、报错片段、函数片段或截图转写代码，并说“这里改一下/这段需要修改/这里有问题”等，但没有明确给出文件路径、符号全名、模块位置或可唯一定位的代码位点时触发。负责先按“用户明确路径、当前活动编辑器/当前打开文件/当前选区、代码片段精确匹配、仓库搜索候选、询问确认”的优先级定位真实目标文件，避免把相似代码误判到仓库其他位置；不要用它代替 code-context-resync-rules 的已知文件重读，也不要代替具体业务实现、Bug 定位或代码修改规则。",
          "core_responsibility": "负责按“用户明示路径 > 当前活动编辑器 / 当前打开文件 / 当前选区 > 代码片段精确匹配 > 仓库搜索候选 > 询问确认”的优先级定位真实目标文件，避免把相似代码误判到其他位置。",
          "skill_path": "code-snippet-location-rules/SKILL.md",
          "directory_path": "code-snippet-location-rules",
          "directory": "code-snippet-location-rules",
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
            "code-snippet-location-rules/references/source-priority.md"
          ],
          "agents": [
            "code-snippet-location-rules/agents/openai.yaml"
          ],
          "has_license": false,
          "focus_points": [
            "优先检查 description 是否具体到触发信号，而不是只写抽象用途。",
            "检查 references 是否足以承接复杂场景，避免 SKILL.md 过厚或过空。",
            "重点看是否只做分流、阻断或全局基础约定，没有越权覆盖单域 skill。"
          ]
        },
        {
          "id": "subagent-dispatch-rules",
          "name": "subagent-dispatch-rules",
          "title": "子代理分发规则",
          "status": "implemented",
          "status_label": "已实现",
          "domain_id": "orchestration",
          "domain_label": "总控层",
          "domain_description": "流程分流、冲突裁决、阶段阻断与全局基础约定",
          "domain_order": 1,
          "item_order": 15,
          "auto_trigger": "当任一 skill 已命中并准备进入执行阶段时自动触发。负责先自动判断当前任务是否满足 subagent 委派条件；委派判定不需要用户逐次要求，但真实启动必须服从当前环境的 subagent / multi-agent / thread 工具元数据、系统规则和权限策略。本仓库默认采用 subagent 完全授权模式：用户已明确允许 agent 在任务可切分、写集不冲突、风险可控时自动启动 subagent；该项目级 standing authorization 视为满足工具的显式授权条件。只有缺少当前轮授权且缺少项目级完全授权声明时，才判定为“工具授权不支持自动启动”并回退本地执行。不要用它代替需求分析、Bug 定位、编码实现、测试验证或交付收口本身。",
          "core_responsibility": "作为全局委派协调层，统一判定“可委派/不可委派/本地优先”，优先分发代码规则、注释、审查等 sidecar 子任务并回收结果；并强制主 agent 输出可见的 subagent 启动/完成状态、逻辑名与平台昵称映射，以及计划线程数、实际启动线程数与回收关闭线程数。",
          "skill_path": "subagent-dispatch-rules/SKILL.md",
          "directory_path": "subagent-dispatch-rules",
          "directory": "subagent-dispatch-rules",
          "sections": [
            "Skill 作用与适用场景",
            "自动触发信号",
            "进入后先做什么",
            "默认执行流程",
            "主 agent 可见公告（强制）",
            "真实启动证据（强制）",
            "平台能力矩阵（新增）",
            "并发上限与空闲回收（强制）",
            "子任务优先委派清单",
            "必须主 agent 本地执行的场景",
            "权责边界与不负责事项",
            "需要暂停并确认的条件",
            "执行通过 / 驳回标准",
            "references 读取规则"
          ],
          "references": [
            "subagent-dispatch-rules/references/blockers-and-fallbacks.md",
            "subagent-dispatch-rules/references/delegation-decision-matrix.md",
            "subagent-dispatch-rules/references/examples/launch-plan-input-batched.json",
            "subagent-dispatch-rules/references/examples/launch-plan-input.json",
            "subagent-dispatch-rules/references/examples/launch-plan-output-batched.json",
            "subagent-dispatch-rules/references/examples/launch-plan-output.json",
            "subagent-dispatch-rules/references/launch-plan-schema.md",
            "subagent-dispatch-rules/references/subagent-task-templates.md"
          ],
          "agents": [
            "subagent-dispatch-rules/agents/openai.yaml"
          ],
          "has_license": false,
          "focus_points": [
            "优先检查 description 是否具体到触发信号，而不是只写抽象用途。",
            "检查 references 是否足以承接复杂场景，避免 SKILL.md 过厚或过空。",
            "重点看是否只做分流、阻断或全局基础约定，没有越权覆盖单域 skill。"
          ]
        },
        {
          "id": "skill-audit-rules",
          "name": "skill-audit-rules",
          "title": "Skill 审计规则",
          "status": "implemented",
          "status_label": "已实现",
          "domain_id": "orchestration",
          "domain_label": "总控层",
          "domain_description": "流程分流、冲突裁决、阶段阻断与全局基础约定",
          "domain_order": 1,
          "item_order": 16,
          "auto_trigger": "【强制自动触发】当主任务存在多 skill 组合、并行拆分或规则收口风险时触发。负责只读审计当前任务是否漏触发应有的 skill，以及已触发 skill 是否还有未执行完的规则；默认优先并行；输出补漏提醒和遗漏清单。只有存在原执行计划内未完成必需项、阻断缺口或用户明确要求建议时，才输出必要后续动作；不得把可选优化伪装成必需后续，原始目标已完成且无三类合法后续时不得输出下一步类占位文案。本 skill 不改代码、不写文件、不做最终收口。",
          "core_responsibility": "负责只读审计是否漏触发应有 skill，以及已触发 skill 是否还有未执行完的规则。",
          "skill_path": "skill-audit-rules/SKILL.md",
          "directory_path": "skill-audit-rules",
          "directory": "skill-audit-rules",
          "sections": [
            "目标",
            "核心职责",
            "输入",
            "输出",
            "边界",
            "使用时机"
          ],
          "references": [],
          "agents": [
            "skill-audit-rules/agents/openai.yaml"
          ],
          "has_license": false,
          "focus_points": [
            "优先检查 description 是否具体到触发信号，而不是只写抽象用途。",
            "检查 references 是否足以承接复杂场景，避免 SKILL.md 过厚或过空。",
            "重点看是否只做分流、阻断或全局基础约定，没有越权覆盖单域 skill。",
            "当前没有 references，可考虑补最小示例或边界文档以降低后续维护成本。"
          ]
        },
        {
          "id": "skill-compliance-gate-rules",
          "name": "skill-compliance-gate-rules",
          "title": "Skill 执行完整性闸门规则",
          "status": "implemented",
          "status_label": "已实现",
          "domain_id": "orchestration",
          "domain_label": "总控层",
          "domain_description": "流程分流、冲突裁决、阶段阻断与全局基础约定",
          "domain_order": 1,
          "item_order": 17,
          "auto_trigger": "【收口强制触发】只要本轮有代码新增/修改，最终回复前必须命中本 skill。负责检查已命中 skill 是否完整执行（特别是注释双 skill 与 `implementation-review-rules` 的测试前收口）。若存在原执行计划内未完成必需项或阻断级规则缺口，禁止给“已完成”结论；最终收口只允许三类合法后续：原执行计划内未完成必需项、阻断项、用户显式要求的建议/backlog。除此之外默认直接结束，不额外制造任何下一步区块、下一步建议、等待指令文案或“无需继续动作”占位。",
          "core_responsibility": "在最终回复前执行一次 skill 完整性闸门检查，补齐主任务优先的下一步建议，并对代码改动执行注释终检。",
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
            "优先检查 description 是否具体到触发信号，而不是只写抽象用途。",
            "检查 references 是否足以承接复杂场景，避免 SKILL.md 过厚或过空。",
            "重点看是否只做分流、阻断或全局基础约定，没有越权覆盖单域 skill。"
          ]
        },
        {
          "id": "reasoning-summary-structure-rules",
          "name": "reasoning-summary-structure-rules",
          "title": "推理总结结构闸门规则",
          "status": "implemented",
          "status_label": "已实现",
          "domain_id": "orchestration",
          "domain_label": "总控层",
          "domain_description": "流程分流、冲突裁决、阶段阻断与全局基础约定",
          "domain_order": 1,
          "item_order": 18,
          "auto_trigger": "当进入本轮最终推理总结或结束输出阶段时自动触发。负责强制检查总结结构是否完整：必须包含 Skill 命中检查、Skill 执行证据、当前要解决的问题（同时写清用户原始需求与模型理解的需求）、问题的解决方案与根因、验证结果（有验证时）以及当前结果与结论；若本轮有改动必须包含本次改动点（放在总结最后）。最终总结必须与推理过程视觉分界，采用统一严谨的 markdown 排版（`---` 分隔线 + 固定一级主标题 `# 📋 本轮总结` + 二级标题小节 + 表格 / 引用块 / 状态徽章），标题字号大于正文且加粗、层级分明。默认禁止“下一步状态/建议”区块；只有存在原执行计划内未完成必需项、阻断项，或用户明确要求提供后续建议时，才允许出现后续内容。原始用户目标完成、用户明确要求结束，或仅剩可选优化时强制无下一步，禁止输出下一步区块、等待类文案或“无需继续动作”占位文案。不要用它代替需求分析、Bug 定位、实现修改或测试执行。",
          "core_responsibility": "作为最终总结结构闸门，统一收口输出顺序和必填字段，防止关键信息缺失。",
          "skill_path": "reasoning-summary-structure-rules/SKILL.md",
          "directory_path": "reasoning-summary-structure-rules",
          "directory": "reasoning-summary-structure-rules",
          "sections": [
            "Skill 作用与适用场景",
            "自动触发信号",
            "进入后先做什么",
            "默认执行流程",
            "输出要求（固定顺序）",
            "总结视觉规范（强制）",
            "权责边界与不负责事项",
            "执行通过 / 驳回标准",
            "references 读取规则"
          ],
          "references": [
            "reasoning-summary-structure-rules/references/conditional-sections-rules.md",
            "reasoning-summary-structure-rules/references/output-examples.md",
            "reasoning-summary-structure-rules/references/summary-structure-template.md"
          ],
          "agents": [
            "reasoning-summary-structure-rules/agents/openai.yaml"
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
      "implemented_count": 6,
      "planned_count": 0,
      "seed_count": 0,
      "total_count": 6,
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
          "auto_trigger": "当当前会话刚开始、缺少历史上下文、用户直接提出与当前项目相关的需求、Bug、编码、测试或交付问题时自动触发。负责优先从 `artifact-storage-rules` 约定的近 3 天需求、测试、Bug、文档、项目专属 skill 根目录和 git 提交中提取最近活动，并按需加载系统的所有 skills 与当前项目根目录下 `./skill`、`./.skills` 的 skill 清单；如果当前任务涉及整项目分析、架构梳理或模块总览，也可额外读取根目录 `项目设计.md` 及其同类设计文档作为弱参考源，但不把它当成最新事实；如果部分目录不存在，则只使用存在的目录和 git 信息；不要把它代替 history-recall-rules 的深度历史回忆、project-timeline-rules 的长期时间线、project-design-doc-rules 的设计文档同步，或当前主域本身的分析执行。",
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
          "id": "obsidian-knowledge-flow",
          "name": "obsidian-knowledge-flow",
          "title": "Obsidian 知识流",
          "status": "implemented",
          "status_label": "已实现",
          "domain_id": "memory",
          "domain_label": "记忆域",
          "domain_description": "新会话近期预热、跨会话历史检索、项目演进回顾、长期上下文补全",
          "domain_order": 2,
          "item_order": 3,
          "auto_trigger": "将固定根目录的 Obsidian vault 作为 Codex 会话知识库管理，并在仓库任务中采用“选择性默认”触发：每轮先轻量判断 `Obsidian:<检索/沉淀/不适用/阻断>`，只有问题依赖历史决策、项目事实、用户偏好、重复实体、知识库内容或“上次/之前/我们约定/当时怎么说”等历史信息时，才通过 Obsidian CLI 检索相关笔记；会话总结、阶段收口或最终回复前，只有存在可复用的事实、决策、流程、定义、偏好、来源或调试经验时，才通过 Obsidian CLI 捕获/沉淀为 Markdown 笔记。适用于 Obsidian、vault、Markdown 知识库、第二大脑、知识图谱、自动会话笔记、知识提取、快速回忆、本地笔记库、知识库检索、会话总结沉淀和 CLI 笔记操作场景。",
          "core_responsibility": "负责输出 `Obsidian:<检索/沉淀/不适用/阻断>` 判定；只有 `检索` 或 `沉淀` 才通过 Obsidian CLI 读取、捕获或沉淀笔记，CLI / vault 不可用时阻断且不得直接读写 vault 文件。",
          "skill_path": "obsidian-knowledge-flow/SKILL.md",
          "directory_path": "obsidian-knowledge-flow",
          "directory": "obsidian-knowledge-flow",
          "sections": [
            "目标",
            "选择性默认判定",
            "固定根目录",
            "工作流程",
            "捕获规则",
            "检索规则",
            "命令行约定"
          ],
          "references": [
            "obsidian-knowledge-flow/references/capture-retrieve-distill.md",
            "obsidian-knowledge-flow/references/cli-operations.md",
            "obsidian-knowledge-flow/references/conflict-staleness.md",
            "obsidian-knowledge-flow/references/note-schema.md",
            "obsidian-knowledge-flow/references/validation-checklist.md",
            "obsidian-knowledge-flow/references/vault-layout.md"
          ],
          "agents": [
            "obsidian-knowledge-flow/agents/openai.yaml"
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
          "item_order": 4,
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
          "id": "project-memory-rules",
          "name": "project-memory-rules",
          "title": "项目记忆规则",
          "status": "implemented",
          "status_label": "已实现",
          "domain_id": "memory",
          "domain_label": "记忆域",
          "domain_description": "新会话近期预热、跨会话历史检索、项目演进回顾、长期上下文补全",
          "domain_order": 2,
          "item_order": 5,
          "auto_trigger": "从对话、代码与项目文档中抽取并维护长期项目记忆，统一写入根目录 `PROJECT_MEMORY.md`。该文件继续作为唯一长期记忆主文件，但内部升级为“人类阅读区 + 底部机器索引区”的单文件双区结构；默认先更新机器索引区，再同步人类阅读区，不得新增 `PROJECT_MEMORY_INDEX.yaml` 等平行记忆根文件。",
          "core_responsibility": "负责维护根目录 `PROJECT_MEMORY.md` 作为唯一长期记忆源，并在规则调整时回写原词条。",
          "skill_path": "project-memory-rules/SKILL.md",
          "directory_path": "project-memory-rules",
          "directory": "project-memory-rules",
          "sections": [
            "核心目标",
            "适用场景",
            "双区模型",
            "默认流程",
            "写入规则",
            "来源优先级",
            "机器索引区结构",
            "人类阅读区同步规则",
            "生命周期与冲突处理",
            "记忆条目结构"
          ],
          "references": [
            "project-memory-rules/references/memory-conflict-and-staleness.md",
            "project-memory-rules/references/memory-entity-types.md",
            "project-memory-rules/references/memory-extraction-workflow.md",
            "project-memory-rules/references/memory-index-schema.md",
            "project-memory-rules/references/memory-relation-types.md",
            "project-memory-rules/references/memory-retrieval-patterns.md",
            "project-memory-rules/references/project-memory-template.md"
          ],
          "agents": [
            "project-memory-rules/agents/openai.yaml"
          ],
          "has_license": false,
          "focus_points": [
            "优先检查 description 是否具体到触发信号，而不是只写抽象用途。",
            "检查 references 是否足以承接复杂场景，避免 SKILL.md 过厚或过空。",
            "重点看它是否只补近期或历史上下文，不越权代替当前需求、Bug、编码或交付判断。"
          ]
        },
        {
          "id": "project-style-rules",
          "name": "project-style-rules",
          "title": "项目风格规则",
          "status": "implemented",
          "status_label": "已实现",
          "domain_id": "memory",
          "domain_label": "记忆域",
          "domain_description": "新会话近期预热、跨会话历史检索、项目演进回顾、长期上下文补全",
          "domain_order": 2,
          "item_order": 6,
          "auto_trigger": "从对话和代码中自动提取、规范化、合并并增量更新项目代码风格示例，写入根目录 `PROJECT_STYLE.md` 作为唯一风格记忆源。用于项目需要长期记住方法、注释、类、结构体、变量、异步、日志、错误处理、接口、工具调用、循环等代码风格样例的场景；后续写代码时由 `code-generation-style-rules` 读取并应用这份风格记忆，本 skill 只负责维护记忆本身，不作为代码生成风格总控入口。当用户给出“根据 skill 补充更新 md / 根据规则更新 md / 按 skill 更新项目 md / 补充更新 md”等聚合指令时，本 skill 负责其中 `PROJECT_STYLE.md` 的检测、缺失则创建、已存在则增量补齐（通常由 `project-agents-bootstrap` 统一编排联动）。",
          "core_responsibility": "负责维护根目录 `PROJECT_STYLE.md` 作为唯一风格记忆源，并在风格调整时回写原样例。",
          "skill_path": "project-style-rules/SKILL.md",
          "directory_path": "project-style-rules",
          "directory": "project-style-rules",
          "sections": [
            "核心目标",
            "适用场景",
            "默认流程",
            "写入规则",
            "来源优先级",
            "风格条目结构"
          ],
          "references": [
            "project-style-rules/references/project-style-template.md"
          ],
          "agents": [
            "project-style-rules/agents/openai.yaml"
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
      "description": "idea 主动侦察、需求接入、侦察后缺口识别、边界确认、验收前置",
      "order": 3,
      "implemented_count": 9,
      "planned_count": 0,
      "seed_count": 0,
      "total_count": 9,
      "items": [
        {
          "id": "requirement-discovery-rules",
          "name": "requirement-discovery-rules",
          "title": "需求主动侦察规则",
          "status": "implemented",
          "status_label": "已实现",
          "domain_id": "requirement",
          "domain_label": "需求域",
          "domain_description": "idea 主动侦察、需求接入、侦察后缺口识别、边界确认、验收前置",
          "domain_order": 3,
          "item_order": 1,
          "auto_trigger": "当用户只提出一句话 idea、粗略想法、老板式方向、新功能愿景或“想做某个能力”，但没有提前整理完整需求资料时触发。负责由 agent 主动侦察、收罗、比对、推理和成文：查当前项目代码、文档、历史需求、数据库线索、配置、上下游服务、第三方调用、关联项目、用户补充的本地项目路径或 URL、GitHub、相关网站和官方 API 文档，形成有证据来源的需求设计、可行方案和最少待确认问题；必须把已验证有复用价值的资料位置、数据库、URL、项目路径和侦察经验转交 `project-memory-rules` 回写长期记忆。不要用它代替需求主文档接入、需求边界裁决、验收标准或编码实施。",
          "core_responsibility": "主动侦察项目、数据库线索、代码、上下游、关联项目、GitHub、相关网站、官方 API 文档和用户补充路径 / URL，形成有证据来源的需求设计，并回写可复用记忆。",
          "skill_path": "requirement-discovery-rules/SKILL.md",
          "directory_path": "requirement-discovery-rules",
          "directory": "requirement-discovery-rules",
          "sections": [
            "核心原则",
            "自动触发信号",
            "进入后先做什么",
            "默认执行流程",
            "权责边界与不负责事项",
            "需要暂停并确认的条件",
            "执行通过 / 驳回标准",
            "执行结果归档要求",
            "references 读取规则"
          ],
          "references": [
            "requirement-discovery-rules/references/discovery-checklist.md",
            "requirement-discovery-rules/references/evidence-and-memory.md",
            "requirement-discovery-rules/references/output-template.md",
            "requirement-discovery-rules/references/requirement-domain-routing.md"
          ],
          "agents": [
            "requirement-discovery-rules/agents/openai.yaml"
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
          "title": "需求接入规则",
          "status": "implemented",
          "status_label": "已实现",
          "domain_id": "requirement",
          "domain_label": "需求域",
          "domain_description": "idea 主动侦察、需求接入、侦察后缺口识别、边界确认、验收前置",
          "domain_order": 3,
          "item_order": 2,
          "auto_trigger": "当用户提出新需求、新功能、新页面、新接口、新模块，且任务刚进入研发阶段、尚未进入实现或 Bug 定位时触发；如果用户只给一句话 idea、老板式方向、粗略想法，或希望 agent 自己找资料、找数据、看代码、查上下游，必须先联动 requirement-discovery-rules 主动侦察。支持从需求 URL、零散资料、物料和补充说明中整理需求，先结合当前项目上下文逐步澄清目标、约束和成功标准，对存在多个合理方向的需求先收敛方案，再补齐到可进入后续代码开发的程度，并将结果沉淀到 `artifact-storage-rules` 约定的需求文档根目录；它同时定义需求域统一文档入口，discovery 形成初稿后必须立即创建或更新需求主文档，同一需求后续只能持续更新由 `artifact-storage-rules` 约定的同一份需求主文档；不要用它代替需求缺口、边界、拆分、变更或验收标准类 skill。",
          "core_responsibility": "把 discovery 或用户资料收口为同一份需求主文档。",
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
          "domain_description": "idea 主动侦察、需求接入、侦察后缺口识别、边界确认、验收前置",
          "domain_order": 3,
          "item_order": 3,
          "auto_trigger": "当需求描述不完整、缺少前提、缺少字段、缺少流程、缺少业务规则、缺少依赖条件、缺少成功标准、存在多种合理解释或关键方案尚未收敛时触发；如果缺口可能通过当前项目、数据库线索、代码、上下游、历史资料、用户补充路径或 URL、GitHub、相关网站或官方 API 文档主动获得，必须先联动 requirement-discovery-rules 侦察。负责识别 discovery 之后仍无法补齐的关键缺口，并在信息不足时阻断盲目编码推进；gap 阶段应在 `doc/2-需求/` 下生成临时缺口文档记录已侦察证据、未补齐项和待确认问题，待用户确认后再将稳定结论回填到同一份需求主文档并删除临时缺口文档；不要用它代替需求边界判断、需求变更判断或验收标准细化 skill。",
          "core_responsibility": "识别 discovery 后仍无法补齐的关键缺口并阻断盲目实现。",
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
          "domain_description": "idea 主动侦察、需求接入、侦察后缺口识别、边界确认、验收前置",
          "domain_order": 3,
          "item_order": 4,
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
          "domain_description": "idea 主动侦察、需求接入、侦察后缺口识别、边界确认、验收前置",
          "domain_order": 3,
          "item_order": 5,
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
          "id": "implementation-planning-rules",
          "name": "implementation-planning-rules",
          "title": "实施规划规则",
          "status": "implemented",
          "status_label": "已实现",
          "domain_id": "requirement",
          "domain_label": "需求域",
          "domain_description": "idea 主动侦察、需求接入、侦察后缺口识别、边界确认、验收前置",
          "domain_order": 3,
          "item_order": 6,
          "auto_trigger": "当来源对象（需求或 Bug）的条件闸门已收敛且前置验收标准已稳定，正式编码前仍需要先把当前优先闭环的文件落点、模块职责、实施周期、阶段步骤、验证步骤和阻断项拆清时触发；当新项目启动、项目初期存在多个需求 / 多份实施总览 / 多个实施周期，需要先建立“需求与实施计划全量顺序实施方案”或实施顺序总表时也触发。若用户准备采纳上一轮建议、方案、修复路线或实施思路并开始执行，但当前还没有正式执行计划，也必须先触发本 skill 把建议收口成可执行实施方案。若当前上下文处于 `Plan Mode`，无论用户问什么，都必须先命中本 skill 作为第一层计划外壳，再按需回流到计划前置 skill 链路中的需求侦察、需求接入、缺口、边界、拆分或其他域；其中 `Plan Mode` 只提升计划链路优先级，不改变这些前置 skill 的职责边界。若运行环境要求使用专用计划包裹输出，包裹层只作为渲染协议，计划正文仍必须遵守本 skill 与模板定义的结构、字段和约束。若用户本轮核心问题本身是在问“这件事怎么做 / 怎么改 / 先给计划 / 先出方案 / 先列步骤”，也必须先命中本 skill；若前置条件尚未齐备，则输出受限计划或阻断计划，而不是不触发。负责把已确认来源对象或已拆分出的当前优先子项转成可执行实施方案，并将结果单独保存到 `artifact-storage-rules` 约定的实施总览/实施周期文档中；在多来源对象场景下还负责创建或更新项目级 / 集合级全量顺序实施方案，作为跨需求执行顺序总表。不要用它代替需求拆分、Bug 定位、验收标准编写、实际编码、测试执行或最终验收。",
          "core_responsibility": "多来源对象先建“需求与实施计划全量顺序实施方案”，再把已确认需求转成可执行实施总览与实施周期，并明确周期顺序、期次定位、周期内最小任务顺序。",
          "skill_path": "implementation-planning-rules/SKILL.md",
          "directory_path": "implementation-planning-rules",
          "directory": "implementation-planning-rules",
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
            "implementation-planning-rules/references/examples/minimum-task-closure-example.md",
            "implementation-planning-rules/references/full-sequence-master-plan.md",
            "implementation-planning-rules/references/plan-boundaries-and-examples.md",
            "implementation-planning-rules/references/plan-entry-checklist.md",
            "implementation-planning-rules/references/plan-output-gate.md",
            "implementation-planning-rules/references/plan-review-checklist.md",
            "implementation-planning-rules/references/plan-structure-template.md",
            "implementation-planning-rules/references/source-notes.md",
            "implementation-planning-rules/references/task-granularity-and-order.md"
          ],
          "agents": [
            "implementation-planning-rules/agents/openai.yaml"
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
          "domain_description": "idea 主动侦察、需求接入、侦察后缺口识别、边界确认、验收前置",
          "domain_order": 3,
          "item_order": 7,
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
          "domain_description": "idea 主动侦察、需求接入、侦察后缺口识别、边界确认、验收前置",
          "domain_order": 3,
          "item_order": 8,
          "auto_trigger": "当任务准备进入实施前确认“做到什么算完成”时触发。负责细化成功条件、异常条件、边界条件和不在范围项，并将前置验收标准单独保存到 `artifact-storage-rules` 约定的验收标准文档中；不要用它代替功能验证、回归验证或最终验收放行。",
          "core_responsibility": "补齐可验证、可测试的前置验收标准。",
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
          "id": "final-acceptance-rules",
          "name": "final-acceptance-rules",
          "title": "最终验收放行规则",
          "status": "implemented",
          "status_label": "已实现",
          "domain_id": "requirement",
          "domain_label": "需求域",
          "domain_description": "idea 主动侦察、需求接入、侦察后缺口识别、边界确认、验收前置",
          "domain_order": 3,
          "item_order": 9,
          "auto_trigger": "当测试与审核均已完成、任务准备最终放行时触发。负责基于来源对象文档（需求或 Bug）、验收标准、实施总览/实施周期、测试结果和审核结果做后置最终验收，并将结论单独保存到 `artifact-storage-rules` 约定的最终验收文档中；不要用它代替前置验收标准、功能验证、回归验证或实现审查。",
          "core_responsibility": "基于验收标准逐条做最终验收，并检查实施周期已按顺序收口、最小任务已有实现 / 真实测试 / 审查 / 验收证据。",
          "skill_path": "final-acceptance-rules/SKILL.md",
          "directory_path": "final-acceptance-rules",
          "directory": "final-acceptance-rules",
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
            "final-acceptance-rules/references/final-acceptance-boundaries.md",
            "final-acceptance-rules/references/final-acceptance-checklist.md",
            "final-acceptance-rules/references/final-acceptance-template.md"
          ],
          "agents": [
            "final-acceptance-rules/agents/openai.yaml"
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
      "implemented_count": 11,
      "planned_count": 0,
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
          "id": "bug-discovery-rules",
          "name": "bug-discovery-rules",
          "title": "Bug 主动侦察规则",
          "status": "implemented",
          "status_label": "已实现",
          "domain_id": "bug",
          "domain_label": "Bug 域",
          "domain_description": "问题录入、定位、运行时诊断、修复建议",
          "domain_order": 4,
          "item_order": 2,
          "auto_trigger": "当用户只用一句话、一个现象、几张截图或简短报错描述提出 Bug，但还没有整理复现步骤、定位证据或根因线索时触发。负责由 agent 主动侦察、取证、比对、推理：看代码与调用链（联动 `codegraph-analysis-rules`）、读现有日志 / trace / 配置、按需只读连接本地数据库查数据并做对比、理解用户截图与报错图，形成有证据来源的根因候选、可疑位点和最少待确认问题；连库严格遵守“仅本地、只读查询、禁增删改”的安全红线，需要改数据时只产出 SQL 脚本交用户手动执行；并把已验证可复用的代码入口、表 / 字段、查询线索按 `project-memory-rules` 回写到对应业务项目的长期记忆。不要用它代替 `bug-intake-rules` 的标准化录入、`bug-gap-rules` 的缺口阻断、`bug-reproduction-rules` 的复现、`bug-root-cause-rules` 的最终静态定位、`bug-runtime-debug-rules` 的运行时诊断或修复方案制定。",
          "core_responsibility": "主动侦察取证：看代码与调用链、查日志、只读连本地库比数据、读截图，形成有证据的根因候选；连库仅本地、只读、禁增删改。",
          "skill_path": "bug-discovery-rules/SKILL.md",
          "directory_path": "bug-discovery-rules",
          "directory": "bug-discovery-rules",
          "sections": [
            "核心原则",
            "自动触发信号",
            "进入后先做什么",
            "默认执行流程",
            "连接本地数据库的安全红线（强制）",
            "权责边界与不负责事项",
            "需要暂停并确认的条件",
            "执行通过 / 驳回标准",
            "执行结果归档要求",
            "references 读取规则"
          ],
          "references": [
            "bug-discovery-rules/references/bug-domain-routing.md",
            "bug-discovery-rules/references/discovery-checklist.md",
            "bug-discovery-rules/references/evidence-and-db-readonly.md",
            "bug-discovery-rules/references/output-template.md"
          ],
          "agents": [],
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
          "item_order": 3,
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
          "item_order": 4,
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
          "domain_order": 4,
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
          "domain_order": 4,
          "item_order": 7,
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
          "domain_order": 4,
          "item_order": 9,
          "auto_trigger": "当问题已定位，需要形成修改建议、风险评估、备选方案并判断是否应等待用户确认时触发。负责把 Bug 域稳定交接到编码域，并统一记录到 Bug 根目录；修复方案必须针对根因、从源头消除问题，拒绝打补丁式修复（表层特判绕过、try-catch 吞异常、对坏数据兜底而不修源头、堆叠 if 特判等）。不要用它代替根因定位或直接实施编码修复。",
          "core_responsibility": "先给修改建议，再决定是否实施。",
          "skill_path": "bug-fix-proposal-rules/SKILL.md",
          "directory_path": "bug-fix-proposal-rules",
          "directory": "bug-fix-proposal-rules",
          "sections": [
            "Skill 作用与适用场景",
            "自动触发信号",
            "进入后先做什么",
            "默认执行流程",
            "根因修复优先（反打补丁式修复）",
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
          "item_order": 10,
          "auto_trigger": "【强制自动触发】当 Bug 修复可能影响公共方法、共享模块、已有接口、数据库行为、缓存行为、兼容性或其他历史能力时触发。负责识别回归风险点、风险等级、验证优先级并统一记录到 Bug 根目录；默认优先并行；不要把它代替实际回归测试。",
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
      "order": 5,
      "implemented_count": 10,
      "planned_count": 0,
      "seed_count": 0,
      "total_count": 10,
      "items": [
        {
          "id": "code-generation-style-rules",
          "name": "code-generation-style-rules",
          "title": "代码生成风格规则",
          "status": "implemented",
          "status_label": "已实现",
          "domain_id": "baseline",
          "domain_label": "编码基线域",
          "domain_description": "开始编码即并行生效的基础质量规则",
          "domain_order": 5,
          "item_order": 1,
          "auto_trigger": "当新增、修改、重构任意代码、脚本、测试支撑代码或配置型代码前自动触发。负责在正式写代码前读取 `PROJECT_STYLE.md`、当前文件与同目录样例，把项目长期风格记忆和局部既有写法收敛成本轮“代码风格契约”，约束命名、结构、注释、日志、错误处理、复用、排版和禁用写法；写完后执行风格闸门，并在形成新的稳定团队偏好时联动 `project-style-rules` 回写 `PROJECT_STYLE.md`。不替代 `project-style-rules` 的记忆维护职责，也不替代 `code-minimal-change-rules`、`code-readability-rules`、`code-style-consistency-rules`、`naming-rules` 或注释类 skill 的专业检查。",
          "core_responsibility": "读取 `PROJECT_STYLE.md`、当前文件和同目录样例，形成本轮代码风格契约，约束后续实现风格。",
          "skill_path": "code-generation-style-rules/SKILL.md",
          "directory_path": "code-generation-style-rules",
          "directory": "code-generation-style-rules",
          "sections": [
            "核心目标",
            "自动触发信号",
            "进入后先做什么",
            "默认执行流程",
            "风格契约内容",
            "与相邻 Skill 的边界",
            "需要暂停并确认的条件",
            "执行通过 / 驳回标准",
            "references 读取规则"
          ],
          "references": [
            "code-generation-style-rules/references/post-change-style-gate.md",
            "code-generation-style-rules/references/pre-coding-checklist.md",
            "code-generation-style-rules/references/style-contract-template.md",
            "code-generation-style-rules/references/style-priority.md"
          ],
          "agents": [],
          "has_license": false,
          "focus_points": [
            "优先检查 description 是否具体到触发信号，而不是只写抽象用途。",
            "检查 references 是否足以承接复杂场景，避免 SKILL.md 过厚或过空。",
            "重点看它是否能并行生效，并且不抢位点域或审查域职责。"
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
          "item_order": 2,
          "auto_trigger": "当新增或修改代码、调整功能、修复 Bug、补测试支撑代码或整理实现细节时触发。负责约束改动范围、删除无关修改并保持变更聚焦，同时要求编码前显式说明假设和成功标准、实现时坚持简单优先与外科手术式改动；默认反对过度封装和过度抽象接口，大多数代码不需要额外封装或抽象接口，只有存在真实复用、边界隔离、复杂度下降或多实现替换证据时才允许新增封装 / 接口层；不要用它代替可读性、风格一致性、代码归位或测试规范等相邻 skill。",
          "core_responsibility": "严控代码变更范围，杜绝无关修改、冗余改动和过度优化，保证每次变更聚焦单一目标，降低回归风险和排查难度；简单处理禁止顺手引入无收益接口抽象。",
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
          "id": "code-context-resync-rules",
          "name": "code-context-resync-rules",
          "title": "代码上下文重同步规则",
          "status": "implemented",
          "status_label": "已实现",
          "domain_id": "baseline",
          "domain_label": "编码基线域",
          "domain_description": "开始编码即并行生效的基础质量规则",
          "domain_order": 5,
          "item_order": 3,
          "auto_trigger": "当继续修改已有代码时，若发现“当前文件内容与 AI 记忆/上次读取内容不一致”（例如用户手动改过、他人提交已更新、补丁上下文失效）自动触发。负责先重读最新代码并以当前文件为唯一真实基线，在保留用户手动修改的前提下继续实现目标，禁止按旧记忆覆盖还原代码；适用于任意代码文件的二次修改、续改、补丁失败重试和上下文漂移场景。",
          "core_responsibility": "先重读最新文件并以当前内容为基线增量合并，禁止按旧记忆覆盖用户手动改动。",
          "skill_path": "code-context-resync-rules/SKILL.md",
          "directory_path": "code-context-resync-rules",
          "directory": "code-context-resync-rules",
          "sections": [
            "核心原则",
            "自动触发信号",
            "进入后先做什么",
            "默认执行流程",
            "强制禁止项",
            "需要暂停并确认的条件",
            "通过 / 驳回标准",
            "与其他规则的关系"
          ],
          "references": [],
          "agents": [
            "code-context-resync-rules/agents/openai.yaml"
          ],
          "has_license": false,
          "focus_points": [
            "优先检查 description 是否具体到触发信号，而不是只写抽象用途。",
            "检查 references 是否足以承接复杂场景，避免 SKILL.md 过厚或过空。",
            "重点看它是否能并行生效，并且不抢位点域或审查域职责。",
            "当前没有 references，可考虑补最小示例或边界文档以降低后续维护成本。"
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
          "item_order": 4,
          "auto_trigger": "当新增或修改业务代码、工具代码、服务代码、脚本代码或 Bug 修复逻辑时触发。负责约束函数结构、逻辑顺序、复杂度和可维护性，并在功能不变前提下优先让最近改动代码表达更清楚、更直接；要求写库、发请求、改状态、发事件等副作用必须从命名和位置可见，避免 query 与 command 混成一个隐蔽职责；当单文件达到 500 行及以上且仍持续新增功能时，必须触发拆分评估；结构调整落地后必须联动 `comment-placement-granularity-rules` 与 `comment-completion-gate-rules` 完成改动位点注释检查与补齐；业务方法禁止直接用 JSON 字符串 key 取字段，必须经 DTO/对象解析层访问；Go 接入第三方 API 时默认使用结构体解析响应，禁止长期使用 map + key 硬编码解析；同时要求已有公共工具优先复用，禁止同语义重复封装；大多数代码默认不需要封装或抽象接口，抽象只有在简单接口隐藏真实复杂度时才有价值，简单场景禁止为了“解耦”“可测试”“以后扩展”无脑新增接口层、接口实现对、helper、factory、manager、adapter 或单实现包装；不要用它代替最小改动、风格一致性、注释规则或代码归位规则。",
          "core_responsibility": "保证函数结构清晰、逻辑顺序自然、副作用显式和复杂度可控，并用深模块口径拦截浅封装与无脑接口抽象。",
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
            "格式化日志示例",
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
          "item_order": 5,
          "auto_trigger": "当新增或修改任意代码文件、脚本文件、配置型代码或测试代码时触发。负责跟随项目现有写法，并在本轮已触发 `code-generation-style-rules` 时依据其产出的代码风格契约检查局部一致性，避免局部风格跳变和个人偏好入侵；不要用它代替最小改动、可读性、注释规范、代码归位规则或代码生成风格契约入口。",
          "core_responsibility": "跟随项目现有风格，不引入风格跳变。",
          "skill_path": "code-style-consistency-rules/SKILL.md",
          "directory_path": "code-style-consistency-rules",
          "directory": "code-style-consistency-rules",
          "sections": [
            "Skill 作用与适用场景",
            "Go 路由风格约定",
            "Go 局部变量声明风格约定",
            "Go 函数签名风格约定",
            "Go 代码排版补充约定",
            "Go 编码规则清单",
            "自动触发信号",
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
            "code-style-consistency-rules/references/go-coding-rules.md",
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
          "item_order": 6,
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
          "item_order": 7,
          "auto_trigger": "当新增或修改后端、前端或脚本代码中的注释、步骤说明、复杂逻辑解释、临时诊断说明或测试说明，且团队要求注释必须使用中文（除标准协议字段/第三方固定错误原文外）时触发。负责中文注释的语言选择、表达方式和禁忌；不要把它代替注释位置与颗粒度规则。",
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
          "id": "comment-placement-granularity-rules",
          "name": "comment-placement-granularity-rules",
          "title": "注释放置与颗粒度规则",
          "status": "implemented",
          "status_label": "已实现",
          "domain_id": "baseline",
          "domain_label": "编码基线域",
          "domain_description": "开始编码即并行生效的基础质量规则",
          "domain_order": 5,
          "item_order": 8,
          "auto_trigger": "【强制自动触发】本轮发生代码新增/修改时，默认与 `comment-completion-gate-rules` 联动命中；当需要判断注释该不该写、写在哪里、写多细时必须命中。若用户提“补充注释/加注释”但未指定细节，也要默认命中本 skill 做注释落点判定。负责注释放置与颗粒度（含字段注释、边界注释、过期注释治理），不代替中文表达、补齐闸门或 Swagger 规则。",
          "core_responsibility": "统一注释位置、颗粒度、字段相关注释和过期注释治理。",
          "skill_path": "comment-placement-granularity-rules/SKILL.md",
          "directory_path": "comment-placement-granularity-rules",
          "directory": "comment-placement-granularity-rules",
          "sections": [
            "Skill 作用与适用场景",
            "自动触发信号",
            "进入后先做什么",
            "默认执行流程",
            "权责边界与不负责事项",
            "需要暂停并确认的条件",
            "执行通过 / 驳回标准",
            "references 读取规则"
          ],
          "references": [
            "comment-placement-granularity-rules/references/comment-examples.md",
            "comment-placement-granularity-rules/references/comment-granularity.md",
            "comment-placement-granularity-rules/references/comment-placement.md"
          ],
          "agents": [
            "comment-placement-granularity-rules/agents/openai.yaml"
          ],
          "has_license": false,
          "focus_points": [
            "优先检查 description 是否具体到触发信号，而不是只写抽象用途。",
            "检查 references 是否足以承接复杂场景，避免 SKILL.md 过厚或过空。",
            "重点看它是否能并行生效，并且不抢位点域或审查域职责。"
          ]
        },
        {
          "id": "comment-completion-gate-rules",
          "name": "comment-completion-gate-rules",
          "title": "注释补齐闸门规则",
          "status": "implemented",
          "status_label": "已实现",
          "domain_id": "baseline",
          "domain_label": "编码基线域",
          "domain_description": "开始编码即并行生效的基础质量规则",
          "domain_order": 5,
          "item_order": 9,
          "auto_trigger": "【强制自动触发】只要本轮发生任意代码新增/修改，或用户提到“补充注释/只补注释/注释完善/补下注释/加注释”，必须命中本 skill。即使用户只发一句“补充注释”，也必须立即触发并输出注释补齐核对结果。负责改动位点注释补齐闸门：函数头 `[参数]`/`[返回]`/`最近修改时间`、方法体步骤编号、补丁原因注释、函数/补丁核对清单。前端文件与后端文件同等纳入检查。缺任一项不得收口。仅负责补齐闸门，不代替中文表达、注释放置颗粒度或 Swagger 注解规则。",
          "core_responsibility": "统一改动位点注释补齐、函数头元信息、步骤编号和注释缺失阻断闸门。",
          "skill_path": "comment-completion-gate-rules/SKILL.md",
          "directory_path": "comment-completion-gate-rules",
          "directory": "comment-completion-gate-rules",
          "sections": [
            "Skill 作用与适用场景",
            "强制规则：补注释优先范围",
            "强制门禁：改动位点注释补齐",
            "强制门禁：前端必注释位点",
            "强制规则：步骤编号",
            "强制规则：函数头元信息",
            "强制规则：函数注释核对清单（可执行闸门）",
            "强制规则：字段/结构体字面量注释核对清单",
            "强制规则：补丁逻辑注释（做了什么 + 为什么）",
            "自动触发信号",
            "进入后先做什么",
            "默认执行流程",
            "权责边界与不负责事项",
            "需要暂停并确认的条件",
            "执行通过 / 驳回标准",
            "references 读取规则"
          ],
          "references": [
            "comment-completion-gate-rules/references/comment-completion-priority.md",
            "comment-completion-gate-rules/references/comment-examples.md",
            "comment-completion-gate-rules/references/comment-function-metadata.md",
            "comment-completion-gate-rules/references/comment-step-numbering-gate.md"
          ],
          "agents": [
            "comment-completion-gate-rules/agents/openai.yaml"
          ],
          "has_license": false,
          "focus_points": [
            "优先检查 description 是否具体到触发信号，而不是只写抽象用途。",
            "检查 references 是否足以承接复杂场景，避免 SKILL.md 过厚或过空。",
            "重点看它是否能并行生效，并且不抢位点域或审查域职责。"
          ]
        },
        {
          "id": "windows-encoding-rules",
          "name": "windows-encoding-rules",
          "title": "Windows 中文编码防护规则",
          "status": "implemented",
          "status_label": "已实现",
          "domain_id": "baseline",
          "domain_label": "编码基线域",
          "domain_description": "开始编码即并行生效的基础质量规则",
          "domain_order": 5,
          "item_order": 10,
          "auto_trigger": "当任务运行在 Windows（Git Bash / bash、PowerShell 或 CMD）且涉及任意代码、文档、配置、脚本、测试资产或生成文本的读写、日志追加、README/Markdown 修改、脚本输出重定向、Git 提交信息或终端显示时触发。用于预防与修复中文乱码（mojibake）、统一跨平台 UTF-8 写入策略，并在落盘前做编码自检；尤其适用于“看到乱码”“中文变成问号/锟斤拷/Ãxx”“同文件中英正常但中文异常”“追加写入后部分行乱码”“担心文件被 GBK/ANSI/默认编码写入”等场景。",
          "core_responsibility": "统一 Windows 终端与文件中文编码防护，避免中文乱码落盘。",
          "skill_path": "windows-encoding-rules/SKILL.md",
          "directory_path": "windows-encoding-rules",
          "directory": "windows-encoding-rules",
          "sections": [
            "自动触发信号",
            "进入后先做什么",
            "Windows 防错基线",
            "推荐执行流程",
            "落盘命令模板",
            "通过 / 驳回标准",
            "边界"
          ],
          "references": [],
          "agents": [
            "windows-encoding-rules/agents/openai.yaml"
          ],
          "has_license": false,
          "focus_points": [
            "优先检查 description 是否具体到触发信号，而不是只写抽象用途。",
            "检查 references 是否足以承接复杂场景，避免 SKILL.md 过厚或过空。",
            "重点看它是否能并行生效，并且不抢位点域或审查域职责。",
            "当前没有 references，可考虑补最小示例或边界文档以降低后续维护成本。"
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
          "auto_trigger": "当新增或修改工具类、通用方法、公共组件、工具函数、通用常量或复用代码时触发。负责统一公共工具代码的判定标准、存放位置、调用方式和边界；`utils` / `common` / `global` / `middleware` 这类通用包根目录应先按职责拆子目录，再在子目录放实现文件，避免循环依赖和命名冲突；同时强制执行“先检索后新增”，禁止同语义工具重复封装（已存在可复用实现时必须复用，不得再新写一份）；对被多处复用的通用代码执行“7天冻结”策略：最近修改时间超过7天的默认只允许新增能力，不允许直接修改既有行为；最近7天内新增/修改的通用代码可继续迭代；简单处理禁止为了“未来扩展”或“统一模式”提前抽公共接口 / 接口实现对；不要用它代替业务逻辑抽象、包结构规则或具体实现细则。",
          "core_responsibility": "统一通用工具代码的编写规范、复用标准、存放位置和调用方式，避免重复造轮子，保证公共代码的通用性、稳定性和可维护性。",
          "skill_path": "common-util-rules/SKILL.md",
          "directory_path": "common-util-rules",
          "directory": "common-util-rules",
          "sections": [
            "复用红线（强制）",
            "Skill 作用与适用场景",
            "自动触发信号",
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
          "auto_trigger": "当新增或修改数据库、表、字段、索引、唯一约束、外键、迁移脚本、DDL、实体结构、schema 定义或自动建库/建表/建索引启动逻辑时自动触发。负责统一数据库结构变更、迁移安全、兼容性和回滚边界；自动初始化必须覆盖库、表、索引三类对象，启动时若支持自动建库和自动建表，也必须同步具备自动检查并创建缺失索引的流程；数据库表模型必须每张表单独一个文件，自动建表/迁移逻辑、自动建索引逻辑也必须分别放在独立文件中；数据库的字段必须要定义数据类型、默认值、是否需要索引、字段 CHARSET=utf8mb4、ENGINE=InnoDB、注释说明等写清楚，不要遗漏；所有金额相关的要强制使用字符串，避免任何出现精度问题的情况；所有表必须包含 created_at 和 updated_at 字段，由数据库自动管理；必须冗余一个毫秒级时间戳的创建时间，避免数据库的时区问题影响不同的时间格式；所有表必须包含逻辑删除字段，1 的状态标识删除，不是 1 代表正常非删除状态，默认 0=非删除；否则会导致自动创建表出现不可控的因素；避免把查询实现、事务控制和业务逻辑混进结构变更；不要用它代替 database-query-rules、项目配置约束或发布回滚流程。",
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
          "auto_trigger": "当新增或修改 SQL、Repository、DAO、Mapper、QueryBuilder、事务、锁、批量 CRUD、分页查询时自动触发。负责统一数据库访问实现、查询性能、事务与锁边界；GORM 查询、统计、更新、创建、保存必须显式使用 `Model(&models.X{})` 或等价方式声明目标表模型，禁止依赖 `Find(&slice)`、`First(&obj)`、`Create(&obj)`、`Save(&obj)` 的类型推导；避免把 schema 设计、缓存策略和业务逻辑混进数据访问层；不要用它代替 database-schema-rules、缓存策略约束或业务规则本身。",
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
            "结构体解析示例（Go）",
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
            "结构体解析示例（Go）",
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
          "auto_trigger": "当新增或修改后端 HTTP API、Swagger/OpenAPI 框架接入、接口文档注解/注释、Swagger 调试入口、接口分组标签、文档暴露路径或 Swagger 环境开关时触发。负责统一 Swagger/OpenAPI 框架选型边界、接口文档最小必填项、请求/响应同步、调试可用性和暴露安全规则；对存在 HTTP API 且需要联调/调试的后端项目，默认要求使用统一的 Swagger/OpenAPI 方案；本 skill 只负责后端代码中的 Swagger/OpenAPI 框架接入、注解与调试入口，当用户要求生成、更新、刷新、补齐 swag，或导出 OpenAPI/Swagger/Apifox YAML 到 swag/ 目录时，属于文档产物维护，必须转交 swag-openapi-maintainer-rules；不要用它代替 swag-openapi-maintainer-rules、api-endpoint-rules、api-request-rules、api-response-rules、普通业务注释规则或功能验证。",
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
          "auto_trigger": "当新增或修改日志、logger、trace、span、审计日志、脱敏字段、排障字段、日志配置文件或链路透传逻辑时触发。负责统一日志与链路追踪规则，后端日志必须使用项目日志框架且不得使用控制台打印，并通过配置文件管理日志参数；业务日志默认必须使用中文表达，只有协议字段、固定 key、第三方固定原文等少数例外可以保留原文；日志初始化必须在 LoadConfig 之后且仅初始化一次，禁止空配置预初始化；不要用它代替错误处理、响应结构或长期监控告警策略。",
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
            "日志排版规范（新增）",
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
          "auto_trigger": "创建具有鲜明风格、达到生产级质量的高品质前端界面。当用户要求构建 Web 组件、页面或前端应用，或进行前端 UI、组件、样式的调整/改进/界面 Bug 修复时优先使用这个 skill。它会生成有创意、打磨精细的代码，并避免出现千篇一律的 AI 模板化审美。",
          "core_responsibility": "生成具有鲜明风格、生产级质量的前端界面，并在与内部前端规则冲突时优先作为主导 skill。",
          "skill_path": "frontend-design/SKILL.md",
          "directory_path": "frontend-design",
          "directory": "frontend-design",
          "sections": [
            "触发后强制联动",
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
          "auto_trigger": "当新增或修改 React、Vue、前端组件拆分、组件目录归属、props 设计、emits 设计、slots 设计、状态归属、事件上抛、组合方式、hooks、composables、复用边界、受控/非受控切换、渲染副作用或客户端展示逻辑时自动触发。负责组件边界、状态边界、接口契约、组合复用和渲染可维护性；若任务同时涉及前端 UI/组件/样式调整、体验改进或界面 Bug 修复，优先让位给 `frontend-design`，本 skill 仅补充组件工程边界。",
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
          "auto_trigger": "当新增或修改前端页面、页面布局、主题样式、配色、字体、图标、卡片、弹窗、表单、表格、图表、导航、空状态、动画、响应式样式、暗黑模式、设计 token、Tailwind 类名、CSS/SCSS/LESS、`.tsx`/`.jsx`/`.vue`/`.html` 中影响界面视觉和交互体验的代码时自动触发，尤其适用于首页、营销页、品牌展示页、数据面板和需要明确设计方向的前端界面。负责页面视觉方向、信息层级、交互反馈、可访问性、响应式适配和交付前 UI 自审；内置合并后的 UI/UX 设计种子数据与搜索脚本，可在风格不明时辅助定方向；若任务属于前端 UI/组件/样式调整、改进或界面 Bug 修复，优先让位给 `frontend-design`，本 skill 主要做视觉规则补充；不要用它代替纯组件工程拆分、状态管理、接口接线或后端规则。",
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
      "implemented_count": 2,
      "planned_count": 0,
      "seed_count": 0,
      "total_count": 2,
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
          "auto_trigger": "【强制自动触发】当功能代码已经完成、准备进入测试前验证时触发。作为唯一自动测试前实现闸门，统一检查 4 组内容：实现质量、格式清理、语法/类型/引用、目录归位/分层边界。负责检查实现是否符合可读性优先、单一职责、命名语义化、注释完整、错误处理明确、日志可追溯、依赖使用审慎、魔法值治理、冗余逻辑清理和编码规范等实现质量要求，并在功能不变前提下检查最近改动代码是否还存在可直接收口的表达层冗余；必须核验本轮改动是否完成 `comment-placement-granularity-rules` 与 `comment-completion-gate-rules` 的改动位点注释检查与补齐；必须完成基础格式、语法/类型/引用、目录归位与依赖方向的测试前收口；必须识别 500 行及以上且持续膨胀的文件并要求拆分或给出拆分方案；必须检查“可复用公共工具是否被重复封装”并拦截重复造轮子；必须检查“最近修改超过7天的高复用通用代码是否被直接修改旧行为”，命中时要求改为新增兼容路径；Go 场景下还需在实现自审阶段扫描 `doc/5-tests/` 外 `*_test.go` 禁放问题，以及本轮改动是否把业务实现直接落在 `internal/service/*.go` 根目录文件，是否把请求/响应/第三方结果结构体散落在 `internal/service` 实现文件，是否在函数/方法内使用 `var (...)` 分组声明局部变量，是否把多参数函数签名直接写成多行参数列表，是否把第三方 API 响应长期用 `map[string]any` + key 硬编码解析；若本轮改动涉及后端 HTTP API，还必须检查 Swagger/OpenAPI 是否同步更新；默认优先并行；不要用它代替功能验证规则。",
          "core_responsibility": "对刚完成的实现做一次测试前静态自审与收口。",
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
            "implementation-review-rules/references/format-cleanup-checks.md",
            "implementation-review-rules/references/placement-and-dependency-checks.md",
            "implementation-review-rules/references/review-boundaries.md",
            "implementation-review-rules/references/review-examples.md",
            "implementation-review-rules/references/review-scope.md",
            "implementation-review-rules/references/syntax-and-reference-checks.md"
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
          "id": "project-change-review-rules",
          "name": "project-change-review-rules",
          "title": "项目当前改动总审查规则",
          "status": "implemented",
          "status_label": "已实现",
          "domain_id": "review",
          "domain_label": "编码审查域",
          "domain_description": "测试前的静态自审、语法检查、清理归位",
          "domain_order": 7,
          "item_order": 2,
          "auto_trigger": "当前改动总审查 skill。两类场景自动成立：用户明确点名 `$project-change-review-rules`、`project-change-review-rules`、说出“审核当前改动/当前 diff”，或本轮存在代码改动且准备最终收口。负责只读审查当前项目未提交改动、已暂存改动和可见新增文件，覆盖需求边界、缺陷、遗漏、安全风险、重复逻辑、未按已命中 skill 规则实现、注释缺失或乱码、日志打印不合规、工具包/公共方法复用不足、代码可读性差、补丁式修补、测试与验证缺口；输出按严重级别排序的问题清单，不直接改代码、不格式化、不提交。",
          "core_responsibility": "对当前工作区 diff 做总审查，补抓边界、风险、遗漏和阻断项。",
          "skill_path": "project-change-review-rules/SKILL.md",
          "directory_path": "project-change-review-rules",
          "directory": "project-change-review-rules",
          "sections": [
            "目标",
            "快速流程",
            "审查矩阵",
            "专门 Skill 联动",
            "读取与证据规则",
            "输出格式",
            "驳回标准",
            "执行结果归档要求",
            "References"
          ],
          "references": [
            "project-change-review-rules/references/checklist.md",
            "project-change-review-rules/references/report-template.md"
          ],
          "agents": [
            "project-change-review-rules/agents/openai.yaml"
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
      "implemented_count": 11,
      "planned_count": 0,
      "seed_count": 0,
      "total_count": 11,
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
          "auto_trigger": "当准备进入测试阶段，需要确定测什么、先测什么、测到什么程度、哪些路径必须覆盖、哪些风险只能记录待补测时触发。负责测试优先级、测试类型组合、覆盖范围和资源收口；必须以 `artifact-storage-rules` 与 `test-task-root-layout-rules` 为基准，把策略摘要统一记录到中央约定的测试任务主说明 `README.md` 中，并在需要拆成多轮独立测试时给出多个时间戳根目录方案；若策略涉及 Go 可编译测试路径，还必须同步遵循 `go-test-compile-path-rules`；同时强制禁止为了测试目的污染生产代码（新增测试专用方法、测试专用数据、测试专用结构体字段等）。不要用它代替具体测试资源管理或验证执行 skill。",
          "core_responsibility": "决定测试层级和覆盖重点。",
          "skill_path": "test-strategy-rules/SKILL.md",
          "directory_path": "test-strategy-rules",
          "directory": "test-strategy-rules",
          "sections": [
            "测试隔离红线（强制）",
            "Skill 作用与适用场景",
            "自动触发信号",
            "进入后先做什么",
            "默认执行流程",
            "权责边界与不负责事项",
            "需要暂停并确认的条件",
            "执行通过 / 驳回标准",
            "执行结果归档要求",
            "references 读取规则",
            "项目联调强制规则（新增）",
            "本地环境配置发现与连接（强制）",
            "测试样本分布优先（强制）"
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
          "id": "test-task-root-layout-rules",
          "name": "test-task-root-layout-rules",
          "title": "测试任务根布局规则",
          "status": "implemented",
          "status_label": "已实现",
          "domain_id": "test",
          "domain_label": "测试域",
          "domain_description": "策略、资源、功能验证、浏览器联动与回归",
          "domain_order": 8,
          "item_order": 2,
          "auto_trigger": "当为当前需求、当前 Bug 或当前验证任务新增测试任务目录，或需要决定 `doc/5-tests/` 根目录下的当天时间戳根目录、中文说明目录和 ASCII 真实代码路径镜像布局时触发。负责统一测试任务根目录创建、当天时间戳校验、中文 README 说明目录和真实测试资产镜像布局；不要用它代替散落测试资产迁移、Go 编译路径冲突处理、测试命名规则或测试程序实现规则。",
          "core_responsibility": "统一测试任务根布局。",
          "skill_path": "test-task-root-layout-rules/SKILL.md",
          "directory_path": "test-task-root-layout-rules",
          "directory": "test-task-root-layout-rules",
          "sections": [
            "Skill 作用与适用场景",
            "自动触发信号",
            "强制规则",
            "默认执行流程",
            "权责边界与不负责事项",
            "通过 / 驳回标准",
            "执行结果归档要求",
            "references 读取规则"
          ],
          "references": [
            "test-task-root-layout-rules/references/task-root-layout.md"
          ],
          "agents": [
            "test-task-root-layout-rules/agents/openai.yaml"
          ],
          "has_license": false,
          "focus_points": [
            "优先检查 description 是否具体到触发信号，而不是只写抽象用途。",
            "检查 references 是否足以承接复杂场景，避免 SKILL.md 过厚或过空。",
            "重点看测试策略、资源、功能验证、联调、回归是否已经拆开。"
          ]
        },
        {
          "id": "test-scattered-asset-location-rules",
          "name": "test-scattered-asset-location-rules",
          "title": "测试资产禁散落规则",
          "status": "implemented",
          "status_label": "已实现",
          "domain_id": "test",
          "domain_label": "测试域",
          "domain_description": "策略、资源、功能验证、浏览器联动与回归",
          "domain_order": 8,
          "item_order": 3,
          "auto_trigger": "当发现测试脚本、测试数据、mock、fixture、测试说明、日志或临时验证资产散落在 `doc/5-tests/` 根目录之外，或混放进业务目录、仓库根目录、文档目录和非测试目录时触发。负责识别、阻断并迁移散落测试资产，统一收拢到中央测试根目录下的正确任务目录；不要用它代替测试任务根目录创建、Go 编译路径禁放处理、测试命名规则或测试程序实现规则。",
          "core_responsibility": "收拢散落测试资产。",
          "skill_path": "test-scattered-asset-location-rules/SKILL.md",
          "directory_path": "test-scattered-asset-location-rules",
          "directory": "test-scattered-asset-location-rules",
          "sections": [
            "Skill 作用与适用场景",
            "自动触发信号",
            "强制规则",
            "默认执行流程",
            "权责边界与不负责事项",
            "通过 / 驳回标准",
            "执行结果归档要求",
            "references 读取规则"
          ],
          "references": [
            "test-scattered-asset-location-rules/references/scattered-asset-migration.md"
          ],
          "agents": [
            "test-scattered-asset-location-rules/agents/openai.yaml"
          ],
          "has_license": false,
          "focus_points": [
            "优先检查 description 是否具体到触发信号，而不是只写抽象用途。",
            "检查 references 是否足以承接复杂场景，避免 SKILL.md 过厚或过空。",
            "重点看测试策略、资源、功能验证、联调、回归是否已经拆开。"
          ]
        },
        {
          "id": "go-test-compile-path-rules",
          "name": "go-test-compile-path-rules",
          "title": "Go 测试编译路径规则  只在“Go 测试路径会影响编译和扫描链路”这个问题上使用本 skill。",
          "status": "implemented",
          "status_label": "已实现",
          "domain_id": "test",
          "domain_label": "测试域",
          "domain_description": "策略、资源、功能验证、浏览器联动与回归",
          "domain_order": 8,
          "item_order": 4,
          "auto_trigger": "当 Go 项目中的测试路径会进入编译链路、出现源码目录 `*_test.go`、中文可编译路径，或存在白盒同包测试诉求时触发。负责统一 Go 测试可编译路径必须保持 ASCII、源码目录禁放 `*_test.go`、白盒诉求改用 seam 方案，并把测试资产收回中央测试根目录；不要用它代替测试任务根目录创建、散落测试资产迁移、测试命名规则或测试程序实现规则。",
          "core_responsibility": "统一 Go 测试可编译路径。",
          "skill_path": "go-test-compile-path-rules/SKILL.md",
          "directory_path": "go-test-compile-path-rules",
          "directory": "go-test-compile-path-rules",
          "sections": [
            "Skill 作用与适用场景",
            "自动触发信号",
            "强制规则",
            "默认执行流程",
            "权责边界与不负责事项",
            "通过 / 驳回标准",
            "references 读取规则"
          ],
          "references": [
            "go-test-compile-path-rules/references/go-compile-path.md"
          ],
          "agents": [
            "go-test-compile-path-rules/agents/openai.yaml"
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
          "item_order": 5,
          "auto_trigger": "当创建或修改测试时间戳根目录、中文说明目录、测试文件、测试脚本、测试数据目录、fixture 目录、mock 目录时触发。负责统一测试目录与文件命名规范，保证名称可读、可检索、与业务目标一致；必须以 `artifact-storage-rules` 与 `test-task-root-layout-rules` 为基础，遵循中央约定的时间戳根目录、中文说明目录和真实代码路径镜像目录命名规则；涉及 Go 可编译路径时，还必须服从 `go-test-compile-path-rules`；同时强制禁止为了测试目的污染生产代码（新增测试专用方法、测试专用数据、测试专用结构体字段等）。不要用它代替 test-task-root-layout-rules、test-program-rules、test-doc-rules 或功能验证规则。",
          "core_responsibility": "统一测试目录和文件命名。",
          "skill_path": "test-naming-rules/SKILL.md",
          "directory_path": "test-naming-rules",
          "directory": "test-naming-rules",
          "sections": [
            "测试隔离红线（强制）",
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
          "item_order": 6,
          "auto_trigger": "当新增或修改测试程序、模拟程序、验证脚本、数据构造脚本、测试辅助代码时触发。负责统一测试程序职责拆分、辅助代码边界和长期保留策略；必须以 `artifact-storage-rules` 与 `test-task-root-layout-rules` 为基准，把真实测试代码、脚本、mock、fixture 和执行产物统一落在中央约定的测试时间戳根目录下的 ASCII 真实代码路径镜像目录中；若发现资产散落在 `doc/5-tests/` 根目录之外，应先按 `test-scattered-asset-location-rules` 收拢；Go 场景下还必须遵循 `go-test-compile-path-rules`，避免中文进入会被 Go 工具链编译的路径；测试脚本执行时必须向控制台输出关键过程日志，便于观察执行进度与定位失败步骤；Go 场景下白盒/黑盒/集成测试都遵循同一落点规则，源码目录禁止 `*_test.go`，白盒诉求通过 seam 解决；第三方 API 文档缺失响应模型时，必须先用测试脚本探测真实响应，再反推结构体定义；同时强制禁止为了测试目的污染生产代码（新增测试专用方法、测试专用数据、测试专用结构体字段等）。不要用它代替 test-task-root-layout-rules、test-naming-rules、test-doc-rules、bug-runtime-debug-rules 或功能验证规则。",
          "core_responsibility": "统一测试程序职责和辅助脚本边界。",
          "skill_path": "test-program-rules/SKILL.md",
          "directory_path": "test-program-rules",
          "directory": "test-program-rules",
          "sections": [
            "测试隔离红线（强制）",
            "Skill 作用与适用场景",
            "自动触发信号",
            "进入后先做什么",
            "默认执行流程",
            "权责边界与不负责事项",
            "需要暂停并确认的条件",
            "执行通过 / 驳回标准",
            "执行结果归档要求",
            "references 读取规则",
            "写接口测试脚本的过程日志约定（强制）"
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
          "item_order": 7,
          "auto_trigger": "当新增或修改测试 README、验证说明、测试报告、覆盖说明、测试执行记录时触发。负责统一测试文档的最小结构、记录字段、主文档入口和归档方式；必须以 `artifact-storage-rules` 与 `test-task-root-layout-rules` 为基准，使用中央约定的测试任务主说明 `README.md` 作为中文主说明入口，并把额外文档放到同一时间戳根目录下的 ASCII 真实代码路径镜像目录中；同时强制禁止为了测试目的污染生产代码（新增测试专用方法、测试专用数据、测试专用结构体字段等）。不要用它代替 test-task-root-layout-rules、test-program-rules、functional-validation-rules 或 test-regression-rules。",
          "core_responsibility": "统一测试说明文档结构。",
          "skill_path": "test-doc-rules/SKILL.md",
          "directory_path": "test-doc-rules",
          "directory": "test-doc-rules",
          "sections": [
            "测试隔离红线（强制）",
            "Skill 作用与适用场景",
            "自动触发信号",
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
          "item_order": 8,
          "auto_trigger": "面向 AI 代理的浏览器自动化 CLI。当用户需要与网站交互时使用，包括打开页面、填写表单、点击按钮、截图、提取数据、测试 Web 应用，或执行任何浏览器自动化任务。典型触发语句包括“打开一个网站”“填写表单”“点击按钮”“截个图”“抓取页面数据”“测试这个 Web 应用”“登录某个网站”“自动化浏览器操作”，以及任何需要通过程序控制浏览器完成的任务。",
          "core_responsibility": "统一浏览器自动化测试与页面交互执行。",
          "skill_path": "agent-browser/SKILL.md",
          "directory_path": "agent-browser",
          "directory": "agent-browser",
          "sections": [
            "核心工作流",
            "实战经验优先流程（新增）",
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
            "测试截图清理（强制）",
            "Ref 生命周期（重要）",
            "带标注的截图（Vision 模式）",
            "语义定位器（Refs 的替代方案）",
            "JavaScript 求值（eval）",
            "配置文件",
            "深入文档",
            "浏览器引擎选择",
            "观测面板（Observability Dashboard）",
            "可直接使用的模板",
            "项目联调强制规则（新增）"
          ],
          "references": [
            "agent-browser/references/authentication.md",
            "agent-browser/references/browser-operation-lessons.md",
            "agent-browser/references/commands.md",
            "agent-browser/references/profiling.md",
            "agent-browser/references/proxy-support.md",
            "agent-browser/references/screenshot-cleanup.md",
            "agent-browser/references/session-management.md",
            "agent-browser/references/snapshot-refs.md",
            "agent-browser/references/tapd-workflow-automation.md",
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
          "item_order": 9,
          "auto_trigger": "当需要验证新功能、修改后的功能、接口行为、页面交互、输入输出结果是否满足当前需求、当前变更和验收标准时触发。负责界定本次功能验证范围、验证步骤、通过驳回标准和结论留痕；必须以 `artifact-storage-rules` 与 `test-task-root-layout-rules` 为基准，把功能验证结论写回中央约定的测试任务主说明 `README.md`，并把详细执行证据放到同一时间戳根目录下的 ASCII 真实代码路径镜像目录中；若该镜像路径会进入 Go 编译链路，还必须同步遵循 `go-test-compile-path-rules`；同时强制禁止为了测试目的污染生产代码（新增测试专用方法、测试专用数据、测试专用结构体字段等）。不要用它代替 test-strategy-rules、test-task-root-layout-rules 或 test-regression-rules。",
          "core_responsibility": "负责当前需求对应的功能正确性验证。",
          "skill_path": "functional-validation-rules/SKILL.md",
          "directory_path": "functional-validation-rules",
          "directory": "functional-validation-rules",
          "sections": [
            "测试隔离红线（强制）",
            "Skill 作用与适用场景",
            "自动触发信号",
            "进入后先做什么",
            "默认执行流程",
            "权责边界与不负责事项",
            "需要暂停并确认的条件",
            "执行通过 / 驳回标准",
            "执行结果归档要求",
            "references 读取规则",
            "项目联调强制规则（新增）",
            "功能验证样本分布（强制）"
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
          "item_order": 10,
          "auto_trigger": "当 Bug 修复、原有功能迭代、公共模块修改、共享逻辑调整、接口兼容性变化后准备执行测试时触发。负责判定回归范围、选择回归用例、验证兼容性影响并输出回归结论；必须以 `artifact-storage-rules` 与 `test-task-root-layout-rules` 为基准，把回归结论统一写回中央约定的测试任务主说明 `README.md`，并把详细回归案例、执行证据和补充说明放到同一时间戳根目录下的 ASCII 真实代码路径镜像目录中；若该镜像路径会进入 Go 编译链路，还必须同步遵循 `go-test-compile-path-rules`；同时强制禁止为了测试目的污染生产代码（新增测试专用方法、测试专用数据、测试专用结构体字段等）。不要用它代替 functional-validation-rules、test-strategy-rules 或测试资源管理类规则。",
          "core_responsibility": "明确回归测试的范围、用例选取、验证要点，针对改动点关联的功能、上下游链路做全覆盖验证，防止修复旧 Bug 引入新问题，保障功能兼容性。",
          "skill_path": "test-regression-rules/SKILL.md",
          "directory_path": "test-regression-rules",
          "directory": "test-regression-rules",
          "sections": [
            "测试隔离红线（强制）",
            "Skill 作用与适用场景",
            "自动触发信号",
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
          "id": "project-release-test-rules",
          "name": "project-release-test-rules",
          "title": "项目上线接口测试门禁规则",
          "status": "implemented",
          "status_label": "已实现",
          "domain_id": "test",
          "domain_label": "测试域",
          "domain_description": "策略、资源、功能验证、浏览器联动与回归",
          "domain_order": 8,
          "item_order": 11,
          "auto_trigger": "当需要做上线前项目级全接口测试、替代人工接口回归验证、生成上线接口测试门禁结论时触发。负责在每次执行前扫描并持续更新项目基线资产库（接口清单、Swagger/OpenAPI 双索引、参数来源、依赖图、可复用参数、场景目录、脚本适配和历史结论）、规划测试范围、按依赖图构造请求参数并执行接口验证、给出 agent 判定的接口级结果和上线放行结论；所有测试资产落地到 `doc/5-tests/` 对应时间戳根目录，强制要求请求参数和简要响应为 JSON 字符串，禁止接口明细输出为 Markdown 表格。",
          "core_responsibility": "负责每次执行前扫描并更新接口基线，完成项目级核心接口门禁测试、结论归档与最终放行输入。",
          "skill_path": "project-release-test-rules/SKILL.md",
          "directory_path": "project-release-test-rules",
          "directory": "project-release-test-rules",
          "sections": [
            "测试隔离红线（强制，和现有测试域规则一致）",
            "Skill 作用与适用场景",
            "自动触发信号",
            "首次触发冷启动规则（强制）",
            "接口基线扫描规则（强制）",
            "Swagger/OpenAPI 双索引同步规则（强制）",
            "基线漂移处理规则（强制）",
            "基线资产库持续更新规则（强制）",
            "参数依赖与复用规则（强制）",
            "可复用脚本工具箱优先规则（强制）",
            "进入后先做什么",
            "默认执行流程",
            "权责边界与不负责事项",
            "需要暂停并确认的条件",
            "执行通过 / 驳回标准",
            "执行结果归档要求",
            "references 读取规则"
          ],
          "references": [
            "project-release-test-rules/references/agent-response-judgement.md",
            "project-release-test-rules/references/baseline-asset-rules.md",
            "project-release-test-rules/references/bootstrap-workflow.md",
            "project-release-test-rules/references/dependency-graph-rules.md",
            "project-release-test-rules/references/execution-gate.md",
            "project-release-test-rules/references/existing-test-skill-integration.md",
            "project-release-test-rules/references/interface-inventory-schema.md",
            "project-release-test-rules/references/inventory-reconcile-rules.md",
            "project-release-test-rules/references/openapi-inventory-sync-rules.md",
            "project-release-test-rules/references/output-artifacts.md",
            "project-release-test-rules/references/report-format.md",
            "project-release-test-rules/references/reusable-script-toolbox.md",
            "project-release-test-rules/references/test-data-construction-rules.md",
            "project-release-test-rules/references/test-selection-policy.md"
          ],
          "agents": [
            "project-release-test-rules/agents/openai.yaml"
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
          "title": "Git 协作规则（最小闭环版）",
          "status": "implemented",
          "status_label": "已实现",
          "domain_id": "delivery",
          "domain_label": "交付域",
          "domain_description": "Git 协作与交付说明",
          "domain_order": 9,
          "item_order": 1,
          "auto_trigger": "【强制触发】凡当前这轮用户消息出现 Git 协作动作即触发（显式关键词 + 隐式语义），包括“提交git/帮我提交/commit一下/推送代码/看下状态/看下改动”等；新会话第一条也必须触发。触发后必须与 skill-hit-check-rules 联动命中。默认执行“最小可执行闭环”：短清单 + 阻断脚本 + 统一证据模板。用户明确请求“提交git”时，目标是清空当前全部未提交改动（staged、unstaged、untracked），允许按业务拆分多次提交，不要求一次提交完成，但必须循环到 `git status --short` 为空（除阻断项外）。",
          "core_responsibility": "统一 Git 协作规则。",
          "skill_path": "git-collaboration-rules/SKILL.md",
          "directory_path": "git-collaboration-rules",
          "directory": "git-collaboration-rules",
          "sections": [
            "-1.4 极简硬闸门（新增，强制）",
            "-1.5 首条输出收敛（新增，强制）",
            "-1.6 违规自恢复（新增，强制）",
            "-1. 触发确认（强制）",
            "-1.8 当前轮次授权边界（新增，强制）",
            "-1.0 新会话首轮保障（强制）",
            "-1.1 语义触发扩展（强制）",
            "-1.2 联动前置（强制）",
            "-1.3 口语与缩写兜底（强制）",
            "-1.7 用户显式放行未由代理改动文件（新增，强制）",
            "0. 首条中间进度（强制）",
            "1. 执行短清单（强制按顺序）",
            "1.1 脚本查找与缺失回退（强制）",
            "2. 阻断条件（脚本化/回退等价）",
            "3. 统一证据输出（强制）",
            "4. 通过标准",
            "5. 执行文件"
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
      "id": "submission_review",
      "label": "提交级专项审查",
      "description": "相对 `main` 的当前分支提交级代码审查，不纳入默认自动审查链",
      "order": 10,
      "implemented_count": 1,
      "planned_count": 0,
      "seed_count": 0,
      "total_count": 1,
      "items": [
        {
          "id": "code-review-automation-rules",
          "name": "code-review-automation-rules",
          "title": "提交级代码审核规则",
          "status": "implemented",
          "status_label": "已实现",
          "domain_id": "submission_review",
          "domain_label": "提交级专项审查",
          "domain_description": "相对 `main` 的当前分支提交级代码审查，不纳入默认自动审查链",
          "domain_order": 10,
          "item_order": 1,
          "auto_trigger": "当用户主动提出“审核代码”“review 当前分支提交”“审查最近提交”时触发。负责读取项目 `main` 分支最近一条提交时间，并仅审查当前分支在该时间之后且尚未并入 `main` 的提交，逐条输出中文结构化结果（致命/严重/中等/建议），再将汇总报告保存到 `artifact-storage-rules` 约定的 `doc/6-审查/` 主文档位置（同主题覆盖或按中央模板更新）；禁止跨提交混审，禁止把非当前 commit 引入的问题混入结论；不因本轮已有代码改动或准备最终收口而自动触发，这类场景由 `project-change-review-rules` 承接。",
          "core_responsibility": "负责按当前分支未并入 `main` 的提交范围执行逐条代码审查并生成结构化中文报告；不纳入默认自动审查链。",
          "skill_path": "code-review-automation-rules/SKILL.md",
          "directory_path": "code-review-automation-rules",
          "directory": "code-review-automation-rules",
          "sections": [
            "Skill 作用与适用场景",
            "触发信号（显式）",
            "进入后先做什么",
            "默认执行流程",
            "强制规则",
            "权责边界与不负责事项",
            "执行结果归档要求",
            "执行通过 / 驳回标准",
            "references 读取规则"
          ],
          "references": [
            "code-review-automation-rules/references/report-and-wecom.md",
            "code-review-automation-rules/references/review-prompt-template.md",
            "code-review-automation-rules/references/review-workflow.md"
          ],
          "agents": [
            "code-review-automation-rules/agents/openai.yaml"
          ],
          "has_license": false,
          "focus_points": [
            "优先检查 description 是否具体到触发信号，而不是只写抽象用途。",
            "检查 references 是否足以承接复杂场景，避免 SKILL.md 过厚或过空。",
            "重点看它是否只处理相对 `main` 的提交级审查，不回退成当前 diff 总审查或默认自动审查链的一部分。"
          ]
        }
      ]
    },
    {
      "id": "seed",
      "label": "扩展种子",
      "description": "已入库但未并入主规划的参考 skill",
      "order": 11,
      "implemented_count": 0,
      "planned_count": 0,
      "seed_count": 24,
      "total_count": 24,
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
          "domain_order": 11,
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
          "id": "\"imagegen\"",
          "name": "\"imagegen\"",
          "title": "Image Generation Skill",
          "status": "seed",
          "status_label": "扩展种子",
          "domain_id": "seed",
          "domain_label": "扩展种子",
          "domain_description": "已入库但未并入主规划的参考 skill",
          "domain_order": 11,
          "item_order": 2,
          "auto_trigger": "\"用于生成或编辑位图图片，例如插画、照片、纹理、精灵图、UI 图、概念图、动作帧、透明底抠图等。当用户要“生图”“改图”“参考图出新图”“做 sprite / mockup / 位图素材”时使用。优先使用内置 `image_gen` 工具；如果当前 turn 没有内置工具，就在本地 imagegen 环境可验证时自动切换到捆绑的 CLI 流程，而不是默认阻断。不要用于更适合直接修改 SVG、矢量资源或代码原生图形的任务。\"",
          "core_responsibility": "当前已在仓库中，但尚未并入主规划域表。",
          "skill_path": "imagegen/SKILL.md",
          "directory_path": "imagegen",
          "directory": "imagegen",
          "sections": [
            "顶层模式",
            "脚本路径解析规则（新增）",
            "核心规则",
            "强阻断规则",
            "内置模式保存规则",
            "什么时候用",
            "什么时候不要用",
            "判定思路",
            "工作流",
            "透明底规则",
            "Prompt 增强",
            "Use-case taxonomy",
            "共享 prompt 模板",
            "Prompt 最佳实践",
            "`gpt-image-2` 指南",
            "CLI fallback 专属约定",
            "参考文件"
          ],
          "references": [
            "imagegen/references/cli.md",
            "imagegen/references/codex-network.md",
            "imagegen/references/image-api.md",
            "imagegen/references/local-entrypoints.md",
            "imagegen/references/prompting.md",
            "imagegen/references/sample-prompts.md"
          ],
          "agents": [
            "imagegen/agents/openai.yaml"
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
          "domain_order": 11,
          "item_order": 3,
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
          "domain_order": 11,
          "item_order": 4,
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
          "id": "2d-asset-design",
          "name": "2d-asset-design",
          "title": "2D 素材设计",
          "status": "seed",
          "status_label": "扩展种子",
          "domain_id": "seed",
          "domain_label": "扩展种子",
          "domain_description": "已入库但未并入主规划的参考 skill",
          "domain_order": 11,
          "item_order": 5,
          "auto_trigger": "用于设计、生成和后处理原创 2D 游戏素材。当用户想要新建、重做、补齐、替换、迭代或统一 2D 游戏素材时自动使用；当角色、怪物、Boss、地图、瓦片、场景道具、UI、图标、特效、投射物、掉落物、Sprite Sheet、逐帧动画、Godot 可导入贴图或分层 2D 资源在需求实现过程中成为阻塞项时也自动使用。也用于先从外部素材网站检索候选参考，再把用户选定的截图当作参考板进行风格提炼，重新设计和生成原创素材，而不是直接复用第三方素材作为最终游戏资产。正式素材任务默认先联动共享根目录设计 skill `agent-sprite-forge-design`：先检索参考候选，再出设计图给用户确认，满意后才进入生产和后处理；当进入角色/怪物/Boss 动画或 sprite sheet 生产时，再自动联动共享根目录 `character-sprite-animation-production`。",
          "core_responsibility": "当前已在仓库中，但尚未并入主规划域表。",
          "skill_path": "2d-asset-design/SKILL.md",
          "directory_path": "2d-asset-design",
          "directory": "2d-asset-design",
          "sections": [
            "作用",
            "自动触发范围",
            "核心原则",
            "执行流程",
            "资产类型约束",
            "默认交付规范",
            "额外强约束",
            "输出模式",
            "资源"
          ],
          "references": [
            "2d-asset-design/references/art-direction-quality-gate.md",
            "2d-asset-design/references/asset-modes.md",
            "2d-asset-design/references/character-animation-production-gate.md",
            "2d-asset-design/references/design-preview-confirmation-gate.md",
            "2d-asset-design/references/image-generation-workflow.md",
            "2d-asset-design/references/image-spec-contract.md",
            "2d-asset-design/references/layered-map-contract.md",
            "2d-asset-design/references/map-strategies.md",
            "2d-asset-design/references/postprocess-workflow.md",
            "2d-asset-design/references/project-style-consistency-contract.md",
            "2d-asset-design/references/prompt-rules.md",
            "2d-asset-design/references/prop-pack-contract.md",
            "2d-asset-design/references/reference-only-policy.md"
          ],
          "agents": [
            "2d-asset-design/agents/openai.yaml"
          ],
          "has_license": false,
          "focus_points": [
            "先决定它是并入主规划、保持外部种子，还是拆成多个更窄的内部 skill。",
            "如果准备纳入体系，先补上与主规划域的映射关系和落位说明。",
            "重点看这个种子是否真的能落入主规划，还是保持独立参考更合适。"
          ]
        },
        {
          "id": "agent-sprite-forge-design",
          "name": "agent-sprite-forge-design",
          "title": "Agent Sprite Forge Design",
          "status": "seed",
          "status_label": "扩展种子",
          "domain_id": "seed",
          "domain_label": "扩展种子",
          "domain_description": "已入库但未并入主规划的参考 skill",
          "domain_order": 11,
          "item_order": 6,
          "auto_trigger": "用于在正式生产 2D 游戏素材前完成美术设计收口。吸收 0x0funky/agent-sprite-forge 的 Codex-first 资产设计思路：先检索外部参考候选并让用户选定截图，再判断资产类型、镜头、构图、sheet/layout、分层地图策略和引擎交付方式，最后用图像生成产出设计图预览。适用于角色、怪物、Boss、地图、场景物件、投射物、FX、掉落物、图标等 2D 游戏资产的“先看参考候选、再做设计预览、确认后生产”流程。当用户需要先看方案图、先确认美术方向、先迭代设计稿再落地素材时必须使用。",
          "core_responsibility": "当前已在仓库中，但尚未并入主规划域表。",
          "skill_path": "agent-sprite-forge-design/SKILL.md",
          "directory_path": "agent-sprite-forge-design",
          "directory": "agent-sprite-forge-design",
          "sections": [
            "作用",
            "强制流程",
            "设计阶段最小交付",
            "设计判断",
            "设计图确认闸门",
            "质量红线",
            "和 2d-asset-design 的关系",
            "参考来源"
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
          "id": "artifact-delivery-gate-rules",
          "name": "artifact-delivery-gate-rules",
          "title": "研发文档落盘闸门规则",
          "status": "seed",
          "status_label": "扩展种子",
          "domain_id": "seed",
          "domain_label": "扩展种子",
          "domain_description": "已入库但未并入主规划的参考 skill",
          "domain_order": 11,
          "item_order": 7,
          "auto_trigger": "当需求、实施、验收、Bug、测试或审查任务准备最终收口，且本轮已经产生或应当产生持久化研发文档时自动触发。负责在最终完成前核对文档是否已经真实落盘到 `artifact-storage-rules` 约定的位置，检查主入口文件、必需配套文件和同任务复用关系是否完整；若文档仍停留在最终回复、临时说明或内存结论中，必须阻断收口并先补齐落盘。适用于需求主文档、实施文档、验收文档、Bug 根目录、测试任务 README 与审查报告，不代替需求分析、Bug 定位、测试执行、审核判断或最终验收本身。",
          "core_responsibility": "当前已在仓库中，但尚未并入主规划域表。",
          "skill_path": "artifact-delivery-gate-rules/SKILL.md",
          "directory_path": "artifact-delivery-gate-rules",
          "directory": "artifact-delivery-gate-rules",
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
          "references": [],
          "agents": [
            "artifact-delivery-gate-rules/agents/openai.yaml"
          ],
          "has_license": false,
          "focus_points": [
            "先决定它是并入主规划、保持外部种子，还是拆成多个更窄的内部 skill。",
            "如果准备纳入体系，先补上与主规划域的映射关系和落位说明。",
            "重点看这个种子是否真的能落入主规划，还是保持独立参考更合适。"
          ]
        },
        {
          "id": "authenticated-url-routing-rules",
          "name": "authenticated-url-routing-rules",
          "title": "认证 URL 路由规则",
          "status": "seed",
          "status_label": "扩展种子",
          "domain_id": "seed",
          "domain_label": "扩展种子",
          "domain_description": "已入库但未并入主规划的参考 skill",
          "domain_order": 11,
          "item_order": 8,
          "auto_trigger": "当用户提供任意 URL、链接或网页地址，并要求打开、读取、分析、总结、截图、提取内容、排查页面、查看文档、理解网页、检查资料、访问在线文档或处理已在浏览器登录过的页面时触发。默认优先使用 Chrome Plugin 的 `chrome:control-chrome` 接管用户已登录的真实 Chrome profile，以复用登录态、扩展、权限和已打开标签页；禁止优先使用 `web`、隔离浏览器、无登录态 Playwright 或普通抓取导致权限丢失。若 Chrome Plugin 不可用，再回退到 `agent-browser` 的 auto-connect、state、profile 或 session；若仍遇到登录页、权限页、验证码或人机验证，要求用户在真实 Chrome 中完成授权后继续，不得通过搜索引擎或第三方页面绕过权限。",
          "core_responsibility": "当前已在仓库中，但尚未并入主规划域表。",
          "skill_path": "authenticated-url-routing-rules/SKILL.md",
          "directory_path": "authenticated-url-routing-rules",
          "directory": "authenticated-url-routing-rules",
          "sections": [
            "目标",
            "默认路由",
            "回退顺序",
            "执行要求",
            "Chrome Plugin 确认步骤",
            "实测回灌清单",
            "异常处理",
            "安全边界",
            "通过标准",
            "维护注意事项",
            "常见触发示例"
          ],
          "references": [],
          "agents": [
            "authenticated-url-routing-rules/agents/openai.yaml"
          ],
          "has_license": false,
          "focus_points": [
            "先决定它是并入主规划、保持外部种子，还是拆成多个更窄的内部 skill。",
            "如果准备纳入体系，先补上与主规划域的映射关系和落位说明。",
            "重点看这个种子是否真的能落入主规划，还是保持独立参考更合适。"
          ]
        },
        {
          "id": "autonomous-execution-rules",
          "name": "autonomous-execution-rules",
          "title": "自主连续执行规则",
          "status": "seed",
          "status_label": "扩展种子",
          "domain_id": "seed",
          "domain_label": "扩展种子",
          "domain_description": "已入库但未并入主规划的参考 skill",
          "domain_order": 11,
          "item_order": 9,
          "auto_trigger": "当多步骤任务尚未闭环且存在原执行计划内可直接执行的必需下一步时自动触发（不仅限于回合结束前）。用于多步骤研发任务（需求实现、Bug 修复、重构、测试闭环、文档同步）的连续推进策略：在非关键节点默认自主执行计划内必需动作，不在每个子步骤后征求确认；仅在关键决策节点或高风险节点暂停并给出结构化选项。用户说“开始实施 / 开始实现 / 开始执行 / 直接做 / 继续做完 / 按文档实现 / 按建议执行 / 按方案执行 / 就按你刚才说的做”等开工类指令时，必须已有执行计划，或先给出包含完成定义、停止条件和最大推进边界的本轮计划；缺少计划或停止条件时不得直接实现。若用户给出明确结束指令（如“结束”“停止”“到此为止”“不要继续”“不要下一步建议”“不要扩散”），该指令对所有 agent 通用，必须立即停止自动继续和扩散性输出。任务完成后若不存在“原计划未完成必需项 / 阻断项 / 用户显式要求的建议”三类合法后续，必须强制无下一步，不得输出可能触发循环 loop 的“等待用户新指令 / 无需继续动作 / 下一步状态”占位文案。若刚发生上下文压缩且未重新确认“是否开始/继续实现代码”，必须暂停确认，不得直接进入编码。不要用于绕过系统安全限制、权限审批或高风险操作防护。",
          "core_responsibility": "当前已在仓库中，但尚未并入主规划域表。",
          "skill_path": "autonomous-execution-rules/SKILL.md",
          "directory_path": "autonomous-execution-rules",
          "directory": "autonomous-execution-rules",
          "sections": [
            "目标",
            "执行许可状态（新增）",
            "触发信号",
            "默认执行策略",
            "必须暂停确认的关键节点",
            "关键节点提问格式（强制）",
            "与其他 Skill 的协作",
            "禁止事项",
            "通过 / 驳回标准",
            "快速示例"
          ],
          "references": [],
          "agents": [
            "autonomous-execution-rules/agents/openai.yaml"
          ],
          "has_license": false,
          "focus_points": [
            "先决定它是并入主规划、保持外部种子，还是拆成多个更窄的内部 skill。",
            "如果准备纳入体系，先补上与主规划域的映射关系和落位说明。",
            "重点看这个种子是否真的能落入主规划，还是保持独立参考更合适。"
          ]
        },
        {
          "id": "character-sprite-animation-production",
          "name": "character-sprite-animation-production",
          "title": "Character Sprite Animation Production",
          "status": "seed",
          "status_label": "扩展种子",
          "domain_id": "seed",
          "domain_label": "扩展种子",
          "domain_description": "已入库但未并入主规划的参考 skill",
          "domain_order": 11,
          "item_order": 10,
          "auto_trigger": "用于在 2D 游戏角色、怪物、Boss 或类角色单位需要动作生产时，负责角色动画的生产、分方向拆分、fixed-cell sheet 布局、动作 QA 与预览验证。吸收 character-animation-creator-skill 的核心思路：先锁定角色 identity，再做 base pose，再按动作和方向逐项扩展，并在生成后做 contact sheet、方向一致性、体量漂移和动画可读性审查。适用于 idle、walk、run、attack、cast、hit、death、4向/8向、fixed-cell sprite sheet 等角色动画任务。",
          "core_responsibility": "当前已在仓库中，但尚未并入主规划域表。",
          "skill_path": "character-sprite-animation-production/SKILL.md",
          "directory_path": "character-sprite-animation-production",
          "directory": "character-sprite-animation-production",
          "sections": [
            "作用",
            "自动触发",
            "核心流程",
            "固定格子规则",
            "默认交付",
            "与 2d-asset-design 的关系",
            "参考来源"
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
          "id": "context-compression-rules",
          "name": "context-compression-rules",
          "title": "上下文压缩规则",
          "status": "seed",
          "status_label": "扩展种子",
          "domain_id": "seed",
          "domain_label": "扩展种子",
          "domain_description": "已入库但未并入主规划的参考 skill",
          "domain_order": 11,
          "item_order": 11,
          "auto_trigger": "当当前会话已发生”压缩上下文 / 自动压缩上下文 / 上下文太多”后的压缩重组，或继续执行前刚得到压缩摘要时自动触发。负责在压缩后立即联动 recent-context-bootstrap-rules 重新加载最近项目上下文（含系统的所有 skills 与当前项目根目录下 `./skill`、`./.skills`），并强制重新读取当前项目根目录 `AGENTS.md`（Codex）/ `CLAUDE.md`（Claude Code），避免压缩后丢失 skill 记忆或仓库级硬规则，再输出可直接续做的最小上下文包；压缩包必须显式携带”是否允许开始/继续实现代码”的许可状态，默认 `unknown`，在未重新确认前不得直接进入编码。不要把它代替 history-recall-rules 的深度历史回忆、project-timeline-rules 的长期时间线分析或当前主域执行。",
          "core_responsibility": "当前已在仓库中，但尚未并入主规划域表。",
          "skill_path": "context-compression-rules/SKILL.md",
          "directory_path": "context-compression-rules",
          "directory": "context-compression-rules",
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
            "context-compression-rules/references/boundary-rules.md",
            "context-compression-rules/references/compression-playbook.md",
            "context-compression-rules/references/trigger-signals.md"
          ],
          "agents": [
            "context-compression-rules/agents/openai.yaml"
          ],
          "has_license": false,
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
          "domain_order": 11,
          "item_order": 12,
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
          "id": "golang-patterns",
          "name": "golang-patterns",
          "title": "Go 开发模式",
          "status": "seed",
          "status_label": "扩展种子",
          "domain_id": "seed",
          "domain_label": "扩展种子",
          "domain_description": "已入库但未并入主规划的参考 skill",
          "domain_order": 11,
          "item_order": 13,
          "auto_trigger": "Go 语言惯用模式、最佳实践与编码约定，用于构建健壮、高效、可维护的 Go 应用。",
          "core_responsibility": "当前已在仓库中，但尚未并入主规划域表。",
          "skill_path": "golang-patterns/SKILL.md",
          "directory_path": "golang-patterns",
          "directory": "golang-patterns",
          "sections": [
            "何时启用",
            "核心原则",
            "错误处理模式",
            "并发模式",
            "接口设计",
            "包结构与命名",
            "常量与枚举",
            "结构体与 API 设计",
            "性能与内存",
            "工具链与质量门禁",
            "快速记忆",
            "常见反模式",
            "最终要求"
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
          "id": "image-redbox-focus-rules",
          "name": "image-redbox-focus-rules",
          "title": "图片红框重点关注规则",
          "status": "seed",
          "status_label": "扩展种子",
          "domain_id": "seed",
          "domain_label": "扩展种子",
          "domain_description": "已入库但未并入主规划的参考 skill",
          "domain_order": 11,
          "item_order": 14,
          "auto_trigger": "当用户提交图片、截图、设计稿并希望分析/修改/排查时触发。硬条件：当消息包含 `<image ...>` 时必须命中本 skill。默认将红框（含红色方框、红圈、红线标注）区域视为本轮重点关注信息，优先围绕该区域给出结论与建议；若无红框，再回退到全图分析。",
          "core_responsibility": "当前已在仓库中，但尚未并入主规划域表。",
          "skill_path": "image-redbox-focus-rules/SKILL.md",
          "directory_path": "image-redbox-focus-rules",
          "directory": "image-redbox-focus-rules",
          "sections": [
            "Skill 作用与适用场景",
            "默认提示词",
            "自动触发信号",
            "默认执行流程",
            "输出要求",
            "权责边界与不负责事项",
            "执行通过 / 驳回标准"
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
          "id": "plugin-installation-rules",
          "name": "plugin-installation-rules",
          "title": "插件检测安装使用规则",
          "status": "seed",
          "status_label": "扩展种子",
          "domain_id": "seed",
          "domain_label": "扩展种子",
          "domain_description": "已入库但未并入主规划的参考 skill",
          "domain_order": 11,
          "item_order": 15,
          "auto_trigger": "当用户要求分析项目、检查是否需要安装某个 AI 编码插件 / agent 增强插件，或提到具体插件名（如 Ponytail）需要安装、启用、配置时自动触发。负责通用的\"插件检测 → 安装 → 验证 → 使用 → 回退\"流程，适用于 Claude Code、Codex 等多种 AI 环境；安装命令与配置一律以官方仓库为准，拒绝沿用第三方博客/公众号转述的旧命名、旧参数或臆造命令。具体插件条目（含 Ponytail）见 references/plugin-catalog.md，未来新增插件只追加条目、不改框架；其中标记为【必装】的插件（当前为 Ponytail）在会话 / 项目准备时默认强制安装与启用。不要用它代替 mcp-installation-rules 的 MCP server 判定，也不代替具体编码 / 测试 / 审查 skill。",
          "core_responsibility": "当前已在仓库中，但尚未并入主规划域表。",
          "skill_path": "plugin-installation-rules/SKILL.md",
          "directory_path": "plugin-installation-rules",
          "directory": "plugin-installation-rules",
          "sections": [
            "Skill 作用与适用场景",
            "自动触发信号",
            "进入后先做什么",
            "默认执行流程",
            "必装插件（默认强制）",
            "关键原则",
            "与相邻 skill 的边界",
            "执行通过 / 驳回标准",
            "references 读取规则"
          ],
          "references": [
            "plugin-installation-rules/references/plugin-catalog.md"
          ],
          "agents": [
            "plugin-installation-rules/agents/openai.yaml"
          ],
          "has_license": false,
          "focus_points": [
            "先决定它是并入主规划、保持外部种子，还是拆成多个更窄的内部 skill。",
            "如果准备纳入体系，先补上与主规划域的映射关系和落位说明。",
            "重点看这个种子是否真的能落入主规划，还是保持独立参考更合适。"
          ]
        },
        {
          "id": "skill-split-preserve-rules",
          "name": "skill-split-preserve-rules",
          "title": "Skill 拆分保护规则",
          "status": "seed",
          "status_label": "扩展种子",
          "domain_id": "seed",
          "domain_label": "扩展种子",
          "domain_description": "已入库但未并入主规划的参考 skill",
          "domain_order": 11,
          "item_order": 16,
          "auto_trigger": "当某个现有 skill 已出现多个可独立命中的职责组、触发边界混合或内容膨胀到难以继续承接新增规则，且需要在功能零丢失前提下把它拆成多个独立 skill 并在承接完成后删除旧 skill 时触发。负责先做进入判定、规则原子化、按分类二分拆分、覆盖映射、多轮多模式测试验证、删除前承接检查、按新 skill description 命名并删除旧 skill；不要用它代替普通小修、纯文案润色或业务需求分析。",
          "core_responsibility": "当前已在仓库中，但尚未并入主规划域表。",
          "skill_path": "skill-split-preserve-rules/SKILL.md",
          "directory_path": "skill-split-preserve-rules",
          "directory": "skill-split-preserve-rules",
          "sections": [
            "Skill 作用与适用场景",
            "默认执行流程",
            "强制约束",
            "输出要求",
            "阻断条件",
            "references 读取规则"
          ],
          "references": [
            "skill-split-preserve-rules/references/entry-and-splitting.md",
            "skill-split-preserve-rules/references/mapping-and-deletion.md",
            "skill-split-preserve-rules/references/naming-and-output.md",
            "skill-split-preserve-rules/references/validation-and-testing.md"
          ],
          "agents": [
            "skill-split-preserve-rules/agents/openai.yaml"
          ],
          "has_license": false,
          "focus_points": [
            "先决定它是并入主规划、保持外部种子，还是拆成多个更窄的内部 skill。",
            "如果准备纳入体系，先补上与主规划域的映射关系和落位说明。",
            "重点看这个种子是否真的能落入主规划，还是保持独立参考更合适。"
          ]
        },
        {
          "id": "swag-openapi-maintainer-rules",
          "name": "swag-openapi-maintainer-rules",
          "title": "Swag / OpenAPI 全量维护规则",
          "status": "seed",
          "status_label": "扩展种子",
          "domain_id": "seed",
          "domain_label": "扩展种子",
          "domain_description": "已入库但未并入主规划的参考 skill",
          "domain_order": 11,
          "item_order": 17,
          "auto_trigger": "当用户要求生成、补齐、刷新、维护项目 swag、更新 swag、导出 Apifox/OpenAPI/Swagger 接口文档，或需要让项目所有 HTTP 接口持续同步为 YAML 文档时触发。负责从真实路由、controller、请求 DTO、响应 DTO、统一响应包装和鉴权中间件读取接口契约，生成或更新项目根目录 swag/ 下的全量接口 OpenAPI/Swagger YAML；每个接口单独一个 YAML，同时维护一个包含所有接口的总 YAML。单接口 YAML 默认直导入 Apifox 选中的目录，不额外生成父目录；单接口文件名默认采用“路径名 + 中文简要说明”格式，中文简介后缀必须去掉数字前缀、序号和无业务意义的特殊符号；头部、请求参数、响应字段都必须有中文说明，可在证据充分时做受控推导。本 skill 只生成或维护 swag/ 目录下的 YAML 文档产物，不修改后端代码中的 Swagger 注解、框架接入或调试入口（那属于 api-swagger-rules）；不要用它代替 api-swagger-rules、业务接口实现、接口需求设计、功能测试或线上联调。",
          "core_responsibility": "当前已在仓库中，但尚未并入主规划域表。",
          "skill_path": "swag-openapi-maintainer-rules/SKILL.md",
          "directory_path": "swag-openapi-maintainer-rules",
          "directory": "swag-openapi-maintainer-rules",
          "sections": [
            "Skill 作用与适用场景",
            "自动触发信号",
            "核心约束",
            "默认执行流程",
            "进入后先做什么",
            "执行通过 / 驳回标准",
            "references 读取规则",
            "scripts"
          ],
          "references": [
            "swag-openapi-maintainer-rules/references/description-rules.md",
            "swag-openapi-maintainer-rules/references/discovery-rules.md",
            "swag-openapi-maintainer-rules/references/naming-rules.md",
            "swag-openapi-maintainer-rules/references/schema-rules.md",
            "swag-openapi-maintainer-rules/references/validation-rules.md"
          ],
          "agents": [],
          "has_license": false,
          "focus_points": [
            "先决定它是并入主规划、保持外部种子，还是拆成多个更窄的内部 skill。",
            "如果准备纳入体系，先补上与主规划域的映射关系和落位说明。",
            "重点看这个种子是否真的能落入主规划，还是保持独立参考更合适。"
          ]
        },
        {
          "id": "time-util-rules",
          "name": "time-util-rules",
          "title": "时间处理规则",
          "status": "seed",
          "status_label": "扩展种子",
          "domain_id": "seed",
          "domain_label": "扩展种子",
          "domain_description": "已入库但未并入主规划的参考 skill",
          "domain_order": 11,
          "item_order": 18,
          "auto_trigger": "当新增或修改时间、日期、时区、时间窗、开始结束区间、时间字符串格式化/解析、定时任务或报表快照口径时触发。负责统一强制通过项目内 timeUtil 处理时间；不要用它代替数据库时间规则或业务口径规则。",
          "core_responsibility": "当前已在仓库中，但尚未并入主规划域表。",
          "skill_path": "time-util-rules/SKILL.md",
          "directory_path": "time-util-rules",
          "directory": "time-util-rules",
          "sections": [
            "作用",
            "自动触发",
            "强制规则",
            "执行流程",
            "边界",
            "通过标准"
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
          "id": "vercel-react-best-practices",
          "name": "vercel-react-best-practices",
          "title": "Vercel React 最佳实践",
          "status": "seed",
          "status_label": "扩展种子",
          "domain_id": "seed",
          "domain_label": "扩展种子",
          "domain_description": "已入库但未并入主规划的参考 skill",
          "domain_order": 11,
          "item_order": 19,
          "auto_trigger": "来自 Vercel Engineering 的 React / Next.js 性能优化指南。适用于编写、评审、重构 React/Next.js 代码时，确保采用高性能实现模式。触发场景包括 React 组件、Next.js 页面、数据获取、包体积优化与性能改进任务。",
          "core_responsibility": "当前已在仓库中，但尚未并入主规划域表。",
          "skill_path": "vercel-react-best-practices/SKILL.md",
          "directory_path": "vercel-react-best-practices",
          "directory": "vercel-react-best-practices",
          "sections": [
            "何时使用",
            "按优先级划分的规则类别",
            "快速索引",
            "使用方式",
            "完整汇总文档"
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
          "id": "vue-best-practices",
          "name": "vue-best-practices",
          "title": "Vue 最佳实践工作流",
          "status": "seed",
          "status_label": "扩展种子",
          "domain_id": "seed",
          "domain_label": "扩展种子",
          "domain_description": "已入库但未并入主规划的参考 skill",
          "domain_order": 11,
          "item_order": 20,
          "auto_trigger": "Vue.js 任务必须命中本 skill。默认推荐使用 Composition API + `<script setup>` + TypeScript。覆盖 Vue 3、SSR、Volar、vue-tsc。凡是 Vue、`.vue`、Vue Router、Pinia 或 Vite + Vue 相关工作都应加载。除非项目明确要求 Options API，否则始终优先 Composition API。",
          "core_responsibility": "当前已在仓库中，但尚未并入主规划域表。",
          "skill_path": "vue-best-practices/SKILL.md",
          "directory_path": "vue-best-practices",
          "directory": "vue-best-practices",
          "sections": [
            "核心原则",
            "1) 编码前先确认架构（必做）",
            "2) 应用 Vue 基础能力（必做）",
            "3) 仅在需求明确时使用可选能力",
            "4) 功能正确后再做性能优化",
            "5) 完成前自检"
          ],
          "references": [
            "vue-best-practices/references/animation-class-based-technique.md",
            "vue-best-practices/references/animation-state-driven-technique.md",
            "vue-best-practices/references/component-async.md",
            "vue-best-practices/references/component-data-flow.md",
            "vue-best-practices/references/component-fallthrough-attrs.md",
            "vue-best-practices/references/component-keep-alive.md",
            "vue-best-practices/references/component-slots.md",
            "vue-best-practices/references/component-suspense.md",
            "vue-best-practices/references/component-teleport.md",
            "vue-best-practices/references/component-transition-group.md",
            "vue-best-practices/references/component-transition.md",
            "vue-best-practices/references/composables.md",
            "vue-best-practices/references/directives.md",
            "vue-best-practices/references/perf-avoid-component-abstraction-in-lists.md",
            "vue-best-practices/references/perf-v-once-v-memo-directives.md",
            "vue-best-practices/references/perf-virtualize-large-lists.md",
            "vue-best-practices/references/plugins.md",
            "vue-best-practices/references/reactivity.md",
            "vue-best-practices/references/render-functions.md",
            "vue-best-practices/references/sfc.md",
            "vue-best-practices/references/state-management.md",
            "vue-best-practices/references/updated-hook-performance.md"
          ],
          "agents": [],
          "has_license": false,
          "focus_points": [
            "先决定它是并入主规划、保持外部种子，还是拆成多个更窄的内部 skill。",
            "如果准备纳入体系，先补上与主规划域的映射关系和落位说明。",
            "重点看这个种子是否真的能落入主规划，还是保持独立参考更合适。"
          ]
        },
        {
          "id": "vue-router-best-practices",
          "name": "vue-router-best-practices",
          "title": "vue-router-best-practices",
          "status": "seed",
          "status_label": "扩展种子",
          "domain_id": "seed",
          "domain_label": "扩展种子",
          "domain_description": "已入库但未并入主规划的参考 skill",
          "domain_order": 11,
          "item_order": 21,
          "auto_trigger": "\"Vue Router 4 模式、导航守卫、路由参数以及路由与组件生命周期交互的最佳实践。\"",
          "core_responsibility": "当前已在仓库中，但尚未并入主规划域表。",
          "skill_path": "vue-router-best-practices/SKILL.md",
          "directory_path": "vue-router-best-practices",
          "directory": "vue-router-best-practices",
          "sections": [],
          "references": [],
          "agents": [],
          "has_license": true,
          "focus_points": [
            "先决定它是并入主规划、保持外部种子，还是拆成多个更窄的内部 skill。",
            "如果准备纳入体系，先补上与主规划域的映射关系和落位说明。",
            "重点看这个种子是否真的能落入主规划，还是保持独立参考更合适。"
          ]
        },
        {
          "id": "web-design-guidelines",
          "name": "web-design-guidelines",
          "title": "Web 界面规范审查",
          "status": "seed",
          "status_label": "扩展种子",
          "domain_id": "seed",
          "domain_label": "扩展种子",
          "domain_description": "已入库但未并入主规划的参考 skill",
          "domain_order": 11,
          "item_order": 22,
          "auto_trigger": "用于审查 UI 代码是否符合 Web Interface Guidelines。适用于“帮我审查 UI”“检查可访问性”“设计审计”“UX 评审”“按最佳实践检查网站”等请求。",
          "core_responsibility": "当前已在仓库中，但尚未并入主规划域表。",
          "skill_path": "web-design-guidelines/SKILL.md",
          "directory_path": "web-design-guidelines",
          "directory": "web-design-guidelines",
          "sections": [
            "工作方式",
            "规范来源",
            "使用方式"
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
          "id": "windows-wsl-execution-rules",
          "name": "windows-wsl-execution-rules",
          "title": "Windows / WSL 执行规范（代码在 WSL）",
          "status": "seed",
          "status_label": "扩展种子",
          "domain_id": "seed",
          "domain_label": "扩展种子",
          "domain_description": "已入库但未并入主规划的参考 skill",
          "domain_order": 11,
          "item_order": 23,
          "auto_trigger": "当项目代码位于 WSL 文件系统内（如 `/home/user/project`）、且当前任务发生在 Windows 环境时触发。核心边界：只有执行类动作才优先进入 WSL，例如编译、运行/启动程序、测试、调试、会真实启动运行时的依赖安装；看代码、改代码、搜索、读写规则文件、普通 git 操作与多数只读检查默认优先使用 Git Bash / bash。PowerShell 不作为 Windows 下普通仓库命令入口，只在 `.ps1` 脚本、Windows 专用 cmdlet、PowerShell profile / 编码初始化或用户明确要求时使用。agent 在 WSL 时直接访问代码与执行；agent 在 Windows 时（如 Claude Desktop GUI），普通命令通过 Git Bash / bash 访问 `//wsl.localhost/distro/...` 或等价 Windows 可访问路径，执行类动作再用 `wsl.exe --cd /home/user/project target-command` 进 WSL。无论文件写入发生在 Windows、WSL 还是 Linux，都必须遵守 UTF-8 文件写入规则，禁止 GBK/ANSI/默认编码落盘。回复中需要引用项目内文件路径（Markdown 链接、审查证据路径、截图说明、最终总结里的文件路径等）时同样触发本 skill：这条只看用户查看环境，与 agent 自身运行在 WSL 还是 Windows 无关——只要用户从 Windows 桌面 / GUI 客户端访问、项目代码在 WSL，就必须输出 `\\\\wsl.localhost\\<distro>\\...`，不能因为 agent 本身直接跑在 WSL 内（无需 `wsl.exe` 包裹）就顺手把 `/home/...` 当成用户可打开路径输出。纯 Windows 项目或不需要启动执行的任务，不要误切到 WSL。不要用它代替具体语言/框架实现、测试策略或编码规则。",
          "core_responsibility": "当前已在仓库中，但尚未并入主规划域表。",
          "skill_path": "windows-wsl-execution-rules/SKILL.md",
          "directory_path": "windows-wsl-execution-rules",
          "directory": "windows-wsl-execution-rules",
          "sections": [
            "适用场景",
            "核心架构：先看 agent 在哪运行",
            "什么算执行类命令",
            "为什么只有执行类动作优先在 WSL",
            "路径约定",
            "执行环境分工（agent 在 Windows 时）",
            "命令模板（agent 在 Windows 时）",
            "WSL 内缓存目录建议",
            "不推荐做法",
            "约束总结",
            "与其他规则的协作",
            "参考资料读取规则"
          ],
          "references": [
            "windows-wsl-execution-rules/references/command-templates.md",
            "windows-wsl-execution-rules/references/path-mapping.md",
            "windows-wsl-execution-rules/references/recommended-workflow.md",
            "windows-wsl-execution-rules/references/tool-path-interop.md"
          ],
          "agents": [
            "windows-wsl-execution-rules/agents/openai.yaml"
          ],
          "has_license": false,
          "focus_points": [
            "先决定它是并入主规划、保持外部种子，还是拆成多个更窄的内部 skill。",
            "如果准备纳入体系，先补上与主规划域的映射关系和落位说明。",
            "重点看这个种子是否真的能落入主规划，还是保持独立参考更合适。"
          ]
        },
        {
          "id": "work-report-summary-rules",
          "name": "work-report-summary-rules",
          "title": "工作报告汇总规则",
          "status": "seed",
          "status_label": "扩展种子",
          "domain_id": "seed",
          "domain_label": "扩展种子",
          "domain_description": "已入库但未并入主规划的参考 skill",
          "domain_order": 11,
          "item_order": 24,
          "auto_trigger": "当用户提出“生成年报/月报/周报/日报”“汇总年报/月报/周报/日报”“按项目统计最近提交并输出日报/周报/月报/年报”等请求时触发。负责基于 skill 配置的项目路径与项目名称，统计指定时间范围内的 Git 提交，并按项目补充当前工作区未提交改动对应的“进行中事项”，输出结构化报告（含日期+星期、按项目分组、报告内容点）；报告语言必须为中文且使用 UTF-8 编码，所有时间统一按北京时间；只允许统计当前用户本人提交，严禁混入其他作者提交；日报只统计一天，周报统计自然周，月报统计自然月，年报统计自然年；默认过滤低价值提交（如重命名/回滚/构建/文档/测试），未提交事项也必须使用 Git 工作区真实证据并显式标注为 `进行中`；并按 `?报-YYYYMMDDHHMMSS` 格式自动保存到 `/home/luode/code`（可在配置中覆盖）；不要把它代替发布总结、需求文档或测试报告。",
          "core_responsibility": "当前已在仓库中，但尚未并入主规划域表。",
          "skill_path": "work-report-summary-rules/SKILL.md",
          "directory_path": "work-report-summary-rules",
          "directory": "work-report-summary-rules",
          "sections": [
            "Skill 作用与适用场景",
            "自动触发信号",
            "进入后先做什么",
            "默认执行流程",
            "报告输出要求",
            "权责边界与不负责事项",
            "需要暂停并确认的条件",
            "执行通过 / 驳回标准",
            "references 读取规则"
          ],
          "references": [
            "work-report-summary-rules/references/projects.json",
            "work-report-summary-rules/references/report-format.md",
            "work-report-summary-rules/references/uncommitted-worktree.md"
          ],
          "agents": [
            "work-report-summary-rules/agents/openai.yaml"
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
      "auto_trigger": "当需要定义、调整或解释项目中 `doc/1-架构/`、`doc/2-需求/`、`doc/3-实施/`、`doc/4-bugs/`、`doc/5-tests/`、`doc/6-审查/`、`doc/7-验收/`、`doc/`、`skill/` 以及根目录 `项目设计.md` 等研发产物根目录、主入口文件、命名模板、同任务复用策略或跨域文档引用关系时自动触发。负责提供全局唯一的目录与命名单一真相源，并为需求、实施、验收、Bug、测试、审查、记忆、项目设计和交付类 skill 提供统一引用基准；不要用它代替需求分析、Bug 定位、测试执行、生产代码存放决策或流程分流。",
      "core_responsibility": "作为跨域统一约定 skill，提供目录、命名和复用策略的单一真相源，供需求、实施、验收、Bug、测试、记忆、项目设计和交付类 skill 统一引用。",
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
      "auto_trigger": "当用户要求分析整个项目、梳理项目架构/模块/目录/主链路、检查根目录 `项目设计.md` 及同类设计文档是否偏移、同步更新项目设计文档，或在完成全项目分析后为缺失项目补建根目录 `项目设计.md` 时自动触发。负责把根目录项目设计类文档作为弱参考源读取，按“代码与当前文档优先、设计文档低优先级”原则校验偏移，并统一同步到根目录 `项目设计.md`；不要用它代替 recent-context-bootstrap-rules 的轻量预热、artifact-storage-rules 的路径命名总规则、project-timeline-rules 的长期时间线，或 package-structure-rules / implementation-review-rules 的测试前归位判断。",
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
      "id": "architecture-doc-rules",
      "name": "architecture-doc-rules",
      "title": "架构文档规则",
      "status": "implemented",
      "status_label": "已实现",
      "domain_id": "orchestration",
      "domain_label": "总控层",
      "domain_description": "流程分流、冲突裁决、阶段阻断与全局基础约定",
      "domain_order": 1,
      "item_order": 4,
      "auto_trigger": "当需要创建、更新、审查或解释 `doc/1-架构/` 下的长期架构文档时自动触发，适用于总架构、目录树、目录职责、模块职责、主要业务/功能设计架构、模块关系、关键链路、运行时设计和架构专题说明；负责维护 `1-总架构.md`、`2-目录树.md`、`3-模块职责.md`、`4-主要业务链路.md` 四个有序中文主入口，并支持从序号 5 开始更新或追加“序号-业务链路-中文业务名称.md”文档。同时区分专题架构文档与根目录 `项目设计.md` 的分层关系，并确保路径、命名和复用策略服从 `artifact-storage-rules`。不要用它代替 project-design-doc-rules 的根目录项目总览同步、implementation-planning-rules 的当前需求实施计划、package-structure-rules 的生产代码目录归位或 codegraph-analysis-rules 的源码图谱探索。",
      "core_responsibility": "负责维护 `1-4` 四个有序中文主入口；业务链路从 `5` 开始依次下推，同一链路保留编号更新，新链路使用最大编号加一，并区分它与根目录 `项目设计.md` 的总览分层关系。",
      "skill_path": "architecture-doc-rules/SKILL.md",
      "directory_path": "architecture-doc-rules",
      "directory": "architecture-doc-rules",
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
        "architecture-doc-rules/references/architecture-doc-template.md",
        "architecture-doc-rules/references/architecture-topic-examples.md",
        "architecture-doc-rules/references/layering-with-project-design.md",
        "architecture-doc-rules/references/update-policy.md"
      ],
      "agents": [],
      "has_license": false,
      "focus_points": [
        "优先检查 description 是否具体到触发信号，而不是只写抽象用途。",
        "检查 references 是否足以承接复杂场景，避免 SKILL.md 过厚或过空。",
        "重点看是否只做分流、阻断或全局基础约定，没有越权覆盖单域 skill。"
      ]
    },
    {
      "id": "project-local-skills-rules",
      "name": "project-local-skills-rules",
      "title": "项目专属 Skill 沉淀规则",
      "status": "implemented",
      "status_label": "已实现",
      "domain_id": "orchestration",
      "domain_label": "总控层",
      "domain_description": "流程分流、冲突裁决、阶段阻断与全局基础约定",
      "domain_order": 1,
      "item_order": 5,
      "auto_trigger": "当用户要求“分析项目”并明确希望总结该项目专属编码规则/实践为 skill，或要求沉淀项目私有 skill 清单时自动触发。负责把项目专属能力拆成多个独立 skill 并统一写入项目根目录 `skill/`，用于后续上下文预热和编码阶段优先命中；不要用它代替通用体系 skill 的执行，也不要代替 `artifact-storage-rules` 的全局路径裁决。",
      "core_responsibility": "负责把项目专属规则拆成多个独立 skill，并统一落到项目根目录 `skill/`，供后续预热和编码阶段优先命中。",
      "skill_path": "project-local-skills-rules/SKILL.md",
      "directory_path": "project-local-skills-rules",
      "directory": "project-local-skills-rules",
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
        "project-local-skills-rules/references/priority-and-roadmap.md",
        "project-local-skills-rules/references/project-skill-template.md",
        "project-local-skills-rules/references/scope-and-splitting.md"
      ],
      "agents": [
        "project-local-skills-rules/agents/openai.yaml"
      ],
      "has_license": false,
      "focus_points": [
        "优先检查 description 是否具体到触发信号，而不是只写抽象用途。",
        "检查 references 是否足以承接复杂场景，避免 SKILL.md 过厚或过空。",
        "重点看是否只做分流、阻断或全局基础约定，没有越权覆盖单域 skill。"
      ]
    },
    {
      "id": "mcp-installation-rules",
      "name": "mcp-installation-rules",
      "title": "MCP 安装判定规则",
      "status": "implemented",
      "status_label": "已实现",
      "domain_id": "orchestration",
      "domain_label": "总控层",
      "domain_description": "流程分流、冲突裁决、阶段阻断与全局基础约定",
      "domain_order": 1,
      "item_order": 6,
      "auto_trigger": "当用户要求分析项目、检查当前项目是否需要安装 MCP、判断浏览器或 Godot 编辑器应优先由哪个工具接管，或任务即将涉及前端页面验证、浏览器联动、Godot 编辑器操控且需要先根据项目结构决定是否安装 Chrome DevTools MCP 或 Godot AI MCP 时自动触发。对“谷歌浏览器 MCP / Google Chrome MCP / Chrome MCP / Chrome DevTools for agents”统一按官方当前名称 `Chrome DevTools MCP` 处理。负责识别前端项目与 Godot 项目标记，给出 MCP 安装结论、优先级、Codex 配置补齐规则和后续工具让路规则；若已具备对应 MCP，应优先使用它们控制浏览器或 Godot 编辑器，再在缺失或不可用时回退到其他本地工具。此外，任何代码仓库默认推荐 CodeGraph（代码探索默认入口）与 codebase-memory-mcp（架构分析补充）这组代码图谱 MCP，安装与配置以官方仓库为准。",
      "core_responsibility": "负责识别前端项目与 Godot 项目标记，给出 MCP 安装结论、安装流程、优先级和后续工具让路规则，并将“谷歌浏览器 MCP / Google Chrome MCP / Chrome DevTools for agents”等称呼统一归一到 Chrome DevTools MCP；若项目级 Codex `config.toml` 缺少目标 MCP 配置，则默认补齐。",
      "skill_path": "mcp-installation-rules/SKILL.md",
      "directory_path": "mcp-installation-rules",
      "directory": "mcp-installation-rules",
      "sections": [
        "Skill 作用与适用场景",
        "自动触发信号",
        "进入后先做什么",
        "默认执行流程",
        "代码图谱 MCP（CodeGraph + codebase-memory-mcp）",
        "平台判定与 Claude Code MCP 配置分支（新增）",
        "Chrome DevTools MCP 安装流程（本节专属 Codex CLI 环境）",
        "适用安装结论模板",
        "默认优先级",
        "与相邻 skill 的边界",
        "需要暂停并确认的条件",
        "执行通过 / 驳回标准",
        "references 读取规则"
      ],
      "references": [
        "mcp-installation-rules/references/config-bootstrap.md",
        "mcp-installation-rules/references/current-sources.md",
        "mcp-installation-rules/references/project-signals.md",
        "mcp-installation-rules/references/tool-priority.md"
      ],
      "agents": [
        "mcp-installation-rules/agents/openai.yaml"
      ],
      "has_license": false,
      "focus_points": [
        "优先检查 description 是否具体到触发信号，而不是只写抽象用途。",
        "检查 references 是否足以承接复杂场景，避免 SKILL.md 过厚或过空。",
        "重点看是否只做分流、阻断或全局基础约定，没有越权覆盖单域 skill。"
      ]
    },
    {
      "id": "godot-project-bootstrap-rules",
      "name": "godot-project-bootstrap-rules",
      "title": "Godot 项目自举规则",
      "status": "implemented",
      "status_label": "已实现",
      "domain_id": "orchestration",
      "domain_label": "总控层",
      "domain_description": "流程分流、冲突裁决、阶段阻断与全局基础约定",
      "domain_order": 1,
      "item_order": 7,
      "auto_trigger": "当仓库命中 `project.godot`、`.gd`、`.tscn`、`addons/`、`export_presets.cfg` 等 Godot 项目标记，且需要自动补齐项目级规则文件（`AGENTS.md` / `CLAUDE.md`）、Godot AI MCP 配置、图像生成配置模板或检查 Godot 开发环境是否可直接进入执行时强制自动触发。负责把 Godot 项目的环境准备、自举补齐、图像通道模板和只差人工配置的缺口一次性收口。",
      "core_responsibility": "负责把 Godot 项目的环境准备、自举补齐、图像通道模板和只差人工配置的缺口一次性收口，并联动 `project-agents-bootstrap`、`mcp-installation-rules` 与 `imagegen`。",
      "skill_path": "godot-project-bootstrap-rules/SKILL.md",
      "directory_path": "godot-project-bootstrap-rules",
      "directory": "godot-project-bootstrap-rules",
      "sections": [
        "目标",
        "自动触发信号",
        "进入后先做什么",
        "默认执行流程",
        "图像配置硬规则",
        "输出要求",
        "与相邻 skill 的边界",
        "通过标准"
      ],
      "references": [],
      "agents": [
        "godot-project-bootstrap-rules/agents/openai.yaml"
      ],
      "has_license": false,
      "focus_points": [
        "优先检查 description 是否具体到触发信号，而不是只写抽象用途。",
        "检查 references 是否足以承接复杂场景，避免 SKILL.md 过厚或过空。",
        "重点看是否只做分流、阻断或全局基础约定，没有越权覆盖单域 skill。",
        "当前没有 references，可考虑补最小示例或边界文档以降低后续维护成本。"
      ]
    },
    {
      "id": "codegraph-analysis-rules",
      "name": "codegraph-analysis-rules",
      "title": "CodeGraph 分析规则",
      "status": "implemented",
      "status_label": "已实现",
      "domain_id": "orchestration",
      "domain_label": "总控层",
      "domain_description": "流程分流、冲突裁决、阶段阻断与全局基础约定",
      "domain_order": 1,
      "item_order": 8,
      "auto_trigger": "当需要分析代码库结构、符号关系、调用链、被调用方、影响面、重构范围或跨文件根因时自动触发。任何仓库都默认先尝试由 CodeGraph 支撑；若未安装 `codegraph`，必须从 `colbymchenry/codegraph` 强制下载并安装；若 `.codegraph/` 未初始化，则先自动初始化再用；若安装或初始化失败、当前环境不支持，则直接回退到 `rg`、`find`、`read` 等本地手段。不要把它代替项目设计、需求澄清、编码实现或测试验证主流程。",
      "core_responsibility": "负责优先提醒使用 CodeGraph 做图谱探索；未初始化时先自动初始化，失败后回退到 `rg`、`find`、`read` 等本地手段。",
      "skill_path": "codegraph-analysis-rules/SKILL.md",
      "directory_path": "codegraph-analysis-rules",
      "directory": "codegraph-analysis-rules",
      "sections": [
        "Skill 作用与适用场景",
        "自动触发信号",
        "进入后先做什么",
        "默认优先级",
        "CodeGraph 初始化规则",
        "与相邻 skill 的边界",
        "需要暂停并确认的条件",
        "执行通过 / 驳回标准"
      ],
      "references": [],
      "agents": [
        "codegraph-analysis-rules/agents/openai.yaml"
      ],
      "has_license": false,
      "focus_points": [
        "优先检查 description 是否具体到触发信号，而不是只写抽象用途。",
        "检查 references 是否足以承接复杂场景，避免 SKILL.md 过厚或过空。",
        "重点看是否只做分流、阻断或全局基础约定，没有越权覆盖单域 skill。",
        "当前没有 references，可考虑补最小示例或边界文档以降低后续维护成本。"
      ]
    },
    {
      "id": "project-agents-bootstrap",
      "name": "project-agents-bootstrap",
      "title": "项目 AGENTS.md 自举与补齐 Skill",
      "status": "implemented",
      "status_label": "已实现",
      "domain_id": "orchestration",
      "domain_label": "总控层",
      "domain_description": "流程分流、冲突裁决、阶段阻断与全局基础约定",
      "domain_order": 1,
      "item_order": 9,
      "auto_trigger": "若当前 AI 为 Claude Code，目标规则文件为 `CLAUDE.md`；若为 Codex，目标规则文件为 `AGENTS.md`；新会话第一轮默认自动触发（不依赖用户意图）；也可被”创建、补齐或更新 AGENTS.md / CLAUDE.md / 补充仓库级规则”等显式请求触发。负责在项目根目录强制检测 AGENTS.md / CLAUDE.md：不存在则必须创建最小可用模板，存在则对受管章节执行增量补齐与幂等 upsert，既保留用户已有规则，也持续同步最新仓库规则；同时确保包含代码生成风格入口规则、注释类任务流程、跨平台 UTF-8 文件写入约束、按平台能力矩阵执行的会话动态重命名规则，以及”上下文压缩后必须重新读取项目根目录规则文件再继续主任务”的硬规则。若仓库命中 Godot 项目标记，还必须额外补齐 Godot 工具接管与图像生成配置模板，并明确规则文件里不能存真实密钥；图像生成配置必须同步主通道与回退规则，且回退规则必须写成 `回退规则：回退配置` 的层级结构，并在其下声明 `api` / `baseurl`；若仓库需要长期记忆与长期风格，两者都要同步引入 `project-memory-rules`、`project-style-rules` 和 `code-generation-style-rules` 的仓库级入口口径，并确保其最低命中要求写入仓库级规则。当用户给出“根据 skill 补充更新 md / 根据规则更新 md / 按 skill 更新项目 md / 更新这几个 md”等聚合指令时，本 skill 作为统一入口，一次性编排项目根目录 `AGENTS.md`、`CLAUDE.md`、`PROJECT_MEMORY.md`、`PROJECT_STYLE.md` 四个核心 md 的“检测→缺失则创建→已存在则增量补齐”；其中 `PROJECT_MEMORY.md` 必须继续保持为唯一长期记忆主文件，但内部补齐为“人类阅读区 + 底部机器索引区”的单文件双区结构，且不得新增 `PROJECT_MEMORY_INDEX.yaml`。",
      "core_responsibility": "负责为项目补齐或同步仓库级规则文件，并把基础硬规则、自举模板和关键白名单口径统一收口。",
      "skill_path": "project-agents-bootstrap/SKILL.md",
      "directory_path": "project-agents-bootstrap",
      "directory": "project-agents-bootstrap",
      "sections": [
        "AI 环境检测与规则文件约定",
        "目标",
        "仓库级总控规则",
        "触发条件",
        "会话动态重命名规则",
        "统一 md 补齐编排（根据 skill 补充更新 md）",
        "执行步骤",
        "脚本用法",
        "最小模板（缺失时使用）",
        "适用范围",
        "Skill 强制自动触发规则（最高优先级）",
        "严禁脑补工具调用与结果（最高优先级，强制）",
        "严禁自动提交 Git（最高优先级，强制）",
        "Skill 命中强制规则",
        "代码生成风格入口规则",
        "会话动态重命名规则",
        "注释任务强制流程",
        "上下文压缩续做规则",
        "文件编码与写入规则",
        "变更最小化",
        "本地连接调试测试红线（最高优先级，强制）",
        "依赖与工具复用优先规则",
        "输出格式规则",
        "Windows / WSL 执行规则",
        "CodeGraph 强制准备规则",
        "代码库探索规则",
        "插件检测安装规则",
        "边界"
      ],
      "references": [],
      "agents": [],
      "has_license": false,
      "focus_points": [
        "优先检查 description 是否具体到触发信号，而不是只写抽象用途。",
        "检查 references 是否足以承接复杂场景，避免 SKILL.md 过厚或过空。",
        "重点看是否只做分流、阻断或全局基础约定，没有越权覆盖单域 skill。",
        "当前没有 references，可考虑补最小示例或边界文档以降低后续维护成本。"
      ]
    },
    {
      "id": "thread-title-rules",
      "name": "thread-title-rules",
      "title": "会话标题规则",
      "status": "implemented",
      "status_label": "已实现",
      "domain_id": "orchestration",
      "domain_label": "总控层",
      "domain_description": "流程分流、冲突裁决、阶段阻断与全局基础约定",
      "domain_order": 1,
      "item_order": 10,
      "auto_trigger": "【强制自动触发】当当前会话收到明确提问、需求、Bug、实施、审查、测试、提交、规则更新或其他可命名请求，或进入 goal 创建 / goal 恢复 / 上下文压缩续做 / 长任务阶段切换等过程节点，且可稳定归纳出中文任务主题时触发。负责自动生成 8-24 字中文简要标题，并按平台能力矩阵调用真实线程重命名工具重命名当前会话：Codex 使用 `set_thread_title`，Claude Code 仅在存在真实改名工具时执行，Claude Desktop 默认视为无真实自动改名工具并显式跳过；不等待用户显式要求，也不等到最终总结。问题过于闲聊、主题过散、标题已准确、工具不可用或用户明确禁止时不改名。不要用它代替需求分析、Bug 定位、实施规划、测试验证或提交动作。",
      "core_responsibility": "负责生成 8-24 字中文简要标题，并按平台能力矩阵调用当前环境真实线程重命名工具更新当前会话标题；Codex 优先使用 `set_thread_title`，Claude Code 仅在存在真实改名工具时执行，Claude Desktop 默认显式跳过。",
      "skill_path": "thread-title-rules/SKILL.md",
      "directory_path": "thread-title-rules",
      "directory": "thread-title-rules",
      "sections": [
        "目标",
        "自动触发条件",
        "跳过条件",
        "标题生成规则",
        "平台能力矩阵",
        "执行流程",
        "工具与证据约束",
        "通过标准"
      ],
      "references": [],
      "agents": [
        "thread-title-rules/agents/openai.yaml"
      ],
      "has_license": false,
      "focus_points": [
        "优先检查 description 是否具体到触发信号，而不是只写抽象用途。",
        "检查 references 是否足以承接复杂场景，避免 SKILL.md 过厚或过空。",
        "重点看是否只做分流、阻断或全局基础约定，没有越权覆盖单域 skill。",
        "当前没有 references，可考虑补最小示例或边界文档以降低后续维护成本。"
      ]
    },
    {
      "id": "parallel-task-dispatch-rules",
      "name": "parallel-task-dispatch-rules",
      "title": "并行任务分发规则",
      "status": "implemented",
      "status_label": "已实现",
      "domain_id": "orchestration",
      "domain_label": "总控层",
      "domain_description": "流程分流、冲突裁决、阶段阻断与全局基础约定",
      "domain_order": 1,
      "item_order": 11,
      "auto_trigger": "【强制自动触发】当研发、分析、侦察、审查、测试或文档任务进入实质执行前触发，不限于固定 skill 映射；主 agent 必须自主判断当前目标是否存在可由子 agent 并行推进的独立问题、证据来源、文件集、模块边界或职责边界。负责判断当前工作应并行、条件并行还是串行推进，并给出线程拆分、文件归属、收口合并与回退条件；若判定为可并行或条件并行且无阻断，必须联动 `subagent-dispatch-rules` 做真实启动判定。本仓库完全授权模式视为满足工具显式授权条件；只要环境支持、写集不冲突且风险可控，就应发起真实子线程 / 子代理并行执行。适用于项目分析、代码库侦察、需求完善侦察、Bug 分诊与证据收集、代码规范检查、注释补充、格式清理、lint 修复、测试补充、文档更新等可独立推进的任务；审查类 skill 只要能只读或按独立文件集检查，默认优先并行；单一根因裁决、接口边界冻结、数据库 schema 变更等必须先串行定边界，但其旁路证据收集可在边界清晰时条件并行。",
      "core_responsibility": "负责判断当前工作应并行、条件并行还是串行推进；若允许并行且无阻断，继续联动 `subagent-dispatch-rules` 发起真实子线程，并输出并行技能与文件归属。",
      "skill_path": "parallel-task-dispatch-rules/SKILL.md",
      "directory_path": "parallel-task-dispatch-rules",
      "directory": "parallel-task-dispatch-rules",
      "sections": [
        "目标",
        "核心判定规则",
        "典型分类",
        "分发流程",
        "输出要求",
        "与 subagent-dispatch-rules 的联动闸门",
        "执行通过 / 驳回标准",
        "references 读取规则"
      ],
      "references": [
        "parallel-task-dispatch-rules/references/existing-skill-mapping.md",
        "parallel-task-dispatch-rules/references/task-classification.md",
        "parallel-task-dispatch-rules/references/thread-template.md"
      ],
      "agents": [
        "parallel-task-dispatch-rules/agents/openai.yaml"
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
      "item_order": 12,
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
      "id": "skill-hit-check-rules",
      "name": "skill-hit-check-rules",
      "title": "Skill 命中检查规则（最小闭环版）",
      "status": "implemented",
      "status_label": "已实现",
      "domain_id": "orchestration",
      "domain_label": "总控层",
      "domain_description": "流程分流、冲突裁决、阶段阻断与全局基础约定",
      "domain_order": 1,
      "item_order": 13,
      "auto_trigger": "【强制总控】每轮用户新消息（含新会话第一条）都必须先做命中检查并在首条中间进度输出。凡涉及 Git 协作动作（含显式关键词与隐式语义，如“提交git/帮我提交/commit一下/推送代码/看下状态”），必须联动命中 git-collaboration-rules。凡处理本仓库任务，最低还必须联动命中 `parallel-task-dispatch-rules`，并执行 Obsidian 知识流选择性默认判断，输出 `Obsidian:<检索/沉淀/不适用/阻断>`；当判断为 `检索` 或 `沉淀` 时必须同时命中 `obsidian-knowledge-flow`。首条中间进度最小必填包含 `命中检查`、`命中技能`，若本轮命中 `parallel-task-dispatch-rules` 还必须追加 `并行技能`。",
      "core_responsibility": "在每轮开始前强制执行命中检查并显式回报命中列表，避免静默漏触发。",
      "skill_path": "skill-hit-check-rules/SKILL.md",
      "directory_path": "skill-hit-check-rules",
      "directory": "skill-hit-check-rules",
      "sections": [
        "-1.4 极简硬闸门（强制）",
        "-1.5 违规处理（强制）",
        "-1. 触发确认（强制）",
        "-1.0 新会话首轮保障（强制）",
        "-1.1 Git 意图识别（强制）",
        "-1.1.1 Git 仅限当前轮次（新增，强制）",
        "-1.2 Git 判定优先级（强制）",
        "-1.3 新会话首轮联动（强制）",
        "0. 首条消息格式（强制）",
        "1. 最小流程",
        "1.1 首条闸门（强制阻断）",
        "2. Git 联动闸门（强制）",
        "2.3 Skill 资产改动联动闸门（强制）",
        "3. 通过标准",
        "4. 执行文件"
      ],
      "references": [
        "skill-hit-check-rules/references/hit-checklist.md",
        "skill-hit-check-rules/references/output-format.md"
      ],
      "agents": [
        "skill-hit-check-rules/agents/openai.yaml"
      ],
      "has_license": false,
      "focus_points": [
        "优先检查 description 是否具体到触发信号，而不是只写抽象用途。",
        "检查 references 是否足以承接复杂场景，避免 SKILL.md 过厚或过空。",
        "重点看是否只做分流、阻断或全局基础约定，没有越权覆盖单域 skill。"
      ]
    },
    {
      "id": "code-snippet-location-rules",
      "name": "code-snippet-location-rules",
      "title": "代码片段位置定位规则",
      "status": "implemented",
      "status_label": "已实现",
      "domain_id": "orchestration",
      "domain_label": "总控层",
      "domain_description": "流程分流、冲突裁决、阶段阻断与全局基础约定",
      "domain_order": 1,
      "item_order": 14,
      "auto_trigger": "当用户只粘贴一段代码、报错片段、函数片段或截图转写代码，并说“这里改一下/这段需要修改/这里有问题”等，但没有明确给出文件路径、符号全名、模块位置或可唯一定位的代码位点时触发。负责先按“用户明确路径、当前活动编辑器/当前打开文件/当前选区、代码片段精确匹配、仓库搜索候选、询问确认”的优先级定位真实目标文件，避免把相似代码误判到仓库其他位置；不要用它代替 code-context-resync-rules 的已知文件重读，也不要代替具体业务实现、Bug 定位或代码修改规则。",
      "core_responsibility": "负责按“用户明示路径 > 当前活动编辑器 / 当前打开文件 / 当前选区 > 代码片段精确匹配 > 仓库搜索候选 > 询问确认”的优先级定位真实目标文件，避免把相似代码误判到其他位置。",
      "skill_path": "code-snippet-location-rules/SKILL.md",
      "directory_path": "code-snippet-location-rules",
      "directory": "code-snippet-location-rules",
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
        "code-snippet-location-rules/references/source-priority.md"
      ],
      "agents": [
        "code-snippet-location-rules/agents/openai.yaml"
      ],
      "has_license": false,
      "focus_points": [
        "优先检查 description 是否具体到触发信号，而不是只写抽象用途。",
        "检查 references 是否足以承接复杂场景，避免 SKILL.md 过厚或过空。",
        "重点看是否只做分流、阻断或全局基础约定，没有越权覆盖单域 skill。"
      ]
    },
    {
      "id": "subagent-dispatch-rules",
      "name": "subagent-dispatch-rules",
      "title": "子代理分发规则",
      "status": "implemented",
      "status_label": "已实现",
      "domain_id": "orchestration",
      "domain_label": "总控层",
      "domain_description": "流程分流、冲突裁决、阶段阻断与全局基础约定",
      "domain_order": 1,
      "item_order": 15,
      "auto_trigger": "当任一 skill 已命中并准备进入执行阶段时自动触发。负责先自动判断当前任务是否满足 subagent 委派条件；委派判定不需要用户逐次要求，但真实启动必须服从当前环境的 subagent / multi-agent / thread 工具元数据、系统规则和权限策略。本仓库默认采用 subagent 完全授权模式：用户已明确允许 agent 在任务可切分、写集不冲突、风险可控时自动启动 subagent；该项目级 standing authorization 视为满足工具的显式授权条件。只有缺少当前轮授权且缺少项目级完全授权声明时，才判定为“工具授权不支持自动启动”并回退本地执行。不要用它代替需求分析、Bug 定位、编码实现、测试验证或交付收口本身。",
      "core_responsibility": "作为全局委派协调层，统一判定“可委派/不可委派/本地优先”，优先分发代码规则、注释、审查等 sidecar 子任务并回收结果；并强制主 agent 输出可见的 subagent 启动/完成状态、逻辑名与平台昵称映射，以及计划线程数、实际启动线程数与回收关闭线程数。",
      "skill_path": "subagent-dispatch-rules/SKILL.md",
      "directory_path": "subagent-dispatch-rules",
      "directory": "subagent-dispatch-rules",
      "sections": [
        "Skill 作用与适用场景",
        "自动触发信号",
        "进入后先做什么",
        "默认执行流程",
        "主 agent 可见公告（强制）",
        "真实启动证据（强制）",
        "平台能力矩阵（新增）",
        "并发上限与空闲回收（强制）",
        "子任务优先委派清单",
        "必须主 agent 本地执行的场景",
        "权责边界与不负责事项",
        "需要暂停并确认的条件",
        "执行通过 / 驳回标准",
        "references 读取规则"
      ],
      "references": [
        "subagent-dispatch-rules/references/blockers-and-fallbacks.md",
        "subagent-dispatch-rules/references/delegation-decision-matrix.md",
        "subagent-dispatch-rules/references/examples/launch-plan-input-batched.json",
        "subagent-dispatch-rules/references/examples/launch-plan-input.json",
        "subagent-dispatch-rules/references/examples/launch-plan-output-batched.json",
        "subagent-dispatch-rules/references/examples/launch-plan-output.json",
        "subagent-dispatch-rules/references/launch-plan-schema.md",
        "subagent-dispatch-rules/references/subagent-task-templates.md"
      ],
      "agents": [
        "subagent-dispatch-rules/agents/openai.yaml"
      ],
      "has_license": false,
      "focus_points": [
        "优先检查 description 是否具体到触发信号，而不是只写抽象用途。",
        "检查 references 是否足以承接复杂场景，避免 SKILL.md 过厚或过空。",
        "重点看是否只做分流、阻断或全局基础约定，没有越权覆盖单域 skill。"
      ]
    },
    {
      "id": "skill-audit-rules",
      "name": "skill-audit-rules",
      "title": "Skill 审计规则",
      "status": "implemented",
      "status_label": "已实现",
      "domain_id": "orchestration",
      "domain_label": "总控层",
      "domain_description": "流程分流、冲突裁决、阶段阻断与全局基础约定",
      "domain_order": 1,
      "item_order": 16,
      "auto_trigger": "【强制自动触发】当主任务存在多 skill 组合、并行拆分或规则收口风险时触发。负责只读审计当前任务是否漏触发应有的 skill，以及已触发 skill 是否还有未执行完的规则；默认优先并行；输出补漏提醒和遗漏清单。只有存在原执行计划内未完成必需项、阻断缺口或用户明确要求建议时，才输出必要后续动作；不得把可选优化伪装成必需后续，原始目标已完成且无三类合法后续时不得输出下一步类占位文案。本 skill 不改代码、不写文件、不做最终收口。",
      "core_responsibility": "负责只读审计是否漏触发应有 skill，以及已触发 skill 是否还有未执行完的规则。",
      "skill_path": "skill-audit-rules/SKILL.md",
      "directory_path": "skill-audit-rules",
      "directory": "skill-audit-rules",
      "sections": [
        "目标",
        "核心职责",
        "输入",
        "输出",
        "边界",
        "使用时机"
      ],
      "references": [],
      "agents": [
        "skill-audit-rules/agents/openai.yaml"
      ],
      "has_license": false,
      "focus_points": [
        "优先检查 description 是否具体到触发信号，而不是只写抽象用途。",
        "检查 references 是否足以承接复杂场景，避免 SKILL.md 过厚或过空。",
        "重点看是否只做分流、阻断或全局基础约定，没有越权覆盖单域 skill。",
        "当前没有 references，可考虑补最小示例或边界文档以降低后续维护成本。"
      ]
    },
    {
      "id": "skill-compliance-gate-rules",
      "name": "skill-compliance-gate-rules",
      "title": "Skill 执行完整性闸门规则",
      "status": "implemented",
      "status_label": "已实现",
      "domain_id": "orchestration",
      "domain_label": "总控层",
      "domain_description": "流程分流、冲突裁决、阶段阻断与全局基础约定",
      "domain_order": 1,
      "item_order": 17,
      "auto_trigger": "【收口强制触发】只要本轮有代码新增/修改，最终回复前必须命中本 skill。负责检查已命中 skill 是否完整执行（特别是注释双 skill 与 `implementation-review-rules` 的测试前收口）。若存在原执行计划内未完成必需项或阻断级规则缺口，禁止给“已完成”结论；最终收口只允许三类合法后续：原执行计划内未完成必需项、阻断项、用户显式要求的建议/backlog。除此之外默认直接结束，不额外制造任何下一步区块、下一步建议、等待指令文案或“无需继续动作”占位。",
      "core_responsibility": "在最终回复前执行一次 skill 完整性闸门检查，补齐主任务优先的下一步建议，并对代码改动执行注释终检。",
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
        "优先检查 description 是否具体到触发信号，而不是只写抽象用途。",
        "检查 references 是否足以承接复杂场景，避免 SKILL.md 过厚或过空。",
        "重点看是否只做分流、阻断或全局基础约定，没有越权覆盖单域 skill。"
      ]
    },
    {
      "id": "reasoning-summary-structure-rules",
      "name": "reasoning-summary-structure-rules",
      "title": "推理总结结构闸门规则",
      "status": "implemented",
      "status_label": "已实现",
      "domain_id": "orchestration",
      "domain_label": "总控层",
      "domain_description": "流程分流、冲突裁决、阶段阻断与全局基础约定",
      "domain_order": 1,
      "item_order": 18,
      "auto_trigger": "当进入本轮最终推理总结或结束输出阶段时自动触发。负责强制检查总结结构是否完整：必须包含 Skill 命中检查、Skill 执行证据、当前要解决的问题（同时写清用户原始需求与模型理解的需求）、问题的解决方案与根因、验证结果（有验证时）以及当前结果与结论；若本轮有改动必须包含本次改动点（放在总结最后）。最终总结必须与推理过程视觉分界，采用统一严谨的 markdown 排版（`---` 分隔线 + 固定一级主标题 `# 📋 本轮总结` + 二级标题小节 + 表格 / 引用块 / 状态徽章），标题字号大于正文且加粗、层级分明。默认禁止“下一步状态/建议”区块；只有存在原执行计划内未完成必需项、阻断项，或用户明确要求提供后续建议时，才允许出现后续内容。原始用户目标完成、用户明确要求结束，或仅剩可选优化时强制无下一步，禁止输出下一步区块、等待类文案或“无需继续动作”占位文案。不要用它代替需求分析、Bug 定位、实现修改或测试执行。",
      "core_responsibility": "作为最终总结结构闸门，统一收口输出顺序和必填字段，防止关键信息缺失。",
      "skill_path": "reasoning-summary-structure-rules/SKILL.md",
      "directory_path": "reasoning-summary-structure-rules",
      "directory": "reasoning-summary-structure-rules",
      "sections": [
        "Skill 作用与适用场景",
        "自动触发信号",
        "进入后先做什么",
        "默认执行流程",
        "输出要求（固定顺序）",
        "总结视觉规范（强制）",
        "权责边界与不负责事项",
        "执行通过 / 驳回标准",
        "references 读取规则"
      ],
      "references": [
        "reasoning-summary-structure-rules/references/conditional-sections-rules.md",
        "reasoning-summary-structure-rules/references/output-examples.md",
        "reasoning-summary-structure-rules/references/summary-structure-template.md"
      ],
      "agents": [
        "reasoning-summary-structure-rules/agents/openai.yaml"
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
      "auto_trigger": "当当前会话刚开始、缺少历史上下文、用户直接提出与当前项目相关的需求、Bug、编码、测试或交付问题时自动触发。负责优先从 `artifact-storage-rules` 约定的近 3 天需求、测试、Bug、文档、项目专属 skill 根目录和 git 提交中提取最近活动，并按需加载系统的所有 skills 与当前项目根目录下 `./skill`、`./.skills` 的 skill 清单；如果当前任务涉及整项目分析、架构梳理或模块总览，也可额外读取根目录 `项目设计.md` 及其同类设计文档作为弱参考源，但不把它当成最新事实；如果部分目录不存在，则只使用存在的目录和 git 信息；不要把它代替 history-recall-rules 的深度历史回忆、project-timeline-rules 的长期时间线、project-design-doc-rules 的设计文档同步，或当前主域本身的分析执行。",
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
      "id": "obsidian-knowledge-flow",
      "name": "obsidian-knowledge-flow",
      "title": "Obsidian 知识流",
      "status": "implemented",
      "status_label": "已实现",
      "domain_id": "memory",
      "domain_label": "记忆域",
      "domain_description": "新会话近期预热、跨会话历史检索、项目演进回顾、长期上下文补全",
      "domain_order": 2,
      "item_order": 3,
      "auto_trigger": "将固定根目录的 Obsidian vault 作为 Codex 会话知识库管理，并在仓库任务中采用“选择性默认”触发：每轮先轻量判断 `Obsidian:<检索/沉淀/不适用/阻断>`，只有问题依赖历史决策、项目事实、用户偏好、重复实体、知识库内容或“上次/之前/我们约定/当时怎么说”等历史信息时，才通过 Obsidian CLI 检索相关笔记；会话总结、阶段收口或最终回复前，只有存在可复用的事实、决策、流程、定义、偏好、来源或调试经验时，才通过 Obsidian CLI 捕获/沉淀为 Markdown 笔记。适用于 Obsidian、vault、Markdown 知识库、第二大脑、知识图谱、自动会话笔记、知识提取、快速回忆、本地笔记库、知识库检索、会话总结沉淀和 CLI 笔记操作场景。",
      "core_responsibility": "负责输出 `Obsidian:<检索/沉淀/不适用/阻断>` 判定；只有 `检索` 或 `沉淀` 才通过 Obsidian CLI 读取、捕获或沉淀笔记，CLI / vault 不可用时阻断且不得直接读写 vault 文件。",
      "skill_path": "obsidian-knowledge-flow/SKILL.md",
      "directory_path": "obsidian-knowledge-flow",
      "directory": "obsidian-knowledge-flow",
      "sections": [
        "目标",
        "选择性默认判定",
        "固定根目录",
        "工作流程",
        "捕获规则",
        "检索规则",
        "命令行约定"
      ],
      "references": [
        "obsidian-knowledge-flow/references/capture-retrieve-distill.md",
        "obsidian-knowledge-flow/references/cli-operations.md",
        "obsidian-knowledge-flow/references/conflict-staleness.md",
        "obsidian-knowledge-flow/references/note-schema.md",
        "obsidian-knowledge-flow/references/validation-checklist.md",
        "obsidian-knowledge-flow/references/vault-layout.md"
      ],
      "agents": [
        "obsidian-knowledge-flow/agents/openai.yaml"
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
      "item_order": 4,
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
      "id": "project-memory-rules",
      "name": "project-memory-rules",
      "title": "项目记忆规则",
      "status": "implemented",
      "status_label": "已实现",
      "domain_id": "memory",
      "domain_label": "记忆域",
      "domain_description": "新会话近期预热、跨会话历史检索、项目演进回顾、长期上下文补全",
      "domain_order": 2,
      "item_order": 5,
      "auto_trigger": "从对话、代码与项目文档中抽取并维护长期项目记忆，统一写入根目录 `PROJECT_MEMORY.md`。该文件继续作为唯一长期记忆主文件，但内部升级为“人类阅读区 + 底部机器索引区”的单文件双区结构；默认先更新机器索引区，再同步人类阅读区，不得新增 `PROJECT_MEMORY_INDEX.yaml` 等平行记忆根文件。",
      "core_responsibility": "负责维护根目录 `PROJECT_MEMORY.md` 作为唯一长期记忆源，并在规则调整时回写原词条。",
      "skill_path": "project-memory-rules/SKILL.md",
      "directory_path": "project-memory-rules",
      "directory": "project-memory-rules",
      "sections": [
        "核心目标",
        "适用场景",
        "双区模型",
        "默认流程",
        "写入规则",
        "来源优先级",
        "机器索引区结构",
        "人类阅读区同步规则",
        "生命周期与冲突处理",
        "记忆条目结构"
      ],
      "references": [
        "project-memory-rules/references/memory-conflict-and-staleness.md",
        "project-memory-rules/references/memory-entity-types.md",
        "project-memory-rules/references/memory-extraction-workflow.md",
        "project-memory-rules/references/memory-index-schema.md",
        "project-memory-rules/references/memory-relation-types.md",
        "project-memory-rules/references/memory-retrieval-patterns.md",
        "project-memory-rules/references/project-memory-template.md"
      ],
      "agents": [
        "project-memory-rules/agents/openai.yaml"
      ],
      "has_license": false,
      "focus_points": [
        "优先检查 description 是否具体到触发信号，而不是只写抽象用途。",
        "检查 references 是否足以承接复杂场景，避免 SKILL.md 过厚或过空。",
        "重点看它是否只补近期或历史上下文，不越权代替当前需求、Bug、编码或交付判断。"
      ]
    },
    {
      "id": "project-style-rules",
      "name": "project-style-rules",
      "title": "项目风格规则",
      "status": "implemented",
      "status_label": "已实现",
      "domain_id": "memory",
      "domain_label": "记忆域",
      "domain_description": "新会话近期预热、跨会话历史检索、项目演进回顾、长期上下文补全",
      "domain_order": 2,
      "item_order": 6,
      "auto_trigger": "从对话和代码中自动提取、规范化、合并并增量更新项目代码风格示例，写入根目录 `PROJECT_STYLE.md` 作为唯一风格记忆源。用于项目需要长期记住方法、注释、类、结构体、变量、异步、日志、错误处理、接口、工具调用、循环等代码风格样例的场景；后续写代码时由 `code-generation-style-rules` 读取并应用这份风格记忆，本 skill 只负责维护记忆本身，不作为代码生成风格总控入口。当用户给出“根据 skill 补充更新 md / 根据规则更新 md / 按 skill 更新项目 md / 补充更新 md”等聚合指令时，本 skill 负责其中 `PROJECT_STYLE.md` 的检测、缺失则创建、已存在则增量补齐（通常由 `project-agents-bootstrap` 统一编排联动）。",
      "core_responsibility": "负责维护根目录 `PROJECT_STYLE.md` 作为唯一风格记忆源，并在风格调整时回写原样例。",
      "skill_path": "project-style-rules/SKILL.md",
      "directory_path": "project-style-rules",
      "directory": "project-style-rules",
      "sections": [
        "核心目标",
        "适用场景",
        "默认流程",
        "写入规则",
        "来源优先级",
        "风格条目结构"
      ],
      "references": [
        "project-style-rules/references/project-style-template.md"
      ],
      "agents": [
        "project-style-rules/agents/openai.yaml"
      ],
      "has_license": false,
      "focus_points": [
        "优先检查 description 是否具体到触发信号，而不是只写抽象用途。",
        "检查 references 是否足以承接复杂场景，避免 SKILL.md 过厚或过空。",
        "重点看它是否只补近期或历史上下文，不越权代替当前需求、Bug、编码或交付判断。"
      ]
    },
    {
      "id": "requirement-discovery-rules",
      "name": "requirement-discovery-rules",
      "title": "需求主动侦察规则",
      "status": "implemented",
      "status_label": "已实现",
      "domain_id": "requirement",
      "domain_label": "需求域",
      "domain_description": "idea 主动侦察、需求接入、侦察后缺口识别、边界确认、验收前置",
      "domain_order": 3,
      "item_order": 1,
      "auto_trigger": "当用户只提出一句话 idea、粗略想法、老板式方向、新功能愿景或“想做某个能力”，但没有提前整理完整需求资料时触发。负责由 agent 主动侦察、收罗、比对、推理和成文：查当前项目代码、文档、历史需求、数据库线索、配置、上下游服务、第三方调用、关联项目、用户补充的本地项目路径或 URL、GitHub、相关网站和官方 API 文档，形成有证据来源的需求设计、可行方案和最少待确认问题；必须把已验证有复用价值的资料位置、数据库、URL、项目路径和侦察经验转交 `project-memory-rules` 回写长期记忆。不要用它代替需求主文档接入、需求边界裁决、验收标准或编码实施。",
      "core_responsibility": "主动侦察项目、数据库线索、代码、上下游、关联项目、GitHub、相关网站、官方 API 文档和用户补充路径 / URL，形成有证据来源的需求设计，并回写可复用记忆。",
      "skill_path": "requirement-discovery-rules/SKILL.md",
      "directory_path": "requirement-discovery-rules",
      "directory": "requirement-discovery-rules",
      "sections": [
        "核心原则",
        "自动触发信号",
        "进入后先做什么",
        "默认执行流程",
        "权责边界与不负责事项",
        "需要暂停并确认的条件",
        "执行通过 / 驳回标准",
        "执行结果归档要求",
        "references 读取规则"
      ],
      "references": [
        "requirement-discovery-rules/references/discovery-checklist.md",
        "requirement-discovery-rules/references/evidence-and-memory.md",
        "requirement-discovery-rules/references/output-template.md",
        "requirement-discovery-rules/references/requirement-domain-routing.md"
      ],
      "agents": [
        "requirement-discovery-rules/agents/openai.yaml"
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
      "title": "需求接入规则",
      "status": "implemented",
      "status_label": "已实现",
      "domain_id": "requirement",
      "domain_label": "需求域",
      "domain_description": "idea 主动侦察、需求接入、侦察后缺口识别、边界确认、验收前置",
      "domain_order": 3,
      "item_order": 2,
      "auto_trigger": "当用户提出新需求、新功能、新页面、新接口、新模块，且任务刚进入研发阶段、尚未进入实现或 Bug 定位时触发；如果用户只给一句话 idea、老板式方向、粗略想法，或希望 agent 自己找资料、找数据、看代码、查上下游，必须先联动 requirement-discovery-rules 主动侦察。支持从需求 URL、零散资料、物料和补充说明中整理需求，先结合当前项目上下文逐步澄清目标、约束和成功标准，对存在多个合理方向的需求先收敛方案，再补齐到可进入后续代码开发的程度，并将结果沉淀到 `artifact-storage-rules` 约定的需求文档根目录；它同时定义需求域统一文档入口，discovery 形成初稿后必须立即创建或更新需求主文档，同一需求后续只能持续更新由 `artifact-storage-rules` 约定的同一份需求主文档；不要用它代替需求缺口、边界、拆分、变更或验收标准类 skill。",
      "core_responsibility": "把 discovery 或用户资料收口为同一份需求主文档。",
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
      "domain_description": "idea 主动侦察、需求接入、侦察后缺口识别、边界确认、验收前置",
      "domain_order": 3,
      "item_order": 3,
      "auto_trigger": "当需求描述不完整、缺少前提、缺少字段、缺少流程、缺少业务规则、缺少依赖条件、缺少成功标准、存在多种合理解释或关键方案尚未收敛时触发；如果缺口可能通过当前项目、数据库线索、代码、上下游、历史资料、用户补充路径或 URL、GitHub、相关网站或官方 API 文档主动获得，必须先联动 requirement-discovery-rules 侦察。负责识别 discovery 之后仍无法补齐的关键缺口，并在信息不足时阻断盲目编码推进；gap 阶段应在 `doc/2-需求/` 下生成临时缺口文档记录已侦察证据、未补齐项和待确认问题，待用户确认后再将稳定结论回填到同一份需求主文档并删除临时缺口文档；不要用它代替需求边界判断、需求变更判断或验收标准细化 skill。",
      "core_responsibility": "识别 discovery 后仍无法补齐的关键缺口并阻断盲目实现。",
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
      "domain_description": "idea 主动侦察、需求接入、侦察后缺口识别、边界确认、验收前置",
      "domain_order": 3,
      "item_order": 4,
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
      "domain_description": "idea 主动侦察、需求接入、侦察后缺口识别、边界确认、验收前置",
      "domain_order": 3,
      "item_order": 5,
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
      "id": "implementation-planning-rules",
      "name": "implementation-planning-rules",
      "title": "实施规划规则",
      "status": "implemented",
      "status_label": "已实现",
      "domain_id": "requirement",
      "domain_label": "需求域",
      "domain_description": "idea 主动侦察、需求接入、侦察后缺口识别、边界确认、验收前置",
      "domain_order": 3,
      "item_order": 6,
      "auto_trigger": "当来源对象（需求或 Bug）的条件闸门已收敛且前置验收标准已稳定，正式编码前仍需要先把当前优先闭环的文件落点、模块职责、实施周期、阶段步骤、验证步骤和阻断项拆清时触发；当新项目启动、项目初期存在多个需求 / 多份实施总览 / 多个实施周期，需要先建立“需求与实施计划全量顺序实施方案”或实施顺序总表时也触发。若用户准备采纳上一轮建议、方案、修复路线或实施思路并开始执行，但当前还没有正式执行计划，也必须先触发本 skill 把建议收口成可执行实施方案。若当前上下文处于 `Plan Mode`，无论用户问什么，都必须先命中本 skill 作为第一层计划外壳，再按需回流到计划前置 skill 链路中的需求侦察、需求接入、缺口、边界、拆分或其他域；其中 `Plan Mode` 只提升计划链路优先级，不改变这些前置 skill 的职责边界。若运行环境要求使用专用计划包裹输出，包裹层只作为渲染协议，计划正文仍必须遵守本 skill 与模板定义的结构、字段和约束。若用户本轮核心问题本身是在问“这件事怎么做 / 怎么改 / 先给计划 / 先出方案 / 先列步骤”，也必须先命中本 skill；若前置条件尚未齐备，则输出受限计划或阻断计划，而不是不触发。负责把已确认来源对象或已拆分出的当前优先子项转成可执行实施方案，并将结果单独保存到 `artifact-storage-rules` 约定的实施总览/实施周期文档中；在多来源对象场景下还负责创建或更新项目级 / 集合级全量顺序实施方案，作为跨需求执行顺序总表。不要用它代替需求拆分、Bug 定位、验收标准编写、实际编码、测试执行或最终验收。",
      "core_responsibility": "多来源对象先建“需求与实施计划全量顺序实施方案”，再把已确认需求转成可执行实施总览与实施周期，并明确周期顺序、期次定位、周期内最小任务顺序。",
      "skill_path": "implementation-planning-rules/SKILL.md",
      "directory_path": "implementation-planning-rules",
      "directory": "implementation-planning-rules",
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
        "implementation-planning-rules/references/examples/minimum-task-closure-example.md",
        "implementation-planning-rules/references/full-sequence-master-plan.md",
        "implementation-planning-rules/references/plan-boundaries-and-examples.md",
        "implementation-planning-rules/references/plan-entry-checklist.md",
        "implementation-planning-rules/references/plan-output-gate.md",
        "implementation-planning-rules/references/plan-review-checklist.md",
        "implementation-planning-rules/references/plan-structure-template.md",
        "implementation-planning-rules/references/source-notes.md",
        "implementation-planning-rules/references/task-granularity-and-order.md"
      ],
      "agents": [
        "implementation-planning-rules/agents/openai.yaml"
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
      "domain_description": "idea 主动侦察、需求接入、侦察后缺口识别、边界确认、验收前置",
      "domain_order": 3,
      "item_order": 7,
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
      "domain_description": "idea 主动侦察、需求接入、侦察后缺口识别、边界确认、验收前置",
      "domain_order": 3,
      "item_order": 8,
      "auto_trigger": "当任务准备进入实施前确认“做到什么算完成”时触发。负责细化成功条件、异常条件、边界条件和不在范围项，并将前置验收标准单独保存到 `artifact-storage-rules` 约定的验收标准文档中；不要用它代替功能验证、回归验证或最终验收放行。",
      "core_responsibility": "补齐可验证、可测试的前置验收标准。",
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
      "id": "final-acceptance-rules",
      "name": "final-acceptance-rules",
      "title": "最终验收放行规则",
      "status": "implemented",
      "status_label": "已实现",
      "domain_id": "requirement",
      "domain_label": "需求域",
      "domain_description": "idea 主动侦察、需求接入、侦察后缺口识别、边界确认、验收前置",
      "domain_order": 3,
      "item_order": 9,
      "auto_trigger": "当测试与审核均已完成、任务准备最终放行时触发。负责基于来源对象文档（需求或 Bug）、验收标准、实施总览/实施周期、测试结果和审核结果做后置最终验收，并将结论单独保存到 `artifact-storage-rules` 约定的最终验收文档中；不要用它代替前置验收标准、功能验证、回归验证或实现审查。",
      "core_responsibility": "基于验收标准逐条做最终验收，并检查实施周期已按顺序收口、最小任务已有实现 / 真实测试 / 审查 / 验收证据。",
      "skill_path": "final-acceptance-rules/SKILL.md",
      "directory_path": "final-acceptance-rules",
      "directory": "final-acceptance-rules",
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
        "final-acceptance-rules/references/final-acceptance-boundaries.md",
        "final-acceptance-rules/references/final-acceptance-checklist.md",
        "final-acceptance-rules/references/final-acceptance-template.md"
      ],
      "agents": [
        "final-acceptance-rules/agents/openai.yaml"
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
      "id": "bug-discovery-rules",
      "name": "bug-discovery-rules",
      "title": "Bug 主动侦察规则",
      "status": "implemented",
      "status_label": "已实现",
      "domain_id": "bug",
      "domain_label": "Bug 域",
      "domain_description": "问题录入、定位、运行时诊断、修复建议",
      "domain_order": 4,
      "item_order": 2,
      "auto_trigger": "当用户只用一句话、一个现象、几张截图或简短报错描述提出 Bug，但还没有整理复现步骤、定位证据或根因线索时触发。负责由 agent 主动侦察、取证、比对、推理：看代码与调用链（联动 `codegraph-analysis-rules`）、读现有日志 / trace / 配置、按需只读连接本地数据库查数据并做对比、理解用户截图与报错图，形成有证据来源的根因候选、可疑位点和最少待确认问题；连库严格遵守“仅本地、只读查询、禁增删改”的安全红线，需要改数据时只产出 SQL 脚本交用户手动执行；并把已验证可复用的代码入口、表 / 字段、查询线索按 `project-memory-rules` 回写到对应业务项目的长期记忆。不要用它代替 `bug-intake-rules` 的标准化录入、`bug-gap-rules` 的缺口阻断、`bug-reproduction-rules` 的复现、`bug-root-cause-rules` 的最终静态定位、`bug-runtime-debug-rules` 的运行时诊断或修复方案制定。",
      "core_responsibility": "主动侦察取证：看代码与调用链、查日志、只读连本地库比数据、读截图，形成有证据的根因候选；连库仅本地、只读、禁增删改。",
      "skill_path": "bug-discovery-rules/SKILL.md",
      "directory_path": "bug-discovery-rules",
      "directory": "bug-discovery-rules",
      "sections": [
        "核心原则",
        "自动触发信号",
        "进入后先做什么",
        "默认执行流程",
        "连接本地数据库的安全红线（强制）",
        "权责边界与不负责事项",
        "需要暂停并确认的条件",
        "执行通过 / 驳回标准",
        "执行结果归档要求",
        "references 读取规则"
      ],
      "references": [
        "bug-discovery-rules/references/bug-domain-routing.md",
        "bug-discovery-rules/references/discovery-checklist.md",
        "bug-discovery-rules/references/evidence-and-db-readonly.md",
        "bug-discovery-rules/references/output-template.md"
      ],
      "agents": [],
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
      "item_order": 3,
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
      "item_order": 4,
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
      "domain_order": 4,
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
      "domain_order": 4,
      "item_order": 7,
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
      "domain_order": 4,
      "item_order": 9,
      "auto_trigger": "当问题已定位，需要形成修改建议、风险评估、备选方案并判断是否应等待用户确认时触发。负责把 Bug 域稳定交接到编码域，并统一记录到 Bug 根目录；修复方案必须针对根因、从源头消除问题，拒绝打补丁式修复（表层特判绕过、try-catch 吞异常、对坏数据兜底而不修源头、堆叠 if 特判等）。不要用它代替根因定位或直接实施编码修复。",
      "core_responsibility": "先给修改建议，再决定是否实施。",
      "skill_path": "bug-fix-proposal-rules/SKILL.md",
      "directory_path": "bug-fix-proposal-rules",
      "directory": "bug-fix-proposal-rules",
      "sections": [
        "Skill 作用与适用场景",
        "自动触发信号",
        "进入后先做什么",
        "默认执行流程",
        "根因修复优先（反打补丁式修复）",
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
      "item_order": 10,
      "auto_trigger": "【强制自动触发】当 Bug 修复可能影响公共方法、共享模块、已有接口、数据库行为、缓存行为、兼容性或其他历史能力时触发。负责识别回归风险点、风险等级、验证优先级并统一记录到 Bug 根目录；默认优先并行；不要把它代替实际回归测试。",
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
      "id": "code-generation-style-rules",
      "name": "code-generation-style-rules",
      "title": "代码生成风格规则",
      "status": "implemented",
      "status_label": "已实现",
      "domain_id": "baseline",
      "domain_label": "编码基线域",
      "domain_description": "开始编码即并行生效的基础质量规则",
      "domain_order": 5,
      "item_order": 1,
      "auto_trigger": "当新增、修改、重构任意代码、脚本、测试支撑代码或配置型代码前自动触发。负责在正式写代码前读取 `PROJECT_STYLE.md`、当前文件与同目录样例，把项目长期风格记忆和局部既有写法收敛成本轮“代码风格契约”，约束命名、结构、注释、日志、错误处理、复用、排版和禁用写法；写完后执行风格闸门，并在形成新的稳定团队偏好时联动 `project-style-rules` 回写 `PROJECT_STYLE.md`。不替代 `project-style-rules` 的记忆维护职责，也不替代 `code-minimal-change-rules`、`code-readability-rules`、`code-style-consistency-rules`、`naming-rules` 或注释类 skill 的专业检查。",
      "core_responsibility": "读取 `PROJECT_STYLE.md`、当前文件和同目录样例，形成本轮代码风格契约，约束后续实现风格。",
      "skill_path": "code-generation-style-rules/SKILL.md",
      "directory_path": "code-generation-style-rules",
      "directory": "code-generation-style-rules",
      "sections": [
        "核心目标",
        "自动触发信号",
        "进入后先做什么",
        "默认执行流程",
        "风格契约内容",
        "与相邻 Skill 的边界",
        "需要暂停并确认的条件",
        "执行通过 / 驳回标准",
        "references 读取规则"
      ],
      "references": [
        "code-generation-style-rules/references/post-change-style-gate.md",
        "code-generation-style-rules/references/pre-coding-checklist.md",
        "code-generation-style-rules/references/style-contract-template.md",
        "code-generation-style-rules/references/style-priority.md"
      ],
      "agents": [],
      "has_license": false,
      "focus_points": [
        "优先检查 description 是否具体到触发信号，而不是只写抽象用途。",
        "检查 references 是否足以承接复杂场景，避免 SKILL.md 过厚或过空。",
        "重点看它是否能并行生效，并且不抢位点域或审查域职责。"
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
      "item_order": 2,
      "auto_trigger": "当新增或修改代码、调整功能、修复 Bug、补测试支撑代码或整理实现细节时触发。负责约束改动范围、删除无关修改并保持变更聚焦，同时要求编码前显式说明假设和成功标准、实现时坚持简单优先与外科手术式改动；默认反对过度封装和过度抽象接口，大多数代码不需要额外封装或抽象接口，只有存在真实复用、边界隔离、复杂度下降或多实现替换证据时才允许新增封装 / 接口层；不要用它代替可读性、风格一致性、代码归位或测试规范等相邻 skill。",
      "core_responsibility": "严控代码变更范围，杜绝无关修改、冗余改动和过度优化，保证每次变更聚焦单一目标，降低回归风险和排查难度；简单处理禁止顺手引入无收益接口抽象。",
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
      "id": "code-context-resync-rules",
      "name": "code-context-resync-rules",
      "title": "代码上下文重同步规则",
      "status": "implemented",
      "status_label": "已实现",
      "domain_id": "baseline",
      "domain_label": "编码基线域",
      "domain_description": "开始编码即并行生效的基础质量规则",
      "domain_order": 5,
      "item_order": 3,
      "auto_trigger": "当继续修改已有代码时，若发现“当前文件内容与 AI 记忆/上次读取内容不一致”（例如用户手动改过、他人提交已更新、补丁上下文失效）自动触发。负责先重读最新代码并以当前文件为唯一真实基线，在保留用户手动修改的前提下继续实现目标，禁止按旧记忆覆盖还原代码；适用于任意代码文件的二次修改、续改、补丁失败重试和上下文漂移场景。",
      "core_responsibility": "先重读最新文件并以当前内容为基线增量合并，禁止按旧记忆覆盖用户手动改动。",
      "skill_path": "code-context-resync-rules/SKILL.md",
      "directory_path": "code-context-resync-rules",
      "directory": "code-context-resync-rules",
      "sections": [
        "核心原则",
        "自动触发信号",
        "进入后先做什么",
        "默认执行流程",
        "强制禁止项",
        "需要暂停并确认的条件",
        "通过 / 驳回标准",
        "与其他规则的关系"
      ],
      "references": [],
      "agents": [
        "code-context-resync-rules/agents/openai.yaml"
      ],
      "has_license": false,
      "focus_points": [
        "优先检查 description 是否具体到触发信号，而不是只写抽象用途。",
        "检查 references 是否足以承接复杂场景，避免 SKILL.md 过厚或过空。",
        "重点看它是否能并行生效，并且不抢位点域或审查域职责。",
        "当前没有 references，可考虑补最小示例或边界文档以降低后续维护成本。"
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
      "item_order": 4,
      "auto_trigger": "当新增或修改业务代码、工具代码、服务代码、脚本代码或 Bug 修复逻辑时触发。负责约束函数结构、逻辑顺序、复杂度和可维护性，并在功能不变前提下优先让最近改动代码表达更清楚、更直接；要求写库、发请求、改状态、发事件等副作用必须从命名和位置可见，避免 query 与 command 混成一个隐蔽职责；当单文件达到 500 行及以上且仍持续新增功能时，必须触发拆分评估；结构调整落地后必须联动 `comment-placement-granularity-rules` 与 `comment-completion-gate-rules` 完成改动位点注释检查与补齐；业务方法禁止直接用 JSON 字符串 key 取字段，必须经 DTO/对象解析层访问；Go 接入第三方 API 时默认使用结构体解析响应，禁止长期使用 map + key 硬编码解析；同时要求已有公共工具优先复用，禁止同语义重复封装；大多数代码默认不需要封装或抽象接口，抽象只有在简单接口隐藏真实复杂度时才有价值，简单场景禁止为了“解耦”“可测试”“以后扩展”无脑新增接口层、接口实现对、helper、factory、manager、adapter 或单实现包装；不要用它代替最小改动、风格一致性、注释规则或代码归位规则。",
      "core_responsibility": "保证函数结构清晰、逻辑顺序自然、副作用显式和复杂度可控，并用深模块口径拦截浅封装与无脑接口抽象。",
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
        "格式化日志示例",
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
      "item_order": 5,
      "auto_trigger": "当新增或修改任意代码文件、脚本文件、配置型代码或测试代码时触发。负责跟随项目现有写法，并在本轮已触发 `code-generation-style-rules` 时依据其产出的代码风格契约检查局部一致性，避免局部风格跳变和个人偏好入侵；不要用它代替最小改动、可读性、注释规范、代码归位规则或代码生成风格契约入口。",
      "core_responsibility": "跟随项目现有风格，不引入风格跳变。",
      "skill_path": "code-style-consistency-rules/SKILL.md",
      "directory_path": "code-style-consistency-rules",
      "directory": "code-style-consistency-rules",
      "sections": [
        "Skill 作用与适用场景",
        "Go 路由风格约定",
        "Go 局部变量声明风格约定",
        "Go 函数签名风格约定",
        "Go 代码排版补充约定",
        "Go 编码规则清单",
        "自动触发信号",
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
        "code-style-consistency-rules/references/go-coding-rules.md",
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
      "item_order": 6,
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
      "item_order": 7,
      "auto_trigger": "当新增或修改后端、前端或脚本代码中的注释、步骤说明、复杂逻辑解释、临时诊断说明或测试说明，且团队要求注释必须使用中文（除标准协议字段/第三方固定错误原文外）时触发。负责中文注释的语言选择、表达方式和禁忌；不要把它代替注释位置与颗粒度规则。",
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
      "id": "comment-placement-granularity-rules",
      "name": "comment-placement-granularity-rules",
      "title": "注释放置与颗粒度规则",
      "status": "implemented",
      "status_label": "已实现",
      "domain_id": "baseline",
      "domain_label": "编码基线域",
      "domain_description": "开始编码即并行生效的基础质量规则",
      "domain_order": 5,
      "item_order": 8,
      "auto_trigger": "【强制自动触发】本轮发生代码新增/修改时，默认与 `comment-completion-gate-rules` 联动命中；当需要判断注释该不该写、写在哪里、写多细时必须命中。若用户提“补充注释/加注释”但未指定细节，也要默认命中本 skill 做注释落点判定。负责注释放置与颗粒度（含字段注释、边界注释、过期注释治理），不代替中文表达、补齐闸门或 Swagger 规则。",
      "core_responsibility": "统一注释位置、颗粒度、字段相关注释和过期注释治理。",
      "skill_path": "comment-placement-granularity-rules/SKILL.md",
      "directory_path": "comment-placement-granularity-rules",
      "directory": "comment-placement-granularity-rules",
      "sections": [
        "Skill 作用与适用场景",
        "自动触发信号",
        "进入后先做什么",
        "默认执行流程",
        "权责边界与不负责事项",
        "需要暂停并确认的条件",
        "执行通过 / 驳回标准",
        "references 读取规则"
      ],
      "references": [
        "comment-placement-granularity-rules/references/comment-examples.md",
        "comment-placement-granularity-rules/references/comment-granularity.md",
        "comment-placement-granularity-rules/references/comment-placement.md"
      ],
      "agents": [
        "comment-placement-granularity-rules/agents/openai.yaml"
      ],
      "has_license": false,
      "focus_points": [
        "优先检查 description 是否具体到触发信号，而不是只写抽象用途。",
        "检查 references 是否足以承接复杂场景，避免 SKILL.md 过厚或过空。",
        "重点看它是否能并行生效，并且不抢位点域或审查域职责。"
      ]
    },
    {
      "id": "comment-completion-gate-rules",
      "name": "comment-completion-gate-rules",
      "title": "注释补齐闸门规则",
      "status": "implemented",
      "status_label": "已实现",
      "domain_id": "baseline",
      "domain_label": "编码基线域",
      "domain_description": "开始编码即并行生效的基础质量规则",
      "domain_order": 5,
      "item_order": 9,
      "auto_trigger": "【强制自动触发】只要本轮发生任意代码新增/修改，或用户提到“补充注释/只补注释/注释完善/补下注释/加注释”，必须命中本 skill。即使用户只发一句“补充注释”，也必须立即触发并输出注释补齐核对结果。负责改动位点注释补齐闸门：函数头 `[参数]`/`[返回]`/`最近修改时间`、方法体步骤编号、补丁原因注释、函数/补丁核对清单。前端文件与后端文件同等纳入检查。缺任一项不得收口。仅负责补齐闸门，不代替中文表达、注释放置颗粒度或 Swagger 注解规则。",
      "core_responsibility": "统一改动位点注释补齐、函数头元信息、步骤编号和注释缺失阻断闸门。",
      "skill_path": "comment-completion-gate-rules/SKILL.md",
      "directory_path": "comment-completion-gate-rules",
      "directory": "comment-completion-gate-rules",
      "sections": [
        "Skill 作用与适用场景",
        "强制规则：补注释优先范围",
        "强制门禁：改动位点注释补齐",
        "强制门禁：前端必注释位点",
        "强制规则：步骤编号",
        "强制规则：函数头元信息",
        "强制规则：函数注释核对清单（可执行闸门）",
        "强制规则：字段/结构体字面量注释核对清单",
        "强制规则：补丁逻辑注释（做了什么 + 为什么）",
        "自动触发信号",
        "进入后先做什么",
        "默认执行流程",
        "权责边界与不负责事项",
        "需要暂停并确认的条件",
        "执行通过 / 驳回标准",
        "references 读取规则"
      ],
      "references": [
        "comment-completion-gate-rules/references/comment-completion-priority.md",
        "comment-completion-gate-rules/references/comment-examples.md",
        "comment-completion-gate-rules/references/comment-function-metadata.md",
        "comment-completion-gate-rules/references/comment-step-numbering-gate.md"
      ],
      "agents": [
        "comment-completion-gate-rules/agents/openai.yaml"
      ],
      "has_license": false,
      "focus_points": [
        "优先检查 description 是否具体到触发信号，而不是只写抽象用途。",
        "检查 references 是否足以承接复杂场景，避免 SKILL.md 过厚或过空。",
        "重点看它是否能并行生效，并且不抢位点域或审查域职责。"
      ]
    },
    {
      "id": "windows-encoding-rules",
      "name": "windows-encoding-rules",
      "title": "Windows 中文编码防护规则",
      "status": "implemented",
      "status_label": "已实现",
      "domain_id": "baseline",
      "domain_label": "编码基线域",
      "domain_description": "开始编码即并行生效的基础质量规则",
      "domain_order": 5,
      "item_order": 10,
      "auto_trigger": "当任务运行在 Windows（Git Bash / bash、PowerShell 或 CMD）且涉及任意代码、文档、配置、脚本、测试资产或生成文本的读写、日志追加、README/Markdown 修改、脚本输出重定向、Git 提交信息或终端显示时触发。用于预防与修复中文乱码（mojibake）、统一跨平台 UTF-8 写入策略，并在落盘前做编码自检；尤其适用于“看到乱码”“中文变成问号/锟斤拷/Ãxx”“同文件中英正常但中文异常”“追加写入后部分行乱码”“担心文件被 GBK/ANSI/默认编码写入”等场景。",
      "core_responsibility": "统一 Windows 终端与文件中文编码防护，避免中文乱码落盘。",
      "skill_path": "windows-encoding-rules/SKILL.md",
      "directory_path": "windows-encoding-rules",
      "directory": "windows-encoding-rules",
      "sections": [
        "自动触发信号",
        "进入后先做什么",
        "Windows 防错基线",
        "推荐执行流程",
        "落盘命令模板",
        "通过 / 驳回标准",
        "边界"
      ],
      "references": [],
      "agents": [
        "windows-encoding-rules/agents/openai.yaml"
      ],
      "has_license": false,
      "focus_points": [
        "优先检查 description 是否具体到触发信号，而不是只写抽象用途。",
        "检查 references 是否足以承接复杂场景，避免 SKILL.md 过厚或过空。",
        "重点看它是否能并行生效，并且不抢位点域或审查域职责。",
        "当前没有 references，可考虑补最小示例或边界文档以降低后续维护成本。"
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
      "auto_trigger": "当新增或修改工具类、通用方法、公共组件、工具函数、通用常量或复用代码时触发。负责统一公共工具代码的判定标准、存放位置、调用方式和边界；`utils` / `common` / `global` / `middleware` 这类通用包根目录应先按职责拆子目录，再在子目录放实现文件，避免循环依赖和命名冲突；同时强制执行“先检索后新增”，禁止同语义工具重复封装（已存在可复用实现时必须复用，不得再新写一份）；对被多处复用的通用代码执行“7天冻结”策略：最近修改时间超过7天的默认只允许新增能力，不允许直接修改既有行为；最近7天内新增/修改的通用代码可继续迭代；简单处理禁止为了“未来扩展”或“统一模式”提前抽公共接口 / 接口实现对；不要用它代替业务逻辑抽象、包结构规则或具体实现细则。",
      "core_responsibility": "统一通用工具代码的编写规范、复用标准、存放位置和调用方式，避免重复造轮子，保证公共代码的通用性、稳定性和可维护性。",
      "skill_path": "common-util-rules/SKILL.md",
      "directory_path": "common-util-rules",
      "directory": "common-util-rules",
      "sections": [
        "复用红线（强制）",
        "Skill 作用与适用场景",
        "自动触发信号",
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
      "auto_trigger": "当新增或修改数据库、表、字段、索引、唯一约束、外键、迁移脚本、DDL、实体结构、schema 定义或自动建库/建表/建索引启动逻辑时自动触发。负责统一数据库结构变更、迁移安全、兼容性和回滚边界；自动初始化必须覆盖库、表、索引三类对象，启动时若支持自动建库和自动建表，也必须同步具备自动检查并创建缺失索引的流程；数据库表模型必须每张表单独一个文件，自动建表/迁移逻辑、自动建索引逻辑也必须分别放在独立文件中；数据库的字段必须要定义数据类型、默认值、是否需要索引、字段 CHARSET=utf8mb4、ENGINE=InnoDB、注释说明等写清楚，不要遗漏；所有金额相关的要强制使用字符串，避免任何出现精度问题的情况；所有表必须包含 created_at 和 updated_at 字段，由数据库自动管理；必须冗余一个毫秒级时间戳的创建时间，避免数据库的时区问题影响不同的时间格式；所有表必须包含逻辑删除字段，1 的状态标识删除，不是 1 代表正常非删除状态，默认 0=非删除；否则会导致自动创建表出现不可控的因素；避免把查询实现、事务控制和业务逻辑混进结构变更；不要用它代替 database-query-rules、项目配置约束或发布回滚流程。",
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
      "auto_trigger": "当新增或修改 SQL、Repository、DAO、Mapper、QueryBuilder、事务、锁、批量 CRUD、分页查询时自动触发。负责统一数据库访问实现、查询性能、事务与锁边界；GORM 查询、统计、更新、创建、保存必须显式使用 `Model(&models.X{})` 或等价方式声明目标表模型，禁止依赖 `Find(&slice)`、`First(&obj)`、`Create(&obj)`、`Save(&obj)` 的类型推导；避免把 schema 设计、缓存策略和业务逻辑混进数据访问层；不要用它代替 database-schema-rules、缓存策略约束或业务规则本身。",
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
        "结构体解析示例（Go）",
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
        "结构体解析示例（Go）",
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
      "auto_trigger": "当新增或修改后端 HTTP API、Swagger/OpenAPI 框架接入、接口文档注解/注释、Swagger 调试入口、接口分组标签、文档暴露路径或 Swagger 环境开关时触发。负责统一 Swagger/OpenAPI 框架选型边界、接口文档最小必填项、请求/响应同步、调试可用性和暴露安全规则；对存在 HTTP API 且需要联调/调试的后端项目，默认要求使用统一的 Swagger/OpenAPI 方案；本 skill 只负责后端代码中的 Swagger/OpenAPI 框架接入、注解与调试入口，当用户要求生成、更新、刷新、补齐 swag，或导出 OpenAPI/Swagger/Apifox YAML 到 swag/ 目录时，属于文档产物维护，必须转交 swag-openapi-maintainer-rules；不要用它代替 swag-openapi-maintainer-rules、api-endpoint-rules、api-request-rules、api-response-rules、普通业务注释规则或功能验证。",
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
      "auto_trigger": "当新增或修改日志、logger、trace、span、审计日志、脱敏字段、排障字段、日志配置文件或链路透传逻辑时触发。负责统一日志与链路追踪规则，后端日志必须使用项目日志框架且不得使用控制台打印，并通过配置文件管理日志参数；业务日志默认必须使用中文表达，只有协议字段、固定 key、第三方固定原文等少数例外可以保留原文；日志初始化必须在 LoadConfig 之后且仅初始化一次，禁止空配置预初始化；不要用它代替错误处理、响应结构或长期监控告警策略。",
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
        "日志排版规范（新增）",
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
      "auto_trigger": "创建具有鲜明风格、达到生产级质量的高品质前端界面。当用户要求构建 Web 组件、页面或前端应用，或进行前端 UI、组件、样式的调整/改进/界面 Bug 修复时优先使用这个 skill。它会生成有创意、打磨精细的代码，并避免出现千篇一律的 AI 模板化审美。",
      "core_responsibility": "生成具有鲜明风格、生产级质量的前端界面，并在与内部前端规则冲突时优先作为主导 skill。",
      "skill_path": "frontend-design/SKILL.md",
      "directory_path": "frontend-design",
      "directory": "frontend-design",
      "sections": [
        "触发后强制联动",
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
      "auto_trigger": "当新增或修改 React、Vue、前端组件拆分、组件目录归属、props 设计、emits 设计、slots 设计、状态归属、事件上抛、组合方式、hooks、composables、复用边界、受控/非受控切换、渲染副作用或客户端展示逻辑时自动触发。负责组件边界、状态边界、接口契约、组合复用和渲染可维护性；若任务同时涉及前端 UI/组件/样式调整、体验改进或界面 Bug 修复，优先让位给 `frontend-design`，本 skill 仅补充组件工程边界。",
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
      "auto_trigger": "当新增或修改前端页面、页面布局、主题样式、配色、字体、图标、卡片、弹窗、表单、表格、图表、导航、空状态、动画、响应式样式、暗黑模式、设计 token、Tailwind 类名、CSS/SCSS/LESS、`.tsx`/`.jsx`/`.vue`/`.html` 中影响界面视觉和交互体验的代码时自动触发，尤其适用于首页、营销页、品牌展示页、数据面板和需要明确设计方向的前端界面。负责页面视觉方向、信息层级、交互反馈、可访问性、响应式适配和交付前 UI 自审；内置合并后的 UI/UX 设计种子数据与搜索脚本，可在风格不明时辅助定方向；若任务属于前端 UI/组件/样式调整、改进或界面 Bug 修复，优先让位给 `frontend-design`，本 skill 主要做视觉规则补充；不要用它代替纯组件工程拆分、状态管理、接口接线或后端规则。",
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
      "auto_trigger": "【强制自动触发】当功能代码已经完成、准备进入测试前验证时触发。作为唯一自动测试前实现闸门，统一检查 4 组内容：实现质量、格式清理、语法/类型/引用、目录归位/分层边界。负责检查实现是否符合可读性优先、单一职责、命名语义化、注释完整、错误处理明确、日志可追溯、依赖使用审慎、魔法值治理、冗余逻辑清理和编码规范等实现质量要求，并在功能不变前提下检查最近改动代码是否还存在可直接收口的表达层冗余；必须核验本轮改动是否完成 `comment-placement-granularity-rules` 与 `comment-completion-gate-rules` 的改动位点注释检查与补齐；必须完成基础格式、语法/类型/引用、目录归位与依赖方向的测试前收口；必须识别 500 行及以上且持续膨胀的文件并要求拆分或给出拆分方案；必须检查“可复用公共工具是否被重复封装”并拦截重复造轮子；必须检查“最近修改超过7天的高复用通用代码是否被直接修改旧行为”，命中时要求改为新增兼容路径；Go 场景下还需在实现自审阶段扫描 `doc/5-tests/` 外 `*_test.go` 禁放问题，以及本轮改动是否把业务实现直接落在 `internal/service/*.go` 根目录文件，是否把请求/响应/第三方结果结构体散落在 `internal/service` 实现文件，是否在函数/方法内使用 `var (...)` 分组声明局部变量，是否把多参数函数签名直接写成多行参数列表，是否把第三方 API 响应长期用 `map[string]any` + key 硬编码解析；若本轮改动涉及后端 HTTP API，还必须检查 Swagger/OpenAPI 是否同步更新；默认优先并行；不要用它代替功能验证规则。",
      "core_responsibility": "对刚完成的实现做一次测试前静态自审与收口。",
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
        "implementation-review-rules/references/format-cleanup-checks.md",
        "implementation-review-rules/references/placement-and-dependency-checks.md",
        "implementation-review-rules/references/review-boundaries.md",
        "implementation-review-rules/references/review-examples.md",
        "implementation-review-rules/references/review-scope.md",
        "implementation-review-rules/references/syntax-and-reference-checks.md"
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
      "id": "project-change-review-rules",
      "name": "project-change-review-rules",
      "title": "项目当前改动总审查规则",
      "status": "implemented",
      "status_label": "已实现",
      "domain_id": "review",
      "domain_label": "编码审查域",
      "domain_description": "测试前的静态自审、语法检查、清理归位",
      "domain_order": 7,
      "item_order": 2,
      "auto_trigger": "当前改动总审查 skill。两类场景自动成立：用户明确点名 `$project-change-review-rules`、`project-change-review-rules`、说出“审核当前改动/当前 diff”，或本轮存在代码改动且准备最终收口。负责只读审查当前项目未提交改动、已暂存改动和可见新增文件，覆盖需求边界、缺陷、遗漏、安全风险、重复逻辑、未按已命中 skill 规则实现、注释缺失或乱码、日志打印不合规、工具包/公共方法复用不足、代码可读性差、补丁式修补、测试与验证缺口；输出按严重级别排序的问题清单，不直接改代码、不格式化、不提交。",
      "core_responsibility": "对当前工作区 diff 做总审查，补抓边界、风险、遗漏和阻断项。",
      "skill_path": "project-change-review-rules/SKILL.md",
      "directory_path": "project-change-review-rules",
      "directory": "project-change-review-rules",
      "sections": [
        "目标",
        "快速流程",
        "审查矩阵",
        "专门 Skill 联动",
        "读取与证据规则",
        "输出格式",
        "驳回标准",
        "执行结果归档要求",
        "References"
      ],
      "references": [
        "project-change-review-rules/references/checklist.md",
        "project-change-review-rules/references/report-template.md"
      ],
      "agents": [
        "project-change-review-rules/agents/openai.yaml"
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
      "auto_trigger": "当准备进入测试阶段，需要确定测什么、先测什么、测到什么程度、哪些路径必须覆盖、哪些风险只能记录待补测时触发。负责测试优先级、测试类型组合、覆盖范围和资源收口；必须以 `artifact-storage-rules` 与 `test-task-root-layout-rules` 为基准，把策略摘要统一记录到中央约定的测试任务主说明 `README.md` 中，并在需要拆成多轮独立测试时给出多个时间戳根目录方案；若策略涉及 Go 可编译测试路径，还必须同步遵循 `go-test-compile-path-rules`；同时强制禁止为了测试目的污染生产代码（新增测试专用方法、测试专用数据、测试专用结构体字段等）。不要用它代替具体测试资源管理或验证执行 skill。",
      "core_responsibility": "决定测试层级和覆盖重点。",
      "skill_path": "test-strategy-rules/SKILL.md",
      "directory_path": "test-strategy-rules",
      "directory": "test-strategy-rules",
      "sections": [
        "测试隔离红线（强制）",
        "Skill 作用与适用场景",
        "自动触发信号",
        "进入后先做什么",
        "默认执行流程",
        "权责边界与不负责事项",
        "需要暂停并确认的条件",
        "执行通过 / 驳回标准",
        "执行结果归档要求",
        "references 读取规则",
        "项目联调强制规则（新增）",
        "本地环境配置发现与连接（强制）",
        "测试样本分布优先（强制）"
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
      "id": "test-task-root-layout-rules",
      "name": "test-task-root-layout-rules",
      "title": "测试任务根布局规则",
      "status": "implemented",
      "status_label": "已实现",
      "domain_id": "test",
      "domain_label": "测试域",
      "domain_description": "策略、资源、功能验证、浏览器联动与回归",
      "domain_order": 8,
      "item_order": 2,
      "auto_trigger": "当为当前需求、当前 Bug 或当前验证任务新增测试任务目录，或需要决定 `doc/5-tests/` 根目录下的当天时间戳根目录、中文说明目录和 ASCII 真实代码路径镜像布局时触发。负责统一测试任务根目录创建、当天时间戳校验、中文 README 说明目录和真实测试资产镜像布局；不要用它代替散落测试资产迁移、Go 编译路径冲突处理、测试命名规则或测试程序实现规则。",
      "core_responsibility": "统一测试任务根布局。",
      "skill_path": "test-task-root-layout-rules/SKILL.md",
      "directory_path": "test-task-root-layout-rules",
      "directory": "test-task-root-layout-rules",
      "sections": [
        "Skill 作用与适用场景",
        "自动触发信号",
        "强制规则",
        "默认执行流程",
        "权责边界与不负责事项",
        "通过 / 驳回标准",
        "执行结果归档要求",
        "references 读取规则"
      ],
      "references": [
        "test-task-root-layout-rules/references/task-root-layout.md"
      ],
      "agents": [
        "test-task-root-layout-rules/agents/openai.yaml"
      ],
      "has_license": false,
      "focus_points": [
        "优先检查 description 是否具体到触发信号，而不是只写抽象用途。",
        "检查 references 是否足以承接复杂场景，避免 SKILL.md 过厚或过空。",
        "重点看测试策略、资源、功能验证、联调、回归是否已经拆开。"
      ]
    },
    {
      "id": "test-scattered-asset-location-rules",
      "name": "test-scattered-asset-location-rules",
      "title": "测试资产禁散落规则",
      "status": "implemented",
      "status_label": "已实现",
      "domain_id": "test",
      "domain_label": "测试域",
      "domain_description": "策略、资源、功能验证、浏览器联动与回归",
      "domain_order": 8,
      "item_order": 3,
      "auto_trigger": "当发现测试脚本、测试数据、mock、fixture、测试说明、日志或临时验证资产散落在 `doc/5-tests/` 根目录之外，或混放进业务目录、仓库根目录、文档目录和非测试目录时触发。负责识别、阻断并迁移散落测试资产，统一收拢到中央测试根目录下的正确任务目录；不要用它代替测试任务根目录创建、Go 编译路径禁放处理、测试命名规则或测试程序实现规则。",
      "core_responsibility": "收拢散落测试资产。",
      "skill_path": "test-scattered-asset-location-rules/SKILL.md",
      "directory_path": "test-scattered-asset-location-rules",
      "directory": "test-scattered-asset-location-rules",
      "sections": [
        "Skill 作用与适用场景",
        "自动触发信号",
        "强制规则",
        "默认执行流程",
        "权责边界与不负责事项",
        "通过 / 驳回标准",
        "执行结果归档要求",
        "references 读取规则"
      ],
      "references": [
        "test-scattered-asset-location-rules/references/scattered-asset-migration.md"
      ],
      "agents": [
        "test-scattered-asset-location-rules/agents/openai.yaml"
      ],
      "has_license": false,
      "focus_points": [
        "优先检查 description 是否具体到触发信号，而不是只写抽象用途。",
        "检查 references 是否足以承接复杂场景，避免 SKILL.md 过厚或过空。",
        "重点看测试策略、资源、功能验证、联调、回归是否已经拆开。"
      ]
    },
    {
      "id": "go-test-compile-path-rules",
      "name": "go-test-compile-path-rules",
      "title": "Go 测试编译路径规则  只在“Go 测试路径会影响编译和扫描链路”这个问题上使用本 skill。",
      "status": "implemented",
      "status_label": "已实现",
      "domain_id": "test",
      "domain_label": "测试域",
      "domain_description": "策略、资源、功能验证、浏览器联动与回归",
      "domain_order": 8,
      "item_order": 4,
      "auto_trigger": "当 Go 项目中的测试路径会进入编译链路、出现源码目录 `*_test.go`、中文可编译路径，或存在白盒同包测试诉求时触发。负责统一 Go 测试可编译路径必须保持 ASCII、源码目录禁放 `*_test.go`、白盒诉求改用 seam 方案，并把测试资产收回中央测试根目录；不要用它代替测试任务根目录创建、散落测试资产迁移、测试命名规则或测试程序实现规则。",
      "core_responsibility": "统一 Go 测试可编译路径。",
      "skill_path": "go-test-compile-path-rules/SKILL.md",
      "directory_path": "go-test-compile-path-rules",
      "directory": "go-test-compile-path-rules",
      "sections": [
        "Skill 作用与适用场景",
        "自动触发信号",
        "强制规则",
        "默认执行流程",
        "权责边界与不负责事项",
        "通过 / 驳回标准",
        "references 读取规则"
      ],
      "references": [
        "go-test-compile-path-rules/references/go-compile-path.md"
      ],
      "agents": [
        "go-test-compile-path-rules/agents/openai.yaml"
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
      "item_order": 5,
      "auto_trigger": "当创建或修改测试时间戳根目录、中文说明目录、测试文件、测试脚本、测试数据目录、fixture 目录、mock 目录时触发。负责统一测试目录与文件命名规范，保证名称可读、可检索、与业务目标一致；必须以 `artifact-storage-rules` 与 `test-task-root-layout-rules` 为基础，遵循中央约定的时间戳根目录、中文说明目录和真实代码路径镜像目录命名规则；涉及 Go 可编译路径时，还必须服从 `go-test-compile-path-rules`；同时强制禁止为了测试目的污染生产代码（新增测试专用方法、测试专用数据、测试专用结构体字段等）。不要用它代替 test-task-root-layout-rules、test-program-rules、test-doc-rules 或功能验证规则。",
      "core_responsibility": "统一测试目录和文件命名。",
      "skill_path": "test-naming-rules/SKILL.md",
      "directory_path": "test-naming-rules",
      "directory": "test-naming-rules",
      "sections": [
        "测试隔离红线（强制）",
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
      "item_order": 6,
      "auto_trigger": "当新增或修改测试程序、模拟程序、验证脚本、数据构造脚本、测试辅助代码时触发。负责统一测试程序职责拆分、辅助代码边界和长期保留策略；必须以 `artifact-storage-rules` 与 `test-task-root-layout-rules` 为基准，把真实测试代码、脚本、mock、fixture 和执行产物统一落在中央约定的测试时间戳根目录下的 ASCII 真实代码路径镜像目录中；若发现资产散落在 `doc/5-tests/` 根目录之外，应先按 `test-scattered-asset-location-rules` 收拢；Go 场景下还必须遵循 `go-test-compile-path-rules`，避免中文进入会被 Go 工具链编译的路径；测试脚本执行时必须向控制台输出关键过程日志，便于观察执行进度与定位失败步骤；Go 场景下白盒/黑盒/集成测试都遵循同一落点规则，源码目录禁止 `*_test.go`，白盒诉求通过 seam 解决；第三方 API 文档缺失响应模型时，必须先用测试脚本探测真实响应，再反推结构体定义；同时强制禁止为了测试目的污染生产代码（新增测试专用方法、测试专用数据、测试专用结构体字段等）。不要用它代替 test-task-root-layout-rules、test-naming-rules、test-doc-rules、bug-runtime-debug-rules 或功能验证规则。",
      "core_responsibility": "统一测试程序职责和辅助脚本边界。",
      "skill_path": "test-program-rules/SKILL.md",
      "directory_path": "test-program-rules",
      "directory": "test-program-rules",
      "sections": [
        "测试隔离红线（强制）",
        "Skill 作用与适用场景",
        "自动触发信号",
        "进入后先做什么",
        "默认执行流程",
        "权责边界与不负责事项",
        "需要暂停并确认的条件",
        "执行通过 / 驳回标准",
        "执行结果归档要求",
        "references 读取规则",
        "写接口测试脚本的过程日志约定（强制）"
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
      "item_order": 7,
      "auto_trigger": "当新增或修改测试 README、验证说明、测试报告、覆盖说明、测试执行记录时触发。负责统一测试文档的最小结构、记录字段、主文档入口和归档方式；必须以 `artifact-storage-rules` 与 `test-task-root-layout-rules` 为基准，使用中央约定的测试任务主说明 `README.md` 作为中文主说明入口，并把额外文档放到同一时间戳根目录下的 ASCII 真实代码路径镜像目录中；同时强制禁止为了测试目的污染生产代码（新增测试专用方法、测试专用数据、测试专用结构体字段等）。不要用它代替 test-task-root-layout-rules、test-program-rules、functional-validation-rules 或 test-regression-rules。",
      "core_responsibility": "统一测试说明文档结构。",
      "skill_path": "test-doc-rules/SKILL.md",
      "directory_path": "test-doc-rules",
      "directory": "test-doc-rules",
      "sections": [
        "测试隔离红线（强制）",
        "Skill 作用与适用场景",
        "自动触发信号",
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
      "item_order": 8,
      "auto_trigger": "面向 AI 代理的浏览器自动化 CLI。当用户需要与网站交互时使用，包括打开页面、填写表单、点击按钮、截图、提取数据、测试 Web 应用，或执行任何浏览器自动化任务。典型触发语句包括“打开一个网站”“填写表单”“点击按钮”“截个图”“抓取页面数据”“测试这个 Web 应用”“登录某个网站”“自动化浏览器操作”，以及任何需要通过程序控制浏览器完成的任务。",
      "core_responsibility": "统一浏览器自动化测试与页面交互执行。",
      "skill_path": "agent-browser/SKILL.md",
      "directory_path": "agent-browser",
      "directory": "agent-browser",
      "sections": [
        "核心工作流",
        "实战经验优先流程（新增）",
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
        "测试截图清理（强制）",
        "Ref 生命周期（重要）",
        "带标注的截图（Vision 模式）",
        "语义定位器（Refs 的替代方案）",
        "JavaScript 求值（eval）",
        "配置文件",
        "深入文档",
        "浏览器引擎选择",
        "观测面板（Observability Dashboard）",
        "可直接使用的模板",
        "项目联调强制规则（新增）"
      ],
      "references": [
        "agent-browser/references/authentication.md",
        "agent-browser/references/browser-operation-lessons.md",
        "agent-browser/references/commands.md",
        "agent-browser/references/profiling.md",
        "agent-browser/references/proxy-support.md",
        "agent-browser/references/screenshot-cleanup.md",
        "agent-browser/references/session-management.md",
        "agent-browser/references/snapshot-refs.md",
        "agent-browser/references/tapd-workflow-automation.md",
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
      "item_order": 9,
      "auto_trigger": "当需要验证新功能、修改后的功能、接口行为、页面交互、输入输出结果是否满足当前需求、当前变更和验收标准时触发。负责界定本次功能验证范围、验证步骤、通过驳回标准和结论留痕；必须以 `artifact-storage-rules` 与 `test-task-root-layout-rules` 为基准，把功能验证结论写回中央约定的测试任务主说明 `README.md`，并把详细执行证据放到同一时间戳根目录下的 ASCII 真实代码路径镜像目录中；若该镜像路径会进入 Go 编译链路，还必须同步遵循 `go-test-compile-path-rules`；同时强制禁止为了测试目的污染生产代码（新增测试专用方法、测试专用数据、测试专用结构体字段等）。不要用它代替 test-strategy-rules、test-task-root-layout-rules 或 test-regression-rules。",
      "core_responsibility": "负责当前需求对应的功能正确性验证。",
      "skill_path": "functional-validation-rules/SKILL.md",
      "directory_path": "functional-validation-rules",
      "directory": "functional-validation-rules",
      "sections": [
        "测试隔离红线（强制）",
        "Skill 作用与适用场景",
        "自动触发信号",
        "进入后先做什么",
        "默认执行流程",
        "权责边界与不负责事项",
        "需要暂停并确认的条件",
        "执行通过 / 驳回标准",
        "执行结果归档要求",
        "references 读取规则",
        "项目联调强制规则（新增）",
        "功能验证样本分布（强制）"
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
      "item_order": 10,
      "auto_trigger": "当 Bug 修复、原有功能迭代、公共模块修改、共享逻辑调整、接口兼容性变化后准备执行测试时触发。负责判定回归范围、选择回归用例、验证兼容性影响并输出回归结论；必须以 `artifact-storage-rules` 与 `test-task-root-layout-rules` 为基准，把回归结论统一写回中央约定的测试任务主说明 `README.md`，并把详细回归案例、执行证据和补充说明放到同一时间戳根目录下的 ASCII 真实代码路径镜像目录中；若该镜像路径会进入 Go 编译链路，还必须同步遵循 `go-test-compile-path-rules`；同时强制禁止为了测试目的污染生产代码（新增测试专用方法、测试专用数据、测试专用结构体字段等）。不要用它代替 functional-validation-rules、test-strategy-rules 或测试资源管理类规则。",
      "core_responsibility": "明确回归测试的范围、用例选取、验证要点，针对改动点关联的功能、上下游链路做全覆盖验证，防止修复旧 Bug 引入新问题，保障功能兼容性。",
      "skill_path": "test-regression-rules/SKILL.md",
      "directory_path": "test-regression-rules",
      "directory": "test-regression-rules",
      "sections": [
        "测试隔离红线（强制）",
        "Skill 作用与适用场景",
        "自动触发信号",
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
      "id": "project-release-test-rules",
      "name": "project-release-test-rules",
      "title": "项目上线接口测试门禁规则",
      "status": "implemented",
      "status_label": "已实现",
      "domain_id": "test",
      "domain_label": "测试域",
      "domain_description": "策略、资源、功能验证、浏览器联动与回归",
      "domain_order": 8,
      "item_order": 11,
      "auto_trigger": "当需要做上线前项目级全接口测试、替代人工接口回归验证、生成上线接口测试门禁结论时触发。负责在每次执行前扫描并持续更新项目基线资产库（接口清单、Swagger/OpenAPI 双索引、参数来源、依赖图、可复用参数、场景目录、脚本适配和历史结论）、规划测试范围、按依赖图构造请求参数并执行接口验证、给出 agent 判定的接口级结果和上线放行结论；所有测试资产落地到 `doc/5-tests/` 对应时间戳根目录，强制要求请求参数和简要响应为 JSON 字符串，禁止接口明细输出为 Markdown 表格。",
      "core_responsibility": "负责每次执行前扫描并更新接口基线，完成项目级核心接口门禁测试、结论归档与最终放行输入。",
      "skill_path": "project-release-test-rules/SKILL.md",
      "directory_path": "project-release-test-rules",
      "directory": "project-release-test-rules",
      "sections": [
        "测试隔离红线（强制，和现有测试域规则一致）",
        "Skill 作用与适用场景",
        "自动触发信号",
        "首次触发冷启动规则（强制）",
        "接口基线扫描规则（强制）",
        "Swagger/OpenAPI 双索引同步规则（强制）",
        "基线漂移处理规则（强制）",
        "基线资产库持续更新规则（强制）",
        "参数依赖与复用规则（强制）",
        "可复用脚本工具箱优先规则（强制）",
        "进入后先做什么",
        "默认执行流程",
        "权责边界与不负责事项",
        "需要暂停并确认的条件",
        "执行通过 / 驳回标准",
        "执行结果归档要求",
        "references 读取规则"
      ],
      "references": [
        "project-release-test-rules/references/agent-response-judgement.md",
        "project-release-test-rules/references/baseline-asset-rules.md",
        "project-release-test-rules/references/bootstrap-workflow.md",
        "project-release-test-rules/references/dependency-graph-rules.md",
        "project-release-test-rules/references/execution-gate.md",
        "project-release-test-rules/references/existing-test-skill-integration.md",
        "project-release-test-rules/references/interface-inventory-schema.md",
        "project-release-test-rules/references/inventory-reconcile-rules.md",
        "project-release-test-rules/references/openapi-inventory-sync-rules.md",
        "project-release-test-rules/references/output-artifacts.md",
        "project-release-test-rules/references/report-format.md",
        "project-release-test-rules/references/reusable-script-toolbox.md",
        "project-release-test-rules/references/test-data-construction-rules.md",
        "project-release-test-rules/references/test-selection-policy.md"
      ],
      "agents": [
        "project-release-test-rules/agents/openai.yaml"
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
      "title": "Git 协作规则（最小闭环版）",
      "status": "implemented",
      "status_label": "已实现",
      "domain_id": "delivery",
      "domain_label": "交付域",
      "domain_description": "Git 协作与交付说明",
      "domain_order": 9,
      "item_order": 1,
      "auto_trigger": "【强制触发】凡当前这轮用户消息出现 Git 协作动作即触发（显式关键词 + 隐式语义），包括“提交git/帮我提交/commit一下/推送代码/看下状态/看下改动”等；新会话第一条也必须触发。触发后必须与 skill-hit-check-rules 联动命中。默认执行“最小可执行闭环”：短清单 + 阻断脚本 + 统一证据模板。用户明确请求“提交git”时，目标是清空当前全部未提交改动（staged、unstaged、untracked），允许按业务拆分多次提交，不要求一次提交完成，但必须循环到 `git status --short` 为空（除阻断项外）。",
      "core_responsibility": "统一 Git 协作规则。",
      "skill_path": "git-collaboration-rules/SKILL.md",
      "directory_path": "git-collaboration-rules",
      "directory": "git-collaboration-rules",
      "sections": [
        "-1.4 极简硬闸门（新增，强制）",
        "-1.5 首条输出收敛（新增，强制）",
        "-1.6 违规自恢复（新增，强制）",
        "-1. 触发确认（强制）",
        "-1.8 当前轮次授权边界（新增，强制）",
        "-1.0 新会话首轮保障（强制）",
        "-1.1 语义触发扩展（强制）",
        "-1.2 联动前置（强制）",
        "-1.3 口语与缩写兜底（强制）",
        "-1.7 用户显式放行未由代理改动文件（新增，强制）",
        "0. 首条中间进度（强制）",
        "1. 执行短清单（强制按顺序）",
        "1.1 脚本查找与缺失回退（强制）",
        "2. 阻断条件（脚本化/回退等价）",
        "3. 统一证据输出（强制）",
        "4. 通过标准",
        "5. 执行文件"
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
      "id": "code-review-automation-rules",
      "name": "code-review-automation-rules",
      "title": "提交级代码审核规则",
      "status": "implemented",
      "status_label": "已实现",
      "domain_id": "submission_review",
      "domain_label": "提交级专项审查",
      "domain_description": "相对 `main` 的当前分支提交级代码审查，不纳入默认自动审查链",
      "domain_order": 10,
      "item_order": 1,
      "auto_trigger": "当用户主动提出“审核代码”“review 当前分支提交”“审查最近提交”时触发。负责读取项目 `main` 分支最近一条提交时间，并仅审查当前分支在该时间之后且尚未并入 `main` 的提交，逐条输出中文结构化结果（致命/严重/中等/建议），再将汇总报告保存到 `artifact-storage-rules` 约定的 `doc/6-审查/` 主文档位置（同主题覆盖或按中央模板更新）；禁止跨提交混审，禁止把非当前 commit 引入的问题混入结论；不因本轮已有代码改动或准备最终收口而自动触发，这类场景由 `project-change-review-rules` 承接。",
      "core_responsibility": "负责按当前分支未并入 `main` 的提交范围执行逐条代码审查并生成结构化中文报告；不纳入默认自动审查链。",
      "skill_path": "code-review-automation-rules/SKILL.md",
      "directory_path": "code-review-automation-rules",
      "directory": "code-review-automation-rules",
      "sections": [
        "Skill 作用与适用场景",
        "触发信号（显式）",
        "进入后先做什么",
        "默认执行流程",
        "强制规则",
        "权责边界与不负责事项",
        "执行结果归档要求",
        "执行通过 / 驳回标准",
        "references 读取规则"
      ],
      "references": [
        "code-review-automation-rules/references/report-and-wecom.md",
        "code-review-automation-rules/references/review-prompt-template.md",
        "code-review-automation-rules/references/review-workflow.md"
      ],
      "agents": [
        "code-review-automation-rules/agents/openai.yaml"
      ],
      "has_license": false,
      "focus_points": [
        "优先检查 description 是否具体到触发信号，而不是只写抽象用途。",
        "检查 references 是否足以承接复杂场景，避免 SKILL.md 过厚或过空。",
        "重点看它是否只处理相对 `main` 的提交级审查，不回退成当前 diff 总审查或默认自动审查链的一部分。"
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
      "domain_order": 11,
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
      "id": "\"imagegen\"",
      "name": "\"imagegen\"",
      "title": "Image Generation Skill",
      "status": "seed",
      "status_label": "扩展种子",
      "domain_id": "seed",
      "domain_label": "扩展种子",
      "domain_description": "已入库但未并入主规划的参考 skill",
      "domain_order": 11,
      "item_order": 2,
      "auto_trigger": "\"用于生成或编辑位图图片，例如插画、照片、纹理、精灵图、UI 图、概念图、动作帧、透明底抠图等。当用户要“生图”“改图”“参考图出新图”“做 sprite / mockup / 位图素材”时使用。优先使用内置 `image_gen` 工具；如果当前 turn 没有内置工具，就在本地 imagegen 环境可验证时自动切换到捆绑的 CLI 流程，而不是默认阻断。不要用于更适合直接修改 SVG、矢量资源或代码原生图形的任务。\"",
      "core_responsibility": "当前已在仓库中，但尚未并入主规划域表。",
      "skill_path": "imagegen/SKILL.md",
      "directory_path": "imagegen",
      "directory": "imagegen",
      "sections": [
        "顶层模式",
        "脚本路径解析规则（新增）",
        "核心规则",
        "强阻断规则",
        "内置模式保存规则",
        "什么时候用",
        "什么时候不要用",
        "判定思路",
        "工作流",
        "透明底规则",
        "Prompt 增强",
        "Use-case taxonomy",
        "共享 prompt 模板",
        "Prompt 最佳实践",
        "`gpt-image-2` 指南",
        "CLI fallback 专属约定",
        "参考文件"
      ],
      "references": [
        "imagegen/references/cli.md",
        "imagegen/references/codex-network.md",
        "imagegen/references/image-api.md",
        "imagegen/references/local-entrypoints.md",
        "imagegen/references/prompting.md",
        "imagegen/references/sample-prompts.md"
      ],
      "agents": [
        "imagegen/agents/openai.yaml"
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
      "domain_order": 11,
      "item_order": 3,
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
      "domain_order": 11,
      "item_order": 4,
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
      "id": "2d-asset-design",
      "name": "2d-asset-design",
      "title": "2D 素材设计",
      "status": "seed",
      "status_label": "扩展种子",
      "domain_id": "seed",
      "domain_label": "扩展种子",
      "domain_description": "已入库但未并入主规划的参考 skill",
      "domain_order": 11,
      "item_order": 5,
      "auto_trigger": "用于设计、生成和后处理原创 2D 游戏素材。当用户想要新建、重做、补齐、替换、迭代或统一 2D 游戏素材时自动使用；当角色、怪物、Boss、地图、瓦片、场景道具、UI、图标、特效、投射物、掉落物、Sprite Sheet、逐帧动画、Godot 可导入贴图或分层 2D 资源在需求实现过程中成为阻塞项时也自动使用。也用于先从外部素材网站检索候选参考，再把用户选定的截图当作参考板进行风格提炼，重新设计和生成原创素材，而不是直接复用第三方素材作为最终游戏资产。正式素材任务默认先联动共享根目录设计 skill `agent-sprite-forge-design`：先检索参考候选，再出设计图给用户确认，满意后才进入生产和后处理；当进入角色/怪物/Boss 动画或 sprite sheet 生产时，再自动联动共享根目录 `character-sprite-animation-production`。",
      "core_responsibility": "当前已在仓库中，但尚未并入主规划域表。",
      "skill_path": "2d-asset-design/SKILL.md",
      "directory_path": "2d-asset-design",
      "directory": "2d-asset-design",
      "sections": [
        "作用",
        "自动触发范围",
        "核心原则",
        "执行流程",
        "资产类型约束",
        "默认交付规范",
        "额外强约束",
        "输出模式",
        "资源"
      ],
      "references": [
        "2d-asset-design/references/art-direction-quality-gate.md",
        "2d-asset-design/references/asset-modes.md",
        "2d-asset-design/references/character-animation-production-gate.md",
        "2d-asset-design/references/design-preview-confirmation-gate.md",
        "2d-asset-design/references/image-generation-workflow.md",
        "2d-asset-design/references/image-spec-contract.md",
        "2d-asset-design/references/layered-map-contract.md",
        "2d-asset-design/references/map-strategies.md",
        "2d-asset-design/references/postprocess-workflow.md",
        "2d-asset-design/references/project-style-consistency-contract.md",
        "2d-asset-design/references/prompt-rules.md",
        "2d-asset-design/references/prop-pack-contract.md",
        "2d-asset-design/references/reference-only-policy.md"
      ],
      "agents": [
        "2d-asset-design/agents/openai.yaml"
      ],
      "has_license": false,
      "focus_points": [
        "先决定它是并入主规划、保持外部种子，还是拆成多个更窄的内部 skill。",
        "如果准备纳入体系，先补上与主规划域的映射关系和落位说明。",
        "重点看这个种子是否真的能落入主规划，还是保持独立参考更合适。"
      ]
    },
    {
      "id": "agent-sprite-forge-design",
      "name": "agent-sprite-forge-design",
      "title": "Agent Sprite Forge Design",
      "status": "seed",
      "status_label": "扩展种子",
      "domain_id": "seed",
      "domain_label": "扩展种子",
      "domain_description": "已入库但未并入主规划的参考 skill",
      "domain_order": 11,
      "item_order": 6,
      "auto_trigger": "用于在正式生产 2D 游戏素材前完成美术设计收口。吸收 0x0funky/agent-sprite-forge 的 Codex-first 资产设计思路：先检索外部参考候选并让用户选定截图，再判断资产类型、镜头、构图、sheet/layout、分层地图策略和引擎交付方式，最后用图像生成产出设计图预览。适用于角色、怪物、Boss、地图、场景物件、投射物、FX、掉落物、图标等 2D 游戏资产的“先看参考候选、再做设计预览、确认后生产”流程。当用户需要先看方案图、先确认美术方向、先迭代设计稿再落地素材时必须使用。",
      "core_responsibility": "当前已在仓库中，但尚未并入主规划域表。",
      "skill_path": "agent-sprite-forge-design/SKILL.md",
      "directory_path": "agent-sprite-forge-design",
      "directory": "agent-sprite-forge-design",
      "sections": [
        "作用",
        "强制流程",
        "设计阶段最小交付",
        "设计判断",
        "设计图确认闸门",
        "质量红线",
        "和 2d-asset-design 的关系",
        "参考来源"
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
      "id": "artifact-delivery-gate-rules",
      "name": "artifact-delivery-gate-rules",
      "title": "研发文档落盘闸门规则",
      "status": "seed",
      "status_label": "扩展种子",
      "domain_id": "seed",
      "domain_label": "扩展种子",
      "domain_description": "已入库但未并入主规划的参考 skill",
      "domain_order": 11,
      "item_order": 7,
      "auto_trigger": "当需求、实施、验收、Bug、测试或审查任务准备最终收口，且本轮已经产生或应当产生持久化研发文档时自动触发。负责在最终完成前核对文档是否已经真实落盘到 `artifact-storage-rules` 约定的位置，检查主入口文件、必需配套文件和同任务复用关系是否完整；若文档仍停留在最终回复、临时说明或内存结论中，必须阻断收口并先补齐落盘。适用于需求主文档、实施文档、验收文档、Bug 根目录、测试任务 README 与审查报告，不代替需求分析、Bug 定位、测试执行、审核判断或最终验收本身。",
      "core_responsibility": "当前已在仓库中，但尚未并入主规划域表。",
      "skill_path": "artifact-delivery-gate-rules/SKILL.md",
      "directory_path": "artifact-delivery-gate-rules",
      "directory": "artifact-delivery-gate-rules",
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
      "references": [],
      "agents": [
        "artifact-delivery-gate-rules/agents/openai.yaml"
      ],
      "has_license": false,
      "focus_points": [
        "先决定它是并入主规划、保持外部种子，还是拆成多个更窄的内部 skill。",
        "如果准备纳入体系，先补上与主规划域的映射关系和落位说明。",
        "重点看这个种子是否真的能落入主规划，还是保持独立参考更合适。"
      ]
    },
    {
      "id": "authenticated-url-routing-rules",
      "name": "authenticated-url-routing-rules",
      "title": "认证 URL 路由规则",
      "status": "seed",
      "status_label": "扩展种子",
      "domain_id": "seed",
      "domain_label": "扩展种子",
      "domain_description": "已入库但未并入主规划的参考 skill",
      "domain_order": 11,
      "item_order": 8,
      "auto_trigger": "当用户提供任意 URL、链接或网页地址，并要求打开、读取、分析、总结、截图、提取内容、排查页面、查看文档、理解网页、检查资料、访问在线文档或处理已在浏览器登录过的页面时触发。默认优先使用 Chrome Plugin 的 `chrome:control-chrome` 接管用户已登录的真实 Chrome profile，以复用登录态、扩展、权限和已打开标签页；禁止优先使用 `web`、隔离浏览器、无登录态 Playwright 或普通抓取导致权限丢失。若 Chrome Plugin 不可用，再回退到 `agent-browser` 的 auto-connect、state、profile 或 session；若仍遇到登录页、权限页、验证码或人机验证，要求用户在真实 Chrome 中完成授权后继续，不得通过搜索引擎或第三方页面绕过权限。",
      "core_responsibility": "当前已在仓库中，但尚未并入主规划域表。",
      "skill_path": "authenticated-url-routing-rules/SKILL.md",
      "directory_path": "authenticated-url-routing-rules",
      "directory": "authenticated-url-routing-rules",
      "sections": [
        "目标",
        "默认路由",
        "回退顺序",
        "执行要求",
        "Chrome Plugin 确认步骤",
        "实测回灌清单",
        "异常处理",
        "安全边界",
        "通过标准",
        "维护注意事项",
        "常见触发示例"
      ],
      "references": [],
      "agents": [
        "authenticated-url-routing-rules/agents/openai.yaml"
      ],
      "has_license": false,
      "focus_points": [
        "先决定它是并入主规划、保持外部种子，还是拆成多个更窄的内部 skill。",
        "如果准备纳入体系，先补上与主规划域的映射关系和落位说明。",
        "重点看这个种子是否真的能落入主规划，还是保持独立参考更合适。"
      ]
    },
    {
      "id": "autonomous-execution-rules",
      "name": "autonomous-execution-rules",
      "title": "自主连续执行规则",
      "status": "seed",
      "status_label": "扩展种子",
      "domain_id": "seed",
      "domain_label": "扩展种子",
      "domain_description": "已入库但未并入主规划的参考 skill",
      "domain_order": 11,
      "item_order": 9,
      "auto_trigger": "当多步骤任务尚未闭环且存在原执行计划内可直接执行的必需下一步时自动触发（不仅限于回合结束前）。用于多步骤研发任务（需求实现、Bug 修复、重构、测试闭环、文档同步）的连续推进策略：在非关键节点默认自主执行计划内必需动作，不在每个子步骤后征求确认；仅在关键决策节点或高风险节点暂停并给出结构化选项。用户说“开始实施 / 开始实现 / 开始执行 / 直接做 / 继续做完 / 按文档实现 / 按建议执行 / 按方案执行 / 就按你刚才说的做”等开工类指令时，必须已有执行计划，或先给出包含完成定义、停止条件和最大推进边界的本轮计划；缺少计划或停止条件时不得直接实现。若用户给出明确结束指令（如“结束”“停止”“到此为止”“不要继续”“不要下一步建议”“不要扩散”），该指令对所有 agent 通用，必须立即停止自动继续和扩散性输出。任务完成后若不存在“原计划未完成必需项 / 阻断项 / 用户显式要求的建议”三类合法后续，必须强制无下一步，不得输出可能触发循环 loop 的“等待用户新指令 / 无需继续动作 / 下一步状态”占位文案。若刚发生上下文压缩且未重新确认“是否开始/继续实现代码”，必须暂停确认，不得直接进入编码。不要用于绕过系统安全限制、权限审批或高风险操作防护。",
      "core_responsibility": "当前已在仓库中，但尚未并入主规划域表。",
      "skill_path": "autonomous-execution-rules/SKILL.md",
      "directory_path": "autonomous-execution-rules",
      "directory": "autonomous-execution-rules",
      "sections": [
        "目标",
        "执行许可状态（新增）",
        "触发信号",
        "默认执行策略",
        "必须暂停确认的关键节点",
        "关键节点提问格式（强制）",
        "与其他 Skill 的协作",
        "禁止事项",
        "通过 / 驳回标准",
        "快速示例"
      ],
      "references": [],
      "agents": [
        "autonomous-execution-rules/agents/openai.yaml"
      ],
      "has_license": false,
      "focus_points": [
        "先决定它是并入主规划、保持外部种子，还是拆成多个更窄的内部 skill。",
        "如果准备纳入体系，先补上与主规划域的映射关系和落位说明。",
        "重点看这个种子是否真的能落入主规划，还是保持独立参考更合适。"
      ]
    },
    {
      "id": "character-sprite-animation-production",
      "name": "character-sprite-animation-production",
      "title": "Character Sprite Animation Production",
      "status": "seed",
      "status_label": "扩展种子",
      "domain_id": "seed",
      "domain_label": "扩展种子",
      "domain_description": "已入库但未并入主规划的参考 skill",
      "domain_order": 11,
      "item_order": 10,
      "auto_trigger": "用于在 2D 游戏角色、怪物、Boss 或类角色单位需要动作生产时，负责角色动画的生产、分方向拆分、fixed-cell sheet 布局、动作 QA 与预览验证。吸收 character-animation-creator-skill 的核心思路：先锁定角色 identity，再做 base pose，再按动作和方向逐项扩展，并在生成后做 contact sheet、方向一致性、体量漂移和动画可读性审查。适用于 idle、walk、run、attack、cast、hit、death、4向/8向、fixed-cell sprite sheet 等角色动画任务。",
      "core_responsibility": "当前已在仓库中，但尚未并入主规划域表。",
      "skill_path": "character-sprite-animation-production/SKILL.md",
      "directory_path": "character-sprite-animation-production",
      "directory": "character-sprite-animation-production",
      "sections": [
        "作用",
        "自动触发",
        "核心流程",
        "固定格子规则",
        "默认交付",
        "与 2d-asset-design 的关系",
        "参考来源"
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
      "id": "context-compression-rules",
      "name": "context-compression-rules",
      "title": "上下文压缩规则",
      "status": "seed",
      "status_label": "扩展种子",
      "domain_id": "seed",
      "domain_label": "扩展种子",
      "domain_description": "已入库但未并入主规划的参考 skill",
      "domain_order": 11,
      "item_order": 11,
      "auto_trigger": "当当前会话已发生”压缩上下文 / 自动压缩上下文 / 上下文太多”后的压缩重组，或继续执行前刚得到压缩摘要时自动触发。负责在压缩后立即联动 recent-context-bootstrap-rules 重新加载最近项目上下文（含系统的所有 skills 与当前项目根目录下 `./skill`、`./.skills`），并强制重新读取当前项目根目录 `AGENTS.md`（Codex）/ `CLAUDE.md`（Claude Code），避免压缩后丢失 skill 记忆或仓库级硬规则，再输出可直接续做的最小上下文包；压缩包必须显式携带”是否允许开始/继续实现代码”的许可状态，默认 `unknown`，在未重新确认前不得直接进入编码。不要把它代替 history-recall-rules 的深度历史回忆、project-timeline-rules 的长期时间线分析或当前主域执行。",
      "core_responsibility": "当前已在仓库中，但尚未并入主规划域表。",
      "skill_path": "context-compression-rules/SKILL.md",
      "directory_path": "context-compression-rules",
      "directory": "context-compression-rules",
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
        "context-compression-rules/references/boundary-rules.md",
        "context-compression-rules/references/compression-playbook.md",
        "context-compression-rules/references/trigger-signals.md"
      ],
      "agents": [
        "context-compression-rules/agents/openai.yaml"
      ],
      "has_license": false,
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
      "domain_order": 11,
      "item_order": 12,
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
      "id": "golang-patterns",
      "name": "golang-patterns",
      "title": "Go 开发模式",
      "status": "seed",
      "status_label": "扩展种子",
      "domain_id": "seed",
      "domain_label": "扩展种子",
      "domain_description": "已入库但未并入主规划的参考 skill",
      "domain_order": 11,
      "item_order": 13,
      "auto_trigger": "Go 语言惯用模式、最佳实践与编码约定，用于构建健壮、高效、可维护的 Go 应用。",
      "core_responsibility": "当前已在仓库中，但尚未并入主规划域表。",
      "skill_path": "golang-patterns/SKILL.md",
      "directory_path": "golang-patterns",
      "directory": "golang-patterns",
      "sections": [
        "何时启用",
        "核心原则",
        "错误处理模式",
        "并发模式",
        "接口设计",
        "包结构与命名",
        "常量与枚举",
        "结构体与 API 设计",
        "性能与内存",
        "工具链与质量门禁",
        "快速记忆",
        "常见反模式",
        "最终要求"
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
      "id": "image-redbox-focus-rules",
      "name": "image-redbox-focus-rules",
      "title": "图片红框重点关注规则",
      "status": "seed",
      "status_label": "扩展种子",
      "domain_id": "seed",
      "domain_label": "扩展种子",
      "domain_description": "已入库但未并入主规划的参考 skill",
      "domain_order": 11,
      "item_order": 14,
      "auto_trigger": "当用户提交图片、截图、设计稿并希望分析/修改/排查时触发。硬条件：当消息包含 `<image ...>` 时必须命中本 skill。默认将红框（含红色方框、红圈、红线标注）区域视为本轮重点关注信息，优先围绕该区域给出结论与建议；若无红框，再回退到全图分析。",
      "core_responsibility": "当前已在仓库中，但尚未并入主规划域表。",
      "skill_path": "image-redbox-focus-rules/SKILL.md",
      "directory_path": "image-redbox-focus-rules",
      "directory": "image-redbox-focus-rules",
      "sections": [
        "Skill 作用与适用场景",
        "默认提示词",
        "自动触发信号",
        "默认执行流程",
        "输出要求",
        "权责边界与不负责事项",
        "执行通过 / 驳回标准"
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
      "id": "plugin-installation-rules",
      "name": "plugin-installation-rules",
      "title": "插件检测安装使用规则",
      "status": "seed",
      "status_label": "扩展种子",
      "domain_id": "seed",
      "domain_label": "扩展种子",
      "domain_description": "已入库但未并入主规划的参考 skill",
      "domain_order": 11,
      "item_order": 15,
      "auto_trigger": "当用户要求分析项目、检查是否需要安装某个 AI 编码插件 / agent 增强插件，或提到具体插件名（如 Ponytail）需要安装、启用、配置时自动触发。负责通用的\"插件检测 → 安装 → 验证 → 使用 → 回退\"流程，适用于 Claude Code、Codex 等多种 AI 环境；安装命令与配置一律以官方仓库为准，拒绝沿用第三方博客/公众号转述的旧命名、旧参数或臆造命令。具体插件条目（含 Ponytail）见 references/plugin-catalog.md，未来新增插件只追加条目、不改框架；其中标记为【必装】的插件（当前为 Ponytail）在会话 / 项目准备时默认强制安装与启用。不要用它代替 mcp-installation-rules 的 MCP server 判定，也不代替具体编码 / 测试 / 审查 skill。",
      "core_responsibility": "当前已在仓库中，但尚未并入主规划域表。",
      "skill_path": "plugin-installation-rules/SKILL.md",
      "directory_path": "plugin-installation-rules",
      "directory": "plugin-installation-rules",
      "sections": [
        "Skill 作用与适用场景",
        "自动触发信号",
        "进入后先做什么",
        "默认执行流程",
        "必装插件（默认强制）",
        "关键原则",
        "与相邻 skill 的边界",
        "执行通过 / 驳回标准",
        "references 读取规则"
      ],
      "references": [
        "plugin-installation-rules/references/plugin-catalog.md"
      ],
      "agents": [
        "plugin-installation-rules/agents/openai.yaml"
      ],
      "has_license": false,
      "focus_points": [
        "先决定它是并入主规划、保持外部种子，还是拆成多个更窄的内部 skill。",
        "如果准备纳入体系，先补上与主规划域的映射关系和落位说明。",
        "重点看这个种子是否真的能落入主规划，还是保持独立参考更合适。"
      ]
    },
    {
      "id": "skill-split-preserve-rules",
      "name": "skill-split-preserve-rules",
      "title": "Skill 拆分保护规则",
      "status": "seed",
      "status_label": "扩展种子",
      "domain_id": "seed",
      "domain_label": "扩展种子",
      "domain_description": "已入库但未并入主规划的参考 skill",
      "domain_order": 11,
      "item_order": 16,
      "auto_trigger": "当某个现有 skill 已出现多个可独立命中的职责组、触发边界混合或内容膨胀到难以继续承接新增规则，且需要在功能零丢失前提下把它拆成多个独立 skill 并在承接完成后删除旧 skill 时触发。负责先做进入判定、规则原子化、按分类二分拆分、覆盖映射、多轮多模式测试验证、删除前承接检查、按新 skill description 命名并删除旧 skill；不要用它代替普通小修、纯文案润色或业务需求分析。",
      "core_responsibility": "当前已在仓库中，但尚未并入主规划域表。",
      "skill_path": "skill-split-preserve-rules/SKILL.md",
      "directory_path": "skill-split-preserve-rules",
      "directory": "skill-split-preserve-rules",
      "sections": [
        "Skill 作用与适用场景",
        "默认执行流程",
        "强制约束",
        "输出要求",
        "阻断条件",
        "references 读取规则"
      ],
      "references": [
        "skill-split-preserve-rules/references/entry-and-splitting.md",
        "skill-split-preserve-rules/references/mapping-and-deletion.md",
        "skill-split-preserve-rules/references/naming-and-output.md",
        "skill-split-preserve-rules/references/validation-and-testing.md"
      ],
      "agents": [
        "skill-split-preserve-rules/agents/openai.yaml"
      ],
      "has_license": false,
      "focus_points": [
        "先决定它是并入主规划、保持外部种子，还是拆成多个更窄的内部 skill。",
        "如果准备纳入体系，先补上与主规划域的映射关系和落位说明。",
        "重点看这个种子是否真的能落入主规划，还是保持独立参考更合适。"
      ]
    },
    {
      "id": "swag-openapi-maintainer-rules",
      "name": "swag-openapi-maintainer-rules",
      "title": "Swag / OpenAPI 全量维护规则",
      "status": "seed",
      "status_label": "扩展种子",
      "domain_id": "seed",
      "domain_label": "扩展种子",
      "domain_description": "已入库但未并入主规划的参考 skill",
      "domain_order": 11,
      "item_order": 17,
      "auto_trigger": "当用户要求生成、补齐、刷新、维护项目 swag、更新 swag、导出 Apifox/OpenAPI/Swagger 接口文档，或需要让项目所有 HTTP 接口持续同步为 YAML 文档时触发。负责从真实路由、controller、请求 DTO、响应 DTO、统一响应包装和鉴权中间件读取接口契约，生成或更新项目根目录 swag/ 下的全量接口 OpenAPI/Swagger YAML；每个接口单独一个 YAML，同时维护一个包含所有接口的总 YAML。单接口 YAML 默认直导入 Apifox 选中的目录，不额外生成父目录；单接口文件名默认采用“路径名 + 中文简要说明”格式，中文简介后缀必须去掉数字前缀、序号和无业务意义的特殊符号；头部、请求参数、响应字段都必须有中文说明，可在证据充分时做受控推导。本 skill 只生成或维护 swag/ 目录下的 YAML 文档产物，不修改后端代码中的 Swagger 注解、框架接入或调试入口（那属于 api-swagger-rules）；不要用它代替 api-swagger-rules、业务接口实现、接口需求设计、功能测试或线上联调。",
      "core_responsibility": "当前已在仓库中，但尚未并入主规划域表。",
      "skill_path": "swag-openapi-maintainer-rules/SKILL.md",
      "directory_path": "swag-openapi-maintainer-rules",
      "directory": "swag-openapi-maintainer-rules",
      "sections": [
        "Skill 作用与适用场景",
        "自动触发信号",
        "核心约束",
        "默认执行流程",
        "进入后先做什么",
        "执行通过 / 驳回标准",
        "references 读取规则",
        "scripts"
      ],
      "references": [
        "swag-openapi-maintainer-rules/references/description-rules.md",
        "swag-openapi-maintainer-rules/references/discovery-rules.md",
        "swag-openapi-maintainer-rules/references/naming-rules.md",
        "swag-openapi-maintainer-rules/references/schema-rules.md",
        "swag-openapi-maintainer-rules/references/validation-rules.md"
      ],
      "agents": [],
      "has_license": false,
      "focus_points": [
        "先决定它是并入主规划、保持外部种子，还是拆成多个更窄的内部 skill。",
        "如果准备纳入体系，先补上与主规划域的映射关系和落位说明。",
        "重点看这个种子是否真的能落入主规划，还是保持独立参考更合适。"
      ]
    },
    {
      "id": "time-util-rules",
      "name": "time-util-rules",
      "title": "时间处理规则",
      "status": "seed",
      "status_label": "扩展种子",
      "domain_id": "seed",
      "domain_label": "扩展种子",
      "domain_description": "已入库但未并入主规划的参考 skill",
      "domain_order": 11,
      "item_order": 18,
      "auto_trigger": "当新增或修改时间、日期、时区、时间窗、开始结束区间、时间字符串格式化/解析、定时任务或报表快照口径时触发。负责统一强制通过项目内 timeUtil 处理时间；不要用它代替数据库时间规则或业务口径规则。",
      "core_responsibility": "当前已在仓库中，但尚未并入主规划域表。",
      "skill_path": "time-util-rules/SKILL.md",
      "directory_path": "time-util-rules",
      "directory": "time-util-rules",
      "sections": [
        "作用",
        "自动触发",
        "强制规则",
        "执行流程",
        "边界",
        "通过标准"
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
      "id": "vercel-react-best-practices",
      "name": "vercel-react-best-practices",
      "title": "Vercel React 最佳实践",
      "status": "seed",
      "status_label": "扩展种子",
      "domain_id": "seed",
      "domain_label": "扩展种子",
      "domain_description": "已入库但未并入主规划的参考 skill",
      "domain_order": 11,
      "item_order": 19,
      "auto_trigger": "来自 Vercel Engineering 的 React / Next.js 性能优化指南。适用于编写、评审、重构 React/Next.js 代码时，确保采用高性能实现模式。触发场景包括 React 组件、Next.js 页面、数据获取、包体积优化与性能改进任务。",
      "core_responsibility": "当前已在仓库中，但尚未并入主规划域表。",
      "skill_path": "vercel-react-best-practices/SKILL.md",
      "directory_path": "vercel-react-best-practices",
      "directory": "vercel-react-best-practices",
      "sections": [
        "何时使用",
        "按优先级划分的规则类别",
        "快速索引",
        "使用方式",
        "完整汇总文档"
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
      "id": "vue-best-practices",
      "name": "vue-best-practices",
      "title": "Vue 最佳实践工作流",
      "status": "seed",
      "status_label": "扩展种子",
      "domain_id": "seed",
      "domain_label": "扩展种子",
      "domain_description": "已入库但未并入主规划的参考 skill",
      "domain_order": 11,
      "item_order": 20,
      "auto_trigger": "Vue.js 任务必须命中本 skill。默认推荐使用 Composition API + `<script setup>` + TypeScript。覆盖 Vue 3、SSR、Volar、vue-tsc。凡是 Vue、`.vue`、Vue Router、Pinia 或 Vite + Vue 相关工作都应加载。除非项目明确要求 Options API，否则始终优先 Composition API。",
      "core_responsibility": "当前已在仓库中，但尚未并入主规划域表。",
      "skill_path": "vue-best-practices/SKILL.md",
      "directory_path": "vue-best-practices",
      "directory": "vue-best-practices",
      "sections": [
        "核心原则",
        "1) 编码前先确认架构（必做）",
        "2) 应用 Vue 基础能力（必做）",
        "3) 仅在需求明确时使用可选能力",
        "4) 功能正确后再做性能优化",
        "5) 完成前自检"
      ],
      "references": [
        "vue-best-practices/references/animation-class-based-technique.md",
        "vue-best-practices/references/animation-state-driven-technique.md",
        "vue-best-practices/references/component-async.md",
        "vue-best-practices/references/component-data-flow.md",
        "vue-best-practices/references/component-fallthrough-attrs.md",
        "vue-best-practices/references/component-keep-alive.md",
        "vue-best-practices/references/component-slots.md",
        "vue-best-practices/references/component-suspense.md",
        "vue-best-practices/references/component-teleport.md",
        "vue-best-practices/references/component-transition-group.md",
        "vue-best-practices/references/component-transition.md",
        "vue-best-practices/references/composables.md",
        "vue-best-practices/references/directives.md",
        "vue-best-practices/references/perf-avoid-component-abstraction-in-lists.md",
        "vue-best-practices/references/perf-v-once-v-memo-directives.md",
        "vue-best-practices/references/perf-virtualize-large-lists.md",
        "vue-best-practices/references/plugins.md",
        "vue-best-practices/references/reactivity.md",
        "vue-best-practices/references/render-functions.md",
        "vue-best-practices/references/sfc.md",
        "vue-best-practices/references/state-management.md",
        "vue-best-practices/references/updated-hook-performance.md"
      ],
      "agents": [],
      "has_license": false,
      "focus_points": [
        "先决定它是并入主规划、保持外部种子，还是拆成多个更窄的内部 skill。",
        "如果准备纳入体系，先补上与主规划域的映射关系和落位说明。",
        "重点看这个种子是否真的能落入主规划，还是保持独立参考更合适。"
      ]
    },
    {
      "id": "vue-router-best-practices",
      "name": "vue-router-best-practices",
      "title": "vue-router-best-practices",
      "status": "seed",
      "status_label": "扩展种子",
      "domain_id": "seed",
      "domain_label": "扩展种子",
      "domain_description": "已入库但未并入主规划的参考 skill",
      "domain_order": 11,
      "item_order": 21,
      "auto_trigger": "\"Vue Router 4 模式、导航守卫、路由参数以及路由与组件生命周期交互的最佳实践。\"",
      "core_responsibility": "当前已在仓库中，但尚未并入主规划域表。",
      "skill_path": "vue-router-best-practices/SKILL.md",
      "directory_path": "vue-router-best-practices",
      "directory": "vue-router-best-practices",
      "sections": [],
      "references": [],
      "agents": [],
      "has_license": true,
      "focus_points": [
        "先决定它是并入主规划、保持外部种子，还是拆成多个更窄的内部 skill。",
        "如果准备纳入体系，先补上与主规划域的映射关系和落位说明。",
        "重点看这个种子是否真的能落入主规划，还是保持独立参考更合适。"
      ]
    },
    {
      "id": "web-design-guidelines",
      "name": "web-design-guidelines",
      "title": "Web 界面规范审查",
      "status": "seed",
      "status_label": "扩展种子",
      "domain_id": "seed",
      "domain_label": "扩展种子",
      "domain_description": "已入库但未并入主规划的参考 skill",
      "domain_order": 11,
      "item_order": 22,
      "auto_trigger": "用于审查 UI 代码是否符合 Web Interface Guidelines。适用于“帮我审查 UI”“检查可访问性”“设计审计”“UX 评审”“按最佳实践检查网站”等请求。",
      "core_responsibility": "当前已在仓库中，但尚未并入主规划域表。",
      "skill_path": "web-design-guidelines/SKILL.md",
      "directory_path": "web-design-guidelines",
      "directory": "web-design-guidelines",
      "sections": [
        "工作方式",
        "规范来源",
        "使用方式"
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
      "id": "windows-wsl-execution-rules",
      "name": "windows-wsl-execution-rules",
      "title": "Windows / WSL 执行规范（代码在 WSL）",
      "status": "seed",
      "status_label": "扩展种子",
      "domain_id": "seed",
      "domain_label": "扩展种子",
      "domain_description": "已入库但未并入主规划的参考 skill",
      "domain_order": 11,
      "item_order": 23,
      "auto_trigger": "当项目代码位于 WSL 文件系统内（如 `/home/user/project`）、且当前任务发生在 Windows 环境时触发。核心边界：只有执行类动作才优先进入 WSL，例如编译、运行/启动程序、测试、调试、会真实启动运行时的依赖安装；看代码、改代码、搜索、读写规则文件、普通 git 操作与多数只读检查默认优先使用 Git Bash / bash。PowerShell 不作为 Windows 下普通仓库命令入口，只在 `.ps1` 脚本、Windows 专用 cmdlet、PowerShell profile / 编码初始化或用户明确要求时使用。agent 在 WSL 时直接访问代码与执行；agent 在 Windows 时（如 Claude Desktop GUI），普通命令通过 Git Bash / bash 访问 `//wsl.localhost/distro/...` 或等价 Windows 可访问路径，执行类动作再用 `wsl.exe --cd /home/user/project target-command` 进 WSL。无论文件写入发生在 Windows、WSL 还是 Linux，都必须遵守 UTF-8 文件写入规则，禁止 GBK/ANSI/默认编码落盘。回复中需要引用项目内文件路径（Markdown 链接、审查证据路径、截图说明、最终总结里的文件路径等）时同样触发本 skill：这条只看用户查看环境，与 agent 自身运行在 WSL 还是 Windows 无关——只要用户从 Windows 桌面 / GUI 客户端访问、项目代码在 WSL，就必须输出 `\\\\wsl.localhost\\<distro>\\...`，不能因为 agent 本身直接跑在 WSL 内（无需 `wsl.exe` 包裹）就顺手把 `/home/...` 当成用户可打开路径输出。纯 Windows 项目或不需要启动执行的任务，不要误切到 WSL。不要用它代替具体语言/框架实现、测试策略或编码规则。",
      "core_responsibility": "当前已在仓库中，但尚未并入主规划域表。",
      "skill_path": "windows-wsl-execution-rules/SKILL.md",
      "directory_path": "windows-wsl-execution-rules",
      "directory": "windows-wsl-execution-rules",
      "sections": [
        "适用场景",
        "核心架构：先看 agent 在哪运行",
        "什么算执行类命令",
        "为什么只有执行类动作优先在 WSL",
        "路径约定",
        "执行环境分工（agent 在 Windows 时）",
        "命令模板（agent 在 Windows 时）",
        "WSL 内缓存目录建议",
        "不推荐做法",
        "约束总结",
        "与其他规则的协作",
        "参考资料读取规则"
      ],
      "references": [
        "windows-wsl-execution-rules/references/command-templates.md",
        "windows-wsl-execution-rules/references/path-mapping.md",
        "windows-wsl-execution-rules/references/recommended-workflow.md",
        "windows-wsl-execution-rules/references/tool-path-interop.md"
      ],
      "agents": [
        "windows-wsl-execution-rules/agents/openai.yaml"
      ],
      "has_license": false,
      "focus_points": [
        "先决定它是并入主规划、保持外部种子，还是拆成多个更窄的内部 skill。",
        "如果准备纳入体系，先补上与主规划域的映射关系和落位说明。",
        "重点看这个种子是否真的能落入主规划，还是保持独立参考更合适。"
      ]
    },
    {
      "id": "work-report-summary-rules",
      "name": "work-report-summary-rules",
      "title": "工作报告汇总规则",
      "status": "seed",
      "status_label": "扩展种子",
      "domain_id": "seed",
      "domain_label": "扩展种子",
      "domain_description": "已入库但未并入主规划的参考 skill",
      "domain_order": 11,
      "item_order": 24,
      "auto_trigger": "当用户提出“生成年报/月报/周报/日报”“汇总年报/月报/周报/日报”“按项目统计最近提交并输出日报/周报/月报/年报”等请求时触发。负责基于 skill 配置的项目路径与项目名称，统计指定时间范围内的 Git 提交，并按项目补充当前工作区未提交改动对应的“进行中事项”，输出结构化报告（含日期+星期、按项目分组、报告内容点）；报告语言必须为中文且使用 UTF-8 编码，所有时间统一按北京时间；只允许统计当前用户本人提交，严禁混入其他作者提交；日报只统计一天，周报统计自然周，月报统计自然月，年报统计自然年；默认过滤低价值提交（如重命名/回滚/构建/文档/测试），未提交事项也必须使用 Git 工作区真实证据并显式标注为 `进行中`；并按 `?报-YYYYMMDDHHMMSS` 格式自动保存到 `/home/luode/code`（可在配置中覆盖）；不要把它代替发布总结、需求文档或测试报告。",
      "core_responsibility": "当前已在仓库中，但尚未并入主规划域表。",
      "skill_path": "work-report-summary-rules/SKILL.md",
      "directory_path": "work-report-summary-rules",
      "directory": "work-report-summary-rules",
      "sections": [
        "Skill 作用与适用场景",
        "自动触发信号",
        "进入后先做什么",
        "默认执行流程",
        "报告输出要求",
        "权责边界与不负责事项",
        "需要暂停并确认的条件",
        "执行通过 / 驳回标准",
        "references 读取规则"
      ],
      "references": [
        "work-report-summary-rules/references/projects.json",
        "work-report-summary-rules/references/report-format.md",
        "work-report-summary-rules/references/uncommitted-worktree.md"
      ],
      "agents": [
        "work-report-summary-rules/agents/openai.yaml"
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
      "title": "编码 Skill 体系整体计划（持续迭代稿）",
      "kind": "总规划",
      "path": "编码skill.md",
      "is_plan_doc": true
    },
    {
      "id": "doc:AGENTS",
      "name": "AGENTS",
      "file_name": "AGENTS.md",
      "title": "AGENTS.md",
      "kind": "其他文档",
      "path": "AGENTS.md",
      "is_plan_doc": false
    },
    {
      "id": "doc:CLAUDE",
      "name": "CLAUDE",
      "file_name": "CLAUDE.md",
      "title": "AGENTS.md / CLAUDE.md",
      "kind": "其他文档",
      "path": "CLAUDE.md",
      "is_plan_doc": false
    },
    {
      "id": "doc:PROJECT_MEMORY",
      "name": "PROJECT_MEMORY",
      "file_name": "PROJECT_MEMORY.md",
      "title": "项目长期记忆",
      "kind": "其他文档",
      "path": "PROJECT_MEMORY.md",
      "is_plan_doc": false
    },
    {
      "id": "doc:PROJECT_STYLE",
      "name": "PROJECT_STYLE",
      "file_name": "PROJECT_STYLE.md",
      "title": "项目风格记忆",
      "kind": "其他文档",
      "path": "PROJECT_STYLE.md",
      "is_plan_doc": false
    },
    {
      "id": "doc:README",
      "name": "README",
      "file_name": "README.md",
      "title": "luode-skills",
      "kind": "其他文档",
      "path": "README.md",
      "is_plan_doc": false
    },
    {
      "id": "doc:skills拆分",
      "name": "skills拆分",
      "file_name": "skills拆分.md",
      "title": "Skill 拆分 Skill 设计（功能不删减版）",
      "kind": "其他文档",
      "path": "skills拆分.md",
      "is_plan_doc": false
    },
    {
      "id": "doc:项目设计",
      "name": "项目设计",
      "file_name": "项目设计.md",
      "title": "项目设计",
      "kind": "其他文档",
      "path": "项目设计.md",
      "is_plan_doc": false
    }
  ],
  "recommendations": [
    "83 个规划 skill 已全部独立落地，后续优化优先检查 description 命中率、相邻 skill 边界和 references 的信息密度。",
    "当前规划同时包含 `frontend-component-rules` 与 `frontend-ui-visual-rules`，建议前者聚焦组件工程与状态边界，后者聚焦页面视觉与交互体验，避免触发歧义。",
    "可以开始按域做第二轮巡检：先审触发 description 是否足够具体，再审 references 是否过厚、过空或与相邻 skill 重叠。"
  ]
};
