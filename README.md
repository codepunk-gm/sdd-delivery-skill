# SDD Delivery Plugin

[中文](#中文说明) | [English](#english)

## 中文说明

SDD Delivery 是一个面向 AI 编程助手的研发交付插件。它把 PRD 先整理成可审查的 Spec，再推进到技术方案、方案审查、实现任务、代码实现、单测计划、单测报告、交付审查，以及可恢复的检查点和可观测面板。

它适合希望把 AI 编程过程标准化的团队：不是让模型直接“看 PRD 写代码”，而是让每一步都有产物、有审查、有追踪、有恢复点。

## 视觉概览

### 项目定位

![SDD Delivery Hero](assets/images/sdd-delivery-hero.png)

### 完整流程

![SDD Delivery Workflow](assets/images/workflow-diagram.png)

```text
PRD → Spec → Spec 审查 → 需求追踪矩阵 → 技术方案 → 方案审查 → 实现任务 → 代码实现 → 单测 → 交付审查 → Checkpoint 与可观测面板
```

### 交互示例

![Friendly Guided Interaction](assets/images/interaction-demo.png)

## 核心能力

- **Spec 前置**：PRD 先转成 Spec，再进入评审和技术方案。
- **需求追踪**：通过 `03-requirement-trace.md` 串联 PRD、Spec、方案、任务、代码和单测。
- **审查关卡**：内置 Spec 审查、方案审查和交付审查。
- **单测闭环**：支持单测计划、单测报告，以及 `SPEC-*` 反查测试覆盖。
- **可观测交付**：维护检查点、事件日志和可观测面板。
- **可恢复上下文**：适合长任务、上下文压缩、切换智能体或中断后继续。
- **无 Python 兜底**：脚本是加速器；没有 Python 时，agent 仍可用 Markdown / JSON 手动维护产物。
- **Plugin 分发**：可作为 Codex 插件安装和使用。

## 推荐工作流

```text
1. PRD 输入
2. 生成 Spec
3. 审查 Spec
4. 维护需求追踪矩阵
5. 生成技术方案
6. 审查技术方案
7. 拆分实现任务
8. 编码实现
9. 编写和执行单测
10. 交付审查
11. 更新 checkpoint 和可观测面板
```

## 目录结构

```text
sdd-delivery/
├── .codex-plugin/
│   └── plugin.json
├── README.md
├── assets/
│   └── images/
└── skills/
    └── sdd-delivery/
        ├── SKILL.md
        ├── README.md
        ├── agents/
        ├── references/
        ├── scripts/
        └── assets/
```

## 安装方式

### 作为 Codex 插件安装

推荐将本仓库作为 Codex plugin 安装。安装后，在 Codex 中直接调用：

```text
使用 sdd-delivery，基于这个 PRD 生成 Spec、技术方案、审查清单、实现任务、单测计划和可观测交付产物。
```

也可以使用英文调用：

```text
Use $sdd-delivery to turn this PRD into Spec, solution, reviewed implementation tasks, unit tests, and observable delivery artifacts.
```

### 作为纯技能使用

如果不使用 plugin，也可以复制内置 skill 目录：

```bash
cp -R skills/sdd-delivery ~/.codex/skills/sdd-delivery
```

## 交互方式

加载技能后，如果用户没有指定阶段，建议先展示中文能力菜单：

```text
请选择要执行的 SDD Delivery 阶段：
1. PRD 转 Spec
2. Spec 审查
3. 技术方案
4. 方案审查
5. 实现任务拆分
6. 代码实现
7. 单测计划 / 单测报告
8. 需求追踪 / 覆盖率检查
9. GitHub PR / CI 资产
10. 检查点 / 交接

请发送 PRD，或回复编号继续。
```

对于小改动，可以走轻量模式：

```text
这个需求看起来比较小，可以选择：
1. 轻量模式：最小改动 + 简短验证
2. 完整流程：Spec、审查、需求追踪、单测、检查点
```

## 快速开始

脚本不是必须的；如果本地有 Python，可以用下面的命令加速生成产物：

```bash
python skills/sdd-delivery/scripts/init_artifacts.py login-rate-limit
python skills/sdd-delivery/scripts/parse_prd_to_spec.py prd.md .sdd-delivery/login-rate-limit --force
python skills/sdd-delivery/scripts/trace_coverage.py .sdd-delivery/login-rate-limit
python skills/sdd-delivery/scripts/scan_test_coverage.py . .sdd-delivery/login-rate-limit --update-report --update-trace
python skills/sdd-delivery/scripts/sync_observability.py .sdd-delivery/login-rate-limit
python skills/sdd-delivery/scripts/validate_artifacts.py .sdd-delivery/login-rate-limit
```

生成的交付产物位于：

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
└── events.jsonl
```

## 单测如何关联 Spec

在测试文件中标注对应的 Spec ID：

```python
def test_login_rate_limit_blocks_after_threshold():
    """Covers SPEC-1 and SPEC-2."""
    assert True
```

然后运行：

```bash
python skills/sdd-delivery/scripts/scan_test_coverage.py . .sdd-delivery/login-rate-limit --update-report --update-trace
```

脚本会更新：

```text
03-requirement-trace.md
09-unit-test-report.md
11-checkpoint.json
```

## GitHub 集成

生成 PR 模板和 GitHub Actions 校验文件：

```bash
python skills/sdd-delivery/scripts/generate_github_assets.py .
```

会生成：

```text
.github/pull_request_template.md
.github/workflows/sdd-delivery-artifacts.yml
.github/scripts/validate_devflow_artifacts.py
```

## 常用 AI 工具

### Codex

```text
使用 sdd-delivery，基于这个 PRD 生成 Spec、技术方案、实现任务、单测计划和可观测交付产物。
```

### Claude Code

```text
请先阅读 skills/sdd-delivery/SKILL.md，并按照 SDD Delivery 流程处理这个 PRD。如果本地没有 Python，请手动创建和维护 Markdown / JSON 产物。
```

### Cursor

```text
请按照 skills/sdd-delivery/SKILL.md 中的流程，在 .sdd-delivery/<feature> 下创建交付产物，并维护需求追踪矩阵。
```

### GitHub Copilot Chat

```text
请基于 .sdd-delivery/<feature>/01-spec.md、03-requirement-trace.md、04-tech-solution.md 和 09-unit-test-report.md 审查这个 PR，优先输出风险和问题。
```

## 维护说明

- 修改 skill 后同步更新 `skills/sdd-delivery/SKILL.md`。
- 用户可见行为变化时更新 README。
- 破坏性 schema 变化时提升 major version。
- 新增脚本或新 artifact 时提升 minor version。
- 文档、提示词、模板微调提升 patch version。
- 保持无 Python 模式可用，脚本只能作为加速器。

详细说明见：`skills/sdd-delivery/references/plugin-operations.md`。

## 设计参考

SDD Delivery 综合参考了以下公开实践：

- GitHub Spec Kit：Spec-first、阶段化、artifact-first 的 SDD 工作流。
- OpenSpec：面向既有项目的变更规格和 brownfield 友好流程。
- Agent Skill 模式：`SKILL.md` + `references/` + `scripts/` 的渐进加载。
- Context checkpoint 模式：压缩 / 交接前写确定性 checkpoint。
- Requirement Traceability：把需求、Spec、方案、任务、代码、单测串起来。
- GitHub Delivery Practices：PR template、CI artifact validation、review gate。

详细说明见：`skills/sdd-delivery/references/open-source-influences.md`。

## English

SDD Delivery is a Codex plugin for PRD-driven, Spec-first engineering delivery. It helps AI coding agents turn a PRD into a reviewed Spec, then continue through technical solution design, review gates, implementation tasks, coding, unit tests, delivery review, checkpoints, and observability.

The goal is not to let an agent jump directly from PRD to code. The goal is to keep each delivery step reviewable, traceable, and recoverable.

## Visual Overview

### Positioning

![SDD Delivery Hero](assets/images/sdd-delivery-hero.png)

### Workflow

![SDD Delivery Workflow](assets/images/workflow-diagram.png)

```text
PRD → Spec → Spec Review → Trace Matrix → Technical Solution → Solution Review → Implementation Tasks → Code → Unit Tests → Delivery Review → Checkpoint & Observability
```

### Interaction

![Friendly Guided Interaction](assets/images/interaction-demo.png)

## Features

- **Spec-first delivery**: normalize PRDs into reviewable Specs before solution design.
- **Traceability**: connect PRD items, Spec items, solution sections, tasks, code, and tests.
- **Review gates**: built-in Spec Review, Solution Review, and Delivery Review.
- **Unit test loop**: maintain unit test plans, reports, and reverse `SPEC-*` coverage scans.
- **Observable delivery**: keep checkpoints, events, and an observability dashboard.
- **Context recovery**: resume long-running work after compaction, interruption, or agent handoff.
- **No Python fallback**: scripts are accelerators; the workflow still works with manual Markdown / JSON updates.
- **Plugin distribution**: packaged as a Codex plugin.

## Installation

Install this repository as a Codex plugin, then invoke:

```text
Use $sdd-delivery to turn this PRD into Spec, solution, reviewed implementation tasks, unit tests, and observable delivery artifacts.
```

You can also copy the skill directly:

```bash
cp -R skills/sdd-delivery ~/.codex/skills/sdd-delivery
```

## Guided Interaction

When no phase is specified, the agent should start with:

```text
Choose an SDD Delivery stage:
1. PRD to Spec
2. Spec Review
3. Technical Solution
4. Solution Review
5. Implementation Tasks
6. Code Implementation
7. Unit Test Plan / Report
8. Trace / Coverage
9. GitHub PR / CI Assets
10. 检查点 / 交接

Send a PRD or reply with a number.
```

## Quick Start

If Python is available, scripts can accelerate the workflow:

```bash
python skills/sdd-delivery/scripts/init_artifacts.py login-rate-limit
python skills/sdd-delivery/scripts/parse_prd_to_spec.py prd.md .sdd-delivery/login-rate-limit --force
python skills/sdd-delivery/scripts/trace_coverage.py .sdd-delivery/login-rate-limit
python skills/sdd-delivery/scripts/scan_test_coverage.py . .sdd-delivery/login-rate-limit --update-report --update-trace
python skills/sdd-delivery/scripts/sync_observability.py .sdd-delivery/login-rate-limit
python skills/sdd-delivery/scripts/validate_artifacts.py .sdd-delivery/login-rate-limit
```

## No Python Mode

If Python is unavailable, the agent should not fail. It should create and update the same Markdown / JSON artifacts manually and explain which automation steps were skipped.

## License

Choose a license before publishing. MIT is a common default for open-source developer tooling.

