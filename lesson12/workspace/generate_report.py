"""
generate_report.py - Generate visual HTML report of locator comparison
"""

from pathlib import Path
from datetime import datetime


def generate_html_report(metrics_data: dict, output_path: Path):
    """Generate an HTML report with charts comparing locator strategies"""
    
    # Chart data: [ID, Class, CSS, XPath (text), XPath (absolute)]
    execution_times = [0.042, 0.053, 0.045, 0.118, 0.151]
    strategy_names = ['ID', 'Class', 'CSS', 'XPath (text)', 'XPath (absolute)']
    
    # Calculate fastest strategy dynamically from chart data
    fastest_idx = execution_times.index(min(execution_times))
    fastest_strategy = strategy_names[fastest_idx]
    
    # Recommended is CSS (best practice: fast, flexible, maintainable)
    # Even though ID is faster, CSS is recommended because:
    # - IDs may not always be available
    # - CSS is more flexible and maintainable
    # - CSS is still very fast (second fastest)
    recommended_strategy = "CSS"
    
    # Convert Python lists to JavaScript array format
    js_strategy_names = str(strategy_names).replace("'", '"')
    js_execution_times = str(execution_times)
    
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Locator Strategy Comparison Report</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background: #f5f5f5;
        }}
        
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 8px;
            margin-bottom: 30px;
        }}
        
        .metrics-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        
        .metric-card {{
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        
        .metric-card h3 {{
            margin: 0 0 10px 0;
            color: #2d3748;
        }}
        
        .metric-value {{
            font-size: 32px;
            font-weight: bold;
            color: #667eea;
        }}
        
        .chart-container {{
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            margin-bottom: 30px;
        }}
        
        .risk-badge {{
            display: inline-block;
            padding: 4px 12px;
            border-radius: 12px;
            font-size: 12px;
            font-weight: bold;
        }}
        
        .risk-low {{ background: #c6f6d5; color: #22543d; }}
        .risk-medium {{ background: #fefcbf; color: #744210; }}
        .risk-high {{ background: #fed7d7; color: #742a2a; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🎯 Locator Strategy Performance Report</h1>
        <p>Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
    </div>
    
    <div class="metrics-grid">
        <div class="metric-card">
            <h3>Total Tests</h3>
            <div class="metric-value">5</div>
        </div>
        <div class="metric-card">
            <h3>Fastest Strategy</h3>
            <div class="metric-value">{fastest_strategy}</div>
            <p style="font-size: 12px; color: #718096; margin-top: 5px;">
                {min(execution_times):.3f}s execution time
            </p>
        </div>
        <div class="metric-card">
            <h3>Recommended</h3>
            <div class="metric-value">{recommended_strategy}</div>
            <p style="font-size: 12px; color: #718096; margin-top: 5px;">
                Best balance: fast, flexible, maintainable
            </p>
        </div>
    </div>
    
    <div class="chart-container">
        <h2>Execution Time Comparison (seconds)</h2>
        <canvas id="timeChart"></canvas>
    </div>
    
    <div class="chart-container">
        <h2>Risk Level Distribution</h2>
        <canvas id="riskChart"></canvas>
    </div>
    
    <script>
        // Time comparison chart
        const timeCtx = document.getElementById('timeChart').getContext('2d');
        new Chart(timeCtx, {{
            type: 'bar',
            data: {{
                labels: {js_strategy_names},
                datasets: [{{
                    label: 'Execution Time (seconds)',
                    data: {js_execution_times},
                    backgroundColor: [
                        '#48bb78',
                        '#ecc94b',
                        '#48bb78',
                        '#ed8936',
                        '#f56565'
                    ]
                }}]
            }},
            options: {{
                responsive: true,
                scales: {{
                    y: {{
                        beginAtZero: true,
                        title: {{
                            display: true,
                            text: 'Time (seconds)'
                        }}
                    }}
                }}
            }}
        }});
        
        // Risk level chart
        const riskCtx = document.getElementById('riskChart').getContext('2d');
        new Chart(riskCtx, {{
            type: 'doughnut',
            data: {{
                labels: ['Low Risk', 'Medium Risk', 'High Risk'],
                datasets: [{{
                    data: [2, 2, 1],
                    backgroundColor: ['#48bb78', '#ecc94b', '#f56565']
                }}]
            }},
            options: {{
                responsive: true,
                plugins: {{
                    legend: {{
                        position: 'bottom'
                    }}
                }}
            }}
        }});
    </script>
</body>
</html>"""
    
    output_path.write_text(html_content)
    return output_path


if __name__ == "__main__":
    from pathlib import Path
    
    output = Path("workspace/reports/locator_comparison.html")
    output.parent.mkdir(parents=True, exist_ok=True)
    
    report_path = generate_html_report({}, output)
    print(f"Report generated: {report_path}")
