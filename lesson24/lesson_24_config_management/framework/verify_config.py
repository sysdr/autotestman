"""
Verification script to ensure configuration management is working correctly.
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from framework.config_manager import ConfigManager


def verify_setup():
    """Run verification checks."""
    print("\n" + "="*60)
    print("CONFIGURATION MANAGEMENT VERIFICATION")
    print("="*60 + "\n")
    
    checks_passed = 0
    checks_total = 5
    
    # Check 1: Config file loads
    try:
        config = ConfigManager()
        print("✓ Check 1: Config file loaded successfully")
        checks_passed += 1
    except Exception as e:
        print(f"✗ Check 1 FAILED: {e}")
        return False
    
    # Check 2: Can read headless mode
    try:
        headless = config.get_headless_mode()
        print(f"✓ Check 2: Headless mode setting = {headless}")
        checks_passed += 1
    except Exception as e:
        print(f"✗ Check 2 FAILED: {e}")
    
    # Check 3: Can read browser type
    try:
        browser = config.get_browser_type()
        print(f"✓ Check 3: Browser type = {browser}")
        checks_passed += 1
    except Exception as e:
        print(f"✗ Check 3 FAILED: {e}")
    
    # Check 4: Singleton pattern works
    try:
        config2 = ConfigManager()
        if config is config2:
            print(f"✓ Check 4: Singleton pattern verified (same instance)")
            checks_passed += 1
        else:
            print("✗ Check 4 FAILED: Multiple instances created")
    except Exception as e:
        print(f"✗ Check 4 FAILED: {e}")
    
    # Check 5: Environment override works
    try:
        import os
        os.environ['HEADLESS'] = 'false'
        config3 = ConfigManager()
        
        # Force reload by creating new instance after env change
        ConfigManager._initialized = False
        ConfigManager._instance = None
        config3 = ConfigManager()
        
        headless_override = config3.get_headless_mode()
        if headless_override == False:
            print(f"✓ Check 5: Environment override working (HEADLESS=false)")
            checks_passed += 1
        else:
            print("✗ Check 5 FAILED: Environment override not applied")
        
        # Cleanup
        del os.environ['HEADLESS']
    except Exception as e:
        print(f"✗ Check 5 FAILED: {e}")
    
    # Summary
    print("\n" + "="*60)
    print(f"VERIFICATION RESULTS: {checks_passed}/{checks_total} checks passed")
    print("="*60 + "\n")
    
    return checks_passed == checks_total


if __name__ == "__main__":
    success = verify_setup()
    sys.exit(0 if success else 1)
