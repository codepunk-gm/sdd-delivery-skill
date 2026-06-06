# 单测计划

> 使用说明：先写测试再实现（RED -> GREEN -> REFACTOR）。每个测试映射到 Spec 验收标准，并随着 TDD 阶段更新状态。

## 测试用例

| Test ID | Spec ID | 场景（Given/When/Then） | 输入 / 准备 | 期望结果 | 测试目标 | Status |
|---|---|---|---|---|---|---|
| UT-1 | SPEC-1 | 有效登录：给定有效凭据，调用登录后返回 token | Mock auth service，DB 中有有效用户 | HTTP 200 + JWT token | test_auth.py::test_valid_login | red |
| UT-2 | SPEC-2 | 无效登录：给定错误密码，调用登录后返回错误 | Mock auth service，DB 中有有效用户 | HTTP 401 + error message | test_auth.py::test_invalid_login | pending |

## TDD 顺序

测试应按以下顺序编写和执行：

1. UT-1：有效登录（先覆盖主路径）
2. UT-2：无效凭据（错误路径）
3. UT-3：缺少字段（边界场景）

## 覆盖目标

- 需要覆盖的 Spec 条目：X / Y
- P0 条目覆盖率：必须 100%
- 边界场景覆盖：X / Y
- 已接受缺口：[列出原因]

## 状态说明

| Status | 含义 |
|--------|------|
| pending | 尚未编写 |
| red | 已编写、可运行，并且失败（功能尚未实现） |
| green | 已编写、可运行，并且通过（实现完成） |
| refactored | 在测试保持通过的前提下完成重构 |
| skipped | 有意跳过（需记录原因） |
