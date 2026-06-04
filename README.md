# SDD Delivery Plugin

[中文](#中文说明) | [English](#english)

## 中文说明

SDD Delivery 是一个面向 AI 编程助手的 Spec-first 研发交付插件。它的目标不是让 AI 直接“看 PRD 写代码”，而是把交付过程拆成可审查、可追踪、可恢复的步骤：PRD 先转成 Spec，再进入方案、审查、实现、单测和交付检查。

## 安装与使用

### 方式一：通过 Codex 插件市场安装（推荐）

在 Codex 客户端中，先添加这个仓库作为插件市场：

```text
/plugin marketplace add codepunk-gm/sdd-delivery-skill
```

客户端会读取本仓库根目录的 `marketplace.json`。然后安装插件：

```text
/plugin install sdd-delivery
```

安装完成后，建议开启一个新的 Codex 会话，然后输入：

```text
使用 sdd-delivery，基于这个 PRD 生成 Spec、技术方案、审查清单、实现任务、单测计划和可观测交付产物。
```

也可以使用英文：

```text
Use $sdd-delivery to turn this PRD into Spec, solution, reviewed implementation tasks, unit tests, and observable delivery artifacts.
```
### 方式二：作为普通 Skill 安装

如果你只想安装 skill，可以复制内置目录：

```bash
cp -R skills/sdd-delivery ~/.codex/skills/sdd-delivery
```

Windows 可以复制到：

```text
%USERPROFILE%\.codex\skills\sdd-delivery
```

### 方式三：在其他 AI 编程工具中使用

如果使用 Claude Code、Cursor、GitHub Copilot Chat、Windsurf 或 Continue，可以让工具先读取：

```text
skills/sdd-delivery/SKILL.md
```

然后使用类似提示：

```text
请按照 SDD Delivery 的流程处理这个 PRD。先生成 Spec，再进行审查、技术方案、任务拆分、实现和单测。没有 Python 时，请直接手动维护 Markdown / JSON 产物。
```

## 日常使用方式

用户不需要记脚本命令。正常使用时，只要把 PRD 发给 AI，并选择下一步即可。

推荐的启动交互：

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

对于小改动，可以选择轻量模式：

```text
这个需求看起来比较小，可以选择：
1. 轻量模式：最小改动 + 简短验证
2. 完整流程：Spec、审查、需求追踪、单测、检查点
```

## 视觉概览

### 项目定位

![SDD Delivery Hero](assets/images/sdd-delivery-hero.png)

### 完整流程

![SDD Delivery Workflow](assets/images/workflow-diagram.png)

```text
PRD → Spec → Spec 审查 → 需求追踪矩阵 → 技术方案 → 方案审查 → 实现任务 → 代码实现 → 单测 → 交付审查 → 检查点与可观测面板
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
- **无 Python 兜底**：脚本是加速器；没有 Python 时，agent 仍可手动维护 Markdown / JSON 产物。
- **插件分发**：可作为 Codex 插件安装和使用。

## 产物目录

完整流程会在项目中维护一个需求级目录：

```text
.sdd-delivery/<feature>/
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

## 无 Python 模式

Python 不是使用前提。没有 Python 时，AI 应该继续执行同样流程，只是改为手动创建和更新 Markdown / JSON 文件。

无 Python 模式下，agent 应完成：

```text
1. 创建 .sdd-delivery/<feature>/ 目录
2. 整理 PRD 到 00-prd.md
3. 生成 01-spec.md
4. 维护 03-requirement-trace.md
5. 输出技术方案和审查结果
6. 维护单测计划、单测报告和交付审查
7. 更新 11-checkpoint.json 和 12-observability.md
```

## 可选自动化脚本

脚本只用于加速，不是使用者必须执行的步骤。如果环境中有 Python，可以用以下脚本自动生成或校验产物：

```bash
python skills/sdd-delivery/scripts/init_artifacts.py login-rate-limit
python skills/sdd-delivery/scripts/parse_prd_to_spec.py prd.md .sdd-delivery/login-rate-limit --force
python skills/sdd-delivery/scripts/trace_coverage.py .sdd-delivery/login-rate-limit
python skills/sdd-delivery/scripts/scan_test_coverage.py . .sdd-delivery/login-rate-limit --update-report --update-trace
python skills/sdd-delivery/scripts/sync_observability.py .sdd-delivery/login-rate-limit
python skills/sdd-delivery/scripts/validate_artifacts.py .sdd-delivery/login-rate-limit
```

## 单测如何关联 Spec

在测试文件中标注对应的 Spec ID：

```python
def test_login_rate_limit_blocks_after_threshold():
    """Covers SPEC-1 and SPEC-2."""
    assert True
```

如果启用脚本，可以反查测试覆盖并回写追踪矩阵：

```bash
python skills/sdd-delivery/scripts/scan_test_coverage.py . .sdd-delivery/login-rate-limit --update-report --update-trace
```

## GitHub 集成

可以生成 PR 模板和 GitHub Actions 校验文件：

```bash
python skills/sdd-delivery/scripts/generate_github_assets.py .
```

生成内容：

```text
.github/pull_request_template.md
.github/workflows/sdd-delivery-artifacts.yml
.github/scripts/validate_devflow_artifacts.py
```

## 仓库结构

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

## 维护说明

- 修改 skill 后同步更新 `skills/sdd-delivery/SKILL.md`。
- 用户可见行为变化时更新 README。
- 破坏性 schema 变化时提升 major version。
- 新增脚本或新 artifact 时提升 minor version。
- 文档、提示词、模板微调提升 patch version。
- 保持无 Python 模式可用，脚本只能作为加速器。

详细说明见：`skills/sdd-delivery/references/plugin-operations.md`。

## 参考的优秀设计

SDD Delivery 不是从零发明一套流程，而是把社区里比较成熟的工程实践组合成一个适合 AI 编程助手使用的交付插件。

| 参考来源 | 借鉴点 | 在 SDD Delivery 中的落地 |
|---|---|---|
| [GitHub Spec Kit](https://github.com/github/spec-kit) | Spec-first、阶段化、以产物驱动实现 | 把 `01-spec.md` 作为 PRD 审查前置产物，并通过 Spec → 方案 → 任务 → 实现推进 |
| [OpenSpec](https://github.com/Fission-AI/OpenSpec) | 面向既有项目的变更规格、提案和演进记录 | 增加 `04-tech-solution.md`、`05-solution-review.md`、`10-delivery-review.md`，让变更有设计和审查记录 |
| Agent Skill 设计模式 | `SKILL.md` 负责触发和流程，详细说明按需加载 | 使用 `SKILL.md` + `references/` + `assets/templates/` + `scripts/` 的渐进加载结构 |
| 上下文工程 / Checkpoint 实践 | 长任务不能只依赖聊天记录，需要可恢复的结构化状态 | 使用 `11-checkpoint.json`、`12-observability.md` 和 `events.jsonl` 记录阶段、风险、测试和下一步 |
| 需求追踪矩阵 | 需求、设计、任务、代码和测试需要可追溯 | 使用 `03-requirement-trace.md` 串联 PRD、Spec、方案、任务、代码文件和单测 |
| GitHub 交付实践 | PR 模板、CI 校验、审查清单可以降低交付风险 | 提供 `generate_github_assets.py` 生成 PR 模板和 GitHub Actions artifact 校验 |
| 测试覆盖反查 | 测试应该能说明覆盖了哪些需求或验收标准 | 使用 `SPEC-*` 标记和 `scan_test_coverage.py` 反查单测覆盖 |

这些参考只提供设计思路。本项目的核心目标是把它们整理成一个可安装、可交互、可恢复、可观测的 Codex 插件。
## English

SDD Delivery is a Codex plugin for PRD-driven, Spec-first engineering delivery. It helps AI coding agents turn a PRD into a reviewed Spec, then continue through technical solution design, review gates, implementation tasks, coding, unit tests, delivery review, checkpoints, and observability.

## Installation and Usage

### Install from the Codex plugin marketplace

In the Codex client, add this repository as a plugin marketplace:

```text
/plugin marketplace add codepunk-gm/sdd-delivery-skill
```

The client reads the root `marketplace.json` from this repository. Then install the plugin:

```text
/plugin install sdd-delivery
```

Start a new Codex session and invoke:

```text
Use $sdd-delivery to turn this PRD into Spec, solution, reviewed implementation tasks, unit tests, and observable delivery artifacts.
```

### Install as a standalone skill

```bash
cp -R skills/sdd-delivery ~/.codex/skills/sdd-delivery
```

### Use with other AI coding tools

Ask the tool to read:

```text
skills/sdd-delivery/SKILL.md
```

Then prompt:

```text
Follow the SDD Delivery workflow for this PRD. Start with Spec, then review, technical solution, task breakdown, implementation, and unit tests. If Python is unavailable, maintain the Markdown / JSON artifacts manually.
```

## Normal Usage

Users do not need to remember script commands. Start by sending a PRD or choosing a stage:

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
10. Checkpoint / Handoff

Send a PRD or reply with a number.
```

## Features

- **Spec-first delivery**: normalize PRDs into reviewable Specs before solution design.
- **Traceability**: connect PRD items, Spec items, solution sections, tasks, code, and tests.
- **Review gates**: built-in Spec Review, Solution Review, and Delivery Review.
- **Unit test loop**: maintain unit test plans, reports, and reverse `SPEC-*` coverage scans.
- **Observable delivery**: keep checkpoints, events, and an observability dashboard.
- **No Python fallback**: scripts are accelerators; the workflow still works with manual Markdown / JSON updates.
- **Plugin distribution**: packaged as a Codex plugin.

## Optional Automation

If Python is available, scripts can speed up artifact creation and validation:

```bash
python skills/sdd-delivery/scripts/init_artifacts.py login-rate-limit
python skills/sdd-delivery/scripts/parse_prd_to_spec.py prd.md .sdd-delivery/login-rate-limit --force
python skills/sdd-delivery/scripts/trace_coverage.py .sdd-delivery/login-rate-limit
python skills/sdd-delivery/scripts/scan_test_coverage.py . .sdd-delivery/login-rate-limit --update-report --update-trace
python skills/sdd-delivery/scripts/sync_observability.py .sdd-delivery/login-rate-limit
python skills/sdd-delivery/scripts/validate_artifacts.py .sdd-delivery/login-rate-limit
```

## No Python Mode

Python is not required. If Python is unavailable, the agent should create and update the same Markdown / JSON artifacts manually and explain which automation steps were skipped.

## Design References

SDD Delivery is not a new process invented from scratch. It combines proven engineering patterns into a plugin-friendly workflow for AI coding agents.

| Reference | What it inspired | How SDD Delivery applies it |
|---|---|---|
| [GitHub Spec Kit](https://github.com/github/spec-kit) | Spec-first development, phased workflow, artifact-driven implementation | Uses `01-spec.md` as the reviewable contract before technical solution and implementation |
| [OpenSpec](https://github.com/Fission-AI/OpenSpec) | Brownfield-friendly change specs, proposals, and evolution records | Adds technical solution, solution review, and delivery review artifacts for existing projects |
| Agent Skill patterns | Keep trigger logic concise and load details progressively | Uses `SKILL.md`, `references/`, `assets/templates/`, and optional `scripts/` |
| Context engineering / checkpoint patterns | Long-running agent work needs recoverable structured state | Uses `11-checkpoint.json`, `12-observability.md`, and `events.jsonl` |
| Requirement traceability | Requirements, design, tasks, code, and tests should stay connected | Uses `03-requirement-trace.md` to map PRD, Spec, solution, tasks, files, and tests |
| GitHub delivery practices | PR templates, CI checks, and review checklists reduce delivery risk | Provides `generate_github_assets.py` for PR templates and GitHub Actions artifact validation |
| Test coverage reverse mapping | Tests should indicate which requirements or acceptance criteria they cover | Uses `SPEC-*` markers and `scan_test_coverage.py` to scan unit test coverage |

These projects and practices are design references, not copied implementations. SDD Delivery packages the ideas into an installable, interactive, recoverable, and observable Codex plugin.

## License

Choose a license before publishing. MIT is a common default for open-source developer tooling.






