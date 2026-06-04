# Security Audit Checklist

Run during Solution Review (phase 8) and again during Delivery Review (phase 13). Mark findings in the corresponding review artifact.

Adapted from Don Cheli SDD Framework's OWASP-based security audit.

## When to Run

- **Solution Review:** Check the proposed design for security risks.
- **Delivery Review:** Check the implemented changes for introduced vulnerabilities.
- **On-demand:** When the change touches auth, data, APIs, or configuration.

## Checklist

### 1. Authentication and Authorization
- [ ] Does this change introduce new auth mechanisms or modify existing ones?
- [ ] Are there new roles, permissions, or access control rules?
- [ ] Is there any endpoint or function that bypasses authentication?
- [ ] Are session tokens, API keys, or credentials handled securely?

### 2. Data Exposure
- [ ] Does any new log message, error response, or debug output include sensitive data?
- [ ] Are new API responses filtering fields appropriately (no password hashes, internal IDs)?
- [ ] Is PII (email, name, phone, address) handled according to data policy?
- [ ] Are stack traces exposed to end users?

### 3. Input Validation
- [ ] Are all new user inputs validated (type, length, range, format)?
- [ ] Is there protection against SQL/NoSQL injection in new queries?
- [ ] Is there protection against XSS in new UI output?
- [ ] Are file uploads constrained (type, size, path)?

### 4. Dependency Changes
- [ ] Are new packages or libraries introduced? Version pinned?
- [ ] Are existing packages upgraded? Breaking changes reviewed?
- [ ] Are there known vulnerabilities in new or upgraded dependencies?

### 5. Configuration and Secrets
- [ ] Are new environment variables, config files, or secrets introduced?
- [ ] Are secrets hardcoded (check for API keys, tokens, passwords in source)?
- [ ] Are new config values documented with safe defaults?

### 6. API Surface Changes
- [ ] Are new API endpoints or changed signatures introduced?
- [ ] Is rate limiting considered for new endpoints?
- [ ] Is input size bounded for new endpoints?
- [ ] Are error responses consistent with existing API patterns?

### 7. File System and Infrastructure
- [ ] Does this change create, read, or delete files on disk?
- [ ] Are file paths validated (path traversal prevention)?
- [ ] Are there new database migrations or schema changes?
- [ ] Is there any change to container, orchestration, or deployment config?

## Severity

| Level | Definition | Examples |
|-------|-----------|---------|
| CRITICAL | Data breach, privilege escalation, remote code execution | SQL injection, exposed admin endpoint, hardcoded production secret |
| HIGH | Missing validation, exposed sensitive data, auth bypass | Unvalidated file upload, PII in logs, missing access control check |
| MEDIUM | Information leak, weak defaults, missing best practice | Verbose error messages, default password, missing HTTPS enforcement |
| LOW | Best practice deviation, minor hardening opportunity | Missing security header, overly permissive CORS |

## Output

Add a `## Security Audit` section to the review artifact:

```markdown
## Security Audit

| # | Category | Finding | Severity | Suggested Fix | Status |
|---|----------|---------|----------|---------------|--------|
| 1 | Input Validation | User search query is interpolated directly into SQL string | CRITICAL | Use parameterized query | Open |
| 2 | Data Exposure | Error response includes full stack trace | MEDIUM | Replace with generic error message in production | Open |

### Summary
- CRITICAL: N | HIGH: N | MEDIUM: N | LOW: N
- Blocks delivery: Yes (if any CRITICAL or HIGH unresolved)
```

## Post-Audit Actions

- CRITICAL findings: Must be fixed or accepted by user before delivery.
- HIGH findings: Should be fixed. Accept only with explicit user override and recorded risk.
- MEDIUM findings: Should be tracked. Can be deferred with rationale.
- LOW findings: Optional. Record for future hardening.
