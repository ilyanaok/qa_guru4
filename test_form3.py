import os
import pytest
import time  # Добавлен импорт time
from selene import browser, be, have
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

    # Стратегия загрузки страницы:
    # 'normal' - ждать полной загрузки (по умолчанию)
    # 'eager' - ждать загрузки DOM, но не ресурсов (быстрее)
    # 'none' - не ждать вообще
    driver_options.page_load_strategy = 'eager'

    # Дополнительные опции для ускорения и стабильности
    driver_options.add_argument('--disable-notifications')
    driver_options.add_argument('--disable-popup-blocking')
    driver_options.add_argument('--disable-infobars')

    # Применяем настройки к браузеру
    browser.config.driver_options = driver_options

    # Открываем страницу с формой
    browser.open('/automation-practice-form')

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


def test_fill_form_simple(setup_browser):
    """Упрощенный тест"""
    # Только обязательные поля
    browser.element('#firstName').should(be.visible).type('Иляна')
    browser.element('#lastName').should(be.visible).type('Очирова')
    browser.element('#userEmail').should(be.visible).type('ilyana@example.com')
    browser.element('[for="gender-radio-2"]').should(be.visible).click()
    browser.element('#userNumber').should(be.visible).type('1234567890')
    browser.element('#currentAddress').should(be.visible).type('Moscow')

    # Скролл и отправка
    submit = browser.element('#submit').should(be.visible)
    browser.driver.execute_script("arguments[0].scrollIntoView(true);", submit())
    time.sleep(0.5)  # Теперь time импортирован

    # Лучше использовать стандартный клик вместо JS submit
    # browser.driver.execute_script("document.getElementById('userForm').submit();")
    submit.click()

    # Проверка
    browser.element('.modal-content').should(be.visible)
    print("✓ Форма отправлена")