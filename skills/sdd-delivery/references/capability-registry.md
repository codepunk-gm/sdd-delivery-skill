# Capability Registry

Optional capability modules extend SDD Delivery at specific workflow nodes. User-facing interaction should describe what the capability does, not internal adapter/executor details.

## User-Facing Capability Names

| Internal ID | User-facing name | User-facing value |
|---|---|---|
| `frontend_template` | 前端模板保护 | 识别内置模板和组件目录，避免误改，并补充 UI 验证 |
| `java_modular_project` | Java 模块边界保护 | 识别模块边界和依赖方向，避免跨模块乱改 |
| `mcp_component_protocol` | 组件协议支持 | 优先通过 MCP / 组件协议选择现有组件，而不是手写替代 |
| `github_delivery_assets` | GitHub 交付资产 | 生成或检查 PR 模板、CI 校验和交付清单 |
| `team_code_principles` | 团队代码原则 | 启用设计模式、扩展性、长度限制、命名和错误处理审查 |

When talking to the user, use the user-facing name. Do not say "adapter", "executor", "registry", or raw capability IDs unless the user asks for internal details.

## How to Use

1. Detect project signals during Discovery.
2. Present at most 3 relevant capabilities to the user.
3. Read `11-checkpoint.json` capability switches.
4. If a relevant capability is `ask`, ask whether to enable it for the current feature.
5. Record the decision in `capabilities.<id>.state`.
6. Build `capability_executor_plan` from enabled capabilities.
7. Load only capabilities with `state: enabled` when entering the matching phase.

If the user skips capability setup, leave relevant capabilities as `ask`. If the user disables a capability, set it to `disabled` and do not ask again unless the user changes their mind.

## Capability Switch States

| State | Meaning | Agent Behavior |
|---|---|---|
| `enabled` | Capability is active for this feature | Load and apply the module instructions |
| `disabled` | Capability is intentionally off | Do not ask or apply it |
| `ask` | No durable decision yet | Ask only when project signals make it relevant |

Structured checkpoint shape:

```json
"capabilities": {
  "frontend_template": {
    "state": "enabled",
    "reason": "Detected package.json and src/components",
    "source": "user",
    "updated_at": "2026-06-06T10:00:00Z"
  }
}
```

`enabled_capabilities` is a compatibility index. The structured `capabilities` object is authoritative.

## Internal Adapter / Executor Model

Each capability has:

- **Adapter:** Detects whether the capability is relevant. Examples: repo scan, team-rule config, MCP/tool discovery.
- **Executor:** Describes how the enabled capability changes workflow behavior. Examples: phase instructions, script command, tool-mediated component discovery, review checklist.

The machine-readable registry lives in `assets/capabilities.json`. Use:

```bash
python scripts/manage_capabilities.py .sdd-delivery/<feature> --project-root . --detect --plan
python scripts/manage_capabilities.py .sdd-delivery/<feature> --set frontend_template=enabled --plan
```

Enabled executors are recorded in checkpoint `capability_executor_plan`.

## Capability Modules

| ID | Trigger Signals | Ask At | Adds |
|---|---|---|---|
| `frontend_template` | `package.json`, `vite.config.*`, `next.config.*`, `src/components/`, `app/`, `pages/` | Technical Solution or Implementation Tasks | Template/file inventory, UI verification expectations, screenshot/test checklist |
| `java_modular_project` | `pom.xml`, `build.gradle*`, `settings.gradle*`, `src/main/java`, multi-module folders | Technical Solution | Module boundary map, dependency direction checks, package-level task boundaries |
| `mcp_component_protocol` | MCP server config, component MCP tool references, design-system MCP, user mentions MCP components | Technical Solution or Implementation | MCP discovery step, component selection evidence, fallback if MCP is unavailable |
| `github_delivery_assets` | User asks for PR/CI assets or repo uses GitHub Actions | Delivery Review | PR template, CI artifact validation, delivery checklist |
| `team_code_principles` | User wants team rules, code review standards, file length/parameter/design checks | Startup or Per-Task Review | Loads `references/code-principles.md` modules into Gate 9 and Gate 12 review |

## User Prompt Pattern

```text
发现这个项目可能适合启用可插拔能力：

1. frontend_template：检测到 package.json / src/components
2. mcp_component_protocol：需求涉及 MCP 组件
3. team_code_principles：启用设计模式、扩展性、文件长度、参数数量等团队规则

是否启用？
1. 全部启用（推荐）
2. 只启用部分
3. 暂不决定，保持 ask
4. 全部禁用，不再询问
```

## Frontend Template Module

When enabled:

- Inventory existing templates, routes, components, styles, and generated files before proposing changes.
- Do not overwrite built-in files unless the task explicitly requires it.
- Add UI verification to the solution and test plan: browser preview, screenshot, responsive checks, and component state checks when tooling supports them.
- Keep template-specific work in bounded tasks. Example boundary: `src/components/auth/`, not the entire frontend app.

## Java Modular Project Module

When enabled:

- Identify modules, package boundaries, and dependency direction before proposing changes.
- Treat each module as a task boundary unless the solution explains why a cross-module change is necessary.
- Prefer interface-first changes at module edges.
- Record module dependency risks in the pre-mortem and solution review.

## MCP Component Protocol Module

When enabled:

- Discover available MCP component/tool capabilities before inventing UI components.
- Record chosen MCP component/tool names and evidence in `04-tech-solution.md`.
- If MCP is unavailable, document the fallback and ask before replacing it with hand-built components.
- Add verification for rendered component states and integration points.

## GitHub Delivery Assets Module

When enabled:

- Read `references/github-integration.md`.
- Generate or update GitHub PR/CI assets only when requested or when the user approves.
- Keep generated assets traceable to the delivery review.

## Team Code Principles Module

When enabled:

- Read `references/code-principles.md`.
- Apply enabled modules from `references/team-rules.md`.
- At Per-Task Review, check only modules that are enabled or accepted by the user.
- At Delivery Review, summarize violations by module and severity.
