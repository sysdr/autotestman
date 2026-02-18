"""Utility for generating and managing Allure reports"""
from pathlib import Path
import subprocess
import webbrowser
from typing import Optional
import shutil


class AllureReportManager:
    """Manages Allure report generation and viewing"""
    
    def __init__(self, results_dir: str = "allure-results", 
                 report_dir: str = "allure-report"):
        self.results_dir = Path(results_dir)
        self.report_dir = Path(report_dir)
    
    def check_allure_installed(self) -> bool:
        """Check if Allure CLI is installed"""
        try:
            result = subprocess.run(
                ["allure", "--version"],
                capture_output=True,
                text=True
            )
            return result.returncode == 0
        except FileNotFoundError:
            return False
    
    def generate_report(self, clean: bool = True) -> bool:
        """Generate HTML report from JSON results"""
        if not self.check_allure_installed():
            print("❌ Allure CLI not installed. Install: brew install allure (macOS)")
            return False
        
        cmd = ["allure", "generate", str(self.results_dir), 
               "-o", str(self.report_dir)]
        if clean:
            cmd.append("--clean")
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode == 0:
                print(f"✓ Report generated: {self.report_dir / 'index.html'}")
                return True
            else:
                print(f"❌ Report generation failed: {result.stderr}")
                return False
        except Exception as e:
            print(f"❌ Error: {e}")
            return False
    
    def serve_report(self, port: int = 8080) -> None:
        """Start local server to view report"""
        if not self.check_allure_installed():
            print("❌ Allure CLI not installed")
            return
        
        try:
            subprocess.run(
                ["allure", "serve", str(self.results_dir), "-p", str(port)],
                check=True
            )
        except KeyboardInterrupt:
            print("\nServer stopped")
    
    def open_report(self) -> None:
        """Open generated report in browser"""
        index_file = self.report_dir / "index.html"
        if index_file.exists():
            webbrowser.open(f"file://{index_file.absolute()}")
        else:
            print("❌ Report not found. Run generate_report() first.")
    
    def clear_results(self) -> None:
        """Clear previous test results"""
        if self.results_dir.exists():
            shutil.rmtree(self.results_dir)
            self.results_dir.mkdir()
            print(f"✓ Cleared {self.results_dir}")
    
    def get_summary(self) -> dict:
        """Extract summary from generated report"""
        summary_file = self.report_dir / "widgets" / "summary.json"
        if summary_file.exists():
            import json
            with open(summary_file) as f:
                return json.load(f)
        return {}
