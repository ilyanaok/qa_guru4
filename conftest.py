import pytest
from selene import browser
from selene.support.shared import config
from selenium import webdriver


@pytest.fixture(scope='function')
def setup_browser():
    """Настройка браузера перед каждым тестом"""
    # Конфигурация Selene
    config.browser_name = 'chrome'
    config.base_url = 'https://demoqa.com'
    config.timeout = 10
    config.window_width = 1600
    config.window_height = 1200

    # Настройки Chrome Driver
    driver_options = webdriver.ChromeOptions()
    driver_options.page_load_strategy = 'eager'
    driver_options.add_argument('--disable-notifications')
    driver_options.add_argument('--disable-popup-blocking')
    driver_options.add_argument('--disable-infobars')

    # Применяем настройки к браузеру chrome
    browser.config.driver_options = driver_options

    # Убираем мешающие элементы (рекламу, футер)
    browser.execute_script("""
        const footer = document.querySelector('footer');
        if (footer) footer.style.display = 'none';
        const fixedban = document.getElementById('fixedban');
        if (fixedban) fixedban.style.display = 'none';
    """)

    yield

    # Закрываем браузер после теста
    browser.quit()