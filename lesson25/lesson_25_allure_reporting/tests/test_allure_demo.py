"""Test suite demonstrating Allure features"""
import pytest
import allure
from selenium.webdriver.common.by import By
from pages.login_page import LoginPage
import time


@allure.epic("E-Commerce Platform")
@allure.feature("Authentication")
class TestLogin:
    """Login functionality tests with Allure reporting"""
    
    @allure.story("Successful Login")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("User can login with valid credentials")
    @allure.description("""
        Test validates that a user with valid credentials can successfully
        log into the system and is redirected to the dashboard.
    """)
    @allure.tag("smoke", "authentication", "critical-path")
    def test_valid_login(self, driver):
        """Test successful login flow"""
        with allure.step("Navigate to login page"):
            driver.get("https://the-internet.herokuapp.com/login")
        
        with allure.step("Enter valid credentials"):
            login_page = LoginPage(driver)
            login_page.login("tomsmith", "SuperSecretPassword!")
        
        with allure.step("Verify successful login"):
            success_msg = driver.find_element(By.CLASS_NAME, "flash").text
            assert "You logged into a secure area!" in success_msg
            allure.attach(
                driver.get_screenshot_as_png(),
                name="successful_login",
                attachment_type=allure.attachment_type.PNG
            )
    
    @allure.story("Invalid Login")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Login fails with invalid credentials")
    @allure.tag("negative", "authentication")
    @pytest.mark.parametrize("username,password,expected_error", [
        ("invalid_user", "invalid_pass", "Your username is invalid!"),
        ("tomsmith", "wrong_password", "Your password is invalid!"),
    ], ids=["invalid_username", "invalid_password"])
    def test_invalid_login(self, driver, username, password, expected_error):
        """Test login failure scenarios"""
        with allure.step(f"Attempt login with {username}"):
            driver.get("https://the-internet.herokuapp.com/login")
            login_page = LoginPage(driver)
            login_page.login(username, password)
        
        with allure.step("Verify error message"):
            error_msg = driver.find_element(By.CLASS_NAME, "flash").text
            assert expected_error in error_msg
            allure.attach(
                f"Username: {username}, Password: {password}",
                name="test_data",
                attachment_type=allure.attachment_type.TEXT
            )


@allure.epic("E-Commerce Platform")
@allure.feature("UI Components")
class TestDynamicContent:
    """Tests for dynamic content loading"""
    
    @allure.story("Dynamic Loading")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Element appears after delay")
    @allure.tag("ui", "dynamic-content")
    def test_dynamic_loading(self, driver):
        """Test dynamic element loading"""
        with allure.step("Navigate to dynamic loading page"):
            driver.get("https://the-internet.herokuapp.com/dynamic_loading/2")
        
        with allure.step("Click start button"):
            start_button = driver.find_element(By.CSS_SELECTOR, "#start button")
            start_button.click()
        
        with allure.step("Wait for element to appear"):
            from selenium.webdriver.support.ui import WebDriverWait
            from selenium.webdriver.support import expected_conditions as EC
            
            element = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.ID, "finish"))
            )
            
            assert element.text == "Hello World!"
            allure.attach(
                driver.get_screenshot_as_png(),
                name="element_appeared",
                attachment_type=allure.attachment_type.PNG
            )
    
    @allure.story("Dynamic Loading")
    @allure.severity(allure.severity_level.MINOR)
    @allure.title("Performance test - element load time")
    @allure.tag("performance", "timing")
    def test_loading_performance(self, driver):
        """Measure dynamic content load time"""
        driver.get("https://the-internet.herokuapp.com/dynamic_loading/2")
        
        with allure.step("Measure load time"):
            start_time = time.time()
            
            start_button = driver.find_element(By.CSS_SELECTOR, "#start button")
            start_button.click()
            
            from selenium.webdriver.support.ui import WebDriverWait
            from selenium.webdriver.support import expected_conditions as EC
            
            WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.ID, "finish"))
            )
            
            load_time = time.time() - start_time
            
            # Attach performance data
            allure.attach(
                f"Load Time: {load_time:.2f} seconds",
                name="performance_metrics",
                attachment_type=allure.attachment_type.TEXT
            )
            
            # Performance assertion
            assert load_time < 7.0, f"Load time {load_time}s exceeded 7s threshold"


@allure.epic("E-Commerce Platform")
@allure.feature("Navigation")
class TestNavigation:
    """Navigation flow tests"""
    
    @allure.story("Multi-step Navigation")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("User can navigate through multiple pages")
    @allure.tag("navigation", "smoke")
    def test_multi_page_navigation(self, driver):
        """Test navigation across multiple pages"""
        pages = [
            ("Home", "https://the-internet.herokuapp.com/"),
            ("Checkboxes", "https://the-internet.herokuapp.com/checkboxes"),
            ("Dropdown", "https://the-internet.herokuapp.com/dropdown"),
        ]
        
        for page_name, url in pages:
            with allure.step(f"Navigate to {page_name}"):
                driver.get(url)
                assert url in driver.current_url
                time.sleep(0.5)  # Brief pause for stability
