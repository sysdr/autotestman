#!/usr/bin/env python3
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
    print("\n" + "="*60)
    print("[UQAP] Automation Environment Validation")
    print("="*60 + "\n")
    
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
    
    print("\n" + "="*60)
    print("[UQAP] Environment Validated Successfully ✓")
    print("="*60 + "\n")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
