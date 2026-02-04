#!/usr/bin/env python3
"""
UQAP Lesson 1 Setup Script
Creates a production-grade Python automation project structure.

Run: python setup_lesson.py
"""

import subprocess
import sys
import shutil
from pathlib import Path
from typing import NamedTuple
from dataclasses import dataclass
from enum import Enum


class Color(str, Enum):
    """ANSI color codes for terminal output"""
    GREEN = '\033[92m'
    BLUE = '\033[94m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    RESET = '\033[0m'
    BOLD = '\033[1m'


@dataclass
class SetupResult:
    """Results from environment setup"""
    success: bool
    message: str
    details: dict[str, any] = None


class FileTemplate(NamedTuple):
    """Template for generating project files"""
    path: str
    content: str


def print_colored(message: str, color: Color = Color.RESET, bold: bool = False) -> None:
    """Print colored output to terminal"""
    style = f"{Color.BOLD.value}{color.value}" if bold else color.value
    print(f"{style}{message}{Color.RESET.value}")


def validate_prerequisites() -> SetupResult:
    """Validate Python version and required tools"""
    print_colored("\n🔍 Validating Prerequisites...", Color.BLUE, bold=True)
    
    # Check Python version
    if sys.version_info < (3, 11):
        return SetupResult(
            success=False,
            message=f"Python 3.11+ required. Found: {sys.version}",
            details={"python_version": f"{sys.version_info.major}.{sys.version_info.minor}"}
        )
    
    print_colored(f"  ✓ Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}", Color.GREEN)
    
    # Check Git
    try:
        result = subprocess.run(
            ["git", "--version"], 
            capture_output=True, 
            text=True, 
            check=True
        )
        git_version = result.stdout.strip()
        print_colored(f"  ✓ {git_version}", Color.GREEN)
    except (subprocess.CalledProcessError, FileNotFoundError):
        return SetupResult(
            success=False,
            message="Git not found. Install from https://git-scm.com",
            details={"git_installed": False}
        )
    
    return SetupResult(success=True, message="Prerequisites validated")


def create_project_structure() -> Path:
    """Create the UQAP project directory structure"""
    print_colored("\n📁 Creating Project Structure...", Color.BLUE, bold=True)
    
    project_root = Path.cwd() / "uqap-lesson-01"
    
    # Define directory structure
    directories = [
        project_root / "src" / "automation",
        project_root / "tests",
        project_root / "docs",
    ]
    
    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)
        print_colored(f"  ✓ Created {directory.relative_to(Path.cwd())}", Color.GREEN)
    
    return project_root


def generate_project_files(project_root: Path) -> None:
    """Generate all necessary project files"""
    print_colored("\n📝 Generating Project Files...", Color.BLUE, bold=True)
    
    templates = [
        FileTemplate(
            path="pyproject.toml",
            content="""[build-system]
requires = ["setuptools>=68.0", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "uqap-automation"
version = "0.1.0"
description = "Unified Quality Assurance Platform - Lesson 1"
requires-python = ">=3.11"
dependencies = [
    "selenium>=4.15.0,<5.0.0",
    "pytest>=7.4.0,<8.0.0",
    "pytest-html>=4.1.0,<5.0.0",
]

[project.optional-dependencies]
dev = [
    "black>=23.0.0",
    "ruff>=0.1.0",
]

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_functions = ["test_*"]
addopts = "-v --tb=short"

[tool.ruff]
line-length = 100
target-version = "py311"
"""
        ),
        FileTemplate(
            path=".gitignore",
            content="""# Virtual Environment
.venv/
venv/
env/

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python

# Testing
.pytest_cache/
.coverage
htmlcov/
*.log

# IDEs
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Build
dist/
build/
*.egg-info/
"""
        ),
        FileTemplate(
            path="src/automation/__init__.py",
            content='"""UQAP Automation Package"""\n\n__version__ = "0.1.0"\n'
        ),
        FileTemplate(
            path="src/automation/hello.py",
            content='''#!/usr/bin/env python3
"""
Hello Automation Script
Validates the UQAP development environment.
"""

import sys
from pathlib import Path
from typing import NamedTuple


class EnvironmentInfo(NamedTuple):
    """Environment validation result"""
    python_version: str
    working_dir: Path
    venv_active: bool


def check_virtual_environment() -> bool:
    """Verify virtual environment is active"""
    return (
        hasattr(sys, 'real_prefix') or
        (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)
    )


def get_environment_info() -> EnvironmentInfo:
    """Gather environment information"""
    return EnvironmentInfo(
        python_version=f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
        working_dir=Path.cwd(),
        venv_active=check_virtual_environment()
    )


def main() -> int:
    """Main execution function"""
    print("\\n" + "="*60)
    print("[UQAP] Automation Environment Validation")
    print("="*60 + "\\n")
    
    env = get_environment_info()
    
    print(f"Python Version: {env.python_version}")
    print(f"Working Directory: {env.working_dir}")
    print(f"Virtual Environment: {'✓ Active' if env.venv_active else '✗ Not Active'}")
    
    try:
        import selenium
        print(f"Selenium Version: {selenium.__version__}")
    except ImportError:
        print("Selenium: ✗ Not Installed")
        return 1
    
    try:
        import pytest
        print(f"Pytest Version: {pytest.__version__}")
    except ImportError:
        print("Pytest: ✗ Not Installed")
        return 1
    
    print("\\n" + "="*60)
    print("[UQAP] Environment Validated Successfully ✓")
    print("="*60 + "\\n")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
'''
        ),
        FileTemplate(
            path="tests/__init__.py",
            content='"""UQAP Test Suite"""\n'
        ),
        FileTemplate(
            path="tests/test_hello.py",
            content='''"""
Tests for hello.py automation script
"""

import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from automation.hello import (
    check_virtual_environment,
    get_environment_info,
    EnvironmentInfo
)


def test_environment_info_structure():
    """Verify EnvironmentInfo has correct fields"""
    env = get_environment_info()
    
    assert isinstance(env, EnvironmentInfo)
    assert isinstance(env.python_version, str)
    assert isinstance(env.working_dir, Path)
    assert isinstance(env.venv_active, bool)


def test_python_version_format():
    """Verify Python version string is formatted correctly"""
    env = get_environment_info()
    
    # Should be in format "3.11.x"
    parts = env.python_version.split(".")
    assert len(parts) == 3
    assert parts[0].isdigit()
    assert parts[1].isdigit()
    assert parts[2].isdigit()


def test_virtual_environment_detection():
    """Test virtual environment detection logic"""
    is_venv = check_virtual_environment()
    
    # This should be True if running in venv, False otherwise
    assert isinstance(is_venv, bool)
    
    # If we're in a venv, verify sys attributes
    if is_venv:
        assert (
            hasattr(sys, 'real_prefix') or
            (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)
        )


def test_working_directory_exists():
    """Verify working directory is a valid path"""
    env = get_environment_info()
    
    assert env.working_dir.exists()
    assert env.working_dir.is_dir()


def test_selenium_import():
    """Verify Selenium is installed"""
    try:
        import selenium
        assert hasattr(selenium, '__version__')
    except ImportError:
        assert False, "Selenium not installed in environment"


def test_pytest_import():
    """Verify Pytest is installed"""
    try:
        import pytest
        assert hasattr(pytest, '__version__')
    except ImportError:
        assert False, "Pytest not installed in environment"
'''
        ),
        FileTemplate(
            path="README.md",
            content="""# UQAP Lesson 1: Environment Setup

## Overview
This project demonstrates production-grade Python test automation environment setup.

## Quick Start

### 1. Create Virtual Environment
```bash
python -m venv .venv
```

### 2. Activate Virtual Environment
**macOS/Linux:**
```bash
source .venv/bin/activate
```

**Windows (Command Prompt):**
```bash
.venv\\Scripts\\activate.bat
```

**Windows (PowerShell):**
```bash
.venv\\Scripts\\Activate.ps1
```

### 3. Install Dependencies
```bash
pip install -e .
```

### 4. Run Hello Automation
```bash
python src/automation/hello.py
```

### 5. Run Tests
```bash
pytest tests/ -v
```

## Project Structure
```
uqap-lesson-01/
├── src/
│   └── automation/
│       ├── __init__.py
│       └── hello.py          # Main automation script
├── tests/
│   ├── __init__.py
│   └── test_hello.py         # Test suite
├── pyproject.toml            # Project dependencies
├── .gitignore
└── README.md
```

## Verification Checklist
- [ ] Python 3.11+ installed
- [ ] Virtual environment created and activated
- [ ] Dependencies installed
- [ ] `hello.py` runs without errors
- [ ] All tests pass

## Next Steps
Lesson 2: File manipulation and CSV parsing for test data management.
"""
        ),
    ]
    
    for template in templates:
        file_path = project_root / template.path
        file_path.write_text(template.content)
        print_colored(f"  ✓ Generated {template.path}", Color.GREEN)


def setup_virtual_environment(project_root: Path) -> SetupResult:
    """Create and configure virtual environment"""
    print_colored("\n🐍 Setting Up Virtual Environment...", Color.BLUE, bold=True)
    
    venv_path = project_root / ".venv"
    
    # Create venv
    try:
        subprocess.run(
            [sys.executable, "-m", "venv", str(venv_path)],
            check=True,
            capture_output=True
        )
        print_colored(f"  ✓ Created virtual environment at {venv_path.name}", Color.GREEN)
    except subprocess.CalledProcessError as e:
        return SetupResult(
            success=False,
            message=f"Failed to create venv: {e.stderr.decode()}",
            details={"venv_created": False}
        )
    
    # Determine pip path
    if sys.platform == "win32":
        pip_path = venv_path / "Scripts" / "pip.exe"
    else:
        pip_path = venv_path / "bin" / "pip"
    
    # Upgrade pip
    try:
        subprocess.run(
            [str(pip_path), "install", "--upgrade", "pip"],
            check=True,
            capture_output=True
        )
        print_colored("  ✓ Upgraded pip", Color.GREEN)
    except subprocess.CalledProcessError:
        print_colored("  ⚠ Warning: Could not upgrade pip", Color.YELLOW)
    
    # Install project in editable mode
    try:
        subprocess.run(
            [str(pip_path), "install", "-e", str(project_root)],
            check=True,
            capture_output=True,
            cwd=str(project_root)
        )
        print_colored("  ✓ Installed project dependencies", Color.GREEN)
    except subprocess.CalledProcessError as e:
        return SetupResult(
            success=False,
            message=f"Failed to install dependencies: {e.stderr.decode()}",
            details={"dependencies_installed": False}
        )
    
    return SetupResult(success=True, message="Virtual environment configured")


def initialize_git(project_root: Path) -> SetupResult:
    """Initialize Git repository"""
    print_colored("\n🔧 Initializing Git Repository...", Color.BLUE, bold=True)
    
    try:
        subprocess.run(
            ["git", "init"],
            cwd=str(project_root),
            check=True,
            capture_output=True
        )
        print_colored("  ✓ Initialized Git repository", Color.GREEN)
        
        subprocess.run(
            ["git", "add", "."],
            cwd=str(project_root),
            check=True,
            capture_output=True
        )
        print_colored("  ✓ Staged files", Color.GREEN)
        
        subprocess.run(
            ["git", "commit", "-m", "Initial commit: UQAP Lesson 1 - Environment Setup"],
            cwd=str(project_root),
            check=True,
            capture_output=True
        )
        print_colored("  ✓ Created initial commit", Color.GREEN)
        
    except subprocess.CalledProcessError as e:
        return SetupResult(
            success=False,
            message=f"Git initialization failed: {e.stderr.decode()}",
            details={"git_initialized": False}
        )
    
    return SetupResult(success=True, message="Git repository initialized")


def run_test(project_root: Path) -> SetupResult:
    """Execute the hello.py script to verify setup"""
    print_colored("\n🧪 Running Environment Validation Test...", Color.BLUE, bold=True)
    
    venv_path = project_root / ".venv"
    
    if sys.platform == "win32":
        python_path = venv_path / "Scripts" / "python.exe"
    else:
        python_path = venv_path / "bin" / "python"
    
    hello_script = project_root / "src" / "automation" / "hello.py"
    
    try:
        result = subprocess.run(
            [str(python_path), str(hello_script)],
            cwd=str(project_root),
            capture_output=True,
            text=True,
            check=True
        )
        
        print_colored(result.stdout, Color.GREEN)
        
        return SetupResult(
            success=True,
            message="Environment validation passed",
            details={"exit_code": result.returncode}
        )
        
    except subprocess.CalledProcessError as e:
        print_colored(e.stdout, Color.RED)
        print_colored(e.stderr, Color.RED)
        return SetupResult(
            success=False,
            message=f"Validation failed with exit code {e.returncode}",
            details={"exit_code": e.returncode, "stderr": e.stderr}
        )


def verify_result(project_root: Path) -> bool:
    """Verify the entire setup was successful"""
    print_colored("\n✅ Verifying Setup...", Color.BLUE, bold=True)
    
    checks = {
        "pyproject.toml exists": (project_root / "pyproject.toml").exists(),
        "Virtual environment exists": (project_root / ".venv").exists(),
        "hello.py exists": (project_root / "src" / "automation" / "hello.py").exists(),
        "tests exist": (project_root / "tests" / "test_hello.py").exists(),
        "Git initialized": (project_root / ".git").exists(),
    }
    
    all_passed = True
    for check_name, passed in checks.items():
        if passed:
            print_colored(f"  ✓ {check_name}", Color.GREEN)
        else:
            print_colored(f"  ✗ {check_name}", Color.RED)
            all_passed = False
    
    return all_passed


def generate_completion_report(project_root: Path) -> None:
    """Generate HTML completion report"""
    html_content = f"""<!DOCTYPE html>
<html>
<head>
    <title>UQAP Lesson 1 - Setup Complete</title>
    <style>
        body {{
            font-family: 'Segoe UI', system-ui, sans-serif;
            max-width: 800px;
            margin: 50px auto;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        }}
        .container {{
            background: white;
            border-radius: 10px;
            padding: 40px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
        }}
        h1 {{
            color: #667eea;
            margin-top: 0;
        }}
        .status {{
            background: #10b981;
            color: white;
            padding: 15px;
            border-radius: 5px;
            font-weight: bold;
            text-align: center;
            font-size: 18px;
        }}
        .next-steps {{
            background: #f3f4f6;
            padding: 20px;
            border-radius: 5px;
            margin-top: 20px;
        }}
        code {{
            background: #1f2937;
            color: #10b981;
            padding: 2px 6px;
            border-radius: 3px;
            font-family: 'Courier New', monospace;
        }}
        .path {{
            color: #6366f1;
            font-weight: bold;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🚀 UQAP Lesson 1 Complete!</h1>
        
        <div class="status">
            ✓ Environment Setup Successful
        </div>
        
        <h2>Project Location</h2>
        <p class="path">{project_root}</p>
        
        <div class="next-steps">
            <h3>Next Steps:</h3>
            <ol>
                <li>Open the project in VS Code: <code>code {project_root.name}</code></li>
                <li>Activate virtual environment:
                    <br><code>source .venv/bin/activate</code> (Mac/Linux)
                    <br><code>.venv\\Scripts\\activate.bat</code> (Windows)
                </li>
                <li>Run tests: <code>pytest tests/ -v</code></li>
                <li>Push to GitHub:
                    <br><code>git remote add origin YOUR_REPO_URL</code>
                    <br><code>git push -u origin main</code>
                </li>
            </ol>
        </div>
        
        <h2>What You Built</h2>
        <ul>
            <li>✓ Isolated Python 3.11+ environment</li>
            <li>✓ Declarative dependency management (pyproject.toml)</li>
            <li>✓ Production-ready project structure</li>
            <li>✓ Automated environment validation</li>
            <li>✓ Git version control</li>
        </ul>
        
        <p style="margin-top: 30px; text-align: center; color: #6b7280;">
            <strong>Ready for Lesson 2:</strong> File Manipulation & CSV Parsing
        </p>
    </div>
</body>
</html>
"""
    
    report_path = project_root / "docs" / "setup_complete.html"
    report_path.write_text(html_content)
    print_colored(f"\n📊 Completion report: {report_path}", Color.BLUE)


def main() -> int:
    """Main setup execution"""
    print_colored("""
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║        UQAP Lesson 1: Environment Setup Automation           ║
║        The Complete Python SDET Bootcamp                     ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
    """, Color.BOLD)
    
    # Step 1: Validate prerequisites
    result = validate_prerequisites()
    if not result.success:
        print_colored(f"\n❌ {result.message}", Color.RED, bold=True)
        return 1
    
    # Step 2: Create project structure
    project_root = create_project_structure()
    
    # Step 3: Generate files
    generate_project_files(project_root)
    
    # Step 4: Setup virtual environment
    result = setup_virtual_environment(project_root)
    if not result.success:
        print_colored(f"\n❌ {result.message}", Color.RED, bold=True)
        return 1
    
    # Step 5: Initialize Git
    result = initialize_git(project_root)
    if not result.success:
        print_colored(f"\n⚠️  {result.message}", Color.YELLOW, bold=True)
        print_colored("  (You can initialize Git manually later)", Color.YELLOW)
    
    # Step 6: Run validation test
    result = run_test(project_root)
    if not result.success:
        print_colored(f"\n❌ {result.message}", Color.RED, bold=True)
        return 1
    
    # Step 7: Verify everything
    if not verify_result(project_root):
        print_colored("\n❌ Setup verification failed", Color.RED, bold=True)
        return 1
    
    # Step 8: Generate completion report
    generate_completion_report(project_root)
    
    print_colored(f"""
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║                   ✓ SETUP COMPLETE!                          ║
║                                                               ║
║  Next: cd {project_root.name:<44} ║
║        source .venv/bin/activate                             ║
║        pytest tests/ -v                                      ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
    """, Color.GREEN, bold=True)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())