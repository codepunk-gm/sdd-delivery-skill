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

推荐启动菜单：

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

## 视觉概览

![SDD Delivery Hero](assets/images/sdd-delivery-hero.png)

![SDD Delivery Workflow](assets/images/workflow-diagram.png)

![Friendly Guided Interaction](assets/images/interaction-demo.png)

## 核心能力

- PRD 转 Spec
- Spec 审查
- 技术方案与方案审查
- 需求追踪矩阵
- 实现任务拆分
- 单测计划和单测报告
- 检查点与可观测面板
- 无 Python 模式

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
python scripts/validate_artifacts.py .sdd-delivery/login-rate-limit
```

## English

SDD Delivery is a Spec-first delivery skill for AI coding agents. Users do not need to remember script commands. They can send a PRD or choose a workflow stage, and the agent maintains the delivery artifacts.

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

## Optional Scripts

Scripts are optional accelerators:

```bash
python scripts/init_artifacts.py login-rate-limit
python scripts/parse_prd_to_spec.py prd.md .sdd-delivery/login-rate-limit --force
python scripts/validate_artifacts.py .sdd-delivery/login-rate-limit
```

