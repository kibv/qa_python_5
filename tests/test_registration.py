import pytest
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from conftest import generate_email, generate_name
from locators import RegistrationPageLocators, MainPageLocators, LoginPageLocators

class TestRegistration:
    def fill_registration_form(self, driver, name, email, password):
        name_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(RegistrationPageLocators.NAME_FIELD))
        name_field.send_keys(name)

        email_field = driver.find_element(*RegistrationPageLocators.EMAIL_FIELD)
        email_field.send_keys(email)

        password_field = driver.find_element(*RegistrationPageLocators.PASSWORD_FIELD)
        password_field.send_keys(password)

    def test_successful_registration(self, driver):
        name = generate_name()
        email = generate_email()
        password = "validPassword123"

        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(MainPageLocators.LOGIN_BUTTON)
        ).click()

        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(MainPageLocators.REGISTER_LINK)
        ).click()

        self.fill_registration_form(driver, name, email, password)

        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(RegistrationPageLocators.REGISTER_BUTTON)
        ).click()

        try:
            WebDriverWait(driver, 10).until(EC.url_contains("/login"))

            WebDriverWait(driver, 5).until(
                EC.presence_of_element_located(LoginPageLocators.EMAIL_INPUT)
            )
            assert True
        except Exception as e:
            driver.save_screenshot("registration_failed.png")
            pytest.fail(f"Ошибка регистрации: {str(e)}")

    @pytest.mark.parametrize("invalid_password", ["12345", "qwert", "pass"])
    def test_invalid_password_registration(self, driver, invalid_password):
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(MainPageLocators.LOGIN_BUTTON)
        ).click()

        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(MainPageLocators.REGISTER_LINK)
        ).click()

        name = generate_name()
        email = generate_email()
        self.fill_registration_form(driver, name, email, invalid_password)

        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(RegistrationPageLocators.REGISTER_BUTTON)
        ).click()

        error = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located(RegistrationPageLocators.PASSWORD_ERROR)
        )
        assert error.text == "Некорректный пароль", "Неверное сообщение об ошибке"