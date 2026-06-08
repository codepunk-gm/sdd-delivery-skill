# SDD Delivery Skill

[中文](#中文说明) | [English](#english)

## 中文说明

SDD Delivery 是一个面向 AI 编程助手的 Spec-first 研发交付技能。安装后，用户不需要记脚本命令，只需要发送 PRD 或选择阶段，AI 就会按流程生成和维护交付产物。

## 如何安装

复制当前 skill 目录到 Codex skills 目录：

```bash
cp -R sdd-delivery ~/.codex/skills/sdd-delivery
```

Windows 可以复制到：

```text
%USERPROFILE%\.codex\skills\sdd-delivery
```

如果通过 Codex 插件市场安装，推荐使用：

```text
/plugin marketplace add codepunk-gm/sdd-delivery-skill
/plugin install sdd-delivery
```

## 如何更新

已经安装过插件时，拉取仓库更新后需要在 Codex 中重新安装或刷新插件，否则可能仍在使用旧版 skill：

```text
/plugin marketplace add codepunk-gm/sdd-delivery-skill
/plugin install sdd-delivery
```

如果客户端支持重载插件，安装后执行：

```text
/reload-plugins
```

然后开启一个新的 Codex 会话再使用。若仍看到旧菜单、旧模板或中英文混排，请检查是否安装了旧插件包，或本地 `~/.codex/skills/sdd-delivery` 中存在旧副本。

## 如何使用

在 Codex 中输入：

```text
使用 sdd-delivery，基于这个 PRD 生成 Spec、技术方案、审查清单、实现任务、单测计划和可观测交付产物。
```

启动后，小智会先给出欢迎语和阶段菜单：

```text
你好，我是小智，SDD Delivery 模式已就位。

你负责把想法、PRD 或现有问题丢过来；我负责把它收拾成可审查的 Spec、技术方案、任务拆分、测试记录和交付证据链。放心，不会一上来就冲进代码里横冲直撞。

默认使用中文产物；关键方案和技术栈会先让你拍板；中途插话、补充、改方向也没关系，我会先保存 checkpoint，再把流程带回正轨。

你现在可以这样开始：
  1. 直接发送 PRD，我从 PRD 转 Spec 开始
  2. 回复阶段编号，从指定阶段开始
  3. 回复“配置”，先调整语言、团队规则和增强能力

阶段菜单
  1. PRD 转 Spec - 把你的想法整理成可检查的需求说明
  2. 需求澄清 - 找出还没说清楚、容易误解的地方
  3. Spec 审查 - 检查需求说明能不能支撑后续开发
  4. 一致性分析 - 看需求、约束和现有项目有没有冲突
  5. 技术方案 - 先设计怎么做，再决定动哪些代码
  6. 方案审查 - 检查方案的风险、兼容性、安全和回滚
  7. 任务拆分 - 把方案拆成一件件可执行的小任务
  8. 代码实现 - 按任务写测试、改代码、记录过程
  9. 单测 - 补齐测试计划、测试结果和覆盖关系
  10. 交付审查 - 最后检查改动是否完整、可交接
  11. 检查点 / 交接 - 保存当前进度，方便中断后继续

小改动可以直接说“轻量模式”。
```

默认助理名为「小智」。小智会使用中文产物，关键方案先确认；如果中途打断或改方向，会记录状态并把流程带回正轨。

## 门禁与自动化边界

SDD Delivery 的门禁是 AI agent 的工作协议，不是强制拦截所有文件写入的运行时沙箱。它通过产物、checkpoint、审查记录和用户确认来约束流程：

- 方案确认：`04-tech-solution.md` 完成后先确认架构、技术栈和实现方向，再进入任务拆分。
- TDD 门禁：先写测试并记录 RED 证据，再进入实现；脚本可辅助扫描覆盖关系，但不能替代真实测试判断。
- 逐任务审查：每个任务后检查边界、测试、实现日志和 checkpoint。
- 无 Python 模式：脚本是加速器和校验助手；没有 Python 时，AI 应手动维护 Markdown / JSON 产物。

这个 skill 提供的是可审查的交付约束和可恢复的证据链，不是硬执行引擎。

## 人机协同审查

每个 feature 目录都能脱离聊天记录被人工审查：

- `11-checkpoint.json`：机器可恢复的状态事实源
- `12-observability.md`：人工可读的进度与质量面板
- `13-dashboard.html`：可选静态业务看板
- `events.jsonl`：追加式过程流水

默认里程碑：M1 需求基线、M2 方案确认、M3 实现受控、M4 验证完成、M5 交付就绪。人工审查结论会写入 checkpoint 的 `human_reviews` 和 `milestones`，并同步展示在 `12-observability.md`。

## 视觉概览

![SDD Delivery Hero](assets/images/sdd-delivery-hero.png)

![SDD Delivery Workflow](assets/images/workflow-diagram.png)

![Friendly Guided Interaction](assets/images/interaction-demo.png)

## 核心能力

1. PRD 转 Spec — 将 PRD 解析为可审查的 Spec 和需求追踪矩阵
2. 需求澄清 — 10 类歧义扫描，每轮最多 5 个问题
3. Spec 审查 — 完整性、可测试性、边界检查
4. 一致性分析 — 四遍交叉产物一致性检查
5. 技术方案 — 基于 repo 证据的方案设计 + 事前验尸
6. 方案审查 — 架构、兼容性、安全、性能、回滚审查
7. 任务拆分 — 带边界标注的可追踪任务拆分
8. 代码实现 — TDD 驱动、逐任务审查、实现日志
9. 单测 — 单测计划 + 单测报告 + SPEC-* 反查覆盖
10. 交付审查 — 边界验证、追踪覆盖、安全审计
11. 检查点 / 交接 — 结构化状态保存，支持中断恢复

## v0.7 SQL 规范命令维护

- `setup_team_rules.py` 支持直接维护 SQL dialect、schema、表前缀、迁移工具、全局规则开关、遗留对象例外和需求级例外。
- 团队可以把通用 SQL 规范放在 `global`，把项目差异放在 `project_overrides`，把临时放行放在 `feature_exceptions`。
- 例外必须写明规则、范围、原因、审批人和失效条件，避免“这次先这样”变成永久债务。

示例：

```bash
python scripts/setup_team_rules.py --root . --sql-dialect postgresql --sql-schema billing --sql-migration-tool alembic
python scripts/setup_team_rules.py --root . --sql-rule query.forbid_select_star=false
python scripts/setup_team_rules.py --root . --sql-allow-legacy "legacy_order::table_case::上游 ERP 既有表"
python scripts/setup_team_rules.py --root . --sql-feature-exception "require_index_for_filter_columns::SPEC-3 export::一次性小表导出::tech lead::2026-09-01 前移除"
python scripts/setup_team_rules.py --root . --validate
```

## v0.6 SQL 规范治理

- SQL 规范进入 `.sdd-delivery/team-rules.json`，支持全局通用规则、项目覆盖和需求级例外。
- `setup_team_rules.py --validate` 会校验 SQL 规则结构、项目覆盖和例外审批字段。
- 技术方案和交付审查模板补充 SQL 规范检查：参数化查询、禁止 `SELECT *`、分页排序、索引、迁移、回滚和事务边界。

## v0.5 企业 MCP 能力复用

- 企业 MCP 能力复用：实现前通过 MCP 查询企业内部工具、资源、组件、服务、API、SDK、脚手架、知识库或运维能力，优先复用已有能力。
- 查询意图：`record_mcp_discovery.py` 支持 `--query-intent`，记录这次 MCP 查询要解决什么能力需求。
- 接入约束：`mcp-component-selection.md` 记录调用方式、参数、权限、endpoint、import、SDK 方法或内部使用说明。
- 方案与任务联动：技术方案、任务拆分和单测计划模板会要求记录能力复用、fallback 和验证要求。

## v0.4 体验与中文一致性增强

- 启动欢迎语：小智会先说明默认中文、方案确认、中断恢复和阶段菜单，降低首次使用成本。
- 阶段菜单：每个阶段增加一句白话说明，帮助新手理解该选哪一步。
- 中文生成物：PRD 解析、可观测面板、HTML dashboard 和观测模板统一使用中文标签。
- 看板标签复用：新增 `dashboard_labels.py`，集中维护 dashboard 文案。
- MCP 看板增强：展示已发现的 MCP server、tool、component 名称，而不只展示数量。
- 校验稳定性：无效 `mcp-discovery.json` 会进入结构化问题列表，不再打断校验流程。
- golden workflow 测试：覆盖中文生成物、MCP 看板和异常校验路径。

## v0.3 工作流增强

- 方案确认门禁：`04-tech-solution.md` 完成后必须确认架构和技术栈，再进入任务拆分。
- 可插拔能力：按需启用前端模板、Java 模块化项目、企业 MCP 能力复用、GitHub 交付资产和团队代码原则。
- 工程化开关：每个能力支持 `enabled` / `disabled` / `ask` 三态，记录在 checkpoint。
- 增强能力规划：自动检测项目特征，按需启用前端模板保护、企业 MCP 能力复用、团队代码原则等能力。
- 团队规则脚本：`setup_team_rules.py` 初始化并校验 `.sdd-delivery/team-rules.json`。
- 语言偏好：根据用户输入、仓库文档和团队规则推断产物语言，也可显式设置中文 / 英文 / 双语。
- 中断恢复：实现或测试中被追问、打岔或改需求时，先 checkpoint，再恢复原链路或重置下游门禁。

## 无 Python 模式

Python 不是使用前提。没有 Python 时，AI 应直接手动创建和更新 Markdown / JSON 产物，并说明哪些自动化步骤被跳过。

## 可选脚本

有 Python 时，可以使用脚本加速：

```bash
python scripts/init_artifacts.py login-rate-limit
python scripts/parse_prd_to_spec.py prd.md .sdd-delivery/login-rate-limit --force
python scripts/trace_coverage.py .sdd-delivery/login-rate-limit
python scripts/scan_test_coverage.py . .sdd-delivery/login-rate-limit --update-report --update-trace
python scripts/sync_observability.py .sdd-delivery/login-rate-limit
python scripts/generate_dashboard.py .sdd-delivery/login-rate-limit
python scripts/validate_artifacts.py .sdd-delivery/login-rate-limit
python scripts/manage_capabilities.py .sdd-delivery/login-rate-limit --project-root . --detect --plan
python scripts/record_mcp_discovery.py .sdd-delivery/login-rate-limit --enable-capability --source "Codex MCP tools" --query-intent "查找企业内部可复用的账单查询 API、数据表格组件和权限校验 SDK"
python scripts/setup_team_rules.py --root . --init
python scripts/setup_team_rules.py --root . --sql-dialect postgresql --sql-schema billing --sql-migration-tool alembic
python scripts/setup_team_rules.py --root . --sql-rule query.forbid_select_star=false
python scripts/setup_team_rules.py --root . --sql-feature-exception "require_index_for_filter_columns::SPEC-3 export::一次性小表导出::tech lead::2026-09-01 前移除"
python scripts/setup_team_rules.py --root . --validate
```

## 企业 MCP 能力复用

启用“企业 MCP 能力复用”后，skill 会在实现前要求 agent 先通过 MCP 查询企业内部可复用能力，优先复用已有工具、资源、组件、服务、API、SDK、脚手架、知识库或运维能力：

- `mcp-discovery.json`：记录 MCP server、tool、resource、component、查询意图和不可用项
- `mcp-component-selection.md`：记录选择理由、接入 / 使用约束、fallback 决策和集成验证
- `12-observability.md`：展示 MCP 状态和证据文件

不同 agent 可以用自己的 MCP 调用方式发现能力，再通过脚本或手工方式写入这些产物。若 MCP 不可用或没有合适能力，需要先记录 fallback，并在手写替代实现前确认。

## 版本历史

| 版本 | 日期 | 重点变化 |
|---|---|---|
| v0.7.0 | 2026-06-08 | 增加 SQL 规范命令行维护入口：可设置 dialect、schema、表前缀、迁移工具、全局规则开关、遗留对象例外和需求级例外。 |
| v0.6.0 | 2026-06-08 | 团队规则新增 SQL 规范三层治理：全局规则、项目覆盖、需求级例外，并补充结构化校验、方案适配和交付审查清单。 |
| v0.5.0 | 2026-06-08 | 将 MCP 能力调整为企业内部能力复用：查询意图、resource 记录、接入约束、方案复用决策、任务级能力记录和 fallback 确认。 |
| v0.4.0 | 2026-06-08 | 小智欢迎语、阶段菜单白话说明、中文生成物一致性、dashboard 标签复用、MCP 对象名展示、无效 MCP JSON 校验和 golden workflow 测试。 |
| v0.3.0 | 2026-06-07 | 方案确认门禁、可插拔能力开关、团队规则、语言偏好、中断恢复、人机协同里程碑和质量看板。 |
| v0.2.x | 2026-06-05 | 完整 Spec-first 产物链：PRD、Spec、审查、方案、任务、实现日志、单测、交付审查、checkpoint 和 observability。 |
| v0.1.x | 2026-06-04 | 初始 skill 结构、模板、参考文档、脚本和插件包装。 |

改动用户可见行为、产物结构、脚本参数或协作流程时，需要同步更新本节。

## 设计参考

本技能参考了 GitHub Spec Kit 的 Spec-first 阶段化流程、OpenSpec 的 brownfield 变更思路、Agent Skill 的渐进加载模式、checkpoint 上下文恢复实践、需求追踪矩阵，以及 GitHub PR / CI 交付实践。详细说明见：`references/open-source-influences.md`。
## English

SDD Delivery is a Spec-first delivery skill for AI coding agents. Users do not need to remember script commands. They can send a PRD or choose a workflow stage, and the agent maintains the delivery artifacts.

It does not jump directly from PRD to code. It turns delivery into reviewable, traceable, recoverable steps with explicit solution approval, TDD evidence, per-task review, checkpoints, and observable artifacts.

## Installation

To install through the Codex plugin marketplace:

```text
/plugin marketplace add codepunk-gm/sdd-delivery-skill
/plugin install sdd-delivery
```

Or copy this skill directory into Codex skills:

```bash
cp -R sdd-delivery ~/.codex/skills/sdd-delivery
```

## Usage

```text
Use $sdd-delivery to turn this PRD into Spec, solution, reviewed implementation tasks, unit tests, and observable delivery artifacts.
```

Recommended menu:

```text
Stage menu
  1. PRD to Spec - Turn the idea into a requirement document that can be reviewed.
  2. Clarify Requirements - Find missing or ambiguous details before design starts.
  3. Spec Review - Check whether the requirement document is ready for development.
  4. Consistency Analysis - Compare requirements, constraints, and the existing project for conflicts.
  5. Technical Solution - Design the approach before changing code.
  6. Solution Review - Check risk, compatibility, security, rollback, and verification.
  7. Task Split - Break the solution into small, executable tasks.
  8. Implementation - Write tests, change code, and record progress task by task.
  9. Unit Test - Complete the test plan, test results, and coverage mapping.
  10. Delivery Review - Final check before handoff.
  11. Checkpoint / Handoff - Save progress so the workflow can resume later.

Send a PRD or reply with a number.
```

The default guided assistant is named **小智**. It confirms architecture and technology-stack decisions before implementation and records state before resuming after interruptions.

## Gate and Automation Boundaries

SDD Delivery gates are an agent workflow contract, not a runtime sandbox. The skill constrains work through artifacts, checkpoint state, review records, and explicit user confirmation:

- Solution approval: pause after `04-tech-solution.md`, ask for approval, and record the result in `11-checkpoint.json`.
- TDD gate: create tests first and record RED evidence before implementation; scripts can scan `SPEC-*` coverage but cannot replace real test judgment.
- Per-task review: check boundaries, tests, implementation log, and checkpoint after each task.
- No Python mode: scripts are accelerators and validation helpers; without Python, maintain the same Markdown / JSON artifacts manually.

The skill provides reviewable delivery constraints and a recoverable evidence trail. It is not a hard enforcement engine.

## Human-in-the-Loop Review

Each feature folder can be reviewed without chat history:

- `11-checkpoint.json`: machine-readable state source for recovery
- `12-observability.md`: human-readable progress and quality dashboard
- `13-dashboard.html`: optional static business dashboard
- `events.jsonl`: append-only process log

Default milestones: M1 Requirements Baseline, M2 Solution Approval, M3 Controlled Implementation, M4 Verification Complete, and M5 Delivery Ready. Human review decisions are recorded in checkpoint `human_reviews` and `milestones`, then rendered into `12-observability.md`.

## Core Capabilities

1. PRD to Spec — convert PRDs into reviewable Specs and trace matrices
2. Clarify Requirements — scan ambiguity categories and ask focused questions
3. Spec Review — check completeness, testability, and boundaries
4. Consistency Analysis — detect duplication, ambiguity, underspecification, and principle conflicts
5. Technical Solution — design from repo evidence with pre-mortem risks
6. Solution Review — review architecture, compatibility, security, performance, rollback, and verification
7. Task Split — create bounded, traceable implementation tasks
8. Implementation — follow TDD evidence and per-task review
9. Unit Test — maintain test plan, test report, and reverse SPEC-* coverage
10. Delivery Review — verify boundaries, trace coverage, and security audit results
11. Checkpoint / Handoff — save structured state for interruption recovery

## v0.7 SQL Standards Maintenance Commands

- `setup_team_rules.py` can update SQL dialect, schema, table prefix, migration tool, global rule toggles, legacy exceptions, and feature exceptions.
- Teams can keep common SQL standards in `global`, project-specific differences in `project_overrides`, and temporary approvals in `feature_exceptions`.
- Exceptions must include rule, scope, reason, approver, and expiration so temporary debt stays visible.

Example:

```bash
python scripts/setup_team_rules.py --root . --sql-dialect postgresql --sql-schema billing --sql-migration-tool alembic
python scripts/setup_team_rules.py --root . --sql-rule query.forbid_select_star=false
python scripts/setup_team_rules.py --root . --sql-allow-legacy "legacy_order::table_case::Existing upstream ERP table"
python scripts/setup_team_rules.py --root . --sql-feature-exception "require_index_for_filter_columns::SPEC-3 export::One-time small-table export::tech lead::Remove before 2026-09-01"
python scripts/setup_team_rules.py --root . --validate
```

## v0.6 SQL Standards Governance

- SQL standards live in `.sdd-delivery/team-rules.json` with global rules, project overrides, and feature-level exceptions.
- `setup_team_rules.py --validate` validates SQL rule shape, project overrides, and required exception approval fields.
- Technical solution and delivery review templates include SQL checks for parameterized queries, no `SELECT *`, pagination order, indexes, migrations, rollback, and transaction boundaries.

## v0.5 Enterprise MCP Capability Reuse

- Enterprise MCP capability reuse queries internal tools, resources, components, services, APIs, SDKs, scaffolds, knowledge bases, or operations capabilities before implementation and prefers reuse.
- Query intent: `record_mcp_discovery.py` supports `--query-intent` to record what capability need the MCP query was trying to solve.
- Integration constraints: `mcp-component-selection.md` records call style, parameters, permissions, endpoints, imports, SDK methods, and internal usage notes.
- Solution/task linkage: technical solution, task split, and unit test plan templates now require capability reuse, fallback, and verification expectations.

## v0.4 Experience and Language Consistency

- Welcome flow: 小智 explains default Chinese artifacts, solution approval, interrupt recovery, and the stage menu before work starts.
- Stage menu: each phase now has a plain-language explanation to help first-time users choose the right step.
- Chinese artifacts: PRD parsing, observability markdown, HTML dashboards, and observability templates now use consistent Chinese labels.
- Dashboard label reuse: `dashboard_labels.py` centralizes generated dashboard copy.
- MCP dashboard improvements: summaries show discovered MCP server, tool, and component names instead of counts only.
- Validation stability: invalid `mcp-discovery.json` is reported as a structured issue instead of stopping validation.
- Golden workflow tests cover Chinese generated artifacts, MCP dashboards, and invalid JSON validation.

## v0.3 Workflow Enhancements

- Solution approval gate before task splitting and implementation.
- Optional capabilities for frontend templates, Java modular projects, MCP component protocol, GitHub delivery assets, and team code principles.
- Capability switches with `enabled`, `disabled`, and `ask` states recorded in checkpoint.
- Language preference inference for Chinese, English, or bilingual artifacts.
- Interrupt recovery protocol for questions, scope changes, solution changes, and stop requests.

## Optional Scripts

Scripts are optional accelerators:

```bash
python scripts/init_artifacts.py login-rate-limit
python scripts/parse_prd_to_spec.py prd.md .sdd-delivery/login-rate-limit --force
python scripts/trace_coverage.py .sdd-delivery/login-rate-limit
python scripts/scan_test_coverage.py . .sdd-delivery/login-rate-limit --update-report --update-trace
python scripts/sync_observability.py .sdd-delivery/login-rate-limit
python scripts/generate_dashboard.py .sdd-delivery/login-rate-limit
python scripts/validate_artifacts.py .sdd-delivery/login-rate-limit
python scripts/manage_capabilities.py .sdd-delivery/login-rate-limit --project-root . --detect --plan
python scripts/record_mcp_discovery.py .sdd-delivery/login-rate-limit --enable-capability --source "Codex MCP tools" --query-intent "Find reusable enterprise billing APIs, table components, and permission SDKs"
python scripts/setup_team_rules.py --root . --init
python scripts/setup_team_rules.py --root . --sql-dialect postgresql --sql-schema billing --sql-migration-tool alembic
python scripts/setup_team_rules.py --root . --sql-rule query.forbid_select_star=false
python scripts/setup_team_rules.py --root . --sql-feature-exception "require_index_for_filter_columns::SPEC-3 export::One-time small-table export::tech lead::Remove before 2026-09-01"
python scripts/setup_team_rules.py --root . --validate
```

## Enterprise MCP Capability Reuse

When enterprise MCP capability reuse is enabled, the skill asks the agent to query reusable internal capabilities through MCP before implementation:

- `mcp-discovery.json`: MCP servers, tools, resources, components, query intent, and unavailable capabilities
- `mcp-component-selection.md`: selection rationale, usage / integration constraints, fallback decisions, and integration verification
- `12-observability.md`: MCP status and evidence-file links

Different agents can discover MCP capabilities through their own environment, then record the result through the script or manual artifacts. If MCP is unavailable or no suitable capability exists, the fallback must be recorded and confirmed before hand-building alternatives.

## Version History

| Version | Date | Highlights |
|---|---|---|
| v0.7.0 | 2026-06-08 | Added command-line maintenance for SQL standards: dialect, schema, table prefix, migration tool, global rule toggles, legacy exceptions, and feature exceptions. |
| v0.6.0 | 2026-06-08 | Added SQL standards governance in team rules: global rules, project overrides, feature exceptions, structured validation, solution adaptation, and delivery review checks. |
| v0.5.0 | 2026-06-08 | Reframed MCP support as enterprise internal capability reuse: query intent, resource records, integration constraints, solution reuse decisions, task-level capability records, and fallback confirmation. |
| v0.4.0 | 2026-06-08 | 小智 welcome flow, plain-language stage menu, Chinese artifact consistency, reusable dashboard labels, MCP object-name summaries, invalid MCP JSON validation, and golden workflow tests. |
| v0.3.0 | 2026-06-07 | Solution approval gate, pluggable capability switches, team rules, language preferences, interrupt recovery, human-review milestones, and quality dashboards. |
| v0.2.x | 2026-06-05 | Full Spec-first artifact chain: PRD, Spec, reviews, solution, tasks, implementation log, unit tests, delivery review, checkpoint, and observability. |
| v0.1.x | 2026-06-04 | Initial skill structure, templates, reference docs, scripts, and plugin packaging. |

Update this section when user-visible behavior, artifact shape, script arguments, or collaboration workflow changes.


## Design References

This skill references GitHub Spec Kit for Spec-first phased delivery, OpenSpec for brownfield-friendly changes, Agent Skill progressive disclosure, checkpoint-based recovery, requirement traceability, and GitHub PR / CI delivery practices. See `references/open-source-influences.md` for details.
