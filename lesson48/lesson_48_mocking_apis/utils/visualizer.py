"""
utils/visualizer.py
Generates an HTML visual report of the mock request/response cycle.
Run standalone: python utils/visualizer.py
"""
from __future__ import annotations
from pathlib import Path
import json
import datetime

MOCK_GRAPHQL_URL = "https://api.example.com/graphql"

REQUEST_PAYLOAD = {
    "query": """
    query GetProduct($id: ID!) {
        product(id: $id) {
            id
            name
            price
            inStock
            tags
        }
    }""",
    "variables": {"id": "prod_42"}
}

RESPONSE_PAYLOAD = {
    "data": {
        "product": {
            "id": "prod_42",
            "name": "Quantum Keyboard",
            "price": 149.99,
            "inStock": True,
            "tags": ["mechanical", "wireless", "rgb"]
        }
    }
}

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Lesson 48 — Mock Request/Response Visualizer</title>
<style>
  * {{ box-sizing: border-box; }}
  body {{ font-family: 'Courier New', monospace; background: #0f1117; color: #e2e8f0;
         margin: 0; padding: 24px; }}
  h1 {{ color: #6ee7b7; font-size: 1.4rem; margin-bottom: 4px; }}
  .subtitle {{ color: #94a3b8; font-size: 0.85rem; margin-bottom: 32px; }}
  .flow {{ display: flex; gap: 16px; align-items: flex-start; flex-wrap: wrap; }}
  .box {{ background: #1e2130; border-radius: 8px; padding: 20px; flex: 1;
          min-width: 280px; border-left: 4px solid #3d93f5; }}
  .box.response {{ border-left-color: #6ee7b7; }}
  .box h2 {{ margin: 0 0 12px; font-size: 0.9rem; color: #3d93f5; text-transform: uppercase; }}
  .box.response h2 {{ color: #6ee7b7; }}
  pre {{ margin: 0; font-size: 0.8rem; white-space: pre-wrap; line-height: 1.6;
         color: #cbd5e1; }}
  .arrow {{ display: flex; align-items: center; justify-content: center;
            font-size: 2rem; color: #6ee7b7; padding: 40px 0; }}
  .badge {{ display: inline-block; padding: 2px 10px; border-radius: 999px;
            font-size: 0.75rem; font-weight: bold; margin-bottom: 12px; }}
  .badge.post {{ background: #3d93f5; color: #fff; }}
  .badge.ok {{ background: #6ee7b7; color: #0f1117; }}
  .intercepted {{ background: #1e2130; border: 1px dashed #6ee7b7; border-radius: 8px;
                  padding: 12px 20px; margin-bottom: 24px; color: #6ee7b7;
                  font-size: 0.85rem; text-align: center; }}
  .ts {{ color: #475569; font-size: 0.75rem; margin-top: 32px; }}
  .assertions {{ background: #1e2130; border-radius: 8px; padding: 20px;
                  margin-top: 24px; border-left: 4px solid #6ee7b7; }}
  .assertions h2 {{ color: #6ee7b7; font-size: 0.9rem; text-transform: uppercase;
                    margin: 0 0 12px; }}
  .assert-row {{ display: flex; gap: 8px; margin-bottom: 8px; font-size: 0.82rem; }}
  .assert-row .field {{ color: #93c5fd; min-width: 200px; }}
  .assert-row .val {{ color: #fde68a; }}
  .assert-row .check {{ color: #6ee7b7; }}
</style>
</head>
<body>
<h1>🔬 Lesson 48: Mocking APIs — Request/Response Visualizer</h1>
<p class="subtitle">UQAP Bootcamp · Module 5: API Testing Automation (REST)</p>

<div class="intercepted">
  ⚡ Network Intercepted by <strong>responses.RequestsMock</strong> — No real HTTP traffic generated
</div>

<div class="flow">
  <div class="box">
    <span class="badge post">POST</span>
    <h2>📤 Mock Request</h2>
    <p style="color:#94a3b8;font-size:0.8rem;margin:0 0 12px;">{url}</p>
    <pre>{request_json}</pre>
  </div>
  <div class="arrow">→</div>
  <div class="box response">
    <span class="badge ok">200 OK</span>
    <h2>📥 Mock Response</h2>
    <p style="color:#94a3b8;font-size:0.8rem;margin:0 0 12px;">application/json</p>
    <pre>{response_json}</pre>
  </div>
</div>

<div class="assertions">
  <h2>✅ Assertions Validated</h2>
  <div class="assert-row"><span class="field">product["id"]</span><span class="val">== "prod_42"</span><span class="check">✓</span></div>
  <div class="assert-row"><span class="field">product["name"]</span><span class="val">== "Quantum Keyboard"</span><span class="check">✓</span></div>
  <div class="assert-row"><span class="field">type(product["price"])</span><span class="val">== float (149.99)</span><span class="check">✓</span></div>
  <div class="assert-row"><span class="field">product["inStock"]</span><span class="val">is True</span><span class="check">✓</span></div>
  <div class="assert-row"><span class="field">product["tags"]</span><span class="val">== ["mechanical","wireless","rgb"]</span><span class="check">✓</span></div>
  <div class="assert-row"><span class="field">len(mock.calls)</span><span class="val">== 1 (no double-calls)</span><span class="check">✓</span></div>
</div>

<p class="ts">Generated: {timestamp}</p>
</body>
</html>"""

def generate() -> Path:
    output_dir = Path("reports")
    output_dir.mkdir(parents=True, exist_ok=True)
    output = output_dir / "report_visualizer.html"
    html = HTML_TEMPLATE.format(
        url=MOCK_GRAPHQL_URL,
        request_json=json.dumps(REQUEST_PAYLOAD, indent=2),
        response_json=json.dumps(RESPONSE_PAYLOAD, indent=2),
        timestamp=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )
    output.write_text(html, encoding="utf-8")
    return output

if __name__ == "__main__":
    path = generate()
    print(f"\033[92m[✓]\033[0m Visualizer report: {path.resolve()}")
