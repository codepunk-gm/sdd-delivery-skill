# Capability Menu

When starting a new SDD Delivery workflow, present this menu to the user unless they already gave a specific command.

## Supported capabilities

1. PRD 转 Spec
   - 白话说明：把你的想法整理成可检查的需求说明。
   - Parse or manually convert PRD into `00-prd.md`, `01-spec.md`, and `03-requirement-trace.md`.

2. 需求澄清
   - 白话说明：找出还没说清楚、容易误解的地方。
   - Run taxonomy-driven ambiguity scan against PRD items. Present at most 5 prioritized questions. Record resolutions.

3. Spec 审查
   - 白话说明：检查需求说明能不能支撑后续开发。
   - Review whether Spec is complete, testable, and suitable as the PRD review contract.

4. 一致性分析
   - 白话说明：看需求、约束和现有项目有没有冲突。
   - Run four-pass cross-artifact consistency check (duplications, ambiguities, underspecified, constitution conflicts).

5. 技术方案
   - 白话说明：先设计怎么做，再决定动哪些代码。
   - Produce `04-tech-solution.md` from approved Spec and repo evidence. Include pre-mortem.

6. 方案审查
   - 白话说明：检查方案的风险、兼容性、安全和回滚。
   - Review architecture, compatibility, security, performance, rollback, and verification strategy.

7. 任务拆分
   - 白话说明：把方案拆成一件件可执行的小任务。
   - Split the approved solution into bounded, traceable tasks in `06-implementation-tasks.md` with boundary annotations.

8. 代码实现
   - 白话说明：按任务写测试、改代码、记录过程。
   - Implement one task at a time (TDD: RED → GREEN → REFACTOR) while maintaining Context Contract, trace, log, and checkpoint.

9. 单测
   - 白话说明：补齐测试计划、测试结果和覆盖关系。
   - Create `08-unit-test-plan.md`, run or document tests, update `09-unit-test-report.md`, and scan reverse SPEC-* coverage.

10. 交付审查
    - 白话说明：最后检查改动是否完整、可交接。
    - Final review in `10-delivery-review.md`. Verify boundaries, trace coverage, and security audit.

11. 检查点 / 交接
    - 白话说明：保存当前进度，方便中断后继续。
    - Update `11-checkpoint.json`, `12-observability.md`, and next action for compaction or handoff.

## Recommended opening response

Use concise wording:

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
