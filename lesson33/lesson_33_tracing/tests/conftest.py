"""
Global pytest configuration with Playwright tracing fixtures.
Implements smart tracing that only saves traces on test failure.
"""

import pytest
from pathlib import Path
from datetime import datetime
from typing import Generator
from playwright.sync_api import Browser, BrowserContext


# Hook to capture test results for conditional trace saving
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Attach test result to request for fixture access"""
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)


@pytest.fixture(scope="function")
def traced_context(browser: Browser, request: pytest.FixtureRequest) -> Generator[BrowserContext, None, None]:
    """
    Browser context with automatic tracing enabled.
    Saves trace only on test failure to optimize storage.
    
    Args:
        browser: Playwright browser instance (from pytest-playwright)
        request: Pytest request object for test metadata
    
    Yields:
        BrowserContext: Context with tracing enabled
    """
    # Create new context and start tracing
    context = browser.new_context(
        viewport={"width": 1920, "height": 1080},
        locale="en-US"
    )
    
    context.tracing.start(
        screenshots=True,   # Capture screenshots at each action
        snapshots=True,     # Record DOM snapshots for time-travel
        sources=True        # Include source code in trace
    )
    
    print(f"\n🎬 Tracing started for: {request.node.name}")
    
    yield context
    
    # Conditional trace saving based on test result
    trace_saved = False
    
    try:
        # Check if test failed
        if hasattr(request.node, 'rep_call') and request.node.rep_call.failed:
            # Generate unique trace filename
            test_name = request.node.name
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            trace_filename = f"{test_name}_{timestamp}.zip"
            trace_path = Path("traces") / trace_filename
            
            # Save trace
            context.tracing.stop(path=str(trace_path))
            trace_saved = True
            
            print(f"\n❌ Test FAILED - Trace saved: {trace_path}")
            print(f"   View with: playwright show-trace {trace_path}")
            
        else:
            # Test passed - discard trace to save storage
            context.tracing.stop()
            print(f"\n✅ Test PASSED - Trace discarded (saving storage)")
            
    except Exception as e:
        print(f"\n⚠️  Warning: Failed to save trace: {e}")
        context.tracing.stop()
    
    finally:
        context.close()


@pytest.fixture(scope="function")
def always_traced_context(browser: Browser, request: pytest.FixtureRequest) -> Generator[BrowserContext, None, None]:
    """
    Browser context that ALWAYS saves traces (useful for debugging).
    Use this when you want to inspect passing tests too.
    
    Args:
        browser: Playwright browser instance
        request: Pytest request object
    
    Yields:
        BrowserContext: Context with tracing enabled
    """
    context = browser.new_context(
        viewport={"width": 1920, "height": 1080}
    )
    
    context.tracing.start(screenshots=True, snapshots=True, sources=True)
    
    yield context
    
    # Always save trace
    test_name = request.node.name
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    trace_path = Path("traces") / f"{test_name}_{timestamp}.zip"
    
    context.tracing.stop(path=str(trace_path))
    print(f"\n📦 Trace saved: {trace_path}")
    
    context.close()


@pytest.fixture(scope="session")
def setup_trace_directory():
    """Ensure traces directory exists and is clean"""
    trace_dir = Path("traces")
    trace_dir.mkdir(exist_ok=True)
    print(f"\n📁 Trace directory ready: {trace_dir.absolute()}")
    return trace_dir
