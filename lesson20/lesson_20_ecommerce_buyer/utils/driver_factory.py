"""
WebDriver Factory - Centralized driver initialization
Default: ChromeDriver only (no third-party driver manager).
ChromeDriver is used for every project; third-party managers are not used.
"""
import os
import shutil
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from typing import Literal


# Default ChromeDriver locations (checked in order; first found is used)
CHROMEDRIVER_PATHS = [
    os.path.expanduser("~/.wdm/drivers/chromedriver/linux64/144.0.7559.133/chromedriver-linux64/chromedriver"),
    "chromedriver",  # chromedriver on PATH
]


def _get_chromedriver_path() -> str:
    """Resolve ChromeDriver binary path. Uses ChromeDriver only (no third-party)."""
    for path in CHROMEDRIVER_PATHS:
        if path == "chromedriver":
            found = shutil.which("chromedriver")
            if found:
                return found
            continue
        if os.path.exists(path) and os.access(path, os.X_OK):
            return path
    raise FileNotFoundError(
        "ChromeDriver not found. Install ChromeDriver and ensure it is on PATH, "
        "or place it in ~/.wdm/drivers/chromedriver/... (this project uses ChromeDriver only, not third-party managers)."
    )


class DriverFactory:
    """Factory for creating WebDriver instances. Default is ChromeDriver only."""

    @staticmethod
    def create_driver(
        browser: Literal["chrome", "firefox"] = "chrome",
        headless: bool = False
    ) -> webdriver.Remote:
        """
        Create and configure WebDriver instance.
        Chrome: uses ChromeDriver only (default for every project).
        """
        if browser == "chrome":
            return DriverFactory._create_chrome_driver(headless)
        elif browser == "firefox":
            return DriverFactory._create_firefox_driver(headless)
        else:
            raise ValueError(f"Unsupported browser: {browser}")

    @staticmethod
    def _create_chrome_driver(headless: bool) -> webdriver.Chrome:
        """Create Chrome driver using ChromeDriver binary only (no third-party)."""
        options = ChromeOptions()

        if headless:
            options.add_argument("--headless=new")

        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-popup-blocking")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.set_capability("unhandledPromptBehavior", "accept")

        # ChromeDriver only: resolve binary path (no webdriver-manager / third-party)
        chromedriver_path = _get_chromedriver_path()
        service = ChromeService(chromedriver_path)

        # Chrome/Chromium binary for environments where default lookup fails
        for _path in ("/usr/bin/chromium-browser", "/usr/bin/chromium", "/opt/google/chrome/google-chrome", "/usr/bin/google-chrome"):
            if os.path.exists(_path):
                options.binary_location = _path
                break

        driver = webdriver.Chrome(service=service, options=options)
        driver.implicitly_wait(0)
        return driver

    @staticmethod
    def _create_firefox_driver(headless: bool) -> webdriver.Firefox:
        """Create Firefox driver (uses geckodriver from PATH or Selenium Manager)."""
        options = FirefoxOptions()
        if headless:
            options.add_argument("--headless")
        options.add_argument("--width=1920")
        options.add_argument("--height=1080")
        service = FirefoxService()  # No third-party: Selenium resolves geckodriver if needed
        driver = webdriver.Firefox(service=service, options=options)
        driver.implicitly_wait(0)
        return driver
