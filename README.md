# SDD Delivery

<p align="center">
  <strong>PRD → Spec → Review → Solution → Implement → Test → Deliver</strong>
  <br>
  Spec-driven, gate-governed, observable engineering delivery for AI coding agents.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/version-0.2.0-blue" alt="Version">
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
1. PRD 转 Spec    2. 需求澄清      3. Spec 审查     4. 一致性分析
5. 技术方案        6. 方案审查      7. 任务拆分      8. 代码实现
9. 单测            10. 交付审查     11. 检查点 / 交接
```

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
| 功能开发、Bug 修复、重构 | 完整模式 | 全部 11 个门 + 14 个产物 |

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

### 设计参考

借鉴社区优秀工程实践，融合为可安装技能包：

| 来源 | 借鉴模式 |
|------|---------|
| [Spec-Kit](https://github.com/github/spec-kit) (43.7k⭐) | Constitution、Clarify、Analyze 阶段 |
| [cc-sdd](https://github.com/gotalab/cc-sdd) | Discovery 路由、边界标注、每任务审查 |
| [Don Cheli SDD](https://github.com/doncheli/don-cheli-sdd) | TDD 阻断、事前验尸、OWASP 安全审计 |
| [PreviewForge](https://github.com/two-weeks-team/previewforgeforclaudecode) | 多智能体审查、分控交付 |
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

SDD Delivery is a Spec-first engineering delivery skill for AI coding agents. It breaks delivery into reviewable, traceable, recoverable steps governed by 8 constitutional principles.

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
SDD Delivery stages:
1. PRD to Spec   2. Clarify       3. Spec Review   4. Analyze
5. Solution      6. Solution Rev  7. Task Split    8. Implement
9. Unit Test     10. Delivery Rev 11. Checkpoint

Send a PRD or reply with a number.
```

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
| Features, bug fixes, refactors | Full Mode | All 11 gates + 14 artifacts |

Quick Mode must be explicitly requested. Full Mode is the default.

#### No Python Mode

Python is not required. All scripts have manual Markdown/JSON fallbacks. The agent will note which automation steps were skipped.

#### Optional Scripts

```bash
python scripts/init_artifacts.py login-rate-limit
python scripts/parse_prd_to_spec.py prd.md .sdd-delivery/login-rate-limit --force
python scripts/trace_coverage.py .sdd-delivery/login-rate-limit
python scripts/scan_test_coverage.py . .sdd-delivery/login-rate-limit --update-report --update-trace
python scripts/sync_observability.py .sdd-delivery/login-rate-limit
python scripts/validate_artifacts.py .sdd-delivery/login-rate-limit
python scripts/generate_github_assets.py .
```

### Architecture

A progressive-disclosure design: `SKILL.md` is the trigger and table of contents (~280 lines). Detailed instructions live in 25 reference files loaded on-demand. Templates provide repeatable artifact scaffolding. Python scripts are optional accelerators.

### Key Features

- **Constitution-governed** — 8 non-negotiable principles with conflict resolution
- **14-phase workflow** — PRD Intake → Clarify → Spec Authoring → Spec Review → Analyze → Trace → Technical Solution → Solution Review → Implementation Tasks → Implementation → Unit Test Plan → Test Report → Delivery Review → Checkpoint + Observability
- **11 mandatory gates** — Clarify, Spec, Spec Review, Analyze, Solution, Solution Review, TDD, Per-Task Review, Unit Test Plan, Test Report, Checkpoint
- **Clarify taxonomy** — 10-category ambiguity scan, max 5 questions per session
- **Boundary annotations** — `_Boundary:_` and `_Depends:_` with P0 enforcement
- **Pre-mortem reasoning** — "Assume this failed. Why?" before design and implementation
- **Cross-artifact analysis** — Four-pass consistency check (duplications, ambiguities, underspecified, constitution conflicts)
- **TDD structural blocking** — RED → GREEN → REFACTOR enforced per task
- **Per-task review** — Independent boundary/test/scope verification after each task
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
| [Don Cheli SDD](https://github.com/doncheli/don-cheli-sdd) | TDD as iron law, pre-mortem reasoning, OWASP security audit |
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
