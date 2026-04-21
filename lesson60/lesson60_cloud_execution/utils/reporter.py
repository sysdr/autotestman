"""
utils/reporter.py — UQAP Lesson 60
Captures BrowserStack session URLs and writes a local HTML report.
"""
from __future__ import annotations
import json
import os
from pathlib import Path
from datetime import datetime

REPORT_DIR = Path("reports")


def save_session_report(
    session_id: str,
    test_name: str,
    status: str,
    duration_s: float,
    provider: str = "browserstack"
) -> Path:
    REPORT_DIR.mkdir(exist_ok=True)

    if provider == "browserstack":
        bs_user = os.getenv("BS_USERNAME", "unknown")
        session_url = (
            f"https://app-automate.browserstack.com/builds/"
            f"?sessionId={session_id}&userName={bs_user}"
        )
    else:
        session_url = f"https://app.saucelabs.com/tests/{session_id}"

    entry = {
        "session_id": session_id,
        "test": test_name,
        "status": status,
        "duration_s": round(duration_s, 2),
        "session_url": session_url,
        "timestamp": datetime.now().isoformat()
    }

    json_path = REPORT_DIR / "cloud_sessions.json"
    history: list[dict] = []
    if json_path.exists():
        history = json.loads(json_path.read_text())
    history.append(entry)
    json_path.write_text(json.dumps(history, indent=2))

    _generate_html(history)
    return json_path


def _generate_html(sessions: list[dict]) -> None:
    rows = ""
    for s in sessions:
        if s["status"] == "PASSED":
            colour = "#6ee7b7"
        elif s["status"] == "SKIPPED":
            colour = "#fcd34d"
        else:
            colour = "#fca5a5"
        rows += (
            f"<tr style='background:{colour}22'>"
            f"<td>{s['test']}</td>"
            f"<td><b>{s['status']}</b></td>"
            f"<td>{s['duration_s']}s</td>"
            f"<td><a href='{s['session_url']}' target='_blank'>"
            f"{s['session_id'][:12]}…</a></td>"
            f"<td>{s['timestamp'][:19]}</td></tr>"
        )

    html = f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8">
<title>UQAP Cloud Session Report</title>
<style>
  body {{ font-family: monospace; background: #0f172a; color: #e2e8f0; padding: 2rem; }}
  h1 {{ color: #6ee7b7; }} table {{ border-collapse: collapse; width: 100%; }}
  th {{ background: #1e293b; color: #3d93f5; padding: 8px 12px; text-align: left; }}
  td {{ padding: 8px 12px; border-bottom: 1px solid #334155; }}
  a {{ color: #3d93f5; }}
</style></head><body>
<h1>⚡ UQAP Cloud Session Report</h1>
<p>Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
<table><tr>
  <th>Test</th><th>Status</th><th>Duration</th><th>Session</th><th>Timestamp</th>
</tr>{rows}</table></body></html>"""

    (REPORT_DIR / "cloud_report.html").write_text(html)
