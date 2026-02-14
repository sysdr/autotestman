"""
test_locator_strategy.py - Comprehensive locator strategy tests
"""

import pytest
from selenium.common.exceptions import NoSuchElementException
from pages.demo_page import DemoPage
from utils.metrics import MetricsCollector, LocatorMetric


class TestLocatorStrategy:
    """Test suite demonstrating different locator strategies"""
    
    @pytest.fixture(autouse=True)
    def setup(self, chrome_driver, test_page_url):
        """Setup page object for each test"""
        self.page = DemoPage(chrome_driver, test_page_url)
        self.page.load()
        self.metrics_collector = MetricsCollector()
    
    def test_locate_by_id(self):
        """Test locating element by ID - fastest and most stable"""
        strategy = self.page.LOCATORS["by_id"]
        
        try:
            element, elapsed_time = self.page.find_button_with_strategy("by_id")
            
            assert element is not None
            assert element.text == "Submit Order"
            assert elapsed_time < 0.1, f"ID lookup took {elapsed_time}s (should be < 0.1s)"
            
            metric = LocatorMetric(
                strategy_name=strategy.name,
                locator_type=strategy.type.value,
                locator_value=strategy.value,
                execution_time=elapsed_time,
                success=True,
                risk_level=strategy.risk_level
            )
            self.metrics_collector.add_metric(metric)
            
            print(f"\n✓ {strategy.name}: {elapsed_time:.4f}s [FASTEST]")
            
        except Exception as e:
            pytest.fail(f"Failed to locate by ID: {e}")
    
    def test_locate_by_class(self):
        """Test locating element by class name - medium risk"""
        strategy = self.page.LOCATORS["by_class"]
        
        try:
            element, elapsed_time = self.page.find_button_with_strategy("by_class")
            
            assert element is not None
            assert element.text == "Submit Order"
            
            metric = LocatorMetric(
                strategy_name=strategy.name,
                locator_type=strategy.type.value,
                locator_value=strategy.value,
                execution_time=elapsed_time,
                success=True,
                risk_level=strategy.risk_level
            )
            self.metrics_collector.add_metric(metric)
            
            print(f"\n🟡 {strategy.name}: {elapsed_time:.4f}s [MEDIUM RISK]")
            print(f"   Warning: Class 'btn-primary' might be used multiple times")
            
        except Exception as e:
            pytest.fail(f"Failed to locate by class: {e}")
    
    def test_locate_by_css(self):
        """Test locating element by CSS selector - recommended approach"""
        strategy = self.page.LOCATORS["by_css_attribute"]
        
        try:
            element, elapsed_time = self.page.find_button_with_strategy("by_css_attribute")
            
            assert element is not None
            assert element.text == "Submit Order"
            assert elapsed_time < 0.1, f"CSS lookup took {elapsed_time}s (should be < 0.1s)"
            
            metric = LocatorMetric(
                strategy_name=strategy.name,
                locator_type=strategy.type.value,
                locator_value=strategy.value,
                execution_time=elapsed_time,
                success=True,
                risk_level=strategy.risk_level
            )
            self.metrics_collector.add_metric(metric)
            
            print(f"\n✓ {strategy.name}: {elapsed_time:.4f}s [RECOMMENDED]")
            
        except Exception as e:
            pytest.fail(f"Failed to locate by CSS: {e}")
    
    def test_locate_by_xpath_text(self):
        """Test locating element by XPath with text - slower but useful"""
        strategy = self.page.LOCATORS["by_xpath_text"]
        
        try:
            element, elapsed_time = self.page.find_button_with_strategy("by_xpath_text")
            
            assert element is not None
            assert "Submit" in element.text
            
            metric = LocatorMetric(
                strategy_name=strategy.name,
                locator_type=strategy.type.value,
                locator_value=strategy.value,
                execution_time=elapsed_time,
                success=True,
                risk_level=strategy.risk_level
            )
            self.metrics_collector.add_metric(metric)
            
            print(f"\n🟡 {strategy.name}: {elapsed_time:.4f}s [SLOWER]")
            print(f"   Note: XPath is ~3x slower than CSS for simple queries")
            
        except Exception as e:
            pytest.fail(f"Failed to locate by XPath text: {e}")
    
    def test_locate_by_xpath_absolute(self):
        """Test locating element by absolute XPath - ANTI-PATTERN"""
        strategy = self.page.LOCATORS["by_xpath_absolute"]
        
        try:
            element, elapsed_time = self.page.find_button_with_strategy("by_xpath_absolute")
            
            assert element is not None
            
            metric = LocatorMetric(
                strategy_name=strategy.name,
                locator_type=strategy.type.value,
                locator_value=strategy.value,
                execution_time=elapsed_time,
                success=True,
                risk_level=strategy.risk_level
            )
            self.metrics_collector.add_metric(metric)
            
            print(f"\n🔴 {strategy.name}: {elapsed_time:.4f}s [ANTI-PATTERN]")
            print(f"   ⚠️  WARNING: Absolute XPath will break with any DOM change!")
            print(f"   ⚠️  Never use this in production code!")
            
        except NoSuchElementException:
            # This is actually expected if the DOM structure doesn't match exactly
            print(f"\n🔴 {strategy.name}: FAILED (as expected)")
            print(f"   This demonstrates why absolute XPath is fragile")
    
    def test_compare_all_strategies(self, chrome_driver, test_page_url):
        """Comprehensive test comparing all locator strategies"""
        page = DemoPage(chrome_driver, test_page_url)
        page.load()
        
        collector = MetricsCollector()
        
        print("\n" + "="*70)
        print("RUNNING COMPREHENSIVE LOCATOR COMPARISON")
        print("="*70)
        
        for strategy_key, strategy in page.LOCATORS.items():
            try:
                element, elapsed_time = page.find_button_with_strategy(strategy_key)
                
                metric = LocatorMetric(
                    strategy_name=strategy.name,
                    locator_type=strategy.type.value,
                    locator_value=strategy.value,
                    execution_time=elapsed_time,
                    success=True,
                    risk_level=strategy.risk_level
                )
                collector.add_metric(metric)
                
            except Exception as e:
                metric = LocatorMetric(
                    strategy_name=strategy.name,
                    locator_type=strategy.type.value,
                    locator_value=strategy.value,
                    execution_time=0.0,
                    success=False,
                    error_message=str(e),
                    risk_level=strategy.risk_level
                )
                collector.add_metric(metric)
        
        # Print the full report
        print(collector.generate_report())
        
        # Assertions
        fastest = collector.get_fastest()
        assert fastest is not None, "No successful locators found"
        assert fastest.execution_time < 0.2, "Even fastest locator is too slow"


def test_visual_demo():
    """
    Standalone test that can be run with browser visible.
    Run with: pytest tests/test_locator_strategy.py::test_visual_demo --no-headless
    """
    from selenium import webdriver
    from pathlib import Path
    import time
    
    # Use visible browser
    driver = webdriver.Chrome()
    
    try:
        html_file = Path(__file__).parent.parent / "html" / "test_page.html"
        page = DemoPage(driver, f"file://{html_file.absolute()}")
        page.load()
        
        print("\n" + "="*70)
        print("VISUAL DEMO: Watch the browser locate and click the button")
        print("="*70 + "\n")
        
        # Demonstrate each strategy with visible browser
        strategies_to_demo = ["by_id", "by_css_attribute", "by_xpath_text"]
        
        for strategy_key in strategies_to_demo:
            strategy = page.LOCATORS[strategy_key]
            print(f"Testing: {strategy.name}")
            print(f"Locator: {strategy.value}")
            
            element, elapsed_time = page.find_button_with_strategy(strategy_key)
            
            # Highlight the element
            driver.execute_script(
                "arguments[0].style.border='3px solid red'", element
            )
            time.sleep(1)
            
            # Click it
            element.click()
            time.sleep(1)
            
            # Reset for next demo
            driver.execute_script(
                "arguments[0].style.border=''", element
            )
            driver.execute_script(
                "document.getElementById('result').style.display='none'"
            )
            
            print(f"✓ Success in {elapsed_time:.4f}s\n")
            time.sleep(0.5)
        
        print("Demo complete! Browser will close in 3 seconds...")
        time.sleep(3)
        
    finally:
        driver.quit()
