# 实现任务

> 使用说明：每个任务必须包含 `_Boundary:_`、`_Depends:_`、`_Size:_`，可并行任务使用 `[P]` 标记。禁止 XL 任务，超过 200 行预估变更必须拆分。

## 任务列表

### T1: [P] [SPEC-1] 实现用户登录接口

_Boundary:_ 仅 src/api/auth/。不要修改 src/models/ 或 src/services/。
_Depends:_ None
_Size:_ M

- [ ] T1 [P] [SPEC-1] 在 src/api/auth/login.py 实现 POST /auth/login
  - **Files:** src/api/auth/login.py, src/api/auth/__init__.py
  - **Verify:** `pytest tests/api/auth/test_login.py -v`
  - **Pre-TDD:** 先写测试并确认 RED，再实现

### T2: [SPEC-2] 增加登录限流

_Boundary:_ 仅 src/middleware/rate_limit/。不要修改 src/api/。
_Depends:_ T1（登录接口）
_Size:_ S

- [ ] T2 [SPEC-2] 在 src/middleware/rate_limit/login_limiter.py 增加限流中间件
  - **Files:** src/middleware/rate_limit/login_limiter.py
  - **Verify:** `pytest tests/middleware/rate_limit/test_login_limiter.py -v`

## 实现备注

> 记录跨任务经验。随着实现推进持续更新，避免后续任务重复踩坑。

- T1: [learning]
- T2: [learning]

## 任务规模

| 任务 | 规模 | 预估行数 | 是否就绪 |
|------|------|----------|----------|
| T1 | M | ~120 | Yes（无依赖） |
| T2 | S | ~45 | Pending（依赖 T1） |
