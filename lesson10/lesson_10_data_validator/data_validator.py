"""
Data Validator - Production-Ready CSV Email Validation
Usage: python data_validator.py
"""

from pathlib import Path
import sys

# Add parent directory to path to import from setup.py
sys.path.insert(0, str(Path(__file__).parent.parent))

# Import from the setup script (in production, these would be separate modules)
from setup import (
    CSVEmailValidator,
    DirectoryScanner,
    ConsoleReporter,
    HTMLReporter
)


def main():
    """Main entry point for the data validator"""
    # Configuration
    data_directory = Path("sample_data")
    report_path = Path("validation_report.html")
    
    # Initialize validator and scanner
    validator = CSVEmailValidator(email_column="email")
    scanner = DirectoryScanner(validator)
    
    # Run validation
    print("Starting CSV validation...")
    results = scanner.scan(data_directory)
    
    # Generate reports
    ConsoleReporter.report(results)
    HTMLReporter.generate(results, report_path)
    
    # Exit with appropriate code for CI/CD
    has_failures = any(r.status.value in ['invalid', 'error'] for r in results)
    sys.exit(1 if has_failures else 0)


if __name__ == "__main__":
    main()
