"""
verify_result.py
Static verification — checks the workspace structure and import health
without requiring a live Appium session.
"""
from __future__ import annotations
import sys
import importlib
from pathlib import Path

WORKSPACE = Path(__file__).parent

REQUIRED_FILES = [
    "utils/__init__.py",
    "utils/permission_handler.py",
    "utils/capabilities.py",
    "tests/__init__.py",
    "tests/conftest.py",
    "tests/test_permission_handling.py",
]

class C:
    GREEN = "\033[92m"; RED = "\033[91m"; RESET = "\033[0m"; BOLD = "\033[1m"

def verify_files() -> bool:
    print(f"\n{C.BOLD}-- File Structure Check -----------------------------{C.RESET}")
    all_ok = True
    for rel_path in REQUIRED_FILES:
        full = WORKSPACE / rel_path
        if full.exists():
            print(f"  {C.GREEN}[OK] {rel_path}{C.RESET}")
        else:
            print(f"  {C.RED}[MISSING] {rel_path}{C.RESET}")
            all_ok = False
    return all_ok

def verify_imports() -> bool:
    print(f"\n{C.BOLD}-- Import Health Check ------------------------------{C.RESET}")
    modules_to_check = [
        ("utils.permission_handler", ["PermissionHandler", "PermissionPopupType", "Platform"]),
        ("utils.capabilities",       ["build_android_options", "AndroidCapConfig"]),
    ]
    sys.path.insert(0, str(WORKSPACE))
    all_ok = True
    for mod_name, symbols in modules_to_check:
        try:
            module = importlib.import_module(mod_name)
            for sym in symbols:
                assert hasattr(module, sym), f"Missing symbol: {sym}"
            print(f"  {C.GREEN}[OK] {mod_name}: {', '.join(symbols)}{C.RESET}")
        except Exception as exc:
            print(f"  {C.RED}[FAIL] {mod_name}: {exc}{C.RESET}")
            all_ok = False
    return all_ok

if __name__ == "__main__":
    ok_files   = verify_files()
    ok_imports = verify_imports()
    print()
    if ok_files and ok_imports:
        print(f"{C.GREEN}{C.BOLD}[OK] Workspace verification PASSED - ready to run pytest{C.RESET}")
        sys.exit(0)
    else:
        print(f"{C.RED}{C.BOLD}[FAIL] Verification FAILED - check errors above{C.RESET}")
        sys.exit(1)
