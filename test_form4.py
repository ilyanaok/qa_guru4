import time
import os
from selene import browser, be, have


def test_fill_complete_form(setup_browser):
    """Полный тест формы с проверкой всех данных"""
    # Открыть форму
    browser.open('/automation-practice-form')

    # Заполнить личную информацию
    browser.element('#firstName').should(be.visible).type('Иляна')
    browser.element('#lastName').should(be.visible).type('Очирова')
    browser.element('#userEmail').should(be.visible).type('ilyana@example.com')
    browser.element('[for="gender-radio-2"]').should(be.visible).click()
    browser.element('#userNumber').should(be.visible).type('1234567890')

    # Выбрать дату рождения
    browser.element('#dateOfBirthInput').click()
    browser.element('.react-datepicker__month-select').type('May')
    browser.element('.react-datepicker__year-select').type('1990')
    browser.element('.react-datepicker__day--015').click()

    # Заполнить Subjects
    browser.element('#subjectsInput').type('Maths').press_enter()
    browser.element('#subjectsInput').type('Physics').press_enter()

    # Выбрать хобби
    browser.element('[for="hobbies-checkbox-2"]').should(be.visible).click()  # Reading
    browser.element('[for="hobbies-checkbox-3"]').should(be.visible).click()  # Music

    # Прикрепить файл
    file_path = os.path.abspath('test_picture.jpg')
    if not os.path.exists(file_path):
        with open(file_path, 'w') as f:
            f.write('test content')
    browser.element('#uploadPicture').send_keys(file_path)

    # Заполнить адрес
    browser.element('#currentAddress').should(be.visible).type('Moscow, Red Square, 1')

    # Выбрать штат и город
    browser.execute_script("window.scrollBy(0, 500)")
    browser.element('#state').click()
    browser.element('#react-select-3-option-0').should(be.visible).click()  # NCR
    browser.element('#city').click()
    browser.element('#react-select-4-option-0').should(be.visible).click()  # Delhi

    # Отправить форму
    browser.element('#submit').should(be.visible).click()

    # Проверить модальное окно
    browser.element('.modal-content').should(be.visible)
    browser.element('#example-modal-sizes-title-lg').should(have.text('Thanks for submitting the form'))

    # Проверить все данные
    browser.element('tbody tr:nth-child(1) td:nth-child(2)').should(have.text('Иляна Очирова'))
    browser.element('tbody tr:nth-child(2) td:nth-child(2)').should(have.text('ilyana@example.com'))
    browser.element('tbody tr:nth-child(3) td:nth-child(2)').should(have.text('Female'))
    browser.element('tbody tr:nth-child(4) td:nth-child(2)').should(have.text('1234567890'))
    browser.element('tbody tr:nth-child(5) td:nth-child(2)').should(have.text('15 May,1990'))
    browser.element('tbody tr:nth-child(6) td:nth-child(2)').should(have.text('Maths, Physics'))
    browser.element('tbody tr:nth-child(7) td:nth-child(2)').should(have.text('Reading, Music'))
    browser.element('tbody tr:nth-child(8) td:nth-child(2)').should(have.text('test_picture.jpg'))
    browser.element('tbody tr:nth-child(9) td:nth-child(2)').should(have.text('Moscow, Red Square, 1'))
    browser.element('tbody tr:nth-child(10) td:nth-child(2)').should(have.text('NCR Delhi'))

    print("✓ Форма успешно заполнена и все данные проверены")

    # Закрыть модальное окно
    browser.element('#closeLargeModal').click()