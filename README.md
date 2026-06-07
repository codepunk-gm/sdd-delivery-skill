# SDD Delivery

<p align="center">
  <strong>PRD → Spec → Review → Solution → Implement → Test → Deliver</strong>
  <br>
  Spec-driven, gate-governed, observable engineering delivery for AI coding agents.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/version-0.3.0-blue" alt="Version">
  <img src="https://img.shields.io/badge/license-MIT-green" alt="License">
  <img src="https://img.shields.io/badge/agents-Codex%20%7C%20Claude%20Code%20%7C%20Cursor%20%7C%20Copilot%20%7C%20Windsurf-orange" alt="Agents">
  <img src="https://img.shields.io/badge/python-optional-lightgrey" alt="Python">
</p>

[中文](#中文) | [English](#english)

---

## 中文

### 概述

SDD Delivery 是一个面向 AI 编程助手的 Spec-first 研发交付技能包。它不直接"看 PRD 写代码"，而是把交付拆成可审查、可追踪、可恢复的步骤。

**核心理念（8 条宪法原则）：**
1. Spec Before Code — 实现之前必须有审查过的 Spec
2. Artifacts Over Chat — 结构化文件优先于聊天记忆
3. Gates Before Progress — 风险必须可见并被接受才能前进
4. Traceability Forever — PRD→Spec→方案→任务→代码→单测全链路追踪
5. Minimal, Reviewable Diffs — 仅修改必要文件，边界违规即 P0 拒绝
6. UTF-8 Always — 永不产生乱码
7. No-Python Universality — 脚本是加速器，不是依赖
8. Evidence Over Assertion — 每个 repo 事实必须有来源

**v0.3 新增：**
- 方案确认门禁：技术方案和技术栈必须由用户确认后才能进入任务拆分 / 实现
- 可插拔能力注册：前端模板、Java 模块化项目、MCP 组件协议、GitHub 交付资产、团队代码原则可按节点启用
- 工程化开关：每个能力支持 `enabled` / `disabled` / `ask` 三态，记录在 checkpoint，避免重复询问
- 增强能力规划：自动检测项目特征，按需启用前端模板保护、组件协议支持、团队代码原则等能力
- 语言与团队规则启动设置：可自动推断或配置中文 / 英文 / 双语产物语言，并记录在 checkpoint
- 团队规则配置：`setup_team_rules.py` 初始化并校验 `.sdd-delivery/team-rules.json`
- 中断恢复协议：实现或测试中被追问 / 打岔后，先保存状态，再回到原链路或重置下游门禁

### 门禁与自动化边界

SDD Delivery 的门禁是 AI agent 的工作协议，不是一个会拦截所有文件写入的运行时沙箱。它通过产物、checkpoint、审查记录和用户确认来约束流程：

- **方案确认**：agent 必须在 `04-tech-solution.md` 后停下，向用户确认架构、技术栈和实现方向，并把结果写入 `11-checkpoint.json`。
- **TDD 门禁**：agent 必须先写测试、记录 RED 证据，再进入实现；脚本可以辅助扫描 `SPEC-*` 覆盖和测试报告，但不能替代真实测试判断。
- **逐任务审查**：agent 在每个任务后检查边界、测试、实现日志和 checkpoint；`validate_artifacts.py` 能检查文件和字段完整性，但不会证明业务逻辑一定正确。
- **无 Python 模式**：脚本是加速器和校验助手，不是使用前提。没有 Python 时，agent 应手动维护 Markdown / JSON 产物，并说明跳过了哪些自动化。

换句话说，这个 skill 提供的是“可审查的交付约束”和“可恢复的证据链”，不是强制执行引擎。

### 人机协同审查

每个 feature 目录都能脱离聊天记录被人工审查。`11-checkpoint.json` 是机器可恢复的状态事实源，`12-observability.md` 是人工可读的进度与质量面板，`events.jsonl` 是过程流水。

需要更友好的业务审查界面时，可以生成 `13-dashboard.html` 静态看板。它只读取现有 Markdown / JSON 产物，不替代事实源。

默认里程碑：

| 里程碑 | 人工审查重点 | 证据文件 |
|---|---|---|
| M1 需求基线 | PRD、澄清、Spec、审查、一致性是否可进入方案 | `00-prd.md`, `01-spec.md`, `02-spec-review.md`, `03-requirement-trace.md` |
| M2 方案确认 | 架构、技术栈、风险、回滚、安全审查是否可进入实现 | `04-tech-solution.md`, `05-solution-review.md`, `11-checkpoint.json` |
| M3 实现受控 | 任务边界、TDD 证据、逐任务审查、变更范围是否受控 | `06-implementation-tasks.md`, `07-implementation-log.md` |
| M4 验证完成 | 单测计划、单测报告、覆盖缺口是否清楚 | `08-unit-test-plan.md`, `09-unit-test-report.md` |
| M5 交付就绪 | 最终审查、风险状态、下一步和交接信息是否完整 | `10-delivery-review.md`, `11-checkpoint.json`, `12-observability.md` |

人工审查结论会记录到 checkpoint 的 `human_reviews` 和 `milestones`，并同步展示在 `12-observability.md`。

### 快速开始

**Claude Code:**
```text
/plugin marketplace add codepunk-gm/sdd-delivery-skill
/plugin install sdd-delivery@sdd-delivery-skill
/reload-plugins
```

**Codex:**
```text
/plugin marketplace add codepunk-gm/sdd-delivery-skill
/plugin install sdd-delivery
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
```

默认助理名为「小智」。小智会使用中文产物，关键方案先确认；如果中途打断或改方向，会记录状态并把流程带回正轨。

### 使用指南

#### 启动工作流

安装后，在 AI 编程助手中发送 PRD 即可启动。AI 会展示阶段菜单，你可以选择从哪个阶段开始：

```text
将这个 PRD 转为 Spec 和技术方案。
```

```text
使用 sdd-delivery，审查已有的 Spec。
```

```text
基于 .sdd-delivery/login-rate-limit 的 checkpoint 恢复上次进度。
```

#### 完整流程（14 阶段）

```
PRD 录入 → 需求澄清 → Spec 编写 → Spec 审查 → 一致性分析
    ↓
需求追踪矩阵 → 技术方案（含事前验尸） → 方案审查（含安全审计）
    ↓
任务拆分 → 代码实现（TDD + 逐任务审查） → 单测计划 → 单测报告
    ↓
交付审查（含安全审计） → 检查点 + 可观测面板
```

#### 轻量模式 vs 完整模式

| 场景 | 模式 | 说明 |
|------|------|------|
| 错别字、配置值、文档字符串 | 轻量模式 | 跳过 1-4 号门，仅维护实现日志 |
| 功能开发、Bug 修复、重构 | 完整模式 | 全部 13 个门禁 + 14 个产物 |

轻量模式需用户明确请求（"使用轻量模式"）。完整模式为默认。

#### 无 Python 模式

Python 不是使用前提。所有自动化脚本都可以用 Markdown / JSON 手动编辑替代。没有 Python 时，AI 会说明哪些脚本被跳过，并直接创建产物文件。

#### 产物目录

产物保存在项目的 `.sdd-delivery/<feature>/` 下：

```text
.sdd-delivery/login-rate-limit/
├── 00-prd.md                # PRD 文档（含需求澄清结果）
├── 01-spec.md               # Spec 规格
├── 02-spec-review.md        # Spec 审查
├── 03-requirement-trace.md  # 需求追踪矩阵（含一致性分析）
├── 04-tech-solution.md      # 技术方案（含事前验尸）
├── 05-solution-review.md    # 方案审查（含安全审计）
├── 06-implementation-tasks.md # 实现任务拆分
├── 07-implementation-log.md # 实现日志
├── 08-unit-test-plan.md     # 单测计划
├── 09-unit-test-report.md   # 单测报告
├── 10-delivery-review.md    # 交付审查（含安全审计）
├── 11-checkpoint.json       # 检查点（可恢复状态）
├── 12-observability.md      # 可观测面板
├── 13-dashboard.html        # 可选静态业务看板
└── events.jsonl             # 事件日志
```

#### 可选脚本加速

有 Python 环境时，可以用脚本加速常见操作：

```bash
# 初始化产物目录
python scripts/init_artifacts.py login-rate-limit

# PRD 自动解析为 Spec
python scripts/parse_prd_to_spec.py prd.md .sdd-delivery/login-rate-limit --force

# 计算需求追踪覆盖率
python scripts/trace_coverage.py .sdd-delivery/login-rate-limit

# 反查测试覆盖
python scripts/scan_test_coverage.py . .sdd-delivery/login-rate-limit --update-report --update-trace

# 同步可观测面板
python scripts/sync_observability.py .sdd-delivery/login-rate-limit

# 生成静态 HTML 业务看板
python scripts/generate_dashboard.py .sdd-delivery/login-rate-limit

# 检测并规划可插拔能力
python scripts/manage_capabilities.py .sdd-delivery/login-rate-limit --project-root . --detect --plan

# 记录 MCP 发现与组件选择证据
python scripts/record_mcp_discovery.py .sdd-delivery/login-rate-limit --enable-capability --source "Codex MCP tools"

# 初始化 / 校验团队规则
python scripts/setup_team_rules.py --root . --init
python scripts/setup_team_rules.py --root . --validate

# 验证产物完整性
python scripts/validate_artifacts.py .sdd-delivery/login-rate-limit

# 生成 GitHub PR 模板和 CI
python scripts/generate_github_assets.py .
```

### 架构

```
SKILL.md (触发 + 流程编排)
  ├── references/ (25 个参考文件，按需加载)
  │   ├── constitution.md    宪法原则
  │   ├── clarify-taxonomy.md  歧义扫描
  │   ├── boundary-rules.md   边界标注
  │   ├── pre-mortem.md       事前验尸
  │   ├── analyze-rubric.md   一致性检查
  │   ├── security-audit.md   安全检查
  │   └── ... (18 more)
  ├── assets/templates/ (14 个产物模板)
  └── scripts/ (9 个可选 Python 加速器)
```

### MCP 支持边界

MCP 支持已经包含能力开关、发现证据、选择记录和看板摘要。启用“组件协议支持”后，流程会维护：

- `mcp-discovery.json`：记录 MCP server、tool、component、不可用项和来源
- `mcp-component-selection.md`：记录选择理由、fallback 决策和集成验证
- `11-checkpoint.json`：记录 `mcp_component_protocol` 开关和发现数量
- `12-observability.md`：展示 MCP 能力状态、发现状态和证据文件

它不绑定某个具体 agent 的 MCP API；不同环境可以由 agent 调用 MCP 后，用脚本或手工方式把结果写入证据链。

### 版本历史

| 版本 | 日期 | 重点变化 |
|---|---|---|
| v0.3.0 | 2026-06 | 引入方案确认门禁、可插拔能力开关、团队规则、语言偏好、中断恢复、人机协同里程碑和质量看板；明确门禁是 agent 工作协议，脚本是加速器和校验助手。 |
| v0.2.x | 2026-06 | 完善 Spec-first 全流程：PRD、澄清、Spec、审查、技术方案、任务拆分、实现日志、单测计划、单测报告、交付审查、checkpoint 和 observability。 |
| v0.1.x | 2026-06 | 建立基础 skill 结构、模板目录、参考文档、自动化脚本和插件市场包装。 |

维护规则：

- 用户可见行为、产物结构、脚本参数、安装方式或协作流程变化时，必须更新本节。
- 只改错别字、格式或内部注释时，可不新增版本记录。
- 版本号以 `plugins/sdd-delivery/.codex-plugin/plugin.json` 为准；README 记录面向用户的变化摘要。

### 设计参考

借鉴社区优秀工程实践，融合为可安装技能包：

| 来源 | 借鉴模式 |
|------|---------|
| [Spec-Kit](https://github.com/github/spec-kit) (43.7k⭐) | Constitution、Clarify、Analyze 阶段 |
| [cc-sdd](https://github.com/gotalab/cc-sdd) | Discovery 路由、边界标注、每任务审查 |
| [Don Cheli SDD](https://github.com/doncheli/don-cheli-sdd) | TDD 阻断、事前验尸、OWASP 安全审计 |
| [PreviewForge](https://github.com/two-weeks-team/previewforgeforclaudecode) | 多智能体审查、分控交付 |
| [Superpowers](https://github.com/obra/superpowers) | 可组合技能、计划确认、TDD、执行批次、审查节点 |
| OpenSpec | 存量项目变更规格 |
| Agent Skill 模式 | SKILL.md + references 渐进加载 |
| 上下文工程实践 | Checkpoint / Observability / events.jsonl |

### 贡献

```
修改 skill:
1. 编辑 plugins/sdd-delivery/skills/sdd-delivery/ 下的文件
2. 同步到 skills/sdd-delivery/（根目录副本）
3. 更新版本号（4 个 plugin.json）
4. 改动行为时更新 README
5. 确保无 Python 模式可用

版本规则:
- MAJOR: 产物重新编号、schema 字段删除
- MINOR: 新 reference、新模板、新脚本、新 gate
- PATCH: 拼写修复、模板措辞调整
```

详见 `plugins/sdd-delivery/skills/sdd-delivery/references/plugin-operations.md`。

---

## English

### Overview

SDD Delivery is a Spec-first engineering delivery skill for AI coding agents. It does not jump straight from PRD to code. It turns delivery into reviewable, traceable, recoverable steps backed by artifacts, checkpoints, and explicit approval gates.

**Core principles:**
1. Spec Before Code — implementation starts from a reviewed Spec
2. Artifacts Over Chat — durable files beat chat memory
3. Gates Before Progress — unresolved risk must be visible and accepted
4. Traceability Forever — PRD → Spec → Solution → Task → Code → Test stays connected
5. Minimal, Reviewable Diffs — changes stay scoped and reviewable
6. UTF-8 Always — avoid mojibake and preserve multilingual content
7. No-Python Universality — scripts accelerate the workflow, but are not required
8. Evidence Over Assertion — repo facts and gate decisions need evidence

**v0.3 highlights:**
- Solution approval gate: the agent must ask for architecture, technology stack, and implementation-direction approval after `04-tech-solution.md`.
- Pluggable capabilities: frontend template protection, Java module boundaries, MCP component protocol, GitHub delivery assets, and team code principles can be enabled when relevant.
- Capability switches: each optional capability can be `enabled`, `disabled`, or `ask`, and the decision is stored in checkpoint.
- Language and team-rule setup: the workflow can infer or configure Chinese, English, or bilingual artifacts and persist the choice.
- Interrupt recovery: when the user asks a question or changes scope mid-flow, the agent checkpoints first, then resumes or resets downstream gates.

### Gate and Automation Boundaries

SDD Delivery gates are an agent workflow contract, not a runtime sandbox that can physically prevent every file write. The skill constrains delivery through artifacts, checkpoint state, review records, and explicit user confirmation:

- **Solution approval** means the agent must pause after `04-tech-solution.md`, ask for approval of the architecture, stack, and implementation direction, then record the outcome in `11-checkpoint.json`.
- **TDD gate** means the agent must create tests first and record RED evidence before implementation. Scripts can scan `SPEC-*` references and update reports, but they cannot replace real test judgment.
- **Per-task review** means the agent checks boundaries, tests, logs, and checkpoint state after each task. `validate_artifacts.py` can verify file and field completeness; it does not prove business correctness.
- **No Python mode** means scripts are optional accelerators. Without Python, the agent should maintain the same Markdown / JSON artifacts manually and state which automation was skipped.

In short, the skill provides reviewable delivery constraints and a recoverable evidence trail. It is not a hard enforcement engine.

### Human-in-the-Loop Review

Each feature folder can be reviewed without relying on chat history. `11-checkpoint.json` is the machine-readable state source, `12-observability.md` is the human-readable progress and quality dashboard, and `events.jsonl` is the append-only process log.

Default milestones:

| Milestone | Human Review Focus | Evidence Files |
|---|---|---|
| M1 Requirements Baseline | PRD, clarification, Spec, review, and consistency are ready for solution design | `00-prd.md`, `01-spec.md`, `02-spec-review.md`, `03-requirement-trace.md` |
| M2 Solution Approval | Architecture, stack, risks, rollback, and security review are ready for implementation | `04-tech-solution.md`, `05-solution-review.md`, `11-checkpoint.json` |
| M3 Controlled Implementation | Task boundaries, TDD evidence, per-task review, and changed files are controlled | `06-implementation-tasks.md`, `07-implementation-log.md` |
| M4 Verification Complete | Unit test plan, test report, and coverage gaps are clear | `08-unit-test-plan.md`, `09-unit-test-report.md` |
| M5 Delivery Ready | Final review, risk posture, next action, and handoff state are complete | `10-delivery-review.md`, `11-checkpoint.json`, `12-observability.md` |

Human review decisions are recorded in checkpoint `human_reviews` and `milestones`, then rendered into `12-observability.md`.

For a more business-friendly review surface, generate `13-dashboard.html`. It reads existing Markdown / JSON artifacts and does not replace them as the source of truth.

### Quick Start

**Claude Code:**
```text
/plugin marketplace add codepunk-gm/sdd-delivery-skill
/plugin install sdd-delivery@sdd-delivery-skill
/reload-plugins
```

**Codex:**
```text
/plugin marketplace add codepunk-gm/sdd-delivery-skill
/plugin install sdd-delivery
```

**Other AI tools (Cursor, Copilot, Windsurf, Continue):**
Ask the tool to read `skills/sdd-delivery/SKILL.md`, then follow the workflow. All artifacts are plain Markdown/JSON — no tool-specific lock-in.

After installation, send a PRD or choose a stage:

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

The default guided assistant is named **小智**. It uses Chinese artifacts when the user is Chinese, confirms key solution decisions before implementation, and records state before resuming after interruptions.

### Usage Guide

#### Starting a Workflow

Send a PRD to your AI coding agent after installing the skill. The agent will present the stage menu. Examples:

```text
Turn this PRD into a Spec and technical solution.
```

```text
Use sdd-delivery to review the existing Spec.
```

```text
Resume from .sdd-delivery/login-rate-limit checkpoint.
```

#### Full Workflow (14 Phases)

```
PRD Intake → Clarify → Spec Authoring → Spec Review → Analyze
    ↓
Requirement Trace → Technical Solution (+Pre-Mortem) → Solution Review (+Security Audit)
    ↓
Implementation Tasks → Implementation (TDD + Per-Task Review) → Unit Test Plan → Test Report
    ↓
Delivery Review (+Security Audit) → Checkpoint + Observability
```

#### Quick Mode vs Full Mode

| Scenario | Mode | Notes |
|----------|------|-------|
| Typos, config values, docstrings | Quick Mode | Bypasses gates 1-4, implementation log only |
| Features, bug fixes, refactors | Full Mode | All 13 gates + 14 artifacts |

Quick Mode must be explicitly requested. Full Mode is the default.

#### No Python Mode

Python is not required. All scripts have manual Markdown/JSON fallbacks. The agent should note which automation steps were skipped and maintain equivalent artifacts by hand.

#### Artifact Directory

Artifacts are stored under `.sdd-delivery/<feature>/` in the target project:

```text
.sdd-delivery/login-rate-limit/
├── 00-prd.md
├── 01-spec.md
├── 02-spec-review.md
├── 03-requirement-trace.md
├── 04-tech-solution.md
├── 05-solution-review.md
├── 06-implementation-tasks.md
├── 07-implementation-log.md
├── 08-unit-test-plan.md
├── 09-unit-test-report.md
├── 10-delivery-review.md
├── 11-checkpoint.json
├── 12-observability.md
├── 13-dashboard.html
└── events.jsonl
```

#### Optional Scripts

```bash
# Initialize artifacts
python scripts/init_artifacts.py login-rate-limit

# Parse PRD into draft Spec artifacts
python scripts/parse_prd_to_spec.py prd.md .sdd-delivery/login-rate-limit --force

# Calculate trace coverage
python scripts/trace_coverage.py .sdd-delivery/login-rate-limit

# Scan reverse test-to-Spec coverage
python scripts/scan_test_coverage.py . .sdd-delivery/login-rate-limit --update-report --update-trace

# Refresh observability
python scripts/sync_observability.py .sdd-delivery/login-rate-limit

# Generate static HTML business dashboard
python scripts/generate_dashboard.py .sdd-delivery/login-rate-limit

# Validate artifact completeness
python scripts/validate_artifacts.py .sdd-delivery/login-rate-limit

# Detect and plan optional capabilities
python scripts/manage_capabilities.py .sdd-delivery/login-rate-limit --project-root . --detect --plan

# Record MCP discovery and component-selection evidence
python scripts/record_mcp_discovery.py .sdd-delivery/login-rate-limit --enable-capability --source "Codex MCP tools"

# Initialize / validate team rules
python scripts/setup_team_rules.py --root . --init
python scripts/setup_team_rules.py --root . --validate

# Generate GitHub PR and CI assets
python scripts/generate_github_assets.py .
```

### Architecture

A progressive-disclosure design: `SKILL.md` is the trigger and table of contents (~280 lines). Detailed instructions live in 25 reference files loaded on-demand. Templates provide repeatable artifact scaffolding. Python scripts are optional accelerators.

### MCP Support Boundary

MCP support now includes capability switches, discovery evidence, component-selection records, and observability summaries. When component protocol support is enabled, the workflow maintains:

- `mcp-discovery.json`: MCP servers, tools, components, unavailable capabilities, and sources
- `mcp-component-selection.md`: selection rationale, fallback decisions, and integration verification
- `11-checkpoint.json`: `mcp_component_protocol` state and discovered item counts
- `12-observability.md`: MCP status, discovery status, and evidence-file links

It does not bind to one specific agent MCP API. Each agent can call MCP in its own environment, then record the result through the script or manual evidence files.

### Version History

| Version | Date | Highlights |
|---|---|---|
| v0.3.0 | 2026-06 | Added solution approval, pluggable capability switches, team rules, language preferences, interrupt recovery, human-review milestones, and quality dashboards; clarified that gates are agent workflow contracts and scripts are accelerators / validators. |
| v0.2.x | 2026-06 | Expanded the Spec-first delivery chain: PRD, clarification, Spec, reviews, technical solution, task split, implementation log, unit test plan, test report, delivery review, checkpoint, and observability. |
| v0.1.x | 2026-06 | Established the initial skill structure, templates, reference docs, automation scripts, and plugin marketplace packaging. |

Maintenance rules:

- Update this section when user-visible behavior, artifact shape, script arguments, installation flow, or collaboration workflow changes.
- Typo-only, formatting-only, or internal-comment changes do not need a new version entry.
- The source of truth for the package version is `plugins/sdd-delivery/.codex-plugin/plugin.json`; README history summarizes user-facing changes.

### Key Features

- **Constitution-governed** — 8 non-negotiable principles with conflict resolution
- **14-phase workflow** — PRD Intake → Clarify → Spec Authoring → Spec Review → Analyze → Trace → Technical Solution → Solution Review → Implementation Tasks → Implementation → Unit Test Plan → Test Report → Delivery Review → Checkpoint + Observability
- **13 mandatory gates** — Clarify, Spec, Spec Review, Analyze, Solution, Solution Approval, Solution Review, TDD, Per-Task Review, Unit Test Plan, Test Report, Delivery Review, Checkpoint
- **Clarify taxonomy** — 10-category ambiguity scan, max 5 questions per session
- **Boundary annotations** — `_Boundary:_` and `_Depends:_` with P0 enforcement
- **Pre-mortem reasoning** — "Assume this failed. Why?" before design and implementation
- **Cross-artifact analysis** — Four-pass consistency check (duplications, ambiguities, underspecified, constitution conflicts)
- **TDD workflow contract** — RED → GREEN → REFACTOR evidence is recorded per task
- **Per-task review** — Boundary, test, log, and scope checks after each task
- **Security audit** — OWASP-style checklist during solution and delivery review
- **Traceability matrix** — PRD→Spec→Solution→Task→Code→Test with coverage thresholds
- **Parallel task markers** — `[P]` prefix for independent tasks
- **Task size estimation** — XS-XL with mandatory XL split
- **Checkpoint recovery** — Structured state survives context loss, compaction, and handoff
- **No-Python fallback** — Scripts are accelerators; the workflow works with manual Markdown/JSON editing

### Design References

SDD Delivery synthesizes patterns from leading open-source SDD projects:

| Source | Pattern Adapted |
|--------|----------------|
| [Spec-Kit](https://github.com/github/spec-kit) (43.7k⭐) | Constitution, Clarify taxonomy, Analyze phase, task format |
| [cc-sdd](https://github.com/gotalab/cc-sdd) | Discovery routing, boundary annotations, per-task subagent review |
| [Don Cheli SDD](https://github.com/doncheli/don-cheli-sdd) | TDD discipline, pre-mortem reasoning, OWASP security audit |
| [PreviewForge](https://github.com/two-weeks-team/previewforgeforclaudecode) | Score-gated delivery, multi-agent review |
| OpenSpec | Brownfield change specs, evolution records |
| Context engineering | Checkpoint, observability, event sourcing for long-running agents |

### Contributing

1. Edit files under `plugins/sdd-delivery/skills/sdd-delivery/`
2. Sync changes to `skills/sdd-delivery/` (root-level mirror copy)
3. Bump version in all 4 `plugin.json` files
4. Update README for user-visible changes
5. Ensure No-Python mode still works

### License

MIT — see [LICENSE](LICENSE).
