"""
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
