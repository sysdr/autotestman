"""
utils/bdd_reporter.py
Pure-Python HTML report generator.

Design goals:
  1. Zero external dependencies (no Jinja2, no Allure, no Node)
  2. Self-contained HTML — no CDN links (works on corporate VPNs)
  3. PM-readable: feature grouping, color badges, summary card
  4. CI-friendly: write once, archive as build artifact
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from datetime import datetime
from dataclasses import asdict


def generate_html_report(
    results: list,
    session_duration_s: float,
    output_path: Path,
) -> None:
    total   = len(results)
    passed  = sum(1 for r in results if r.status == "PASSED")
    failed  = total - passed
    pass_pct = round((passed / total * 100) if total else 0, 1)

    # Group by feature
    features: dict[str, list] = {}
    for r in results:
        features.setdefault(r.feature, []).append(r)

    rows_html = ""
    for feature_name, scenarios in features.items():
        rows_html += f'''
        <tr class="feature-header">
          <td colspan="4">📁 {feature_name}</td>
        </tr>'''
        for r in scenarios:
            badge   = "✅ PASSED" if r.status == "PASSED" else "❌ FAILED"
            row_cls = "passed" if r.status == "PASSED" else "failed"
            error   = f'<div class="error-detail">{r.error}</div>' if r.error else ""
            rows_html += f'''
        <tr class="{row_cls}">
          <td class="badge">{badge}</td>
          <td class="scenario-name">{r.scenario}{error}</td>
          <td class="duration">{r.duration_ms:.1f} ms</td>
          <td class="timestamp">{r.timestamp}</td>
        </tr>'''

    generated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>BDD Cucumber Report — UQAP</title>
  <style>
    /* ── Reset & Base ─────────────────────────────────── */
    *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      background: #f8fafc;
      color: #1e293b;
      padding: 2rem;
    }}

    /* ── Header ───────────────────────────────────────── */
    .header {{
      background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
      color: white;
      padding: 2rem 2.5rem;
      border-radius: 12px;
      margin-bottom: 1.5rem;
    }}
    .header h1 {{ font-size: 1.6rem; font-weight: 700; }}
    .header p  {{ color: #94a3b8; font-size: 0.9rem; margin-top: 0.3rem; }}

    /* ── Summary Cards ────────────────────────────────── */
    .summary {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
      gap: 1rem;
      margin-bottom: 1.5rem;
    }}
    .card {{
      background: white;
      border-radius: 10px;
      padding: 1.2rem 1.5rem;
      box-shadow: 0 1px 3px rgba(0,0,0,0.08);
      border-top: 4px solid #6ee7b7;
    }}
    .card.red {{ border-top-color: #fca5a5; }}
    .card.blue {{ border-top-color: #3d93f5; }}
    .card .value {{ font-size: 2rem; font-weight: 800; color: #0f172a; }}
    .card .label {{ font-size: 0.75rem; color: #64748b; text-transform: uppercase;
                    letter-spacing: 0.05em; margin-top: 0.2rem; }}

    /* ── Table ────────────────────────────────────────── */
    .table-wrap {{
      background: white;
      border-radius: 10px;
      box-shadow: 0 1px 3px rgba(0,0,0,0.08);
      overflow: hidden;
    }}
    table {{
      width: 100%;
      border-collapse: collapse;
      font-size: 0.9rem;
    }}
    th {{
      background: #f1f5f9;
      padding: 0.75rem 1rem;
      text-align: left;
      font-size: 0.75rem;
      text-transform: uppercase;
      letter-spacing: 0.06em;
      color: #475569;
      border-bottom: 1px solid #e2e8f0;
    }}
    td {{
      padding: 0.75rem 1rem;
      border-bottom: 1px solid #f1f5f9;
      vertical-align: top;
    }}

    /* ── Row States ───────────────────────────────────── */
    tr.passed  {{ background: #f0fdf4; }}
    tr.failed  {{ background: #fff1f2; }}
    tr.feature-header td {{
      background: #f8fafc;
      font-weight: 700;
      font-size: 0.85rem;
      color: #334155;
      padding: 0.6rem 1rem;
      border-top: 2px solid #e2e8f0;
    }}

    /* ── Cell Styles ─────────────────────────────────── */
    .badge        {{ font-weight: 600; white-space: nowrap; width: 110px; }}
    .scenario-name {{ font-weight: 500; }}
    .duration     {{ color: #64748b; white-space: nowrap; width: 100px; }}
    .timestamp    {{ color: #94a3b8; font-size: 0.8rem; white-space: nowrap; }}
    .error-detail {{
      font-family: monospace;
      font-size: 0.75rem;
      color: #dc2626;
      background: #fef2f2;
      border-left: 3px solid #fca5a5;
      padding: 0.4rem 0.6rem;
      margin-top: 0.4rem;
      border-radius: 4px;
      white-space: pre-wrap;
      max-height: 120px;
      overflow-y: auto;
    }}

    /* ── Footer ───────────────────────────────────────── */
    .footer {{
      text-align: center;
      color: #94a3b8;
      font-size: 0.8rem;
      margin-top: 1.5rem;
    }}
  </style>
</head>
<body>

  <div class="header">
    <h1>🥒 BDD Cucumber Report</h1>
    <p>Generated: {generated_at} &nbsp;·&nbsp; Total duration: {session_duration_s:.2f}s &nbsp;·&nbsp; UQAP Test Suite</p>
  </div>

  <div class="summary">
    <div class="card">
      <div class="value">{total}</div>
      <div class="label">Total Scenarios</div>
    </div>
    <div class="card">
      <div class="value" style="color:#16a34a">{passed}</div>
      <div class="label">Passed</div>
    </div>
    <div class="card red">
      <div class="value" style="color:#dc2626">{failed}</div>
      <div class="label">Failed</div>
    </div>
    <div class="card blue">
      <div class="value" style="color:#2563eb">{pass_pct}%</div>
      <div class="label">Pass Rate</div>
    </div>
    <div class="card">
      <div class="value">{session_duration_s:.2f}s</div>
      <div class="label">Total Duration</div>
    </div>
  </div>

  <div class="table-wrap">
    <table>
      <thead>
        <tr>
          <th>Status</th>
          <th>Scenario</th>
          <th>Duration</th>
          <th>Timestamp</th>
        </tr>
      </thead>
      <tbody>
        {rows_html}
      </tbody>
    </table>
  </div>

  <div class="footer">
    UQAP · Lesson 68: Reporting in BDD · Generated by bdd_reporter.py
  </div>

</body>
</html>'''

    output_path.write_text(html, encoding="utf-8")


def validate_report(report_path: Path) -> dict:
    """
    verify_result() helper.
    Returns a dict with validation results — no assertions,
    so callers can decide how to handle failures.
    """
    checks: dict[str, bool] = {}

    if not report_path.exists():
        return {"exists": False}

    content = report_path.read_text(encoding="utf-8")
    size_kb = report_path.stat().st_size / 1024

    checks["exists"]            = True
    checks["size_ok"]           = size_kb > 2          # must be >2KB (not empty)
    checks["has_summary_cards"] = "Total Scenarios" in content
    checks["has_table"]         = "<table" in content
    checks["no_cdn_links"]      = "cdn.jsdelivr" not in content and "cdnjs" not in content
    checks["self_contained"]    = checks["no_cdn_links"]
    checks["has_passed_row"]    = "PASSED" in content
    checks["valid_html"]        = content.startswith("<!DOCTYPE html>")

    # Dashboard summary cards: must show a real run (totals not stuck at zero)
    checks["summary_metrics_nonzero"] = False
    sm = re.search(r'<div class="summary">(.*?)<div class="table-wrap">', content, re.DOTALL)
    if sm:
        vals = re.findall(r'<div class="value"[^>]*>([^<]+)</div>', sm.group(1))
        if len(vals) >= 2:
            try:
                total_n = int(vals[0].strip())
                passed_n = int(vals[1].strip())
                checks["summary_metrics_nonzero"] = total_n > 0 and passed_n > 0
            except ValueError:
                pass

    return checks
