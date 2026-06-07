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

## 如何使用

在 Codex 中输入：

```text
使用 sdd-delivery，基于这个 PRD 生成 Spec、技术方案、审查清单、实现任务、单测计划和可观测交付产物。
```

启动后发送 PRD，或选择阶段：

```text
阶段菜单
  1. PRD 转 Spec
  2. 需求澄清
  3. Spec 审查
  4. 一致性分析
  5. 技术方案
  6. 方案审查
  7. 任务拆分
  8. 代码实现
  9. 单测
  10. 交付审查
  11. 检查点 / 交接

请发送 PRD，或回复编号继续。
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

## v0.3 工作流增强

- 方案确认门禁：`04-tech-solution.md` 完成后必须确认架构和技术栈，再进入任务拆分。
- 可插拔能力：按需启用前端模板、Java 模块化项目、MCP 组件协议、GitHub 交付资产和团队代码原则。
- 工程化开关：每个能力支持 `enabled` / `disabled` / `ask` 三态，记录在 checkpoint。
- 增强能力规划：自动检测项目特征，按需启用前端模板保护、组件协议支持、团队代码原则等能力。
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
python scripts/record_mcp_discovery.py .sdd-delivery/login-rate-limit --enable-capability --source "Codex MCP tools"
python scripts/setup_team_rules.py --root . --init
```

## MCP 支持

启用“组件协议支持”后，skill 会维护 MCP 证据链：

- `mcp-discovery.json`：记录 MCP server、tool、component 和不可用项
- `mcp-component-selection.md`：记录选择理由、fallback 决策和集成验证
- `12-observability.md`：展示 MCP 状态和证据文件

不同 agent 可以用自己的 MCP 调用方式发现能力，再通过脚本或手工方式写入这些产物。

## 版本历史

| 版本 | 日期 | 重点变化 |
|---|---|---|
| v0.3.0 | 2026-06 | 方案确认门禁、可插拔能力开关、团队规则、语言偏好、中断恢复、人机协同里程碑和质量看板。 |
| v0.2.x | 2026-06 | 完整 Spec-first 产物链：PRD、Spec、审查、方案、任务、实现日志、单测、交付审查、checkpoint 和 observability。 |
| v0.1.x | 2026-06 | 初始 skill 结构、模板、参考文档、脚本和插件包装。 |

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
  1. PRD to Spec
  2. Clarify Requirements
  3. Spec Review
  4. Consistency Analysis
  5. Technical Solution
  6. Solution Review
  7. Task Split
  8. Implementation
  9. Unit Test
  10. Delivery Review
  11. Checkpoint / Handoff

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
python scripts/record_mcp_discovery.py .sdd-delivery/login-rate-limit --enable-capability --source "Codex MCP tools"
python scripts/setup_team_rules.py --root . --init
```

## MCP Support

When component protocol support is enabled, the skill maintains MCP evidence:

- `mcp-discovery.json`: MCP servers, tools, components, and unavailable capabilities
- `mcp-component-selection.md`: selection rationale, fallback decisions, and integration verification
- `12-observability.md`: MCP status and evidence-file links

Different agents can discover MCP capabilities through their own environment, then record the result through the script or manual artifacts.

## Version History

| Version | Date | Highlights |
|---|---|---|
| v0.3.0 | 2026-06 | Solution approval gate, pluggable capability switches, team rules, language preferences, interrupt recovery, human-review milestones, and quality dashboards. |
| v0.2.x | 2026-06 | Full Spec-first artifact chain: PRD, Spec, reviews, solution, tasks, implementation log, unit tests, delivery review, checkpoint, and observability. |
| v0.1.x | 2026-06 | Initial skill structure, templates, reference docs, scripts, and plugin packaging. |

Update this section when user-visible behavior, artifact shape, script arguments, or collaboration workflow changes.


## Design References

This skill references GitHub Spec Kit for Spec-first phased delivery, OpenSpec for brownfield-friendly changes, Agent Skill progressive disclosure, checkpoint-based recovery, requirement traceability, and GitHub PR / CI delivery practices. See `references/open-source-influences.md` for details.
