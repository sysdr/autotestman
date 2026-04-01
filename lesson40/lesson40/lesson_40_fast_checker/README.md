# Lesson 40: Fast Checker

## Why `pytest` fails when run directly

If you run **`pytest`** or **`python -m pytest`** from the terminal without using this project’s venv, you may see:

```text
AttributeError: 'FixtureDef' object has no attribute 'unittest'
```

**Reason:** Your shell is using a **different** Python environment (e.g. another `automation-venv` or system pytest) that has:

- **pytest 8.2+** or **pytest 9.x** (which removed `FixtureDef.unittest`)
- **pytest-asyncio 0.21.x** (which still uses that attribute)

So the versions in that environment are incompatible. This project pins **pytest 8.1.2** and **pytest-asyncio 0.23.8** in its own venv to avoid that.

## How to run tests

**Option 1 – Use the script (recommended)**  
This always uses this project’s venv, no matter which env is active:

```bash
./run_tests.sh -v
```

**Option 2 – Activate this project’s venv, then pytest**  
If you activate this project’s venv first, `pytest` will use the right versions:

```bash
source automation-venv/bin/activate
pytest -v
# or: python -m pytest -v
```

If you run `pytest` without activating this project’s venv, you’ll use whatever pytest is on your `PATH` (the other environment) and hit the error above.
