# 需求追踪

> 使用说明：这是追踪关系的事实源。每当 Spec、任务、代码文件或测试变化时都要更新。Status 列反映当前进度。

## 追踪矩阵

| PRD ID | Spec ID | 验收标准 | 方案章节 | Task ID | 代码文件 | 单元测试 | Status |
|---|---|---|---|---|---|---|---|
| PRD-1 | SPEC-1 | 用户可使用有效邮箱和密码登录 | Auth Module (section 3) | T1, T3 | auth/login.py, auth/models.py | test_login.py::test_valid_login | tested |
| PRD-2 | SPEC-2 | 无效凭据展示错误信息 | Auth Module (section 3) | T1 | auth/login.py | test_login.py::test_invalid_login | implemented |

## 状态说明

| Status | 含义 |
|--------|------|
| pending | 尚未处理 |
| specified | 已写入 Spec |
| reviewed | Spec 审查已通过或风险已接受 |
| designed | 已写入方案章节 |
| implemented | 代码已实现且测试通过 |
| tested | 单测报告已完成 |
| deferred | 有意推迟 |
| blocked | 因未决事项阻塞 |

## 已接受缺口

| Spec ID | 验收标准 | 原因 | 接受人 |
|---------|----------|------|--------|
| SPEC-5 | 10000 并发用户下限流正常 | 需要生产级压测环境 | User, 2025-01-15 |

## 一致性分析（第 5 阶段添加）

### Pass 1: 重复

- [发现项或“未发现”]

### Pass 2: 歧义

- [发现项]

### Pass 3: 规格不足

- [发现项]

### Pass 4: 宪法原则冲突

- [发现项]

### 摘要

- P0: N | P1: N | P2: N
