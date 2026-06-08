#!/usr/bin/env python3
"""Generate a static HTML dashboard for an SDD Delivery feature."""
from __future__ import annotations

import argparse
import html
import json
from pathlib import Path

try:
    from _utils import append_event, load_json, now
    from dashboard_labels import QUALITY_LABELS, TEXT
except ImportError:
    from scripts._utils import append_event, load_json, now
    from scripts.dashboard_labels import QUALITY_LABELS, TEXT


DASHBOARD_FILE = "13-dashboard.html"


def esc(value: object) -> str:
    return html.escape("" if value is None else str(value), quote=True)


def status_class(value: object) -> str:
    normalized = str(value or "").lower().replace("_", "-")
    if normalized in {"passed", "approved", "reviewed", "ready", "sufficient", "high", "on-track", "available", "enabled", "pass"}:
        return "good"
    if normalized in {"accepted-risk", "partial", "medium", "gap", "changes-requested", "at-risk", "ask"}:
        return "warn"
    if normalized in {"blocked", "failed", "rejected", "low", "unavailable", "disabled"}:
        return "bad"
    return "muted"


def percent(part: int | float, total: int | float) -> int:
    try:
        total_value = float(total)
        if total_value <= 0:
            return 0
        return max(0, min(100, round(float(part) / total_value * 100)))
    except (TypeError, ValueError):
        return 0


def read_events(folder: Path, limit: int = 8) -> list[dict]:
    path = folder / "events.jsonl"
    if not path.exists():
        return []
    events: list[dict] = []
    for line in path.read_text(encoding="utf-8-sig").splitlines():
        if not line.strip():
            continue
        try:
            events.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return events[-limit:]


def list_artifacts(folder: Path) -> list[str]:
    names = [
        "00-prd.md",
        "01-spec.md",
        "02-spec-review.md",
        "03-requirement-trace.md",
        "04-tech-solution.md",
        "05-solution-review.md",
        "06-implementation-tasks.md",
        "07-implementation-log.md",
        "08-unit-test-plan.md",
        "09-unit-test-report.md",
        "10-delivery-review.md",
        "11-checkpoint.json",
        "12-observability.md",
        "mcp-discovery.json",
        "mcp-component-selection.md",
        "events.jsonl",
    ]
    return [name for name in names if (folder / name).exists()]


def pill(label: object) -> str:
    return f'<span class="pill {status_class(label)}">{esc(label or "pending")}</span>'


def progress_bar(label: str, value: int) -> str:
    return (
        '<div class="progress-row">'
        f'<span>{esc(label)}</span>'
        '<div class="bar"><i style="width: {width}%"></i></div>'
        f'<strong>{value}%</strong>'
        '</div>'
    ).format(width=value)


def mcp_item_names(mcp: dict) -> str:
    if not mcp:
        return "-"
    names: list[str] = []
    for key in ["servers", "tools", "resources", "components"]:
        for item in mcp.get(key, []):
            name = item.get("name") if isinstance(item, dict) else ""
            if name:
                names.append(str(name))
    return "、".join(names) if names else "-"


def render_dashboard(folder: Path) -> str:
    checkpoint = load_json(folder / "11-checkpoint.json")
    trace = load_json(folder / "trace-coverage.json")
    tests = load_json(folder / "test-spec-coverage.json")
    mcp = load_json(folder / "mcp-discovery.json")

    metrics = dict(checkpoint.get("metrics", {}))
    metrics.update(trace)
    gates = checkpoint.get("gate_status", {})
    capabilities = checkpoint.get("capabilities", {})
    mcp_switch = capabilities.get("mcp_component_protocol", {}) if isinstance(capabilities, dict) else {}
    milestones = checkpoint.get("milestones", [])
    human_reviews = checkpoint.get("human_reviews", [])
    quality = checkpoint.get("quality_status", {})
    risks = checkpoint.get("risks", [])
    blockers = checkpoint.get("blockers", [])
    events = read_events(folder)
    artifacts = list_artifacts(folder)

    tasks_total = metrics.get("tasks_total", 0)
    tasks_completed = metrics.get("tasks_completed", 0)
    checks_total = metrics.get("checks_total", 0)
    checks_passed = metrics.get("checks_passed", 0)
    review_open = metrics.get("review_findings_open", 0)
    review_closed = metrics.get("review_findings_closed", 0)
    mcp_items = (
        len(mcp.get("servers", []))
        + len(mcp.get("tools", []))
        + len(mcp.get("resources", []))
        + len(mcp.get("components", []))
        if mcp
        else 0
    )
    mcp_names = mcp_item_names(mcp)

    milestone_cards = []
    for milestone in milestones:
        evidence = milestone.get("evidence", [])
        evidence_links = " ".join(
            f'<a href="{esc(name)}">{esc(name)}</a>' for name in evidence if isinstance(name, str)
        )
        milestone_cards.append(
            '<article class="milestone">'
            f'<div><strong>{esc(milestone.get("id", ""))}</strong><h3>{esc(milestone.get("name", ""))}</h3></div>'
            f'{pill(milestone.get("status", "pending"))}'
            f'<p>Reviewer: {esc(milestone.get("reviewer", "") or "-")}</p>'
            f'<p class="links">{evidence_links}</p>'
            '</article>'
        )

    gate_rows = "".join(
        f"<tr><td>{esc(gate)}</td><td>{pill(status)}</td></tr>"
        for gate, status in gates.items()
    )
    quality_rows = "".join(
        f"<tr><td>{esc(QUALITY_LABELS.get(key, key))}</td><td>{pill(value)}</td></tr>"
        for key, value in quality.items()
    )
    review_rows = "".join(
        "<tr>"
        f"<td>{esc(item.get('time', ''))}</td>"
        f"<td>{esc(item.get('reviewer', ''))}</td>"
        f"<td>{esc(item.get('target', ''))}</td>"
        f"<td>{pill(item.get('result', ''))}</td>"
        f"<td>{esc(item.get('notes', ''))}</td>"
        "</tr>"
        for item in human_reviews
    ) or f'<tr><td colspan="5" class="empty">{TEXT["no_reviews"]}</td></tr>'

    event_rows = "".join(
        "<tr>"
        f"<td>{esc(item.get('time', ''))}</td>"
        f"<td>{esc(item.get('event', ''))}</td>"
        f"<td>{esc(json.dumps(item.get('detail', {}), ensure_ascii=False))}</td>"
        "</tr>"
        for item in events
    ) or f'<tr><td colspan="3" class="empty">{TEXT["no_events"]}</td></tr>'

    artifact_links = "".join(f'<a href="{esc(name)}">{esc(name)}</a>' for name in artifacts)
    risk_items = "".join(f"<li>{esc(item)}</li>" for item in risks) or f'<li class="empty">{TEXT["no_risks"]}</li>'
    blocker_items = "".join(f"<li>{esc(item)}</li>" for item in blockers) or f'<li class="empty">{TEXT["no_blockers"]}</li>'

    task_rate = percent(tasks_completed, tasks_total)
    check_rate = percent(checks_passed, checks_total)
    review_rate = percent(review_closed, review_open + review_closed)

    generated_at = now()
    return f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{TEXT["dashboard_title"]} - {esc(checkpoint.get('feature', folder.name))}</title>
  <style>
    :root {{
      color-scheme: light;
      --bg: #f6f7f9;
      --panel: #ffffff;
      --text: #17202a;
      --muted: #637083;
      --line: #d9dee7;
      --good: #0f7b4f;
      --good-bg: #dff6ea;
      --warn: #946200;
      --warn-bg: #fff1cc;
      --bad: #b42318;
      --bad-bg: #ffe4df;
      --info: #2457a6;
      --info-bg: #e4edff;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      background: var(--bg);
      color: var(--text);
      font: 14px/1.5 -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    }}
    header {{
      padding: 24px 32px 18px;
      background: #ffffff;
      border-bottom: 1px solid var(--line);
    }}
    header h1 {{ margin: 0 0 8px; font-size: 28px; letter-spacing: 0; }}
    header p {{ margin: 0; color: var(--muted); }}
    main {{ padding: 24px 32px 40px; max-width: 1440px; margin: 0 auto; }}
    .grid {{ display: grid; gap: 16px; }}
    .top {{ grid-template-columns: 1.2fr .8fr; align-items: stretch; }}
    .three {{ grid-template-columns: repeat(3, minmax(0, 1fr)); }}
    .two {{ grid-template-columns: repeat(2, minmax(0, 1fr)); }}
    section, .card {{
      background: var(--panel);
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 16px;
      min-width: 0;
    }}
    h2 {{ margin: 0 0 12px; font-size: 16px; }}
    h3 {{ margin: 2px 0 0; font-size: 15px; }}
    .summary {{
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 12px;
    }}
    .metric span, .meta span {{ display: block; color: var(--muted); font-size: 12px; }}
    .metric strong {{ display: block; margin-top: 2px; font-size: 24px; }}
    .meta strong {{ display: block; margin-top: 2px; word-break: break-word; }}
    .pill {{
      display: inline-flex;
      align-items: center;
      min-height: 24px;
      padding: 2px 8px;
      border-radius: 999px;
      font-size: 12px;
      font-weight: 650;
      white-space: nowrap;
    }}
    .pill.good {{ color: var(--good); background: var(--good-bg); }}
    .pill.warn {{ color: var(--warn); background: var(--warn-bg); }}
    .pill.bad {{ color: var(--bad); background: var(--bad-bg); }}
    .pill.muted {{ color: var(--muted); background: #eef1f5; }}
    table {{ width: 100%; border-collapse: collapse; }}
    th, td {{ padding: 9px 8px; border-top: 1px solid var(--line); text-align: left; vertical-align: top; }}
    th {{ color: var(--muted); font-size: 12px; font-weight: 650; }}
    .milestones {{ grid-template-columns: repeat(5, minmax(150px, 1fr)); }}
    .milestone {{ padding: 14px; border: 1px solid var(--line); border-radius: 8px; background: #fbfcfe; }}
    .milestone p {{ margin: 8px 0 0; color: var(--muted); }}
    .links {{ display: flex; flex-wrap: wrap; gap: 6px; }}
    a {{ color: var(--info); text-decoration: none; }}
    a:hover {{ text-decoration: underline; }}
    .links a, .artifact-list a {{
      display: inline-flex;
      padding: 3px 7px;
      border-radius: 6px;
      background: var(--info-bg);
      margin: 0 6px 6px 0;
      font-size: 12px;
    }}
    .progress-row {{ display: grid; grid-template-columns: 150px 1fr 48px; gap: 10px; align-items: center; margin: 10px 0; }}
    .bar {{ height: 10px; background: #e8ecf2; border-radius: 999px; overflow: hidden; }}
    .bar i {{ display: block; height: 100%; background: var(--info); border-radius: inherit; }}
    ul {{ margin: 0; padding-left: 18px; }}
    .empty {{ color: var(--muted); }}
    .footer {{ margin-top: 18px; color: var(--muted); font-size: 12px; }}
    @media (max-width: 980px) {{
      header, main {{ padding-left: 16px; padding-right: 16px; }}
      .top, .three, .two, .milestones {{ grid-template-columns: 1fr; }}
      .summary {{ grid-template-columns: 1fr; }}
      .progress-row {{ grid-template-columns: 1fr; }}
    }}
  </style>
</head>
<body>
  <header>
    <h1>{TEXT["dashboard_title"]}</h1>
    <p>{esc(checkpoint.get('feature', folder.name))} · {TEXT["generated"]} {esc(generated_at)}</p>
  </header>
  <main class="grid">
    <div class="grid top">
      <section>
        <h2>{TEXT["current_status"]}</h2>
        <div class="summary">
          <div class="meta"><span>{TEXT["goal"]}</span><strong>{esc(checkpoint.get('goal', '') or '-')}</strong></div>
          <div class="meta"><span>{TEXT["next_action"]}</span><strong>{esc(checkpoint.get('next_action', '') or '-')}</strong></div>
          <div class="meta"><span>{TEXT["current_phase"]}</span><strong>{esc(checkpoint.get('current_phase', '') or '-')}</strong></div>
          <div class="meta"><span>{TEXT["active_task"]}</span><strong>{esc(checkpoint.get('active_task', '') or '-')}</strong></div>
        </div>
      </section>
      <section>
        <h2>{TEXT["delivery_metrics"]}</h2>
        {progress_bar(TEXT["tasks_completed"], task_rate)}
        {progress_bar(TEXT["checks_passed"], check_rate)}
        {progress_bar(TEXT["review_findings_closed"], review_rate)}
      </section>
    </div>

    <section>
      <h2>{TEXT["milestones"]}</h2>
      <div class="grid milestones">{''.join(milestone_cards)}</div>
    </section>

    <div class="grid two">
      <section>
        <h2>{TEXT["gate_status"]}</h2>
        <table><thead><tr><th>{TEXT["gate"]}</th><th>{TEXT["status"]}</th></tr></thead><tbody>{gate_rows}</tbody></table>
      </section>
      <section>
        <h2>{TEXT["quality_status"]}</h2>
        <table><thead><tr><th>{TEXT["area"]}</th><th>{TEXT["status"]}</th></tr></thead><tbody>{quality_rows}</tbody></table>
      </section>
    </div>

    <div class="grid three">
      <section>
        <h2>{TEXT["mcp_evidence"]}</h2>
        <div class="summary">
          <div class="metric"><span>{TEXT["capability"]}</span><strong>{pill(mcp_switch.get('state', 'ask'))}</strong></div>
          <div class="metric"><span>{TEXT["discovery"]}</span><strong>{pill(mcp.get('status', 'not_started') if mcp else 'not_started')}</strong></div>
          <div class="metric"><span>{TEXT["items"]}</span><strong>{esc(mcp_items)}</strong></div>
          <div class="metric"><span>{TEXT["source"]}</span><strong>{esc(mcp.get('source', '') if mcp else '-')}</strong></div>
          <div class="meta"><span>{TEXT["discovered_items"]}</span><strong>{esc(mcp_names)}</strong></div>
        </div>
      </section>
      <section>
        <h2>{TEXT["risks"]}</h2>
        <ul>{risk_items}</ul>
      </section>
      <section>
        <h2>{TEXT["blockers"]}</h2>
        <ul>{blocker_items}</ul>
      </section>
    </div>

    <section>
      <h2>{TEXT["human_reviews"]}</h2>
      <table><thead><tr><th>{TEXT["time"]}</th><th>{TEXT["reviewer"]}</th><th>{TEXT["target"]}</th><th>{TEXT["result"]}</th><th>{TEXT["notes"]}</th></tr></thead><tbody>{review_rows}</tbody></table>
    </section>

    <section>
      <h2>{TEXT["recent_events"]}</h2>
      <table><thead><tr><th>{TEXT["time"]}</th><th>{TEXT["event"]}</th><th>{TEXT["detail"]}</th></tr></thead><tbody>{event_rows}</tbody></table>
    </section>

    <section>
      <h2>{TEXT["evidence_files"]}</h2>
      <div class="artifact-list">{artifact_links}</div>
      <p class="footer">{TEXT["footer"]}</p>
    </section>
  </main>
</body>
</html>
"""


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate a static SDD Delivery HTML dashboard.")
    parser.add_argument("folder", help="Feature artifact folder")
    args = parser.parse_args()

    folder = Path(args.folder).resolve()
    html_text = render_dashboard(folder)
    output = folder / DASHBOARD_FILE
    output.write_text(html_text, encoding="utf-8")
    append_event(folder, "dashboard_generated", {"file": DASHBOARD_FILE})
    print(json.dumps({"dashboard": str(output)}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
