"""
Utility functions for test suite
"""
from pathlib import Path
from datetime import datetime
from typing import Dict, Any
import json


class TestReporter:
    """Generate test execution reports"""
    
    def __init__(self, output_dir: Path = Path("reports")):
        self.output_dir = output_dir
        self.output_dir.mkdir(exist_ok=True)
        self.results: list[Dict[str, Any]] = []
    
    def add_result(self, test_name: str, status: str, duration: float, error: str = ""):
        """Add a test result"""
        self.results.append({
            "test": test_name,
            "status": status,
            "duration": duration,
            "error": error,
            "timestamp": datetime.now().isoformat()
        })
    
    def generate_report(self) -> Path:
        """Generate JSON report"""
        report_file = self.output_dir / f"test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        summary = {
            "total": len(self.results),
            "passed": sum(1 for r in self.results if r["status"] == "passed"),
            "failed": sum(1 for r in self.results if r["status"] == "failed"),
            "total_duration": sum(r["duration"] for r in self.results),
            "results": self.results
        }
        
        report_file.write_text(json.dumps(summary, indent=2))
        return report_file


def calculate_flakiness_rate(test_runs: list[bool]) -> float:
    """Calculate flakiness rate from test run results"""
    if not test_runs:
        return 0.0
    
    pass_count = sum(test_runs)
    total_runs = len(test_runs)
    pass_rate = pass_count / total_runs
    
    # Flakiness is when neither 100% pass nor 100% fail
    if pass_rate == 1.0 or pass_rate == 0.0:
        return 0.0
    
    return 1.0 - abs(2 * pass_rate - 1)  # Returns 0 at extremes, 1 at 50%


def format_duration(seconds: float) -> str:
    """Format duration in human-readable format"""
    if seconds < 1:
        return f"{seconds * 1000:.0f}ms"
    elif seconds < 60:
        return f"{seconds:.2f}s"
    else:
        minutes = int(seconds // 60)
        secs = seconds % 60
        return f"{minutes}m {secs:.1f}s"
