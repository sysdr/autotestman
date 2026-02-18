"""
Utility to analyze screenshot metadata and generate a report.
This helps QA engineers quickly review test failures.
"""

from pathlib import Path
from datetime import datetime
import json
from typing import List, Dict


def analyze_screenshots(screenshot_dir: Path = Path("screenshots")) -> Dict:
    """
    Analyze all screenshots and generate metadata report.
    
    Returns:
        Dictionary with screenshot statistics and details
    """
    if not screenshot_dir.exists():
        return {"total": 0, "screenshots": []}
    
    screenshots = []
    for png_file in screenshot_dir.rglob("*.png"):
        file_stat = png_file.stat()
        screenshots.append({
            "filename": png_file.name,
            "path": str(png_file),
            "size_kb": round(file_stat.st_size / 1024, 2),
            "created": datetime.fromtimestamp(file_stat.st_ctime).isoformat(),
            "test_name": png_file.stem.rsplit("_", 3)[0],  # Extract test name before timestamp
        })
    
    return {
        "total": len(screenshots),
        "screenshots": sorted(screenshots, key=lambda x: x["created"], reverse=True),
        "total_size_mb": round(sum(s["size_kb"] for s in screenshots) / 1024, 2),
    }


def generate_html_report(screenshot_dir: Path = Path("screenshots")) -> Path:
    """
    Generate an HTML report of all screenshots.
    Useful for CI/CD artifact viewing.
    """
    data = analyze_screenshots(screenshot_dir)
    
    html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Screenshot Failure Report</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }}
        h1 {{ color: #333; }}
        .summary {{ background: white; padding: 20px; border-radius: 8px; margin-bottom: 20px; }}
        .screenshot {{ background: white; padding: 15px; margin-bottom: 15px; border-radius: 8px; }}
        .screenshot img {{ max-width: 100%; border: 1px solid #ddd; }}
        .metadata {{ color: #666; font-size: 0.9em; margin-top: 10px; }}
    </style>
</head>
<body>
    <h1>Test Failure Screenshot Report</h1>
    <div class="summary">
        <h2>Summary</h2>
        <p><strong>Total Screenshots:</strong> {data['total']}</p>
        <p><strong>Total Size:</strong> {data['total_size_mb']} MB</p>
        <p><strong>Generated:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
    </div>
"""
    
    for screenshot in data['screenshots']:
        html_content += f"""
    <div class="screenshot">
        <h3>{screenshot['test_name']}</h3>
        <img src="{screenshot['path']}" alt="{screenshot['filename']}">
        <div class="metadata">
            <p><strong>Filename:</strong> {screenshot['filename']}</p>
            <p><strong>Size:</strong> {screenshot['size_kb']} KB</p>
            <p><strong>Created:</strong> {screenshot['created']}</p>
        </div>
    </div>
"""
    
    html_content += """
</body>
</html>
"""
    
    report_path = screenshot_dir / "report.html"
    report_path.write_text(html_content)
    return report_path


if __name__ == "__main__":
    report = analyze_screenshots()
    print(json.dumps(report, indent=2))
