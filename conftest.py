import pytest
from selene import browser
from selene.support.shared import config
from selenium import webdriver


@pytest.fixture(scope='function')
def setup_browser():
    config.browser_name = 'chrome'
    config.base_url = 'https://demoqa.com'
    config.timeout = 10
    config.window_width = 1600
    config.window_height = 1200

    driver_options = webdriver.ChromeOptions()
    driver_options.page_load_strategy = 'eager'
    driver_options.add_argument('--disable-notifications')
    driver_options.add_argument('--disable-popup-blocking')
    driver_options.add_argument('--disable-infobars')

    browser.config.driver_options = driver_options

    browser.driver.get(config.base_url)

    # Wait a bit for the page to stabilize
    import time
    time.sleep(1)

    # Remove the fixed banner if it exists
    browser.driver.execute_script("""
        var element = document.getElementById('fixedban');
        if (element) {
            element.remove();
        }

        // Also try to remove by class or other selectors if needed
        var banners = document.querySelectorAll('.fixedban, [class*="banner"], [id*="fixed"]');
        banners.forEach(function(el) {
            el.remove();
        });
    """)

