# Lesson 33: Playwright Tracing & Time Travel

## Quick Start

### 1. Install Dependencies
```bash
pip install pytest-playwright --break-system-packages
playwright install chromium
```

### 2. Run Tests
```bash
# Run all tests with verbose output
pytest tests/ -v

# Run specific test
pytest tests/test_tracing_demo.py::TestTracingDemo::test_failing_element_search -v

# Run with HTML report
pytest tests/ -v --html=reports/report.html --self-contained-html
```

### 3. View Traces

After tests run, failed tests will generate trace files in `traces/` directory.

```bash
# View a trace (replace with your trace filename or use glob for latest)
playwright show-trace traces/*.zip

# Or view a specific trace
playwright show-trace traces/test_failing_element_search_20260214_143022.zip

# View latest trace (Linux/Mac)
playwright show-trace $(ls -t traces/*.zip | head -1)
```

## Understanding Tracing

### What Gets Captured

- **Screenshots**: Visual state at each action
- **DOM Snapshots**: Complete HTML structure for time-travel inspection
- **Network Activity**: All HTTP requests with timing and payloads
- **Console Logs**: JavaScript errors and console output
- **Source Code**: Which test lines triggered which actions

### Trace Fixtures

**`traced_context`** (Smart Tracing)
- Only saves traces on test failure
- Optimizes storage for CI/CD
- Production-ready pattern

**`always_traced_context`** (Debug Mode)
- Saves every trace regardless of result
- Useful for inspecting passing tests
- Use when debugging complex interactions

## Project Structure

```
lesson_33_tracing/
├── tests/
│   ├── conftest.py              # Tracing fixtures
│   └── test_tracing_demo.py     # Example tests
├── traces/                      # Generated trace files (gitignored)
├── reports/                     # HTML reports
└── README.md
```

## Production Patterns

### CI/CD Integration

```yaml
# .github/workflows/tests.yml
- name: Run tests with tracing
  run: pytest tests/ -v

- name: Upload traces on failure
  if: failure()
  uses: actions/upload-artifact@v3
  with:
    name: playwright-traces
    path: traces/
    retention-days: 7
```

### Trace Retention Policy

- Keep traces for 7 days maximum
- Auto-delete old traces in CI
- Monitor trace storage size (< 5MB per trace)

## Time-Travel Debugging Workflow

1. **Test fails in CI**
2. **Download trace artifact** from pipeline
3. **Open in trace viewer**: `playwright show-trace trace.zip`
4. **Scrub timeline** to failure point
5. **Inspect**:
   - DOM structure at that moment
   - Network requests in-flight
   - Console errors
   - Which test line executed
6. **Fix root cause** with complete context
7. **Commit fix** with confidence

## Key Takeaways

✅ Tracing eliminates "works on my machine" debugging
✅ Time-travel inspection beats print statements
✅ Conditional saving optimizes storage
✅ Complete context enables 6x faster debugging

## Next Steps

- Integrate traces with CI artifact storage
- Add trace size monitoring
- Implement automated trace cleanup
- Configure parallel test execution with tracing
