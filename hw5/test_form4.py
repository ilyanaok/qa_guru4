import time
import os
from selene import browser, be, have, by
from selene import command

def test_fill_complete_form(setup_browser):
    browser.open('/automation-practice-form')
    # Удалить баннер (чистый JavaScript)
    browser.driver.execute_script("""
        var fixedban = document.getElementById('fixedban');
        if (fixedban) fixedban.remove();
    """)

    browser.element('#firstName').type('Иляна')
    browser.element('#lastName').type('Очирова')
    browser.element('#userEmail').type('ilyana@example.com')
    browser.element('[for="gender-radio-2"]').click()
    browser.element('#userNumber').type('1234567890')


    browser.element('#dateOfBirthInput').click()
    browser.element('.react-datepicker__month-select').type('May')
    browser.element('.react-datepicker__year-select').type('1990')
    browser.element('.react-datepicker__day--015').click()


    browser.element('#subjectsInput').type('Maths').press_enter()
    browser.element('#subjectsInput').type('Physics').press_enter()

    browser.element('[for="hobbies-checkbox-2"]').click()  # Reading
    browser.element('[for="hobbies-checkbox-3"]').click()  # Music

    browser.element('#uploadPicture').set_value(os.path.abspath('../test_picture.jpg'))

    browser.element('#currentAddress').type('Moscow, Red Square, 1')
    browser.element("#state").perform(command.js.scroll_into_view)
    time.sleep(0.5)
    browser.element("#state").click()
    browser.element(by.text('NCR')).click()
    browser.element("#city").click()
    browser.element(by.text('Delhi')).click()
    browser.element('#submit').click()

    browser.element('.modal-content').should(be.visible)
    browser.element('#example-modal-sizes-title-lg').should(have.text('Thanks for submitting the form'))

    browser.element('.table-responsive').should(have.text('Иляна Очирова'))
    browser.element('.table-responsive').should(have.text('ilyana@example.com'))
    browser.element('.table-responsive').should(have.text('Female'))
    browser.element('.table-responsive').should(have.text('1234567890'))
    browser.element('.table-responsive').should(
        have.text('Date of Birth 15 May,1990'))
    browser.element('.table-responsive').should(have.text('Maths'))
    browser.element('.table-responsive').should(have.text('Physics'))
    browser.element('.table-responsive').should(have.text('Reading'))
    browser.element('.table-responsive').should(have.text('Music'))
    browser.element('.table-responsive').should(have.text('test_picture.jpg'))
    browser.element('.table-responsive').should(have.text('Moscow, Red Square, 1'))
    browser.element('.table-responsive').should(have.text('NCR Delhi'))

    print("✓ Форма успешно заполнена и все данные проверены")

    # Закрыть модальное окно
    browser.element('#closeLargeModal').click()