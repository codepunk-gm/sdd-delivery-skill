# Capability Menu

When starting a new SDD Delivery workflow, present this menu to the user unless they already gave a specific command.

## Supported capabilities

1. PRD 转 Spec
   - Parse or manually convert PRD into `00-prd.md`, `01-spec.md`, and `03-requirement-trace.md`.

2. 需求澄清
   - Run taxonomy-driven ambiguity scan against PRD items. Present at most 5 prioritized questions. Record resolutions.

3. Spec 审查
   - Review whether Spec is complete, testable, and suitable as the PRD review contract.

4. 一致性分析
   - Run four-pass cross-artifact consistency check (duplications, ambiguities, underspecified, constitution conflicts).

5. 技术方案
   - Produce `04-tech-solution.md` from approved Spec and repo evidence. Include pre-mortem.

6. 方案审查
   - Review architecture, compatibility, security, performance, rollback, and verification strategy.

7. 任务拆分
   - Split the approved solution into bounded, traceable tasks in `06-implementation-tasks.md` with boundary annotations.

8. 代码实现
   - Implement one task at a time (TDD: RED → GREEN → REFACTOR) while maintaining Context Contract, trace, log, and checkpoint.

9. 单测
   - Create `08-unit-test-plan.md`, run or document tests, update `09-unit-test-report.md`, and scan reverse SPEC-* coverage.

10. 交付审查
    - Final review in `10-delivery-review.md`. Verify boundaries, trace coverage, and security audit.

11. 检查点 / 交接
    - Update `11-checkpoint.json`, `12-observability.md`, and next action for compaction or handoff.

## Recommended opening response

Use concise wording:

```text
小智就绪。你可以直接发送 PRD，也可以选择阶段：

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

默认会使用中文产物、方案确认、按项目特征询问增强能力。
回复“配置”可以先调整语言、团队规则和增强能力。
```
