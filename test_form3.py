# test.py - с настройкой page_load_strategy
import os
import pytest
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


def test_fill_form_with_minimal_data(setup_browser):
    """Тест 1: Заполнение формы минимальными обязательными данными"""
    # Заполняем обязательные поля
    browser.element('#firstName').should(be.visible).type('Иляна')
    browser.element('#lastName').type('Очирова')
    browser.element('#userEmail').type('ilyana@example.com')

    # Выбираем пол (Male)
    browser.element('[for="gender-radio-2"]').click()

    # Заполняем номер телефона
    browser.element('#userNumber').type('1234567890')

    # Дополнительное поле даты рождения (опционально)
    # browser.element('#dateOfBirthInput').click()
    # browser.element('.react-datepicker__month-select').click()
    # browser.element('.react-datepicker__month-select option[value="0"]').click()
    # browser.element('.react-datepicker__year-select').click()
    # browser.element('.react-datepicker__year-select option[value="1990"]').click()
    # browser.element('.react-datepicker__day--001:not(.react-datepicker__day--outside-month)').click()

    # Хобби (опционально)
    # browser.element('[for="hobbies-checkbox-1"]').click()

    # Адрес (опционально, но рекомендуется)
    browser.element('#currentAddress').type('Moscow region')

    # Скроллим к кнопке (исправленная версия)
    submit_button = browser.element('#submit')
    browser.driver.execute_script("arguments[0].scrollIntoView(true);", submit_button())

    # Ждем немного чтобы кнопка стала активной после скролла
    import time
    time.sleep(0.5)

    # Отправляем форму
    submit_button.click()

    # Проверяем что появилось модальное окно с результатами
    browser.element('.modal-content').should(be.visible)

    # Ждем появления заголовка модального окна
    browser.element('#ex9ample-modal-sizes-title-lg').should(be.visible)

    # Проверяем что имя отображается правильно
    browser.all('tbody tr')[0].element('td:nth-child(2)').should(have.text('Иван Иванов'))

    # Проверяем email
    browser.all('tbody tr')[1].element('td:nth-child(2)').should(have.text('ivan@example.com'))

    # Проверяем пол
    browser.all('tbody tr')[2].element('td:nth-child(2)').should(have.text('Male'))

    # Проверяем телефон
    browser.all('tbody tr')[3].element('td:nth-child(2)').should(have.text('1234567890'))

    # Закрываем модальное окно
    browser.element('#closeLargeModal').click()

    print("✓ Тест пройден успешно")


if __name__ == '__main__':
    pytest.main(['-v', '-s'])