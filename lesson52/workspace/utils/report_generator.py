"""
report_generator.py — Creates a visual HTML inspection report.
"""
from pathlib import Path
from datetime import datetime, timezone
from dataclasses import dataclass


def generate_html_report(
    elements: list,
    output_path: Path,
    title: str = "Appium Inspection Report",
) -> None:
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    rows = ""
    for el in elements:
        status = "✅" if el.resource_id else "⚠️ "
        clickable_badge = (
            '<span style="color:#059669;font-weight:bold">clickable</span>'
            if el.clickable else
            '<span style="color:#9ca3af">not-clickable</span>'
        )
        rows += f"""
        <tr>
          <td>{status}</td>
          <td><code>{el.resource_id or "—"}</code></td>
          <td>{el.text or "—"}</td>
          <td><code style="font-size:11px">{el.class_name}</code></td>
          <td>{clickable_badge}</td>
          <td><code style="font-size:10px">{el.bounds}</code></td>
        </tr>"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>{title}</title>
  <style>
    body   {{ font-family: -apple-system, sans-serif; background:#f9fafb; padding:24px; }}
    h1     {{ color:#1f2937; }}
    .meta  {{ color:#6b7280; font-size:13px; margin-bottom:24px; }}
    table  {{ border-collapse:collapse; width:100%; background:#fff;
              border-radius:8px; overflow:hidden;
              box-shadow:0 1px 3px rgba(0,0,0,0.1); }}
    th     {{ background:#3d93f5; color:#fff; padding:10px 14px; text-align:left; }}
    td     {{ padding:9px 14px; border-bottom:1px solid #e5e7eb; font-size:13px; }}
    tr:last-child td {{ border-bottom:none; }}
    tr:hover td {{ background:#eff6ff; }}
    code   {{ background:#f3f4f6; padding:2px 5px; border-radius:3px; }}
    .badge {{ background:#6ee7b7; color:#065f46; padding:2px 8px;
              border-radius:10px; font-size:11px; font-weight:bold; }}
  </style>
</head>
<body>
  <h1>🔍 {title}</h1>
  <p class="meta">Generated: {timestamp} | Elements found: {len(elements)}</p>
  <p><span class="badge">UQAP Lesson 52</span></p>
  <table>
    <thead>
      <tr>
        <th>Status</th><th>resource-id</th><th>text</th>
        <th>class</th><th>clickable</th><th>bounds</th>
      </tr>
    </thead>
    <tbody>{rows}</tbody>
  </table>
</body>
</html>"""

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(html, encoding="utf-8")
