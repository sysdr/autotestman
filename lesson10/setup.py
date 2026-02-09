# setup_lesson.py
"""
Lesson 10: Data Validator - Workspace Setup
Creates a production-grade CSV validation system with sample data and HTML reporting.
"""

from pathlib import Path
from dataclasses import dataclass
from enum import Enum
from typing import List
import csv
import html

# ============================================================================
# CONFIGURATION
# ============================================================================

WORKSPACE_DIR = Path("lesson_10_data_validator")
SAMPLE_DATA_DIR = WORKSPACE_DIR / "sample_data"


# ============================================================================
# DATA MODELS
# ============================================================================

class ValidationStatus(Enum):
    """Validation result status codes"""
    VALID = "valid"
    INVALID = "invalid"
    ERROR = "error"


@dataclass
class ValidationResult:
    """Captures the outcome of validating a single CSV file"""
    file_path: Path
    status: ValidationStatus
    total_rows: int = 0
    row_number: int = 0
    column_name: str = ""
    message: str = ""
    
    def is_valid(self) -> bool:
        return self.status == ValidationStatus.VALID


# ============================================================================
# CORE VALIDATOR
# ============================================================================

class CSVEmailValidator:
    """
    Validates that all email fields in a CSV file are non-empty.
    
    Production-grade implementation:
    - Uses DictReader for column name safety
    - Handles encoding issues gracefully
    - Provides detailed error context
    """
    
    def __init__(self, email_column: str = "email"):
        self.email_column = email_column
    
    def validate_file(self, file_path: Path) -> ValidationResult:
        """
        Validate a single CSV file for empty email fields.
        
        Args:
            file_path: Path to CSV file
            
        Returns:
            ValidationResult with detailed status and context
        """
        if not file_path.exists():
            return ValidationResult(
                file_path=file_path,
                status=ValidationStatus.ERROR,
                message=f"File not found: {file_path}"
            )
        
        try:
            with open(file_path, 'r', encoding='utf-8', newline='') as f:
                reader = csv.DictReader(f)
                
                # Validate header contains email column
                if reader.fieldnames is None or self.email_column not in reader.fieldnames:
                    return ValidationResult(
                        file_path=file_path,
                        status=ValidationStatus.ERROR,
                        message=f"CSV missing '{self.email_column}' column. Found: {reader.fieldnames}"
                    )
                
                # Validate each row
                total_rows = 0
                for row_num, row in enumerate(reader, start=2):  # start=2 accounts for header row
                    total_rows += 1
                    email_value = row.get(self.email_column, "")
                    
                    # Check for empty or whitespace-only email
                    if not email_value or not email_value.strip():
                        return ValidationResult(
                            file_path=file_path,
                            status=ValidationStatus.INVALID,
                            total_rows=total_rows,
                            row_number=row_num,
                            column_name=self.email_column,
                            message=f"Empty email field at row {row_num}"
                        )
                
                # All rows valid
                return ValidationResult(
                    file_path=file_path,
                    status=ValidationStatus.VALID,
                    total_rows=total_rows,
                    message=f"All {total_rows} rows validated successfully"
                )
                
        except UnicodeDecodeError as e:
            return ValidationResult(
                file_path=file_path,
                status=ValidationStatus.ERROR,
                message=f"Encoding error: {str(e)}"
            )
        except csv.Error as e:
            return ValidationResult(
                file_path=file_path,
                status=ValidationStatus.ERROR,
                message=f"CSV parsing error: {str(e)}"
            )
        except Exception as e:
            return ValidationResult(
                file_path=file_path,
                status=ValidationStatus.ERROR,
                message=f"Unexpected error: {str(e)}"
            )


# ============================================================================
# DIRECTORY SCANNER
# ============================================================================

class DirectoryScanner:
    """
    Scans a directory for CSV files and validates them.
    
    Uses generator pattern to handle large directories efficiently.
    """
    
    def __init__(self, validator: CSVEmailValidator):
        self.validator = validator
    
    def scan(self, directory: Path) -> List[ValidationResult]:
        """
        Scan directory for CSV files and validate each one.
        
        Args:
            directory: Path to directory containing CSV files
            
        Returns:
            List of ValidationResult objects
        """
        if not directory.exists():
            return [ValidationResult(
                file_path=directory,
                status=ValidationStatus.ERROR,
                message=f"Directory not found: {directory}"
            )]
        
        results = []
        csv_files = sorted(directory.glob("*.csv"))
        
        if not csv_files:
            return [ValidationResult(
                file_path=directory,
                status=ValidationStatus.ERROR,
                message="No CSV files found in directory"
            )]
        
        for csv_file in csv_files:
            result = self.validator.validate_file(csv_file)
            results.append(result)
        
        return results


# ============================================================================
# REPORTING
# ============================================================================

class ConsoleReporter:
    """Colored console output for immediate feedback"""
    
    # ANSI color codes
    GREEN = "\033[92m"
    RED = "\033[91m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    RESET = "\033[0m"
    BOLD = "\033[1m"
    
    @classmethod
    def report(cls, results: List[ValidationResult]) -> None:
        """Print colored validation results to console"""
        print(f"\n{cls.BOLD}{cls.BLUE}{'='*70}{cls.RESET}")
        print(f"{cls.BOLD}CSV Email Validation Report{cls.RESET}")
        print(f"{cls.BLUE}{'='*70}{cls.RESET}\n")
        
        valid_count = sum(1 for r in results if r.status == ValidationStatus.VALID)
        invalid_count = sum(1 for r in results if r.status == ValidationStatus.INVALID)
        error_count = sum(1 for r in results if r.status == ValidationStatus.ERROR)
        
        for result in results:
            status_color = {
                ValidationStatus.VALID: cls.GREEN,
                ValidationStatus.INVALID: cls.RED,
                ValidationStatus.ERROR: cls.YELLOW
            }[result.status]
            
            status_icon = {
                ValidationStatus.VALID: "✓",
                ValidationStatus.INVALID: "✗",
                ValidationStatus.ERROR: "!"
            }[result.status]
            
            print(f"{status_color}{status_icon} {result.file_path.name}{cls.RESET}")
            print(f"  Status: {status_color}{result.status.value.upper()}{cls.RESET}")
            print(f"  Message: {result.message}")
            if result.total_rows > 0:
                print(f"  Rows processed: {result.total_rows}")
            print()
        
        print(f"{cls.BOLD}Summary:{cls.RESET}")
        print(f"  {cls.GREEN}Valid: {valid_count}{cls.RESET}")
        print(f"  {cls.RED}Invalid: {invalid_count}{cls.RESET}")
        print(f"  {cls.YELLOW}Errors: {error_count}{cls.RESET}")
        print(f"{cls.BLUE}{'='*70}{cls.RESET}\n")


class HTMLReporter:
    """Generate HTML report for CI/CD artifact archiving"""
    
    @staticmethod
    def generate(results: List[ValidationResult], output_path: Path) -> None:
        """Generate styled HTML report"""
        valid_count = sum(1 for r in results if r.status == ValidationStatus.VALID)
        invalid_count = sum(1 for r in results if r.status == ValidationStatus.INVALID)
        error_count = sum(1 for r in results if r.status == ValidationStatus.ERROR)
        
        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CSV Validation Report</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif;
            max-width: 1200px;
            margin: 40px auto;
            padding: 20px;
            background: #f5f5f5;
        }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 10px;
            margin-bottom: 30px;
        }}
        .header h1 {{
            margin: 0 0 10px 0;
        }}
        .summary {{
            display: flex;
            gap: 20px;
            margin-bottom: 30px;
        }}
        .summary-card {{
            flex: 1;
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .summary-card h3 {{
            margin: 0 0 10px 0;
            font-size: 14px;
            text-transform: uppercase;
            color: #666;
        }}
        .summary-card .number {{
            font-size: 36px;
            font-weight: bold;
        }}
        .valid .number {{ color: #10b981; }}
        .invalid .number {{ color: #ef4444; }}
        .error .number {{ color: #f59e0b; }}
        .results {{
            background: white;
            border-radius: 8px;
            padding: 20px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .result-item {{
            border-left: 4px solid #e5e7eb;
            padding: 15px;
            margin-bottom: 15px;
            background: #f9fafb;
            border-radius: 4px;
        }}
        .result-item.valid {{ border-left-color: #10b981; }}
        .result-item.invalid {{ border-left-color: #ef4444; }}
        .result-item.error {{ border-left-color: #f59e0b; }}
        .result-item h4 {{
            margin: 0 0 10px 0;
            display: flex;
            align-items: center;
            gap: 10px;
        }}
        .badge {{
            display: inline-block;
            padding: 4px 12px;
            border-radius: 12px;
            font-size: 12px;
            font-weight: bold;
            text-transform: uppercase;
        }}
        .badge.valid {{ background: #d1fae5; color: #065f46; }}
        .badge.invalid {{ background: #fee2e2; color: #991b1b; }}
        .badge.error {{ background: #fef3c7; color: #92400e; }}
        .details {{
            font-size: 14px;
            color: #666;
            margin-top: 8px;
        }}
        .details div {{
            margin: 4px 0;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>CSV Email Validation Report</h1>
        <p>Automated validation results for CSV data integrity</p>
    </div>
    
    <div class="summary">
        <div class="summary-card valid">
            <h3>Valid Files</h3>
            <div class="number">{valid_count}</div>
        </div>
        <div class="summary-card invalid">
            <h3>Invalid Files</h3>
            <div class="number">{invalid_count}</div>
        </div>
        <div class="summary-card error">
            <h3>Errors</h3>
            <div class="number">{error_count}</div>
        </div>
    </div>
    
    <div class="results">
        <h2>Detailed Results</h2>
"""
        
        for result in results:
            status_class = result.status.value
            html_content += f"""
        <div class="result-item {status_class}">
            <h4>
                {html.escape(result.file_path.name)}
                <span class="badge {status_class}">{result.status.value}</span>
            </h4>
            <div class="details">
                <div><strong>Message:</strong> {html.escape(result.message)}</div>
"""
            if result.total_rows > 0:
                html_content += f"                <div><strong>Rows Processed:</strong> {result.total_rows}</div>\n"
            if result.row_number > 0:
                html_content += f"                <div><strong>Failed at Row:</strong> {result.row_number}</div>\n"
            
            html_content += """            </div>
        </div>
"""
        
        html_content += """    </div>
</body>
</html>"""
        
        output_path.write_text(html_content, encoding='utf-8')
        print(f"HTML report generated: {output_path}")


# ============================================================================
# SAMPLE DATA GENERATOR
# ============================================================================

def create_sample_data(data_dir: Path) -> None:
    """Generate sample CSV files with valid and invalid data"""
    data_dir.mkdir(parents=True, exist_ok=True)
    
    # Valid file 1: Customer data
    (data_dir / "customers_valid.csv").write_text("""name,email,age,city
Alice Johnson,alice@example.com,28,New York
Bob Smith,bob.smith@example.com,34,Los Angeles
Carol White,carol.white@example.com,45,Chicago
David Brown,david.brown@example.com,29,Houston
""", encoding='utf-8')
    
    # Valid file 2: Employee data
    (data_dir / "employees_valid.csv").write_text("""employee_id,name,email,department
E001,John Doe,john.doe@company.com,Engineering
E002,Jane Smith,jane.smith@company.com,Marketing
E003,Mike Johnson,mike.johnson@company.com,Sales
""", encoding='utf-8')
    
    # Invalid file 1: Empty email in middle
    (data_dir / "customers_invalid_1.csv").write_text("""name,email,age,city
Alice Johnson,alice@example.com,28,New York
Bob Smith,,34,Los Angeles
Carol White,carol.white@example.com,45,Chicago
""", encoding='utf-8')
    
    # Invalid file 2: Whitespace-only email
    (data_dir / "customers_invalid_2.csv").write_text("""name,email,age,city
Alice Johnson,alice@example.com,28,New York
Bob Smith,   ,34,Los Angeles
Carol White,carol.white@example.com,45,Chicago
""", encoding='utf-8')
    
    # Invalid file 3: Empty email at end
    (data_dir / "employees_invalid.csv").write_text("""employee_id,name,email,department
E001,John Doe,john.doe@company.com,Engineering
E002,Jane Smith,jane.smith@company.com,Marketing
E003,Mike Johnson,,Sales
""", encoding='utf-8')
    
    print(f"✓ Generated sample CSV files in {data_dir}")


# ============================================================================
# MAIN VALIDATOR SCRIPT
# ============================================================================

def create_validator_script(workspace_dir: Path) -> None:
    """Create the main data_validator.py script"""
    script_content = '''"""
Data Validator - Production-Ready CSV Email Validation
Usage: python data_validator.py
"""

from pathlib import Path
import sys

# Import from the setup script (in production, these would be separate modules)
from setup_lesson import (
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
'''
    
    (workspace_dir / "data_validator.py").write_text(script_content, encoding='utf-8')
    print(f"✓ Created data_validator.py")


# ============================================================================
# WORKSPACE SETUP
# ============================================================================

def setup_workspace():
    """Create the complete lesson workspace"""
    print("\n" + "="*70)
    print("Setting up Lesson 10: Data Validator")
    print("="*70 + "\n")
    
    # Create workspace structure
    WORKSPACE_DIR.mkdir(exist_ok=True)
    print(f"✓ Created workspace: {WORKSPACE_DIR}")
    
    # Generate sample data
    create_sample_data(SAMPLE_DATA_DIR)
    
    # Create validator script
    create_validator_script(WORKSPACE_DIR)
    
    # Create README
    readme_content = """# Lesson 10: Data Validator

## Overview
Production-grade CSV email validation system demonstrating:
- Path abstraction with pathlib
- Result objects with dataclasses
- Structured logging for CI/CD
- HTML report generation

## Quick Start
```bash
# Run the validator
python data_validator.py

# View HTML report
open validation_report.html  # macOS
xdg-open validation_report.html  # Linux
start validation_report.html  # Windows
```

## Architecture
- `CSVEmailValidator`: Core validation logic
- `DirectoryScanner`: File discovery and orchestration
- `ConsoleReporter`: Colored CLI output
- `HTMLReporter`: CI/CD artifact generation

## Success Criteria
✓ All empty email fields detected
✓ Exact row numbers reported
✓ HTML report generated
✓ Cross-platform compatibility
"""
    
    (WORKSPACE_DIR / "README.md").write_text(readme_content, encoding='utf-8')
    print(f"✓ Created README.md")
    
    print("\n" + "="*70)
    print("✓ Workspace setup complete!")
    print("="*70)
    print(f"\nNext steps:")
    print(f"1. cd {WORKSPACE_DIR}")
    print(f"2. python data_validator.py")
    print(f"3. open validation_report.html\n")


# ============================================================================
# RUN TEST & VERIFICATION
# ============================================================================

def run_test():
    """Execute the validator and verify results"""
    print("\n" + "="*70)
    print("Running Test Validation")
    print("="*70 + "\n")
    
    validator = CSVEmailValidator()
    scanner = DirectoryScanner(validator)
    results = scanner.scan(SAMPLE_DATA_DIR)
    
    ConsoleReporter.report(results)
    HTMLReporter.generate(results, WORKSPACE_DIR / "validation_report.html")
    
    return results


def verify_result(results: List[ValidationResult]) -> bool:
    """Verify that the validation produced expected results"""
    print("\n" + "="*70)
    print("Verification Report")
    print("="*70 + "\n")
    
    checks = []
    
    # Check 1: Should have 5 files total
    check_1 = len(results) == 5
    checks.append(("5 CSV files processed", check_1))
    
    # Check 2: Should have exactly 2 valid files
    valid_count = sum(1 for r in results if r.status == ValidationStatus.VALID)
    check_2 = valid_count == 2
    checks.append(("2 valid files detected", check_2))
    
    # Check 3: Should have exactly 3 invalid files
    invalid_count = sum(1 for r in results if r.status == ValidationStatus.INVALID)
    check_3 = invalid_count == 3
    checks.append(("3 invalid files detected", check_3))
    
    # Check 4: Invalid files should have row numbers
    invalid_results = [r for r in results if r.status == ValidationStatus.INVALID]
    check_4 = all(r.row_number > 0 for r in invalid_results)
    checks.append(("Row numbers captured for failures", check_4))
    
    # Check 5: HTML report should exist
    check_5 = (WORKSPACE_DIR / "validation_report.html").exists()
    checks.append(("HTML report generated", check_5))
    
    # Print results
    all_passed = all(passed for _, passed in checks)
    
    for check_name, passed in checks:
        status = "✓" if passed else "✗"
        color = ConsoleReporter.GREEN if passed else ConsoleReporter.RED
        print(f"{color}{status} {check_name}{ConsoleReporter.RESET}")
    
    print(f"\n{'='*70}")
    if all_passed:
        print(f"{ConsoleReporter.GREEN}✓ All verification checks passed!{ConsoleReporter.RESET}")
    else:
        print(f"{ConsoleReporter.RED}✗ Some checks failed{ConsoleReporter.RESET}")
    print(f"{'='*70}\n")
    
    return all_passed


# ============================================================================
# ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    # Setup workspace
    setup_workspace()
    
    # Run tests
    results = run_test()
    
    # Verify results
    verify_result(results)